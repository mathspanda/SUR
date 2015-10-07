name: coreos_server
flavor: 0 
image: "CoreOS"
key_name: testkey
networks:
  - network: private
user_data: cloud-config.yaml

