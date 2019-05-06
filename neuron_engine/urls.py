from django.contrib import admin
from django.urls import path
from django.conf import settings
from django.conf.urls.static import static

from . import views

app_name = 'neuron_engine'
urlpatterns = [
    path('admin/', admin.site.urls),
    path('', views.main_page, name='main_page'),
    path('<board_url>/', views.board, name='board'),
    path('<board_url>/thread/<int:original_post_counter>/', views.thread, name='thread'),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
