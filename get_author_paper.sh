
#!/bin/bash
i=0

while read line
do
    key=`echo $line | awk -F " " '{print $2}'`
    #echo $key
    #value=`echo $line | awk -F " " '{print $2}'`
    #score=`echo $line | awk -F " " '{print $3}'`
    
    grep $key ./net_train_100/author_paper.txt | awk -F " " '{print$0}' 
    #key_tags=`grep $key ./net_train_all_100/author_paper.txt | awk -F " " '{print$0}'` 
    #value_tags=`grep $value ./net_train_all_$1/author_tag.txt | awk -F " " '{print$0}'` 
    #if [ $((${i}%10)) = 0 ]; then
    #    echo "================================="
    #    echo $key_tags
    #fi
    #echo $key_tags
    let i+=1
done < $1

