import json
import redis

client = redis.Redis()

bytes_list = client.lrange('my_list', 0 ,2)

print(bytes_list)

new_list = []

for temp in bytes_list:
    new = json.loads(temp.decode())
    new_list.append(new)

print(new_list) 

# lpush chat_list '{"msg": "我是人工添加的消息", "nick": "yeshan", "post_time":"2019-11-22 16:15:00"}'
# lpush chat_list '{"msg": "what", "nick": "testman", "post_time":"2019-11-22 16:15:00"}'
#---------------------------------------------------------------------------

""" bytes_list = [b'5', b'4', b'3', b'2', b'1', b'hello', b'python', b'python']

new_list = []

for temp in bytes_list:
    new = json.loads(temp.decode())
    new_list.append(new)

print(new_list) """
    