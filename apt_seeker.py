#!/usr/bin/python
import urllib2
import BeautifulSoup
import smtplib
import time
import pickle
from email.mime.text import MIMEText
from email.MIMEMultipart import MIMEMultipart
import random
from collections import defaultdict
import csv



class post:
    def __init__(self,the_post, title, url, post_id):
        self.post = the_post
        self.title = title
        self.post_url = url
        self.post_id = post_id
        
    def getPrice(self):
        start = self.title.find(';')
        end = self.title.find('/')
        if start > 0 and end > 0:
            return self.title[start +1:end]
        else:
            return 'No listed Price'
    def getRooms(self):
        start = self.title.find('/')
        end = self.title.find('-')
        if start > 0 and end > 0:
            return self.title[start+1:end]
        else:
            return 'no rooms'

    def getNeiborhood(self):
        start = self.title.find('(')
        if start > 0 :
            return self.title[ start+1: -1 ]
        else:
            return 'No Neiborhood'

    def getPost(self):
        return self.post

    def getTitle(self):
        return self.title

    def get_url(self):
        return self.post_url

    def getpostID(self):
        return self.post_id
    

def send_email(mssg):
    fromaddr = 'andelgado53@gmail.com'
    toaddrs  = ['andelgado53@gmail.com'] #, 'kbreagan@hotmail.com']
    message = MIMEMultipart()
    message['Subject'] = "Let's check out these places!"
    message['From'] = 'Andres Delgado'
    message.attach(MIMEText(mssg))
    username = 'andelgado53@gmail.com'
    password = passw
    server = smtplib.SMTP('smtp.gmail.com:587')
    server.ehlo()
    server.starttls()
    server.login(username,password)
    server.sendmail(fromaddr, toaddrs, message.as_string())
    server.quit()   

def getID(post):
        start = post.find(':')
        post = post[start+1:].strip()
        return post

def add_to_index(index, post):
    clean_words = []
    words_to_avoid = ['a', 'the', 'i', 'we', 'they', 'she',
                      'he', 'in', 'of', 'all', '', 'and',
                      'to','with', 'for', 'is', 'you', 'your', 'at',
                      'on', 'our', 'are', 'or', '&', 'this', 'that',
                      'from', 'an']
    list_of_words = post.getPost().split()
    for word in list_of_words:
        word = word.strip('.,!@#;-$:*)(')
        word = word.strip()
        if word not in words_to_avoid:
            index[word.lower()].append(post.get_url())
        
    #return clean_words
        
        
        

indexes = ['', 'index100.html', 'index200.html', 'index300.html']
message_headers = ['Mo apartments to look at', 'Baby look! I found us a place to live!!! ', "Aren't these nice places to live? baby!! ", "How about them apples?? ", "These look nice! I only hope there isn't any snakes in the bedroom :( "]

nei = 'queen anne'
maxprice = 2000
berrooms = '2b3b'
mssg_body = message_headers[random.randint(0, len(message_headers)-1)]
mssg_len_test = len(mssg_body)
posts_list = []
date_time = set()
id_set = set()
posts_dic = {}
word_index = defaultdict(list)
#passw = open('/home/andres/Documents/code').read()

##try:
##    last_post_time = pickle.load(open('maxdate.p', 'rb'))
##except:
##    last_post_time = 0

for index in indexes:
    
    request = urllib2.urlopen('http://seattle.craigslist.org/apa/{0}'.format(index))
    html = request.read()
    soup = BeautifulSoup.BeautifulSoup(html)
    posts = soup.findAll('p')   
   
   

    for p in posts:
        try:
            post_url = 'http://seattle.craigslist.org' + p.contents[1].attrs[0][1]
            request_post = urllib2.urlopen(post_url)                                   
            post_html = request_post.read()
            post_soup = BeautifulSoup.BeautifulSoup(post_html)
            post_body = post_soup.find('section', id="postingbody").getText().encode('utf-8').lower()
            post_tittle = post_soup.find('h2', "postingtitle").getText().encode('utf-8').lower()
            post_time = post_soup.find('time').getText()
            post_id = post_soup.findAll('p', {'class':"postinginfo"})
            post_id = getID(post_id[1].getText())
            #print(post_id)
            post_time = time.strptime(post_time, '%Y-%m-%d  %I:%M%p')
            post_time = time.mktime(post_time)
            a_post = post(post_body, post_tittle, post_url, post_id)
            posts_dic[a_post.getpostID()] = a_post
        #print(posts_dic.keys())
##        if post_id not in id_set:
##            a_post = post(post_body, post_tittle, post_url, post_id)
##            post_list.append(a_post)
##        if post_time > last_post_time:
##            a_post = post(post_body, post_tittle, post_url) 
##            posts_list.append(a_post)
##            date_time.add(post_time)
        except:
            continue
##try:
##    last_post_time = max(date_time)
##except:
##    last_post_time = last_post_time
##    
##for post in posts_list:
##    if nei in post.getNeiborhood() or nei in post.getPost():
##        mssg_body = mssg_body + '\n\n' + post.getNeiborhood() + ': ' + post.get_url() + ' ,' + post.getRooms() + ', ' + '$' + post.getPrice() + '\n'
##    
##pickle.dump(last_post_time, open('maxdate.p', 'wb'))
##
##if len(mssg_body) > mssg_len_test:
##    send_email(mssg_body)
##else:
##    send_email('No new listings')
for value in posts_dic.values():
    try:
        add_to_index(word_index, value)
    except:
        continue
csvopener = open('C:/Users/delandre/Documents/Documents/Projects/apt_words.csv', 'wb')
wr = csv.writer(csvopener)
wr.writerow(['word', 'count'])
for key in word_index:
    wr.writerow([key, len(word_index[key])])
    #print(key + str(len(word_index[key])))
csvopener.close()
    
