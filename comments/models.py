from django.db import models
from system_files.models import System_Files

# Create your models here.
class Comments(models.Model):
    comment_id = models.AutoField(primary_key=True)
    file_id = models.OneToOneField(System_Files, on_delete=models.CASCADE)
    comment = models.JSONField()
    comment_date = models.CharField(max_length=100)
    approver = models.CharField(max_length=100)
    requester = models.CharField(max_length=100)
    
    def save(self, *args, **kwargs):
        from datetime import datetime
        
        # Format the current date as DD/MM/YYYY
        current_date = datetime.now().timestamp()
        
        # Set created_date only for new instances
        if not self.pk:
            self.comment_date = current_date
        
        super().save(*args, **kwargs)
    
    def __str__(self):
        return f"{self.file_id}"
    
    
    

    
    
