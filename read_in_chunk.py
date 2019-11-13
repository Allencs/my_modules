def read_in_chunk(file_obj, chunk_size=2048):
    while True:
        data = file_obj.read(chunk_size)
        if not data:
            break
        yield data


def read_in_line(file_obj):
    while True:
        line = file_obj.readline(2048)
        if not line:
            break
        yield line


def test_read_in_chunk():
    with open(r"D:\sgmuserprofile\pt543f\Desktop\test.txt", encoding='utf-8') as f:
        file_generator = read_in_chunk(f)
        while True:
            try:
                print(file_generator.__next__())
            except StopIteration:
                break
        # return "finish"


def test_read_in_line():
    with open(r"D:\sgmuserprofile\pt543f\Desktop\性能测试需要OS参数.txt", encoding='utf-8') as f:
        file_generator = read_in_line(f)
        line_count = 0
        while line_count < 5:
            try:
                print(file_generator.__next__())
                line_count += 1
            except StopIteration:
                break