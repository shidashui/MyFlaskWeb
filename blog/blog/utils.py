import re
from unidecode import unidecode

_punct_re = re.compile(r'[\t !"#$%&\'()*\-/<=>?@\[\\\]^_`{|},.]+')

def slugify(text, delim=u'-'):
    result = []
    for word in _punct_re.split(text.lower()):
        result.extend(unidecode(word).lower().split())
    print(unidecode(delim.join(result)))
    return unidecode(delim.join(result))

slugify(u'My Neighbor Totoro')
slugify(u'邻家的豆豆龙')
slugify(u'となりのトトロ')