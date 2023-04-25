import os
import stat
import shutil
from shutil import copyfile
import re



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

def test(srcpath,dstpath):
    # 先把上一次测试的文件删除，再进行本次测试
    del_file(os.path.join(dstpath, "test"))
    del_file(os.path.join(dstpath, "contracts"))
    del_file(os.path.join(dstpath,"coverage","contracts"))
    # 将待测文件复制到对应文件夹中
    for file_name in os.listdir(srcpath):
        # 如果是测试文件就放到test文件夹下
        if os.path.isdir(os.path.join(srcpath, file_name)):
            continue
        if file_name.find(".js") != -1:
            copyfile(os.path.join(srcpath, file_name), os.path.join(dstpath, "test", file_name))
        else:
            # 如果是sol文件就放到contract文件夹下，并打开sol文件读取对应的solidity版本
            copyfile(os.path.join(srcpath, file_name), os.path.join(dstpath, "contracts", file_name))
            op_file = open(os.path.join(srcpath, file_name), "r")
            lines = op_file.readlines()
            version = ""
            for line in lines:
                # 找到版本
                if line.find("pragma solidity") != -1:
                    version = findversion(line)
                    break
            config_file = open(os.path.join(dstpath, "hardhat.config.js"), "r")
            lines = config_file.readlines()
            config_file.close()
            config_file = open(os.path.join(dstpath, "hardhat.config.js"), "w")
            i = 0
            while i < len(lines):
                if lines[i].find("solidity") != -1:
                    lines[i] = "  solidity: \"" + version + "\",\n"
                    break
                i += 1
            config_file.writelines(lines)
            config_file.close()

# 得到event中的数据
os.chdir("/home/liu/Tool/a")
strs = os.popen("npx hardhat test").read()
tmp = strs[:strs.find("✔")].strip()
print("+++++++++++" + tmp + "+++++++++++")

teststr = "const filter = { \n\t address:_contract.address, \n\t topic:[ethers.utils.id('')]\n};" \
          "const events = await _contract.provider.getLogs(filter);\n" \
          "const parseEvents = events.map((event)=>_contract.interface.parseLog(event));\n" \
          "for(var i = 0;i < parseEvents.length;i++){\n" \
          "\tif(parseEvents[i].name == \"testtestglobal\"){\n" \
          "\t\tfor(var j = 0;j < parseEvents[i].args.length;j ++){\n" \
          "\t\t\tconsole.log('',parseEvents[i].args[j]);\n" \
          "\t\t}\n\t}\n" \
          "\tif(parseEvents[i].name == \"testtestlocal\"){\n" \
          "\t\tfor(var j = 0;j < parseEvents[i].args.length;j ++){\n" \
          "\t\t\tconsole.log('',parseEvents[i].args[j]);\n" \
          "\t\t}\n\t}\n}\n"


