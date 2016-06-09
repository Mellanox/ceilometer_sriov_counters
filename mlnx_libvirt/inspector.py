#!/usr/bin/env python
#
# Copyright 2015 Mellanox Technologies, Ltd
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#    http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or
# implied.
# See the License for the specific language governing permissions and
# limitations under the License.
"""Implementation of Inspector abstraction for mlnx_libvirt."""

from lxml import etree
import os
import re

from oslo_config import cfg

from ceilometer.i18n import _
from ceilometer import utils
from oslo_log import log
from ceilometer.compute.virt import inspector as virt_inspector
from ceilometer.compute.virt.libvirt.inspector import LibvirtInspector

PORT_DIRECT_TYPE = "hostdev"
COUNTERS_DEST = "/sys/class/net/%(if_name)s/vf%(vf)s/statistics/%(cnt_name)s"


CONF = cfg.CONF
LOG = log.getLogger(__name__)

class MlnxLibvirtInspector(LibvirtInspector):

    def __init__(self):
        super(MlnxLibvirtInspector,self).__init__()
        self.counters_names = ("rx_bytes", "rx_packets", "tx_bytes", "tx_packets")
        self.counters_dic = dict([(key,0) for key in self.counters_names])
        self.regex_get_string = re.compile("\W+")
        self.regex_get_number = re.compile("\d+")
        self.regex_get_vf_number = re.compile("(\s+vf\s)(\d+)([\s+MAC]*)")

    def _init_vf_counters(self, if_name, vf_num):
        for counter_name in self.counters_names:
            counter_path = COUNTERS_DEST % {
                                            "if_name":if_name,
                                            "vf": vf_num,
                                            "cnt_name": counter_name
                                           }
            try:
                with open(counter_path,'r') as f:
                    counter_value = f.readline().strip()
                    self.counters_dic[counter_name] = int(counter_value)
            except Exception as e:
                LOG.error("Failed to open counter_path %(counter_path)s %(e)s" %
                          {'counter_path': counter_path, 'e': e})
                pass

    def inspect_vnics(self, instance):
        domain = self._get_domain_not_shut_off_or_raise(instance)

        tree = etree.fromstring(domain.XMLDesc(0))

        for iface in tree.findall('devices/interface'):
            if iface.get('type') != PORT_DIRECT_TYPE:
                #Not SRIOV
                generator = super(MlnxLibvirtInspector, self).inspect_vnics(instance)
                if hasattr(generator,"__iter__"):
                    for gen in generator:
                        yield gen
                return

            mac = iface.find('mac')
            if mac is not None:
                mac_address = mac.get('address')
            else:
                continue

            args = ["ip" ,"link", "show"]
            try:
                (output, rc) = utils.execute(*args)
            except:
                LOG.error('Unable to run command: %s' % output)
                continue

            lines = output.split(os.linesep)

            name = vf_num = None

            for line in reversed(lines):
                if mac_address in line:
                    try:
                        vf_num =  int(self.regex_get_vf_number.match(line).groups()[1])
                    except:
                        continue

                elif vf_num is not None:
                    if self.regex_get_number.match(line) is not None:
                        name = self.regex_get_string.split(line)[1].strip()
                        break

            if vf_num is None or name is None:
                LOG.error('Unable to reach counters: unknown VF number or interface name for MAC=%s' % mac_address)
                continue

            #filtertref (fref) is not supported in SRIOV
            interface = virt_inspector.Interface(name=name, mac=mac_address,
                                                 fref=None, parameters=None)

            self._init_vf_counters(name, vf_num)
            stats = virt_inspector.InterfaceStats(rx_bytes=self.counters_dic["rx_bytes"],
                                                  rx_packets=self.counters_dic["rx_packets"],
                                                  tx_bytes=self.counters_dic["tx_bytes"],
                                                  tx_packets=self.counters_dic["tx_packets"])
            yield (interface, stats)
