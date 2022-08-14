
#!/bin/bash
i=0

while read line
do
    #tmp[$i]=$line
    #echo $line
    key=`echo $line | awk -F " " '{print $1}'`
    value=`echo $line | awk -F " " '{print $2}'`
    score=`echo $line | awk -F " " '{print $3}'`
    
    #key_tags=`grep $key ./net_train_all_$1/author_tag.txt | awk -F " " '{print$0}'` 
    #value_tags=`grep $value ./net_train_all_$1/author_tag.txt | awk -F " " '{print$0}'` 
    key_tags=`grep $key ./biaozhu_all | awk -F " " '{print$0}'` 
    value_tags=`grep $value ./biaozhu_all | awk -F " " '{print$0}'` 
    #if [ $((${i}%10)) = 0 ]; then
    #    echo "================================="
    #    echo $key_tags
    #fi
    echo "$score $key_tags $value_tags \n"
    let i+=1
done < $1

