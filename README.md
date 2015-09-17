#Usage
Inspired by https://github.com/NikolaiT/GoogleScraper and
https://github.com/DanMcInerney/search-google
This is a google web search crawler with random useragent and automatic result save 
based at python2 + selenium + firefox profile(firefox is mainly for debug, you can use phantomjs instead for headless crawl ) 
For more info please refer to the Chinese Version below 
Sorry for my poor english 

# 用途
使用python2 + selenium + firefox profile 实现的随机user agent 模拟抓取Google搜索结果和关键词的结果数。

使用firefox的目的在于交互的查看爬取错误进行调试，你也可以使用phantomjs进行headless抓取。

相关文件说明：

1. google-web-search.py：从Google抓取某个关键词的所有结果，以“标题 ; 链接”的格式进行保存。
2. google-web-search-state-crawler.py： 从Google抓取某个关键词的结果数，即提取类似“找到约 1,130,000 条结果”中的数字。
3. result-crawler.py： 从Google返回的结果链接中抓取文本。注意只会处理网页和pdf文件。（pdf的下载处理貌似有点问题，可能需要再改一下。）

# 使用

0. 首先请自行安装selenium。
1. 因为Google会封禁任何他认为是BOT的请求，所以如果你要进行批量爬取，最好是自己建立Google的反向代理，推荐：https://www.centos.bz/2014/06/nginx-proxy-google/ 注意最好upstream选择不在一个段的IP（未验证），理论上upstream越多越好（并没有测试。。希望有人可以测试）。将你的IP放入google-add.txt
2. 修改相应的变量，进行抓取。
