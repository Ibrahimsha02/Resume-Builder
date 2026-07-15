from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('dashboard/', views.dashboard, name='dashboard'),
    path('resume/create/', views.create_resume, name='create_resume'),
    path('resume/<int:resume_id>/', views.resume_detail, name='resume_detail'),
    path('resume/<int:resume_id>/pdf/', views.resume_pdf, name='resume_pdf'),
    path('resume/<int:resume_id>/edit/', views.edit_resume, name='edit_resume'),
    path('resume/<int:resume_id>/delete/', views.delete_resume, name='delete_resume'),
    path('resume/start/<str:template_name>/', views.start_resume_with_template, name='start_resume_with_template'),
    path('samples/', views.sample_gallery, name='sample_gallery'),
    path('samples/<str:sample_key>/use/', views.use_sample_resume, name='use_sample_resume'),
]