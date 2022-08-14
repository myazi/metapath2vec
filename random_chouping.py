# -*- coding: utf-8 -*-
import sys
import re
def random_data(file_name):
    with open(file_name) as f:
        res = set()
        for line in f:
            line_list = line.strip().split(" ")
            key = line_list[0]
            value_tags = line_list[1].split("\t")
            value = value_tags[0]
            tags_ch = re.sub("[A-Za-z0-9\!\%\[\]\,\。]", "", line_list[1])
            if (len(tags_ch) / len(value_tags) < 5):
                continue
            value_tags_str = "\t".join(value_tags)
            print(str(key) + "\t" + str(value_tags_str))
            res.add(str(key) + "\t" + str(value))
    i = 0 
    for a in res:
        i += 1
        if i > 1500:
            break
        print(a)

        

if __name__ == '__main__':
    file_name = sys.argv[1]
    random_data(file_name)
