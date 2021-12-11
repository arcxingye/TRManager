import json,requests,urllib,urllib3,re
from .config import *

# 发送执行命令请求
async def SendTrRequest(alias: str, types: str, req: str):
    exec_url = 'http://' + get_server_info(alias,1) + ':' + get_server_info(alias,2)
    if types == "cmd":
        exec_url += '/v3/server/rawcmd?cmd='+req+'&token='
    elif types == "ban":
        exec_url += '/v2/players/ban?player='+req+'&token='
    elif types == "inv":
        exec_url += '/v3/players/read?player='+req+'&token='
    exec_url += get_server_info(alias,3)
    try:
        r = requests.get(exec_url, timeout=1)
    except:
        return ''
    else:
        return json.loads(r.content)

# 爬物品的wiki图
async def get_wiki_img(name: str):
    _name = urllib.parse.quote(str(name.replace(" ", "_").replace("/", "_")))
    wiki_url = "https://terraria.fandom.com/wiki/"+_name
    try:
        page = urllib.request.urlopen(wiki_url)
    except:
        return ''
    else:
        wiki_html = page.read().decode('utf-8')
        reg = 'src="(https://static.wikia.nocookie.net/terraria_gamepedia/images/.*?)"'
        img_result = re.findall(reg, wiki_html)
        img_url = [s for s in img_result if _name+"." in s][0]
        print(img_url)
        img = urllib3.PoolManager().request('GET', img_url)
        path = "./data/TRMResources/tr_item/"+name+".png"
        with open(path, 'wb') as f:
            f.write(img.data)
        return path

# 爬装备的wiki图
# def get_arm_wiki_img(id:str):
#     wiki_url = "https://terraria.fandom.com/zh/wiki/%E7%89%A9%E5%93%81_ID"
#     try:
#         page = urllib.request.urlopen(wiki_url)
#     except:
#         return ''
#     else:
#         wiki_html = page.read().decode('utf-8')
#         reg = '<td>5117</td>'
#         img_result = re.findall(reg, wiki_html)
#         print(img_result)

# get_arm_wiki_img("2763")