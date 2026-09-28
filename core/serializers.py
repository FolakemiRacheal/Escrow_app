from restframework import serializer
from core.models import Agreement, Milestone, Entry, Audit


class AgreementSerializer(serializers.ModelSerializier):
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
            


class MilestoneSerializer(serializers.modelsSerializer):
    is_overdue = SerializerMethodField()
    class Meta:
        model = Milestone
        fields=(
            "id",
            "agreement",
            "title",
            "amount",
            "status"
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
