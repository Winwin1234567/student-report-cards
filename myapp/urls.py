from django.urls import path
from . import views

urlpatterns = [
    # Report Card
    path('report-card/', views.report_card, name='report_card'),

    # Student CRUD
    path('students/', views.student_list, name='student_list'),
    path('students/create/', views.student_add, name='student_create'),
    path('students/<int:pk>/update/', views.student_edit, name='student_update'),
    path('students/<int:pk>/delete/', views.student_delete, name='student_delete'),

    # Subject CRUD
    path('subjects/', views.subject_list, name='subject_list'),
    path('subjects/create/', views.subject_create, name='subject_create'),
    path('subjects/<int:pk>/update/', views.subject_update, name='subject_update'),
    path('subjects/<int:pk>/delete/', views.subject_delete, name='subject_delete'),

    # Marks CRUD
    path("marks/", views.mark_list, name="mark_list"),          
    path("marks/create/", views.mark_create, name="mark_create"),
    path("marks/<int:pk>/update/", views.mark_update, name="mark_update"),
    path("marks/<int:pk>/delete/", views.mark_delete, name="mark_delete"),

    # Combined Student + Mark creation
    path("students/add-with-marks/", views.student_mark_add, name="student_mark_add"),

     path("chatbot/", views.chatbot_api, name="chatbot_api"),
]
