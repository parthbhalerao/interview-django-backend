from django.db import models
from django.conf import settings

User = settings.AUTH_USER_MODEL

class Company(models.Model):
    name = models.CharField(max_length=255)
    description = models.TextField(blank=True)
    website = models.URLField(blank=True)
    location = models.CharField(max_length=255, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name_plural = "Companies"

    def __str__(self):
        return self.name

class JobLevel(models.TextChoices):
    INTERN = "intern", "Intern"
    ENTRY = "entry", "Entry Level"
    MID = "mid", "Mid Level"
    SENIOR = "senior", "Senior"
    LEAD = "lead", "Lead"
    MANAGER = "manager", "Manager"
    DIRECTOR = "director", "Director"

class JobRole(models.Model):
    title = models.CharField(max_length=255)
    company = models.ForeignKey(Company, on_delete=models.CASCADE)
    level = models.CharField(max_length=20, choices=JobLevel.choices)
    description = models.TextField(blank=True)
    requirements = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.title} at {self.company.name}"
