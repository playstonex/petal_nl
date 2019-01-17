import re


kEmailRg = r'\w[-\w.+]*@([A-Za-z0-9][-A-Za-z0-9]+\.)+[A-Za-z]{2,14}'
kDomainRg = r'[a-zA-Z0-9][-a-zA-Z0-9]{0,62}(/.[a-zA-Z0-9][-a-zA-Z0-9]{0,62})+/.?'

kURLRg = r'''^(https?:\/\/)? # match http or https
             ([\da-z\.-]+)            # match domain
             \.([a-z\.]{2,6})         # match domain
             ([\/\w \.-]*)\/?$        # match api or file
             '''
kNumberRg = '^[0-9]*$'

kIPRg = '((?:(?:25[0-5]|2[0-4]\\d|[01]?\\d?\\d)\\.){3}(?:25[0-5]|2[0-4]\\d|[01]?\\d?\\d))'


kHTMLRg = '<[^/>][^>]*>'


class Marcher:
    def __init__(self, rg, label):
        self.exp = re.compile(rg, re.X)
        self.label = label

    def isMatch(self, text):
        return self.exp.match(text)


marchers = [
    Marcher(kEmailRg, 'Email'),
    Marcher(kDomainRg, 'Domain'),
    Marcher(kURLRg, 'URL'),
    Marcher(kHTMLRg, 'HTML'),
    Marcher(kNumberRg, 'Number'),
    Marcher(kIPRg, "IP")
]


def isMarch(text):
    for m in marchers:
        if m.isMatch(text) != None:
            print('%s is match %s' % (text, m.label))
            return True
    return False


# a = 'guolei@me.com'
# b = '13123234'
# c = 'hello'
# d = 'https://www.w3cschool.cn/regexp/m2ez1pqk.html'
# e = 'playstone.org'
# f = '12.3.4.1'
# g = '<img src="/img">'

# ra = isMarch(a)
# print(ra)
# rb = isMarch(b)
# print(rb)
# rc = isMarch(c)
# print(rc)
# rd = isMarch(d)
# print(rd)
# rg = isMarch(e)
# print(rg)
# rg = isMarch(f)
# print(rg)
# rg = isMarch(g)
# print(rg)
