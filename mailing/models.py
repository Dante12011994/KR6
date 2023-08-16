from django.db import models

NULLABLE = {'blank': True, 'null': True}


class Customer(models.Model):
    email = models.CharField(max_length=250, verbose_name='email')
    fio = models.CharField(max_length=150, verbose_name='ФИО')
    comment = models.TextField(verbose_name='коментарий', **NULLABLE)

    def __str__(self):
        return self.fio

    class Meta:
        verbose_name = 'клиент'
        verbose_name_plural = 'клиенты'


class Mailing(models.Model):
    INTERVAL = [('day', 'каждый день'), ('week', 'раз в неделю'), ('month', 'раз в месяц')]
    STATUS = [('create', 'создана'), ('start', 'запущена'), ('finished', 'завершена')]
    name = models.CharField(max_length=150, verbose_name='название рассылки')
    start = models.DateTimeField(verbose_name='начало рассылки')
    stop = models.DateTimeField(verbose_name='конец рассылки')
    interval = models.CharField(max_length=5, choices=INTERVAL, default='day')
    users_group = models.ManyToManyField(Customer, verbose_name='группа пользователей для рассылки')
    status_mail = models.CharField(max_length=8, choices=STATUS, default='create')

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = 'рассылка'
        verbose_name_plural = 'рассылки'


class Massage(models.Model):
    mailing = models.ForeignKey(Mailing, on_delete=models.CASCADE, verbose_name='рассылка')
    mail_subject = models.CharField(max_length=300, verbose_name='тема письма')
    text = models.TextField(verbose_name='тело письма')

    def __str__(self):
        return self.mail_subject

    class Meta:
        verbose_name = 'письмо'
        verbose_name_plural = 'письма'


class Attempt(models.Model):
    mailing = models.ForeignKey(Mailing, on_delete=models.CASCADE, verbose_name='рассылка')
    datetime = models.DateTimeField(auto_now_add=True, verbose_name='дата и время попытки')
    attempt = models.BooleanField(default=False, verbose_name='статус попытки')
    feedback = models.TextField(verbose_name='ответ сервера', **NULLABLE)

    def __str__(self):
        return self.mailing

    class Meta:
        verbose_name = 'попытка'
        verbose_name_plural = 'попытки'
