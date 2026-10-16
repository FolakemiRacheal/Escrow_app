from django.db import transaction
from django.db.models import Q
from django.shortcuts import get_object_or_404
from rest_framework import generics, status
from rest_framework.response import Response

from core.models import Agreement, Audit, Entry, Milestone
from core.serializers import AgreementSerializer, EntrySerializer, MilestoneSerializer, AuditSerializer

class HomeView(generics.GenericAPIView):
    def get(self, request):
        return Response({"message": "Welcome to the Escrow API!"})


# POST    -> create an agreement (you become the client)
# GET   -> list the agreements you are part of
class AgreementListView(generics.ListCreateAPIView):
    serializer_class = AgreementSerializer

    def get_queryset(self):
        user = self.request.user
        return Agreement.objects.filter(Q(client=user) | Q(contractor=user))

    def perform_create(self, serializer):
        agreement = serializer.save(client=self.request.user)
        Audit.objects.create(
            agreement=agreement, actor=self.request.user, action="Agreement created"
        )


# GET  -> one agreement's detail
class AgreementDetailsView(generics.RetrieveAPIView):
    serializer_class = AgreementSerializer

    def get_queryset(self):
        user = self.request.user
        return Agreement.objects.filter(Q(client=user) | Q(contractor=user))


# POST-> the client funds the agreement
class FundAgreementView(generics.GenericAPIView):
    serializer_class = AgreementSerializer

    def get_queryset(self):
        user = self.request.user
        return Agreement.objects.filter(Q(client=user) | Q(contractor=user))

    def post(self, request, pk):
        agreement = self.get_object()

        if request.user != agreement.client:
            return Response(
                {"detail": "Only the client can fund this agreement."},
                status=status.HTTP_403_FORBIDDEN,
            )

        with transaction.atomic():
            agreement = Agreement.objects.select_for_update().get(pk=agreement.pk)

            if agreement.status != Agreement.Status.PENDING:
                return Response(
                    {"detail": "Agreement is not pending."},
                    status=status.HTTP_400_BAD_REQUEST,
                )

            agreement.status = Agreement.Status.FUNDED
            agreement.save(update_fields=["status"])

            Entry.objects.create(
                agreement=agreement,
                amount=agreement.amount,
                type=Entry.EntryType.FUNDING,
            )
            Audit.objects.create(
                agreement=agreement, actor=request.user, action="Agreement funded"
            )

        return Response(self.get_serializer(agreement).data, status=status.HTTP_200_OK)


# GET -> the money history of one agreement
class LedgerAgreementView(generics.ListAPIView):
    serializer_class = EntrySerializer

    def get_queryset(self):
        user = self.request.user
        agreement = get_object_or_404(
            Agreement.objects.filter(Q(client=user) | Q(contractor=user)),
            pk=self.kwargs["pk"],
        )
        return Entry.objects.filter(agreement=agreement).order_by("timestamp")


# GET -> the milestones of one agreement
class MilestoneListView(generics.ListAPIView):
    serializer_class = MilestoneSerializer

    def get_queryset(self):
        user = self.request.user
        agreement = get_object_or_404(
            Agreement.objects.filter(Q(client=user) | Q(contractor=user)),
            pk=self.kwargs["pk"],
        )
        return Milestone.objects.filter(agreement=agreement)



#GET /core/audit_agreement/<pk>/submit_milestone, approve_milestone release_milestone
class AuditAgreementView(generics.ListAPIView):
    serializer_class = AuditSerializer

    def get_queryset(self):
        user = self.request.user
        agreement = get_object_or_404(
            Agreement.objects.filter(Q(contractor=user) |Q(client=user)),
            pk=self.kwargs["pk"]
        )
        return Audit.objects.filter(agreement=agreement).order_by("timestamp")


class SubmitMilestoneView(generics.GenericAPIView):
    serializer_class = MilestoneSerializer

    def post(self, request, pk):
        user = request.user
        agreement = get_object_or_404(
            Agreement.objects.filter(Q(contractor=user) | Q(client=user)),
            pk=pk
        )
        if user != agreement.contractor:
            return Response(
                {"detail": "Only the contractor can submit a milestone."},
                status=status.HTTP_403_FORBIDDEN,
            )
        milestone_id = request.data.get("milestone_id")
        milestone = get_object_or_404(Milestone, id=milestone_id, agreement=agreement)
        if milestone.status != Milestone.Status.PENDING:
            return Response(
                {"detail": "Milestone is not pending."},
                status=status.HTTP_400_BAD_REQUEST,
            )
        milestone.status = Milestone.Status.SUBMITTED
        milestone.save(update_fields=["status"])
        Audit.objects.create(
            agreement=agreement,
            actor=request.user,
            action=f"Milestone {milestone.id} submitted"
        )
        return Response({"detail": "Milestone submitted successfully."}, status=status.HTTP_200_OK)

class ApproveMilestoneView(generics.GenericAPIView):
    serializer_class = MilestoneSerializer

    def post(self, request, pk):
        user = request.user
        agreement = get_object_or_404(
            Agreement.objects.filter(Q(contractor=user) | Q(client=user)),
            pk=pk
        )
        if user != agreement.client:
            return Response(
                {"detail": "Only the client can approve a milestone."},
                status=status.HTTP_403_FORBIDDEN,
            )
        milestone_id = request.data.get("milestone_id")
        milestone = get_object_or_404(Milestone, id=milestone_id, agreement=agreement)
        if milestone.status != Milestone.Status.SUBMITTED:
            return Response(
                {"detail": "Milestone is not submitted."},
                status=status.HTTP_400_BAD_REQUEST,
            )
        milestone.status = Milestone.Status.APPROVED
        milestone.save(update_fields=["status"])
        Audit.objects.create(
            agreement=agreement,
            actor=request.user,
            action=f"Milestone {milestone.id} approved"
        )
        return Response({"detail": "Milestone approved successfully."}, status=status.HTTP_200_OK)


class ReleaseMilestoneView(generics.GenericAPIView):
    serializer_class = MilestoneSerializer

    def post(self, request, pk):
        user = request.user
        agreement = get_object_or_404(
            Agreement.objects.filter(Q(contractor=user) | Q(client=user)),
            pk=pk
        )
        if user != agreement.client:
            return Response(
                {"detail": "Only the client can release a milestone."},
                status=status.HTTP_403_FORBIDDEN,
            )
        milestone_id = request.data.get("milestone_id")
        milestone = get_object_or_404(Milestone, id=milestone_id, agreement=agreement)
        if milestone.status != Milestone.Status.APPROVED:
            return Response(
                {"detail": "Milestone is not approved."},
                status=status.HTTP_400_BAD_REQUEST,
            )
        milestone.status = Milestone.Status.RELEASED
        milestone.save(update_fields=["status"])
        Entry.objects.create(
            agreement=agreement,
            amount=milestone.amount,
            type=Entry.EntryType.MILESTONE_RELEASE,
        )
        Audit.objects.create(
            agreement=agreement,
            actor=request.user,
            action=f"Milestone {milestone.id} released"
        )
        return Response({"detail": "Milestone released successfully."}, status=status.HTTP_200_OK)




class sumaryView(generics.GenericAPIView):
    def get(self, request):
        user = request.user
        agreements = Agreement.objects.filter(Q(client=user) | Q(contractor=user))
        total_funded = sum(
            Entry.objects.filter(agreement=agreement, type=Entry.EntryType.FUNDING).aggregate(total=models.Sum('amount'))['total'] or 0
            for agreement in agreements
        )
        total_released = sum(
            Entry.objects.filter(agreement=agreement, type=Entry.EntryType.MILESTONE_RELEASE).aggregate(total=models.Sum('amount'))['total'] or 0
            for agreement in agreements
        )
        return Response({
            "total_funded": total_funded,
            "total_released": total_released,
        })        