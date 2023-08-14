unset PROXY_ARR
while read line
do
        PROXY_ARR=("${PROXY_ARR[@]}" "$line")
done < ../common/list_proxy
max_proxy=${#PROXY_ARR[@]}

