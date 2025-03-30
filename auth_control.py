import re
import pandas as pd
import requests
from sqlalchemy import create_engine

def query_CRM_by_pd(
            sql: str,
            server: str,
            database: str,
            username: str,
            password: str
            ):
    """
    使用 SQLAlchemy 连接 SQL Server 数据库，并执行 SQL 查询。
    """
    # 创建连接字符串
    connection_string = f"mssql+pymssql://{username}:{password}@{server}/{database}"

    # 创建引擎
    engine = create_engine(connection_string)

    # 使用 pandas 的 read_sql_query 方法执行 SQL 查询
    df = pd.read_sql_query(sql, con=engine)

    return df

def control_by_leader_relationship(df_user_filter,biz_dept:str,server:str,database:str,username:str,password:str):
    user_uuid_list = df_user_filter['systemuserid'].values.tolist()
    print(user_uuid_list)
    if len(user_uuid_list) > 1:
        print('该用户有多个角色，uuid：{}'.format(','.join([str(x) for x in user_uuid_list])))
    #查询权限内容
    df_user_auth_list = []
    for user_uuid in user_uuid_list:
        sql_user_auth = "select * from fn_GetAISystemuserByUser('{}')".format(user_uuid)
        user_auth = query_CRM_by_pd(sql_user_auth,server,database,username,password)
        df_user_auth_list.append(user_auth)
    df_user_auth = pd.concat(df_user_auth_list)
    return df_user_auth

def control_by_dept(df_filter,biz_dept,server,database,username,password):
    user_uuid_list = df_filter['systemuserid'].values.tolist()
    print(user_uuid_list)
    #查询权限内容
    df_user_auth_list = []
    for user_uuid in user_uuid_list:
        sql_user_auth = "select * from fn_GetAISystemuserByUser('{}')".format(user_uuid)
        user_auth = query_CRM_by_pd(sql_user_auth,server,database,username,password)
        df_user_auth_list.append(user_auth)
    df_user_auth = pd.concat(df_user_auth_list)
    return df_user_auth

def control_role(job_num,biz_dept,server,database,username,password):
    #查询用户权限表
    sql = """
        select new_subcompany_idName --事业部
        ,new_code --工号
        ,fullname --全名
        ,new_functiondepartment --部门
        ,systemuserid 
        from systemuser 
        where IsDisabled=0
    """
    df_user = query_CRM_by_pd(sql,server,database,username,password)
    #筛选人员
    df_user_filter = df_user[df_user['new_code'].astype(str) == str(job_num)]
    dept_list = df_user_filter['new_functiondepartment'].values.tolist()
    if len(dept_list)>1:
        print('存在多个部门：{}'.format(','.join(dept_list)))
    dept = dept_list[0] #需要对多个部门的进行逻辑处理，尤其是其中一个是有营销指挥中心的
    if '营销指挥中心' in dept:
        #特殊人员类别，例如营销指挥中心，读取所属事业部所有数据
        df_dept_filter = df_user[df_user['new_subcompany_idName'].astype(str) == dept]
        df_user_auth = control_by_dept(df_dept_filter,biz_dept,server,database,username,password)
    else:
        #通过上下级筛选权限
        df_user_auth =control_by_leader_relationship(df_user_filter,biz_dept,server,database,username,password)
    #特殊高层，含多个事业部权限
    return df_user_auth

def account_auth_control(job_num,biz_dept,account_name,server,database,username,password):
    df_control_role = control_role(job_num,biz_dept,server,database,username,password)
    systemuserName_list = df_control_role['fullname'].drop_duplicates().values.tolist()
    systemuserName_limit="'" + "','".join(systemuserName_list) + "'"
    systemuserid_list = df_control_role['systemuserid'].drop_duplicates().values.tolist()
    systemuserid_limit="'" + "','".join(systemuserid_list) + "'"
    sql = """
        select *
        from account
        where OwnerId in ({})
    """.format(systemuserid_limit)
    df_account = query_CRM_by_pd(sql,server,database,username,password)
    #可查看客户id和客户名称
    account_reachable_id_list = df_account['AccountId'].values.tolist()
    account_reachable_name_list = df_account['Name'].values.tolist()
    if account_name in account_reachable_name_list:
        return True,account_name
    else:
        return False,'您无查看{}的权限'.format(account_name)


if __name__ == '__main__':
    #用户信息
    job_num = 'B12939'
    biz_dept = '板带事业部'
    server = '10.10.10.8'
    database = 'BowayCRM_MSCRM'
    username = 'yxai_read'
    password = 'Yxai01PAssW0rd'
    account_name = '泰科电子（苏州）有限公司'
    result = account_auth_control(job_num,biz_dept,account_name,server,database,username,password)
    print(result)
    