CC = /usr/bin/gcc
CPP = /usr/bin/g++

#FLAGS = -lm -pthread -O3 -march=native -Wall -funroll-loops -Wno-unused-result
FLAGS = -lm -pthread -O3 -march=native -funroll-loops -Wno-unused-result

all: metapath2vec distance similar pair_similar position similar_top10 similar_topall similar_top1 diff_distance

metapath2vec : metapath2vec.cpp
	$(CPP) metapath2vec.cpp -o metapath2vec $(FLAGS)

distance : distance.c
	$(CC) distance.c -o distance $(FLAGS)

similar : get_similar_author.c
	$(CC) get_similar_author.c -o similar $(FLAGS)

similar_top1000: get_similar_author_zj.c
	$(CC) get_similar_author_zj.c -o similar_top1000 $(FLAGS)

similar_top10000: get_similar_author_10000.c
	$(CC) get_similar_author_10000.c -o similar_top10000 $(FLAGS)

similar_topall: get_similar_author_all.c
	$(CC) get_similar_author_all.c -o similar_topall $(FLAGS)
    
similar_top1: get_similar_author_lzj.c
	$(CC) get_similar_author_lzj.c -o similar_top1 $(FLAGS)

similar_top3: get_similar_author_top3.c
	$(CC) get_similar_author_top3.c -o similar_top3 $(FLAGS)

similar_top10: get_similar_author_top10.c
	$(CC) get_similar_author_top10.c -o similar_top10 $(FLAGS)

position: get_position.c
	$(CC) get_position.c -o position $(FLAGS)

pair_similar : get_similar_author_2.c
	$(CC) get_similar_author_2.c -o pair_similar $(FLAGS)

diff_distance: diff_distance.c
	$(CC) diff_distance.c -o diff_distance $(FLAGS)
clean:
	rm -rf metapath2vec distance similar pair_similar position
