import os
import shutil
import time

del_extension = {
    '.tmp': '临时文件',
    '._mp': '临时文件_mp',
    '.log': '日志文件',
    '.gid': '临时帮助文件',
    '.chk': '磁盘检查文件',
    '.old': '临时备份文件',
    '.xlk': 'Excel备份文件',
    '.bak': '临时备份文件bak'
}

ISOTIMEFORMAT = '%Y-%m-%d %X'
t_time = time.strftime(ISOTIMEFORMAT, time.localtime(time.time()))
log_extension = t_time.split(' ')[1].replace(':', '_')

del_userprofile = ['cookies', 'recent', 'Temporary Internet Files', 'Temp']
del_windir = ['prefetch', 'temp']

# 显示当前已定义的扫描文件类型
print("###当前扫描文件：###")
for del_item_type in del_extension:
    print(del_item_type, del_extension[del_item_type])


# 获取系统盘
SYS_DRIVE = os.environ['systemdrive'] + '\\'
# 获取用户目录
USER_PROFILE = os.environ['userprofile']
# 获取 Windows 目录
WIN_DIR = os.environ['windir']


# 获取当前路径 os.getcwd() 'E:\\Software\\Python27'
# 跳转至指定的文件目录 os.chdir('d://wamp')
# 获取系统盘符 os.environ['systemdrive'] 'C:'
# 获取用户目录 os.environ['userprofile'] 'C:\\Users\\Administrator'
# 获取 Windows 目录 os.environ['windir'] 'C:\\Windows'


def GetDesktopPath():  # 获取桌面路径
    return os.path.join(os.path.expanduser("~"), 'Desktop')


# 添加自定义文件类型
def add_del_items():
    old_del_extension_len = len(del_extension)
    yes_or_no = input(">>>>>>是否添加新文件类型？(y/n) ##注意添加时不需要符号”.“")
    if yes_or_no is 'y':
        while 1:
            new_input = input(">>>>输入文件类型(退出请输入quit)：")
            if new_input == 'quit':
                break
            else:
                file_extension = "." + new_input
                del_extension[file_extension] = input(">>>>输入自定义名称：")
    if old_del_extension_len < len(del_extension):
        print("添加类型成功！！！共添加{}个文件类型。".format(str(len(del_extension) - old_del_extension_len)))


# 删除类型
def remove_del_issue():
    old_del_extension_len = len(del_extension)
    yes_or_no = input(">>>>>>是否删除文件类型？(y/n) ##注意添加时不需要符号”.“")
    if yes_or_no is 'y':
        while 1:
            new_input = input(">>>>输入文件类型(退出请输入quit)：")
            if new_input == 'quit':
                break
            else:
                file_extension = "." + new_input
                if file_extension not in del_extension:
                    print("类型不存在，请重新输入！！！")
                    continue
                else:
                    del_extension.pop(file_extension)

    if old_del_extension_len > len(del_extension):
        print("删除类型成功！！！共删除{}个文件类型。".format(str(abs(len(del_extension) - old_del_extension_len))))


def add_or_remove():
    while 1:
        judge = int(input(">>>>>> 需要添加类型请输入：1，删除类型输入：2,退出输入：3 <<<<<<"))
        if judge == 1:
            add_del_items()
        elif judge == 2:
            remove_del_issue()
        elif judge == 3:
            break
        else:
            print("请输入正确的数字！！！")
            continue


def del_dir_or_file(root):
    try:
        if os.path.isfile(root):
            # 删除文件
            os.remove(root)
            print('file: ' + root + ' removed')

        elif os.path.isdir(root):
            # 删除文件夹
            shutil.rmtree(root)
            print('directory: ' + root + ' removed')

    except WindowsError as message:
        print('failure: ' + root + " can't remove" + '\n' + str(message))


# 字节bytes转化kb\m\g
def formatSize(bytes):
    try:
        bytes = float(bytes)
        kb = bytes / 1024
    except TypeError:
        print("传入的字节格式不对")
        return "Error"
    if kb >= 1024:
        M = kb / 1024
        if M >= 1024:
            G = M / 1024
            return "%.3f" % G
        else:
            return "%.3f" % M
    else:
        return "%.3f" % kb


class DiskClean(object):
    def __init__(self):
        self.del_info = {}
        self.del_file_paths = []
        self.total_size = 0
        self.root_path = ""
        for k, v in del_extension.items():
            self.del_info[k] = dict(name=v, count=0)

    def scan(self):
        print("当前待扫描地址{}".format(USER_PROFILE))
        y_n = input("<<<<<< 是否更换盘符?（y/n） >>>>>>")
        if y_n == 'n':
            print("！！！请稍后！！！")
            for roots, dirs, files in os.walk(USER_PROFILE, topdown=False):
                # 生成并展开以 root 为根目录的目录树，参数 topdown 设定展开方式从底层到顶层
                for file_item in files:
                    # 获取扩展名
                    file_extension = os.path.splitext(file_item)[1]
                    # print os.path.join(roots, file_item)
                    if file_extension in self.del_info:
                        # 文件完整路径
                        file_full_path = os.path.join(roots, file_item)
                        self.del_file_paths.append(file_full_path)
                        self.del_info[file_extension]['count'] += 1
                        self.total_size += os.path.getsize(file_full_path)
                        self.root_path = roots.split(':')[0]
        elif y_n == 'y':
            while 1:
                aim_add = input('输入盘符>>>>>>')
                if len(aim_add) > 1 and os.path.exists(aim_add):
                    pass
                    break
                elif len(aim_add) == 1:
                    if aim_add.isupper():
                        pass
                        break
                    else:
                        aim_add = aim_add.upper() + ":\\"
                        break
                elif os.path.exists(aim_add) is False:
                    print("！！！输入的地址不存在，请重新输入。")

            print("！！！请稍后！！！")
            for roots, dirs, files in os.walk(aim_add, topdown=False):
                # 生成并展开以 root 为根目录的目录树，参数 topdown 设定展开方式从底层到顶层
                for file_item in files:
                    # 获取扩展名
                    file_extension = os.path.splitext(file_item)[1]
                    # print os.path.join(roots, file_item)
                    if file_extension in self.del_info:
                        # 文件完整路径
                        file_full_path = os.path.join(roots, file_item)
                        self.del_file_paths.append(file_full_path)
                        self.del_info[file_extension]['count'] += 1
                        self.total_size += os.path.getsize(file_full_path)
                        # self.root_path = roots.split(':')[0]

    def write_log(self):
        log_file = open(GetDesktopPath() + "/log{}.txt".format(log_extension), "w")
        log_file.write("{}盘".format(self.root_path) + '\n')
        for extension, dict_info in self.del_info.items():
            print(extension + " " + dict_info['name'] + " " + str(dict_info['count']) + "个")
            log_file.write(extension + " " + dict_info['name'] +
                           " " + str(dict_info['count']) + "个" + '\n')
        log_file.close()

    def show(self):
        for extension, dict_info in self.del_info.items():
            print(extension + " " + dict_info['name'] + " " + str(dict_info['count']) + "个")

        print('删除可节省:%s 空间' % formatSize(self.total_size))

    def delete_files(self):
        del_log_file = open(GetDesktopPath() + "/del_log{}.txt".format(log_extension), "w")
        for i in self.del_file_paths:
            del_log_file.write(i + '\n')
            del_dir_or_file(i)
        del_log_file.close()
        print("删除成功！！")

    def show_full_path(self):
        for full_path in self.del_file_paths:
            print(full_path)


if __name__ == '__main__':
    add_or_remove()
    cleaner = DiskClean()
    cleaner.scan()
    cleaner.show()
    # cleaner.show_full_path()
    # cleaner.write_log()
    if_del = input('！！！是否删除y/n:')
    if if_del == 'y':
        cleaner.delete_files()
    time.sleep(3)
