from django.db import models
from django.contrib.auth.models import User

class Profile(models.Model):
    user = models.OneToOneField(User, verbose_name='Пользователь', on_delete=models.CASCADE)
    date_time = models.DateTimeField(verbose_name='Дата регистрации', auto_now_add=True)
    b_day = models.DateField(verbose_name='Дата рождения', blank=True)
    skype = models.CharField('Skype', max_length=250, blank=True)
    facebook = models.URLField('Facebook', blank=True)
    about = models.TextField('About', blank=True)

    def __str__(self):
        return '{0} - {1}'.format(self.user.username, self.about)

class Post(models.Model):
    title = models.CharField('Заголовок', max_length=250)
    text = models.TextField('Пост')
    user = models.ForeignKey(User, verbose_name='Пользователь', on_delete=models.CASCADE)
    date_time = models.DateTimeField(verbose_name='Дата регистрации', auto_now_add=True)

    def __str__(self):
        return '{0} - {1} - {2}'.format(self.title, self.text[:150] ,self.date_time)

class Comment(models.Model):
    user = models.ForeignKey(User, verbose_name='Пользователь', on_delete=models.CASCADE)
    post = models.ForeignKey(Post, verbose_name='Пост', on_delete=models.CASCADE)
    text = models.TextField('Коментарий', blank=True)
    date_time = models.DateTimeField(verbose_name='Дата регистрации', auto_now_add=True)

    def __str__(self):
        return self.text


class Message(models.Model):
    _meg_list = []
    text = models.TextField('message')
    date_time = models.DateTimeField(verbose_name='Дата', auto_now_add=True, null=True)
    read = models.BooleanField(verbose_name='Прочитано')
    sender = models.ForeignKey(User, verbose_name='Отправыитель', on_delete=models.CASCADE, related_name="user_s")
    receiver = models.ForeignKey(User, verbose_name='Получатель', on_delete=models.CASCADE, related_name="user_r")

    def __str__(self):
        return '{0} - {1} ({2})'.format(self.text[:150], self.sender.username, self.read)

    def __init__(self, *args, **kwargs):
        self.__class__._meg_list.append(self)
        super(Message, self).__init__(*args, **kwargs)

    # def __new__(self, *args, **kwargs):
    #     self.__class__._meg_list.append(self)
    #     super(Message, self).__new__(*args, **kwargs)



    def unread(self):
        # return len(self.__class__._meg_list)
        return self.sender.user_r.filter(read=False).count()
        # return Message.objects.filter(read=False).count()
