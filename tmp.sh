
#!/bin/bash
i=0

while read line
do
    echo $line
    key_tags=`grep $line zhengpai_data_mthid | awk -F " " '{print$0"\n"}'` 
    echo $key_tags
done < $1

