from django.db import models
from django.contrib.auth.models import User


class Resume(models.Model):
    TEMPLATE_CHOICES = [
        ('classic', 'Classic'),
        ('modern', 'Modern'),
        ('minimal', 'Minimal'),
    ]
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    title = models.CharField(max_length=200, help_text="e.g. Software Developer Resume")
    template = models.CharField(max_length=20, choices=TEMPLATE_CHOICES, default='classic')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.title


class PersonalInfo(models.Model):
    resume = models.OneToOneField(Resume, on_delete=models.CASCADE, related_name='personal_info')
    full_name = models.CharField(max_length=200)
    email = models.EmailField()
    phone = models.CharField(max_length=20, blank=True)
    location = models.CharField(max_length=200, blank=True)
    linkedin = models.URLField(blank=True)
    github = models.URLField(blank=True)
    summary = models.TextField(blank=True, help_text="Short professional summary")

    def __str__(self):
        return self.full_name


class Education(models.Model):
    resume = models.ForeignKey(Resume, on_delete=models.CASCADE, related_name='education')
    degree = models.CharField(max_length=200)
    institution = models.CharField(max_length=200)
    year = models.CharField(max_length=20, help_text="e.g. 2022-2026")
    score = models.CharField(max_length=50, blank=True, help_text="CGPA or %")

    def __str__(self):
        return f"{self.degree} - {self.institution}"


class Experience(models.Model):
    resume = models.ForeignKey(Resume, on_delete=models.CASCADE, related_name='experience')
    company = models.CharField(max_length=200)
    role = models.CharField(max_length=200)
    duration = models.CharField(max_length=100, help_text="e.g. Jul 2026 - Present")
    description = models.TextField(blank=True)

    def __str__(self):
        return f"{self.role} at {self.company}"


class Skill(models.Model):
    resume = models.ForeignKey(Resume, on_delete=models.CASCADE, related_name='skills')
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name


class Project(models.Model):
    resume = models.ForeignKey(Resume, on_delete=models.CASCADE, related_name='projects')
    title = models.CharField(max_length=200)
    description = models.TextField(blank=True)
    tech_stack = models.CharField(max_length=300, blank=True)
    link = models.URLField(blank=True)

    def __str__(self):
        return self.title


class Certification(models.Model):
    resume = models.ForeignKey(Resume, on_delete=models.CASCADE, related_name='certifications')
    name = models.CharField(max_length=200)
    issuer = models.CharField(max_length=200, blank=True)
    year = models.CharField(max_length=20, blank=True)

    def __str__(self):
        return self.name


class Achievement(models.Model):
    resume = models.ForeignKey(Resume, on_delete=models.CASCADE, related_name='achievements')
    title = models.CharField(max_length=300)

    def __str__(self):
        return self.title


class Language(models.Model):
    resume = models.ForeignKey(Resume, on_delete=models.CASCADE, related_name='languages')
    name = models.CharField(max_length=100)
    proficiency = models.CharField(max_length=50, blank=True, help_text="e.g. Fluent, Intermediate")

    def __str__(self):
        return self.name