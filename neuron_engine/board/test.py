''' this file is just like scratchpad, not really needed '''


def f(e):
    for regexp in wakaba_mark:
        r = re.compile(regexp[0])
        e = r.sub(regexp[1], e)
    return e

result = map(f, new_text)
print(result)


''' actual '''

import re
text = '%%текст%% текст текст %%**текст%%** текст **%%текст**%% ``текст`` %%``**текст**``%% ``%%текст%%`` %%``текст%%``>текст ``%%текст``%% %%'
wakaba_mark = (
    (r'(&gt;&gt;&gt;)([\s\S]*?)(&lt;&lt;&lt;)', r'<div class="citation">&gt; \2</div>'),
    (r'(?<!(&gt;))(&gt;(?!(&gt;))[^\r\n$]+)', r'<span class="citation">\2</span>'),
    (r'(%%)([\s\S]*?)(%%)', r'<span class="spoiler">\2</span>'),
    (r'(\*\*)([\s\S]*?)(\*\*)', r'<strong>\2</strong>'),
    (r'(__)([\s\S]*?)(__)', r'<em>\2</em>'),
    (r'(\^\^)([\s\S]*?)(\^\^)', r'<del>\2</del>'),
    (r'(``)([\s\S]*?)(``)', r'<span class="mono">\2</span>'),
    (r'(https?:\/\/(www\.)?[-\w\d@:%._\+~#=]{2,256}\.[\w]{2,6}\b([-\w\d@:%_\+.~#?&//=]*))', r'<a href="\1">\1</a>'),
)
finded = []
for regexp in wakaba_mark:
    r = re.compile(regexp[0])
    iterator = r.finditer(text)
    for match in iterator:
        finded.append((match.span(1), match.span(3)))

finded.sort()
for span in finded:

previous = ((0, 0), (0, 0))
unwanted = []
for n, span in enumerate(finded):
    if previous[0][0] < span[0][0] and span[1][0] < previous[1][0] or previous[0][0] <= span[0][0] and previous[1][0] <= span[0][0]:
        previous = span
    else:
        unwanted.append(span)

finded = [e for e in finded if e not in unwanted]
for span in finded:
    print(text[span[0][0]:span[1][1]], span[0][0], span[1][1])

new_text = []
prev = 0
unwanted.sort()
for span in unwanted:
    new_text.append(text[prev:span[0][0]])
    new_text.append(text[span[0][1]:span[1][0]])
    prev = span[1][1]

result = ''
for e in new_text:
    result += e

for regexp in wakaba_mark:
    r = re.compile(regexp[0])
    result = r.sub(regexp[1], result)

print(text)
print(result)
