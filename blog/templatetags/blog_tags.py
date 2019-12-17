# -*- coding:utf-8 -*-
__date__ = '18-6-8 上午9:11'

from django import template
from ..models import Post,Tag,Category,Carousel
from django.db.models.aggregates import Count
from django.db.models import Q

register = template.Library()

@register.simple_tag
def archives():
    return Post.objects.dates('created_time', 'month', order='DESC')

@register.simple_tag
def get_archives_count(year,month):
    return Post.objects.filter(Q(created_time__year=year,created_time__month=month),Q(topped=False)).count()

@register.simple_tag
def get_recent_posts(num=4):
    return Post.objects.filter(topped=False)[:num]

@register.simple_tag
def get_tags():
    return Tag.objects.annotate(post_nums = Count('post')).filter(post_nums__gt = 0)

@register.simple_tag
def get_categories():
    return  Category.objects.all()

@register.simple_tag
def get_carousel_list():
    return Carousel.objects.all()