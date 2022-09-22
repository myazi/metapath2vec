#coding=utf-8
import sys
import json

def tag(tags_file):
    i = 0
    tag_num = {}
    tag_set = set()
    with open(tags_file) as f:
        for line in f:
            if i % 1000000 == 0:
                print(line)
            i += 1
            if i > 100000000:
                break
            line_list = line.strip().split("\t")
            nid,title,url,public_time,mthid,upload,author_band,tags,general_tags,manual_tags = line_list[:10]
             
            manual_tags = manual_tags.replace("]","")
            manual_tags = manual_tags.replace("[","")
            manual_tags = manual_tags.replace("\"","")
            manual_tags = manual_tags.split(",")
            for tag in manual_tags:
                if tag not in tag_num:
                    tag_num[tag] = 0
                tag_num[tag] += 1

    for tag, num in tag_num.items():
        if num > 10:
            tag_set.add(tag)
    return tag_set

def net_to_sample(net_file, zhongzi_file, tag_set, dir_name):
    author_dict = {}
    id_author = {}
    id_tag = {}
    tag_id = {}
    tag_num = {}

    id_author_len = 0
    id_tag_len = 0

    paper_author = {}
    paper_tag = {}
    
    #cate_remove_set = {"影视","娱乐","明星周边","军事","社会"}
    cate_remove_set = {}
    with open(net_file) as f:
        i = 0
        for line in f:
            if i % 1000000 == 0:
                print(line)
            i += 1
            if i >= 100000000:
                break
            line_list = line.strip().split("\t")
            nid, title, url, public_time, mthid, new_cate_v2, new_sub_cate_v2, manual_tags = line_list[:8] ##mthid, nid, manual_tags
            
            if new_cate_v2 in cate_remove_set:
                continue
            if manual_tags == "": #文章tag为空过滤
                continue
            mthid = 'a' + mthid
            if mthid not in author_dict:
                author_dict[mthid] = {}
                author_dict[mthid]["num"] = 0
                author_dict[mthid]["tag"] = {}
                author_dict[mthid]["cate"] = set()
                author_dict[mthid]["cate_num"] = {}
                author_dict[mthid]["manual_tags"] = []
                author_dict[mthid]["nid"] = []
                author_dict[mthid]["index"] = id_author_len
                id_author_len += 1
            #manual_tags = manual_tags.replace("]","")
            #manual_tags = manual_tags.replace("[","")
            #manual_tags = manual_tags.replace("\"","")
            #manual_tags = manual_tags.split(",")
            manual_tags = json.loads(manual_tags).keys()
            for tag in manual_tags:
                if tag not in author_dict[mthid]["tag"]:
                    author_dict[mthid]["tag"][tag] = 0
                author_dict[mthid]["tag"][tag] += 1

            author_dict[mthid]["num"] += 1
            author_dict[mthid]["cate"].add(new_cate_v2)
            if new_cate_v2 not in author_dict[mthid]["cate_num"]:
                author_dict[mthid]["cate_num"][new_cate_v2] = 0
            author_dict[mthid]["cate_num"][new_cate_v2] += 1
            manual_tags_str = str("$".join(manual_tags))
            author_dict[mthid]["manual_tags"].append(manual_tags_str)
            author_dict[mthid]["nid"].append([nid,title,url,new_cate_v2,new_sub_cate_v2,manual_tags_str,manual_tags])
    #for mthid in author_dict.keys():
    author_set = set(author_dict.keys())
    for mthid in author_set:
        author_nid_num = author_dict[mthid]["num"]
        cate_set = author_dict[mthid]["cate"]
        cate_sum = len(cate_set)
        #if author_nid_num < 10 or cate_sum > 5 or (author_nid_num / cate_sum) < 5: # 剔除非行业作者，发文小于30，一级分类数量大于5，发文量/一级分类小于10
        #if author_nid_num < 10 or (author_nid_num / cate_sum) < 5: # 剔除非行业作者，发文小于30，一级分类数量大于5，发文量/一级分类小于10
        author_cate_num_list = sorted(author_dict[mthid]["cate_num"].items(), key=lambda e:e[1], reverse=True)
        top3 = 0
        for cc in author_cate_num_list[0:3]:
            top3 += cc[1]
        if author_nid_num < 10 or (float(top3) / author_nid_num) < 0.5: # 剔除非行业作者，发文小于30，一级分类数量大于5，发文量/一级分类小于10
            author_dict.pop(mthid)
            print("popopopopop"  + "\t" + str(mthid) + "\t" + str(author_nid_num) + "\t" + str(top3) + "\t" + str(cate_sum))
            continue
        cate_str = "#".join(cate_set)
        author_tag_num_dict = author_dict[mthid]["tag"]
        author_tag_num_list = sorted(author_tag_num_dict.items(), key=lambda e:e[1], reverse=True)
        tag_sum = len(author_tag_num_list)
        tag_str = ""
        tag_i = 0
        for tt in author_tag_num_list:
            tag = tt[0]
            num = tt[1]
            #if tag in tag_set and tag_i <= tag_sum * 0.9 and num > 2 and tag_i < 100: # 剔除长尾tag，后百分之70，频次小于10, 每个作者tag上限为50
            if tag_i <= tag_sum * 0.9 and num > 2 and tag_i < 100: # 剔除长尾tag，后百分之70，频次小于10, 每个作者tag上限为50
                tag_str += ("$" + str(tag) + ":" + str(num) + " ")
                if tag not in tag_id:
                    id_tag[id_tag_len] = tag
                    tag_id[tag] = id_tag_len
                    tag_num[tag] = 0
                    id_tag_len += 1
                tag_num[tag] += 1
            else:
                author_dict[mthid]["tag"].pop(tag)
            tag_i += 1
        id_author[author_dict[mthid]["index"]] = mthid
        nid_datas = author_dict[mthid]["nid"]
        for nid_data in nid_datas:
            nid = nid_data[0]
            paper_author[nid] = author_dict[mthid]["index"] 
            manual_tags = nid_data[6]
            for tag in manual_tags:
                if tag not in author_dict[mthid]["tag"]:
                    continue
                if nid not in paper_tag:
                    paper_tag[nid] = []
                paper_tag[nid].append(str(tag_id[tag]))
        print(str(mthid) + "\t" + str(author_nid_num) + "\t" + str(cate_sum) + "\t" + str(tag_sum) + "\t" + cate_str + "\t" + tag_str)

    id_author_file = open(str(dir_name) + "/id_author.txt",'w')
    id_tag_file = open(str(dir_name) + "/id_tag.txt",'w')
    paper_author_file = open(str(dir_name) + "/paper_author.txt",'w')
    paper_tag_file = open(str(dir_name) + "/paper_tag.txt",'w')
    
    author_paper_file = open(str(dir_name) + "/author_paper.txt",'w')
    author_tag_file = open(str(dir_name) + "/author_tag.txt",'w')
    tag_num_file = open(str(dir_name) + "/tag_num.txt",'w')
    
    for id,author in id_author.items():
        id_author_file.write(str(id) + "\t" + str(author) + "\n")
    for id, tag in id_tag.items():
        id_tag_file.write(str(id) + "\t" + 'i' + str(id) + "\t"+ str(tag) + "\n")
    for paper,author_id in paper_author.items():
        paper_author_file.write(str(paper) + "\t" + str(author_id) + "\n")
    for paper,tag_ids in paper_tag.items():
        for tag_id in tag_ids: 
            paper_tag_file.write(str(paper) + "\t" + str(tag_id) + "\n")

    for mthid in author_dict:
        tag_str = "\t".join(author_dict[mthid]["manual_tags"])
        author_tag_file.write(str(mthid) + "\t" + str(tag_str) + "\n")
        nids = author_dict[mthid]["nid"]
        for nid in nids:
            del nid[6]
            nid_str = "\t".join(nid)
            author_paper_file.write(str(mthid) + "\t" + str(nid_str) + "\n")
    for tag, num in tag_num.items():
        tag_num_file.write(str(tag) + "\t" + str(num) + "\n")

    id_author_file.close()
    id_tag_file.close()
    paper_author_file.close()
    paper_tag_file.close()
    author_paper_file.close()
    author_tag_file.close()
    tag_num_file.close()
            
if __name__ == '__main__':

    numwalks = sys.argv[1]
    dir_name = "./data/net_train_" + str(numwalks)
    #tag_set = tag("all_all")
    tag_set = set()
    net_to_sample("./data/zhengpai_tuwen", "./data/zhongzi_author", tag_set, dir_name)
