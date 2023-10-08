from django.db import models
from psqlextra.models import PostgresPartitionedModel
from psqlextra.types import PostgresPartitioningMethod


class DifferentialAnalysis(PostgresPartitionedModel):
    """
    A Model to store differential analysis tables as textfield
    """
    name = models.TextField(max_length=100)
    description = models.TextField(blank=True, null=True)
    data = models.JSONField(blank=True, null=True)
    index_col = models.TextField(blank=True, null=True)
    fold_change_col = models.TextField(blank=True, null=True)
    metadata = models.JSONField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    file_type_choices = [
        ("csv", "csv"),
        ("tsv", "tsv"),
        ("txt", "tabulated text"),
        ("txt", "space separated text"),
    ]
    file_type = models.CharField(max_length=3, choices=file_type_choices, default="tsv")

    class PartitioningMeta:
        method = PostgresPartitioningMethod.RANGE
        key = ["id"]
        ordering = ["id"]
        app_label = "clavicle"
        using = "clavicle"

    def __str__(self):
        return f"{self.name} {self.created_at} {self.description}"

    def __repr__(self):
        return f"{self.name} {self.created_at}"


class RawData(PostgresPartitionedModel):
    """
    A Model to store raw data tables as textfield
    """
    name = models.TextField(max_length=100)
    description = models.TextField(blank=True, null=True)
    data = models.TextField(blank=True, null=True)
    index_col = models.TextField(blank=True, null=True)
    sample_cols = models.JSONField(blank=True, null=True)
    metadata = models.JSONField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    value = models.JSONField(blank=True, null=True)

    file_type_choices = [
        ("csv", "csv"),
        ("tsv", "tsv"),
        ("txt", "tabulated text"),
        ("txt", "space separated text"),
    ]
    file_type = models.CharField(max_length=3, choices=file_type_choices, default="tsv")


    class PartitioningMeta:
        method = PostgresPartitioningMethod.RANGE
        key = ["id"]
        ordering = ["id"]
        app_label = "clavicle"
        using = "clavicle"

    def __str__(self):
        return f"{self.name} {self.created_at} {self.description}"

    def __repr__(self):
        return f"{self.name} {self.created_at}"