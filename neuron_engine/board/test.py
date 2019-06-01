''' this file is just like scratchpad, not really needed '''


import re
text = '''&gt;wbnfnf
%%текст%% текст текст %%**текст%%** текст **%%текст**%% ``текст`` %%``**текст**``%% ``%%текст%%`` %%``текст%%``>текст ``%%текст``%% %% ntrcn mtrcm
&gt;цитата
а если так
123
456'''
import re
#text = 'никакой разметки'
#text = '&gt;%%цитата%%'
markdown_tags = (
    (r'(&gt;&gt;&gt;)([\s\S]*?)(&lt;&lt;&lt;)', r'<div class="citation">&gt; \2</div>'),
    (r'(%%)([\s\S]*?)(%%)', r'<span class="spoiler">\2</span>'),
    (r'(\*)([\s\S]*?)(\*)', r'<strong>\2</strong>'),
    (r'(_)([\s\S]*?)(_)', r'<em>\2</em>'),
    (r'(\^)([\s\S]*?)(\^)', r'<del>\2</del>'),
    (r'(`)([\s\S]*?)(`)', r'<span class="mono">\2</span>'),
)
markdown_other = (
    (r'(?<!(&gt;))(&gt;(?!(&gt;))[^\r\n$]+)', r'<span class="citation">\2</span>'),
    (r'(https?:\/\/(www\.)?[-\w\d@:%._\+~#=]{2,256}\.[\w]{2,6}\b([-\w\d@:%_\+.~#?&//=]*))', r'<a href="\1">\1</a>'),    
)
finded = []
for regexp in markdown_tags:
    r = re.compile(regexp[0])
    iterator = r.finditer(text)
    for match in iterator:
        finded.append((match.span(1), match.span(3)))

finded.sort()

previous = ((0, 0), (0, 0))
unwanted = []
for span in finded:
    if previous[0][0] < span[0][0] and span[1][0] < previous[1][0] or previous[0][0] <= span[0][0] and previous[1][0] <= span[0][0]:
        previous = span
    else:
        unwanted.append(span)

new_text = ''
prev = 0
unwanted.sort()
print(unwanted)
for span in unwanted:
    new_text += text[prev:span[0][0]]
    new_text += text[span[0][1]:span[1][0]]
    prev = span[1][1]

new_text += text[prev:len(text)]
for regexp in (markdown_tags+markdown_other):
    r = re.compile(regexp[0])
    new_text = r.sub(regexp[1], new_text)

print(text)
print(new_text)






'''actual'''



import re
text = '''&gt;wbnfnf
%%текст%% текст текст %%*текст%%* текст *%%текст*%% `текст` %%`*текст*`%% `%%текст%%` %%`текст%%`>текст `%%текст`%% %% ntrcn mtrcm
&gt;цитата
https://iichan.hk
а если так
123
456'''
markdown_tags = (
    (r'(&gt;&gt;&gt;)([\s\S]*?)(&lt;&lt;&lt;)', r'<div class="citation">&gt; \2</div>'),
    (r'(%%)([\s\S]*?)(%%)', r'<span class="spoiler">\2</span>'),
    (r'(\*)([\s\S]*?)(\*)', r'<strong>\2</strong>'),
    (r'(_)([\s\S]*?)(_)', r'<em>\2</em>'),
    (r'(\^)([\s\S]*?)(\^)', r'<del>\2</del>'),
    (r'(`)([\s\S]*?)(`)', r'<span class="mono">\2</span>'),
)
markdown_other = (
    (r'(?<!(&gt;))(&gt;(?!(&gt;))[^\r\n$]+)', r'<span class="citation">\2</span>'),
    (r'(https?:\/\/(www\.)?[-\w\d@:%._\+~#=]{2,256}\.[\w]{2,6}\b([-\w\d@:%_\+.~#?&//=]*))', r'<a href="\1">\1</a>'),    
)

def find_all(tags, text):
    finded = []
    for regexp in tags:
        r = re.compile(regexp[0])
        iterator = r.finditer(text)
        for match in iterator:
            finded.append((match.span(1), match.span(3)))
    finded.sort()
    return finded

def find_unwanted(finded):
    previous = ((0, 0), (0, 0))
    unwanted = []
    for span in finded:
        if previous[0][0] < span[0][0] and span[1][0] < previous[1][0] or previous[0][0] <= span[0][0] and previous[1][0] <= span[0][0]:
            previous = span
        else:
            unwanted.append(span)
    unwanted.sort()
    return unwanted

def assemble_text(unwanted, text):
    new_text = ''
    previous = 0
    for span in unwanted:
        new_text += text[previous:span[0][0]]
        new_text += text[span[0][1]:span[1][0]]
        previous = span[1][1]
    new_text += text[previous:len(text)]
    return new_text

def markup_to_html(tags, text):
    for regexp in tags:
        r = re.compile(regexp[0])
        text = r.sub(regexp[1], text)
    return text

def markup_text(board, tags, other, text):
    text = escape(text)
    reply_regex = re.compile(r'&gt;&gt;([0-9]+)')
    finded_replies = reply_regex.findall(text)
    if finded_replies:
        text, replies_relations = make_reply_sub(finded_replies, board, text, reply_regex)
    else:
        replies_relations = None
    finded = find_all(tags, text)
    unwanted = find_unwanted(finded) if finded else False
    if unwanted:
        text = assemble_text(unwanted, text)
    text = markup_to_html(tags+other, text)
    return text, replies_relations





def markup_text(tags, other, text):
    finded = find_all(tags, text)
    unwanted = find_unwanted(finded) if finded else False
    if unwanted:
        text = assemble_text(unwanted, text)
    return markup_to_html(tags+other, text)

print(text)
text = markup_text(markdown_tags, markdown_other, text)
print(text)
