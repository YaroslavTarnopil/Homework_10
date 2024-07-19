from django.shortcuts import render, redirect
from django.contrib.auth import login, authenticate
from django.contrib.auth.forms import AuthenticationForm
from .forms import RegisterForm

def register(request):
    if request.method == 'POST':
        form = RegisterForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect('home')
    else:
        form = RegisterForm()
    return render(request, 'register.html', {'form': form})

def login_view(request):
    if request.method == 'POST':
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            user = form.get_user()
            login(request, user)
            return redirect('home')
    else:
        form = AuthenticationForm()
    return render(request, 'login.html', {'form': form})

from django.contrib.auth.decorators import login_required
from .forms import AuthorForm, QuoteForm

@login_required
def add_author(request):
    if request.method == 'POST':
        form = AuthorForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('home')
    else:
        form = AuthorForm()
    return render(request, 'add_author.html', {'form': form})

@login_required
def add_quote(request):
    if request.method == 'POST':
        form = QuoteForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('home')
    else:
        form = QuoteForm()
    return render(request, 'add_quote.html', {'form': form})

from .models import Author, Quote

def author_list(request):
    authors = Author.objects.all()
    return render(request, 'author_list.html', {'authors': authors})

def quote_list(request):
    quotes = Quote.objects.all()
    return render(request, 'quote_list.html', {'quotes': quotes})


from django.shortcuts import render, get_object_or_404
from .models import Tag, Quote

def tag_quotes(request, tag_name):
    tag = get_object_or_404(Tag, name=tag_name)
    quotes = tag.quotes.all()
    return render(request, 'tag_quotes.html', {'tag': tag, 'quotes': quotes})

from django.db.models import Count

def top_tags(request):
    top_tags = Tag.objects.annotate(num_quotes=Count('quotes')).order_by('-num_quotes')[:10]
    return {'top_tags': top_tags}

from django.core.paginator import Paginator

def quote_list(request):
    quotes = Quote.objects.all()
    paginator = Paginator(quotes, 10)  
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    return render(request, 'quote_list.html', {'page_obj': page_obj})

import requests
from bs4 import BeautifulSoup

def scrape_quotes(request):
    response = requests.get('http://quotes.toscrape.com')
    soup = BeautifulSoup(response.text, 'html.parser')

    for quote_div in soup.find_all('div', class_='quote'):
        text = quote_div.find('span', class_='text').get_text()
        author_name = quote_div.find('small', class_='author').get_text()
        tags = [tag.get_text() for tag in quote_div.find_all('a', class_='tag')]

        author, created = Author.objects.get_or_create(name=author_name)
        quote = Quote.objects.create(text=text, author=author)

        for tag_name in tags:
            tag, created = Tag.objects.get_or_create(name=tag_name)
            quote.tags.add(tag)

    return render(request, 'scrape_quotes.html', {'status': 'Quotes have been scraped and saved!'})
