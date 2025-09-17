from django.db import models

# Create your models here.


class Student(models.Model):
    name = models.CharField(max_length=100)
    roll_number = models.CharField(max_length=20, unique=True)

    def __str__(self):
        return f"{self.name} ({self.roll_number})"


class Subject(models.Model):
    name = models.CharField(max_length=100, unique=True)

    def __str__(self):
        return self.name


class Mark(models.Model):
    student = models.ForeignKey(Student, on_delete=models.CASCADE)
    subject = models.ForeignKey(Subject, on_delete=models.CASCADE)
    marks_obtained = models.FloatField()

    def __str__(self):
        return f"{self.student.name} - {self.subject.name}: {self.marks_obtained}"
