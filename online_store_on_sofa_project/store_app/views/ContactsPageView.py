from django.shortcuts import render
from django.views import View


class ContactsPageView(View):
    """Класс просмотра страницы с контактами"""

    def get(self, request):
        return render(request, 'contacts.html')

