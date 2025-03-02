from typing import List
from datetime import datetime
from at_common_schemas.base import BaseSchema
from pydantic import Field
from at_common_schemas.common.stock import StockFiling, StockFilingForm

class StockFilingBatchRequest(BaseSchema):
    symbol: str = Field(..., description="Stock symbol")
    form: StockFilingForm = Field(..., description="Form of the filing")
    date_from: datetime = Field(..., description="Start date for the request")
    date_to: datetime = Field(..., description="End date for the request")

class StockFilingBatchResponse(BaseSchema):
    items: List[StockFiling] = Field(..., description="List of filings")