#!/bin/sh
source ~/.bashrc
source ~/.bash_profile
ROOT_DIR="./"
BIN='./bin'
DATA_DIR="./data"
RESULT_DIR="./data/result"
LOG_DIR="./log"
email="yingwenjie@baidu.com"
cur_min=`date -d "-1 minute" +%Y%m%d%H%M`
last_min=`date -d "-300 minute" +%Y%m%d%H%M`
echo "$cur_min"

numwalks=10
walklength=10

#检查旧进程是否结束，未结束，发送邮件报警
IP_FILE='nid_district.pid'
if [ -f $IP_FILE ];then
    echo "nid_district pre process is not over: "$datetime | mail -s "warning: local_rep_district" $email
    exit -1
fi
echo "PID of this script: $$" > $IP_FILE
rm -rf ${DATA_DIR}/net_train_${numwalks}
mkdir ${DATA_DIR}/net_train_${numwalks}
rm -rf ${DATA_DIR}/in_train_${numwalks}
mkdir ${DATA_DIR}/in_train_${numwalks}
rm -rf ${DATA_DIR}/out_train_${numwalks}
mkdir ${DATA_DIR}/out_train_${numwalks}
#构建网络
/opt/compiler/gcc-8.2/lib/ld-linux-x86-64.so.2 --library-path /opt/compiler/gcc-8.2/lib `which python` ${BIN}/net_to_sample.py ${numwalks} > ${DATA_DIR}/author_tmp

#随机游走生成序列样本
/opt/compiler/gcc-8.2/lib/ld-linux-x86-64.so.2 --library-path /opt/compiler/gcc-8.2/lib `which python` ${BIN}/metapath.py $numwalks $walklength ${DATA_DIR}/net_train_${numwalks}

#metapath 训练，注意输入文件匹配 
${BIN}/metapath2vec -train ${DATA_DIR}/in_train_${numwalks}/train.cac.w${numwalks}.l${walklength}.newconf.txt -output ${DATA_DIR}/out_train_${numwalks}/train.cac.w${numwalks}.l${walklength} -pp 1 -size 64 -window 5 -negative 3 -threads 32

#种子作者
grep author ${DATA_DIR}/net_train_${numwalks}/id_author.txt | awk -F "\t" '{print $2}' | sort  > ${DATA_DIR}/test_author_tag
#cut -f 2 ./net_train_${numwalks}/id_author.txt > all_author

#获取种子作者的top10相似作者
#./similar_top10 ./out_train/train.cac.w${numwalks}.l${walklength} zhongzi_author_pm_author zhongzi_author_pm_author_out
#./similar_top1000 ./out_train/train.cac.w${numwalks}.l${walklength} all_author all_author_out
#./similar_top10000 ./out_train/train.cac.w${numwalks}.l${walklength} yongshang_author yongshang_author_out
#./similar_top1 ./out_train_all/train.cac.w${numwalks}.l${walklength} biaozhu_pm_remove_other_fz biaozhu_pm_remove_other_out
${BIN}/similar_topall ${DATA_DIR}/out_train_${numwalks}/train.cac.w${numwalks}.l${walklength} ${DATA_DIR}/yongshang_author ${DATA_DIR}/yongshang_author_out

#输出种子作者以及top10作者的 tags标签
#sh pinggu_author.sh ${numwalks} test_author_tag_out  > pinggu_res_${numwalks}_${walklength} 
#sh pinggu_author.sh ${numwalks} zhongzi_author_pm_author_out_09  > pinggu_res_${numwalks}_${walklength}_09 

rm $IP_FILE
