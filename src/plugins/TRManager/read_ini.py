import configparser,os

BASE_DIR = os.path.dirname(os.path.abspath(__file__))

# 服务器列表
server_list = configparser.ConfigParser()
server_list.read(os.path.join(BASE_DIR, 'server_list.ini'))
server_alias_list=server_list.sections()
def get_server_config(alias:str,value:str):
    return server_list.get(alias, value)

# 管理员/管理群列表
tr_admin_list = configparser.ConfigParser()
tr_admin_list.read(os.path.join(BASE_DIR, 'config.ini'))
def get_tr_admin(admin:str,type:str):
    return tr_admin_list.get(admin, type)

# 验证权限
def VerifyPermissions(tr_admin: str, types: str):
    for item in tr_admin_list.get("tr_admin", types).split(","):
        if tr_admin == item:
            return True
    return False