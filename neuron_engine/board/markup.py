from django.utils.html import escape

from ..models import OriginalPost, Post, Replies

import re

''' markup '''

wakaba_mark = [
    (r'(&gt;&gt;&gt;)([\s\S]*?)(&lt;&lt;&lt;)', r'<div class="citation">&gt; \2</div>'),
    (r'(?<!(&gt;))(&gt;(?!(&gt;))[^\r\n$]+)', r'<span class="citation">\2</span>'),
    (r'(%%)([\s\S]*?)(%%)', r'<span class="spoiler">\2</span>'),
    (r'(\*\*)([\s\S]*?)(\*\*)', r'<strong>\2</strong>'),
    (r'(__)([\s\S]*?)(__)', r'<em>\2</em>'),
    (r'(\^\^)([\s\S]*?)(\^\^)', r'<del>\2</del>'),
]

def markup_text(board, markup_list, text):

    text = escape(text)

    reply_regex = re.compile(r'&gt;&gt;([0-9]+)')

    finded = reply_regex.findall(text)

    if finded:
        text, replies_relations = make_reply_sub(finded, board, text, reply_regex)
    else:
        replies_relations = None

    for regex, sub in markup_list:
        text = re.sub(regex, sub, text)

    return text, replies_relations


def make_reply_sub(finded, board, text, reply_regexp):

    replies_relations = []

    for num in finded:

        int(num)

        print(num)

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
