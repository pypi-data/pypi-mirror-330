import pandas as pd
import pandera as pa
from pandera import Bool
from pandera.typing import Series, String, Float, DateTime
import pandera.extensions as extensions
from brynq_sdk_functions import BrynQPanderaDataFrameModel


class EmploymentSchema(BrynQPanderaDataFrameModel):
    employee_id: Series[String] = pa.Field(coerce=True)
    employment_id: Series[String] = pa.Field(coerce=True)
    start_date: Series[DateTime] = pa.Field(coerce=True)
    end_date: Series[DateTime] = pa.Field(coerce=True, nullable=True)
    end_contract_reason: Series[String] = pa.Field(coerce=True, nullable=True)
    # created_at: Series[DateTime] = pa.Field(coerce=True)
    # todo: implement salary tables
    # created_at: Series[DateTime] = pa.Field(coerce=True, nullable=True)
    # company_id: Series[String] = pa.Field(coerce=True)

    class Annotation:
        primary_key = "employment_id"
        foreign_keys = {
            "employee_id": {
                "parent_schema": "EmployeeSchema",
                "parent_column": "employee_id",
                "cardinality": "N:1"
                }
            }