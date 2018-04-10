from django.shortcuts import render
from django.shortcuts import redirect
from django.contrib.auth.decorators import login_required
from django.template import RequestContext
import os
import subprocess
from .models import Project, Step,Test_Result,Step_Result,Project_result
from _tracemalloc import start
from django.http import JsonResponse
import time
import threading
import time



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
    
    for i in steps :
        #test_list = [ob for ob in i.tests]
        test_list = [] 
        test_list_name = []
        for j in i.tests.all() :
            metric_list = j.metrics.all()
            #print(metric_list)
            oneTest  = Test_Result(name = j.name)
            oneTest.save()
            print(metric_list)
            
            for k in metric_list:
                #oneMetric = Metric.objects.get(name=)
                oneTest.metrics.add(k)
            
            test_list.append(oneTest)
            test_list_name.append(oneTest.name)
            
        description_step = ",".join(test_list_name)
        
        oneStep = Step_Result(project_result=project_result ,name=i.name,description=description_step,step_number=i.step_number)
        oneStep.save()
        for j in test_list:
           oneStep.test_result.add(j)   
    ste = Step_Result.objects.all().filter(project_result=project_result).order_by('step_number')
    
    #example = ThreadingExample()
    return render(request,'test.html',context={'mess':message,'latest_results_list':ste,"project_name":project})

def update(request):
    project_result = Project_result.objects.get(project_result_id=project_id)
    results = [ob.as_json() for ob in Step_Result.objects.all().filter(project_result=project_result).order_by('step_number')]
    return JsonResponse({'latest_results_list':results})

class ThreadingExample(object):
    """ Threading example class
    The run() method will be started and it will run in the background
    until the application exits.
    """

    def __init__(self, interval=1):
        """ Constructor
        :type interval: int
        :param interval: Check interval, in seconds
        """
        self.interval = interval

        thread = threading.Thread(target=self.run, args=())
        thread.daemon = True                            # Daemonize thread
        thread.start()                                  # Start the execution

    def run(self):
        """ Method that runs forever """
        i=0
        while i<200:
            # Do something
            print('Doing something imporant in the background')

            time.sleep(self.interval)
            i=i+1



