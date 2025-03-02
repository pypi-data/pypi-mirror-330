from typing import List
from datetime import datetime
from at_common_schemas.base import BaseSchema
from pydantic import Field
from at_common_schemas.common.stock import StockFilingMeta, StockFilingDocument, StockFilingForm

class StockFilingMetaBatchRequest(BaseSchema):
    symbol: str = Field(..., description="Stock symbol")
    form: StockFilingForm = Field(..., description="Form of the filing")
    date_from: datetime = Field(..., description="Start date for the request")
    date_to: datetime = Field(..., description="End date for the request")

class StockFilingMetaBatchResponse(BaseSchema):
    items: List[StockFilingMeta] = Field(..., description="List of filings")

class StockFilingDocumentRequest(BaseSchema):
    accession_number: str = Field(..., description="Accession number of the filing")

class StockFilingDocumentResponse(StockFilingDocument):
    pass