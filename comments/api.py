from ninja_extra import NinjaExtraAPI
from ninja_jwt.controller import NinjaJWTDefaultController
from comments.schemas import ViewCommentSchema, AddCommentSchema
from comments.models import Comments
from typing import List
from datetime import datetime
from ninja.errors import HttpError


comment_api = NinjaExtraAPI(urls_namespace="comment_api")
comment_api.register_controllers(NinjaJWTDefaultController)

@comment_api.get('/viewcomment', response=ViewCommentSchema)
def ViewComment(request, file_id : int):
    try:
        comment = Comments.objects.filter(file_id_id=file_id).first()
        if comment:
            return ViewCommentSchema(
                comment_id=comment.comment_id,
                file_id= comment.file_id_id,
                comment=comment.comment,
                comment_date=datetime.fromtimestamp(float(comment.comment_date)).strftime("%d/%m/%Y"),
                comment_time=datetime.fromtimestamp(float(comment.comment_date)).strftime("%H:%M:%S"),
                approver=comment.approver,
                requester=comment.requester,
            )
        else:
            raise HttpError(404, "Comment not found")
    except Exception as e:
        raise HttpError(500, f"Error: {e}")

@comment_api.post('/addcomment')
def AddComment(request, comment: AddCommentSchema):
    from system_files.models import System_Files
    try:
        comments_obj = Comments.objects.filter(file_id=comment.file_id).first()
        if comments_obj:
            # Existing comment thread for this file
            comment_data = comments_obj.comment or {}
            # Append new approver_comments if provided
            if 'approver_comments' in comment.comment:
                comment_data.setdefault('approver_comments', [])
                new_approver_comments = comment.comment['approver_comments']
                if isinstance(new_approver_comments, list):
                    comment_data['approver_comments'].extend(new_approver_comments)
                else:
                    comment_data['approver_comments'].append(new_approver_comments)
            # Append new requester_comments if provided
            if 'requester_comments' in comment.comment:
                comment_data.setdefault('requester_comments', [])
                new_requester_comments = comment.comment['requester_comments']
                if isinstance(new_requester_comments, list):
                    comment_data['requester_comments'].extend(new_requester_comments)
                else:
                    comment_data['requester_comments'].append(new_requester_comments)
            comments_obj.comment = comment_data
            comments_obj.save()
            return 'Comment(s) added successfully'
        else:
            # No comment thread for this file, create new
            file_instance = System_Files.objects.get(pk=comment.file_id)
            new_comment = Comments.objects.create(
                file_id=file_instance,
                comment=comment.comment,
                approver=comment.approver,
                requester=comment.requester,
            )
            if new_comment:
                return '1st Comment added successfully'
            else:
                raise HttpError(500, "Error adding comment")
    except Exception as e:
        raise HttpError(500, f"Error: {e}")

    
