import os
from multiprocessing import Process, Lock
import multiprocessing
import time


class CleanScripts(object):
    def __init__(self, scriptsFilePath):
        self.scriptsFilePath = scriptsFilePath

    processPool = []
    deleteContents = ["result", "data", "res"]

    @classmethod
    def changeDeleteContents(cls):
        jud = input("1，增加 2，移除>>>")
        if int(jud) == 1:
            changeItem = input("Type your contents >>>")
            cls.deleteContents.append(changeItem)
        elif int(jud) == 2:
            changeItem = input("Type your contents >>>")
            cls.deleteContents.remove(changeItem)
        else:
            pass

    def clean(self, item, lock):
        for roots, dirs, files in os.walk(self.scriptsFilePath, topdown=False):
            for dir in dirs:
                completeDirPath = os.path.join(roots, dir)
                if item in completeDirPath:
                    if os.path.isdir(completeDirPath):
                        try:
                            if len(os.listdir(completeDirPath)) == 0:  # 判断文件夹是否为空
                                with lock:
                                    try:
                                        os.rmdir(completeDirPath)  # 删除文件夹
                                    except OSError:
                                        continue

                            else:
                                for fileItem in os.listdir(completeDirPath):  # 列出非空文件夹下的内容
                                    completeFilePath = os.path.join(completeDirPath, fileItem)
                                    if os.path.isfile(completeFilePath):  # 判断是否为文件
                                        with lock:
                                            try:
                                                os.remove(completeFilePath)  # 删除文件
                                            except OSError:

                                                continue
                                if os.path.isdir(completeDirPath):
                                    with lock:
                                        try:
                                            os.rmdir(completeDirPath)  # 删除剩余文件夹
                                        except OSError:
                                            pass
                        except OSError:
                            pass

    def startClean(self):
        lock = Lock()
        for deleteContent in self.deleteContents:
            pro = Process(target=self.clean, args=(deleteContent, lock))
            self.processPool.append(pro)
            pro.start()

        for process in self.processPool:
            process.join()


if __name__ == '__main__':
    multiprocessing.freeze_support()
    filePath = input(">>>脚本文件目录：")
    if filePath == "change":
        CleanScripts.changeDeleteContents()
        filePath = input(">>>脚本文件目录：")
        if os.path.exists(filePath):
            LRClean = CleanScripts(filePath)
            LRClean.startClean()
            print("清理完成......")
            time.sleep(5)
        else:
            print("路径不存在...........")
            time.sleep(5)
    else:
        if os.path.exists(filePath):
            LRClean = CleanScripts(filePath)
            LRClean.startClean()
            print("清理完成......")
            time.sleep(5)
        else:
            print("路径不存在...........")
