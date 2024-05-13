from django.shortcuts import get_list_or_404, get_object_or_404, render
from django.core.paginator import Paginator
from lessons.forms import CommentForm
from lessons.utils import q_search
from lessons.models import Lesson, Category, Module, Comment
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views import View
from django.http import HttpResponseRedirect
from django.shortcuts import redirect
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
    
    page = request.GET.get('page', 1)
    query = request.GET.get('q', None)
    print("q ", query)
    
    if query:
        lessons = q_search(query)
        print("ARAAAAAAAAAAAAA")
    
    elif category_slug == 'all':
        lessons = Lesson.objects.all() 
        print('BABLO')
        
    else:
        lessons = get_list_or_404(Lesson.objects.filter(category__slug=category_slug))
        
    if lessons:
        current_category=(lessons[0].category)
        
    else:
        current_category=None
        
    paginator = Paginator(lessons, 6)
    current_page = paginator.page(int(page))
    
    categories = Category.objects.all()
    context = {
        "lessons" : current_page,
        "categories":categories,
        "slug_url" : category_slug,
        "current_category": current_category
    }
    
    return render(request, 'home.html', context)




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