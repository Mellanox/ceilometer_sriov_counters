# ceilometer_SR-IOV_counters
Plugin for Ceilometer SR-IOV traffic counters

#### Table of Contents

1. [Overview - What is the Ceilometer SR-IOV traffic counters plugin?](#overview)
2. [Module description - What does the module do?](#module-description)
3. [Prerequisites - The basics to work with the plugin](#prerequisites)
4. [Configuration - How to configure the plugin?](#configuration)
5. [Description of the traffic counters](#description-of-the-traffic-counters)
6. [Show the traffic counters](#show-the-traffic-counters)

Overview
--------

The Mellanox Ceilometer SR-IOV module allows the OpenStack Ceilometer to collect measurements of SR-IOV counters.

Module description
------------------

The Mellanox Ceilometer SR-IOV module allows the OpenStack Ceilometer to collect measurements of SR-IOV counters.
The Ceilometer libvirt inspector looks for the an interface (tap device) that is bound to the VM.
The VM that is connected via SR-IOV doesn't have such interface therefore the libvirt inspector ignores it.
The Mellanox Ceilometer SR-IOV module looks for VF PCI Device of the VM, then it acquires the counters from
the driver and passes the counters to the OpenStack Ceilometer inspector.

Prerequisites
-------------

  *     Supported OS: RH6.X RH7.X
  *     OpenStack supported versions: Juno and later.
  *     Other requirements if exists: SR-IOV enable

Configuration
-------------

  *     To install the Ceilometer just install rpm file.
  *     Update /etc/ceilometer/ceilometer.conf
  ```
  hypervisor_inspector=mlnx_libvirt
  ```
  *     Restart Ceilometer
  
  ```
  RH7:# systemctl restart openstack-ceilometer-compute
  RH6:# service openstack-ceilometer-compute restart
  ```

Description of the traffic counters
-----------------------------------

  * network.outgoing.bytes
  * network.incoming.bytes
  * network.outgoing.packets
  * network.incoming.packets

Show the traffic counters
-------------------------

  * From OpenStack horizon: go to admin -> resource Usage and then query for the counters.
  * From cli run: ceilometer statistics -m (counter_name)
  ```
  for example: ceilometer statistics -m network.outgoing.bytes
  ```
