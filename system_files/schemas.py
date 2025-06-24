from ninja import Schema, UploadedFile
from typing import Optional
from datetime import date

class uploadFile(Schema):
    file_name: str
    file_type: str
    system: str
    file: str
    author: str
    signature_status: str
    approval_status: str
    qrcode: str
    month: str
    # size: str = ""

class viewFile(Schema):
    file_id: int
    file_name: str
    file_type: str
    system: str
    created_date: str = ""
    modified_date: str = ""
    author: str
    signature_status: str
    approval_status: str
    qrcode: str = ""
    month: str = ""
    size: str = ""
    
class viewOneFile(Schema):
    file_id: int
    file_name: str
    file: str
    system: str
    created_date: str = ""
    modified_date: str = ""
    author: str
    signature_status: str
    approval_status: str
    qrcode: str = ""
    month: str = ""
    size: str = ""
    
class uploadFiles(Schema):
    file_name: str
    system: str
    author: str
    signature_status: str
    approval_status: str
    qrcode: str = ""
    month: str = ""
    # size: str = ""
    

class editFile(Schema):
    file_name: str
    system: str
    author: str
    qrcode: str = ""
    month: str = ""
    signature_status: str
    approval_status: str
