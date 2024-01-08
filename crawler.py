import re
import urllib.request as req
import urllib.error
import global_vars
from url import URL
from sitemap import Sitemap
from visual_sitemap import VisualSitemap
from pprint import pprint
from urllib.parse import urlparse



class Crawler(object):
    def __init__(self):
        pass

    def run(self):
        if not global_vars.sitemap_xml_file_path:
            self.crawl(URL(global_vars.starting_url))
            for u in global_vars.url_list:
                # DEF VAlidate URL DEF
                #if not self.uri_validator(u.complete_url):
                #    continue
                if not u.has_been_crawled:
                    self.crawl(u)
                if len(global_vars.url_list) >= global_vars.urls_tocrawl:    
                    break
            self.save()

            self.wordcount()

            Sitemap().build()
            self.build_children()
            VisualSitemap().build()
        elif global_vars.sitemap_xml_file_path.endswith(tuple(".xml")):
            Sitemap().load()
            self.save()
            self.build_children()
            VisualSitemap().build()
        else:
            print("Stopped")
            return
            
    
    def uri_validator(self, x):
                try:
                    result = urlparse(x)
                    return all([result.scheme, result.netloc])
                except:
                    return False

    def crawl(self, u):
        hdr = { 'User-Agent' : 'Mozilla/5.0 (Windows NT 6.1; Win64; x64)' }
        # pprint(vars(u)) # DEBUGG META

        #Validator url 
        #print('URL VALID  : ')
        #print(u.complete_url)
        #print(self.uri_validator(u.complete_url))
        
        #if not self.uri_validator(u.complete_url):
        #        return False
        
        
        try:
            metareq = req.Request(u.complete_url, headers=hdr)
            x = req.urlopen(metareq ).read().decode('utf-8', errors='ignore' ) #, errors='ignore' 
        
            #print(x) #debugg

        except urllib.error.HTTPError as err:
            print(f'A HTTPError was thrown: {err.code} {err.reason}')
            return False
        
        else:
            for s in re.findall('href="(.*?)"', x, re.S):
                u.has_been_crawled = True
                
                # Find Canonical URL for Relative html urls ORF
                if s.endswith('.html'):
                    canonical_url = re.findall('<link\s+rel="canonical"\s+href=["\'](\S+?)["\']' , x)
                    if canonical_url:
                            canonical_url = canonical_url[0].rsplit('/', 1)[0] + '/'
                            s = canonical_url + s
                    else: 
                    
                            print('Not Relative HTML' , s)

                 # MEtaMode PRE If Relative URL /meinSubUrl
                if (global_vars.starting_url not in s) and len(s)>2 and s.startswith('/') :
                    s = global_vars.starting_url + s

                
                #Excluded SUB-DOMAINS
                if any(dom in s for dom in (global_vars.subdom_exclud)):
                    continue

                #Excluded URLs
                if any(sub in s for sub in ('./','mailto:','tel:','{{link}}','data.href','.css', '.js', '.woff2','.png','.jpg','.ico','#', '?', 'javascript')):
                    continue
                
                # Exclude all relative links Joomla Typo
                #if global_vars.starting_url not in s:
                #    continue
                
                # Add to URL List s to List if not already added
                if s not in [url.complete_url for url in global_vars.url_list]:
                    global_vars.url_list.append(URL(s))

    def save(self):
        with open('urls.txt', 'w') as f:
            for val in global_vars.url_list:
                f.writelines(val.complete_url + "\n")
    
    def wordcount(self):
        words=0
        for url in global_vars.url_list:
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

        pass

    def build_children(self):
        pass