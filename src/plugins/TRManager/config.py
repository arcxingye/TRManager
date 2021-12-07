# TR群(只能在这些群用本插件普通指令)
TR_GROUP=[180093493,399915856,728833061]
# TR管理群(只能在这些群用本插件服管命令)，管理群不用填上边，只填下面就行
TR_ADMIN_GROUP=[12345,54321]

# 商店配置：("商品描述","执行的指令",花费积分数)
# 可无限添加商品，续写一定要注意格式和符号
shop_list=[
    ("木材99个","/give 9 [player] 99",2),
    ("爱吃的大嘴巴子","/slap [player] 1",1),
    ("芜湖起飞","/rocket [player]",1),
    ("木板条箱3个","/give 2334 [player] 3",3),
    ("草药袋2个","/give 3093 [player] 2",2),
    ("生命水晶2个","/give 29 [player] 2",4),
]

raffle_list=[] # 这个还没做

# 服务器列表：(服名，服ip，服Rest端口，服RestToken)
# 可无限添加服务器，续写一定要注意格式
# 没事可别截图，防止token泄露
server_list=[
    ("k77","k.thac.cc","64212","token"),
    ("s77","s.thac.cc","12345","test"),
]

# 下面不用管-----------------------------
# 服名称列表:
server_alias_list=[]
for item in server_list:
    server_alias_list.append(item[0])
# 根据服名称获取信息
def get_server_info(alias:str,info:int):
    for item in server_list:
        if alias==item[0]:
            return item[info]
# 验证是否TR群
def VerifyTrGroup(group:str):
    for item in TR_GROUP+TR_ADMIN_GROUP:
        if int(group) == item:
            return True
    return False
# 验证权限群
def VerifyPermissions(group: str):
    for item in TR_ADMIN_GROUP:
        if int(group) == item:
            return True
    return False