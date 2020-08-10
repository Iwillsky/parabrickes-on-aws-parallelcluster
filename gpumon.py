# Copyright 2017 Amazon.com, Inc. or its affiliates. All Rights Reserved.
#
# Licensed under the Apache License, Version 2.0 (the "License").
# You may not use this file except in compliance with the License.
# A copy of the License is located at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#  
#  or in the "license" file accompanying this file. This file is distributed 
#  on an "AS IS" BASIS, WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either 
#  express or implied. See the License for the specific language governing 
#  permissions and limitations under the License.
#
# Modifier: Xianghui Cui (github.com/iwillsky)
# Customize metrics 
# Aug,01,2020

import urllib2
import boto3
from pynvml import *
from datetime import datetime
from time import sleep

### CHOOSE REGION ####
EC2_REGION = 'us-east-2'

###CHOOSE NAMESPACE PARMETERS HERE###
my_NameSpace = 'CW-Parabricks' 

### CHOOSE PUSH INTERVAL ####
sleep_interval = 10 

### CHOOSE STORAGE RESOLUTION (1 / 60) ####
store_reso = 1

#Instance information
BASE_URL = 'http://169.254.169.254/latest/meta-data/'
INSTANCE_ID = urllib2.urlopen(BASE_URL + 'instance-id').read()
INSTANCE_AZ = urllib2.urlopen(BASE_URL + 'placement/availability-zone').read()
EC2_REGION = INSTANCE_AZ[:-1]

# Create CloudWatch client
cloudwatch = boto3.client('cloudwatch', region_name=EC2_REGION)

# Flag to push to CloudWatch
PUSH_TO_CW = True

def getPowerDraw(handle):
    try:
        powDraw = nvmlDeviceGetPowerUsage(handle) / 1000.0
        powDrawStr = '%.2f' % powDraw
    except NVMLError as err:
        powDrawStr = handleError(err)
        PUSH_TO_CW = False
    return powDraw

def getTemp(handle):
    try:
        temp = str(nvmlDeviceGetTemperature(handle, NVML_TEMPERATURE_GPU))
    except NVMLError as err:
        temp = handleError(err) 
        PUSH_TO_CW = False
    return temp

def getUtilization(handle):
    try:
        util = nvmlDeviceGetUtilizationRates(handle)
        gpu_util = str(util.gpu)
        mem_util = str(util.memory)
    except NVMLError as err:
        error = handleError(err)
        gpu_util = error
        mem_util = error
        PUSH_TO_CW = False
    return util, gpu_util, mem_util

def logResults(i, util, gpu_util, mem_util, powDrawVal, temp):
    if (PUSH_TO_CW):
        MY_DIMENSIONS=[
                    {
                        'Name': 'InstanceId',
                        'Value': INSTANCE_ID
                    },                    
                    {
                        'Name': 'GPUNumber',
                        'Value': str(i)
                    }
                ]
        cloudwatch.put_metric_data(
            MetricData=[
                {
                    'MetricName': 'GPU-Usage',
                    'Dimensions': MY_DIMENSIONS,
                    'Unit': 'Percent',
                    'StorageResolution': store_reso,
                    'Value': util.gpu
                },
                {
                    'MetricName': 'GPU-MemUsage',
                    'Dimensions': MY_DIMENSIONS,
                    'Unit': 'Percent',
                    'StorageResolution': store_reso,
                    'Value': util.memory
                },
                {
                    'MetricName': 'GPU-Power',
                    'Dimensions': MY_DIMENSIONS,
                    'Unit': 'Percent',
                    'StorageResolution': store_reso,
                    'Value': powDrawVal
                }           
            ],
            Namespace=my_NameSpace
        )

def main():
    try:
        nvmlInit()
        deviceCount = nvmlDeviceGetCount()

        while True:
            PUSH_TO_CW = True
            # Find the metrics for each GPU on instance
            for i in range(deviceCount):
                handle = nvmlDeviceGetHandleByIndex(i)

                powDrawVal = getPowerDraw(handle)
                temp = getTemp(handle)
                util, gpu_util, mem_util = getUtilization(handle)
                #print(gpu_util, mem_util, temp, powDrawVal)
                logResults(i, util, gpu_util, mem_util, powDrawVal, temp)

            sleep(sleep_interval)
    finally:
        nvmlShutdown()

if __name__=='__main__':
    main()


