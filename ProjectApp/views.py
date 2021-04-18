from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.forms import inlineformset_factory
from .filters import CourseFilter
from .models import *
from .forms import *

from django.db import connection
cursor = connection.cursor()

ACCT = [['ACCT 2101', 'Financial Accounting'], ['ACCT 2102', 'Managerial Accounting'], ['ACCT 2501', 'Survey of Accounting'], ['ACCT 2521', 'Cost Accounting'], ['ACCT 2901', 'Honors Financial Accounting'], ['ACCT 2902', 'Honors Managerial Accounting'], ['ACCT 3511', 'Intermediate Accounting I'], ['ACCT 3512', 'Intermediate Accounting II'], ['ACCT 3526', 'Accounting Information Systems'], ['ACCT 3531', 'Federal Taxes on Income'], ['ACCT 3533', 'Advanced Accounting'], ['ACCT 3561', 'International Accounting'], ['ACCT 3580', 'Special Topics - Accounting'], ['ACCT 3581', 'Co-operative Experience in Accounting'], ['ACCT 3582', 'Independent Study'], ['ACCT 3596', 'Auditing'], ['ACCT 3911', 'Honors Intermediate Accounting I'], ['ACCT 3999', 'Honors Thesis I'], ['ACCT 4501', 'Accounting Senior Seminar'], ['ACCT 4502', 'Senior Seminar - Management Accounting'], ['ACCT 4999', 'Honors Senior Thesis II']]
def inputDB():
    #CourseID Program CourseName
    for i in ACCT:
        i_0 = i[0].split(" ")
        C = Course(CourseID=i_0[1],Program=i_0[0],CourseName=i[1])
        C.save()

def CoursePage(request, dept, Id):

    C = Course.objects.get(CourseID=Id, Program=dept)
    OrderFormSet = inlineformset_factory(Course, Comments, fields=('comment','course','rating'), extra=1)
    formset = OrderFormSet(queryset=Comments.objects.none(),instance=C)
    if request.method == "POST":
        srcBar = request.POST.get('SearchBar', "")
        if srcBar != "":
            return searchCourses(request, srcBar)
        formset = OrderFormSet(request.POST, instance=C)
        if formset.is_valid(): 
            formset.save()
        return redirect(f"/{dept}/{Id}")

    RatingSum = 0
    try:
        comments = C.comments_set.all()
        times = []
        rate = []
        for k in C.comments_set.all():
            times.append(k.date_created.strftime("%I:%M  %m/%d/%Y"))
            rate.append(k.rating)
            RatingSum += k.rating
    
    except:
        comments = ""
        times = ''

    comment_Count = C.comments_set.all().count()
    
    if comment_Count == 0:
        RatingSum = "None"
    else:
        RatingSum = round(RatingSum/comment_Count, 2)

    context = {
        "name" : C.CourseName,
        "id_0" : C.CourseID,
        "dept" : C.Program,
        "form" : formset,
        'zip': zip(comments, times, rate),
        "Avg": RatingSum,
    }

    return render(request, 'ProjectApp/C_page.html', context)

def searchCourses(request, query):
    print("HI")
    C = Course.objects.all()
    output = []
    for course in C:
        if query.lower() in course.CourseName.lower():
            output.append(course)

    SET = C.filter(Program=query) | C.filter(CourseID=query)
    if SET.count() > 0:
        for c in SET:
            output.append(c)
    
    if request.method == "POST":
        srcBar = request.POST.get('SearchBar', "")
        if srcBar != "":
            return redirect(f"/search/{srcBar}")

    return render(request, "ProjectApp/search.html" ,{"output":output, "Q": query, "key":len(output)})

def index(request): #STD page

    CoursesArray = Course.objects.all()
    init_count = len(CoursesArray)
    # print(request.GET)
    program= request.GET.get('Program')
    courseid = request.GET.get('CourseID')
    # ProgramAPPX= request.GET.get('ProgramAPPX')
    # CourseNumA= request.GET.get('CourseNumA')
    # CourseNumB= request.GET.get('CourseNumB')

    CFilter = CourseFilter(request.GET, queryset=CoursesArray)
    CoursesArray = CFilter.qs

    # print(CoursesArray)

    CoursesArray2 = []
    if (program is not None and courseid is not None):
        if (len(program) != 0 and len(courseid) != 0):
            sqlstatement = "SELECT * FROM ProjectApp_course WHERE Program LIKE %" + program +"% AND CourseID=" + courseid
        elif (len(courseid) != 0 and len(program) == 0):
            sqlstatement = "SELECT * FROM ProjectApp_course WHERE CourseID=" + courseid
        elif (len(program) != 0 and len(courseid) == 0):
            sqlstatement = "SELECT * FROM ProjectApp_course WHERE Program LIKE %"  + program + "%"
        else:
            sqlstatement = "SELECT * FROM ProjectApp_course"


        print("\n\n\n" + sqlstatement+  "\n\n")

        for c in Course.objects.raw(sqlstatement):
            CoursesArray2.append(c)

    # print(CoursesArray2)

    final_count = len(CoursesArray2)
    # flag =  final_count if final_count > 0 and final_count != init_count else 0
    flag = 1
    #pass in to render

    context = {
                'form':CFilter,
                'query': CoursesArray2,
                'flag': flag if final_count > 0 else -1,
    }
    return render(request, 'ProjectApp/index.html', context)




'''
#defunct searching

def index(request):
    form = CourseForm()
    if request.method == "POST":
        srcBar = request.POST.get('SearchBar', "")
        if srcBar != "":
            return searchCourses(request, srcBar)
        form = CourseForm(request.POST)
        if form.is_valid():
            if request.POST.get('CourseName', "") == "":
                try:
                    P0 = request.POST['Program'].upper()
                    C = Course.objects.get(CourseID=request.POST['CourseID'].upper(), Program=P0)
                    return redirect(f'/{C.Program}/{C.CourseID}')
                except:
                    pass
            else:
                try:
                    C = Course.objects.get(CourseName=request.POST['CourseName'])
                    return redirect(f'/{C.Program}/{C.CourseID}')
                except:
                    var = request.POST['CourseName']
                    return redirect(f'/search/{var}')

        
        return redirect('/')
    context = {'form':form,}
    return render(request, 'ProjectApp/index.html', {'form':form})
'''
