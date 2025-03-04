from django.db.models.signals import post_save
from django.dispatch import receiver
from .models import People
import sys
from .EncodeGenerator import generate_encodings
import os


@receiver(post_save, sender=People)
def update_encodings_on_new_person(sender, instance, created, **kwargs):
    if created:  
        folderPath = '/Users/atazhan/django-faceID/FaceRasp/rasp/rcog/face_id/Images/all_face'
        output_file = '/Users/atazhan/django-faceID/FaceRasp/rasp/rcog/face_id/EncodeFile.p' 
        if os.path.exists(folderPath):
            generate_encodings(folderPath, output_file)
        else:
            print(f"Folder not found: {folderPath}")




@receiver(post_save, sender=People)
def rename_faceImg(sender, instance, **kwargs):
    if instance.faceImg:
        old_path = instance.faceImg.path  
        extension = os.path.splitext(old_path)[1]  
        new_name = f"{instance.firstName}_{instance.lastName}{extension}"
        new_path = os.path.join(os.path.dirname(old_path), new_name) 


        if old_path != new_path:
            os.rename(old_path, new_path)

            instance.faceImg.name = f'all_face/{new_name}'
            instance.save(update_fields=['faceImg'])
