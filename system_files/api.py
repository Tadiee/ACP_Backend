from ninja_extra import NinjaExtraAPI
from ninja import UploadedFile
from ninja_jwt.controller import NinjaJWTDefaultController
from system_files.schemas import uploadFile, viewFile, editFile, uploadFiles, viewOneFile
from system_files.models import System_Files
from typing import List
from channels.layers import get_channel_layer
from asgiref.sync import async_to_sync
from django.conf import settings
import os
from ninja import File, Form


upload_api = NinjaExtraAPI(urls_namespace="upload_api")
upload_api.register_controllers(NinjaJWTDefaultController)

import os
from datetime import datetime

@upload_api.post('/upload')
def upload_file(
    request,
    file: UploadedFile = File(...),
    file_type: str = Form(...),
    file_name: str = Form(...),
    system: str = Form(...),
    author: str = Form(...),
    signature_status: str = Form(...),
    approval_status: str = Form(...),
    qrcode: str = Form(...),
    month: str = Form(...),
):
    try:
        upload_dir = os.path.join(settings.MEDIA_ROOT, 'uploads')
        os.makedirs(upload_dir, exist_ok=True)

        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        _, ext = os.path.splitext(file.name)
        unique_filename = f"{timestamp}_{file_name}{ext}"
        relative_path = os.path.join('uploads', unique_filename)
        full_path = os.path.join(settings.MEDIA_ROOT, relative_path)

        with open(full_path, 'wb+') as dest:
            for chunk in file.chunks():
                dest.write(chunk)

        uploaded = System_Files.objects.create(
            file_name=file_name,
            file_type=file_type,
            system=system,
            file=relative_path,
            author=author,
            signature_status=signature_status,
            approval_status=approval_status,
            qrcode=qrcode,
            month=month,
        )
        return {"message": "File uploaded successfully", "file_id": uploaded.file_id}
    except Exception as e:
        try:
            if 'full_path' in locals() and os.path.exists(full_path):
                os.remove(full_path)
        except Exception:
            pass
        print(f"Error in upload_file: {e}")
        return {"message": f"File upload failed: {str(e)}"}, 500
    
    
@upload_api.post('/uploadfiles')
def uploadFiles(request, files: List[uploadFiles]):
    try: 
        for file in files:
            System_Files.objects.create(
                file_name = file.file_name,
                system = file.system,
                author = file.author,
                signature_status = file.signature_status,
                approval_status = file.approval_status,
                qrcode = file.qrcode,
                month = file.month,
                # size = file.size,
            )
            
        # After successful upload, notify all connected clients
        channel_layer = get_channel_layer()
        async_to_sync(channel_layer.group_send)(
            "chart_updates",
            {
                "type": "chart_update",
            }
        )
        return {"message": "Files uploaded successfully"}
    except Exception as e:
        print(e)
        return {"message": "Failed to upload files"}
    
@upload_api.get ('/viewuploads', response = List[viewFile])
def viewUpload (request):
    files = System_Files.objects.all()
    result = []
    for file in files:
        result.append(viewFile(
            file_id=file.file_id or "",
            file_name=file.file_name or "",
            file_type=file.file_type or "",
            system=file.system or "",
            created_date=file.created_date or "",
            modified_date=file.modified_date or "",
            author=file.author or "",
            signature_status=file.signature_status or "",
            approval_status=file.approval_status or "",
            qrcode=file.qrcode or "",
            month=file.month or "",
            size=file.size or "",
        ))
    return result

@upload_api.get('/viewoneupload', response={200: viewOneFile, 404: dict, 500: dict})
def viewOneUpload(request, f_id: int):
    try:
        file = System_Files.objects.filter(file_id=f_id).first()
        if not file:
            return {"message": "File not found"}
            
        return 200, viewOneFile(
            file_id=file.file_id or "",
            file_name=file.file_name or "",
            file=file.file or "",
            system=file.system or "",
            created_date=str(file.created_date) if file.created_date else "",
            modified_date=str(file.modified_date) if file.modified_date else "",
            author=file.author or "",
            signature_status=file.signature_status or "",
            approval_status=file.approval_status or "",
            qrcode=file.qrcode or "",
            month=file.month or "",
            size=file.size or "",
        )
        
    except Exception as e:
        print(f"Error in viewOneUpload: {str(e)}")
        return 500, {"message": "Failed to view file"}
    
@upload_api.delete('/removefile')
def removeFile(request, f_id: int):
    file = System_Files.objects.filter(file_id = f_id).first()
    
    try:
        if file:
            file.delete()
            return 200, {"message": "File deleted successfully"}
        else:
            return {"message": "File not found"}
    
    except Exception as e:
        print(f"Error in removeFile: {str(e)}")
        return 500, {"message": "Failed to delete file"}
    

@upload_api.put('/editfile')
def editFile (request, f_id: int, file: editFile):
    updatefile = System_Files.objects.filter(file_id = f_id).first()
    
    try:
        if file:
            updatefile.file_name = file.file_name if file.file_name else updatefile.file_name
            updatefile.system = file.system if file.system else updatefile.system
            updatefile.author = file.author if file.author else updatefile.author
            updatefile.qrcode = file.qrcode if file.qrcode else updatefile.qrcode
            updatefile.month = file.month if file.month else updatefile.month
            updatefile.signature_status = file.signature_status if file.signature_status else updatefile.signature_status
            updatefile.approval_status = file.approval_status if file.approval_status else updatefile.approval_status
            updatefile.save()
            return 200, {"message": "File updated successfully"}
        else:
            return {"message": "File not found"}
    
    except Exception as e:
        print(f"Error in editFile: {str(e)}")
        return 500, {"message": "Failed to update file"}
    
#<<---------------------------------APIs for uploaded files retrieval below----------------->>>


