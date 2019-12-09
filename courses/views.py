from django.shortcuts import render
from .models import Course, Lesson
from django.shortcuts import render, get_object_or_404
from home.models import UserMembership

# Create your views here.


def cour(request):    
    courses = Course.objects.all()
    return render(request,'courses/hp.html',{'courses':courses})

def less(request,course):    
    lessons = Lesson.objects.filter(course=1)
    courses = Course.objects.filter(title=lessons[0].course.title).first()
    user_membership = get_object_or_404(UserMembership, user=request.user)
    user_membership_type = user_membership.membership.membership_type
    course_allowed_mem_types = courses.allowed_memberships.all()
    context = { 'lessons': None }
    if course_allowed_mem_types.filter(membership_type=user_membership_type).exists():
        context = {'lessons': lessons}
    return render(request,'courses/less.html',context)



