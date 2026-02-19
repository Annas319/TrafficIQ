from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver


class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    bio = models.TextField(blank=True, null=True)
    location = models.CharField(max_length=100, blank=True, null=True)
    phone = models.CharField(max_length=15, blank=True, null=True)
    city = models.CharField(max_length=100, blank=True, null=True)
    profile_picture = models.ImageField(
        upload_to='profile_pics/',
        default='profile_pics/default.png',
        blank=True,
        null=True
    )

    def __str__(self):
        return self.user.username


# 🔹 Auto-create and save Profile for each User
@receiver(post_save, sender=User)
def create_user_profile(sender, instance, created, **kwargs):
    if created:
        Profile.objects.create(user=instance)

@receiver(post_save, sender=User)
def save_user_profile(sender, instance, **kwargs):
    instance.profile.save()

ANSWER_CHOICES = [
    ('A', 'Option A'),
    ('B', 'Option B'),
    ('C', 'Option C'),
    ('D', 'Option D'),
]

# 🔹 A test (e.g. Traffic Rules Test 1)
class QuizTest(models.Model):
    title = models.CharField(max_length=200)
    created_by = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title

class QuizQuestion(models.Model):
    test = models.ForeignKey(QuizTest, on_delete=models.CASCADE, related_name='questions')
    question = models.TextField()
    option_a = models.CharField(max_length=255)
    option_b = models.CharField(max_length=255)
    option_c = models.CharField(max_length=255)
    option_d = models.CharField(max_length=255)
    image = models.ImageField(upload_to='quiz_images/', blank=True, null=True)

    # 👇 this makes a dropdown automatically appear in admin
    correct_answer = models.CharField(
        max_length=1,
        choices=ANSWER_CHOICES,
        default='A'
    )

    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.question[:50]

# 🔹 Store user's attempts
class QuizAttempt(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    test = models.ForeignKey(QuizTest, on_delete=models.CASCADE)
    score = models.IntegerField()
    total = models.IntegerField()
    attempted_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.user.username} - {self.test.title} ({self.score}/{self.total})"

from django.contrib.auth.models import User

class TrafficRule(models.Model):
    title_en = models.CharField("Title (English)", max_length=255)
    title_ur = models.CharField("Title (Urdu)", max_length=255, blank=True, null=True)
    file = models.FileField(upload_to="rules_files/", blank=True, null=True)  # 📂 Uploads stored in MEDIA/rules_files/
    created_at = models.DateTimeField(auto_now_add=True)
    added_by = models.ForeignKey(User, on_delete=models.CASCADE)

    def __str__(self):
        # return f"{self.title_en} / {self.title_ur or ''} (by {self.added_by.username})"
        return f"{self.title_en} (by {self.added_by.username})"

class Tutorial(models.Model):
    title_en = models.CharField("Title (English)", max_length=255)
    title_ur = models.CharField("Title (Urdu)", max_length=255, blank=True, null=True)
    file = models.FileField(upload_to="tutorials/", blank=True, null=True)  # optional PDF/video
    created_at = models.DateTimeField(auto_now_add=True)
    added_by = models.ForeignKey(User, on_delete=models.CASCADE)  # admin who added

    def __str__(self):
        # return f"{self.title_en} / {self.title_ur or ''} (by {self.added_by.username})"
        return f"{self.title_en} (by {self.added_by.username})"