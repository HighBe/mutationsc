import random

#使用随机数来决定是否对关键词进行变异
def rr():
    #return True
    if random.randint(0,1) == 1:
        return True
    else:
        return False

def mutateSC(pathsrc,dstpath,j):
    file = open(pathsrc,"r")
    mfile = open(dstpath + '/' + pathsrc.rsplit('/',1)[-1].split('.',1)[0] +  + str(j) +".sol","a")
    orilines = file.readlines()
    lines = orilines
    i = 0
    while i < len(lines):
        # mfile.writelines(lines[i])
        # i += 1
        # 如果是空行,直接看下一行
        if lines[i] == " ":
            mfile.writelines(lines[i])
            i += 1
        #判断每一行是否包含需要修改的关键词，如果存在，再判断是否进行修改
        #一行代码中如果有多个可以修改的关键词，每个关键词都需要判断一次
        #将一行中所有可以修改的关键词都修改完成后，再将这一行写入新的文件中
        # pure -> view
        if lines[i].find(" pure ") != -1:
            #如果r为1则修改，为0则不修改
            if rr():
                #replace不改变原来的字符串，它的返回值才是替换后的结果
                lines[i] = lines[i].replace(" pure "," view ")
        # private internal external ->public
        if lines[i].find(" private ") !=-1 or lines[i].find(" internal ") != -1 or \
                lines[i].find(" external ") != -1:
            if rr():
                lines[i] = lines[i].replace(" private "," public ")
                lines[i] = lines[i].replace(" internal "," public ")
                lines[i] = lines[i].replace(" external ", " public ")
        # delete "require" "assert"
        if lines[i].find("require(") != -1 or lines[i].find("assert(") != -1:
            if rr():
                lines[i] = "/*" + lines[i]
                while lines[i].find(");") == -1:
                    mfile.writelines(lines[i])
                    i += 1
                lines[i] = lines[i] + "*/"
        # && -> ||
        # &&要一起修改，防止因为随机数不一致，变成&|或|&
        if lines[i].find("&&") != -1:
            if rr():
                lines[i] = lines[i].replace("&&","||")
        #防止出现<= >=的情况
        if lines[i].find(" < ") != -1 or lines[i].find(" > ") != -1:
            if rr():
                if random.randint(0,1) == 0:
                    lines[i] = lines[i].replace("<","!=")
                    lines[i] = lines[i].replace(">","!=")
                else:
                    lines[i] = lines[i].replace("<", "<=")
                    lines[i] = lines[i].replace(">", ">=")
        # bytes8 -> bytes32;uint8 ->uint256..
        # 确保是bytes1，bytes2..而不是单纯的bytes,并且保证修改的不是bytes32
        if lines[i].find("bytes") != -1 and lines[i][lines[i].find("bytes")+5] != " "\
                and lines[i].find("bytes32") == -1:
            if rr():
                lines_list = list(lines[i])
                ii = lines[i].find("bytes") + 5
                while lines_list[ii] != " ":
                    lines_list.pop(ii)
                lines_list.insert(ii,"32")
                lines[i] = ''.join(lines_list)
        if lines[i].find("uint") != -1 and lines[i][lines[i].find("uint")+4] != " " \
                and lines[i].find("uint256") == -1:
            if rr():
                lines_list = list(lines[i])
                ii = lines[i].find("uint") + 4
                while lines_list[ii] != " ":
                    lines_list.pop(ii)
                lines_list.insert(ii,"256")
                lines[i] = ''.join(lines_list)

        #    -> payable
        if lines[i].find("function") != -1:
            if rr():
                lines_list = list(lines[i])
                lines_list.insert(lines[i].find(")")+1," payable ")
                lines[i] = ''.join(lines_list)
        # If(**  ##) -> if(true)
        if lines[i].find(" if") != -1:
            if rr():
                lines_list = list(lines[i])
                ii = lines[i].find("(")
                if ii == -1 :
                    continue
                ii += 1
                iiii = ii
                iii = lines[i].rfind(")") #找最后一个右括号，防止出现 if ((a*b)>c)的情况
                while ii < iii:
                    lines_list.pop(iiii)
                    ii += 1
                lines_list.insert(lines[i].find("(")+1,"True")
                lines[i] = ''.join(lines_list)
        mfile.writelines(lines[i])
        print( lines[i])
        i += 1
    file.close()
    mfile.close()

