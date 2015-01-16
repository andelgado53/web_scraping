import requests
import json

def get_sentiment(text):
    datumbox_key = '4e6f2dad931f77ae100cd7924a259f05'
    url= 'http://api.datumbox.com/1.0/TwitterSentimentAnalysis.json'
    para = {'api_key': datumbox_key, 'text': text }
    r = requests.post(url, para)
    json_r = json.loads(r.text)
    return json_r['output']['result']
sent = get_sentiment("too bad been having a lot of fun with the Amazon Prime music ap and prime TV &amp; movies".encode('utf-8'))
print(sent)