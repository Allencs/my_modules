import os

class CleanScripts(object):
    scriptsFilePath = None
    deleteItems = ["result", "data"]
    @classmethod
    def setPath(cls):
        path = input(">>>脚本文件目录：")
        cls.scriptsFilePath = path

    def scan(self):
        for roots, dirs, files in os.walk(self.scriptsFilePath, topdown=False):
            # 生成并展开以 root 为根目录的目录树，参数 topdown 设定展开方式从底层到顶层
            for file in files:
                completeFilePath = os.path.join(roots, file)
                for deleItem in self.deleteItems:
                    if deleItem in completeFilePath:
                        os.remove(completeFilePath)
            for dir in dirs:
                for deleItem in self.deleteItems:
                    completeDir = os.path.join(roots, dir)
                    if deleItem in completeDir:
                        # print(dir)
                        print(completeDir)
                        if len(os.listdir(completeDir)) == 0:
                            try:
                                os.rmdir(completeDir)
                            except OSError as error:
                                print(error)



    def clean(self):
        for roots, dirs, files in os.walk(self.scriptsFilePath, topdown=False):
            for dir in dirs:
                for deleItem in self.deleteItems:
                    if deleItem in dir:
                        completeDirPath = os.path.join(roots, dir)
                        for item in os.listdir(completeDirPath):
                            completePath = os.path.join(completeDirPath, item)
                            if os.path.isfile(completePath) == True:
                                os.remove(completePath)


                        os.rmdir(completeDirPath)


if __name__ == '__main__':
    # pass
    LRClean = CleanScripts()
    LRClean.setPath()
    LRClean.scan()
