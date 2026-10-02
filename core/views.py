from core.serializers import AgreementSerializer, EntrySerializer, MilestoneSerializer, AuditSerializer
from rest_framework imports generics

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