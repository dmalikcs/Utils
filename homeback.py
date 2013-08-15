#!/usr/bin/env python
import sys
import commands 
import datetime

DATE=datetime.date.today()
FINAL_DATE=DATE.isoformat()
SYS_LEN=len(sys.argv)
if SYS_LEN >=2:
	if sys.argv[1]:
		SYS_DEBUG=sys.argv[1]
else:
	SYS_DEBUG=None

####Linux commands variable#####
DEBUG='--debug'
HOME_DIR_LIST='/bin/ls -1 /home/'
VAR_TAR='/bin/tar'
VAR_BACKUP_DIR='/usb/backup/django/'
VAR_BAKUP_SOURCE='/home/*'
VAR_BUNZIP='/usr/bin/bzip2'
VAR_BACKUP_FILE_NAME=VAR_BACKUP_DIR+FINAL_DATE+'.'+'tar'
CMD_COMPRESS=VAR_BUNZIP+' '+VAR_BACKUP_FILE_NAME
CMD=VAR_TAR+' '+'-cvf'+' '+VAR_BACKUP_FILE_NAME+' '+VAR_BAKUP_SOURCE
VAR_LOG='/home/dmalik5/logs/backup.log'
###################################

#######################
LOG=open(VAR_LOG,'a+')
######################
T_LS_OUTPUT=commands.getstatusoutput(HOME_DIR_LIST)
if T_LS_OUTPUT[0]==0:
	if SYS_DEBUG==DEBUG:
		print VAR_BACKUP_FILE_NAME
		print VAR_BAKUP_SOURCE
		print CMD
	(BACKUP_STATUS,OUTPUT)=commands.getstatusoutput(CMD)
	if BACKUP_STATUS==0:
		BACKUP_LOG="%s :Success: archived completed\n" %(FINAL_DATE)
		LOG.write(BACKUP_LOG)
			
	else:
		BACKUP_LOG="%s :Error: archived failed\n" %(FINAL_DATE)
		LOG.write(BACKUP_LOG)
	
	if SYS_DEBUG==DEBUG:
		print VAR_BACKUP_FILE_NAME
	(COMPRESS_STATUS,COMRESS_OUTPUT)=commands.getstatusoutput(CMD_COMPRESS)
	if COMPRESS_STATUS==0:
		CMP_LOG="%s :Success: compressed completed\n" %(FINAL_DATE)
		LOG.write(CMP_LOG)
	else:
		CMP_LOG="%s :Error:compressed failed\n" %(FINAL_DATE)
		LOG.write(CMP_LOG)
		if SYS_DEBUG==DEBUG:
			print COMRESS_OUTPUT
else:
	LIST_LOG="%s :Error: File systems not accessible" %s (FINAL_DATE)
	LOG.write(LIST_LOG)


LOG.close()
