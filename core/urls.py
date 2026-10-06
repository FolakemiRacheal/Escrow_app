from django.urls import path
from . import views

urlpatterns =[
    path('', views.home, name='homepage'),
    path('agreement/', views.AgreementListView.as_view()),
    path('agreement_details/<int:pk>/',views.AgreementDetailsView.as_view()),
    path('fund_agreement/', views.FundAgreementView.as_view()),
    path('ledger_agreement/<int:pk>/', views.LedgerAgreementView.as_view()),
    path('milestone_agreement/<int:pk>/', views.MilestoneListView.as_view())

]