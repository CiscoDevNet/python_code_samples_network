import paramiko

def Server1():
    l_password = "Password"
    l_host = "IP"
    l_user = "UserName"
    ssh = paramiko.SSHClient()
    ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    ssh.connect(l_host, username=l_user, password=l_password)    
    transport = ssh.get_transport()
    session = transport.open_session()
    session.set_combine_stderr(True)
    session.get_pty()
    session.exec_command("ls")
    stdin = session.makefile('wb', -1)
    stdout = session.makefile('rb', -1)
    stdin.write(l_password +'\n')
    stdin.flush()
    for line in stdout.read().splitlines():
        print ('host: %s: %s' % (l_host, line))

#For Other Servers
def Server2():
    l_password = "Password"
    l_host = "IP"
    l_user = "UserName"
    ssh = paramiko.SSHClient()
    ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    ssh.connect(l_host, username=l_user, password=l_password)    
    transport = ssh.get_transport()
    session = transport.open_session()
    session.set_combine_stderr(True)
    session.get_pty()
    session.exec_command("sudo brctl show")
    stdin = session.makefile('wb', -1)
    stdout = session.makefile('rb', -1)
    stdin.write(l_password +'\n')
    stdin.flush()
    for line in stdout.read().splitlines():        
        print ('host: %s: %s' % (l_host, line))

#For Other Servers
        
def Server3():
    l_password = "Password"
    l_host = "IP"
    l_user = "UserName"
    ssh = paramiko.SSHClient()
    ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    ssh.connect(l_host, username=l_user, password=l_password)    
    transport = ssh.get_transport()
    session = transport.open_session()
    session.set_combine_stderr(True)
    session.get_pty()
    session.exec_command("Command")
    stdin = session.makefile('wb', -1)
    stdout = session.makefile('rb', -1)
    stdin.write(l_password +'\n')
    stdin.flush()
    for line in stdout.read().splitlines():        
        print ('host: %s: %s' % (l_host, line))

    
#For Other Servers

def Server4():
    l_password = "Password"
    l_host = "IP"
    l_user = "UserName"
    ssh = paramiko.SSHClient()
    ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    ssh.connect(l_host, username=l_user, password=l_password)    
    transport = ssh.get_transport()
    session = transport.open_session()
    session.set_combine_stderr(True)
    session.get_pty()
    session.exec_command("Command")
    stdin = session.makefile('wb', -1)
    stdout = session.makefile('rb', -1)
    stdin.write(l_password +'\n')
    stdin.flush()
    for line in stdout.read().splitlines():        
        print ('host: %s: %s' % (l_host, line))

def Server5():
    l_password = "Password"
    l_host = "IP"
    l_user = "UserName"
    ssh = paramiko.SSHClient()
    ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    ssh.connect(l_host, username=l_user, password=l_password)    
    transport = ssh.get_transport()
    session = transport.open_session()
    session.set_combine_stderr(True)
    session.get_pty()
    session.exec_command("Command")
    stdin = session.makefile('wb', -1)
    stdout = session.makefile('rb', -1)
    stdin.write(l_password +'\n')
    stdin.flush()
    for line in stdout.read().splitlines():        
        print ('host: %s: %s' % (l_host, line))

Server1() 
#Server2()
#Server3()
#Server4()
#Server5()
