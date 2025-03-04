import cv2
import face_recognition
import pickle
import os
from multiprocessing import Pool

def encode_single_image(img_info):
    """Извлекает кодировку лица и связанный ID."""
    idx, img, student_id = img_info
    try:
        img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
        encodes = face_recognition.face_encodings(img)
        if encodes:
            return encodes[0], student_id
        else:
            print(f"No face detected in image {student_id}. Skipping...")
            return None
    except Exception as e:
        print(f"Error encoding image {student_id}: {e}")
        return None

def load_existing_encodings(output_file):
    """Загружает существующие кодировки из файла, если он существует."""
    if os.path.exists(output_file):
        with open(output_file, 'rb') as file:
            return pickle.load(file)  # Это возвращает кортеж, например, ([encoded_faces], [student_ids])
    return [], []  # Возвращаем два пустых списка, если файла нет

def save_encodings(output_file, encodeListKnown, studentIDsKnown):
    """Сохраняет кодировки в файл."""
    with open(output_file, 'wb') as file:
        pickle.dump([encodeListKnown, studentIDsKnown], file)
    print(f"Encodings saved successfully in {output_file}.")

def generate_encodings(folderPath, output_file="EncodeFile.p"):
    """Генерирует кодировки для лиц и сохраняет их в файл."""
    pathList = os.listdir(folderPath)
    imgList = []
    studentIDs = []

    def load_and_resize_image(path):
        try:
            img = cv2.imread(path)
            img = cv2.resize(img, (0, 0), fx=0.5, fy=0.5)
            return img
        except Exception as e:
            print(f"Error loading image: {e}")
            return None

    # Загружаем изображения и ID студентов
    for path in pathList:
        fullPath = os.path.join(folderPath, path)
        img = load_and_resize_image(fullPath)
        if img is not None:
            student_id = os.path.splitext(path)[0]
            imgList.append(img)
            studentIDs.append(student_id)
    print(f"Loaded {len(studentIDs)} student images.")

    # Загружаем существующие кодировки из файла
    existing_encodings, existing_ids = load_existing_encodings(output_file)
    print(f"Loaded {len(existing_ids)} existing encodings.")

    # Находим новые изображения, которых еще нет в кодировках
    new_images = []
    new_ids = []
    for img, student_id in zip(imgList, studentIDs):
        if student_id not in existing_ids:
            new_images.append(img)
            new_ids.append(student_id)

    if not new_images:
        print("No new images to encode.")
        return

    # Получаем кодировки для новых изображений
    def findEncodings(imagesList, ids):
        """Параллельно кодирует изображения и возвращает их кодировки с ID."""
        with Pool() as pool:
            results = pool.map(encode_single_image, [(idx, img, ids[idx]) for idx, img in enumerate(imagesList)])
        return [res for res in results if res]

    # Кодируем только новые изображения
    encodings_with_ids = findEncodings(new_images, new_ids)
    if encodings_with_ids:
        encodeListKnown, studentIDsKnown = zip(*encodings_with_ids)

        # Преобразуем результаты из кортежа в списки для дальнейшей работы
        encodeListKnown = list(encodeListKnown)
        studentIDsKnown = list(studentIDsKnown)

        # Дополняем существующие кодировки новыми
        encodeListKnown.extend(existing_encodings)
        studentIDsKnown.extend(existing_ids)

        # Сохраняем обновленные кодировки в файл
        save_encodings(output_file, encodeListKnown, studentIDsKnown)
        print("Encodings updated successfully.")
    else:
        print("No new encodings to add.")
