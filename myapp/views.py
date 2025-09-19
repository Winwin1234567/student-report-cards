from django.shortcuts import render,redirect,get_object_or_404
from django.http import HttpResponse
from django.contrib.auth.decorators import login_required


from .models import *
from .forms import SubjectForm,MarkForm,StudentMarkForm,StudentForm
from django.db.models import Sum, Avg, Max, Min
from django.db.models import Count
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from myapp.models import Student, Subject, Mark
import json
import re

# Create your views here.
def report_card(request):
    # Get all students and prefetch their marks to reduce queries
    students = Student.objects.prefetch_related('mark_set__subject')
    return render(request, "myapp/report_card.html", {"students": students})
# ========== STUDENT CRUD ==========
@login_required(login_url='login')
def student_list(request):
    students = Student.objects.all()
    return render(request, "myapp/student_list.html", {"students": students})

@login_required(login_url='login')
def student_add(request):
    if request.method == "POST":
        form = StudentForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect("student_list")
    else:
        form = StudentForm()
    return render(request, "myapp/student_form.html", {"form": form})
@login_required(login_url='login')
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
@login_required(login_url='login')
def student_delete(request, pk):
    student = get_object_or_404(Student, pk=pk)
    if request.method == "POST":
        student.delete()
        return redirect("student_list")
    return render(request, "myapp/student_confirm_delete.html", {"object": student, "type": "Student"})
@login_required(login_url='login')
def subject_list(request):
    subjects = Subject.objects.prefetch_related("mark_set__student")
    return render(request, "myapp/subject_list.html", {"subjects": subjects})
@login_required(login_url='login')
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
@login_required(login_url='login')
def subject_delete(request, pk):
    subject = get_object_or_404(Subject, pk=pk)
    if request.method == "POST":
        subject.delete()
        return redirect("subject_list")
    return render(request, "myapp/subject_confirm_delete.html", {"subject": subject})
@login_required(login_url='login')
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
@login_required(login_url='login')
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
@login_required(login_url='login')
def mark_delete(request, pk):
    mark = get_object_or_404(Mark, pk=pk)
    if request.method == "POST":
        mark.delete()
        return redirect("mark_list")
    return render(request, "myapp/mark_confirm_delete.html", {"mark": mark})



@login_required(login_url='login')
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
@login_required(login_url='login')
def mark_list(request):
    marks = Mark.objects.select_related("student", "subject")
    return render(request, "myapp/mark_list.html", {"marks": marks})

@login_required(login_url='login')
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
@login_required(login_url='login')
# Delete a Mark
def mark_delete(request, pk):
    mark = get_object_or_404(Mark, pk=pk)
    if request.method == "POST":
        mark.delete()
        return redirect("mark_list")  # redirect back after deletion
    return render(request, "myapp/mark_confirm_delete.html", {"mark": mark})









@csrf_exempt
def chatbot_api(request):
    if request.method == "POST":
        data = json.loads(request.body)
        message = data.get("message", "").lower()

        # 1. "highest marks"
        if "highest" in message:
            top_student = (
                Student.objects.annotate(total_marks=Sum('mark__marks_obtained'))
                .order_by('-total_marks')
                .first()
            )
            if top_student:
                return JsonResponse({
                    "reply": f"{top_student.name} has the highest total marks ({top_student.total_marks})."
                })

        # 2. "lowest marks"
        if "lowest" in message:
            low_student = (
                Student.objects.annotate(total_marks=Sum('mark__marks_obtained'))
                .order_by('total_marks')
                .first()
            )
            if low_student:
                return JsonResponse({
                    "reply": f"{low_student.name} has the lowest total marks ({low_student.total_marks})."
                })

        # 3. "popular subjects"
        if "popular" in message and "subject" in message:
            popular_subjects = (
                Subject.objects.annotate(num_marks=Count('mark'))
                .order_by('-num_marks')
            )
            if popular_subjects.exists():
                top = popular_subjects.first()
                return JsonResponse({
                    "reply": f"The most popular subject is {top.name} with {top.num_marks} marks recorded."
                })
            return JsonResponse({"reply": "No subjects found."})

        # 4. "total students" or "how many students"
        if "total students" in message or "how many students" in message:
            total_students = Student.objects.count()
            return JsonResponse({"reply": f"There are {total_students} students in the database."})

        # 5. "marks of John"
        if "marks of" in message:
            name = message.replace("marks of", "").strip()
            student = Student.objects.filter(name__icontains=name).first()
            if student:
                marks = student.mark_set.all()
                if marks.exists():
                    reply = ", ".join([f"{m.subject.name}: {m.marks_obtained}" for m in marks])
                    return JsonResponse({"reply": f"Marks of {student.name}: {reply}"})
                return JsonResponse({"reply": f"{student.name} has no marks recorded."})

        # 6. "subjects of roll no"
        if "subjects of roll" in message:
            try:
                roll_no = int(message.split()[-1])
                student = Student.objects.filter(roll_number=roll_no).first()
                if student:
                    subjects = [m.subject.name for m in student.mark_set.all()]
                    return JsonResponse({"reply": f"Subjects of {student.name}: {', '.join(subjects)}"})
            except ValueError:
                pass

        # 7. Fallback
        total_marks = Mark.objects.count()
        return JsonResponse({"reply": f"There are {total_marks} marks recorded."})

    return JsonResponse({"reply": "Invalid request."})
