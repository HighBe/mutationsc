import json


def generateEvent(solpath,astpath):
    sol_file = open(solpath,"r")
    ast_file = open(astpath,"r")
    data = json.load(ast_file)
    lines = sol_file.readlines()
    sol_file.close()
    contractname = solpath.rsplit("/",1)[1]
    nodes = data["output"]["sources"]["contracts/"+contractname]["ast"]["nodes"]
    globalname = []
    globaltype = []
    localname = []
    localtype = []
    for node in nodes:
        #找到contract的节点
        if "contractKind" in node and node["contractKind"] == "contract":
            contractname = node["name"]
            #找到定义的全局变量
            for snode in node["nodes"]:
                #找到定义变量的语句
                if snode["nodeType"] == "VariableDeclaration" and snode["typeName"]["nodeType"] == "ElementaryTypeName":
                        globaltype.append(snode["typeName"]["name"])
                        globalname.append(snode["name"])
            #生成全局变量的event
            globalevent = ""
            globalemit =""
            if len(globaltype) > 0:
                globalevent = "    event testtestglobal(" + str(globaltype[0]) + " " + str(globalname[0])
                globalemit = "    emit testtestglobal(" + str(globaltype[0]) + " " + str(globalname[0])
                i = 1
                while i < len(globaltype):
                    globalevent = globalevent +  "," + str(globaltype[i]) + " " + str(globalname[i])
                    globalemit =  globalemit + "," + str(globaltype[i]) + " " + str(globalname[i])
                    i += 1
                globalevent += ");"
                globalemit += ");"
            #找每一个函数中的局部变量，并在每一个函数中新增两个event，一个记录全局变量，一个记录局部变量
            for snode in node["nodes"]:
                #找到函数
                if snode["nodeType"] == "FunctionDefinition" and snode["kind"] != "constractor" and snode["body"]["statements"] != False:
                    localevent = ""
                    localemit = ""
                    #每一个statements中的node都是一条语句
                    for statenode in snode["body"]["statements"]:
                        if "declarations" in statenode:
                            #有局部变量的定义
                            #在每个函数中把之前记录的局部变量清空
                            localtype.clear()
                            localname.clear()
                            for decl in statenode["declarations"]:
                                if decl["nodeType"] == "VariableDeclaration" and decl["typeName"]["nodeType"] == "ElementaryTypeName":
                                    localtype.append(decl["typeName"]["name"])
                                    localname.append(decl["name"])
                    #生成局部变量的event
                    if len(localtype) > 0:
                        localevent = "    event testtestlocal(" + str(localtype[0]) + " " + str(localname[0])
                        localemit = "    emit testtestlocal(" + str(localtype[0]) + " " + str(localname[0])
                        i = 1
                        while i < len(localtype):
                            localevent = localevent +  "," + str(localtype[i]) + " " + str(localname[i])
                            localemit = localemit + "," + str(localtype[i]) + " " + str(localname[i])
                            i += 1
                        localevent += ");"
                        localemit += ");"
                    funcname = snode["name"]
                    #如果没有全局变量和局部变量，就跳过，找下一个函数
                    if len(localtype) == 0 and len(globaltype) == 0:
                        continue
                    #要找到对应合约中的对应函数，在函数中插入event语句
                    contractflag = 0
                    j = 0
                    while j < len(lines):
                        if lines[j].find("contract " + contractname) != -1:
                            contractflag = 1
                        #找到对应的函数
                        if lines[j].find("function " + funcname) != -1 and contractflag == 1:
                            #进行括号匹配，找到函数最后一个右大括号，在这前面插入event语句
                            countleft = 0
                            countright = 0
                            while j < len(lines):
                                countleft += lines[j].count('{')
                                countright += lines[j].count('}')
                                if lines[j].find("return") and len(funcname) != 0:
                                    last = lines[j].find("return")
                                    lines[j] = lines[j][:last - 1] + "\n" + globalevent + "\n" + globalemit + "\n" \
                                               + localevent + "\n" + localemit + "\n" + lines[j][last:]
                                    break
                                #找到最后一个右括号
                                if countleft == countright and len(funcname) != 0:
                                    last = lines[j].rfind('}')
                                    lines[j] = lines[j][:last-1] + "\n" + globalevent + "\n" + globalemit + "\n"\
                                    + localevent + "\n" + localemit + "\n" + lines[j][last:]
                                    break
                                j += 1
                            break
                        j += 1
    sol_file = open(solpath,"w")
    sol_file.writelines(lines)





