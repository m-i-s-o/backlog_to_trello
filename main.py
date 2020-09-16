import datetime
import json
import os
import requests

ENV = os.getenv('ENV')  # DEV / PROD

T_API_KEY = os.getenv('T_API_KEY')
T_API_TOKEN = os.getenv('T_API_TOKEN')
T_MEMBER_ID = os.getenv('T_MEMBER_ID')
T_BOARD_ID = os.getenv(f'{ENV}_T_BOARD_ID')
T_LIST_ID = os.getenv(f'{ENV}_T_LIST_ID')

B_API_KEY = os.getenv('B_API_KEY')
B_URL_BASE = os.getenv('B_URL_BASE')
B_PROJECT_KEY = os.getenv('B_PROJECT_KEY')
B_PROJECT_ID = int(os.getenv('B_PROJECT_ID'))
B_STATUS_ID = int(os.getenv('B_STATUS_ID'))
B_STORY_TYPE_ID = int(os.getenv('B_STORY_TYPE_ID'))


def get(url, param):
    res = requests.get(url, param)
    res.raise_for_status()

    return res.json()


def post(url, param):
    res = requests.post(url, param)
    res.raise_for_status()


def get_backlog_issues():
    lastweek = datetime.date.today() - datetime.timedelta(weeks=1)
    lastweek_str = lastweek.strftime('%Y-%m-%d')

    param = {
        "apiKey": B_API_KEY,
        "projectId[]": [B_PROJECT_ID],
        "statusId[]": [B_STATUS_ID],
        "issueTypeId[]": [B_STORY_TYPE_ID],
        "updatedSince": lastweek_str
    }
    issues = get(f'{B_URL_BASE}/api/v2/issues', param)

    return issues


def filter_issues(issues):
    if not issues:
        return

    BACKLOG_PROJECT_URL = f'{B_URL_BASE}/view/{B_PROJECT_KEY}'
    doing_issues = []
    for issue in issues:
        card = {
            "name": issue['summary'],
            "desc": issue['description'] + '\n\n課題URL：' + f'{BACKLOG_PROJECT_URL}-{issue["keyId"]}',
            "due": issue['dueDate'][:10] if issue['dueDate'] else None
        }
        doing_issues.append(card)
    
    return doing_issues


def create_trello_cards(doing_issues):
    if not doing_issues:
        return

    url = 'https://trello.com/1/cards/'
    param = {
        "key": T_API_KEY,
        "token": T_API_TOKEN,
        "idList": [T_LIST_ID],
        "idMembers": [T_MEMBER_ID],
        "pos": 'top'
    }

    for card in doing_issues:
        card.update(param)
        post(url, card)


def main(event, _):
    issues = get_backlog_issues()
    doing_issues = filter_issues(issues)
    create_trello_cards(doing_issues)
