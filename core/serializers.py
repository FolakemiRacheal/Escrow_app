from rest_framework import serializers
from core.models import Agreement, Milestone, Entry, Audit


class AgreementSerializer(serializers.ModelSerializer):
    milestone = MilestoneSerializer(many=True)
    class Meta:
        model = Agreement
        fields= (
            "id",
            "client",
            "contractor",
            "amount",
            "description",
            "status",
            "milestones",
            "created_at"
        )
        read_only_fields =["id", "client", "status","created_at"]

    def validate_amount(self, value):
        if amount <= 0:
            raise seriailizer.ValidationError("amount can not be less than or equal=0")
        return amount

    def validate(self, attrs):
        if self.instance is None:  # only on create
            request = self.context["request"]
            if attrs["contractor"] == request.user:
                raise serializers.ValidationError("You cannot create an agreement with yourself.")

            milestones = attrs.get("milestones", [])
            if not milestones:
                raise serializers.ValidationError("An agreement needs at least one milestone.")

            total = sum(m["amount"] for m in milestones)
            if total != attrs["amount"]:
                raise serializers.ValidationError("Milestone amounts must add up to the agreement amount.")
        return attrs

    def create(self, validated_data):
        milestones_data = validated_data.pop("milestones")
        with transaction.atomic():
            agreement = Agreement.objects.create(**validated_data)
            for m in milestones_data:
                Milestone.objects.create(agreement=agreement, **m)
        return agreement    


class MilestoneSerializer(serializers.ModelSerializer):
    is_overdue = SerializerMethodField()
    class Meta:
        model = Milestone
        fields=(
            "id",
            "agreement",
            "title",
            "amount",
            "status",
            "due_date",
            "is_overdue",
        )
        read_only = ["id", "agreement", "status"]


class EntrySerializeer(serializers.modelsSerializers):
    class Meta:
        model = Entry
        fields = [
            "id",
            "type",
            "amount",
            "aggreement"
            
        ]
        read_only_fields = fields

class AuditSerializer(serializers.modelsSerialiser):
    action = serializer.StringRelatedField()
    class Meta:
        model = Audit
        fields = [
            "id",
            "agreement",
            "actor",
            "action"
            "timestamp",
        ]
        read_only = fields