from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import redirect, render, get_object_or_404, HttpResponse
from django import views
from django.db.models import Q
from .models import *
from .forms import *
from django.core.paginator import Paginator
from django.db.models.functions import Cast

# Create your views here.

class CategoryView(views.View):

    def get(self, request, pc):
        primary = pc
        category = CategoryModel.objects.all().order_by("primary_cat", "number")
        return render(request, 'store/category.html', {'category':category, 'primary':primary})


class CategoryProductsView(views.View):

    def get(self, request, cid):
        products = ProductModel.objects.filter(Q(category__id=cid) & Q(available=True)).order_by('-created_date')
        category = get_object_or_404(CategoryModel, pk=cid)
        categories = CategoryModel.objects.filter(Q(primary_cat=category.primary_cat) & ~Q(pk=cid)).order_by("number")
        sale = ProductModel.objects.filter(Q(category__primary_cat=category.primary_cat) & Q(available=True) & Q(on_sale__gt="0"))
        tags = TagsModel.objects.all()
        paginator = Paginator(products, 24)
        page_number = request.GET.get('page')
        page_obj = paginator.get_page(page_number)
        page_content = {
            'page_obj':page_obj,
            'categories':categories,
            'sale':sale,
            'tags':tags,
            'category':category,
            'filter':'all',
        }
        return render(request, 'store/category-products.html', page_content)


class CategoryProductsVisitedView(views.View):

    def get(self, request, cid):
        products = ProductModel.objects.filter(Q(category__id=cid) & Q(available=True)).order_by('-visit')
        category = get_object_or_404(CategoryModel, pk=cid)
        categories = CategoryModel.objects.filter(Q(primary_cat=category.primary_cat) & ~Q(pk=cid)).order_by("number")
        sale = ProductModel.objects.filter(Q(category__primary_cat=category.primary_cat) & Q(available=True) & Q(on_sale__gt="0"))
        tags = TagsModel.objects.all()
        paginator = Paginator(products, 24)
        page_number = request.GET.get('page')
        page_obj = paginator.get_page(page_number)
        page_content = {
            'page_obj':page_obj,
            'categories':categories,
            'sale':sale,
            'tags':tags,
            'category':category,
            'filter':'visited',
        }
        return render(request, 'store/category-products.html', page_content)


class CategoryProductsSaleView(views.View):

    def get(self, request, cid):
        products = ProductModel.objects.filter(Q(category__id=cid) & Q(available=True)).order_by('-on_sale')
        category = get_object_or_404(CategoryModel, pk=cid)
        categories = CategoryModel.objects.filter(Q(primary_cat=category.primary_cat) & ~Q(pk=cid)).order_by("number")
        sale = ProductModel.objects.filter(Q(category__primary_cat=category.primary_cat) & Q(available=True) & Q(on_sale__gt="0"))
        tags = TagsModel.objects.all()
        paginator = Paginator(products, 24)
        page_number = request.GET.get('page')
        page_obj = paginator.get_page(page_number)
        page_content = {
            'page_obj':page_obj,
            'categories':categories,
            'sale':sale,
            'tags':tags,
            'category':category,
            'filter':'sale',
        }
        return render(request, 'store/category-products.html', page_content)


class CategoryProductsHighView(views.View):

    def get(self, request, cid):
        products = ProductModel.objects.annotate(my_int_field=Cast('price', output_field=models.IntegerField())).filter(Q(category__id=cid) & Q(available=True) & ~Q(price=None)).order_by('-my_int_field')
        category = get_object_or_404(CategoryModel, pk=cid)
        categories = CategoryModel.objects.filter(Q(primary_cat=category.primary_cat) & ~Q(pk=cid)).order_by("number")
        sale = ProductModel.objects.filter(Q(category__primary_cat=category.primary_cat) & Q(available=True) & Q(on_sale__gt="0"))
        tags = TagsModel.objects.all()
        paginator = Paginator(products, 24)
        page_number = request.GET.get('page')
        page_obj = paginator.get_page(page_number)
        page_content = {
            'page_obj':page_obj,
            'categories':categories,
            'sale':sale,
            'tags':tags,
            'category':category,
            'filter':'high',
        }
        return render(request, 'store/category-products.html', page_content)


class CategoryProductsLowView(views.View):

    def get(self, request, cid):
        products = ProductModel.objects.annotate(my_int_field=Cast('price', output_field=models.IntegerField())).filter(Q(category__id=cid) & Q(available=True) & ~Q(price=None)).order_by('my_int_field')
        category = get_object_or_404(CategoryModel, pk=cid)
        categories = CategoryModel.objects.filter(Q(primary_cat=category.primary_cat) & ~Q(pk=cid)).order_by("number")
        sale = ProductModel.objects.filter(Q(category__primary_cat=category.primary_cat) & Q(available=True) & Q(on_sale__gt="0"))
        tags = TagsModel.objects.all()
        paginator = Paginator(products, 24)
        page_number = request.GET.get('page')
        page_obj = paginator.get_page(page_number)
        page_content = {
            'page_obj':page_obj,
            'categories':categories,
            'sale':sale,
            'tags':tags,
            'category':category,
            'filter':'low',
        }
        return render(request, 'store/category-products.html', page_content)
        

class AllProductsView(views.View):

    def get(self, request):
        form_f = FilterForm(request.GET)
        on_sale = ProductModel.objects.filter(on_sale__gt=0)[:3]
        tags = TagsModel.objects.all()
        products = ""
        if form_f.is_valid():
            wate = form_f.cleaned_data["wate"]
            pattern = form_f.cleaned_data["pattern"]
            price = form_f.cleaned_data["price"]
            if wate and pattern:
                products = ProductModel.objects.filter(Q(wate__in=wate) & Q(pattern__in=pattern)).order_by('available', '-created_date')
                if price == "lth":
                    products = ProductModel.objects.annotate(my_int_field=Cast('price', output_field=models.IntegerField())).filter(Q(wate__in=wate) & Q(pattern__in=pattern) & ~Q(price=None)).order_by('available', 'my_int_field')
                elif price == "htl":
                    products = ProductModel.objects.annotate(my_int_field=Cast('price', output_field=models.IntegerField())).filter(Q(wate__in=wate) & Q(pattern__in=pattern) & ~Q(price=None)).order_by('available', '-my_int_field')
                elif price == "fav":
                    products = ProductModel.objects.filter(Q(wate__in=wate) & Q(pattern__in=pattern)).order_by('available', '-visit')
                paginator = Paginator(products, 24)
                page_number = request.GET.get('page')
                page_obj = paginator.get_page(page_number)
                page_content = {
                    'page_obj':page_obj,
                    'sale':on_sale,
                    'tags':tags,
                    'form_f':form_f,
                    'wate':wate,
                    'pattern':pattern,
                    'price':price,
                }
                return render(request, 'store/all-products.html', page_content)
            elif not wate and not pattern:
                products =ProductModel.objects.all().order_by('available', '-created_date')
                if price == "lth":
                    products = ProductModel.objects.annotate(my_int_field=Cast('price', output_field=models.IntegerField())).filter(~Q(price=None)).order_by('available', 'my_int_field')
                elif price == "htl":
                    products = ProductModel.objects.annotate(my_int_field=Cast('price', output_field=models.IntegerField())).filter(~Q(price=None)).order_by('available', '-my_int_field')
                elif price == "fav":
                    products = ProductModel.objects.all().order_by('available', '-visit')
                paginator = Paginator(products, 24)
                page_number = request.GET.get('page')
                page_obj = paginator.get_page(page_number)
                page_content = {
                    'page_obj':page_obj,
                    'sale':on_sale,
                    'tags':tags,
                    'form_f':form_f,
                    'wate':wate,
                    'pattern':pattern,
                    'price':price,
                }
                return render(request, 'store/all-products.html', page_content)
            else:
                products = ProductModel.objects.filter(Q(wate__in=wate) | Q(pattern__in=pattern)).order_by('available', '-created_date')
                if price == "lth":
                    products = ProductModel.objects.annotate(my_int_field=Cast('price', output_field=models.IntegerField())).filter(Q(wate__in=wate) | Q(pattern__in=pattern) & ~Q(price=None)).order_by('available', 'my_int_field')
                elif price == "htl":
                    products = ProductModel.objects.annotate(my_int_field=Cast('price', output_field=models.IntegerField())).filter(Q(wate__in=wate) | Q(pattern__in=pattern) & ~Q(price=None)).order_by('available', '-my_int_field')
                elif price == "fav":
                    products = ProductModel.objects.filter(Q(wate__in=wate) | Q(pattern__in=pattern)).order_by('available', '-visit')
                paginator = Paginator(products, 24)
                page_number = request.GET.get('page')
                page_obj = paginator.get_page(page_number)
                page_content = {
                    'page_obj':page_obj,
                    'sale':on_sale,
                    'tags':tags,
                    'form_f':form_f,
                    'wate':wate,
                    'pattern':pattern,
                    'price':price,
                }
                return render(request, 'store/all-products.html', page_content)
        else:
            products = ProductModel.objects.all().order_by('available', '-created_date')
            paginator = Paginator(products, 24)
            page_number = request.GET.get('page')
            page_obj = paginator.get_page(page_number)
            page_content = {
                'page_obj':page_obj,
                'sale':on_sale,
                'tags':tags,
                'form_f':form_f,
                'wate':wate,
                'pattern':pattern,
                'price':price,
            }
            return render(request, 'store/all-products.html', page_content)


class ProductDetailsView(views.View):

    def get(self, request, code):
        product = get_object_or_404(ProductModel, code=code)
        product.visit += 1
        product.save()
        suggests = ProductModel.objects.filter(pattern=product.pattern).order_by('-created_date')[:4]
        images = ProductImageModel.objects.filter(name_id=product.id)
        page_content = {
            'product':product,
            'images':images,
            'suggests':suggests,
        }
        return render(request, 'store/product-details.html', page_content)


class CartAddView(views.View):

    def get(self, request, pid):
        ref = request.META['HTTP_REFERER']
        product = get_object_or_404(ProductModel, id=pid)
        cart = request.session.get('cart', {})
        k = str(product.id)
        if product.available:
            if k in cart:
                cart[k] = 1    
            else:
                cart[k] = 1
        else:
            pass
        request.session['cart'] = cart
        return redirect(ref)


class CartDetailsView(views.View):

    def get(self, request):
        cart = request.session.get('cart', {})
        products = ProductModel.objects.filter(id__in=[int(id) for id in cart.keys()])
        c = {}
        total = 0
        for k,v in cart.items():
            product = products.get(id=int(k))
            total += product.price * v
            c[k] = {'product': product, 'count': v}
        return render(request, 'store/cartdetails.html', {'cart': c, "total":total})


class CartRemoveView(views.View):

    def get(self, request, pid):
        cart = request.session.get('cart', {})
        id = str(pid)
        if id in cart:
            cart.pop(id)
        request.session['cart'] = cart
        ref = request.META['HTTP_REFERER']
        return redirect(ref)


class TagsView(views.View):

    def get(self, request, id):
        tag = get_object_or_404(TagsModel, pk=id)
        form_f = FilterForm(request.GET)
        on_sale = ProductModel.objects.filter(on_sale__gt=0)[:3]
        tags = TagsModel.objects.all()
        products = ""
        if form_f.is_valid():
            wate = form_f.cleaned_data["wate"]
            pattern = form_f.cleaned_data["pattern"]
            price = form_f.cleaned_data["price"]
            if wate and pattern:
                products = ProductModel.objects.filter(Q(wate__in=wate) & Q(pattern__in=pattern) & Q(tags=tag)).order_by('available', '-created_date')
                if price == "lth":
                    products = ProductModel.objects.annotate(my_int_field=Cast('price', output_field=models.IntegerField())).filter(Q(wate__in=wate) & Q(pattern__in=pattern) & ~Q(price=None) & Q(tags=tag)).order_by('available', 'my_int_field')
                elif price == "htl":
                    products = ProductModel.objects.annotate(my_int_field=Cast('price', output_field=models.IntegerField())).filter(Q(wate__in=wate) & Q(pattern__in=pattern) & ~Q(price=None) & Q(tags=tag)).order_by('available', '-my_int_field')
                elif price == "fav":
                    products = ProductModel.objects.filter(Q(wate__in=wate) & Q(pattern__in=pattern) & Q(tags=tag)).order_by('available', '-visit')
                paginator = Paginator(products, 24)
                page_number = request.GET.get('page')
                page_obj = paginator.get_page(page_number)
                page_content = {
                    'page_obj':page_obj,
                    'sale':on_sale,
                    'tags':tags,
                    'form_f':form_f,
                    'tag':tag,
                    'wate':wate,
                    'pattern':pattern,
                    'price':price,
                }
                return render(request, 'store/tag-products.html', page_content)
            elif not wate and not pattern:
                products =ProductModel.objects.filter(tags=tag).order_by('available', '-created_date')
                if price == "lth":
                    products = ProductModel.objects.annotate(my_int_field=Cast('price', output_field=models.IntegerField())).filter(~Q(price=None) & Q(tags=tag)).order_by('available', 'my_int_field')
                elif price == "htl":
                    products = ProductModel.objects.annotate(my_int_field=Cast('price', output_field=models.IntegerField())).filter(~Q(price=None) & Q(tags=tag)).order_by('available', '-my_int_field')
                elif price == "fav":
                    products = ProductModel.objects.filter(tags=tag).order_by('available', '-visit')
                paginator = Paginator(products, 24)
                page_number = request.GET.get('page')
                page_obj = paginator.get_page(page_number)
                page_content = {
                    'page_obj':page_obj,
                    'sale':on_sale,
                    'tags':tags,
                    'form_f':form_f,
                    'tag':tag,
                    'wate':wate,
                    'pattern':pattern,
                    'price':price,
                }
                return render(request, 'store/tag-products.html', page_content)
            else:
                products = ProductModel.objects.filter(Q(tags=tag)).filter(Q(wate__in=wate) | Q(pattern__in=pattern)).order_by('available', '-created_date')
                if price == "lth":
                    products = ProductModel.objects.annotate(my_int_field=Cast('price', output_field=models.IntegerField())).filter(~Q(price=None) & Q(tags=tag)).filter(Q(wate__in=wate) | Q(pattern__in=pattern)).order_by('available', 'my_int_field')
                elif price == "htl":
                    products = ProductModel.objects.annotate(my_int_field=Cast('price', output_field=models.IntegerField())).filter(~Q(price=None) & Q(tags=tag)).filter(Q(wate__in=wate) | Q(pattern__in=pattern)).order_by('available', '-my_int_field')
                elif price == "fav":
                    products = ProductModel.objects.filter(Q(wate__in=wate) | Q(pattern__in=pattern) & Q(tags=tag)).order_by('available', '-visit')
                paginator = Paginator(products, 24)
                page_number = request.GET.get('page')
                page_obj = paginator.get_page(page_number)
                page_content = {
                    'page_obj':page_obj,
                    'sale':on_sale,
                    'tags':tags,
                    'form_f':form_f,
                    'tag':tag,
                    'wate':wate,
                    'pattern':pattern,
                    'price':price,
                }
                return render(request, 'store/tag-products.html', page_content)
        else:
            products = ProductModel.objects.filter(tags=tag).order_by('available', '-created_date')
            paginator = Paginator(products, 24)
            page_number = request.GET.get('page')
            page_obj = paginator.get_page(page_number)
            page_content = {
                'page_obj':page_obj,
                'sale':on_sale,
                'tags':tags,
                'form_f':form_f,
                'tag':tag,
                'wate':wate,
                'pattern':pattern,
                'price':price,
            }
            return render(request, 'store/tag-products.html', page_content)
    

class HeaderSearchView(views.View):

    def get(self, request):
        form = HeaderSearchForm(request.GET)
        products = []
        if form.is_valid():
            query = form.cleaned_data.get('query')
            products = ProductModel.objects.filter((Q(name__icontains=query) | Q(code__icontains=query) | Q(short_description__icontains=query)), Q(available=True))
            paginator = Paginator(products, 24)
            page_number = request.GET.get('page')
            page_obj = paginator.get_page(page_number)
            return render(request, 'jcompany/search.html', {'page_obj':page_obj})
        return render(request, 'jcompany/search.html', {"results":"none"})

        
# class PriceUpdateView(LoginRequiredMixin, views.View):
#     login_url = 'login'

#     def get(self, request):
#         user = get_object_or_404(User, pk=request.user.id)
#         if user.is_staff and user.is_superuser:
#             form = PriceUpdateForm()
#             return render(request, 'store/price-update.html', {'form':form})
#         return HttpResponse('عدم دسترسی')
    
#     def post(self, request):
#         form = PriceUpdateForm(request.POST, request.FILES)
#         if form.is_valid():
#             file = request.FILES['file']
#             dataframe1 = pd.read_excel(file, converters={'کد':str, 'قیمت':int, 'قیمت با تخفیف':int})
#             for i in range(0, len(dataframe1)):
#                 c = dataframe1.at[i, 'کد']
#                 p = dataframe1.at[i, 'قیمت']
#                 p_i = dataframe1.at[i, 'قیمت با تخفیف']
#                 if p_i and p_i > 0:
#                     try:
#                         obj = ProductModel.objects.get(code=c)
#                         obj.price = p_i
#                         obj.save()
#                     except ProductModel.DoesNotExist:
#                         pass
#                 if p and p > 0:
#                     try:
#                         obj = ProductModel.objects.get(code=c)
#                         obj.price_in = p
#                         obj.save()
#                     except ProductModel.DoesNotExist:
#                         pass
#             return HttpResponse('موفق')
#         return HttpResponse('اخطار')
    

class ImagesDeleteView(LoginRequiredMixin, views.View):
    login_url = 'login'

    def get(self, request):
        user = get_object_or_404(User, pk=request.user.id)
        if user.is_staff and user.is_superuser:
            obj = ProductModel.objects.filter(available=False)
            for i in obj:
                i.cover.delete()
                img = ProductImageModel.objects.filter(name=i)
                for j in img:
                    j.images.delete()
            return HttpResponse('موفق')
        return HttpResponse('عدم دسترسی')