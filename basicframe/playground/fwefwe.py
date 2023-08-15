from newspaper import Article

# 创建 Article 对象
article = Article('https://www.cfr.org/podcasts/presidents-inbox-north-korea')

# 下载文章内容
article.download()

# 解析文章内容
article.parse()

# 输出文章标题、作者、发布日期和正文内容
print("Title:", article.title)
print("Authors:", article.authors)
print("Publish Date:", article.publish_date)
print("Text:", article.text)
