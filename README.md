# Arxiv crawler

## Usage

### Crawl multiple types

1. Create a file similar to `arxiv.cat`, including every types you are targeting.
2. Execute
  ```bash
  ./run.sh < your_arxiv.cat
  ```
  And each category will be stored in `<category>.json`.
  
### Crawl single type

```bash
scrapy crawl arxiv -o $type.json
```

Then input the category and index range you want to crawl (default: 0 - 20000) as asked.

## Tool
* scrapy (python3)

## Good Reference
1. [scrapy Selector](http://www.pycoding.com/2016/03/14/scrapy-04.html)
