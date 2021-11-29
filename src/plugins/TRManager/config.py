# TR管理群，在这些群里的人才能用管理命令
TR_ADMIN_GROUP=[12345,54321]

# 商店配置：商店列表id，物品名，物品id，物品数量，兑换所需分数
# 可无限添加商品，续写一定要注意格式
shop_list=[
    (1,"生命水晶",1291,2,3),
    (2,"木材",9,99,1)
]

# 服务器列表：服名，服ip，服rest端口，服token
# 可无限添加服务器，续写一定要注意格式
server_list=[
    ("服名","ip","restapi端口","token"),
    ("s77","s.thac.cc","12345","test")
]

# 下面不用管--------------
# 服名称列表:
server_alias_list=[]
for item in server_list:
    server_alias_list.append(item[0])
# 根据服名称获取信息
def get_server_info(alias:str,info:int):
    for item in server_list:
        if alias==item[0]:
            return item[info]
# 验证权限
def VerifyPermissions(tr_admin: str):
    for item in TR_ADMIN_GROUP:
        if int(tr_admin) == item:
            return True
    return False