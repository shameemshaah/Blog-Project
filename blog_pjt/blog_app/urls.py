from django.urls import path
from .import views
urlpatterns = [
    path("sample/", views.sample),
    path("Hi/", views.index),
    path("demo/", views.demo),
    path("demo2/", views.demo2),
    path("demo3/", views.demo3),
    path("demo4/", views.demo4),
    path("demo5/", views.demo5),

    #blog
    path('home/', views.home,name='home'),
    path('create_blog/',views.create_blog, name='create'),
    path('edit_blog/<int:id>/',views.edit_blog, name='edit'),
    path('delete_blog/<int:id>/',views.delete_blog,name='delete'),
    path('detail/<int:id>/',views.detail, name='detail'),


    #register
    path('register',views.register,name='register'),
    path('',views.login,name='login'),
    path('logout/',views.logout,name='logout'),


    path('comment_delete/<int:id>/',views.comment_delete,name='comment_delete'),
    path('comment_edit/<int:id>/',views.comment_edit,name='comment_edit'),


    path('forget_password/',views.forget_password,name='forget_password'),
    path('otp_verify/<int:id>/',views.otp_verify,name='otp_verify'),
    path('password_reset/<int:id>/',views.password_reset,name='password_reset'),
    

    path('forms/create_new/',views.create_new,name='create_new'),
    path('forms/edit_new/<int:id>/',views.edit_new,name='edit_new'),

    path('admin_home/',views.admin_home,name='admin_home'),
    path('change_status/<int:id>/',views.change_status,name='change_status'),

]

