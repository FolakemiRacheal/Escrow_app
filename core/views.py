from core.serializers import AgreementSerializer, EntrySerializer, MilestoneSerializer, AuditSerializer
from rest_framework import generics
from django.db.models import Q
from django.shortcuts import render, get_object_or_404
from rest_framework import permissions
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from django.db import transaction
from core.models import Agreement, Entry, Milestone, Audit, Entry

def home(request):
    return render(request, "ums.html")


class AgreementListView(generics.ListCreateAPIView):
    serializer_class = AgreementSerializer

    def get_queryset(self):
        user = self.request.user

        return Agreement.objects.filter(
            Q(client=user)| Q(contractor=user)
        )

#GET	View one agreement's detail
class AgreementDetailsView (generics.RetrieveAPIView):
    serializer_class = AgreementSerializer

    def get_queryset(self):
        user = self.request.user
        return Agreement.objects.filter(
            Q(client=user) | Q(contractor=user)
        )

class FundAgreementView(generics.CreateAPIView):
    serializer_class = AgreementSerializer

    def get_queryset(self):
        user = self.request.user
        return Agreement.objects.filter(
            Q(client=user) | Q(contractor=user)
        )

    def post(self, request, pk):
        user = request.user

        agreement = self.get_object()

        if request.user != agreement.client:
            return Response("Only Client can perform these action")

        with transaction.atomic():
            agreement = Agreement.objects.select_for_update().get(pk=agreement.pk)

            if agreement.status != "pending":
                return Response("Agreement is not Pending")

            agreement.status = "Funded"
            agreement.save(update_fields=["status"])

            Entry.objects.create(agreement=agreement,amount=agreement.amount,type=EntryType.Funding)
            Audit.objects.create(agreement=agreement,actor=request.user,action="Agreement Funded")

            return Response(AgreementSerializer(agreement).data,status=200)

class LedgerAgreementView(generics. ListAPIView):
        serializer_class = EntrySerializer
        permission_classes = [IsAuthenticated]

        def get_queryset(self):
            user = self.request.user
            agreement = get_object_or_404(Agreement, id=self.kwargs["agreement_id"])

            if user == agreement.client or user == agreement.contractor:
                return Entry.objects.filter(agreement=agreement)
            else:
                return Response("You are not permitted to view the ledger for this agreement")



#GET	/api/agreements/{id}/milestones/	List milestones + status


class MilestoneListView(generics.ListAPIView):
    serializer_class = MilestoneSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        user = self.request.user
        agreement = get_object_or_404(
            Agreement.objects.filter(
                Q(client=user) | Q(contractor=user)
            ), pk=self.kwargs["pk"]
        )
        return Milestone.objects.filter(agreement=agreement)






