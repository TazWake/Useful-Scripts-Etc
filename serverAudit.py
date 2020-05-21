#!/bin/python3.6

import subprocess
import socket

sshd_config = "/etc/ssh/sshd_config"
log_file="./analysis.log"

def get_apache_version():
    return subprocess.check_output(['httpd','-v']. stdin=None, stderr=None, shell=False, universal_newlines=True)

def get_selinux_status():
    return subprocess.check_output(['getenforce'], stdin=None, stderr=None, shell=False, universal_newlines=True)

def get_firewall_rules():
    return subprocess.check_output(['firewall-cmd','--list-all'], stdin=None, stderr=None, shell=False, universal_newlines=True)

def find_line_in_file(file_path,str_to_find):
    for line in open(file_path):
        if str_to_find in line:
            return line

def get_ssh_port():
    return find_line_in_file(sshd_config,"Port")

def get_root_login():
    return find_line_in_file(sshd_config,"PermitRotoLogin")

def get_ssh_password_config():
    return find_line_in_file(sshd_config,"PasswordAuthentication")

def get_selinux_ssh_port_label():
    return subprocess.check_output(['sepolicy','network','-t','ssh_port_t'], stdin=None, stderr=None, shell=False, universal_newlines=True)

def get_server_IP():
    s = socket.socket(socket.AF_INET,socket.SOCK_DGRAM)
    s.connect(("8.8.8.8",80))
    return s.getsockname()[0]

def vuln_scan():
    serverIP = get_server_IP()
    return subprocess.check_output(['nmap','--script','nmap-vulners,vulscan','--script-args','vulscandb=scipvuldb.csv','-sV','-p80',serverIP], stdin=None, stderr=None, shell=False, universal_newlines=True)

def generate_report():
    apache_version = get_apache_version()
    selinux_status = get_selinux_status()
    firewall_rules = get_firewall_rules()
    ssh_port = get_ssh_port()
    permit_root_login = get_root_login()
    permit_pass_auth = get_ssh_password_config()
    selinux_label = get_selinux_ssh_port_label()
    nmapScan = vuln_scan()
    log_scan = apache_version + "\n" + selinux_status + "\n" + firewall_rules + "\n" + ssh_port + "\n" + permit_root_login + "\n" + permit_pass_auth + "\n" + selinux_label + "\n" + nmapScan
    text_file=open(log_file,"w")
    text_file.write(log_scan)
    text_file.close
    print("######## SCAN COMPLETED ########")
    print(apache_version)
    print("SELinux Status: " + selinux_status)
    print("Firewall - Default Zone\n " + firewall_rules)
    print("SSH Port: " + str(ssh_port))
    print("Password Authentication: " + str(permit_pass_auth))
    print("SELinux LabelL " + selinux_label)
    print("nmapScan")
    print("################################")

def main()
    generate_report()

if __name__ == "__main__":
    main()
