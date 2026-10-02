from django.urls import path
from . import views

urlpatterns =[
    path('', views.home, name='homepage'),
    path('agreement/', views.AgreementList.as_view()),
    path('agreement_details/<int:pk>/',views.AgreementDetailView.as_view()),
    path('fund_agreement/', views.FundAgreementView.as_View())
]