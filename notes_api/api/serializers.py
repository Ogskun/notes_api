from rest_framework import serializers

from core.models import Note


class NoteSerializer(serializers.ModelSerializer):
    class Meta:
        model = Note
        exclude = [
            'is_deleted', 
            'user',
        ]