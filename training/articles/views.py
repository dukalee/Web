from django.shortcuts import render, redirect, get_object_or_404
from .models import Article, Comment
from .forms import ArticleForm, CommentForm

# Create your views here.
# def list(request):
#     articles = Article.objects.all()

#     context = {
#         'articles': articles,
#     }
#     return render(request, "list.html", context)

def list(request):
    articles = Article.objects.all()
    context = {
        'articles': articles,
    }
    return render(request, "list.html", context)


def create(request):
    if request.user.is_authenticated:
        if request.method == "POST":
            form = ArticleForm(request.POST)
            if form.is_valid():
                article = form.save(commit=False)
                article.author = request.user
                article.save()
                return redirect("articles:list")
        else:
            form = ArticleForm()
        
        context = {
            'form': form,
        }
        return render(request, "create.html", context)
    return redirect("accounts:login")


def detail(request, pk):
    article = get_object_or_404(Article, pk=pk)
    comments = article.comment_set.all()
    form = CommentForm()

    context = {
        'comments': comments,
        'article': article,
        'form': form,
    }

    return render(request, "detail.html", context)


def delete(request, pk):
    article = get_object_or_404(Article, pk=pk)

    if request.user == article.author:
        article.delete()
        return redirect("articles:list")
    return redirect("articles:list")


def update(request, pk):
    article = get_object_or_404(Article, pk=pk)

    if request.user == article.author:
        if request.method == "POST":
            form = ArticleForm(request.POST, instance=article)
            if form.is_valid():
                tmp = form.save(commit=False)
                tmp.author = request.user
                tmp.save()
                return redirect("articles:detail", article.id)
        else:
            form = ArticleForm(instance=article)

        context = {
            'article': article,
            'form': form,
        }

        return render(request, "update.html", context)
    return redirect("articles:list")


def comment_create(request, pk):
    article = get_object_or_404(Article, pk=pk)

    form = CommentForm(request.POST)
    comment = form.save(commit=False)
    comment.article = article
    comment.author = request.user
    comment.save()

    return redirect("articles:detail", article.id)
    

def comment_delete(request, article_pk, comment_pk):
    article = get_object_or_404(Article, pk=article_pk)
    comment = get_object_or_404(Comment, pk=comment_pk)

    if comment.author == request.user or article.author == request.user:
        comment.delete()
    return redirect("articles:detail", article_pk)