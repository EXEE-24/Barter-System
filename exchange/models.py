from django.db import models
from ads.models import Ad
from django.utils import timezone

def is_pending(self):
    return self.status == 'pending'

class ExchangeProposal(models.Model):
    STATUS_CHOICES = [
        ('pending', 'Ожидает рассмотрения'),
        ('accepted', 'Принято'),
        ('rejected', 'Отклонено'),
        ('canceled', 'Отменено'),
    ]

    ad_sender = models.ForeignKey(
        Ad,
        related_name='sent_proposals',
        on_delete=models.CASCADE,
        verbose_name='Предлагаемый товар'
    )
    ad_receiver = models.ForeignKey(
        Ad,
        related_name='received_proposals',
        on_delete=models.CASCADE,
        verbose_name='Запрашиваемый товар'
    )
    comment = models.TextField(verbose_name='Комментарий', blank=True)
    status = models.CharField(
        max_length=20,
        choices=STATUS_CHOICES,
        default='pending',
        verbose_name='Статус'
    )
    created_at = models.DateTimeField(default=timezone.now)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = 'Предложение обмена'
        verbose_name_plural = 'Предложения обмена'
        ordering = ['-created_at']
        constraints = [
            models.UniqueConstraint(
                fields=['ad_sender', 'ad_receiver'],
                name='unique_proposal'
            )
        ]

    def __str__(self):
        return f"Обмен {self.ad_sender} на {self.ad_receiver}"

    def save(self, *args, **kwargs):
        if self.ad_sender.user == self.ad_receiver.user:
            raise ValueError("Нельзя создавать предложение для своего же товара")
        super().save(*args, **kwargs)