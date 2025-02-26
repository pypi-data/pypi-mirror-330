from jira import JIRA
import re

def get_jira_info(jira_user, jira_api_key):
    """
    获取jira对象
    @return:
    """
    # api_key = "ATATT3xFfGF0JPzR4t2coi53yM2eKZfUy5eXJSbZHqWmbX9PzStyaNCM2lEjn_uP5TkOl_p4pqZCICH5ZqdWkdmfSxJmTsn6AOcU7I3vVWnDl0i1PRktMdSSqWs1yg1JVSVtlGCrMKfZaztsJOjAQsp3Jd6hHdKpB4A4nVBBkmB7sDOpsNbTNeY=910B5249"

    # Jira 服务器的 URL
    jira_url = "https://shopline.atlassian.net/"
    # # Jira API 密钥
    # jira_api_key = api_key
    # # Jira 用户名
    # jira_user = "lu.lu@shopline.com"

    # 连接到 Jira 服务器
    jira = JIRA(server=jira_url, basic_auth=(jira_user, jira_api_key))
    return jira


def get_jira_prodcut(jira, project_key):
    project = jira.project(str(project_key))
    print(f"Project: {project.key} - {project.name}")
    return project


def get_custom_fields(jira_obj, project_key='10559'):
    """
    查询指定项目jira中的自定义字段，smartpush项目是 10559
    @param project_id: 项目id
    @param jira_obj: 对象
    @return:
    """
    all_fields = jira_obj.fields()
    # print("all_fields:",all_fields)
    custom_fields = {}
    for field in all_fields:
        try:
            if field.get('custom'):
                if field['scope']['project']['id'] == str(project_key):
                    custom_fields[field['id']] = field['name']
        except:
            continue
    print("custom_fields:", custom_fields)
    return custom_fields


def get_custom_fields_map(jira, project_key=10559):
    # 获取项目的问题
    issues = jira.search_issues(f"project={project_key}")
    issue = jira.issue(issues[0])
    custom_fields = get_custom_fields(jira, project_key)
    print(custom_fields)
    fields_map = {}
    for field_name, field_value in issue.fields.__dict__.items():
        try:
            if field_name.startswith("customfield_"):
                fields_map[custom_fields[field_name]] = field_value
                print(f"Custom Field ID: {field_name}, NAME:{custom_fields[field_name]}, Value: {field_value}")
            else:
                fields_map[field_name] = field_value
                print(f"ID: {field_name},Value: {field_value}")
        except:
            # raise
            continue
    print('fields_map:',fields_map)
if __name__ == '__main__':
    api_key = "ATATT3xFfGF0JPzR4t2coi53yM2eKZfUy5eXJSbZHqWmbX9PzStyaNCM2lEjn_uP5TkOl_p4pqZCICH5ZqdWkdmfSxJmTsn6AOcU7I3vVWnDl0i1PRktMdSSqWs1yg1JVSVtlGCrMKfZaztsJOjAQsp3Jd6hHdKpB4A4nVBBkmB7sDOpsNbTNeY=910B5249"
    # Jira 用户名
    jira_user = "lu.lu@shopline.com"
    jira = get_jira_info(jira_user, api_key)
    get_custom_fields_map(jira)
