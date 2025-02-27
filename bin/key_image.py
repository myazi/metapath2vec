#########################################################################
# File Name: key_image.py
# Author: yingwenjie
# mail: yingwenjie@tencent.com
# Created Time: Thu 18 Apr 2024 05:55:41 PM CST
#########################################################################
import sys
import random
#import pandas as pd
import math
import time

"""
file_name = sys.argv[1]
df = pd.read_csv(file_name, sep='\t')
keys = df['keyword']
cids = df['query']
shows = df['show']
clicks = df['click']
"""
key_images = {}
image_keys = {}

key2id = {}
image2id = {}
k = 0
key_id = -1
kid = 0
cid_id = -1
cid = 0
#for key, component_id, show, click in zip(keys, cids, shows, clicks):
for line in sys.stdin:
    line_list = line.strip('\n').split('\t')
    if len(line_list) != 5: continue
    component_id, key, show, click, click_key = line_list[0:5]
    try:
        click = int(click)
    except:
        continue
    if click <= 3: continue
    #if k > 1000000: break
    #if click <= 10: continue
    #print(key)
    if key not in key2id: 
        key_id += 1
        key2id[key] = key_id
        kid = key_id
    else:
        kid = key2id.get(key)
    if component_id not in image2id: 
        cid_id += 1
        image2id[component_id] = cid_id
        cid = cid_id
    else:
        cid = image2id.get(component_id)

    key_images.setdefault(kid, {})
    key_images[kid].setdefault("cids", [])
    key_images[kid].setdefault("cid_weights", [])
    key_images[kid].setdefault("clicks", 0)
    key_images[kid]["clicks"] += click
    key_images[kid]["cids"].append(cid)
    key_images[kid]["cid_weights"].append(click)

    image_keys.setdefault(cid, {})
    image_keys[cid].setdefault("kids", [])
    image_keys[cid].setdefault("kid_weights", [])
    image_keys[cid].setdefault("clicks", 0)
    image_keys[cid]["clicks"] += click
    image_keys[cid]["kids"].append(kid)
    image_keys[cid]["kid_weights"].append(click)

print("done")
kid_file =  open('20240601_20250115_click_qk_sort_key_id4', 'w')
for key, kid in key2id.items():
    kid_file.write(key + "\t" + str(kid) + "\n")
kid_file.close()

cid_file =  open('20240601_20250115_click_qk_sort_cid_id4', 'w')
for component_id, cid in image2id.items():
    cid_file.write(str(component_id) + "\t" + str(cid) + "\n")
cid_file.close()

for kid in key_images:
    clicks = key_images[kid]["clicks"]
    if clicks == 0: continue
    cur_click = 0
    for i in range(len(key_images[kid]["cid_weights"])):
        key_images[kid]["cid_weights"][i] /= clicks
        cur_click += key_images[kid]["cid_weights"][i]
        key_images[kid]["cid_weights"][i] = cur_click
        #print("\t".join([str(i) for i in [kid, key_images[kid]["cids"][i],key_images[kid]["cid_weights"][i], cur_click]]))

for cid in image_keys:
    clicks = image_keys[cid]["clicks"]
    if clicks == 0: continue
    cur_click = 0
    for i in range(len(image_keys[cid]["kid_weights"])):
        image_keys[cid]["kid_weights"][i] /= clicks
        cur_click += image_keys[cid]["kid_weights"][i]
        image_keys[cid]["kid_weights"][i] = cur_click
        #print("\t".join([str(i) for i in [cid, image_keys[cid]["kids"][i],image_keys[cid]["kid_weights"][i], cur_click]]))

#print(len(key_images))
#print(len(image_keys))
out_file = open("20240601_20250115_click_qk_sort_seq4", 'w')
k = 0
for kid in key_images:
    k += 1
    clicks = key_images[kid]['clicks']
    #if clicks < 1000: continue
    #numwalks = int(math.log(clicks + 1, 1.3))
    #numwalks = int(50 - k * 0.00004)
    #numwalks = 10
    numwalks = int(math.log(clicks + 1, 2))
    walklength = 50

    kid0 = kid
    outs = ""
    for i in range(numwalks):
        kid = kid0
        out = "a" + str(kid)
        for j in range(walklength):
            #time1 = time.time()
            cids = key_images[kid]["cids"]
            cid_weights = key_images[kid]["cid_weights"]
            #time2 = time.time()
            prob = random.random()
            #time3 = time.time()
            for i in range(len(cid_weights)): 
                if prob < cid_weights[i]: break
            #time4 = time.time()
            cid = cids[i]
            #cid = random.choices(cids, weights=cid_weights, k=1)[0]
            #cid = random.choices(cids, k=1)[0]
            out += " i" + str(cid)
            kids = image_keys[cid]["kids"]
            kid_weights = image_keys[cid]["kid_weights"]
            #time5 = time.time()
            prob = random.random()
            #time6 = time.time()
            for i in range(len(kid_weights)): 
                if prob < kid_weights[i]: break
            #time7 = time.time()
            kid = kids[i]
            #kid = random.choices(kids, weights=kid_weights, k=1)[0]
            #kid = random.choices(kids, k=1)[0]
            out += " a" + str(kid)
        #time8 = time.time()
        outs += (out + "\n")
        #time9 = time.time()
        #time1 = time2 - time1
        #time2 = time3 - time2
        #time3 = time4 - time3
        #time4 = time5 - time4
        #time5 = time6 - time5
        #time6 = time7 - time6
        #time7 = time8 - time7
        #time8 = time9 - time8
        #print("\t".join([str(i) for i in [time1, time2, time3, time4, time5, time6, time7, time8]]))
    out_file.write(outs)
out_file.close()

