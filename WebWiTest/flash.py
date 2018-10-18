import serial
import logging
import time
import sys
import netifaces
import requests
import re
import os
from pathlib import Path

CFE_Password = {"arcadyan-starlite":"BE9B6BD915F5803C80D6EBD28CC78EB04EB8C75E02533285CFFAAF3C8505198A","askey-stargatev2":"fL3xZpv6umpbKyhR",
                "siligence-cut2":"fL3xZpv6umpbKyhR"}
Uboot_Image = {"sagem_lbv3":"scs_gener","sagem_mib4":"sc_bcm63138.scos.oper.secure"}

class Target(object):
    """docstring for Target"""
    def __init__(self,hardware):
        self.ser      = None
        self.port     = "/dev/ttyS0"
        self.baud     = 115200
        self.timeout  = 600
        self.hardware = hardware
        self.option   = '\n\n\n'
        self.tftp_server = '0.0.0.0'
        self.target_ip   = '192.168.1.1'
        self.end_boot = 'Sysinit done.'
        self.CFE_HARD = ["arcadyan-starlite","askey-stargatev2"]
        self.UBOOT_Hard = ["sagem-mib4","sagem_lbv3"]
        self.cfe      = False
        self.uboot    = False
        self.sequence = None
        self.cfe_sequence   = [['Auto run second count down:', self.option],
                               ["Enter password:","{}\n".format(CFE_Password[self.hardware])],
                               ["CFE>",self.option]]
        self.uboot_sequence = [['Hit any key to stop autoboot:', self.option],
                               ['>', 'setenv serverip {0}{1}'.format(self.tftp_server,self.option)],
                               ['>', 'run load_oper{}'.format(self.option)],
                               ['>', 'reset{}'.format(self.option)],
                               [self.end_boot, self.option]]

    def open_serial_connection(self):
        self.ser = serial.Serial(self.port, self.baud, timeout=0)
        if self.ser is None:
            raise Exception("Cannot open serial port")

    def close_serial_connection(self):
        try:
            if self.ser is not None:
                self.ser.close()
                self.ser = None
        except Exception as e:
            logging.error(e.message)

    def get_serial(self):
        return self.ser

    def serial_read(self,buffersize=2048,to_stdout=True):
        data = self.ser.read(buffersize)
        if to_stdout and len(data) > 0:
            sys.stdout.write(data)
        return data

    def serial_write(self,text):
        try:
            self.ser.write(text + '\n')
            logging.info("write {} to serial".format(text))
        except Exception as e:
            logging.error(e.message)

    def add_target(self,serial_port,lan_intf):
        self.port = serial_port
        if self.hardware in self.CFE_HARD:
            self.cfe = True
            self.sequence = self.cfe_sequence
        elif self.hardware in self.UBOOT_Hard:
            self.uboot = True
            self.tftp_server = self.get_ip(lan_intf)
            self.sequence = self.uboot_sequence
        else:
            raise Exception("Hardware not supported")
        self.open_serial_connection()

    def get_ip(self,interface):
        netifaces.ifaddresses(interface)
        return netifaces.ifaddresses(interface)[2][0]['addr']

    def send_file(self,build):
        try:
            os.system("sudo curl -F filename=@/tmp/{0} {1}/upload.cgi 2>/dev/null 1>&2".format(build,self.target_ip))
        except Exception as e:
            logging.error(e.message)

    def get_build(self,path,build):
        dir = '/tmp/'
        file = Path(dir + build)
        if not file.is_file():
            os.system("sudo wget -P {0} {1}{2} 2>/dev/null 1>&2".format(dir,path,build.replace("#", "%23")))
        assert file.is_file(), "cannot get file from build server"

    def is_host_up(self):
        host_up = True if os.system("ping -c 1 -W 2 {0} >/dev/null 2>&1".format(self.target_ip)) is 0 else False
        return host_up

    def login_to_target(self,user='root',password='sah'):
        bufferis = ''
        retry = 1
        self.serial_write('\n')
        while retry <= 5:
            time.sleep(0.5)
            data = self.serial_read()
            if len(data) > 0:
                bufferis += data
                if re.search("login",bufferis,re.IGNORECASE):
                    self.serial_write(user)
                elif re.search("password",bufferis,re.IGNORECASE):
                    self.serial_write(password)
                elif re.search("#",bufferis,re.IGNORECASE):
                    logging.info("user is logged")
                    return True
            bufferis = ''
            retry += 1
        return False

    def is_logged(self):
        bufferis = ''
        self.serial_write('\n')
        time.sleep(1)
        data = self.serial_read()
        bufferis += data
        if re.search("#", bufferis, re.IGNORECASE):
            return True
        else:
            return False

    def reboot_target(self):
        if not self.is_logged():
            assert self.login_to_target(),"cannot login to the DUT"
        self.serial_write("reboot")


    def wait_end_of_boot(self,to_stdout=True):
        bufferis = ''
        timeris = 0
        while (timeris < self.timeout):
            while (self.ser.inWaiting() > 0):
                timeris = 0
                data = self.serial_read()
                if len(data) > 0:
                    bufferis += data
                    if to_stdout:
                        sys.stdout.write(data)
                    if re.search(self.end_boot,bufferis,re.IGNORECASE):
                        return True
            time.sleep(0.1)
            timeris += 0.1
        return False

    def fw_update(self,sleep_time=0.1):
        bufferis = ''
        timeris = 0
        seeq_no = 0
        while (timeris < self.timeout):
            if (seeq_no >= len(self.sequence)):
                #self.close_serial_connection()
                return True
            while (self.ser.inWaiting() > 0) and (seeq_no < len(self.sequence)):
                timeris = 0
                data = self.serial_read()
                if len(data) > 0:
                    bufferis += data
                    if re.search(self.sequence[seeq_no][0],bufferis,re.IGNORECASE):
                        if len(self.sequence[seeq_no][1]) > 0 :
                            time.sleep(0.5)
                            self.serial_write(self.sequence[seeq_no][1])
                        bufferis = ''
                        seeq_no +=1
            time.sleep(sleep_time)
            timeris += sleep_time
        #self.close_serial_connection()

    def update_cfe_hardware(self,build):
        self.send_file(build)

    def update_uboot_hardware(self,build):
        os.system("sudo cp -f /tmp/{} /tmp/{}".format(build,Uboot_Image[self.hardware]))

target = Target("arcadyan-starlite")

path = "http://builds.be.softathome.com/GEN/V9.0/PROJ/SWISSCOM/REL/2018/04/2018-04-23_V10.00.04/swisscom/starlite/arcadyan-starlite/swisscom_multi_sip_normal/"
build = "2018-04-23_V10.00.04#00_swisscom_starlite_arcadyan-starlite_swisscom_multi_sip_normal_bcmflash.img"

def firmware_upgrade(path,build):
    assert target.is_host_up(), "DUT is not reacheable"
    target.get_build(path=path, build=build)
    target.add_target(serial_port='/dev/ttyUSB0', lan_intf='DUT')
    if target.uboot:
        target.update_uboot_hardware(build)
    target.reboot_target()
    target.fw_update()
    if target.cfe:
        target.update_cfe_hardware(build)
    target.wait_end_of_boot()
    target.close_serial_connection()

firmware_upgrade(path,build)