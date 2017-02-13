import csv
import paramiko
from datetime import *
import re
import threading
import argparse

dict1 = {}
#cmd = 'hostname'
date = datetime.now().strftime('%d-%m-%Y')


def workon(host,username,password):
    try:
        # print(type(host))
        ssh = paramiko.SSHClient()
        ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        print("creating connection")

        ssh.connect(host, username=username, password=password)
        print("connected")
        stdin, stdout, stderr = ssh.exec_command(cmd)
        s = stdout.readlines()
        print(s)
        with open(r'C:\temp\lab_{}.txt'.format(date), 'a') as fw_txt:
            fw_txt.write(date + ':\t' + host + '\t'+ str(s)+'\n')
    except Exception as e:
        print(e)
        with open(r'C:\temp\lab_{}.log'.format(date), 'a') as fw_log:
            fw_log.write(date + ':\t' + host + '\t'+ str(e) + '\n')

class SshConnection(threading.Thread):
    def __init__(self,host,username,password):
        threading.Thread.__init__(self)
        self.host = host
        self.username = username
        self.password = password


    def run(self):
        workon(self.host,self.username,self.password)


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--search',help='Specify Hostname to lookup')
    parser.add_argument('--cmd',help='Input command to be executed on Target host')

    args = parser.parse_args()
    global cmd
    if args.search == 'pune':
        what2look4 = 'Pune'
        patterns = re.compile(r'\bPUN|\bTAC1|\bPES|\bPSS')

    elif args.search =='all':
        what2look4 = 'all'
        patterns = re.compile(".*")

    else:
        what2look4 = args.search
        patterns = re.compile(".*({}).*".format(what2look4))

    cmd = args.cmd



    with open(r'C:\temp\auditedDeviceList.csv','r') as infile:
        reader = csv.reader(infile)
        headers = next(reader)[1:]
        #patterns = re.compile(r'\bDD-WRT|\bTAC1|\bPES')
        #patterns = re.compile(".*({}).*".format(what2look4))
        print("Looking into {} Servers".format(what2look4))

        for row in reader:
            dict1[row[0]] = {key: value for key, value in zip(headers, row[1:])}
            s = row[0]
            if patterns.search(s):
                print(row)
                # Assigning Host and credentials
                host = row[1]
                if dict1[row[0]]['ResourceFamilyName'] == 'NTCT Server':
                    username = 'root'
                    password = 'netscout1'

                elif dict1[row[0]]['ResourceFamilyName'] == 'nG1-PM':
                    username = 'root'
                    password = 'netscout1'

                elif dict1[row[0]]['ResourceFamilyName'] == 'Infinistream':
                    username = 'root'
                    password = 'netscout'

                else:
                    username = 'root'
                    password = 'password'

                conn = SshConnection(host,username,password)
                conn.start()
                #conn.join()

if __name__ == '__main__':
    try:
        main()
    except KeyboardInterrupt as e:
        print('Stopping Scan {}'.format(e))
