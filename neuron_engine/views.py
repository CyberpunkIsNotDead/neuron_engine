from django.shortcuts import render, get_object_or_404
from django.http import HttpResponse, Http404
from django.utils.safestring import *

#from django.urls import reverse

from .models import Board, OriginalPost
from .forms import *


from .board import board as b, thread as t, markup, posting, misc



# index view

def main_page(request):

    boards = Board.objects.all()
    info = {}

    for board in boards:
        counter = misc.post_counter(board)
        info[board] = counter - 1


    context = {
        'info': info,
    }

    return render(request, 'neuron_engine/main_page.html', context)



# board view

def board(request, board_url):

    board = get_object_or_404(Board, url=board_url)

    form = PostForm()

    # methods

    if request.method == "GET":

        context = b.assemble_board_page(request, board, form)
        return render(request, 'neuron_engine/board.html', context)

    elif request.method == "POST":

        uploads = request.FILES.getlist('upload')
        form = PostForm(request.POST)

        posting.create_thread(board, form, uploads)

        context = b.assemble_board_page(request, board, form)
        return render(request, 'neuron_engine/board.html', context)



# thread view

def thread(request, board_url, original_post_counter):

    board = get_object_or_404(Board, url=board_url)

    try:
        original_post = OriginalPost.objects.filter(board=board.id).get(
            counter=original_post_counter
            )
        original_post.text = mark_safe(original_post.text)

    except OriginalPost.DoesNotExist:
        raise Http404()

    form = PostForm()

    # methods

    if request.method == "GET":

        context = t.assemble_thread(board, form, original_post)
        return render(request, 'neuron_engine/thread.html', context)


    elif request.method == "POST":

        uploads = request.FILES.getlist('upload')
        form = PostForm(request.POST)

        posting.create_post(board, original_post, form, uploads)

        context = t.assemble_thread(board, form, original_post)
        return render(request, 'neuron_engine/thread.html', context)
