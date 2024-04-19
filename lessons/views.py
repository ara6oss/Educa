from django.shortcuts import get_list_or_404, render
from django.core.paginator import Paginator
from lessons.utils import q_search
from lessons.models import Lesson, Category

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
        
    paginator = Paginator(lessons, 6)
    current_page = paginator.page(int(page))
    
    categories = Category.objects.all()
    context = {
        "lessons" : current_page,
        "categories":categories,
        "slug_url" : category_slug,
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