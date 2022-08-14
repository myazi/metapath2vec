import sys

pair_file = sys.argv[1]

i = 0
with open(pair_file) as f:
    key_set = set()
    value_list  = []
    i = 1
    num = 0
    for line in f:
        if i % 100 == 0:
            for key in key_set:
                if key in value_list:
                    print(key)
                    num += 1
            print(key_set)
            key_set = set()
            value_list  = []

        line_list = line.strip().split("\t")
        key_set.add(line_list[0])
        value_list.append(line_list[1])
        i += 1
    print(num)
