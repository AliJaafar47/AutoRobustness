from apt_pkg import Description
from django.db import models
from django.template.defaultfilters import default
from django.urls import reverse  # Used to generate URLs by reversing the URL patterns
import uuid
from datetime import datetime


# Create your models here.
class Class(models.Model):
    name = models.CharField(max_length=200, unique=True,help_text="Name of Project class") 

    def __str__(self):
        return self.name
    
    def save_project(self):
        if self.name_present(self.name):
            print("Name exists")
            return (Class.objects.get(name=self.name))
        else :
            print("Name don't exist")
            self.save()
            return self
    def name_present(self,name):
        if Class.objects.filter(name=name).exists():
            return True
        return False


class Metric(models.Model):
    THROUGHPUT = 'THROUGHPUT'
    PACKET_LOSS = 'PACKET_LOSS'
    NUMBER_OF_CONNECTIONS = 'NUMBER_OF_CONNECTION'
    PESQ_UPSTREAM =  'PESQ_UPSTREAM'
    PESQ_DOWNSTREAM = "PESQ_DOWNSTREAM"
    ONE_WAY_DELAY_UPSTREAM = "ONE_WAY_DELAY_UPSTREAM"
    ONE_WAY_DELAY_DOWNSTREAM = "ONE_WAY_DELAY_DOWNSTREAM"
    NA="N/A"
    CPU_USAGE = 'CPU_USAGE'
    MEMORY_USAGE= 'MEMORY_USAGE'
    
    METRICS_CHOICES = ((THROUGHPUT, 'THROUGHPUT'),(PACKET_LOSS, 'PACKET_LOSS'),(NUMBER_OF_CONNECTIONS, 'NUMBER_OF_CONNECTIONS'),(PESQ_UPSTREAM, 'PESQ_UPSTREAM'),(PESQ_DOWNSTREAM, 'PESQ_DOWNSTREAM'),(ONE_WAY_DELAY_UPSTREAM, 'ONE_WAY_DELAY_UPSTREAM'),(ONE_WAY_DELAY_DOWNSTREAM, 'ONE_WAY_DELAY_DOWNSTREAM'),(NA, 'N/A'),(CPU_USAGE,'CPU_USAGE'),(MEMORY_USAGE,'MEMORY_USAGE'))
    name = models.CharField(max_length=100,unique=True, choices=METRICS_CHOICES)
    values = models.CharField(max_length=5000,default="N/A",help_text="Value of one Metric") 
    
    
    def update_values(self,new_values):
        Metric.objects.filter(id=self.id).update(values = str(new_values))

    
    
    
    
    def __str__(self):
        return self.name
    
    
    
    
class Metric_Result(models.Model):
    name = models.CharField(max_length=100)
    values = models.CharField(max_length=60000,default="0",help_text="Values of one Metric") 
    list_of_values = models.CharField(max_length=5000,default="",help_text="Values of one Metric")
    project_name = models.CharField(max_length=100)
    gateway_name = models.CharField(max_length=100,default="Generic2")
    step_name = models.CharField(max_length=100)
    test_name = models.CharField(max_length=100)
    execution_date=models.DateTimeField(default=datetime.now())
    
    def update_values(self,new_values):
        Metric_Result.objects.filter(id=self.id).update(values = str(new_values))

    def add_all_values (self,new_values):
        Metric_Result.objects.filter(id=self.id).update(list_of_values = str(new_values))
        
    def add_new_value (self,new_values):
        a = Metric_Result.objects.get(id=self.id)
        ch = a.list_of_values
        new = str(new_values) + ','+ch
        Metric_Result.objects.filter(id=self.id).update(list_of_values = str(new))
        
    def __str__(self):
        return (self.project_name+" "+" "+self.step_name +" "+self.test_name+" "+self.name)
    
    
    
    
class Project(models.Model):
    classe = models.ForeignKey('Class', on_delete=models.SET_NULL, null=True)
    name = models.CharField(max_length=200,unique=True, help_text="Name of project")

    def __str__(self):
         
        return self.name
    
    def save_project(self):
        if self.name_present(self.name):
            print("Name exists")
            return (Project.objects.get(name=self.name))
        else :
            print("Name don't exist")
            self.save()
            return self
            
        
    def name_present(self,name):
        if Project.objects.filter(name=name).exists():
            return True
        return False
    
    

    
    
class Test(models.Model):
    #name = models.CharField(max_length=200,unique=True,help_text="Name of the Test")  
    description = models.CharField(max_length=5000,help_text="Short Description for Test ")
    VOIP_TEST = 'VoIP'
    DATA_LAN_LAN = 'DATA_LAN_LAN'
    DATA_LAN_WLAN_2_4_Ghz = 'DATA_LAN_WLAN_2_4_Ghz'
    DATA_LAN_WLAN_5_Ghz = 'DATA_LAN_WLAN_5_Ghz'
    DATA_WAN_WLAN_5_Ghz = 'DATA_WAN_WLAN_5_Ghz'
    P2P_WLAN_5_Ghz = "P2P_WLAN_5_Ghz"
    
    IPTV_WLAN_5_Ghz_1 = "1xIPTV_WLAN_5_Ghz"
    IPTV_WLAN_5_Ghz_2 = "2xIPTV_WLAN_5_Ghz"
    IPTV_LAN = "2xIPTV_LAN"
    
    WEBUI = "WEBUI"
    TEST_CHOICES = ((VOIP_TEST, 'VoIP'),(DATA_LAN_LAN, 'DATA_LAN_LAN'),(DATA_LAN_WLAN_2_4_Ghz, 'DATA_LAN_WLAN_2_4_Ghz'),(DATA_LAN_WLAN_5_Ghz, 'DATA_LAN_WLAN_5_Ghz'),(DATA_WAN_WLAN_5_Ghz, 'DATA_WAN_WLAN_5_Ghz'),(IPTV_WLAN_5_Ghz_1, '1xIPTV_WLAN_5_Ghz'),(IPTV_WLAN_5_Ghz_2, '2xIPTV_WLAN_5_Ghz'),(P2P_WLAN_5_Ghz, 'P2P_WLAN_5_Ghz'),(IPTV_LAN, '2xIPTV_LAN'),(WEBUI, 'WEBUI'))
    name = models.CharField(max_length=50,unique=True, choices=TEST_CHOICES)
    metrics = models.ManyToManyField(Metric) 
    
    def __str__(self):
        return self.name
    

    
class Step(models.Model):

    name = models.CharField(max_length=200, help_text="Name of the Step",unique=True)
    description = models.CharField(max_length=5000,help_text="Short Description for Test")
    step_number = models.IntegerField(unique=True,help_text="Number Of Step")
    tests = models.ManyToManyField(Test) 
    
    def as_json(self):
        return {
            "name": self.name,
            "description":self.description,
            "step_number":self.step_number,
            "tests" : self.name,
            }
        
class Project_result(models.Model):
    project_result_id = models.CharField(max_length=200,unique=True, help_text="ID")
    gateway_name = models.CharField(max_length=200,help_text="Gateway Name",default="Generic2")
    
    def __str__(self):
        return self.project_result_id
        
class Test_Result(models.Model):
    name = models.CharField(max_length=200, help_text="Name of the Test ")
    test_id = models.AutoField(primary_key=True)
    state = models.CharField(max_length=200, help_text="State",default="Unfinished")
    metrics = models.ManyToManyField(Metric_Result)
    progress = models.CharField(max_length=200, help_text="progress",default="0")
    
    def __str__(self):
        return self.name
    
class Step_Result(models.Model):
    project_result = models.ForeignKey('Project_result', on_delete=models.SET_NULL, null=True)
    test_result = models.ManyToManyField(Test_Result)
    name = models.CharField(max_length=200, help_text="Name of the Step")
    description = models.CharField(max_length=5000,help_text="Short Description for Test")
    step_number = models.IntegerField(help_text="Number Of Step")
    state = models.CharField(max_length=200, help_text="State",default="Unfinished")
    progress = models.CharField(max_length=200, help_text="progress",default="0")
    metrics = models.CharField(max_length=50000,help_text="metrics",default="N/A")
    
    def update_state(self,new_state):
        
        Step_Result.objects.filter(project_result=self.project_result,name=self.name).update(state = new_state)
            
    def update_progress(self,new_progress):
        Step_Result.objects.filter(project_result=self.project_result,name=self.name).update(progress = str(new_progress))
    
    
    def update_metrics(self,new_metrics):
        Step_Result.objects.filter(project_result=self.project_result,name=self.name).update(metrics = str(new_metrics))
    
    def __str__(self):
        return self.name
    
    def as_json(self):
        return {
            "name": self.name,
            "description":self.description,
            "step_number":self.step_number,
            "state" : self.state,
            "progress":self.progress,
            "metrics" : self.metrics
            }
    
    
    
    
class Config_IP(models.Model):
    VOIP_TEST_WAN_IP = 'VOIP_TEST_WAN_IP'
    
    DATA_LAN_LAN_IP_1 = 'DATA_LAN_LAN_IP_1'
    DATA_LAN_LAN_IP_2 = 'DATA_LAN_LAN_IP_2'
    DATA_LAN_WLAN_2_4_Ghz_IP_1 = 'DATA_LAN_WLAN_2_4_Ghz_IP_1'
    DATA_LAN_WLAN_2_4_Ghz_IP_2 = 'DATA_LAN_WLAN_2_4_Ghz_IP_2'
    DATA_LAN_WLAN_5_Ghz_IP_1 = 'DATA_LAN_WLAN_5_Ghz_IP_1'
    DATA_LAN_WLAN_5_Ghz_IP_2 = 'DATA_LAN_WLAN_5_Ghz_IP_2'
    DATA_WAN_WLAN_5_Ghz_IP_1 = 'DATA_WAN_WLAN_5_Ghz_IP_1'
    DATA_WAN_WLAN_5_Ghz_IP_2 = 'DATA_WAN_WLAN_5_Ghz_IP_2'
    P2P_WLAN_5_Ghz_IP = "P2P_WLAN_5_Ghz_IP"
    
    
    IPTV_WLAN_5_Ghz_1_IP = "IPTV_WLAN_5_Ghz_1_IP"
    IPTV_WLAN_5_Ghz_2_IP = "IPTV_WLAN_5_Ghz_2_IP"
    IPTV_LAN_IP = "IPTV_LAN_IP"
    
    WEBUI_IP = "WEBUI_IP"
    TEST_CHOICES = ((VOIP_TEST_WAN_IP, 'VOIP_TEST_WAN_IP'),
                    (DATA_LAN_LAN_IP_1, 'DATA_LAN_LAN_IP_1'),
                    (DATA_LAN_LAN_IP_2, 'DATA_LAN_LAN_IP_2'),
                    (DATA_LAN_WLAN_2_4_Ghz_IP_1, 'DATA_LAN_WLAN_2_4_Ghz_IP_1'),
                    (DATA_LAN_WLAN_2_4_Ghz_IP_2, 'DATA_LAN_WLAN_2_4_Ghz_IP_2'),
                    (DATA_LAN_WLAN_5_Ghz_IP_1, 'DATA_LAN_WLAN_5_Ghz_IP_1'),
                    (DATA_LAN_WLAN_5_Ghz_IP_2, 'DATA_LAN_WLAN_5_Ghz_IP_2'),
                    
                    (DATA_WAN_WLAN_5_Ghz_IP_1, 'DATA_WAN_WLAN_5_Ghz_IP_1'),
                    (DATA_WAN_WLAN_5_Ghz_IP_2, 'DATA_WAN_WLAN_5_Ghz_IP_2'),
                    
                    (IPTV_WLAN_5_Ghz_1_IP, 'IPTV_WLAN_5_Ghz_1_IP'),
                    (IPTV_WLAN_5_Ghz_2_IP, 'IPTV_WLAN_5_Ghz_2_IP'),
                    
                    (IPTV_LAN_IP, 'IPTV_LAN_IP'),
                    (WEBUI_IP, 'WEBUI_IP'))
    
    name = models.CharField(max_length=50,unique=True, choices=TEST_CHOICES)
    ip = models.CharField(max_length=50)
    
    def __str__(self):
        return (self.name+"  : "+self.ip)


class Config_time(models.Model):
    test_time = models.TimeField(blank=True, null=True)
    name=models.CharField(max_length=50,unique=True)
    def __str__(self):
        return (self.name +'  '+ str(self.test_time))

    
    