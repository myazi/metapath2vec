#!/bin/sh
source ~/.bashrc
source ~/.bash_profile
ROOT_DIR="./"
DATA_DIR="../data"
LOG_DIR="../log"
email="yingwenjie@baidu.com"
cur_min=`date -d "-1 minute" +%Y%m%d%H%M`
last_min=`date -d "-300 minute" +%Y%m%d%H%M`
#echo "$cur_min"

numwalks=100
walklength=100

#/opt/compiler/gcc-8.2/lib/ld-linux-x86-64.so.2 --library-path /opt/compiler/gcc-8.2/lib `which python` /home/yingwenjie/workspace/user_business/metapath2vec/code_metapath2vec/top_paper_author.py zhengpai_data_yuce_jiaoyu > jiaoyu_author

#获取种子作者的top10相似作者
#cut -f 2 jiaoyu_author > jiaoyu_author_mthid_tmp
#`cat jiaoyu_author_mthid_tmp | awk '{print "a"$0}' > jiaoyu_author_mthid`
#./similar_top10 ./out_train_all/train.cac.w${numwalks}.l${walklength} jiaoyu_author_mthid jiaoyu_author_mthid_out

#输出种子作者以及top10作者的 tags标签
#sh pinggu_author.sh ${numwalks} jiaoyu_author_mthid_out  > pinggu_jiaoyu

 
while read line
do
    key_author=`echo $line | awk -F " " '{print $1}'`
    key_author=${key_author:1--1}
    value_author=`echo $line | awk -F " " '{print $2}'`
    score=`echo $line | awk -F " " '{print $3}'`
    if [[ `expr $score \> 0.9` -eq 0 ]];then
        echo $key_author $value_author  $score
        continue
    fi
    hangye_key_author=`grep $key_author jiazhuang_author | awk -F "\t" '{print $1,$3,$2}'`
    #value_author_nid=`grep $value_author ./net_train_all_100/author_paper.txt | awk -F " " '{print$0}'`
    grep $value_author ./net_train_all_100/author_paper.txt | awk -F " " '{print$0}' > value_author_nid
    while read line
    do
        echo $hangye_key_author $score $line
    done < value_author_nid
    #echo $hangye_key_author $value_author_nid
done < jiazhuang_author_mthid_out
#rm jiazhuang_author_mthid_tmp
#rm jiazhuang_author_mthid
rm $IP_FILE
