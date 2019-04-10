from django.contrib import admin

from .models import *

admin.site.register(Board)
admin.site.register(OriginalPost)
admin.site.register(Post)
admin.site.register(Replies)
admin.site.register(Upload)

