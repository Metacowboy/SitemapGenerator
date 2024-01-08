import requests
from requests.adapters import HTTPAdapter

from urllib.request import Request, urlopen
from urllib.parse import urlparse
import urllib.error

#import urllib3
#from urllib3.util.retry import Retry
#urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

from bs4 import BeautifulSoup
url_list = []
base_url =''
hdr = {'User-Agent', 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_9_2) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/34.0.1847.131 Safari/537.36'}


#session = requests.Session()
#session.headers['User-Agent'] = 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_9_2) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/34.0.1847.131 Safari/537.36'
#session.get(url)
#retry = Retry(connect=3, backoff_factor=0.5)
#adapter = HTTPAdapter(max_retries=retry)
#session.mount('http://', adapter)
#session.mount('https://', adapter)


base_url  = input("Please enter the website URL Counting the Words for: >> ")

session.get(base_url)

try:
    req = Request(url=base_url, headers=hdr)
    html  = urlopen(req)

except urllib.error.HTTPError as err:
    print(f'A HTTPError was thrown: {err.code} {err.reason}')
    quit()



bsObj = BeautifulSoup(html.read(), features="html.parser");

# Get all Urls on these page 
urls=[]
for link in bsObj.find_all('a'):
    if link.get('href') not in urls:
        urls.append(link.get('href'))
    else:
        pass
print(urls)

# Count words in html on each and SUM
words=0
for url in urls:
    if url not in ["NULL", "_blank", "None", None, "NoneType", ""]:


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
        
        
        try:
            r = requests.get(specific_url, verify=False, timeout=5)
        
        except requests.exceptions.Timeout:
                # Maybe set up for a retry, or continue in a retry loop
                continue
        except requests.exceptions.TooManyRedirects:
                # Tell the user their URL was bad and try a different one
                continue
        except requests.exceptions.ConnectionError:
                print("Site not rechable", specific_url)
                continue
        except requests.exceptions.RequestException as e:
                # catastrophic error. bail.
                raise SystemExit(e)

        


        soup = BeautifulSoup(r.text, features="html.parser")
        for script in soup(["script", "style"]):
            script.extract()
        text = soup.get_text()
        lines = (line.strip() for line in text.splitlines())
        chunks = (phrase.strip() for line in lines for phrase in line.split("  "))
        text = '\n'.join(chunk for chunk in chunks if chunk)
        text_list = text.split()
        print(f"{specific_url}: {len(text_list)} words")
        
        url_list.append(specific_url +" "+ str(len(text_list)) +" words")
        


        words += len(text_list)
    else:
        pass
print(f"Total: {words} words")



domain = urlparse(base_url).netloc
domain =('.'.join(domain.split('.')[-2:]))

url_list.append("####################################################")
url_list.append(domain +" "+ str(words) +" #Total words")

with open(domain+'.txt', 'w') as f:
            for val in url_list:
                f.writelines(val + "\n")
