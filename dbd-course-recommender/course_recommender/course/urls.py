from django.urls import path
from . import views


urlpatterns = [
    path('', views.home, name='course-home'),
    path('about/', views.about, name='course-about'),
    path('courses/', views.courses_list, name='course-courses'),
    path('categories/<int:domain_id>', views.DomainView, name='domain-view'),
    path('courses/<int:category_id>', views.CategoryView, name ='category-view'),
    #path('courses/<int: domain_id>/<int: category_id>', views.course_list, name='course_list_by_category')
    #path('courses/<int: domain_id>', views.course_list, name='course_list_by_domain')
    path('courses-cb/', views.courses_cb, name='course-cb'),
    path('courses-cf/', views.courses_cf, name='course-cf'),
    path('courses-single/<int:course_id>', views.course_single, name='courses-single'),
    path('course-enroll/<int:course_id>', views.course_enroll, name='course-enroll'),
    path('course-dismiss', views.course_dismiss, name='course-dismiss'),
    path('courseProgress/', views.course_progress, name='course-progress'),
    path('compare/', views.comparator, name='course-comparator'),
]