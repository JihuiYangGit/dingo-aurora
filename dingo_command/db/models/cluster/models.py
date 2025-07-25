# 数据表对应的model对象

from __future__ import annotations

from sqlalchemy import Column, String, Text, DateTime, Integer, Boolean
from sqlalchemy.orm import declarative_base

Base = declarative_base()

# 集群对象
class Cluster(Base):
    __tablename__ = "ops_cluster_info"

    id = Column(String(length=128), primary_key= True, nullable=False, index=True, unique=False)
    name = Column(String(length=128), primary_key= True, nullable=False, index=True, unique=False)
    project_id = Column(String(length=128), nullable=True)
    user_id = Column(String(length=128), nullable=True)
    labels = Column(String(length=128), nullable=True)
    status = Column(String(length=128), nullable=True)
    status_msg = Column(Text, nullable=True)
    region_name = Column(String(length=128), nullable=True)
    admin_network_id = Column(String(length=128), nullable=True)
    admin_subnet_id = Column(String(length=128), nullable=True)
    admin_network_name = Column(String(length=128), nullable=True)
    admin_network_cidr = Column(String(length=128), nullable=True)
    bus_network_id = Column(String(length=128), nullable=True)
    bus_subnet_id = Column(String(length=128), nullable=True)
    bus_network_name = Column(String(length=128), nullable=True)
    bus_network_cidr = Column(String(length=128), nullable=True)
    type = Column(String(length=128), nullable=True)
    kube_info = Column(Text, nullable=True)
    create_time = Column(DateTime, nullable=True)
    update_time = Column(DateTime, nullable=True)
    description = Column(String(length=255), nullable=True)
    cpu =  Column(Integer, nullable=True)
    mem =  Column(Integer, nullable=True)
    gpu =  Column(Integer, nullable=True)
    gpu_mem =  Column(Integer, nullable=True)
    extra = Column(Text, nullable=True)
    private_key = Column(Text, nullable=True)

class ClusterParams(Base):
    __tablename__ = "ops_cluster_params"

#     image = Column(String(length=128), primary_key= True, nullable=False, index=True, unique=False)
#     k8s_version = Column(String(length=128), primary_key= True, nullable=False, index=True, unique=False)
#     runtime = Column(String(length=128), nullable=True)
#     network_plugin = Column(String(length=128), nullable=True)
#     kube_proxy = Column(String(length=128), nullable=True)
#     service_cidr = Column(String(length=128), nullable=True)
#     lb_enable = Column(String(length=128), nullable=True)
    key = Column(String(length=128), primary_key= True, nullable=False, index=True, unique=False)
    value = Column(String(length=255), nullable=True)
# 节点对象
class Taskinfo(Base):
    __tablename__ = "ops_task_info"

    id = Column(Integer, primary_key= True, nullable=False, index=True, unique=False)
    cluster_id = Column(String(length=128), nullable=True)
    task_id = Column(String(length=128), nullable=True)
    state = Column(String(length=128), nullable=True)
    msg = Column(String(length=128), nullable=True)
    detail = Column(String(length=128), default=0, nullable= False)
    start_time = Column(DateTime, nullable=True)
    end_time = Column(DateTime, nullable=True)