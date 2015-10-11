#!/bin/sh

senlin node-delete sur_cluster_master
senlin cluster-delete sur_cluster
senlin profile-delete master_profile
senlin profile-delete minion_profile
