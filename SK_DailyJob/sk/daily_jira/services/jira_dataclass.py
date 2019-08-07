from daily_jira.services.jira_basic import JiraMeta
import csv
import inject
from datetime import datetime
import os
from daily_jira.dependencies import Config
from dateutil.parser import parse


config = inject.instance(Config)

jira_status_list = [
    'Backlog', 'Ongoing', 'Developing', 'Developed', 'Testing', 'Tested',
    'Open', 'In Progress', 'Resolved', 'Fixed', 'Closed', 'Done', '', None
    ]


class JiraData(JiraMeta):

    def __init__(self):
        super(JiraData, self).__init__()
        self.init_csv()

    def get_issue_logs(self, issue, issue_type=None):
        issues = self.get_jira_changelog(issue)
        big_change_info = []
        change_logs = issues.get('changelog').get('histories') or None
        if issues:
            if not change_logs:
                created_time = issues['fields']['created']
                author = issues['fields']['creator']['name']
                big_change_info.append([issue,
                                       issue_type,
                                       author,
                                       datetime.strftime(parse(created_time), '%Y-%m-%d %H:%M:%S'),
                                       'Backlog',
                                        ''])
                print(big_change_info)
                return big_change_info

            for changelog in change_logs:
                # if changelog['items'][0]['field'] == 'status':
                author = changelog['author']['name']
                created_time = changelog['created']
                from_string = changelog['items'][0]['fromString']
                to_string = changelog['items'][0]['toString']
                if from_string not in jira_status_list:
                    continue
                if to_string not in jira_status_list:
                    continue
                big_change_info.append([issue,
                                        issue_type,
                                        author,
                                        datetime.strftime(parse(created_time), '%Y-%m-%d %H:%M:%S'),
                                        from_string,
                                        to_string])
        else:
            pass

        print(big_change_info)
        return big_change_info

    @staticmethod
    def init_csv():
        if os.path.exists(config.STORY_CSV_FILE):
            os.remove(config.STORY_CSV_FILE)
        if os.path.exists(config.EFFICIENCY_CSV_FILE):
            os.remove(config.EFFICIENCY_CSV_FILE)
        csv_header = ['ID', 'type', 'author', 'created_time', 'status_from', 'statues_to']
        with open(config.STORY_CSV_FILE, 'w+') as csv_file:
            csv_obj = csv.writer(csv_file)
            csv_obj.writerow(csv_header)
        csv_header = ['ID', 'type', 'author', 'used_time', 'timeoriginalestimate']
        with open(config.EFFICIENCY_CSV_FILE, 'w+') as E_CSV_FILE:
            csv_obj = csv.writer(E_CSV_FILE)
            csv_obj.writerow(csv_header)

    def csv_writer(self, issue, issue_type, issues, file_type=None):
        csv_body = self.get_issue_logs(issue=issue, issue_type=issue_type)
        if csv_body:
            if file_type == 'story':
                with open(config.STORY_CSV_FILE, 'a+') as csv_file:
                    csv_obj = csv.writer(csv_file)
                    csv_obj.writerows(csv_body)
            if file_type == 'efficiency':
                efficiency = self.calculate_efficiency(csv_body, issues)
                with open(config.EFFICIENCY_CSV_FILE, 'a+') as csv_file:
                    csv_obj = csv.writer(csv_file)
                    csv_obj.writerow(efficiency)
            else:
                return False
        return True

    @staticmethod
    def deal_issue(issues):
        bug_list, subtask_list, task_list, story_list, test_list = [], [], [], [], []
        for issue in issues:
            issue_type = issue['fields']['issuetype']['name']
            print(issue_type)
            if issue_type == '故障':
                bug_list.append(issue['key'])
            elif issue_type == '子任务':
                subtask_list.append(issue['key'])
            elif issue_type == '任务':
                task_list.append(issue['key'])
            elif issue_type == '故事':
                story_list.append(issue['key'])
            elif issue_type == 'Test':
                test_list.append(issue['key'])
            else:
                continue
        issue_dict = {'bug': bug_list,
                      'subtask': subtask_list,
                      'task': task_list,
                      'story': story_list,
                      'test': test_list
                      }
        return issue_dict

    @staticmethod
    def calculate_efficiency(csv_body, issues):
        end_time = start_time = '2019-01-01 00:00:00'
        timeoriginalestimate = None
        if csv_body[0][1] == 'bug':
            status_from, status_to = 'In Progress', 'Fixed'
        else:
            status_from, status_to = 'Ongoing', 'Done'
            for story_key in issues:
                if story_key['key'] == csv_body[0][0]:
                    timeoriginalestimate = story_key.get('fields').get('timeoriginalestimate')
                    if timeoriginalestimate:
                        timeoriginalestimate = timeoriginalestimate/3600/8
                    break

        for row_fix in reversed(csv_body):
            if row_fix[5] == status_to:
                end_time = row_fix[3]
                break
        for row_progress in csv_body:
            if row_progress[5] == status_from:
                start_time = row_progress[3]
                break
        print(end_time, start_time)
        end_time = datetime.strptime(end_time, '%Y-%m-%d %H:%M:%S')
        start_time = datetime.strptime(start_time, '%Y-%m-%d %H:%M:%S')
        efficiency_time = end_time - start_time if end_time > start_time else None
        if efficiency_time:
            cross_date = end_time.day - start_time.day
            print(cross_date)
            # efficiency_time = (efficiency_time.seconds - (12*60*60*cross_date)) / 3600
            # print(efficiency_time)

        return [csv_body[0][0], csv_body[0][1], csv_body[0][2], efficiency_time, timeoriginalestimate]




