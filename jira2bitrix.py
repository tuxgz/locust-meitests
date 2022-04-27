import json
from pydoc import resolve
from urllib import response
import requests
from bitrix24 import *

bitrix_url = 'https://rustime.bitrix24.ru/rest/176/p32nxxpgp67v21g3/'

bx24 = Bitrix24(bitrix_url)

jira_url = 'https://tst-project.atlassian.net/rest/api/2/'

jira_auth = 'd2ViNDdAeWFuZGV4LnJ1OndUZ1JKOEE0cHZ1UG04QTlwSUtJQzkxMA=='

def transofm_data(data, transform):
    result = {}
    for list in data:
        result[transform[list]] = data[list]
    return(result)

def get_tasks_from_bitrix():
    response=requests.get(bitrix_url + 'tasks.task.get?taskId=4288')
    #response=requests.get(bitrix_url + 'tasks.task.getFields')
    print(response.status_code)
    print(response.content)

def get_tasks_from_jira(page):
    path ='search'
    query={ 'jql' : 'project = TST', 'fields' : 'created,updated', 'maxResults' : 60, 'startAt': page*60}
    response=requests.get(jira_url + path, params=query, headers={'Authorization' : 'Basic ' + jira_auth, 'Content-Type' : 'application/json'})
    print(response.status_code)
    j_data=json.loads(response.text)
    print(j_data['total'])
    #print(json.dumps(json.loads(response.text), sort_keys=True, indent=4, separators=(",", ": ")))
    return(j_data['issues'])

def get_data_from_jira(key):
    path='issue/'+key
    query='*all'
    response=requests.get(jira_url+path, params=query, headers={'Authorization' : 'Basic ' + jira_auth, 'Content-Type' : 'application/json'})
    j_data=json.loads(response.text)
    print(json.dumps(json.loads(response.text), sort_keys=True, indent=4, separators=(",", ": ")))
    return(j_data)

def create_task(j_data):
    title = '[' + j_data['key'] + '] '+ j_data['fields']['summary']
    try:
        bx24.callMethod('tasks.task.add', fields={'TITLE': title, 'PARENT_ID': 4288, 'RESPONSIBLE_ID' : 176})
    except BitrixError as message:
        print(message)
    pass

def main():
    #create_task('1')
    #get_tasks_from_bitrix()
    for i in range(0,1,1):
        issues=get_tasks_from_jira(i)
        for issue in issues:
            print(issue['key'])
            create_task(get_data_from_jira(issue['key']))

    pass

if __name__=='__main__':
    main()
    