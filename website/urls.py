from django.urls import path
from .views import home, logout_user, register_user, customer_record, delete_record, add_record, update_record


urlpatterns = [
    path('', home, name='home'),
    path('logout/', logout_user, name='logout'),
    path('register/', register_user, name='register'),
    path('record/<int:id>/', customer_record, name='record'),
    path('record/delete/<int:id>/', delete_record, name='delete_record'),
    path('record/add/', add_record, name='add_record'),
    path('record/update/<int:id>/', update_record, name='update_record'),
]