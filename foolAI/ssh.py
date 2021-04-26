import time
import paramiko
import multiprocessing as mp
import os

def recv_shell(shell,cmd=''):
    while True:
        time.sleep(1)
        msg=shell.recv(1024).decode("utf8","ignore")
        print(msg)
        if len(msg)<1:
            return


class SSHSession:
    def __init__(self, host, username='xxxxx',passwd='', pubkey_path='', port=22):

        self.host = host
        self.port = port
        self.username = username
        self.passwd=passwd
        self.pubkey_path=pubkey_path

    def connect(self):
        self.ssh = paramiko.SSHClient()
        self.ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        if self.passwd!='':
            self.ssh.connect(hostname=self.host, port=self.port, username=self.username, password=self.passwd)
            self.shell=self.ssh.invoke_shell()
        else:
            private_key = paramiko.RSAKey.from_private_key_file(self.pubkey_path)
            self.ssh.connect(hostname=self.host, port=self.port, username=self.username, pkey=private_key)
            self.shell=self.ssh.invoke_shell()
    def get_shell(self):
        return self.shell
    def get_ssh(self):
        return ssh
    #def get_virtual_env(self):
    def env_install(self):
        self.shell.send('pip3 install virtualenv\n')
        self.shell.send('mkdir .virtualenv && cd .virtualenv\n')
        self.shell.send('source /home/ubuntu/.virtualenvs/autoenv/bin/activate \n')
        cmd='scp -P %d -i %s ./requirements.txt %s@%s:~/'%(self.port,self.pubkey_path,self.username,self.host)
        os.system(cmd)
        self.shell.send('pip3 install -r ~/requirements.txt -i https://mirrors.aliyun.com/pypi/simple \n')
        #self.shell.send('pip3 install ')
        p1 = mp.Process(target=recv_shell,args=(self.shell,2))
        p1.run()
        p1.join()
        self.ssh.close()


if __name__ == '__main__':
    key_path='/Users/admin/.ssh/id_rsa_dingwenbing_172.28.6.33'
    host='172.28.6.33'
    username="ubuntu"
    port=20160
    ssh=SSHSession(host=host,username=username,pubkey_path=key_path,port=port)
    ssh.connect()
    ssh.env_install()




