from django.db import models
from django.utils import timezone
from register.models import User, Member
from django.core.validators import MaxValueValidator, MinValueValidator

status = (
    ('1', 'Stuck'),
    ('2', 'Working'),
    ('3', 'Done'),
)

due = (
    ('1', 'On Due'),
    ('2', 'Overdue'),
    ('3', 'Done'),
)

# Create your models here.
class Project(models.Model):
    name = models.CharField(max_length=80)
    slug = models.SlugField('shortcut', blank=True)
    efforts = models.DurationField()
    status = models.CharField(max_length=7, choices=status, default=1)
    complete_per = models.FloatField(default=0,max_length=2, validators = [MinValueValidator(0), MaxValueValidator(100)])
    description = models.TextField(blank=True)
    start_date = models.DateField(auto_now_add=True)
    upd_date = models.DateField(auto_now_add=False, auto_now=True)
    dead_line = models.DateField()
    github = models.URLField(blank=True)
    product_link = models.URLField(blank=True)
    requester = models.ForeignKey(User, on_delete=models.CASCADE, related_name="requested_project")
    developers = models.ManyToManyField(Member, related_name="developing_project")
    managers = models.ManyToManyField(Member, related_name="managing_project")

    class Meta:
        ordering = ['name']

    def __str__(self):
        return (self.name)
    
class ProjectRequest(models.Model):
    requester = models.ForeignKey(User, on_delete=models.CASCADE, related_name="requested_project_request")
    name = models.CharField(max_length=80)
    slug = models.SlugField('shortcut', blank=True)
    dead_line = models.DateField()
    description = models.TextField()
    started = models.BooleanField(default=False)
    class Meta:
        ordering = ['name']

    def __str__(self):
        return (self.name)


class Task(models.Model):
    project = models.ForeignKey(Project, on_delete=models.CASCADE)
    assign = models.ManyToManyField(Member)
    task_name = models.CharField(max_length=80)
    status = models.CharField(max_length=7, choices=status, default=1)
    due = models.CharField(max_length=7, choices=due, default=1)

    class Meta:
        ordering = ['project', 'task_name']

    def __str__(self):
        return(self.task_name)