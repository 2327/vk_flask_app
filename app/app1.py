import vk

session = vk.Session(access_token='c9c3cb759a75aa19c67be961d2314e50bb721de57049391dbec183822da7d0ec09be96ddc5c69b525e1f1')
api = vk.API(session, v='5.52', lang='ru', timeout=10)

def searchForUser(user_list, ID):
    for user in user_list:
        if type(user) is int:
            continue
        if user['uid'] == ID:
            return user['first_name'] + ' ' + user['last_name'] + '\n'

def checkMessages(message_list):
    IDS = []
    for message in message_list:
        if type(message) is int:
            continue
        if message['read_state'] == 0:
            if 'chat_id' not in message:
                IDS.append(str(message['uid']))

    user_list = api.users.get(user_ids = ','.join(IDS))
    text = ''

    for message in message_list:
        if type(message) is int:
            continue
        if message['read_state'] == 0:
            if 'chat_id' not in message:
                text = text + searchForUser(user_list, message['uid']) + message['body'] + '\n'
            else:
               text = text + 'Сообщение из чата\n' + message['body'] + '\n'
    print(text)
    return text

# api.wall.post(message="hello")
#api.messages.send(users_id=0, messages='hell')
print(api.users.get(user_id='33411499', fields='online, last_seen' ))

'''
https://oauth.vk.com/authorize?client_id=7271238&display=page&redirect_uri=https://oauth.vk.com/blank.html&scope=friends&response_type=token&v=5.52
https://oauth.vk.com/authorize?client_id=7271238&display=page&redirect_uri=https://oauth.vk.com/blank.html&scope=friends,photos,audio,video,docs,notes,pages,status,wall,groups,messages,notifications&response_type=token&v=5.52


https://oauth.vk.com/authorize?client_id=7271238&display=page&redirect_uri=https://oauth.vk.com/blank.html&scope=friends,groups,photos,docs,notes,pages,status,wall,notifications&response_type=token&v=5.52

https://oauth.vk.com/authorize?client_id=7272469&display=page&redirect_uri=https://netmyst.ru/callback&scope=friends,groups,photos,docs,notes,pages,status,wall,notifications&response_type=token&v=5.103
my id: 33411499
'''

