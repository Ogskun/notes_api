from rest_framework import serializers

from core.models import Note


class NoteSerializer(serializers.ModelSerializer):
    date_created = serializers.DateField(
        read_only=True,
        format='%m-%d-%Y'
    )

    class Meta:
        model = Note
        exclude = [
            'is_deleted', 
            'user',
        ]