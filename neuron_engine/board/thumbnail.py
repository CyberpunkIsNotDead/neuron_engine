from django.conf import settings
from PIL import Image
import os

def create_thumbnail(board, infile):

    outfile = os.path.splitext(infile.name)[0] + "_thumbnail"
    im = Image.open(infile)

    im.thumbnail((200, 200), Image.ANTIALIAS)
    thumb_path = os.path.join(board.url, 'thumbnails')

    save_path = os.path.join(settings.MEDIA_ROOT, thumb_path)
    os.makedirs(save_path, exist_ok=True)
    im.save(save_path + '/' + outfile + '.png', "PNG")

    return os.path.join(thumb_path, outfile + '.png')

# todo: try-except
