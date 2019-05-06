from django.utils import timezone
from django.conf import settings

from ..models import OriginalPost, Post, Upload

from .markup import *
from .misc import *
from .thumbnail import *
from .upload_validation import *

import os

''' posting '''

m = magic.open(magic.MAGIC_MIME)
m.load()

def create_post(board, original_post, form, uploads): # form(request.POST, request.FILES)

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

        if uploads:

            for upload in uploads:

                upl_path = os.path.join(board.url, upload.name)
                save_path = os.path.join(settings.MEDIA_ROOT, upl_path)

                with open(save_path, 'wb+') as destination:
                    for chunk in upload.chunks():
                        destination.write(chunk)

                if validate_uploaded_file(save_path, m):

                    thumb = create_thumbnail(board, upload)

                    upl = Upload(
                        board=board,
                        thread=original_post,
                        reply=reply,
                        upload=upl_path,
                        thumbnail=thumb,
                        )

                    upl.save()
    else:
        print(form.errors)



def create_thread(board, form, uploads): # form(request.POST, request.FILES)

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


        if uploads:

            for upload in uploads:

                upl_path = os.path.join(board.url, upload.name)
                save_path = os.path.join(settings.MEDIA_ROOT, upl_path)

                with open(save_path, 'wb+') as destination:
                    for chunk in upload.chunks():
                        destination.write(chunk)

                if validate_uploaded_file(save_path, m):

                    thumb = create_thumbnail(board, upload)

                    upl = Upload(
                        board=board,
                        thread=op,
                        upload=upl_path,
                        thumbnail=thumb,
                        )

                    upl.save()
    else:
        print(form.errors)
