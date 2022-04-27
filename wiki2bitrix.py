from asyncio.proactor_events import _ProactorBaseWritePipeTransport
import json
from pydoc import resolve
from urllib import response
import requests
from bitrix24 import *
import binascii
from codecs import decode


bitrix_url = 'https://rustime.bitrix24.ru/rest/176/p32nxxpgp67v21g3/'

jira_url = 'https://tst-test.atlassian.net/wiki/rest/api/'

jira_auth = 'bnluZWxsZS5kYXZpZG9mZkBnbWFpbC5jb206T1JlcXh3TjdOdW1EZXBzdFM5aEpEQzc5'

headers={'Authorization' : 'Basic ' + jira_auth, 'Content-Type' : 'application/json'}

def get_page(page_id):
    '''Get page by id [page_id]
    '''
    path='content/'+page_id
    query={'expand' : 'body.view'}
    response=requests.get(jira_url + path, params=query, headers=headers)
    j_data=response.json()
    print(json.dumps(j_data, sort_keys=True, ensure_ascii=True, indent=4, separators=(",", ": ")))
    return j_data['body']['view']['value']

def get_space(space_key, offset):
    path='space/' + space_key + '/content'
    query={'limit' : 50, 'start' : offset}
    response=requests.get(jira_url + path, params=query, headers=headers)
    j_data=response.json()
    #print(decode(json.dumps(j_data, sort_keys=True, ensure_ascii=True, indent=4, separators=(",", ": ")),'unicode-escape'))
    return j_data['page']['results']
    
    

def main():
    #print(get_page('1146880'))
    pages={}
    morepages=True
    offset=0
    while morepages:
        r=get_space('GBP',offset)
        for p in r:
            print(p['id'],' - ',p['title'])
            pages[p['id']] = p['title']
        if len(r)<50:
            morepages = False
        offset+=50

    print(len(pages))
    

if __name__=='__main__':
    main()