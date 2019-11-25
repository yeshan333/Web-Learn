# Redis 是一个单进程、单线程的数据库
import redis

# 方法名基本和 redis 命令一致
client = redis.Redis()

#--------------------------------------------------------------------
# Redis 字符串

# 列出所有 keys
print(client.keys())

# 有问题
""" for key in client.keys():
    print(key.decode('gbk'))  # 解码，正常显示中文 """

# 创建字符串
client.set('test_key', 'test_value')
client.set('test_key', 'test_value', nx=True)  # 不覆盖原有数据

# 获取字符串
print(client.get('test_key'))  # bytes类型

client.append('key', 'nihao')  # 把新字符添加到已有字符的末尾

# client.incr('number', 1)  # 值加 1
# client.decr('number', 1)  # 值减 1

#--------------------------------------------------------------------
# Redis 列表

client.lpush('Python_example_list', 'python', 'hello')  # 从列表（Python_example_list）左侧插入数据

client.rpush('Python_example_list', 'python')  # 从列表右侧插入数据

datas = ['1', '2', '3', '4', '5']
client.lpush('Python_example_list', *datas)  # 批量添加数据

client.llen('Python_example_list')  # 获取列表长度

print(client.lrange('Python_example_list', 0, -1))  # 获取一定索引范围内的数据，这里是获取全部的数据

client.lpop('Python_example_list')  # 从左侧弹出数据

# 修改 List 中指定索引的数据
client.lset('Python_example_list', 0, "made")

#--------------------------------------------------------------------
# Redis 无序集合，集合内的元素是唯一的

client.sadd('example_set', '1', '2')  # 向集合（example_set）添加元素

datas = ['3', '4', '5']
client.sadd('example_set', *datas)

print(client.scard('example_set'))  # 查看集合中元素的个数

print(client.smembers('example_set'))  # 获取集合中的所有元素

client.srem('example_set', '1')  # 移除集合中的元素

# 集合运算
test_datas = ['a', 'c', 'd', '1']
client.sadd('example_set_1', *test_datas)

client.sinter('example_set', 'example_set_1')  # 集合交运算

client.sunion('example_set', 'example_set_1')  # 集合并运算

client.sdiff('example_set', 'example_set_1')  # 集合差运算













