from django.contrib import admin
from .models import Company, JobRole

@admin.register(Company)
class CompanyAdmin(admin.ModelAdmin):
    list_display = ['name', 'location', 'website']
    search_fields = ['name', 'location']

@admin.register(JobRole)
class JobRoleAdmin(admin.ModelAdmin):
    list_display = ['title', 'company', 'level']
    list_filter = ['level', 'company']
    search_fields = ['title', 'company__name']
