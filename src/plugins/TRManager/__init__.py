from nonebot import on_keyword, on_command
from nonebot.adapters import Bot, Event
from nonebot.adapters.onebot.v11.permission import PRIVATE, GROUP
import urllib,os,re,random,math
from datetime import datetime
from .model import *
from .config import *
from .data_source import SendTrRequest,get_wiki_img
from .syn_img import synInv

admin_menu_list="执行<服名> /<命令>\n" \
    "全服执行 /<命令>\n" \
    "<服名> !ban <名字>\n" \
    "trban <qq> <理由>\n" \
    "bandel <qq>\n" \
    "qq查tr <qq>\n" \
    "tr查qq <服名> <名字>\n" \
    "删号 <服名> <名字>\n" \
    "改分 <qq> <分> <天>"
tr_menu_list="<服名>在线\n" \
    "全服在线\n" \
    "<服名> inv <名字>\n" \
    "<服名> arm <名字>\n" \
    "wiki <内容>\n" \
    "trqd\n" \
    "baka值\n" \
    "baka超商\n" \
    "看baka"

# 服管菜单
admin_menu = on_command("服管菜单", priority=5, permission=GROUP)
@admin_menu.handle()
async def admin_menu_(bot: Bot, event: Event, state: T_State):
    if VerifyPermissions((str(event.get_session_id()).split("_"))[1]):
        await admin_menu.send(admin_menu_list)

# tr菜单
tr_menu = on_command("tr菜单", priority=5, permission=GROUP)
@tr_menu.handle()
async def tr_menu_(bot: Bot, event: Event):
    if VerifyTrGroup((str(event.get_session_id()).split("_"))[1]):
        await tr_menu.send(tr_menu_list)

# 泰拉瑞亚wiki查询
tr_wiki = on_command("wiki", priority=5, permission=GROUP)
@tr_wiki.handle()
async def tr_wiki_(bot: Bot, event: Event, state: dict):
    if VerifyTrGroup((str(event.get_session_id()).split("_"))[1]):
        await tr_wiki.send("https://searchwiki.biligame.com/tr/index.php?search="+urllib.parse.quote(str(event.message)))

# 单服在线查询
tr_online = on_keyword([i + "在线" for i in server_alias_list], priority=5, permission=GROUP)
@tr_online.handle()
async def tr_online_(bot: Bot, event: Event):
    if VerifyTrGroup((str(event.get_session_id()).split("_"))[1]):
        server_online = (await SendTrRequest((str(event.get_message()).strip()).replace("/","").replace("在线",""), "cmd", "/playing"))
        if server_online:
            if server_online['status'] == '200':
                server_online = ('\n'.join(server_online['response'])).replace(r"Online Players", "在线玩家")
            else:
                server_online = "响应错误~ err 2"
        else:
            server_online = "你要查询的服爆炸了~ err 1"
        await tr_online.send(server_online)

# 全服在线查询
all_online = on_command("全服在线", priority=5, permission=GROUP)
@all_online.handle()
async def all_online_(bot: Bot, event: Event):
    if VerifyTrGroup((str(event.get_session_id()).split("_"))[1]):
        all = ''
        num = []
        total = 0
        for item in server_alias_list:
            single_online = await SendTrRequest(item, "cmd", "/playing")
            if single_online:
                if single_online['status'] == '200':
                    if(len(single_online['response']) >= 2):
                        all += (item+">"+str(single_online['response'][0]) +":"+str(''.join(single_online['response'][1:])) + "\n")
                        num.append(re.findall('\d+', str(re.findall(r"Online Players (.*.+?)/", str(single_online['response']))))[0])
                    elif(len(single_online['response']) == 1):
                        all += (item+">"+str(single_online['response'][0])+"没人~\n")
                    else:
                        all += (item+">未响应所需内容~ err 3\n")
                else:
                    all += (item+">响应错误~ err 2\n")
            else:
                all += (item+">爆炸了~ err 1\n")
        for i in range(0, len(num)):
            total = total + int(num[i])
        await all_online.send("当前全服在线总计"+str(total)+"人\n" + all.replace("Online Players ", "").replace("There are currently no players online.","").strip('\n'))

# 单服执行指令
single_exec = on_keyword(["执行" + i for i in server_alias_list], priority=5, permission=GROUP)
@single_exec.handle()
async def single_exec_(bot: Bot, event: Event):
    command=str(event.get_message()).split(" ")
    if len(command) > 1:
        if VerifyPermissions((str(event.get_session_id()).split("_"))[1]):
            server=command[0].replace("执行","")
            exec_cmd=' '.join(command[1:])
            server_exec_result = await SendTrRequest(server, "cmd", exec_cmd.strip())
            if server_exec_result:
                if server_exec_result['status'] == '200':
                    server_exec_result = '\n'.join(server_exec_result['response'])
                else:
                    server_exec_result = "响应错误~ err 2"
            else:
                server_exec_result = "你要执行的服爆炸了~ err 1"
            await single_exec.send(server_exec_result)

# 全服执行
all_exec = on_command("全服执行", priority=5, permission=GROUP)
@all_exec.handle()
async def all_exec_(bot: Bot, event: Event):
    if VerifyPermissions((str(event.get_session_id()).split("_"))[1]):
        all_result = ''
        for item in server_alias_list:
            single_result = await SendTrRequest(item, "cmd", str(event.message).strip())
            if single_result:
                if single_result['status'] == '200':
                    all_result += (item+">" + ''.join(single_result['response'])+"\n")
                else:
                    all_result += (item+">响应错误~ err 2\n")
            else:
                all_result += str(item+">爆炸了~ err 1\n").strip('\n')
        await all_exec.send(all_result)

# 执行ban
tr_cmd_ban = on_keyword([i + " !ban" for i in server_alias_list], priority=5, permission=GROUP)
@tr_cmd_ban.handle()
async def tr_cmd_ban_(bot: Bot, event: Event):
    command=str(event.get_message()).split(" ")
    if len(command) > 2:
        if VerifyPermissions((str(event.get_session_id()).split("_"))[1]):
            server=command[0].replace("/","")
            name=' '.join(command[2:])
            server_exec_result = await SendTrRequest(server, "ban", name)
            if server_exec_result:
                if server_exec_result['status'] == '200':
                    server_exec_result = server_exec_result['response']
                else:
                    server_exec_result = "响应错误~ err 2"
            else:
                server_exec_result = "你要执行的服爆炸了~ err 1"
            await tr_cmd_ban.send(server_exec_result)

# 查背包
tr_inv = on_keyword([i + " inv" for i in server_alias_list], priority=5, permission=GROUP)
@tr_inv.handle()
async def tr_inv_(bot: Bot, event: Event):
    command=str(event.get_message()).split(" ")
    if len(command) > 2:
        if VerifyTrGroup((str(event.get_session_id()).split("_"))[1]):
            server=command[0].replace("/","")
            name=' '.join(command[2:])
            result = await SendTrRequest(server, "inv", name)
            if result:
                if result['status'] == '200':
                    server_inv_result = result['inventory']
                    s1 = []
                    s2 = []
                    s3 = []
                    for item in (str(server_inv_result).split(", ")):
                        data = item.split(":")
                        s1.append(data[0]),
                        s2.append(data[1])
                    for item in s1:
                        if item:
                            tr_item_path="./data/TRMResources/tr_item/"+item+".png"
                            if os.path.exists(tr_item_path):
                                s3.append(tr_item_path)
                            else:
                                s3.append((await get_wiki_img(item)))
                        else:
                            s3.append('')
                    inv_result = await synInv(s3,s2,result['nickname'])
                    if inv_result:
                        test=str(os.path.abspath(inv_result)).replace(r'\\',r'/')
                        server_inv_result = [{
                            "type": "image",
                            "data": {
                                "file": "file:///"+test
                            }
                        }]
                    else:
                        server_inv_result = "查询处理失败，请重试"
                else:
                    server_inv_result = "你要找的人在"+server+"神隐了~ err 2"
            else:
                server_inv_result = "你要执行的服爆炸了~ err 1"
            await tr_inv.send(server_inv_result)

# 查装备
tr_arm = on_keyword([i + " arm" for i in server_alias_list], priority=5, permission=GROUP)
@tr_arm.handle()
async def tr_arm_(bot: Bot, event: Event):
    command=str(event.get_message()).split(" ")
    if len(command) > 2:
        if VerifyTrGroup((str(event.get_session_id()).split("_"))[1]):
            server=command[0].replace("/","")
            name=' '.join(command[2:])
            server_inv_result = await SendTrRequest(server, "inv", name)
            if server_inv_result:
                if server_inv_result['status'] == '200':
                    server_inv_result = server_inv_result['armor']
                    await tr_arm.send(server_inv_result)

# 群聊注册提示
tr_tip_reg=on_command("注册", priority=5, permission=GROUP)
@tr_tip_reg.handle()
async def tr_tip_reg_(bot: Bot, event: Event):
    if VerifyTrGroup((str(event.get_session_id()).split("_"))[1]):
        text=["私聊啊╮(╯▽╰)╭","会不会私聊？","别在群里说，来私聊"]
        await tr_tip_reg.send(text[random.randint(0,len(text)-1)])

# 执行注册
tr_exec_reg = on_command("注册", priority=4, permission=PRIVATE)
@tr_exec_reg.handle()
async def tr_exec_reg_(bot: Bot, event: Event):
    if VerifyTrGroup(str(event.sender.group_id)) or VerifyPermissions(str(event.sender.group_id)):
        command=str(event.get_message()).strip().split(" ")
        if len(command)==3:
            server=command[0].replace("注册","").replace("/","")
            username=command[1]
            password=command[2]
            # 验证是否有空值
            if server and username and password:
                VerifyBan=get_tr_isban(event.get_user_id())
                # 验证QQ是否被封禁
                if not VerifyBan:
                    result=False
                    for item in server_alias_list:
                        if server==item:
                            result=await SendTrRequest(item, "cmd", "/playing")
                    if result:
                        reged=get_tr_reged(int(event.get_user_id()),server)
                        #验证是否已注册
                        if not reged:
                            if re.search("^[\u4e00-\u9fa5_a-zA-Z0-9]+$", username, flags=0):
                                exec_result=await SendTrRequest(server, "cmd", "/user add "+username+" "+password+" default")
                                if exec_result:
                                    if exec_result['response'][0]=="User "+username+" already exists!":
                                        await tr_exec_reg.send("该服id:"+username+"已存在，请尝试使用其他名字")
                                    elif exec_result['response'][0]=="Account "+username+" has been added to group default!":
                                        insert_result=tr_add_user(event.get_user_id(),server,username)
                                        if insert_result:
                                            await tr_exec_reg.send("已完成")
                                        else:
                                            del_result=await SendTrRequest(server, "cmd", "/user del "+username)
                                            await tr_exec_reg.send("失败了，请截图私聊服管进行相应处理")
                                            for group in TR_ADMIN_GROUP:
                                                await bot.send_group_msg(
                                                    group_id=int(group),
                                                    message=event.get_user_id()+"在"+server+"reg"+username+"失败,请注意可能需要删除该账号，返回"+str(del_result),
                                                )
                                    else:
                                        await tr_exec_reg.send("reg失败")
                                        for group in TR_ADMIN_GROUP:
                                            await bot.send_group_msg(
                                                group_id=int(group),
                                                message=event.get_user_id()+"在"+server+"reg"+username+"失败"+str(exec_result['response']),
                                            )
                            else:
                                await tr_exec_reg.send("名包含中文英文数字下划线以外的字符，请重新输入")
                        else:
                            await tr_exec_reg.send("你已在"+server+"整过了，一人一服一号~")
                    else:
                        await tr_exec_reg.send("服名不存在或没在开，请重新输入")
                else:
                    await tr_exec_reg.send("你已被封禁，无法进行操作。理由:"+VerifyBan[0][2])
            else:
                await tr_exec_reg.send("命令中存在空值")
        else:
            await tr_exec_reg.send("指令格式不正确，看看公告吧")

# 查询qq号:
tr_qq = on_command("tr查qq", priority=5, permission=GROUP)
@tr_qq.handle()
async def tr_qq_(bot: Bot, event: Event):
    command=str(event.get_message()).strip().split(" ")
    if len(command) > 1:
        if VerifyPermissions((str(event.get_session_id()).split("_"))[1]):
            server=command[0]
            name=' '.join(command[1:])
            result=get_tr_qq(server,name)
            if result:
                await tr_qq.send(str(result[0][1]))
            else:
                await tr_qq.send("没有记录")

# 查询tr号:
qq_tr = on_command("qq查tr", priority=5, permission=GROUP)
@qq_tr.handle()
async def qq_tr_(bot: Bot, event: Event):
    if VerifyPermissions((str(event.get_session_id()).split("_"))[1]):
        result=get_qq_tr(str(event.get_message()).strip())
        if result:
            msg=''
            for item in result:
                msg+=item[2]+"->"+item[3]+"\n"
            await qq_tr.send(msg)
        else:
            await qq_tr.send("没有记录")

# 删除单个服角色
userdel = on_command("删号", priority=5, permission=GROUP)
@userdel.handle()
async def userdel_(bot: Bot, event: Event):
    command=str(event.get_message()).strip().split(" ")
    if len(command) > 1:
        if VerifyPermissions((str(event.get_session_id()).split("_"))[1]):
            server=command[0]
            name=' '.join(command[1:])
            sql_result=tr_del_char(str(server),str(name))
            if sql_result:
                await userdel.send("删除完成")
            else:
                await userdel.send("删除失败")    

# 加入黑名单
add_ban = on_command("trban", priority=5, permission=GROUP)
@add_ban.handle()
async def add_ban_(bot: Bot, event: Event):
    command=str(event.get_message()).strip().split(" ")
    if len(command)>1:
        if VerifyPermissions((str(event.get_session_id()).split("_"))[1]):
            result=tr_add_ban(int(command[0]),str(command[1]))
            if result:
                #全服删除账号
                user_list=get_qq_tr(int(command[0]))
                if user_list:
                    user=[]
                    server=[]
                    msg=''
                    for x in user_list:
                        user.append(x[3])
                        server.append(x[2])
                    i=0
                    for y in server:
                        exec_result=await SendTrRequest(y,"cmd","/user del "+user[i])
                        i+=1
                        if exec_result["response"][0]=="Account removed successfully.":
                            msg+=y+"删除账号成功\n"
                        else:
                            msg+=y+"删除账号失败\n"
                    sql_result=tr_del_user(int(command[0]))
                    if sql_result:
                        await add_ban.send(msg+"插件数据库中删除[成功]，请注意如有服务器未删除成功的账号，需要服管手动去清除")
                    else:
                        await add_ban.send(msg+"插件数据库中删除[失败]，请注意如有服务器未删除成功的账号，需要服管手动去清除")
                else:
                    await add_ban.send("加入黑名单成功，但是插件数据库中没有该qq reg的记录")
            else:
                await add_ban.send("操作失败")

# 删除黑名单
bandel = on_command("bandel", priority=5, permission=GROUP)
@bandel.handle()
async def bandel_(bot: Bot, event: Event):
    if VerifyPermissions((str(event.get_session_id()).split("_"))[1]):
        result=tr_del_ban(int(str(event.get_message()).strip()))
        if result:
            await bandel.send("解除黑名单成功")
        else:
            await bandel.send("解除黑名单失败")

# 签到
sign_in = on_command("trqd", aliases={"tr签到"}, priority=5, permission=GROUP)
@sign_in.handle()
async def sign_in_(bot: Bot, event: Event):
    if VerifyTrGroup((str(event.get_session_id()).split("_"))[1]):
        result=tr_sign_in(event.get_user_id())
        if result:
            if result[0][2]>=0:
                time_dif=(datetime.now()-datetime.strptime(str(result[0][4]),"%Y-%m-%d")).days
                if time_dif>0:
                    # 时间相差为1天时判定为连续签到
                    if time_dif==1:
                        count=result[0][3]+1
                    else:
                        count=0
                    add_score=1
                    #连续签到阶段奖励
                    if count<3:
                        add_score=random.randint(1,3)
                    elif count==3:
                        add_score=random.randint(2,4)
                    elif count>=5:
                        add_score=random.randint(3,5)
                    elif count>=7:
                        add_score=random.randint(4,6)
                    score_add=tr_update_score(event.get_user_id(),int(result[0][2])+add_score,count)
                    if score_add:
                        await sign_in.send("baka值"+str(result[0][2])+"+"+str(add_score)+"连"+str(count)+"天")
                    else:
                        await sign_in.send("败惹")
                else:
                    await sign_in.send("你已经变成baka了~请明天再来叭")
            else:
                await sign_in.send("获取失败")
        else:
            score_add=tr_create_score(event.get_user_id(),1,0)
            if score_add:
                await sign_in.send("baka值+1")
            else:
                await sign_in.send("败惹")

# 查询积分
query_score = on_command("baka值", priority=5, permission=GROUP)
@query_score.handle()
async def query_score_(bot: Bot, event: Event):
    if VerifyTrGroup((str(event.get_session_id()).split("_"))[1]):
        if len(str(event.get_message()))==0:
            result=tr_sign_in(int(event.get_user_id()))
            if result:
                if result[0][2]>=0:
                    await query_score.send("现"+str(result[0][2])+"baka值连"+str(result[0][3])+"天")
                else:
                    await query_score.send("获取失败")
            else:
                await query_score.send("未找到，先来报道吧。/trqd")
        elif len(str(event.get_message()))>0:
            result=tr_sign_in(int(str(event.get_message())))
            if result:
                if result[0][2]>=0:
                    await query_score.send("TA现"+str(result[0][2])+"baka值连"+str(result[0][3])+"天")
                else:
                    await query_score.send("获取失败")
            else:
                await query_score.send("未找到")

# 积分排行榜
score_top = on_command("看baka", priority=5, permission=GROUP)
@score_top.handle()
async def score_top_(bot: Bot, event: Event):
    if VerifyTrGroup((str(event.get_session_id()).split("_"))[1]):
        result=tr_score_top()
        if result:
            msg=""
            i=1
            for item in result:
                msg+=str(i)+"."+str(item[1])+"->"+str(item[2])+"\n"
                i+=1
            await score_top.send(msg+"前10的大baka们")
        else:
            await score_top.send("获取失败")

# 改分
set_score = on_command("改分", priority=5, permission=GROUP)
@set_score.handle()
async def set_score_(bot: Bot, event: Event):
    command=str(event.get_message()).strip().split(" ")
    if len(str(command)) > 3:
        if VerifyPermissions((str(event.get_session_id()).split("_"))[1]):
            result=tr_update_score(int(command[0]),int(command[1]),int(command[2]))
            if result:
                await set_score.send("更新成功")
            else:
                await set_score.send("更新失败")

# tr商店
tr_shop = on_command("baka超商", priority=5, permission=GROUP)
@tr_shop.handle()
async def tr_shop_(bot: Bot, event: Event):
    if VerifyTrGroup((str(event.get_session_id()).split("_"))[1]):
        if event.get_message():
            page=int(str(event.get_message()).strip())
        else:
            page=1
        title="下面是可以换的东西~\n"
        num=10 # 每页数量
        goods='' # 单个项目
        count=len(shop_list)
        total=math.ceil(count/num)
        start=(page-1)*num
        end=page*num
        if page==total:
            end=start+count%num
        elif page>total:
            await tr_shop.finish("一共就"+str(total)+"页")
        elif page<0:
            await tr_shop.finish("你TM负数页码都整出来了是吧")
        for i in range(start,end):
            goods+=str(start+1)+"."+shop_list[i][0]+" "+str(shop_list[i][2])+"baka\n"
            start+=1
        page_list=''
        for j in range(0,total):
            if page-1==j:
                page_list+=">"+str(j+1)+" "
            else:
                page_list+=str(j+1)+" "
        tips="\n/tr换 <服名> <角色> <商品序号>"
        await tr_shop.send(title+goods+page_list+tips)

# tr兑换
tr_buy = on_command("tr换", priority=5, permission=GROUP)
@tr_buy.handle()
async def tr_buy_(bot: Bot, event: Event):
    if VerifyTrGroup((str(event.get_session_id()).split("_"))[1]):
        command=str(event.get_message()).strip().split(" ")
        if len(command) > 2:
            server=command[0].replace("/","")
            username=command[1]
            good=command[2]
            cost=shop_list[int(good)-1][2]
            exec=str(shop_list[int(good)-1][1]).replace("[player]",username)
            # 查询积分
            score_result=tr_sign_in(event.get_user_id())
            if score_result:
                if score_result[0][2]-cost>=0:
                    # 查询玩家是否在线
                    online_result=await SendTrRequest(server, "inv", username)
                    if online_result:
                        if online_result['status']=='200':
                            # 扣除积分
                            delete_result=tr_delete_score(int(event.get_user_id()),score_result[0][2]-cost)
                            if delete_result:
                                # 执行给物品指令
                                exec_result=await SendTrRequest(server,"cmd",exec)
                                if exec_result:
                                    await tr_buy.send(str(exec_result['response'][0]))
                                else:
                                    await tr_buy.send("服不存在或裂开了，baka值花了个寂寞(")
                            else:
                                await tr_buy.send("baka值操作失败")
                        else:
                            await tr_buy.send("角色不在线")
                    else:
                        await tr_buy.send("服裂开了，暂时不能换")
                else:
                    await tr_buy.send("baka值不足")
            else:
                await tr_buy.send("没有数据")

# #抽奖 去世功能，会被冻结
# tr_raffle = on_command("/tr抽奖", priority=5, permission=GROUP)
# @tr_raffle.handle()
# async def tr_raffle_(bot: Bot, event: Event):
#     if VerifyTrGroup((str(event.get_session_id()).split("_"))[1]):
#         await tr_raffle.send("[奖池]\n还没东西~")