from django.db import models

# Create your models here.
class System_Files(models.Model):
    # Choices
    SIG_STATUS_CHOICES = [
        ('Signed', 'Signed'),
        ('Not signed', 'Not signed'),
    ]
    
    APPROVAL_STATUS_CHOICES = [
        ('Pending', 'Pending'),
        ('Approved', 'Approved'),
        ('Rejected', 'Rejected'),
    ]
    
    # Model fields
    file_id = models.AutoField(primary_key=True)
    file_name = models.CharField(max_length=100)
    system = models.CharField(max_length=100)
    created_date = models.CharField(max_length=10)  # DD/MM/YYYY
    modified_date = models.CharField(max_length=10)  # DD/MM/YYYY
    file = models.FileField(upload_to='files/')
    author = models.CharField(max_length=100)
    file_type = models.CharField(max_length=100)
    signature_status = models.CharField(
        max_length=100, 
        choices=SIG_STATUS_CHOICES,
        default='Pending'
    )
    approval_status = models.CharField(
        max_length=100, 
        choices=APPROVAL_STATUS_CHOICES,
        default='Not signed'
    )
    qrcode = models.CharField(max_length=100, blank=True)
    month = models.CharField(max_length=100)
    size = models.CharField(max_length=50)
    
    def save(self, *args, **kwargs):
        from datetime import datetime
        
        # Format the current date as DD/MM/YYYY
        current_date = datetime.now().strftime("%d/%m/%Y")
        
        # Set created_date only for new instances
        if not self.pk:
            self.created_date = current_date
            
        # Always update modified_date
        self.modified_date = current_date
        
        super().save(*args, **kwargs)
    
    def __str__(self):
        return f"{self.file_name} - {self.system}"
    
