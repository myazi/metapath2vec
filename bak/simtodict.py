import sys

if __name__ == '__main__':
    th = 0.85
    author_dict = {}
    for line in sys.stdin:
        line_list = line.strip().split("\t")
        if len(line_list) < 3:
            continue
        author1 = "MTHID_" + str(line_list[0])
        author2 = line_list[1]
        score = float(line_list[2])
        if score < th:
            continue
        if author1 not in author_dict:
            author_dict[author1] = []
        author_dict[author1].append(author2)
    for author in author_dict:
        author2_str = "\t".join(author_dict[author])
        print(str(author) + "\t" + str(author2_str))
