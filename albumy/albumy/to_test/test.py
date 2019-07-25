from itsdangerous import Serializer

a = Serializer('mima')
token_a = a.dumps('test')
print(token_a)


b = Serializer('mima')
c = b.loads(token_a)
print(c)


roles_permissions_map = {
            'Locked': ['FOLLOW', 'COLLECT'],
            'User': ['FOLLOW', 'COLLECT','COMMENT','UPLOAD'],
            'Moderator':['FOLLOW','COLLECT','COMMENT','UPLOAD','MODERATE'],
            'Administrator':['FOLLOW','COLLECT','COMMENT','UPLOAD','MODERATE','ADMINISTER']
        }

for key, value in roles_permissions_map.items():
    print(key,value)