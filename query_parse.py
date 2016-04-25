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

tmpr = open("tmprenderer.py", 'w')
if n != -1:
    nxt = w if w != -1 else i if i != -1 else p
    filename = q[n+6:nxt]
print >>tmpr,\
      """import string
from plasTeX.Renderers import Renderer
class Renderer(Renderer):
    def default(self, node):
        s = []
        if len(node.nodeName) == 1 and node.nodeName not in string.letters:
            return self.textDefault(node.nodeName)
        if node.hasAttributes():
            for key, value in node.attributes.items():
                if key == 'self':
                    continue
        s.append(unicode(node))
        return u'\\n'.join(s)
    def textDefault(self, node):
        return node.replace('&','&amp;').replace('<','&lt;').replace('>','&gt;')        
"""
tmpr.close()
tmp = open("tmp.py", 'w')
print >>tmp,\
      """from tmprenderer import Renderer
from plasTeX.TeX import TeX
__tex = TeX(file=open("{}"))
__tex.ownerDocument.config['files']['split-level'] = -100
__tex.ownerDocument.config['files']['filename'] = 'test.xml'
__doc = __tex.parse()
__renderer = Renderer()
__output_file = open(\"$$tmp25$$.tmp\", 'w')
__res = ""
""".format(filename)
if w != -1:
    nxt = i if i > -1 else p
    wslicel = q[w+7:nxt].find('[')
    if wslicel == -1:
        print >>tmp, """def handle_{0}(node):
    global __res
    __res += node.source.strip()
    return u'\\n'.join(unicode(node))
__renderer['{0}'] = handle_{0}
""".format(q[w+8:nxt])
    else:
        wslicer = q[wslicel:nxt].find(']')
        slicen = q[w+8+wslicel:wslicel+wslicer]
        print >>tmp, """__cnt_{0} = {1}
__cur_{0} = 0
def handle_{0}(node):
    global __res, __cnt_{0}, __cur_{0}
    if __cur_{0} == __cnt_{0}:
        __res += node.source.strip()
    __cur_{0} += 1
    return u'\\n'.join(unicode(node))
__renderer['{0}'] = handle_{0}
""".format(q[w+8:w+7+wslicel], slicen)
    #print >>tmp, q[w+1:nxt] + ':'
##if i != -1:
##    res = "" if f == -1 else "  "
##    res += q[i+1:p] + ':'
##    print >>tmp, res
##if w != -1:
##    res = "    " if i > -1 else "  "
##else:
##    res = "  " if i > -1 else ""
##res += q[p+1:p+7] + ">>__output_file, " + q[p+7:]
##print >>tmp, res
print >>tmp, """__renderer.render(__doc)
print >>__output_file, __res
__output_file.close()
"""
tmp.close()

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
