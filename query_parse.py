from os import remove, system

f = open("query.txt")
q = []
for s in f.readlines():
    q.append(s.strip())
q = ' ' + ' '.join(q) + ' '
f.close()

n = q.find(" name ")
w = q.find(" within ")
i = q.find(" if ")
p = q.find(" print ")
if n == -1 or p == -1:
    exit()

if n != -1:
    nxt = w if w != -1 else i if i != -1 else p
    filename = q[n+6:nxt]
tmp = open("tmp.py", 'w')
print >>tmp,\
      """from tmprenderer import Renderer, __getres
from plasTeX.TeX import TeX
__tex = TeX(file=open("{}"))
__tex.ownerDocument.config['files']['split-level'] = -100
__tex.ownerDocument.config['files']['filename'] = 'test.xml'
__doc = __tex.parse()
__renderer = Renderer()
__renderer.render(__doc)
__output_file = open(\"$$tmp25$$.tmp\", 'w')
print >>__output_file, __getres()
__output_file.close()
""".format(filename)
tmp.close()

tmpr = open("tmprenderer.py", 'w')
print >>tmpr,\
      """import string
from plasTeX.Renderers import Renderer
def __getres():
    try:
        return __res
    except NameError:
        return ""
def appendres(x):
    global __res
    try:
        __res += x
    except NameError:
        __res = x
class Renderer(Renderer):
    def default(self, node):
        s = []
        if len(node.nodeName) == 1 and node.nodeName not in string.letters:
            return self.textDefault(node.nodeName)
        if node.hasAttributes():
            for key, value in node.attributes.items():
                if key == 'self':
                    continue
"""

if w != -1:
    nxt = i if i > -1 else p
    csci = q[w+7:nxt].find('>')
    if csci == -1:
        wslicel = q[w+7:nxt].find('[')
        if wslicel == -1:
            print >>tmpr, """        if node.nodeName == '{}':
            appendres(node.source)
""".format(q[w+8:nxt])
        else:
            wslicer = q[wslicel:nxt].find(']')
            slicen = q[w+8+wslicel:wslicel+wslicer]
            print >>tmpr, """        target_{0} = {1}
        def get_{0}():
            try:
                return {0}
            except NameError:
                return 0
        def inc_{0}():
            global {0}
            try:
                {0} += 1
            except NameError:
                {0} = 1
        if node.nodeName == '{0}':
            if get_{0}() == target_{0}:
                appendres(node.source)
            inc_{0}()""".format(q[w+8:w+7+wslicel], slicen)
    else:
        keys = [i.strip() for i in q[w+7:nxt].split('>')]
        print >>tmpr, "        keys = []"
        for key in keys:
            print >>tmpr, "        keys.append('{}')".format(key)
        print >>tmpr, """        def search_keys(node, key):
            slicel = keys[key].find('[')
            if slicel == -1:
                for n in node.childNodes:
                    if n.name == keys[key]:
                        if key == len(keys) - 1:
                            appendres(n.source)
                        else:
                            search_keys(n, key + 1)
                    else:
                        search_keys(n, key)
            else:
                slicer = keys[key][slicel:].find(']')
                slicen = int(keys[key][slicel+1:slicel+slicer])
                try:
                    target = filter(lambda x : x.nodeName ==
                                    keys[key][:slicel], node.childNodes)[slicen]
                    if key == len(keys) - 1:
                        appendres(target.source)
                    else:
                        search_keys(target, key + 1)
                except IndexError:
                    for n in node.childNodes:
                        search_keys(n, key)
"""
        wslicel = keys[0].find('[')
        if wslicel == -1:
            print >>tmpr, """        if node.nodeName == '{}':
            search_keys(node, 1)
""".format(keys[0])
        else:
            wslicer = keys[0][wslicel:].find(']')
            slicen = keys[0][wslicel+1:wslicel+wslicer]
            print >>tmpr, """        target_{0} = {1}
        def get_{0}():
            try:
                return {0}
            except NameError:
                return 0
        def inc_{0}():
            global {0}
            try:
                {0} += 1
            except NameError:
                {0} = 1
        if node.nodeName == '{0}':
            if get_{0}() == target_{0}:
                search_keys(node, 1)
            inc_{0}()""".format(keys[0][:wslicel], slicen)

print >>tmpr, """        s.append(unicode(node))
        return u'\\n'.join(s)
    def textDefault(self, node):
        return node.replace('&','&amp;').replace('<','&lt;').replace('>','&gt;')        
"""
tmpr.close()

system("py tmp.py")
#remove("tmp.py")
#remove("test.xml")
#remove("myrenderer.py")
#remove("myrenderer.pyc")
g = open("$$tmp25$$.tmp")
for j in g.readlines():
    print j.strip()
g.close()
remove("$$tmp25$$.tmp")
