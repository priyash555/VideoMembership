from django.shortcuts import render
from .models import Course, Lesson
from django.shortcuts import render, get_object_or_404
from home.models import UserMembership

# Create your views here.


def cour(request):    
    courses = Course.objects.all()
    return render(request,'courses/hp.html',{'courses':courses})

def less(request,course):    
    courses = Course.objects.filter(slug=course).first()
    print(courses)
    lessons = Lesson.objects.filter(course=courses)
    user_membership = get_object_or_404(UserMembership, user=request.user)
    user_membership_type = user_membership.membership.membership_type
    course_allowed_mem_types = courses.allowed_memberships.all()
    context = { 'lessons': None,
               'membership':course_allowed_mem_types,
               'havemem': 'true' }
    if course_allowed_mem_types.filter(membership_type=user_membership_type).exists() or course_allowed_mem_types.filter(membership_type='Free').exists():
        context = {'lessons': lessons,
                    'membership':course_allowed_mem_types,
                    'havemem': 'true'}
    else:
        lessons = Lesson.objects.filter(position=1,course=courses)
        context = {'lessons': lessons,
                    'membership':course_allowed_mem_types,
                    'havemem': 'false'}
    print(context)
    return render(request,'courses/less.html',context)



