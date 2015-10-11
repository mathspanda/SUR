import logging
import time
from sur.client import SURClient
from sur.action.senlin.clusters import Cluster
from sur.action.senlin.nodes import Node
from sur.action.senlin.profiles import Profile

LOG = logging.getLogger(__name__)
logging.basicConfig(level=logging.INFO)


def wait_for_node_active(sc, node):
    while True:
        status = Node.node_show(sc, node)['node']['status']
        if status == 'ACTIVE':
            break
        time.sleep(1)


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

def main():
    sc = SURClient().setup_client()
    
    params = {
        'master_profile_spec': 'specs/heat_stack_random_string.yaml',
        'minion_profile_spec': 'specs/heat_stack_random_string.yaml',
	'node_count': 2
    }
    
    create_stack(sc, **params)	


if __name__ == '__main__':
    main()
