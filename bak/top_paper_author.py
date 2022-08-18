#coding=utf-8
import sys
import json
reload(sys)
sys.setdefaultencoding("utf-8")
def top_paper_author(nid_file):
    mthid_dict = {}
    hangye_dict = {}
    hangye_id = {}
    i = 0
    with open(nid_file) as f:
        for line in f:
           #if i > 10000:
           #     break
           i += 1
           line_list = line.strip().split("\t")
           if len(line_list) < 3:
               continue
           hangye = line_list[2]
           hangye_list = hangye.split(" ")
           hangye = hangye_list[0]
           hangye_name = hangye_list[1]
           hangye_id[hangye] = hangye_name
           line = line_list[6]
           line_json = json.loads(line)
           nid = line_json["line"][0]
           public_time = line_json["line"][3]
           mthid = line_json["line"][4]
           tag = line_json["line"][9]
           if mthid == '0':
               continue
           if hangye not in hangye_dict:
                hangye_dict[hangye] = {}
                hangye_dict[hangye][mthid] = 0
           if mthid not in hangye_dict[hangye]:
               hangye_dict[hangye][mthid] = 0
           hangye_dict[hangye][mthid] += 1
           if mthid not in mthid_dict:
               mthid_dict[mthid] = {}
               mthid_dict[mthid]["all_nid"] = 0 
               #mthid_dict[mthid][hangye] = {}
           #if hangye not in mthid_dict[mthid]:
           #    mthid_dict[mthid][hangye] = {}
           #    mthid_dict[mthid]["all_nid"] = 0 
           #    mthid_dict[mthid][hangye]["nid_num"] = 0
           #    mthid_dict[mthid][hangye][nid] = tag
           #mthid_dict[mthid][hangye]["nid_num"] += 1
           mthid_dict[mthid]["all_nid"] += 1 
    
    for hangye in hangye_dict:
        for mthid in hangye_dict[hangye]:
            #print(str(mthid) + "\t" + str(hangye_dict[hangye][mthid]) + "\t" + str(mthid_dict[mthid]["all_nid"]))
            #if (hangye_dict[hangye][mthid]) < 10 or (float(hangye_dict[hangye][mthid]) / float(mthid_dict[mthid]["all_nid"])) < 0.6:
            #    hangye_dict[hangye].pop(mthid)
            #    continue
            hangye_dict[hangye][mthid] = [float(hangye_dict[hangye][mthid]) / float(mthid_dict[mthid]["all_nid"] + 2), float(hangye_dict[hangye][mthid]), float(mthid_dict[mthid]["all_nid"] + 2)]
    for hangye in hangye_dict:
        tmp_dict = hangye_dict[hangye]
        tmp = sorted(tmp_dict.items(), key = lambda kv:(kv[1][0], kv[0]),reverse=True)
        i = 0
        for mthid in tmp:
            i += 1
            if i > 10 or mthid[1][0] < 0.6:
                break
            print (str(hangye_id[hangye]) + "\t" + str(mthid[0]) + "\t" +str(mthid[1][0]) + "\t" + str(mthid[1][1]) + "\t" + str(mthid[1][2]))
            

           #print(str(hangye) + "\t" + str(nid) + "\t" + str(public_time) + "\t" + str(mthid) + "\t" + str(tag))
if __name__ == '__main__':
    nid_file = sys.argv[1]
    top_paper_author(nid_file)

