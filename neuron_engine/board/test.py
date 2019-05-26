''' this file is just like scratchpad, not really needed '''

import re

patterns = () # (pattern, (pat, repl))

replacements = ()

text = ''

startfrom = 0

while startfrom < len(text):

    finded = []

    for pattern, replacement in patterns:
        finded.append((re.search(pattern, text).span(), replacement))

    start_indexes = (x[0][0] for x in finded)

    first = finded[start_indexes.index(min(start_indexes))]

    #first = finded[index(min(map(lambda x: x[0][0], finded_indexes)))]
    # [x[0][0] for x in finded] as an alternative

    startfrom = first[0][1]



replaced = [text]

for span in spans:
    
    finded = []
    
    for pattern, replacement in patterns:
        finded.append((re.search(pattern, text).span(), replacement))

    start_indexes = (x[0][0] for x in finded)

    first = finded[start_indexes.index(min(start_indexes))]
    
    replaced += text[first[0]:first[1]]
    
    span[0] = first[1]



op_tags = ('`', '%%')
cl_tags = ('`', '%%')
op_repl = ('<span class="mono">', '<span class="spoiler">')
cl_repl = ('</span>', '</span>')
text = 'текст %%текст%% `текст`'
spans = [text]
new_text = ''

for op, cl, op_r, cl_r in zip(op_tags, cl_tags, op_repl, cl_repl):
    for span in spans:
        regex_op = re.compile(op)
        finded_op = regex_op.search(text)
        while finded_op:
            if finded_op.start() > 0:
                new_text += text[0:finded_op.start()]
            regex_cl = re.compile(cl)
            finded_cl = regex_cl.search(text[finded_op.end():])
            spans = []
            #finded_op = regex.search(text)


for op, cl, op_r, cl_r in zip(op_tags, cl_tags, op_repl, cl_repl):
    end = len(text) - 1
    finded_op = re.search(op, text)
    print(finded_op)
    if finded_op:
        finded_cl = re.search(cl, text[finded_op.end():])
        print(finded_cl)
    spans = [text[0:finded_op.start()], text[finded_op.start():finded_op.end()], text[finded_op.end():finded_op.end()+finded_cl.start()], text[finded_op.end()+finded_cl.start():finded_op.end()+finded_cl.end()], text[finded_op.end()+finded_cl.end():],]
    
    #print(finded_op.start())
    #new_text += text[0:finded_op.start()]
    #spans.append(text[0:finded_op.start()])
    #text = text[finded_cl.end():]
text = '%%текст%% ``текст`` %%``текст``%% ``%%текст%%`` %%``текст%%`` ``%%текст``%% %%'

wakaba_mark = (r'(&gt;&gt;&gt;)([\s\S]*?)(&lt;&lt;&lt;)', r'(?<!(&gt;))(&gt;(?!(&gt;))[^\r\n$]+)', r'(%%)([\s\S]*?)(%%)', r'(\*\*)([\s\S]*?)(\*\*)', r'(__)([\s\S]*?)(__)', r'(\^\^)([\s\S]*?)(\^\^)', r'(``)([\s\S]*?)(``)', r'(https?:\/\/(www\.)?[-\w\d@:%._\+~#=]{2,256}\.[\w]{2,6}\b([-\w\d@:%_\+.~#?&//=]*))',)

finded = []

for op, cl, op_r, cl_r in zip(op_tags, cl_tags, op_repl, cl_repl):
    finded_op = re.search(op, text)
    if finded_op:
        finded_cl = re.search(cl, text[finded_op.end():])
    finded.append((finded_op.span(), (finded_op.end()+finded_cl.start(), finded_op.end()+finded_cl.end())))




''' actual '''

import re
text = '%%текст%% текст текст %%**текст%%** текст **%%текст**%% ``текст`` %%``**текст**``%% ``%%текст%%`` %%``текст%%`` ``%%текст``%% %%'
wakaba_mark = (
r'(&gt;&gt;&gt;)([\s\S]*?)(&lt;&lt;&lt;)',
r'(?<!(&gt;))(&gt;(?!(&gt;))[^\r\n$]+)',
r'(%%)([\s\S]*?)(%%)',
r'(\*\*)([\s\S]*?)(\*\*)',
r'(__)([\s\S]*?)(__)',
r'(\^\^)([\s\S]*?)(\^\^)',
r'(``)([\s\S]*?)(``)',
r'(https?:\/\/(www\.)?[-\w\d@:%._\+~#=]{2,256}\.[\w]{2,6}\b([-\w\d@:%_\+.~#?&//=]*))',
)
finded = []
for regexp in wakaba_mark:
    r = re.compile(regexp)
    iterator = r.finditer(text)
    for match in iterator:
        finded.append(match.span())

finded.sort()
print(finded)
previous = (0, 0)
unwanted = set()
for n, span in enumerate(finded):
    print(str(previous) + ', ' + str(span))
    #(20, 37), (22, 35)
    #if (previous[1] > span[1] and previous[0] > span[0]) or (span[0] < previous[1] and span[1] > previous[1]):
    if previous[0] < span[0] and span[1] < previous[1] or previous[0] <= span[0] and previous[1] <= span[0]:
        previous = span
    else:
        print(str(span) + 'marked for deletion')
        unwanted.add(span)
    #previous = span

finded = [e for e in finded if e not in unwanted]
print(finded)

for span in finded:
    
