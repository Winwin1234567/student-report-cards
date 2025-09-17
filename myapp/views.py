from django.shortcuts import render,redirect,get_object_or_404
from django.http import HttpResponse



from .models import *
from .forms import SubjectForm,MarkForm,StudentMarkForm,StudentForm
# Create your views here.
def report_card(request):
    # Get all students and prefetch their marks to reduce queries
    students = Student.objects.prefetch_related('mark_set__subject')
    return render(request, "myapp/report_card.html", {"students": students})
# ========== STUDENT CRUD ==========
def student_list(request):
    students = Student.objects.all()
    return render(request, "myapp/student_list.html", {"students": students})

def student_add(request):
    if request.method == "POST":
        form = StudentForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect("student_list")
    else:
        form = StudentForm()
    return render(request, "myapp/student_form.html", {"form": form})

def student_edit(request, pk):
    student = get_object_or_404(Student, pk=pk)
    if request.method == "POST":
        form = StudentForm(request.POST, instance=student)
        if form.is_valid():
            form.save()
            return redirect("student_list")
    else:
        form = StudentForm(instance=student)
    return render(request, "myapp/student_form.html", {"form": form})

def student_delete(request, pk):
    student = get_object_or_404(Student, pk=pk)
    if request.method == "POST":
        student.delete()
        return redirect("student_list")
    return render(request, "myapp/student_confirm_delete.html", {"object": student, "type": "Student"})

def subject_list(request):
    subjects = Subject.objects.prefetch_related("mark_set__student")
    return render(request, "myapp/subject_list.html", {"subjects": subjects})

def subject_create(request):
    if request.method == "POST":
        form = SubjectForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect("subject_list")  # go back to subject list after saving
    else:
        form = SubjectForm()
    return render(request, "myapp/subject_form.html", {"form": form})

def subject_update(request, pk):
    subject = get_object_or_404(Subject, pk=pk)
    if request.method == "POST":
        form = SubjectForm(request.POST, instance=subject)
        if form.is_valid():
            form.save()
            return redirect("subject_list")
    else:
        form = SubjectForm(instance=subject)
    return render(request, "myapp/subject_form.html", {"form": form})

def subject_delete(request, pk):
    subject = get_object_or_404(Subject, pk=pk)
    if request.method == "POST":
        subject.delete()
        return redirect("subject_list")
    return render(request, "myapp/subject_confirm_delete.html", {"subject": subject})

def mark_create(request):
    subject_id = request.GET.get("subject")
    if request.method == "POST":
        form = MarkForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect("subject_list")
    else:
        form = MarkForm(initial={"subject": subject_id})
    return render(request, "myapp/mark_form.html", {"form": form})
def mark_update(request, pk):
    mark = get_object_or_404(Mark, pk=pk)
    if request.method == "POST":
        form = MarkForm(request.POST, instance=mark)
        if form.is_valid():
            form.save()
            return redirect("mark_list")
    else:
        form = MarkForm(instance=mark)
    return render(request, "myapp/mark_form.html", {"form": form})

def mark_delete(request, pk):
    mark = get_object_or_404(Mark, pk=pk)
    if request.method == "POST":
        mark.delete()
        return redirect("mark_list")
    return render(request, "myapp/mark_confirm_delete.html", {"mark": mark})




def student_mark_add(request):
    if request.method == "POST":
        form = StudentMarkForm(request.POST)
        if form.is_valid():
            # ✅ Use existing student OR create new one
            if form.cleaned_data.get("existing_student"):
                student = form.cleaned_data["existing_student"]
            else:
                student = Student.objects.create(
                    name=form.cleaned_data["student_name"],
                    roll_number=form.cleaned_data["roll_number"]
                )

            # ✅ Create Mark
            Mark.objects.create(
                student=student,
                subject=form.cleaned_data["subject"],
                marks_obtained=form.cleaned_data["marks_obtained"],
            )

            return redirect("mark_list")  # back to mark list page
    else:
        form = StudentMarkForm()

    return render(request, "myapp/student_mark_form.html", {"form": form})

def mark_list(request):
    marks = Mark.objects.select_related("student", "subject")
    return render(request, "myapp/mark_list.html", {"marks": marks})


# Edit (Update) a Mark
def mark_update(request, pk):
    mark = get_object_or_404(Mark, pk=pk)
    if request.method == "POST":
        form = MarkForm(request.POST, instance=mark)
        if form.is_valid():
            form.save()
            return redirect("mark_list")  # or "mark_list" if you prefer
    else:
        form = MarkForm(instance=mark)
    return render(request, "myapp/mark_form.html", {"form": form})

# Delete a Mark
def mark_delete(request, pk):
    mark = get_object_or_404(Mark, pk=pk)
    if request.method == "POST":
        mark.delete()
        return redirect("mark_list")  # redirect back after deletion
    return render(request, "myapp/mark_confirm_delete.html", {"mark": mark})