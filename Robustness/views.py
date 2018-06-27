from _tracemalloc import start
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from django.shortcuts import redirect
from django.shortcuts import render
from django.template import RequestContext
import os
import subprocess
import time
import time
import json
from django.http import HttpResponse
from .models import Project, Step, Test_Result, Step_Result, Project_result,Metric_Result,Test,Config_time
from .threads import WebUiThread, Synchronize_Steps
import datetime
from _mysql import result




@login_required(login_url='/accounts/login/')
def dashbord(request):
    
    if request.is_ajax():
        for key, value in request.POST.items():
            print(key,value)
            if key == "project":
                project_id = value
                print(project_id)
            results = [ob.as_json() for ob in Step_Result.objects.all()]
            print(results)
            return JsonResponse({'all_tests':results})
        
        
        
    for key, value in request.POST.items():
        if key == "project":
            project_id = value
            print(project_id)
    
    executed_project = Project_result.objects.get(project_result_id=project_id)
    steps = Step_Result.objects.all().filter(project_result=executed_project).order_by('step_number')

    return render(request,'dashbord.html',context={'steps_result':steps})

"""
def update_dashbord(request):
    results = [ob.as_json() for ob in Step_Result.objects.all()]
    print(results)
    return JsonResponse({'all_tests':results})
    
"""

# Create your views here.
# verify if service is running 
def is_service_running(name):
    with open(os.devnull, 'wb') as hide_output:
        exit_code = subprocess.Popen(['service', name, 'status'], stdout=hide_output, stderr=hide_output).wait()
        return exit_code == 0
    
    
    
@login_required(login_url='/accounts/login/')
def login_success(request):
    if not is_service_running('elasticsearch'):
        # uncomment this to be show when ElasticSearch is not runnig
        #message="Elasticseach is not runnning! please contact the adminnistrator"
        message=""
    projects = Project.objects.all().order_by('-name')
    return render(request,'index.html',context={'projects':projects})


@login_required(login_url='/accounts/login/')
def save(request):
    if request.is_ajax():
        data = json.loads(request.POST.get('json_items'))
        timer  = json.loads(request.POST.get('time'))
        print(timer[0])
        
        for key, value in timer[0].items():
            if key == "hour" :
                hour = value
            if key == "minute" :
                minute = value
            if key == "second" :
                second = value
                
        new = datetime.time(int(hour),int(minute),int(second))
        Config_time.objects.filter(name="test_time").update(test_time=new)
        
        Step.objects.all().delete()
        count = 0
        for i in data:
            tests = get_step_tests(i)
            if len(tests) == 0 :
                continue
            

            #creation of steps and tests tables  
            description_step = ",".join(tests)
            count = count + 1  
            test_name = "Step_"+str(count)  
            oneStep = Step(name=test_name,step_number=count,description=description_step)
            oneStep.save()
            for j in tests : 
                oneTest = Test.objects.get(name=j)
                oneStep.tests.add(oneTest)
              
        return HttpResponse("OK")



@login_required(login_url='/accounts/login/')
def after_login(request):
    keys = []
    global project 
    for key, value in request.POST.items():
        keys.append(key) 
        #print(keys)
        if key == "project":
            project = value
    #print(keys) 
    
    if "Start_Test" in keys:
        return start_test(request)
            
    if "Configure" in keys:
        return configure_test(request)
    
    message=""
    projects = Project.objects.all().order_by('-name')
    return render(request,'index.html',context={'mess':message,'projects':projects})



@login_required(login_url='/accounts/login/')
def configure_test(request):

    steps = Step.objects.all().order_by('step_number')
    test_time = Config_time.objects.all()[0].test_time
    print(test_time)
    
    return render(request,'configure.html',context={'steps':steps ,'test_time':str(test_time)})



@login_required(login_url='/accounts/login/')
def start_test(request):
    message = "Test Page"
    steps = Step.objects.all().order_by('-name')
    keys = []
    for key, value in request.POST.items():
        keys.append(key)
    # Project ID format : Name + time of the execution 
    current_time = time.localtime()
    now = time.strftime('%d-%m-%YT%H:%M:%S', current_time)
    global project_id
    project_id = project+"_"+now 
    project_result = Project_result(project_result_id = project_id)
    project_result.save()
    class_name = Project.objects.get(name = project).classe.name
    for i in steps :
        test_list = []
        state_list = [] 
        test_list_name = []
        for j in i.tests.all() :
            #creating tests
            metric_list = j.metrics.all()
            oneTest  = Test_Result(name = j.name)
            oneTest.save()
            print(metric_list)
            print(oneTest.test_id)            
            for k in metric_list:
                oneMetricResult  = Metric_Result(name = k.name,test_name=j.name,step_name=i.name,project_name=project_result.project_result_id)
                oneMetricResult.save()
                oneTest.metrics.add(oneMetricResult)
                
            test_list.append(oneTest)
            test_list_name.append(oneTest.name)
            state_list.append("Unfinished")
            # starting test ( function to start one test )
            #test_starter(i,class_name,oneTest)
        description_step = ",".join(test_list_name)
        state_step = ','.join(state_list)    
        #creating steps
        oneStep = Step_Result(project_result=project_result ,state = state_step,name=i.name,description=description_step,step_number=i.step_number)
        oneStep.save()
        for j in test_list:
           oneStep.test_result.add(j)

    # Sending all steps to the front          
    ste = Step_Result.objects.all().filter(project_result=project_result).order_by('step_number')    
    # Synchronize_Steps a deamon that synchronize all tests in the steps
    # time to execute one tests (step)
    a = Config_time.objects.all().filter(name="test_time")[0].test_time
    test_time=(a.hour*3600+a.minute*60+a.second)
    test_time = 14400
    Synchronize_Steps(ste,test_time,class_name)
    
    return render(request,'test.html',context={'mess':message,'latest_results_list':ste,"project_name":project,"project_id":project_result.project_result_id,"project_id":project_id})

def update(request):
    project_result = Project_result.objects.get(project_result_id=project_id)
    steps = Step_Result.objects.all().filter(project_result=project_result).order_by('step_number')
    for i in  steps :
        total_state=[]
        total_progress=0
        k = 0
        metric_list = []
        for j in i.test_result.all():
            total_state.append(j.state)
            k=k+1
            total_progress = total_progress+int(j.progress)
            b = j.metrics.all()
            for d in b :
                metric_list.append(d.name+": "+d.values)
        
        progress = int(total_progress / k) 
        
        new_metric = ",".join(metric_list)
        print(new_metric)
        new = ",".join(total_state)
        i.update_state(new)
        i.update_progress(progress)
        i.update_metrics(new_metric)
        
            
     
    results = [ob.as_json() for ob in Step_Result.objects.all().filter(project_result=project_result).order_by('step_number')]
    return JsonResponse({'latest_results_list':results})


def get_step_name(data):
    for key, value in data.items():
        if key == "Name":
            return(value)
    return None

def get_step_tests(data):
    tests=[]
    for key, value in data.items():
        if key == "Tests" :
            #print(value)
            for j in value : 
                for key1, value1 in j.items():
                    tests.append(value1)
               
    return tests


                

    


