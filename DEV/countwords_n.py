import requests
from urllib.request import urlopen
from bs4 import BeautifulSoup

####
#Some Bugs with schema
######

base_url = "https://independencerpgs.com/"
html = urlopen(base_url)
bsObj = BeautifulSoup(html.read(), features="html.parser");

# Sets handle duplicate items automatically
urls=set()
for link in bsObj.find_all('a'):
    urls.add(link.get('href'))
print(urls)

words=0
for url in urls:
    # Having the logic this way saves 4 spaces indent on all the logic
    if url in ["NULL", "_blank", "None", None, "NoneType", base_url]:
        continue

    # The == base_url case is handled in the above `if`
    if url[0] == "/":
        specific_url = base_url + url # requests.get does not care about the num of '/'
    else:
        specific_url = url

    r = requests.get(specific_url)
    soup = BeautifulSoup(r.text, features="html.parser")
    for script in soup(["script", "style"]):
        # Use clear rather than extract
        script.clear()
    # text is text you don't need to preprocess it just yet.
    text = soup.get_text()
    print(f"{specific_url}: {len(text)} words")
    words += len(text)


print(f"Total: {words} words")