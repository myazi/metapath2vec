import sys
import os
import hnswlib
import numpy as np
import time

dim = 64

ids2key = {}
with open("20240601_20250115_click_qk_sort_key_id1") as f:
    for line in f:
        line_list = line.strip('\n').split('\t')
        key, ids = line_list
        ids2key[ids] = key

def ann():
    faiss_index = hnswlib.Index(space = 'cosine', dim = dim)
    faiss_index.load_index("20240601_20250115_click_qk_sort_seq1_log2_50_window5_negative5.txt_build_ann.index")
    index2title = {}
    i = 0
    with open("20240601_20250115_click_qk_sort_seq1_log2_50_window5_negative5.txt_build_ann_words") as f:
        for line in f:
            title = line.strip('\n')
            index2title[i] = title
            i += 1

    embs = []
    keys = []
    with open("20240601_20250115_click_qk_sort_seq1_log2_50_window5_negative5.txt") as f:
        for line in f:
            line_list = line.strip('\n').strip(' ').split(' ')
            key = line_list[0]
            del line_list[0]
            if 'a' in key:
                ids = key.split('a')[1]
                key = ids2key.get(ids, "")
                line_list = [float(i) for i in line_list]
                keys.append(key)
                embs.append(line_list)
            if len(embs) == 1000:
                embs = np.array(embs)
                texts_embs = embs
                time1 = time.time()
                I, D = faiss_index.knn_query(np.array(texts_embs), 200)
                m, n = D.shape
                for i in range(m):
                    for j in range(n):
                        cid = I[i][j]
                        title = index2title[cid]
                        print(keys[i] + "\t" + title + "\t" + str(1 - D[i][j]))
                embs = []
                keys = []

def get_product_emb(product_emb_file, product_file):
	vecs = []
	out = open(product_file, "w")
	cnt = 0
	with open(product_emb_file) as f:
		for line in f:
			line_list = line.strip('\n').split('\t')
			if(len(line_list) < 2): continue
			vec = line_list[1].strip(' ').split(' ')
			if len(vec) != dim: continue
			cnt += 1
	print(cnt)
	vecs_np = np.zeros((cnt, dim), dtype="float32")
	i = 0
	with open(product_emb_file) as f:
		for line in f:
			line_list = line.strip('\n').split('\t')
			if(len(line_list) < 2): continue
			vec = line_list[1].strip(' ').split(' ')
			if len(vec) != dim: continue
			vecs_np[i, :] = np.array(vec)
			i += 1
			out.write("\t".join(line_list[0:1]) + "\n")
	vecs = vecs_np
#vecs = np.array(vecs, dtype="float32")
	assert(len(vecs) > 10000)
	return vecs

if __name__ == "__main__":
	ann()
	exit()
	product_emb_file = sys.argv[1]
	ef_construction = int(sys.argv[2])
	M = int(sys.argv[3])
	ef = int(sys.argv[4])
	topk = int(sys.argv[5])
	save_index_file = sys.argv[6]
	product_file = sys.argv[7]
	X = get_product_emb(product_emb_file, product_file)
	print("get product emb done")
	hnsw_index = hnswlib.Index(space='cosine', dim=len(X[0]))
	hnsw_index.init_index(max_elements=len(X),
		ef_construction=ef_construction,
		M=M)
	data_labels = np.arange(len(X))
	hnsw_index.add_items(np.asarray(X), data_labels)
	hnsw_index.save_index(save_index_file)
	print("index train done")
