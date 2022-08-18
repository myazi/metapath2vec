
#!/bin/bash
i=0

while read line
do
    tmp[$i]=$line
    #echo $line
    key=`echo $line | awk -F " " '{print $1}'`
    value=`echo $line | awk -F " " '{print $2}'`
    score=`echo $line | awk -F " " '{print $3}'`
    #key_tags=`cat ./net_train_$1/author_tag.txt | awk -F " " '{if($1==$key) print $1}'` 
    #value_tags=`cat ./net_train_$1/author_tag.txt | awk -F "\t" '{if($1==$value) print$0}'` 
    value_tags=`cat ./net_train_$1/author_tag.txt | awk -F "\t" -v author="$value" '{if($1==author) print$0}'`
    #cat ./net_train_$1/author_tag.txt | awk -F "\t" '{if($1=="a1643917922845879") print$0}'
    #cat ./net_train_$1/author_tag.txt | awk -F "\t" '{print$1}'
    #key_tags=`grep $key ./biaozhu_all | awk -F " " '{print$0}'` 
    #value_tags=`grep $value ./biaozhu_all | awk -F " " '{print$0}'` 
    #if [ $((${i}%10)) = 0 ]; then
        #echo "================================="
        #echo $key_tags
    #fi
    echo "$key" "$value_tags"
    #echo "$key_tags"
    let i+=1
done < $2

