
#import pxssh
import time
from pexpect import pxssh
#import getpass


hostlist = ['0.0.0.0', '0.0.0.0', '0.0.0.0']

i= bi = ci = 0

#bashcommand list: include all the eports .. 
#commands thats performed at the start once..
#use "r" if it include apecial charachters
bashcommand = [r'export /a/b',
 r'cd $server_HOME',]

#checkcommand list: include all testing commands
checkcommand = [r'hostname -I',
r'nodetool -u user -pw pass status',
r'nodetool -u user -pw pass compactionstats -H  |grep pending',
r'df -h|grep u01',
r'cd anothefrDile',
r'./shellScript1.sh',
r'./shellScript2.sh']
while true:
	i=0
	while i<len(hostlist):

		try:                                                           
			s = pxssh.pxssh()
			#hostname = input('hostname: ')
			#username = input('username: ')
			#password = getpass.getpass('password: ')
			#s.login (hostname, username, password)
			print('in server ',i+1,hostlist[i]) 
			s.login (hostlist[i], 'k2viewmonitor', 'k2v13w.m0n')
			bi=0
			while (bi<len(bashcommand)):
					s.sendline(bashcommand[bi])
					s.prompt()
					#bi: counter for bashcommand list
					bi+=1

			filename = open(hostlist[i],mode = 'ab')

			#ci: the counter for the checkcommand list
			ci=0
			while (ci<len(checkcommand)):
		
				s.sendline (checkcommand[ci])   # run a command
				s.prompt()            		 # match the prompt
				print (s.before)       		   # print everything before the prompt.		
				ci+=1
				time.sleep(5)
				filename.write(s.before)
				
		
			#nmon i think its not a good idea here => nmom
			s.sendline (r'./nmon_x86_64_centos6')
			s.prompt()
			s.sendline('l')
			s.prompt()
			s.sendline('m')
			time.sleep(5)
			s.prompt()
			filename.write(s.before)
			#print (s.before)
			s.logout()
			i+=1
		except pxssh.ExceptionPxssh as e:
			print ("pxssh failed on login.", hostlist[i])
			print (str(e))	
		i+=1
#sleep for 20 mins
time.sleep(1200)
