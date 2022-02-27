import psycopg2

con = psycopg2.connect(host="", database="", user="", password="")

# cur = con.cursor()
# cur.execute('''select user_id from ali_ag_db.registry ''')
# load = cur.fetchall()
# con.commit()
# cur.close()
# user = [i[0] for i in load]
# for user_id in user:
#     cur = con.cursor()
#     cur.execute(f"""INSERT INTO ali_ag_db.diamonds (chat_id,user_id,diamond)
#                VALUES (-1001476763360,%(user_id)s,100)""", {'user_id': int(user_id)})
#     con.commit()
#     cur.close()


# cur = con.cursor()
# cur.execute(f'''UPDATE ali_ag_db.diamonds SET diamond = 100''')
# con.commit()
# cur.close()


def add_diamond(chat_id,user_id, num):
    cur = con.cursor()
    cur.execute('''UPDATE ali_ag_db.diamonds SET diamond=diamond + %(num)s WHERE chat_id=%(chat_id)s AND user_id=%(user_id)s;
    INSERT INTO ali_ag_db.diamonds (chat_id,user_id, diamond)
       SELECT %(chat_id)s,%(user_id)s , %(num)s
       WHERE NOT EXISTS (SELECT 1 FROM ali_ag_db.diamonds WHERE chat_id=%(chat_id)s AND user_id=%(user_id)s);''',
                {'chat_id': int(chat_id),'user_id': int(user_id), 'num': int(num)})
    con.commit()
    cur.close()


def add_admin(chat_id,user_id):
    cur = con.cursor()
    cur.execute(f"""INSERT INTO ali_ag_db.admins (chat_id,user_id) 
               VALUES (%(chat_id)s,%(user_id)s)""", {'chat_id':int(chat_id),'user_id': int(user_id)})
    con.commit()
    cur.close()


def rem_admin(chat_id,user_id):
    cur = con.cursor()
    cur.execute('''DELETE FROM ali_ag_db.admins
                 WHERE chat_id= %(chat_id)s AND user_id = %(user_id)s''', {'chat_id': int(chat_id),'user_id': int(user_id)})
    con.commit()
    cur.close()


def save_bet(chat_id,user_id, num, team,zarib):
    cur = con.cursor()
    cur.execute('''UPDATE ali_ag_db.betting SET team=%(team)s , diamond = %(num)s , zarib = %(zarib)s WHERE chat_id= %(chat_id)s AND user_id=%(user_id)s ;
    INSERT INTO ali_ag_db.betting (chat_id,user_id,team, diamond,zarib)
       SELECT %(chat_id)s,%(user_id)s, %(team)s, %(num)s, %(zarib)s
       WHERE NOT EXISTS (SELECT 1 FROM ali_ag_db.betting WHERE chat_id= %(chat_id)s AND user_id=%(user_id)s);''',
                {'chat_id': int(chat_id),'user_id': int(user_id), 'num': int(num), 'team': str(team),'zarib': float(zarib)})
    con.commit()
    cur.close()


def save_personbet(chat_id,user_id,bet_user_id ,num,zarib):
    cur = con.cursor()
    cur.execute('''UPDATE ali_ag_db.personbet SET bet_user_id = %(bet_user_id)s, diamond = %(num)s , zarib = %(zarib)s WHERE chat_id= %(chat_id)s AND user_id=%(user_id)s ;
    INSERT INTO ali_ag_db.personbet (chat_id,user_id,bet_user_id, diamond,zarib)
       SELECT %(chat_id)s,%(user_id)s, %(bet_user_id)s, %(num)s, %(zarib)s
       WHERE NOT EXISTS (SELECT 1 FROM ali_ag_db.personbet WHERE chat_id= %(chat_id)s AND user_id=%(user_id)s);''',
                {'chat_id': int(chat_id),'user_id': int(user_id), 'num': int(num),  'bet_user_id':int(bet_user_id),'zarib': float(zarib)})
    con.commit()
    cur.close()


def save_rolebet(chat_id,user_id, num, role,zarib):
    cur = con.cursor()
    cur.execute('''UPDATE ali_ag_db.rolebet SET role=%(role)s , diamond = %(num)s , zarib = %(zarib)s WHERE chat_id = %(chat_id)s AND user_id=%(user_id)s ;
    INSERT INTO ali_ag_db.rolebet (chat_id,user_id,role, diamond,zarib)
       SELECT %(chat_id)s,%(user_id)s, %(role)s, %(num)s, %(zarib)s
       WHERE NOT EXISTS (SELECT 1 FROM ali_ag_db.rolebet WHERE chat_id = %(chat_id)s AND user_id=%(user_id)s);''',
                {'chat_id': int(chat_id),'user_id': int(user_id), 'num': int(num), 'role': str(role),'zarib': float(zarib)})
    con.commit()
    cur.close()


def get_users(chat_id):
    cur = con.cursor()
    cur.execute('''select user_id,bet_user_id,diamond,zarib from ali_ag_db.personbet 
    WHERE chat_id = %(chat_id)s''',{'chat_id': int(chat_id)})
    load = cur.fetchall()
    con.commit()
    cur.close()
    users = [i[0] for i in load]
    bet_users = [i[1] for i in load]
    diamond = [i[2] for i in load]
    zarib = [i[3] for i in load]
    return users, bet_users, diamond, zarib


def winners(chat_id,team):
    cur = con.cursor()
    cur.execute('''SELECT user_id ,diamond,zarib  FROM ali_ag_db.betting
                   WHERE chat_id = %(chat_id)s AND team = %(team)s''', {'chat_id': int(chat_id),'team': str(team)})
    load = cur.fetchall()
    con.commit()
    cur.close()
    win_users = [i[0] for i in load]
    bet_num = [i[1] for i in load]
    zarib = [i[2] for i in load]
    for i, user in enumerate(win_users, start=0):
        add_diamond(chat_id,user, zarib[i]*bet_num[i])
    return win_users, bet_num , zarib


def losers(chat_id,team):
    cur = con.cursor()
    cur.execute('''SELECT user_id ,diamond,team  FROM ali_ag_db.betting
                   WHERE chat_id = %(chat_id)s AND team != %(team)s''', {'chat_id': int(chat_id),'team': str(team)})
    load = cur.fetchall()
    con.commit()
    cur.close()
    lose_users = [i[0] for i in load]
    bet_num = [i[1] for i in load]
    teams = [i[2] for i in load]
    return lose_users, bet_num, teams


def delete_data(chat_id):
    cur = con.cursor()
    cur.execute('''DELETE FROM ali_ag_db.betting
    WHERE chat_id = %(chat_id)s''',{'chat_id': int(chat_id)})
    con.commit()
    cur.close()


def delete_persondb(chat_id):
    cur = con.cursor()
    cur.execute('''DELETE FROM ali_ag_db.personbet
    WHERE chat_id = %(chat_id)s''',{'chat_id': int(chat_id)})
    con.commit()
    cur.close()


def load_admin(chat_id):
    cur = con.cursor()
    cur.execute('''SELECT user_id FROM ali_ag_db.admins
    WHERE chat_id = %(chat_id)s''',{'chat_id': int(chat_id)})
    load = cur.fetchall()
    con.commit()
    cur.close()
    admins = [i[0] for i in load]
    return admins


def load_diamond(chat_id,user_id):
    cur = con.cursor()
    cur.execute('''SELECT diamond FROM ali_ag_db.diamonds
    WHERE chat_id = %(chat_id)s AND user_id = %(user_id)s''', {'chat_id': int(chat_id),'user_id': int(user_id)})
    load = cur.fetchall()
    con.commit()
    cur.close()
    dia = [i[0] for i in load]
    return dia


def load_hendoone(chat_id,user_id):
    cur = con.cursor()
    cur.execute('''SELECT diamond FROM ali_ag_db.yalda
    WHERE chat_id = %(chat_id)s AND user_id = %(user_id)s''', {'chat_id': int(chat_id),'user_id': int(user_id)})
    load = cur.fetchall()
    con.commit()
    cur.close()
    dia = [i[0] for i in load]
    return dia


def register(user_id):
    cur = con.cursor()
    cur.execute(f"""INSERT INTO ali_ag_db.registry (user_id,channels,register) 
               VALUES (%(user_id)s,FALSE,TRUE )""", {'user_id': int(user_id)})
    con.commit()
    cur.close()


def check_register(user_id):
    cur = con.cursor()
    cur.execute('''SELECT register FROM ali_ag_db.registry
    WHERE user_id = %(user_id)s''', {'user_id': int(user_id)})
    load = cur.fetchone()
    con.commit()
    cur.close()
    if load is None or load == False:
        return False
    return True


def save_channels(user_id):
    cur = con.cursor()
    cur.execute(f'''UPDATE ali_ag_db.registry
                SET channels=TRUE 
                 Where user_id = %(user_id)s''',{'user_id':int(user_id)})
    con.commit()
    cur.close()


def check_channel(user_id):
    cur = con.cursor()
    cur.execute('''SELECT channels FROM ali_ag_db.registry
    WHERE user_id = %(user_id)s''', {'user_id': int(user_id)})
    load = cur.fetchall()
    con.commit()
    cur.close()
    if not load[0][0]:
        return False
    return True


def save_record(chat_id,user_id,team,diamond,win):
    cur = con.cursor()
    cur.execute(f"""INSERT INTO ali_ag_db.record (chat_id,user_id,team,diamond,win) 
               VALUES (%(chat_id)s,%(user_id)s,%(team)s,%(diamond)s,%(win)s )""", {'chat_id': int(chat_id),'user_id': int(user_id),'team': str(team),'diamond': int(diamond),'win':win})
    con.commit()
    cur.close()


def load_state(chat_id,user_id):
    query = f'''
with play as (
    SELECT count(user_id) as plays
    FROM ali_ag_db.record
    WHERE chat_id = %(chat_id)s AND user_id = %(user_id)s
),
     win as (
         SELECT count(user_id) as wins
         FROM ali_ag_db.record
         WHERE chat_id = %(chat_id)s AND user_id = %(user_id)s AND win = TRUE 
     ),
     lose as (
         SELECT count(user_id) as loses
         FROM ali_ag_db.record
         WHERE chat_id = %(chat_id)s AND user_id = %(user_id)s AND win = FALSE 
     ),
     income as (
         SELECT SUM (diamond) as incomes
         FROM ali_ag_db.record
         WHERE chat_id = %(chat_id)s AND user_id = %(user_id)s AND win = TRUE 
     ),
     lost as (
         SELECT SUM (diamond) as losts
         FROM ali_ag_db.record
         WHERE chat_id = %(chat_id)s AND user_id = %(user_id)s AND win = FALSE 
     )
select *
from play,
     win,
     lose,
     income, 
     lost
'''
    try:
        cur = con.cursor()
        cur.execute(query, {'chat_id': int(chat_id),'user_id': int(user_id)})
        res = cur.fetchone()
        con.commit()
        cur.close()

        return res[0], res[1], res[2], res[3], res[4]
    except Exception as e:
        print(e)
        return 0, 0, 0, 0, 0


def load_user(chat_id):
    cur = con.cursor()
    cur.execute('''SELECT user_id FROM ali_ag_db.betting
    WHERE chat_id = %(chat_id)s''', {'chat_id': int(chat_id)})
    load = cur.fetchall()
    con.commit()
    cur.close()
    user = [i[0] for i in load]
    if len(user) == 0:
        return False
    return user


def load_register_user():
    cur = con.cursor()
    cur.execute('select user_id from ali_ag_db.diamonds')
    load = cur.fetchall()
    con.commit()
    cur.close()
    user = [i[0] for i in load]
    return user


def get_best(chat_id):
    cur = con.cursor()
    cur.execute('''select user_id ,diamond from ali_ag_db.diamonds 
    WHERE chat_id = %(chat_id)s
    order by diamond desc limit 5''',{'chat_id': int(chat_id)})
    load = cur.fetchall()
    con.commit()
    cur.close()
    user = [i[0] for i in load]
    diamond = [i[1] for i in load]
    return user, diamond


def get_best_bet(chat_id):
    cur = con.cursor()
    cur.execute('''select user_id ,diamond,team from ali_ag_db.record
     WHERE chat_id = %(chat_id)s AND win = TRUE 
     order by diamond desc limit 5''',{'chat_id': int(chat_id)})
    load = cur.fetchall()
    con.commit()
    cur.close()
    user = [i[0] for i in load]
    diamond = [i[1] for i in load]
    team = [i[2] for i in load]
    return user, diamond, team


def stats(chat_id,user_id):
    query = f'''
    with besty as (
        SELECT MAX (diamond) as bestys
        FROM ali_ag_db.record
        WHERE chat_id = %(chat_id)s AND user_id = %(user_id)s AND win = TRUE 
    ),
         worst as (
             SELECT count(diamond) as worsts
             FROM ali_ag_db.record
             WHERE chat_id = %(chat_id)s AND user_id = %(user_id)s AND win = FALSE 
         )
select *
from besty,
     worst
'''
    try:
        cur = con.cursor()
        cur.execute(query, {'chat_id': int(chat_id),'user_id': int(user_id)})
        res = cur.fetchone()
        con.commit()
        cur.close()

        return res[0], res[1]
    except Exception as e:
        print(e)
        return 0, 0


def check_player(chat_id,user_id):
    cur = con.cursor()
    cur.execute('''SELECT user_id FROM ali_ag_db.rolebet 
                WHERE chat_id = %(chat_id)s AND user_id = %(user_id)s''',{'chat_id': int(chat_id),'user_id': int(user_id)})
    load = cur.fetchall()
    con.commit()
    cur.close()
    load = [i[0] for i in load]
    if len(load)==0:
        return False
    else:
        return True


def load_data(chat_id,user_id):
    cur = con.cursor()
    cur.execute('''SELECT diamond,role,zarib  FROM ali_ag_db.rolebet
                   WHERE chat_id = %(chat_id)s AND user_id = %(user_id)s''', {'chat_id': int(chat_id),'user_id': int(user_id)})
    load = cur.fetchall()
    con.commit()
    cur.close()
    diamond = [i[0] for i in load]
    role = [i[1] for i in load]
    zarib = [i[2] for i in load]
    return diamond, role, zarib


def delete_user(chat_id, user_id):
    cur = con.cursor()
    cur.execute('''DELETE FROM ali_ag_db.rolebet
                 WHERE chat_id = %(chat_id)s AND user_id = %(user_id)s''', {'chat_id': int(chat_id),'user_id': int(user_id)})
    con.commit()
    cur.close()


def load_roleuser(chat_id):
    cur = con.cursor()
    cur.execute('''SELECT user_id FROM ali_ag_db.rolebet
    WHERE chat_id = %(chat_id)s''', {'chat_id': int(chat_id)})
    load = cur.fetchall()
    con.commit()
    cur.close()
    user = [i[0] for i in load]
    return user


def load_emoji():
    cur = con.cursor()
    cur.execute('SELECT emoji FROM ali_ag_db.shop')
    load = cur.fetchall()
    con.commit()
    cur.close()
    emoji = [i[0] for i in load]
    return emoji


def load_emojicost(emoji):
    cur = con.cursor()
    cur.execute('''SELECT cost FROM ali_ag_db.shop
    WHERE emoji = %(emoji)s''', {'emoji': str(emoji)})
    load = cur.fetchall()
    con.commit()
    cur.close()
    cost = [i[0] for i in load]
    return cost


def save_emoji(chat_id,user_id,emoji):
    cur = con.cursor()
    cur.execute(f'''UPDATE ali_ag_db.diamonds
                SET emoji= %(emoji)s 
                 WHERE user_id = %(user_id)s AND chat_id = %(chat_id)s''',{'emoji': str(emoji), 'chat_id': int(chat_id), 'user_id': int(user_id)})
    con.commit()
    cur.close()


def save_rank(chat_id,user_id,rank):
    cur = con.cursor()
    cur.execute(f'''UPDATE ali_ag_db.diamonds
                SET rank= %(rank)s 
                 WHERE user_id = %(user_id)s AND chat_id = %(chat_id)s''',{'rank': str(rank), 'chat_id': int(chat_id), 'user_id': int(user_id)})
    con.commit()
    cur.close()


def load_rank(chat_id,user_id):
    cur = con.cursor()
    cur.execute('''SELECT rank FROM ali_ag_db.diamonds
    WHERE user_id = %(user_id)s AND chat_id = %(chat_id)s''',{'chat_id': int(chat_id), 'user_id': int(user_id)})
    load = cur.fetchall()
    con.commit()
    cur.close()
    rank = [i[0] for i in load]
    if len(rank) == 0:
        return False
    return rank[0]


def load_purchaseemoji(chat_id,user_id):
    cur = con.cursor()
    cur.execute('''SELECT emoji FROM ali_ag_db.diamonds
    WHERE user_id = %(user_id)s AND chat_id = %(chat_id)s''',{'chat_id': int(chat_id), 'user_id': int(user_id)})
    load = cur.fetchall()
    con.commit()
    cur.close()
    emoji = [i[0] for i in load]
    if len(emoji) == 0:
        return False
    return emoji[0]


def add_emoji(emoji,cost):
    cur = con.cursor()
    cur.execute(f"""INSERT INTO ali_ag_db.shop (emoji,cost) 
               VALUES (%(emoji)s,%(cost)s)""", {'cost':int(cost),'emoji': str(emoji)})
    con.commit()
    cur.close()


def rem_emoji(emoji):
    cur = con.cursor()
    cur.execute('''DELETE FROM ali_ag_db.shop
                   WHERE emoji = %(emoji)s''',
                {'emoji': str(emoji)})
    con.commit()
    cur.close()


def submit_invite(user_id, invite_id):
    cur = con.cursor()
    cur.execute(f'''UPDATE ali_ag_db.registry
                SET invitelink= TRUE , invite_id = %(invite_id)s
                WHERE user_id = %(user_id)s''', {'user_id': int(user_id), 'invite_id': int(invite_id)})
    con.commit()
    cur.close()


def countinvite(user_id):
    cur = con.cursor()
    cur.execute(f'''UPDATE ali_ag_db.registry
                SET countinvite = countinvite + 1
                WHERE user_id = %(user_id)s''', {'user_id': int(user_id)})
    con.commit()
    cur.close()


def best_inviters():
    cur = con.cursor()
    cur.execute('''select user_id, countinvite from ali_ag_db.registry
    order by countinvite desc limit 5''')
    load = cur.fetchall()
    con.commit()
    cur.close()
    users = [i[0] for i in load]
    count = [i[1] for i in load]
    return users, count


def myplayers(user_id):
    cur = con.cursor()
    cur.execute('''select user_id from ali_ag_db.registry
    where invite_id = %(user_id)s''', {'user_id': int(user_id)})
    load = cur.fetchall()
    con.commit()
    cur.close()
    players = [i[0] for i in load]
    return players


def check_invite(user_id):
    cur = con.cursor()
    cur.execute('''SELECT invitelink FROM ali_ag_db.registry
    WHERE user_id = %(user_id)s''', {'user_id': int(user_id)})
    load = cur.fetchone()
    con.commit()
    cur.close()
    if load[0]:
        return True
    return False
