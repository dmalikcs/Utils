#!/usr/bin/env python 
import MySQLdb
import os 
import django
import sys
import datetime
import commands 
from bs4 import BeautifulSoup
import re

##########Adding the Django Project path ################
PROJECT_PATH='/home/krunk3/krunkdata/'
os.path.dirname('/home/krunk3/krunkdata/krunkdata/')
sys.path.append(PROJECT_PATH)
os.environ['PROJECT_PATH']='/home/krunk3/krunkdata/'
os.environ['DJANGO_SETTINGS_MODULE']='krunkdata.settings'
#############################################

from krunkuser.models import A2M1_user
from krunkapp.models import A1M1_gorilla,A1M2_category
from krunkapp.models import A2M1_user
from django.contrib.auth.models import User
#from django.core.exceptions import DoesNotExist
from django.db.utils import IntegrityError

#################Database configuration############
HOST='localhost'
DB_USER='dmalik5'
DB_PASSWD='unix123'
DB_NAME='DB_DAILY'
##################################################
cmd_cp='/bin/cp'

###################################################

##############Config #####################
FILE_EXTENS=['blend','png','gif']

###########################################
PROGRESS_DIR='/usb/backup/progress-report/'
PROGRESS_DIR_REPORTS='/usb/backup/progress-report/Krunksystems-Marketing/data/'


def checkFileNameIntoDatabase(filename):
	SPLIT_FILE_NAME=filename.split('_')
	version=SPLIT_FILE_NAME.pop(-1)
	VER=None
	for i in range(0,10):
		if 'v'+str(i) in version or 'V'+str(i) in version:
			VER=True		
	if VER is None:
		SPLIT_FILE_NAME.append(version)
	newfilename='_'.join(SPLIT_FILE_NAME)
	if A1M1_gorilla.objects.filter(A1M1F6_filename__startswith=newfilename).exists():
		return True
	else:
		return None


def UpdateNewVersion(username,filename):
	NOW=datetime.datetime.now()
	SPLIT_FILE_NAME=filename.split('_')
        version=SPLIT_FILE_NAME.pop(-1)
        VER=None
        for i in range(0,10):
                if 'v'+str(i) in version or 'V'+str(i) in version:
                        VER=True
        if VER is not None:
		try:
			newfilename='_'.join(SPLIT_FILE_NAME)
			A1M1_gorilla.objects.filter(A1M1F6_filename__startswith=newfilename).update(
													A1M1F1_user_id=username.id,
													A1M1F15_version=version,
													A1M1F11_date_update=NOW
													)
		except Exception as e:
			print "Getting Errors while updating"
			print e
		else:
			print "Version updated"



#################################################
#  	Progress report -I 			#
#################################################
def fetchDataFromTextFile(filename):
	RETURN_DATA={}
	RETURN_DATA['error']={}
	RETURN_DATA['TAGS']=None
	RETURN_DATA['DETAIL']=None
	INFO_FILE_NAME=filename
	if os.path.exists(INFO_FILE_NAME):
		FH_INFO_FILE=open(INFO_FILE_NAME,'r')
		soup=BeautifulSoup(FH_INFO_FILE)
		try:
			LIST_DETAIL=[]
			VAR_DETAIL=soup.detail.contents[0].split('\n')
			print VAR_DETAIL
			for i in VAR_DETAIL:
				strip_i=i.strip('\r')
				LIST_DETAIL.append(strip_i)
			PRE_DETAIL=','.join(LIST_DETAIL)
			if PRE_DETAIL[0]==',':
				RETURN_DATA['DETAIL']=PRE_DETAIL.replace(',','',1)
		except AttributeError:
			print "Details not Defined"
		try:	
			LIST_TAG=[]
			VAR_TAG=soup.tags.contents[0].split('\n')
			for j in VAR_TAG:
				strip_j=j.strip('\r')
				LIST_TAG.append(strip_j)
			PRE_TAGS=','.join(LIST_TAG)
			if PRE_TAGS[0]==',':
				RETURN_DATA['TAGS']=PRE_TAGS.replace(',','',1)
		except AttributeError:
			print "Tags not Defined"
						
	else:
		print "File doesn't exists %s" % INFO_FILE_NAME	
	if RETURN_DATA['TAGS']:
		pass
	else:
		RETURN_DATA['TAGS']='NA'
	return RETURN_DATA

def data_move(file):
	VAR_DIR='/usb/blender-data/'
	IMG_DIR='/usb/blender-data/images'
	MOV_DIR='/usb/blender-data/movies'
	try:
		split_file=file.split('.')
		####Blend files only #######
		if split_file[-1]=='blend':
			try:
				split_date=file.split('_')
				#print split_date
				Year=datetime.datetime.strptime(split_date[0],'%Y%m%d').year
				Month=datetime.datetime.strptime(split_date[0],'%Y%m%d').strftime('%B')
				Day=datetime.datetime.strptime(split_date[0],'%Y%m%d').day
				DATA_ROOT_DIR=VAR_DIR+str(Year)+'/'+Month+'/'+str(Day)
				if not os.path.exists(DATA_ROOT_DIR):
					try:
						os.makedirs(DATA_ROOT_DIR)
					except:
						print "Not able to create a directory %s " % DATA_ROOT_DIR
				FILE_NAME=os.getcwd()+'/'+file
				cmd=cmd_cp+' '+FILE_NAME+' '+DATA_ROOT_DIR+'/'
				try:
					commands.getstatusoutput(cmd)
				except:
					print "copy failed"

			except:
				print 'Date split failed'
		####png & jpeg files only #######
		if split_file[-1]=='png' or split_file[-1]=='jpeg' or split_file[-1]=='jpg' or split_file[-1]=='gif':
			print "Processing the image files "
			try:
				split_date=file.split('_')
				print split_date[1]
				DATA_ROOT_DIR=IMG_DIR+'/'+split_date[1]	
				if not os.path.exists(DATA_ROOT_DIR):
					try:
						os.makedirs(DATA_ROOT_DIR)
					except:
						print "Not able to create a directory %s " % DATA_ROOT_DIR
				FILE_NAME=os.getcwd()+'/'+file
				print FILE_NAME
				cmd=cmd_cp+' '+FILE_NAME+' '+DATA_ROOT_DIR+'/'
				print cmd
				try:
					commands.getstatusoutput(cmd)
				except:
					print "copy failed"

			except:
				print 'Date split failed'
		####Move & Animation  files only #######
		if split_file[-1]=='mov' or split_file[-1]=='dvd':
			print "Processing the Movie files "
			try:
				split_date=file.split('_')
				print split_date[1]
				DATA_ROOT_DIR=MOV_DIR+'/'+split_date[1]	
				if not os.path.exists(DATA_ROOT_DIR):
					try:
						os.makedirs(DATA_ROOT_DIR)
					except:
						print "Not able to create a directory %s " % DATA_ROOT_DIR
				FILE_NAME=os.getcwd()+'/'+file
				print FILE_NAME
				cmd=cmd_cp+' '+FILE_NAME+' '+DATA_ROOT_DIR+'/'
				try:
					commands.getstatusoutput(cmd)
				except:
					print "copy failed"

			except:
				print 'Date split failed'

	except:
		print 'Split failed'

def UpdateToDatabase(**kwargs):
	RETURN_DATA={}
	try:
		A1M1_gorilla.objects.create(
					A1M1F1_user_id=kwargs['username'],
					A1M1F2_category=kwargs['c'],
					A1M1F9_detail=kwargs['DETAIL'],
					A1M1F8_tagline=kwargs['TAGS'],
					A1M1F7_File='uploads/'+kwargs['VAR_DIR'],
					A1M1F12_status='New',
			      		A1M1F6_filename=kwargs['VAR_DIR']
					)
	except IntegrityError:
		print "Duplicate Error "
		RETURN_DATA['status']='Failed'
	else:
		RETURN_DATA['status']='created'
	return RETURN_DATA		
	

def progressUpdate(username):
	print "%s" % username
        UPDATE_DATA={}
        UPDATE_DATA['username']=username
	UPDATE_DATA['c']=A1M2_category.objects.get(id=1)
	if A2M1_user.objects.filter(A2M1F1_username_id=username.id).exists():
		SMB_DRIVE=A2M1_user.objects.get(A2M1F1_username_id=username.id).A2M1F8_sambha
		try:
			os.chdir(SMB_DRIVE)
		except:
			TASK_STATUS='Failed'
		else:
			TASK_STATUS='Sucess'
		finally:
			print "Step:1:samba:%s" % TASK_STATUS
		LIST_DIR=os.listdir('.')
		for VAR_DIR in LIST_DIR:
			split_filename=VAR_DIR.split('.')
			if len(split_filename) >=2:
				for extension in FILE_EXTENS:
					if split_filename[-1]==extension:
						Status=checkFileNameIntoDatabase(split_filename[0])
						if Status:
							print "Going for version update"
							UpdateNewVersion(username,split_filename[0])
						else:
							#print "%s -----> %s" %  (VAR_DIR,(split_filename[0]+'.txt'))
							INFO_FILE_NAME=os.getcwd()+'/'+split_filename[0]+'.txt'
							if os.path.exists(INFO_FILE_NAME):
								DATA_FROM_DETAIL=fetchDataFromTextFile(INFO_FILE_NAME)
                                                		UPDATE_DATA['TAGS']=DATA_FROM_DETAIL['TAGS']
                                                		UPDATE_DATA['DETAIL']=DATA_FROM_DETAIL['DETAIL']
                                                		UPDATE_DATA['VAR_DIR']=VAR_DIR
								update_data=UpdateToDatabase(**UPDATE_DATA)
								if update_data.__getitem__('status')=='created':
									print "Data has been updated"
								else:
									print "Failed to updateToDatabase"	
							else:
								print "%s" % VAR_DIR
								for i in range(0,len(VAR_DIR)):
									print '+'.strip(' '),
								print "\nThis File doesn\'t have txt file as well as information into database"	
					#####This part will report  if any extension is not in our configuration ###
					if split_filename[-1] not in FILE_EXTENS and split_filename[-1]!='txt':
						print "Warning: This Extension Going to miss" 
						print "*%s*" % VAR_DIR


			else:
				print "Normal file"
			data_move(VAR_DIR)

	else:
		print "Samba drive doesn't exists for user %s" % username




def email_report():
	var_date=datetime.date.today()
	email_file="email_report_blender.wiki"
	if os.path.exists(PROGRESS_DIR_REPORTS):
		os.chdir(PROGRESS_DIR_REPORTS)
		FH=open(email_file,'w')
	FH.write("++Progress report as on %s" % var_date)
	for user in User.objects.all():
		try:
			Dept=A2M1_user.objects.get(A2M1F1_username=user.id).A2M1F6_department
		except A2M1_user.DoesNotExist:
			Dept=None
		if Dept=='blender':
			NAME="*%s %s*" % (user.first_name,user.last_name)
			FH.write("\n")
			FH.write(NAME)
			FH.write("\n")
			reports=A1M1_gorilla.objects.filter(
							A1M1F1_user_id=user.id,
							A1M1F11_date_update__year=var_date.year,
							A1M1F11_date_update__month=var_date.month,
							A1M1F11_date_update__day=var_date.day,
							)
			if len(reports)!=0:
				FH.write("\n")
			 	FH.write("<<|")
				FH.write("\n")
				FH.write("ID|File name|User|Status|Details|Tags|Quality|Version|Response")
				FH.write("\n")
				for report in reports:
					DATA="%d|%s|%s|%s|%s|%s|%s|%s|%s" %  (report.pk,report.A1M1F6_filename,user.first_name,report.A1M1F12_status,report.A1M1F9_detail,report.A1M1F8_tagline,report.A1M1F14_quality,report.A1M1F15_version,report.A1M1F13_response)
					FH.write(DATA)
					FH.write("\n")
				FH.write(">>")
				FH.write("\n")
			else:
				FH.write("\n")
				FH.write("<<|")
				FH.write("\n")
				FH.write("ID|File name|User|Status|Details|Tags|Quality|Version|Response")
				FH.write("\n")
				FH.write("No Reports")
				FH.write("\n")
				FH.write(">>")
				FH.write("\n")

		
	


def daily_email_report():
	var_date=datetime.date.today()
	wiki_report=var_date.isoformat()+'.wiki'
	if os.path.exists(PROGRESS_DIR_REPORTS):
		os.chdir(PROGRESS_DIR_REPORTS)
		FH=open(wiki_report,'a+')	
		FH.write("<<|")
		FH.write("\n")
		FH.write("ID|File name|User|Status|Details|Tags|Quality|Version|Response")
		FH.write("\n")
	for user in User.objects.all():
		try:
			Dept=A2M1_user.objects.get(A2M1F1_username=user.id).A2M1F6_department
		except A2M1_user.DoesNotExist:
			Dept=None
		if Dept=='blender':
			#FH.write("*%s %s|%s*" % (user.first_name,user.last_name,var_date))
			#FH.write("\n")
			reports=A1M1_gorilla.objects.filter(
							A1M1F1_user_id=user.id,
							A1M1F11_date_update__year=var_date.year,
							A1M1F11_date_update__month=var_date.month,
							A1M1F11_date_update__day=var_date.day,
							)
			for report in reports:
				DATA="%d|%s|%s|%s|%s|%s|%s|%s|%s" %  (report.pk,report.A1M1F6_filename,user.first_name,report.A1M1F12_status,report.A1M1F9_detail,report.A1M1F8_tagline,report.A1M1F14_quality,report.A1M1F15_version,report.A1M1F13_response)
				FH.write(DATA)
				FH.write("\n")
	FH.write(">>")
	FH.write("\n")
	FH.close()

def dir_creation():
	VAR_DIR='/usb/blender-data/'
	os.chdir(VAR_DIR)
	TODAY_DATE=datetime.date.today()
	ROOT_DIR=VAR_DIR+'/'+str(TODAY_DATE.year)
	if not os.path.exists(ROOT_DIR):
		try:
			os.mkdir(ROOT_DIR)
			cmd="/usr/bin/setfacl -m group:management:rwx %s" % ROOT_DIR
			(status,coutput)=commands.getstatusoutput(cmd)
		except OSError:
			print "Error while creating the Directory"
	SUB_ROOT_DIR=ROOT_DIR+'/'+datetime.date.today().strftime("%B")
	if not os.path.exists(SUB_ROOT_DIR):
		try:
			os.mkdir(SUB_ROOT_DIR)
			cmd="/usr/bin/setfacl -m group:management:rwx %s" % SUB_ROOT_DIR
			(status,coutput)=commands.getstatussoutput(cmd)
		except OSError:
			print "Error while creating the Directory"
	DATA_ROOT_DIR=SUB_ROOT_DIR+'/'+str(datetime.date.today().day)
	if not os.path.exists(DATA_ROOT_DIR):
		try:
			os.mkdir(DATA_ROOT_DIR)
			cmd="/usr/bin/setfacl -m group:management:rwx %s" % DATA_ROOT_DIR
			(status,output)=commands.getstatusoutput(cmd)
		except OSError: 
			print "Error While creating the root Directory"
		
	
	
def help():
	print "\tCommands line online helpi\n"
	print "\t--help:\tDisplay the help funcation"
	print "\t--Report:\tRun the verbose report for today\'s work"
	print "\t--update:\tUpdate the response from wiki to Database"
	print "\t--create-dir:\tCreate the directory for Today"
	print "\t--email-report:\tIt's create final report for User It should create  run after the --Report & --update with same command"


def response_update():
	var_date=datetime.date.today()
	NOW=datetime.datetime.now()
	wiki_report=var_date.isoformat()+'.wiki'
	if os.path.exists(PROGRESS_DIR_REPORTS):
		os.chdir(PROGRESS_DIR_REPORTS)
		FH=open(wiki_report,'r')
		reports=FH.readlines()
	for report in reports:
		report_s=report.strip('\n')
		if not re.match('\<\<\||>>|\AID',report_s):
				SPLIT_DATA=report_s.split('|')
				if len(SPLIT_DATA)==9:
					var_pk=SPLIT_DATA[0]
					var_A1M1F6_filename=SPLIT_DATA[1]
					var_first_name=SPLIT_DATA[2]
					var_A1M1F12_status=SPLIT_DATA[3]
					var_A1M1F9_detail=SPLIT_DATA[4]
					var_A1M1F8_tagline=SPLIT_DATA[5]
					var_A1M1F14_quality=SPLIT_DATA[6]
					var_A1M1F15_version=SPLIT_DATA[7]
					var_A1M1F13_response=SPLIT_DATA[8]
					p=A1M1_gorilla.objects.filter(pk=var_pk).update(
									A1M1F6_filename=var_A1M1F6_filename,
									A1M1F12_status=var_A1M1F12_status,
									A1M1F9_detail=var_A1M1F9_detail,
									A1M1F8_tagline=var_A1M1F8_tagline,
									A1M1F14_quality=var_A1M1F14_quality,
									A1M1F15_version=var_A1M1F15_version,
									A1M1F13_response=var_A1M1F13_response,
									A1M1F11_date_update=NOW
								)

			



#print "\tReport Generation Tool"
if len(sys.argv) >1:
	if sys.argv[1]=='--Report':
		var_date=datetime.date.today()
		blender_latest='blender-latest.wiki'
		try:
			if os.path.exists(PROGRESS_DIR_REPORTS):
				os.chdir(PROGRESS_DIR_REPORTS)
				FH=open(blender_latest,'a+')
				FH.write("[%s]\n" % var_date)
				daily_email_report()
		except:
			print "Not able to change the directory %s" % PROGRESS_DIR_REPORTS
		finally:
			FH.close()
	if sys.argv[1]=='--help':
		help()
	if sys.argv[1]=='--update':
		response_update()
	if sys.argv[1]=='--create-dir':
		 dir_creation()
	if sys.argv[1]=='--email-Report':
		email_report()
else:
	#x=raw_input("Do you want to run progress report (Yes/No) ?") 
	#if x=='Yes' or x=='yes':
	for j in User.objects.all():
		pass
		progressUpdate(j)
	#else:
	#	print "Thank you chosing Report Tools"
	


