# -*- coding: utf-8 -*-
from __future__ import unicode_literals
import os
from django.shortcuts import render,HttpResponse
from cootalk import models
from cootalk.src import fetch_config,config_diff,gitpull,clearold
from cootalk.src import Myexception
from cootalk.src import CheckDirFilename
from django.core.cache import cache
import time
import json
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
# Create your views here.




import logging
from cootalk.conf import mylogging
logger = logging.getLogger(__name__)
mylogging.load_my_logging_cfg()




def index(request):
	


	#item = {'ip_addr':'172.18.3.180','ssh_port':22,'app':'cootalk','country':'柬埔寨','is_config':False}
	#models.Inventory.objects.create(**item)
	
	
	res = models.Inventory.objects.all()
	return render(request,'index.html',{"res":res})


def action(request):

	
	repo_path = os.path.join(BASE_DIR,'cootalk','outfile','base')
	repo_url = 'git@git.cootel.com:liuliangliang/tomcat_config.git'
	if request.method == "POST":
	        if  cache.get("action_lock"):
			status = 1
			result = "the compare_job is comparing right now ,please hold on!"
			return HttpResponse(json.dumps({"status": status, "result": result}))
		cache.set("action_lock",True)
		clearold.run()
		res = request.POST.values()
		try:
				gitfile = gitpull.Ger_gitfile(repo_path,repo_url)
				gitfile.clone()
				ip_list = models.Inventory.objects.filter(nid__in=res).values_list("ip_addr",flat=True)
 				print(ip_list)
        			config_dir = os.path.join(BASE_DIR,'cootalk','conf','hosts')
        			with open(config_dir, 'a') as w:
                			w.write("[cootalk]"+"\n")
        			for ip in ip_list:
                			with open(config_dir,'a') as w:
                        			w.write(ip+' ansible_connection=ssh ansible_ssh_user=configer ansible_ssh_pass=xinwei'+'\n')
        			
				yaml_dir = os.path.join(BASE_DIR,'cootalk','conf','key')
				getfile_path = os.path.join(BASE_DIR,'cootalk','outfile','remote_file')
				ansible_fetch = fetch_config.PlayUbook(config_dir,yaml_dir,getfile_path)
				ansible_fetch.playnow()
				#fetch_config.core()
				print(11111111111111111111111111)
				keydir = os.path.join(BASE_DIR,'cootalk','outfile','base')
				
				page_list = []
        			for ip in ip_list:
					compare_dir = os.path.join(BASE_DIR,'cootalk','outfile','remote_file',ip)
					check_result = CheckDirFilename.CheckFilename(keydir,compare_dir)
					if  check_result.check_res():
						 #print check_result.check_res()
						 raise(Myexception.NofileException(check_result.check_res()))
					local_dir = os.path.join('remote_file',ip)
					
                			page = config_diff.core(local_dir)
					page_list.append(page)

                                #res = f.readlines()
                                status = 0
                                result = page_list
				cache.set("action_lock",False)
                                return HttpResponse(json.dumps({"status": status, "result": result}))
		except Exception,Argument:
				
                                print 'error>>>%s\n'%Argument
				logger.error('error>>>%s\n' % Argument)
				result = str(Argument)
				status = 1
				cache.set("action_lock",False)
				return HttpResponse(json.dumps({"status": status, "result": result}))

                #finally:
				#res = f.readlines()
				#status = 0
				#result = res
				#return HttpResponse(json.dumps({"status": status, "result": result}))





def configupdate(request):
	repo_path = os.path.join(BASE_DIR,'cootalk','outfile','update')
        repo_url = 'git@git.cootel.com:liuliangliang/tomcat_config.git'
	if request.method == 'POST':
		res = request.POST.values()
		gitfile = gitpull.Ger_gitfile(repo_path,repo_url)
                gitfile.clone()
                ip_list = models.Inventory.objects.filter(nid__in=res).values_list("ip_addr",flat=True)
                print(ip_list)
                config_dir = os.path.join(BASE_DIR,'cootalk','conf','update')
                with open(config_dir, 'a') as w:
                        w.write("[cootalk]"+"\n")
                for ip in ip_list:
                        with open(config_dir,'a') as w:
                              w.write(ip+' ansible_connection=ssh ansible_ssh_user=configer ansible_ssh_pass=xinwei ansible_become_pass=xinwei'+'\n')
                                
                print(11111111111111111111111111)
		config_dir = os.path.join(BASE_DIR,'cootalk','conf','update')
		yaml_dir = os.path.join(BASE_DIR,'cootalk','conf','copy.yaml')
                getfile_path = os.path.join(BASE_DIR,'cootalk','outfile','update')
                ansible_fetch = fetch_config.PlayUbook(config_dir,yaml_dir,getfile_path)
                ansible_fetch.playnow()	
		status = 0
		result = 2222
	return  HttpResponse(json.dumps({"status": status, "result": result}))

def log(request):
	while True:
        	msg = request.receive()  # 接客户端的消息
    		print msg
