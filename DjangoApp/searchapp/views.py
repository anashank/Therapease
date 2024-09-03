from django.shortcuts import render
from django.db import models
from .models import Article
from django.contrib.auth.decorators import login_required

# Create your views here.
def search(request):
    query = request.GET.get('q')
    results = []
    if query:
        results = Article.objects.filter(
            models.Q(title__icontains=query) | 
            models.Q(content__icontains=query)
        )
    return render(request, 'searchapp/search.html', {'results': results, 'query': query})