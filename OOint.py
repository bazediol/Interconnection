class Server:
    
    def __init__(self):
        self.data = None
        
    def rules (self):
        pass
        
    def gateways (self):
        pass
    
    def iptables (self):
        self.data += "\nnano /etc/sysconfig/iptables\n"
        self.data +="\n#{}\n".format(self.company)
        for IP in self.IPs:
            self.data +="-A INPUT -p tcp --dport 1024: -s {} -j ACCEPT\n".format(IP)
            self.data +="-A INPUT -p udp --dport 1024: -s {} -j ACCEPT\n".format(IP)
    
    def acl(self):
        self.data += "\nnano /etc/freeswitch/autoload_configs/acl.conf.xml\n\n"
        for IP in self.IPs:
            self.data +='      <node type="allow" cidr="{}/32"/>\n'.format(IP)
    
    def carriers (self, number, company):
        pass
    
    def getData (self):
        pass
    
class Server29(Server):
    
    def __init__(self, company, IPs, trunks, cps):
        #Server.__init__(self)
        self.company = company
        self.IPs = IPs
        self.trunks = trunks
        self.cps = cps
        self.data = 'Server .29\n'
    
    def rules (self):
        self.data += "\nnano /etc/opensips/db/dr_rules\n\n"
        for trunk, prefix in self.trunks.items():
            self.data +="0:XXX:{}:20100801T000000|0:0::#out16:{}|XXXXXXX|{}:{}_{}\n".format(prefix, len(prefix), self.cps, self.company, trunk)
    
    def gateways (self):
        self.data += "\nnano /etc/opensips/db/dr_gateways\n\n"
        for IP in self.IPs:
        #data += "0:out-gwXXX:2:sip\:{}\:5060:0:::0:0::{}\n".format(IP, company)
            self.data += "0:in-gwXXXX:1:sip\:{}\:5060:0::XXX:0:0::{}\n".format(IP, self.company)
            
    def getData(self):
        self.rules ()
        self.gateways ()
        self.iptables ()
        self.data += '\nsudo /etc/init.d/iptables restart\nsudo opensipsctl fifo dr_reload\n'
        print self.data

class Server99 (Server):
    
    def __init__(self, IPs, company):
        self.IPs = IPs
        self.company = company
        self.data = '\nServer .99\n'
        
    def getData(self):
        self.iptables()
        self.acl()
        self.data += "\nsudo /bin/systemctl restart iptables.service\n"
        print self.data
        
class Server103 (Server):
    
    def __init__(self, IPs, company):
        self.IPs = IPs
        self.company = company
        self.data = '\nServer .103\n'
        
    def getData(self):
        self.iptables()
        self.acl()
        self.data += "\nsudo /bin/systemctl restart iptables.service\n"
        print self.data
        
class Server49 (Server):
    
    def __init__(self, company, IPs, trunks):
        self.company = company
        self.IPs = IPs
        self.trunks = trunks
        self.data = '\nServer .49\n'
        
    def rules (self):
        self.data += "\nnano /etc/opensips/db/dr_rules\n\n"
        for trunk, prefix in self.trunks.items():
            self.data +="0:1:XXXXXXX:20100801T000000|0:0::#outXX:7|{}|0:from_outfs_to_{}_{}\n".format(prefix, self.company.replace(' ', '_'), trunk)
            
    def iptables (self):
        self.data += "\nnano /etc/sysconfig/iptables\n"
        self.data +="\n#{}\n".format(company)
        for IP in self.IPs:
            self.data +="-A INPUT -p udp --dport 1024: -s {} -j ACCEPT\n".format(IP)

    def gateways (self):
        self.data  += '\nnano /etc/opensips/db/dr_gateways\n'
        for IP in self.IPs:
            self.data += "\n0:out-gwXXX:2:sip\:{}\:5060:0:::0:0::{}\n".format(IP, self.company)
    
    def carriers (self):
        self.data += '\nnano /etc/opensips/db/dr_carriers\n\n'
        if len(self.IPs) == 1:
            self.data += "0:outXX:out-gwXXX:0:0:to:{}\n".format(self.company.replace(' ', '_'))
        elif len(self.IPs) == 2:
            self.data += "0:outXX:out-gwXXX=50,out-gwXXX=50:1:0:to:{}\n".format(self.company.replace(' ', '_'))
        elif len(self.IPs) == 3:
            self.data += "0:outXX:out-gwXXX=33,out-gwXXX=33,out-gwXXX=33:1:0:to:{}\n".format(self.company.replace(' ', '_'))
        else:
            self.data += "Need to clarify with admin!!!\n"
            
    def getData(self):
        self.rules()
        self.iptables()
        self.gateways()
        self.carriers()
        self.data += '\nsudo /etc/init.d/iptables restart\nsudo opensipsctl fifo dr_reload\n'
        print self.data
    
company = 'IPstudio'
IPs = ['192.168.0.1']
trunks = {'Silver': '001', 'Gold': '002', 'Platinum': '003'}
cps = 10

srv29 = Server29(company, IPs, trunks, cps)
srv99 = Server99(IPs, company)
srv103 = Server103(IPs, company)
srv49 = Server49(company, IPs, trunks)
srv29.getData()
srv99.getData()
srv103.getData()
srv49.getData()