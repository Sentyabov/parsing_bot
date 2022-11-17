import os
import time


class ClearLog:

    def __init__(self, path_log_file):
        self.path_log = path_log_file
        self.limit_lines = 10000
        self.count = 0

    def check_size(self):
        with open(self.path_log, mode='r') as file:
            for i in file:
                self.count += 1
        return self.count

    def clear_file(self):
        with open(self.path_log, mode='r+') as input_file:
            line_list = []
            for line in input_file:
                line_list.append(line)
        if self.count >= self.limit_lines:
            with open(self.path_log, mode='w') as output_file:
                for string in line_list[self.count - self.limit_lines + 5000:]:
                    output_file.write(string)


if __name__ == '__main__':
    filename = 'stdout'
    log_obj = ClearLog(filename)
    log_obj.check_size()
    log_obj.clear_file()
