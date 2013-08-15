#!/usr/bin/env python
import os 
import sys
import datetime
import logging 
import commands
from bs4 import BeautifulSoup

#######Global Variable ############
DOS_UNIX='/usr/bin/dos2unix'
VAR_BLENDER='/download/blender/'
VAR_BLENDER_DIR='/download/blender/data/'
VAR_LOG_FILE_NAME='/home/dmalik5/logs/blender.log'
VAR_DATE=datetime.date.today()
DATE_FINAL=VAR_DATE.isoformat()
TEAM_LIST=['ankit','anshul','sandeep','naim','anu']
TEAM_DIC={
	'ankit':'Ankit Kumar',
	'anshul':'Anshul Verma',
	'sandeep':'Sandeep Kumar',
	'naim':'Naimudin Ansari',
	'anu':'Anu Malik',
}
logging.basicConfig(filename=VAR_LOG_FILE_NAME, format='%(asctime)s : %(message)s', datefmt='%m/%d/%Y %I:%M:%S %p',level=logging.INFO)



logging.info('Task started')
###############################
DIR_NAME=VAR_BLENDER_DIR+DATE_FINAL
if os.path.exists(DIR_NAME):
	LOG='File exists %s' % DIR_NAME
	logging.warning('flie already exisis')
else:
	LOG='File %s created' % DIR_NAME
	logging.info(LOG)
	os.mkdir(DIR_NAME)

if os.path.exists(DIR_NAME):
	logging.info('permission changed to blender::staff ')
	os.chown(DIR_NAME,532,522)
else:
	LOG='File not exists %s' % DIR_NAME
	logging.error('flie not  exisis')

##########creating the subdirectory###############
for i in TEAM_LIST:
	TEAM_DIR=DIR_NAME+'/'+i
	if not os.path.exists(TEAM_DIR):
		os.mkdir(TEAM_DIR)
		
	else:
		LOG='File already exists %s ' % TEAM_DIR
		logging.warning(LOG)
#####################################################
for i in TEAM_LIST:
	TEAM_DIR=DIR_NAME+'/'+i
	if os.path.exists(TEAM_DIR):
		logging.info('permission changed to blender::staff ')
		os.chown(TEAM_DIR,532,522)
	else:
		LOG='File not exists %s' % TEAM_DIR
		logging.error('flie not  exisis')

os.chdir(VAR_BLENDER)
LINK_FILE_NAME=VAR_BLENDER+'latest'
if os.path.exists(LINK_FILE_NAME):
	os.unlink('latest')
else:
	LOG='No link file found '
	logging.warning(LOG)

###################################################
######		Softlink creation                ##
###################################################
os.chdir(VAR_BLENDER)
os.symlink('data'+'/'+DATE_FINAL, 'latest')
#
LOG='Task Finished'
logging.info(LOG)


#######################################################
### Backup for belnder files 			     ##
#######################################################
DEBUG='--debug'
VAR_TAR='/bin/tar'
VAR_BACKUP_DIR='/usb/backup/blender/'
L_DATE=datetime.date.today()-datetime.timedelta(days=1)
F_L_DATE=L_DATE.isoformat()
DATA_DIR='/download/blender/data/'
VAR_BAKUP_SOURCE=F_L_DATE+'/'+'*'
VAR_BUNZIP='/usr/bin/bzip2'
VAR_BACKUP_FILE_NAME=VAR_BACKUP_DIR+F_L_DATE+'.'+'tar'
CMD_COMPRESS=VAR_BUNZIP+' '+VAR_BACKUP_FILE_NAME
CMD=VAR_TAR+' '+'-cvf'+' '+VAR_BACKUP_FILE_NAME+' '+VAR_BAKUP_SOURCE
####################################################
def backup():
	os.chdir(DATA_DIR)
	(tar_status,output)=commands.getstatusoutput(CMD)
	if tar_status==0:
		LOG="File %s successfully archived " % VAR_BAKUP_SOURCE
		logging.info(LOG)
		(cmp_status,cmd_output)=commands.getstatusoutput(VAR_BACKUP_FILE_NAME)
		if cmp_status==0:
			LOG="File successfully compressed "
			logging.info(LOG)
		else:
			LOG="File compress to fail "
			logging.error(LOG)
	else:
		LOG="File %s failed" % VAR_BAKUP_SOURCE
		logging.error(LOG)
		logging.error(output)

	
backup()
