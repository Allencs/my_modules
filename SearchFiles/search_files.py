import os
import time
from multiprocessing import Process, Lock
import json
import tempFile_content

# 获取桌面路径
des = os.path.join(os.path.expanduser("~"), 'Desktop')
# 保存结果
res = []
# 获取系统盘
SYS_DRIVE = os.environ['systemdrive'] + '\\'
# 获取用户目录
USER_PROFILE = os.environ['userprofile']
# 获取 Windows 目录
WIN_DIR = os.environ['windir']


def tempFile():
    tempFile = des + "\\temp"
    if os.path.exists(tempFile):
        with open(tempFile + "\\注意.txt", 'w') as f:
            f.write(tempFile_content.content)
        f.close()
        return tempFile
    else:
        try:
            os.mkdir(tempFile)
            with open(tempFile + "\\注意.txt", 'w') as f:
                f.write(tempFile_content.content)
            f.close()
            return tempFile
        except BaseException as info_error:
            print(info_error)


def add_search_items():
    search_extension = {}
    tempFile_path = tempFile() + "\\search_Items.txt"
    old_del_extension_len = len(search_extension)
    yes_or_no = input(">>>>>>添加新文件类型？(y/n) ##注意添加时不需要符号(.)")
    if yes_or_no is 'y':
        while True:
            new_input = input(">>>>输入文件类型(退出请输入qq)：")
            if new_input == 'qq':
                break
            else:
                file_extension = "." + new_input
                search_extension[file_extension] = input(">>>>输入自定义名称：")
        if os.path.exists(tempFile_path):
            os.remove(tempFile_path)
            json.dump(search_extension, open(tempFile_path, 'a', encoding='utf-8'))
            if old_del_extension_len < len(search_extension):
                print("添加类型成功！！！共添加{}个文件类型。".format(str(len(search_extension) - old_del_extension_len)))
                print("===================================")
                print("当前扫描文件：")
                for search_item_type in search_extension:
                    print(search_item_type, search_extension[search_item_type])
                print("===================================")
                return 1
        else:
            json.dump(search_extension, open(tempFile_path, 'a', encoding='utf-8'))
            if old_del_extension_len < len(search_extension):
                print("添加类型成功！！！共添加{}个文件类型。".format(str(len(search_extension) - old_del_extension_len)))
                print("===================================")
                print("当前扫描文件：")
                for search_item_type in search_extension:
                    print(search_item_type, search_extension[search_item_type])
                print("===================================")
                return 1
    else:
        # json.dump(search_extension, open(tempFile_path, 'w', encoding='utf-8'))
        return 0


def choose():
    # 存储需要搜索的盘符
    search_field = []
    while True:
        aim_add = input('输入盘符,如：c,d或指定路径(退出请输入“qq”)>>>>>>')
        if aim_add == "qq":
            if len(search_field) == 0:
                print("请输入盘符！")
            else:
                break
        else:
            if len(aim_add) > 1 and os.path.exists(aim_add):
                search_field.append(aim_add)
            elif len(aim_add) == 1:
                aim_add = aim_add.upper() + ":\\"
                if os.path.exists(aim_add):
                    search_field.append(aim_add)
                else:
                    print("！！！输入的地址不存在，请重新输入。")

            elif os.path.exists(aim_add) is False:
                print("！！！输入的地址不存在，请重新输入。")

    tempFile_path = tempFile() + "/diskNum.txt"
    if os.path.exists(tempFile_path):
        os.remove(tempFile_path)
        with open(tempFile_path, "a", encoding='utf-8') as f:
            json.dump(search_field, f)
            print("添加成功。")
        f.close()
    else:
        with open(tempFile_path, "w", encoding='utf-8') as f:
            json.dump(search_field, f)
            print("添加成功。")
        f.close()


def scan(path):
    tempFile_path = tempFile() + "\\search_Items.txt"
    extension = json.load(open(tempFile_path, 'r', encoding='utf-8'))
    print(extension)
    search_info = {}
    for i, j in extension.items():
        search_info[i] = dict(name=j, count=0)
    lock = Lock()
    print("！！！请稍后！！！")
    for roots, dirs, files in os.walk(path, topdown=False):
        # 生成并展开以 root 为根目录的目录树，参数 topdown 设定展开方式从底层到顶层
        for file_item in files:
            # 获取扩展名
            file_extension = os.path.splitext(file_item)[1]
            if file_extension in search_info:
                search_info[file_extension]['count'] += 1
                res.append(os.path.join(roots, file_item))
                with lock:
                    with open(des + "\\SearchFiles.txt", 'a', encoding='utf-8') as f:
                        f.write(os.path.join(roots, file_item) + "\n")
                        # print("======== %s" % file_item)
                        f.close()


# 检索搜寻信息
def file_info():
    try:
        f_info = open(des + "\\SearchFiles.txt", 'rb')
        lines = f_info.readlines()
        print("===================================")
        print("总共搜索到文件：{}个".format(str(len(lines) - 3)))
        print("请查看桌面文件《SearchFiles.txt》")
        print("===================================")
        f_info.close()
    except BaseException as error:
        print(error)


def main():
    if add_search_items() == 0:
        pass
    else:
        if os.path.exists(des + "\\SearchFiles.txt"):
            os.remove(des + "\\SearchFiles.txt")
            # 添加盘符
            choose()
            p_list = []
            print("待搜索范围：")
            print("===================================")
            with open(des + "\\SearchFiles.txt", 'w', encoding='utf-8') as f:
                f.write("===================================" + "\n")
                f.write("搜索结果" + "\n")
                f.write("===================================" + "\n")
            f.close()
            search_field = json.load(open(tempFile() + "\\diskNum.txt", 'r', encoding='utf-8'))
            for path in search_field:
                pro = Process(target=scan, args=(path,))
                p_list.append(pro)
                pro.start()
            for p in p_list:
                p.join()
            file_info()
        else:
            # 添加盘符
            choose()
            p_list = []
            print("待搜索范围：")
            print("===================================")
            with open(des + "\\SearchFiles.txt", 'w', encoding='utf-8') as f:
                f.write("===================================" + "\n")
                f.write("搜索结果" + "\n")
                f.write("===================================" + "\n")
            f.close()
            search_field = json.load(open(tempFile() + "\\diskNum.txt", 'r', encoding='utf-8'))
            for path in search_field:
                pro = Process(target=scan, args=(path,))
                p_list.append(pro)
                pro.start()
            for p in p_list:
                p.join()
            file_info()

        time.sleep(3)


if __name__ == '__main__':
    main()




