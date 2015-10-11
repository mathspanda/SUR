from sur.client import SURClient
from sur.action.senlin.nodes import Node
from sur.action.senlin.profiles import Profile

def main():
    sc = SURClient('localhost', '8778', '1').setup_client()
    
    print Profile.profile_create(sc, 'test_profile', 'os.heat.stack',
        'specs/heat_stack_random_string.yaml', '')

if __name__ == '__main__':
    main()
