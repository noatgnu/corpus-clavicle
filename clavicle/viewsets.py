import json

from django.contrib.postgres.search import SearchVector
from django.db.models import TextField
from django.db.models.functions import Cast
from rest_framework import viewsets, status, permissions
from rest_framework.decorators import action
from rest_framework.parsers import MultiPartParser, JSONParser
from rest_framework.response import Response
import pandas as pd
from clavicle.models import RawData, DifferentialAnalysis, SampleGroupAssignments
from clavicle.serializers import RawDataSerializer, DifferentialAnalysisSerializer
from clavicle.validations import raw_data_query_schema


class RawDataViewSets(viewsets.ModelViewSet):
    queryset = RawData.objects.all()
    serializer_class = RawDataSerializer
    permission_classes = (permissions.AllowAny,)
    parser_classes = (MultiPartParser, JSONParser)
    filter_mappings = {
        "name": "name__icontains",
        "data": "data__search"
    }
    filter_validation_schema = raw_data_query_schema

    def get_queryset(self):
        print(self.queryset)
        queryset = self.queryset
        start_date = self.request.query_params.get('start_date', None)
        end_date = self.request.query_params.get('end_date', None)
        text_search = self.request.query_params.get('text_search', None)
        value_cutoff = self.request.query_params.get('value_cutoff', None)

        if start_date is not None and end_date is not None:
            queryset = queryset.filter(date__range=[start_date, end_date])

        if text_search is not None:
            queryset = queryset.annotate(
                search=SearchVector(Cast('data', TextField()), 'name', 'description', Cast('metadata', TextField()))
            ).filter(search=text_search)

        return queryset

    def create(self, request, **kwargs):
        print(request.data)
        rawdata = RawData(
            name=request.data['name'],
            description=request.data['description'],
            index_col=request.data['index_col'],
            metadata=request.data['metadata'],
            file_type=request.data['file_type']
        )
        # read uploaded tabulated file into data jsonfield
        if request.data["file_type"] == "csv":
            df = pd.read_csv(request.data["file"])
        elif request.data["file_type"] == "tsv":
            df = pd.read_csv(request.data["file"], sep="\t")
        elif request.data["file_type"] == "txt":
            df = pd.read_csv(request.data["file"], sep="\t")
        else:
            return Response(status=status.HTTP_400_BAD_REQUEST)
        sample_assignments = SampleGroupAssignments.objects.create(sample_cols=json.loads(request.data["sample_cols"]))

        print(sample_assignments.sample_cols)
        melted = df.melt(id_vars=request.data['index_col'], value_vars=[i["name"] for i in sample_assignments.sample_cols], var_name="sample", value_name="value").fillna("")
        melted.rename(columns={request.data["index_col"]: "index"}, inplace=True)
        rawdata.value = melted.to_dict(orient="records")
        request.data["file"].seek(0)
        rawdata.data = request.data["file"].read().decode("utf-8")
        rawdata.save()
        sample_assignments.raw_data = rawdata
        sample_assignments.save()
        return Response(status=status.HTTP_201_CREATED)

    def update(self, request, pk=None, **kwargs):
        rawdata = self.get_object()
        rawdata.name = request.data['name']
        rawdata.description = request.data['description']
        rawdata.index_col = request.data['index_col']
        rawdata.metadata = request.data['metadata']
        rawdata.file_type = request.data['file_type']
        rawdata.save()
        return Response(status=status.HTTP_200_OK)

    def destroy(self, request, pk=None, **kwargs):
        rawdata = self.get_object()
        rawdata.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)

    @action(methods=["get"], detail=True, permission_classes=[permissions.AllowAny])
    def get_data(self, request, pk=None, **kwargs):
        rawdata = self.get_object()
        return Response(data=rawdata.data, status=status.HTTP_200_OK)


class DifferentialAnalysisViewSets(viewsets.ModelViewSet):
    queryset = DifferentialAnalysis.objects.all()
    serializer_class = DifferentialAnalysisSerializer
    permission_classes = (permissions.AllowAny,)

    def get_queryset(self):
        queryset = self.queryset
        start_date = self.request.query_params.get('start_date', None)
        end_date = self.request.query_params.get('end_date', None)
        if start_date is not None and end_date is not None:
            queryset = queryset.filter(date__range=[start_date, end_date])
        return queryset

    def create(self, request, **kwargs):
        diff = DifferentialAnalysis(name=request.data['name'], description=request.data['description'], data=request.data["file"], index_col=request.data['index_col'], fold_change_col=request.data['fold_change_col'], metadata=request.data['metadata'], file_type=request.data['file_type'])
        diff.save()
        return Response(status=status.HTTP_201_CREATED)

    def update(self, request, pk=None, **kwargs):
        diff = self.get_object()
        diff.name = request.data['name']
        diff.description = request.data['description']
        diff.index_col = request.data['index_col']
        diff.fold_change_col = request.data['fold_change_col']
        diff.metadata = request.data['metadata']
        diff.file_type = request.data['file_type']
        diff.save()
        return Response(status=status.HTTP_200_OK)

    def destroy(self, request, pk=None, **kwargs):
        diff = self.get_object()
        diff.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)

    @action(methods=["get"], detail=True, permission_classes=[permissions.AllowAny])
    def get_data(self, request, pk=None, **kwargs):
        rawdata = self.get_object()
        return Response(data=rawdata.data, status=status.HTTP_200_OK)
