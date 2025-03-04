import os
import shutil

# Путь к главной папке
main_folder = "/Users/atazhan/Downloads/lfw"


output_folder = "/Users/atazhan/django-faceID/FaceRasp/rasp/rcog/face_id/Images/all_face"
os.makedirs(output_folder, exist_ok=True)


image_extensions = (".jpg", ".jpeg", ".png", ".bmp", ".gif", ".tiff")


counter = 1
max_images = 1000  


for root, dirs, files in os.walk(main_folder):
    for file in files:
        if file.lower().endswith(image_extensions):
            if counter > max_images: 
                break
            source_path = os.path.join(root, file)
            new_file_name = f"face_{counter}.jpg"
            destination_path = os.path.join(output_folder, new_file_name)

            shutil.copy2(source_path, destination_path)
            print(f"Copied: {source_path} -> {destination_path}")
            
            counter += 1 
    if counter > max_images:  
        break
