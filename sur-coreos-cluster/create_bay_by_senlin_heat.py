import logging
import time
from sur.client import SURClient
from sur.action.senlin.clusters import Cluster
from sur.action.senlin.nodes import Node
from sur.action.senlin.profiles import Profile
from sur.action.senlin.policies import ScalingInPolicy as SIPolicy
from sur.action.senlin.policies import ScalingOutPolicy as SOPolicy
from sur.action.senlin.webhooks import Webhook

LOG = logging.getLogger(__name__)
logging.basicConfig(level=logging.INFO)


def wait_for_node_active(sc, node):
    while True:
        status = Node.node_show(sc, node)['node']['status']
        if status == 'ACTIVE':
            break
        time.sleep(1)


def attach_policy(sc, **params):
    cluster_name = params.get('cluster_name', 'sur_cluster')
    
    # create scaling policy
    si_policy_name = cluster_name + '_si_policy'
    so_policy_name = cluster_name + '_so_policy'

    si_policy_spec = params.get('si_policy_spec', None)
    so_policy_spec = params.get('so_policy_spec', None)

    SIPolicy.policy_create(sc, si_policy_name, si_policy_spec)
    SOPolicy.policy_create(sc, so_policy_name, so_policy_spec)
    time.sleep(1)

    Cluster.cluster_policy_attach(sc, cluster_name, si_policy_name)
    Cluster.cluster_policy_attach(sc, cluster_name, so_policy_name)


def create_stack(sc, **params):
    master_profile_name = params.get('master_profile_name', 'master_profile')
    minion_profile_name = params.get('minion_profile_name', 'minion_profile')

    master_profile_spec = params.get('master_profile_spec', None)
    minion_profile_spec = params.get('minion_profile_spec', None)

    cluster_name = params.get('cluster_name', 'sur_cluster')

    # create master profile
    Profile.profile_create(sc, master_profile_name, 'os.heat.stack',
        master_profile_spec, '')
    time.sleep(1)

    master_name = cluster_name + '_master'
    # create master
    Node.node_create(sc, master_name, None, master_profile_name)
    time.sleep(5) 
    # wait master active
    wait_for_node_active(sc, master_name)

    master_stack_id = Node.node_show(sc, master_name)['node']['physical_id']
    LOG.info('Master create successfully! master_stack_id=%s' % master_stack_id)

    # create minion profile
    Profile.profile_create(sc, minion_profile_name, 'os.heat.stack',
        minion_profile_spec, '')
    time.sleep(1)

    # create cluster
    Cluster.cluster_create(sc, cluster_name, minion_profile_name)
    time.sleep(1)

    # join master
    Node.node_join(sc, master_name, cluster_name)

    node_count = params.get('node_count', 1)
    
    # create minions
    for i in range(node_count):
        Node.node_create(sc, cluster_name + '_minion_' + str(i), cluster_name,
            minion_profile_name)
        time.sleep(1)

    # attach scaling policy
    attach_policy(sc, **params)

    # create scale-out webhook
    wb = Webhook.cluster_webhook_create(sc, cluster_name + '_so_webhook',
        cluster_name, 'CLUSTER_SCALE_OUT', {})
    time.sleep(1)
    wb_url = wb['webhook']['url']
    LOG.info('webhook_url=%s' % wb_url)


def main():
    sc = SURClient().setup_client()
    
    params = {
        'master_profile_spec': 'specs/heat_stack_random_string.yaml',
        'minion_profile_spec': 'specs/heat_stack_random_string.yaml',
	'node_count': 2,
	'si_policy_spec': 'specs/scaling_policy.spec',
	'so_policy_spec': 'specs/scaling_policy.spec'
    }
    
    create_stack(sc, **params)	


if __name__ == '__main__':
    main()
