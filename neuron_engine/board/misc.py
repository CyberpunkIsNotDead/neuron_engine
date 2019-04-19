from ..models import OriginalPost, Post, Upload

''' getting replies '''

def assemble_replies(replies_to_post, board, post):
    replies_urls = []
    for r in replies_to_post:
        if r:
            if r.child_thread:
                link = '<a href="/%s/thread/%s/">&gt;&gt;%s</a>' % (
                    board.url,
                    r.child_thread.counter,
                    r.child_thread.counter,
                    )
                replies_urls.append(link)
            elif r.child_post:
                link = '<a href="/%s/thread/%s/#%s">&gt;&gt;%s</a>' % (
                    board.url,
                    r.child_post.thread.counter,
                    r.child_post.counter,
                    r.child_post.counter,
                    )
                replies_urls.append(link)
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

''' getting file info '''

def get_file_info(rows):

    short_filenames = []
    full_filenames = []
    filesize = []
    length = 0

    for r in rows:
        n = str((r.upload.name.split('/')[-1:])[0])
        full_filenames.append(n)
        if len(n) > 20:
            n = n[:8] + '...' + n[-8:]
            short_filenames.append(n)
        else:
            short_filenames.append(n)
        filesize.append(r.upload.size)
        length += 1

    return length, zip(rows, short_filenames, full_filenames, filesize)
