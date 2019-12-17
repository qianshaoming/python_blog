from django.shortcuts import render

# Create your views here.
from .models import Post,Tag,Category,Link,Cooperator
from django.views.generic.base import View
from pure_pagination import Paginator, EmptyPage, PageNotAnInteger
from django.shortcuts import render,get_object_or_404,redirect
from comments.forms import CommentForm
from django.db.models import Q
import markdown
import pygments


class IndexView(View):
    def get(self,request):
        links = Link.objects.all()
        cooperators = Cooperator.objects.all()
        topped_posts = Post.objects.filter(topped=True)

        all_post = Post.objects.filter(topped=False)

        # 对文章进行分页
        try:
            page = request.GET.get('page', 1)
        except PageNotAnInteger:
            page = 1

        # Provide Paginator with the request object for complete querystring generation
        p = Paginator(all_post, 2, request=request)
        posts = p.page(page)
        return render(request,'blog/index.html',{
            "posts":posts,
            "links":links,
            "cooperators": cooperators,
            "topped_posts":topped_posts,
        })

class TagView(View):
    def get(self,request,pk):
        links = Link.objects.all()
        cooperators = Cooperator.objects.all()
        tags = get_object_or_404(Tag,pk=pk)
        all_post = Post.objects.filter(Q(tags=tags),Q(topped=False))

        # 对文章进行分页
        try:
            page = request.GET.get('page', 1)
        except PageNotAnInteger:
            page = 1

        # Provide Paginator with the request object for complete querystring generation
        p = Paginator(all_post, 2, request=request)
        posts = p.page(page)

        return render(request, 'blog/tag.html', {
            "posts": posts,
            "tags":tags,
            "links": links,
            "cooperators": cooperators,
        })


class CategoryView(View):
    def get(self,request,pk):
        links = Link.objects.all()
        cooperators = Cooperator.objects.all()
        categories = get_object_or_404(Category,pk=pk)
        all_post = Post.objects.filter(Q(category=categories),Q(topped=False))

        # 对文章进行分页
        try:
            page = request.GET.get('page', 1)
        except PageNotAnInteger:
            page = 1

        # Provide Paginator with the request object for complete querystring generation
        p = Paginator(all_post, 2, request=request)
        posts = p.page(page)

        return render(request, 'blog/category.html', {
            "posts": posts,
            "categories":categories,
            "links":links,
            "cooperators": cooperators,
        })



class ArchiveView(View):
    def get(self,request,year,month):
        links = Link.objects.all()
        cooperators = Cooperator.objects.all()
        all_post = Post.objects.filter(Q(created_time__year=year,created_time__month=month),Q(topped=False))

        # 对文章进行分页
        try:
            page = request.GET.get('page', 1)
        except PageNotAnInteger:
            page = 1

        # Provide Paginator with the request object for complete querystring generation
        p = Paginator(all_post, 2, request=request)
        posts = p.page(page)

        return render(request, 'blog/archive.html', {
            "posts": posts,
            "links":links,
            "cooperators": cooperators,
        })


class PostView(View):
    def get(self,request,pk):
        links = Link.objects.all()
        cooperators = Cooperator.objects.all()
        post = get_object_or_404(Post,pk=pk)
        post.increase_views()
        comments = post.comment_set.all()
        # 评论表单
        form = CommentForm()

        #markdown引入
        md = markdown.Markdown(extensions=[
            'markdown.extensions.extra',
            'markdown.extensions.codehilite',
            # 'markdown.extensions.toc',
        ])
        post.content = md.convert(post.content)
        # post.toc = md.toc

        return render(request, 'blog/detail.html',
                      {
            "post":post,
            "form":form,
            "comments":comments,
            "links": links,
            "cooperators": cooperators,
        }
        #               locals()
                      )


class SearchView(View):
    def get(self, request):
        links = Link.objects.all()
        cooperators = Cooperator.objects.all()
        keyword = request.GET.get('keyword',None)
        if not keyword:
            error_msg = "请输入关键字!"
            return render(request,"blog/search.html",locals())
        all_post = Post.objects.filter(Q(title__icontains=keyword)|Q(content__contains=keyword)|Q(excerpt__contains=keyword),Q(topped=False))

        # 对文章进行分页
        try:
            page = request.GET.get('page', 1)
        except PageNotAnInteger:
            page = 1

        # Provide Paginator with the request object for complete querystring generation
        p = Paginator(all_post, 2, request=request)
        posts = p.page(page)

        return render(request, 'blog/search.html', {
            "posts": posts,
            "links": links,
            "cooperators":cooperators,
        })


def permission_denied(request):
    links = Link.objects.all()
    cooperators = Cooperator.objects.all()
    return render(request,'blog/403.html',locals())

def page_not_found(request):
    links = Link.objects.all()
    cooperators = Cooperator.objects.all()
    return render(request,'blog/404.html',locals())

def page_error(request):
    links = Link.objects.all()
    cooperators = Cooperator.objects.all()
    return render(request,'blog/500.html',locals())