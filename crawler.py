import re
import urllib.request as req
import global_vars
from url import URL
from sitemap import Sitemap
from visual_sitemap import VisualSitemap
from pprint import pprint




class Crawler(object):
    def __init__(self):
        pass

    def run(self):
        if not global_vars.sitemap_xml_file_path:
            self.crawl(URL(global_vars.starting_url))
            for u in global_vars.url_list:
                if not u.has_been_crawled:
                    self.crawl(u)
                #if len(global_vars.url_list) >= 512:
                if len(global_vars.url_list) >= global_vars.urls_tocrawl:    
                    break
            self.save()
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
            

    def crawl(self, u):
        hdr = { 'User-Agent' : 'Mozilla/5.0 (Windows NT 6.1; Win64; x64)' }
        
        # pprint(vars(u)) # DEBUGG META
        metareq = req.Request(u.complete_url, headers=hdr)

        x = req.urlopen(metareq ).read().decode('utf-8', errors='ignore')
        
        #print(x) #debugg

        for s in re.findall('href="(.*?)"', x, re.S):
            u.has_been_crawled = True
            
            # MEtaMode PRE If Relative URL /meinSubUrl
            if (global_vars.starting_url not in s) and len(s)>2 and s.startswith('/') :
                s = global_vars.starting_url + s

            
            #print("S-ulr : " +s) #DEBUGG
            
            if any(sub in s for sub in ('.css', '.js', '.woff2','.png','.jpg','.ico','//','#', '?', 'javascript')):
                continue
            
            # Exclude all relative links Joomla Typo
            if global_vars.starting_url not in s:
                continue
            
            # BUG DUBLICATE Add URL s to List if not already added
            if s not in [url.complete_url for url in global_vars.url_list]:
                global_vars.url_list.append(URL(s))

    def save(self):
        with open('urls.txt', 'w') as f:
            for val in global_vars.url_list:
                f.writelines(val.complete_url + "\n")

    def build_children(self):
        pass