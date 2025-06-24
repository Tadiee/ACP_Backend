from ninja import Schema
from typing import Dict

class ViewCommentSchema(Schema):
    comment_id: int
    file_id: int
    comment: Dict
    comment_date: str
    comment_time: str
    approver: str
    requester: str

class AddCommentSchema(Schema):
    file_id: int
    comment: Dict
    approver: str
    requester: str