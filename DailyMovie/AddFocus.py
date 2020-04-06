
class AddFocus(object):

    focus_file = "F:\\A's Files\\focus_file.txt"

    @classmethod
    def add_focus(cls):
        focus_films = set()
        file = open(cls.focus_file, 'r')
        for cur_line_number, line, in enumerate(file):
            if cur_line_number > 0:
                focus_films.add(line.replace("\n", ""))
        return focus_films
