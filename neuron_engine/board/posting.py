from django.utils import timezone
from django.conf import settings

from django.core.files.storage import default_storage

from ..models import OriginalPost, Post, Upload

from .markup import *
from .misc import *
from .thumbnail import *

import os

''' posting '''


def create_post(board, original_post, form): # form(request.POST, request.FILES)

    if form.is_valid():

        now = timezone.now()
        original_post.upd_date = now

        markup = markup_text(
            board,
            wakaba_mark,
            form.cleaned_data['text']
            )

        formatted_text, replies_relations = markup


        if form.cleaned_data['author']:

            reply = Post(
                board=board,
                thread=original_post,
                author=form.cleaned_data['author'],
                subject=form.cleaned_data['subject'],
                text=formatted_text,
                pub_date=now,
                counter=post_counter(board)
                )

            reply.save()

        else:

            reply = Post(
                board=board,
                thread=original_post,
                subject=form.cleaned_data['subject'],
                text=formatted_text,
                pub_date=now,
                counter=post_counter(board)
                )

            reply.save()


        if replies_relations:

            for replies_relation in replies_relations:
                update_chi_p = Replies.objects.filter(
                    id=replies_relation
                    ).update(child_post=reply)

        original_post.save()

        upload = form.cleaned_data['upload']

        if upload:

            upl_path = os.path.join(board.url, upload.name)
            save_path = os.path.join(settings.MEDIA_ROOT, upl_path)

            path = default_storage.save(save_path, upload)
            path = '/'.join(path.split('/')[-2:]) #todo: os-independent path

            thumb = create_thumbnail(board, upload)

            upl = Upload(
                board=board,
                thread=original_post,
                reply=reply,
                upload=path,
                thumbnail=thumb,
                )

            upl.save()
    else:
        return HttpResponse('form error')



def create_thread(board, form): # form(request.POST, request.FILES)

    if form.is_valid():

        now = timezone.now()

        markup = markup_text(
            board,
            wakaba_mark,
            form.cleaned_data['text']
            )

        formatted_text, replies_relations = markup

        if form.cleaned_data['author']:

            op = OriginalPost(
                board=board,
                author=form.cleaned_data['author'],
                subject=form.cleaned_data['subject'],
                text=formatted_text,
                pub_date=now,
                upd_date=now,
                counter=post_counter(board)
                )

            op.save()

        else:

            op = OriginalPost(
                board=board,
                subject=form.cleaned_data['subject'],
                text=formatted_text,
                pub_date=now,
                upd_date=now,
                counter=post_counter(board)
                )

            op.save()

        if replies_relations:

            for replies_relation in replies_relations:
                update_chi_p = Replies.objects.filter(
                    id=replies_relation
                    ).update(child_thread=op)

        upload = form.cleaned_data['upload']

        if upload:

            upl_path = os.path.join(board.url, upload.name)
            save_path = os.path.join(settings.MEDIA_ROOT, upl_path)

            path = default_storage.save(save_path, upload)
            path = '/'.join(path.split('/')[-2:]) #todo: os-independent path

            thumb = create_thumbnail(board, upload)

            upl = Upload(
                board=board,
                thread=op,
                upload=path,
                thumbnail=thumb,
                )

            upl.save()
    else:
        return HttpResponse('form error')
