from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import JsonResponse
from django.views import View

from store_app.models import Product, Comment


class AddNewCommentView(LoginRequiredMixin, View):
    """Класс добавления комментария (мнения по товару, его оценка)"""

    def post(self, request):
        response_data = {}
        try:
            rating = request.POST.get('rating')
            text_comment = request.POST.get('text_comment')
            commented_product = Product.objects.get(pk=request.POST.get('product_id'))

            Comment.objects.create(rating=int(rating), text_comment=text_comment,
                                   author_comment=request.user, product=commented_product)

            # изменить инфу в БД Products
            # commented_product.update_avgRating_countReviews(commented_product)
            # commented_product.count_reviews += 1
            # commented_product.avg_rating = product.comment_set.all().aggregate(Avg('rating'))['rating__avg']
            # commented_product.save()

            response_data['status'] = 'OK'
            response_data['rating'] = rating
            response_data['text_comment'] = text_comment
            response_data['user'] = request.user.username
            return JsonResponse(response_data)

        except Exception as e:
            print(e)
            response_data['status'] = 'BAD'
            return JsonResponse(response_data)