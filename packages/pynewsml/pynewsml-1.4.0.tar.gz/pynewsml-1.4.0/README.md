# pynewsml

A NewsML parsing library

## Installation

```bash
pip install pynewsml
```

## Usage

```python
from pynewsml import NewsML

with open('path/to/newsml.xml', mode='r') as fp:
    xml_content = fp.read()

newsml = NewsML(xml_content)
news = newsml.news_items[0]

print(news.news_lines.headline)
```
