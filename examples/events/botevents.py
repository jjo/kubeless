import json
from kubernetes import client, config

config.load_incluster_config()

v1 = client.CoreV1Api()


def handler(context):
    msg = "k8s event: %s" % context

    # print "MSG: {}".format(msg)
    return msg
