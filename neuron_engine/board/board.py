from django.utils.safestring import *

from ..models import Board, OriginalPost, Upload

from .misc import *

''' assembling board '''


def assemble_board_page(request, board, form):

    boards = Board.objects.all()

    current_page = int(request.GET.get('page')) if request.GET.get('page') else 1
    n = 10
    ops_count = OriginalPost.objects.filter(board=board.id).count()
    pages_count = int(ops_count / n) + 1 if ops_count % n > 0 else int(ops_count / n)
    pagination = make_pagination(current_page, pages_count)

    limit = n * current_page
    offset = limit - n
    ops = OriginalPost.objects.filter(
        board=board.id
        ).order_by('-upd_date')[offset:limit]

    threads = assemble_threads(ops)

    context = {
        'threads': threads,
        'pagination': pagination,
        'board': board,
        'boards': boards,
        'form': form
    }

    return context


def assemble_threads(ops):

    ops_with_files = []
    omitted_counters = []
    replies_sets = []
    replies_to_op_sets = []

    for op in ops:
        op.text = mark_safe(op.text)

        replies_to_op = assemble_replies(
            op.replies_to_thread.all().order_by('id'),
            op.board,
            op
            )
        replies_to_op_sets.append(replies_to_op)

        op_files = Upload.objects.filter(reply=None, thread=op.id)
        op_with_files = {}
        op_with_files[op] = op_files
        ops_with_files.append(op_with_files)
        last_replies = op.post_set.all().order_by('-id')[:5][::-1]

        c = op.post_set.all().count()
        omitted_replies = c - 5 if c >= 5 else 0
        omitted_counters.append(omitted_replies)

        inthread_counter = list(range(omitted_replies+1, c+1))

        replies_with_files, replies_to_reply_sets = get_files(last_replies)

        replies = zip(inthread_counter, replies_with_files, replies_to_reply_sets)
        #replies[inthread_counter] = replies_with_files
        replies_sets.append(replies)

    threads = zip(
        ops_with_files,
        omitted_counters,
        replies_sets,
        replies_to_op_sets
        )

    return threads


def make_pagination(current_page, pages_count):
    pagination = []
    for page in range(1, pages_count+1):
        if page == current_page:
            string = '<a class="active" href="?page=%s">[%s]</a>' % (
                current_page,
                current_page
                )
        else:
            string = '<a href="?page=%s">[%s]</a>' % (
                page,
                page
                )
        pagination.append(string)
    return pagination


def get_files(last_replies):

    replies_with_files = []
    replies_to_reply_sets = []

    for reply in last_replies:
        reply.text = mark_safe(reply.text)

        replies_to_reply = assemble_replies(
            reply.replies_to_post.all().order_by('id'),
            reply.board,
            reply
            )
        replies_to_reply_sets.append(replies_to_reply)

        reply_files = Upload.objects.filter(reply=reply.id)
        reply_with_files = {}
        reply_with_files[reply] = reply_files
        replies_with_files.append(reply_with_files)

    return replies_with_files, replies_to_reply_sets
