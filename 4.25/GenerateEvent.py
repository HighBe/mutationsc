import json


def generateEvent(solpath,astpath):
    sol_file = open(solpath,"r")
    ast_file = open(astpath,"r")
    data = json.load(ast_file)
    lines = sol_file.readlines()
    sol_file.close()
    contractname = solpath.rsplit("/",1)[1]
    #几种无法继续测试的情况，直接测试下一个合约
    if "contracts/"+contractname not in data["output"]["sources"]:
        print("compile failed~")
        return False
    if 'ast' not in data["output"]["sources"]["contracts/"+contractname]:
        return False
    nodes = data["output"]["sources"]["contracts/"+contractname]["ast"]["nodes"]
    globalname = []
    globaltype = []
    localname = []
    localtype = []
    for node in nodes:
        # 找到contract的节点
        if "contractKind" in node and node["contractKind"] == "contract":
            contractname = node["name"]
            #在每个合约中把之前的全局变量都清空
            globaltype.clear()
            globalname.clear()
            # 找到定义的全局变量
            for snode in node["nodes"]:
                # 找到定义变量的语句 ,并判断是否是以storage形式存储
                if snode["nodeType"] == "VariableDeclaration" and snode["typeName"]["nodeType"] == "ElementaryTypeName" and snode["storageLocation"] == "default":
                    if "pathNode" in snode["typeName"]:
                        globaltype.append(snode["typeName"]["pathNode"]["name"])
                    else:
                        globaltype.append(snode["typeDescriptions"]["typeString"])
                    globalname.append(snode["name"])
            #生成全局变量的event
            globalevent = ""
            globalemit = ""
            if len(globaltype) > 0:
                globalevent = "    event testtestglobal(" + str(globaltype[0]) + " " + str(globalname[0])
                globalemit = "    emit testtestglobal(" + str(globalname[0])
                i = 1
                while i < len(globaltype):
                    globalevent = globalevent + "," + str(globaltype[i]) + " " + str(globalname[i])
                    globalemit = globalemit + "," + str(globalname[i])
                    i += 1
                globalevent += ");"
                globalemit += ");"
            #写入全局变量的event的定义
            j = 0
            while j < len(lines) and len(globaltype) > 0:
                if lines[j].find("contract " + contractname) != -1:
                    tmp = lines[j]
                    last = tmp.find("{")
                    tmp = tmp[:last+1] + "\n" + globalevent + tmp[last+1:]
                    lines[j] = tmp
                    break
                j += 1

            #找每一个函数中的局部变量，并在每一个函数中新增两个event，一个记录全局变量，一个记录局部变量
            for snode in node["nodes"]:
                #找到函数,并且不能是 pure或view类型的函数
                if snode["nodeType"] == "FunctionDefinition" and 'kind' in snode and snode["kind"] != "constractor" and \
                        'body' in snode and snode['body'] != None and 'statements' in snode['body']  and snode["body"]["statements"] != False \
                        and snode["stateMutability"] != "view" and snode["stateMutability"] != "pure":
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
                                if decl != None and decl["nodeType"] == "VariableDeclaration" and decl["typeName"]["nodeType"] == "ElementaryTypeName" and decl["storageLocation"] == "storage":
                                    if "pathNode" in decl["typeName"]:
                                        localtype.append(decl["typeName"]["pathNode"]["name"])
                                    else :
                                        localtype.append(decl["typeDescriptions"]["typeString"])
                                    localname.append(decl["name"])
                    #生成局部变量的event
                    if len(localtype) > 0:
                        localevent = "    event testtestlocal(" + str(localtype[0]) + " " + str(localname[0])
                        localemit = "    emit testtestlocal(" + str(localname[0])
                        i = 1
                        while i < len(localtype):
                            localevent = localevent +  "," + str(localtype[i]) + " " + str(localname[i])
                            localemit = localemit + "," + str(localname[i])
                            i += 1
                        localevent += ");"
                        localemit += ");"
                    funcname = snode["name"]
                    #如果没有全局变量和局部变量，就跳过，找下一个函数
                    if len(localtype) == 0 and len(globaltype) == 0:
                        continue
                    j = 0
                    while j < len(lines) and len(localtype) > 0:
                        if lines[j].find("contract " + contractname) != -1:
                            tmp = lines[j]
                            last = tmp.find("{")
                            tmp = tmp[:last] + "\n" + localevent + '\n' + tmp[last:]
                            lines[j] = tmp
                            break
                        j += 1


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
                                #找到return
                                if lines[j].find("return") and len(funcname) != 0 and lines[j].find("return") > lines[j].find("{"):
                                    last = lines[j].find("return")
                                    tempstr = lines[j][:last - 1]
                                    # 如果有符合条件的全局变量
                                    if len(globaltype) > 0:
                                        tempstr += "\n" + globalemit + "\n"
                                    # 如果局部变量中有以storage形式存储的变量
                                    if len(localtype) > 0:
                                        tempstr += localemit + "\n"
                                    tempstr += lines[j][last:]
                                    lines[j] = tempstr
                                    break
                                #找到最后一个右括号
                                if countleft == countright and len(funcname) != 0:
                                    last = lines[j].rfind('}')
                                    tempstr = lines[j][:last-1]
                                    #如果有符合条件的全局变量
                                    if len(globaltype) > 0:
                                        tempstr += "\n" + globalemit + "\n"
                                    #如果局部变量中有以storage形式存储的变量
                                    if len(localtype) > 0:
                                        tempstr += localemit + "\n"
                                    tempstr += lines[j][last:]
                                    lines[j] = tempstr
                                    break
                                j += 1
                            break
                        j += 1
    sol_file = open(solpath,"w")
    sol_file.writelines(lines)





