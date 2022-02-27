#!/usr/bin/python
# -*- coding: utf-8 -*-
import random
import re
import time
import telebot
from telebot import types
from telebot.types import InlineKeyboardMarkup, InlineKeyboardButton
from pyrogram import Filters
import diamond_db
from tenacity import retry, wait_fixed, stop_after_attempt
import requests
import wwresult

TOKEN = '1351328826:AAGHSrELXj3uMel8addsZWJknpZA3ZLTSho'

bot = telebot.TeleBot(token=TOKEN, num_threads=10)

creators = [835478580, 638994540, 1258617062]
partner = [835478580, 638994540, 1255111343, 1318109205]
partners = {-1001476763360: [], -1001128468995: []}
rolepartners = {-1001476763360: [], -1001128468995: []}
personpartners = {-1001476763360: [], -1001128468995: []}
nextbet = {-1001476763360: [], -1001128468995: []}
checkrole = {-1001476763360: False, -1001128468995: False}
betting = {-1001476763360: False, -1001128468995: False}
rolling = {-1001476763360: False, -1001128468995: False}
onPerson = {-1001476763360: False, -1001128468995: False}
checkperson = {-1001476763360: False, -1001128468995: False}
players = {}
teams = ['roosta', 'ferghe', 'ghatel', 'atash', 'gorg', 'monafegh']
lupin = -1001476763360
wolverines = -1001128468995
lupin_link = 'https://t.me/joinchat/aO3cMk0UriEyYmEx'
helpme = '''᪥᪥᪥᪥᪥᪥᪥᪥᪥᪥᪥᪥᪥᪥᪥᪥᪥᪥᪥᪥᪥᪥᪥
به بخش راهنمای لوپین بت خوش آمدید🐾
❗️توضیحات

❕این ربات به این گونه است که شرط بندی برای چند بازی در روز باز میشود(در کانال لوپین ولف اطلاع داده میشود) و شما میتوانید روی آن بازی ها شرط بسته و الماس بدست آورید💎

❕این ربات دارای ضریب می باشد و به شما ضریبی ارائه میدهد که در صورت برد شما در شرط بندی ، ضریب در مقدار الماس شرط بندی شده ضرب خواهد شد و به تعداد الماس های شما اضافه میشود💎

❕هرروز سه چالش در کانال لوپین ولف گزاشته میشود که شما میتوانید با انجام آن ها الماس بدست آورید ، همچنین شما میتوانید با ثبت نام در ربات (/registerme) و عضو شدن در کانال ها میتوانید الماس بدست آورید💎

❕هر بازی که شما در گروه لوپین ولف جوین شوید به شما 2 الماس اضافه خواهد کرد پس حتما در گروه پلی بدهید تا الماس جمع آوری کنید💎

❕شما با استفاده از الماس هایتان میتوانید کار های زیادی انجام بدید که متن کامل آن را میتوانید در کانال زیر مشاهده کنید💎
ID : @lupine_wolf

❗️دستورات بات :

/getstate :
شما با استفاده از این دستور میتوانید آمار کامل بت های خود را مشاهده کنید🐾

/wallet :
شما با استفاده از این دستور میتوانید تعداد الماس های خود را مشاهده کنید🐾

/bestbet :
شما با استفاده از این دستور میتوانید لیست بهترین بت باز های گروه و بهترین شرط های بسته شده را مشاهده کنید🐾

/betting :
شما با استفاده از این دستور در زمان باز شدن شرط بندی میتوانید شرط خود را ببندید🐾

/registerme :
شما با استفاده از این دستور میتوانید در ربات ثبت نام کنید و الماس رایگان بدست آورید🐾


༆𝒎𝒖𝒔𝒕 𝒃𝒆 𝒂 𝒍𝒖𝒑𝒊𝒏𝒆 𝒈𝒖𝒚 𝒕𝒐 𝒃𝒆 𝒂𝒍𝒊𝒗𝒆 💎
᪥᪥᪥᪥᪥᪥᪥᪥᪥᪥᪥᪥᪥᪥᪥᪥᪥᪥᪥᪥᪥᪥᪥'''


def add_chatplayer(chat_id):
    global players
    if chat_id not in players:
        players.update({chat_id: []})


def check_admin(chat_id, user_id):
    admins = diamond_db.load_admin(chat_id)
    if user_id in admins:
        return True
    else:
        return False


def check_group(message):
    chat_id = message.chat.id
    groups = [-1001476763360, -1001128468995]
    if chat_id not in groups:
        bot.send_message(chat_id, '''برای شرط بندی و استفاده از ربات در گروه زیر عضو شوید

🔥 ᒪIᑎK : https://t.me/joinchat/aO3cMk0UriEyYmEx''')
        bot.leave_chat(chat_id)
        return True
    else:
        return False


@bot.message_handler(commands=['betadminlist'], func=Filters.user(creators))
def adminlist(message):
    admins = diamond_db.load_admin(message.chat.id)
    msg = 'lupin bet admins : '
    for admin in admins:
        try:
            x = bot.get_chat_member(chat_id=message.chat.id, user_id=admin)
            msg += f'\n[{x.user.first_name}](tg://user?id={x.user.id}) `{admin}`'
        except:
            diamond_db.rem_admin(message.chat.id, admin)
    bot.send_message(message.chat.id, msg, parse_mode='markdown')


def get_stats(user_id):
    wuff_url = "http://www.tgwerewolf.com/Stats/PlayerStats/?pid={}&json=true"

    stats = requests.get(wuff_url.format(user_id)).json()

    return stats


@bot.message_handler(commands=['nextbet'], func=Filters.group)
def call_me(message):
    global nextbet
    chat_id = message.chat.id
    user_id = message.from_user.id
    if user_id not in nextbet[chat_id]:
        if chat_id == -1001476763360:
            group = '🐾𖡼ᏝᏬᎮᎥᏁ ꪡᴏʟғ⸸🐾'
            link = lupin_link
            hy_link = f'[{group}]({link})'
        try:
            nextbet[chat_id].append(user_id)
            bot.send_message(user_id, f'''|✜ شمــا بہ ليســت انتظار بــــت در
 گروه {hy_link} اضافہ شديـــد ✜|''', parse_mode='markdown', disable_web_page_preview=True)
        except:
            bot.reply_to(message, '✦| ابتدا ربات را استارت کنید و مجدد این دستور را بزنید ✖️')
    elif user_id in nextbet[chat_id]:
        try:
            msg = bot.reply_to(message, 'شما در لــــیــــســــت انــــتــــظــــار بت حضور دارید...🐾')
            time.sleep(2)
            bot.delete_message(chat_id, msg.message_id)
        except:
            pass


@bot.message_handler(regexp='plus', func=Filters.group)
def get_diamond(message):
    if check_group(message):
        return
    user_id = message.from_user.id
    chat_id = message.chat.id
    if not message.reply_to_message:
        return
    if not check_admin(chat_id, user_id):
        return
    rep_id = message.reply_to_message.from_user.id
    num = message.text.split(" ")
    try:
        numdiamond = int(num[1])
    except:
        return

    try:
        if num[2] == '💎':
            diamond_db.add_diamond(chat_id, rep_id, numdiamond)
            bot.reply_to(message,
                         f'''✦| [{message.reply_to_message.from_user.first_name}](tg://user?id={rep_id})
            {numdiamond} المـ💎ـاس دریافت کرد ✔️''',
                         parse_mode='Markdown')
        else:
            bot.reply_to(message, 'لطفا اموجی را درست وارد کنید')
    except:
        bot.reply_to(message, 'لطفا دستور را درست وارد کنید')
        return


@bot.message_handler(commands=['sendlupinbanner'], func=Filters.user(creators))
def banner(message):
    user_list = diamond_db.load_register_user()
    j = 0
    bot.send_message(message.chat.id, 'start')
    for user_id in user_list:
        try:
            bot.send_message(user_id, """🔥فصل جديد بت هم اكنون آغاز شد و سوپرایز جدیدمون لوپین باکس معرفی شد
            🔥همین الان توی گپ جوین شو و شروع کن به المـ💎ـاس جمع کردن و لوپین باکس بخر

🔥 ᒪIᑎK : https://t.me/joinchat/aO3cMk0UriEyYmEx""", disable_web_page_preview=True)
            j += 1
            time.sleep(2)
        except:
            pass
    bot.send_message(message.chat.id, f'be {j} az {len(user_list)} ersal shod')


# @bot.message_handler(commands=['sendwolvbanner'], func=Filters.user(257095001))
# def banner_wlv(message):
#     user_list = diamond_db.load_register_user(wolverines)
#
#     for user_id in user_list:
#         try:
#             bot.send_message(user_id, """لینک جدید گروه ولورین
#
# 🔥 ᒪIᑎK : https://t.me/joinchat/SiQiUkNDEgM6tLiDXMr68w""", disable_web_page_preview=True)
#         except:
#             pass
#     bot.send_message(message.chat.id, 'حله چشاته امیر خ')


@bot.message_handler(regexp='sub', func=Filters.group)
def get_diamond(message):
    if check_group(message):
        return
    user_id = message.from_user.id
    chat_id = message.chat.id
    if not message.reply_to_message:
        return
    if not check_admin(chat_id, user_id):
        return
    rep_id = message.reply_to_message.from_user.id
    num = message.text.split(" ")
    try:
        numdiamond = int(num[1])
    except:
        return

    try:
        if num[2] != '💎':
            bot.reply_to(message, 'لطفا اموجی را درست وارد کنید')
            return
    except:
        bot.reply_to(message, 'لطفا دستور را درست وارد کنید')
        return
    inventory = diamond_db.load_diamond(chat_id, rep_id)
    if numdiamond > round(inventory[0]):
        bot.send_message(user_id, '✦| مقدار وارد شده بیشتر از تعداد کل المـ💎ـاس ها است ✖️')
        return
    diamond_db.add_diamond(chat_id, rep_id, -1 * numdiamond)
    bot.reply_to(message,
                 f'''✦| [{message.reply_to_message.from_user.first_name}](tg://user?id={rep_id})
{numdiamond} المـ💎ـاس از دست داد ✔️''',
                 parse_mode='Markdown')


@bot.message_handler(regexp='addadmin', func=Filters.user(creators))
def add_admin(message):
    if not message.reply_to_message:
        return
    rep_id = message.reply_to_message.from_user.id
    chat_id = message.chat.id
    diamond_db.add_admin(chat_id, rep_id)
    bot.reply_to(message,
                 f'✦| [{message.reply_to_message.from_user.first_name}](tg://user?id={rep_id}) با موفقیت به لیست ادمین ها اضافه شد✔️',
                 parse_mode='Markdown')


@bot.message_handler(regexp='remadmin', func=Filters.user(creators))
def rem_admin(message):
    if not message.reply_to_message:
        return
    rep_id = message.reply_to_message.from_user.id
    chat_id = message.chat.id
    diamond_db.rem_admin(chat_id, rep_id)
    bot.reply_to(message,
                 f'✦| [{message.reply_to_message.from_user.first_name}](tg://user?id={rep_id}) با موفقیت از لیست ادمین ها حذف شد✔️',
                 parse_mode='Markdown')


@bot.message_handler(commands=['removeadmin'],
                     func=Filters.user([880924041, 835478580, 638994540, 1507491362, 1258617062]))
def remadmin(message):
    text = message.text
    text = text.split(" ")
    user = text[1]
    diamond_db.rem_admin(message.chat.id, user)
    bot.reply_to(message, 'done')


@bot.message_handler(commands=['add'], func=Filters.user(partner))
def add_emoji(message):
    try:
        msg = message.text.split(' ')
        emoji = msg[1]
        cost = msg[2]
        diamond_db.add_emoji(emoji, cost)
        bot.reply_to(message, f'emoji {emoji} ba gheymate {cost} be database ezafe shod')
    except:
        bot.reply_to(message, 'ERROR')


@bot.message_handler(commands=['remove'], func=Filters.user(partner))
def add_emoji(message):
    try:
        msg = message.text.split(' ')
        emoji = msg[1]
        diamond_db.rem_emoji(emoji)
        bot.reply_to(message, f'emoji {emoji} az database hazf shod')
    except:
        bot.reply_to(message, 'ERROR')


@bot.message_handler(commands=['setemoji'], func=Filters.user(creators))
def set_emoji(message):
    try:
        msg = message.text.split(' ')
        chat_id = message.chat.id
        user_id = int(msg[1])
        emoji = msg[2]
        diamond_db.save_emoji(chat_id, user_id, emoji)
        bot.reply_to(message, f'emoji {emoji} baraye {user_id} save shod')
    except:
        bot.reply_to(message, 'ERROR')


@bot.message_handler(commands=['setrank'], func=Filters.user(creators))
def set_emoji(message):
    try:
        msg = message.text.split(' ')
        chat_id = message.chat.id
        user_id = int(msg[1])
        rank = msg[2]
        diamond_db.save_rank(chat_id, user_id, rank)
        bot.reply_to(message, f'rank [{rank}] baraye {user_id} save shod')
    except:
        bot.reply_to(message, 'ERROR')


@bot.message_handler(commands=['personon'], func=Filters.group)
def personon(message):
    global onPerson
    global players
    if check_group(message):
        return
    user_id = message.from_user.id
    chat_id = message.chat.id
    if not message.reply_to_message:
        return
    if not check_admin(chat_id, user_id):
        bot.reply_to(message, '✦| شما ادمین ربات نیستید✖️')
        return
    if onPerson[chat_id]:
        bot.reply_to(message, '✦| بت فعال است✖️')
    add_chatplayer(chat_id)
    all = message.reply_to_message.entities
    for player in all:
        try:
            players[chat_id].append(player.user)
        except:
            pass
    onPerson[chat_id] = True
    checkperson[chat_id] = True
    bot.send_message(message.chat.id, '''✦| بت آغاز شد هم اکنون میتوانید با زدن دستور 
    /personbet
    روي پلیر موردنظر خود شرط ببندید✔️''')


@bot.message_handler(commands=['personoff'], func=Filters.group)
def personoff(message):
    global onPerson
    global players
    if check_group(message):
        return
    user_id = message.from_user.id
    chat_id = message.chat.id
    if not check_admin(chat_id, user_id):
        bot.reply_to(message, '✦| شما ادمین ربات نیستید✖️')
        return
    if not onPerson[chat_id]:
        bot.reply_to(message, '✦| بت غیرفعال است✖️')
    add_chatplayer(chat_id)
    onPerson[chat_id] = False
    players.pop(chat_id)
    bot.send_message(message.chat.id, '✦| بت با موفقیت غیرفعال شد✔️')


@bot.message_handler(commands=['beton'], func=Filters.group)
def beton(message):
    global betting
    global nextbet
    if check_group(message):
        return
    user_id = message.from_user.id
    chat_id = message.chat.id
    if not check_admin(chat_id, user_id):
        bot.reply_to(message, '✦| شما ادمین ربات نیستید✖️')
        return
    if betting[chat_id]:
        bot.reply_to(message, '✦| بت فعال است✖️')
    betting[chat_id] = True
    msg = bot.send_message(message.chat.id, '''✦| بت آغاز شد هم اکنون میتوانید با زدن دستور 
/betting
تیم برنده بازی بعد را پیش بینی کنید✔️''')
    if chat_id == -1001476763360:
        group = '🐾𖡼ᏝᏬᎮᎥᏁ ꪡᴏʟғ⸸🐾'
        link = lupin_link
        hy_link = f'[{group}]({link})'
    for user in nextbet[chat_id]:
        try:
            bot.send_message(user, f'''هورا 💥بـــت در گروه {hy_link} فعال شـــد!💥

|✜با زدن دستــور زیر در گـروه بــرای شــرطبندی خود در بازی بعــد اقدام کنیــد✜|

✧ /betting ✧''', parse_mode='markdown', disable_web_page_preview=True)
        except:
            pass
    nextbet[chat_id].clear()


@bot.message_handler(commands=['betoff'], func=Filters.group)
def bettoff(message):
    global betting
    if check_group(message):
        return
    user_id = message.from_user.id
    chat_id = message.chat.id
    if not check_admin(chat_id, user_id):
        bot.reply_to(message, '✦| شما ادمین ربات نیستید✖️')
        return
    if not betting[chat_id]:
        bot.reply_to(message, '✦| بت غیرفعال است✖️')
    betting[chat_id] = False
    bot.send_message(message.chat.id, '✦| بت با موفقیت غیرفعال شد✔️')


@bot.message_handler(commands=['roleon'], func=Filters.group)
def beton(message):
    global rolling
    if check_group(message):
        return
    user_id = message.from_user.id
    chat_id = message.chat.id
    if not check_admin(chat_id, user_id):
        bot.reply_to(message, '✦| شما ادمین ربات نیستید✖️')
        return
    if rolling[chat_id]:
        bot.reply_to(message, '✦| بت فعال است✖️')
    rolling[chat_id] = True
    bot.send_message(message.chat.id, '''✦| بت آغاز شد هم اکنون میتوانید با زدن دستور 
/rolebet
نقش خود در بازی بعد را پیش بینی کنید✔️''')


@bot.message_handler(commands=['roleoff'], func=Filters.group)
def bettoff(message):
    global rolling
    if check_group(message):
        return
    user_id = message.from_user.id
    chat_id = message.chat.id
    if not check_admin(chat_id, user_id):
        bot.reply_to(message, '✦| شما ادمین ربات نیستید✖️')
        return
    if not rolling[chat_id]:
        bot.reply_to(message, '✦| بت غیرفعال است✖️')
    rolling[chat_id] = False
    bot.send_message(message.chat.id, '✦| بت با موفقیت غیرفعال شد✔️')


def build_person_markup(players, chat_id):
    zarib = round(random.uniform(3, 6), 1)
    markup = InlineKeyboardMarkup()
    for player in players:
        try:
            markup.add(InlineKeyboardButton(player.first_name, callback_data=f'pr {player.id} {zarib} {chat_id}'))
        except:
            pass
    return markup


def build_markup(chat_id):
    if chat_id == -1001476763360:
        group = 'lup'
    elif chat_id == -1001128468995:
        group = 'wlv'
    z1 = round(random.uniform(1.5, 2.5), 1)
    z2 = round(random.uniform(2, 3), 1)
    z3 = round(random.uniform(2.5, 3.5), 1)
    z4 = round(random.uniform(6, 7.5), 1)
    z5 = round(random.uniform(6, 7.5), 1)
    z6 = round(random.uniform(4, 5.5), 1)
    markup = InlineKeyboardMarkup()
    markup.add(InlineKeyboardButton('برد روستا👨', callback_data=f'roosta {z1} {z2} {z3} {z4} {z5} {z6} {group}'),
               InlineKeyboardButton('برد فرقه👤', callback_data=f'ferghe {z1} {z2} {z3} {z4} {z5} {z6} {group}'))
    markup.add(InlineKeyboardButton('برد گرگ ها🐺', callback_data=f'gorg {z1} {z2} {z3} {z4} {z5} {z6} {group}'),
               InlineKeyboardButton('برد قاتل🔪', callback_data=f'ghatel {z1} {z2} {z3} {z4} {z5} {z6} {group}'))
    markup.add(InlineKeyboardButton('برد آتش زن🔥', callback_data=f'atash {z1} {z2} {z3} {z4} {z5} {z6} {group}'),
               InlineKeyboardButton('برد منافق👺', callback_data=f'monafegh {z1} {z2} {z3} {z4} {z5} {z6} {group}'))
    markup.add(InlineKeyboardButton('✖️مشاهده ضرایب✖️', callback_data=f'zarayeb {z1} {z2} {z3} {z4} {z5} {z6} {group}'))
    return markup


@bot.message_handler(commands=['personbet'], func=Filters.group)
def perbet(message):
    global onPerson
    global players
    global personpartners
    if check_group(message):
        return
    chat_id = message.chat.id
    if not onPerson[chat_id]:
        bot.reply_to(message, '✦| بت غیرفعال است✖️')
        return
    user_id = message.from_user.id
    if not diamond_db.check_register(user_id):
        bot.send_message(chat_id=message.chat.id, reply_to_message_id=message.message_id,
                         text='''✦|برای شروع بت اول باید در ربات ثبت نام کنید✖️''', reply_markup=build_markup1(chat_id))
        return
    if user_id in personpartners[chat_id]:
        msg = bot.reply_to(message, '✦|امكان مجدد شری بندي براي شما وجود ندارد')
        time.sleep(3)
        try:
            bot.delete_message(chat_id, msg.message_id)
        except:
            pass
        return
    try:
        bot.send_message(user_id, '''بـت آغاز شـــد💥

    ↲ پیش‌بینـے شما روی برد کدام پلیر است؟ ↳''', reply_markup=build_person_markup(players[chat_id], chat_id))
    except:
        bot.send_message(chat_id, '✦| ابتدا ربات را استارت کنید و مجدد این دستور را بزنید ✖️')
        return
    if user_id not in personpartners[chat_id]:
        personpartners[chat_id].append(user_id)
    msg = bot.reply_to(message, '✦|پیام بت در pv  برای شما ارسال شد ✔️')
    time.sleep(2)
    try:
        bot.delete_message(chat_id, msg.message_id)
    except:
        pass


@bot.message_handler(commands=['betting'], func=Filters.group)
def bet(message):
    global betting
    global partners
    if check_group(message):
        return
    chat_id = message.chat.id
    if not betting[chat_id]:
        bot.reply_to(message, '✦| بت غیرفعال است✖️')
        return
    user_id = message.from_user.id
    if not diamond_db.check_register(user_id):
        bot.send_message(chat_id=message.chat.id, reply_to_message_id=message.message_id,
                         text='''✦|برای شروع بت اول باید در ربات ثبت نام کنید✖️''', reply_markup=build_markup1(chat_id))
        return
    if user_id in partners[chat_id]:
        msg = bot.reply_to(message, '✦|امكان مجدد شری بندي براي شما وجود ندارد')
        time.sleep(3)
        try:
            bot.delete_message(chat_id, msg.message_id)
        except:
            pass
        return
    try:
        bot.send_message(user_id, '''بـت آغاز شـــد💥

↲ پیش‌بینـے شما روی برد کدام تیـــم است؟ ↳''', reply_markup=build_markup(chat_id))
    except:
        bot.send_message(chat_id, '✦| ابتدا ربات را استارت کنید و مجدد این دستور را بزنید ✖️')
        return
    if user_id not in partners[chat_id]:
        partners[chat_id].append(user_id)
    msg = bot.reply_to(message, '✦|پیام بت در pv  برای شما ارسال شد ✔️')
    time.sleep(2)
    try:
        bot.delete_message(chat_id, msg.message_id)
    except:
        pass


@bot.callback_query_handler(func=lambda call: True)
def callback(call):
    data = call.data
    user_id = call.from_user.id
    try:
        cht = data.split(' ')
        if cht[7] == 'wlv':
            chat_id = wolverines
        elif cht[7] == 'lup':
            chat_id = lupin
    except:
        pass
    try:
        txt = data.split(' ')
        if txt[0] == 'pr':
            chat_id = int(txt[3])
    except:
        pass
    if 'checkinvite' in data:
        dt = data.split(" ")
        invite_id = int(dt[1])
        chat_id = int(dt[2])
        status = bot.get_chat_member(user_id=user_id, chat_id=chat_id).status
        if status == 'member' or status == 'creator' or status == 'administrator' or status == 'restricted':
            try:
                if get_stats(user_id)['gamesPlayed'] < 40:
                    bot.answer_callback_query(call.id, "⌬ استیت شما از حد مجاز [ حداقل 40 ]  پایین‌تر است...✖️",
                                              show_alert=True)
                    return
            except:
                bot.answer_callback_query(call.id, "⌬ استیت شما از حد مجاز [ حداقل 40 ]  پایین‌تر است...✖️",
                                          show_alert=True)
                return
            if not diamond_db.check_register(invite_id):
                bot.answer_callback_query(call.id, "⌬ شخص دعوت دهنده شما در بات ثبت نام نیست...✖️", show_alert=True)
                return

            if not diamond_db.check_register(user_id):
                diamond_db.register(user_id)
                diamond_db.add_diamond(chat_id, user_id, 20)
                bot.send_message(user_id, '''✦| شما با موفقیت در ربات بت ثبت نام شدید و 20 المـ💎ـاس دریافت کرديد✔️

✦| پلیر عزیز
با عضو شدن در دو کانال زیر میتوانید 20 المـ💎ـاس دریافت کنید✔️'''
                                 , reply_markup=build_markup2(chat_id))
            if diamond_db.check_invite(user_id):
                bot.send_message(user_id, '''◇ شما توسط شخص دیگری از قبل به گروه دعوت شده ایید...🎮
◇ معطل نکن هر چه سریع تر دستور زیر و لمس کن و با لینک دعوت دوست های خودت بیار گپ و الماس بگیر...😉

[ /invitelink ]''')
                return
            diamond_db.submit_invite(user_id, invite_id)
            diamond_db.add_diamond(chat_id, user_id, 200)
            diamond_db.add_diamond(chat_id, invite_id, 400)
            diamond_db.countinvite(invite_id)
            bot.send_message(user_id, '''⌬ هورا🎉 جوین شدی 200 الماس💎 گرفتی...🐾
بزن‌ روی دستور زیر و لينكتو بده به افراد دیگه و اونها رو بیار گپ تا الماس بگیری...💎
[ /invitelink ]''')
            bot.send_message(invite_id,
                             f'''◇ تبریک🎉 شخص [{call.from_user.first_name}](tg://user?id={user_id}) با موفقیت در گروه توسط شما عضو شد شما ۴۰۰ الماس دریافت کردید...🐾

⌬ افراد بیشتری بیار تا الماس بیشتری بگیری...😉''', parse_mode='Markdown')
            bot.send_message(638994540,
                             f'''کاربر [{call.from_user.first_name}](tg://user?id={user_id}) با لينك دعوت وارد گروه شد''',
                             parse_mode='Markdown')
        else:
            bot.answer_callback_query(call.id, '✦| ابتدا در گروه عضو شوید و سپس دکمه عضو شدم را انتخاب کنید✖️',
                                      show_alert=True)
    elif 'check_channel' in data:
        if diamond_db.check_channel(user_id):
            bot.answer_callback_query(call.id, '✦| شما از قبل ثبت نام کرده اید✔️')
        else:
            status = bot.get_chat_member(user_id=user_id, chat_id=-1001326809310).status
            status1 = bot.get_chat_member(user_id=user_id, chat_id='@LUPINe_history').status
            if status == 'member' or status == 'creator' or status == 'administrator':
                if status1 == 'member' or status1 == 'creator' or status1 == 'administrator':
                    diamond_db.save_channels(user_id)
                    bot.send_message(user_id, '''✦| تایید عضویت
20 المـ💎ـاس دیگر بعنوان هدیه از من به شما ارسال شد✔️''')
                    sp = data.split(' ')
                    chat = sp[1]
                    diamond_db.add_diamond(chat, user_id, 20)
                else:
                    bot.answer_callback_query(call.id,
                                              '''✦| ابتدا در کانال هاعضو شوید و سپس دکمه عضو شدم را انتخاب کنید✖️''',
                                              show_alert=True)
            else:
                bot.answer_callback_query(call.id, '✦| ابتدا در کانال هاعضو شوید و سپس دکمه عضو شدم را انتخاب کنید✖️',
                                          show_alert=True)
    elif onPerson[chat_id]:
        markup = types.ReplyKeyboardMarkup(one_time_keyboard=True, resize_keyboard=2)
        markup.add('cancel✖️')
        msg = bot.send_message(user_id, '''✦| با موفقیت ثبت شد✔️
از چند المـ💎ـاس برای این بت روی این شخص استفاده میکنید؟''',
                               reply_markup=markup)
        try:
            bot.delete_message(call.message.chat.id, call.message.message_id)
        except:
            pass
        details = data.split(' ')
        userid = details[1]
        zarib = details[2]
        try:
            bot.register_next_step_handler(msg, finalperson, zarib, userid, chat_id)
        except:
            bot.send_message(call.message.chat.id, 'لطفا مجددا تلاش كنيد')

    elif not betting[chat_id]:
        bot.answer_callback_query(call.id, '✦| بت غیرفعال است✖️')
        try:
            bot.delete_message(call.message.chat.id, call.message.message_id)
        except:
            pass
        return
    elif 'zarayeb' in data:
        dataa = data.split(' ')
        msg = f'''ضرایب بت برای شما:
برد روستا👨 : {dataa[1]}
برد فرقه👤 : {dataa[2]}
برد گرگ🐺 : {dataa[3]}
برد آتش زن🔥 : {dataa[4]}
برد قاتل🔪 : {dataa[5]}
برد منافق👺 : {dataa[6]}'''
        bot.answer_callback_query(call.id, msg, show_alert=True)
    else:
        markup = types.ReplyKeyboardMarkup(one_time_keyboard=True, resize_keyboard=2)
        markup.add('cancel✖️')
        msg = bot.send_message(user_id, '''✦| با موفقیت ثبت شد✔️
از چند المـ💎ـاس برای این بت استفاده میکنید؟''',
                               reply_markup=markup)
        try:
            bot.delete_message(call.message.chat.id, call.message.message_id)
        except:
            pass
        zaribs = data.split(' ')
        if 'roosta' in data:
            zarib = zaribs[1]
        elif 'ferghe' in data:
            zarib = zaribs[2]
        elif 'gorg' in data:
            zarib = zaribs[3]
        elif 'atash' in data:
            zarib = zaribs[4]
        elif 'ghatel' in data:
            zarib = zaribs[5]
        elif 'monafegh' in data:
            zarib = zaribs[6]

        if zaribs[7] == 'wlv':
            chat_id = wolverines
        elif zaribs[7] == 'lup':
            chat_id = lupin
        try:
            bot.register_next_step_handler(msg, savediamonds, zaribs[0], zarib, chat_id)
        except:
            bot.send_message(call.message.chat.id, 'لطفا مجددا تلاش كنيد')


def finalperson(message, zarib, bet_user_id, chat_id):
    global personpartners
    global onPerson
    user_id = message.from_user.id
    if message.text == 'cancel✖️':
        bot.reply_to(message, '''✦| این بت لغو شد
برای شروع بت جدید در گروه دستور
/betting@LupinBet_bot 
را بزنید✔️''')
        if user_id in personpartners[chat_id]:
            personpartners[chat_id].remove(user_id)
        return
    if not onPerson[chat_id]:
        bot.send_message(user_id, '✦| بت غیرفعال است✖️')
        return
    try:
        diamond = int(message.text)
        if diamond > 100000:
            msg1 = bot.send_message(user_id, '''سقف شرط بندي 100000 الماس ميباشد
لطفا عدد زير 1000000 وارد كنيد''')
            bot.register_next_step_handler(msg1, finalperson, zarib, bet_user_id, chat_id)
            return
        inventory = diamond_db.load_diamond(chat_id, user_id)
        if diamond > round(inventory[0]) or diamond <= 0:
            msg = '✦| تعداد  المـ💎ـاس های شما کافی نیست ✖️'
            dia = diamond_db.load_diamond(chat_id, user_id)
            try:
                msg += f'''\nموجودي شما در حال حاضر : {dia[0]} 💎'''
            except:
                msg += f'''\nموجودي شما در حال حاضر : {0} 💎'''
            bot.send_message(user_id, msg)
            msg1 = bot.send_message(user_id, '✦|یک عدد وارد کنید✔️')
            bot.register_next_step_handler(msg1, finalperson, zarib, bet_user_id, chat_id)
        else:
            diamond_db.save_personbet(chat_id, user_id, bet_user_id, diamond, zarib)
            diamond_db.add_diamond(chat_id, user_id, -1 * diamond)
            x = bot.get_chat_member(chat_id=chat_id, user_id=bet_user_id)
            name = x.user.first_name
            bot.send_message(user_id, f'''✦| شما با تعداد {diamond} المـ💎ـاس
با ضریب{zarib}
با پیشبینی برد پلیر {name}
وارد بت شدید''')
            bot.send_message(-1001134572701, f'''✦| [{message.from_user.first_name}](tg://user?id={user_id})  
با پیش بینی برد {name} و تعداد {diamond} المـ💎ـاس با
ضریب{zarib} 
وارد بت شد''',
                             parse_mode='Markdown')
    except:
        msg2 = bot.send_message(user_id, '✦|یک عدد وارد کنید✔️')
        bot.register_next_step_handler(msg2, finalperson, zarib, bet_user_id, chat_id)


def savediamonds(message, data, zarib, chat_id):
    global partners
    user_id = message.from_user.id
    if message.text == 'cancel✖️':
        bot.reply_to(message, '''✦| این بت لغو شد
برای شروع بت جدید در گروه دستور
/betting@LupinBet_bot 
را بزنید✔️''')
        if user_id in partners[chat_id]:
            partners[chat_id].remove(user_id)
        return
    if not betting[chat_id]:
        bot.send_message(user_id, '✦| بت غیرفعال است✖️')
        return
    try:
        diamond = int(message.text)
        if diamond > 100000:
            msg1 = bot.send_message(user_id, '''سقف شرط بندي 100000 الماس ميباشد
لطفا عدد زير 1000000 وارد كنيد''')
            bot.register_next_step_handler(msg1, savediamonds, data, zarib, chat_id)
            return
        inventory = diamond_db.load_diamond(chat_id, user_id)
        if diamond > round(inventory[0]) or diamond <= 0:
            msg = '✦| تعداد  المـ💎ـاس های شما کافی نیست ✖️'
            dia = diamond_db.load_diamond(chat_id, user_id)
            try:
                msg += f'''\nموجودي شما در حال حاضر : {dia[0]} 💎'''
            except:
                msg += f'''\nموجودي شما در حال حاضر : {0} 💎'''
            bot.send_message(user_id, msg)
            msg1 = bot.send_message(user_id, '✦|یک عدد وارد کنید✔️')
            bot.register_next_step_handler(msg1, savediamonds, data, zarib, chat_id)
        else:
            diamond_db.save_bet(chat_id, user_id, diamond, data, zarib)
            diamond_db.add_diamond(chat_id, user_id, -1 * diamond)
            bot.send_message(user_id, f'''✦| شما با پیش بینی
برد {translatee(data)} و تعداد {diamond} المـ💎ـاس
با ضریب {zarib}
 وارد بت شدید ✔️''')
            bot.send_message(-1001134572701, f'''✦| [{message.from_user.first_name}](tg://user?id={user_id})  
با پیش بینی برد {translatee(data)} و تعداد {diamond} المـ💎ـاس با
 ضریب {zarib} 
 وارد بت شد✔️''',
                             parse_mode='Markdown')
    except:
        msg2 = bot.send_message(user_id, '✦|یک عدد وارد کنید✔️')
        bot.register_next_step_handler(msg2, savediamonds, data, zarib, chat_id)


@bot.message_handler(commands=['result'], func=Filters.group)
def check(message):
    global betting
    global partners
    if check_group(message):
        return
    chat_id = message.chat.id
    if betting[chat_id]:
        bot.reply_to(message, '✦|لطفا ابتدا شرط بندي را ببنديد')
        return
    user_id = message.from_user.id
    if not check_admin(chat_id, user_id):
        bot.reply_to(message, '✦| شما ادمین ربات نیستید✖️')
        return
    try:
        messag = message.text.split(" ")
        winner = messag[1]
    except:
        bot.reply_to(message, '''✦| دستور را همراه با اسم تیم وارد کنید ✖️

به شکل زیر👇🏼
/result gorg''')
        return
    if winner not in teams:
        bot.reply_to(message, '''✦| دستور را همراه با اسم تیم درست وارد کنید ✖️

به شکل زیر👇🏼
/result gorg''')
        return
    msgg = bot.send_message(message.chat.id, '✦| درحال بررسي...')
    msg = '•| لــیــســـت نــهـایـی شـرط بـنـدی |•'
    load = diamond_db.winners(chat_id, winner)
    users = load[0]
    diamond = load[1]
    zarib = load[2]
    msg += '\nᴡɪɴ🐾'
    for i, user in enumerate(users, start=0):
        try:
            bot.send_message(user,
                             f'''✦|تبریک 👍🏻
شما بت را بردید و {round(zarib[i] * diamond[i])} المـ💎ـاس بدست آوردید✔️''')
        except:
            pass
        diamond_db.save_record(chat_id, user, winner, zarib[i] * diamond[i], True)
        try:
            emoji = diamond_db.load_purchaseemoji(chat_id, user)
            x = bot.get_chat_member(chat_id=message.chat.id, user_id=user)
            if emoji:
                msg += f'\n[[{emoji}]]✔️[{x.user.first_name}](tg://user?id={x.user.id}) | +{round(zarib[i] * diamond[i])} 💎 |'
            else:
                msg += f'\n[[-]]✔️[{x.user.first_name}](tg://user?id={x.user.id}) | +{round(zarib[i] * diamond[i])} 💎 |'
        except:
            pass

    load = diamond_db.losers(chat_id, winner)
    users = load[0]
    diamond = load[1]
    team = load[2]
    j = 0
    msg += '\n'
    msg += '\nʟᴏsᴇ🕸'
    for i, user in enumerate(users, start=0):
        try:
            bot.send_message(user, f'''✦|متاسفم 👎🏾
شما بت را باختید و {diamond[i]} المـ💎ـاس را از دست دادید✖️''')
        except:
            pass
        diamond_db.save_record(chat_id, user, team[j], diamond[i], False)
        try:
            emoji = diamond_db.load_purchaseemoji(chat_id, user)
            x = bot.get_chat_member(chat_id=message.chat.id, user_id=user)
            if emoji:
                msg += f'\n[[{emoji}]]✖️[{x.user.first_name}](tg://user?id={x.user.id})  | -{round(diamond[i])} 💎|'
            else:
                msg += f'\n[[-]]✖️[{x.user.first_name}](tg://user?id={x.user.id})  | -{round(diamond[i])} 💎 |'
            j += 1
        except:
            j += 1
            pass
    msg += '\n\n/registerme 💎'
    msg += '\n༆𝒎𝒖𝒔𝒕 𝒃𝒆 𝒂 𝒍𝒖𝒑𝒊𝒏𝒆 𝒈𝒖𝒚 𝒕𝒐 𝒃𝒆 𝒂𝒍𝒊𝒗𝒆 💎'
    diamond_db.delete_data(chat_id)
    partners[chat_id].clear()
    try:
        bot.edit_message_text(message_id=msgg.message_id, chat_id=msgg.chat.id, text='✦| كامل شد✔️')
    except:
        pass
    bot.send_message(chat_id, msg, parse_mode='markdown')


@bot.message_handler(commands=['almasbede'], func=Filters.group)
def getdiamond(message):
    if check_group(message):
        return
    bot.reply_to(message, '''◇ معطل نکن هر چه سریع تر دستور زیر و لمس کن و با لینک دعوتت دوست های خودت بیار گپ و الماس بگیر...😉
[ /invitelink ]''')


@bot.message_handler(commands=['wallet'], func=Filters.group)
def info(message):
    if check_group(message):
        return
    msg = ''
    user_id = message.from_user.id
    chat_id = message.chat.id
    diamond = diamond_db.load_diamond(chat_id, user_id)
    if len(diamond) == 0:
        diamond.append(0)
    msg += f'مقدار الــــمــ💎ــاس شما [{diamond[0]}]'
    if diamond[0] < 5000:
        msg += '\nᴘʟᴀʏᴇʀ ʟᴇᴠᴇʟ [ᴀᴍᴀᴛᴇᴜʀ👶🏻]'
    elif 5000 <= diamond[0] < 15000:
        msg += '\nᴘʟᴀʏᴇʀ ʟᴇᴠᴇʟ [ʙᴇɢɪɴɴᴇʀ👦🏻]'
    elif 15000 <= diamond[0] < 50000:
        msg += '\nᴘʟᴀʏᴇʀ ʟᴇᴠᴇʟ [ᴘʀᴏғᴇssɪᴏɴᴀʟ👱🏻‍♀]'
    elif 50000 <= diamond[0] < 350000:
        msg += '\nᴘʟᴀʏᴇʀ ʟᴇᴠᴇʟ [sᴜᴘᴇʀsᴛᴀʀ🦸🏻]'
    elif 350000 <= diamond[0] < 500000:
        msg += '\nᴘʟᴀʏᴇʀ ʟᴇᴠᴇʟ [ʟᴇɢᴇɴᴅᴀʀʏ🧝🏻]'
    elif diamond[0] >= 500000:
        msg += '\nᴘʟᴀʏᴇʀ ʟᴇᴠᴇʟ [ᴜʟᴛɪᴍᴀᴛᴇ🤴🏻]'
    try:
        emoji = diamond_db.load_purchaseemoji(chat_id, user_id)
        if emoji:
            msg += f'\nᴇᴍᴏᴊɪ [{emoji}]'
        else:
            msg += f'\nᴇᴍᴏᴊɪ [-]'
        rank = diamond_db.load_rank(chat_id, user_id)
        if rank:
            msg += f'\nʀᴀɴᴋ [{rank}]'
        else:
            msg += f'\nʀᴀɴᴋ [-]'
        bot.reply_to(message, msg)
    except:
        bot.reply_to(message, f'✦|شما {0} المـ💎ـاس دارید✔️')


@bot.message_handler(commands=['registerme'], func=Filters.group)
def reg(message):
    chat_id = message.chat.id
    user_id = message.from_user.id
    bot.send_message(chat_id, '❖برای ثبـت نـام در ربات دکمـه زیر رو بزنیــد❖', reply_markup=build_markup1(chat_id))


@bot.message_handler(commands=['rolebet'], func=Filters.group)
def role_bet(message):
    global rolling
    global rolepartners
    if check_group(message):
        return
    chat_id = message.chat.id
    if not rolling[chat_id]:
        bot.reply_to(message, '✦| بت غیرفعال است✖️')
        return
    user_id = message.from_user.id
    if not diamond_db.check_register(user_id):
        bot.send_message(chat_id=message.chat.id, reply_to_message_id=message.message_id,
                         text='''✦|برای شروع بت اول باید در ربات ثبت نام کنید✖️''', reply_markup=build_markup1(chat_id))
        return
    if user_id in rolepartners[chat_id]:
        msg = bot.reply_to(message, '✦|امكان مجدد شری بندي براي شما وجود ندارد')
        time.sleep(3)
        try:
            bot.delete_message(chat_id, msg.message_id)
        except:
            pass
        return
    try:
        msg1 = bot.send_message(user_id, '''بـت آغاز شـــد💥

    ↲ حدس میزنید نقش شما در بازی بعد کدام است؟ ↳''', reply_markup=build_markup4())
    except:
        bot.send_message(chat_id, '✦| ابتدا ربات را استارت کنید و مجدد این دستور را بزنید ✖️')
        return
    if user_id not in rolepartners[chat_id]:
        rolepartners[chat_id].append(user_id)
    msg = bot.reply_to(message, '✦|پیام بت در pv  برای شما ارسال شد ✔️')
    time.sleep(2)
    try:
        bot.delete_message(chat_id, msg.message_id)
    except:
        pass
    bot.register_next_step_handler(msg1, submitrole, chat_id)


def submitrole(message, chat_id):
    if not rolling:
        bot.send_message(message.chat.id, '✦| بت غیرفعال است✖️')
        return
    roles = ['روستایی', 'گرگینه', 'مست', 'پیشگو', 'نفرین شده', 'فاحشه', 'ناظر', 'تفنگدار', 'خائن', 'فرشته نگهبان',
             'کاراگاه', 'پیشگوی رزرو', 'شکارچی', 'بچه وحشی', 'احمق', 'فراماسون', 'همزاد', 'الهه عشق',
             'کلانتر', 'قاتل زنجیره ای', 'منافق', 'کدخدا', 'شاهزاده', 'جادوگر', 'پسر گیج', 'آهنگر', 'گرگ آلفا',
             'توله گرگ',
             'پیشگوی نگاتیوی', 'گرگ نما', 'گرگ ایکس', 'صلح گرا', 'ریش سفید', 'دزد', 'دردسرساز', 'شیمیدان', 'گرگ برفی',
             'گورکن', 'رمال', 'آتش زن']
    user_id = message.chat.id
    try:
        role = str(message.text)
    except:
        msg = bot.send_message(user_id, 'لطفا از دکمه های موجود استفاده کنید', reply_markup=build_markup4())
        bot.register_next_step_handler(msg, submitrole, chat_id)
        return
    if message.text not in roles:
        msg = bot.send_message(user_id, 'لطفا از دکمه های موجود استفاده کنید', reply_markup=build_markup4())
        bot.register_next_step_handler(msg, submitrole, chat_id)
        return
    markup = types.ReplyKeyboardMarkup(one_time_keyboard=True, resize_keyboard=2)
    markup.add('cancel✖️')
    msg = bot.send_message(user_id, '''✦| با موفقیت ثبت شد✔️
    از چند المـ💎ـاس برای این بت استفاده میکنید؟''',
                           reply_markup=markup)
    zarib = round(random.uniform(1.5, 4), 1)
    bot.register_next_step_handler(msg, submitbet, message.text, zarib, chat_id)


def submitbet(message, role, zarib, chat_id):
    global rolepartners
    user_id = message.from_user.id
    if message.text == 'cancel✖️':
        bot.reply_to(message, '''✦| این بت لغو شد
برای شروع بت جدید در گروه دستور
/rolebet@LupinBet_bot 
    را بزنید✔️''')
        if user_id in rolepartners[chat_id]:
            rolepartners[chat_id].remove(user_id)
        return
    if not rolling[chat_id]:
        bot.send_message(user_id, '✦| بت غیرفعال است✖️')
        return
    try:
        diamond = int(message.text)
        if diamond > 100000:
            msg1 = bot.send_message(user_id, '''سقف شرط بندي 100000 الماس ميباشد
    لطفا عدد زير 1000000 وارد كنيد''')
            bot.register_next_step_handler(msg1, submitbet, role, zarib, chat_id)
            return
        inventory = diamond_db.load_diamond(chat_id, user_id)
        if diamond > round(inventory[0]) or diamond <= 0:
            msg = '✦| تعداد  المـ💎ـاس های شما کافی نیست ✖️'
            dia = diamond_db.load_diamond(chat_id, user_id)
            try:
                msg += f'''\nموجودي شما در حال حاضر : {dia[0]} 💎'''
            except:
                msg += f'''\nموجودي شما در حال حاضر : {0} 💎'''
            bot.send_message(user_id, msg)
            msg1 = bot.send_message(user_id, '✦|یک عدد وارد کنید✔️')
            bot.register_next_step_handler(msg1, submitbet, role, zarib, chat_id)
            return
        else:
            diamond_db.save_rolebet(chat_id, user_id, diamond, role, zarib)
            bot.send_message(user_id, f'''✦| شما با پیش بینی
    {role} و تعداد {diamond} المـ💎ـاس
    با ضریب {zarib}
     وارد بت شدید ✔️''')
            bot.send_message(-1001134572701, f'''✦| [{message.from_user.first_name}](tg://user?id={user_id})  
    با پیش بینی {role} و تعداد {diamond} المـ💎ـاس با
     ضریب {zarib} 
     وارد بت شد✔️''',
                             parse_mode='Markdown')
    except:
        msg2 = bot.send_message(user_id, '✦|یک عدد وارد کنید✔️')
        bot.register_next_step_handler(msg2, submitbet, role, zarib, chat_id)


def build_markup4():
    roles = ['روستایی', 'گرگینه', 'مست', 'پیشگو', 'نفرین شده', 'فاحشه', 'ناظر', 'تفنگدار', 'خائن', 'فرشته نگهبان',
             'کاراگاه', 'پیشگوی رزرو', 'شکارچی', 'بچه وحشی', 'احمق', 'فراماسون', 'همزاد', 'الهه عشق', 'کلانتر',
             'قاتل زنجیره ای', 'منافق',
             'کدخدا', 'شاهزاده', 'جادوگر', 'پسر گیج', 'آهنگر', 'گرگ آلفا', 'توله گرگ', 'پیشگوی نگاتیوی', 'گرگ نما',
             'گرگ ایکس', 'صلح گرا', 'ریش سفید', 'دزد', 'دردسرساز', 'شیمیدان', 'گرگ برفی', 'گورکن', 'رمال', 'آتش زن']
    li = []
    markup = types.ReplyKeyboardMarkup(one_time_keyboard=True, resize_keyboard=2)
    for e, i in enumerate(roles, start=1):
        li.append(i)
        if e % 3 == 0 and e:
            markup.add(telebot.types.KeyboardButton(li[0]), telebot.types.KeyboardButton(li[1]),
                       telebot.types.KeyboardButton(li[2]))
            li = []
    if li:
        if len(li) == 1:
            markup.add(telebot.types.KeyboardButton(li[0]))
        else:
            markup.add(telebot.types.KeyboardButton(li[0]), telebot.types.KeyboardButton(li[1]))
    return markup


def build_markup1(chat_id):
    markup = InlineKeyboardMarkup()
    url = f'https://t.me/LupinBet_bot?start={chat_id}'
    markup.add(InlineKeyboardButton('ثبت نام📑', url=url))
    return markup


def build_markup2(chat_id):
    markup = InlineKeyboardMarkup()
    markup.add(InlineKeyboardButton('𖡼ᏝᏬᎮᎥᏁ ˡⁱᵛᵉ🐾⛓', url='https://t.me/joinchat/TxWA3pBIxIT8EFRX'))
    markup.add(InlineKeyboardButton('𖡼ᏝᏬᎮᎥᏁ ʰⁱˢᵗᵒʳʸ🐾', url='t.me/LUPINe_history'))
    # markup.add(InlineKeyboardButton('~ᴡᴏʟᴠᴇʀɪɴᴇꜱ [ʟɪᴠᴇ]🍷', url='t.me/joinchat/AAAAAFc62-0ttvA2Nm2DMg'))
    # markup.add(InlineKeyboardButton('ωσℓνєяιηєѕ cнαηηєℓ🥂', url='t.me/wolverines_org'))
    markup.add(InlineKeyboardButton('عضو شدم✅', callback_data=f'check_channel {chat_id}'))
    return markup


@bot.message_handler(commands=['getstate'], func=Filters.group)
def state(message):
    if check_group(message):
        return
    chat_id = message.chat.id
    if message.reply_to_message:
        user_id = message.reply_to_message.from_user.id
        firstname = message.reply_to_message.from_user.first_name
    else:
        user_id = message.from_user.id
        firstname = message.from_user.first_name
    state = diamond_db.load_state(chat_id, user_id)
    bw = diamond_db.stats(chat_id, user_id)
    dia = diamond_db.load_diamond(chat_id, user_id)
    if len(dia) == 0:
        dia.append(0)
    msg = f'sᴛᴀᴛᴇ ғᴏʀ [{firstname}](tg://user?id={user_id})'
    if dia[0] < 5000:
        msg += '\nᴘʟᴀʏᴇʀ ʟᴇᴠᴇʟ [[ᴀᴍᴀᴛᴇᴜʀ👶🏻]]'
    elif 5000 <= dia[0] < 15000:
        msg += '\nᴘʟᴀʏᴇʀ ʟᴇᴠᴇʟ [[ʙᴇɢɪɴɴᴇʀ👦🏻]]'
    elif 15000 <= dia[0] < 50000:
        msg += '\nᴘʟᴀʏᴇʀ ʟᴇᴠᴇʟ [[ᴘʀᴏғᴇssɪᴏɴᴀʟ👱🏻‍♀]]'
    elif 50000 <= dia[0] < 350000:
        msg += '\nᴘʟᴀʏᴇʀ ʟᴇᴠᴇʟ [[sᴜᴘᴇʀsᴛᴀʀ🦸🏻]]'
    elif 350000 <= dia[0] < 500000:
        msg += '\nᴘʟᴀʏᴇʀ ʟᴇᴠᴇʟ [[ʟᴇɢᴇɴᴅᴀʀʏ🧝🏻]]'
    elif dia[0] >= 500000:
        msg += '\nᴘʟᴀʏᴇʀ ʟᴇᴠᴇʟ [[ᴜʟᴛɪᴍᴀᴛᴇ🤴🏻]]'
    emoji = diamond_db.load_purchaseemoji(chat_id, user_id)
    if emoji:
        msg += f'\nᴇᴍᴏᴊɪ [[{emoji}]]'
    else:
        msg += f'\nᴇᴍᴏᴊɪ [[-]]'
    rank = diamond_db.load_rank(chat_id, user_id)
    if rank:
        msg += f'\nʀᴀɴᴋ [[{rank}]]'
    else:
        msg += f'\nʀᴀɴᴋ [[-]]'
    msg += f'''\n`{state[0]}` تـعـداد بت🎰'''
    msg += f'''\n`{state[1]}` تــــعــــداد بــꜛــرد🏆'''
    msg += f'''\n`{state[2]}` تــــعــــداد بـاخـــꜜـت 🕳'''
    if bw[0] is None:
        msg += f'''\n`{0}` بـهـتـریـن بـت ✨'''
    else:
        msg += f'''\n`{bw[0]}` بـهـتـریـن بـت ✨'''
    if bw[1] is None:
        msg += f'''\n`{0}` بـدتـریـن بـت 💥'''
    else:
        msg += f'''\n`{bw[1]}` بـدتـریـن بـت 💥'''
    if state[3] is None:
        msg += f'''\n`{0}` الــــمـــ💎ـاس دریافــت کردی...'''
    else:
        msg += f'''\n`{state[3]}` الــــمـــ💎ـاس دریافــت کردی...'''
    if state[4] is None:
        msg += f'''\n`{0}` الــــمــ💎ــاس از دســت دادی...'''
    else:
        msg += f'''\n`{state[4]}` الــــمــ💎ــاس از دســت دادی...'''
    try:
        msg += f'''\n`{dia[0]}` ✜ موجودی ✜'''
    except:
        msg += f'''\n`{0}` ✜ موجودی ✜'''
    msg += '\n༆𝒎𝒖𝒔𝒕 𝒃𝒆 𝒂 𝒍𝒖𝒑𝒊𝒏𝒆 𝒈𝒖𝒚 𝒕𝒐 𝒃𝒆 𝒂𝒍𝒊𝒗𝒆 💎'
    bot.send_message(chat_id, msg, parse_mode='markdown')


@bot.message_handler(commands=['bestbet'], func=Filters.group)
def best(message):
    if check_group(message):
        return
    chat_id = message.chat.id
    best = diamond_db.get_best(chat_id)
    rank = ['🥇', '🥈', '🥉', '', '']
    user = best[0]
    diamond = best[1]
    msg = 'پــــنــــج بــــت باز بــــرتــــر گروه🐾\n'
    j = 1
    for i in user:
        try:
            if diamond[j - 1] < 5000:
                level = 'ᴀᴍᴀᴛᴇᴜʀ'
            elif 5000 <= diamond[j - 1] < 15000:
                level = 'ʙᴇɢɪɴɴᴇʀ'
            elif 15000 <= diamond[j - 1] < 50000:
                level = 'ᴘʀᴏғᴇssɪᴏɴᴀʟ'
            elif 50000 <= diamond[j - 1] < 350000:
                level = 'sᴜᴘᴇʀsᴛᴀʀ'
            elif 350000 <= diamond[j - 1] < 500000:
                level = 'ʟᴇɢᴇɴᴅᴀʀʏ'
            elif diamond[j - 1] >= 500000:
                level = 'ᴜʟᴛɪᴍᴀᴛᴇ'
            emoji = diamond_db.load_purchaseemoji(chat_id, i)
            x = bot.get_chat_member(chat_id=message.chat.id, user_id=i)
            if emoji:
                msg += f'\n{rank[j - 1]}[[{emoji}]] [{x.user.first_name}](tg://user?id={x.user.id}) | `{diamond[j - 1]}` 💎 | {level}'
            else:
                msg += f'\n{rank[j - 1]}[[-]] [{x.user.first_name}](tg://user?id={x.user.id}) | `{diamond[j - 1]}` 💎 | {level}'
            j += 1
        except:
            pass
    bets = diamond_db.get_best_bet(chat_id)
    users = bets[0]
    diamonds = bets[1]
    teames = translate(bets[2])
    msg += '\n\n➰➰➰➰➰➰➰➰➰➰➰➰'
    msg += '\nپــــنــــج بــــت بــــرتــــر گروه🐾\n'
    j = 1
    for i in users:
        try:
            emoji = diamond_db.load_purchaseemoji(chat_id, i)
            x = bot.get_chat_member(chat_id=message.chat.id, user_id=i)
            if emoji:
                msg += f'\n{rank[j - 1]}[[{emoji}]] [{x.user.first_name}](tg://user?id={x.user.id}) ⊰ ᴘʀᴏғɪᴛ ⊱ `{round(diamonds[j - 1])}` 💎 | ⊰ ʙᴇᴛ ᴏɴ ⊱{teames[j - 1]}'
            else:
                msg += f'\n{rank[j - 1]}[[-]] [{x.user.first_name}](tg://user?id={x.user.id}) ⊰ ᴘʀᴏғɪᴛ ⊱ `{round(diamonds[j - 1])}` 💎 |⊰ ʙᴇᴛ ᴏɴ ⊱{teames[j - 1]}'
            j += 1
        except:
            pass
    msg += '\n\n༆𝒎𝒖𝒔𝒕 𝒃𝒆 𝒂 𝒍𝒖𝒑𝒊𝒏𝒆 𝒈𝒖𝒚 𝒕𝒐 𝒃𝒆 𝒂𝒍𝒊𝒗𝒆 💎'
    bot.send_message(chat_id, msg, parse_mode='Markdown')


def translate(teamss):
    translated = []
    for i in teamss:
        if i == 'ghatel':
            translated.append('قاتل')
        elif i == 'roosta':
            translated.append('روستا')
        elif i == 'gorg':
            translated.append('گرگ')
        elif i == 'atash':
            translated.append('آتش زن')
        elif i == 'ferghe':
            translated.append('فرقه')
        elif i == 'monafegh':
            translated.append('منافق')
    return translated


def translatee(teamss):
    if teamss == 'ghatel':
        return 'قاتل'
    elif teamss == 'roosta':
        return 'روستا'
    elif teamss == 'gorg':
        return 'گرگ'
    elif teamss == 'atash':
        return 'آتش زن'
    elif teamss == 'ferghe':
        return 'فرقه'
    elif teamss == 'monafegh':
        return 'منافق'


@bot.message_handler(commands=['checkplayers'], func=Filters.user(
    [1121528614, 638994540, 941773249, 1218919578, 562842109, 416527724, 1236372753, 1258617062]))
def checking(message):
    global checkrole
    global rolepartners
    chat_id = message.chat.id
    if not message.reply_to_message:
        return
    all = message.reply_to_message.entities
    users = []
    for player in all:
        try:
            diamond_db.add_diamond(chat_id, player.user.id, 2)
            users.append(player.user.id)
        except:
            pass
    bot.send_message(chat_id, 'به تمام پلیرهای این بازی دو 💎 افزوده شد✅')

    if diamond_db.load_user(chat_id):
        if chat_id == -1001476763360:
            group = '🐾𖡼ᏝᏬᎮᎥᏁ ꪡᴏʟғ⸸🐾'
            link = lupin_link
            hy_link = f'[{group}]({link})'
        elif chat_id == -1001128468995:
            group = 'ωσℓνєяιηєѕ🥂'
            link = 'https://t.me/joinchat/SiQiUkNDEgM6tLiDXMr68w'
            hy_link = f'[{group}]({link})'
        users = diamond_db.load_user(chat_id)
        for user in users:
            try:
                bot.send_message(user, f'''هم اکنون گیمی که روی آن شرط بسته بودید در گروه
                {hy_link}          
                            آغاز شد. زود جوین بده''', parse_mode='markdown', disable_web_page_preview=True)
            except:
                pass
    if checkperson[chat_id]:
        user = diamond_db.get_users(chat_id)
        user_id = user[0]
        bet_user = user[1]
        diamond = user[2]
        zarib = user[3]
        j = 0
        game = wwresult.WWGame(message.reply_to_message)
        winners = game.game_winners()
        win = []
        msg = '✦|ليست نهايي شرط بندي:'
        for player in winners:
            win.append(player.user_id)
        for player in user_id:
            if bet_user[j] in win:
                diamond_db.add_diamond(chat_id, player, zarib[j] * diamond[j])
                try:
                    bot.send_message(player,
                                     f'''✦|تبریک 👍🏻
                شما بت را بردید و{round(zarib[j] * diamond[j])} المـ💎ـاس بدست آوردید✔️''')
                except:
                    pass
                try:
                    emoji = diamond_db.load_purchaseemoji(chat_id, player)
                    x = bot.get_chat_member(chat_id=message.chat.id, user_id=player)
                    if emoji:
                        msg += f'\n[[{emoji}]] |✔️[{x.user.first_name}](tg://user?id={x.user.id}) | +`{round(zarib[j] * diamond[j])}` 💎 |'
                    else:
                        msg += f'\n[[-]]|✔️[{x.user.first_name}](tg://user?id={x.user.id}) | +`{round(zarib[j] * diamond[j])}` 💎 |'
                except:
                    pass
            else:
                diamond_db.add_diamond(chat_id, player, -1 * diamond[j])
                try:
                    bot.send_message(player, f'''✦|متاسفم 👎🏾
                شما بت را باختید و{diamond[j]} المـ💎ـاس را از دست دادید✖️''')
                except:
                    pass
                try:
                    emoji = diamond_db.load_purchaseemoji(chat_id, player)
                    x = bot.get_chat_member(chat_id=message.chat.id, user_id=player)
                    if emoji:
                        msg += f'\n[[{emoji}]] |✖️[{x.user.first_name}](tg://user?id={x.user.id}) | -`{round(diamond[j])}` 💎 |'
                    else:
                        msg += f'\n[[-]]|✖️[{x.user.first_name}](tg://user?id={x.user.id}) | -`{round(diamond[j])}` 💎 |'
                except:
                    pass
            j += 1
            continue
        msg += '\n\n/registerme 💎'
        msg += '\n༆𝒎𝒖𝒔𝒕 𝒃𝒆 𝒂 𝒍𝒖𝒑𝒊𝒏𝒆 𝒈𝒖𝒚 𝒕𝒐 𝒃𝒆 𝒂𝒍𝒊𝒗𝒆 💎'
        bot.send_message(chat_id, msg, parse_mode='markdown')
        checkperson[chat_id] = False
        diamond_db.delete_persondb(chat_id)
        personpartners[chat_id].clear()

    if not checkrole[chat_id]:
        return
    j = 0
    game = wwresult.WWGame(message.reply_to_message.text)
    msg = '✦|ليست نهايي شرط بندي:'
    for player in game.players:
        if diamond_db.check_player(chat_id, users[j]):
            load = diamond_db.load_data(chat_id, users[j])
            diamond = load[0]
            role = load[1]
            zarib = load[2]
            if re.search(role[0], player.player_role):
                diamond_db.add_diamond(chat_id, users[j], zarib[0] * diamond[0])
                try:
                    bot.send_message(users[j],
                                     f'''✦|تبریک 👍🏻
شما بت را بردید و{round(zarib[0] * diamond[0])} المـ💎ـاس بدست آوردید✔️''')
                except:
                    pass
                try:
                    emoji = diamond_db.load_purchaseemoji(chat_id, users[j])
                    x = bot.get_chat_member(chat_id=message.chat.id, user_id=users[j])
                    if emoji:
                        msg += f'\n[[{emoji}]] |✔️[{x.user.first_name}](tg://user?id={x.user.id}) | +`{round(zarib[0] * diamond[0])}` 💎 |'
                    else:
                        msg += f'\n[[-]]|✔️[{x.user.first_name}](tg://user?id={x.user.id}) | +`{round(zarib[0] * diamond[0])}` 💎 |'
                except:
                    pass
            else:
                diamond_db.add_diamond(chat_id, users[j], -1 * diamond[0])
                try:
                    bot.send_message(users[j], f'''✦|متاسفم 👎🏾
شما بت را باختید و{diamond[0]} المـ💎ـاس را از دست دادید✖️''')
                except:
                    pass
                try:
                    emoji = diamond_db.load_purchaseemoji(chat_id, users[j])
                    x = bot.get_chat_member(chat_id=message.chat.id, user_id=users[j])
                    if emoji:
                        msg += f'\n[[{emoji}]] |✖️[{x.user.first_name}](tg://user?id={x.user.id}) | -`{round(diamond[0])}` 💎 |'
                    else:
                        msg += f'\n[[-]]|✖️[{x.user.first_name}](tg://user?id={x.user.id}) | -`{round(diamond[0])}` 💎 |'
                except:
                    pass
            diamond_db.delete_user(chat_id, users[j])
            j += 1
            continue
        else:
            j += 1
            continue
    users = diamond_db.load_roleuser(chat_id)
    for i in users:
        load = diamond_db.load_data(chat_id, i)
        diamond = load[0]
        diamond_db.add_diamond(chat_id, i, -1 * diamond[0])
        diamond_db.delete_user(chat_id, i)
    msg += '\n\n/registerme 💎'
    msg += '\n༆𝒎𝒖𝒔𝒕 𝒃𝒆 𝒂 𝒍𝒖𝒑𝒊𝒏𝒆 𝒈𝒖𝒚 𝒕𝒐 𝒃𝒆 𝒂𝒍𝒊𝒗𝒆 💎'
    bot.send_message(chat_id, msg, parse_mode='markdown')
    checkrole[chat_id] = False
    rolepartners[chat_id].clear()
    users.clear()


@bot.message_handler(commands=['checkroles'], func=Filters.group)
def checking(message):
    global checkrole
    chat_id = message.chat.id
    user_id = message.from_user.id
    if check_group(message):
        return
    if not check_admin(chat_id, user_id):
        bot.reply_to(message, '✦| شما ادمین ربات نیستید✖️')
        return
    if checkrole[chat_id]:
        return
    checkrole[chat_id] = True
    bot.send_message(message.chat.id, 'actived')


def build_markup6(emoji):
    li = []
    markup = types.ReplyKeyboardMarkup(one_time_keyboard=True, resize_keyboard=2)
    for e, i in enumerate(emoji, start=1):
        li.append(i)
        if e % 3 == 0 and e:
            markup.add(telebot.types.KeyboardButton(li[0]), telebot.types.KeyboardButton(li[1]),
                       telebot.types.KeyboardButton(li[2]))
            li = []
    if li:
        if len(li) == 1:
            markup.add(telebot.types.KeyboardButton(li[0]))
        else:
            markup.add(telebot.types.KeyboardButton(li[0]), telebot.types.KeyboardButton(li[1]))
    markup.add('cancel❌')
    return markup


def build_markup11(user_id, chat_id):
    markup = InlineKeyboardMarkup()
    if chat_id == lupin:
        markup.add(InlineKeyboardButton('𖡼ᏝᏬᎮᎥᏁ🐾 LINK', url=lupin_link))
    markup.add(InlineKeyboardButton('عضو شدم✅', callback_data=f'checkinvite {user_id} {chat_id}'))
    return markup


@bot.message_handler(commands=['bestinviters'])
def best_inviters(message):
    chat_id = message.chat.id
    if check_group(message):
        return
    load = diamond_db.best_inviters()
    rank = ['🥇', '🥈', '🥉', '🏅', '🎖']
    users = load[0]
    counts = load[1]
    j = 1
    msg = '⌬ پــنــج دعــوت دهــنــده بــرتــر:\n'
    for i in users:
        try:
            emoji = diamond_db.load_purchaseemoji(chat_id, i)
            x = bot.get_chat_member(chat_id=message.chat.id, user_id=i)
            if emoji:
                msg += f'\n{rank[j - 1]}[[{emoji}]] | [{x.user.first_name}](tg://user?id={x.user.id}) | `{counts[j - 1]}` |'
            else:
                msg += f'\n{rank[j - 1]}[[-]] | [{x.user.first_name}](tg://user?id={x.user.id}) | `{counts[j - 1]}` |'
            j += 1
        except:
            pass
    msg += '''\n◇ معطل نکن هر چه سریع تر دستور زیر و لمس کن و با لینک دعوت دوست های خودت بیار گپ و الماس بگیر...😉
[ /invitelink ]'''
    msg += '\n\n༆𝒎𝒖𝒔𝒕 𝒃𝒆 𝒂 𝒍𝒖𝒑𝒊𝒏𝒆 𝒈𝒖𝒚 𝒕𝒐 𝒃𝒆 𝒂𝒍𝒊𝒗𝒆 💎'
    bot.send_message(chat_id, msg, parse_mode='markdown')


@bot.message_handler(commands=['myclub'])
def myplayers(message):
    chat_id = message.chat.id
    user_id = message.from_user.id
    if check_group(message):
        return
    players = diamond_db.myplayers(user_id)
    j = 1
    msg = '⌬ افــراد دعــوت شدهــ توسط شما:\n'
    for i in players:
        try:
            x = bot.get_chat_member(chat_id=message.chat.id, user_id=i)
            msg += f'\n{j}- [{x.user.first_name}](tg://user?id={x.user.id}) 💎'
            j = j + 1
        except:
            pass
    msg += '''\n◇ معطل نکن هر چه سریع تر دستور زیر و لمس کن و با لینک دعوت دوست های خودت بیار گپ و الماس بگیر...😉
[ /invitelink ]'''
    msg += '\n\n༆𝒎𝒖𝒔𝒕 𝒃𝒆 𝒂 𝒍𝒖𝒑𝒊𝒏𝒆 𝒈𝒖𝒚 𝒕𝒐 𝒃𝒆 𝒂𝒍𝒊𝒗𝒆 💎'
    bot.send_message(chat_id, msg, parse_mode='Markdown')


@bot.message_handler(commands=['invitelink'], func=Filters.group)
def build_link(message):
    user_id = message.from_user.id
    chat_id = message.chat.id
    if check_group(message):
        return
    if not diamond_db.check_register(user_id):
        bot.send_message(chat_id=message.chat.id, reply_to_message_id=message.message_id,
                         text='''✦|برای دريافت لينك اول باید در ربات ثبت نام کنید✖️''',
                         reply_markup=build_markup1(chat_id))
        return
    try:
        if get_stats(user_id)['gamesPlayed'] < 40:
            bot.reply_to(message, '⌬ استیت شما از حد مجاز [ حداقل 40 ]  پایین‌تر است...✖️')
            return
    except:
        bot.reply_to(message, '⌬ استیت شما از حد مجاز [ حداقل 40 ]  پایین‌تر است...✖️')
        return
    msg = '''لینک دعوت شما ساخته شد و شما با فرستادن این لینک به دوستان خود و دعوت از آنها به گپ [ درصورتی که افراد با لینک دعوت شما بات را استارت و عضو گپ شدن ] مقدار 400 الــمــاســ💎 بگیر...🐾
    🖇تــوجــهــ: [ Sᴛᴀᴛs ꜛ 40 ]'''
    msg += f'\n\nhttps://t.me/LupinBet_bot?start=invite-{user_id}{chat_id} 📎'
    try:
        bot.send_message(user_id, msg, disable_web_page_preview=True)
        bot.reply_to(message, 'لینک شما در pv ارسال شد')
    except:
        bot.reply_to(message, 'لطفا ابتدا بات را استارت نمونده سپس دستور را ارسال نمایید')


# @bot.message_handler(commands=['invitelink'], func=Filters.private)
# def build_link(message):
#     user_id = message.chat.id
#     if not diamond_db.check_register(user_id):
#         bot.send_message(chat_id=message.chat.id, reply_to_message_id=message.message_id,
#                          text='''✦|برای شروع بت اول باید در ربات ثبت نام کنید✖️''', reply_markup=build_markup1(lupin))
#         return
#     try:
#         if get_stats(user_id)['gamesPlayed'] < 40:
#             bot.reply_to(message, '⌬ استیت شما از حد مجاز [ حداقل 40 ]  پایین‌تر است...✖️')
#             return
#     except:
#         bot.reply_to(message, '⌬ استیت شما از حد مجاز [ حداقل 40 ]  پایین‌تر است...✖️')
#         return
#     msg = '''لینک دعوت شما ساخته شد و شما با فرستادن این لینک به دوستان خود و دعوت از آنها به گپ [ درصورتی که افراد با لینک دعوت شما بات را استارت و عضو گپ شدن ] مقدار 400 الــمــاســ💎 بگیر...🐾
# 🖇تــوجــهــ: [ Sᴛᴀᴛs ꜛ 40 ]'''
#     msg += f'\n\nhttps://t.me/LupinBet_bot?start=invite-{user_id}-{chat_id} 📎'
#     bot.send_message(user_id, msg, disable_web_page_preview=True)


@bot.message_handler(commands=['shop'], func=Filters.group)
def shops(message):
    try:
        bot.reply_to(message, '🛒   ‌فروشگاه برای شما در پیوی ارسال شد.')
        start2(message.from_user.id)
    except:
        bot.reply_to(message, "لطفا ابتدا ربات را استارت نمایید")


@bot.message_handler(commands=['start'], func=Filters.private)
def start(message):
    chat_id = message.chat.id
    user_id = message.from_user.id
    try:
        text = message.text
        text = text.split(' ')
        if re.search('invite', text[1]):
            text = text[1].split('-')
            chatid = int(text[2]) * -1
            if user_id == int(text[1]):
                bot.send_message(user_id, '⌬ شما نمی‌توانید خودتون رو دعوت کنید...✖️')
                return
            bot.send_message(user_id,
                             f'''🕹 شما توسط به گروه بازی لوپین دعوت شده‌اید با جوین دادن به گروه توسط دکمه زیر میتونی 200 الــمــاســ💎 بگیری و دعوت خود را كامل كنيد...📱''',
                             reply_markup=build_markup11(int(text[1]), chatid))
        else:
            chat = text[1]
            if diamond_db.check_register(user_id):
                bot.send_message(user_id, 'شما ثبت نام کرده ایید📑')
            else:
                diamond_db.register(user_id)
                diamond_db.add_diamond(chat, user_id, 20)
                bot.send_message(user_id, '''✦| شما با موفقیت در ربات بت ثبت نام شدید و 20 المـ💎ـاس دریافت کرديد✔️

✦| پلیر عزیز 
با عضو شدن در دو کانال زیر میتوانید 20 المـ💎ـاس دریافت کنید✔️'''
                                 , reply_markup=build_markup2(chat))

    except IndexError:
        bot.send_message(chat_id, '''᪥᪥᪥᪥᪥᪥᪥᪥᪥᪥᪥᪥᪥᪥᪥᪥᪥᪥᪥᪥᪥᪥᪥᪥
به ربات لوپین بِت خوش آمدید 🐾

تجربه ایی متفاوت برای اولین بار در ورولف💎

شما با استفاده از این ربات قادر خواهید بود روی برد تیم مورد نظر خود شرط بسته و الماس کسب کنید💎

برای شرط بندی باید حتما در گروه لوپین ولف عضو باشید تا از ساعت باز شدن شرط بندی و چالش ها و روش ها برای دریافت الماس و خرج آن اطلاع کسب کنید💎

راهنمای ربات : /help 💎


 ༆𝒎𝒖𝒔𝒕 𝒃𝒆 𝒂 𝒍𝒖𝒑𝒊𝒏𝒆 𝒈𝒖𝒚 𝒕𝒐 𝒃𝒆 𝒂𝒍𝒊𝒗𝒆 💎
        ᪥᪥᪥᪥᪥᪥᪥᪥᪥᪥᪥᪥᪥᪥᪥᪥᪥᪥᪥᪥᪥᪥᪥᪥''')


def start2(chat_id):
    markup = types.ReplyKeyboardMarkup(one_time_keyboard=True, resize_keyboard=2)
    markup.add('فروشگاه🏢')
    markup.add('رنک اختصاصی💎')
    markup.add('cancel❌')
    msg = bot.send_message(chat_id, '''‌    🛍    به فروشگاه لوپین ولف خوش آمدید.
  -  لطفا یکی از گزینه های زیر را انتخاب کنید.''', reply_markup=markup)
    bot.register_next_step_handler(msg, shop)
    return


def shop(message):
    text = message.text
    user_id = message.chat.id

    if not diamond_db.check_register(user_id):
        group = '🐾𖡼ᏝᏬᎮᎥᏁ ꪡᴏʟғ⸸🐾'
        link = 'https://t.me/joinchat/aO3cMk0UriEyYmEx'
        lup_link = f'[{group}]({link})'
        bot.send_message(chat_id=message.chat.id, reply_to_message_id=message.message_id,
                         text=f'''شما در بات ثــــبــــت نــــام نیستید با جوین شدن در گپ

{lup_link}

نسبت به ثبت نام اقدام کنید...🐾🕷''', parse_mode='markdown', disable_web_page_preview=True)
        return

    if text == 'cancel❌':
        bot.send_message(user_id, 'کنسل شد')
        return
    elif text == 'فروشگاه🏢':
        emoji = diamond_db.load_emoji()
        msg = bot.send_message(user_id, 'به فروشگاه خوش اومدید ایــــمــــوجــــی مورد نظر خود را انتخاب کنید...🐾',
                               reply_markup=build_markup6(emoji))
        bot.register_next_step_handler(msg, emojishop, emoji)
        return
    elif text == 'رنک اختصاصی💎':
        markup = types.ReplyKeyboardMarkup(one_time_keyboard=True, resize_keyboard=2)
        markup.add('🐾𖡼ᏝᏬᎮᎥᏁ ꪡᴏʟғ⸸🐾')
        markup.add('cancel❌')
        msg = bot.send_message(user_id,
                               f'''هزینه رنک اختصاصی 10000 الماس میباشد
رنک را برای کدام گپ میخواهید؟''', reply_markup=markup)
        bot.register_next_step_handler(msg, chooserank)
        return
    else:
        bot.send_message(user_id, 'لطفا از دکــــمــــه های موجود استفاده کنید...🕹')
        start2(user_id)


def chooserank(message):
    user_id = message.chat.id
    text = message.text

    if text == 'cancel❌':
        bot.send_message(user_id, 'کنسل شد')
        return

    elif text == '🐾𖡼ᏝᏬᎮᎥᏁ ꪡᴏʟғ⸸🐾':
        inventory = diamond_db.load_diamond(lupin, user_id)
        cost = 10000

        try:
            if cost > round(inventory[0]):
                bot.send_message(user_id, f'''موجودی شما کافی نیست...✖️
            موجودی شما [{inventory[0]}💎]''')
                return
            elif cost <= round(inventory[0]):
                markup = types.ReplyKeyboardMarkup(one_time_keyboard=True, resize_keyboard=2)
                markup.add('cancel❌')
                msg = bot.send_message(user_id, f'لطفا رنک خود را وارد کنید', reply_markup=markup)
                bot.register_next_step_handler(msg, setrank, lupin)
                return
        except:
            bot.send_message(user_id, 'شما توانايي خريد رنک در اين گروه را نداريد')
            return

    # elif text == '🐾𖡼ᏝᏬᎮᎥᏁ ꪡᴏʟғ⸸🐾':
    #     inventory = diamond_db.load_diamond(lupin_wolf, user_id)
    #     cost = 10000
    #
    #     try:
    #         if cost > round(inventory[0]):
    #             bot.send_message(user_id, f'''موجودی شما کافی نیست...✖️
    #         موجودی شما [{inventory[0]}💎]''')
    #             return
    #         elif cost <= round(inventory[0]):
    #             markup = types.ReplyKeyboardMarkup(one_time_keyboard=True, resize_keyboard=2)
    #             markup.add('cancel❌')
    #             msg = bot.send_message(user_id, f'لطفا رنک خود را وارد کنید')
    #             bot.register_next_step_handler(msg, setrank, lupin_wolf)
    #             return
    #     except:
    #         bot.send_message(user_id, 'شما توانايي خريد رنک در اين گروه را نداريد')
    #         return

    else:
        bot.send_message(user_id, 'لطفا از دکــــمــــه های موجود استفاده کنید...🕹')
        start2(user_id)


def setrank(message, chat_id):
    user_id = message.chat.id
    if message.text == 'cancel❌':
        bot.send_message(user_id, 'کنسل شد')
        return
    elif message.text == '/start':
        start2(chat_id)
        return
    elif not message.text:
        msg = bot.send_message(user_id, 'لطفا رنک خود را بصورت تکست وارد کنید')
        bot.register_next_step_handler(msg, setrank, chat_id)
        return
    rank = message.text
    diamond_db.save_rank(chat_id, user_id, rank)
    bot.send_message(user_id, f'رنک [{rank}] با موفقیت برای شما خریداری شد...🛍🕷')
    diamond_db.add_diamond(lupin, user_id, -1 * 10000)


def emojishop(message, emoji):
    text = message.text
    user_id = message.chat.id

    if text == 'cancel❌':
        bot.send_message(user_id, 'کنسل شد')
        return
    elif not text in emoji:
        bot.send_message(user_id, 'لطفا از دکــــمــــه های موجود استفاده کنید...🕹')
        start2(user_id)
    else:
        markup = types.ReplyKeyboardMarkup(one_time_keyboard=True, resize_keyboard=2)
        markup.add('🐾𖡼ᏝᏬᎮᎥᏁ ꪡᴏʟғ⸸🐾')
        markup.add('cancel❌')
        msg = bot.send_message(user_id,
                               f'''هزینه این ایــــمــــوجــــی [ {diamond_db.load_emojicost(text)}💎 ] می‌باشد...
این ایــــمــــوجــــی را برای کدام گپ میخواهید؟🛎''', reply_markup=markup)
        bot.register_next_step_handler(msg, checkwallet, text)


def checkwallet(message, emoji):
    user_id = message.chat.id
    text = message.text

    if text == 'cancel❌':
        bot.send_message(user_id, 'کنسل شد')
        return

    elif text == '🐾𖡼ᏝᏬᎮᎥᏁ ꪡᴏʟғ⸸🐾':
        inventory = diamond_db.load_diamond(lupin, user_id)
        cost = diamond_db.load_emojicost(emoji)

        try:
            if cost[0] > round(inventory[0]):
                bot.send_message(user_id, f'''موجودی شما کافی نیست...✖️
            موجودی شما [{inventory[0]}💎]''')
                return
            elif cost[0] <= round(inventory[0]):
                diamond_db.save_emoji(lupin, user_id, emoji)
                diamond_db.add_diamond(lupin, user_id, -1 * cost[0])
                bot.send_message(user_id, f'ایموجی [{emoji}] با موفقیت برای شما خریداری شد...🛍🕷')
        except:
            bot.send_message(user_id, 'شما توانايي خريد اموجي در اين گروه را نداريد')
            return

    # elif text == '🐾𖡼ᏝᏬᎮᎥᏁ ꪡᴏʟғ⸸🐾':
    #     inventory = diamond_db.load_diamond(lupin_wolf, user_id)
    #     cost = diamond_db.load_emojicost(emoji)
    #
    #     try:
    #         if cost[0] > round(inventory[0]):
    #             bot.send_message(user_id, f'''موجودی شما کافی نیست...✖️
    #         موجودی شما [{inventory[0]}💎]''')
    #             return
    #         elif cost[0] <= round(inventory[0]):
    #             diamond_db.save_emoji(lupin_wolf, user_id, emoji)
    #             diamond_db.add_diamond(lupin_wolf, user_id, -1 * cost[0])
    #             bot.send_message(user_id, f'ایموجی [{emoji}] با موفقیت برای شما خریداری شد...🛍🕷')
    #     except:
    #         bot.send_message(user_id, 'شما توانايي خريد اموجي در اين گروه را نداريد')
    #         return

    else:
        bot.send_message(user_id, 'لطفا از دکــــمــــه های موجود استفاده کنید...🕹')
        start2(user_id)

        #         start2(chat_id)
        #
        #
        # def start2(chat_id):
        #     markup = types.ReplyKeyboardMarkup(one_time_keyboard=True, resize_keyboard=2)
        #     markup.add('انتقال الماس💎')
        #     msg = bot.send_message(chat_id,'💎لطفا انتخاب کنید💎', reply_markup=markup)
        #     bot.register_next_step_handler(msg, tranfer)
        #
        #
        # def tranfer(message):
        #     text = message.text
        #     chat_id = message.chat.id
        #     if text == 'انتقال الماس💎':
        #         if not diamond_db.check_register(chat_id):
        #             bot.send_message(chat_id=chat_id, reply_to_message_id=message.message_id,
        #                              text='''✦|اول باید در ربات ثبت نام کنید✖️''',
        #                              reply_markup=build_markup1(chat_id))
        #             return
        #         markup = types.ReplyKeyboardMarkup(one_time_keyboard=True, resize_keyboard=2)
        #         markup.add('cancel✖️')
        #         msg = bot.send_message(chat_id,'لطفا ایدی عددی شخص مورد نظر را وارد کنید',reply_markup=markup)
        #         bot.register_next_step_handler(msg, sectransfer)
        #     elif text == '/help':
        #         bot.send_message(chat_id, helpme)
        #         start2(chat_id)
        #     else:
        #         start2(chat_id)
        #
        #
        # def sectransfer(message):
        #     text = message.text
        #     chat_id = message.chat.id
        #     if text == 'cancel✖️':
        #         bot.send_message(chat_id,'کنسل شد')
        #         return
        #     elif text == '/help':
        #         bot.send_message(chat_id, helpme)
        #         return
        #     else:
        #         try:
        #             text = int(text)
        #             if not diamond_db.check_register(text):
        #                 bot.send_message(chat_id, 'این شخص ثبت نام نکرده است')
        #                 start2(chat_id)
        #             else:
        #                 markup = types.ReplyKeyboardMarkup(one_time_keyboard=True, resize_keyboard=2)
        #                 markup.add('cancel✖️')
        #                 msg = bot.send_message(chat_id, 'تعداد الماس مورد نظر را وارد کنید', reply_markup=markup)
        #                 bot.register_next_step_handler(msg, finaltransfer, text)
        #         except:
        #             msg = bot.send_message(chat_id, 'لطفا عدد وارد کنید')
        #             bot.register_next_step_handler(msg, sectransfer)
        #
        #
        # def finaltransfer(message,user_id):
        #     chat_id = message.chat.id
        #     num = message.text
        #     if num == 'cancel✖️':
        #         bot.send_message(chat_id,'کنسل شد')
        #         return
        #     elif num == '/help':
        #         bot.send_message(chat_id, helpme)
        #         return
        #     else:
        #         try:
        #             num = int(num)
        #             if num <= 0:
        #                 msg1 = bot.send_message(chat_id, 'لطفا عدد را درست وارد کنید')
        #                 bot.register_next_step_handler(msg1, finaltransfer, user_id)
        #                 return
        #             inventory = diamond_db.load_diamond(chat_id)
        #             if num > round(inventory[0]):
        #                 msg = '✦| تعداد  المـ💎ـاس های شما کافی نیست ✖️'
        #                 dia = diamond_db.load_diamond(chat_id)
        #                 try:
        #                     msg += f'''\nموجودي شما در حال حاضر : {dia[0]} 💎'''
        #                 except:
        #                     msg += f'''\nموجودي شما در حال حاضر : {0} 💎'''
        #                 bot.send_message(chat_id, msg)
        #                 msg2 = bot.send_message(chat_id, '✦|یک عدد وارد کنید✔️')
        #                 bot.register_next_step_handler(msg2, finaltransfer, user_id)
        #                 return
        #             diamond_db.add_diamond(chat_id, -1 * num)
        #             diamond_db.add_diamond(user_id, num)
        #             bot.send_message(chat_id, 'done')
        #             bot.send_message(user_id,
        #                              f'✦|کاربر [{message.from_user.first_name}](tg://user?id={chat_id}) , به شما {num} المـ💎ـاس هدیه داد🎁',
        #                              parse_mode='markdown')
        #             start2(chat_id)
        #         except:
        #             msg = bot.send_message(chat_id, 'لطفا عدد وارد کنید')
        #             bot.register_next_step_handler(msg, finaltransfer, user_id)


@bot.message_handler(func=Filters.group, commands=['help'])
def gp_help(message):
    if check_group(message):
        return
    user_id = message.from_user.id
    try:
        bot.send_message(user_id, helpme)
        bot.reply_to(message, '✦|یک پیام در pv  برای شما ارسال شد ✔️')
    except:
        try:
            bot.reply_to(message, '✦| ابتدا ربات را استارت کنید و مجدد این دستور را بزنید ✖️')
        except:
            pass


@retry(wait=wait_fixed(2), stop=stop_after_attempt(10))
def poll():
    if __name__ == "__main__":
        try:
            # bot.enable_save_next_step_handlers(delay=2)
            # bot.load_next_step_handlers()
            bot.polling(none_stop=True, timeout=234)
        except Exception as e:
            bot.send_message(chat_id=638994540, text=e)
            raise e


poll()

while True:
    pass
