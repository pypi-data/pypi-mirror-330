"""Schema definitions for Nmbrs package"""

DATEFORMAT = '%Y%m%d'

from .address import AddressSchema
from .bank import BankSchema
from .contracts import ContractSchema
from .department import DepartmentSchema
from .employees import EmployeeSchema
from .employment import EmploymentSchema
from .function import FunctionSchema
from .hours import FixedHoursSchema, VariableHoursSchema
from .salary import SalarySchema
from .wagecomponents import FixedWageComponentSchema, VariableWageComponentSchema


__all__ = [
    'DATEFORMAT',
    'AddressSchema',
    'BankSchema',
    'ContractSchema',
    'DepartmentSchema',
    'EmployeeSchema',
    'EmploymentSchema',
    'FunctionSchema',
    'FixedHoursSchema',
    'VariableHoursSchema',
    'SalarySchema',
    'FixedWageComponentSchema',
    'VariableWageComponentSchema'
]
