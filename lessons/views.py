from django.shortcuts import get_list_or_404, get_object_or_404, render
from django.core.paginator import Paginator
from django.urls import reverse
from lessons.forms import CommentForm
from lessons.utils import q_search
from lessons.models import Lesson, Category, Module, Comment
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views import View
from django.http import HttpResponseRedirect
from django.shortcuts import redirect
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator
# Create your views here.

# def home (request):
    
    

#     lessons = Lesson.objects.all() 
    
    
#     categories = Category.objects.all()
#     context = {
#         "lessons" : lessons,
#         "categories":categories, 
#     }
    
#     return render(request, 'home.html', context)


def home (request, category_slug='all'):
    
    if request.user.is_authenticated:
        user_comments_count = Comment.objects.filter(author=request.user).count()
    else:
        user_comments_count = 0
    page = request.GET.get('page', 1)
    query = request.GET.get('q', None)
    
    if query:
        lessons = q_search(query)
    
    elif category_slug == 'all':
        lessons = Lesson.objects.all() 
        
    else:
        lessons = get_list_or_404(Lesson.objects.filter(category__slug=category_slug))
        
    if category_slug == 'all':
        current_category = 'all'
        
    else:
        current_category = (lessons[0].category)
        
    paginator = Paginator(lessons, 6)
    current_page = paginator.page(int(page))
    
    categories = Category.objects.all()

    context = {
        "lessons" : current_page,
        "categories":categories,
        "slug_url" : category_slug,
        "current_category": current_category,
        "count": user_comments_count
    }
    
    return render(request, 'home.html', context)

def about(request):
    return render(request, 'about.html')



def course_detail(request, course_slug):
    lesson = Lesson.objects.get(slug=course_slug)
    context = {
        "lesson": lesson
    }
    
    return render(request, 'lessons/playlist.html', context)

def course_posts(request):
    lessons = Lesson.objects.all()
    paginator = Paginator(lessons, 6)
    
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    return render(request, 'home.html', {'page_obj': page_obj})

# def module_detail(request, course_slug, module_slug):
#     lesson = Lesson.objects.get(slug=course_slug)
#     module = lesson.modules.get(slug=module_slug)
    
#     context = {
#         'lesson': lesson,
#         "module": module
#     }
    
#     return render(request, 'lessons/module.html', context)

class AddLike(LoginRequiredMixin, View):
    
    def get(self, request, course_slug, module_slug, *args, **kwargs):
        lesson = get_object_or_404(Lesson, slug=course_slug)
        module = get_object_or_404(Module, lesson=lesson, slug=module_slug)
        context = {
            'lesson': lesson,
            'module': module
        }
        
        return render(request, 'lessons/module.html', context)
    
    
    
    def post(self, request, course_slug, module_slug, *args, **kwargs):
        lesson = get_object_or_404(Lesson, slug=course_slug)
        module = get_object_or_404(Module, lesson=lesson, slug=module_slug)

        is_dislike = False

        for dislike in module.dislikes.all():
            if dislike == request.user:
                is_dislike = True
                break

        if is_dislike:
            module.dislikes.remove(request.user)

        is_like = False

        for like in module.likes.all():
            if like == request.user:
                is_like = True
                break

        if not is_like:
            module.likes.add(request.user)

        if is_like:
            module.likes.remove(request.user)

        return redirect(request.META.get('HTTP_REFERER', '/'))
    
    
class AddDislike(LoginRequiredMixin, View):
    def post(self, request, course_slug, module_slug, *args, **kwargs):
        lesson = get_object_or_404(Lesson, slug=course_slug)
        module = get_object_or_404(Module, lesson=lesson, slug=module_slug)

        is_like = False

        for like in module.likes.all():
            if like == request.user:
                is_like = True
                break

        if is_like:
            module.likes.remove(request.user)

        is_dislike = False

        for dislike in module.dislikes.all():
            if dislike == request.user:
                is_dislike = True
                break

        if not is_dislike:
            module.dislikes.add(request.user)

        if is_dislike:
            module.dislikes.remove(request.user)

        return redirect(request.META.get('HTTP_REFERER', '/'))
    


class ModuleDetailView(View):
    def get(self, request, course_slug, module_slug):
        lesson = Lesson.objects.get(slug=course_slug)
        module = lesson.modules.get(slug=module_slug)
        form = CommentForm
        comments = Comment.objects.filter(module=module).order_by('-created_on')
        
        context = {
            'lesson': lesson,
            'module': module,
            'form': form,
            'comments': comments,
        }
        return render(request, 'lessons/module.html', context)
    
    @method_decorator(login_required)
    def post(self, request, course_slug, module_slug, *args, **kwargs):
        lesson = Lesson.objects.get(slug=course_slug)
        module = lesson.modules.get(slug=module_slug)        
        form = CommentForm(request.POST)
        if form.is_valid():
            new_comment = form.save(commit=False)
            new_comment.author = request.user
            new_comment.module = module
            new_comment.save()
            
            form = CommentForm()
    
        comments = Comment.objects.filter(module=module).order_by('-created_on')

        context = {
            'lesson':lesson,
            'module': module,
            'form': form,
            'comments': comments,
        }

        return render(request, 'lessons/module.html', context)
    
def edit_comment(request, course_slug, module_slug, comment_id):
    if request.method == 'POST':
        lesson = Lesson.objects.get(slug=course_slug)
        module = lesson.modules.get(slug=module_slug)
        comment = Comment.objects.get(pk=comment_id)
        comment_form = CommentForm(instance=comment)
        
        if comment_form.is_valid():
            comment_form.save()
            comment_form.author = request.user
            comment_form.module = module
            comment_form.save()
            
        comments = Comment.objects.filter(module=module).order_by('-created_on')
        
        context = {
            'lesson':lesson,
            'module': module,
            'form': comment_form,
            'comments': comments,
            'comment_id': comment_id,
            'edit': True
        }
        return render(request, 'lessons/module.html', context)
    
    
    
def update_comment(request, course_slug, module_slug, comment_id):
    
    
    if request.method == 'POST':
        lesson = Lesson.objects.get(slug=course_slug)
        module = lesson.modules.get(slug=module_slug)
        comment = Comment.objects.get(pk=comment_id)
        comment_form = CommentForm(request.POST, instance=comment)
        
        
        
        if comment_form.is_valid():
            updated_comment = comment_form.save(commit=False)  # Create a new instance but don't save it yet
            updated_comment.author = request.user
            updated_comment.module = module
            updated_comment.save()  # Save the updated comment
        
        else:
            comment = Comment.objects.get(pk=comment_id)
            comment_form = CommentForm(instance=comment)
        
        comments = Comment.objects.filter(module=module).order_by('-created_on')
    
        context = {
            'lesson':lesson,
            'module': module,
            'form': comment_form,
            'comments': comments,
            'comment_id': comment_id,
            'edit': True
        }
        return redirect(reverse('lesson:module_detail', args=[course_slug, module_slug]))
        
            
    
def delete_comment(request, course_slug, module_slug, comment_id):
    comment = Comment.objects.get(pk=comment_id)
    comment.delete()
    return redirect(reverse('lesson:module_detail', args=[course_slug, module_slug]))

class AddSave(LoginRequiredMixin, View):
    
    def get(self, request, course_slug):
        lesson = get_object_or_404(Lesson, slug=course_slug)
        context = {
            'lesson': lesson
        }
        
        return render(request, 'lessons/playlist.html', context)
    
    def post(self, request, course_slug):
        lesson = get_object_or_404(Lesson, slug=course_slug)
        if lesson.save.filter(id=request.user.id).exists():
            lesson.save.remove(request.user)
        else:
            lesson.save.add(request.user)
        
        context = {
            'lesson': lesson
        }
        # return redirect(request.META.get('HTTP_REFERER', '/'))
        return render(request, 'lessons/playlist.html', context )
    
@login_required
def liked_modules(request):
    if request.method == 'GET':
        user = request.user
        modules = Module.objects.filter(likes=user) 
        context = {
            'modules': modules  
        }
        
        return render(request, 'lessons/liked_modules.html', context)
        
def view_comments(request):
    
    user = request.user
    comments = Comment.objects.filter(author=user)
    
    context = {
        'comments': comments
    }
    
    return render(request, 'lessons/view_comments.html', context)

def saved_playlists(request):
    
    lessons = Lesson.objects.filter(save=request.user)
    
    context = {
        'lessons': lessons
    } 
    return render(request, 'lessons/saved_playlists.html', context)
    
    
        
    
    # if request.method == 'POST':
    #     lesson = Lesson.objects.get(slug=course_slug)
    #     module = lesson.modules.get(slug=module_slug)
    #     comment = Comment.objects.get(pk=comment_id)
    #     comment_form = CommentForm(instance=comment)
        
    #     if comment_form.is_valid():
    #         new_com = comment_form.save()
    #         new_com = comment_form.author = request.user
    #         new_com = comment_form.module = module
    #         new_com = comment_form.save()
    #         comment.comment = new_com.comment
    #         comment.save()
    #         new_com.delete()
    #     comments = Comment.objects.filter(module=module).order_by('-created_on')
        
    #     context = {
    #         'lesson':lesson,
    #         'module': module,
    #         'form': comment_form,
    #         'comments': comments,
    #         'edit': True
    #     }
    #     return render(request, 'lessons/module.html', context)

        

            


    
    # class CommentReplyView(LoginRequiredMixin, View):
    #     def post(self, request, post_pk, pk, *args, **kwargs):
    #         post = Post.objects.get(pk=post_pk)
    #         parent_comment = Comment.objects.get(pk=pk)
    #         form = CommentForm(request.POST)

    #         if form.is_valid():
    #             new_comment = form.save(commit=False)
    #             new_comment.author = request.user
    #             new_comment.post = post
    #             new_comment.parent = parent_comment
    #             new_comment.save()

    #         return redirect('post-detail', pk=post_pk)
    
        