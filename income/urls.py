from django.urls import path
from income import views

urlpatterns = [
    path('', views.index, name='income'),
    path('chart', views.chart, name='chart'),
    path('get_chart_data', views.get_chart_data, name='get_chart_data'),
    path('create_pdf', views.create_pdf, name='create_pdf'),
    path('import_excel', views.import_excel, name='import_excel'),
]



