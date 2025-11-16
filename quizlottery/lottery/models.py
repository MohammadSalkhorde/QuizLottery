from django.db import models
from accounts.models import CustomUser
from django.utils import timezone
import uuid
import random

class Questions(models.Model):
    ANSWER_CHOICES = (
        ('1', 'answer1'),
        ('2', 'answer2'),
    )

    question = models.CharField(max_length=100, verbose_name='سوال')
    answer1 = models.CharField(max_length=100, verbose_name='پاسخ 1')
    answer2 = models.CharField(max_length=100, verbose_name='پاسخ 2')
    correct_answer = models.CharField(
        max_length=1,
        choices=ANSWER_CHOICES,
        verbose_name='پاسخ صحیح'
    )
    amount = models.PositiveIntegerField(default=0, verbose_name='مبلغ قابل پرداخت')
    register_date = models.DateTimeField(auto_now_add=True, verbose_name='تاریخ درج سوال')
    is_active = models.BooleanField(default=False, verbose_name='وضعیت')

    def __str__(self):
        return f'{self.question} ({self.get_correct_answer_display()})'

    class Meta:
        verbose_name = 'سوال'
        verbose_name_plural = 'سوالات'


class GoldCard(models.Model):
    """
    GoldCard assigned to a user for a specific question.
    Serial number is unique and 16-digit numeric.
    """
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE, verbose_name='کاربر', related_name='user_gold_card')
    question = models.ForeignKey(Questions, on_delete=models.CASCADE, verbose_name='سوال', related_name='question_gold_card')
    serial = models.CharField(max_length=16, unique=True, verbose_name='سریال کارت')
    register_date = models.DateTimeField(auto_now_add=True, verbose_name='تاریخ فعالسازی')
    expire_date = models.DateTimeField(verbose_name='تاریخ انقضا')

    def save(self, *args, **kwargs):
        if not self.serial:
            # Generate unique 16-digit numeric serial
            while True:
                new_serial = ''.join([str(random.randint(0, 9)) for _ in range(16)])
                if not GoldCard.objects.filter(serial=new_serial).exists():
                    self.serial = new_serial
                    break
        super().save(*args, **kwargs)

    def __str__(self):
        return f'{self.user} - {self.serial}'

    class Meta:
        verbose_name='کارت طلایی'
        verbose_name_plural='کارت طلایی'
class LotteryList(models.Model):
    """
    Records of users participating in lotteries for questions, optionally using GoldCards.
    """
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE, verbose_name='کاربر', related_name='user_lottery_list')
    question = models.ForeignKey(Questions, on_delete=models.CASCADE, verbose_name='سوال', related_name='question_lottery_list')
    gold_card = models.ForeignKey(GoldCard, on_delete=models.CASCADE, verbose_name='کارت طلایی', related_name='gold_card_lottery_list', null=True, blank=True)

    def __str__(self):
        return f'{self.user} - {self.question}'

    class Meta:
        verbose_name = 'لیست قرعه کشی'
        verbose_name_plural = 'لیست قرعه کشی'
