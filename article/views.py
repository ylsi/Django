#-*- coding: utf-8 -*- 

from django.shortcuts import render
from django.http import HttpResponse
from article.models import Article
from datetime import datetime
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
# Create your views here.

class ArticleNotExist(Exception):
	print("Article Not Found")
	
def index(request, id):
	try:
		post = Article.objects.get(id=int(id))
	except Article.DoesNotExist:
		raise Http404
	return render(request, 'post.html', {'post': post})
	
def test(request):
	return render(request, 'test.html', {'current_time': datetime.now()})
	
def home(request):
	posts = Article.objects.all()
	paginator = Paginator(posts, 2) 
	page = request.GET.get('page')
	try:
		post_list = paginator.page(page)
	except PageNotAnInteger:
		post_list = paginator.page(1)
	except EmptyPage:
		post_list = paginator.paginator(paginator.num_pages)
	
	return render(request, 'home.html', {'post_list': post_list})
	
def archives(request):
	try:
		post_list = Article.objects.all()
	except ArticleNotExist:
		raise Http404
	return render(request, 'archives.html', {'post_list': post_list, 'error': False})
	
def aboutme(request):
	if request.method == 'POST':
		print(request)
		filename = request.files['file']
	return render(request, 'aboutme.html')
	
def search_tag(request, tag):
	try:
		post_list = Article.objects.filter(category__iexact=tag)
	except ArticleNotExist:
		raise Http404
	return render(request, 'search_tag.html', {'post_list': post_list})
	
def blog_search(request):
	if 's' in request.GET:
		s = request.GET['s']
		if not s:
			return render(request, 'home.htm')
		else:
			post_list = Article.objects.filter(title__icontains=s)
			if len(post_list) == 0:
				return render(request, 'archives.html', {'post_list': post_list, 'error': True})
			else:
				return render(request, 'archives.html', {'post_list': post_list, 'error': False})
	return redirect('/')