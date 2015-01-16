import urllib2
import BeautifulSoup
import re
import csv
import time
import pickle


thePostings = {}
indexes= ['', 'index100.html', 'index200.html', 'index300.html']
cities = ['atlanta' , 'austin' ,'boston', 'chicago', 'dallas', 'denver',
          'detroit', 'houston','lasvegas','losangeles', 'miami',
          'minneapolis', 'newyork', 'orangecounty','philadelphia', 'phoenix',
          'portland', 'sacramento', 'sandiego', 'sfbay', 'washingtondc',
          'seattle' ]

newregex = "(\(? ?[2-9] ?[0-9] ?[0-9] ?\)? {0,2}['.-]? ?[0-9] ?[0-9] ?[0-9] ?['.-]? ?[0-9] ?[0-9] ?[-.']?[0-9] ?[-.']?[0-9])"
csvfile = 'C:/Users/delandre/Desktop/resellers_6_25.csv'
#date_time ={}
#citi_times= []

#try:
    #old_timers = pickle.load(open('maxdate.p', 'rb'))
#except:
    #old_timers = {}




def numbcleaner(theNumber):
    if theNumber == 'no num':
        theNumber = 'no num'
               
    else:
        theNumber = theNumber.replace('-', '')
        theNumber = theNumber.replace('(', '')
        theNumber = theNumber.replace(')', '')
        theNumber = theNumber.replace('.', '')
        theNumber = theNumber.replace(' ', '')
        theNumber = theNumber.strip()
    return theNumber

def tmoindicator(post):
    try:
        tmo= re.search('([Tt][- _.]?[Mm]obile)', post)
        tmo= tmo.group(0)
    except:
        tmo = 'Non T-Mobile'
    return tmo

def getPrice(text):
    try:
        price = re.search('(\$[0-9]{1,4}\.?[0-9]?[0-9]?)', text)
        price = price.group(0)

    except:
        price = 'No Price'
    return price

def getphone(post):
    
    try:
        phone = re.search("(\(? ?[2-9] ?[0-9] ?[0-9] ?\)? {0,2}['.-]? ?[0-9] ?[0-9] ?[0-9] ?['.-]? ?[0-9] ?[0-9] ?[-.']?[0-9] ?[-.']?[0-9])", post)
        phone = phone.group(0)
    except:
        phone = 'no num'
    return phone

def cleandate(date):
    try:
        date = date.replace(',', ' ')
        date = date[:-4]
        return date
    except:
        return 'no date'



for city in cities:
    post_cnt = 0
    #date_time.setdefault(city, [])
    
    for index in indexes:
        site = 'http://{0}.craigslist.org/moa/{1}'.format(city, index)

        request = urllib2.urlopen(site)
        html = request.read()
        soup= BeautifulSoup.BeautifulSoup(html)
        #print(soup)
        postings = soup.findAll('p')
        #print(postings)
        
    
   

        for post in postings:
            if post.contents[1].attrs[0][0] =='href':
                #print(post.contents[1].attrs[0][1])
                link = 'http://{0}.craigslist.org'.format(city) + post.contents[1].attrs[0][1]
                #print(link)
                try:
                    postRequest = urllib2.urlopen(link)
                    postHTML= postRequest.read()
                    postSoup= BeautifulSoup.BeautifulSoup(postHTML)
                    d = postSoup.find('section', id="postingbody")
                    date = postSoup.find("time").getText()
                    date = cleandate(date)
                    title = postSoup.find('h2', "postingtitle")
                    #tuple_date = time.strptime(date, '%Y-%m-%d  %I:%M%p')
                    #tick_date = time.mktime(tuple_date)
                    price = getPrice(title.getText())
                    #str_post = str(d)
                    #cleanpost_1 = postcleaner(str_post)
                    cleanpost_1 = d.getText()
                    #print(cleanpost_1)
                except:
                    continue
                phone = getphone(cleanpost_1)
                tmobileInd = tmoindicator(cleanpost_1)
                cleanedPhone = numbcleaner(phone)
            
                
                    
                try:
                    #if tick_date > old_timers[city]:
                    #thePhone = phone.group(0)
                    #cleanedPhone = numbcleaner(thePhone)                   
                    thePostings[cleanpost_1]= (title.getText().encode('utf-8'), cleanedPhone, link, price, city, date, tmobileInd)
                    post_cnt = post_cnt +1
                    #date_time[city].append(tick_date)
                        #print(date_time)
                        #print(thePostings)
                        #print(type(phone.group(0)))
                    #else:
                        #date_time[city].append(tick_date)
                        #continue
            

                except:
                    thePostings[cleanpost_1] = (title.getText().encode('utf-8'), cleanedPhone, link, price, city, date, tmobileInd)
                    post_cnt = post_cnt +1
                    #date_time[city].append(tick_date)
                    continue
    print(city + ' completed: ' + str(post_cnt) + ' posts...')
    #date_time[city] = max(date_time[city])
    
    


csvopener = open(csvfile, 'wb')
wr = csv.writer(csvopener)
wr.writerow([ 'post', 'title', 'number',  'link','price', 'city', 'date','tmo_indicator'])


for poste in thePostings.keys():
    wr.writerow([poste.encode('utf-8'),thePostings[poste][0].encode('utf-8'), thePostings[poste][1].encode('utf-8'), thePostings[poste][2].encode('utf-8'), thePostings[poste][3], thePostings[poste][4], thePostings[poste][5], thePostings[poste][6]])
     

csvopener.close()
#print(date_time)
#pickle.dump(date_time, open('maxdate.p', 'wb'))
#print(old_timers)





