import sqlite3,os
import numpy as np
sqlite3.register_adapter(np.int64, int)
sqlite_path='./data/TRMResources/tr.db'
#无数据库时创建并建表
if not os.path.exists(sqlite_path):
    # 用户数据
    conn = sqlite3.connect(sqlite_path)
    cur = conn.cursor()
    sql_table_1 = '''CREATE TABLE tr_user 
               (id integer PRIMARY KEY autoincrement, 
                qq integer, 
                server TEXT,
                username TEXT);''' 
    cur.execute(sql_table_1)
    # 黑名单
    sql_table_2 = '''CREATE TABLE tr_ban 
               (id integer PRIMARY KEY autoincrement, 
                qq integer, 
                reason TEXT);''' 
    cur.execute(sql_table_2)
    # 积分数据
    sql_table_3 = '''CREATE TABLE tr_score 
               (id integer PRIMARY KEY autoincrement, 
                qq integer, 
                score integer,
                count integer,
                update_time timestamp,
                create_time timestamp);''' 
    cur.execute(sql_table_3)

# 创建与数据库的连接 
conn = sqlite3.connect(sqlite_path)
# 创建一个游标 cursor
cur = conn.cursor()

# 查询QQ是否黑名单
def get_tr_isban(qq:int):
    sql="SELECT * FROM tr_ban WHERE qq=?"
    param=(np.int64(qq),)
    cur.execute(sql, param)
    return cur.fetchall()

# 查询QQ是否已注册某服
def get_tr_reged(qq:int,server:str):
    sql="SELECT * FROM tr_user WHERE qq=? and server=?"
    param=(np.int64(qq),server)
    cur.execute(sql, param)
    return cur.fetchall()

# 根据QQ查询user所有账号
def get_qq_tr(qq:int):
    sql="SELECT * FROM tr_user WHERE qq=?"
    param=(np.int64(qq),)
    cur.execute(sql, param)
    return cur.fetchall()

# 根据玩家名查询QQ账号
def get_tr_qq(server:str,username:str):
    sql="SELECT * FROM tr_user WHERE server=? and username=?"
    param=(server,username)
    cur.execute(sql, param)
    return cur.fetchall()

# user新建一个服账号
def tr_add_user(qq:int,server:str,username:str):
    sql="INSERT INTO tr_user (qq,server,username) VALUES(?,?,?)"
    param=(np.int64(qq),server,username)
    cur.execute(sql, param)
    conn.commit()
    return True

# user删除一个服账号
def tr_del_user(qq:int):
    sql="delete from tr_user where qq=?"
    param=(np.int64(qq),)
    cur.execute(sql, param)
    conn.commit()
    return True

# 加入黑名单
def tr_add_ban(qq:int,reason:str):
    sql="INSERT INTO tr_ban (qq,reason) VALUES(?,?)"
    param=(np.int64(qq),reason)
    cur.execute(sql, param)
    conn.commit()
    return True

# 删除黑名单
def tr_del_ban(qq:int):
    sql="delete from tr_ban where qq=?"
    param=(np.int64(qq),)
    cur.execute(sql, param)
    conn.commit()
    return True

# 查询积分
def tr_sign_in(qq:int):
    sql="SELECT * FROM tr_score WHERE qq=?"
    param=(np.int64(qq),)
    cur.execute(sql, param)
    return cur.fetchall()

# 积分账号创建
def tr_create_score(qq:int,score:int,count:int):
    sql="INSERT INTO tr_score (qq,score,count,update_time,create_time) VALUES(?,?,?,date('now','localtime'),date('now','localtime'))"
    param=(np.int64(qq),np.int64(score),np.int64(count))
    cur.execute(sql, param)
    conn.commit()
    return True

# 积分更新含时间更新
def tr_update_score(qq:int,score:int,count:int):
    sql="UPDATE tr_score SET score=?,count=?,update_time=date('now','localtime') WHERE qq=?"
    param=(int(score),np.int64(count),np.int64(qq))
    cur.execute(sql, param)
    conn.commit()
    return True

# 积分删除
def tr_delete_score(qq:int,score:int):
    sql="UPDATE tr_score SET score=? WHERE qq=?"
    param=(int(score),np.int64(qq))
    cur.execute(sql, param)
    conn.commit()
    return True

# 积分排行榜
def tr_score_top():
    sql="SELECT * FROM tr_score ORDER BY score desc LIMIT 10"
    cur.execute(sql)
    return cur.fetchall()