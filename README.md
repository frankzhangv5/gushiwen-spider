# gushiwen-spider
![](https://img.shields.io/badge/platform-ubuntu%2019.04-blue.svg)
![](https://img.shields.io/badge/python-2.7-blue.svg)
![](https://img.shields.io/badge/mysql--server-v5.7.26-blue.svg)
![](https://img.shields.io/badge/Scrapy-v1.6.0-blue.svg)
![](https://img.shields.io/badge/scrapy--redis-v0.6.8-blue.svg)
![](https://img.shields.io/badge/scrapy--splash-v0.7.2-blue.svg)


## 1. 简介
本项目基于scrapy + scrapy-redis + scrapy-splash编写的爬取gushiwen.org上面诗词的爬虫，在爬取的过程中将需要解析的链接存入redis，将诗词数据持久化到mysql数据库

## 2. 爬取思路
首先按“朝代”这个分类来将所有朝代的链接提取出来存入到redis，然后根据上一步爬取的朝代链接爬取这个朝代的所有页的链接，将页链接存入redis，然后根据每个页链接爬取当前页面上所有诗词的链接，将诗词的链接存入redis，然后根据每个诗词链接，从诗词页面提取所需的数据并存入mysql数据库，当诗词页面有作者信息时，把作者链接存入redis，最后爬取每个作者的页面，将作者的信息提取出来存入mysql数据库

## 3. spider列表
|编号|spider名|spider说明|
|:-:|-|-|
|1|dynasty|爬取所有朝代的链接并存入redis|
|2|page|爬取每个朝代的所有页面链接并存入redis|
|3|list|爬取每个页面上诗词的链接并存入redis|
|4|poem|爬取每个诗词链接页面所需信息，并存入数据库|
|5|poet|爬取每个作者的链接页面所需信息，并存入数据|

## 4. spider执行顺序
由于每个爬虫的输入链接依赖前一个爬虫爬取的结果，所以应该按照上面表格中的编号从小到大依次执行。但是每个spider在无输入链接时会处于等待的状态，所以同时运行每个spider也是可以的。

## 5. 注意事项
- scrapy-splash依赖docker镜像运行，需参考github说明运行docker服务
- scrapy-redis只是redis的客户端，需要提前安装redis-server

## 6. 扩展
+ 可以利用scrapyd与scrapyd-client部署到web
+ 更简单的是使用Gerapy部署到web
