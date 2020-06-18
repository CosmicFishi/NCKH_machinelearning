from newspaper import Article
import newspaper

paper = newspaper.build("https://surgeons.conferenceseries.com/?fbclid=IwAR3wxHh95DtOgn2BMZgqZYddS37b9vqXiV_vIowCSd_uoiSg4HjaZMn6ZR8", memoize_articles=False)


print("=== DANH SÁCH DANH MỤC ===")
for cat in paper.category_urls():
    news = newspaper.build(cat, memoize_articles=False)
    # print("=== DANH SÁCH BÀI BÁO ===")
    for article in news.articles:
        print(article.url)
        print("=========")

print("=== LẤY NỘI DUNG CÁC BÀI BÁO ===")
# http://market-analysis.conferenceseries.com/organic-and-inorganic-chemistry-market-reports
# http://market-analysis.conferenceseries.com/internal-medicine-and-hospital-medicine-market-reports
# https://plus.google.com/u/0/b/118167199714932089007/+Omicsgroup
article = Article("http://market-analysis.conferenceseries.com/organic-and-inorganic-chemistry-market-reports", memoize_articles=False)
article.download()
article.parse()
print(article.summary)
print(article.text)
