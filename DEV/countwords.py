import requests
from urllib.request import urlopen
from bs4 import BeautifulSoup

# https://independencerpgs.com/
base_url = "https://metaprime.at/"
html = urlopen(base_url)
bsObj = BeautifulSoup(html.read(), features="html.parser");

urls=[]
for link in bsObj.find_all('a'):
    if link.get('href') not in urls:
        urls.append(link.get('href'))
    else:
        pass
print(urls)

words=0
for url in urls:
    if url not in ["NULL", "_blank", "None", None, "NoneType"]:
        if url[0] == "/":
            url=url[1:]
        if base_url in url:
            if base_url == url:
                pass
            if base_url != url and "https://"in url:
                url=url[len(base_url)-1:]
        if "http://" in url:
            specific_url=url
        elif "https://" in url:
            specific_url = url
        else:
            specific_url = base_url + url
        r = requests.get(specific_url)
        soup = BeautifulSoup(r.text, features="html.parser")
        for script in soup(["script", "style"]):
            script.extract()
        text = soup.get_text()
        lines = (line.strip() for line in text.splitlines())
        chunks = (phrase.strip() for line in lines for phrase in line.split("  "))
        text = '\n'.join(chunk for chunk in chunks if chunk)
        text_list = text.split()
        print(f"{specific_url}: {len(text_list)} words")
        words += len(text_list)
    else:
        pass
print(f"Total: {words} words")