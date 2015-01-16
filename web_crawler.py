import BeautifulSoup
import urllib2




def get_all_links(page):
    links =[]
    request = urllib2.urlopen(page)
    html = request.read()
    soup = BeautifulSoup.BeautifulSoup(html)
    p = soup.findAll('a')
    for link in p:
        if link.attrs[0][0] == 'href':        
            links.append(link.attrs[0][1].encode('utf-8'))
    return links


def crawl(seed):
    to_crawl = [seed]
    crawled = []
    while to_crawl:
        page = to_crawl.pop()
        if page not in crawled:
            crawled.append(page)
            union(get_all_links(page), to_crawl)
            
    return crawled
    
def union(l1, l2):
    for x in l1:
        if x not in l2:
            l2.append(x)


def get_target(page):
    html = page
    index = html.find('a href=')
    if index < 0 :
        return None, None
    else:    
        quote_start = html.find('"', index)
        quote_end = html.find('"', quote_start+1)
        #print(html[quote_start+1:quote_end])
        link = html[quote_start+1:quote_end]
        new_index = quote_end
        return (link, quote_end)



def print_all_links(html):    
    n= 0
    while True:
        link, n = get_target(html)
        if n is None:
            break    
        print(link)
        html = html[n:]
#print_all_links(html)
    
    
print(crawl('https://www.udacity.com/cs101x/index.html'))


