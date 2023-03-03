import os
import stat
import randomdeletion
from shutil import copyfile
import shutil
import re
import  MuKeyWord

hardhat_workspace = "/home/liu/Tool/a"

def testAllFiles(srcpath,hardhatpath):
    ls = os.listdir(srcpath)
    i = 731
    while i < len(ls):
        src_path = os.path.join(srcpath,ls[i])
        randomDeleteTest(src_path,hardhatpath)
        i += 1
        print("++++++++++++++++++++"+str(i)+"++++++++++++++++++++++")
    # for dir in ls:
    #     src_path = os.path.join(srcpath,dir)
    #     randomDeleteTest(src_path,hardhatpath)

def del_file(path):
    ls = os.listdir(path)
    for file in ls:
        c_path = os.path.join(path,file)
        if os.path.isdir(c_path):
            del_file(c_path)
        else:
            os.chmod(c_path,stat.S_IRWXO)
            os.remove(c_path)

def findversion(input_str):
    if input_str.find(">") == -1 and input_str.find("<") == -1:
        start = input_str.find("0")
        end = input_str.find(";")
        version = input_str[start:end]
        return version
    match = re.search(r">=?(?P<major>\d+)\.(?P<minor>\d+)\.(?P<patch>\d+)\s*(?:<|<=|>|>=)?",input_str)
    if match:
        version = match.group('major')+'.'+match.group('minor')+'.'+match.group('patch')
        return version

def randomDeleteTest(srcpath,dstpath):
    # 先把上一次测试的文件删除，再进行本次测试
    del_file(os.path.join(dstpath,"test"))
    del_file(os.path.join(dstpath,"contracts"))
    del_file(os.path.join(dstpath,"coverage","contracts"))
    #将待测文件复制到对应文件夹中
    for file_name in os.listdir(srcpath):
        #如果是测试文件就放到test文件夹下
        if os.path.isdir(os.path.join(srcpath,file_name)):
            continue
        if file_name.find(".js") !=-1:
            copyfile(os.path.join(srcpath,file_name),os.path.join(dstpath,"test",file_name))
        else:
            #如果是sol文件就放到contract文件夹下，并打开sol文件读取对应的solidity版本
            copyfile(os.path.join(srcpath, file_name), os.path.join(dstpath, "contracts", file_name))
            op_file = open(os.path.join(srcpath,file_name),"r")
            lines = op_file.readlines()
            version = ""
            for line in lines:
                #找到版本
                if line.find("pragma solidity") != -1:
                    version = findversion(line)
                    break
            config_file = open(os.path.join(dstpath,"hardhat.config.js"),"r")
            lines = config_file.readlines()
            config_file.close()
            config_file = open(os.path.join(dstpath,"hardhat.config.js"),"w")
            i = 0
            while i < len(lines):
                if lines[i].find("solidity") != -1:
                    lines[i] = "  solidity: \"" + version+ "\",\n"
                    break
                i += 1
            config_file.writelines(lines)
            config_file.close()



    #命令行运行，生成coverage文件,并保存返回值
    os.chdir(hardhat_workspace)
    result_origin = os.system("npx hardhat coverage --temp build")

    #将生成的coverage文件复制到待测文件所在文件夹保存，并重命名
    if os.path.exists(os.path.join(srcpath,"coverage_origin")):
        shutil.rmtree(os.path.join(srcpath,"coverage_origin"))
    shutil.copytree(os.path.join(dstpath,"coverage"),os.path.join(srcpath,"coverage_origin"))

    #将contract文件夹中的文件进行修改
    #找到生成的包含coverage信息的html文件

    ls = os.listdir(os.path.join(dstpath,"contracts"))
    src_path = os.path.join(srcpath,ls[0])
    html_path = os.path.join(srcpath, "coverage_origin", "contracts", ls[0]+".html")
    print(html_path,src_path)

    #随机修剪十次
    j = 0
    for j in range(0,1):
        del_file(os.path.join(dstpath, "contracts"))
        del_file(os.path.join(dstpath, "coverage", "contracts"))
        if os.path.isfile(html_path) == False:
            print("compile failed")
            return
        #随机删除
        randomdeletion.FindNoCoverage(html_path,src_path,os.path.join(dstpath,'contracts'),j)
        #随机修改关键词
        # MuKeyWord.mutateSC(src_path,)

        #再次运行hardhat对比两次命令行结果，如果两次结果不同，则对该次修改进行保存
        result_new = os.system("npx hardhat coverage --temp build")
        if os.path.exists(os.path.join(srcpath, "new")) and j == 0:
            shutil.rmtree(os.path.join(srcpath, "new"))
        if result_new != result_origin:
            print("-------------------------------------------------------------------------------------------------")
            if os.path.isdir(os.path.join(srcpath,"new")) == False:
                os.mkdir(os.path.join(srcpath,"new"))
            ls = os.listdir(os.path.join(dstpath,"contracts"))
            # newname = ls[0].split(".",1)[0]+"1"+".sol"
            # os.rename(os.path.join(dstpath,"contracts",ls[0]),os.path.join(dstpath,"contracts",newname))
            copyfile(os.path.join(dstpath,"contracts",ls[0]),os.path.join(srcpath,"new",ls[0]))

