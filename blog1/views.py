from django.http.response import HttpResponse
from django.shortcuts import redirect, render
from django.views.decorators.csrf import csrf_exempt, csrf_protect, requires_csrf_token
from .models import Article, Author
from .forms import AuthorForm, AuthorRegiterForm, ArticleForm
from django.utils.text import slugify


# Create your views here.
def home(request):
    if not request.session.get('is_logged_in') or not request.session['is_logged_in']:
        data = request.GET
        form = AuthorForm()
        return render(request, 'home.html', {'form':form, 'problem':data, 'state': request.session})
    return redirect('/dashboard/'+request.session['user'])

@csrf_exempt
def login(request):
    if not request.session.get('is_logged_in') or not request.session['is_logged_in']:
        if request.method == 'POST':
            form = AuthorForm(request.POST)
            if form.is_valid():
                print("yes")
                request.session['user'] = request.POST.get('username') 
                request.session['is_logged_in'] = True
                return redirect('/dashboard/'+request.session['user'])
            return render(request, 'home.html', {'form':form, 'state': request.session})
        form = AuthorForm()
        return render(request, 'home.html', {'form':form, 'state':request.session})
    return redirect('/dashboard/'+request.session['user'])

@csrf_exempt
def register(request):
    if not request.session.get('is_logged_in') or not request.session['is_logged_in']:
        if request.method=='POST':
            data = request.POST
            form = AuthorRegiterForm(data)
            if form.is_valid():
                form.save()
                return redirect('/?done=1')
            
            return render(request, 'register.html', {'form':form, 'state':request.session})
        
        form = AuthorRegiterForm()
        return render(request, 'register.html', {'form':form, 'state':request.session})
    return redirect('/dashboard/'+request.session['user'])

def dashboard(request, username):
    if request.session['user']==username and request.session['is_logged_in']:
        articles = Author.objects.get(username=username).articles.all()
        return render(request, 'dashboard.html', {'data':request.session['user'], 'articles':articles})
    return redirect('/')

@csrf_exempt
def logout(request):
    request.session['user'] = ''
    request.session['is_logged_in'] = False
    return redirect('/')

@csrf_exempt
def addArticle(request, username):
    if request.session['user']==username and request.session['is_logged_in']:
        saved=0
        exists=0
        data={}
        if request.method == 'POST':
            data = request.POST
            form = ArticleForm(data)
            if form.is_valid and form.errors=={} and (not Author.objects.get(username=username).articles.filter(title=data['title']).exists()):
                article = Article.objects.create(title=data['title'], content=data['content'])
                article.slugtitle = article.slug()
                article.save()
                author = Author.objects.get(username=username)
                author.articles.add(article)
                author.save()
                saved=1
            exists=1
        if data=={}:
            form = ArticleForm()
        else:
            form = ArticleForm(data)
        if saved==1:
            a = Author.objects.get(username=username).articles.get(title=data['title'])
            return render(request, 'viewArticle.html', {'data':request.session['user'], 'article':a, 'saved':1, 'edited':0})
        return render(request, 'addArticle.html', {'form':form, 'data':request.session['user'], 'exists':exists})
    return redirect('/')

@csrf_exempt
def viewArticle(request, username, slugtitle):
    if request.session['user']==username and request.session['is_logged_in']:
        if Author.objects.get(username=username).articles.filter(slugtitle=slugtitle).exists():
            a = Author.objects.get(username=username).articles.get(slugtitle=slugtitle)
            return render(request, 'viewArticle.html', {'article':a, 'user':username})
        return redirect('/dashboard/'+username)
    return redirect('/')

@csrf_exempt
def editArticle(request, username, slugtitle):
    if request.session['user']==username and request.session['is_logged_in']:
        a = Author.objects.get(username=username).articles.get(slugtitle=slugtitle)
        if request.method == 'GET':
            if Article.objects.filter(slugtitle=slugtitle).exists():
                form = ArticleForm({'title':a.title, 'content':a.content})
                return render(request, 'editArticle.html', {'data':username, 'form':form, 'slugtitle':slugtitle})
        else:
            form = ArticleForm(request.POST)
            if not (request.POST['title']!=a.title and (Author.objects.get(username=username).articles.filter(title=request.POST['title']).exists())):
                a.title = request.POST['title']
                a.content = request.POST['content']
                a.slugtitle = a.slug()
                a.save()
                # articles = Author.objects.get(username=username).articles.all()
                return render(request, 'viewArticle.html', {'data':request.session['user'], 'article':a, 'saved':0, 'edited':1})
            return render(request, 'editArticle.html', {'data':username, 'form':form, 'slugtitle':slugtitle, 'exists':1})
        return redirect('/dashboard/'+username)
    return redirect('/')

def deleteArticle(request, username, slugtitle):
    if request.session['user']==username and request.session['is_logged_in']:
        if Author.objects.get(username=username).articles.filter(slugtitle=slugtitle).exists():
            a = Author.objects.get(username=username).articles.get(slugtitle=slugtitle)
            author = Author.objects.get(username=username)
            author.articles.remove(a)
            author.save()
            a.delete()
            articles = Author.objects.get(username=username).articles.all()
            return render(request, 'dashboard.html', {'data':request.session['user'], 'articles':articles, 'saved':0, 'deleted':1, 'edited':0})
        return redirect('/dashboard/'+username)
    return redirect('/')