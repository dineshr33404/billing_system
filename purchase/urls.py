
from django.urls import path
from . import views

urlpatterns = [
    path('', views.billing, name='billing'),
    path('processBill', views.processBill, name='processBill'),
    path('final-call', views.finalBill, name='finalBill'),
    path('customer-history', views.customerHistory, name='customerHistory'),
    path('purchase-list', views.purchaseList, name='purchaseList'),
]
