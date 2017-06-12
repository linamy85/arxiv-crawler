#!/bin/bash
while IFS='' read -r line || [[ -n "$line"  ]]; do
    type="$(echo "$line" | cut -d$'\t' -f1)"
    echo "Processing: $line"
    printf "$type\n\n\n" | scrapy crawl arxiv -o $type.json
done < "$1"
