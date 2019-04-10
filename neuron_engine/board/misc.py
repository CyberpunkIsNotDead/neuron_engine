from ..models import OriginalPost, Post

''' getting replies '''

def assemble_replies(replies_to_post, board, post):
    replies_urls = []
    for r in replies_to_post:
        if r:
            if r.child_thread:
                link = '>>%s' % r.child_thread.counter
                url = '/%s/thread/%s/' % (
                    board.url,
                    r.child_thread.counter
                    )
                i = (link, url)
                replies_urls.append(i)
            elif r.child_post:
                url = '/%s/thread/%s/#%s' % (
                    board.url,
                    r.child_post.thread.counter,
                    r.child_post.counter
                    )
                link = '>>%s' % r.child_post.counter
                i = (link, url)
                replies_urls.append(i)
    return replies_urls

''' counter '''

def post_counter(board):

    try:
        latest_op = OriginalPost.objects.filter(board=board.id).latest('counter')
        latest_reply = Post.objects.filter(board=board.id).latest('counter')
        latest = latest_op if latest_op.counter > latest_reply.counter else latest_reply
        counter = latest.counter + 1

    except OriginalPost.DoesNotExist:
        counter = 1

    except Post.DoesNotExist:
        counter = latest_op.counter + 1

    return counter
