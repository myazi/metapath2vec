#!/bin/sh
source ~/.bashrc
source ~/.bash_profile
ROOT_DIR="./"
BIN='./bin'
DATA_DIR="./data"
email="yingwenjie@baidu.com"
cur_min=`date -d "-1 minute" +%Y%m%d%H%M`

numwalks=10 ##游走步数
walklength=10 ##游走长度

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
python ${BIN}/net_to_sample.py ${numwalks} > ${DATA_DIR}/author_tmp

#随机游走生成序列样本
python2 ${BIN}/metapath.py $numwalks $walklength ${DATA_DIR}/net_train_${numwalks}

#metapath2vec 训练，注意输入文件匹配
${BIN}/metapath2vec -train ${DATA_DIR}/in_train_${numwalks}/train.cac.w${numwalks}.l${walklength}.newconf.txt -output ${DATA_DIR}/out_train_${numwalks}/train.cac.w${numwalks}.l${walklength} -pp 1 -size 64 -window 5 -negative 3 -threads 32

#随机100个种子作者
cat ${DATA_DIR}/net_train_${numwalks}/id_author.txt | awk -F "\t" '{print $2}' | head -n 100  > ${DATA_DIR}/test_author

#获取种子作者的top10相似作者
${BIN}/similar_top10 ${DATA_DIR}/out_train_${numwalks}/train.cac.w${numwalks}.l${walklength} ${DATA_DIR}/test_author ${DATA_DIR}/test_author_sim

#输出种子作者以及top10作者的 tags标签
sh ${BIN}/pinggu_author.sh ${numwalks} ${DATA_DIR}/test_author_sim > ${DATA_DIR}/pinggu_res_${numwalks}_${walklength}

rm $IP_FILE
