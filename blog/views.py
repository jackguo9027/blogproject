from django.shortcuts import render
from django.http import HttpResponse
from django.shortcuts import get_object_or_404
from .models import Post,Category,Tag
import markdown
import re
from django.utils.text import slugify
from markdown.extensions.toc import TocExtension
from django.views.generic import ListView,DetailView
# Create your views here.

class IndexView(ListView):
    model=Post
    template_name='blog/index.html'
    context_object_name='post_list'

class PostDetailView(DetailView):
    model=Post
    template_name='blog/detail.html'
    context_object_name='post'

    def get(self,request,*args,**kwargs):
        response=super(PostDetailView,self).get(request,*args,**kwargs)
        self.object.increase_views()
        return response
    def get_object(self,queryset=None):
        post = super().get_object(queryset=None)
        md = markdown.Markdown(extensions=[
            'markdown.extensions.extra',
            'markdown.extensions.codehilite',
            # 记得在顶部引入 TocExtension 和 slugify
            TocExtension(slugify=slugify),
        ])
        post.body = md.convert(post.body)

        m = re.search(r'<div class="toc">\s*<ul>(.*)</ul>\s*</div>', md.toc, re.S)
        post.toc = m.group(1) if m is not None else ''

        return post
class ArchiveView(ListView):
    model=Post
    template_name='blog/index.html'
    context_object_name='post_list'

    def get_queryset(self):
        year=self.kwargs.get('year')
        month=self.kwargs.get('month')
        return super(ArchiveView,self).get_queryset().filter(created_time__year=year,created_time__month=month)


class CategoryView(ListView):
    model=Post
    template_name='blog/index.html'
    context_object_name='post_list'

    def get_queryset(self):
        cate=get_object_or_404(Category,pk=self.kwargs.get('pk'))
        return super(CategoryView,self).get_queryset().filter(category=cate)

class TagView(ListView):

    model=Tag
    template_name='blog/index.html'
    context_object_name='post_list'
    def get_queryset(self):
        t=get_object_or_404(Tag,pk=self.kwargs.get('pk'))
        return super(TagView,self).get_queryset().filter(tag=t)

# def tag(request,pk):
#     t=get_object_or_404(Tag,pk=pk)
#     post_list=Post.objects.filter(tags=t).order_by('-created_time')
#     return render(request,'blog/index.html',context={'post_list':post_list})