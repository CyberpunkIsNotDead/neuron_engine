from django.utils.safestring import *

from ..models import Board, Upload

from .misc import *

''' assembling thread '''

def assemble_thread(board, form, original_post):

    boards = Board.objects.all()

    replies_to_op = assemble_replies(
        original_post.replies_to_thread.all().order_by('id'),
        board,
        original_post
        )

    op_file_counter, op_files = get_file_info(Upload.objects.filter(reply=None, thread=original_post.id))
    op_with_files = {}
    op_with_files[original_post] = op_files

    replies = original_post.post_set.all().order_by('id')

    post_file_counters = []

    inthread_counter = tuple(range(1, replies.count()+1))

    replies_with_files = []

    replies_to_reply_sets = []

    for reply in replies:

        reply.text = mark_safe(reply.text)

        replies_to_reply = assemble_replies(
            reply.replies_to_post.all().order_by('id'),
            board,
            reply
            )
        replies_to_reply_sets.append(replies_to_reply)

        post_file_counter, reply_files = get_file_info(Upload.objects.filter(reply=reply.id))
        post_file_counters.append(post_file_counter)
        reply_with_files = {}
        reply_with_files[reply] = reply_files
        replies_with_files.append(reply_with_files)

    replies_sets = zip(post_file_counters, replies_with_files, replies_to_reply_sets, inthread_counter)

    context = {
        'file_counter': op_file_counter,
        'replies_sets': replies_sets,
        'original_post': original_post,
        'op_with_files': op_with_files,
        'replies_to_post': replies_to_op,
        'board': board,
        'boards': boards,
        'form': form,
    }

    return context
