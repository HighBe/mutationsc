import function
import os
import shutil
import test
import randomdeletion
import GenerateEvent


# Press the green button in the gutter to run the script.
if __name__ == '__main__':
    # function.testAllFiles("/home/liu/Tool/generateTestScript-master/test suite","/home/liu/Tool/a")

    #测试在每个函数中添加event
    solpath = "/home/liu/Tool/a/contracts/ERC20PresetFixedSupply.sol"
    astpath = "/home/liu/Tool/a/artifacts/build-info/161e9fe941b8b1f3c913187f03aea36c.json"
    GenerateEvent.generateEvent(solpath,astpath)

    #人工单个查看
    # srcpath = "/home/liu/Tool/generateTestScript-master/test s161e9fe941b8b1f3c913187f03aea36c.jsonuite/0x05237e2bd2dfab39a135d254cabae94b183c8bad"
    # dstpath = "/home/liu/Tool/a"
    # function.testSingle(srcpath,dstpath)
    #
    # os.chdir(dstpath)
    # os.system("npx hardhat compile")


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




# See PyCharm help at https://www.jetbrains.com/help/pycharm/
