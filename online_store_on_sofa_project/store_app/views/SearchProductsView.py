from django.contrib.postgres.search import SearchVector, SearchQuery, SearchRank
from django.shortcuts import render
from django.views import View
from store_app.models import Product


class SearchProductsView(View):
    def get(self, request):
        query = request.GET['search_text']
        search_query = SearchQuery(query)
        search_vector = SearchVector('title', 'description', weight='A') + SearchVector('brand', weight='C')
        products = Product.objects.annotate(
            search=search_vector,
            rank=SearchRank(search_vector, search_query)
        ).filter(search=search_query).order_by('-rank')
        return render(request, 'search_products_page.html', {'query': query, 'products': products})
