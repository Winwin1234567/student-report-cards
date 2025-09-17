from django import forms
from .models import Student,Subject,Mark


class StudentForm(forms.ModelForm):
    class Meta:
        model = Student
        fields = ['name', 'roll_number']
class SubjectForm(forms.ModelForm):
    class Meta:
        model = Subject
        fields = ['name']

class MarkForm(forms.ModelForm):
    class Meta:
        model = Mark
        fields = ['student','subject','marks_obtained']


class StudentMarkForm(forms.Form):
    existing_student = forms.ModelChoiceField(
        queryset=Student.objects.all(),
        required=False,
        label="Choose Existing Student"
    )
    student_name = forms.CharField(label="Student Name", max_length=100, required=False)
    roll_number = forms.CharField(label="Roll Number", max_length=20, required=False)
    subject = forms.ModelChoiceField(queryset=Subject.objects.all())
    marks_obtained = forms.IntegerField(min_value=0, label="Marks Obtained")

    def clean(self):
        cleaned_data = super().clean()
        if not cleaned_data.get("existing_student") and not cleaned_data.get("student_name"):
            raise forms.ValidationError("You must choose an existing student OR enter a new one.")
        return cleaned_data