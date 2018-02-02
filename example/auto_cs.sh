FILE=arxiv.list

while read line; do
  #echo "$line"
  cate=$(echo $line | awk '{print $1}')
  echo "${cate}\n\n\n" | scrapy crawl arxiv -o ${cate}.json
  echo "Done\n\n\n"
done < "$FILE"
