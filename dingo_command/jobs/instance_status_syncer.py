import time
from datetime import datetime, timedelta
from apscheduler.schedulers.blocking import BlockingScheduler
from apscheduler.schedulers.background import BackgroundScheduler
from oslo_log import log

from dingo_command.db.models.node.sql import NodeSQL
from dingo_command.db.models.instance.sql import InstanceSQL
from dingo_command.common.nova_client import NovaClient

LOG = log.getLogger(__name__)

scheduler = BackgroundScheduler()
blocking_scheduler = BlockingScheduler()
# 启动完成后执行
run_time_10s = datetime.now() + timedelta(seconds=10)  # 任务将在10秒后执行
run_time_30s = datetime.now() + timedelta(seconds=30)  # 任务将在30秒后执行


def start():
    # scheduler.add_job(fetch_bigscreen_metrics, 'interval', seconds=5, next_run_time=datetime.now())
    # 添加检查集群状态的定时任务，每60秒执行一次
    scheduler.add_job(check_instance_status, 'interval', seconds=60, next_run_time=datetime.now())
    scheduler.add_job(check_node_status, 'interval', seconds=60, next_run_time=datetime.now())
    scheduler.start()


def check_instance_status():
    """
    定期检查k8s集群状态并更新数据库
    """
    try:
        LOG.info(f"Starting check instance status at {time.strftime('%Y-%m-%d %H:%M:%S')}")

        # 获取所有状态为 creating、running 或 error 的集群
        query_params = {}
        # query_params["status_in"] = ["creating", "running", "error"]
        count, instances = InstanceSQL.list_instances(query_params, page_size=-1)

        for instance in instances:
            try:
                # 检查节点状态
                server_id = instance.server_id

                # 检查实例状态
                if server_id:
                    nova_client = NovaClient()
                    server = nova_client.nova_get_server_detail(server_id)

                    # 如果状态发生变化，更新集群状态
                    # if (server.get("status") == "ERROR" and instance.status != "error" or
                    #         server.get("status") != "ACTIVE" and instance.status == "running" or
                    #         server.get("status") == "ACTIVE" and instance.status != "running"):
                    LOG.info(f"Updating instance {instance.id} status from {instance.status} to "
                             f"{server.get('status')}")
                    if server.get("status") == "ERROR" and instance.status not in ("error", "deleting"):
                        instance.status = "error"
                        instance.status_msg = server.get("fault").get("details")
                    elif server.get("status") == "ACTIVE" and instance.status not in  ("deleting", "running"):
                        instance.status = "running"
                        instance.status_msg = ""
                    elif server.get("status") == "BUILD" and instance.status not in ("creating", "deleting"):
                        instance.status = "creating"
                        instance.status_msg = ""
                    elif server.get("status") == "PAUSED" and instance.status not in ("paused", "deleting"):
                        instance.status = "paused"
                        instance.status_msg = ""
                    elif server.get("status") == "SUSPENDED" and instance.status not in ("suspended", "deleting"):
                        instance.status = "suspended"
                        instance.status_msg = ""
                    elif server.get("status") == "SHUTOFF" and instance.status not in ("shutoff", "deleting"):
                        instance.status = "shutoff"
                        instance.status_msg = ""
                    elif (server.get("status") == "SHELVED_OFFLOADED" and instance.status 
                          not in ("shelved_offloaded", "deleting")):
                        instance.status = "shelved_offloaded"
                        instance.status_msg = ""
                    else:
                        continue
                    InstanceSQL.update_instance(instance)
            except Exception as e:
                LOG.error(f"Error checking status for instance {instance.id}: {str(e)}")
                if "could not be found." in str(e):
                    InstanceSQL.delete_instance(instance)
    except Exception as e:
        LOG.error(f"Error in instance_status: {str(e)}")


def check_node_status():
    """
    定期检查k8s集群状态并更新数据库
    """
    try:
        LOG.info(f"Starting check node status at {time.strftime('%Y-%m-%d %H:%M:%S')}")

        # 获取所有状态为 creating、running 或 error 的集群
        query_params = {}
        # query_params["status_in"] = ["creating", "running", "error"]
        count, nodes = NodeSQL.list_nodes(query_params, page_size=-1)

        for node in nodes:
            try:
                # 检查节点状态
                server_id = node.server_id

                # 检查实例状态
                if server_id:
                    nova_client = NovaClient()
                    server = nova_client.nova_get_server_detail(server_id)

                    # 如果状态发生变化，更新集群状态
                    # if (server.get("status") == "ERROR" and node.status != "error" or
                    #         server.get("status") != "ACTIVE" and node.status == "running" or
                    #         server.get("status") == "ACTIVE" and node.status != "running"):
                    LOG.info(f"Updating node {node.id} status from {node.status} to {server.get('status')}")
                    if server.get("status") == "ERROR" and node.status not in ("error", "deleting"):
                        node.status = "error"
                        node.status_msg = server.get("fault").get("details")
                    elif server.get("status") == "ACTIVE" and node.status not in ("deleting", "running"):
                        node.status = "running"
                        node.status_msg = ""
                    elif server.get("status") == "BUILD" and node.status not in ("creating", "deleting"):
                        node.status = "creating"
                        node.status_msg = ""
                    elif server.get("status") == "PAUSED" and node.status not in ("paused", "deleting"):
                        node.status = "paused"
                        node.status_msg = ""
                    elif server.get("status") == "SUSPENDED" and node.status not in ("suspended", "deleting"):
                        node.status = "suspended"
                        node.status_msg = ""
                    elif server.get("status") == "SHUTOFF" and node.status not in ("shutoff", "deleting"):
                        node.status = "shutoff"
                        node.status_msg = ""
                    elif (server.get("status") == "SHELVED_OFFLOADED" and node.status
                          not in ("shelved_offloaded", "deleting")):
                        node.status = "shelved_offloaded"
                        node.status_msg = ""
                    else:
                        continue
                    NodeSQL.update_node(node)
            except Exception as e:
                LOG.error(f"Error checking status for node {node.id}: {str(e)}")
                if "could not be found." in str(e):
                    NodeSQL.delete_node(node)

    except Exception as e:
        LOG.error(f"Error in node_status: {str(e)}")
