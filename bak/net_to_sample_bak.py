#coding=utf-8
import sys

def net_to_sample(net_file, zhongzi_file):
    id_author = {}
    author_id = {}
    id_subcate = {}
    subcate_id = {}
    id_tag = {}
    tag_id = {}
    tag_num = {}

    id_subcate_len = 0
    id_author_len = 0
    id_tag_len = 0

    paper_author = {}
    paper_subcate = {}
    paper_tag = {}
    
    author_subcate = {}
    author_nids = {}
    author_tag = {}

    tag_set = set()
    author_dict = {}
    cate_remove_set = set()
    cate_remove_set = {"影视","娱乐","明星周边","军事","社会"}
    with open(net_file) as f:
        i = 0
        for line in f:
            if i % 100000 == 0:
                print(line)
            i += 1
            if i >= 1000000000:
                break
            line_list = line.strip().split("\t")
            nid,title,url,public_time,mthid,uploader,sv_author_brand_level,tags,general_tag,manual_tags,\
                    video_type,realurl,video_duration,new_cate_v2,new_sub_cate_v2,bjh_is_v = line_list[:16]
            
            #if new_cate_v2 in cate_remove_set:
            #    continue
            mthid = 'a' + mthid
            if mthid not in author_dict:
                author_dict[mthid] = {}
                author_dict[mthid]["num"] = 0
                author_dict[mthid]["tag"] = {}
                author_dict[mthid]["cate"] = set()
            author_dict[mthid]["num"] += 1
            author_dict[mthid]["cate"].add(new_cate_v2)

            manual_tags = manual_tags.replace("]","")
            manual_tags = manual_tags.replace("[","")
            manual_tags = manual_tags.replace("\"","")
            manual_tags = manual_tags.split(",")
            for tag in manual_tags:
                if tag not in author_dict[mthid]["tag"]:
                    author_dict[mthid]["tag"][tag] = 0
                author_dict[mthid]["tag"][tag] += 1

    for mthid in author_dict.keys():
        num = author_dict[mthid]["num"]
        cate_set = author_dict[mthid]["cate"]
        cate_sum = len(cate_set)
        #if num < 30 or cate_sum > 5 or (num / cate_sum) < 10: # 剔除非行业作者，发文小于30，一级分类数量大于5，发文量/一级分类小于10
        #    author_dict.pop(mthid)
        #    continue
        cate_str = "#".join(cate_set) + " "
        tag_num_dict = author_dict[mthid]["tag"]
        tag_sum = len(tag_num_dict)
        tag_num_list = sorted(tag_num_dict.items(), key=lambda e:e[1], reverse=True)
        tag_str = ""
        #tag_i = 0
        for tt in tag_num_list:
            #if tag_i <= tag_sum * 0.3 and tt[1] > 10 and tag_i < 30: # 剔除长尾tag，后百分之70，频次小于10, 每个作者tag上限为50
            tag_str += ("$" + str(tt[0]) + ":" + str(tt[1]) + " ")
            tag_set.add(tt[0]) 
            #else:
            #    author_dict[mthid]["tag"].pop(tt[0])
            #tag_i += 1
        print(str(mthid) + "\t" + str(num) + "\t" + str(cate_sum) + "\t" + str(tag_sum) + "\t" + cate_str + "\t" + tag_str)
        
    print("================")
    exit()
    with open(net_file) as f:
        i = 0
        for line in f:
            if i % 100000 == 0:
                print(line)
            i += 1
            if i >= 1000000000:
                break
            line_list = line.strip().split("\t")
            nid,title,url,public_time,mthid,uploader,sv_author_brand_level,tags,general_tag,manual_tags,\
                    video_type,realurl,video_duration,new_cate_v2,new_sub_cate_v2,bjh_is_v = line_list[:16]
            
            mthid = 'a' + mthid
            if mthid not in author_dict:
                continue
            if new_cate_v2 in cate_remove_set:
                continue
            if mthid not in author_id:
                id_author[id_author_len] = mthid
                author_id[mthid] = id_author_len
                id_author_len += 1
            
            if mthid not in author_subcate:
                author_subcate[mthid] = []
                author_nids[mthid] = []
                author_tag[mthid] = []
            author_subcate[mthid].append(new_sub_cate_v2)
            author_nids[mthid].append([nid,title,url,new_cate_v2,new_sub_cate_v2])
            author_tag[mthid].append(manual_tags)
            
            if new_sub_cate_v2 not in subcate_id:
                id_subcate[id_subcate_len] = new_sub_cate_v2
                subcate_id[new_sub_cate_v2] = id_subcate_len
                id_subcate_len += 1
            
            if nid not in paper_author:
                paper_author[nid] = []
            paper_author[nid].append(str(author_id[mthid]))
            #paper_author.setdefault(nid, []).append(nid)
            
            if nid not in paper_subcate:
                paper_subcate[nid] = []
            paper_subcate[nid].append(str(subcate_id[new_sub_cate_v2]))
                       
            manual_tags = manual_tags.replace("]","")
            manual_tags = manual_tags.replace("[","")
            manual_tags = manual_tags.replace("\"","")
            manual_tags = manual_tags.split(",")
            for tag in manual_tags:
                #if tag not in tag_set:
                #    continue
                if tag not in author_dict[mthid]["tag"]:
                    continue
                if tag not in tag_id:
                    id_tag[id_tag_len] = tag
                    tag_id[tag] = id_tag_len
                    tag_num[tag] = 0
                    id_tag_len += 1
                tag_num[tag] += 1
                if nid not in paper_tag:
                    paper_tag[nid] = []
                paper_tag[nid].append(str(tag_id[tag]))

    with open(zhongzi_file) as f:
        i = 0
        for line in f:
            line_list = line.strip().split("\t")
            tag_list = line_list[0].strip().split(",")
            id_author[id_author_len] = "a" + str(i) + "_author" #种子作者
            author_tag["a" + str(i) + "_author"] = tag_list
            k = 0 
            while k < 100:
                paper_author[str(i) + "_nid_" + str(k)] = []
                paper_author[str(i) + "_nid_" + str(k)].append(id_author_len)#种子文章
                paper_tag[str(i) + "_nid_" + str(k)] = []
                for tag in tag_list:
                    paper_tag[str(i) + "_nid_" + str(k)].append(tag_id.get(tag,""))
                k += 1
            id_author_len += 1
            i += 1 
    id_author_file = open("./net_train/id_author.txt",'w')
    id_subcate_file = open("./net_train/id_conf.txt",'w')
    id_tag_file = open("./net_train/id_tag.txt",'w')
    paper_author_file = open("./net_train/paper_author.txt",'w')
    paper_subcate_file = open("./net_train/paper_conf.txt",'w')
    paper_tag_file = open("./net_train/paper_tag.txt",'w')
    
    author_subcate_file = open("./net_train/author_subcate.txt",'w')
    author_nid_file = open("./net_train/author_nid.txt",'w')
    author_tag_file = open("./net_train/author_tag.txt",'w')
    
    tag_num_file = open("./net_train/tag_num.txt",'w')
    
    for id,author in id_author.items():
        id_author_file.write(str(id) + "\t" + str(author) + "\n")
    for id,subcate in id_subcate.items():
        id_subcate_file.write(str(id) + "\t" + 'v' + str(id) + "\t"+ str(subcate) + "\n")
    for id, tag in id_tag.items():
        id_tag_file.write(str(id) + "\t" + 'i' + str(id) + "\t"+ str(tag) + "\n")

    for tag, num in tag_num.items():
        tag_num_file.write(str(tag) + "\t" + str(num) + "\n")

    for paper,author_ids in paper_author.items():
        for author_id in author_ids: 
            paper_author_file.write(str(paper) + "\t" + str(author_id) + "\n")
   
    for paper,subcate_ids in paper_subcate.items():
        for subcate_id in subcate_ids: 
            paper_subcate_file.write(str(paper) + "\t" + str(subcate_id) + "\n")
    
    for paper,tag_ids in paper_tag.items():
        for tag_id in tag_ids: 
            paper_tag_file.write(str(paper) + "\t" + str(tag_id) + "\n")

    for author,subcate in author_subcate.items():
        subcate_str = "\t".join(subcate)
        author_subcate_file.write(str(author) + "\t" + str(subcate_str) + "\n")
    
    for author,tags in author_tag.items():
        tag_str = "\t".join(tags)
        author_tag_file.write(str(author) + "\t" + str(tag_str) + "\n")
    
    for author,nids in author_nids.items():
        for nid in nids:
            nid_str = "\t".join(nid)
            author_nid_file.write(str(author) + "\t" + str(nid_str) + "\n")
    
    id_author_file.close()
    id_subcate_file.close()
    paper_author_file.close()
    paper_subcate_file.close()
    paper_tag_file.close()
    author_subcate_file.close()
    author_nid_file.close()
    author_tag_file.close()
    tag_num_file.close()

            
if __name__ == '__main__':
    
    net_to_sample("zhengpai_data_mthid", "zhongzi_author")
