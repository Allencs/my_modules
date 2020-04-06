import json
import os


class BeautifyJson(object):

    desktopPath = os.path.join(os.path.expanduser("~"), 'Desktop')
    operationItem = set()

    def scan(self):
        for roots, dirs, files in os.walk(self.desktopPath):
            for file in files:
                try:
                    file_ext = os.path.splitext(file)[1]
                    if file_ext == ".json":
                        self.operationItem.add(os.path.join(roots, file))
                except OSError as error:
                    print(error)

    @classmethod
    def beautify(cls):
        BeautifyJson().scan()
        if len(BeautifyJson().operationItem) != 0:
            for file in cls.operationItem:
                if os.path.exists(file):
                    with open(file, 'r') as f:
                        try:
                            json_in = json.load(f)
                            f.close()
                        except IOError as error:
                            print(error)
                        else:
                            new_json = json.dumps(json_in, sort_keys=False, indent=4)
                            with open(file, 'w') as f_2:
                                try:
                                    f_2.write(new_json)
                                    f_2.close()
                                except IOError as error2:
                                    print(error2)
                else:
                    print("File doesn't exist: {}".format(file))
                print("Jsons have been beautified......")
        else:
            print("No Json Files......")


if __name__ == '__main__':
    BeautifyJson().beautify()
