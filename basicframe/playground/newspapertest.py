import newspaper
url = "http://www.kekenet.com/Article/videolis/List_2129.shtml"


keke = newspaper.build(url)
for articel in keke.articles:
    print(articel.url)