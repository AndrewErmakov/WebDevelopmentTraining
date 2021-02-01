from django.db.models import signals, Avg
from django.dispatch import receiver

from .models import Comment


@receiver(signals.post_save, sender=Comment)
def post_save_comment(sender, instance, created, **kwargs):
    """Сигналы после добавления комментария"""
    product = instance.product
    product.count_reviews += 1
    product.avg_rating = product.comment_set.all().aggregate(Avg('rating'))['rating__avg']
    product.save()


@receiver(signals.post_delete, sender=Comment)
def post_delete_comment(sender, instance, created=False, **kwargs):
    """Сигнал после удаления комментария"""
    product = instance.product
    product.count_reviews -= 1
    if product.count_reviews == 0:
        product.avg_rating = -1
    else:
        product.avg_rating = product.comment_set.all().aggregate(Avg('rating'))['rating__avg']
    product.save()


