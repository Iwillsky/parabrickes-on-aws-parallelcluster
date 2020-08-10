#!/bin/bash
timestr=$(date "+%Y%m%d%H%M%S")

. "/etc/parallelcluster/cfnconfig"

case "${cfn_node_type}" in
    MasterServer)
        echo "Master launched."
    ;;
    ComputeFleet)
        echo "Compute launched."
        wget -P /home/ubuntu/ https://awshcls.s3.cn-northwest-1.amazonaws.com.cn/parabricks-on-awspcluster/gpumon.py
        nohup python -u /home/ubuntu/gpumon.py > /home/ubuntu/cwmon$timestr.log 2>&1 &
    ;;
*)
;; esac
