import asyncio
import json
import time
from names_translator import Transliterator

class Profinder:
    def __init__(self, client, groups, save_dump=None, dump=None, sleep=None):
        self.client = client
        self.dialogs = {}
        self.users = {}
        self.loop = asyncio.get_event_loop()
        self.groups = groups
        self.sleep = sleep
        self.loop.run_until_complete(self.__get_dialogs())
        if not dump:
            self.loop.run_until_complete(self.__get_users())
        else:
            with open(dump, 'r') as f:
                for u in f:
                    try:
                        uid = int(u.split(':')[0])
                        data = json.loads(':'.join(u.split(':')[1:]))
                        self.users[uid] = data
                    except Exception as e:
                        print(e)
        if save_dump:
            with open(save_dump, 'w') as f:
                for u in self.users:
                    f.write(str(u) + ':' + json.dumps(self.users[u]) + '\n')
            print(f'Saved results to {dump}')

    async def __get_dialogs(self):
        async for dialog in self.client.iter_dialogs():
            if dialog.id < 0 and dialog.name in self.groups:
                self.dialogs[dialog.id] = dialog.name

    async def __get_users(self):
        for d in self.dialogs.keys():
            chat = await self.client.get_entity(d)
            print('Dumping users from chat:', self.dialogs[d])
            async for user in self.client.iter_participants(chat, aggressive=False):
                full_name = ''
                try:
                    full_name += user.first_name
                    full_name += ' '
                except:
                    pass
                try:
                    full_name += user.last_name
                except:
                    pass
                if user.id in self.users:
                    self.users[user.id]['chat_ids'].append(d)
                    self.users[user.id]['chat_names'].append(self.dialogs[d])
                else:
                    link = None
                    if user.username:
                        link = f'https://t.me/{user.username}'
                    else:
                        link = f'[{full_name}](tg://user?id={user.id})'
                    self.users[user.id] = {'name':full_name, 'username':user.username, 'phone':user.phone, 'link':link, 'chat_ids':[d], 'chat_names':[self.dialogs[d]]}
            if self.sleep:
                time.sleep(self.sleep)
        print('Number of users:', len(self.users))


    def __extend_names(self, names):
        pass
    
    def findUser(self, user_names):
        return self.loop.run_until_complete(self.__findUser(user_names))

    async def __findUser(self, user_names):
        matches = {}
        tr = Transliterator()
        for user_id in self.users:
            user = self.users[user_id]
            for name in user_names:
                n = name.split(' ')
                if len(n) < 2:
                    n.append('')
                variants = tr.transliterate(n[0], n[1], '', use_ukrainian_transliteration=False)
                found = False
                for v in variants:
                    v_ = v.split(' ')
                    found = True
                    for v__ in v_:
                        if v__.lower() not in user['name'].lower():
                            found = False
                            break
                    if found:
                        break
                if found:
                    matches[user_id] = user
        return matches

        # Used to search using telegram api search engine
        # Failes on big data
        '''for d in self.dialogs.keys():
            chat = await self.client.get_entity(d)
            for name in user_names:
                async for user in self.client.iter_participants(chat, aggressive=False, limit=2000, search=name):
                    full_name = ''
                    try:
                        full_name += user.first_name
                        full_name += ' '
                    except:
                        pass
                    try:
                        full_name += user.last_name
                    except:
                        pass
                    if user.id in matches:
                        matches[user.id]['chat_ids'].append(d)
                        matches[user.id]['chat_names'].append(self.dialogs[d])
                    else:
                        link = None
                        if user.username:
                            link = f'https://t.me/{user.username}'
                        else:
                            link = f'[{full_name}](tg://user?id={user.id})'
                        matches[user.id] = {'name':full_name, 'username':user.username, 'phone':user.phone, 'link':link, 'chat_ids':[d], 'chat_names':[self.dialogs[d]]}
        return matches'''
