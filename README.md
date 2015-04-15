# ceilometer_sriov_counters
Plugin for Ceilometer SRIOV traffic counters

#### Table of Contents

1. [Overview - What is the Ceilometer SRIOV traffic counters plugin?](#overview)
2. [Module description - What does the module do?](#module-description)
3. [Prerequisites - The basics to work with the plugin](#prerequisites)
4. [Configuration - How to configure the plugin?](#configuration)
5. [Description of the traffic counters](#description-of-the-traffic-counters)
6. [Show the traffic counters](#show-the-traffic-counters)

Overview
--------

The Ceilometer SRiov traffic counters allow the ceilometer to inspect the traffic counters 
of the SRiov VM.

Module description
------------------

The ceilometer libvirt inspector looking for the interface that binded for the VM.
The SRiov VM do not create such an interface therefore the libvirt inspector ignore SRiov VM's.
The Ceilometer SRiov traffic counters plugin is looking for a SRiov VM's and then it acquire the SRiov
Counters from the SRiov driver and pass the counters to the ceilometer inspector.

Prerequisites
-------------

  *	Supported OS: RH6.X RH7.X
  *	OpenStack supported versions: Valid from Juno.
  *	Other requirements if exists: SRiov enable

Configuration
-------------

  *	To install the ceilometer just install the rpm file.
  *	Possiblem configurable parameters – There are no configurable parameters.

Description of the traffic counters
-----------------------------------

  * network.outgoing.bytes
  * network.incoming.bytes
  * network.outgoing.packets
  * network.incoming.packets


Show the traffic counters
-------------------------

  * From openstack horizon: go to admin -> resource Usage and then query for the counters.
  * From cli run: ceilometer  statistics -m  (counter_name)

  ```
  for example: ceilometer  statistics -m network.outgoing.bytes
  ```

