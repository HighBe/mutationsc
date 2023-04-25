import function
import os
import shutil
import test
import randomdeletion
import GenerateEvent


# Press the green button in the gutter to run the script.
if __name__ == '__main__':
    function.testAllFiles("/home/liu/Tool/generateTestScript-master/test suite","/home/liu/Tool/a")

    # os.chdir("/home/liu/Tool/a")
    # strs = os.popen("npx hardhat test").read()
    # tmp = strs[:strs.find("✔")].strip()
    # print("+++++++++++" + tmp + "+++++++++++")

    #人工单个查看
    # srcpath = "/home/liu/Tool/generateTestScript-master/test suite/0x3be7bf1a5f23bd8336787d0289b70602f1940875"
    # dstpath = "/home/liu/Tool/a"
    # os.chdir(dstpath)
    # function.testSingle(srcpath,dstpath)


    # 统计一共有多少个生成了不同的文件
    # path = "/home/liu/Tool/generateTestScript-master/test suite"
    # ls = os.listdir(path)
    # count = 0
    # for dir in ls:
    #     if os.path.isdir(os.path.join(path,dir,"new")) :
    #         lls = os.listdir(os.path.join(path,dir,"new"))
    #         if len(lls) != 0:
    #             count += 1
    # print(count)


    #将所有的test文件都增加查看event的语句，删除之前多余的内容
    # srcpath = "/home/liu/Tool/generateTestScript-master/test suite"
    # lists = os.listdir(srcpath)
    # for d in lists:
    #     ds = os.listdir(os.path.join(srcpath,d))
    #     print("+++++++++++" + d + "++++++++++++++++")
    #     for l in ds:
    #         if l.find("new") != -1:
    #             shutil.rmtree(os.path.join(srcpath,d,l))




# See PyCharm help at https://www.jetbrains.com/help/pycharm/
