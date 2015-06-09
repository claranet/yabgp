# Copyright 2015 Cisco Systems, Inc.
# All rights reserved.
#
#    Licensed under the Apache License, Version 2.0 (the "License"); you may
#    not use this file except in compliance with the License. You may obtain
#    a copy of the License at
#
#         http://www.apache.org/licenses/LICENSE-2.0
#
#    Unless required by applicable law or agreed to in writing, software
#    distributed under the License is distributed on an "AS IS" BASIS, WITHOUT
#    WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied. See the
#    License for the specific language governing permissions and limitations
#    under the License.

import time

from oslo.config import cfg

from yabgp.common import constants as common_cons


def get_peer_conf_and_state(peer_ip=None):
    """
    get peer configuration and state
    :param peer_ip: peer ip address
    :return:
    """
    def get_peer_state(peer):
        one_peer_state = {key: cfg.CONF.bgp.running_config[peer][key] for key in [
            'remote_as', 'remote_addr', 'local_as', 'local_addr']}
        fsm = cfg.CONF.bgp.running_config[peer]['factory'].fsm.state
        one_peer_state['fsm'] = common_cons.stateDescr[fsm]
        if fsm == common_cons.ST_ESTABLISHED:
            one_peer_state['uptime'] = time.time() - cfg.CONF.bgp.running_config[peer]['factory'].fsm.uptime
        else:
            one_peer_state['uptime'] = 0
        return one_peer_state

    if peer_ip:
        peer_state = {}
        if peer_ip in cfg.CONF.bgp.running_config:
            peer_state = get_peer_state(peer_ip)
        return {'peer': peer_state}
    # for multi peers
    result = {'peers': []}
    for peer_ip in cfg.CONF.bgp.running_config:
        result['peers'].append(get_peer_state(peer_ip))
    return result


def get_peer_msg_statistic(peer_ip=None):
    """
    get peer send and receive message statistic
    :param peer_ip: peer ip address
    :return:
    """

    if peer_ip and peer_ip in cfg.CONF.bgp.running_config:
        return {
            'send': cfg.CONF.bgp.running_config[peer_ip]['factory'].fsm.protocol.msg_sent_stat,
            'receive': cfg.CONF.bgp.running_config[peer_ip]['factory'].fsm.protocol.msg_recv_stat,
        }
    else:
        return {}
