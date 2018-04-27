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

from .models import Project, Step, Test_Result, Step_Result, Project_result
from .threads import WebUiThread, Synchronize_Steps


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
    
    return render(request,'index.html',context={'mess':message,'projects':projects})

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
    message=""
    projects = Project.objects.all().order_by('-name')
    return render(request,'index.html',context={'mess':message,'projects':projects})

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
                oneTest.metrics.add(k)
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
    test_time = 20
    Synchronize_Steps(ste,test_time,class_name)
    
    return render(request,'test.html',context={'mess':message,'latest_results_list':ste,"project_name":project,"project_id":project_id})

def update(request):
    project_result = Project_result.objects.get(project_result_id=project_id)
    steps = Step_Result.objects.all().filter(project_result=project_result).order_by('step_number')
    for i in  steps :
        total_state=[]
        total_progress=0
        k = 0
        for j in i.test_result.all():
            total_state.append(j.state)
            k=k+1
            total_progress = total_progress+int(j.progress)
        
        progress = int(total_progress / k) 
            
        new = ",".join(total_state)
        i.update_state(new)
        i.update_progress(progress)
        
            
     
    results = [ob.as_json() for ob in Step_Result.objects.all().filter(project_result=project_result).order_by('step_number')]
    return JsonResponse({'latest_results_list':results})




    


