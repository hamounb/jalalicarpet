from django.shortcuts import render, redirect, get_object_or_404
from django import views
from .models import *
from django.core.paginator import Paginator
from store.models import ProductModel
from .forms import ContactUsForm, FooterNewsForm
from blog.models import BlogModel
from store.context_processors import HeaderSearchForm
from django.db.models import Q

# Create your views here.



class IndexView(views.View):

    def get(self, request):
        a = False
        if a:
            return render(request, 'jcompany/index1.html')
        posters = PosterModel.objects.all()
        new_blog = BlogModel.objects.all().order_by('-created_date')[:4]
        on_sale = OnSalePosterModel.objects.all().order_by("-created_date")[:1]
        ex = ExibitionModel.objects.all().order_by('-start_date')[:4]
        video = VideoModel.objects.all().order_by('-created_date')[:3]
        customer_video = CustomerVideoModel.objects.all().order_by("-created_date")[:3]
        page_content = {
            'posters':posters,
            'new_blog':new_blog,
            'on_sale':on_sale,
            'ex':ex,
            'video':video,
            'customer_video':customer_video,
        }
        return render(request, 'jcompany/index.html', page_content)
    
    
class AboutUsView(views.View):

    def get(self, request):
        return render(request, 'jcompany/about-us.html', )


class ContactUsView(views.View):

    def get(self, request):
        form = ContactUsForm()
        return render(request, 'jcompany/contact-us.html', {'form':form})

    def post(self, request):
        form = ContactUsForm(request.POST)
        if form.is_valid():
            form.save()
            return render(request, 'jcompany/message-success.html')
        return render(request, 'jcompany/contact-us.html', {'form':form})


class ExhibitionView(views.View):

    def get(self, request):
        try:
            exhibition = ExibitionModel.objects.all().order_by('-created_date')
        except ExibitionModel.DoesNotExist:
            exhibition = []
        suggests = ProductModel.objects.filter(on_sale__gt=0).order_by('-created_date')[:3]
        city = CityModel.objects.all()
        paginator = Paginator(exhibition, 12)
        page_number = request.GET.get('page')
        page_obj = paginator.get_page(page_number)
        context = {
            'exhibition':page_obj,
            'suggests':suggests,
            'city':city,
        }
        return render(request, 'jcompany/exhibition.html', context)   
        

class CityView(views.View):

    def get(self, request, cit):
        name = get_object_or_404(CityModel, pk=cit)
        exhibition = ExibitionModel.objects.filter(city=name).order_by("-created_date")
        suggests = ProductModel.objects.filter(on_sale__gt=0).order_by('-created_date')[:3]
        city = CityModel.objects.all()
        paginator = Paginator(exhibition, 12)
        page_number = request.GET.get('page')
        page_obj = paginator.get_page(page_number)
        context = {
            'name':name,
            'exhibition':page_obj,
            'suggests':suggests,
            'city':city,
        }
        return render(request, 'jcompany/exhibition.html', context)

        
class SearchView(views.View):

    def get(self, request):
        form = HeaderSearchForm(request.GET)
        if form.is_valid():
            search = form.cleaned_data['search']
            return redirect('jcompany:search-resault', search=search)


class SearchResaultView(views.View):

    def get(self, request, search):
        products = ProductModel.objects.filter(Q(code__iexact=search) | Q(category__title__icontains=search) | 
        Q(name__contains=search))
        paginator = Paginator(products, 12)
        page_number = request.GET.get('page')
        page_obj = paginator.get_page(page_number)
        return render(request, 'jcompany/search.html', {'page_obj':page_obj})
    

class QuestionView(views.View):

    def get(self, request):
        questions = QuestionModel.objects.filter(available=True).order_by("created_date")
        return render(request, "jcompany/question.html", {"questions":questions})
    

class FooterNewsView(views.View):

    def post(self , request):
        form = FooterNewsForm(request.POST)
        if form.is_valid():
            text = form.cleaned_data.get("text")
            form.save()
            return render(request, "jcompany/news.html", {"text":text})
        return render(request, "jcompany/news.html", {"form":form})
