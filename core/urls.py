from django.urls import path
from . import views

urlpatterns =[
    path('agreement/', views.AgreementListView.as_view()),
    path('agreement_details/<int:pk>/',views.AgreementDetailsView.as_view()),
    path('fund_agreement/<int:pk>/', views.FundAgreementView.as_view()),
    path('ledger_agreement/<int:pk>/', views.LedgerAgreementView.as_view()),
    path('milestone_agreement/<int:pk>/', views.MilestoneListView.as_view()),
    path("submit_milestone/<int:pk>/", views.SubmitMilestoneView.as_view()),
    path("approve_milestone/<int:pk>/", views.ApproveMilestoneView.as_view()),
    path("release_milestone/<int:pk>/", views.ReleaseMilestoneView.as_view()),
    path("audit_agreement/<int:pk>/", views.AuditAgreementView.as_view())
    
]