import random

from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.core.paginator import Paginator
from django.http import HttpResponse, JsonResponse
from django.shortcuts import get_object_or_404, redirect, render
from django.views.decorators.cache import cache_page
from django.views.decorators.vary import vary_on_cookie

from users.models import Student

from .cfService import get_recommmendations_cf
from .forms import CourseDismissForm, CourseEnrollForm, CommentForm
from .models import *
from .services import get_enrolled_subjects, get_recommmendations


def home(request):
    domains = Domain.objects.all()
    courses = Course.objects.all().order_by('name')[:3]
    context = {'home_page': 'active',
               'domains' : domains ,
               'courses': courses,
               }
    return render(request, 'index.html', context)


def about(request):
    domains = Domain.objects.all()
    courses = Course.objects.all().order_by('name')[:5]
    context = {'home_page': 'active',
               'domains' : domains ,
               'courses': courses,
               }
    return render(request, 'index.html', context)


def courses_list(request):
    filter_str = request.POST.get('filter_str', '').strip()
    if len(filter_str) == 0:
        filter_str = request.GET.get('filter_str', '').strip()
    course_list = []
    if len(filter_str) == 0:
        course_list = list(Course.objects.all())
        base_url = '?page='

    else:
        course_list = list(Course.objects.filter(
            name__icontains=filter_str))
        base_url = '?filter_str=' + filter_str + '&page='

    #Pagination
    paginator = Paginator(course_list, 6)
    page = request.GET.get('page')
    courses = paginator.get_page(page)

    context = {
        'courses_page': 'active',
        'courses': courses,
        'courses_size': course_list.__len__,
        'base_url': base_url,
        'filter_str': filter_str
    }
    return render(request, 'courses-list.html', context)


@cache_page(60 * 15)
@vary_on_cookie
@login_required
def courses_cb(request):
    #get content-based filtering list
    subs = get_enrolled_subjects(request.user.id)
    if len(subs) == 0:
        recommmend_list = list(Course.objects.all())
    else:
        l1=[]
        cats=[sub.course.category for sub in subs]
        for cat in cats:
            l1 += list(Course.objects.filter(category = cat))
            l1=list(set(l1))
        l2=[]
        for sub in subs:
            l2 +=list(Course.objects.filter(instructor = sub.course.instructor))
            l2 +=list(Course.objects.filter(cost = sub.course.cost))
            l2 +=list(Course.objects.filter(platform = sub.course.platform))
            l2 +=list(Course.objects.filter(language = sub.course.language))
            l2 +=list(Course.objects.filter(level = sub.course.level))
            l2 +=list(Course.objects.filter(certificate = sub.course.certificate))
            l2=list(set(l2))
        recommmend_list = list(set(l1+l2))

    paginator = Paginator(recommmend_list, 6)
    page = request.GET.get('page')
    courses = paginator.get_page(page)

    context = {
        'courses_page': 'active',
        'courses': courses,
        'courses_size': recommmend_list.__len__
    }
    return render(request, 'courses-cb.html', context)


@cache_page(60 * 15)
@vary_on_cookie
@login_required
def courses_cf(request):
    #get content-based filtering list
    subs = get_enrolled_subjects(request.user.id)
    if len(subs) == 0:
        recommmend_list = random.choices(list(Course.objects.all()), k=min(len(list(Course.objects.all())),10))
    else:
        l1=[]
        cats=[sub.course.category for sub in subs]
        for cat in cats:
            l1 += list(Course.objects.filter(category = cat))
            l1=list(set(l1))
        l2=[]
        for sub in subs:
            l2 +=list(Course.objects.filter(instructor = sub.course.instructor))
            l2 +=list(Course.objects.filter(cost = sub.cost))
            l2 +=list(Course.objects.filter(platform = sub.course.platform))
            l2 +=list(Course.objects.filter(language = sub.course.language))
            l2 +=list(Course.objects.filter(level = sub.course.level))
            l2=list(set(l2))
        recommmend_list = random.choices(list(set(l1+l2)), k=min(len(list(set(l1+l2))),10))

    #Pagination
    paginator = Paginator(recommmend_list, 6)
    page = request.GET.get('page')
    courses = paginator.get_page(page)

    context = {
        'courses_page': 'active',
        'courses': courses,
        'courses_size': recommmend_list.__len__
    }
    return render(request, 'courses-cf.html', context)


def course_single(request, course_id):
    course = get_object_or_404(Course, pk=course_id)
    reviews = SubjectRating.objects.filter(subject = course)
    if request.method == 'POST':
        if request.user.is_authenticated:
            current_student = Student.objects.get(account=request.user.id)
            form = CommentForm(request.POST)
            if form.is_valid():
                comment = SubjectRating(
                    subject = course,
                    student = current_student,
                    comment=form.cleaned_data["comment"],
                    rating =int(form.cleaned_data["rating"]),
                    )
                comment.save()
                messages.success(request, 'review posted')
            else:
                messages.error(request, form.errors)
        else:
            return redirect('/login')
    form = CommentForm()

    #check if enrolled this subject if user has logged in
    is_enrolled = False
    if request.user.is_authenticated:  #atuthenticated user
        enrolled_course_list = get_enrolled_subjects(request.user.id)
        if course in enrolled_course_list:
            is_enrolled = True
    l1 = list(Course.objects.filter(category = course.category))
    l2 =list(Course.objects.filter(instructor = course.instructor))
    l3 =list(Course.objects.filter(cost = course.cost))
    l4 =list(Course.objects.filter(platform = course.platform))
    l4 +=list(Course.objects.filter(language = course.language))
    l4 +=list(Course.objects.filter(level = course.level))
    recommmend_list =list(set(l1+l2+l4+l3))
    random_items = [recommmend_list[random.randrange(len(recommmend_list))]
                    for item in range(2)]
    context = {
        'courses_page': 'active',
        'course': course,
        'recommended_courses': random_items,
        'is_enrolled': is_enrolled,
        'reviews' : reviews,
        'form' : form,
    }
    return render(request, 'courses-single.html', context)


@login_required
def course_enroll(request,course_id):
    """
    1. Enrolling course
    2. Refreshing recommendation course list by deleting request.session['recommmend_list']
    3. Message either success or error
    """
    if request.method == 'POST':
        current_student = Student.objects.get(account=request.user.id)
        form = CourseEnrollForm(request.POST)
        if form.is_valid():
            e = Enrollment(
                    course = get_object_or_404(Course, pk=course_id),
                    student = current_student,
                    status=1,
                    )
            e.save()
            #_refresh_session(request)
            messages.success(request, 'You have enrolled the subject.')
        else:
            messages.error(request, form.errors)

    return redirect('course-progress')


@login_required
def course_dismiss(request):
    """
    1. Dismissing course
    2. Refreshing recommendation course list by deleting request.session['recommmend_list']
    3. Message either success or error
    """
    if request.method == 'POST':
        current_student = Student.objects.get(account=request.user.id)
        form = CourseDismissForm(request.POST)
        if form.is_valid():
            e = Enrollment.objects.filter(
                course=form.instance.course, student=current_student)
            e.delete()
            #_refresh_session(request)
            messages.success(request, 'You have dismissed the subject.')
        else:
            messages.error(request, form.errors)

    return redirect('course-progress')


def _refresh_session(request):
    del request.session['recommmend_list']
    del request.session['recommmend_cf_list']


@login_required
def course_progress(request):
    subs = get_enrolled_subjects(request.user.id)
    """
    Display 
    1. content-based filtering recommmended course list
    2. collaborative filtering recommmended course list
    2. enrolled course list
    """
    #get cb list
    if len(subs) == 0:
        recommmend_list = list(Course.objects.all())[:min(len(list(Course.objects.all())),4)]
    else:
        l1=[]
        cats=[sub.course.category for sub in subs]
        for cat in cats:
            l1 += list(Course.objects.filter(category = cat))
            l1=list(set(l1))
        l2=[]
        for sub in subs:
            l2 +=list(Course.objects.filter(instructor = sub.course.instructor))
            l2 +=list(Course.objects.filter(cost = sub.course.cost))
            l2 +=list(Course.objects.filter(platform = sub.course.platform))
            l2 +=list(Course.objects.filter(language = sub.course.language))
            l2 +=list(Course.objects.filter(level = sub.course.level))
            l2 +=list(Course.objects.filter(certificate = sub.course.certificate))
            l2=list(set(l2))
        recommmend_list = list(set(l1+l2))[:min(len(list(set(l1+l2))),4)]
    #get collaborative filtering list
    if len(subs) == 0:
        recommmend_cf_list = random.choices(list(Course.objects.all()), k=min(len(list(Course.objects.all())),4))
    else:
        l1=[]
        cats=[sub.course.category for sub in subs]
        for cat in cats:
            l1 += list(Course.objects.filter(category = cat))
            l1=list(set(l1))
        l2=[]
        for sub in subs:
            l2 +=list(Course.objects.filter(instructor = sub.course.instructor))
            #l2 +=list(Course.objects.filter(cost = sub.cost))
            l2 +=list(Course.objects.filter(platform = sub.course.platform))
            l2 +=list(Course.objects.filter(language = sub.course.language))
            l2 +=list(Course.objects.filter(level = sub.course.level))
            l2=list(set(l2))
        recommmend_cf_list = random.choices(list(set(l1+l2)), k=min(len(list(set(l1+l2))),4))

    #get enrolled subject list
    enrolled_course_list = get_enrolled_subjects(request.user.id)
    enrolled_course0 = []
    enrolled_course1 = []
    remain_course_list = []
    has_enrolled_course0 = False
    has_enrolled_course1 = False
    has_enrolled_course_remain = False
    has_more = False
    list_size = len(enrolled_course_list)
    if list_size > 0:
        enrolled_course0 = enrolled_course_list[0]
        has_enrolled_course0 = True
    if list_size > 1:
        enrolled_course1 = enrolled_course_list[1]
        has_enrolled_course1 = True
    if list_size > 2:
        remain_course_list = enrolled_course_list[2:None]
        remain_course_list = remain_course_list[0:7]
        has_enrolled_course_remain = True
    if list_size > 9:  #show more option
        has_more = True

    context = {
        'courses_progress_page': 'active',
        'recommended_courses_cb': recommmend_list,
        'recommended_courses_cf': recommmend_cf_list,
        'enrolled_course0': enrolled_course0,
        'enrolled_course1': enrolled_course1,
        'remain_course_list': remain_course_list,
        'has_enrolled_course0': has_enrolled_course0,
        'has_enrolled_course1': has_enrolled_course1,
        'has_enrolled_course_remain': has_enrolled_course_remain,
        'has_more': has_more
    }
    return render(request, 'courses-progress.html', context)

def DomainView(request, domain_id):
    domain= get_object_or_404(Domain, pk=domain_id)
    filter_str = request.POST.get('filter_str', '').strip()
    if len(filter_str) == 0:
        filter_str = request.GET.get('filter_str', '').strip()
    category_list = []
    if len(filter_str) == 0:
        category_list = list(Category.objects.filter(domain = domain))
        base_url = '?page='

    else:
        category_list = list(Category.objects.filter( domain=domain,
            name__icontains=filter_str))
        base_url = '?filter_str=' + filter_str + '&page='

    #Pagination
    paginator = Paginator(category_list, 6)
    page = request.GET.get('page')
    categories = paginator.get_page(page)
    context = {
        'domain':domain,
        'category_page': 'active',
        'categories': categories,
        'categories_size': category_list.__len__,
        'base_url': base_url,
        'filter_str': filter_str
    }
    return render(request, 'domain-view.html',context)

def CategoryView(request, category_id):
    category= get_object_or_404(Category, pk=category_id)
    filter_str = request.POST.get('filter_str', '').strip()
    if len(filter_str) == 0:
        filter_str = request.GET.get('filter_str', '').strip()
    category_list = []
    if len(filter_str) == 0:
        course_list = list(Course.objects.filter(category = category))
        base_url = '?page='

    else:
        course_list = list(Course.objects.filter( category=category,
            name__icontains=filter_str))
        base_url = '?filter_str=' + filter_str + '&page='

    #Pagination
    paginator = Paginator(course_list, 6)
    page = request.GET.get('page')
    courses = paginator.get_page(page)
    context = {
        'category':category,
        'course_page': 'active',
        'courses': courses,
        'courses_size': course_list.__len__,
        'base_url': base_url,
        'filter_str': filter_str
    }
    return render(request, 'category-view.html',context)
@login_required
def comparator(request):
    if request.method =='POST':
        course_id1 = request.POST.get('course1')
        course_id2 = request.POST.get('course2')
        course1 = get_object_or_404(Course, pk=course_id1)
        course2 = get_object_or_404(Course, pk=course_id2)
        context = {
            'courses_page': 'active',
            'course1': course1,
            'course2': course2,
        }
        return render(request, 'comparator-result.html',context)
    
    courses = list(Course.objects.all())
    context = {
        'courses_page': 'active',
        'courses': courses,
        'courses_size': courses.__len__
    }
    return render(request, 'comparator.html', context)
