from rest_framework import serializers

from clavicle.models import RawData


class RawDataSerializer(serializers.ModelSerializer):
    class Meta:
        model = RawData
        fields = ('id', 'name', 'description', 'index_col', 'data', 'metadata', 'created_at', 'updated_at', 'file_type')


class DifferentialAnalysisSerializer(serializers.ModelSerializer):
    class Meta:
        model = RawData
        fields = ('id', 'name', 'description', 'index_col', 'data', 'fold_change_col', 'metadata', 'created_at', 'updated_at', 'file_type')
