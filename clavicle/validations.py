import six
from filters.schema import base_query_params_schema
from filters.validations import IntegerLike

raw_data_query_schema = base_query_params_schema.extend(
    {
        "id": IntegerLike(),
        "name": six.text_type,
        "description": six.text_type,
        "index_col": six.text_type,
        "data": six.text_type,
        "metadata": six.text_type,
        "created_at": six.text_type,
        "updated_at": six.text_type,
        "file_type": six.text_type,
    }
)

differential_analysis_query_schema = base_query_params_schema.extend(
    {
        "id": IntegerLike(),
        "name": six.text_type,
        "description": six.text_type,
        "index_col": six.text_type,
        "fold_change_col": six.text_type,
        "data": six.text_type,
        "metadata": six.text_type,
        "created_at": six.text_type,
        "updated_at": six.text_type,
        "file_type": six.text_type,
    }
)