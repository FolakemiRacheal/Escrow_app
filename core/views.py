from core.serializers import AgreementSerializer, EntrySerializer, MilestoneSerializer, AuditSerializer
from rest_framework imports generics
from django.db.models import Q
from django.shortcuts import render, get_object_or_404
from rest_framwork import permissions
from res_framework.permissions import IsAuthenticated
from rest_framework,response import Response
from django.db import traansaction
from core.models import Agreement, Entry, Milestone, Audit, EntryType

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

    def get_queryset(self)
    user = self.request.user
    return Agreement.objects.filter(
        Q(client=user) | Q(contractor=user)
    )

class FundAgreementView(generics.CREATEAPIView):
    serializer_class = AgreementSerializer

    def get_queryset(self)
    user = self.request.user
    return Agreement.objects.filter(
        Q(client=user)| Q(contractor=user)
    )

    if request.user != agreement.client:
        return Response("Only Client can perform these action")

    def post(self, request, pk):
        user = self.get_object()

    with transaction.atomic():
    agreement = agreement.objects.select_update().get(pk=agreement.pk)

    if agreement.status != "pending":
        return Response("Agreement is not Pending")

        agreement.status = "Funded"
        agreement.save = (update_fields=[status])

        Entry.objects.Create(agreement=agreement, amount=agreement.amount,type=EntryType.Funding)
        Audit.objects.Create(agreement=agreement, actor=request.user, action="Agreement Funded" )

    return Response(AgreementSerializer(agreement).data status=200)


 class LedgerAgreementView(generics. ListAPIView):
        serializer_class = EntrySerializer
        permission_classes = [IsAuthenticated]

        def get_queryset(self):
            user = self.request.user
            agreement = get_object_or_404(Agreement, id=self.kwargs["agreement_id"])

            if user == agreement.client or user == agreement.contractor
            return Entry.objects.filter(agreement=agreement)





#GET	/api/agreements/{id}/milestones/	List milestones + status


class MilestoneListView(generics.ListAPIView):
    serializer_class = MilestoneSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        user = self.request.user
       agreement = get_object_or_404(
        Agreement.objects.filter(
            Q(client=user) | Q(contractor=user)), pk=self.kwargs["pk"])
        return Milestone.objects.filter(agreement=agreement)

       else:
         return Response("you are not permitted to view the List of Milestones") 





