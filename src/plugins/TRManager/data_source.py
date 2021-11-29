import json,requests,urllib,urllib3,re
from .read_ini import get_server_config

# 发送执行命令请求
async def SendTrRequest(alias: str, types: str, req: str):
    exec_url = 'http://' + get_server_config(alias, "ip") + ':' + get_server_config(alias, "rest_port")
    if types == "cmd":
        exec_url += '/v3/server/rawcmd?cmd='+req+'&token='
    elif types == "ban":
        exec_url += '/v2/players/ban?player='+req+'&token='
    elif types == "inv":
        exec_url += '/v3/players/read?player='+req+'&token='
    exec_url += get_server_config(alias, "token")
    try:
        r = requests.get(exec_url, timeout=1)
    except:
        return ''
    else:
        return json.loads(r.content)

# 爬wiki图
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
        img_url = [s for s in img_result if _name in s][0]
        print(img_url)
        img = urllib3.PoolManager().request('GET', img_url)
        path = "./data/images/tr_item/"+name+".png"
        with open(path, 'wb') as f:
            f.write(img.data)
        return path