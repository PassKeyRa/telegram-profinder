import asyncio

class Profinder:
    def __init__(self, client, groups):
        self.client = client
        self.dialogs = {}
        self.loop = asyncio.get_event_loop()
        self.groups = groups
        self.loop.run_until_complete(self.__get_dialogs())

    async def __get_dialogs(self):
        async for dialog in self.client.iter_dialogs():
            if dialog.id < 0 and dialog.name in self.groups:
                self.dialogs[dialog.id] = dialog.name

    def __extend_names(self, names):
        pass
    
    def findUser(self, user_names):
        return self.loop.run_until_complete(self.__findUser(user_names))

    async def __findUser(self, user_names):
        matches = {}
        for d in self.dialogs.keys():
            chat = await self.client.get_entity(d)
            for name in user_names:
                async for user in self.client.iter_participants(chat, search=name):
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
        return matches
