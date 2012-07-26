# coding: utf-8
"""This simple tool was made for creating new dns zones. 
!!! Check and replace IP's in the code inside the script !!!
Simply start it using Python, with domain name as first argument.
Tested on Python 2.7 & 2.6
"""

import time
import random
import sys

def NSD(name):
    if '-h' in name or '--help' in name:
        print __doc__
        sys.exit(1)
    ns1 = ['192.168.0.165','192.168.1.165','ns1.yoursns.com.']
    ns2 = ['192.168.0.166','192.168.1.166','ns2.yoursns.com.']
    serial = time.strftime('%Y%m%d%H%M%S')
    secret = ''.join(random.choice('0123456789ABCDEF') for i in range(16)).encode('base64').strip()
    path_master = '/etc/nsd/zones/master/'
    path_slave = '/etc/nsd/zones/slave/'

    TTL = ['$TTL 1800 ;minimum ttl', '''(
                    %s      ;serial
                    3600            ;refresh
                    9600            ;retry
                    180000          ;expire
                    600             ;negative ttl
                    )''' % serial]

    MX = 'mx.%s.' % name
    A = {'.':'192.168.0.163', 'www':'192.168.0.163', 'mail':'192.168.0.164', 'mx':'192.168.0.164'}

    key_zone_m = {'key':{
                    'name':name,
                    'algorithm':'hmac-md5',
                    'secret':secret},
                'zone':{
                    'name':name,
                    'zonefile':path_master+name, 
                    'notify':[(ns2[0], name), (ns2[1], name)],
                    'provide-xfr':[(ns2[0], name), (ns2[1], name)]}}

    key_zone_s = {'key':{
                    'name':name,
                    'algorithm':'hmac-md5',
                    'secret':secret},
                'zone':{
                    'name':name,
                    'zonefile':path_slave+name, 
                    'allow-notify':[(ns1[0], name), (ns1[1], name)],
                    'request-xfr':[('AXFR '+ns1[0], name), ('AXFR '+ns1[1], name)]}}


    for i in 'key', 'zone':
        print i + ':    '
        for j in key_zone_m[i].keys():
            if j == 'provide-xfr' or j == 'notify':
                for k in key_zone_m[i][j]:
                    print '    ' + j + ':    ' + k[0] + '    ' +  k[1]
            else:
                if j == 'algorithm':
                    print '    ' + j + ':    ' + key_zone_m[i][j]
                else:
                    print '    ' + j + ':    ', '"' + key_zone_m[i][j] + '"'

    print ''

    for i in 'key', 'zone':
        print i + ':    '
        for j in key_zone_s[i].keys():
            if j == 'request-xfr' or j == 'allow-notify':
                for k in key_zone_s[i][j]:
                    print '    ' + j + ':    ' + k[0] + '    ' +  k[1]
            else:
                if j == 'algorithm':
                    print '    ' + j + ':    ' + key_zone_s[i][j]
                else:
                    print '    ' + j + ':    ', '"' + key_zone_s[i][j] + '"'

    print ''

    print TTL[0]
    print name+'.    ' + 'IN    SOA', ns1[2], 'hostmaster.'+name+'.', TTL[1]
    print '    '*4, 'NS', '    ', ns1[2]
    print '    '*4, 'NS', '    ', ns2[2]
    print '    '*4, 'A', '    '*2, A['.']
    print '    '*3, 'MX    5', MX

    for i in A.keys():
        if i != '.':
            print i, '    '*2,  'A', '    '*2, A[i]


if __name__ == '__main__':
   NSD(sys.argv[1])
