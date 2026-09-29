from django.shortcuts import render
from core.serializers import AgreementSerializer, EntrySerializer
from rest_framework import generics

# Create your views here.
def home(request):
    return render(request, 'ums/home.html')

class AgreementList(generics.ListCreateAPIView):
    serializer_class = AgreementSerializer

    def get_queryset(self):
        user = self.request.user
        return Agreement.objects.filter(
            Q(client=user) | Q(contractor=user)
        )


class AgreementDetailView(generics.RetrieveAPIView):
    queryset = Agreement.objects.all()
    serializer_class = AgreementSerializer



#POST	/api/agreements/{id}/fund/	Fund the agreement (simulated)
class FundAgreementView(generics.CreateAPIView):
    serializer_class = AgreementSerializer

    def get_queryset(self)
    user = self.request.user

    if request.user != user.client:
        return serializer.ValidationError("you dont have the right to perform these action")

    else:
        return     
