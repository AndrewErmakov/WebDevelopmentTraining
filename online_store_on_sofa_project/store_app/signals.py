from django.db.models import Avg
from django.db.models.signals import post_save
from django.dispatch import receiver

from .models import Comment


@receiver(post_save, sender=Comment)
def update_avgRating_countReviews(instance, **kwargs):
    """Сигнал после добавления комментария на товар"""
    print('comment saved')
    product = instance.product
    product.count_reviews += 1
    product.avg_rating = instance.objects.filter(product=product).aggregate(Avg('rating'))['rating__avg']
    product.save()
