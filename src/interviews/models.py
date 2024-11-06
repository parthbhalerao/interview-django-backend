from django.db import models
from django.conf import settings

User = settings.AUTH_USER_MODEL

class InterviewStatus(models.TextChoices):
    SCHEDULED = "scheduled", "Scheduled"
    IN_PROGRESS = "in_progress", "In Progress"
    COMPLETED = "completed", "Completed"
    CANCELLED = "cancelled", "Cancelled"
    RESCHEDULED = "rescheduled", "Rescheduled"

class InterviewType(models.TextChoices):
    TECHNICAL = "technical", "Technical"
    BEHAVIORAL = "behavioral", "Behavioral"
    SYSTEM_DESIGN = "system_design", "System Design"
    CODING = "coding", "Coding"

class InterviewDifficultyLevel(models.TextChoices):
    EASY = "easy", "Easy"
    MEDIUM = "medium", "Medium"
    HARD = "hard", "Hard"

class Interview(models.Model):
    room_name = models.CharField(max_length=255, unique=True)
    title = models.CharField(max_length=255)
    description = models.TextField(blank=True)
    status = models.CharField(max_length=255, choices=InterviewStatus.choices)
    company = models.ForeignKey('jobs.Company', on_delete=models.SET_NULL, null=True, blank=True)
    job_role = models.ForeignKey('jobs.JobRole', on_delete=models.SET_NULL, null=True, blank=True)
    scheduled_at = models.DateTimeField()
    duration_minutes = models.IntegerField(default=60)
    interview_type = models.CharField(max_length=50, choices=InterviewType.choices)
    difficulty_level = models.CharField(max_length=20, choices=InterviewDifficultyLevel.choices)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    

    def __str__(self):
        return f"{self.title} - {self.room_name}"
    
class InterviewParticipantRole(models.TextChoices):
    INTERVIEWER = "interviewer", "Interviewer"
    INTERVIEWEE = "interviewee", "Interviewee"
    OBSERVER = "observer", "Observer"

class InterviewParticipant(models.Model):
    interview = models.ForeignKey(Interview, on_delete=models.CASCADE, related_name='participants')
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    role = models.CharField(max_length=20, choices=InterviewParticipantRole.choices)
    feedback = models.TextField(blank=True)
    rating = models.IntegerField(null=True, blank=True, choices=[(i, i) for i in range(1, 6)])
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        unique_together = ['interview', 'user']

    def __str__(self):
        return f"{self.user.username} - {self.role} - {self.interview.room_name}"

