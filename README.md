# pynfvo
Python client for NFVO package 4.2 for NSO

admin@ncs# show packages package tailf-nfvo
packages package tailf-nfvo
 package-version 1.3
 description     "Tail-f NFVO"
 ncs-min-version [ 4.2 ]
 directory       ./state/packages-in-use/1/tailf-nfvo
 oper-status up



>>> nso.get_api_version()
u'0.5'


Sample use:

import pynfvo
nso = pynfvo.Nso()
nso.create_nfvo_vnfd('sg-vrouter-vnfd.json')
nso.get_nfvo_vnfd('vrouter-vnfd')
nso.create_nfvo_vnfr('sg_vrouter4_vnfr.json')
nso.get_nfvo_vnfrs()
nso.get_nfvo_vnfr('esc23-demo', 'vr1dep', 'esc23')
nso.get_nfvo_vnfr_status('esc23-demo', 'vr1dep', 'esc23')
