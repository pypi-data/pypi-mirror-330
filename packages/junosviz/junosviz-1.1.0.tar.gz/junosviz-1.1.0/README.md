#junosviz

`junosviz` is a Python package for monitoring and alerting BGP states and metrics of juniper  using snmp, NETCONF, and gNMI.

## Features(v1.1.0)
- Predict internet prefix count in DFZ zone
- bogon filtering automation for ISP gateways
- State monitoring of juniper hardware devices
- Monitor BGP peer state.
- Return Data can be easily feeded into timeseries database like influx db(so you can easily visulize it using grafana)
- Retrieve bgp metrics using Juniper-specific MIBs,openconfig yang models,ietf and juniper native yang models
- Generate alerts for BGP state changes.(in built bettertack alerting method)
- Support bgp next hop encoding capablity.
- tested on junos 23.4R2-S2.1 
- support ipv6 and ipv4
- mibs not needed, all are handled by the code
- you can detect anomalies and predict DDOS attacks caused by bgp updates,using predicted prefix counts and actual prefix counts.
- Structured row data is easily availble for feeding to a ML or AI platform which you desire
- Easy integratoin with Nornir framework

## Installation
Install `junosviz` via pip:
```bash
pip install junosviz

