import configparser
import os
import paramiko
from os.path import expanduser

# given a list of hosts, a listing of local files, and a remote dir, deploy
def deploy_to_host(list_of_hosts, local_files, remote_dir, local_node_code):
    for host in list_of_hosts:
        transport = paramiko.Transport((host, 22))
        transport.connect(username="pi", password="raspberry")
        sftp = paramiko.sftp_client.SFTPClient.from_transport(transport)
        for node_file in local_files:
            actual_node_file = os.path.join(local_node_code, node_file)
            if os.path.isfile(actual_node_file) and node_file[-len('.csv'):] != '.csv':
                remote_node_code_file = os.path.join(remote_dir, node_file)
                print("Placing the {0} file on {1}.".format(actual_node_file, host))
                sftp.put(actual_node_file, remote_node_code_file, confirm=True)

        # deploy one more file
        model_path_end = "cloud_computing/Parallel-Image-Processing/models/research/slim/nets/inception_v1_dist.py"
        model_file = expanduser("~/"+model_path_end)
        remote_model_file = "/home/pi/"+model_path_end
        print("Placing the {0} file on {1}.".format(model_file, host))
        sftp.put(model_file, remote_model_file, confirm=True)


def deploy():
    # build config
    config_file = expanduser("~/cloud_computing/Parallel-Image-Processing/node_code/ps_worker.ini")
    config = configparser.ConfigParser()
    config.read(config_file)
    jobs = dict(config.items("IP Listing"))

    # build remote and local paths
    local_node_code = expanduser("~/cloud_computing/Parallel-Image-Processing/node_code/")
    remote_node_code = "/home/pi/cloud_computing/Parallel-Image-Processing/node_code/"
    local_node_code_files = os.listdir(expanduser("~/cloud_computing/Parallel-Image-Processing/node_code/"))

    deploy_to_host(jobs["worker"].split(", "), local_node_code_files, remote_node_code, local_node_code)
