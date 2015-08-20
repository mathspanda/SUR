'''
Created on Aug 6, 2015

'''

import argparse
import logging
import time

from sur.client import SURClient
from sur.action.senlin.clusters import Cluster
from sur.action.senlin.nodes import Node
from sur.action.senlin.profiles import Profile

LOG = logging.getLogger(__name__)
logging.basicConfig(level=logging.INFO)


def main():
    # parse arguments
    parser = argparse.ArgumentParser()
    parser.add_argument("profile_name", help="the name of profile")
    parser.add_argument("spec_file", help="the location of spec file")
    parser.add_argument("cluster_name", help="the name of cluster")
    parser.add_argument("node_number", help="the number of nodes", type=int)
    args = parser.parse_args()

    LOG.info('Start build coreos cluster %s...' % (args.cluster_name))

    # setup client
    sc = SURClient().setup_client()

    # create profile
    LOG.info('Start create profile %s...' % (args.profile_name))
    result = Profile.profile_create(sc, args.profile_name, 'os.nova.server',
                                    args.spec_file, '1111')
    time.sleep(1)
    LOG.info(result)
    LOG.info('End create profile %s' % (args.profile_name))

    # create cluster
    LOG.info('Start create cluster %s...' % (args.cluster_name))
    result = Cluster.cluster_create(sc, args.cluster_name, args.profile_name)
    time.sleep(1)
    LOG.info(result)
    LOG.info('End create cluster %s' % (args.cluster_name))

    # create nodes
    for i in range(args.node_number):
        LOG.info('Creating node%s of cluster %s' % (i, args.cluster_name))
        result = Node.node_create(sc, '%s_node%s' % (args.cluster_name, i),
                                  args.cluster_name, args.profile_name)
        time.sleep(1)
        LOG.info(result)

    LOG.info('End build coreos cluster %s...' % (args.cluster_name))


if __name__ == '__main__':
    main()
