from .exception import *
from datetime import datetime
import gspread
from oauth2client.service_account import ServiceAccountCredentials
import os

class Client():
  
  def __init__(self, file_name, debt_sheet_name):

    self.file_name = file_name
    self.debt_sheet = debt_sheet_name
    self.session = self._create_session()
    self.member = ["พ้ง", "เว็บ", "อู๋","ป้อง"]

  def _create_session(self):
    scope = ["https://spreadsheets.google.com/feeds",'https://www.googleapis.com/auth/spreadsheets',"https://www.googleapis.com/auth/drive.file","https://www.googleapis.com/auth/drive"]
    credential_data = os.getenv("GOOGLE_CREDENTIALS_JSON")
    cerds = ServiceAccountCredentials.from_json_keyfile_dict(credential_data, scope)
    session = gspread.authorize(cerds)
    return session
  
  def _get_file(self):
    file = self.session.open(self.file_name)
    return file
  
  def _get_sheet(self, sheet_name=None):
    if not sheet_name:
      sheet = self._get_file().worksheet(self.debt_sheet)
    else:
      sheet = self._get_file().worksheet(sheet_name)
    return sheet
  
  def debt_list(self):
    sheet = self._get_sheet()
    data = sheet.get_all_records()
    return data
  
  def add_debt(self, debt_detail):
    sheet = self._get_sheet()
    formatted_debt_detail = [] 
    formatted_debt_detail.append(datetime.now().strftime("%d/%m/%Y %H:%M:%S"))
    
    headers = sheet.get("B1:G1")
    for header in headers[0]:
      if header in debt_detail:
        formatted_debt_detail.append(debt_detail[header])
      else:
        formatted_debt_detail.append("")

    response = sheet.append_row(formatted_debt_detail, insert_data_option="INSERT_ROWS", value_input_option="USER_ENTERED", include_values_in_response=True)
    return response
  
  def check_debt(self, debtor=None):
    if debtor and debtor in self.member:
      sheet = self._get_sheet(f"ลูกหนี้{debtor}")
      data = sheet.get_all_records()[0]
      if "เจ้านี่" in data:
        del data["เจ้านี่"]
      formatted_data = {"borrower": debtor, "amount":data}
      return formatted_data
    else:
      return {"message": "please give me a name"}
