from django.db import models



class Board(models.Model):
    name = models.CharField(max_length=100)
    url = models.CharField(max_length=10)
    max_pages = models.IntegerField(default=10)
    max_file_size = models.IntegerField(default=1024)
    max_files = models.IntegerField(default=15000)
    def __str__(self):
        return self.name

class OriginalPost(models.Model):
    board = models.ForeignKey(Board, on_delete=models.CASCADE)
    author = models.CharField(max_length=100, blank=True, default='Аноним')
    subject = models.CharField(max_length=100, blank=True)
    text = models.TextField(max_length=3000)
    pub_date = models.DateTimeField()
    upd_date = models.DateTimeField()
    counter = models.IntegerField()
    def __str__(self):
        return str(self.id)

class Post(models.Model):
    board = models.ForeignKey(Board, default=1, on_delete=models.CASCADE)
    thread = models.ForeignKey(OriginalPost, on_delete=models.CASCADE)
    author = models.CharField(max_length=100, blank=True, default='Аноним')
    subject = models.CharField(max_length=100, blank=True)
    text = models.TextField(max_length=3000)
    pub_date = models.DateTimeField()
    counter = models.IntegerField()
    def __str__(self):
        return str(self.id)
        
class Replies(models.Model):
    parent_thread = models.ForeignKey(OriginalPost, on_delete=models.SET_NULL, blank=True, null=True, related_name='replies_to_thread')
    parent_post = models.ForeignKey(Post, on_delete=models.SET_NULL, blank=True, null=True, related_name='replies_to_post')
    child_thread = models.ForeignKey(OriginalPost, on_delete=models.CASCADE, blank=True, null=True)
    child_post = models.ForeignKey(Post, on_delete=models.CASCADE, blank=True, null=True)
    def __str__(self):
        return str(self.id)
        
def uploads_path(instance, filename):
    return '{0}/uploads/{1}'.format(instance.board.id, filename)

class Upload(models.Model):
    board = models.ForeignKey(Board, on_delete=models.CASCADE)
    thread = models.ForeignKey(OriginalPost, on_delete=models.CASCADE)
    reply = models.ForeignKey(Post, on_delete=models.CASCADE, blank=True, null=True)
    upload = models.FileField(upload_to=uploads_path)
    def __str__(self):
        return str(self.upload)
