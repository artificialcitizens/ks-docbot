import os
import requests
from bs4 import BeautifulSoup

url = "https://help.knapsack.cloud/category/144-managing-documentation"
directory = "knapsack/docs/managing-documentation"

response = requests.get(url)
soup = BeautifulSoup(response.content, "html.parser")

article_list = soup.find("ul", class_="articleList")
for article in article_list.find_all("a"):
    article_url = article.get("href")
    article_response = requests.get("https://help.knapsack.cloud" + article_url)
    article_soup = BeautifulSoup(article_response.content, "html.parser")
    # get the main content div
    main_content = article_soup.find("article", id="fullArticle")

    # extract the article name from the URL
    article_name = os.path.splitext(os.path.basename(article_url))[0]
    
    # create the directory if it doesn't exist
    if not os.path.exists(directory):
        os.makedirs(directory)
        
        # create the file if it doesn't exist
    file_path = f"{directory}/{article_name}.txt"
    if not os.path.exists(file_path):
        open(file_path, "w").close()

    # write the article text to the file
    with open(file_path, "w") as f:
        f.write(main_content.get_text())