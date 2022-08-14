#coding=utf-8
import sys
import json
reload (sys)
sys.setdefaultencoding("utf-8")
def get_pair_author(author_file,pair_file):
    author_dict = {}
    pm_dict = {}
    hangye_pairnum_dict = {}
    with open(author_file) as f:
        for line in f:
            line = line.strip().split("\t")
            hangye = line[0]
            #hangye = line[0].split(" ")
            #if len(hangye) == 2:
            #    hangye = line[0].split(" ")[1].split("/")[0]
            #else:
            #    hangye = line[0].split(" ")[0]
            author = line[1]
            if author not in author_dict:
                author_dict[author] = hangye
            if hangye not in pm_dict:
                pm_dict[hangye] = 0;
            pm_dict[hangye] += 1

    with open(pair_file) as f:
        for line in f:
            line_list = line.strip().split("\t")
            #print(line_list)
            author1 = line_list[0]
            author2 = line_list[1]
            score = float(line_list[2])
            #if author1 in author_dict and author2 in author_dict  and score > 0.7:
            if author1 in author_dict and author2 in author_dict and score > 0.85:
                hangye1 = author_dict[author1]
                hangye2 = author_dict[author2]
                if hangye1 not in hangye_pairnum_dict:
                    hangye_pairnum_dict[hangye1] = {}
                    hangye_pairnum_dict[hangye1]["yy"] = 0 
                    hangye_pairnum_dict[hangye1]["all"] = 0 
                if hangye1 == hangye2:
                    hangye_pairnum_dict[hangye1]["yy"] +=1 
                hangye_pairnum_dict[hangye1]["all"] +=1 
                
    for hangye in hangye_pairnum_dict:
        yy = hangye_pairnum_dict[hangye]["yy"]
        all = hangye_pairnum_dict[hangye]["all"]
        print(str(hangye) + "\t" +  str(yy) + "\t" + str(all) + "\t" + str(pm_dict[hangye] * (pm_dict[hangye] -1)) + "\t" + str(yy/(all+0.0001)) + "\t" + str(yy/(pm_dict[hangye] * (pm_dict[hangye] -1) + 0.00001)))

if __name__ == "__main__":
    author = sys.argv[1]
    pair = sys.argv[2]
    get_pair_author(author,pair)
