import os

import PIL
from PIL import Image
from itsdangerous import Serializer

def A():
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

def B():
    a = 'abc.img'
    ext = os.path.splitext(a)
    print(ext)

image = 'Bing_0001.jpeg'
def resize_image(image, filename, base_width):
    filename, ext = os.path.splitext(filename)
    img = Image.open(image)
    if img.size[0] <= base_width:
        return filename + ext
    print(img.size)
    w_percent = (base_width / float(img.size[0]))
    print(w_percent)
    h_size = int((float(img.size[1]) * float(w_percent)))
    print(h_size)
    img = img.resize((base_width, h_size), PIL.Image.ANTIALIAS)

    filename += '_test' + ext
    img.save(filename, optimize=True, quality=85)
    return filename

if __name__ == '__main__':
    resize_image(image,image,400)