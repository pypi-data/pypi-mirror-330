from datetime import datetime

import pandas as pd
import pandera as pa
from pandera import Bool
from pandera.typing import Series, String, Float, DateTime
import pandera.extensions as extensions
from brynq_sdk_functions import BrynQPanderaDataFrameModel


class FunctionSchema(BrynQPanderaDataFrameModel):
    employee_id: Series[pa.String] = pa.Field(coerce=True)  # UUID as string
    function_id: Series[pa.String] = pa.Field(coerce=True)  # UUID as string
    code: Series[pd.Int64Dtype] = pa.Field(coerce=True)
    description: Series[pa.String] = pa.Field(coerce=True)
    created_at: Series[datetime] = pa.Field(coerce=True)  # datetime format enforced
    period_period: Series[pd.Int64Dtype] = pa.Field(coerce=True)  # integer period value
    period_year: Series[pd.Int64Dtype] = pa.Field(coerce=True)  # required year as integer

    class Annotation: 
        primary_key = "function_id" 
        foreign_keys = {
            "employee_id": {
                "parent_schema": "EmployeeSchema",
                "parent_column": "employee_id",
                "cardinality": "N:1"
                }
            }