from django.contrib.auth.models import User
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth import login, logout, authenticate
from django.contrib import messages,admin
from .forms import CustomUserCreationForm, CustomAuthenticationForm
from django.contrib.auth.decorators import login_required
from .forms import UserUpdateForm, ProfileUpdateForm 
from django.contrib.auth.decorators import login_required, user_passes_test
from .models import QuizQuestion, QuizTest, QuizAttempt, TrafficRule, Tutorial
from .forms import QuizQuestionForm, QuizTestForm, TrafficRuleForm, TutorialForm, ForgetPasswordForm, ResetPasswordForm
from django.db import models
from django.contrib.auth.hashers import make_password


def landing_page(request):
    return render(request, 'Trafficapp/landing.html')  # Make sure landing.html is in your templates

@login_required
def rules(request):
    rules = TrafficRule.objects.all().order_by("-created_at")
    return render(request, 'Trafficapp/rules.html', {"rules": rules})

@login_required
def tutorials(request):
    tutorials = Tutorial.objects.all().order_by("-created_at")
    print("DEBUG >>> Tutorials count:", tutorials.count())  # 👈 check server logs
    return render(request, "Trafficapp/tutorials.html", {"tutorials": tutorials})

@login_required
@user_passes_test(lambda u: u.is_superuser)
def manage_tutorials(request):
    tutorials = Tutorial.objects.all().order_by("-created_at")
    return render(request, "Trafficapp/manage_tutorials.html", {"tutorials": tutorials})


@login_required
@user_passes_test(lambda u: u.is_superuser)
def add_tutorial(request):
    if request.method == "POST":
        form = TutorialForm(request.POST, request.FILES)
        if form.is_valid():
            tutorial = form.save(commit=False)
            tutorial.added_by = request.user
            tutorial.save()
            messages.success(request, "✅ Tutorial added successfully!")
            return redirect("manage_tutorials")
    else:
        form = TutorialForm()

    return render(request, "Trafficapp/add_tutorial.html", {"form": form})


@login_required
@user_passes_test(lambda u: u.is_superuser)
def delete_tutorial(request, tutorial_id):
    tutorial = get_object_or_404(Tutorial, id=tutorial_id)
    tutorial.delete()
    messages.success(request, "🗑️ Tutorial deleted successfully!")
    return redirect("manage_tutorials")

@login_required
def quiz(request):
    question = QuizQuestion.objects.first()  # just the first one for test
    selected_answer = None
    is_correct = None

    if request.method == "POST":
        selected_answer = request.POST.get("answer")
        if selected_answer == question.correct_answer:
            messages.success(request, "✅ Correct Answer!")
            is_correct = True
        else:
            messages.error(request, "❌ Wrong Answer. Try Again.")
            is_correct = False

    context = {
        "question": question,
        "selected_answer": selected_answer,
        "is_correct": is_correct
    }
    return render(request, "Trafficapp/quiz.html", context)




def signup_view(request):
    if request.method == "POST":
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.set_password(form.cleaned_data['password1'])  # 🔒 Hash password
            user.save()
            login(request, user)  # Auto login after signup
            messages.success(request, "Account created successfully 🚦")
            return redirect("landing")
        else:
            messages.error(request, "Please correct the errors below ❌")
    else:
        form = CustomUserCreationForm()
    return render(request, "Trafficapp/signup.html", {"form": form})


def login_view(request):
    if request.method == "POST":
        form = CustomAuthenticationForm(data=request.POST)
        if form.is_valid():
            user = form.get_user()
            login(request, user)
            messages.success(request, f"Welcome back {user.username}! 👋")

            # Only two roles: admin or normal user
            if user.is_superuser:
                return redirect("admin_dashboard")
            else:
                return redirect("landing")
        else:
            messages.error(request, "Invalid username or password ❌")
    else:
        form = CustomAuthenticationForm()

    return render(request, "Trafficapp/login.html", {"form": form, "hide_navbar": True})

def logout_view(request):
    logout(request)
    messages.info(request, "You have been logged out 👋")
    return redirect("login")

def not_admin(user):
    return not user.is_superuser

# def tutorials(request):
#     return render(request, "Trafficapp/tutorials.html")

def road_signs(request):
    return render(request, "Trafficapp/road_signs.html")

def driving_tips(request):
    return render(request, "Trafficapp/driving_tips.html")

def safety_rules(request):
    return render(request, "Trafficapp/safety_rules.html")

@login_required
def profile(request):
    if request.method == 'POST':
        u_form = UserUpdateForm(request.POST, instance=request.user)
        p_form = ProfileUpdateForm(request.POST, request.FILES, instance=request.user.profile)

        if u_form.is_valid() and p_form.is_valid():
            u_form.save()
            p_form.save()
            messages.success(request, "✅ Your profile has been updated!")
            return redirect('profile')
    else:
        u_form = UserUpdateForm(instance=request.user)
        p_form = ProfileUpdateForm(instance=request.user.profile)

    context = {
        'u_form': u_form,
        'p_form': p_form,
    }

    # ✅ Only show quiz report if the logged-in user is NOT a superuser
    if not request.user.is_superuser:
        quiz_attempts = QuizAttempt.objects.filter(user=request.user)
        if quiz_attempts.exists():
            total_attempts = quiz_attempts.count()
            total_score = sum(a.score for a in quiz_attempts)
            total_possible = sum(a.total for a in quiz_attempts)
            pass_fail = [
                {
                    "title": a.test.title,
                    "score": a.score,
                    "total": a.total,
                    "status": "Pass" if a.score >= a.total * 0.5 else "Fail"
                }
                for a in quiz_attempts
            ]

            context.update({
                'quiz_attempts': quiz_attempts,
                'total_attempts': total_attempts,
                'total_score': total_score,
                'total_possible': total_possible,
                'pass_fail': pass_fail,
            })

    return render(request, 'Trafficapp/profile.html', context)


def is_admin(user):
    return hasattr(user, "profile") and user.profile.role == "admin"

@login_required
@user_passes_test(lambda u: u.is_superuser)
def admin_dashboard(request):
    return render(request, "Trafficapp/admin_dashboard.html")

# Create Normal User
@login_required
@user_passes_test(lambda u: u.is_superuser)
def create_user(request):
    if request.method == "POST":
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.set_password(form.cleaned_data["password"])  # hash password
            user.save()
            messages.success(request, f"✅ User {user.username} created successfully!")
            return redirect("manage_users")
    else:
        form = CustomUserCreationForm()
    return render(request, "Trafficapp/create_user.html", {"form": form})


# Create Admin User
@login_required
@user_passes_test(lambda u: u.is_superuser)
def create_admin(request):
    if request.method == "POST":
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.set_password(form.cleaned_data["password"])  # hash password
            user.is_staff = True
            user.is_superuser = True
            user.save()
            messages.success(request, f"✅ Admin {user.username} created successfully!")
            return redirect("manage_users")
    else:
        form = CustomUserCreationForm()
    return render(request, "Trafficapp/create_admin.html", {"form": form})

# Manage Users
@login_required
@user_passes_test(lambda u: u.is_superuser)
def manage_users(request):
    admins = User.objects.filter(is_superuser=True)
    users = User.objects.filter(is_superuser=False)

    return render(request, "Trafficapp/manage_users.html", {
        "admins": admins,
        "users": users,
    })

# Remove User
@login_required
@user_passes_test(lambda u: u.is_superuser)
def remove_user(request, user_id):
    user = get_object_or_404(User, id=user_id)

    # Don’t allow deleting admins
    if user.is_superuser:
        messages.error(request, "⚠️ You cannot delete another admin!")
        return redirect("manage_users")

    user.delete()
    messages.success(request, f"✅ User '{user.username}' removed successfully.")
    return redirect("manage_users")

# Add Content
@login_required
@user_passes_test(lambda u: u.is_superuser)
def add_content(request):
    return render(request, "Trafficapp/add_content.html")


# Reports
@login_required
@user_passes_test(lambda u: u.is_superuser)
def reports(request):
    return render(request, "Trafficapp/reports.html")

# View User Report (quiz history)
@login_required
@user_passes_test(lambda u: u.is_superuser)
def user_report(request, user_id):
    user = get_object_or_404(User, id=user_id)
    attempts = QuizAttempt.objects.filter(user=user).order_by("-attempted_at")
    return render(request, "Trafficapp/user_report.html", {
        "user": user,
        "attempts": attempts
    })


PASS_MARKS = 6  # threshold

@user_passes_test(not_admin)
@login_required
def quiz_list(request):
    tests = QuizTest.objects.all().order_by("id")
    unlocked_tests = []

    for i, test in enumerate(tests, start=1):
        if i == 1:
            unlocked_tests.append((test, True))  # Test 1 always unlocked
        else:
            prev_test = tests[i - 2]
            attempt = QuizAttempt.objects.filter(user=request.user, test=prev_test).order_by("-score").first()
            if attempt and attempt.score >= 6:  # pass mark
                unlocked_tests.append((test, True))
            else:
                unlocked_tests.append((test, False))

    return render(request, "Trafficapp/quiz_list.html", {"unlocked_tests": unlocked_tests})



@login_required
@user_passes_test(lambda u: u.is_superuser)
def quiz_tests(request):
    if request.method == "POST":
        form = QuizTestForm(request.POST)
        if form.is_valid():
            quiz_test = form.save(commit=False)
            quiz_test.created_by = request.user  # ✅ link admin who creates test
            quiz_test.save()
            messages.success(request, "Quiz test created successfully!")
            return redirect("quiz_tests")
    else:
        form = QuizTestForm()

    tests = QuizTest.objects.all().order_by("-created_at")
    return render(request, "Trafficapp/quiz_tests.html", {"form": form, "tests": tests})



@login_required
@user_passes_test(lambda u: u.is_superuser)
def edit_quiz_test(request, test_id):
    test = get_object_or_404(QuizTest, id=test_id)
    if request.method == "POST":
        title = request.POST.get("title")
        if title:
            test.title = title
            test.save()
            messages.success(request, "✅ Test updated successfully!")
            return redirect("quiz_tests")
    return render(request, "Trafficapp/edit_quiz_test.html", {"test": test})


@login_required
@user_passes_test(lambda u: u.is_superuser)
def delete_quiz_test(request, test_id):
    test = get_object_or_404(QuizTest, id=test_id)
    test.delete()
    messages.success(request, "❌ Test deleted successfully!")
    return redirect("quiz_tests")

@login_required
@user_passes_test(lambda u: u.is_superuser)
def add_quiz_test(request):
    if request.method == "POST":
        form = QuizTestForm(request.POST)
        if form.is_valid():
            test = form.save()
            messages.success(request, "✅ Quiz Test created successfully!")
            return redirect("add_quiz_question", test_id=test.id)  # redirect to add questions
    else:
        form = QuizTestForm()

    tests = QuizTest.objects.all().order_by("-created_at")
    return render(request, "Trafficapp/add_quiz_test.html", {"form": form, "tests": tests})


@login_required
@user_passes_test(lambda u: u.is_superuser)
def quiz_questions(request, test_id):
    test = get_object_or_404(QuizTest, id=test_id)
    questions = test.questions.all().order_by("-created_at")
    return render(request, "Trafficapp/quiz_questions.html", {"test": test, "questions": questions})

@login_required
@user_passes_test(lambda u: u.is_superuser)
def edit_quiz_question(request, test_id, question_id):
    test = get_object_or_404(QuizTest, id=test_id)
    question = get_object_or_404(QuizQuestion, id=question_id, test=test)

    if request.method == "POST":
        form = QuizQuestionForm(request.POST, instance=question)
        if form.is_valid():
            form.save()
            messages.success(request, "✅ Question updated successfully!")
            return redirect("quiz_questions", test_id=test.id)
    else:
        form = QuizQuestionForm(instance=question)

    return render(request, "Trafficapp/edit_quiz_question.html", {"form": form, "test": test})


@login_required
@user_passes_test(lambda u: u.is_superuser)
def delete_quiz_question(request, test_id, question_id):
    test = get_object_or_404(QuizTest, id=test_id)
    question = get_object_or_404(QuizQuestion, id=question_id, test=test)
    question.delete()
    messages.success(request, "❌ Question deleted successfully!")
    return redirect("quiz_questions", test_id=test.id)


@login_required
@user_passes_test(lambda u: u.is_superuser)
def add_quiz_question(request, test_id):
    test = get_object_or_404(QuizTest, id=test_id)

    if request.method == "POST":
        form = QuizQuestionForm(request.POST, request.FILES)   # ✅ include request.FILES
        if form.is_valid():
            question = form.save(commit=False)
            question.test = test
            question.save()
            messages.success(request, "✅ Question added successfully!")
            return redirect("add_quiz_question", test_id=test.id)
    else:
        form = QuizQuestionForm()

    questions = test.questions.all()
    return render(request, "Trafficapp/add_quiz_question.html", {
        "form": form,
        "test": test,
        "questions": questions
    })



# Manage rules (list + button)
@login_required
@user_passes_test(lambda u: u.is_superuser)
def manage_rules(request):
    rules = TrafficRule.objects.all().order_by("-created_at")
    return render(request, "Trafficapp/manage_rules.html", {"rules": rules})

# Add new rule
@login_required
@user_passes_test(lambda u: u.is_superuser)
def add_rule(request):
    if request.method == "POST":
        form = TrafficRuleForm(request.POST, request.FILES)
        if form.is_valid():
            rule = form.save(commit=False)
            rule.added_by = request.user
            rule.save()
            messages.success(request, "✅ Rule added successfully!")
            return redirect("manage_rules")
    else:
        form = TrafficRuleForm()
    return render(request, "Trafficapp/add_rule.html", {"form": form})

# Edit Rule
@login_required
@user_passes_test(lambda u: u.is_superuser)
def edit_rule(request, rule_id):
    rule = get_object_or_404(TrafficRule, id=rule_id)
    if request.method == "POST":
        form = TrafficRuleForm(request.POST, instance=rule)
        if form.is_valid():
            form.save()
            messages.success(request, "✏️ Rule updated successfully!")
            return redirect("manage_rules")
    else:
        form = TrafficRuleForm(instance=rule)
    return render(request, "Trafficapp/edit_rule.html", {"form": form, "rule": rule})

# Delete Rule
@login_required
@user_passes_test(lambda u: u.is_superuser)
def delete_rule(request, rule_id):
    rule = get_object_or_404(TrafficRule, id=rule_id)

    if request.method == "POST":
        rule.delete()
        messages.success(request, "🗑️ Rule deleted successfully!")
        return redirect("manage_rules")

    return render(request, "Trafficapp/delete_rule.html", {"rule": rule})

import random
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .models import QuizQuestion, QuizTest, QuizAttempt

@login_required
def start_quiz(request):
    """Create a test dynamically from 15 random questions."""
    all_questions = list(QuizQuestion.objects.all())
    if len(all_questions) < 15:
        messages.warning(request, "⚠️ Not enough questions in the question bank. Please contact admin.")
        return redirect("landing")

    # Select 15 random questions
    selected_questions = random.sample(all_questions, 15)

    # Create temporary test instance
    test = QuizTest.objects.create(title=f"Auto Test - {request.user.username}")

    # Attach selected questions to this test
    for q in selected_questions:
        q.test = test
        q.save()

    return redirect("take_quiz", test_id=test.id)

@login_required
def take_quiz(request, test_id):
    """Display and evaluate quiz on same page, with safe error handling."""
    test = get_object_or_404(QuizTest, id=test_id)  # ✅ prevents DoesNotExist error
    questions = test.questions.all()
    result_data = None  # default state

    if request.method == "POST":
        score = 0
        total = questions.count()

        for q in questions:
            selected = request.POST.get(str(q.id))
            if selected == q.correct_answer:
                score += 1

        # Save result
        QuizAttempt.objects.create(user=request.user, test=test, score=score, total=total)

        # Calculate result
        percentage = round((score / total) * 100, 2) if total > 0 else 0
        status = "Pass" if score >= 10 else "Fail"

        result_data = {
            "score": score,
            "total": total,
            "percentage": percentage,
            "status": status,
        }

    return render(request, "Trafficapp/take_quiz.html", {
        "test": test,
        "questions": questions,
        "result_data": result_data,
    })
    
        
@login_required
def quiz_result(request, test_id):
    test = get_object_or_404(QuizTest, id=test_id)
    attempt = QuizAttempt.objects.filter(user=request.user, test=test).last()
    percentage = round((attempt.score / attempt.total) * 100, 2)
    status = "Pass" if attempt.score >= 10 else "Fail"

    return render(request, "Trafficapp/quiz_result.html", {
        "attempt": attempt,
        "percentage": percentage,
        "status": status,
    })

def forgot_password(request):
    if request.method == "POST":
        form = ForgetPasswordForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data["username"]
            email = form.cleaned_data["email"]

            try:
                user = User.objects.get(username=username, email=email)
                # Redirect user to reset password page
                return redirect("reset_password", username=user.username)

            except User.DoesNotExist:
                messages.error(request, "Invalid username or email ❌")

    else:
        form = ForgetPasswordForm()

    return render(request, "Trafficapp/forgot_password.html", {"form": form})


def reset_password(request, username):
    user = get_object_or_404(User, username=username)

    if request.method == "POST":
        form = ResetPasswordForm(request.POST)

        if form.is_valid():
            new_password = form.cleaned_data["new_password"]
            confirm_password = form.cleaned_data["confirm_password"]

            if new_password != confirm_password:
                messages.error(request, "Passwords do not match ❌")
            else:
                user.password = make_password(new_password)
                user.save()
                messages.success(request, "Password reset successfully ✔")
                return redirect("login")

    else:
        form = ResetPasswordForm()

    return render(request, "Trafficapp/reset_password.html", {"form": form, "username": username})
