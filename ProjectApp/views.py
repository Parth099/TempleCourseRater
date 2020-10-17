from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.forms import inlineformset_factory
from .models import *
from .forms import *

ACCT = [['ACCT 2101', 'Financial Accounting'], ['ACCT 2102', 'Managerial Accounting'], ['ACCT 2501', 'Survey of Accounting'], ['ACCT 2521', 'Cost Accounting'], ['ACCT 2901', 'Honors Financial Accounting'], ['ACCT 2902', 'Honors Managerial Accounting'], ['ACCT 3511', 'Intermediate Accounting I'], ['ACCT 3512', 'Intermediate Accounting II'], ['ACCT 3526', 'Accounting Information Systems'], ['ACCT 3531', 'Federal Taxes on Income'], ['ACCT 3533', 'Advanced Accounting'], ['ACCT 3561', 'International Accounting'], ['ACCT 3580', 'Special Topics - Accounting'], ['ACCT 3581', 'Co-operative Experience in Accounting'], ['ACCT 3582', 'Independent Study'], ['ACCT 3596', 'Auditing'], ['ACCT 3911', 'Honors Intermediate Accounting I'], ['ACCT 3999', 'Honors Thesis I'], ['ACCT 4501', 'Accounting Senior Seminar'], ['ACCT 4502', 'Senior Seminar - Management Accounting'], ['ACCT 4999', 'Honors Senior Thesis II']]
def inputDB():
    #CourseID Program CourseName
    for i in ACCT:
        i_0 = i[0].split(" ")
        C = Course(CourseID=i_0[1],Program=i_0[0],CourseName=i[1])
        C.save()

def index(request):
    form = CourseForm()
    if request.method == "POST":
        form = CourseForm(request.POST)
        if form.is_valid():
            try:
                P0 = request.POST['Program'].upper()
                C = Course.objects.get(CourseID=request.POST['CourseID'].upper(), Program=P0)
                errMSG = ""
                return redirect(f'/{C.Program}/{C.CourseID}')
            except:
                pass
        return redirect('/')
    context = {'form':form}
    return render(request, 'ProjectApp/index.html', {'form':form})

def CoursePage(request, dept, Id):
    #print(dept, Id)
    C = Course.objects.get(CourseID=Id, Program=dept)
    OrderFormSet = inlineformset_factory(Course, Comments, fields=('comment','course','rating'), extra=1)
    formset = OrderFormSet(queryset=Comments.objects.none(),instance=C)
    if request.method == "POST":
        #print("P:", request.POST)
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
    print(comment_Count)

    if comment_Count == 0:
        RatingSum = "None"
    else:
        RatingSum = round(RatingSum/comment_Count, 2)

    print(comments)
    context = {
        "name" : C.CourseName,
        "id_0" : C.CourseID,
        "dept" : C.Program,
        "form" : formset,
        'zip': zip(comments, times, rate),
        "Avg": RatingSum,
    }
    print(zip(comments, times))
    return render(request, 'ProjectApp/C_page.html', context)