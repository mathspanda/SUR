import time
from sur.client import SURClient
from sur.action.senlin.clusters import Cluster
from sur.action.senlin.nodes import Node
from sur.action.senlin.profiles import Profile


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

    # create master
    Node.node_create(sc, cluster_name + '_master', None, master_profile_name) 

    # create minion profile
    Profile.profile_create(sc, minion_profile_name, 'os.heat.stack',
        minion_profile_spec, '')
    time.sleep(1)

    # create cluster
    Cluster.cluster_create(sc, cluster_name, minion_profile_name)
    time.sleep(1)

    # join master
    Node.node_join(sc, cluster_name + '_master', cluster_name)

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
