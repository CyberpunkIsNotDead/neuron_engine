from django.utils.html import escape

from ..models import OriginalPost, Post, Replies

import re

''' markup '''

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


def make_reply_sub(finded, board, text, reply_regexp):

    replies_relations = []

    for num in finded:

        int(num)

        replies_relation = Replies.objects.create().id
        replies_relations.append(replies_relation)

        try:
            op = OriginalPost.objects.filter(board=board).get(counter=num)
            url = '/%s/thread/%s/' % (board.url, op.counter)
            sub = '<a href="%s">&gt;&gt;%s</a>' % (url, num)
            #build thread link

            update_par_th = Replies.objects.filter(
                id=replies_relation
                ).update(parent_thread=op)

            text = text.replace('&gt;&gt;%s' % num, sub)

        except OriginalPost.DoesNotExist:

            try:
                post = Post.objects.filter(board=board).get(counter=num)
                url = '/%s/thread/%s/#%s' % (
                    board.url,
                    post.thread.counter,
                    post.counter
                    )
                sub = '<a href="%s">&gt;&gt;%s</a>' % (url, num)
                #build post link

                update_par_p = Replies.objects.filter(
                    id=replies_relation
                    ).update(parent_post=post)

                text = text.replace('&gt;&gt;%s' % num, sub)

            except Post.DoesNotExist:

                sub = '<span class="inactive">>>%s</span>' % num
                #build inactive link

                text = text.replace('&gt;&gt;%s' % num, sub)

    return text, replies_relations


def make_code_sub(finded_code, text):
    
    for code in finded_code:

        sub = '<div style="overflow-x: auto;"><pre><ol class="code">'

        for n, string in enumerate(code.splitlines()):
            print(str(n)+' '+string)
            sub += '<li><span class="code_string">%s</span></li>' % string
        
        sub += '</ol><pre></div>'
        
        text = text.replace('```%s```' % code, sub)
    
    return text
