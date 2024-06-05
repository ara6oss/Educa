from django.shortcuts import render, redirect 
from django.contrib import messages
from django.views import View
from django.contrib.auth.views import LoginView, PasswordChangeView, PasswordResetView
from django.contrib.messages.views import SuccessMessageMixin
from django.urls import reverse_lazy
from django.contrib.auth.decorators import login_required
from students.models import Profile
from lessons.models import Comment, Lesson
from .forms import LoginForm, RegisterForm, UpdateProfileForm, UpdateUserForm

# Create your views here.

@login_required
def profile(request):
    user_comments_count = Comment.objects.filter(author=request.user).count()
    context = {
        'count': user_comments_count
    }
    return render(request, 'students/profile.html', context)


@login_required
def update_profile(request):
    if request.method == 'POST':
        user_form = UpdateUserForm(request.POST, instance=request.user)
        profile_form = UpdateProfileForm(request.POST, request.FILES, instance=request.user.profile)

        if user_form.is_valid() and profile_form.is_valid():
            user_form.save()
            profile_form.save()
            messages.success(request, 'Your profile is updated successfully')
            return redirect(to='profile')
    else:
        user_form = UpdateUserForm(instance=request.user)
        profile_form = UpdateProfileForm(instance=request.user.profile)
    return render(request, 'students/update.html', {'user_form': user_form, 'profile_form': profile_form})

from django.contrib.auth.models import User

def owner_profile(request, pk):
    if request.method == 'GET':
        owner = User.objects.get(pk=pk)
        user_comments_count = Comment.objects.filter(author=owner).count()
        context = {
        'owner': owner,
        'count': user_comments_count
        }
        return render(request, 'students/owner_profile.html', context)        








class RegisterView(View):
    form_class = RegisterForm
    initial = {'key': 'value'}
    template_name = 'students/register.html'

    def get(self, request, *args, **kwargs):
        form = self.form_class(initial=self.initial)
        return render(request, self.template_name, {'form': form})

    def post(self, request, *args, **kwargs):
        form = self.form_class(request.POST)

        if form.is_valid():
            form.save()

            username = form.cleaned_data.get('username')
            messages.success(request, f'Account created for {username}')

            return redirect(to='/login')

        return render(request, self.template_name, {'form': form})
    
    def dispatch(self, request, *args, **kwargs):
        # will redirect to the home page if a user tries to access the register page while logged in
        if request.user.is_authenticated:
            return redirect(to='/')

        # else process dispatch as it otherwise normally would
        return super(RegisterView, self).dispatch(request, *args, **kwargs)
    
class CustomLoginView(LoginView):
    form_class = LoginForm
    authentication_form = LoginForm
    redirect_authenticated_user = True
    template_name = 'students/login.html'
    def form_valid(self, form):
        remember_me = form.cleaned_data.get('remember_me')

        if not remember_me:
            # set session expiry to 0 seconds. So it will automatically close the session after the browser is closed.
            self.request.session.set_expiry(0)

            # Set session as modified to force data updates/cookie to be saved.
            self.request.session.modified = True

        # else browser session will be as long as the session cookie time "SESSION_COOKIE_AGE" defined in settings.py
        return super(CustomLoginView, self).form_valid(form)
    
class ResetPasswordView(SuccessMessageMixin, PasswordResetView):
    template_name = 'students/password_reset.html'
    email_template_name = 'students/password_reset_email.html'
    subject_template_name = 'students/password_reset_subject.txt'
    success_message = "We've emailed you instructions for setting your password, " \
                      "if an account exists with the email you entered. You should receive them shortly." \
                      " If you don't receive an email, " \
                      "please make sure you've entered the address you registered with, and check your spam folder."
    success_url = reverse_lazy('home')
    
class ChangePasswordView(SuccessMessageMixin, PasswordChangeView):
    template_name = 'students/change_password.html'
    success_message = "Successfully Changed Your Password"
    success_url = reverse_lazy('home')
    
    
def teachers_profile1(request):
    teachers = Profile.objects.filter(status='teacher')
    lessons = Lesson.objects.all()
    #найти уроки по пользователю который в teachers и передать через словарь
    
    teacher_lesson_counts = {
        teacher.user.id: Lesson.objects.filter(owner=teacher.user).count()
        for teacher in teachers
    }
    teacher_module_counts = {}

    for teacher in teachers:
        # Find lessons taught by the current teacher
        lessons_taught = Lesson.objects.filter(owner=teacher.user)
        
        # Calculate the total module count for the current teacher
        total_module_count = sum(lesson.modules.count() for lesson in lessons_taught)
        
        # Store the total module count in the dictionary
        teacher_module_counts[teacher.user.id] = total_module_count
        
        
        #TODO to finish
        total_likes_count = sum(module.likes.count() for lesson in lessons_taught for module in lesson.modules.all())
    
    
    context = {
        "teachers": teachers,
        "lessons": lessons,
        "teacher_lesson_counts": teacher_lesson_counts,
        "teacher_module_counts": teacher_module_counts
    }
    return render(request, "teachers.html", context)


def teachers(request):
    teachers = Profile.objects.filter(status='teacher')
    
    # Initialize an empty dictionary to store various counts for each teacher
    teacher_counts = {}

    for teacher in teachers:
        # Find lessons taught by the current teacher
        lessons_taught = Lesson.objects.filter(owner=teacher.user)
        
        # Calculate the total counts for the current teacher
        total_lesson_count = lessons_taught.count()
        total_module_count = sum(lesson.modules.count() for lesson in lessons_taught)
        total_likes_count = sum(module.likes.count() for lesson in lessons_taught for module in lesson.modules.all())
        
        # Store the counts in the dictionary
        teacher_counts[teacher.user.id] = {
            'total_lesson_count': total_lesson_count,
            'total_module_count': total_module_count,
            'total_likes_count': total_likes_count
        }
    
    context = {
        "teachers": teachers,
        "teacher_counts": teacher_counts
    }
    return render(request, "teachers.html", context)

def teacher_profile(request, id):
    user = User.objects.get(pk=id)
    teacher = Profile.objects.get(user=user)
    lessons = Lesson.objects.filter(owner=user)
    total_lesson_count = lessons.count()
    total_module_count = sum(lesson.modules.count() for lesson in lessons)
    total_likes_count = sum(module.likes.count() for lesson in lessons for module in lesson.modules.all())
    total_comment_count = sum(Comment.objects.filter(module=module).count() for lesson in lessons for module in lesson.modules.all())
    context = {
        'teacher': teacher,
        'lessons': lessons,
        'total_lesson_count': total_lesson_count,
        'total_module_count': total_module_count,
        'total_likes_count': total_likes_count,
        'total_comment_count': total_comment_count
    }
    return render(request, 'students/teacher_profile.html', context)

def courses(request):
    lessons = Lesson.objects.all()
    context = {
        'lessons': lessons
    }
    return render(request, 'courses.html', context)