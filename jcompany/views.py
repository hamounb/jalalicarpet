from django.shortcuts import render, redirect, get_object_or_404
from django import views
from .models import *
from django.core.paginator import Paginator
from store.models import ProductModel, CategoryModel
from .forms import ContactUsForm, FooterNewsForm
from blog.models import BlogModel
from store.context_processors import HeaderSearchForm
from django.db.models import Q
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from django.contrib import messages
from django.db.utils import IntegrityError

# Create your views here.

password = "yghx xikb lkdo mnmh"

gmail_user = 'jalalicollection@gmail.com'
gmail_password = 'yghxxikblkdomnmh'

class IndexView(views.View):

    def get(self, request):
        a = False
        if a:
            return render(request, 'jcompany/index1.html')
        posters = PosterModel.objects.all()
        try:
            lux = CategoryModel.objects.get(title__contains='کلکسیونی')
        except CategoryModel.DoesNotExist:
            lux = ""
        new_blog = BlogModel.objects.all().order_by('-created_date')[:6]
        on_sale = OnSalePosterModel.objects.all().order_by("-created_date")[:1]
        ex = ExibitionModel.objects.all().order_by('-start_date')[:6]
        video = VideoModel.objects.all().order_by('-created_date')[:3]
        customer_video = CustomerVideoModel.objects.all().order_by("-created_date")[:3]
        page_content = {
            'posters':posters,
            'new_blog':new_blog,
            'on_sale':on_sale,
            'ex':ex,
            'video':video,
            'customer_video':customer_video,
            'lux':lux,
        }
        return render(request, 'jcompany/index.html', page_content)
    
    
class AboutUsView(views.View):

    def get(self, request):
        return render(request, 'jcompany/about-us.html', )


class ContactUsView(views.View):

    def get(self, request):
        form_c = ContactUsForm()
        return render(request, 'jcompany/contact-us.html', {'form_c':form_c})

    def post(self, request):
        form_c = ContactUsForm(request.POST)
        if form_c.is_valid():
            form_c.save()
            name = form_c.cleaned_data.get("full_name")
            phone = form_c.cleaned_data.get("phone")
            subject = form_c.cleaned_data.get("subject")
            message = form_c.cleaned_data.get("message")
            try:
                server = smtplib.SMTP(host='smtp.gmail.com', port=587)
                server.starttls()
                server.login(gmail_user, gmail_password)
                msg = MIMEMultipart()
                msg['From'] = gmail_user
                msg['To'] = 'jalalicarpet.ir@gmail.com'
                msg['Subject'] = f"{subject}"
                message = f"""
                Contact Us Form

                نام کامل: {name}
                شماره موبایل یا ایمیل: {phone}
                متن پیام:
                {message}
                """
                msg.attach(MIMEText(message, 'plain'))
                server.send_message(msg)
            except Exception as e:
                messages.error(request, f"خطای سیستمی رخ داده است، لطفاً دوباره پیام خود را ارسال کنید.")
                return render(request, 'jcompany/contact-us.html', {'form_c':form_c})
            return render(request, 'jcompany/message-success.html')
        return render(request, 'jcompany/contact-us.html', {'form_c':form_c})


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
        paginator = Paginator(products, 24)
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
            try:
                form.save()
            except IntegrityError:
                return render(request, "jcompany/news.html", {"text":text})
            try:
                server = smtplib.SMTP(host='smtp.gmail.com', port=587)
                server.starttls()
                server.login(gmail_user, gmail_password)
                msg = MIMEMultipart()
                msg['From'] = gmail_user
                msg['To'] = 'jalalicarpet.ir@gmail.com'
                msg['Subject'] = f"عضویت جدید در خبرنامه"
                message = f"""
                News Form
                شماره موبایل یا ایمیل: {text}
                متن پیام: عضو جدید با موفقیت ثبت شد.
                """
                msg.attach(MIMEText(message, 'plain'))
                server.send_message(msg)
            except Exception as e:
                return render(request, "jcompany/news.html", {"form":form})
            return render(request, "jcompany/news.html", {"text":text})
        return render(request, "jcompany/news.html", {"form":form})
