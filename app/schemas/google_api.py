from pydantic import BaseModel


class SpreadSheetLink(BaseModel):

    spreadsheet_url: str
