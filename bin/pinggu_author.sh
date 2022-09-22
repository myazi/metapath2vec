
#!/bin/bash
i=0

while read line
do
    tmp[$i]=$line
    #echo $line
    key=`echo $line | awk -F " " '{print $1}'`
    value=`echo $line | awk -F " " '{print $2}'`
    score=`echo $line | awk -F " " '{print $3}'`
    key_tags=`cat ./data/net_train_$1/author_tag.txt | awk -F "\t" -v author="$key" '{if($1==author) print $0}'` 
    value_tags=`cat ./data/net_train_$1/author_tag.txt | awk -F "\t" -v author="$value" '{if($1==author) print$0}'`
    #echo "$key" "$value_tags" "${score}"
    echo "${key_tags}" "$value_tags" "${score}"
    let i+=1
done < $2

