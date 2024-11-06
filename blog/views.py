from django import views
from django.shortcuts import get_object_or_404, render
from .models import *
from django.core.paginator import Paginator

# Create your views here.

class BlogView(views.View):

    def get(self, request):
        try:
            blog = BlogModel.objects.all().order_by('-created_date')
        except BlogModel.DoesNotExist:
            blog = []
        paginator = Paginator(blog, 9)
        page_number = request.GET.get('page')
        page_obj = paginator.get_page(page_number)
        return render(request, 'blog/blog.html', {'blog':page_obj})


class BlogDetailsView(views.View):

    def get(self, request, bid):
        blog = get_object_or_404(BlogModel, pk=bid)
        blog_rec = BlogModel.objects.all().order_by('-created_date')[:4]
        blog_category = BlogCategoryModel.objects.all()
        return render(request, 'blog/blog-details.html', {'blog':blog,'recent':blog_rec,'cat':blog_category})