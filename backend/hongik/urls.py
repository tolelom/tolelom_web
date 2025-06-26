from django.urls import path
from . import views


app_name = 'hongik'
urlpatterns = [
    path('', views.index, name='index'),
    path('editor/', views.editor, name='editor'),
    path('api/execute/batch/', views.execute_batch, name='execute_batch'),  # POST: 일괄 실행
    path('execute/interactive/', views.execute_interactive, name='execute_interactive'),
    path('docs/', views.docs, name='docs'),
]