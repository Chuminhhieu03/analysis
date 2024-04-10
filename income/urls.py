from django.urls import path
from income import views

urlpatterns = [
    path('', views.index, name='income'),
    path('analyze', views.chart, name='analyze_income'),
    path('get_chart_data', views.get_chart_data, name='get_chart_data'),
    path('create_pdf', views.create_pdf, name='create_pdf'),
    path('import_excel', views.import_excel, name='import_excel'),
    path('add', views.add, name='add_income'),
    path('edit/<int:id>', views.edit, name='edit_income'),
    path('delete/<int:id>', views.delete, name='delete_income'),
]



