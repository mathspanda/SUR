'''
Created on Aug 16, 2015

'''

from sur.client import SenlinSURClient
from sur.action.policies import Policy
from sur.action.policies import LoadBalancingPolicy as LBPolicy
from sur.action.policies import ScalingInPolicy as SIPolicy
from sur.action.policies import ScalingOutPolicy as SOPolicy
from sur.action.clusters import Cluster
from sur.action.webhooks import Webhook


def main():
    # setup client
    sc = SenlinSURClient().setup_client()

    # create loadbalancing policy
    LBPolicy.policy_create(sc, 'coreos_lb', '/home/mp/Desktop/lb_policy_lbaas.spec')

    # attach loadbalancing policy
    Cluster.cluster_policy_attach(sc, 'coreos_cluster', 'coreos_lb')

    #create scaling policy
    SIPolicy.policy_create(sc, 'coreos_si', '/home/mp/Desktop/scaling_policy.spec')
    SOPolicy.policy_create(sc, 'coreos_so', '/home/mp/Desktop/scaling_policy.spec')

    # attach scaling policy
    Cluster.cluster_policy_attach(sc, 'coreos_cluster', 'coreos_si')
    Cluster.cluster_policy_attach(sc, 'coreos_cluster', 'coreos_so')

    # scale out cluster
    Cluster.cluster_scale_out(sc, 'coreos_cluster')
    # scale in cluster
    Cluster.cluster_scale_in(sc, 'coreos_cluster')
    
    # create scale-out webhook
    print Webhook.cluster_webhook_create(sc, 'test', 'coreos_cluster', 'CLUSTER_SCALE_OUT', {})


if __name__ == '__main__':
    main()
