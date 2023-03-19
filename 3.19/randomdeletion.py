import os
import random
import json
# 第一个参数是生成的覆盖率文件所在位置，第二个参数是对应的源文件所在的位置,第三个参数是目标文件夹目前没用

#用来判断括号匹配，防止删除一半括号
def isMatch(str):
    symbol = {')':'(',']':'[','}':'{'}
    Save = []
    for i in str:
        if i in symbol:
            if len(Save) == 0:
                return False
            if Save[-1] == symbol[i]:
                Save.pop()
            else:
                return False
        if i == '(' or i == '[' or i == '{':
            Save.append(i)
    return not Save

#通过编译生成的ast，寻找继承的合约，interface,struct等生成自己定义的变量
def findDefination(astpath,solname):
    astls = os.listdir(astpath)
    fp = open(os.path.join(astpath,astls[0]),"r")
    data = json.load(fp)
    solname = "contracts/" + solname
    def_list = ["function","int","bool","bytes","_;","address","if","else","string","return","var","try","catch","event","emit"]
    contractnodes = data["output"]["sources"][solname]["ast"]["nodes"]
    for ls in contractnodes:
        if ls["nodeType"] == "ContractDefinition":
            def_list.append(ls["name"])
        if "nodes" not in ls:
            continue
        for nodels in ls["nodes"]:
            if nodels["nodeType"] == "StructDefinition":
                def_list.append(nodels["name"])


    return def_list


def FindNoCoverage(htmlpath,solpath,dstpath,astpath,j):
    filehtml = open(htmlpath,'r')
    lines = filehtml.readlines()
    filesol= open(solpath,"r+")
    solline = filesol.readlines()
    flag = 0 #用来判断是否到了标记覆盖率的代码
    counts = [] #记录没有覆盖的行数
    count = 0 #记录当前是在第几行
    solname = solpath.rsplit('/',1)[-1]
    #存储用来定义的关键词
    def_list = findDefination(astpath,solname)

    #查找没有覆盖的行数
    for line in lines:
        #找到记录覆盖率代码的开始位置
        if flag == 0 and line.find("line-coverage") != -1:
            flag = 1
        #找到记录代码覆盖率的结束位置
        if flag == 1 and line.find("span") == -1:
            flag = 0
        #记录是在第多少行
        if flag == 1:
            count += 1
        #找到没有覆盖的行数
        # if flag == 1 and line.find("cline-no") != -1 and solline[count-1].find("function") == -1 and solline[count-1].find("int") == -1\
        #         and solline[count-1].find("bool") == -1 and solline[count-1].find("bytes") == -1 and solline[count-1].find("_;") == -1\
        #         and solline[count-1].find("address") == -1 and solline[count-1].find("if") == -1 and solline[count-1].find("else") == -1\
        #         and solline[count-1].find("string") == -1 and solline[count-1].find("return") == -1 and solline[count-1].find("var") == -1\
        #         and solline[count-1].find("try") == -1 and solline[count-1].find("catch") == -1:

        if flag == 1 and line.find("cline-no") != -1:
            def_flag = 0
            if solline[count-1].find(";") == -1:
                def_flag = 1
            for i in def_list:
                if solline[count-1].find(i) != -1:
                    def_flag = 1
                    break
            if def_flag == 0 and isMatch(solline[count-1]) == True:
                counts.append(count)

    #随机删除没有覆盖的行数
    if len(counts) == 0:
        print("All Covergae")
        return
    delnum = random.randint(1,len(counts))#随机确定需要删除的行数
    dellines = random.sample(counts,delnum) #随机选择上面数量的需要删除第几行
    #删除上面随机选择出的行
    #遍历需要删除的行数进行删除操作
    for delline in dellines:
        tmp = solline[delline-1]
        solline[delline-1] = "//" + tmp #在需要删除的行前面加注释，相当于删除

    #写到目标文件
    dstfile = open(dstpath + "/" + solpath.rsplit('/',1)[-1].split('.',1)[0]+str(j)+'.sol',"w+")
    dstfile.writelines(solline)
    #写回原文件
    # filesol = open(solpath,"w+")
    # filesol.writelines(solline)



    #输出删除一共多少行和分别是哪几行
    # print(str(delnum) + " " + str(dellines))



