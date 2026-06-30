#!/usr/bin/env python3
"""
Passenger MVP Tracker — GitHub Actions generator
Llama a Jira, embeds los datos en el HTML template, escribe index.html
"""
import os, json, base64, urllib.request, urllib.error, datetime, re

CLOUD_ID   = 'bf2a27a9-2a62-40a9-89c4-9d8eee40e741'
JIRA_BASE  = 'https://grupokinetic.atlassian.net'
EMAIL      = os.environ['JIRA_EMAIL']
TOKEN      = os.environ['JIRA_TOKEN']
CREDENTIALS = base64.b64encode(f'{EMAIL}:{TOKEN}'.encode()).decode()

def jira_search(jql, fields, max_results=100):
    url = f'{JIRA_BASE}/rest/api/3/search'
    payload = json.dumps({
        'jql': jql,
        'fields': fields,
        'maxResults': max_results
    }).encode()
    req = urllib.request.Request(url, data=payload, method='POST', headers={
        'Authorization': f'Basic {CREDENTIALS}',
        'Content-Type': 'application/json',
        'Accept': 'application/json'
    })
    try:
        with urllib.request.urlopen(req) as resp:
            return json.loads(resp.read())
    except urllib.error.HTTPError as e:
        print(f'Jira error {e.code}: {e.read().decode()}')
        return {'issues': []}

def get_sprint_issues():
    result = jira_search(
        jql='project = P224 AND sprint in openSprints() ORDER BY assignee ASC, updated DESC',
        fields=['summary', 'status', 'assignee', 'updated', 'issuetype', 'priority']
    )
    issues = []
    for i in result.get('issues', []):
        issues.append({
            'key': i['key'],
            'webUrl': f"{JIRA_BASE}/browse/{i['key']}",
            'summary': i['fields'].get('summary', ''),
            'status': i['fields'].get('status', {}).get('name', ''),
            'statusCat': i['fields'].get('status', {}).get('statusCategory', {}).get('name', ''),
            'assignee': (i['fields'].get('assignee') or {}).get('displayName', 'Sin asignar'),
            'updated': i['fields'].get('updated', ''),
            'issuetype': i['fields'].get('issuetype', {}).get('name', '')
        })
    return issues

def read_template():
    template_path = os.path.join(os.path.dirname(__file__), 'template.html')
    with open(template_path, 'r', encoding='utf-8') as f:
        return f.read()

def main():
    print('Fetching Jira sprint issues...')
    issues = get_sprint_issues()
    print(f'Got {len(issues)} issues')

    now = datetime.datetime.now(datetime.timezone(datetime.timedelta(hours=-3)))  # ART
    updated_at = now.strftime('%d/%m/%Y %H:%M')
    today_day = 7  # Day 7 = Jun 30 — UPDATE THIS DAILY OR CALCULATE DYNAMICALLY

    # Calculate today's working day dynamically
    working_days = [
        ('2026-06-22', 1), ('2026-06-23', 2), ('2026-06-24', 3),
        ('2026-06-25', 4), ('2026-06-26', 5), ('2026-06-29', 6),
        ('2026-06-30', 7), ('2026-07-01', 8), ('2026-07-02', 9),
        ('2026-07-03', 10), ('2026-07-06', 11), ('2026-07-07', 12),
        ('2026-07-08', 13), ('2026-07-13', 14), ('2026-07-14', 15),
        ('2026-07-15', 16), ('2026-07-16', 17), ('2026-07-17', 18),
    ]
    today_str = now.strftime('%Y-%m-%d')
    for date_str, day_n in working_days:
        if date_str == today_str:
            today_day = day_n
            break

    template = read_template()
    issues_json = json.dumps(issues, ensure_ascii=False)

    output = template \
        .replace('{{ISSUES_JSON}}', issues_json) \
        .replace('{{UPDATED_AT}}', updated_at) \
        .replace('{{TODAY_DAY}}', str(today_day))

    output_path = os.path.join(os.path.dirname(__file__), 'index.html')
    with open(output_path, 'w', encoding='utf-8') as f:
        f.write(output)

    print(f'Generated index.html with {len(issues)} issues. Today = Day {today_day}')

if __name__ == '__main__':
    main()
