'''
TGWerewolf python lib
Written by @Arminshhhh
ALL rights reserved
'''


class WWPlayer:
    def __init__(self, text_line, user_id=None):
        self._text_line = text_line
        self._name_split = self._text_line.split(':')
        self.player_name = ':'.join(self._name_split[:-1])
        self.user_id = user_id
        self.player_id = user_id
        self._player_info = self._name_split[-1]
        self._player_info_split = self._player_info.split('-')
        self.player_state = self._player_info_split[0][:-1]
        self.player_game_result = 'برنده' if 'برنده' in self._player_info_split[1] else 'بازنده'
        self.player_role = self._player_info_split[1].replace('برنده', '').replace('بازنده', '')

    def __repr__(self):
        return f'<{self.player_name if not self.user_id else self.user_id} WWPlayer Object>'

    def is_winner(self):
        return self.player_game_result == 'برنده'

    def is_loser(self):
        return not self.is_winner()

    def is_alive(self):
        return 'زنده' in self.player_state

    def is_dead(self):
        return not self.is_alive()

    def is_lover(self):
        return '❤️' in self.role_emoji()

    def state_emoji(self):
        from emoji import UNICODE_EMOJI
        return '‍'.join(c for c in self.player_state if c in UNICODE_EMOJI)

    def role_emoji(self):
        from emoji import UNICODE_EMOJI
        return '‍'.join(c for c in self.player_role if c in UNICODE_EMOJI)

    def role_without_emoji(self):
        from emoji import UNICODE_EMOJI
        return ''.join(c for c in self.player_role if c not in UNICODE_EMOJI)


class WWGame:

    def __init__(self, game_message):
        try:
            game_text = game_message.text
            players_ids = [ent.user.id for ent in game_message.entities if ent.user]
        except:
            game_text = game_message
            players_ids = None
        self.__game_text = game_text
        self._game_text_split = game_text.split('\n')
        self._game_text_first_line = self._game_text_split[0].split()
        self.all_players_count = int(self._game_text_first_line[5])
        self.alive_players_count = int(self._game_text_first_line[3])
        self.dead_players_count = self.all_players_count - self.alive_players_count
        self._players = self._game_text_split[1:-3]
        if players_ids:
            self.players = [WWPlayer(line, players_ids[i]) for i, line in enumerate(self._players)]
        else:
            self.players = [WWPlayer(line) for line in self._players]

    def __repr__(self):
        return f'<{self.all_players_count} Players Werwolf Game Object>'

    def game_time(self, timestamp=True):
        if timestamp:
            return self._game_text_split[-1][-8:]
        else:
            from datetime import timedelta
            time = self._game_text_split[-1][-8:]
            hours, minutes, seconds = time.split(':')
            return timedelta(hours=int(hours), minutes=int(minutes), seconds=int(seconds))

    def winner_team(self):
        roosta, ferghe, gorgs, ghatel, atish, monaf, bitim = [], [], [], [], [], [], []
        game_roles = {0: roosta, 1: ferghe, 2: gorgs, 3: ghatel, 4: atish, 5: monaf}
        all_winners = []
        for player in self.players:
            role_indexes = {'فرقه': 1, 'قاتل': 3, 'آتش زن': 4, 'گرگ': 2, 'جادوگر': 2, 'منافق': 5, 'دزد': 6, 'همزاد': 6}
            for ww_role in role_indexes:
                if ww_role in player.player_role and 'نما' not in player.player_role:
                    game_roles[role_indexes[ww_role]].append(player.is_winner())
                    break
            else:
                game_roles[0].append(player.is_winner())
            if player.is_winner():
                all_winners.append(True)
        for team in game_roles:
            if all(game_roles[team]) and game_roles[team]:
                if not any([any(game_roles[i]) for i in game_roles if game_roles[i] != game_roles[team]]):
                    return {0: 'روستاییا👱', 1: 'فرقه گراها👤', 2: 'گرگ ها🐺', 3: 'قاتل زنجیره ای🔪', 4: 'آتش زن🔥',
                            5: 'منافق👺'}[team]
        else:
            if len(all_winners) == 2:
                return 'لاورا💞'
        return 'بدون برنده😞'

    def game_winners(self):
        return [player for player in self.players if player.is_winner()]

    def game_winners_count(self):
        return len(self.game_winners())

    def game_losers(self):
        return [player for player in self.players if player.is_loser()]

    def game_losers_count(self):
        return len(self.game_losers())

    def __lt__(self, other):
        return self.all_players_count < other.all_players_count

#
# ### example
# text = '''بازیکن های زنده: 3 / 14
# ᴅᴇʟᴀʀᴀᴍ🦋: 💀 مرده - بچه وحشی 👶 برنده
# M.shahriar: 💀 مرده - کاراگاه 🕵️ برنده
# ღ bahar ツ: 💀 مرده - روستایی 👱 برنده
# #ᏦᎥm: 💀 مرده - پسر گیج 🤕 برنده
# ᴀʏsᴜᴅᴀ ر9: 💀 مرده - خائن 🖕 برنده
# -//Mrym ‣🐰🎈: 💀 مرده - آهنگر ⚒ برنده
# αѕαℓ♡🐾: 💀 مرده - ریش سفید 📚 برنده
# ᴿᴼᴴᴼᴸᴬᴴ🍷: 💀 مرده - گرگینه 🐺 بازنده
# ᴢʜʀᴀ: 💀 مرده - گرگینه 🐺 بازنده
# Qᴀᴢʟ⋆☽⃤: 💀 مرده - مست 🍻 برنده
# ʳᵃˢʰᶦⁿ: 💀 مرده - 🔪قاتل زنجیره ای بازنده
# mąhđį: 🙂 زنده - کلانتر🎯 برنده
# Mrym: 🙂 زنده -  گورکن ☠️ برنده
# 𝑴𝒐𝒉𝒂𝒏𝒅𝒆𝒔🔥𝑺𝒂𝒎𝒂 𝑪𝑹7: 🙂 زنده - شکارچی 💂 برنده
#
#
# مدت زمان بازی: 00:15:10'''
# from datetime import datetime
# import time
#
# print(time.time())
# game = WWGame(text)
# print(time.time())
#
# print(game.all_players_count)
# print(game.winner_team())
# for player in game.players:
#     print(player.player_role)
#     print(player.role_emoji())
#     print(player.user_id)
