from .models import CategoryModel, ProductModel
from blog.models import BlogModel, BlogEnModel
from django import forms


class SearchForm(forms.Form):
    search = forms.CharField(label='جستجو')


def menu(request):
    form = SearchForm()
    category_c = CategoryModel.objects.filter(primary_cat="carpet")
    category_w = CategoryModel.objects.filter(primary_cat="wallcarpet")
    category_k = CategoryModel.objects.filter(primary_cat="kilim")
    blog = BlogModel.objects.all().order_by('-created_date')[:3]
    blog_en = BlogEnModel.objects.all().order_by('-created_date')[:3]
    cart = request.session.get('cart', {})
    products = ProductModel.objects.filter(id__in=[int(id) for id in cart.keys()])
    c = {}
    total = 0
    for k,v in cart.items():
        product = products.get(id=int(k))
        total += product.price
        c[k] = {'product': product, 'count': v}
    return {"carpet":category_c, "wall":category_w, "kilim":category_k, "cart":c, "total":total, 'blogs':blog, 'enblogs':blog_en, 'form':form}