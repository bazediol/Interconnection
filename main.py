#Interconnection commands

def server29 (company, IPs, trunks, cps):
    data = 'Server .29\n'
    data += rules (company, trunks, cps) + gateways (company, IPs) +  iptables (company, IPs)
    data += '\nsudo /etc/init.d/iptables restart\nsudo opensipsctl fifo dr_reload\n'
    return data

def server99 (IPs, company):
    data = "\nserver .99\n"
    data += iptables (company, IPs) + acl(IPs)
    data += "\nsudo /bin/systemctl restart iptables.service\n"
    return data
    
def server103 (IPs, company):
    data = "\nserver .103\n"
    data += iptables (company, IPs) + acl(IPs)
    data += "\nsudo /bin/systemctl restart iptables.service\n"
    return data

def server49 (company, IPs, trunks):
    data = '\nServer .49\n'
    data += rules_out (company, trunks) + iptables_out (company, IPs) + gateways_out (IPs, company) + carriers (len(IPs), company)
    data += '\nsudo /etc/init.d/iptables restart\nsudo opensipsctl fifo dr_reload\n'
    return data

def rules_out (company, trunks):
    data = "\nnano /etc/opensips/db/dr_rules\n\n"
    for trunk, prefix in trunks.items():
        data +="0:1:XXXXXXX:20100801T000000|0:0::#outXX:7|{}|0:from_outfs_to_{}_{}\n".format(prefix, company.replace(' ', '_'), trunk)
    return data

def carriers (number, company):
    data = '\nnano /etc/opensips/db/dr_carriers\n'
    if number == 1:
        data += "0:outXX:out-gwXXX=100:0:0:to:{}\n".format(company.replace(' ', '_'))
    elif number == 2:
        data += "0:outXX:out-gwXXX=50,out-gwXXX=50:1:0:to:{}\n".format(company.replace(' ', '_'))
    elif number == 3:
        data += "0:outXX:out-gwXXX=33,out-gwXXX=33,out-gwXXX=33:1:0:to:{}\n".format(company.replace(' ', '_'))
    else:
        data += "Need to clarify with admin!!!\n"
    return data

def gateways_out (IPs, company):
    data  = '\nnano /etc/opensips/db/dr_gateways\n'
    for IP in IPs:
        data += "0:out-gwXXX:2:sip\:{}\:5060:0:::0:0::{}\n".format(IP, company)
    return data

def acl (IPs):
    data = "\nnano /etc/freeswitch/autoload_configs/acl.conf.xml\n\n"
    for IP in IPs:
        data +='      <node type="allow" cidr="{}/32"/>\n'.format(IP)
    return data

def gateways (company, IPs):
    data = "\nnano /etc/opensips/db/dr_gateways\n\n"
    for IP in IPs:
        #data += "0:out-gwXXX:2:sip\:{}\:5060:0:::0:0::{}\n".format(IP, company)
        data += "0:in-gwXXXX:1:sip\:{}\:5060:0::XXX:0:0::{}\n".format(IP, company)
    return data

def iptables (company, IPs):
    data = "\nnano /etc/sysconfig/iptables\n"
    data +="\n#{}\n".format(company)
    for IP in IPs:
        data +="-A INPUT -p tcp --dport 1024: -s {} -j ACCEPT\n".format(IP)
        data +="-A INPUT -p udp --dport 1024: -s {} -j ACCEPT\n".format(IP)
    return data

def iptables_out (company, IPs):
    data = "\nnano /etc/sysconfig/iptables\n"
    data +="\n#{}\n".format(company)
    for IP in IPs:
        data +="-A INPUT -p udp --dport 1024: -s {} -j ACCEPT\n".format(IP)
    return data

def rules (company, trunks, cps):
    data = "\nnano /etc/opensips/db/dr_rules\n\n"
    for trunk, prefix in trunks.items():
        data +="0:XXX:{}:20100801T000000|0:0::#out16:{}|XXXXXXX|{}:{}_{}\n".format(prefix, len(prefix), cps, company, trunk)
    return data

def create_file (company, data):
    file_name = '{}.txt'.format(company)
    file = open (file_name, 'w')
    file.write(data)
    file.close
    print "Succeessfully done!\nFile is in the working folder"

def portal_interconnection ():
    trunks = {'Silver': '001', 'Gold': '002', 'Platinum': '003'}
    company = get_name()
    print 'Provide customer IPs'
    IPs = get_IP()
    data = 'Password is jimFR4unFErgh69%fbnDd\n'
    data += server29 (company, IPs, trunks, 10) + server99  (IPs, company)
    create_file (company, data)

def standard_interconnectin ():
    company = get_name()
    print '\n**********************\nProvide signal IPs'
    IPs_signal = get_IP()
    same = raw_input ("Are media IPs same? (y/n)")
    while True:
        if same == 'y':
            IPs_media = IPs_signal
            break
        elif same == 'n':
            print '\n**********************\nProvide media IPs'
            IPs_media = get_IP()
            break
        else:
            continue   
    IPs_all = set(IPs_signal + IPs_media)
    print '\n**********************\nEnter cursomter trunks details'
    trunks_in = get_trunks()
    print '\n**********************\nEnter our trunks details'
    trunks_out = get_trunks()
    data = 'Password is jimFR4unFErgh69%fbnDd\n'
    data += server29 (company, IPs_signal, trunks_in, 0) + server99 (IPs_media, company) + server103 (IPs_all, company) + server49(company, IPs_signal, trunks_out)
    create_file (company, data)
    
def get_IP():
    IPs = []
    print "Type CL to stop input"
    while True:
        IP = raw_input ('Enter IP:\n')
        str(IP)
        if IP == "CL":
            break
        else:
            IPs.append(IP)
    return IPs
    
def get_trunks():
    trunks = {}
    print "Type CL to stop input"
    while True:
        trunk = raw_input ('Enter trunk name:\n')
        if trunk == 'CL':
            break
        else:
            prefix = raw_input ('Enter prefix for {} trunk:\n'.format(trunk))
            trunks [trunk] = prefix
    return trunks

def get_name():
    company = raw_input ('Input company name:\n')
    while True:
        check = raw_input('Is company name "{}" correct? (y/n)'.format(company))
        if check == 'y':
            return company
            break
        elif check == 'n':
            company = raw_input ('Input company name:\n')
        else:
            continue
    return company

        
print "\nPress 1 for portal company interconnection \nPress 2 for standard intercoonection"
interconnection = input ()
if interconnection == 1:
    portal_interconnection ()
elif interconnection ==2:
    standard_interconnectin ()
else:
    print 'Only values 1 or 2 allowed'

