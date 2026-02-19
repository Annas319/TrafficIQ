import csv
import os
from django.core.files import File
from django.conf import settings
from .models import QuizQuestion


def import_questions_from_csv(csv_path, quiz_test):
    """
    Imports MCQ questions into QuizQuestion model with optional image support.
    """

    images_folder = os.path.join(settings.MEDIA_ROOT, "quiz_images")

    # Load all available images for fast matching
    existing_files = {f.lower(): f for f in os.listdir(images_folder)}

    with open(csv_path, newline='', encoding='utf-8') as file:
        reader = csv.DictReader(file)

        for row in reader:

            # Create question object
            q = QuizQuestion(
                test=quiz_test,
                question=row["question"].strip(),
                option_a=row["option_a"].strip(),
                option_b=row["option_b"].strip(),
                option_c=row["option_c"].strip(),
                option_d=row["option_d"].strip(),
                correct_answer=row["correct_answer"].strip().upper(),
            )

            # Handle image column
            image_name = (row.get("image") or "").strip()

            if image_name:
                key = image_name.lower()

                if key in existing_files:
                    real_name = existing_files[key]
                    path = os.path.join(images_folder, real_name)

                    try:
                        with open(path, "rb") as img:
                            q.image.save(real_name, File(img), save=False)
                    except Exception as e:
                        print(f"⚠️ Error loading image {image_name}: {e}")
                else:
                    print(f"⚠️ Image NOT FOUND: {image_name}")

            q.save()

    print("✅ CSV Import Completed Successfully!")


# import csv
# import os
# from django.core.files import File
# from django.conf import settings
# from .models import QuizQuestion

# def import_questions_from_csv(csv_path, quiz_test):
#     images_folder = os.path.join(settings.MEDIA_ROOT, "quiz_images")

#     # Get all filenames in lower-case for easy matching
#     existing_files = {f.lower(): f for f in os.listdir(images_folder)}

#     with open(csv_path, newline='', encoding='utf-8') as file:
#         # Define the fieldnames we expect, regardless of what's in the CSV header
#         fieldnames = ["question", "option_a", "option_b", "option_c", "option_d", "correct_answer", "image"]

#         reader = csv.DictReader(file, fieldnames=fieldnames)
#         next(reader)  # 🚀 skip the first row (Excel's "Column 1, Column 2...")

#         for row in reader:
#             q = QuizQuestion(
#                 test=quiz_test,
#                 question=row["question"].strip(),
#                 option_a=row["option_a"].strip(),
#                 option_b=row["option_b"].strip(),
#                 option_c=row["option_c"].strip(),
#                 option_d=row["option_d"].strip(),
#                 correct_answer=row["correct_answer"].strip().upper(),
#             )

#             # IMAGE HANDLING
#             image_name = (row.get("image") or "").strip()
#             if image_name:
#                 image_key = image_name.lower()
#                 if image_key in existing_files:
#                     real_file = existing_files[image_key]
#                     image_path = os.path.join(images_folder, real_file)

#                     try:
#                         with open(image_path, "rb") as img_file:
#                             q.image.save(real_file, File(img_file), save=False)
#                     except Exception as e:
#                         print("Image load error:", e)

#             q.save()
