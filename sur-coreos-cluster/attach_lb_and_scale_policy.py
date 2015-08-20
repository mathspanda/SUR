'''
Created on Aug 16, 2015

'''

from sur.client import SURClient
from sur.action.senlin.policies import Policy
from sur.action.senlin.policies import LoadBalancingPolicy as LBPolicy
from sur.action.senlin.policies import ScalingInPolicy as SIPolicy
from sur.action.senlin.policies import ScalingOutPolicy as SOPolicy
from sur.action.senlin.clusters import Cluster
from sur.action.senlin.webhooks import Webhook
from sur.action.ceilometer.alarms import Alarm


def main():
    # setup senlin client
    sc = SURClient('localhost', '8778', '1').setup_client()

    # create loadbalancing policy
#     LBPolicy.policy_create(sc, 'coreos_lb', '/home/mp/Desktop/lb_policy_lbaas.spec')

    # attach loadbalancing policy
#     Cluster.cluster_policy_attach(sc, 'coreos_cluster', 'coreos_lb')

    #create scaling policy
#     SIPolicy.policy_create(sc, 'coreos_si', '/home/mp/Desktop/scaling_policy.spec')
#     SOPolicy.policy_create(sc, 'coreos_so', '/home/mp/Desktop/scaling_policy.spec')

    # attach scaling policy
#     Cluster.cluster_policy_attach(sc, 'coreos_cluster', 'coreos_si')
#     Cluster.cluster_policy_attach(sc, 'coreos_cluster', 'coreos_so')
    
    # create scale-out webhook
    wb = Webhook.cluster_webhook_create(sc, 'so_webhook', 'coreos_cluster',
                                        'CLUSTER_SCALE_OUT', {})
    wb_url = wb['webhook']['url']
    
    # setup ceilometer client
    cc = SURClient('localhost', '8777', '2', 'ceilometer').setup_client()
    
    # create ceilometer threshold alarm
    alarm_args = {
        'name': 'test_alarm',
        'meter_name': 'cpu_util',
        'threshold': 50.0,
        'state': 'alarm',
        'severity': 'moderate',
        'enabled': True,
        'repeat_actions': False,
        'alarm_actions': [wb_url],
        'comparison_operator': 'gt',
        'statistic': 'max'
    }
    Alarm.alarm_threshold_create(cc, **alarm_args)


if __name__ == '__main__':
    main()
