# -*- coding: utf8 -*-
# Copyright (c) 2017-2021 THL A29 Limited, a Tencent company. All Rights Reserved.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#    http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

import warnings

from tdlc.tencentcloud.common.abstract_model import AbstractModel


class AVROFile(AbstractModel):
    """AVRO类型文件

    """

    def __init__(self):
        r"""
        :param Format: 文本类型，本参数取值为AVRO。
        :type Format: str
        :param CodeCompress: 压缩格式，["Snappy","Gzip","None"选一]
        :type CodeCompress: str
        """
        self.Format = None
        self.CodeCompress = None


    def _deserialize(self, params):
        self.Format = params.get("Format")
        self.CodeCompress = params.get("CodeCompress")
        memeber_set = set(params.keys())
        for name, value in vars(self).items():
            if name in memeber_set:
                memeber_set.remove(name)
        if len(memeber_set) > 0:
            warnings.warn("%s fileds are useless." % ",".join(memeber_set))
        


class AccessGroup(AbstractModel):
    """权限组

    """

    def __init__(self):
        r"""
        :param AccessGroupId: 权限组ID
        :type AccessGroupId: str
        :param AccessGroupName: 权限组名称
注意：此字段可能返回 null，表示取不到有效值。
        :type AccessGroupName: str
        :param Description: 权限组描述
注意：此字段可能返回 null，表示取不到有效值。
        :type Description: str
        :param VpcId: VPC网络ID
注意：此字段可能返回 null，表示取不到有效值。
        :type VpcId: str
        :param VpcType: VPC网络类型（1：CVM；2：黑石1.0）
注意：此字段可能返回 null，表示取不到有效值。
        :type VpcType: int
        :param CreateTime: 创建时间
注意：此字段可能返回 null，表示取不到有效值。
        :type CreateTime: str
        """
        self.AccessGroupId = None
        self.AccessGroupName = None
        self.Description = None
        self.VpcId = None
        self.VpcType = None
        self.CreateTime = None


    def _deserialize(self, params):
        self.AccessGroupId = params.get("AccessGroupId")
        self.AccessGroupName = params.get("AccessGroupName")
        self.Description = params.get("Description")
        self.VpcId = params.get("VpcId")
        self.VpcType = params.get("VpcType")
        self.CreateTime = params.get("CreateTime")
        memeber_set = set(params.keys())
        for name, value in vars(self).items():
            if name in memeber_set:
                memeber_set.remove(name)
        if len(memeber_set) > 0:
            warnings.warn("%s fileds are useless." % ",".join(memeber_set))
        


class AddColumnAfterRequest(AbstractModel):
    """AddColumnAfter请求参数结构体

    """

    def __init__(self):
        r"""
        :param DatabaseName: 数据库名称
        :type DatabaseName: str
        :param TableName: 表名
        :type TableName: str
        :param Column: 添加的字段
        :type Column: :class:`tencentcloud.dlc.v20210125.models.Column`
        :param AfterColumnName: 在某字段后插入新字段的某字段名
        :type AfterColumnName: str
        """
        self.DatabaseName = None
        self.TableName = None
        self.Column = None
        self.AfterColumnName = None


    def _deserialize(self, params):
        self.DatabaseName = params.get("DatabaseName")
        self.TableName = params.get("TableName")
        if params.get("Column") is not None:
            self.Column = Column()
            self.Column._deserialize(params.get("Column"))
        self.AfterColumnName = params.get("AfterColumnName")
        memeber_set = set(params.keys())
        for name, value in vars(self).items():
            if name in memeber_set:
                memeber_set.remove(name)
        if len(memeber_set) > 0:
            warnings.warn("%s fileds are useless." % ",".join(memeber_set))
        


class AddColumnAfterResponse(AbstractModel):
    """AddColumnAfter返回参数结构体

    """

    def __init__(self):
        r"""
        :param Execution: 执行语句
        :type Execution: :class:`tencentcloud.dlc.v20210125.models.Execution`
        :param TaskId: 任务id
        :type TaskId: str
        :param RequestId: 唯一请求 ID，每次请求都会返回。定位问题时需要提供该次请求的 RequestId。
        :type RequestId: str
        """
        self.Execution = None
        self.TaskId = None
        self.RequestId = None


    def _deserialize(self, params):
        if params.get("Execution") is not None:
            self.Execution = Execution()
            self.Execution._deserialize(params.get("Execution"))
        self.TaskId = params.get("TaskId")
        self.RequestId = params.get("RequestId")


class AddColumnsRequest(AbstractModel):
    """AddColumns请求参数结构体

    """

    def __init__(self):
        r"""
        :param DatabaseName: 数据库名称
        :type DatabaseName: str
        :param TableName: 数据表名称
        :type TableName: str
        :param Columns: 字段列表
        :type Columns: list of Column
        :param DatasourceConnectionName: 数据源名称
        :type DatasourceConnectionName: str
        """
        self.DatabaseName = None
        self.TableName = None
        self.Columns = None
        self.DatasourceConnectionName = None


    def _deserialize(self, params):
        self.DatabaseName = params.get("DatabaseName")
        self.TableName = params.get("TableName")
        if params.get("Columns") is not None:
            self.Columns = []
            for item in params.get("Columns"):
                obj = Column()
                obj._deserialize(item)
                self.Columns.append(obj)
        self.DatasourceConnectionName = params.get("DatasourceConnectionName")
        memeber_set = set(params.keys())
        for name, value in vars(self).items():
            if name in memeber_set:
                memeber_set.remove(name)
        if len(memeber_set) > 0:
            warnings.warn("%s fileds are useless." % ",".join(memeber_set))
        


class AddColumnsResponse(AbstractModel):
    """AddColumns返回参数结构体

    """

    def __init__(self):
        r"""
        :param Execution: 修改表执行语句
        :type Execution: :class:`tencentcloud.dlc.v20210125.models.Execution`
        :param TaskId: 任务Id
        :type TaskId: str
        :param RequestId: 唯一请求 ID，每次请求都会返回。定位问题时需要提供该次请求的 RequestId。
        :type RequestId: str
        """
        self.Execution = None
        self.TaskId = None
        self.RequestId = None


    def _deserialize(self, params):
        if params.get("Execution") is not None:
            self.Execution = Execution()
            self.Execution._deserialize(params.get("Execution"))
        self.TaskId = params.get("TaskId")
        self.RequestId = params.get("RequestId")


class AddDMSPartitionsRequest(AbstractModel):
    """AddDMSPartitions请求参数结构体

    """

    def __init__(self):
        r"""
        :param Partitions: 分区
        :type Partitions: list of DMSPartition
        """
        self.Partitions = None


    def _deserialize(self, params):
        if params.get("Partitions") is not None:
            self.Partitions = []
            for item in params.get("Partitions"):
                obj = DMSPartition()
                obj._deserialize(item)
                self.Partitions.append(obj)
        memeber_set = set(params.keys())
        for name, value in vars(self).items():
            if name in memeber_set:
                memeber_set.remove(name)
        if len(memeber_set) > 0:
            warnings.warn("%s fileds are useless." % ",".join(memeber_set))
        


class AddDMSPartitionsResponse(AbstractModel):
    """AddDMSPartitions返回参数结构体

    """

    def __init__(self):
        r"""
        :param Total: 成功数量
        :type Total: int
        :param Partitions: 分区值
        :type Partitions: list of DMSPartition
        :param RequestId: 唯一请求 ID，每次请求都会返回。定位问题时需要提供该次请求的 RequestId。
        :type RequestId: str
        """
        self.Total = None
        self.Partitions = None
        self.RequestId = None


    def _deserialize(self, params):
        self.Total = params.get("Total")
        if params.get("Partitions") is not None:
            self.Partitions = []
            for item in params.get("Partitions"):
                obj = DMSPartition()
                obj._deserialize(item)
                self.Partitions.append(obj)
        self.RequestId = params.get("RequestId")


class AddLakeFsChdfsBindingRequest(AbstractModel):
    """AddLakeFsChdfsBinding请求参数结构体

    """

    def __init__(self):
        r"""
        :param MountPoint: 挂载点ID
        :type MountPoint: str
        :param AccessGroups: 权限组列表
        :type AccessGroups: list of AccessGroup
        :param SupperUsers: 超级用户列表
        :type SupperUsers: list of str
        """
        self.MountPoint = None
        self.AccessGroups = None
        self.SupperUsers = None


    def _deserialize(self, params):
        self.MountPoint = params.get("MountPoint")
        if params.get("AccessGroups") is not None:
            self.AccessGroups = []
            for item in params.get("AccessGroups"):
                obj = AccessGroup()
                obj._deserialize(item)
                self.AccessGroups.append(obj)
        self.SupperUsers = params.get("SupperUsers")
        memeber_set = set(params.keys())
        for name, value in vars(self).items():
            if name in memeber_set:
                memeber_set.remove(name)
        if len(memeber_set) > 0:
            warnings.warn("%s fileds are useless." % ",".join(memeber_set))
        


class AddLakeFsChdfsBindingResponse(AbstractModel):
    """AddLakeFsChdfsBinding返回参数结构体

    """

    def __init__(self):
        r"""
        :param RequestId: 唯一请求 ID，每次请求都会返回。定位问题时需要提供该次请求的 RequestId。
        :type RequestId: str
        """
        self.RequestId = None


    def _deserialize(self, params):
        self.RequestId = params.get("RequestId")


class AddPartitionFieldRequest(AbstractModel):
    """AddPartitionField请求参数结构体

    """

    def __init__(self):
        r"""
        :param DatabaseName: 数据库名称
        :type DatabaseName: str
        :param TableName: 数据表名称
        :type TableName: str
        :param Partition: 分区信息
        :type Partition: :class:`tencentcloud.dlc.v20210125.models.Partition`
        :param DatasourceConnectionName: 数据源名称
        :type DatasourceConnectionName: str
        """
        self.DatabaseName = None
        self.TableName = None
        self.Partition = None
        self.DatasourceConnectionName = None


    def _deserialize(self, params):
        self.DatabaseName = params.get("DatabaseName")
        self.TableName = params.get("TableName")
        if params.get("Partition") is not None:
            self.Partition = Partition()
            self.Partition._deserialize(params.get("Partition"))
        self.DatasourceConnectionName = params.get("DatasourceConnectionName")
        memeber_set = set(params.keys())
        for name, value in vars(self).items():
            if name in memeber_set:
                memeber_set.remove(name)
        if len(memeber_set) > 0:
            warnings.warn("%s fileds are useless." % ",".join(memeber_set))
        


class AddPartitionFieldResponse(AbstractModel):
    """AddPartitionField返回参数结构体

    """

    def __init__(self):
        r"""
        :param Execution: 修改表执行语句
        :type Execution: :class:`tencentcloud.dlc.v20210125.models.Execution`
        :param TaskId: 任务Id
        :type TaskId: str
        :param RequestId: 唯一请求 ID，每次请求都会返回。定位问题时需要提供该次请求的 RequestId。
        :type RequestId: str
        """
        self.Execution = None
        self.TaskId = None
        self.RequestId = None


    def _deserialize(self, params):
        if params.get("Execution") is not None:
            self.Execution = Execution()
            self.Execution._deserialize(params.get("Execution"))
        self.TaskId = params.get("TaskId")
        self.RequestId = params.get("RequestId")


class AddSparkImageRequest(AbstractModel):
    """AddSparkImage请求参数结构体

    """

    def __init__(self):
        r"""
        :param ImageVersion: 镜像version
        :type ImageVersion: str
        :param ImageTag: 镜像tag
        :type ImageTag: str
        :param IsPublic: 是否为公共镜像：0：非公共；1：公共
        :type IsPublic: int
        :param Description: 镜像描述
        :type Description: str
        :param ImageVersionId: 镜像唯一id
        :type ImageVersionId: str
        :param Operator: 操作者
        :type Operator: str
        """
        self.ImageVersion = None
        self.ImageTag = None
        self.IsPublic = None
        self.Description = None
        self.ImageVersionId = None
        self.Operator = None


    def _deserialize(self, params):
        self.ImageVersion = params.get("ImageVersion")
        self.ImageTag = params.get("ImageTag")
        self.IsPublic = params.get("IsPublic")
        self.Description = params.get("Description")
        self.ImageVersionId = params.get("ImageVersionId")
        self.Operator = params.get("Operator")
        memeber_set = set(params.keys())
        for name, value in vars(self).items():
            if name in memeber_set:
                memeber_set.remove(name)
        if len(memeber_set) > 0:
            warnings.warn("%s fileds are useless." % ",".join(memeber_set))
        


class AddSparkImageResponse(AbstractModel):
    """AddSparkImage返回参数结构体

    """

    def __init__(self):
        r"""
        :param ImageId: 镜像编码
        :type ImageId: str
        :param RequestId: 唯一请求 ID，每次请求都会返回。定位问题时需要提供该次请求的 RequestId。
        :type RequestId: str
        """
        self.ImageId = None
        self.RequestId = None


    def _deserialize(self, params):
        self.ImageId = params.get("ImageId")
        self.RequestId = params.get("RequestId")


class AddSparkImageUserRecordsRequest(AbstractModel):
    """AddSparkImageUserRecords请求参数结构体

    """

    def __init__(self):
        r"""
        :param ImageId: 镜像编码
        :type ImageId: str
        :param UserAppId: 用户APPID
        :type UserAppId: int
        :param UserUin: 用户UIN
        :type UserUin: str
        :param ImageType: ImageType：1（父版本）、2（子版本）、3（pyspark镜像）；
        :type ImageType: int
        """
        self.ImageId = None
        self.UserAppId = None
        self.UserUin = None
        self.ImageType = None


    def _deserialize(self, params):
        self.ImageId = params.get("ImageId")
        self.UserAppId = params.get("UserAppId")
        self.UserUin = params.get("UserUin")
        self.ImageType = params.get("ImageType")
        memeber_set = set(params.keys())
        for name, value in vars(self).items():
            if name in memeber_set:
                memeber_set.remove(name)
        if len(memeber_set) > 0:
            warnings.warn("%s fileds are useless." % ",".join(memeber_set))
        


class AddSparkImageUserRecordsResponse(AbstractModel):
    """AddSparkImageUserRecords返回参数结构体

    """

    def __init__(self):
        r"""
        :param RecordId: 记录id
        :type RecordId: str
        :param RequestId: 唯一请求 ID，每次请求都会返回。定位问题时需要提供该次请求的 RequestId。
        :type RequestId: str
        """
        self.RecordId = None
        self.RequestId = None


    def _deserialize(self, params):
        self.RecordId = params.get("RecordId")
        self.RequestId = params.get("RequestId")


class AddTasksRequest(AbstractModel):
    """AddTasks请求参数结构体

    """

    def __init__(self):
        r"""
        :param WorkflowId: 调度计划ID
        :type WorkflowId: str
        :param Tasks: 任务列表
        :type Tasks: list of TaskDto
        """
        self.WorkflowId = None
        self.Tasks = None


    def _deserialize(self, params):
        self.WorkflowId = params.get("WorkflowId")
        if params.get("Tasks") is not None:
            self.Tasks = []
            for item in params.get("Tasks"):
                obj = TaskDto()
                obj._deserialize(item)
                self.Tasks.append(obj)
        memeber_set = set(params.keys())
        for name, value in vars(self).items():
            if name in memeber_set:
                memeber_set.remove(name)
        if len(memeber_set) > 0:
            warnings.warn("%s fileds are useless." % ",".join(memeber_set))
        


class AddTasksResponse(AbstractModel):
    """AddTasks返回参数结构体

    """

    def __init__(self):
        r"""
        :param RequestId: 唯一请求 ID，每次请求都会返回。定位问题时需要提供该次请求的 RequestId。
        :type RequestId: str
        """
        self.RequestId = None


    def _deserialize(self, params):
        self.RequestId = params.get("RequestId")


class AddUsersToWorkGroupRequest(AbstractModel):
    """AddUsersToWorkGroup请求参数结构体

    """

    def __init__(self):
        r"""
        :param AddInfo: 要操作的工作组和用户信息
        :type AddInfo: :class:`tencentcloud.dlc.v20210125.models.UserIdSetOfWorkGroupId`
        """
        self.AddInfo = None


    def _deserialize(self, params):
        if params.get("AddInfo") is not None:
            self.AddInfo = UserIdSetOfWorkGroupId()
            self.AddInfo._deserialize(params.get("AddInfo"))
        memeber_set = set(params.keys())
        for name, value in vars(self).items():
            if name in memeber_set:
                memeber_set.remove(name)
        if len(memeber_set) > 0:
            warnings.warn("%s fileds are useless." % ",".join(memeber_set))
        


class AddUsersToWorkGroupResponse(AbstractModel):
    """AddUsersToWorkGroup返回参数结构体

    """

    def __init__(self):
        r"""
        :param RequestId: 唯一请求 ID，每次请求都会返回。定位问题时需要提供该次请求的 RequestId。
        :type RequestId: str
        """
        self.RequestId = None


    def _deserialize(self, params):
        self.RequestId = params.get("RequestId")


class AddWhiteStrategyRequest(AbstractModel):
    """AddWhiteStrategy请求参数结构体

    """

    def __init__(self):
        r"""
        :param WhitelistInfo: 白名单策略
        :type WhitelistInfo: :class:`tencentcloud.dlc.v20210125.models.Whitelist`
        """
        self.WhitelistInfo = None


    def _deserialize(self, params):
        if params.get("WhitelistInfo") is not None:
            self.WhitelistInfo = Whitelist()
            self.WhitelistInfo._deserialize(params.get("WhitelistInfo"))
        memeber_set = set(params.keys())
        for name, value in vars(self).items():
            if name in memeber_set:
                memeber_set.remove(name)
        if len(memeber_set) > 0:
            warnings.warn("%s fileds are useless." % ",".join(memeber_set))
        


class AddWhiteStrategyResponse(AbstractModel):
    """AddWhiteStrategy返回参数结构体

    """

    def __init__(self):
        r"""
        :param RequestId: 唯一请求 ID，每次请求都会返回。定位问题时需要提供该次请求的 RequestId。
        :type RequestId: str
        """
        self.RequestId = None


    def _deserialize(self, params):
        self.RequestId = params.get("RequestId")


class AdvanceSetting(AbstractModel):
    """高级配置

    """

    def __init__(self):
        r"""
        :param FileLocation: 文件路径
注意：此字段可能返回 null，表示取不到有效值。
        :type FileLocation: str
        :param IsFullMode: true：全量模式（默认）、false：非全量模式
注意：此字段可能返回 null，表示取不到有效值。
        :type IsFullMode: str
        """
        self.FileLocation = None
        self.IsFullMode = None


    def _deserialize(self, params):
        self.FileLocation = params.get("FileLocation")
        self.IsFullMode = params.get("IsFullMode")
        memeber_set = set(params.keys())
        for name, value in vars(self).items():
            if name in memeber_set:
                memeber_set.remove(name)
        if len(memeber_set) > 0:
            warnings.warn("%s fileds are useless." % ",".join(memeber_set))
        


class AlterDMSDatabaseRequest(AbstractModel):
    """AlterDMSDatabase请求参数结构体

    """

    def __init__(self):
        r"""
        :param CurrentName: 当前名称
        :type CurrentName: str
        :param SchemaName: schema名称
        :type SchemaName: str
        :param Location: 路径
        :type Location: str
        :param Asset: 基础对象
        :type Asset: :class:`tencentcloud.dlc.v20210125.models.Asset`
        """
        self.CurrentName = None
        self.SchemaName = None
        self.Location = None
        self.Asset = None


    def _deserialize(self, params):
        self.CurrentName = params.get("CurrentName")
        self.SchemaName = params.get("SchemaName")
        self.Location = params.get("Location")
        if params.get("Asset") is not None:
            self.Asset = Asset()
            self.Asset._deserialize(params.get("Asset"))
        memeber_set = set(params.keys())
        for name, value in vars(self).items():
            if name in memeber_set:
                memeber_set.remove(name)
        if len(memeber_set) > 0:
            warnings.warn("%s fileds are useless." % ",".join(memeber_set))
        


class AlterDMSDatabaseResponse(AbstractModel):
    """AlterDMSDatabase返回参数结构体

    """

    def __init__(self):
        r"""
        :param RequestId: 唯一请求 ID，每次请求都会返回。定位问题时需要提供该次请求的 RequestId。
        :type RequestId: str
        """
        self.RequestId = None


    def _deserialize(self, params):
        self.RequestId = params.get("RequestId")


class AlterDMSPartitionColumnStatisticRequest(AbstractModel):
    """AlterDMSPartitionColumnStatistic请求参数结构体

    """

    def __init__(self):
        r"""
        :param DatabaseName: 数据库名
        :type DatabaseName: str
        :param TableName: 表名称
        :type TableName: str
        :param PartitionName: 分区名
        :type PartitionName: str
        :param ColumnStatisticList: Column统计信息
        :type ColumnStatisticList: list of DMSColumnStatistic
        :param PartitionId: 分区编码
        :type PartitionId: int
        """
        self.DatabaseName = None
        self.TableName = None
        self.PartitionName = None
        self.ColumnStatisticList = None
        self.PartitionId = None


    def _deserialize(self, params):
        self.DatabaseName = params.get("DatabaseName")
        self.TableName = params.get("TableName")
        self.PartitionName = params.get("PartitionName")
        if params.get("ColumnStatisticList") is not None:
            self.ColumnStatisticList = []
            for item in params.get("ColumnStatisticList"):
                obj = DMSColumnStatistic()
                obj._deserialize(item)
                self.ColumnStatisticList.append(obj)
        self.PartitionId = params.get("PartitionId")
        memeber_set = set(params.keys())
        for name, value in vars(self).items():
            if name in memeber_set:
                memeber_set.remove(name)
        if len(memeber_set) > 0:
            warnings.warn("%s fileds are useless." % ",".join(memeber_set))
        


class AlterDMSPartitionColumnStatisticResponse(AbstractModel):
    """AlterDMSPartitionColumnStatistic返回参数结构体

    """

    def __init__(self):
        r"""
        :param Status: 状态
        :type Status: bool
        :param RequestId: 唯一请求 ID，每次请求都会返回。定位问题时需要提供该次请求的 RequestId。
        :type RequestId: str
        """
        self.Status = None
        self.RequestId = None


    def _deserialize(self, params):
        self.Status = params.get("Status")
        self.RequestId = params.get("RequestId")


class AlterDMSPartitionRequest(AbstractModel):
    """AlterDMSPartition请求参数结构体

    """

    def __init__(self):
        r"""
        :param CurrentDbName: 当前名称，变更前db名称
        :type CurrentDbName: str
        :param CurrentTableName: 当前名称，变更前table名称
        :type CurrentTableName: str
        :param CurrentValues: 当前名称，变更前Part名称
        :type CurrentValues: str
        :param Partition: 分区
        :type Partition: :class:`tencentcloud.dlc.v20210125.models.DMSPartition`
        """
        self.CurrentDbName = None
        self.CurrentTableName = None
        self.CurrentValues = None
        self.Partition = None


    def _deserialize(self, params):
        self.CurrentDbName = params.get("CurrentDbName")
        self.CurrentTableName = params.get("CurrentTableName")
        self.CurrentValues = params.get("CurrentValues")
        if params.get("Partition") is not None:
            self.Partition = DMSPartition()
            self.Partition._deserialize(params.get("Partition"))
        memeber_set = set(params.keys())
        for name, value in vars(self).items():
            if name in memeber_set:
                memeber_set.remove(name)
        if len(memeber_set) > 0:
            warnings.warn("%s fileds are useless." % ",".join(memeber_set))
        


class AlterDMSPartitionResponse(AbstractModel):
    """AlterDMSPartition返回参数结构体

    """

    def __init__(self):
        r"""
        :param RequestId: 唯一请求 ID，每次请求都会返回。定位问题时需要提供该次请求的 RequestId。
        :type RequestId: str
        """
        self.RequestId = None


    def _deserialize(self, params):
        self.RequestId = params.get("RequestId")


class AlterDMSTableColumnStatisticRequest(AbstractModel):
    """AlterDMSTableColumnStatistic请求参数结构体

    """

    def __init__(self):
        r"""
        :param DatabaseName: 数据库名
        :type DatabaseName: str
        :param TableName: 表名称
        :type TableName: str
        :param ColumnStatistic: Column统计信息
        :type ColumnStatistic: list of DMSColumnStatistic
        """
        self.DatabaseName = None
        self.TableName = None
        self.ColumnStatistic = None


    def _deserialize(self, params):
        self.DatabaseName = params.get("DatabaseName")
        self.TableName = params.get("TableName")
        if params.get("ColumnStatistic") is not None:
            self.ColumnStatistic = []
            for item in params.get("ColumnStatistic"):
                obj = DMSColumnStatistic()
                obj._deserialize(item)
                self.ColumnStatistic.append(obj)
        memeber_set = set(params.keys())
        for name, value in vars(self).items():
            if name in memeber_set:
                memeber_set.remove(name)
        if len(memeber_set) > 0:
            warnings.warn("%s fileds are useless." % ",".join(memeber_set))
        


class AlterDMSTableColumnStatisticResponse(AbstractModel):
    """AlterDMSTableColumnStatistic返回参数结构体

    """

    def __init__(self):
        r"""
        :param Status: 状态
        :type Status: bool
        :param RequestId: 唯一请求 ID，每次请求都会返回。定位问题时需要提供该次请求的 RequestId。
        :type RequestId: str
        """
        self.Status = None
        self.RequestId = None


    def _deserialize(self, params):
        self.Status = params.get("Status")
        self.RequestId = params.get("RequestId")


class AlterDMSTableRequest(AbstractModel):
    """AlterDMSTable请求参数结构体

    """

    def __init__(self):
        r"""
        :param CurrentName: 当前名称
        :type CurrentName: str
        :param CurrentDbName: 当前数据库名称
        :type CurrentDbName: str
        :param Asset: 基础对象
        :type Asset: :class:`tencentcloud.dlc.v20210125.models.Asset`
        :param Type: 表类型
        :type Type: str
        :param DbName: 数据库名称
        :type DbName: str
        :param StorageSize: 存储大小
        :type StorageSize: int
        :param RecordCount: 记录数量
        :type RecordCount: int
        :param LifeTime: 生命周期
        :type LifeTime: int
        :param DataUpdateTime: 数据更新时间
        :type DataUpdateTime: str
        :param StructUpdateTime: 结构更新时间
        :type StructUpdateTime: str
        :param LastAccessTime: 最后访问时间
        :type LastAccessTime: str
        :param Sds: 存储对象
        :type Sds: :class:`tencentcloud.dlc.v20210125.models.DMSSds`
        :param Columns: 列
        :type Columns: list of DMSColumn
        :param PartitionKeys: 分区键值
        :type PartitionKeys: list of DMSColumn
        :param ViewOriginalText: 视图文本
        :type ViewOriginalText: str
        :param ViewExpandedText: 视图文本
        :type ViewExpandedText: str
        :param Partitions: 分区
        :type Partitions: list of DMSPartition
        :param Name: 当前表名
        :type Name: str
        """
        self.CurrentName = None
        self.CurrentDbName = None
        self.Asset = None
        self.Type = None
        self.DbName = None
        self.StorageSize = None
        self.RecordCount = None
        self.LifeTime = None
        self.DataUpdateTime = None
        self.StructUpdateTime = None
        self.LastAccessTime = None
        self.Sds = None
        self.Columns = None
        self.PartitionKeys = None
        self.ViewOriginalText = None
        self.ViewExpandedText = None
        self.Partitions = None
        self.Name = None


    def _deserialize(self, params):
        self.CurrentName = params.get("CurrentName")
        self.CurrentDbName = params.get("CurrentDbName")
        if params.get("Asset") is not None:
            self.Asset = Asset()
            self.Asset._deserialize(params.get("Asset"))
        self.Type = params.get("Type")
        self.DbName = params.get("DbName")
        self.StorageSize = params.get("StorageSize")
        self.RecordCount = params.get("RecordCount")
        self.LifeTime = params.get("LifeTime")
        self.DataUpdateTime = params.get("DataUpdateTime")
        self.StructUpdateTime = params.get("StructUpdateTime")
        self.LastAccessTime = params.get("LastAccessTime")
        if params.get("Sds") is not None:
            self.Sds = DMSSds()
            self.Sds._deserialize(params.get("Sds"))
        if params.get("Columns") is not None:
            self.Columns = []
            for item in params.get("Columns"):
                obj = DMSColumn()
                obj._deserialize(item)
                self.Columns.append(obj)
        if params.get("PartitionKeys") is not None:
            self.PartitionKeys = []
            for item in params.get("PartitionKeys"):
                obj = DMSColumn()
                obj._deserialize(item)
                self.PartitionKeys.append(obj)
        self.ViewOriginalText = params.get("ViewOriginalText")
        self.ViewExpandedText = params.get("ViewExpandedText")
        if params.get("Partitions") is not None:
            self.Partitions = []
            for item in params.get("Partitions"):
                obj = DMSPartition()
                obj._deserialize(item)
                self.Partitions.append(obj)
        self.Name = params.get("Name")
        memeber_set = set(params.keys())
        for name, value in vars(self).items():
            if name in memeber_set:
                memeber_set.remove(name)
        if len(memeber_set) > 0:
            warnings.warn("%s fileds are useless." % ",".join(memeber_set))
        


class AlterDMSTableResponse(AbstractModel):
    """AlterDMSTable返回参数结构体

    """

    def __init__(self):
        r"""
        :param RequestId: 唯一请求 ID，每次请求都会返回。定位问题时需要提供该次请求的 RequestId。
        :type RequestId: str
        """
        self.RequestId = None


    def _deserialize(self, params):
        self.RequestId = params.get("RequestId")


class AlterMetaKeyConstraintRequest(AbstractModel):
    """AlterMetaKeyConstraint请求参数结构体

    """

    def __init__(self):
        r"""
        :param MetaKeyConstraint: 元数据约束
        :type MetaKeyConstraint: :class:`tencentcloud.dlc.v20210125.models.MetaKeyConstraint`
        """
        self.MetaKeyConstraint = None


    def _deserialize(self, params):
        if params.get("MetaKeyConstraint") is not None:
            self.MetaKeyConstraint = MetaKeyConstraint()
            self.MetaKeyConstraint._deserialize(params.get("MetaKeyConstraint"))
        memeber_set = set(params.keys())
        for name, value in vars(self).items():
            if name in memeber_set:
                memeber_set.remove(name)
        if len(memeber_set) > 0:
            warnings.warn("%s fileds are useless." % ",".join(memeber_set))
        


class AlterMetaKeyConstraintResponse(AbstractModel):
    """AlterMetaKeyConstraint返回参数结构体

    """

    def __init__(self):
        r"""
        :param Success: 状态
        :type Success: bool
        :param RequestId: 唯一请求 ID，每次请求都会返回。定位问题时需要提供该次请求的 RequestId。
        :type RequestId: str
        """
        self.Success = None
        self.RequestId = None


    def _deserialize(self, params):
        self.Success = params.get("Success")
        self.RequestId = params.get("RequestId")


class AlterTableColumnsRequest(AbstractModel):
    """AlterTableColumns请求参数结构体

    """

    def __init__(self):
        r"""
        :param TableInfo: 表字段修改信息
        :type TableInfo: :class:`tencentcloud.dlc.v20210125.models.TableInfo`
        """
        self.TableInfo = None


    def _deserialize(self, params):
        if params.get("TableInfo") is not None:
            self.TableInfo = TableInfo()
            self.TableInfo._deserialize(params.get("TableInfo"))
        memeber_set = set(params.keys())
        for name, value in vars(self).items():
            if name in memeber_set:
                memeber_set.remove(name)
        if len(memeber_set) > 0:
            warnings.warn("%s fileds are useless." % ",".join(memeber_set))
        


class AlterTableColumnsResponse(AbstractModel):
    """AlterTableColumns返回参数结构体

    """

    def __init__(self):
        r"""
        :param Execution: 修改表执行语句
        :type Execution: :class:`tencentcloud.dlc.v20210125.models.Execution`
        :param TaskId: 任务id
        :type TaskId: str
        :param RequestId: 唯一请求 ID，每次请求都会返回。定位问题时需要提供该次请求的 RequestId。
        :type RequestId: str
        """
        self.Execution = None
        self.TaskId = None
        self.RequestId = None


    def _deserialize(self, params):
        if params.get("Execution") is not None:
            self.Execution = Execution()
            self.Execution._deserialize(params.get("Execution"))
        self.TaskId = params.get("TaskId")
        self.RequestId = params.get("RequestId")


class AlterTableCommentRequest(AbstractModel):
    """AlterTableComment请求参数结构体

    """

    def __init__(self):
        r"""
        :param TableBaseInfo: 修改表的基本信息
        :type TableBaseInfo: :class:`tencentcloud.dlc.v20210125.models.TableBaseInfo`
        """
        self.TableBaseInfo = None


    def _deserialize(self, params):
        if params.get("TableBaseInfo") is not None:
            self.TableBaseInfo = TableBaseInfo()
            self.TableBaseInfo._deserialize(params.get("TableBaseInfo"))
        memeber_set = set(params.keys())
        for name, value in vars(self).items():
            if name in memeber_set:
                memeber_set.remove(name)
        if len(memeber_set) > 0:
            warnings.warn("%s fileds are useless." % ",".join(memeber_set))
        


class AlterTableCommentResponse(AbstractModel):
    """AlterTableComment返回参数结构体

    """

    def __init__(self):
        r"""
        :param RequestId: 唯一请求 ID，每次请求都会返回。定位问题时需要提供该次请求的 RequestId。
        :type RequestId: str
        """
        self.RequestId = None


    def _deserialize(self, params):
        self.RequestId = params.get("RequestId")


class AlterTablePropertiesRequest(AbstractModel):
    """AlterTableProperties请求参数结构体

    """

    def __init__(self):
        r"""
        :param DatabaseName: 数据库名称
        :type DatabaseName: str
        :param TableName: 表名称
        :type TableName: str
        :param Properties: 属性配置
        :type Properties: list of KVPair
        :param DatasourceConnectionName: 数据源名称
        :type DatasourceConnectionName: str
        :param StorageSize: 表存储大小
        :type StorageSize: int
        :param RecordCount: 表记录数
        :type RecordCount: int
        """
        self.DatabaseName = None
        self.TableName = None
        self.Properties = None
        self.DatasourceConnectionName = None
        self.StorageSize = None
        self.RecordCount = None


    def _deserialize(self, params):
        self.DatabaseName = params.get("DatabaseName")
        self.TableName = params.get("TableName")
        if params.get("Properties") is not None:
            self.Properties = []
            for item in params.get("Properties"):
                obj = KVPair()
                obj._deserialize(item)
                self.Properties.append(obj)
        self.DatasourceConnectionName = params.get("DatasourceConnectionName")
        self.StorageSize = params.get("StorageSize")
        self.RecordCount = params.get("RecordCount")
        memeber_set = set(params.keys())
        for name, value in vars(self).items():
            if name in memeber_set:
                memeber_set.remove(name)
        if len(memeber_set) > 0:
            warnings.warn("%s fileds are useless." % ",".join(memeber_set))
        


class AlterTablePropertiesResponse(AbstractModel):
    """AlterTableProperties返回参数结构体

    """

    def __init__(self):
        r"""
        :param Result: 修改返回信息
        :type Result: str
        :param RequestId: 唯一请求 ID，每次请求都会返回。定位问题时需要提供该次请求的 RequestId。
        :type RequestId: str
        """
        self.Result = None
        self.RequestId = None


    def _deserialize(self, params):
        self.Result = params.get("Result")
        self.RequestId = params.get("RequestId")


class Asset(AbstractModel):
    """元数据基本对象

    """

    def __init__(self):
        r"""
        :param Id: 主键
注意：此字段可能返回 null，表示取不到有效值。
        :type Id: int
        :param Name: 名称
注意：此字段可能返回 null，表示取不到有效值。
        :type Name: str
        :param Guid: 对象GUID值
注意：此字段可能返回 null，表示取不到有效值。
        :type Guid: str
        :param Catalog: 数据目录
注意：此字段可能返回 null，表示取不到有效值。
        :type Catalog: str
        :param Description: 描述信息
        :type Description: str
        :param Owner: 对象owner
        :type Owner: str
        :param OwnerAccount: 对象owner账户
        :type OwnerAccount: str
        :param PermValues: 权限
        :type PermValues: list of KVPair
        :param Params: 附加属性
        :type Params: list of KVPair
        :param BizParams: 附加业务属性
        :type BizParams: list of KVPair
        :param DataVersion: 数据版本
        :type DataVersion: int
        :param CreateTime: 创建时间
        :type CreateTime: str
        :param ModifiedTime: 修改时间
        :type ModifiedTime: str
        :param DatasourceId: 数据源主键
        :type DatasourceId: int
        """
        self.Id = None
        self.Name = None
        self.Guid = None
        self.Catalog = None
        self.Description = None
        self.Owner = None
        self.OwnerAccount = None
        self.PermValues = None
        self.Params = None
        self.BizParams = None
        self.DataVersion = None
        self.CreateTime = None
        self.ModifiedTime = None
        self.DatasourceId = None


    def _deserialize(self, params):
        self.Id = params.get("Id")
        self.Name = params.get("Name")
        self.Guid = params.get("Guid")
        self.Catalog = params.get("Catalog")
        self.Description = params.get("Description")
        self.Owner = params.get("Owner")
        self.OwnerAccount = params.get("OwnerAccount")
        if params.get("PermValues") is not None:
            self.PermValues = []
            for item in params.get("PermValues"):
                obj = KVPair()
                obj._deserialize(item)
                self.PermValues.append(obj)
        if params.get("Params") is not None:
            self.Params = []
            for item in params.get("Params"):
                obj = KVPair()
                obj._deserialize(item)
                self.Params.append(obj)
        if params.get("BizParams") is not None:
            self.BizParams = []
            for item in params.get("BizParams"):
                obj = KVPair()
                obj._deserialize(item)
                self.BizParams.append(obj)
        self.DataVersion = params.get("DataVersion")
        self.CreateTime = params.get("CreateTime")
        self.ModifiedTime = params.get("ModifiedTime")
        self.DatasourceId = params.get("DatasourceId")
        memeber_set = set(params.keys())
        for name, value in vars(self).items():
            if name in memeber_set:
                memeber_set.remove(name)
        if len(memeber_set) > 0:
            warnings.warn("%s fileds are useless." % ",".join(memeber_set))
        


class AssociateCHDFSAccessGroupsRequest(AbstractModel):
    """AssociateCHDFSAccessGroups请求参数结构体

    """

    def __init__(self):
        r"""
        :param DataEngineName: 引擎名称
        :type DataEngineName: str
        :param MountPointIds: 挂载点列表
        :type MountPointIds: list of str
        """
        self.DataEngineName = None
        self.MountPointIds = None


    def _deserialize(self, params):
        self.DataEngineName = params.get("DataEngineName")
        self.MountPointIds = params.get("MountPointIds")
        memeber_set = set(params.keys())
        for name, value in vars(self).items():
            if name in memeber_set:
                memeber_set.remove(name)
        if len(memeber_set) > 0:
            warnings.warn("%s fileds are useless." % ",".join(memeber_set))
        


class AssociateCHDFSAccessGroupsResponse(AbstractModel):
    """AssociateCHDFSAccessGroups返回参数结构体

    """

    def __init__(self):
        r"""
        :param RequestId: 唯一请求 ID，每次请求都会返回。定位问题时需要提供该次请求的 RequestId。
        :type RequestId: str
        """
        self.RequestId = None


    def _deserialize(self, params):
        self.RequestId = params.get("RequestId")


class AssociateDatasourceHouseRequest(AbstractModel):
    """AssociateDatasourceHouse请求参数结构体

    """

    def __init__(self):
        r"""
        :param DatasourceConnectionName: 网络配置名称
        :type DatasourceConnectionName: str
        :param DatasourceConnectionType: 数据源类型
        :type DatasourceConnectionType: str
        :param DatasourceConnectionConfig: 数据源网络配置
        :type DatasourceConnectionConfig: :class:`tencentcloud.dlc.v20210125.models.DatasourceConnectionConfig`
        :param DataEngineNames: 引擎名称，只允许绑定一个引擎
        :type DataEngineNames: list of str
        :param NetworkConnectionType: 网络类型，2-跨源型，4-增强型
        :type NetworkConnectionType: int
        :param NetworkConnectionDesc: 网络配置描述
        :type NetworkConnectionDesc: str
        """
        self.DatasourceConnectionName = None
        self.DatasourceConnectionType = None
        self.DatasourceConnectionConfig = None
        self.DataEngineNames = None
        self.NetworkConnectionType = None
        self.NetworkConnectionDesc = None


    def _deserialize(self, params):
        self.DatasourceConnectionName = params.get("DatasourceConnectionName")
        self.DatasourceConnectionType = params.get("DatasourceConnectionType")
        if params.get("DatasourceConnectionConfig") is not None:
            self.DatasourceConnectionConfig = DatasourceConnectionConfig()
            self.DatasourceConnectionConfig._deserialize(params.get("DatasourceConnectionConfig"))
        self.DataEngineNames = params.get("DataEngineNames")
        self.NetworkConnectionType = params.get("NetworkConnectionType")
        self.NetworkConnectionDesc = params.get("NetworkConnectionDesc")
        memeber_set = set(params.keys())
        for name, value in vars(self).items():
            if name in memeber_set:
                memeber_set.remove(name)
        if len(memeber_set) > 0:
            warnings.warn("%s fileds are useless." % ",".join(memeber_set))
        


class AssociateDatasourceHouseResponse(AbstractModel):
    """AssociateDatasourceHouse返回参数结构体

    """

    def __init__(self):
        r"""
        :param RequestId: 唯一请求 ID，每次请求都会返回。定位问题时需要提供该次请求的 RequestId。
        :type RequestId: str
        """
        self.RequestId = None


    def _deserialize(self, params):
        self.RequestId = params.get("RequestId")


class AttachUserPolicyRequest(AbstractModel):
    """AttachUserPolicy请求参数结构体

    """

    def __init__(self):
        r"""
        :param UserId: 用户Id，和子用户uin相同，需要先使用CreateUser接口创建用户。可以使用DescribeUsers接口查看。
        :type UserId: str
        :param PolicySet: 鉴权策略集合
        :type PolicySet: list of Policy
        """
        self.UserId = None
        self.PolicySet = None


    def _deserialize(self, params):
        self.UserId = params.get("UserId")
        if params.get("PolicySet") is not None:
            self.PolicySet = []
            for item in params.get("PolicySet"):
                obj = Policy()
                obj._deserialize(item)
                self.PolicySet.append(obj)
        memeber_set = set(params.keys())
        for name, value in vars(self).items():
            if name in memeber_set:
                memeber_set.remove(name)
        if len(memeber_set) > 0:
            warnings.warn("%s fileds are useless." % ",".join(memeber_set))
        


class AttachUserPolicyResponse(AbstractModel):
    """AttachUserPolicy返回参数结构体

    """

    def __init__(self):
        r"""
        :param RequestId: 唯一请求 ID，每次请求都会返回。定位问题时需要提供该次请求的 RequestId。
        :type RequestId: str
        """
        self.RequestId = None


    def _deserialize(self, params):
        self.RequestId = params.get("RequestId")


class AttachWorkGroupPolicyRequest(AbstractModel):
    """AttachWorkGroupPolicy请求参数结构体

    """

    def __init__(self):
        r"""
        :param WorkGroupId: 工作组Id
        :type WorkGroupId: int
        :param PolicySet: 要绑定的策略集合
        :type PolicySet: list of Policy
        """
        self.WorkGroupId = None
        self.PolicySet = None


    def _deserialize(self, params):
        self.WorkGroupId = params.get("WorkGroupId")
        if params.get("PolicySet") is not None:
            self.PolicySet = []
            for item in params.get("PolicySet"):
                obj = Policy()
                obj._deserialize(item)
                self.PolicySet.append(obj)
        memeber_set = set(params.keys())
        for name, value in vars(self).items():
            if name in memeber_set:
                memeber_set.remove(name)
        if len(memeber_set) > 0:
            warnings.warn("%s fileds are useless." % ",".join(memeber_set))
        


class AttachWorkGroupPolicyResponse(AbstractModel):
    """AttachWorkGroupPolicy返回参数结构体

    """

    def __init__(self):
        r"""
        :param RequestId: 唯一请求 ID，每次请求都会返回。定位问题时需要提供该次请求的 RequestId。
        :type RequestId: str
        """
        self.RequestId = None


    def _deserialize(self, params):
        self.RequestId = params.get("RequestId")


class AuditDataEngineEvent(AbstractModel):
    """引擎审计事件

    """

    def __init__(self):
        r"""
        :param UserId: uin
注意：此字段可能返回 null，表示取不到有效值。
        :type UserId: str
        :param EventName: DataEngine-xxx
注意：此字段可能返回 null，表示取不到有效值。
        :type EventName: str
        :param DataEngineName: testname
注意：此字段可能返回 null，表示取不到有效值。
        :type DataEngineName: str
        :param State: 1
注意：此字段可能返回 null，表示取不到有效值。
        :type State: int
        :param Size: 16
注意：此字段可能返回 null，表示取不到有效值。
        :type Size: int
        :param EngineType: presto
注意：此字段可能返回 null，表示取不到有效值。
        :type EngineType: str
        """
        self.UserId = None
        self.EventName = None
        self.DataEngineName = None
        self.State = None
        self.Size = None
        self.EngineType = None


    def _deserialize(self, params):
        self.UserId = params.get("UserId")
        self.EventName = params.get("EventName")
        self.DataEngineName = params.get("DataEngineName")
        self.State = params.get("State")
        self.Size = params.get("Size")
        self.EngineType = params.get("EngineType")
        memeber_set = set(params.keys())
        for name, value in vars(self).items():
            if name in memeber_set:
                memeber_set.remove(name)
        if len(memeber_set) > 0:
            warnings.warn("%s fileds are useless." % ",".join(memeber_set))
        


class AuditEvent(AbstractModel):
    """审计事件信息

    """

    def __init__(self):
        r"""
        :param EventId: 事件ID
注意：此字段可能返回 null，表示取不到有效值。
        :type EventId: str
        :param EventTime: 事件时间
注意：此字段可能返回 null，表示取不到有效值。
        :type EventTime: str
        :param Username: 用户名uin
注意：此字段可能返回 null，表示取不到有效值。
        :type Username: str
        :param SourceIPAddress: 源IP
注意：此字段可能返回 null，表示取不到有效值。
        :type SourceIPAddress: str
        :param EventType: 事件类型
注意：此字段可能返回 null，表示取不到有效值。
        :type EventType: str
        :param EventName: 事件名称
注意：此字段可能返回 null，表示取不到有效值。
        :type EventName: str
        :param EventRequestID: 请求ID
注意：此字段可能返回 null，表示取不到有效值。
        :type EventRequestID: str
        :param ErrorMessage: 错误信息
注意：此字段可能返回 null，表示取不到有效值。
        :type ErrorMessage: str
        :param DataEngineEvent: 引擎事件
注意：此字段可能返回 null，表示取不到有效值。
        :type DataEngineEvent: list of AuditDataEngineEvent
        :param TaskEvent: 任务事件
注意：此字段可能返回 null，表示取不到有效值。
        :type TaskEvent: list of AuditTaskEvent
        :param ScheduleEvent: 调度计划事件
注意：此字段可能返回 null，表示取不到有效值。
        :type ScheduleEvent: :class:`tencentcloud.dlc.v20210125.models.AuditScheduleEvent`
        :param EventRegion: 事件请求地域
注意：此字段可能返回 null，表示取不到有效值。
        :type EventRegion: str
        """
        self.EventId = None
        self.EventTime = None
        self.Username = None
        self.SourceIPAddress = None
        self.EventType = None
        self.EventName = None
        self.EventRequestID = None
        self.ErrorMessage = None
        self.DataEngineEvent = None
        self.TaskEvent = None
        self.ScheduleEvent = None
        self.EventRegion = None


    def _deserialize(self, params):
        self.EventId = params.get("EventId")
        self.EventTime = params.get("EventTime")
        self.Username = params.get("Username")
        self.SourceIPAddress = params.get("SourceIPAddress")
        self.EventType = params.get("EventType")
        self.EventName = params.get("EventName")
        self.EventRequestID = params.get("EventRequestID")
        self.ErrorMessage = params.get("ErrorMessage")
        if params.get("DataEngineEvent") is not None:
            self.DataEngineEvent = []
            for item in params.get("DataEngineEvent"):
                obj = AuditDataEngineEvent()
                obj._deserialize(item)
                self.DataEngineEvent.append(obj)
        if params.get("TaskEvent") is not None:
            self.TaskEvent = []
            for item in params.get("TaskEvent"):
                obj = AuditTaskEvent()
                obj._deserialize(item)
                self.TaskEvent.append(obj)
        if params.get("ScheduleEvent") is not None:
            self.ScheduleEvent = AuditScheduleEvent()
            self.ScheduleEvent._deserialize(params.get("ScheduleEvent"))
        self.EventRegion = params.get("EventRegion")
        memeber_set = set(params.keys())
        for name, value in vars(self).items():
            if name in memeber_set:
                memeber_set.remove(name)
        if len(memeber_set) > 0:
            warnings.warn("%s fileds are useless." % ",".join(memeber_set))
        


class AuditScheduleEvent(AbstractModel):
    """调度计划审计事件

    """

    def __init__(self):
        r"""
        :param UserId: 用户uin
注意：此字段可能返回 null，表示取不到有效值。
        :type UserId: str
        :param EventName: 事件名称
注意：此字段可能返回 null，表示取不到有效值。
        :type EventName: str
        :param WorkflowId: 调度计划ID
注意：此字段可能返回 null，表示取不到有效值。
        :type WorkflowId: str
        :param WorkflowName: 调度计划名字
注意：此字段可能返回 null，表示取不到有效值。
        :type WorkflowName: str
        """
        self.UserId = None
        self.EventName = None
        self.WorkflowId = None
        self.WorkflowName = None


    def _deserialize(self, params):
        self.UserId = params.get("UserId")
        self.EventName = params.get("EventName")
        self.WorkflowId = params.get("WorkflowId")
        self.WorkflowName = params.get("WorkflowName")
        memeber_set = set(params.keys())
        for name, value in vars(self).items():
            if name in memeber_set:
                memeber_set.remove(name)
        if len(memeber_set) > 0:
            warnings.warn("%s fileds are useless." % ",".join(memeber_set))
        


class AuditTaskEvent(AbstractModel):
    """任务审计事件

    """

    def __init__(self):
        r"""
        :param UserId: uin
注意：此字段可能返回 null，表示取不到有效值。
        :type UserId: str
        :param EventName: createtask
注意：此字段可能返回 null，表示取不到有效值。
        :type EventName: str
        :param TaskId: 任务id
注意：此字段可能返回 null，表示取不到有效值。
        :type TaskId: str
        :param SQLType: sql类型
注意：此字段可能返回 null，表示取不到有效值。
        :type SQLType: str
        :param UsedTime: 耗时
注意：此字段可能返回 null，表示取不到有效值。
        :type UsedTime: int
        :param CreateTime: 创建时间
注意：此字段可能返回 null，表示取不到有效值。
        :type CreateTime: str
        :param State: 1
注意：此字段可能返回 null，表示取不到有效值。
        :type State: int
        :param DataEngineName: 引擎任务
注意：此字段可能返回 null，表示取不到有效值。
        :type DataEngineName: str
        :param SQL: sql内容
注意：此字段可能返回 null，表示取不到有效值。
        :type SQL: str
        :param DataSet: 任务结果
注意：此字段可能返回 null，表示取不到有效值。
        :type DataSet: str
        :param SparkJobName: spark作业名字
注意：此字段可能返回 null，表示取不到有效值。
        :type SparkJobName: str
        :param TaskKind: 任务类别
注意：此字段可能返回 null，表示取不到有效值。
        :type TaskKind: str
        :param SparkJobId: SparkJob id
注意：此字段可能返回 null，表示取不到有效值。
        :type SparkJobId: str
        :param SparkJobFile: SparkJob的文件名
注意：此字段可能返回 null，表示取不到有效值。
        :type SparkJobFile: str
        """
        self.UserId = None
        self.EventName = None
        self.TaskId = None
        self.SQLType = None
        self.UsedTime = None
        self.CreateTime = None
        self.State = None
        self.DataEngineName = None
        self.SQL = None
        self.DataSet = None
        self.SparkJobName = None
        self.TaskKind = None
        self.SparkJobId = None
        self.SparkJobFile = None


    def _deserialize(self, params):
        self.UserId = params.get("UserId")
        self.EventName = params.get("EventName")
        self.TaskId = params.get("TaskId")
        self.SQLType = params.get("SQLType")
        self.UsedTime = params.get("UsedTime")
        self.CreateTime = params.get("CreateTime")
        self.State = params.get("State")
        self.DataEngineName = params.get("DataEngineName")
        self.SQL = params.get("SQL")
        self.DataSet = params.get("DataSet")
        self.SparkJobName = params.get("SparkJobName")
        self.TaskKind = params.get("TaskKind")
        self.SparkJobId = params.get("SparkJobId")
        self.SparkJobFile = params.get("SparkJobFile")
        memeber_set = set(params.keys())
        for name, value in vars(self).items():
            if name in memeber_set:
                memeber_set.remove(name)
        if len(memeber_set) > 0:
            warnings.warn("%s fileds are useless." % ",".join(memeber_set))
        


class BindDefaultSharedEngineRequest(AbstractModel):
    """BindDefaultSharedEngine请求参数结构体

    """


class BindDefaultSharedEngineResponse(AbstractModel):
    """BindDefaultSharedEngine返回参数结构体

    """

    def __init__(self):
        r"""
        :param RequestId: 唯一请求 ID，每次请求都会返回。定位问题时需要提供该次请求的 RequestId。
        :type RequestId: str
        """
        self.RequestId = None


    def _deserialize(self, params):
        self.RequestId = params.get("RequestId")


class BindTagsToDataEnginesRequest(AbstractModel):
    """BindTagsToDataEngines请求参数结构体

    """

    def __init__(self):
        r"""
        :param DataEngineIds: 需要绑定标签的数据引擎ID列表
        :type DataEngineIds: list of str
        :param Tags: 需要绑定的标签列表
        :type Tags: list of TagInfo
        :param DryRun: 是否空跑，true：空跑，只对权限等进行判断，成功后也不会真正绑定标签
        :type DryRun: bool
        """
        self.DataEngineIds = None
        self.Tags = None
        self.DryRun = None


    def _deserialize(self, params):
        self.DataEngineIds = params.get("DataEngineIds")
        if params.get("Tags") is not None:
            self.Tags = []
            for item in params.get("Tags"):
                obj = TagInfo()
                obj._deserialize(item)
                self.Tags.append(obj)
        self.DryRun = params.get("DryRun")
        memeber_set = set(params.keys())
        for name, value in vars(self).items():
            if name in memeber_set:
                memeber_set.remove(name)
        if len(memeber_set) > 0:
            warnings.warn("%s fileds are useless." % ",".join(memeber_set))
        


class BindTagsToDataEnginesResponse(AbstractModel):
    """BindTagsToDataEngines返回参数结构体

    """

    def __init__(self):
        r"""
        :param RequestId: 唯一请求 ID，每次请求都会返回。定位问题时需要提供该次请求的 RequestId。
        :type RequestId: str
        """
        self.RequestId = None


    def _deserialize(self, params):
        self.RequestId = params.get("RequestId")


class BindWorkGroupsToUserRequest(AbstractModel):
    """BindWorkGroupsToUser请求参数结构体

    """

    def __init__(self):
        r"""
        :param AddInfo: 绑定的用户和工作组信息
        :type AddInfo: :class:`tencentcloud.dlc.v20210125.models.WorkGroupIdSetOfUserId`
        """
        self.AddInfo = None


    def _deserialize(self, params):
        if params.get("AddInfo") is not None:
            self.AddInfo = WorkGroupIdSetOfUserId()
            self.AddInfo._deserialize(params.get("AddInfo"))
        memeber_set = set(params.keys())
        for name, value in vars(self).items():
            if name in memeber_set:
                memeber_set.remove(name)
        if len(memeber_set) > 0:
            warnings.warn("%s fileds are useless." % ",".join(memeber_set))
        


class BindWorkGroupsToUserResponse(AbstractModel):
    """BindWorkGroupsToUser返回参数结构体

    """

    def __init__(self):
        r"""
        :param RequestId: 唯一请求 ID，每次请求都会返回。定位问题时需要提供该次请求的 RequestId。
        :type RequestId: str
        """
        self.RequestId = None


    def _deserialize(self, params):
        self.RequestId = params.get("RequestId")


class CHDFSAccessInfo(AbstractModel):
    """元数据加速桶访问权限配置列表

    """

    def __init__(self):
        r"""
        :param BucketId: 桶名
注意：此字段可能返回 null，表示取不到有效值。
        :type BucketId: str
        :param BucketType: 桶类型
注意：此字段可能返回 null，表示取不到有效值。
        :type BucketType: str
        :param BindProNum: 已绑定的产品数量（该字段已废弃）
注意：此字段可能返回 null，表示取不到有效值。
        :type BindProNum: int
        :param ProNum: 产品总数（该字段已废弃）
注意：此字段可能返回 null，表示取不到有效值。
        :type ProNum: int
        :param BindProNameList: 已绑定产品名称列表（该字段已废弃）
注意：此字段可能返回 null，表示取不到有效值。
        :type BindProNameList: list of str
        :param BindEngineNum: 已绑定的引擎数量
注意：此字段可能返回 null，表示取不到有效值。
        :type BindEngineNum: int
        :param EngineNum: 引擎数量

注意：此字段可能返回 null，表示取不到有效值。
        :type EngineNum: int
        """
        self.BucketId = None
        self.BucketType = None
        self.BindProNum = None
        self.ProNum = None
        self.BindProNameList = None
        self.BindEngineNum = None
        self.EngineNum = None


    def _deserialize(self, params):
        self.BucketId = params.get("BucketId")
        self.BucketType = params.get("BucketType")
        self.BindProNum = params.get("BindProNum")
        self.ProNum = params.get("ProNum")
        self.BindProNameList = params.get("BindProNameList")
        self.BindEngineNum = params.get("BindEngineNum")
        self.EngineNum = params.get("EngineNum")
        memeber_set = set(params.keys())
        for name, value in vars(self).items():
            if name in memeber_set:
                memeber_set.remove(name)
        if len(memeber_set) > 0:
            warnings.warn("%s fileds are useless." % ",".join(memeber_set))
        


class CHDFSProductInfo(AbstractModel):
    """chdfs产品信息

    """

    def __init__(self):
        r"""
        :param ProductName: 产品名称
注意：此字段可能返回 null，表示取不到有效值。
        :type ProductName: str
        :param SuperUser: 用户名称
注意：此字段可能返回 null，表示取不到有效值。
        :type SuperUser: list of str
        :param VpcInfo: vpc配置信息

注意：此字段可能返回 null，表示取不到有效值。
        :type VpcInfo: list of CHDFSProductVpcInfo
        :param CanBeDeleted: 能够被删除
注意：此字段可能返回 null，表示取不到有效值。
        :type CanBeDeleted: bool
        """
        self.ProductName = None
        self.SuperUser = None
        self.VpcInfo = None
        self.CanBeDeleted = None


    def _deserialize(self, params):
        self.ProductName = params.get("ProductName")
        self.SuperUser = params.get("SuperUser")
        if params.get("VpcInfo") is not None:
            self.VpcInfo = []
            for item in params.get("VpcInfo"):
                obj = CHDFSProductVpcInfo()
                obj._deserialize(item)
                self.VpcInfo.append(obj)
        self.CanBeDeleted = params.get("CanBeDeleted")
        memeber_set = set(params.keys())
        for name, value in vars(self).items():
            if name in memeber_set:
                memeber_set.remove(name)
        if len(memeber_set) > 0:
            warnings.warn("%s fileds are useless." % ",".join(memeber_set))
        


class CHDFSProductVpcInfo(AbstractModel):
    """chdfs产品vpc信息

    """

    def __init__(self):
        r"""
        :param VpcId: vpc id

注意：此字段可能返回 null，表示取不到有效值。
        :type VpcId: str
        :param VpcName: vpc名称
注意：此字段可能返回 null，表示取不到有效值。
        :type VpcName: str
        :param VpcCidrBlock: vpc子网信息列表
注意：此字段可能返回 null，表示取不到有效值。
        :type VpcCidrBlock: list of VpcCidrBlock
        """
        self.VpcId = None
        self.VpcName = None
        self.VpcCidrBlock = None


    def _deserialize(self, params):
        self.VpcId = params.get("VpcId")
        self.VpcName = params.get("VpcName")
        if params.get("VpcCidrBlock") is not None:
            self.VpcCidrBlock = []
            for item in params.get("VpcCidrBlock"):
                obj = VpcCidrBlock()
                obj._deserialize(item)
                self.VpcCidrBlock.append(obj)
        memeber_set = set(params.keys())
        for name, value in vars(self).items():
            if name in memeber_set:
                memeber_set.remove(name)
        if len(memeber_set) > 0:
            warnings.warn("%s fileds are useless." % ",".join(memeber_set))
        


class CSV(AbstractModel):
    """CSV类型数据格式

    """

    def __init__(self):
        r"""
        :param CodeCompress: 压缩格式，["Snappy", "Gzip", "None"选一]。
        :type CodeCompress: str
        :param CSVSerde: CSV序列化及反序列化数据结构。
        :type CSVSerde: :class:`tencentcloud.dlc.v20210125.models.CSVSerde`
        :param HeadLines: 标题行，默认为0。
        :type HeadLines: int
        :param Format: 格式，默认值为CSV
        :type Format: str
        """
        self.CodeCompress = None
        self.CSVSerde = None
        self.HeadLines = None
        self.Format = None


    def _deserialize(self, params):
        self.CodeCompress = params.get("CodeCompress")
        if params.get("CSVSerde") is not None:
            self.CSVSerde = CSVSerde()
            self.CSVSerde._deserialize(params.get("CSVSerde"))
        self.HeadLines = params.get("HeadLines")
        self.Format = params.get("Format")
        memeber_set = set(params.keys())
        for name, value in vars(self).items():
            if name in memeber_set:
                memeber_set.remove(name)
        if len(memeber_set) > 0:
            warnings.warn("%s fileds are useless." % ",".join(memeber_set))
        


class CSVFile(AbstractModel):
    """CSV类型文件

    """

    def __init__(self):
        r"""
        :param Format: 文本类型，本参数取值为CSV
        :type Format: str
        :param CodeCompress: 压缩格式，["Snappy", "Gzip", "None"选一]。
        :type CodeCompress: str
        :param HeaderLine: 标题行，默认为False。
        :type HeaderLine: bool
        :param NewLineSymbol: 数据行分隔符。
        :type NewLineSymbol: str
        :param CSVSerde: CSV序列化及反序列化数据结构。
        :type CSVSerde: :class:`tencentcloud.dlc.v20210125.models.CSVSerde`
        """
        self.Format = None
        self.CodeCompress = None
        self.HeaderLine = None
        self.NewLineSymbol = None
        self.CSVSerde = None


    def _deserialize(self, params):
        self.Format = params.get("Format")
        self.CodeCompress = params.get("CodeCompress")
        self.HeaderLine = params.get("HeaderLine")
        self.NewLineSymbol = params.get("NewLineSymbol")
        if params.get("CSVSerde") is not None:
            self.CSVSerde = CSVSerde()
            self.CSVSerde._deserialize(params.get("CSVSerde"))
        memeber_set = set(params.keys())
        for name, value in vars(self).items():
            if name in memeber_set:
                memeber_set.remove(name)
        if len(memeber_set) > 0:
            warnings.warn("%s fileds are useless." % ",".join(memeber_set))
        


class CSVSerde(AbstractModel):
    """CSV序列化及反序列化数据结构

    """

    def __init__(self):
        r"""
        :param Escape: CSV序列化转义符，默认为"\\"，最长8个字符，如 Escape: "/\"
        :type Escape: str
        :param Quote: CSV序列化字段域符，默认为"'"，最长8个字符, 如 Quote: "\""
        :type Quote: str
        :param Separator: CSV序列化分隔符，默认为"\t"，最长8个字符, 如 Separator: "\t"
        :type Separator: str
        """
        self.Escape = None
        self.Quote = None
        self.Separator = None


    def _deserialize(self, params):
        self.Escape = params.get("Escape")
        self.Quote = params.get("Quote")
        self.Separator = params.get("Separator")
        memeber_set = set(params.keys())
        for name, value in vars(self).items():
            if name in memeber_set:
                memeber_set.remove(name)
        if len(memeber_set) > 0:
            warnings.warn("%s fileds are useless." % ",".join(memeber_set))
        


class CancelNotebookSessionStatementBatchRequest(AbstractModel):
    """CancelNotebookSessionStatementBatch请求参数结构体

    """

    def __init__(self):
        r"""
        :param SessionId: Session唯一标识
        :type SessionId: str
        :param BatchId: 批任务唯一标识
        :type BatchId: str
        """
        self.SessionId = None
        self.BatchId = None


    def _deserialize(self, params):
        self.SessionId = params.get("SessionId")
        self.BatchId = params.get("BatchId")
        memeber_set = set(params.keys())
        for name, value in vars(self).items():
            if name in memeber_set:
                memeber_set.remove(name)
        if len(memeber_set) > 0:
            warnings.warn("%s fileds are useless." % ",".join(memeber_set))
        


class CancelNotebookSessionStatementBatchResponse(AbstractModel):
    """CancelNotebookSessionStatementBatch返回参数结构体

    """

    def __init__(self):
        r"""
        :param RequestId: 唯一请求 ID，每次请求都会返回。定位问题时需要提供该次请求的 RequestId。
        :type RequestId: str
        """
        self.RequestId = None


    def _deserialize(self, params):
        self.RequestId = params.get("RequestId")


class CancelNotebookSessionStatementRequest(AbstractModel):
    """CancelNotebookSessionStatement请求参数结构体

    """

    def __init__(self):
        r"""
        :param SessionId: Session唯一标识
        :type SessionId: str
        :param StatementId: Session Statement唯一标识
        :type StatementId: str
        """
        self.SessionId = None
        self.StatementId = None


    def _deserialize(self, params):
        self.SessionId = params.get("SessionId")
        self.StatementId = params.get("StatementId")
        memeber_set = set(params.keys())
        for name, value in vars(self).items():
            if name in memeber_set:
                memeber_set.remove(name)
        if len(memeber_set) > 0:
            warnings.warn("%s fileds are useless." % ",".join(memeber_set))
        


class CancelNotebookSessionStatementResponse(AbstractModel):
    """CancelNotebookSessionStatement返回参数结构体

    """

    def __init__(self):
        r"""
        :param RequestId: 唯一请求 ID，每次请求都会返回。定位问题时需要提供该次请求的 RequestId。
        :type RequestId: str
        """
        self.RequestId = None


    def _deserialize(self, params):
        self.RequestId = params.get("RequestId")


class CancelSparkSessionBatchSQLRequest(AbstractModel):
    """CancelSparkSessionBatchSQL请求参数结构体

    """

    def __init__(self):
        r"""
        :param BatchId: 批任务唯一标识
        :type BatchId: str
        """
        self.BatchId = None


    def _deserialize(self, params):
        self.BatchId = params.get("BatchId")
        memeber_set = set(params.keys())
        for name, value in vars(self).items():
            if name in memeber_set:
                memeber_set.remove(name)
        if len(memeber_set) > 0:
            warnings.warn("%s fileds are useless." % ",".join(memeber_set))
        


class CancelSparkSessionBatchSQLResponse(AbstractModel):
    """CancelSparkSessionBatchSQL返回参数结构体

    """

    def __init__(self):
        r"""
        :param RequestId: 唯一请求 ID，每次请求都会返回。定位问题时需要提供该次请求的 RequestId。
        :type RequestId: str
        """
        self.RequestId = None


    def _deserialize(self, params):
        self.RequestId = params.get("RequestId")


class CancelTablePropertiesRequest(AbstractModel):
    """CancelTableProperties请求参数结构体

    """

    def __init__(self):
        r"""
        :param DatasourceConnectionName: Catalog名称
        :type DatasourceConnectionName: str
        :param DatabaseName: 库名
        :type DatabaseName: str
        :param TableName: 表名
        :type TableName: str
        :param Properties: 属性列表
        :type Properties: list of str
        """
        self.DatasourceConnectionName = None
        self.DatabaseName = None
        self.TableName = None
        self.Properties = None


    def _deserialize(self, params):
        self.DatasourceConnectionName = params.get("DatasourceConnectionName")
        self.DatabaseName = params.get("DatabaseName")
        self.TableName = params.get("TableName")
        self.Properties = params.get("Properties")
        memeber_set = set(params.keys())
        for name, value in vars(self).items():
            if name in memeber_set:
                memeber_set.remove(name)
        if len(memeber_set) > 0:
            warnings.warn("%s fileds are useless." % ",".join(memeber_set))
        


class CancelTablePropertiesResponse(AbstractModel):
    """CancelTableProperties返回参数结构体

    """

    def __init__(self):
        r"""
        :param BatchId: 批任务Id
        :type BatchId: str
        :param TaskIdSet: TaskId列表
        :type TaskIdSet: list of str
        :param RequestId: 唯一请求 ID，每次请求都会返回。定位问题时需要提供该次请求的 RequestId。
        :type RequestId: str
        """
        self.BatchId = None
        self.TaskIdSet = None
        self.RequestId = None


    def _deserialize(self, params):
        self.BatchId = params.get("BatchId")
        self.TaskIdSet = params.get("TaskIdSet")
        self.RequestId = params.get("RequestId")


class CancelTaskRequest(AbstractModel):
    """CancelTask请求参数结构体

    """

    def __init__(self):
        r"""
        :param TaskId: 任务Id，全局唯一
        :type TaskId: str
        :param Config: 配置信息，key-value数组，对外不可见。key1：AuthorityRole（鉴权角色，默认传SubUin，base64加密，仅在jdbc提交任务时使用）
        :type Config: list of KVPair
        """
        self.TaskId = None
        self.Config = None


    def _deserialize(self, params):
        self.TaskId = params.get("TaskId")
        if params.get("Config") is not None:
            self.Config = []
            for item in params.get("Config"):
                obj = KVPair()
                obj._deserialize(item)
                self.Config.append(obj)
        memeber_set = set(params.keys())
        for name, value in vars(self).items():
            if name in memeber_set:
                memeber_set.remove(name)
        if len(memeber_set) > 0:
            warnings.warn("%s fileds are useless." % ",".join(memeber_set))
        


class CancelTaskResponse(AbstractModel):
    """CancelTask返回参数结构体

    """

    def __init__(self):
        r"""
        :param RequestId: 唯一请求 ID，每次请求都会返回。定位问题时需要提供该次请求的 RequestId。
        :type RequestId: str
        """
        self.RequestId = None


    def _deserialize(self, params):
        self.RequestId = params.get("RequestId")


class CancelTasksRequest(AbstractModel):
    """CancelTasks请求参数结构体

    """

    def __init__(self):
        r"""
        :param TaskId: 任务Id数组，全局唯一
        :type TaskId: list of str
        :param Config: 配置信息，key-value数组，对外不可见。key1：AuthorityRole（鉴权角色，默认传SubUin，base64加密，仅在jdbc提交任务时使用）
        :type Config: list of KVPair
        """
        self.TaskId = None
        self.Config = None


    def _deserialize(self, params):
        self.TaskId = params.get("TaskId")
        if params.get("Config") is not None:
            self.Config = []
            for item in params.get("Config"):
                obj = KVPair()
                obj._deserialize(item)
                self.Config.append(obj)
        memeber_set = set(params.keys())
        for name, value in vars(self).items():
            if name in memeber_set:
                memeber_set.remove(name)
        if len(memeber_set) > 0:
            warnings.warn("%s fileds are useless." % ",".join(memeber_set))
        


class CancelTasksResponse(AbstractModel):
    """CancelTasks返回参数结构体

    """

    def __init__(self):
        r"""
        :param RequestId: 唯一请求 ID，每次请求都会返回。定位问题时需要提供该次请求的 RequestId。
        :type RequestId: str
        """
        self.RequestId = None


    def _deserialize(self, params):
        self.RequestId = params.get("RequestId")


class CanvasInfo(AbstractModel):
    """画布数据

    """

    def __init__(self):
        r"""
        :param FolderId: 文件夹ID
注意：此字段可能返回 null，表示取不到有效值。
        :type FolderId: str
        :param WorkflowId: 调度计划ID
注意：此字段可能返回 null，表示取不到有效值。
        :type WorkflowId: str
        :param WorkflowName: 调度计划名称
注意：此字段可能返回 null，表示取不到有效值。
        :type WorkflowName: str
        :param WorkflowDesc: 调度计划描述
注意：此字段可能返回 null，表示取不到有效值。
        :type WorkflowDesc: str
        :param Tasks: 任务列表
注意：此字段可能返回 null，表示取不到有效值。
        :type Tasks: list of TaskDto
        :param Links: 依赖关系列表
注意：此字段可能返回 null，表示取不到有效值。
        :type Links: list of Link
        """
        self.FolderId = None
        self.WorkflowId = None
        self.WorkflowName = None
        self.WorkflowDesc = None
        self.Tasks = None
        self.Links = None


    def _deserialize(self, params):
        self.FolderId = params.get("FolderId")
        self.WorkflowId = params.get("WorkflowId")
        self.WorkflowName = params.get("WorkflowName")
        self.WorkflowDesc = params.get("WorkflowDesc")
        if params.get("Tasks") is not None:
            self.Tasks = []
            for item in params.get("Tasks"):
                obj = TaskDto()
                obj._deserialize(item)
                self.Tasks.append(obj)
        if params.get("Links") is not None:
            self.Links = []
            for item in params.get("Links"):
                obj = Link()
                obj._deserialize(item)
                self.Links.append(obj)
        memeber_set = set(params.keys())
        for name, value in vars(self).items():
            if name in memeber_set:
                memeber_set.remove(name)
        if len(memeber_set) > 0:
            warnings.warn("%s fileds are useless." % ",".join(memeber_set))
        


class ChangeColumnRequest(AbstractModel):
    """ChangeColumn请求参数结构体

    """

    def __init__(self):
        r"""
        :param DatabaseName: 数据库名称
        :type DatabaseName: str
        :param TableName: 数据表名称
        :type TableName: str
        :param Column: 字段
        :type Column: :class:`tencentcloud.dlc.v20210125.models.Column`
        :param DatasourceConnectionName: 数据源名称
        :type DatasourceConnectionName: str
        """
        self.DatabaseName = None
        self.TableName = None
        self.Column = None
        self.DatasourceConnectionName = None


    def _deserialize(self, params):
        self.DatabaseName = params.get("DatabaseName")
        self.TableName = params.get("TableName")
        if params.get("Column") is not None:
            self.Column = Column()
            self.Column._deserialize(params.get("Column"))
        self.DatasourceConnectionName = params.get("DatasourceConnectionName")
        memeber_set = set(params.keys())
        for name, value in vars(self).items():
            if name in memeber_set:
                memeber_set.remove(name)
        if len(memeber_set) > 0:
            warnings.warn("%s fileds are useless." % ",".join(memeber_set))
        


class ChangeColumnResponse(AbstractModel):
    """ChangeColumn返回参数结构体

    """

    def __init__(self):
        r"""
        :param Execution: 执行语句
        :type Execution: :class:`tencentcloud.dlc.v20210125.models.Execution`
        :param TaskId: 任务Id
        :type TaskId: str
        :param RequestId: 唯一请求 ID，每次请求都会返回。定位问题时需要提供该次请求的 RequestId。
        :type RequestId: str
        """
        self.Execution = None
        self.TaskId = None
        self.RequestId = None


    def _deserialize(self, params):
        if params.get("Execution") is not None:
            self.Execution = Execution()
            self.Execution._deserialize(params.get("Execution"))
        self.TaskId = params.get("TaskId")
        self.RequestId = params.get("RequestId")


class CheckDLCResourceRoleRequest(AbstractModel):
    """CheckDLCResourceRole请求参数结构体

    """

    def __init__(self):
        r"""
        :param RoleName: 角色名称
        :type RoleName: str
        """
        self.RoleName = None


    def _deserialize(self, params):
        self.RoleName = params.get("RoleName")
        memeber_set = set(params.keys())
        for name, value in vars(self).items():
            if name in memeber_set:
                memeber_set.remove(name)
        if len(memeber_set) > 0:
            warnings.warn("%s fileds are useless." % ",".join(memeber_set))
        


class CheckDLCResourceRoleResponse(AbstractModel):
    """CheckDLCResourceRole返回参数结构体

    """

    def __init__(self):
        r"""
        :param Granted: 是否授权。true为已授权，false为未授权。
        :type Granted: bool
        :param RequestId: 唯一请求 ID，每次请求都会返回。定位问题时需要提供该次请求的 RequestId。
        :type RequestId: str
        """
        self.Granted = None
        self.RequestId = None


    def _deserialize(self, params):
        self.Granted = params.get("Granted")
        self.RequestId = params.get("RequestId")


class CheckDataEngineConfigPairsValidityRequest(AbstractModel):
    """CheckDataEngineConfigPairsValidity请求参数结构体

    """

    def __init__(self):
        r"""
        :param ChildImageVersionId: 引擎小版本ID
        :type ChildImageVersionId: str
        :param DataEngineConfigPairs: 用户自定义参数
        :type DataEngineConfigPairs: list of DataEngineConfigPair
        :param ImageVersionId: 引擎大版本ID，存在小版本ID时仅需传入小版本ID，不存在时会获取当前大版本下最新的小版本ID。
        :type ImageVersionId: str
        """
        self.ChildImageVersionId = None
        self.DataEngineConfigPairs = None
        self.ImageVersionId = None


    def _deserialize(self, params):
        self.ChildImageVersionId = params.get("ChildImageVersionId")
        if params.get("DataEngineConfigPairs") is not None:
            self.DataEngineConfigPairs = []
            for item in params.get("DataEngineConfigPairs"):
                obj = DataEngineConfigPair()
                obj._deserialize(item)
                self.DataEngineConfigPairs.append(obj)
        self.ImageVersionId = params.get("ImageVersionId")
        memeber_set = set(params.keys())
        for name, value in vars(self).items():
            if name in memeber_set:
                memeber_set.remove(name)
        if len(memeber_set) > 0:
            warnings.warn("%s fileds are useless." % ",".join(memeber_set))
        


class CheckDataEngineConfigPairsValidityResponse(AbstractModel):
    """CheckDataEngineConfigPairsValidity返回参数结构体

    """

    def __init__(self):
        r"""
        :param IsAvailable: 参数有效性：ture:有效，false:至少存在一个无效参数；
        :type IsAvailable: bool
        :param UnavailableConfig: 无效参数集合
注意：此字段可能返回 null，表示取不到有效值。
        :type UnavailableConfig: list of str
        :param RequestId: 唯一请求 ID，每次请求都会返回。定位问题时需要提供该次请求的 RequestId。
        :type RequestId: str
        """
        self.IsAvailable = None
        self.UnavailableConfig = None
        self.RequestId = None


    def _deserialize(self, params):
        self.IsAvailable = params.get("IsAvailable")
        self.UnavailableConfig = params.get("UnavailableConfig")
        self.RequestId = params.get("RequestId")


class CheckDataEngineImageCanBeRollbackRequest(AbstractModel):
    """CheckDataEngineImageCanBeRollback请求参数结构体

    """

    def __init__(self):
        r"""
        :param DataEngineId: 引擎唯一id
        :type DataEngineId: str
        """
        self.DataEngineId = None


    def _deserialize(self, params):
        self.DataEngineId = params.get("DataEngineId")
        memeber_set = set(params.keys())
        for name, value in vars(self).items():
            if name in memeber_set:
                memeber_set.remove(name)
        if len(memeber_set) > 0:
            warnings.warn("%s fileds are useless." % ",".join(memeber_set))
        


class CheckDataEngineImageCanBeRollbackResponse(AbstractModel):
    """CheckDataEngineImageCanBeRollback返回参数结构体

    """

    def __init__(self):
        r"""
        :param ToRecordId: 回滚后日志记录id
        :type ToRecordId: str
        :param FromRecordId: 回滚前日志记录id
        :type FromRecordId: str
        :param IsRollback: 是否能够回滚
        :type IsRollback: bool
        :param RequestId: 唯一请求 ID，每次请求都会返回。定位问题时需要提供该次请求的 RequestId。
        :type RequestId: str
        """
        self.ToRecordId = None
        self.FromRecordId = None
        self.IsRollback = None
        self.RequestId = None


    def _deserialize(self, params):
        self.ToRecordId = params.get("ToRecordId")
        self.FromRecordId = params.get("FromRecordId")
        self.IsRollback = params.get("IsRollback")
        self.RequestId = params.get("RequestId")


class CheckDataEngineImageCanBeUpgradeRequest(AbstractModel):
    """CheckDataEngineImageCanBeUpgrade请求参数结构体

    """

    def __init__(self):
        r"""
        :param DataEngineId: 集群id
        :type DataEngineId: str
        """
        self.DataEngineId = None


    def _deserialize(self, params):
        self.DataEngineId = params.get("DataEngineId")
        memeber_set = set(params.keys())
        for name, value in vars(self).items():
            if name in memeber_set:
                memeber_set.remove(name)
        if len(memeber_set) > 0:
            warnings.warn("%s fileds are useless." % ",".join(memeber_set))
        


class CheckDataEngineImageCanBeUpgradeResponse(AbstractModel):
    """CheckDataEngineImageCanBeUpgrade返回参数结构体

    """

    def __init__(self):
        r"""
        :param ChildImageVersionId: 当前大版本下，可升级的集群镜像小版本id
        :type ChildImageVersionId: str
        :param IsUpgrade: 是否能够升级
        :type IsUpgrade: bool
        :param RequestId: 唯一请求 ID，每次请求都会返回。定位问题时需要提供该次请求的 RequestId。
        :type RequestId: str
        """
        self.ChildImageVersionId = None
        self.IsUpgrade = None
        self.RequestId = None


    def _deserialize(self, params):
        self.ChildImageVersionId = params.get("ChildImageVersionId")
        self.IsUpgrade = params.get("IsUpgrade")
        self.RequestId = params.get("RequestId")


class CheckDatabaseExistsRequest(AbstractModel):
    """CheckDatabaseExists请求参数结构体

    """

    def __init__(self):
        r"""
        :param DatasourceConnectionName: 指定查询的数据源名称，默认为DataLakeCatalog
        :type DatasourceConnectionName: str
        :param DatabaseName: 指定查询的数据库名称
        :type DatabaseName: str
        """
        self.DatasourceConnectionName = None
        self.DatabaseName = None


    def _deserialize(self, params):
        self.DatasourceConnectionName = params.get("DatasourceConnectionName")
        self.DatabaseName = params.get("DatabaseName")
        memeber_set = set(params.keys())
        for name, value in vars(self).items():
            if name in memeber_set:
                memeber_set.remove(name)
        if len(memeber_set) > 0:
            warnings.warn("%s fileds are useless." % ",".join(memeber_set))
        


class CheckDatabaseExistsResponse(AbstractModel):
    """CheckDatabaseExists返回参数结构体

    """

    def __init__(self):
        r"""
        :param IsExists: 是否存在：true：存在，false（默认）：不存在
        :type IsExists: bool
        :param RequestId: 唯一请求 ID，每次请求都会返回。定位问题时需要提供该次请求的 RequestId。
        :type RequestId: str
        """
        self.IsExists = None
        self.RequestId = None


    def _deserialize(self, params):
        self.IsExists = params.get("IsExists")
        self.RequestId = params.get("RequestId")


class CheckDatabaseUDFExistsRequest(AbstractModel):
    """CheckDatabaseUDFExists请求参数结构体

    """

    def __init__(self):
        r"""
        :param DatabaseName: 指定查询的数据库名称
        :type DatabaseName: str
        :param UDFName: 指定查询的UDF名称
        :type UDFName: str
        :param DatasourceConnectionName: 数据源连接
        :type DatasourceConnectionName: str
        """
        self.DatabaseName = None
        self.UDFName = None
        self.DatasourceConnectionName = None


    def _deserialize(self, params):
        self.DatabaseName = params.get("DatabaseName")
        self.UDFName = params.get("UDFName")
        self.DatasourceConnectionName = params.get("DatasourceConnectionName")
        memeber_set = set(params.keys())
        for name, value in vars(self).items():
            if name in memeber_set:
                memeber_set.remove(name)
        if len(memeber_set) > 0:
            warnings.warn("%s fileds are useless." % ",".join(memeber_set))
        


class CheckDatabaseUDFExistsResponse(AbstractModel):
    """CheckDatabaseUDFExists返回参数结构体

    """

    def __init__(self):
        r"""
        :param IsExists: 是否存在：true：存在，false（默认）：不存在
        :type IsExists: bool
        :param RequestId: 唯一请求 ID，每次请求都会返回。定位问题时需要提供该次请求的 RequestId。
        :type RequestId: str
        """
        self.IsExists = None
        self.RequestId = None


    def _deserialize(self, params):
        self.IsExists = params.get("IsExists")
        self.RequestId = params.get("RequestId")


class CheckDatasourceConnectivityRequest(AbstractModel):
    """CheckDatasourceConnectivity请求参数结构体

    """

    def __init__(self):
        r"""
        :param DatasourceConnectionName: 数据连接名称
        :type DatasourceConnectionName: str
        :param DatasourceConnectionId: 数据连接Id
        :type DatasourceConnectionId: str
        :param DatasourceConnectionType: 数据源连接类型，当前支持：Mysql、HiveCos、HiveHdfs、PostgreSQL、SQLServer、ClickHouse、Elasticsearch
        :type DatasourceConnectionType: str
        :param DatasourceConnectionConfig: 数据源连接属性
        :type DatasourceConnectionConfig: :class:`tencentcloud.dlc.v20210125.models.DatasourceConnectionConfig`
        """
        self.DatasourceConnectionName = None
        self.DatasourceConnectionId = None
        self.DatasourceConnectionType = None
        self.DatasourceConnectionConfig = None


    def _deserialize(self, params):
        self.DatasourceConnectionName = params.get("DatasourceConnectionName")
        self.DatasourceConnectionId = params.get("DatasourceConnectionId")
        self.DatasourceConnectionType = params.get("DatasourceConnectionType")
        if params.get("DatasourceConnectionConfig") is not None:
            self.DatasourceConnectionConfig = DatasourceConnectionConfig()
            self.DatasourceConnectionConfig._deserialize(params.get("DatasourceConnectionConfig"))
        memeber_set = set(params.keys())
        for name, value in vars(self).items():
            if name in memeber_set:
                memeber_set.remove(name)
        if len(memeber_set) > 0:
            warnings.warn("%s fileds are useless." % ",".join(memeber_set))
        


class CheckDatasourceConnectivityResponse(AbstractModel):
    """CheckDatasourceConnectivity返回参数结构体

    """

    def __init__(self):
        r"""
        :param IsSuccess: 连通状态：true（连通）、false（未连通）
        :type IsSuccess: bool
        :param Tips: 连通性测试提示信息
        :type Tips: str
        :param RequestId: 唯一请求 ID，每次请求都会返回。定位问题时需要提供该次请求的 RequestId。
        :type RequestId: str
        """
        self.IsSuccess = None
        self.Tips = None
        self.RequestId = None


    def _deserialize(self, params):
        self.IsSuccess = params.get("IsSuccess")
        self.Tips = params.get("Tips")
        self.RequestId = params.get("RequestId")


class CheckInstanceNameRequest(AbstractModel):
    """CheckInstanceName请求参数结构体

    """

    def __init__(self):
        r"""
        :param InstanceName: 要创建的实例名称
        :type InstanceName: str
        """
        self.InstanceName = None


    def _deserialize(self, params):
        self.InstanceName = params.get("InstanceName")
        memeber_set = set(params.keys())
        for name, value in vars(self).items():
            if name in memeber_set:
                memeber_set.remove(name)
        if len(memeber_set) > 0:
            warnings.warn("%s fileds are useless." % ",".join(memeber_set))
        


class CheckInstanceNameResponse(AbstractModel):
    """CheckInstanceName返回参数结构体

    """

    def __init__(self):
        r"""
        :param Valid: 实例名称是否有效。false：重名；true：没有重名
        :type Valid: bool
        :param RequestId: 唯一请求 ID，每次请求都会返回。定位问题时需要提供该次请求的 RequestId。
        :type RequestId: str
        """
        self.Valid = None
        self.RequestId = None


    def _deserialize(self, params):
        self.Valid = params.get("Valid")
        self.RequestId = params.get("RequestId")


class CheckLakeFsChdfsEnableRequest(AbstractModel):
    """CheckLakeFsChdfsEnable请求参数结构体

    """


class CheckLakeFsChdfsEnableResponse(AbstractModel):
    """CheckLakeFsChdfsEnable返回参数结构体

    """

    def __init__(self):
        r"""
        :param ChdfsEnable: true支持；false不支持
        :type ChdfsEnable: bool
        :param RequestId: 唯一请求 ID，每次请求都会返回。定位问题时需要提供该次请求的 RequestId。
        :type RequestId: str
        """
        self.ChdfsEnable = None
        self.RequestId = None


    def _deserialize(self, params):
        self.ChdfsEnable = params.get("ChdfsEnable")
        self.RequestId = params.get("RequestId")


class CheckLakeFsExistRequest(AbstractModel):
    """CheckLakeFsExist请求参数结构体

    """


class CheckLakeFsExistResponse(AbstractModel):
    """CheckLakeFsExist返回参数结构体

    """

    def __init__(self):
        r"""
        :param LakeFsExist: true已创建；false未创建
        :type LakeFsExist: bool
        :param RequestId: 唯一请求 ID，每次请求都会返回。定位问题时需要提供该次请求的 RequestId。
        :type RequestId: str
        """
        self.LakeFsExist = None
        self.RequestId = None


    def _deserialize(self, params):
        self.LakeFsExist = params.get("LakeFsExist")
        self.RequestId = params.get("RequestId")


class CheckLockMetaDataRequest(AbstractModel):
    """CheckLockMetaData请求参数结构体

    """

    def __init__(self):
        r"""
        :param LockId: 锁ID
        :type LockId: int
        :param DatasourceConnectionName: 数据源名称
        :type DatasourceConnectionName: str
        :param TxnId: 事务ID
        :type TxnId: int
        :param ElapsedMs: 过期时间ms
        :type ElapsedMs: int
        """
        self.LockId = None
        self.DatasourceConnectionName = None
        self.TxnId = None
        self.ElapsedMs = None


    def _deserialize(self, params):
        self.LockId = params.get("LockId")
        self.DatasourceConnectionName = params.get("DatasourceConnectionName")
        self.TxnId = params.get("TxnId")
        self.ElapsedMs = params.get("ElapsedMs")
        memeber_set = set(params.keys())
        for name, value in vars(self).items():
            if name in memeber_set:
                memeber_set.remove(name)
        if len(memeber_set) > 0:
            warnings.warn("%s fileds are useless." % ",".join(memeber_set))
        


class CheckLockMetaDataResponse(AbstractModel):
    """CheckLockMetaData返回参数结构体

    """

    def __init__(self):
        r"""
        :param LockId: 锁ID
        :type LockId: int
        :param LockState: 锁状态：ACQUIRED、WAITING、ABORT、NOT_ACQUIRED
        :type LockState: str
        :param RequestId: 唯一请求 ID，每次请求都会返回。定位问题时需要提供该次请求的 RequestId。
        :type RequestId: str
        """
        self.LockId = None
        self.LockState = None
        self.RequestId = None


    def _deserialize(self, params):
        self.LockId = params.get("LockId")
        self.LockState = params.get("LockState")
        self.RequestId = params.get("RequestId")


class CheckRegionCHDFSEnableRequest(AbstractModel):
    """CheckRegionCHDFSEnable请求参数结构体

    """


class CheckRegionCHDFSEnableResponse(AbstractModel):
    """CheckRegionCHDFSEnable返回参数结构体

    """

    def __init__(self):
        r"""
        :param CHDFSEnable: 是否支持元数据加速能力
        :type CHDFSEnable: bool
        :param RequestId: 唯一请求 ID，每次请求都会返回。定位问题时需要提供该次请求的 RequestId。
        :type RequestId: str
        """
        self.CHDFSEnable = None
        self.RequestId = None


    def _deserialize(self, params):
        self.CHDFSEnable = params.get("CHDFSEnable")
        self.RequestId = params.get("RequestId")


class CheckSQLSessionCatalogNameExistsRequest(AbstractModel):
    """CheckSQLSessionCatalogNameExists请求参数结构体

    """

    def __init__(self):
        r"""
        :param Name: 节点名称
        :type Name: str
        :param Type: 节点类型：0（目录）、1（会话）
        :type Type: str
        :param Path: 父节点路径
        :type Path: str
        """
        self.Name = None
        self.Type = None
        self.Path = None


    def _deserialize(self, params):
        self.Name = params.get("Name")
        self.Type = params.get("Type")
        self.Path = params.get("Path")
        memeber_set = set(params.keys())
        for name, value in vars(self).items():
            if name in memeber_set:
                memeber_set.remove(name)
        if len(memeber_set) > 0:
            warnings.warn("%s fileds are useless." % ",".join(memeber_set))
        


class CheckSQLSessionCatalogNameExistsResponse(AbstractModel):
    """CheckSQLSessionCatalogNameExists返回参数结构体

    """

    def __init__(self):
        r"""
        :param Status: SUCCESS：成功、FAIL：失败、FLUSH：会话内容已变更，请刷新（修改时触发）、DUPLICATE：重名，请调整、NOTEMPTY：该目录下不为空，无法删除、
LIMITEXCEEDED：创建的会话超过限制；
        :type Status: str
        :param RequestId: 唯一请求 ID，每次请求都会返回。定位问题时需要提供该次请求的 RequestId。
        :type RequestId: str
        """
        self.Status = None
        self.RequestId = None


    def _deserialize(self, params):
        self.Status = params.get("Status")
        self.RequestId = params.get("RequestId")


class CheckScheduleScriptExistRequest(AbstractModel):
    """CheckScheduleScriptExist请求参数结构体

    """

    def __init__(self):
        r"""
        :param ScriptId: 脚本ID
        :type ScriptId: str
        :param ScriptName: 脚本名称
        :type ScriptName: str
        """
        self.ScriptId = None
        self.ScriptName = None


    def _deserialize(self, params):
        self.ScriptId = params.get("ScriptId")
        self.ScriptName = params.get("ScriptName")
        memeber_set = set(params.keys())
        for name, value in vars(self).items():
            if name in memeber_set:
                memeber_set.remove(name)
        if len(memeber_set) > 0:
            warnings.warn("%s fileds are useless." % ",".join(memeber_set))
        


class CheckScheduleScriptExistResponse(AbstractModel):
    """CheckScheduleScriptExist返回参数结构体

    """

    def __init__(self):
        r"""
        :param WorkflowIds: 脚本所在工作流列表
        :type WorkflowIds: list of str
        :param TotalElements: 脚本所在工作流数量
        :type TotalElements: int
        :param RequestId: 唯一请求 ID，每次请求都会返回。定位问题时需要提供该次请求的 RequestId。
        :type RequestId: str
        """
        self.WorkflowIds = None
        self.TotalElements = None
        self.RequestId = None


    def _deserialize(self, params):
        self.WorkflowIds = params.get("WorkflowIds")
        self.TotalElements = params.get("TotalElements")
        self.RequestId = params.get("RequestId")


class CheckScheduleTaskNameExistsRequest(AbstractModel):
    """CheckScheduleTaskNameExists请求参数结构体

    """

    def __init__(self):
        r"""
        :param ScheduleTaskName: 调度任务名称
        :type ScheduleTaskName: str
        :param TaskId: 任务ID
        :type TaskId: str
        """
        self.ScheduleTaskName = None
        self.TaskId = None


    def _deserialize(self, params):
        self.ScheduleTaskName = params.get("ScheduleTaskName")
        self.TaskId = params.get("TaskId")
        memeber_set = set(params.keys())
        for name, value in vars(self).items():
            if name in memeber_set:
                memeber_set.remove(name)
        if len(memeber_set) > 0:
            warnings.warn("%s fileds are useless." % ",".join(memeber_set))
        


class CheckScheduleTaskNameExistsResponse(AbstractModel):
    """CheckScheduleTaskNameExists返回参数结构体

    """

    def __init__(self):
        r"""
        :param IsExists: 是否重名
        :type IsExists: bool
        :param RequestId: 唯一请求 ID，每次请求都会返回。定位问题时需要提供该次请求的 RequestId。
        :type RequestId: str
        """
        self.IsExists = None
        self.RequestId = None


    def _deserialize(self, params):
        self.IsExists = params.get("IsExists")
        self.RequestId = params.get("RequestId")


class CheckSparkImageExistsRequest(AbstractModel):
    """CheckSparkImageExists请求参数结构体

    """

    def __init__(self):
        r"""
        :param ImageVersion: 镜像version
        :type ImageVersion: str
        :param ImageVersionId: imageId
        :type ImageVersionId: str
        """
        self.ImageVersion = None
        self.ImageVersionId = None


    def _deserialize(self, params):
        self.ImageVersion = params.get("ImageVersion")
        self.ImageVersionId = params.get("ImageVersionId")
        memeber_set = set(params.keys())
        for name, value in vars(self).items():
            if name in memeber_set:
                memeber_set.remove(name)
        if len(memeber_set) > 0:
            warnings.warn("%s fileds are useless." % ",".join(memeber_set))
        


class CheckSparkImageExistsResponse(AbstractModel):
    """CheckSparkImageExists返回参数结构体

    """

    def __init__(self):
        r"""
        :param IsExists: 镜像是否存在：true：存在、false：不存在
        :type IsExists: bool
        :param RequestId: 唯一请求 ID，每次请求都会返回。定位问题时需要提供该次请求的 RequestId。
        :type RequestId: str
        """
        self.IsExists = None
        self.RequestId = None


    def _deserialize(self, params):
        self.IsExists = params.get("IsExists")
        self.RequestId = params.get("RequestId")


class CheckSparkImageUserRecordExistsRequest(AbstractModel):
    """CheckSparkImageUserRecordExists请求参数结构体

    """

    def __init__(self):
        r"""
        :param ImageId: 镜像编码
        :type ImageId: str
        :param UserAppId: 用户APPID
        :type UserAppId: int
        :param ImageType: 枚举值：1（父版本）、2（子版本）、3（pyspark）
        :type ImageType: int
        """
        self.ImageId = None
        self.UserAppId = None
        self.ImageType = None


    def _deserialize(self, params):
        self.ImageId = params.get("ImageId")
        self.UserAppId = params.get("UserAppId")
        self.ImageType = params.get("ImageType")
        memeber_set = set(params.keys())
        for name, value in vars(self).items():
            if name in memeber_set:
                memeber_set.remove(name)
        if len(memeber_set) > 0:
            warnings.warn("%s fileds are useless." % ",".join(memeber_set))
        


class CheckSparkImageUserRecordExistsResponse(AbstractModel):
    """CheckSparkImageUserRecordExists返回参数结构体

    """

    def __init__(self):
        r"""
        :param IsExists: 记录是否存在：true：存在，false：不存在
        :type IsExists: bool
        :param RequestId: 唯一请求 ID，每次请求都会返回。定位问题时需要提供该次请求的 RequestId。
        :type RequestId: str
        """
        self.IsExists = None
        self.RequestId = None


    def _deserialize(self, params):
        self.IsExists = params.get("IsExists")
        self.RequestId = params.get("RequestId")


class CheckTableExistsRequest(AbstractModel):
    """CheckTableExists请求参数结构体

    """

    def __init__(self):
        r"""
        :param DatasourceConnectionName: 指定查询的数据源名称，默认为DataLakeCatalog
        :type DatasourceConnectionName: str
        :param DatabaseName: 指定查询的数据库名称
        :type DatabaseName: str
        :param TableName: 指定查询的数据表名称
        :type TableName: str
        """
        self.DatasourceConnectionName = None
        self.DatabaseName = None
        self.TableName = None


    def _deserialize(self, params):
        self.DatasourceConnectionName = params.get("DatasourceConnectionName")
        self.DatabaseName = params.get("DatabaseName")
        self.TableName = params.get("TableName")
        memeber_set = set(params.keys())
        for name, value in vars(self).items():
            if name in memeber_set:
                memeber_set.remove(name)
        if len(memeber_set) > 0:
            warnings.warn("%s fileds are useless." % ",".join(memeber_set))
        


class CheckTableExistsResponse(AbstractModel):
    """CheckTableExists返回参数结构体

    """

    def __init__(self):
        r"""
        :param IsExists: 是否存在：true：存在，false（默认）：不存在
        :type IsExists: bool
        :param RequestId: 唯一请求 ID，每次请求都会返回。定位问题时需要提供该次请求的 RequestId。
        :type RequestId: str
        """
        self.IsExists = None
        self.RequestId = None


    def _deserialize(self, params):
        self.IsExists = params.get("IsExists")
        self.RequestId = params.get("RequestId")


class CheckViewExistsRequest(AbstractModel):
    """CheckViewExists请求参数结构体

    """

    def __init__(self):
        r"""
        :param DatasourceConnectionName: 指定查询的数据源名称，默认为DataLakeCatalog
        :type DatasourceConnectionName: str
        :param DatabaseName: 指定查询的数据库名称
        :type DatabaseName: str
        :param ViewName: 指定查询的视图名称
        :type ViewName: str
        """
        self.DatasourceConnectionName = None
        self.DatabaseName = None
        self.ViewName = None


    def _deserialize(self, params):
        self.DatasourceConnectionName = params.get("DatasourceConnectionName")
        self.DatabaseName = params.get("DatabaseName")
        self.ViewName = params.get("ViewName")
        memeber_set = set(params.keys())
        for name, value in vars(self).items():
            if name in memeber_set:
                memeber_set.remove(name)
        if len(memeber_set) > 0:
            warnings.warn("%s fileds are useless." % ",".join(memeber_set))
        


class CheckViewExistsResponse(AbstractModel):
    """CheckViewExists返回参数结构体

    """

    def __init__(self):
        r"""
        :param IsExists: 是否存在：true：存在，false（默认）：不存在
        :type IsExists: bool
        :param RequestId: 唯一请求 ID，每次请求都会返回。定位问题时需要提供该次请求的 RequestId。
        :type RequestId: str
        """
        self.IsExists = None
        self.RequestId = None


    def _deserialize(self, params):
        self.IsExists = params.get("IsExists")
        self.RequestId = params.get("RequestId")


class CheckVpcCidrBlockRequest(AbstractModel):
    """CheckVpcCidrBlock请求参数结构体

    """

    def __init__(self):
        r"""
        :param VpcCidrBlock: vpc的cidrblock
        :type VpcCidrBlock: str
        """
        self.VpcCidrBlock = None


    def _deserialize(self, params):
        self.VpcCidrBlock = params.get("VpcCidrBlock")
        memeber_set = set(params.keys())
        for name, value in vars(self).items():
            if name in memeber_set:
                memeber_set.remove(name)
        if len(memeber_set) > 0:
            warnings.warn("%s fileds are useless." % ",".join(memeber_set))
        


class CheckVpcCidrBlockResponse(AbstractModel):
    """CheckVpcCidrBlock返回参数结构体

    """

    def __init__(self):
        r"""
        :param CidrBlockValid: cidrblock是否符合预期，false不符合，true符合
        :type CidrBlockValid: bool
        :param RequestId: 唯一请求 ID，每次请求都会返回。定位问题时需要提供该次请求的 RequestId。
        :type RequestId: str
        """
        self.CidrBlockValid = None
        self.RequestId = None


    def _deserialize(self, params):
        self.CidrBlockValid = params.get("CidrBlockValid")
        self.RequestId = params.get("RequestId")


class CleanImportStorageRequest(AbstractModel):
    """CleanImportStorage请求参数结构体

    """

    def __init__(self):
        r"""
        :param FsPath: 需要清理的路径
        :type FsPath: str
        """
        self.FsPath = None


    def _deserialize(self, params):
        self.FsPath = params.get("FsPath")
        memeber_set = set(params.keys())
        for name, value in vars(self).items():
            if name in memeber_set:
                memeber_set.remove(name)
        if len(memeber_set) > 0:
            warnings.warn("%s fileds are useless." % ",".join(memeber_set))
        


class CleanImportStorageResponse(AbstractModel):
    """CleanImportStorage返回参数结构体

    """

    def __init__(self):
        r"""
        :param RequestId: 唯一请求 ID，每次请求都会返回。定位问题时需要提供该次请求的 RequestId。
        :type RequestId: str
        """
        self.RequestId = None


    def _deserialize(self, params):
        self.RequestId = params.get("RequestId")


class CloseOrOpenSQLSessionSnapshotRequest(AbstractModel):
    """CloseOrOpenSQLSessionSnapshot请求参数结构体

    """

    def __init__(self):
        r"""
        :param SessionId: 会话ID
        :type SessionId: str
        :param IsOpened: 会话是否被打开：0（关闭，默认）；1（打开）
        :type IsOpened: int
        :param Operator: 操作人
        :type Operator: str
        :param LastUsed: 会话最近一次打开时间
        :type LastUsed: str
        """
        self.SessionId = None
        self.IsOpened = None
        self.Operator = None
        self.LastUsed = None


    def _deserialize(self, params):
        self.SessionId = params.get("SessionId")
        self.IsOpened = params.get("IsOpened")
        self.Operator = params.get("Operator")
        self.LastUsed = params.get("LastUsed")
        memeber_set = set(params.keys())
        for name, value in vars(self).items():
            if name in memeber_set:
                memeber_set.remove(name)
        if len(memeber_set) > 0:
            warnings.warn("%s fileds are useless." % ",".join(memeber_set))
        


class CloseOrOpenSQLSessionSnapshotResponse(AbstractModel):
    """CloseOrOpenSQLSessionSnapshot返回参数结构体

    """

    def __init__(self):
        r"""
        :param Status: SUCCESS：成功、FAIL：失败、FLUSH：会话内容已变更，请刷新（修改时触发）、DUPLICATE：重名，请调整、NOTEMPTY：该目录下不为空，无法删除、
LIMITEXCEEDED：创建的会话超过限制；
        :type Status: str
        :param RequestId: 唯一请求 ID，每次请求都会返回。定位问题时需要提供该次请求的 RequestId。
        :type RequestId: str
        """
        self.Status = None
        self.RequestId = None


    def _deserialize(self, params):
        self.Status = params.get("Status")
        self.RequestId = params.get("RequestId")


class Column(AbstractModel):
    """数据表列信息。

    """

    def __init__(self):
        r"""
        :param Name: 列名称，不区分大小写，最大支持25个字符。
        :type Name: str
        :param Type: 列类型，支持如下类型定义:
string|tinyint|smallint|int|bigint|boolean|float|double|decimal|timestamp|date|binary|array<data_type>|map<primitive_type, data_type>|struct<col_name : data_type [COMMENT col_comment], ...>|uniontype<data_type, data_type, ...>。
        :type Type: str
        :param Comment: 对该类的注释。
注意：此字段可能返回 null，表示取不到有效值。
        :type Comment: str
        :param Precision: 表示整个 numeric 的长度
注意：此字段可能返回 null，表示取不到有效值。
        :type Precision: int
        :param Scale: 表示小数部分的长度
注意：此字段可能返回 null，表示取不到有效值。
        :type Scale: int
        :param Nullable: 是否为null
注意：此字段可能返回 null，表示取不到有效值。
        :type Nullable: str
        :param Position: 字段位置，小的在前
注意：此字段可能返回 null，表示取不到有效值。
        :type Position: int
        :param CreateTime: 字段创建时间
注意：此字段可能返回 null，表示取不到有效值。
        :type CreateTime: str
        :param ModifiedTime: 字段修改时间
注意：此字段可能返回 null，表示取不到有效值。
        :type ModifiedTime: str
        :param IsPartition: 是否为分区字段
注意：此字段可能返回 null，表示取不到有效值。
        :type IsPartition: bool
        """
        self.Name = None
        self.Type = None
        self.Comment = None
        self.Precision = None
        self.Scale = None
        self.Nullable = None
        self.Position = None
        self.CreateTime = None
        self.ModifiedTime = None
        self.IsPartition = None


    def _deserialize(self, params):
        self.Name = params.get("Name")
        self.Type = params.get("Type")
        self.Comment = params.get("Comment")
        self.Precision = params.get("Precision")
        self.Scale = params.get("Scale")
        self.Nullable = params.get("Nullable")
        self.Position = params.get("Position")
        self.CreateTime = params.get("CreateTime")
        self.ModifiedTime = params.get("ModifiedTime")
        self.IsPartition = params.get("IsPartition")
        memeber_set = set(params.keys())
        for name, value in vars(self).items():
            if name in memeber_set:
                memeber_set.remove(name)
        if len(memeber_set) > 0:
            warnings.warn("%s fileds are useless." % ",".join(memeber_set))
        


class CommonMetrics(AbstractModel):
    """任务公共指标

    """

    def __init__(self):
        r"""
        :param CreateTaskTime: 创建任务时长，单位：ms
注意：此字段可能返回 null，表示取不到有效值。
        :type CreateTaskTime: float
        :param ProcessTime: 预处理总时长，单位：ms
注意：此字段可能返回 null，表示取不到有效值。
        :type ProcessTime: float
        :param QueueTime: 排队时长，单位：ms
注意：此字段可能返回 null，表示取不到有效值。
        :type QueueTime: float
        :param ExecutionTime: 执行时长，单位：ms
注意：此字段可能返回 null，表示取不到有效值。
        :type ExecutionTime: float
        :param IsResultCacheHit: 是否命中结果缓存
注意：此字段可能返回 null，表示取不到有效值。
        :type IsResultCacheHit: bool
        :param MatchedMVBytes: 匹配物化视图数据量
注意：此字段可能返回 null，表示取不到有效值。
        :type MatchedMVBytes: int
        :param MatchedMVs: 匹配物化视图列表
注意：此字段可能返回 null，表示取不到有效值。
        :type MatchedMVs: str
        :param AffectedBytes: 结果数据量，单位：byte
注意：此字段可能返回 null，表示取不到有效值。
        :type AffectedBytes: str
        :param AffectedRows: 	结果行数
注意：此字段可能返回 null，表示取不到有效值。
        :type AffectedRows: int
        :param ProcessedBytes: 扫描数据量，单位：byte
注意：此字段可能返回 null，表示取不到有效值。
        :type ProcessedBytes: int
        :param ProcessedRows: 	扫描行数
注意：此字段可能返回 null，表示取不到有效值。
        :type ProcessedRows: int
        """
        self.CreateTaskTime = None
        self.ProcessTime = None
        self.QueueTime = None
        self.ExecutionTime = None
        self.IsResultCacheHit = None
        self.MatchedMVBytes = None
        self.MatchedMVs = None
        self.AffectedBytes = None
        self.AffectedRows = None
        self.ProcessedBytes = None
        self.ProcessedRows = None


    def _deserialize(self, params):
        self.CreateTaskTime = params.get("CreateTaskTime")
        self.ProcessTime = params.get("ProcessTime")
        self.QueueTime = params.get("QueueTime")
        self.ExecutionTime = params.get("ExecutionTime")
        self.IsResultCacheHit = params.get("IsResultCacheHit")
        self.MatchedMVBytes = params.get("MatchedMVBytes")
        self.MatchedMVs = params.get("MatchedMVs")
        self.AffectedBytes = params.get("AffectedBytes")
        self.AffectedRows = params.get("AffectedRows")
        self.ProcessedBytes = params.get("ProcessedBytes")
        self.ProcessedRows = params.get("ProcessedRows")
        memeber_set = set(params.keys())
        for name, value in vars(self).items():
            if name in memeber_set:
                memeber_set.remove(name)
        if len(memeber_set) > 0:
            warnings.warn("%s fileds are useless." % ",".join(memeber_set))
        


class ComputerResource(AbstractModel):
    """计算资源配置。

    """

    def __init__(self):
        r"""
        :param Resource: 计算资源
        :type Resource: str
        :param Engine: 计算引擎
        :type Engine: str
        :param Config: 计算配置
注意：此字段可能返回 null，表示取不到有效值。
        :type Config: list of Config
        :param ChildImageVersionId: 集群小版本ID
注意：此字段可能返回 null，表示取不到有效值。
        :type ChildImageVersionId: str
        :param ImageVersionName: 集群大版本名称
注意：此字段可能返回 null，表示取不到有效值。
        :type ImageVersionName: str
        """
        self.Resource = None
        self.Engine = None
        self.Config = None
        self.ChildImageVersionId = None
        self.ImageVersionName = None


    def _deserialize(self, params):
        self.Resource = params.get("Resource")
        self.Engine = params.get("Engine")
        if params.get("Config") is not None:
            self.Config = []
            for item in params.get("Config"):
                obj = Config()
                obj._deserialize(item)
                self.Config.append(obj)
        self.ChildImageVersionId = params.get("ChildImageVersionId")
        self.ImageVersionName = params.get("ImageVersionName")
        memeber_set = set(params.keys())
        for name, value in vars(self).items():
            if name in memeber_set:
                memeber_set.remove(name)
        if len(memeber_set) > 0:
            warnings.warn("%s fileds are useless." % ",".join(memeber_set))
        


class Config(AbstractModel):
    """配置参数，KEY-VALUE。

    """

    def __init__(self):
        r"""
        :param Key: 参数KEY
        :type Key: str
        :param Value: 参数VALUE
        :type Value: str
        """
        self.Key = None
        self.Value = None


    def _deserialize(self, params):
        self.Key = params.get("Key")
        self.Value = params.get("Value")
        memeber_set = set(params.keys())
        for name, value in vars(self).items():
            if name in memeber_set:
                memeber_set.remove(name)
        if len(memeber_set) > 0:
            warnings.warn("%s fileds are useless." % ",".join(memeber_set))
        


class CosObject(AbstractModel):
    """对象详情

    """

    def __init__(self):
        r"""
        :param Bucket: 桶
        :type Bucket: str
        :param Key: 目录
        :type Key: str
        :param Region: 地域
        :type Region: str
        """
        self.Bucket = None
        self.Key = None
        self.Region = None


    def _deserialize(self, params):
        self.Bucket = params.get("Bucket")
        self.Key = params.get("Key")
        self.Region = params.get("Region")
        memeber_set = set(params.keys())
        for name, value in vars(self).items():
            if name in memeber_set:
                memeber_set.remove(name)
        if len(memeber_set) > 0:
            warnings.warn("%s fileds are useless." % ",".join(memeber_set))
        


class CreateAdministratorRequest(AbstractModel):
    """CreateAdministrator请求参数结构体

    """


class CreateAdministratorResponse(AbstractModel):
    """CreateAdministrator返回参数结构体

    """

    def __init__(self):
        r"""
        :param RequestId: 唯一请求 ID，每次请求都会返回。定位问题时需要提供该次请求的 RequestId。
        :type RequestId: str
        """
        self.RequestId = None


    def _deserialize(self, params):
        self.RequestId = params.get("RequestId")


class CreateCHDFSBindingProductRequest(AbstractModel):
    """CreateCHDFSBindingProduct请求参数结构体

    """

    def __init__(self):
        r"""
        :param MountPoint: 需要绑定的元数据加速桶名
        :type MountPoint: str
        :param BucketType: 桶的类型，分为cos和lakefs
        :type BucketType: str
        :param ProductName: 产品名称
        :type ProductName: str
        :param EngineName: 引擎名称，ProductName选择DLC产品时，必传此参数。其他产品可不传
        :type EngineName: str
        :param VpcInfo: vpc信息，产品名称为other时必传此参数
        :type VpcInfo: list of VpcInfo
        """
        self.MountPoint = None
        self.BucketType = None
        self.ProductName = None
        self.EngineName = None
        self.VpcInfo = None


    def _deserialize(self, params):
        self.MountPoint = params.get("MountPoint")
        self.BucketType = params.get("BucketType")
        self.ProductName = params.get("ProductName")
        self.EngineName = params.get("EngineName")
        if params.get("VpcInfo") is not None:
            self.VpcInfo = []
            for item in params.get("VpcInfo"):
                obj = VpcInfo()
                obj._deserialize(item)
                self.VpcInfo.append(obj)
        memeber_set = set(params.keys())
        for name, value in vars(self).items():
            if name in memeber_set:
                memeber_set.remove(name)
        if len(memeber_set) > 0:
            warnings.warn("%s fileds are useless." % ",".join(memeber_set))
        


class CreateCHDFSBindingProductResponse(AbstractModel):
    """CreateCHDFSBindingProduct返回参数结构体

    """

    def __init__(self):
        r"""
        :param RequestId: 唯一请求 ID，每次请求都会返回。定位问题时需要提供该次请求的 RequestId。
        :type RequestId: str
        """
        self.RequestId = None


    def _deserialize(self, params):
        self.RequestId = params.get("RequestId")


class CreateCHDFSProductRequest(AbstractModel):
    """CreateCHDFSProduct请求参数结构体

    """

    def __init__(self):
        r"""
        :param ProductName: 产品名称
        :type ProductName: str
        :param SuperUser: 超级用户名称数组
        :type SuperUser: list of str
        :param VpcInfo: vpc配置信息数组
        :type VpcInfo: list of CHDFSProductVpcInfo
        """
        self.ProductName = None
        self.SuperUser = None
        self.VpcInfo = None


    def _deserialize(self, params):
        self.ProductName = params.get("ProductName")
        self.SuperUser = params.get("SuperUser")
        if params.get("VpcInfo") is not None:
            self.VpcInfo = []
            for item in params.get("VpcInfo"):
                obj = CHDFSProductVpcInfo()
                obj._deserialize(item)
                self.VpcInfo.append(obj)
        memeber_set = set(params.keys())
        for name, value in vars(self).items():
            if name in memeber_set:
                memeber_set.remove(name)
        if len(memeber_set) > 0:
            warnings.warn("%s fileds are useless." % ",".join(memeber_set))
        


class CreateCHDFSProductResponse(AbstractModel):
    """CreateCHDFSProduct返回参数结构体

    """

    def __init__(self):
        r"""
        :param RequestId: 唯一请求 ID，每次请求都会返回。定位问题时需要提供该次请求的 RequestId。
        :type RequestId: str
        """
        self.RequestId = None


    def _deserialize(self, params):
        self.RequestId = params.get("RequestId")


class CreateDMSDatabaseRequest(AbstractModel):
    """CreateDMSDatabase请求参数结构体

    """

    def __init__(self):
        r"""
        :param Asset: 基础元数据对象
        :type Asset: :class:`tencentcloud.dlc.v20210125.models.Asset`
        :param SchemaName: Schema目录
        :type SchemaName: str
        :param Location: Db存储路径
        :type Location: str
        :param Name: 数据库名称
        :type Name: str
        """
        self.Asset = None
        self.SchemaName = None
        self.Location = None
        self.Name = None


    def _deserialize(self, params):
        if params.get("Asset") is not None:
            self.Asset = Asset()
            self.Asset._deserialize(params.get("Asset"))
        self.SchemaName = params.get("SchemaName")
        self.Location = params.get("Location")
        self.Name = params.get("Name")
        memeber_set = set(params.keys())
        for name, value in vars(self).items():
            if name in memeber_set:
                memeber_set.remove(name)
        if len(memeber_set) > 0:
            warnings.warn("%s fileds are useless." % ",".join(memeber_set))
        


class CreateDMSDatabaseResponse(AbstractModel):
    """CreateDMSDatabase返回参数结构体

    """

    def __init__(self):
        r"""
        :param RequestId: 唯一请求 ID，每次请求都会返回。定位问题时需要提供该次请求的 RequestId。
        :type RequestId: str
        """
        self.RequestId = None


    def _deserialize(self, params):
        self.RequestId = params.get("RequestId")


class CreateDMSTableRequest(AbstractModel):
    """CreateDMSTable请求参数结构体

    """

    def __init__(self):
        r"""
        :param Asset: 基础对象
        :type Asset: :class:`tencentcloud.dlc.v20210125.models.Asset`
        :param Type: 表类型
        :type Type: str
        :param DbName: 数据库名称
        :type DbName: str
        :param StorageSize: 存储大小
        :type StorageSize: int
        :param RecordCount: 记录数量
        :type RecordCount: int
        :param LifeTime: 生命周期
        :type LifeTime: int
        :param DataUpdateTime: 数据更新时间
        :type DataUpdateTime: str
        :param StructUpdateTime: 结构更新时间
        :type StructUpdateTime: str
        :param LastAccessTime: 最后访问时间
        :type LastAccessTime: str
        :param Sds: 存储对象
        :type Sds: :class:`tencentcloud.dlc.v20210125.models.DMSSds`
        :param Columns: 列
        :type Columns: list of DMSColumn
        :param PartitionKeys: 分区键值
        :type PartitionKeys: list of DMSColumn
        :param ViewOriginalText: 视图文本
        :type ViewOriginalText: str
        :param ViewExpandedText: 视图文本
        :type ViewExpandedText: str
        :param Partitions: 分区
        :type Partitions: list of DMSPartition
        :param Name: 表名称
        :type Name: str
        """
        self.Asset = None
        self.Type = None
        self.DbName = None
        self.StorageSize = None
        self.RecordCount = None
        self.LifeTime = None
        self.DataUpdateTime = None
        self.StructUpdateTime = None
        self.LastAccessTime = None
        self.Sds = None
        self.Columns = None
        self.PartitionKeys = None
        self.ViewOriginalText = None
        self.ViewExpandedText = None
        self.Partitions = None
        self.Name = None


    def _deserialize(self, params):
        if params.get("Asset") is not None:
            self.Asset = Asset()
            self.Asset._deserialize(params.get("Asset"))
        self.Type = params.get("Type")
        self.DbName = params.get("DbName")
        self.StorageSize = params.get("StorageSize")
        self.RecordCount = params.get("RecordCount")
        self.LifeTime = params.get("LifeTime")
        self.DataUpdateTime = params.get("DataUpdateTime")
        self.StructUpdateTime = params.get("StructUpdateTime")
        self.LastAccessTime = params.get("LastAccessTime")
        if params.get("Sds") is not None:
            self.Sds = DMSSds()
            self.Sds._deserialize(params.get("Sds"))
        if params.get("Columns") is not None:
            self.Columns = []
            for item in params.get("Columns"):
                obj = DMSColumn()
                obj._deserialize(item)
                self.Columns.append(obj)
        if params.get("PartitionKeys") is not None:
            self.PartitionKeys = []
            for item in params.get("PartitionKeys"):
                obj = DMSColumn()
                obj._deserialize(item)
                self.PartitionKeys.append(obj)
        self.ViewOriginalText = params.get("ViewOriginalText")
        self.ViewExpandedText = params.get("ViewExpandedText")
        if params.get("Partitions") is not None:
            self.Partitions = []
            for item in params.get("Partitions"):
                obj = DMSPartition()
                obj._deserialize(item)
                self.Partitions.append(obj)
        self.Name = params.get("Name")
        memeber_set = set(params.keys())
        for name, value in vars(self).items():
            if name in memeber_set:
                memeber_set.remove(name)
        if len(memeber_set) > 0:
            warnings.warn("%s fileds are useless." % ",".join(memeber_set))
        


class CreateDMSTableResponse(AbstractModel):
    """CreateDMSTable返回参数结构体

    """

    def __init__(self):
        r"""
        :param RequestId: 唯一请求 ID，每次请求都会返回。定位问题时需要提供该次请求的 RequestId。
        :type RequestId: str
        """
        self.RequestId = None


    def _deserialize(self, params):
        self.RequestId = params.get("RequestId")


class CreateDataEngineRequest(AbstractModel):
    """CreateDataEngine请求参数结构体

    """

    def __init__(self):
        r"""
        :param EngineType: 引擎类型spark/presto
        :type EngineType: str
        :param DataEngineName: 虚拟集群名称
        :type DataEngineName: str
        :param ClusterType: 集群类型 spark_private/presto_private/presto_cu/spark_cu
        :type ClusterType: str
        :param Mode: 计费模式 0=共享模式 1=按量计费 2=包年包月
        :type Mode: int
        :param AutoResume: 是否自动启动集群
        :type AutoResume: bool
        :param MinClusters: 最小资源
        :type MinClusters: int
        :param MaxClusters: 最大资源
        :type MaxClusters: int
        :param DefaultDataEngine: 是否为默虚拟集群
        :type DefaultDataEngine: bool
        :param CidrBlock: VPC网段
        :type CidrBlock: str
        :param Message: 描述信息
        :type Message: str
        :param Size: 集群规模
        :type Size: int
        :param PayMode: 计费类型，后付费：0，预付费：1。当前只支持后付费，不填默认为后付费。
        :type PayMode: int
        :param TimeSpan: 资源使用时长，后付费：固定填3600，预付费：最少填1，代表购买资源一个月，最长不超过120。默认3600
        :type TimeSpan: int
        :param TimeUnit: 资源使用时长的单位，后付费：s，预付费：m。默认为s
        :type TimeUnit: str
        :param AutoRenew: 资源的自动续费标志。后付费无需续费，固定填0；预付费下：0表示手动续费、1代表自动续费、2代表不续费，在0下如果是大客户，会自动帮大客户续费。默认为0
        :type AutoRenew: int
        :param Tags: 创建资源的时候需要绑定的标签信息
        :type Tags: list of TagInfo
        :param AutoSuspend: 是否自定挂起集群：false（默认）：不自动挂起、true：自动挂起
        :type AutoSuspend: bool
        :param CrontabResumeSuspend: 定时启停集群策略：0（默认）：关闭定时策略、1：开启定时策略（注：定时启停策略与自动挂起策略互斥）
        :type CrontabResumeSuspend: int
        :param CrontabResumeSuspendStrategy: 定时启停策略，复杂类型：包含启停时间、挂起集群策略
        :type CrontabResumeSuspendStrategy: :class:`tencentcloud.dlc.v20210125.models.CrontabResumeSuspendStrategy`
        :param EngineExecType: 引擎执行任务类型，有效值：SQL/BATCH，默认为SQL
        :type EngineExecType: str
        :param MaxConcurrency: 单个集群最大并发任务数，默认5
        :type MaxConcurrency: int
        :param TolerableQueueTime: 可容忍的排队时间，默认0。当任务排队的时间超过可容忍的时间时可能会触发扩容。如果该参数为0，则表示一旦有任务排队就可能立即触发扩容。
        :type TolerableQueueTime: int
        :param AutoSuspendTime: 集群自动挂起时间，默认10分钟
        :type AutoSuspendTime: int
        :param ResourceType: 资源类型。Standard_CU：标准型；Memory_CU：内存型
        :type ResourceType: str
        :param DataEngineConfigPairs: 集群高级配置
        :type DataEngineConfigPairs: list of DataEngineConfigPair
        :param ImageVersionName: 集群镜像版本名字。如SuperSQL-P 1.1;SuperSQL-S 3.2等,不传，默认创建最新镜像版本的集群
        :type ImageVersionName: str
        :param MainClusterName: 主集群名称
        :type MainClusterName: str
        :param ElasticSwitch: spark jar 包年包月集群是否开启弹性
        :type ElasticSwitch: bool
        :param ElasticLimit: spark jar 包年包月集群弹性上限
        :type ElasticLimit: int
        :param EmrLivyInfo: spark on emr-livy类型集群所需参数，包含emr集群和livy服务的信息
        :type EmrLivyInfo: str
        :param SessionResourceTemplate: spark作业集群session资源配置模板
        :type SessionResourceTemplate: :class:`tencentcloud.dlc.v20210125.models.SessionResourceTemplate`
        """
        self.EngineType = None
        self.DataEngineName = None
        self.ClusterType = None
        self.Mode = None
        self.AutoResume = None
        self.MinClusters = None
        self.MaxClusters = None
        self.DefaultDataEngine = None
        self.CidrBlock = None
        self.Message = None
        self.Size = None
        self.PayMode = None
        self.TimeSpan = None
        self.TimeUnit = None
        self.AutoRenew = None
        self.Tags = None
        self.AutoSuspend = None
        self.CrontabResumeSuspend = None
        self.CrontabResumeSuspendStrategy = None
        self.EngineExecType = None
        self.MaxConcurrency = None
        self.TolerableQueueTime = None
        self.AutoSuspendTime = None
        self.ResourceType = None
        self.DataEngineConfigPairs = None
        self.ImageVersionName = None
        self.MainClusterName = None
        self.ElasticSwitch = None
        self.ElasticLimit = None
        self.EmrLivyInfo = None
        self.SessionResourceTemplate = None


    def _deserialize(self, params):
        self.EngineType = params.get("EngineType")
        self.DataEngineName = params.get("DataEngineName")
        self.ClusterType = params.get("ClusterType")
        self.Mode = params.get("Mode")
        self.AutoResume = params.get("AutoResume")
        self.MinClusters = params.get("MinClusters")
        self.MaxClusters = params.get("MaxClusters")
        self.DefaultDataEngine = params.get("DefaultDataEngine")
        self.CidrBlock = params.get("CidrBlock")
        self.Message = params.get("Message")
        self.Size = params.get("Size")
        self.PayMode = params.get("PayMode")
        self.TimeSpan = params.get("TimeSpan")
        self.TimeUnit = params.get("TimeUnit")
        self.AutoRenew = params.get("AutoRenew")
        if params.get("Tags") is not None:
            self.Tags = []
            for item in params.get("Tags"):
                obj = TagInfo()
                obj._deserialize(item)
                self.Tags.append(obj)
        self.AutoSuspend = params.get("AutoSuspend")
        self.CrontabResumeSuspend = params.get("CrontabResumeSuspend")
        if params.get("CrontabResumeSuspendStrategy") is not None:
            self.CrontabResumeSuspendStrategy = CrontabResumeSuspendStrategy()
            self.CrontabResumeSuspendStrategy._deserialize(params.get("CrontabResumeSuspendStrategy"))
        self.EngineExecType = params.get("EngineExecType")
        self.MaxConcurrency = params.get("MaxConcurrency")
        self.TolerableQueueTime = params.get("TolerableQueueTime")
        self.AutoSuspendTime = params.get("AutoSuspendTime")
        self.ResourceType = params.get("ResourceType")
        if params.get("DataEngineConfigPairs") is not None:
            self.DataEngineConfigPairs = []
            for item in params.get("DataEngineConfigPairs"):
                obj = DataEngineConfigPair()
                obj._deserialize(item)
                self.DataEngineConfigPairs.append(obj)
        self.ImageVersionName = params.get("ImageVersionName")
        self.MainClusterName = params.get("MainClusterName")
        self.ElasticSwitch = params.get("ElasticSwitch")
        self.ElasticLimit = params.get("ElasticLimit")
        self.EmrLivyInfo = params.get("EmrLivyInfo")
        if params.get("SessionResourceTemplate") is not None:
            self.SessionResourceTemplate = SessionResourceTemplate()
            self.SessionResourceTemplate._deserialize(params.get("SessionResourceTemplate"))
        memeber_set = set(params.keys())
        for name, value in vars(self).items():
            if name in memeber_set:
                memeber_set.remove(name)
        if len(memeber_set) > 0:
            warnings.warn("%s fileds are useless." % ",".join(memeber_set))
        


class CreateDataEngineResponse(AbstractModel):
    """CreateDataEngine返回参数结构体

    """

    def __init__(self):
        r"""
        :param DataEngineId: 虚拟引擎id
        :type DataEngineId: str
        :param RequestId: 唯一请求 ID，每次请求都会返回。定位问题时需要提供该次请求的 RequestId。
        :type RequestId: str
        """
        self.DataEngineId = None
        self.RequestId = None


    def _deserialize(self, params):
        self.DataEngineId = params.get("DataEngineId")
        self.RequestId = params.get("RequestId")


class CreateDataQueryRequest(AbstractModel):
    """CreateDataQuery请求参数结构体

    """

    def __init__(self):
        r"""
        :param Name: 创建的数据查询名称
        :type Name: str
        :param Dir: 创建的数据查询所归属的目录名称
        :type Dir: str
        :param Statement: base64编码后的sql语句
        :type Statement: str
        :param Params: base64编码后的参数列表
        :type Params: str
        """
        self.Name = None
        self.Dir = None
        self.Statement = None
        self.Params = None


    def _deserialize(self, params):
        self.Name = params.get("Name")
        self.Dir = params.get("Dir")
        self.Statement = params.get("Statement")
        self.Params = params.get("Params")
        memeber_set = set(params.keys())
        for name, value in vars(self).items():
            if name in memeber_set:
                memeber_set.remove(name)
        if len(memeber_set) > 0:
            warnings.warn("%s fileds are useless." % ",".join(memeber_set))
        


class CreateDataQueryResponse(AbstractModel):
    """CreateDataQuery返回参数结构体

    """

    def __init__(self):
        r"""
        :param RequestId: 唯一请求 ID，每次请求都会返回。定位问题时需要提供该次请求的 RequestId。
        :type RequestId: str
        """
        self.RequestId = None


    def _deserialize(self, params):
        self.RequestId = params.get("RequestId")


class CreateDatabaseRequest(AbstractModel):
    """CreateDatabase请求参数结构体

    """

    def __init__(self):
        r"""
        :param DatabaseInfo: 数据库基础信息
        :type DatabaseInfo: :class:`tencentcloud.dlc.v20210125.models.DatabaseInfo`
        :param DatasourceConnectionName: 数据源名称，默认为DataLakeCatalog
        :type DatasourceConnectionName: str
        """
        self.DatabaseInfo = None
        self.DatasourceConnectionName = None


    def _deserialize(self, params):
        if params.get("DatabaseInfo") is not None:
            self.DatabaseInfo = DatabaseInfo()
            self.DatabaseInfo._deserialize(params.get("DatabaseInfo"))
        self.DatasourceConnectionName = params.get("DatasourceConnectionName")
        memeber_set = set(params.keys())
        for name, value in vars(self).items():
            if name in memeber_set:
                memeber_set.remove(name)
        if len(memeber_set) > 0:
            warnings.warn("%s fileds are useless." % ",".join(memeber_set))
        


class CreateDatabaseResponse(AbstractModel):
    """CreateDatabase返回参数结构体

    """

    def __init__(self):
        r"""
        :param Execution: 生成的建库执行语句对象。
        :type Execution: :class:`tencentcloud.dlc.v20210125.models.Execution`
        :param RequestId: 唯一请求 ID，每次请求都会返回。定位问题时需要提供该次请求的 RequestId。
        :type RequestId: str
        """
        self.Execution = None
        self.RequestId = None


    def _deserialize(self, params):
        if params.get("Execution") is not None:
            self.Execution = Execution()
            self.Execution._deserialize(params.get("Execution"))
        self.RequestId = params.get("RequestId")


class CreateDatasourceConnectionRequest(AbstractModel):
    """CreateDatasourceConnection请求参数结构体

    """

    def __init__(self):
        r"""
        :param DatasourceConnectionName: 数据连接名称
        :type DatasourceConnectionName: str
        :param DatasourceConnectionType: 数据连接类型
        :type DatasourceConnectionType: str
        :param DatasourceConnectionConfig: 数据连接属性
        :type DatasourceConnectionConfig: :class:`tencentcloud.dlc.v20210125.models.DatasourceConnectionConfig`
        :param ServiceType: 数据连接所属服务
        :type ServiceType: str
        :param DatasourceConnectionDesc: 数据连接描述
        :type DatasourceConnectionDesc: str
        :param DataEngineNames: 数据引擎名称数组
        :type DataEngineNames: list of str
        :param NetworkConnectionName: 网络连接名称
        :type NetworkConnectionName: str
        :param NetworkConnectionDesc: 网络连接描述
        :type NetworkConnectionDesc: str
        :param NetworkConnectionType: 网络连接类型 （2-夸源型，4-增强型）
        :type NetworkConnectionType: int
        """
        self.DatasourceConnectionName = None
        self.DatasourceConnectionType = None
        self.DatasourceConnectionConfig = None
        self.ServiceType = None
        self.DatasourceConnectionDesc = None
        self.DataEngineNames = None
        self.NetworkConnectionName = None
        self.NetworkConnectionDesc = None
        self.NetworkConnectionType = None


    def _deserialize(self, params):
        self.DatasourceConnectionName = params.get("DatasourceConnectionName")
        self.DatasourceConnectionType = params.get("DatasourceConnectionType")
        if params.get("DatasourceConnectionConfig") is not None:
            self.DatasourceConnectionConfig = DatasourceConnectionConfig()
            self.DatasourceConnectionConfig._deserialize(params.get("DatasourceConnectionConfig"))
        self.ServiceType = params.get("ServiceType")
        self.DatasourceConnectionDesc = params.get("DatasourceConnectionDesc")
        self.DataEngineNames = params.get("DataEngineNames")
        self.NetworkConnectionName = params.get("NetworkConnectionName")
        self.NetworkConnectionDesc = params.get("NetworkConnectionDesc")
        self.NetworkConnectionType = params.get("NetworkConnectionType")
        memeber_set = set(params.keys())
        for name, value in vars(self).items():
            if name in memeber_set:
                memeber_set.remove(name)
        if len(memeber_set) > 0:
            warnings.warn("%s fileds are useless." % ",".join(memeber_set))
        


class CreateDatasourceConnectionResponse(AbstractModel):
    """CreateDatasourceConnection返回参数结构体

    """

    def __init__(self):
        r"""
        :param DatasourceConnectionId: 数据连接Id
        :type DatasourceConnectionId: str
        :param RequestId: 唯一请求 ID，每次请求都会返回。定位问题时需要提供该次请求的 RequestId。
        :type RequestId: str
        """
        self.DatasourceConnectionId = None
        self.RequestId = None


    def _deserialize(self, params):
        self.DatasourceConnectionId = params.get("DatasourceConnectionId")
        self.RequestId = params.get("RequestId")


class CreateDefaultDatasourceConnectionRequest(AbstractModel):
    """CreateDefaultDatasourceConnection请求参数结构体

    """


class CreateDefaultDatasourceConnectionResponse(AbstractModel):
    """CreateDefaultDatasourceConnection返回参数结构体

    """

    def __init__(self):
        r"""
        :param RequestId: 唯一请求 ID，每次请求都会返回。定位问题时需要提供该次请求的 RequestId。
        :type RequestId: str
        """
        self.RequestId = None


    def _deserialize(self, params):
        self.RequestId = params.get("RequestId")


class CreateExportResultTaskRequest(AbstractModel):
    """CreateExportResultTask请求参数结构体

    """

    def __init__(self):
        r"""
        :param DataPath: SQL查询结果存放的路径，目前只支持托管的查询结果导出，即Path是lakefs协议的路径
        :type DataPath: str
        :param Target: 目标桶信息，包括桶名、区域、Key
        :type Target: :class:`tencentcloud.dlc.v20210125.models.CosObject`
        :param SessionId: SQL查询窗口ID
        :type SessionId: str
        """
        self.DataPath = None
        self.Target = None
        self.SessionId = None


    def _deserialize(self, params):
        self.DataPath = params.get("DataPath")
        if params.get("Target") is not None:
            self.Target = CosObject()
            self.Target._deserialize(params.get("Target"))
        self.SessionId = params.get("SessionId")
        memeber_set = set(params.keys())
        for name, value in vars(self).items():
            if name in memeber_set:
                memeber_set.remove(name)
        if len(memeber_set) > 0:
            warnings.warn("%s fileds are useless." % ",".join(memeber_set))
        


class CreateExportResultTaskResponse(AbstractModel):
    """CreateExportResultTask返回参数结构体

    """

    def __init__(self):
        r"""
        :param TaskId: 任务ID
        :type TaskId: str
        :param RequestId: 唯一请求 ID，每次请求都会返回。定位问题时需要提供该次请求的 RequestId。
        :type RequestId: str
        """
        self.TaskId = None
        self.RequestId = None


    def _deserialize(self, params):
        self.TaskId = params.get("TaskId")
        self.RequestId = params.get("RequestId")


class CreateExportTaskRequest(AbstractModel):
    """CreateExportTask请求参数结构体

    """

    def __init__(self):
        r"""
        :param InputType: 数据来源，lakefsStorage、taskResult
        :type InputType: str
        :param InputConf: 导出任务输入配置
        :type InputConf: list of KVPair
        :param OutputConf: 导出任务输出配置
        :type OutputConf: list of KVPair
        :param OutputType: 目标数据源的类型，目前支持导出到cos
        :type OutputType: str
        """
        self.InputType = None
        self.InputConf = None
        self.OutputConf = None
        self.OutputType = None


    def _deserialize(self, params):
        self.InputType = params.get("InputType")
        if params.get("InputConf") is not None:
            self.InputConf = []
            for item in params.get("InputConf"):
                obj = KVPair()
                obj._deserialize(item)
                self.InputConf.append(obj)
        if params.get("OutputConf") is not None:
            self.OutputConf = []
            for item in params.get("OutputConf"):
                obj = KVPair()
                obj._deserialize(item)
                self.OutputConf.append(obj)
        self.OutputType = params.get("OutputType")
        memeber_set = set(params.keys())
        for name, value in vars(self).items():
            if name in memeber_set:
                memeber_set.remove(name)
        if len(memeber_set) > 0:
            warnings.warn("%s fileds are useless." % ",".join(memeber_set))
        


class CreateExportTaskResponse(AbstractModel):
    """CreateExportTask返回参数结构体

    """

    def __init__(self):
        r"""
        :param TaskId: 任务id
        :type TaskId: str
        :param RequestId: 唯一请求 ID，每次请求都会返回。定位问题时需要提供该次请求的 RequestId。
        :type RequestId: str
        """
        self.TaskId = None
        self.RequestId = None


    def _deserialize(self, params):
        self.TaskId = params.get("TaskId")
        self.RequestId = params.get("RequestId")


class CreateHouseRequest(AbstractModel):
    """CreateHouse请求参数结构体

    """

    def __init__(self):
        r"""
        :param EngineType: 引擎类型spark/presto
        :type EngineType: str
        :param HouseName: 虚拟集群名称
        :type HouseName: str
        :param ClusterType: 集群类型 spark_private/presto_private/presto_cu/spark_cu
        :type ClusterType: str
        :param Mode: 计费模式 0=共享模式 1=按量计费 2=包年包月
        :type Mode: int
        :param AutoResume: 是否自动启动集群
        :type AutoResume: bool
        :param MinClusters: 最小资源
        :type MinClusters: int
        :param MaxClusters: 最大资源
        :type MaxClusters: int
        :param DefaultHouse: 是否为默虚拟集群
        :type DefaultHouse: bool
        :param CidrBlock: VPC网段
        :type CidrBlock: str
        :param Message: 描述信息
        :type Message: str
        :param Size: 集群规模
        :type Size: int
        :param PayMode: 计费类型，后付费：0，预付费：1。当前只支持后付费，不填默认为后付费。
        :type PayMode: int
        :param TimeSpan: 资源使用时长，后付费：固定填3600，预付费：最少填1，代表购买资源一个月，最长不超过120。默认3600
        :type TimeSpan: int
        :param TimeUnit: 资源使用时长的单位，后付费：s，预付费：m。默认为s
        :type TimeUnit: str
        :param AutoRenew: 资源的自动续费标志。后付费无需续费，固定填0；预付费下：0表示手动续费、1代表自动续费、2代表不续费，在0下如果是大客户，会自动帮大客户续费。默认为0
        :type AutoRenew: int
        """
        self.EngineType = None
        self.HouseName = None
        self.ClusterType = None
        self.Mode = None
        self.AutoResume = None
        self.MinClusters = None
        self.MaxClusters = None
        self.DefaultHouse = None
        self.CidrBlock = None
        self.Message = None
        self.Size = None
        self.PayMode = None
        self.TimeSpan = None
        self.TimeUnit = None
        self.AutoRenew = None


    def _deserialize(self, params):
        self.EngineType = params.get("EngineType")
        self.HouseName = params.get("HouseName")
        self.ClusterType = params.get("ClusterType")
        self.Mode = params.get("Mode")
        self.AutoResume = params.get("AutoResume")
        self.MinClusters = params.get("MinClusters")
        self.MaxClusters = params.get("MaxClusters")
        self.DefaultHouse = params.get("DefaultHouse")
        self.CidrBlock = params.get("CidrBlock")
        self.Message = params.get("Message")
        self.Size = params.get("Size")
        self.PayMode = params.get("PayMode")
        self.TimeSpan = params.get("TimeSpan")
        self.TimeUnit = params.get("TimeUnit")
        self.AutoRenew = params.get("AutoRenew")
        memeber_set = set(params.keys())
        for name, value in vars(self).items():
            if name in memeber_set:
                memeber_set.remove(name)
        if len(memeber_set) > 0:
            warnings.warn("%s fileds are useless." % ",".join(memeber_set))
        


class CreateHouseResponse(AbstractModel):
    """CreateHouse返回参数结构体

    """

    def __init__(self):
        r"""
        :param HouseId: 队列id
        :type HouseId: str
        :param RequestId: 唯一请求 ID，每次请求都会返回。定位问题时需要提供该次请求的 RequestId。
        :type RequestId: str
        """
        self.HouseId = None
        self.RequestId = None


    def _deserialize(self, params):
        self.HouseId = params.get("HouseId")
        self.RequestId = params.get("RequestId")


class CreateImportTaskRequest(AbstractModel):
    """CreateImportTask请求参数结构体

    """

    def __init__(self):
        r"""
        :param InputType: 数据来源，cos
        :type InputType: str
        :param InputConf: 输入配置
        :type InputConf: list of KVPair
        :param OutputConf: 输出配置
        :type OutputConf: list of KVPair
        :param OutputType: 目标数据源的类型，目前支持导入到托管存储，即lakefsStorage
        :type OutputType: str
        """
        self.InputType = None
        self.InputConf = None
        self.OutputConf = None
        self.OutputType = None


    def _deserialize(self, params):
        self.InputType = params.get("InputType")
        if params.get("InputConf") is not None:
            self.InputConf = []
            for item in params.get("InputConf"):
                obj = KVPair()
                obj._deserialize(item)
                self.InputConf.append(obj)
        if params.get("OutputConf") is not None:
            self.OutputConf = []
            for item in params.get("OutputConf"):
                obj = KVPair()
                obj._deserialize(item)
                self.OutputConf.append(obj)
        self.OutputType = params.get("OutputType")
        memeber_set = set(params.keys())
        for name, value in vars(self).items():
            if name in memeber_set:
                memeber_set.remove(name)
        if len(memeber_set) > 0:
            warnings.warn("%s fileds are useless." % ",".join(memeber_set))
        


class CreateImportTaskResponse(AbstractModel):
    """CreateImportTask返回参数结构体

    """

    def __init__(self):
        r"""
        :param TaskId: 任务id
        :type TaskId: str
        :param RequestId: 唯一请求 ID，每次请求都会返回。定位问题时需要提供该次请求的 RequestId。
        :type RequestId: str
        """
        self.TaskId = None
        self.RequestId = None


    def _deserialize(self, params):
        self.TaskId = params.get("TaskId")
        self.RequestId = params.get("RequestId")


class CreateInternalTableRequest(AbstractModel):
    """CreateInternalTable请求参数结构体

    """

    def __init__(self):
        r"""
        :param TableBaseInfo: 表基本信息
        :type TableBaseInfo: :class:`tencentcloud.dlc.v20210125.models.TableBaseInfo`
        :param Columns: 表字段信息
        :type Columns: list of TColumn
        :param Partitions: 表分区信息
        :type Partitions: list of TPartition
        :param Properties: 表属性信息
        :type Properties: list of Property
        """
        self.TableBaseInfo = None
        self.Columns = None
        self.Partitions = None
        self.Properties = None


    def _deserialize(self, params):
        if params.get("TableBaseInfo") is not None:
            self.TableBaseInfo = TableBaseInfo()
            self.TableBaseInfo._deserialize(params.get("TableBaseInfo"))
        if params.get("Columns") is not None:
            self.Columns = []
            for item in params.get("Columns"):
                obj = TColumn()
                obj._deserialize(item)
                self.Columns.append(obj)
        if params.get("Partitions") is not None:
            self.Partitions = []
            for item in params.get("Partitions"):
                obj = TPartition()
                obj._deserialize(item)
                self.Partitions.append(obj)
        if params.get("Properties") is not None:
            self.Properties = []
            for item in params.get("Properties"):
                obj = Property()
                obj._deserialize(item)
                self.Properties.append(obj)
        memeber_set = set(params.keys())
        for name, value in vars(self).items():
            if name in memeber_set:
                memeber_set.remove(name)
        if len(memeber_set) > 0:
            warnings.warn("%s fileds are useless." % ",".join(memeber_set))
        


class CreateInternalTableResponse(AbstractModel):
    """CreateInternalTable返回参数结构体

    """

    def __init__(self):
        r"""
        :param Execution: 创建托管存储内表sql语句描述
        :type Execution: str
        :param RequestId: 唯一请求 ID，每次请求都会返回。定位问题时需要提供该次请求的 RequestId。
        :type RequestId: str
        """
        self.Execution = None
        self.RequestId = None


    def _deserialize(self, params):
        self.Execution = params.get("Execution")
        self.RequestId = params.get("RequestId")


class CreateKyuubiTaskRequest(AbstractModel):
    """CreateKyuubiTask请求参数结构体

    """

    def __init__(self):
        r"""
        :param DataEngineName: 计算引擎名称，不填任务提交到默认集群	官
        :type DataEngineName: str
        :param DatasourceConnectionName: 数据源名称，默认为DataLakeCatalog
        :type DatasourceConnectionName: str
        :param DatabaseName: 数据库名称。如果SQL语句中有数据库名称，优先使用SQL语句中的数据库，否则使用该参数指定的数据库（注：当提交建库sql时，该字段传空字符串）。
        :type DatabaseName: str
        :param Task: SQL任务信息
        :type Task: :class:`tencentcloud.dlc.v20210125.models.Task`
        """
        self.DataEngineName = None
        self.DatasourceConnectionName = None
        self.DatabaseName = None
        self.Task = None


    def _deserialize(self, params):
        self.DataEngineName = params.get("DataEngineName")
        self.DatasourceConnectionName = params.get("DatasourceConnectionName")
        self.DatabaseName = params.get("DatabaseName")
        if params.get("Task") is not None:
            self.Task = Task()
            self.Task._deserialize(params.get("Task"))
        memeber_set = set(params.keys())
        for name, value in vars(self).items():
            if name in memeber_set:
                memeber_set.remove(name)
        if len(memeber_set) > 0:
            warnings.warn("%s fileds are useless." % ",".join(memeber_set))
        


class CreateKyuubiTaskResponse(AbstractModel):
    """CreateKyuubiTask返回参数结构体

    """

    def __init__(self):
        r"""
        :param UserAppID: 用户AppID
        :type UserAppID: int
        :param UserUin: 用户uin
        :type UserUin: str
        :param UserSubAccountUin: 用户SubAccountUin
        :type UserSubAccountUin: str
        :param TaskId: TaskId
        :type TaskId: str
        :param Vip: PrivateLink vpi
        :type Vip: str
        :param CoordinatorIp: CoordinatorIp
        :type CoordinatorIp: str
        :param DataEngineStatus: 集群状态 0-初始化 1-暂停 2-运行中
        :type DataEngineStatus: int
        :param RequestId: 唯一请求 ID，每次请求都会返回。定位问题时需要提供该次请求的 RequestId。
        :type RequestId: str
        """
        self.UserAppID = None
        self.UserUin = None
        self.UserSubAccountUin = None
        self.TaskId = None
        self.Vip = None
        self.CoordinatorIp = None
        self.DataEngineStatus = None
        self.RequestId = None


    def _deserialize(self, params):
        self.UserAppID = params.get("UserAppID")
        self.UserUin = params.get("UserUin")
        self.UserSubAccountUin = params.get("UserSubAccountUin")
        self.TaskId = params.get("TaskId")
        self.Vip = params.get("Vip")
        self.CoordinatorIp = params.get("CoordinatorIp")
        self.DataEngineStatus = params.get("DataEngineStatus")
        self.RequestId = params.get("RequestId")


class CreateLakeFsChdfsBindingRequest(AbstractModel):
    """CreateLakeFsChdfsBinding请求参数结构体

    """

    def __init__(self):
        r"""
        :param MountPoint: 挂载点
        :type MountPoint: str
        :param DataEngine: 需要绑定的引擎名
        :type DataEngine: str
        :param SupperUsers: 绑定时的超级用户列表
        :type SupperUsers: list of str
        """
        self.MountPoint = None
        self.DataEngine = None
        self.SupperUsers = None


    def _deserialize(self, params):
        self.MountPoint = params.get("MountPoint")
        self.DataEngine = params.get("DataEngine")
        self.SupperUsers = params.get("SupperUsers")
        memeber_set = set(params.keys())
        for name, value in vars(self).items():
            if name in memeber_set:
                memeber_set.remove(name)
        if len(memeber_set) > 0:
            warnings.warn("%s fileds are useless." % ",".join(memeber_set))
        


class CreateLakeFsChdfsBindingResponse(AbstractModel):
    """CreateLakeFsChdfsBinding返回参数结构体

    """

    def __init__(self):
        r"""
        :param RequestId: 唯一请求 ID，每次请求都会返回。定位问题时需要提供该次请求的 RequestId。
        :type RequestId: str
        """
        self.RequestId = None


    def _deserialize(self, params):
        self.RequestId = params.get("RequestId")


class CreateLakeFsRequest(AbstractModel):
    """CreateLakeFs请求参数结构体

    """

    def __init__(self):
        r"""
        :param Mode: 计费模式
        :type Mode: str
        :param BucketType: 桶类型，cos/chdfs
        :type BucketType: str
        """
        self.Mode = None
        self.BucketType = None


    def _deserialize(self, params):
        self.Mode = params.get("Mode")
        self.BucketType = params.get("BucketType")
        memeber_set = set(params.keys())
        for name, value in vars(self).items():
            if name in memeber_set:
                memeber_set.remove(name)
        if len(memeber_set) > 0:
            warnings.warn("%s fileds are useless." % ",".join(memeber_set))
        


class CreateLakeFsResponse(AbstractModel):
    """CreateLakeFs返回参数结构体

    """

    def __init__(self):
        r"""
        :param RequestId: 唯一请求 ID，每次请求都会返回。定位问题时需要提供该次请求的 RequestId。
        :type RequestId: str
        """
        self.RequestId = None


    def _deserialize(self, params):
        self.RequestId = params.get("RequestId")


class CreateLinkRequest(AbstractModel):
    """CreateLink请求参数结构体

    """

    def __init__(self):
        r"""
        :param Link: 任务依赖关系数据
        :type Link: :class:`tencentcloud.dlc.v20210125.models.Link`
        """
        self.Link = None


    def _deserialize(self, params):
        if params.get("Link") is not None:
            self.Link = Link()
            self.Link._deserialize(params.get("Link"))
        memeber_set = set(params.keys())
        for name, value in vars(self).items():
            if name in memeber_set:
                memeber_set.remove(name)
        if len(memeber_set) > 0:
            warnings.warn("%s fileds are useless." % ",".join(memeber_set))
        


class CreateLinkResponse(AbstractModel):
    """CreateLink返回参数结构体

    """

    def __init__(self):
        r"""
        :param LinkId: 任务依赖关系ID
        :type LinkId: str
        :param RequestId: 唯一请求 ID，每次请求都会返回。定位问题时需要提供该次请求的 RequestId。
        :type RequestId: str
        """
        self.LinkId = None
        self.RequestId = None


    def _deserialize(self, params):
        self.LinkId = params.get("LinkId")
        self.RequestId = params.get("RequestId")


class CreateMetaDatabaseRequest(AbstractModel):
    """CreateMetaDatabase请求参数结构体

    """

    def __init__(self):
        r"""
        :param DatasourceConnectionName: 数据源名称，默认DataLakeCatalog
        :type DatasourceConnectionName: str
        :param MetaDatabaseInfo: 元数据库基本信息
        :type MetaDatabaseInfo: :class:`tencentcloud.dlc.v20210125.models.MetaDatabaseInfo`
        :param GovernPolicy: 数据治理配置项
        :type GovernPolicy: :class:`tencentcloud.dlc.v20210125.models.DataGovernPolicy`
        """
        self.DatasourceConnectionName = None
        self.MetaDatabaseInfo = None
        self.GovernPolicy = None


    def _deserialize(self, params):
        self.DatasourceConnectionName = params.get("DatasourceConnectionName")
        if params.get("MetaDatabaseInfo") is not None:
            self.MetaDatabaseInfo = MetaDatabaseInfo()
            self.MetaDatabaseInfo._deserialize(params.get("MetaDatabaseInfo"))
        if params.get("GovernPolicy") is not None:
            self.GovernPolicy = DataGovernPolicy()
            self.GovernPolicy._deserialize(params.get("GovernPolicy"))
        memeber_set = set(params.keys())
        for name, value in vars(self).items():
            if name in memeber_set:
                memeber_set.remove(name)
        if len(memeber_set) > 0:
            warnings.warn("%s fileds are useless." % ",".join(memeber_set))
        


class CreateMetaDatabaseResponse(AbstractModel):
    """CreateMetaDatabase返回参数结构体

    """

    def __init__(self):
        r"""
        :param BatchId: 本批次提交的任务的批次Id
        :type BatchId: str
        :param TaskIdSet: 任务Id集合，按照执行顺序排列
        :type TaskIdSet: list of str
        :param RequestId: 唯一请求 ID，每次请求都会返回。定位问题时需要提供该次请求的 RequestId。
        :type RequestId: str
        """
        self.BatchId = None
        self.TaskIdSet = None
        self.RequestId = None


    def _deserialize(self, params):
        self.BatchId = params.get("BatchId")
        self.TaskIdSet = params.get("TaskIdSet")
        self.RequestId = params.get("RequestId")


class CreateNotebookSessionRequest(AbstractModel):
    """CreateNotebookSession请求参数结构体

    """

    def __init__(self):
        r"""
        :param Name: Session名称
        :type Name: str
        :param Kind: 类型，当前支持：spark、pyspark、sparkr、sql
        :type Kind: str
        :param DataEngineName: DLC Spark作业引擎名称
        :type DataEngineName: str
        :param ProgramDependentFiles: session文件地址，当前支持：cosn://和lakefs://两种路径
        :type ProgramDependentFiles: list of str
        :param ProgramDependentJars: 依赖的jar程序地址，当前支持：cosn://和lakefs://两种路径
        :type ProgramDependentJars: list of str
        :param ProgramDependentPython: 依赖的python程序地址，当前支持：cosn://和lakefs://两种路径
        :type ProgramDependentPython: list of str
        :param ProgramArchives: 依赖的pyspark虚拟环境地址，当前支持：cosn://和lakefs://两种路径
        :type ProgramArchives: list of str
        :param DriverSize: 指定的Driver规格，当前支持：small（默认，1cu）、medium（2cu）、large（4cu）、xlarge（8cu）
        :type DriverSize: str
        :param ExecutorSize: 指定的Executor规格，当前支持：small（默认，1cu）、medium（2cu）、large（4cu）、xlarge（8cu）
        :type ExecutorSize: str
        :param ExecutorNumbers: 指定的Executor数量，默认为1
        :type ExecutorNumbers: int
        :param Arguments: Session相关配置，当前支持：dlc.eni、dlc.role.arn、dlc.sql.set.config以及用户指定的配置，注：roleArn必填；
        :type Arguments: list of KVPair
        :param ProxyUser: 代理用户，默认为root
        :type ProxyUser: str
        :param TimeoutInSecond: 指定的Session超时时间，单位秒，默认3600秒
        :type TimeoutInSecond: int
        :param ExecutorMaxNumbers: 指定的Executor数量（最大值），默认为1，当开启动态分配有效，若未开启，则该值等于ExecutorNumbers
        :type ExecutorMaxNumbers: int
        :param SparkImage: 指定spark版本名称，当前任务使用该spark镜像运行
        :type SparkImage: str
        """
        self.Name = None
        self.Kind = None
        self.DataEngineName = None
        self.ProgramDependentFiles = None
        self.ProgramDependentJars = None
        self.ProgramDependentPython = None
        self.ProgramArchives = None
        self.DriverSize = None
        self.ExecutorSize = None
        self.ExecutorNumbers = None
        self.Arguments = None
        self.ProxyUser = None
        self.TimeoutInSecond = None
        self.ExecutorMaxNumbers = None
        self.SparkImage = None


    def _deserialize(self, params):
        self.Name = params.get("Name")
        self.Kind = params.get("Kind")
        self.DataEngineName = params.get("DataEngineName")
        self.ProgramDependentFiles = params.get("ProgramDependentFiles")
        self.ProgramDependentJars = params.get("ProgramDependentJars")
        self.ProgramDependentPython = params.get("ProgramDependentPython")
        self.ProgramArchives = params.get("ProgramArchives")
        self.DriverSize = params.get("DriverSize")
        self.ExecutorSize = params.get("ExecutorSize")
        self.ExecutorNumbers = params.get("ExecutorNumbers")
        if params.get("Arguments") is not None:
            self.Arguments = []
            for item in params.get("Arguments"):
                obj = KVPair()
                obj._deserialize(item)
                self.Arguments.append(obj)
        self.ProxyUser = params.get("ProxyUser")
        self.TimeoutInSecond = params.get("TimeoutInSecond")
        self.ExecutorMaxNumbers = params.get("ExecutorMaxNumbers")
        self.SparkImage = params.get("SparkImage")
        memeber_set = set(params.keys())
        for name, value in vars(self).items():
            if name in memeber_set:
                memeber_set.remove(name)
        if len(memeber_set) > 0:
            warnings.warn("%s fileds are useless." % ",".join(memeber_set))
        


class CreateNotebookSessionResponse(AbstractModel):
    """CreateNotebookSession返回参数结构体

    """

    def __init__(self):
        r"""
        :param SessionId: Session唯一标识
        :type SessionId: str
        :param SparkAppId: Spark任务返回的AppId
注意：此字段可能返回 null，表示取不到有效值。
        :type SparkAppId: str
        :param State: Session状态，包含：not_started（未启动）、starting（已启动）、idle（等待输入）、busy(正在运行statement)、shutting_down（停止）、error（异常）、dead（已退出）、killed（被杀死）、success（正常停止）
        :type State: str
        :param RequestId: 唯一请求 ID，每次请求都会返回。定位问题时需要提供该次请求的 RequestId。
        :type RequestId: str
        """
        self.SessionId = None
        self.SparkAppId = None
        self.State = None
        self.RequestId = None


    def _deserialize(self, params):
        self.SessionId = params.get("SessionId")
        self.SparkAppId = params.get("SparkAppId")
        self.State = params.get("State")
        self.RequestId = params.get("RequestId")


class CreateNotebookSessionStatementRequest(AbstractModel):
    """CreateNotebookSessionStatement请求参数结构体

    """

    def __init__(self):
        r"""
        :param SessionId: Session唯一标识
        :type SessionId: str
        :param Code: 执行的代码
        :type Code: str
        :param Kind: 类型，当前支持：spark、pyspark、sparkr、sql
        :type Kind: str
        """
        self.SessionId = None
        self.Code = None
        self.Kind = None


    def _deserialize(self, params):
        self.SessionId = params.get("SessionId")
        self.Code = params.get("Code")
        self.Kind = params.get("Kind")
        memeber_set = set(params.keys())
        for name, value in vars(self).items():
            if name in memeber_set:
                memeber_set.remove(name)
        if len(memeber_set) > 0:
            warnings.warn("%s fileds are useless." % ",".join(memeber_set))
        


class CreateNotebookSessionStatementResponse(AbstractModel):
    """CreateNotebookSessionStatement返回参数结构体

    """

    def __init__(self):
        r"""
        :param NotebookSessionStatement: Session Statement详情
        :type NotebookSessionStatement: :class:`tencentcloud.dlc.v20210125.models.NotebookSessionStatementInfo`
        :param RequestId: 唯一请求 ID，每次请求都会返回。定位问题时需要提供该次请求的 RequestId。
        :type RequestId: str
        """
        self.NotebookSessionStatement = None
        self.RequestId = None


    def _deserialize(self, params):
        if params.get("NotebookSessionStatement") is not None:
            self.NotebookSessionStatement = NotebookSessionStatementInfo()
            self.NotebookSessionStatement._deserialize(params.get("NotebookSessionStatement"))
        self.RequestId = params.get("RequestId")


class CreateNotebookSessionStatementSupportBatchSQLRequest(AbstractModel):
    """CreateNotebookSessionStatementSupportBatchSQL请求参数结构体

    """

    def __init__(self):
        r"""
        :param SessionId: Session唯一标识
        :type SessionId: str
        :param Code: 执行的代码
        :type Code: str
        :param Kind: 类型，当前支持：sql
        :type Kind: str
        :param SaveResult: 是否保存运行结果
        :type SaveResult: bool
        """
        self.SessionId = None
        self.Code = None
        self.Kind = None
        self.SaveResult = None


    def _deserialize(self, params):
        self.SessionId = params.get("SessionId")
        self.Code = params.get("Code")
        self.Kind = params.get("Kind")
        self.SaveResult = params.get("SaveResult")
        memeber_set = set(params.keys())
        for name, value in vars(self).items():
            if name in memeber_set:
                memeber_set.remove(name)
        if len(memeber_set) > 0:
            warnings.warn("%s fileds are useless." % ",".join(memeber_set))
        


class CreateNotebookSessionStatementSupportBatchSQLResponse(AbstractModel):
    """CreateNotebookSessionStatementSupportBatchSQL返回参数结构体

    """

    def __init__(self):
        r"""
        :param NotebookSessionStatementBatches: Session Statement详情
        :type NotebookSessionStatementBatches: :class:`tencentcloud.dlc.v20210125.models.NotebookSessionStatementBatchInformation`
        :param RequestId: 唯一请求 ID，每次请求都会返回。定位问题时需要提供该次请求的 RequestId。
        :type RequestId: str
        """
        self.NotebookSessionStatementBatches = None
        self.RequestId = None


    def _deserialize(self, params):
        if params.get("NotebookSessionStatementBatches") is not None:
            self.NotebookSessionStatementBatches = NotebookSessionStatementBatchInformation()
            self.NotebookSessionStatementBatches._deserialize(params.get("NotebookSessionStatementBatches"))
        self.RequestId = params.get("RequestId")


class CreateOrModifyCHDFSProductRequest(AbstractModel):
    """CreateOrModifyCHDFSProduct请求参数结构体

    """

    def __init__(self):
        r"""
        :param ProductName: 产品名称
        :type ProductName: str
        :param SuperUser: 超级用户名称数组
        :type SuperUser: list of str
        :param VpcInfo: vpc配置信息数组
        :type VpcInfo: list of CHDFSProductVpcInfo
        """
        self.ProductName = None
        self.SuperUser = None
        self.VpcInfo = None


    def _deserialize(self, params):
        self.ProductName = params.get("ProductName")
        self.SuperUser = params.get("SuperUser")
        if params.get("VpcInfo") is not None:
            self.VpcInfo = []
            for item in params.get("VpcInfo"):
                obj = CHDFSProductVpcInfo()
                obj._deserialize(item)
                self.VpcInfo.append(obj)
        memeber_set = set(params.keys())
        for name, value in vars(self).items():
            if name in memeber_set:
                memeber_set.remove(name)
        if len(memeber_set) > 0:
            warnings.warn("%s fileds are useless." % ",".join(memeber_set))
        


class CreateOrModifyCHDFSProductResponse(AbstractModel):
    """CreateOrModifyCHDFSProduct返回参数结构体

    """

    def __init__(self):
        r"""
        :param RequestId: 唯一请求 ID，每次请求都会返回。定位问题时需要提供该次请求的 RequestId。
        :type RequestId: str
        """
        self.RequestId = None


    def _deserialize(self, params):
        self.RequestId = params.get("RequestId")


class CreateQueryDirRequest(AbstractModel):
    """CreateQueryDir请求参数结构体

    """

    def __init__(self):
        r"""
        :param Name: 新创建查询目录的名称
        :type Name: str
        """
        self.Name = None


    def _deserialize(self, params):
        self.Name = params.get("Name")
        memeber_set = set(params.keys())
        for name, value in vars(self).items():
            if name in memeber_set:
                memeber_set.remove(name)
        if len(memeber_set) > 0:
            warnings.warn("%s fileds are useless." % ",".join(memeber_set))
        


class CreateQueryDirResponse(AbstractModel):
    """CreateQueryDir返回参数结构体

    """

    def __init__(self):
        r"""
        :param RequestId: 唯一请求 ID，每次请求都会返回。定位问题时需要提供该次请求的 RequestId。
        :type RequestId: str
        """
        self.RequestId = None


    def _deserialize(self, params):
        self.RequestId = params.get("RequestId")


class CreateResultDownloadRequest(AbstractModel):
    """CreateResultDownload请求参数结构体

    """

    def __init__(self):
        r"""
        :param TaskId: 查询结果任务Id
        :type TaskId: str
        :param Format: 下载格式
        :type Format: str
        :param Options: 下载选项
        :type Options: list of KVPair
        :param Force: 是否重新生成下载文件，仅当之前任务状态为 timeout | error 时有效
        :type Force: bool
        """
        self.TaskId = None
        self.Format = None
        self.Options = None
        self.Force = None


    def _deserialize(self, params):
        self.TaskId = params.get("TaskId")
        self.Format = params.get("Format")
        if params.get("Options") is not None:
            self.Options = []
            for item in params.get("Options"):
                obj = KVPair()
                obj._deserialize(item)
                self.Options.append(obj)
        self.Force = params.get("Force")
        memeber_set = set(params.keys())
        for name, value in vars(self).items():
            if name in memeber_set:
                memeber_set.remove(name)
        if len(memeber_set) > 0:
            warnings.warn("%s fileds are useless." % ",".join(memeber_set))
        


class CreateResultDownloadResponse(AbstractModel):
    """CreateResultDownload返回参数结构体

    """

    def __init__(self):
        r"""
        :param DownloadId: 下载任务Id
        :type DownloadId: str
        :param RequestId: 唯一请求 ID，每次请求都会返回。定位问题时需要提供该次请求的 RequestId。
        :type RequestId: str
        """
        self.DownloadId = None
        self.RequestId = None


    def _deserialize(self, params):
        self.DownloadId = params.get("DownloadId")
        self.RequestId = params.get("RequestId")


class CreateSQLSessionCatalogRequest(AbstractModel):
    """CreateSQLSessionCatalog请求参数结构体

    """

    def __init__(self):
        r"""
        :param Name: 目录名称
        :type Name: str
        :param Operator: 操作者
        :type Operator: str
        :param Path: 父目录名称
        :type Path: str
        :param UserVisibility: 授权的子用户，空为自己和管理员可见
        :type UserVisibility: str
        :param PurviewInfoSet: 权限信息
        :type PurviewInfoSet: list of PurviewInfo
        """
        self.Name = None
        self.Operator = None
        self.Path = None
        self.UserVisibility = None
        self.PurviewInfoSet = None


    def _deserialize(self, params):
        self.Name = params.get("Name")
        self.Operator = params.get("Operator")
        self.Path = params.get("Path")
        self.UserVisibility = params.get("UserVisibility")
        if params.get("PurviewInfoSet") is not None:
            self.PurviewInfoSet = []
            for item in params.get("PurviewInfoSet"):
                obj = PurviewInfo()
                obj._deserialize(item)
                self.PurviewInfoSet.append(obj)
        memeber_set = set(params.keys())
        for name, value in vars(self).items():
            if name in memeber_set:
                memeber_set.remove(name)
        if len(memeber_set) > 0:
            warnings.warn("%s fileds are useless." % ",".join(memeber_set))
        


class CreateSQLSessionCatalogResponse(AbstractModel):
    """CreateSQLSessionCatalog返回参数结构体

    """

    def __init__(self):
        r"""
        :param Status: SUCCESS：成功、FAIL：失败、FLUSH：会话内容已变更，请刷新（修改时触发）、DUPLICATE：重名，请调整、NOTEMPTY：该目录下不为空，无法删除、
LIMITEXCEEDED：创建的会话超过限制；
        :type Status: str
        :param SQLSessionCatalogId: 目录节点id
        :type SQLSessionCatalogId: str
        :param RequestId: 唯一请求 ID，每次请求都会返回。定位问题时需要提供该次请求的 RequestId。
        :type RequestId: str
        """
        self.Status = None
        self.SQLSessionCatalogId = None
        self.RequestId = None


    def _deserialize(self, params):
        self.Status = params.get("Status")
        self.SQLSessionCatalogId = params.get("SQLSessionCatalogId")
        self.RequestId = params.get("RequestId")


class CreateSQLSessionSnapshotRequest(AbstractModel):
    """CreateSQLSessionSnapshot请求参数结构体

    """

    def __init__(self):
        r"""
        :param SQLSessionSnapshotInfo: 会话信息，复杂类型
        :type SQLSessionSnapshotInfo: :class:`tencentcloud.dlc.v20210125.models.SQLSessionSnapshotInfo`
        """
        self.SQLSessionSnapshotInfo = None


    def _deserialize(self, params):
        if params.get("SQLSessionSnapshotInfo") is not None:
            self.SQLSessionSnapshotInfo = SQLSessionSnapshotInfo()
            self.SQLSessionSnapshotInfo._deserialize(params.get("SQLSessionSnapshotInfo"))
        memeber_set = set(params.keys())
        for name, value in vars(self).items():
            if name in memeber_set:
                memeber_set.remove(name)
        if len(memeber_set) > 0:
            warnings.warn("%s fileds are useless." % ",".join(memeber_set))
        


class CreateSQLSessionSnapshotResponse(AbstractModel):
    """CreateSQLSessionSnapshot返回参数结构体

    """

    def __init__(self):
        r"""
        :param SessionId: 会话ID
        :type SessionId: str
        :param Status: SUCCESS：成功、FAIL：失败、FLUSH：会话内容已变更，请刷新（修改时触发）、DUPLICATE：重名，请调整、NOTEMPTY：该目录下不为空，无法删除、
LIMITEXCEEDED：创建的会话超过限制；
        :type Status: str
        :param Version: 版本号
        :type Version: int
        :param RequestId: 唯一请求 ID，每次请求都会返回。定位问题时需要提供该次请求的 RequestId。
        :type RequestId: str
        """
        self.SessionId = None
        self.Status = None
        self.Version = None
        self.RequestId = None


    def _deserialize(self, params):
        self.SessionId = params.get("SessionId")
        self.Status = params.get("Status")
        self.Version = params.get("Version")
        self.RequestId = params.get("RequestId")


class CreateSQLSessionSubmitRecordRequest(AbstractModel):
    """CreateSQLSessionSubmitRecord请求参数结构体

    """

    def __init__(self):
        r"""
        :param SessionId: 会话ID
        :type SessionId: str
        :param BatchId: 批量提交任务ID
        :type BatchId: str
        :param TaskIdSet: 任务ID集合
        :type TaskIdSet: list of str
        :param SubmitTime: 任务提交时间
        :type SubmitTime: str
        :param SessionSQL: 会话SQL
        :type SessionSQL: str
        :param ComputeEngine: 执行引擎
        :type ComputeEngine: str
        :param ComputeResource: 计算资源
        :type ComputeResource: str
        """
        self.SessionId = None
        self.BatchId = None
        self.TaskIdSet = None
        self.SubmitTime = None
        self.SessionSQL = None
        self.ComputeEngine = None
        self.ComputeResource = None


    def _deserialize(self, params):
        self.SessionId = params.get("SessionId")
        self.BatchId = params.get("BatchId")
        self.TaskIdSet = params.get("TaskIdSet")
        self.SubmitTime = params.get("SubmitTime")
        self.SessionSQL = params.get("SessionSQL")
        self.ComputeEngine = params.get("ComputeEngine")
        self.ComputeResource = params.get("ComputeResource")
        memeber_set = set(params.keys())
        for name, value in vars(self).items():
            if name in memeber_set:
                memeber_set.remove(name)
        if len(memeber_set) > 0:
            warnings.warn("%s fileds are useless." % ",".join(memeber_set))
        


class CreateSQLSessionSubmitRecordResponse(AbstractModel):
    """CreateSQLSessionSubmitRecord返回参数结构体

    """

    def __init__(self):
        r"""
        :param Status: SUCCESS：成功、FAIL：失败、FLUSH：会话内容已变更，请刷新（修改时触发）、DUPLICATE：重名，请调整、NOTEMPTY：该目录下不为空，无法删除、
LIMITEXCEEDED：创建的会话超过限制；
        :type Status: str
        :param RequestId: 唯一请求 ID，每次请求都会返回。定位问题时需要提供该次请求的 RequestId。
        :type RequestId: str
        """
        self.Status = None
        self.RequestId = None


    def _deserialize(self, params):
        self.Status = params.get("Status")
        self.RequestId = params.get("RequestId")


class CreateScheduleTaskRequest(AbstractModel):
    """CreateScheduleTask请求参数结构体

    """

    def __init__(self):
        r"""
        :param ScheduleTaskInfo: 调度任务信息
        :type ScheduleTaskInfo: :class:`tencentcloud.dlc.v20210125.models.ScheduleTaskInfo`
        """
        self.ScheduleTaskInfo = None


    def _deserialize(self, params):
        if params.get("ScheduleTaskInfo") is not None:
            self.ScheduleTaskInfo = ScheduleTaskInfo()
            self.ScheduleTaskInfo._deserialize(params.get("ScheduleTaskInfo"))
        memeber_set = set(params.keys())
        for name, value in vars(self).items():
            if name in memeber_set:
                memeber_set.remove(name)
        if len(memeber_set) > 0:
            warnings.warn("%s fileds are useless." % ",".join(memeber_set))
        


class CreateScheduleTaskResponse(AbstractModel):
    """CreateScheduleTask返回参数结构体

    """

    def __init__(self):
        r"""
        :param TaskId: 任务ID
        :type TaskId: str
        :param ScheduleTaskInfo: 任务详情
        :type ScheduleTaskInfo: :class:`tencentcloud.dlc.v20210125.models.ScheduleTaskInfo`
        :param RequestId: 唯一请求 ID，每次请求都会返回。定位问题时需要提供该次请求的 RequestId。
        :type RequestId: str
        """
        self.TaskId = None
        self.ScheduleTaskInfo = None
        self.RequestId = None


    def _deserialize(self, params):
        self.TaskId = params.get("TaskId")
        if params.get("ScheduleTaskInfo") is not None:
            self.ScheduleTaskInfo = ScheduleTaskInfo()
            self.ScheduleTaskInfo._deserialize(params.get("ScheduleTaskInfo"))
        self.RequestId = params.get("RequestId")


class CreateScriptRequest(AbstractModel):
    """CreateScript请求参数结构体

    """

    def __init__(self):
        r"""
        :param ScriptName: 脚本名称，最大不能超过255个字符。
        :type ScriptName: str
        :param SQLStatement: base64编码后的sql语句
        :type SQLStatement: str
        :param ScriptDesc: 脚本描述， 不能超过50个字符
        :type ScriptDesc: str
        :param DatabaseName: 数据库名称
        :type DatabaseName: str
        """
        self.ScriptName = None
        self.SQLStatement = None
        self.ScriptDesc = None
        self.DatabaseName = None


    def _deserialize(self, params):
        self.ScriptName = params.get("ScriptName")
        self.SQLStatement = params.get("SQLStatement")
        self.ScriptDesc = params.get("ScriptDesc")
        self.DatabaseName = params.get("DatabaseName")
        memeber_set = set(params.keys())
        for name, value in vars(self).items():
            if name in memeber_set:
                memeber_set.remove(name)
        if len(memeber_set) > 0:
            warnings.warn("%s fileds are useless." % ",".join(memeber_set))
        


class CreateScriptResponse(AbstractModel):
    """CreateScript返回参数结构体

    """

    def __init__(self):
        r"""
        :param RequestId: 唯一请求 ID，每次请求都会返回。定位问题时需要提供该次请求的 RequestId。
        :type RequestId: str
        """
        self.RequestId = None


    def _deserialize(self, params):
        self.RequestId = params.get("RequestId")


class CreateSparkAppForSQLRequest(AbstractModel):
    """CreateSparkAppForSQL请求参数结构体

    """

    def __init__(self):
        r"""
        :param AppName: spark应用名
        :type AppName: str
        :param DataEngine: 执行spark作业的数据引擎
        :type DataEngine: str
        :param AppDriverSize: spark作业driver资源规格大小, 可取small,medium,large,xlarge
        :type AppDriverSize: str
        :param AppExecutorSize: spark作业executor资源规格大小, 可取small,medium,large,xlarge
        :type AppExecutorSize: str
        :param AppExecutorNums: spark作业executor个数
        :type AppExecutorNums: int
        :param SQL: spark作业命令行参数
        :type SQL: str
        :param ENI: 该字段已下线，请使用字段Datasource
        :type ENI: str
        :param AppExecutorMaxNumbers: 指定的Executor数量（最大值），默认为1，当开启动态分配有效，若未开启，则该值等于AppExecutorNums
        :type AppExecutorMaxNumbers: int
        """
        self.AppName = None
        self.DataEngine = None
        self.AppDriverSize = None
        self.AppExecutorSize = None
        self.AppExecutorNums = None
        self.SQL = None
        self.ENI = None
        self.AppExecutorMaxNumbers = None


    def _deserialize(self, params):
        self.AppName = params.get("AppName")
        self.DataEngine = params.get("DataEngine")
        self.AppDriverSize = params.get("AppDriverSize")
        self.AppExecutorSize = params.get("AppExecutorSize")
        self.AppExecutorNums = params.get("AppExecutorNums")
        self.SQL = params.get("SQL")
        self.ENI = params.get("ENI")
        self.AppExecutorMaxNumbers = params.get("AppExecutorMaxNumbers")
        memeber_set = set(params.keys())
        for name, value in vars(self).items():
            if name in memeber_set:
                memeber_set.remove(name)
        if len(memeber_set) > 0:
            warnings.warn("%s fileds are useless." % ",".join(memeber_set))
        


class CreateSparkAppForSQLResponse(AbstractModel):
    """CreateSparkAppForSQL返回参数结构体

    """

    def __init__(self):
        r"""
        :param SparkAppId: Job id
        :type SparkAppId: str
        :param RequestId: 唯一请求 ID，每次请求都会返回。定位问题时需要提供该次请求的 RequestId。
        :type RequestId: str
        """
        self.SparkAppId = None
        self.RequestId = None


    def _deserialize(self, params):
        self.SparkAppId = params.get("SparkAppId")
        self.RequestId = params.get("RequestId")


class CreateSparkAppRequest(AbstractModel):
    """CreateSparkApp请求参数结构体

    """

    def __init__(self):
        r"""
        :param AppName: spark作业名
        :type AppName: str
        :param AppType: spark作业类型，1代表spark jar作业，2代表spark streaming作业
        :type AppType: int
        :param DataEngine: 执行spark作业的数据引擎名称
        :type DataEngine: str
        :param AppFile: spark作业程序包文件路径
        :type AppFile: str
        :param RoleArn: 数据访问策略，CAM Role arn
        :type RoleArn: int
        :param AppDriverSize: 指定的Driver规格，当前支持：small（默认，1cu）、medium（2cu）、large（4cu）、xlarge（8cu）
        :type AppDriverSize: str
        :param AppExecutorSize: 指定的Executor规格，当前支持：small（默认，1cu）、medium（2cu）、large（4cu）、xlarge（8cu）
        :type AppExecutorSize: str
        :param AppExecutorNums: spark作业executor个数
        :type AppExecutorNums: int
        :param Eni: 该字段已下线，请使用字段Datasource
        :type Eni: str
        :param IsLocal: spark作业程序包是否本地上传，cos：存放与cos，lakefs：本地上传（控制台使用，该方式不支持直接接口调用）
        :type IsLocal: str
        :param MainClass: spark作业主类
        :type MainClass: str
        :param AppConf: spark配置，以换行符分隔
        :type AppConf: str
        :param IsLocalJars: spark 作业依赖jar包是否本地上传，cos：存放与cos，lakefs：本地上传（控制台使用，该方式不支持直接接口调用）
        :type IsLocalJars: str
        :param AppJars: spark 作业依赖jar包（--jars），以逗号分隔
        :type AppJars: str
        :param IsLocalFiles: spark作业依赖文件资源是否本地上传，cos：存放与cos，lakefs：本地上传（控制台使用，该方式不支持直接接口调用）
        :type IsLocalFiles: str
        :param AppFiles: spark作业依赖文件资源（--files）（非jar、zip），以逗号分隔
        :type AppFiles: str
        :param CmdArgs: spark作业程序入参，空格分割
        :type CmdArgs: str
        :param MaxRetries: 最大重试次数，只对spark流任务生效
        :type MaxRetries: int
        :param DataSource: 数据源名称
        :type DataSource: str
        :param IsLocalPythonFiles: pyspark：依赖上传方式，cos：存放与cos，lakefs：本地上传（控制台使用，该方式不支持直接接口调用）
        :type IsLocalPythonFiles: str
        :param AppPythonFiles: pyspark作业依赖python资源（--py-files），支持py/zip/egg等归档格式，多文件以逗号分隔
        :type AppPythonFiles: str
        :param IsLocalArchives: spark作业依赖archives资源是否本地上传，cos：存放与cos，lakefs：本地上传（控制台使用，该方式不支持直接接口调用）
        :type IsLocalArchives: str
        :param AppArchives: spark作业依赖archives资源（--archives），支持tar.gz/tgz/tar等归档格式，以逗号分隔
        :type AppArchives: str
        :param SparkImage: Spark Image 版本号
        :type SparkImage: str
        :param SparkImageVersion: Spark Image 版本名称
        :type SparkImageVersion: str
        :param AppExecutorMaxNumbers: 指定的Executor数量（最大值），默认为1，当开启动态分配有效，若未开启，则该值等于AppExecutorNums
        :type AppExecutorMaxNumbers: int
        :param SessionId: 关联dlc查询脚本id
        :type SessionId: str
        :param IsInherit: 任务资源配置是否继承集群模板，0（默认）不继承，1：继承
        :type IsInherit: int
        """
        self.AppName = None
        self.AppType = None
        self.DataEngine = None
        self.AppFile = None
        self.RoleArn = None
        self.AppDriverSize = None
        self.AppExecutorSize = None
        self.AppExecutorNums = None
        self.Eni = None
        self.IsLocal = None
        self.MainClass = None
        self.AppConf = None
        self.IsLocalJars = None
        self.AppJars = None
        self.IsLocalFiles = None
        self.AppFiles = None
        self.CmdArgs = None
        self.MaxRetries = None
        self.DataSource = None
        self.IsLocalPythonFiles = None
        self.AppPythonFiles = None
        self.IsLocalArchives = None
        self.AppArchives = None
        self.SparkImage = None
        self.SparkImageVersion = None
        self.AppExecutorMaxNumbers = None
        self.SessionId = None
        self.IsInherit = None


    def _deserialize(self, params):
        self.AppName = params.get("AppName")
        self.AppType = params.get("AppType")
        self.DataEngine = params.get("DataEngine")
        self.AppFile = params.get("AppFile")
        self.RoleArn = params.get("RoleArn")
        self.AppDriverSize = params.get("AppDriverSize")
        self.AppExecutorSize = params.get("AppExecutorSize")
        self.AppExecutorNums = params.get("AppExecutorNums")
        self.Eni = params.get("Eni")
        self.IsLocal = params.get("IsLocal")
        self.MainClass = params.get("MainClass")
        self.AppConf = params.get("AppConf")
        self.IsLocalJars = params.get("IsLocalJars")
        self.AppJars = params.get("AppJars")
        self.IsLocalFiles = params.get("IsLocalFiles")
        self.AppFiles = params.get("AppFiles")
        self.CmdArgs = params.get("CmdArgs")
        self.MaxRetries = params.get("MaxRetries")
        self.DataSource = params.get("DataSource")
        self.IsLocalPythonFiles = params.get("IsLocalPythonFiles")
        self.AppPythonFiles = params.get("AppPythonFiles")
        self.IsLocalArchives = params.get("IsLocalArchives")
        self.AppArchives = params.get("AppArchives")
        self.SparkImage = params.get("SparkImage")
        self.SparkImageVersion = params.get("SparkImageVersion")
        self.AppExecutorMaxNumbers = params.get("AppExecutorMaxNumbers")
        self.SessionId = params.get("SessionId")
        self.IsInherit = params.get("IsInherit")
        memeber_set = set(params.keys())
        for name, value in vars(self).items():
            if name in memeber_set:
                memeber_set.remove(name)
        if len(memeber_set) > 0:
            warnings.warn("%s fileds are useless." % ",".join(memeber_set))
        


class CreateSparkAppResponse(AbstractModel):
    """CreateSparkApp返回参数结构体

    """

    def __init__(self):
        r"""
        :param SparkAppId: App唯一标识
注意：此字段可能返回 null，表示取不到有效值。
        :type SparkAppId: str
        :param RequestId: 唯一请求 ID，每次请求都会返回。定位问题时需要提供该次请求的 RequestId。
        :type RequestId: str
        """
        self.SparkAppId = None
        self.RequestId = None


    def _deserialize(self, params):
        self.SparkAppId = params.get("SparkAppId")
        self.RequestId = params.get("RequestId")


class CreateSparkAppTaskRequest(AbstractModel):
    """CreateSparkAppTask请求参数结构体

    """

    def __init__(self):
        r"""
        :param JobName: spark作业名
        :type JobName: str
        :param CmdArgs: spark作业程序入参，以空格分隔；一般用于周期性调用使用
        :type CmdArgs: str
        """
        self.JobName = None
        self.CmdArgs = None


    def _deserialize(self, params):
        self.JobName = params.get("JobName")
        self.CmdArgs = params.get("CmdArgs")
        memeber_set = set(params.keys())
        for name, value in vars(self).items():
            if name in memeber_set:
                memeber_set.remove(name)
        if len(memeber_set) > 0:
            warnings.warn("%s fileds are useless." % ",".join(memeber_set))
        


class CreateSparkAppTaskResponse(AbstractModel):
    """CreateSparkAppTask返回参数结构体

    """

    def __init__(self):
        r"""
        :param BatchId: 批Id
        :type BatchId: str
        :param TaskId: 任务Id
        :type TaskId: str
        :param RequestId: 唯一请求 ID，每次请求都会返回。定位问题时需要提供该次请求的 RequestId。
        :type RequestId: str
        """
        self.BatchId = None
        self.TaskId = None
        self.RequestId = None


    def _deserialize(self, params):
        self.BatchId = params.get("BatchId")
        self.TaskId = params.get("TaskId")
        self.RequestId = params.get("RequestId")


class CreateSparkSessionBatchSQLRequest(AbstractModel):
    """CreateSparkSessionBatchSQL请求参数结构体

    """

    def __init__(self):
        r"""
        :param DataEngineName: DLC Spark作业引擎名称
        :type DataEngineName: str
        :param ExecuteSQL: 运行sql
        :type ExecuteSQL: str
        :param DriverSize: 指定的Driver规格，当前支持：small（默认，1cu）、medium（2cu）、large（4cu）、xlarge（8cu）
        :type DriverSize: str
        :param ExecutorSize: 指定的Executor规格，当前支持：small（默认，1cu）、medium（2cu）、large（4cu）、xlarge（8cu）
        :type ExecutorSize: str
        :param ExecutorNumbers: 指定的Executor数量，默认为1
        :type ExecutorNumbers: int
        :param ExecutorMaxNumbers: 指定的Executor数量（最大值），默认为1，当开启动态分配有效，若未开启，则该值等于ExecutorNumbers
        :type ExecutorMaxNumbers: int
        :param TimeoutInSecond: 指定的Session超时时间，单位秒，默认3600秒
        :type TimeoutInSecond: int
        :param SessionId: Session唯一标识，当指定sessionid，则使用该session运行任务。
        :type SessionId: str
        :param SessionName: 指定要创建的session名称
        :type SessionName: str
        :param Arguments: Session相关配置，当前支持：1.dlc.eni：用户配置的eni网关信息，可以用过该字段设置；
2.dlc.role.arn：用户配置的roleArn鉴权策略配置信息，可以用过该字段设置；
3.dlc.sql.set.config：用户配置的集群配置信息，可以用过该字段设置；
        :type Arguments: list of KVPair
        """
        self.DataEngineName = None
        self.ExecuteSQL = None
        self.DriverSize = None
        self.ExecutorSize = None
        self.ExecutorNumbers = None
        self.ExecutorMaxNumbers = None
        self.TimeoutInSecond = None
        self.SessionId = None
        self.SessionName = None
        self.Arguments = None


    def _deserialize(self, params):
        self.DataEngineName = params.get("DataEngineName")
        self.ExecuteSQL = params.get("ExecuteSQL")
        self.DriverSize = params.get("DriverSize")
        self.ExecutorSize = params.get("ExecutorSize")
        self.ExecutorNumbers = params.get("ExecutorNumbers")
        self.ExecutorMaxNumbers = params.get("ExecutorMaxNumbers")
        self.TimeoutInSecond = params.get("TimeoutInSecond")
        self.SessionId = params.get("SessionId")
        self.SessionName = params.get("SessionName")
        if params.get("Arguments") is not None:
            self.Arguments = []
            for item in params.get("Arguments"):
                obj = KVPair()
                obj._deserialize(item)
                self.Arguments.append(obj)
        memeber_set = set(params.keys())
        for name, value in vars(self).items():
            if name in memeber_set:
                memeber_set.remove(name)
        if len(memeber_set) > 0:
            warnings.warn("%s fileds are useless." % ",".join(memeber_set))
        


class CreateSparkSessionBatchSQLResponse(AbstractModel):
    """CreateSparkSessionBatchSQL返回参数结构体

    """

    def __init__(self):
        r"""
        :param BatchId: 批任务唯一标识
        :type BatchId: str
        :param RequestId: 唯一请求 ID，每次请求都会返回。定位问题时需要提供该次请求的 RequestId。
        :type RequestId: str
        """
        self.BatchId = None
        self.RequestId = None


    def _deserialize(self, params):
        self.BatchId = params.get("BatchId")
        self.RequestId = params.get("RequestId")


class CreateStoreLocationRequest(AbstractModel):
    """CreateStoreLocation请求参数结构体

    """

    def __init__(self):
        r"""
        :param StoreLocation: 计算结果存储cos路径，如：cosn://bucketname/
        :type StoreLocation: str
        """
        self.StoreLocation = None


    def _deserialize(self, params):
        self.StoreLocation = params.get("StoreLocation")
        memeber_set = set(params.keys())
        for name, value in vars(self).items():
            if name in memeber_set:
                memeber_set.remove(name)
        if len(memeber_set) > 0:
            warnings.warn("%s fileds are useless." % ",".join(memeber_set))
        


class CreateStoreLocationResponse(AbstractModel):
    """CreateStoreLocation返回参数结构体

    """

    def __init__(self):
        r"""
        :param RequestId: 唯一请求 ID，每次请求都会返回。定位问题时需要提供该次请求的 RequestId。
        :type RequestId: str
        """
        self.RequestId = None


    def _deserialize(self, params):
        self.RequestId = params.get("RequestId")


class CreateTableRequest(AbstractModel):
    """CreateTable请求参数结构体

    """

    def __init__(self):
        r"""
        :param TableInfo: 数据表配置信息
        :type TableInfo: :class:`tencentcloud.dlc.v20210125.models.TableInfo`
        """
        self.TableInfo = None


    def _deserialize(self, params):
        if params.get("TableInfo") is not None:
            self.TableInfo = TableInfo()
            self.TableInfo._deserialize(params.get("TableInfo"))
        memeber_set = set(params.keys())
        for name, value in vars(self).items():
            if name in memeber_set:
                memeber_set.remove(name)
        if len(memeber_set) > 0:
            warnings.warn("%s fileds are useless." % ",".join(memeber_set))
        


class CreateTableResponse(AbstractModel):
    """CreateTable返回参数结构体

    """

    def __init__(self):
        r"""
        :param Execution: 生成的建表执行语句对象。
        :type Execution: :class:`tencentcloud.dlc.v20210125.models.Execution`
        :param RequestId: 唯一请求 ID，每次请求都会返回。定位问题时需要提供该次请求的 RequestId。
        :type RequestId: str
        """
        self.Execution = None
        self.RequestId = None


    def _deserialize(self, params):
        if params.get("Execution") is not None:
            self.Execution = Execution()
            self.Execution._deserialize(params.get("Execution"))
        self.RequestId = params.get("RequestId")


class CreateTaskRequest(AbstractModel):
    """CreateTask请求参数结构体

    """

    def __init__(self):
        r"""
        :param Task: 计算任务，该参数中包含任务类型及其相关配置信息
        :type Task: :class:`tencentcloud.dlc.v20210125.models.Task`
        :param DatabaseName: 数据库名称。如果SQL语句中有数据库名称，优先使用SQL语句中的数据库，否则使用该参数指定的数据库（注：当提交建库sql时，该字段传空字符串）。
        :type DatabaseName: str
        :param DatasourceConnectionName: 默认数据源名称。
        :type DatasourceConnectionName: str
        :param DataEngineName: 数据引擎名称，不填提交到默认集群
        :type DataEngineName: str
        :param Config: 配置信息，key-value数组，对外不可见。key1：AuthorityRole（鉴权角色，默认传SubUin，base64加密，仅在jdbc提交任务时使用）
        :type Config: list of KVPair
        """
        self.Task = None
        self.DatabaseName = None
        self.DatasourceConnectionName = None
        self.DataEngineName = None
        self.Config = None


    def _deserialize(self, params):
        if params.get("Task") is not None:
            self.Task = Task()
            self.Task._deserialize(params.get("Task"))
        self.DatabaseName = params.get("DatabaseName")
        self.DatasourceConnectionName = params.get("DatasourceConnectionName")
        self.DataEngineName = params.get("DataEngineName")
        if params.get("Config") is not None:
            self.Config = []
            for item in params.get("Config"):
                obj = KVPair()
                obj._deserialize(item)
                self.Config.append(obj)
        memeber_set = set(params.keys())
        for name, value in vars(self).items():
            if name in memeber_set:
                memeber_set.remove(name)
        if len(memeber_set) > 0:
            warnings.warn("%s fileds are useless." % ",".join(memeber_set))
        


class CreateTaskResponse(AbstractModel):
    """CreateTask返回参数结构体

    """

    def __init__(self):
        r"""
        :param TaskId: 任务ID
注意：此字段可能返回 null，表示取不到有效值。
        :type TaskId: str
        :param RequestId: 唯一请求 ID，每次请求都会返回。定位问题时需要提供该次请求的 RequestId。
        :type RequestId: str
        """
        self.TaskId = None
        self.RequestId = None


    def _deserialize(self, params):
        self.TaskId = params.get("TaskId")
        self.RequestId = params.get("RequestId")


class CreateTasksInOrderRequest(AbstractModel):
    """CreateTasksInOrder请求参数结构体

    """

    def __init__(self):
        r"""
        :param DatabaseName: 数据库名称。如果SQL语句中有数据库名称，优先使用SQL语句中的数据库，否则使用该参数指定的数据库。
        :type DatabaseName: str
        :param Tasks: SQL任务信息
        :type Tasks: :class:`tencentcloud.dlc.v20210125.models.TasksInfo`
        :param DatasourceConnectionName: 数据源名称，默认为COSDataCatalog
        :type DatasourceConnectionName: str
        """
        self.DatabaseName = None
        self.Tasks = None
        self.DatasourceConnectionName = None


    def _deserialize(self, params):
        self.DatabaseName = params.get("DatabaseName")
        if params.get("Tasks") is not None:
            self.Tasks = TasksInfo()
            self.Tasks._deserialize(params.get("Tasks"))
        self.DatasourceConnectionName = params.get("DatasourceConnectionName")
        memeber_set = set(params.keys())
        for name, value in vars(self).items():
            if name in memeber_set:
                memeber_set.remove(name)
        if len(memeber_set) > 0:
            warnings.warn("%s fileds are useless." % ",".join(memeber_set))
        


class CreateTasksInOrderResponse(AbstractModel):
    """CreateTasksInOrder返回参数结构体

    """

    def __init__(self):
        r"""
        :param BatchId: 本批次提交的任务的批次Id
        :type BatchId: str
        :param TaskIdSet: 任务Id集合，按照执行顺序排列
        :type TaskIdSet: list of str
        :param RequestId: 唯一请求 ID，每次请求都会返回。定位问题时需要提供该次请求的 RequestId。
        :type RequestId: str
        """
        self.BatchId = None
        self.TaskIdSet = None
        self.RequestId = None


    def _deserialize(self, params):
        self.BatchId = params.get("BatchId")
        self.TaskIdSet = params.get("TaskIdSet")
        self.RequestId = params.get("RequestId")


class CreateTasksRequest(AbstractModel):
    """CreateTasks请求参数结构体

    """

    def __init__(self):
        r"""
        :param DatabaseName: 数据库名称。如果SQL语句中有数据库名称，优先使用SQL语句中的数据库，否则使用该参数指定的数据库（注：当提交建库sql时，该字段传空字符串）。
        :type DatabaseName: str
        :param Tasks: SQL任务信息
        :type Tasks: :class:`tencentcloud.dlc.v20210125.models.TasksInfo`
        :param DatasourceConnectionName: 数据源名称，默认为DataLakeCatalog
        :type DatasourceConnectionName: str
        :param DataEngineName: 计算引擎名称，不填任务提交到默认集群
        :type DataEngineName: str
        """
        self.DatabaseName = None
        self.Tasks = None
        self.DatasourceConnectionName = None
        self.DataEngineName = None


    def _deserialize(self, params):
        self.DatabaseName = params.get("DatabaseName")
        if params.get("Tasks") is not None:
            self.Tasks = TasksInfo()
            self.Tasks._deserialize(params.get("Tasks"))
        self.DatasourceConnectionName = params.get("DatasourceConnectionName")
        self.DataEngineName = params.get("DataEngineName")
        memeber_set = set(params.keys())
        for name, value in vars(self).items():
            if name in memeber_set:
                memeber_set.remove(name)
        if len(memeber_set) > 0:
            warnings.warn("%s fileds are useless." % ",".join(memeber_set))
        


class CreateTasksResponse(AbstractModel):
    """CreateTasks返回参数结构体

    """

    def __init__(self):
        r"""
        :param BatchId: 本批次提交的任务的批次Id
        :type BatchId: str
        :param TaskIdSet: 任务Id集合，按照执行顺序排列
        :type TaskIdSet: list of str
        :param RequestId: 唯一请求 ID，每次请求都会返回。定位问题时需要提供该次请求的 RequestId。
        :type RequestId: str
        """
        self.BatchId = None
        self.TaskIdSet = None
        self.RequestId = None


    def _deserialize(self, params):
        self.BatchId = params.get("BatchId")
        self.TaskIdSet = params.get("TaskIdSet")
        self.RequestId = params.get("RequestId")


class CreateUserRequest(AbstractModel):
    """CreateUser请求参数结构体

    """

    def __init__(self):
        r"""
        :param UserId: 需要授权的子用户uin，可以通过腾讯云控制台右上角 → “账号信息” → “账号ID进行查看”。
        :type UserId: str
        :param UserDescription: 用户描述信息，方便区分不同用户
        :type UserDescription: str
        :param PolicySet: 绑定到用户的权限集合
        :type PolicySet: list of Policy
        :param UserType: 用户类型。ADMIN：管理员 COMMON：一般用户。当用户类型为管理员的时候，不能设置权限集合和绑定的工作组集合，管理员默认拥有所有权限。该参数不填默认为COMMON
        :type UserType: str
        :param WorkGroupIds: 绑定到用户的工作组ID集合。
        :type WorkGroupIds: list of int
        :param UserAlias: 用户别名，字符长度小50
        :type UserAlias: str
        """
        self.UserId = None
        self.UserDescription = None
        self.PolicySet = None
        self.UserType = None
        self.WorkGroupIds = None
        self.UserAlias = None


    def _deserialize(self, params):
        self.UserId = params.get("UserId")
        self.UserDescription = params.get("UserDescription")
        if params.get("PolicySet") is not None:
            self.PolicySet = []
            for item in params.get("PolicySet"):
                obj = Policy()
                obj._deserialize(item)
                self.PolicySet.append(obj)
        self.UserType = params.get("UserType")
        self.WorkGroupIds = params.get("WorkGroupIds")
        self.UserAlias = params.get("UserAlias")
        memeber_set = set(params.keys())
        for name, value in vars(self).items():
            if name in memeber_set:
                memeber_set.remove(name)
        if len(memeber_set) > 0:
            warnings.warn("%s fileds are useless." % ",".join(memeber_set))
        


class CreateUserResponse(AbstractModel):
    """CreateUser返回参数结构体

    """

    def __init__(self):
        r"""
        :param RequestId: 唯一请求 ID，每次请求都会返回。定位问题时需要提供该次请求的 RequestId。
        :type RequestId: str
        """
        self.RequestId = None


    def _deserialize(self, params):
        self.RequestId = params.get("RequestId")


class CreateUserRoleRequest(AbstractModel):
    """CreateUserRole请求参数结构体

    """

    def __init__(self):
        r"""
        :param Arn: 角色Arn信息
        :type Arn: str
        :param Desc: 角色描述信息
        :type Desc: str
        """
        self.Arn = None
        self.Desc = None


    def _deserialize(self, params):
        self.Arn = params.get("Arn")
        self.Desc = params.get("Desc")
        memeber_set = set(params.keys())
        for name, value in vars(self).items():
            if name in memeber_set:
                memeber_set.remove(name)
        if len(memeber_set) > 0:
            warnings.warn("%s fileds are useless." % ",".join(memeber_set))
        


class CreateUserRoleResponse(AbstractModel):
    """CreateUserRole返回参数结构体

    """

    def __init__(self):
        r"""
        :param RequestId: 唯一请求 ID，每次请求都会返回。定位问题时需要提供该次请求的 RequestId。
        :type RequestId: str
        """
        self.RequestId = None


    def _deserialize(self, params):
        self.RequestId = params.get("RequestId")


class CreateWorkGroupRequest(AbstractModel):
    """CreateWorkGroup请求参数结构体

    """

    def __init__(self):
        r"""
        :param WorkGroupName: 工作组名称
        :type WorkGroupName: str
        :param WorkGroupDescription: 工作组描述
        :type WorkGroupDescription: str
        :param PolicySet: 工作组绑定的鉴权策略集合
        :type PolicySet: list of Policy
        :param UserIds: 需要绑定到工作组的用户Id集合
        :type UserIds: list of str
        """
        self.WorkGroupName = None
        self.WorkGroupDescription = None
        self.PolicySet = None
        self.UserIds = None


    def _deserialize(self, params):
        self.WorkGroupName = params.get("WorkGroupName")
        self.WorkGroupDescription = params.get("WorkGroupDescription")
        if params.get("PolicySet") is not None:
            self.PolicySet = []
            for item in params.get("PolicySet"):
                obj = Policy()
                obj._deserialize(item)
                self.PolicySet.append(obj)
        self.UserIds = params.get("UserIds")
        memeber_set = set(params.keys())
        for name, value in vars(self).items():
            if name in memeber_set:
                memeber_set.remove(name)
        if len(memeber_set) > 0:
            warnings.warn("%s fileds are useless." % ",".join(memeber_set))
        


class CreateWorkGroupResponse(AbstractModel):
    """CreateWorkGroup返回参数结构体

    """

    def __init__(self):
        r"""
        :param WorkGroupId: 工作组Id，全局唯一
        :type WorkGroupId: int
        :param RequestId: 唯一请求 ID，每次请求都会返回。定位问题时需要提供该次请求的 RequestId。
        :type RequestId: str
        """
        self.WorkGroupId = None
        self.RequestId = None


    def _deserialize(self, params):
        self.WorkGroupId = params.get("WorkGroupId")
        self.RequestId = params.get("RequestId")


class CreateWorkflowRequest(AbstractModel):
    """CreateWorkflow请求参数结构体

    """

    def __init__(self):
        r"""
        :param WorkflowName: 调度计划名称
        :type WorkflowName: str
        :param CycleType: 调度周期类型，分钟(MINUTE_CYCLE)，小时(HOUR_CYCLE)，天(DAY_CYCLE)，周(WEEK_CYCLE),月(MONTH_CYCLE)，一次性(ONEOFF_CYCLE)
        :type CycleType: str
        :param CycleStep: 任务调度周期间隔
        :type CycleStep: int
        :param DelayTime: 调度任务延迟时间，从调度周期开始时间计算的分钟数
        :type DelayTime: int
        :param TaskAction: 在指定周期的第n个单位时间运行（周和月任务使用），比如周任务周日运行：TaskAction=1；周一运行：TaskAction=2，月任务当月第1天运行：TaskAction=1，等
        :type TaskAction: str
        :param StartTime: 调度计划开始时间
        :type StartTime: str
        :param EndTime: 调度计划结束时间
        :type EndTime: str
        :param WorkflowDesc: 调度计划描述
        :type WorkflowDesc: str
        :param OwnersUin: 调度计划责任人uin数组
        :type OwnersUin: list of str
        """
        self.WorkflowName = None
        self.CycleType = None
        self.CycleStep = None
        self.DelayTime = None
        self.TaskAction = None
        self.StartTime = None
        self.EndTime = None
        self.WorkflowDesc = None
        self.OwnersUin = None


    def _deserialize(self, params):
        self.WorkflowName = params.get("WorkflowName")
        self.CycleType = params.get("CycleType")
        self.CycleStep = params.get("CycleStep")
        self.DelayTime = params.get("DelayTime")
        self.TaskAction = params.get("TaskAction")
        self.StartTime = params.get("StartTime")
        self.EndTime = params.get("EndTime")
        self.WorkflowDesc = params.get("WorkflowDesc")
        self.OwnersUin = params.get("OwnersUin")
        memeber_set = set(params.keys())
        for name, value in vars(self).items():
            if name in memeber_set:
                memeber_set.remove(name)
        if len(memeber_set) > 0:
            warnings.warn("%s fileds are useless." % ",".join(memeber_set))
        


class CreateWorkflowResponse(AbstractModel):
    """CreateWorkflow返回参数结构体

    """

    def __init__(self):
        r"""
        :param WorkflowId: 调度计划ID
        :type WorkflowId: str
        :param RequestId: 唯一请求 ID，每次请求都会返回。定位问题时需要提供该次请求的 RequestId。
        :type RequestId: str
        """
        self.WorkflowId = None
        self.RequestId = None


    def _deserialize(self, params):
        self.WorkflowId = params.get("WorkflowId")
        self.RequestId = params.get("RequestId")


class CrontabResumeSuspendStrategy(AbstractModel):
    """定时启停策略信息

    """

    def __init__(self):
        r"""
        :param ResumeTime: 定时拉起时间：如：周一8点
注意：此字段可能返回 null，表示取不到有效值。
        :type ResumeTime: str
        :param SuspendTime: 定时挂起时间：如：周一20点
注意：此字段可能返回 null，表示取不到有效值。
        :type SuspendTime: str
        :param SuspendStrategy: 挂起配置：0（默认）：等待任务结束后挂起、1：强制挂起
注意：此字段可能返回 null，表示取不到有效值。
        :type SuspendStrategy: int
        """
        self.ResumeTime = None
        self.SuspendTime = None
        self.SuspendStrategy = None


    def _deserialize(self, params):
        self.ResumeTime = params.get("ResumeTime")
        self.SuspendTime = params.get("SuspendTime")
        self.SuspendStrategy = params.get("SuspendStrategy")
        memeber_set = set(params.keys())
        for name, value in vars(self).items():
            if name in memeber_set:
                memeber_set.remove(name)
        if len(memeber_set) > 0:
            warnings.warn("%s fileds are useless." % ",".join(memeber_set))
        


class DLCCHDFSBinding(AbstractModel):
    """dlc引擎绑定桶列表

    """

    def __init__(self):
        r"""
        :param EngineId: 引擎Id
注意：此字段可能返回 null，表示取不到有效值。
        :type EngineId: str
        :param EngineName: 引擎名称
注意：此字段可能返回 null，表示取不到有效值。
        :type EngineName: str
        :param SuperUser: 用户名称（该字段已废弃）
注意：此字段可能返回 null，表示取不到有效值。
        :type SuperUser: list of str
        :param VpcInfo: vpc配置信息（该字段已废弃）
注意：此字段可能返回 null，表示取不到有效值。
        :type VpcInfo: list of CHDFSProductVpcInfo
        :param Permissions: 引擎绑定权限
注意：此字段可能返回 null，表示取不到有效值。
        :type Permissions: list of str
        :param IsBind: 是否与该桶绑定
注意：此字段可能返回 null，表示取不到有效值。
        :type IsBind: bool
        """
        self.EngineId = None
        self.EngineName = None
        self.SuperUser = None
        self.VpcInfo = None
        self.Permissions = None
        self.IsBind = None


    def _deserialize(self, params):
        self.EngineId = params.get("EngineId")
        self.EngineName = params.get("EngineName")
        self.SuperUser = params.get("SuperUser")
        if params.get("VpcInfo") is not None:
            self.VpcInfo = []
            for item in params.get("VpcInfo"):
                obj = CHDFSProductVpcInfo()
                obj._deserialize(item)
                self.VpcInfo.append(obj)
        self.Permissions = params.get("Permissions")
        self.IsBind = params.get("IsBind")
        memeber_set = set(params.keys())
        for name, value in vars(self).items():
            if name in memeber_set:
                memeber_set.remove(name)
        if len(memeber_set) > 0:
            warnings.warn("%s fileds are useless." % ",".join(memeber_set))
        


class DMSColumn(AbstractModel):
    """迁移列对象

    """

    def __init__(self):
        r"""
        :param Name: 名称
注意：此字段可能返回 null，表示取不到有效值。
        :type Name: str
        :param Description: 描述
注意：此字段可能返回 null，表示取不到有效值。
        :type Description: str
        :param Type: 类型
注意：此字段可能返回 null，表示取不到有效值。
        :type Type: str
        :param Position: 排序
注意：此字段可能返回 null，表示取不到有效值。
        :type Position: int
        :param Params: 附加参数
注意：此字段可能返回 null，表示取不到有效值。
        :type Params: list of KVPair
        :param BizParams: 业务参数
注意：此字段可能返回 null，表示取不到有效值。
        :type BizParams: list of KVPair
        :param IsPartition: 是否分区
注意：此字段可能返回 null，表示取不到有效值。
        :type IsPartition: bool
        """
        self.Name = None
        self.Description = None
        self.Type = None
        self.Position = None
        self.Params = None
        self.BizParams = None
        self.IsPartition = None


    def _deserialize(self, params):
        self.Name = params.get("Name")
        self.Description = params.get("Description")
        self.Type = params.get("Type")
        self.Position = params.get("Position")
        if params.get("Params") is not None:
            self.Params = []
            for item in params.get("Params"):
                obj = KVPair()
                obj._deserialize(item)
                self.Params.append(obj)
        if params.get("BizParams") is not None:
            self.BizParams = []
            for item in params.get("BizParams"):
                obj = KVPair()
                obj._deserialize(item)
                self.BizParams.append(obj)
        self.IsPartition = params.get("IsPartition")
        memeber_set = set(params.keys())
        for name, value in vars(self).items():
            if name in memeber_set:
                memeber_set.remove(name)
        if len(memeber_set) > 0:
            warnings.warn("%s fileds are useless." % ",".join(memeber_set))
        


class DMSColumnOrder(AbstractModel):
    """列排序对象

    """

    def __init__(self):
        r"""
        :param Col: 列名
注意：此字段可能返回 null，表示取不到有效值。
        :type Col: str
        :param Order: 排序
注意：此字段可能返回 null，表示取不到有效值。
        :type Order: int
        """
        self.Col = None
        self.Order = None


    def _deserialize(self, params):
        self.Col = params.get("Col")
        self.Order = params.get("Order")
        memeber_set = set(params.keys())
        for name, value in vars(self).items():
            if name in memeber_set:
                memeber_set.remove(name)
        if len(memeber_set) > 0:
            warnings.warn("%s fileds are useless." % ",".join(memeber_set))
        


class DMSColumnStatistic(AbstractModel):
    """DMS字段统计信息。

    """

    def __init__(self):
        r"""
        :param ColumnName: 字段名称
注意：此字段可能返回 null，表示取不到有效值。
        :type ColumnName: str
        :param ColumnType: 字段类型
注意：此字段可能返回 null，表示取不到有效值。
        :type ColumnType: str
        :param LongLowValue: Long类型最小值
注意：此字段可能返回 null，表示取不到有效值。
        :type LongLowValue: int
        :param LongHighValue: Long类型最大值
注意：此字段可能返回 null，表示取不到有效值。
        :type LongHighValue: int
        :param DoubleLowValue: Double类型最小值
注意：此字段可能返回 null，表示取不到有效值。
        :type DoubleLowValue: float
        :param DoubleHighValue: Double类型最大值
注意：此字段可能返回 null，表示取不到有效值。
        :type DoubleHighValue: float
        :param BigDecimalLowValue: Big Decimal 类型最小值
注意：此字段可能返回 null，表示取不到有效值。
        :type BigDecimalLowValue: str
        :param BigDecimalHighValue: Big Decimal 类型最大值
注意：此字段可能返回 null，表示取不到有效值。
        :type BigDecimalHighValue: str
        :param NumNulls: null字段值的个数
注意：此字段可能返回 null，表示取不到有效值。
        :type NumNulls: int
        :param NumDistinct: distinct字段值个数
注意：此字段可能返回 null，表示取不到有效值。
        :type NumDistinct: int
        :param AvgColLen: 1
注意：此字段可能返回 null，表示取不到有效值。
        :type AvgColLen: float
        :param MaxColLen: 字段值最大长度
注意：此字段可能返回 null，表示取不到有效值。
        :type MaxColLen: int
        :param NumTrues: 字段值为true的个数
注意：此字段可能返回 null，表示取不到有效值。
        :type NumTrues: int
        :param NumFalse: 字段值为false的个数
注意：此字段可能返回 null，表示取不到有效值。
        :type NumFalse: int
        :param Histogram: 直方图信息
注意：此字段可能返回 null，表示取不到有效值。
        :type Histogram: str
        :param CreateTime: 创建时间
注意：此字段可能返回 null，表示取不到有效值。
        :type CreateTime: str
        :param UpdateTime: 更新时间
注意：此字段可能返回 null，表示取不到有效值。
        :type UpdateTime: str
        """
        self.ColumnName = None
        self.ColumnType = None
        self.LongLowValue = None
        self.LongHighValue = None
        self.DoubleLowValue = None
        self.DoubleHighValue = None
        self.BigDecimalLowValue = None
        self.BigDecimalHighValue = None
        self.NumNulls = None
        self.NumDistinct = None
        self.AvgColLen = None
        self.MaxColLen = None
        self.NumTrues = None
        self.NumFalse = None
        self.Histogram = None
        self.CreateTime = None
        self.UpdateTime = None


    def _deserialize(self, params):
        self.ColumnName = params.get("ColumnName")
        self.ColumnType = params.get("ColumnType")
        self.LongLowValue = params.get("LongLowValue")
        self.LongHighValue = params.get("LongHighValue")
        self.DoubleLowValue = params.get("DoubleLowValue")
        self.DoubleHighValue = params.get("DoubleHighValue")
        self.BigDecimalLowValue = params.get("BigDecimalLowValue")
        self.BigDecimalHighValue = params.get("BigDecimalHighValue")
        self.NumNulls = params.get("NumNulls")
        self.NumDistinct = params.get("NumDistinct")
        self.AvgColLen = params.get("AvgColLen")
        self.MaxColLen = params.get("MaxColLen")
        self.NumTrues = params.get("NumTrues")
        self.NumFalse = params.get("NumFalse")
        self.Histogram = params.get("Histogram")
        self.CreateTime = params.get("CreateTime")
        self.UpdateTime = params.get("UpdateTime")
        memeber_set = set(params.keys())
        for name, value in vars(self).items():
            if name in memeber_set:
                memeber_set.remove(name)
        if len(memeber_set) > 0:
            warnings.warn("%s fileds are useless." % ",".join(memeber_set))
        


class DMSPartition(AbstractModel):
    """迁移元数据分区对象

    """

    def __init__(self):
        r"""
        :param DatabaseName: 数据库名称
        :type DatabaseName: str
        :param SchemaName: 数据目录名称
        :type SchemaName: str
        :param TableName: 表名称
        :type TableName: str
        :param DataVersion: 数据版本
        :type DataVersion: int
        :param Name: 分区名称
        :type Name: str
        :param Values: 值列表
        :type Values: list of str
        :param StorageSize: 存储大小
        :type StorageSize: int
        :param RecordCount: 记录数量
        :type RecordCount: int
        :param CreateTime: 创建时间
        :type CreateTime: str
        :param ModifiedTime: 修改时间
        :type ModifiedTime: str
        :param LastAccessTime: 最后访问时间
        :type LastAccessTime: str
        :param Params: 附件属性
        :type Params: list of KVPair
        :param Sds: 存储对象
        :type Sds: :class:`tencentcloud.dlc.v20210125.models.DMSSds`
        """
        self.DatabaseName = None
        self.SchemaName = None
        self.TableName = None
        self.DataVersion = None
        self.Name = None
        self.Values = None
        self.StorageSize = None
        self.RecordCount = None
        self.CreateTime = None
        self.ModifiedTime = None
        self.LastAccessTime = None
        self.Params = None
        self.Sds = None


    def _deserialize(self, params):
        self.DatabaseName = params.get("DatabaseName")
        self.SchemaName = params.get("SchemaName")
        self.TableName = params.get("TableName")
        self.DataVersion = params.get("DataVersion")
        self.Name = params.get("Name")
        self.Values = params.get("Values")
        self.StorageSize = params.get("StorageSize")
        self.RecordCount = params.get("RecordCount")
        self.CreateTime = params.get("CreateTime")
        self.ModifiedTime = params.get("ModifiedTime")
        self.LastAccessTime = params.get("LastAccessTime")
        if params.get("Params") is not None:
            self.Params = []
            for item in params.get("Params"):
                obj = KVPair()
                obj._deserialize(item)
                self.Params.append(obj)
        if params.get("Sds") is not None:
            self.Sds = DMSSds()
            self.Sds._deserialize(params.get("Sds"))
        memeber_set = set(params.keys())
        for name, value in vars(self).items():
            if name in memeber_set:
                memeber_set.remove(name)
        if len(memeber_set) > 0:
            warnings.warn("%s fileds are useless." % ",".join(memeber_set))
        


class DMSPartitionColumnStatisticInfo(AbstractModel):
    """DMS分区字段统计信息详情。

    """

    def __init__(self):
        r"""
        :param ColumnStatistic: 字段统计信息
        :type ColumnStatistic: :class:`tencentcloud.dlc.v20210125.models.DMSColumnStatistic`
        :param PartitionName: 分区名
注意：此字段可能返回 null，表示取不到有效值。
        :type PartitionName: str
        :param PartitionId: 分区编码
注意：此字段可能返回 null，表示取不到有效值。
        :type PartitionId: int
        :param DatabaseName: 库名
        :type DatabaseName: str
        :param TableName: 表名
        :type TableName: str
        """
        self.ColumnStatistic = None
        self.PartitionName = None
        self.PartitionId = None
        self.DatabaseName = None
        self.TableName = None


    def _deserialize(self, params):
        if params.get("ColumnStatistic") is not None:
            self.ColumnStatistic = DMSColumnStatistic()
            self.ColumnStatistic._deserialize(params.get("ColumnStatistic"))
        self.PartitionName = params.get("PartitionName")
        self.PartitionId = params.get("PartitionId")
        self.DatabaseName = params.get("DatabaseName")
        self.TableName = params.get("TableName")
        memeber_set = set(params.keys())
        for name, value in vars(self).items():
            if name in memeber_set:
                memeber_set.remove(name)
        if len(memeber_set) > 0:
            warnings.warn("%s fileds are useless." % ",".join(memeber_set))
        


class DMSSds(AbstractModel):
    """元数据存储描述属性

    """

    def __init__(self):
        r"""
        :param Location: 存储地址
注意：此字段可能返回 null，表示取不到有效值。
        :type Location: str
        :param InputFormat: 输入格式
注意：此字段可能返回 null，表示取不到有效值。
        :type InputFormat: str
        :param OutputFormat: 输出格式
注意：此字段可能返回 null，表示取不到有效值。
        :type OutputFormat: str
        :param NumBuckets: bucket数量
注意：此字段可能返回 null，表示取不到有效值。
        :type NumBuckets: int
        :param Compressed: 是是否压缩
注意：此字段可能返回 null，表示取不到有效值。
        :type Compressed: bool
        :param StoredAsSubDirectories: 是否有子目录
注意：此字段可能返回 null，表示取不到有效值。
        :type StoredAsSubDirectories: bool
        :param SerdeLib: 序列化lib
注意：此字段可能返回 null，表示取不到有效值。
        :type SerdeLib: str
        :param SerdeName: 序列化名称
注意：此字段可能返回 null，表示取不到有效值。
        :type SerdeName: str
        :param BucketCols: 桶名称
注意：此字段可能返回 null，表示取不到有效值。
        :type BucketCols: list of str
        :param SerdeParams: 序列化参数
注意：此字段可能返回 null，表示取不到有效值。
        :type SerdeParams: list of KVPair
        :param Params: 附加参数
注意：此字段可能返回 null，表示取不到有效值。
        :type Params: list of KVPair
        :param SortCols: 列排序(Expired)
注意：此字段可能返回 null，表示取不到有效值。
        :type SortCols: :class:`tencentcloud.dlc.v20210125.models.DMSColumnOrder`
        :param Cols: 列
注意：此字段可能返回 null，表示取不到有效值。
        :type Cols: list of DMSColumn
        :param SortColumns: 列排序字段
注意：此字段可能返回 null，表示取不到有效值。
        :type SortColumns: list of DMSColumnOrder
        """
        self.Location = None
        self.InputFormat = None
        self.OutputFormat = None
        self.NumBuckets = None
        self.Compressed = None
        self.StoredAsSubDirectories = None
        self.SerdeLib = None
        self.SerdeName = None
        self.BucketCols = None
        self.SerdeParams = None
        self.Params = None
        self.SortCols = None
        self.Cols = None
        self.SortColumns = None


    def _deserialize(self, params):
        self.Location = params.get("Location")
        self.InputFormat = params.get("InputFormat")
        self.OutputFormat = params.get("OutputFormat")
        self.NumBuckets = params.get("NumBuckets")
        self.Compressed = params.get("Compressed")
        self.StoredAsSubDirectories = params.get("StoredAsSubDirectories")
        self.SerdeLib = params.get("SerdeLib")
        self.SerdeName = params.get("SerdeName")
        self.BucketCols = params.get("BucketCols")
        if params.get("SerdeParams") is not None:
            self.SerdeParams = []
            for item in params.get("SerdeParams"):
                obj = KVPair()
                obj._deserialize(item)
                self.SerdeParams.append(obj)
        if params.get("Params") is not None:
            self.Params = []
            for item in params.get("Params"):
                obj = KVPair()
                obj._deserialize(item)
                self.Params.append(obj)
        if params.get("SortCols") is not None:
            self.SortCols = DMSColumnOrder()
            self.SortCols._deserialize(params.get("SortCols"))
        if params.get("Cols") is not None:
            self.Cols = []
            for item in params.get("Cols"):
                obj = DMSColumn()
                obj._deserialize(item)
                self.Cols.append(obj)
        if params.get("SortColumns") is not None:
            self.SortColumns = []
            for item in params.get("SortColumns"):
                obj = DMSColumnOrder()
                obj._deserialize(item)
                self.SortColumns.append(obj)
        memeber_set = set(params.keys())
        for name, value in vars(self).items():
            if name in memeber_set:
                memeber_set.remove(name)
        if len(memeber_set) > 0:
            warnings.warn("%s fileds are useless." % ",".join(memeber_set))
        


class DMSTable(AbstractModel):
    """DMSTable基本信息

    """

    def __init__(self):
        r"""
        :param ViewOriginalText: 视图文本
注意：此字段可能返回 null，表示取不到有效值。
        :type ViewOriginalText: str
        :param ViewExpandedText: 视图文本
注意：此字段可能返回 null，表示取不到有效值。
        :type ViewExpandedText: str
        :param Retention: hive维护版本
注意：此字段可能返回 null，表示取不到有效值。
        :type Retention: int
        :param Sds: 存储对象
注意：此字段可能返回 null，表示取不到有效值。
        :type Sds: :class:`tencentcloud.dlc.v20210125.models.DMSSds`
        :param PartitionKeys: 分区列
注意：此字段可能返回 null，表示取不到有效值。
        :type PartitionKeys: list of DMSColumn
        :param Partitions: 分区
注意：此字段可能返回 null，表示取不到有效值。
        :type Partitions: list of DMSPartition
        :param Type: 表类型
注意：此字段可能返回 null，表示取不到有效值。
        :type Type: str
        :param DbName: 数据库名称
注意：此字段可能返回 null，表示取不到有效值。
        :type DbName: str
        :param SchemaName: Schema名称
注意：此字段可能返回 null，表示取不到有效值。
        :type SchemaName: str
        :param StorageSize: 存储大小
注意：此字段可能返回 null，表示取不到有效值。
        :type StorageSize: int
        :param RecordCount: 记录数量
注意：此字段可能返回 null，表示取不到有效值。
        :type RecordCount: int
        :param LifeTime: 生命周期
注意：此字段可能返回 null，表示取不到有效值。
        :type LifeTime: int
        :param LastAccessTime: 最后访问时间
注意：此字段可能返回 null，表示取不到有效值。
        :type LastAccessTime: str
        :param DataUpdateTime: 数据更新时间
注意：此字段可能返回 null，表示取不到有效值。
        :type DataUpdateTime: str
        :param StructUpdateTime: 结构更新时间
注意：此字段可能返回 null，表示取不到有效值。
        :type StructUpdateTime: str
        :param Columns: 列
注意：此字段可能返回 null，表示取不到有效值。
        :type Columns: list of DMSColumn
        :param Name: 表名
注意：此字段可能返回 null，表示取不到有效值。
        :type Name: str
        """
        self.ViewOriginalText = None
        self.ViewExpandedText = None
        self.Retention = None
        self.Sds = None
        self.PartitionKeys = None
        self.Partitions = None
        self.Type = None
        self.DbName = None
        self.SchemaName = None
        self.StorageSize = None
        self.RecordCount = None
        self.LifeTime = None
        self.LastAccessTime = None
        self.DataUpdateTime = None
        self.StructUpdateTime = None
        self.Columns = None
        self.Name = None


    def _deserialize(self, params):
        self.ViewOriginalText = params.get("ViewOriginalText")
        self.ViewExpandedText = params.get("ViewExpandedText")
        self.Retention = params.get("Retention")
        if params.get("Sds") is not None:
            self.Sds = DMSSds()
            self.Sds._deserialize(params.get("Sds"))
        if params.get("PartitionKeys") is not None:
            self.PartitionKeys = []
            for item in params.get("PartitionKeys"):
                obj = DMSColumn()
                obj._deserialize(item)
                self.PartitionKeys.append(obj)
        if params.get("Partitions") is not None:
            self.Partitions = []
            for item in params.get("Partitions"):
                obj = DMSPartition()
                obj._deserialize(item)
                self.Partitions.append(obj)
        self.Type = params.get("Type")
        self.DbName = params.get("DbName")
        self.SchemaName = params.get("SchemaName")
        self.StorageSize = params.get("StorageSize")
        self.RecordCount = params.get("RecordCount")
        self.LifeTime = params.get("LifeTime")
        self.LastAccessTime = params.get("LastAccessTime")
        self.DataUpdateTime = params.get("DataUpdateTime")
        self.StructUpdateTime = params.get("StructUpdateTime")
        if params.get("Columns") is not None:
            self.Columns = []
            for item in params.get("Columns"):
                obj = DMSColumn()
                obj._deserialize(item)
                self.Columns.append(obj)
        self.Name = params.get("Name")
        memeber_set = set(params.keys())
        for name, value in vars(self).items():
            if name in memeber_set:
                memeber_set.remove(name)
        if len(memeber_set) > 0:
            warnings.warn("%s fileds are useless." % ",".join(memeber_set))
        


class DMSTableColumnStatisticInfo(AbstractModel):
    """DMS表字段统计信息详情。

    """

    def __init__(self):
        r"""
        :param ColumnStatistic: 字段统计信息
        :type ColumnStatistic: :class:`tencentcloud.dlc.v20210125.models.DMSColumnStatistic`
        :param DatabaseName: 库名
        :type DatabaseName: str
        :param TableName: 表名
        :type TableName: str
        """
        self.ColumnStatistic = None
        self.DatabaseName = None
        self.TableName = None


    def _deserialize(self, params):
        if params.get("ColumnStatistic") is not None:
            self.ColumnStatistic = DMSColumnStatistic()
            self.ColumnStatistic._deserialize(params.get("ColumnStatistic"))
        self.DatabaseName = params.get("DatabaseName")
        self.TableName = params.get("TableName")
        memeber_set = set(params.keys())
        for name, value in vars(self).items():
            if name in memeber_set:
                memeber_set.remove(name)
        if len(memeber_set) > 0:
            warnings.warn("%s fileds are useless." % ",".join(memeber_set))
        


class DMSTableInfo(AbstractModel):
    """DMSTable信息

    """

    def __init__(self):
        r"""
        :param Table: DMS表信息
注意：此字段可能返回 null，表示取不到有效值。
        :type Table: :class:`tencentcloud.dlc.v20210125.models.DMSTable`
        :param Asset: 基础对象信息
注意：此字段可能返回 null，表示取不到有效值。
        :type Asset: :class:`tencentcloud.dlc.v20210125.models.Asset`
        """
        self.Table = None
        self.Asset = None


    def _deserialize(self, params):
        if params.get("Table") is not None:
            self.Table = DMSTable()
            self.Table._deserialize(params.get("Table"))
        if params.get("Asset") is not None:
            self.Asset = Asset()
            self.Asset._deserialize(params.get("Asset"))
        memeber_set = set(params.keys())
        for name, value in vars(self).items():
            if name in memeber_set:
                memeber_set.remove(name)
        if len(memeber_set) > 0:
            warnings.warn("%s fileds are useless." % ",".join(memeber_set))
        


class DataEngineBasicInfo(AbstractModel):
    """DataEngine基本信息

    """

    def __init__(self):
        r"""
        :param DataEngineName: DataEngine名称
        :type DataEngineName: str
        :param State: 数据引擎状态  -2已删除 -1失败 0初始化中 1挂起 2运行中 3准备删除 4删除中
        :type State: int
        :param CreateTime: 创建时间
        :type CreateTime: int
        :param UpdateTime: 更新时间
        :type UpdateTime: int
        :param Message: 返回信息
注意：此字段可能返回 null，表示取不到有效值。
        :type Message: str
        :param DataEngineId: 引擎id
        :type DataEngineId: str
        :param DataEngineType: 引擎类型，有效值：PrestoSQL/SparkSQL/SparkBatch
注意：此字段可能返回 null，表示取不到有效值。
        :type DataEngineType: str
        :param AppId: 用户ID
注意：此字段可能返回 null，表示取不到有效值。
        :type AppId: int
        :param UserUin: 账号ID
注意：此字段可能返回 null，表示取不到有效值。
        :type UserUin: str
        """
        self.DataEngineName = None
        self.State = None
        self.CreateTime = None
        self.UpdateTime = None
        self.Message = None
        self.DataEngineId = None
        self.DataEngineType = None
        self.AppId = None
        self.UserUin = None


    def _deserialize(self, params):
        self.DataEngineName = params.get("DataEngineName")
        self.State = params.get("State")
        self.CreateTime = params.get("CreateTime")
        self.UpdateTime = params.get("UpdateTime")
        self.Message = params.get("Message")
        self.DataEngineId = params.get("DataEngineId")
        self.DataEngineType = params.get("DataEngineType")
        self.AppId = params.get("AppId")
        self.UserUin = params.get("UserUin")
        memeber_set = set(params.keys())
        for name, value in vars(self).items():
            if name in memeber_set:
                memeber_set.remove(name)
        if len(memeber_set) > 0:
            warnings.warn("%s fileds are useless." % ",".join(memeber_set))
        


class DataEngineConfigInstanceInfo(AbstractModel):
    """引擎配置信息

    """

    def __init__(self):
        r"""
        :param DataEngineId: 引擎ID
注意：此字段可能返回 null，表示取不到有效值。
        :type DataEngineId: str
        :param DataEngineConfigPairs: 用户自定义配置项集合
        :type DataEngineConfigPairs: list of DataEngineConfigPair
        :param SessionResourceTemplate: 作业集群资源参数配置模版
        :type SessionResourceTemplate: :class:`tencentcloud.dlc.v20210125.models.SessionResourceTemplate`
        """
        self.DataEngineId = None
        self.DataEngineConfigPairs = None
        self.SessionResourceTemplate = None


    def _deserialize(self, params):
        self.DataEngineId = params.get("DataEngineId")
        if params.get("DataEngineConfigPairs") is not None:
            self.DataEngineConfigPairs = []
            for item in params.get("DataEngineConfigPairs"):
                obj = DataEngineConfigPair()
                obj._deserialize(item)
                self.DataEngineConfigPairs.append(obj)
        if params.get("SessionResourceTemplate") is not None:
            self.SessionResourceTemplate = SessionResourceTemplate()
            self.SessionResourceTemplate._deserialize(params.get("SessionResourceTemplate"))
        memeber_set = set(params.keys())
        for name, value in vars(self).items():
            if name in memeber_set:
                memeber_set.remove(name)
        if len(memeber_set) > 0:
            warnings.warn("%s fileds are useless." % ",".join(memeber_set))
        


class DataEngineConfigPair(AbstractModel):
    """引擎配置

    """

    def __init__(self):
        r"""
        :param ConfigItem: 配置项
注意：此字段可能返回 null，表示取不到有效值。
        :type ConfigItem: str
        :param ConfigValue: 配置值
注意：此字段可能返回 null，表示取不到有效值。
        :type ConfigValue: str
        """
        self.ConfigItem = None
        self.ConfigValue = None


    def _deserialize(self, params):
        self.ConfigItem = params.get("ConfigItem")
        self.ConfigValue = params.get("ConfigValue")
        memeber_set = set(params.keys())
        for name, value in vars(self).items():
            if name in memeber_set:
                memeber_set.remove(name)
        if len(memeber_set) > 0:
            warnings.warn("%s fileds are useless." % ",".join(memeber_set))
        


class DataEngineImageSessionParameter(AbstractModel):
    """集群Session配置信息.

    """

    def __init__(self):
        r"""
        :param ParameterId: 配置id
        :type ParameterId: str
        :param ChildImageVersionId: 小版本镜像ID
        :type ChildImageVersionId: str
        :param EngineType: 集群类型：SparkSQL/PrestoSQL/SparkBatch
        :type EngineType: str
        :param KeyName: 参数key
        :type KeyName: str
        :param KeyDescription: Key描述信息
注意：此字段可能返回 null，表示取不到有效值。
        :type KeyDescription: str
        :param ValueType: value类型
        :type ValueType: str
        :param ValueLengthLimit: value长度限制
注意：此字段可能返回 null，表示取不到有效值。
        :type ValueLengthLimit: str
        :param ValueRegexpLimit: value正则限制
注意：此字段可能返回 null，表示取不到有效值。
        :type ValueRegexpLimit: str
        :param ValueDefault: value默认值
注意：此字段可能返回 null，表示取不到有效值。
        :type ValueDefault: str
        :param IsPublic: 是否为公共版本：1：公共；2：私有
        :type IsPublic: int
        :param ParameterType: 配置类型：1：session配置（默认）；2：common配置；3：cluster配置
        :type ParameterType: int
        :param SubmitMethod: 提交方式：User(用户)、BackGround（后台）
        :type SubmitMethod: str
        :param Operator: 操作者
注意：此字段可能返回 null，表示取不到有效值。
        :type Operator: str
        :param InsertTime: 插入时间
        :type InsertTime: str
        :param UpdateTime: 更新时间
        :type UpdateTime: str
        """
        self.ParameterId = None
        self.ChildImageVersionId = None
        self.EngineType = None
        self.KeyName = None
        self.KeyDescription = None
        self.ValueType = None
        self.ValueLengthLimit = None
        self.ValueRegexpLimit = None
        self.ValueDefault = None
        self.IsPublic = None
        self.ParameterType = None
        self.SubmitMethod = None
        self.Operator = None
        self.InsertTime = None
        self.UpdateTime = None


    def _deserialize(self, params):
        self.ParameterId = params.get("ParameterId")
        self.ChildImageVersionId = params.get("ChildImageVersionId")
        self.EngineType = params.get("EngineType")
        self.KeyName = params.get("KeyName")
        self.KeyDescription = params.get("KeyDescription")
        self.ValueType = params.get("ValueType")
        self.ValueLengthLimit = params.get("ValueLengthLimit")
        self.ValueRegexpLimit = params.get("ValueRegexpLimit")
        self.ValueDefault = params.get("ValueDefault")
        self.IsPublic = params.get("IsPublic")
        self.ParameterType = params.get("ParameterType")
        self.SubmitMethod = params.get("SubmitMethod")
        self.Operator = params.get("Operator")
        self.InsertTime = params.get("InsertTime")
        self.UpdateTime = params.get("UpdateTime")
        memeber_set = set(params.keys())
        for name, value in vars(self).items():
            if name in memeber_set:
                memeber_set.remove(name)
        if len(memeber_set) > 0:
            warnings.warn("%s fileds are useless." % ",".join(memeber_set))
        


class DataEngineImageVersion(AbstractModel):
    """集群大版本镜像信息。

    """

    def __init__(self):
        r"""
        :param ImageVersionId: 镜像大版本ID
        :type ImageVersionId: str
        :param ImageVersion: 镜像大版本名称
        :type ImageVersion: str
        :param Description: 镜像大版本描述
注意：此字段可能返回 null，表示取不到有效值。
        :type Description: str
        :param IsPublic: 是否为公共版本：1：公共；2：私有
        :type IsPublic: int
        :param EngineType: 集群类型：SparkSQL/PrestoSQL/SparkBatch
        :type EngineType: str
        :param IsSharedEngine: 版本状态：1：初始化；2：上线；3：下线
        :type IsSharedEngine: int
        :param State: 版本状态：1：初始化；2：上线；3：下线
        :type State: int
        :param InsertTime: 插入时间
        :type InsertTime: str
        :param UpdateTime: 更新时间
        :type UpdateTime: str
        """
        self.ImageVersionId = None
        self.ImageVersion = None
        self.Description = None
        self.IsPublic = None
        self.EngineType = None
        self.IsSharedEngine = None
        self.State = None
        self.InsertTime = None
        self.UpdateTime = None


    def _deserialize(self, params):
        self.ImageVersionId = params.get("ImageVersionId")
        self.ImageVersion = params.get("ImageVersion")
        self.Description = params.get("Description")
        self.IsPublic = params.get("IsPublic")
        self.EngineType = params.get("EngineType")
        self.IsSharedEngine = params.get("IsSharedEngine")
        self.State = params.get("State")
        self.InsertTime = params.get("InsertTime")
        self.UpdateTime = params.get("UpdateTime")
        memeber_set = set(params.keys())
        for name, value in vars(self).items():
            if name in memeber_set:
                memeber_set.remove(name)
        if len(memeber_set) > 0:
            warnings.warn("%s fileds are useless." % ",".join(memeber_set))
        


class DataEngineInfo(AbstractModel):
    """DataEngine详细信息

    """

    def __init__(self):
        r"""
        :param DataEngineName: DataEngine名称
        :type DataEngineName: str
        :param EngineType: 引擎类型 spark/presto
        :type EngineType: str
        :param ClusterType: 集群资源类型 spark_private/presto_private/presto_cu/spark_cu
        :type ClusterType: str
        :param Id: 主键
        :type Id: int
        :param QuotaId: 引用ID
        :type QuotaId: str
        :param State: 数据引擎状态  -2已删除 -1失败 0初始化中 1挂起 2运行中 3准备删除 4删除中
        :type State: int
        :param CreateTime: 创建时间
        :type CreateTime: int
        :param UpdateTime: 更新时间
        :type UpdateTime: int
        :param Size: 集群规格
注意：此字段可能返回 null，表示取不到有效值。
        :type Size: int
        :param Mode: 计费模式 0共享模式 1按量计费 2包年包月
        :type Mode: int
        :param MinClusters: 最小集群数
注意：此字段可能返回 null，表示取不到有效值。
        :type MinClusters: int
        :param MaxClusters: 最大集群数
注意：此字段可能返回 null，表示取不到有效值。
        :type MaxClusters: int
        :param AutoResume: 是否自动恢复
注意：此字段可能返回 null，表示取不到有效值。
        :type AutoResume: bool
        :param SpendAfter: 自动恢复时间
注意：此字段可能返回 null，表示取不到有效值。
        :type SpendAfter: int
        :param VpcInfo: vpc信息
注意：此字段可能返回 null，表示取不到有效值。
        :type VpcInfo: str
        :param CidrBlock: 集群网段
注意：此字段可能返回 null，表示取不到有效值。
        :type CidrBlock: str
        :param ServiceType: 服务类型
        :type ServiceType: str
        :param DefaultDataEngine: 是否为默认引擎
注意：此字段可能返回 null，表示取不到有效值。
        :type DefaultDataEngine: bool
        :param Message: 返回信息
注意：此字段可能返回 null，表示取不到有效值。
        :type Message: str
        :param DataEngineId: 引擎id
        :type DataEngineId: str
        :param SubAccountUin: 操作者
        :type SubAccountUin: str
        :param ExpireTime: 到期时间
        :type ExpireTime: str
        :param IsolatedTime: 隔离时间
        :type IsolatedTime: str
        :param ReversalTime: 冲正时间
        :type ReversalTime: str
        :param UserAlias: 用户名称
注意：此字段可能返回 null，表示取不到有效值。
        :type UserAlias: str
        :param TagList: 标签对集合
注意：此字段可能返回 null，表示取不到有效值。
        :type TagList: list of TagInfo
        :param Permissions: 引擎拥有的权限
注意：此字段可能返回 null，表示取不到有效值。
        :type Permissions: list of str
        :param AutoSuspend: 是否自定挂起集群：false（默认）：不自动挂起、true：自动挂起
注意：此字段可能返回 null，表示取不到有效值。
        :type AutoSuspend: bool
        :param CrontabResumeSuspend: 定时启停集群策略：0（默认）：关闭定时策略、1：开启定时策略（注：定时启停策略与自动挂起策略互斥）
注意：此字段可能返回 null，表示取不到有效值。
        :type CrontabResumeSuspend: int
        :param CrontabResumeSuspendStrategy: 定时启停策略，复杂类型：包含启停时间、挂起集群策略
注意：此字段可能返回 null，表示取不到有效值。
        :type CrontabResumeSuspendStrategy: :class:`tencentcloud.dlc.v20210125.models.CrontabResumeSuspendStrategy`
        :param EngineExecType: 引擎执行任务类型，有效值：SQL/BATCH
注意：此字段可能返回 null，表示取不到有效值。
        :type EngineExecType: str
        :param RenewFlag: 自动续费标志，0，初始状态，默认不自动续费，若用户有预付费不停服特权，自动续费。1：自动续费。2：明确不自动续费
注意：此字段可能返回 null，表示取不到有效值。
        :type RenewFlag: int
        :param AutoSuspendTime: 集群自动挂起时间
注意：此字段可能返回 null，表示取不到有效值。
        :type AutoSuspendTime: int
        :param NetworkConnectionSet: 网络连接配置
注意：此字段可能返回 null，表示取不到有效值。
        :type NetworkConnectionSet: list of NetworkConnection
        :param UiURL: ui的跳转地址
注意：此字段可能返回 null，表示取不到有效值。
        :type UiURL: str
        :param ResourceType: 引擎的资源类型
注意：此字段可能返回 null，表示取不到有效值。
        :type ResourceType: str
        :param ImageVersionId: 集群镜像版本ID
注意：此字段可能返回 null，表示取不到有效值。
        :type ImageVersionId: str
        :param ChildImageVersionId: 集群镜像小版本ID
注意：此字段可能返回 null，表示取不到有效值。
        :type ChildImageVersionId: str
        :param ImageVersionName: 集群镜像版本名字
注意：此字段可能返回 null，表示取不到有效值。
        :type ImageVersionName: str
        :param StartStandbyCluster: 是否开启备集群
注意：此字段可能返回 null，表示取不到有效值。
        :type StartStandbyCluster: bool
        :param ElasticSwitch: spark jar 包年包月集群是否开启弹性
注意：此字段可能返回 null，表示取不到有效值。
        :type ElasticSwitch: bool
        :param ElasticLimit: spark jar 包年包月集群弹性上限
注意：此字段可能返回 null，表示取不到有效值。
        :type ElasticLimit: int
        :param DefaultHouse: 是否为默认引擎
注意：此字段可能返回 null，表示取不到有效值。
        :type DefaultHouse: bool
        :param MaxConcurrency: 单个集群任务最大并发数
注意：此字段可能返回 null，表示取不到有效值。
        :type MaxConcurrency: int
        :param TolerableQueueTime: 任务排队上限时间
注意：此字段可能返回 null，表示取不到有效值。
        :type TolerableQueueTime: int
        :param UserAppId: 用户appid
注意：此字段可能返回 null，表示取不到有效值。
        :type UserAppId: int
        :param UserUin: 用户uin
注意：此字段可能返回 null，表示取不到有效值。
        :type UserUin: str
        :param SessionResourceTemplate: SessionResourceTemplate
注意：此字段可能返回 null，表示取不到有效值。
        :type SessionResourceTemplate: :class:`tencentcloud.dlc.v20210125.models.SessionResourceTemplate`
        """
        self.DataEngineName = None
        self.EngineType = None
        self.ClusterType = None
        self.Id = None
        self.QuotaId = None
        self.State = None
        self.CreateTime = None
        self.UpdateTime = None
        self.Size = None
        self.Mode = None
        self.MinClusters = None
        self.MaxClusters = None
        self.AutoResume = None
        self.SpendAfter = None
        self.VpcInfo = None
        self.CidrBlock = None
        self.ServiceType = None
        self.DefaultDataEngine = None
        self.Message = None
        self.DataEngineId = None
        self.SubAccountUin = None
        self.ExpireTime = None
        self.IsolatedTime = None
        self.ReversalTime = None
        self.UserAlias = None
        self.TagList = None
        self.Permissions = None
        self.AutoSuspend = None
        self.CrontabResumeSuspend = None
        self.CrontabResumeSuspendStrategy = None
        self.EngineExecType = None
        self.RenewFlag = None
        self.AutoSuspendTime = None
        self.NetworkConnectionSet = None
        self.UiURL = None
        self.ResourceType = None
        self.ImageVersionId = None
        self.ChildImageVersionId = None
        self.ImageVersionName = None
        self.StartStandbyCluster = None
        self.ElasticSwitch = None
        self.ElasticLimit = None
        self.DefaultHouse = None
        self.MaxConcurrency = None
        self.TolerableQueueTime = None
        self.UserAppId = None
        self.UserUin = None
        self.SessionResourceTemplate = None


    def _deserialize(self, params):
        self.DataEngineName = params.get("DataEngineName")
        self.EngineType = params.get("EngineType")
        self.ClusterType = params.get("ClusterType")
        self.Id = params.get("Id")
        self.QuotaId = params.get("QuotaId")
        self.State = params.get("State")
        self.CreateTime = params.get("CreateTime")
        self.UpdateTime = params.get("UpdateTime")
        self.Size = params.get("Size")
        self.Mode = params.get("Mode")
        self.MinClusters = params.get("MinClusters")
        self.MaxClusters = params.get("MaxClusters")
        self.AutoResume = params.get("AutoResume")
        self.SpendAfter = params.get("SpendAfter")
        self.VpcInfo = params.get("VpcInfo")
        self.CidrBlock = params.get("CidrBlock")
        self.ServiceType = params.get("ServiceType")
        self.DefaultDataEngine = params.get("DefaultDataEngine")
        self.Message = params.get("Message")
        self.DataEngineId = params.get("DataEngineId")
        self.SubAccountUin = params.get("SubAccountUin")
        self.ExpireTime = params.get("ExpireTime")
        self.IsolatedTime = params.get("IsolatedTime")
        self.ReversalTime = params.get("ReversalTime")
        self.UserAlias = params.get("UserAlias")
        if params.get("TagList") is not None:
            self.TagList = []
            for item in params.get("TagList"):
                obj = TagInfo()
                obj._deserialize(item)
                self.TagList.append(obj)
        self.Permissions = params.get("Permissions")
        self.AutoSuspend = params.get("AutoSuspend")
        self.CrontabResumeSuspend = params.get("CrontabResumeSuspend")
        if params.get("CrontabResumeSuspendStrategy") is not None:
            self.CrontabResumeSuspendStrategy = CrontabResumeSuspendStrategy()
            self.CrontabResumeSuspendStrategy._deserialize(params.get("CrontabResumeSuspendStrategy"))
        self.EngineExecType = params.get("EngineExecType")
        self.RenewFlag = params.get("RenewFlag")
        self.AutoSuspendTime = params.get("AutoSuspendTime")
        if params.get("NetworkConnectionSet") is not None:
            self.NetworkConnectionSet = []
            for item in params.get("NetworkConnectionSet"):
                obj = NetworkConnection()
                obj._deserialize(item)
                self.NetworkConnectionSet.append(obj)
        self.UiURL = params.get("UiURL")
        self.ResourceType = params.get("ResourceType")
        self.ImageVersionId = params.get("ImageVersionId")
        self.ChildImageVersionId = params.get("ChildImageVersionId")
        self.ImageVersionName = params.get("ImageVersionName")
        self.StartStandbyCluster = params.get("StartStandbyCluster")
        self.ElasticSwitch = params.get("ElasticSwitch")
        self.ElasticLimit = params.get("ElasticLimit")
        self.DefaultHouse = params.get("DefaultHouse")
        self.MaxConcurrency = params.get("MaxConcurrency")
        self.TolerableQueueTime = params.get("TolerableQueueTime")
        self.UserAppId = params.get("UserAppId")
        self.UserUin = params.get("UserUin")
        if params.get("SessionResourceTemplate") is not None:
            self.SessionResourceTemplate = SessionResourceTemplate()
            self.SessionResourceTemplate._deserialize(params.get("SessionResourceTemplate"))
        memeber_set = set(params.keys())
        for name, value in vars(self).items():
            if name in memeber_set:
                memeber_set.remove(name)
        if len(memeber_set) > 0:
            warnings.warn("%s fileds are useless." % ",".join(memeber_set))
        


class DataEngineRefundMessage(AbstractModel):
    """引擎退费信息

    """

    def __init__(self):
        r"""
        :param DataEngineName: 引擎名称
注意：此字段可能返回 null，表示取不到有效值。
        :type DataEngineName: str
        :param RefundAmount: 退费金额，单位为元
注意：此字段可能返回 null，表示取不到有效值。
        :type RefundAmount: float
        """
        self.DataEngineName = None
        self.RefundAmount = None


    def _deserialize(self, params):
        self.DataEngineName = params.get("DataEngineName")
        self.RefundAmount = params.get("RefundAmount")
        memeber_set = set(params.keys())
        for name, value in vars(self).items():
            if name in memeber_set:
                memeber_set.remove(name)
        if len(memeber_set) > 0:
            warnings.warn("%s fileds are useless." % ",".join(memeber_set))
        


class DataFormat(AbstractModel):
    """数据表数据格式。

    """

    def __init__(self):
        r"""
        :param TextFile: 文本格式，TextFile。
注意：此字段可能返回 null，表示取不到有效值。
        :type TextFile: :class:`tencentcloud.dlc.v20210125.models.TextFile`
        :param CSV: 文本格式，CSV。
注意：此字段可能返回 null，表示取不到有效值。
        :type CSV: :class:`tencentcloud.dlc.v20210125.models.CSV`
        :param Json: 文本格式，Json。
注意：此字段可能返回 null，表示取不到有效值。
        :type Json: :class:`tencentcloud.dlc.v20210125.models.Other`
        :param Parquet: Parquet格式
注意：此字段可能返回 null，表示取不到有效值。
        :type Parquet: :class:`tencentcloud.dlc.v20210125.models.Other`
        :param ORC: ORC格式
注意：此字段可能返回 null，表示取不到有效值。
        :type ORC: :class:`tencentcloud.dlc.v20210125.models.Other`
        :param AVRO: AVRO格式
注意：此字段可能返回 null，表示取不到有效值。
        :type AVRO: :class:`tencentcloud.dlc.v20210125.models.Other`
        """
        self.TextFile = None
        self.CSV = None
        self.Json = None
        self.Parquet = None
        self.ORC = None
        self.AVRO = None


    def _deserialize(self, params):
        if params.get("TextFile") is not None:
            self.TextFile = TextFile()
            self.TextFile._deserialize(params.get("TextFile"))
        if params.get("CSV") is not None:
            self.CSV = CSV()
            self.CSV._deserialize(params.get("CSV"))
        if params.get("Json") is not None:
            self.Json = Other()
            self.Json._deserialize(params.get("Json"))
        if params.get("Parquet") is not None:
            self.Parquet = Other()
            self.Parquet._deserialize(params.get("Parquet"))
        if params.get("ORC") is not None:
            self.ORC = Other()
            self.ORC._deserialize(params.get("ORC"))
        if params.get("AVRO") is not None:
            self.AVRO = Other()
            self.AVRO._deserialize(params.get("AVRO"))
        memeber_set = set(params.keys())
        for name, value in vars(self).items():
            if name in memeber_set:
                memeber_set.remove(name)
        if len(memeber_set) > 0:
            warnings.warn("%s fileds are useless." % ",".join(memeber_set))
        


class DataGovernPolicy(AbstractModel):
    """数据治理规则

    """

    def __init__(self):
        r"""
        :param RewriteDataPolicy: 数据排布治理项
注意：此字段可能返回 null，表示取不到有效值。
        :type RewriteDataPolicy: :class:`tencentcloud.dlc.v20210125.models.RewriteDataInfo`
        :param ExpiredSnapshotsPolicy: 快照过期治理项
注意：此字段可能返回 null，表示取不到有效值。
        :type ExpiredSnapshotsPolicy: :class:`tencentcloud.dlc.v20210125.models.ExpiredSnapshotsInfo`
        :param RemoveOrphanFilesPolicy: 移除孤立文件治理项
注意：此字段可能返回 null，表示取不到有效值。
        :type RemoveOrphanFilesPolicy: :class:`tencentcloud.dlc.v20210125.models.RemoveOrphanFilesInfo`
        :param MergeManifestsPolicy: 合并元数据Manifests治理项
注意：此字段可能返回 null，表示取不到有效值。
        :type MergeManifestsPolicy: :class:`tencentcloud.dlc.v20210125.models.MergeManifestsInfo`
        :param InheritDataBase: 是否集成库规则：default（默认继承）、none（不继承）
注意：此字段可能返回 null，表示取不到有效值。
        :type InheritDataBase: str
        :param RuleType: 治理规则类型，Customize: 自定义；Intelligence: 智能治理
注意：此字段可能返回 null，表示取不到有效值。
        :type RuleType: str
        :param GovernEngine: 治理引擎
注意：此字段可能返回 null，表示取不到有效值。
        :type GovernEngine: str
        """
        self.RewriteDataPolicy = None
        self.ExpiredSnapshotsPolicy = None
        self.RemoveOrphanFilesPolicy = None
        self.MergeManifestsPolicy = None
        self.InheritDataBase = None
        self.RuleType = None
        self.GovernEngine = None


    def _deserialize(self, params):
        if params.get("RewriteDataPolicy") is not None:
            self.RewriteDataPolicy = RewriteDataInfo()
            self.RewriteDataPolicy._deserialize(params.get("RewriteDataPolicy"))
        if params.get("ExpiredSnapshotsPolicy") is not None:
            self.ExpiredSnapshotsPolicy = ExpiredSnapshotsInfo()
            self.ExpiredSnapshotsPolicy._deserialize(params.get("ExpiredSnapshotsPolicy"))
        if params.get("RemoveOrphanFilesPolicy") is not None:
            self.RemoveOrphanFilesPolicy = RemoveOrphanFilesInfo()
            self.RemoveOrphanFilesPolicy._deserialize(params.get("RemoveOrphanFilesPolicy"))
        if params.get("MergeManifestsPolicy") is not None:
            self.MergeManifestsPolicy = MergeManifestsInfo()
            self.MergeManifestsPolicy._deserialize(params.get("MergeManifestsPolicy"))
        self.InheritDataBase = params.get("InheritDataBase")
        self.RuleType = params.get("RuleType")
        self.GovernEngine = params.get("GovernEngine")
        memeber_set = set(params.keys())
        for name, value in vars(self).items():
            if name in memeber_set:
                memeber_set.remove(name)
        if len(memeber_set) > 0:
            warnings.warn("%s fileds are useless." % ",".join(memeber_set))
        


class DataQuery(AbstractModel):
    """数据查询实例

    """

    def __init__(self):
        r"""
        :param Name: 数据查询名称
        :type Name: str
        :param Id: 数据查询ID
        :type Id: str
        :param Statement: base64编码后的sql语句
        :type Statement: str
        :param Params: base64编码后的参数清单
        :type Params: str
        :param CreateTime: 创建时间
        :type CreateTime: int
        :param UpdateTime: 更新时间
        :type UpdateTime: int
        """
        self.Name = None
        self.Id = None
        self.Statement = None
        self.Params = None
        self.CreateTime = None
        self.UpdateTime = None


    def _deserialize(self, params):
        self.Name = params.get("Name")
        self.Id = params.get("Id")
        self.Statement = params.get("Statement")
        self.Params = params.get("Params")
        self.CreateTime = params.get("CreateTime")
        self.UpdateTime = params.get("UpdateTime")
        memeber_set = set(params.keys())
        for name, value in vars(self).items():
            if name in memeber_set:
                memeber_set.remove(name)
        if len(memeber_set) > 0:
            warnings.warn("%s fileds are useless." % ",".join(memeber_set))
        


class DataQueryDir(AbstractModel):
    """数据查询实例

    """

    def __init__(self):
        r"""
        :param Name: 目录名称
        :type Name: str
        :param CreateTime: 目录创建时间
        :type CreateTime: int
        """
        self.Name = None
        self.CreateTime = None


    def _deserialize(self, params):
        self.Name = params.get("Name")
        self.CreateTime = params.get("CreateTime")
        memeber_set = set(params.keys())
        for name, value in vars(self).items():
            if name in memeber_set:
                memeber_set.remove(name)
        if len(memeber_set) > 0:
            warnings.warn("%s fileds are useless." % ",".join(memeber_set))
        


class DataSourceInfo(AbstractModel):
    """数据源详细信息

    """

    def __init__(self):
        r"""
        :param InstanceId: 数据源实例的唯一ID
注意：此字段可能返回 null，表示取不到有效值。
        :type InstanceId: str
        :param InstanceName: 数据源的名称
注意：此字段可能返回 null，表示取不到有效值。
        :type InstanceName: str
        :param JdbcUrl: 数据源的JDBC访问链接
注意：此字段可能返回 null，表示取不到有效值。
        :type JdbcUrl: str
        :param User: 用于访问数据源的用户名
注意：此字段可能返回 null，表示取不到有效值。
        :type User: str
        :param Password: 数据源访问密码，需要base64编码
注意：此字段可能返回 null，表示取不到有效值。
        :type Password: str
        :param Location: 数据源的VPC和子网信息
注意：此字段可能返回 null，表示取不到有效值。
        :type Location: :class:`tencentcloud.dlc.v20210125.models.DatasourceConnectionLocation`
        :param DbName: 默认数据库名
注意：此字段可能返回 null，表示取不到有效值。
        :type DbName: str
        """
        self.InstanceId = None
        self.InstanceName = None
        self.JdbcUrl = None
        self.User = None
        self.Password = None
        self.Location = None
        self.DbName = None


    def _deserialize(self, params):
        self.InstanceId = params.get("InstanceId")
        self.InstanceName = params.get("InstanceName")
        self.JdbcUrl = params.get("JdbcUrl")
        self.User = params.get("User")
        self.Password = params.get("Password")
        if params.get("Location") is not None:
            self.Location = DatasourceConnectionLocation()
            self.Location._deserialize(params.get("Location"))
        self.DbName = params.get("DbName")
        memeber_set = set(params.keys())
        for name, value in vars(self).items():
            if name in memeber_set:
                memeber_set.remove(name)
        if len(memeber_set) > 0:
            warnings.warn("%s fileds are useless." % ",".join(memeber_set))
        


class DatabaseInfo(AbstractModel):
    """数据库对象

    """

    def __init__(self):
        r"""
        :param DatabaseName: 数据库名称，长度0~128，支持数字、字母下划线，不允许数字大头，统一转换为小写。
        :type DatabaseName: str
        :param Comment: 数据库描述信息，长度 0~500。
注意：此字段可能返回 null，表示取不到有效值。
        :type Comment: str
        :param Properties: 数据库属性列表。
注意：此字段可能返回 null，表示取不到有效值。
        :type Properties: list of Property
        :param Location: 数据库cos路径
注意：此字段可能返回 null，表示取不到有效值。
        :type Location: str
        """
        self.DatabaseName = None
        self.Comment = None
        self.Properties = None
        self.Location = None


    def _deserialize(self, params):
        self.DatabaseName = params.get("DatabaseName")
        self.Comment = params.get("Comment")
        if params.get("Properties") is not None:
            self.Properties = []
            for item in params.get("Properties"):
                obj = Property()
                obj._deserialize(item)
                self.Properties.append(obj)
        self.Location = params.get("Location")
        memeber_set = set(params.keys())
        for name, value in vars(self).items():
            if name in memeber_set:
                memeber_set.remove(name)
        if len(memeber_set) > 0:
            warnings.warn("%s fileds are useless." % ",".join(memeber_set))
        


class DatabaseResponseInfo(AbstractModel):
    """数据库对象

    """

    def __init__(self):
        r"""
        :param DatabaseName: 数据库名称。
        :type DatabaseName: str
        :param Comment: 数据库描述信息，长度 0~256。
注意：此字段可能返回 null，表示取不到有效值。
        :type Comment: str
        :param Properties: 允许针对数据库的属性元数据信息进行指定。
注意：此字段可能返回 null，表示取不到有效值。
        :type Properties: list of Property
        :param CreateTime: 数据库创建时间戳，单位：s。
注意：此字段可能返回 null，表示取不到有效值。
        :type CreateTime: str
        :param ModifiedTime: 数据库更新时间戳，单位：s。
注意：此字段可能返回 null，表示取不到有效值。
        :type ModifiedTime: str
        :param Location: cos存储路径
注意：此字段可能返回 null，表示取不到有效值。
        :type Location: str
        :param UserAlias: 建库用户昵称
注意：此字段可能返回 null，表示取不到有效值。
        :type UserAlias: str
        :param UserSubUin: 建库用户ID
注意：此字段可能返回 null，表示取不到有效值。
        :type UserSubUin: str
        :param GovernPolicy: 数据治理配置项
注意：此字段可能返回 null，表示取不到有效值。
        :type GovernPolicy: :class:`tencentcloud.dlc.v20210125.models.DataGovernPolicy`
        :param DatabaseId: 数据库ID（无效字段）
注意：此字段可能返回 null，表示取不到有效值。
        :type DatabaseId: str
        """
        self.DatabaseName = None
        self.Comment = None
        self.Properties = None
        self.CreateTime = None
        self.ModifiedTime = None
        self.Location = None
        self.UserAlias = None
        self.UserSubUin = None
        self.GovernPolicy = None
        self.DatabaseId = None


    def _deserialize(self, params):
        self.DatabaseName = params.get("DatabaseName")
        self.Comment = params.get("Comment")
        if params.get("Properties") is not None:
            self.Properties = []
            for item in params.get("Properties"):
                obj = Property()
                obj._deserialize(item)
                self.Properties.append(obj)
        self.CreateTime = params.get("CreateTime")
        self.ModifiedTime = params.get("ModifiedTime")
        self.Location = params.get("Location")
        self.UserAlias = params.get("UserAlias")
        self.UserSubUin = params.get("UserSubUin")
        if params.get("GovernPolicy") is not None:
            self.GovernPolicy = DataGovernPolicy()
            self.GovernPolicy._deserialize(params.get("GovernPolicy"))
        self.DatabaseId = params.get("DatabaseId")
        memeber_set = set(params.keys())
        for name, value in vars(self).items():
            if name in memeber_set:
                memeber_set.remove(name)
        if len(memeber_set) > 0:
            warnings.warn("%s fileds are useless." % ",".join(memeber_set))
        


class DatasourceConnectionConfig(AbstractModel):
    """数据源属性

    """

    def __init__(self):
        r"""
        :param Mysql: Mysql数据源连接的属性
注意：此字段可能返回 null，表示取不到有效值。
        :type Mysql: :class:`tencentcloud.dlc.v20210125.models.MysqlInfo`
        :param Hive: Hive数据源连接的属性
注意：此字段可能返回 null，表示取不到有效值。
        :type Hive: :class:`tencentcloud.dlc.v20210125.models.HiveInfo`
        :param Kafka: Kafka数据源连接的属性
注意：此字段可能返回 null，表示取不到有效值。
        :type Kafka: :class:`tencentcloud.dlc.v20210125.models.KafkaInfo`
        :param OtherDatasourceConnection: 其他数据源连接的属性
注意：此字段可能返回 null，表示取不到有效值。
        :type OtherDatasourceConnection: :class:`tencentcloud.dlc.v20210125.models.OtherDatasourceConnection`
        :param PostgreSql: PostgreSQL数据源连接的属性
注意：此字段可能返回 null，表示取不到有效值。
        :type PostgreSql: :class:`tencentcloud.dlc.v20210125.models.DataSourceInfo`
        :param SqlServer: SQLServer数据源连接的属性
注意：此字段可能返回 null，表示取不到有效值。
        :type SqlServer: :class:`tencentcloud.dlc.v20210125.models.DataSourceInfo`
        :param ClickHouse: ClickHouse数据源连接的属性
注意：此字段可能返回 null，表示取不到有效值。
        :type ClickHouse: :class:`tencentcloud.dlc.v20210125.models.DataSourceInfo`
        :param Elasticsearch: Elasticsearch数据源连接的属性
注意：此字段可能返回 null，表示取不到有效值。
        :type Elasticsearch: :class:`tencentcloud.dlc.v20210125.models.ElasticsearchInfo`
        :param TDSQLPostgreSql: TDSQL-PostgreSQL数据源连接的属性
注意：此字段可能返回 null，表示取不到有效值。
        :type TDSQLPostgreSql: :class:`tencentcloud.dlc.v20210125.models.DataSourceInfo`
        """
        self.Mysql = None
        self.Hive = None
        self.Kafka = None
        self.OtherDatasourceConnection = None
        self.PostgreSql = None
        self.SqlServer = None
        self.ClickHouse = None
        self.Elasticsearch = None
        self.TDSQLPostgreSql = None


    def _deserialize(self, params):
        if params.get("Mysql") is not None:
            self.Mysql = MysqlInfo()
            self.Mysql._deserialize(params.get("Mysql"))
        if params.get("Hive") is not None:
            self.Hive = HiveInfo()
            self.Hive._deserialize(params.get("Hive"))
        if params.get("Kafka") is not None:
            self.Kafka = KafkaInfo()
            self.Kafka._deserialize(params.get("Kafka"))
        if params.get("OtherDatasourceConnection") is not None:
            self.OtherDatasourceConnection = OtherDatasourceConnection()
            self.OtherDatasourceConnection._deserialize(params.get("OtherDatasourceConnection"))
        if params.get("PostgreSql") is not None:
            self.PostgreSql = DataSourceInfo()
            self.PostgreSql._deserialize(params.get("PostgreSql"))
        if params.get("SqlServer") is not None:
            self.SqlServer = DataSourceInfo()
            self.SqlServer._deserialize(params.get("SqlServer"))
        if params.get("ClickHouse") is not None:
            self.ClickHouse = DataSourceInfo()
            self.ClickHouse._deserialize(params.get("ClickHouse"))
        if params.get("Elasticsearch") is not None:
            self.Elasticsearch = ElasticsearchInfo()
            self.Elasticsearch._deserialize(params.get("Elasticsearch"))
        if params.get("TDSQLPostgreSql") is not None:
            self.TDSQLPostgreSql = DataSourceInfo()
            self.TDSQLPostgreSql._deserialize(params.get("TDSQLPostgreSql"))
        memeber_set = set(params.keys())
        for name, value in vars(self).items():
            if name in memeber_set:
                memeber_set.remove(name)
        if len(memeber_set) > 0:
            warnings.warn("%s fileds are useless." % ",".join(memeber_set))
        


class DatasourceConnectionInfo(AbstractModel):
    """数据源信息

    """

    def __init__(self):
        r"""
        :param Id: 数据源数字Id
        :type Id: int
        :param DatasourceConnectionId: 数据源字符串Id
        :type DatasourceConnectionId: str
        :param DatasourceConnectionName: 数据源名称
        :type DatasourceConnectionName: str
        :param DatasourceConnectionDesc: 数据源描述
        :type DatasourceConnectionDesc: str
        :param DatasourceConnectionType: 数据源类型，支持DataLakeCatalog、IcebergCatalog、Result、Mysql、HiveCos、HiveHdfs
        :type DatasourceConnectionType: str
        :param DatasourceConnectionConfig: 数据源属性
注意：此字段可能返回 null，表示取不到有效值。
        :type DatasourceConnectionConfig: :class:`tencentcloud.dlc.v20210125.models.DatasourceConnectionConfig`
        :param State: 数据源状态：0（初始化）、1（成功）、-1（已删除）、-2（失败）、-3（删除中）
        :type State: int
        :param ServiceType: 服务类型，DLC
        :type ServiceType: str
        :param Region: 地域
        :type Region: str
        :param AppId: 用户AppId
        :type AppId: str
        :param CreateTime: 数据源创建时间
        :type CreateTime: str
        :param UpdateTime: 数据源最近一次更新时间
        :type UpdateTime: str
        :param Visible: 数据源是否对外展示
        :type Visible: bool
        :param Message: 数据源同步失败原因
        :type Message: str
        :param DataEngines: 数据源绑定的计算引擎信息
注意：此字段可能返回 null，表示取不到有效值。
        :type DataEngines: list of DataEngineInfo
        :param UserAlias: 创建人
注意：此字段可能返回 null，表示取不到有效值。
        :type UserAlias: str
        :param NetworkConnectionSet: 网络配置列表
注意：此字段可能返回 null，表示取不到有效值。
        :type NetworkConnectionSet: list of NetworkConnection
        :param ConnectivityState: 连通性状态：0（未测试，默认）、1（正常）、2（失败）
注意：此字段可能返回 null，表示取不到有效值。
        :type ConnectivityState: int
        :param ConnectivityTips: 连通性测试提示信息
注意：此字段可能返回 null，表示取不到有效值。
        :type ConnectivityTips: str
        """
        self.Id = None
        self.DatasourceConnectionId = None
        self.DatasourceConnectionName = None
        self.DatasourceConnectionDesc = None
        self.DatasourceConnectionType = None
        self.DatasourceConnectionConfig = None
        self.State = None
        self.ServiceType = None
        self.Region = None
        self.AppId = None
        self.CreateTime = None
        self.UpdateTime = None
        self.Visible = None
        self.Message = None
        self.DataEngines = None
        self.UserAlias = None
        self.NetworkConnectionSet = None
        self.ConnectivityState = None
        self.ConnectivityTips = None


    def _deserialize(self, params):
        self.Id = params.get("Id")
        self.DatasourceConnectionId = params.get("DatasourceConnectionId")
        self.DatasourceConnectionName = params.get("DatasourceConnectionName")
        self.DatasourceConnectionDesc = params.get("DatasourceConnectionDesc")
        self.DatasourceConnectionType = params.get("DatasourceConnectionType")
        if params.get("DatasourceConnectionConfig") is not None:
            self.DatasourceConnectionConfig = DatasourceConnectionConfig()
            self.DatasourceConnectionConfig._deserialize(params.get("DatasourceConnectionConfig"))
        self.State = params.get("State")
        self.ServiceType = params.get("ServiceType")
        self.Region = params.get("Region")
        self.AppId = params.get("AppId")
        self.CreateTime = params.get("CreateTime")
        self.UpdateTime = params.get("UpdateTime")
        self.Visible = params.get("Visible")
        self.Message = params.get("Message")
        if params.get("DataEngines") is not None:
            self.DataEngines = []
            for item in params.get("DataEngines"):
                obj = DataEngineInfo()
                obj._deserialize(item)
                self.DataEngines.append(obj)
        self.UserAlias = params.get("UserAlias")
        if params.get("NetworkConnectionSet") is not None:
            self.NetworkConnectionSet = []
            for item in params.get("NetworkConnectionSet"):
                obj = NetworkConnection()
                obj._deserialize(item)
                self.NetworkConnectionSet.append(obj)
        self.ConnectivityState = params.get("ConnectivityState")
        self.ConnectivityTips = params.get("ConnectivityTips")
        memeber_set = set(params.keys())
        for name, value in vars(self).items():
            if name in memeber_set:
                memeber_set.remove(name)
        if len(memeber_set) > 0:
            warnings.warn("%s fileds are useless." % ",".join(memeber_set))
        


class DatasourceConnectionLocation(AbstractModel):
    """数据源连接的网络信息

    """

    def __init__(self):
        r"""
        :param VpcId: 数据连接所在Vpc实例Id，如“vpc-azd4dt1c”。
        :type VpcId: str
        :param VpcCidrBlock: Vpc的IPv4 CIDR
        :type VpcCidrBlock: str
        :param SubnetId: 数据连接所在子网的实例Id，如“subnet-bthucmmy”
        :type SubnetId: str
        :param SubnetCidrBlock: Subnet的IPv4 CIDR
        :type SubnetCidrBlock: str
        """
        self.VpcId = None
        self.VpcCidrBlock = None
        self.SubnetId = None
        self.SubnetCidrBlock = None


    def _deserialize(self, params):
        self.VpcId = params.get("VpcId")
        self.VpcCidrBlock = params.get("VpcCidrBlock")
        self.SubnetId = params.get("SubnetId")
        self.SubnetCidrBlock = params.get("SubnetCidrBlock")
        memeber_set = set(params.keys())
        for name, value in vars(self).items():
            if name in memeber_set:
                memeber_set.remove(name)
        if len(memeber_set) > 0:
            warnings.warn("%s fileds are useless." % ",".join(memeber_set))
        


class DefaultEngineConfig(AbstractModel):
    """默认引擎配置

    """

    def __init__(self):
        r"""
        :param Id: 配置id
        :type Id: int
        :param PayMode: 付费模式，1预付费 0后付费
        :type PayMode: int
        :param Region: 地域
        :type Region: str
        :param Spec: 规格
        :type Spec: int
        :param MinCluster: 最小集群
        :type MinCluster: int
        :param MaxCluster: 最大集群
        :type MaxCluster: int
        :param DefaultCidr: 默认网段
        :type DefaultCidr: str
        """
        self.Id = None
        self.PayMode = None
        self.Region = None
        self.Spec = None
        self.MinCluster = None
        self.MaxCluster = None
        self.DefaultCidr = None


    def _deserialize(self, params):
        self.Id = params.get("Id")
        self.PayMode = params.get("PayMode")
        self.Region = params.get("Region")
        self.Spec = params.get("Spec")
        self.MinCluster = params.get("MinCluster")
        self.MaxCluster = params.get("MaxCluster")
        self.DefaultCidr = params.get("DefaultCidr")
        memeber_set = set(params.keys())
        for name, value in vars(self).items():
            if name in memeber_set:
                memeber_set.remove(name)
        if len(memeber_set) > 0:
            warnings.warn("%s fileds are useless." % ",".join(memeber_set))
        


class DeleteCHDFSBindingProductRequest(AbstractModel):
    """DeleteCHDFSBindingProduct请求参数结构体

    """

    def __init__(self):
        r"""
        :param MountPoint: 需要解绑的元数据加速桶名
        :type MountPoint: str
        :param BucketType: 桶的类型，分为cos和lakefs
        :type BucketType: str
        :param ProductName: 产品名称
        :type ProductName: str
        :param EngineName: 引擎名称，ProductName选择DLC产品时，必传此参数。其他产品可不传
        :type EngineName: str
        :param VpcInfo: vpc信息，ProductName选择other时，必传此参数
        :type VpcInfo: list of VpcInfo
        """
        self.MountPoint = None
        self.BucketType = None
        self.ProductName = None
        self.EngineName = None
        self.VpcInfo = None


    def _deserialize(self, params):
        self.MountPoint = params.get("MountPoint")
        self.BucketType = params.get("BucketType")
        self.ProductName = params.get("ProductName")
        self.EngineName = params.get("EngineName")
        if params.get("VpcInfo") is not None:
            self.VpcInfo = []
            for item in params.get("VpcInfo"):
                obj = VpcInfo()
                obj._deserialize(item)
                self.VpcInfo.append(obj)
        memeber_set = set(params.keys())
        for name, value in vars(self).items():
            if name in memeber_set:
                memeber_set.remove(name)
        if len(memeber_set) > 0:
            warnings.warn("%s fileds are useless." % ",".join(memeber_set))
        


class DeleteCHDFSBindingProductResponse(AbstractModel):
    """DeleteCHDFSBindingProduct返回参数结构体

    """

    def __init__(self):
        r"""
        :param RequestId: 唯一请求 ID，每次请求都会返回。定位问题时需要提供该次请求的 RequestId。
        :type RequestId: str
        """
        self.RequestId = None


    def _deserialize(self, params):
        self.RequestId = params.get("RequestId")


class DeleteCHDFSProductRequest(AbstractModel):
    """DeleteCHDFSProduct请求参数结构体

    """

    def __init__(self):
        r"""
        :param ProductName: 产品名称
        :type ProductName: str
        """
        self.ProductName = None


    def _deserialize(self, params):
        self.ProductName = params.get("ProductName")
        memeber_set = set(params.keys())
        for name, value in vars(self).items():
            if name in memeber_set:
                memeber_set.remove(name)
        if len(memeber_set) > 0:
            warnings.warn("%s fileds are useless." % ",".join(memeber_set))
        


class DeleteCHDFSProductResponse(AbstractModel):
    """DeleteCHDFSProduct返回参数结构体

    """

    def __init__(self):
        r"""
        :param RequestId: 唯一请求 ID，每次请求都会返回。定位问题时需要提供该次请求的 RequestId。
        :type RequestId: str
        """
        self.RequestId = None


    def _deserialize(self, params):
        self.RequestId = params.get("RequestId")


class DeleteColumnsRequest(AbstractModel):
    """DeleteColumns请求参数结构体

    """

    def __init__(self):
        r"""
        :param DatabaseName: 数据库名称
        :type DatabaseName: str
        :param TableName: 表名称
        :type TableName: str
        :param Columns: 删除字段列表
        :type Columns: list of str
        """
        self.DatabaseName = None
        self.TableName = None
        self.Columns = None


    def _deserialize(self, params):
        self.DatabaseName = params.get("DatabaseName")
        self.TableName = params.get("TableName")
        self.Columns = params.get("Columns")
        memeber_set = set(params.keys())
        for name, value in vars(self).items():
            if name in memeber_set:
                memeber_set.remove(name)
        if len(memeber_set) > 0:
            warnings.warn("%s fileds are useless." % ",".join(memeber_set))
        


class DeleteColumnsResponse(AbstractModel):
    """DeleteColumns返回参数结构体

    """

    def __init__(self):
        r"""
        :param Execution: 执行语句
        :type Execution: :class:`tencentcloud.dlc.v20210125.models.Execution`
        :param TaskId: 任务id
        :type TaskId: str
        :param RequestId: 唯一请求 ID，每次请求都会返回。定位问题时需要提供该次请求的 RequestId。
        :type RequestId: str
        """
        self.Execution = None
        self.TaskId = None
        self.RequestId = None


    def _deserialize(self, params):
        if params.get("Execution") is not None:
            self.Execution = Execution()
            self.Execution._deserialize(params.get("Execution"))
        self.TaskId = params.get("TaskId")
        self.RequestId = params.get("RequestId")


class DeleteDataEngineRequest(AbstractModel):
    """DeleteDataEngine请求参数结构体

    """

    def __init__(self):
        r"""
        :param DataEngineNames: 删除虚拟集群的名称数组
        :type DataEngineNames: list of str
        """
        self.DataEngineNames = None


    def _deserialize(self, params):
        self.DataEngineNames = params.get("DataEngineNames")
        memeber_set = set(params.keys())
        for name, value in vars(self).items():
            if name in memeber_set:
                memeber_set.remove(name)
        if len(memeber_set) > 0:
            warnings.warn("%s fileds are useless." % ",".join(memeber_set))
        


class DeleteDataEngineResponse(AbstractModel):
    """DeleteDataEngine返回参数结构体

    """

    def __init__(self):
        r"""
        :param RequestId: 唯一请求 ID，每次请求都会返回。定位问题时需要提供该次请求的 RequestId。
        :type RequestId: str
        """
        self.RequestId = None


    def _deserialize(self, params):
        self.RequestId = params.get("RequestId")


class DeleteDataQueryRequest(AbstractModel):
    """DeleteDataQuery请求参数结构体

    """

    def __init__(self):
        r"""
        :param Name: 删除的查询的名称
        :type Name: str
        """
        self.Name = None


    def _deserialize(self, params):
        self.Name = params.get("Name")
        memeber_set = set(params.keys())
        for name, value in vars(self).items():
            if name in memeber_set:
                memeber_set.remove(name)
        if len(memeber_set) > 0:
            warnings.warn("%s fileds are useless." % ",".join(memeber_set))
        


class DeleteDataQueryResponse(AbstractModel):
    """DeleteDataQuery返回参数结构体

    """

    def __init__(self):
        r"""
        :param RequestId: 唯一请求 ID，每次请求都会返回。定位问题时需要提供该次请求的 RequestId。
        :type RequestId: str
        """
        self.RequestId = None


    def _deserialize(self, params):
        self.RequestId = params.get("RequestId")


class DeleteDatabaseUDFRequest(AbstractModel):
    """DeleteDatabaseUDF请求参数结构体

    """

    def __init__(self):
        r"""
        :param Id: 要删除的udf唯一Id
        :type Id: int
        :param DatabaseName: 函数对应的数据库名
        :type DatabaseName: str
        :param FuncName: 函数名字
        :type FuncName: str
        """
        self.Id = None
        self.DatabaseName = None
        self.FuncName = None


    def _deserialize(self, params):
        self.Id = params.get("Id")
        self.DatabaseName = params.get("DatabaseName")
        self.FuncName = params.get("FuncName")
        memeber_set = set(params.keys())
        for name, value in vars(self).items():
            if name in memeber_set:
                memeber_set.remove(name)
        if len(memeber_set) > 0:
            warnings.warn("%s fileds are useless." % ",".join(memeber_set))
        


class DeleteDatabaseUDFResponse(AbstractModel):
    """DeleteDatabaseUDF返回参数结构体

    """

    def __init__(self):
        r"""
        :param BatchId: 删除任务批次id
注意：此字段可能返回 null，表示取不到有效值。
        :type BatchId: str
        :param TaskIdSet: 删除任务批次对应的任务id
注意：此字段可能返回 null，表示取不到有效值。
        :type TaskIdSet: list of str
        :param RequestId: 唯一请求 ID，每次请求都会返回。定位问题时需要提供该次请求的 RequestId。
        :type RequestId: str
        """
        self.BatchId = None
        self.TaskIdSet = None
        self.RequestId = None


    def _deserialize(self, params):
        self.BatchId = params.get("BatchId")
        self.TaskIdSet = params.get("TaskIdSet")
        self.RequestId = params.get("RequestId")


class DeleteDatasourceConnectionRequest(AbstractModel):
    """DeleteDatasourceConnection请求参数结构体

    """

    def __init__(self):
        r"""
        :param DatasourceConnectionIds: 要删除的数据源唯一Id
        :type DatasourceConnectionIds: list of str
        """
        self.DatasourceConnectionIds = None


    def _deserialize(self, params):
        self.DatasourceConnectionIds = params.get("DatasourceConnectionIds")
        memeber_set = set(params.keys())
        for name, value in vars(self).items():
            if name in memeber_set:
                memeber_set.remove(name)
        if len(memeber_set) > 0:
            warnings.warn("%s fileds are useless." % ",".join(memeber_set))
        


class DeleteDatasourceConnectionResponse(AbstractModel):
    """DeleteDatasourceConnection返回参数结构体

    """

    def __init__(self):
        r"""
        :param RequestId: 唯一请求 ID，每次请求都会返回。定位问题时需要提供该次请求的 RequestId。
        :type RequestId: str
        """
        self.RequestId = None


    def _deserialize(self, params):
        self.RequestId = params.get("RequestId")


class DeleteHouseRequest(AbstractModel):
    """DeleteHouse请求参数结构体

    """

    def __init__(self):
        r"""
        :param HouseNames: 删除队列的名称数组
        :type HouseNames: list of str
        """
        self.HouseNames = None


    def _deserialize(self, params):
        self.HouseNames = params.get("HouseNames")
        memeber_set = set(params.keys())
        for name, value in vars(self).items():
            if name in memeber_set:
                memeber_set.remove(name)
        if len(memeber_set) > 0:
            warnings.warn("%s fileds are useless." % ",".join(memeber_set))
        


class DeleteHouseResponse(AbstractModel):
    """DeleteHouse返回参数结构体

    """

    def __init__(self):
        r"""
        :param RequestId: 唯一请求 ID，每次请求都会返回。定位问题时需要提供该次请求的 RequestId。
        :type RequestId: str
        """
        self.RequestId = None


    def _deserialize(self, params):
        self.RequestId = params.get("RequestId")


class DeleteLakeFsChdfsBindingRequest(AbstractModel):
    """DeleteLakeFsChdfsBinding请求参数结构体

    """

    def __init__(self):
        r"""
        :param MountPoint: 挂载点
        :type MountPoint: str
        :param DataEngine: DLC引擎名称，删除指定DLC引擎和chdfs绑定关系
        :type DataEngine: str
        :param AccessGroupId: 权限组ID，删除指定权限组和chdfs绑定关系
        :type AccessGroupId: str
        """
        self.MountPoint = None
        self.DataEngine = None
        self.AccessGroupId = None


    def _deserialize(self, params):
        self.MountPoint = params.get("MountPoint")
        self.DataEngine = params.get("DataEngine")
        self.AccessGroupId = params.get("AccessGroupId")
        memeber_set = set(params.keys())
        for name, value in vars(self).items():
            if name in memeber_set:
                memeber_set.remove(name)
        if len(memeber_set) > 0:
            warnings.warn("%s fileds are useless." % ",".join(memeber_set))
        


class DeleteLakeFsChdfsBindingResponse(AbstractModel):
    """DeleteLakeFsChdfsBinding返回参数结构体

    """

    def __init__(self):
        r"""
        :param RequestId: 唯一请求 ID，每次请求都会返回。定位问题时需要提供该次请求的 RequestId。
        :type RequestId: str
        """
        self.RequestId = None


    def _deserialize(self, params):
        self.RequestId = params.get("RequestId")


class DeleteLakeFsRequest(AbstractModel):
    """DeleteLakeFs请求参数结构体

    """

    def __init__(self):
        r"""
        :param FsPath: 托管存储路径
        :type FsPath: list of str
        """
        self.FsPath = None


    def _deserialize(self, params):
        self.FsPath = params.get("FsPath")
        memeber_set = set(params.keys())
        for name, value in vars(self).items():
            if name in memeber_set:
                memeber_set.remove(name)
        if len(memeber_set) > 0:
            warnings.warn("%s fileds are useless." % ",".join(memeber_set))
        


class DeleteLakeFsResponse(AbstractModel):
    """DeleteLakeFs返回参数结构体

    """

    def __init__(self):
        r"""
        :param RequestId: 唯一请求 ID，每次请求都会返回。定位问题时需要提供该次请求的 RequestId。
        :type RequestId: str
        """
        self.RequestId = None


    def _deserialize(self, params):
        self.RequestId = params.get("RequestId")


class DeleteLinkRequest(AbstractModel):
    """DeleteLink请求参数结构体

    """

    def __init__(self):
        r"""
        :param Link: 任务依赖关系
        :type Link: :class:`tencentcloud.dlc.v20210125.models.Link`
        """
        self.Link = None


    def _deserialize(self, params):
        if params.get("Link") is not None:
            self.Link = Link()
            self.Link._deserialize(params.get("Link"))
        memeber_set = set(params.keys())
        for name, value in vars(self).items():
            if name in memeber_set:
                memeber_set.remove(name)
        if len(memeber_set) > 0:
            warnings.warn("%s fileds are useless." % ",".join(memeber_set))
        


class DeleteLinkResponse(AbstractModel):
    """DeleteLink返回参数结构体

    """

    def __init__(self):
        r"""
        :param RequestId: 唯一请求 ID，每次请求都会返回。定位问题时需要提供该次请求的 RequestId。
        :type RequestId: str
        """
        self.RequestId = None


    def _deserialize(self, params):
        self.RequestId = params.get("RequestId")


class DeleteMetaDatabaseRequest(AbstractModel):
    """DeleteMetaDatabase请求参数结构体

    """

    def __init__(self):
        r"""
        :param DatabaseName: 数据库名称
        :type DatabaseName: str
        :param DatasourceConnectionName: 数据源名称，默认DataLakeCatalog
        :type DatasourceConnectionName: str
        """
        self.DatabaseName = None
        self.DatasourceConnectionName = None


    def _deserialize(self, params):
        self.DatabaseName = params.get("DatabaseName")
        self.DatasourceConnectionName = params.get("DatasourceConnectionName")
        memeber_set = set(params.keys())
        for name, value in vars(self).items():
            if name in memeber_set:
                memeber_set.remove(name)
        if len(memeber_set) > 0:
            warnings.warn("%s fileds are useless." % ",".join(memeber_set))
        


class DeleteMetaDatabaseResponse(AbstractModel):
    """DeleteMetaDatabase返回参数结构体

    """

    def __init__(self):
        r"""
        :param BatchId: 本批次提交的任务的批次Id
        :type BatchId: str
        :param TaskIdSet: 任务Id集合，按照执行顺序排列
        :type TaskIdSet: list of str
        :param RequestId: 唯一请求 ID，每次请求都会返回。定位问题时需要提供该次请求的 RequestId。
        :type RequestId: str
        """
        self.BatchId = None
        self.TaskIdSet = None
        self.RequestId = None


    def _deserialize(self, params):
        self.BatchId = params.get("BatchId")
        self.TaskIdSet = params.get("TaskIdSet")
        self.RequestId = params.get("RequestId")


class DeleteNotebookSessionRequest(AbstractModel):
    """DeleteNotebookSession请求参数结构体

    """

    def __init__(self):
        r"""
        :param SessionId: Session唯一标识
        :type SessionId: str
        """
        self.SessionId = None


    def _deserialize(self, params):
        self.SessionId = params.get("SessionId")
        memeber_set = set(params.keys())
        for name, value in vars(self).items():
            if name in memeber_set:
                memeber_set.remove(name)
        if len(memeber_set) > 0:
            warnings.warn("%s fileds are useless." % ",".join(memeber_set))
        


class DeleteNotebookSessionResponse(AbstractModel):
    """DeleteNotebookSession返回参数结构体

    """

    def __init__(self):
        r"""
        :param RequestId: 唯一请求 ID，每次请求都会返回。定位问题时需要提供该次请求的 RequestId。
        :type RequestId: str
        """
        self.RequestId = None


    def _deserialize(self, params):
        self.RequestId = params.get("RequestId")


class DeletePartitionFieldRequest(AbstractModel):
    """DeletePartitionField请求参数结构体

    """

    def __init__(self):
        r"""
        :param DatabaseName: 数据库名称
        :type DatabaseName: str
        :param TableName: 数据表名称
        :type TableName: str
        :param Partition: 分区信息
        :type Partition: :class:`tencentcloud.dlc.v20210125.models.Partition`
        :param DatasourceConnectionName: 数据源名称
        :type DatasourceConnectionName: str
        """
        self.DatabaseName = None
        self.TableName = None
        self.Partition = None
        self.DatasourceConnectionName = None


    def _deserialize(self, params):
        self.DatabaseName = params.get("DatabaseName")
        self.TableName = params.get("TableName")
        if params.get("Partition") is not None:
            self.Partition = Partition()
            self.Partition._deserialize(params.get("Partition"))
        self.DatasourceConnectionName = params.get("DatasourceConnectionName")
        memeber_set = set(params.keys())
        for name, value in vars(self).items():
            if name in memeber_set:
                memeber_set.remove(name)
        if len(memeber_set) > 0:
            warnings.warn("%s fileds are useless." % ",".join(memeber_set))
        


class DeletePartitionFieldResponse(AbstractModel):
    """DeletePartitionField返回参数结构体

    """

    def __init__(self):
        r"""
        :param Execution: 修改表执行语句
        :type Execution: :class:`tencentcloud.dlc.v20210125.models.Execution`
        :param TaskId: 任务Id
        :type TaskId: str
        :param RequestId: 唯一请求 ID，每次请求都会返回。定位问题时需要提供该次请求的 RequestId。
        :type RequestId: str
        """
        self.Execution = None
        self.TaskId = None
        self.RequestId = None


    def _deserialize(self, params):
        if params.get("Execution") is not None:
            self.Execution = Execution()
            self.Execution._deserialize(params.get("Execution"))
        self.TaskId = params.get("TaskId")
        self.RequestId = params.get("RequestId")


class DeleteQueryDirRequest(AbstractModel):
    """DeleteQueryDir请求参数结构体

    """

    def __init__(self):
        r"""
        :param Name: 被删除目录的名称
        :type Name: str
        """
        self.Name = None


    def _deserialize(self, params):
        self.Name = params.get("Name")
        memeber_set = set(params.keys())
        for name, value in vars(self).items():
            if name in memeber_set:
                memeber_set.remove(name)
        if len(memeber_set) > 0:
            warnings.warn("%s fileds are useless." % ",".join(memeber_set))
        


class DeleteQueryDirResponse(AbstractModel):
    """DeleteQueryDir返回参数结构体

    """

    def __init__(self):
        r"""
        :param RequestId: 唯一请求 ID，每次请求都会返回。定位问题时需要提供该次请求的 RequestId。
        :type RequestId: str
        """
        self.RequestId = None


    def _deserialize(self, params):
        self.RequestId = params.get("RequestId")


class DeleteSQLSessionCatalogRequest(AbstractModel):
    """DeleteSQLSessionCatalog请求参数结构体

    """

    def __init__(self):
        r"""
        :param Name: 节点名称
        :type Name: str
        :param Type: 节点类型：0（目录）、1（会话）
        :type Type: str
        :param Operator: 操作者
        :type Operator: str
        :param Path: 父节点路径
        :type Path: str
        """
        self.Name = None
        self.Type = None
        self.Operator = None
        self.Path = None


    def _deserialize(self, params):
        self.Name = params.get("Name")
        self.Type = params.get("Type")
        self.Operator = params.get("Operator")
        self.Path = params.get("Path")
        memeber_set = set(params.keys())
        for name, value in vars(self).items():
            if name in memeber_set:
                memeber_set.remove(name)
        if len(memeber_set) > 0:
            warnings.warn("%s fileds are useless." % ",".join(memeber_set))
        


class DeleteSQLSessionCatalogResponse(AbstractModel):
    """DeleteSQLSessionCatalog返回参数结构体

    """

    def __init__(self):
        r"""
        :param Status: SUCCESS：成功、FAIL：失败、FLUSH：会话内容已变更，请刷新（修改时触发）、DUPLICATE：重名，请调整、NOTEMPTY：该目录下不为空，无法删除、
LIMITEXCEEDED：创建的会话超过限制；
        :type Status: str
        :param RequestId: 唯一请求 ID，每次请求都会返回。定位问题时需要提供该次请求的 RequestId。
        :type RequestId: str
        """
        self.Status = None
        self.RequestId = None


    def _deserialize(self, params):
        self.Status = params.get("Status")
        self.RequestId = params.get("RequestId")


class DeleteSQLSessionSnapshotRequest(AbstractModel):
    """DeleteSQLSessionSnapshot请求参数结构体

    """

    def __init__(self):
        r"""
        :param SessionId: 会话ID
        :type SessionId: str
        :param Operator: 操作者
        :type Operator: str
        """
        self.SessionId = None
        self.Operator = None


    def _deserialize(self, params):
        self.SessionId = params.get("SessionId")
        self.Operator = params.get("Operator")
        memeber_set = set(params.keys())
        for name, value in vars(self).items():
            if name in memeber_set:
                memeber_set.remove(name)
        if len(memeber_set) > 0:
            warnings.warn("%s fileds are useless." % ",".join(memeber_set))
        


class DeleteSQLSessionSnapshotResponse(AbstractModel):
    """DeleteSQLSessionSnapshot返回参数结构体

    """

    def __init__(self):
        r"""
        :param RequestId: 唯一请求 ID，每次请求都会返回。定位问题时需要提供该次请求的 RequestId。
        :type RequestId: str
        """
        self.RequestId = None


    def _deserialize(self, params):
        self.RequestId = params.get("RequestId")


class DeleteScheduleTaskRequest(AbstractModel):
    """DeleteScheduleTask请求参数结构体

    """

    def __init__(self):
        r"""
        :param TaskId: 调度任务ID
        :type TaskId: str
        :param VirtualFlag: 是否为虚拟任务
        :type VirtualFlag: bool
        :param VirtualTaskId: 虚拟任务ID
        :type VirtualTaskId: str
        :param ProjectId: 调度任务所属项目ID
        :type ProjectId: int
        """
        self.TaskId = None
        self.VirtualFlag = None
        self.VirtualTaskId = None
        self.ProjectId = None


    def _deserialize(self, params):
        self.TaskId = params.get("TaskId")
        self.VirtualFlag = params.get("VirtualFlag")
        self.VirtualTaskId = params.get("VirtualTaskId")
        self.ProjectId = params.get("ProjectId")
        memeber_set = set(params.keys())
        for name, value in vars(self).items():
            if name in memeber_set:
                memeber_set.remove(name)
        if len(memeber_set) > 0:
            warnings.warn("%s fileds are useless." % ",".join(memeber_set))
        


class DeleteScheduleTaskResponse(AbstractModel):
    """DeleteScheduleTask返回参数结构体

    """

    def __init__(self):
        r"""
        :param Result: 是否删除成功
        :type Result: bool
        :param RequestId: 唯一请求 ID，每次请求都会返回。定位问题时需要提供该次请求的 RequestId。
        :type RequestId: str
        """
        self.Result = None
        self.RequestId = None


    def _deserialize(self, params):
        self.Result = params.get("Result")
        self.RequestId = params.get("RequestId")


class DeleteScriptRequest(AbstractModel):
    """DeleteScript请求参数结构体

    """

    def __init__(self):
        r"""
        :param ScriptIds: 脚本id，其可以通过DescribeScripts接口提取
        :type ScriptIds: list of str
        """
        self.ScriptIds = None


    def _deserialize(self, params):
        self.ScriptIds = params.get("ScriptIds")
        memeber_set = set(params.keys())
        for name, value in vars(self).items():
            if name in memeber_set:
                memeber_set.remove(name)
        if len(memeber_set) > 0:
            warnings.warn("%s fileds are useless." % ",".join(memeber_set))
        


class DeleteScriptResponse(AbstractModel):
    """DeleteScript返回参数结构体

    """

    def __init__(self):
        r"""
        :param ScriptsAffected: 删除的脚本数量
        :type ScriptsAffected: int
        :param RequestId: 唯一请求 ID，每次请求都会返回。定位问题时需要提供该次请求的 RequestId。
        :type RequestId: str
        """
        self.ScriptsAffected = None
        self.RequestId = None


    def _deserialize(self, params):
        self.ScriptsAffected = params.get("ScriptsAffected")
        self.RequestId = params.get("RequestId")


class DeleteSparkAppRequest(AbstractModel):
    """DeleteSparkApp请求参数结构体

    """

    def __init__(self):
        r"""
        :param AppName: spark作业名
        :type AppName: str
        :param ForceKillJob: 删掉spark应用时，是否强制杀掉当前正在运行的任务
        :type ForceKillJob: bool
        """
        self.AppName = None
        self.ForceKillJob = None


    def _deserialize(self, params):
        self.AppName = params.get("AppName")
        self.ForceKillJob = params.get("ForceKillJob")
        memeber_set = set(params.keys())
        for name, value in vars(self).items():
            if name in memeber_set:
                memeber_set.remove(name)
        if len(memeber_set) > 0:
            warnings.warn("%s fileds are useless." % ",".join(memeber_set))
        


class DeleteSparkAppResponse(AbstractModel):
    """DeleteSparkApp返回参数结构体

    """

    def __init__(self):
        r"""
        :param RequestId: 唯一请求 ID，每次请求都会返回。定位问题时需要提供该次请求的 RequestId。
        :type RequestId: str
        """
        self.RequestId = None


    def _deserialize(self, params):
        self.RequestId = params.get("RequestId")


class DeleteSparkImageRequest(AbstractModel):
    """DeleteSparkImage请求参数结构体

    """

    def __init__(self):
        r"""
        :param ImageId: 镜像编号
        :type ImageId: str
        """
        self.ImageId = None


    def _deserialize(self, params):
        self.ImageId = params.get("ImageId")
        memeber_set = set(params.keys())
        for name, value in vars(self).items():
            if name in memeber_set:
                memeber_set.remove(name)
        if len(memeber_set) > 0:
            warnings.warn("%s fileds are useless." % ",".join(memeber_set))
        


class DeleteSparkImageResponse(AbstractModel):
    """DeleteSparkImage返回参数结构体

    """

    def __init__(self):
        r"""
        :param RequestId: 唯一请求 ID，每次请求都会返回。定位问题时需要提供该次请求的 RequestId。
        :type RequestId: str
        """
        self.RequestId = None


    def _deserialize(self, params):
        self.RequestId = params.get("RequestId")


class DeleteSparkImageUserRecordsRequest(AbstractModel):
    """DeleteSparkImageUserRecords请求参数结构体

    """

    def __init__(self):
        r"""
        :param ImageId: 镜像编码
        :type ImageId: str
        :param UserAppId: 用户APPID
        :type UserAppId: int
        :param ImageType: 枚举值：1（父版本）、2（子版本）、3（pyspark）
        :type ImageType: str
        """
        self.ImageId = None
        self.UserAppId = None
        self.ImageType = None


    def _deserialize(self, params):
        self.ImageId = params.get("ImageId")
        self.UserAppId = params.get("UserAppId")
        self.ImageType = params.get("ImageType")
        memeber_set = set(params.keys())
        for name, value in vars(self).items():
            if name in memeber_set:
                memeber_set.remove(name)
        if len(memeber_set) > 0:
            warnings.warn("%s fileds are useless." % ",".join(memeber_set))
        


class DeleteSparkImageUserRecordsResponse(AbstractModel):
    """DeleteSparkImageUserRecords返回参数结构体

    """

    def __init__(self):
        r"""
        :param RequestId: 唯一请求 ID，每次请求都会返回。定位问题时需要提供该次请求的 RequestId。
        :type RequestId: str
        """
        self.RequestId = None


    def _deserialize(self, params):
        self.RequestId = params.get("RequestId")


class DeleteTableBatchRequest(AbstractModel):
    """DeleteTableBatch请求参数结构体

    """

    def __init__(self):
        r"""
        :param DatasourceConnectionName: Catalog名称
        :type DatasourceConnectionName: str
        :param DatabaseName: 库名
        :type DatabaseName: str
        :param TableNames: 表名列表
        :type TableNames: list of str
        """
        self.DatasourceConnectionName = None
        self.DatabaseName = None
        self.TableNames = None


    def _deserialize(self, params):
        self.DatasourceConnectionName = params.get("DatasourceConnectionName")
        self.DatabaseName = params.get("DatabaseName")
        self.TableNames = params.get("TableNames")
        memeber_set = set(params.keys())
        for name, value in vars(self).items():
            if name in memeber_set:
                memeber_set.remove(name)
        if len(memeber_set) > 0:
            warnings.warn("%s fileds are useless." % ",".join(memeber_set))
        


class DeleteTableBatchResponse(AbstractModel):
    """DeleteTableBatch返回参数结构体

    """

    def __init__(self):
        r"""
        :param BatchId: 批任务Id
        :type BatchId: str
        :param TaskIdSet: TaskId列表
        :type TaskIdSet: list of str
        :param RequestId: 唯一请求 ID，每次请求都会返回。定位问题时需要提供该次请求的 RequestId。
        :type RequestId: str
        """
        self.BatchId = None
        self.TaskIdSet = None
        self.RequestId = None


    def _deserialize(self, params):
        self.BatchId = params.get("BatchId")
        self.TaskIdSet = params.get("TaskIdSet")
        self.RequestId = params.get("RequestId")


class DeleteTableRequest(AbstractModel):
    """DeleteTable请求参数结构体

    """

    def __init__(self):
        r"""
        :param TableBaseInfo: 表基本信息
        :type TableBaseInfo: :class:`tencentcloud.dlc.v20210125.models.TableBaseInfo`
        """
        self.TableBaseInfo = None


    def _deserialize(self, params):
        if params.get("TableBaseInfo") is not None:
            self.TableBaseInfo = TableBaseInfo()
            self.TableBaseInfo._deserialize(params.get("TableBaseInfo"))
        memeber_set = set(params.keys())
        for name, value in vars(self).items():
            if name in memeber_set:
                memeber_set.remove(name)
        if len(memeber_set) > 0:
            warnings.warn("%s fileds are useless." % ",".join(memeber_set))
        


class DeleteTableResponse(AbstractModel):
    """DeleteTable返回参数结构体

    """

    def __init__(self):
        r"""
        :param RequestId: 唯一请求 ID，每次请求都会返回。定位问题时需要提供该次请求的 RequestId。
        :type RequestId: str
        """
        self.RequestId = None


    def _deserialize(self, params):
        self.RequestId = params.get("RequestId")


class DeleteUserRequest(AbstractModel):
    """DeleteUser请求参数结构体

    """

    def __init__(self):
        r"""
        :param UserIds: 需要删除的用户的Id
        :type UserIds: list of str
        """
        self.UserIds = None


    def _deserialize(self, params):
        self.UserIds = params.get("UserIds")
        memeber_set = set(params.keys())
        for name, value in vars(self).items():
            if name in memeber_set:
                memeber_set.remove(name)
        if len(memeber_set) > 0:
            warnings.warn("%s fileds are useless." % ",".join(memeber_set))
        


class DeleteUserResponse(AbstractModel):
    """DeleteUser返回参数结构体

    """

    def __init__(self):
        r"""
        :param RequestId: 唯一请求 ID，每次请求都会返回。定位问题时需要提供该次请求的 RequestId。
        :type RequestId: str
        """
        self.RequestId = None


    def _deserialize(self, params):
        self.RequestId = params.get("RequestId")


class DeleteUserRoleRequest(AbstractModel):
    """DeleteUserRole请求参数结构体

    """

    def __init__(self):
        r"""
        :param RoleId: 角色ID
        :type RoleId: int
        """
        self.RoleId = None


    def _deserialize(self, params):
        self.RoleId = params.get("RoleId")
        memeber_set = set(params.keys())
        for name, value in vars(self).items():
            if name in memeber_set:
                memeber_set.remove(name)
        if len(memeber_set) > 0:
            warnings.warn("%s fileds are useless." % ",".join(memeber_set))
        


class DeleteUserRoleResponse(AbstractModel):
    """DeleteUserRole返回参数结构体

    """

    def __init__(self):
        r"""
        :param RequestId: 唯一请求 ID，每次请求都会返回。定位问题时需要提供该次请求的 RequestId。
        :type RequestId: str
        """
        self.RequestId = None


    def _deserialize(self, params):
        self.RequestId = params.get("RequestId")


class DeleteUsersFromWorkGroupRequest(AbstractModel):
    """DeleteUsersFromWorkGroup请求参数结构体

    """

    def __init__(self):
        r"""
        :param AddInfo: 要删除的用户信息
        :type AddInfo: :class:`tencentcloud.dlc.v20210125.models.UserIdSetOfWorkGroupId`
        """
        self.AddInfo = None


    def _deserialize(self, params):
        if params.get("AddInfo") is not None:
            self.AddInfo = UserIdSetOfWorkGroupId()
            self.AddInfo._deserialize(params.get("AddInfo"))
        memeber_set = set(params.keys())
        for name, value in vars(self).items():
            if name in memeber_set:
                memeber_set.remove(name)
        if len(memeber_set) > 0:
            warnings.warn("%s fileds are useless." % ",".join(memeber_set))
        


class DeleteUsersFromWorkGroupResponse(AbstractModel):
    """DeleteUsersFromWorkGroup返回参数结构体

    """

    def __init__(self):
        r"""
        :param RequestId: 唯一请求 ID，每次请求都会返回。定位问题时需要提供该次请求的 RequestId。
        :type RequestId: str
        """
        self.RequestId = None


    def _deserialize(self, params):
        self.RequestId = params.get("RequestId")


class DeleteViewRequest(AbstractModel):
    """DeleteView请求参数结构体

    """

    def __init__(self):
        r"""
        :param DatabaseName: 数据库名称
        :type DatabaseName: str
        :param ViewName: 视图名称
        :type ViewName: str
        :param DatasourceConnectionName: 数据源名称
        :type DatasourceConnectionName: str
        """
        self.DatabaseName = None
        self.ViewName = None
        self.DatasourceConnectionName = None


    def _deserialize(self, params):
        self.DatabaseName = params.get("DatabaseName")
        self.ViewName = params.get("ViewName")
        self.DatasourceConnectionName = params.get("DatasourceConnectionName")
        memeber_set = set(params.keys())
        for name, value in vars(self).items():
            if name in memeber_set:
                memeber_set.remove(name)
        if len(memeber_set) > 0:
            warnings.warn("%s fileds are useless." % ",".join(memeber_set))
        


class DeleteViewResponse(AbstractModel):
    """DeleteView返回参数结构体

    """

    def __init__(self):
        r"""
        :param Execution: 删除视图执行语句
        :type Execution: :class:`tencentcloud.dlc.v20210125.models.Execution`
        :param TaskId: 任务Id
        :type TaskId: str
        :param RequestId: 唯一请求 ID，每次请求都会返回。定位问题时需要提供该次请求的 RequestId。
        :type RequestId: str
        """
        self.Execution = None
        self.TaskId = None
        self.RequestId = None


    def _deserialize(self, params):
        if params.get("Execution") is not None:
            self.Execution = Execution()
            self.Execution._deserialize(params.get("Execution"))
        self.TaskId = params.get("TaskId")
        self.RequestId = params.get("RequestId")


class DeleteWorkGroupRequest(AbstractModel):
    """DeleteWorkGroup请求参数结构体

    """

    def __init__(self):
        r"""
        :param WorkGroupIds: 要删除的工作组Id集合
        :type WorkGroupIds: list of int
        """
        self.WorkGroupIds = None


    def _deserialize(self, params):
        self.WorkGroupIds = params.get("WorkGroupIds")
        memeber_set = set(params.keys())
        for name, value in vars(self).items():
            if name in memeber_set:
                memeber_set.remove(name)
        if len(memeber_set) > 0:
            warnings.warn("%s fileds are useless." % ",".join(memeber_set))
        


class DeleteWorkGroupResponse(AbstractModel):
    """DeleteWorkGroup返回参数结构体

    """

    def __init__(self):
        r"""
        :param RequestId: 唯一请求 ID，每次请求都会返回。定位问题时需要提供该次请求的 RequestId。
        :type RequestId: str
        """
        self.RequestId = None


    def _deserialize(self, params):
        self.RequestId = params.get("RequestId")


class DeleteWorkflowRequest(AbstractModel):
    """DeleteWorkflow请求参数结构体

    """

    def __init__(self):
        r"""
        :param WorkflowId: 调度计划ID
        :type WorkflowId: str
        """
        self.WorkflowId = None


    def _deserialize(self, params):
        self.WorkflowId = params.get("WorkflowId")
        memeber_set = set(params.keys())
        for name, value in vars(self).items():
            if name in memeber_set:
                memeber_set.remove(name)
        if len(memeber_set) > 0:
            warnings.warn("%s fileds are useless." % ",".join(memeber_set))
        


class DeleteWorkflowResponse(AbstractModel):
    """DeleteWorkflow返回参数结构体

    """

    def __init__(self):
        r"""
        :param RequestId: 唯一请求 ID，每次请求都会返回。定位问题时需要提供该次请求的 RequestId。
        :type RequestId: str
        """
        self.RequestId = None


    def _deserialize(self, params):
        self.RequestId = params.get("RequestId")


class DescribeAdvancedStoreLocationRequest(AbstractModel):
    """DescribeAdvancedStoreLocation请求参数结构体

    """


class DescribeAdvancedStoreLocationResponse(AbstractModel):
    """DescribeAdvancedStoreLocation返回参数结构体

    """

    def __init__(self):
        r"""
        :param Enable: 是否启用高级设置：0-否，1-是
        :type Enable: int
        :param StoreLocation: 查询结果保存cos路径
        :type StoreLocation: str
        :param HasLakeFs: 是否有托管存储权限
        :type HasLakeFs: bool
        :param LakeFsStatus: 托管存储状态，HasLakeFs等于true时，该值才有意义
注意：此字段可能返回 null，表示取不到有效值。
        :type LakeFsStatus: str
        :param BucketType: 托管存储桶类型
注意：此字段可能返回 null，表示取不到有效值。
        :type BucketType: str
        :param RequestId: 唯一请求 ID，每次请求都会返回。定位问题时需要提供该次请求的 RequestId。
        :type RequestId: str
        """
        self.Enable = None
        self.StoreLocation = None
        self.HasLakeFs = None
        self.LakeFsStatus = None
        self.BucketType = None
        self.RequestId = None


    def _deserialize(self, params):
        self.Enable = params.get("Enable")
        self.StoreLocation = params.get("StoreLocation")
        self.HasLakeFs = params.get("HasLakeFs")
        self.LakeFsStatus = params.get("LakeFsStatus")
        self.BucketType = params.get("BucketType")
        self.RequestId = params.get("RequestId")


class DescribeAllColumnsRequest(AbstractModel):
    """DescribeAllColumns请求参数结构体

    """

    def __init__(self):
        r"""
        :param DatabaseName: 数据库名称
        :type DatabaseName: str
        :param TableName: 表名称
        :type TableName: str
        :param DatasourceConnectionName: 数据源名称
        :type DatasourceConnectionName: str
        :param ColumnName: 字段名称
        :type ColumnName: str
        :param KeyWord: 关键字
        :type KeyWord: str
        :param Sort: 排序字段
        :type Sort: str
        :param Asc: 排序方式：true 升序；false 降序
        :type Asc: bool
        :param StartTime: 开始时间（yyyy-MM-dd HH:mm:ss）
        :type StartTime: str
        :param EndTime: 结束时间（yyyy-MM-dd HH:mm:ss）
        :type EndTime: str
        """
        self.DatabaseName = None
        self.TableName = None
        self.DatasourceConnectionName = None
        self.ColumnName = None
        self.KeyWord = None
        self.Sort = None
        self.Asc = None
        self.StartTime = None
        self.EndTime = None


    def _deserialize(self, params):
        self.DatabaseName = params.get("DatabaseName")
        self.TableName = params.get("TableName")
        self.DatasourceConnectionName = params.get("DatasourceConnectionName")
        self.ColumnName = params.get("ColumnName")
        self.KeyWord = params.get("KeyWord")
        self.Sort = params.get("Sort")
        self.Asc = params.get("Asc")
        self.StartTime = params.get("StartTime")
        self.EndTime = params.get("EndTime")
        memeber_set = set(params.keys())
        for name, value in vars(self).items():
            if name in memeber_set:
                memeber_set.remove(name)
        if len(memeber_set) > 0:
            warnings.warn("%s fileds are useless." % ",".join(memeber_set))
        


class DescribeAllColumnsResponse(AbstractModel):
    """DescribeAllColumns返回参数结构体

    """

    def __init__(self):
        r"""
        :param Columns: 字段数组
        :type Columns: list of Column
        :param RequestId: 唯一请求 ID，每次请求都会返回。定位问题时需要提供该次请求的 RequestId。
        :type RequestId: str
        """
        self.Columns = None
        self.RequestId = None


    def _deserialize(self, params):
        if params.get("Columns") is not None:
            self.Columns = []
            for item in params.get("Columns"):
                obj = Column()
                obj._deserialize(item)
                self.Columns.append(obj)
        self.RequestId = params.get("RequestId")


class DescribeAuditEventsRequest(AbstractModel):
    """DescribeAuditEvents请求参数结构体

    """

    def __init__(self):
        r"""
        :param StartTime: 起始时间戳
        :type StartTime: int
        :param EndTime: 结束时间戳
        :type EndTime: int
        :param NextToken: 查看更多日志的凭证
        :type NextToken: int
        :param MaxResults: 返回日志的最大条数（最大 50 条）
        :type MaxResults: int
        :param LookupAttributes: 检索条件PrincipalId：子账号、EventType：事件类型
        :type LookupAttributes: list of LookupAttribute
        """
        self.StartTime = None
        self.EndTime = None
        self.NextToken = None
        self.MaxResults = None
        self.LookupAttributes = None


    def _deserialize(self, params):
        self.StartTime = params.get("StartTime")
        self.EndTime = params.get("EndTime")
        self.NextToken = params.get("NextToken")
        self.MaxResults = params.get("MaxResults")
        if params.get("LookupAttributes") is not None:
            self.LookupAttributes = []
            for item in params.get("LookupAttributes"):
                obj = LookupAttribute()
                obj._deserialize(item)
                self.LookupAttributes.append(obj)
        memeber_set = set(params.keys())
        for name, value in vars(self).items():
            if name in memeber_set:
                memeber_set.remove(name)
        if len(memeber_set) > 0:
            warnings.warn("%s fileds are useless." % ",".join(memeber_set))
        


class DescribeAuditEventsResponse(AbstractModel):
    """DescribeAuditEvents返回参数结构体

    """

    def __init__(self):
        r"""
        :param AuditEvents: 审计事件信息数组
注意：此字段可能返回 null，表示取不到有效值。
        :type AuditEvents: list of AuditEvent
        :param NextToken: 翻页token
注意：此字段可能返回 null，表示取不到有效值。
        :type NextToken: int
        :param ListOver: 是否可以翻页
注意：此字段可能返回 null，表示取不到有效值。
        :type ListOver: bool
        :param RequestId: 唯一请求 ID，每次请求都会返回。定位问题时需要提供该次请求的 RequestId。
        :type RequestId: str
        """
        self.AuditEvents = None
        self.NextToken = None
        self.ListOver = None
        self.RequestId = None


    def _deserialize(self, params):
        if params.get("AuditEvents") is not None:
            self.AuditEvents = []
            for item in params.get("AuditEvents"):
                obj = AuditEvent()
                obj._deserialize(item)
                self.AuditEvents.append(obj)
        self.NextToken = params.get("NextToken")
        self.ListOver = params.get("ListOver")
        self.RequestId = params.get("RequestId")


class DescribeAvailableVpcRequest(AbstractModel):
    """DescribeAvailableVpc请求参数结构体

    """

    def __init__(self):
        r"""
        :param PayMode: 付费模式，0:后付费，1:预付费
        :type PayMode: int
        """
        self.PayMode = None


    def _deserialize(self, params):
        self.PayMode = params.get("PayMode")
        memeber_set = set(params.keys())
        for name, value in vars(self).items():
            if name in memeber_set:
                memeber_set.remove(name)
        if len(memeber_set) > 0:
            warnings.warn("%s fileds are useless." % ",".join(memeber_set))
        


class DescribeAvailableVpcResponse(AbstractModel):
    """DescribeAvailableVpc返回参数结构体

    """

    def __init__(self):
        r"""
        :param VpcConfigures: vpc配置信息
注意：此字段可能返回 null，表示取不到有效值。
        :type VpcConfigures: list of VpcConfigure
        :param RequestId: 唯一请求 ID，每次请求都会返回。定位问题时需要提供该次请求的 RequestId。
        :type RequestId: str
        """
        self.VpcConfigures = None
        self.RequestId = None


    def _deserialize(self, params):
        if params.get("VpcConfigures") is not None:
            self.VpcConfigures = []
            for item in params.get("VpcConfigures"):
                obj = VpcConfigure()
                obj._deserialize(item)
                self.VpcConfigures.append(obj)
        self.RequestId = params.get("RequestId")


class DescribeBucketTypeRequest(AbstractModel):
    """DescribeBucketType请求参数结构体

    """

    def __init__(self):
        r"""
        :param Path: 路径：可以是lakefs://xxx，cos://xxx，cosn://xxx
        :type Path: str
        """
        self.Path = None


    def _deserialize(self, params):
        self.Path = params.get("Path")
        memeber_set = set(params.keys())
        for name, value in vars(self).items():
            if name in memeber_set:
                memeber_set.remove(name)
        if len(memeber_set) > 0:
            warnings.warn("%s fileds are useless." % ",".join(memeber_set))
        


class DescribeBucketTypeResponse(AbstractModel):
    """DescribeBucketType返回参数结构体

    """

    def __init__(self):
        r"""
        :param BucketType: 桶类型：cos/chdfs
        :type BucketType: str
        :param RequestId: 唯一请求 ID，每次请求都会返回。定位问题时需要提供该次请求的 RequestId。
        :type RequestId: str
        """
        self.BucketType = None
        self.RequestId = None


    def _deserialize(self, params):
        self.BucketType = params.get("BucketType")
        self.RequestId = params.get("RequestId")


class DescribeCHDFSAccessInfosRequest(AbstractModel):
    """DescribeCHDFSAccessInfos请求参数结构体

    """


class DescribeCHDFSAccessInfosResponse(AbstractModel):
    """DescribeCHDFSAccessInfos返回参数结构体

    """

    def __init__(self):
        r"""
        :param CHDFSAccessInfos: chdfs产品列表
        :type CHDFSAccessInfos: list of CHDFSAccessInfo
        :param Total: 总条数
        :type Total: int
        :param RequestId: 唯一请求 ID，每次请求都会返回。定位问题时需要提供该次请求的 RequestId。
        :type RequestId: str
        """
        self.CHDFSAccessInfos = None
        self.Total = None
        self.RequestId = None


    def _deserialize(self, params):
        if params.get("CHDFSAccessInfos") is not None:
            self.CHDFSAccessInfos = []
            for item in params.get("CHDFSAccessInfos"):
                obj = CHDFSAccessInfo()
                obj._deserialize(item)
                self.CHDFSAccessInfos.append(obj)
        self.Total = params.get("Total")
        self.RequestId = params.get("RequestId")


class DescribeCHDFSMountPointAssociateInfosRequest(AbstractModel):
    """DescribeCHDFSMountPointAssociateInfos请求参数结构体

    """

    def __init__(self):
        r"""
        :param MountPoints: 挂载点列表
        :type MountPoints: list of MountPoint
        """
        self.MountPoints = None


    def _deserialize(self, params):
        if params.get("MountPoints") is not None:
            self.MountPoints = []
            for item in params.get("MountPoints"):
                obj = MountPoint()
                obj._deserialize(item)
                self.MountPoints.append(obj)
        memeber_set = set(params.keys())
        for name, value in vars(self).items():
            if name in memeber_set:
                memeber_set.remove(name)
        if len(memeber_set) > 0:
            warnings.warn("%s fileds are useless." % ",".join(memeber_set))
        


class DescribeCHDFSMountPointAssociateInfosResponse(AbstractModel):
    """DescribeCHDFSMountPointAssociateInfos返回参数结构体

    """

    def __init__(self):
        r"""
        :param AssociateInfos: 挂载点绑定信息列表
        :type AssociateInfos: list of MountPointAssociateInfo
        :param TotalElements: 挂载点绑定信息列表大小
        :type TotalElements: int
        :param RequestId: 唯一请求 ID，每次请求都会返回。定位问题时需要提供该次请求的 RequestId。
        :type RequestId: str
        """
        self.AssociateInfos = None
        self.TotalElements = None
        self.RequestId = None


    def _deserialize(self, params):
        if params.get("AssociateInfos") is not None:
            self.AssociateInfos = []
            for item in params.get("AssociateInfos"):
                obj = MountPointAssociateInfo()
                obj._deserialize(item)
                self.AssociateInfos.append(obj)
        self.TotalElements = params.get("TotalElements")
        self.RequestId = params.get("RequestId")


class DescribeCHDFSMountPointSuperuserRequest(AbstractModel):
    """DescribeCHDFSMountPointSuperuser请求参数结构体

    """

    def __init__(self):
        r"""
        :param BucketId: 桶id
        :type BucketId: str
        """
        self.BucketId = None


    def _deserialize(self, params):
        self.BucketId = params.get("BucketId")
        memeber_set = set(params.keys())
        for name, value in vars(self).items():
            if name in memeber_set:
                memeber_set.remove(name)
        if len(memeber_set) > 0:
            warnings.warn("%s fileds are useless." % ",".join(memeber_set))
        


class DescribeCHDFSMountPointSuperuserResponse(AbstractModel):
    """DescribeCHDFSMountPointSuperuser返回参数结构体

    """

    def __init__(self):
        r"""
        :param Superusers: Superuser列表
        :type Superusers: list of str
        :param RequestId: 唯一请求 ID，每次请求都会返回。定位问题时需要提供该次请求的 RequestId。
        :type RequestId: str
        """
        self.Superusers = None
        self.RequestId = None


    def _deserialize(self, params):
        self.Superusers = params.get("Superusers")
        self.RequestId = params.get("RequestId")


class DescribeCHDFSMountPointsRequest(AbstractModel):
    """DescribeCHDFSMountPoints请求参数结构体

    """


class DescribeCHDFSMountPointsResponse(AbstractModel):
    """DescribeCHDFSMountPoints返回参数结构体

    """

    def __init__(self):
        r"""
        :param MountPoints: 挂载点信息
        :type MountPoints: list of MountPoint
        :param RequestId: 唯一请求 ID，每次请求都会返回。定位问题时需要提供该次请求的 RequestId。
        :type RequestId: str
        """
        self.MountPoints = None
        self.RequestId = None


    def _deserialize(self, params):
        if params.get("MountPoints") is not None:
            self.MountPoints = []
            for item in params.get("MountPoints"):
                obj = MountPoint()
                obj._deserialize(item)
                self.MountPoints.append(obj)
        self.RequestId = params.get("RequestId")


class DescribeCHDFSProductsRequest(AbstractModel):
    """DescribeCHDFSProducts请求参数结构体

    """


class DescribeCHDFSProductsResponse(AbstractModel):
    """元数据加速桶产品列表

    """

    def __init__(self):
        r"""
        :param CHDFSProductInfos: 产品列表
注意：此字段可能返回 null，表示取不到有效值。
        :type CHDFSProductInfos: list of CHDFSProductInfo
        :param Total: 列表数
注意：此字段可能返回 null，表示取不到有效值。
        :type Total: int
        """
        self.CHDFSProductInfos = None
        self.Total = None


    def _deserialize(self, params):
        if params.get("CHDFSProductInfos") is not None:
            self.CHDFSProductInfos = []
            for item in params.get("CHDFSProductInfos"):
                obj = CHDFSProductInfo()
                obj._deserialize(item)
                self.CHDFSProductInfos.append(obj)
        self.Total = params.get("Total")


class DescribeColumnsRequest(AbstractModel):
    """DescribeColumns请求参数结构体

    """

    def __init__(self):
        r"""
        :param DatabaseName: 数据库名称
        :type DatabaseName: str
        :param TableName: 表名称
        :type TableName: str
        :param Limit: 返回数量
        :type Limit: int
        :param Offset: 数据偏移量，从0开始，默认为0。
        :type Offset: int
        :param DatasourceConnectionName: 数据源名称
        :type DatasourceConnectionName: str
        :param ColumnName: 字段名称
        :type ColumnName: str
        :param KeyWord: 关键字
        :type KeyWord: str
        :param Sort: 排序字段
        :type Sort: str
        :param Asc: 排序方式：true 升序；false 降序
        :type Asc: bool
        :param StartTime: 开始时间（yyyy-MM-dd HH:mm:ss）
        :type StartTime: str
        :param EndTime: 结束时间（yyyy-MM-dd HH:mm:ss）
        :type EndTime: str
        """
        self.DatabaseName = None
        self.TableName = None
        self.Limit = None
        self.Offset = None
        self.DatasourceConnectionName = None
        self.ColumnName = None
        self.KeyWord = None
        self.Sort = None
        self.Asc = None
        self.StartTime = None
        self.EndTime = None


    def _deserialize(self, params):
        self.DatabaseName = params.get("DatabaseName")
        self.TableName = params.get("TableName")
        self.Limit = params.get("Limit")
        self.Offset = params.get("Offset")
        self.DatasourceConnectionName = params.get("DatasourceConnectionName")
        self.ColumnName = params.get("ColumnName")
        self.KeyWord = params.get("KeyWord")
        self.Sort = params.get("Sort")
        self.Asc = params.get("Asc")
        self.StartTime = params.get("StartTime")
        self.EndTime = params.get("EndTime")
        memeber_set = set(params.keys())
        for name, value in vars(self).items():
            if name in memeber_set:
                memeber_set.remove(name)
        if len(memeber_set) > 0:
            warnings.warn("%s fileds are useless." % ",".join(memeber_set))
        


class DescribeColumnsResponse(AbstractModel):
    """DescribeColumns返回参数结构体

    """

    def __init__(self):
        r"""
        :param Columns: 字段信息
        :type Columns: list of Column
        :param TotalElements: 总字段个数
        :type TotalElements: int
        :param TotalPages: 总页数
        :type TotalPages: int
        :param RequestId: 唯一请求 ID，每次请求都会返回。定位问题时需要提供该次请求的 RequestId。
        :type RequestId: str
        """
        self.Columns = None
        self.TotalElements = None
        self.TotalPages = None
        self.RequestId = None


    def _deserialize(self, params):
        if params.get("Columns") is not None:
            self.Columns = []
            for item in params.get("Columns"):
                obj = Column()
                obj._deserialize(item)
                self.Columns.append(obj)
        self.TotalElements = params.get("TotalElements")
        self.TotalPages = params.get("TotalPages")
        self.RequestId = params.get("RequestId")


class DescribeDLCCHDFSBindingListRequest(AbstractModel):
    """DescribeDLCCHDFSBindingList请求参数结构体

    """

    def __init__(self):
        r"""
        :param BucketId: 桶名
        :type BucketId: str
        """
        self.BucketId = None


    def _deserialize(self, params):
        self.BucketId = params.get("BucketId")
        memeber_set = set(params.keys())
        for name, value in vars(self).items():
            if name in memeber_set:
                memeber_set.remove(name)
        if len(memeber_set) > 0:
            warnings.warn("%s fileds are useless." % ",".join(memeber_set))
        


class DescribeDLCCHDFSBindingListResponse(AbstractModel):
    """DescribeDLCCHDFSBindingList返回参数结构体

    """

    def __init__(self):
        r"""
        :param DLCCHDFSBindingList: dlc引擎绑定桶列表
        :type DLCCHDFSBindingList: list of DLCCHDFSBinding
        :param Total: 列表数
        :type Total: int
        :param RequestId: 唯一请求 ID，每次请求都会返回。定位问题时需要提供该次请求的 RequestId。
        :type RequestId: str
        """
        self.DLCCHDFSBindingList = None
        self.Total = None
        self.RequestId = None


    def _deserialize(self, params):
        if params.get("DLCCHDFSBindingList") is not None:
            self.DLCCHDFSBindingList = []
            for item in params.get("DLCCHDFSBindingList"):
                obj = DLCCHDFSBinding()
                obj._deserialize(item)
                self.DLCCHDFSBindingList.append(obj)
        self.Total = params.get("Total")
        self.RequestId = params.get("RequestId")


class DescribeDMSDatabaseRequest(AbstractModel):
    """DescribeDMSDatabase请求参数结构体

    """

    def __init__(self):
        r"""
        :param Name: 数据库名称
        :type Name: str
        :param SchemaName: schema名称
        :type SchemaName: str
        :param Pattern: 匹配规则
        :type Pattern: str
        """
        self.Name = None
        self.SchemaName = None
        self.Pattern = None


    def _deserialize(self, params):
        self.Name = params.get("Name")
        self.SchemaName = params.get("SchemaName")
        self.Pattern = params.get("Pattern")
        memeber_set = set(params.keys())
        for name, value in vars(self).items():
            if name in memeber_set:
                memeber_set.remove(name)
        if len(memeber_set) > 0:
            warnings.warn("%s fileds are useless." % ",".join(memeber_set))
        


class DescribeDMSDatabaseResponse(AbstractModel):
    """DescribeDMSDatabase返回参数结构体

    """

    def __init__(self):
        r"""
        :param Name: 数据库名称
注意：此字段可能返回 null，表示取不到有效值。
        :type Name: str
        :param SchemaName: schema名称
注意：此字段可能返回 null，表示取不到有效值。
        :type SchemaName: str
        :param Location: 存储地址
注意：此字段可能返回 null，表示取不到有效值。
        :type Location: str
        :param Asset: 数据对象
注意：此字段可能返回 null，表示取不到有效值。
        :type Asset: :class:`tencentcloud.dlc.v20210125.models.Asset`
        :param RequestId: 唯一请求 ID，每次请求都会返回。定位问题时需要提供该次请求的 RequestId。
        :type RequestId: str
        """
        self.Name = None
        self.SchemaName = None
        self.Location = None
        self.Asset = None
        self.RequestId = None


    def _deserialize(self, params):
        self.Name = params.get("Name")
        self.SchemaName = params.get("SchemaName")
        self.Location = params.get("Location")
        if params.get("Asset") is not None:
            self.Asset = Asset()
            self.Asset._deserialize(params.get("Asset"))
        self.RequestId = params.get("RequestId")


class DescribeDMSPartitionColumnStatisticListRequest(AbstractModel):
    """DescribeDMSPartitionColumnStatisticList请求参数结构体

    """

    def __init__(self):
        r"""
        :param DatabaseName: 数据库名
        :type DatabaseName: str
        :param TableName: 表名称
        :type TableName: str
        :param PartitionName: 分区名
        :type PartitionName: str
        :param PartitionNames: 分区名列表
        :type PartitionNames: list of str
        :param ColumnName: Column名称
        :type ColumnName: str
        :param ColumnNames: Column列表
        :type ColumnNames: list of str
        """
        self.DatabaseName = None
        self.TableName = None
        self.PartitionName = None
        self.PartitionNames = None
        self.ColumnName = None
        self.ColumnNames = None


    def _deserialize(self, params):
        self.DatabaseName = params.get("DatabaseName")
        self.TableName = params.get("TableName")
        self.PartitionName = params.get("PartitionName")
        self.PartitionNames = params.get("PartitionNames")
        self.ColumnName = params.get("ColumnName")
        self.ColumnNames = params.get("ColumnNames")
        memeber_set = set(params.keys())
        for name, value in vars(self).items():
            if name in memeber_set:
                memeber_set.remove(name)
        if len(memeber_set) > 0:
            warnings.warn("%s fileds are useless." % ",".join(memeber_set))
        


class DescribeDMSPartitionColumnStatisticListResponse(AbstractModel):
    """DescribeDMSPartitionColumnStatisticList返回参数结构体

    """

    def __init__(self):
        r"""
        :param TotalCount: 总数
        :type TotalCount: int
        :param PartitionStatisticList: 分区统计信息列表
        :type PartitionStatisticList: list of DMSPartitionColumnStatisticInfo
        :param RequestId: 唯一请求 ID，每次请求都会返回。定位问题时需要提供该次请求的 RequestId。
        :type RequestId: str
        """
        self.TotalCount = None
        self.PartitionStatisticList = None
        self.RequestId = None


    def _deserialize(self, params):
        self.TotalCount = params.get("TotalCount")
        if params.get("PartitionStatisticList") is not None:
            self.PartitionStatisticList = []
            for item in params.get("PartitionStatisticList"):
                obj = DMSPartitionColumnStatisticInfo()
                obj._deserialize(item)
                self.PartitionStatisticList.append(obj)
        self.RequestId = params.get("RequestId")


class DescribeDMSPartitionsRequest(AbstractModel):
    """DescribeDMSPartitions请求参数结构体

    """

    def __init__(self):
        r"""
        :param DatabaseName: 数据库名
        :type DatabaseName: str
        :param TableName: 表名称
        :type TableName: str
        :param SchemaName: schema名称
        :type SchemaName: str
        :param Name: 名称
        :type Name: str
        :param Values: 单个分区名称，精准匹配
        :type Values: list of str
        :param PartitionNames: 多个分区名称，精准匹配
        :type PartitionNames: list of str
        :param PartValues: 多个分区字段的匹配，模糊匹配
        :type PartValues: list of str
        :param Filter: 过滤SQL
        :type Filter: str
        :param MaxParts: 最大分区数量
        :type MaxParts: int
        :param Offset: 翻页跳过数量
        :type Offset: int
        :param Limit: 页面数量
        :type Limit: int
        :param Expression: 表达式
        :type Expression: str
        """
        self.DatabaseName = None
        self.TableName = None
        self.SchemaName = None
        self.Name = None
        self.Values = None
        self.PartitionNames = None
        self.PartValues = None
        self.Filter = None
        self.MaxParts = None
        self.Offset = None
        self.Limit = None
        self.Expression = None


    def _deserialize(self, params):
        self.DatabaseName = params.get("DatabaseName")
        self.TableName = params.get("TableName")
        self.SchemaName = params.get("SchemaName")
        self.Name = params.get("Name")
        self.Values = params.get("Values")
        self.PartitionNames = params.get("PartitionNames")
        self.PartValues = params.get("PartValues")
        self.Filter = params.get("Filter")
        self.MaxParts = params.get("MaxParts")
        self.Offset = params.get("Offset")
        self.Limit = params.get("Limit")
        self.Expression = params.get("Expression")
        memeber_set = set(params.keys())
        for name, value in vars(self).items():
            if name in memeber_set:
                memeber_set.remove(name)
        if len(memeber_set) > 0:
            warnings.warn("%s fileds are useless." % ",".join(memeber_set))
        


class DescribeDMSPartitionsResponse(AbstractModel):
    """DescribeDMSPartitions返回参数结构体

    """

    def __init__(self):
        r"""
        :param Partitions: 分区信息
        :type Partitions: list of DMSPartition
        :param Total: 总数
        :type Total: int
        :param RequestId: 唯一请求 ID，每次请求都会返回。定位问题时需要提供该次请求的 RequestId。
        :type RequestId: str
        """
        self.Partitions = None
        self.Total = None
        self.RequestId = None


    def _deserialize(self, params):
        if params.get("Partitions") is not None:
            self.Partitions = []
            for item in params.get("Partitions"):
                obj = DMSPartition()
                obj._deserialize(item)
                self.Partitions.append(obj)
        self.Total = params.get("Total")
        self.RequestId = params.get("RequestId")


class DescribeDMSTableColumnStatisticListRequest(AbstractModel):
    """DescribeDMSTableColumnStatisticList请求参数结构体

    """

    def __init__(self):
        r"""
        :param DatabaseName: 数据库名
        :type DatabaseName: str
        :param TableName: 表名称
        :type TableName: str
        :param ColumnName: Column名称
        :type ColumnName: str
        :param ColumnNames: Column列表
        :type ColumnNames: list of str
        """
        self.DatabaseName = None
        self.TableName = None
        self.ColumnName = None
        self.ColumnNames = None


    def _deserialize(self, params):
        self.DatabaseName = params.get("DatabaseName")
        self.TableName = params.get("TableName")
        self.ColumnName = params.get("ColumnName")
        self.ColumnNames = params.get("ColumnNames")
        memeber_set = set(params.keys())
        for name, value in vars(self).items():
            if name in memeber_set:
                memeber_set.remove(name)
        if len(memeber_set) > 0:
            warnings.warn("%s fileds are useless." % ",".join(memeber_set))
        


class DescribeDMSTableColumnStatisticListResponse(AbstractModel):
    """DescribeDMSTableColumnStatisticList返回参数结构体

    """

    def __init__(self):
        r"""
        :param TableStatisticList: 表字段统计信息列表
        :type TableStatisticList: list of DMSTableColumnStatisticInfo
        :param TotalCount: 总数
        :type TotalCount: int
        :param RequestId: 唯一请求 ID，每次请求都会返回。定位问题时需要提供该次请求的 RequestId。
        :type RequestId: str
        """
        self.TableStatisticList = None
        self.TotalCount = None
        self.RequestId = None


    def _deserialize(self, params):
        if params.get("TableStatisticList") is not None:
            self.TableStatisticList = []
            for item in params.get("TableStatisticList"):
                obj = DMSTableColumnStatisticInfo()
                obj._deserialize(item)
                self.TableStatisticList.append(obj)
        self.TotalCount = params.get("TotalCount")
        self.RequestId = params.get("RequestId")


class DescribeDMSTableRequest(AbstractModel):
    """DescribeDMSTable请求参数结构体

    """

    def __init__(self):
        r"""
        :param DbName: 数据库名称
        :type DbName: str
        :param SchemaName: 数据库schema名称
        :type SchemaName: str
        :param Name: 表名称
        :type Name: str
        :param Catalog: 数据目录
        :type Catalog: str
        :param Keyword: 查询关键词
        :type Keyword: str
        :param Pattern: 查询模式
        :type Pattern: str
        :param Type: 表类型
        :type Type: str
        """
        self.DbName = None
        self.SchemaName = None
        self.Name = None
        self.Catalog = None
        self.Keyword = None
        self.Pattern = None
        self.Type = None


    def _deserialize(self, params):
        self.DbName = params.get("DbName")
        self.SchemaName = params.get("SchemaName")
        self.Name = params.get("Name")
        self.Catalog = params.get("Catalog")
        self.Keyword = params.get("Keyword")
        self.Pattern = params.get("Pattern")
        self.Type = params.get("Type")
        memeber_set = set(params.keys())
        for name, value in vars(self).items():
            if name in memeber_set:
                memeber_set.remove(name)
        if len(memeber_set) > 0:
            warnings.warn("%s fileds are useless." % ",".join(memeber_set))
        


class DescribeDMSTableResponse(AbstractModel):
    """DescribeDMSTable返回参数结构体

    """

    def __init__(self):
        r"""
        :param Asset: 基础对象
注意：此字段可能返回 null，表示取不到有效值。
        :type Asset: :class:`tencentcloud.dlc.v20210125.models.Asset`
        :param ViewOriginalText: 视图文本
注意：此字段可能返回 null，表示取不到有效值。
        :type ViewOriginalText: str
        :param ViewExpandedText: 视图文本
注意：此字段可能返回 null，表示取不到有效值。
        :type ViewExpandedText: str
        :param Retention: hive维护版本
注意：此字段可能返回 null，表示取不到有效值。
        :type Retention: int
        :param Sds: 存储对象
注意：此字段可能返回 null，表示取不到有效值。
        :type Sds: :class:`tencentcloud.dlc.v20210125.models.DMSSds`
        :param PartitionKeys: 分区列
注意：此字段可能返回 null，表示取不到有效值。
        :type PartitionKeys: list of DMSColumn
        :param Partitions: 分区
注意：此字段可能返回 null，表示取不到有效值。
        :type Partitions: list of DMSPartition
        :param Type: 表类型
注意：此字段可能返回 null，表示取不到有效值。
        :type Type: str
        :param DbName: 数据库名称
注意：此字段可能返回 null，表示取不到有效值。
        :type DbName: str
        :param SchemaName: Schame名称
注意：此字段可能返回 null，表示取不到有效值。
        :type SchemaName: str
        :param StorageSize: 存储大小
注意：此字段可能返回 null，表示取不到有效值。
        :type StorageSize: int
        :param RecordCount: 记录数量
注意：此字段可能返回 null，表示取不到有效值。
        :type RecordCount: int
        :param LifeTime: 生命周期
注意：此字段可能返回 null，表示取不到有效值。
        :type LifeTime: int
        :param LastAccessTime: 最后访问时间
注意：此字段可能返回 null，表示取不到有效值。
        :type LastAccessTime: str
        :param DataUpdateTime: 数据更新时间
注意：此字段可能返回 null，表示取不到有效值。
        :type DataUpdateTime: str
        :param StructUpdateTime: 结构更新时间
注意：此字段可能返回 null，表示取不到有效值。
        :type StructUpdateTime: str
        :param Columns: 列
注意：此字段可能返回 null，表示取不到有效值。
        :type Columns: list of DMSColumn
        :param Name: 表名称
注意：此字段可能返回 null，表示取不到有效值。
        :type Name: str
        :param RequestId: 唯一请求 ID，每次请求都会返回。定位问题时需要提供该次请求的 RequestId。
        :type RequestId: str
        """
        self.Asset = None
        self.ViewOriginalText = None
        self.ViewExpandedText = None
        self.Retention = None
        self.Sds = None
        self.PartitionKeys = None
        self.Partitions = None
        self.Type = None
        self.DbName = None
        self.SchemaName = None
        self.StorageSize = None
        self.RecordCount = None
        self.LifeTime = None
        self.LastAccessTime = None
        self.DataUpdateTime = None
        self.StructUpdateTime = None
        self.Columns = None
        self.Name = None
        self.RequestId = None


    def _deserialize(self, params):
        if params.get("Asset") is not None:
            self.Asset = Asset()
            self.Asset._deserialize(params.get("Asset"))
        self.ViewOriginalText = params.get("ViewOriginalText")
        self.ViewExpandedText = params.get("ViewExpandedText")
        self.Retention = params.get("Retention")
        if params.get("Sds") is not None:
            self.Sds = DMSSds()
            self.Sds._deserialize(params.get("Sds"))
        if params.get("PartitionKeys") is not None:
            self.PartitionKeys = []
            for item in params.get("PartitionKeys"):
                obj = DMSColumn()
                obj._deserialize(item)
                self.PartitionKeys.append(obj)
        if params.get("Partitions") is not None:
            self.Partitions = []
            for item in params.get("Partitions"):
                obj = DMSPartition()
                obj._deserialize(item)
                self.Partitions.append(obj)
        self.Type = params.get("Type")
        self.DbName = params.get("DbName")
        self.SchemaName = params.get("SchemaName")
        self.StorageSize = params.get("StorageSize")
        self.RecordCount = params.get("RecordCount")
        self.LifeTime = params.get("LifeTime")
        self.LastAccessTime = params.get("LastAccessTime")
        self.DataUpdateTime = params.get("DataUpdateTime")
        self.StructUpdateTime = params.get("StructUpdateTime")
        if params.get("Columns") is not None:
            self.Columns = []
            for item in params.get("Columns"):
                obj = DMSColumn()
                obj._deserialize(item)
                self.Columns.append(obj)
        self.Name = params.get("Name")
        self.RequestId = params.get("RequestId")


class DescribeDMSTablesRequest(AbstractModel):
    """DescribeDMSTables请求参数结构体

    """

    def __init__(self):
        r"""
        :param DbName: 数据库名称
        :type DbName: str
        :param SchemaName: 数据库schema名称
        :type SchemaName: str
        :param Name: 表名称
        :type Name: str
        :param Catalog: 数据目录
        :type Catalog: str
        :param Keyword: 查询关键词
        :type Keyword: str
        :param Pattern: 查询模式
        :type Pattern: str
        :param Type: 表类型
        :type Type: str
        :param StartTime: 筛选参数：更新开始时间
        :type StartTime: str
        :param EndTime: 筛选参数：更新结束时间
        :type EndTime: str
        :param Limit: 分页参数
        :type Limit: int
        :param Offset: 分页参数
        :type Offset: int
        :param Sort: 排序字段：create_time：创建时间
        :type Sort: str
        :param Asc: 排序字段：true：升序（默认），false：降序
        :type Asc: bool
        """
        self.DbName = None
        self.SchemaName = None
        self.Name = None
        self.Catalog = None
        self.Keyword = None
        self.Pattern = None
        self.Type = None
        self.StartTime = None
        self.EndTime = None
        self.Limit = None
        self.Offset = None
        self.Sort = None
        self.Asc = None


    def _deserialize(self, params):
        self.DbName = params.get("DbName")
        self.SchemaName = params.get("SchemaName")
        self.Name = params.get("Name")
        self.Catalog = params.get("Catalog")
        self.Keyword = params.get("Keyword")
        self.Pattern = params.get("Pattern")
        self.Type = params.get("Type")
        self.StartTime = params.get("StartTime")
        self.EndTime = params.get("EndTime")
        self.Limit = params.get("Limit")
        self.Offset = params.get("Offset")
        self.Sort = params.get("Sort")
        self.Asc = params.get("Asc")
        memeber_set = set(params.keys())
        for name, value in vars(self).items():
            if name in memeber_set:
                memeber_set.remove(name)
        if len(memeber_set) > 0:
            warnings.warn("%s fileds are useless." % ",".join(memeber_set))
        


class DescribeDMSTablesResponse(AbstractModel):
    """DescribeDMSTables返回参数结构体

    """

    def __init__(self):
        r"""
        :param TableList: DMS元数据列表信息
注意：此字段可能返回 null，表示取不到有效值。
        :type TableList: list of DMSTableInfo
        :param TotalCount: 统计值
注意：此字段可能返回 null，表示取不到有效值。
        :type TotalCount: int
        :param RequestId: 唯一请求 ID，每次请求都会返回。定位问题时需要提供该次请求的 RequestId。
        :type RequestId: str
        """
        self.TableList = None
        self.TotalCount = None
        self.RequestId = None


    def _deserialize(self, params):
        if params.get("TableList") is not None:
            self.TableList = []
            for item in params.get("TableList"):
                obj = DMSTableInfo()
                obj._deserialize(item)
                self.TableList.append(obj)
        self.TotalCount = params.get("TotalCount")
        self.RequestId = params.get("RequestId")


class DescribeDataEngineEventsRequest(AbstractModel):
    """DescribeDataEngineEvents请求参数结构体

    """

    def __init__(self):
        r"""
        :param DataEngineName: 虚拟集群名称
        :type DataEngineName: str
        :param Limit: 返回数量，默认为10，最大为100
        :type Limit: int
        :param Offset: 偏移量，默认为0
        :type Offset: int
        """
        self.DataEngineName = None
        self.Limit = None
        self.Offset = None


    def _deserialize(self, params):
        self.DataEngineName = params.get("DataEngineName")
        self.Limit = params.get("Limit")
        self.Offset = params.get("Offset")
        memeber_set = set(params.keys())
        for name, value in vars(self).items():
            if name in memeber_set:
                memeber_set.remove(name)
        if len(memeber_set) > 0:
            warnings.warn("%s fileds are useless." % ",".join(memeber_set))
        


class DescribeDataEngineEventsResponse(AbstractModel):
    """DescribeDataEngineEvents返回参数结构体

    """

    def __init__(self):
        r"""
        :param Events: 事件详细信息
注意：此字段可能返回 null，表示取不到有效值。
        :type Events: list of HouseEventsInfo
        :param Page: 分页号
注意：此字段可能返回 null，表示取不到有效值。
        :type Page: int
        :param Size: 分页大小
注意：此字段可能返回 null，表示取不到有效值。
        :type Size: int
        :param TotalPages: 总页数
注意：此字段可能返回 null，表示取不到有效值。
        :type TotalPages: int
        :param TotalCount: 总条数
注意：此字段可能返回 null，表示取不到有效值。
        :type TotalCount: int
        :param RequestId: 唯一请求 ID，每次请求都会返回。定位问题时需要提供该次请求的 RequestId。
        :type RequestId: str
        """
        self.Events = None
        self.Page = None
        self.Size = None
        self.TotalPages = None
        self.TotalCount = None
        self.RequestId = None


    def _deserialize(self, params):
        if params.get("Events") is not None:
            self.Events = []
            for item in params.get("Events"):
                obj = HouseEventsInfo()
                obj._deserialize(item)
                self.Events.append(obj)
        self.Page = params.get("Page")
        self.Size = params.get("Size")
        self.TotalPages = params.get("TotalPages")
        self.TotalCount = params.get("TotalCount")
        self.RequestId = params.get("RequestId")


class DescribeDataEngineImageOperateRecordsRequest(AbstractModel):
    """DescribeDataEngineImageOperateRecords请求参数结构体

    """

    def __init__(self):
        r"""
        :param RecordId: 日志记录唯一id
        :type RecordId: str
        :param DataEngineId: 引擎唯一id
        :type DataEngineId: str
        :param ImageVersionId: 集群镜像大版本唯一id
        :type ImageVersionId: str
        :param ChildImageVersionId: 集群镜像小版本唯一id
        :type ChildImageVersionId: str
        :param Operate: 操作类型：初始化：InitImage、变配ModifyResource、升级：UpgradeImage、切换：SwitchImage、回滚：RollbackImage
        :type Operate: str
        :param Sort: 排序字段：InsertTime(默认)
        :type Sort: str
        :param Asc: 排序字段：true(默认)、false
        :type Asc: bool
        :param Limit: 分页字段：10（默认），传-1查全部
        :type Limit: int
        :param Offset: 分页字段
        :type Offset: int
        """
        self.RecordId = None
        self.DataEngineId = None
        self.ImageVersionId = None
        self.ChildImageVersionId = None
        self.Operate = None
        self.Sort = None
        self.Asc = None
        self.Limit = None
        self.Offset = None


    def _deserialize(self, params):
        self.RecordId = params.get("RecordId")
        self.DataEngineId = params.get("DataEngineId")
        self.ImageVersionId = params.get("ImageVersionId")
        self.ChildImageVersionId = params.get("ChildImageVersionId")
        self.Operate = params.get("Operate")
        self.Sort = params.get("Sort")
        self.Asc = params.get("Asc")
        self.Limit = params.get("Limit")
        self.Offset = params.get("Offset")
        memeber_set = set(params.keys())
        for name, value in vars(self).items():
            if name in memeber_set:
                memeber_set.remove(name)
        if len(memeber_set) > 0:
            warnings.warn("%s fileds are useless." % ",".join(memeber_set))
        


class DescribeDataEngineImageOperateRecordsResponse(AbstractModel):
    """DescribeDataEngineImageOperateRecords返回参数结构体

    """

    def __init__(self):
        r"""
        :param ImageOperateRecords: 镜像操作日志记录列表
        :type ImageOperateRecords: list of ImageOperateRecord
        :param RequestId: 唯一请求 ID，每次请求都会返回。定位问题时需要提供该次请求的 RequestId。
        :type RequestId: str
        """
        self.ImageOperateRecords = None
        self.RequestId = None


    def _deserialize(self, params):
        if params.get("ImageOperateRecords") is not None:
            self.ImageOperateRecords = []
            for item in params.get("ImageOperateRecords"):
                obj = ImageOperateRecord()
                obj._deserialize(item)
                self.ImageOperateRecords.append(obj)
        self.RequestId = params.get("RequestId")


class DescribeDataEngineImageVersionsRequest(AbstractModel):
    """DescribeDataEngineImageVersions请求参数结构体

    """

    def __init__(self):
        r"""
        :param EngineType: 引擎类型：SQL、SparkBatch
        :type EngineType: str
        """
        self.EngineType = None


    def _deserialize(self, params):
        self.EngineType = params.get("EngineType")
        memeber_set = set(params.keys())
        for name, value in vars(self).items():
            if name in memeber_set:
                memeber_set.remove(name)
        if len(memeber_set) > 0:
            warnings.warn("%s fileds are useless." % ",".join(memeber_set))
        


class DescribeDataEngineImageVersionsResponse(AbstractModel):
    """DescribeDataEngineImageVersions返回参数结构体

    """

    def __init__(self):
        r"""
        :param ImageParentVersions: 集群大版本镜像信息列表
        :type ImageParentVersions: list of DataEngineImageVersion
        :param Total: 总数
        :type Total: int
        :param RequestId: 唯一请求 ID，每次请求都会返回。定位问题时需要提供该次请求的 RequestId。
        :type RequestId: str
        """
        self.ImageParentVersions = None
        self.Total = None
        self.RequestId = None


    def _deserialize(self, params):
        if params.get("ImageParentVersions") is not None:
            self.ImageParentVersions = []
            for item in params.get("ImageParentVersions"):
                obj = DataEngineImageVersion()
                obj._deserialize(item)
                self.ImageParentVersions.append(obj)
        self.Total = params.get("Total")
        self.RequestId = params.get("RequestId")


class DescribeDataEngineParametersRequest(AbstractModel):
    """DescribeDataEngineParameters请求参数结构体

    """

    def __init__(self):
        r"""
        :param DataEngineType: 引擎类型，当前支持SparkSQL、PrestoSQL，不传默认查所有。
        :type DataEngineType: str
        :param ParameterType: 配置类型：1：session，2：common，3：cluster
        :type ParameterType: int
        """
        self.DataEngineType = None
        self.ParameterType = None


    def _deserialize(self, params):
        self.DataEngineType = params.get("DataEngineType")
        self.ParameterType = params.get("ParameterType")
        memeber_set = set(params.keys())
        for name, value in vars(self).items():
            if name in memeber_set:
                memeber_set.remove(name)
        if len(memeber_set) > 0:
            warnings.warn("%s fileds are useless." % ",".join(memeber_set))
        


class DescribeDataEngineParametersResponse(AbstractModel):
    """DescribeDataEngineParameters返回参数结构体

    """

    def __init__(self):
        r"""
        :param EngineType: 引擎类型，当前支持spark或presto
        :type EngineType: str
        :param EngineParameters: 引擎参数列表信息
        :type EngineParameters: list of EngineParameter
        :param RequestId: 唯一请求 ID，每次请求都会返回。定位问题时需要提供该次请求的 RequestId。
        :type RequestId: str
        """
        self.EngineType = None
        self.EngineParameters = None
        self.RequestId = None


    def _deserialize(self, params):
        self.EngineType = params.get("EngineType")
        if params.get("EngineParameters") is not None:
            self.EngineParameters = []
            for item in params.get("EngineParameters"):
                obj = EngineParameter()
                obj._deserialize(item)
                self.EngineParameters.append(obj)
        self.RequestId = params.get("RequestId")


class DescribeDataEnginePythonSparkImagesRequest(AbstractModel):
    """DescribeDataEnginePythonSparkImages请求参数结构体

    """

    def __init__(self):
        r"""
        :param ChildImageVersionId: 集群镜像小版本ID
        :type ChildImageVersionId: str
        """
        self.ChildImageVersionId = None


    def _deserialize(self, params):
        self.ChildImageVersionId = params.get("ChildImageVersionId")
        memeber_set = set(params.keys())
        for name, value in vars(self).items():
            if name in memeber_set:
                memeber_set.remove(name)
        if len(memeber_set) > 0:
            warnings.warn("%s fileds are useless." % ",".join(memeber_set))
        


class DescribeDataEnginePythonSparkImagesResponse(AbstractModel):
    """DescribeDataEnginePythonSparkImages返回参数结构体

    """

    def __init__(self):
        r"""
        :param PythonSparkImages: PYSPARK镜像信息列表
        :type PythonSparkImages: list of PythonSparkImage
        :param RequestId: 唯一请求 ID，每次请求都会返回。定位问题时需要提供该次请求的 RequestId。
        :type RequestId: str
        """
        self.PythonSparkImages = None
        self.RequestId = None


    def _deserialize(self, params):
        if params.get("PythonSparkImages") is not None:
            self.PythonSparkImages = []
            for item in params.get("PythonSparkImages"):
                obj = PythonSparkImage()
                obj._deserialize(item)
                self.PythonSparkImages.append(obj)
        self.RequestId = params.get("RequestId")


class DescribeDataEngineRequest(AbstractModel):
    """DescribeDataEngine请求参数结构体

    """

    def __init__(self):
        r"""
        :param DataEngineName: House名称
        :type DataEngineName: str
        """
        self.DataEngineName = None


    def _deserialize(self, params):
        self.DataEngineName = params.get("DataEngineName")
        memeber_set = set(params.keys())
        for name, value in vars(self).items():
            if name in memeber_set:
                memeber_set.remove(name)
        if len(memeber_set) > 0:
            warnings.warn("%s fileds are useless." % ",".join(memeber_set))
        


class DescribeDataEngineResponse(AbstractModel):
    """DescribeDataEngine返回参数结构体

    """

    def __init__(self):
        r"""
        :param DataEngine: 数据引擎详细信息
        :type DataEngine: :class:`tencentcloud.dlc.v20210125.models.DataEngineInfo`
        :param RequestId: 唯一请求 ID，每次请求都会返回。定位问题时需要提供该次请求的 RequestId。
        :type RequestId: str
        """
        self.DataEngine = None
        self.RequestId = None


    def _deserialize(self, params):
        if params.get("DataEngine") is not None:
            self.DataEngine = DataEngineInfo()
            self.DataEngine._deserialize(params.get("DataEngine"))
        self.RequestId = params.get("RequestId")


class DescribeDataEngineSessionParametersRequest(AbstractModel):
    """DescribeDataEngineSessionParameters请求参数结构体

    """

    def __init__(self):
        r"""
        :param DataEngineId: 引擎id
        :type DataEngineId: str
        :param DataEngineName: 引擎名称，当指定引擎名称后优先使用名称获取配置
        :type DataEngineName: str
        """
        self.DataEngineId = None
        self.DataEngineName = None


    def _deserialize(self, params):
        self.DataEngineId = params.get("DataEngineId")
        self.DataEngineName = params.get("DataEngineName")
        memeber_set = set(params.keys())
        for name, value in vars(self).items():
            if name in memeber_set:
                memeber_set.remove(name)
        if len(memeber_set) > 0:
            warnings.warn("%s fileds are useless." % ",".join(memeber_set))
        


class DescribeDataEngineSessionParametersResponse(AbstractModel):
    """DescribeDataEngineSessionParameters返回参数结构体

    """

    def __init__(self):
        r"""
        :param DataEngineParameters: 集群Session配置列表
        :type DataEngineParameters: list of DataEngineImageSessionParameter
        :param RequestId: 唯一请求 ID，每次请求都会返回。定位问题时需要提供该次请求的 RequestId。
        :type RequestId: str
        """
        self.DataEngineParameters = None
        self.RequestId = None


    def _deserialize(self, params):
        if params.get("DataEngineParameters") is not None:
            self.DataEngineParameters = []
            for item in params.get("DataEngineParameters"):
                obj = DataEngineImageSessionParameter()
                obj._deserialize(item)
                self.DataEngineParameters.append(obj)
        self.RequestId = params.get("RequestId")


class DescribeDataEnginesRequest(AbstractModel):
    """DescribeDataEngines请求参数结构体

    """

    def __init__(self):
        r"""
        :param Offset: 偏移量，默认为0。
        :type Offset: int
        :param Filters: 过滤类型，支持如下的过滤类型，传参Name应为以下其中一个, data-engine-name - String（数据引擎名称）：engine-type - String（引擎类型：spark：spark 引擎，presto：presto引擎），state - String (数据引擎状态 -2已删除 -1失败 0初始化中 1挂起 2运行中 3准备删除 4删除中) ， mode - String（计费模式 0共享模式 1按量计费 2包年包月） ， create-time - String（创建时间，10位时间戳） message - String （描述信息），cluster-type - String (集群资源类型 spark_private/presto_private/presto_cu/spark_cu)，engine-id - String（数据引擎ID），key-word - String（数据引擎名称或集群资源类型或描述信息模糊搜索），engine-exec-type - String（引擎执行任务类型，SQL/BATCH）
        :type Filters: list of Filter
        :param SortBy: 排序字段，支持如下字段类型，create-time
        :type SortBy: str
        :param Sorting: 排序方式，desc表示正序，asc表示反序， 默认为asc。
        :type Sorting: str
        :param Limit: 返回数量，默认为10，最大值为100。
        :type Limit: int
        :param DatasourceConnectionName: 已废弃，请使用DatasourceConnectionNameSet
        :type DatasourceConnectionName: str
        :param ExcludePublicEngine: 是否不返回共享引擎，true不返回共享引擎，false可以返回共享引擎
        :type ExcludePublicEngine: bool
        :param AccessTypes: 参数应该为引擎权限类型，有效类型："USE", "MODIFY", "OPERATE", "MONITOR", "DELETE"
        :type AccessTypes: list of str
        :param EngineExecType: 引擎执行任务类型，有效值：SQL/BATCH，默认为SQL
        :type EngineExecType: str
        :param EngineType: 引擎类型，有效值：spark/presto
        :type EngineType: str
        :param DatasourceConnectionNameSet: 网络配置列表，若传入该参数，则返回网络配置关联的计算引擎
        :type DatasourceConnectionNameSet: list of str
        """
        self.Offset = None
        self.Filters = None
        self.SortBy = None
        self.Sorting = None
        self.Limit = None
        self.DatasourceConnectionName = None
        self.ExcludePublicEngine = None
        self.AccessTypes = None
        self.EngineExecType = None
        self.EngineType = None
        self.DatasourceConnectionNameSet = None


    def _deserialize(self, params):
        self.Offset = params.get("Offset")
        if params.get("Filters") is not None:
            self.Filters = []
            for item in params.get("Filters"):
                obj = Filter()
                obj._deserialize(item)
                self.Filters.append(obj)
        self.SortBy = params.get("SortBy")
        self.Sorting = params.get("Sorting")
        self.Limit = params.get("Limit")
        self.DatasourceConnectionName = params.get("DatasourceConnectionName")
        self.ExcludePublicEngine = params.get("ExcludePublicEngine")
        self.AccessTypes = params.get("AccessTypes")
        self.EngineExecType = params.get("EngineExecType")
        self.EngineType = params.get("EngineType")
        self.DatasourceConnectionNameSet = params.get("DatasourceConnectionNameSet")
        memeber_set = set(params.keys())
        for name, value in vars(self).items():
            if name in memeber_set:
                memeber_set.remove(name)
        if len(memeber_set) > 0:
            warnings.warn("%s fileds are useless." % ",".join(memeber_set))
        


class DescribeDataEnginesResponse(AbstractModel):
    """DescribeDataEngines返回参数结构体

    """

    def __init__(self):
        r"""
        :param DataEngines: 数据引擎列表
注意：此字段可能返回 null，表示取不到有效值。
        :type DataEngines: list of DataEngineInfo
        :param TotalCount: 总条数
注意：此字段可能返回 null，表示取不到有效值。
        :type TotalCount: int
        :param RequestId: 唯一请求 ID，每次请求都会返回。定位问题时需要提供该次请求的 RequestId。
        :type RequestId: str
        """
        self.DataEngines = None
        self.TotalCount = None
        self.RequestId = None


    def _deserialize(self, params):
        if params.get("DataEngines") is not None:
            self.DataEngines = []
            for item in params.get("DataEngines"):
                obj = DataEngineInfo()
                obj._deserialize(item)
                self.DataEngines.append(obj)
        self.TotalCount = params.get("TotalCount")
        self.RequestId = params.get("RequestId")


class DescribeDataQueriesRequest(AbstractModel):
    """DescribeDataQueries请求参数结构体

    """

    def __init__(self):
        r"""
        :param Offset: 偏移位置
        :type Offset: int
        :param Limit: 列举个数
        :type Limit: int
        :param Dir: 目录名称
        :type Dir: str
        :param Fuzzy: 按照名称模糊查询
        :type Fuzzy: str
        """
        self.Offset = None
        self.Limit = None
        self.Dir = None
        self.Fuzzy = None


    def _deserialize(self, params):
        self.Offset = params.get("Offset")
        self.Limit = params.get("Limit")
        self.Dir = params.get("Dir")
        self.Fuzzy = params.get("Fuzzy")
        memeber_set = set(params.keys())
        for name, value in vars(self).items():
            if name in memeber_set:
                memeber_set.remove(name)
        if len(memeber_set) > 0:
            warnings.warn("%s fileds are useless." % ",".join(memeber_set))
        


class DescribeDataQueriesResponse(AbstractModel):
    """DescribeDataQueries返回参数结构体

    """

    def __init__(self):
        r"""
        :param Queries: 数据查询清单
注意：此字段可能返回 null，表示取不到有效值。
        :type Queries: list of DataQuery
        :param Total: 当前用户的所有数据查询数量
注意：此字段可能返回 null，表示取不到有效值。
        :type Total: int
        :param RequestId: 唯一请求 ID，每次请求都会返回。定位问题时需要提供该次请求的 RequestId。
        :type RequestId: str
        """
        self.Queries = None
        self.Total = None
        self.RequestId = None


    def _deserialize(self, params):
        if params.get("Queries") is not None:
            self.Queries = []
            for item in params.get("Queries"):
                obj = DataQuery()
                obj._deserialize(item)
                self.Queries.append(obj)
        self.Total = params.get("Total")
        self.RequestId = params.get("RequestId")


class DescribeDataQueryRequest(AbstractModel):
    """DescribeDataQuery请求参数结构体

    """

    def __init__(self):
        r"""
        :param Name: 查询名称
        :type Name: str
        :param Id: 查询ID
        :type Id: str
        """
        self.Name = None
        self.Id = None


    def _deserialize(self, params):
        self.Name = params.get("Name")
        self.Id = params.get("Id")
        memeber_set = set(params.keys())
        for name, value in vars(self).items():
            if name in memeber_set:
                memeber_set.remove(name)
        if len(memeber_set) > 0:
            warnings.warn("%s fileds are useless." % ",".join(memeber_set))
        


class DescribeDataQueryResponse(AbstractModel):
    """DescribeDataQuery返回参数结构体

    """

    def __init__(self):
        r"""
        :param Queries: 查询清单
注意：此字段可能返回 null，表示取不到有效值。
        :type Queries: list of DataQuery
        :param RequestId: 唯一请求 ID，每次请求都会返回。定位问题时需要提供该次请求的 RequestId。
        :type RequestId: str
        """
        self.Queries = None
        self.RequestId = None


    def _deserialize(self, params):
        if params.get("Queries") is not None:
            self.Queries = []
            for item in params.get("Queries"):
                obj = DataQuery()
                obj._deserialize(item)
                self.Queries.append(obj)
        self.RequestId = params.get("RequestId")


class DescribeDataTaskAlarmFiledRequest(AbstractModel):
    """DescribeDataTaskAlarmFiled请求参数结构体

    """

    def __init__(self):
        r"""
        :param DataTaskId: 数据任务ID
        :type DataTaskId: str
        """
        self.DataTaskId = None


    def _deserialize(self, params):
        self.DataTaskId = params.get("DataTaskId")
        memeber_set = set(params.keys())
        for name, value in vars(self).items():
            if name in memeber_set:
                memeber_set.remove(name)
        if len(memeber_set) > 0:
            warnings.warn("%s fileds are useless." % ",".join(memeber_set))
        


class DescribeDataTaskAlarmFiledResponse(AbstractModel):
    """DescribeDataTaskAlarmFiled返回参数结构体

    """

    def __init__(self):
        r"""
        :param TaskName: 任务名称
        :type TaskName: str
        :param RequestId: 唯一请求 ID，每次请求都会返回。定位问题时需要提供该次请求的 RequestId。
        :type RequestId: str
        """
        self.TaskName = None
        self.RequestId = None


    def _deserialize(self, params):
        self.TaskName = params.get("TaskName")
        self.RequestId = params.get("RequestId")


class DescribeDatabaseRequest(AbstractModel):
    """DescribeDatabase请求参数结构体

    """

    def __init__(self):
        r"""
        :param DatabaseName: 数据库名称
        :type DatabaseName: str
        :param DatasourceConnectionName: 数据连接名称，不填默认为DataLakeCatalog
        :type DatasourceConnectionName: str
        """
        self.DatabaseName = None
        self.DatasourceConnectionName = None


    def _deserialize(self, params):
        self.DatabaseName = params.get("DatabaseName")
        self.DatasourceConnectionName = params.get("DatasourceConnectionName")
        memeber_set = set(params.keys())
        for name, value in vars(self).items():
            if name in memeber_set:
                memeber_set.remove(name)
        if len(memeber_set) > 0:
            warnings.warn("%s fileds are useless." % ",".join(memeber_set))
        


class DescribeDatabaseResponse(AbstractModel):
    """DescribeDatabase返回参数结构体

    """

    def __init__(self):
        r"""
        :param DatabaseInfo: 数据库信息
        :type DatabaseInfo: :class:`tencentcloud.dlc.v20210125.models.DatabaseResponseInfo`
        :param RequestId: 唯一请求 ID，每次请求都会返回。定位问题时需要提供该次请求的 RequestId。
        :type RequestId: str
        """
        self.DatabaseInfo = None
        self.RequestId = None


    def _deserialize(self, params):
        if params.get("DatabaseInfo") is not None:
            self.DatabaseInfo = DatabaseResponseInfo()
            self.DatabaseInfo._deserialize(params.get("DatabaseInfo"))
        self.RequestId = params.get("RequestId")


class DescribeDatabaseUDFListRequest(AbstractModel):
    """DescribeDatabaseUDFList请求参数结构体

    """

    def __init__(self):
        r"""
        :param DatabaseName: 数据库名称
        :type DatabaseName: str
        :param Name: UDF名称
        :type Name: str
        :param StartTime: 开始时间，秒时间戳
        :type StartTime: int
        :param EndTime: 结束时间，秒时间戳
        :type EndTime: int
        :param Sort: 排序字段
        :type Sort: str
        :param Asc: 升序or降序
        :type Asc: bool
        :param Limit: 展示条数
        :type Limit: int
        :param Offset: 偏移量
        :type Offset: int
        """
        self.DatabaseName = None
        self.Name = None
        self.StartTime = None
        self.EndTime = None
        self.Sort = None
        self.Asc = None
        self.Limit = None
        self.Offset = None


    def _deserialize(self, params):
        self.DatabaseName = params.get("DatabaseName")
        self.Name = params.get("Name")
        self.StartTime = params.get("StartTime")
        self.EndTime = params.get("EndTime")
        self.Sort = params.get("Sort")
        self.Asc = params.get("Asc")
        self.Limit = params.get("Limit")
        self.Offset = params.get("Offset")
        memeber_set = set(params.keys())
        for name, value in vars(self).items():
            if name in memeber_set:
                memeber_set.remove(name)
        if len(memeber_set) > 0:
            warnings.warn("%s fileds are useless." % ",".join(memeber_set))
        


class DescribeDatabaseUDFListResponse(AbstractModel):
    """DescribeDatabaseUDFList返回参数结构体

    """

    def __init__(self):
        r"""
        :param TotalCount: 列表总数
注意：此字段可能返回 null，表示取不到有效值。
        :type TotalCount: int
        :param Rows: UDF数据
注意：此字段可能返回 null，表示取不到有效值。
        :type Rows: list of UdfInfo
        :param RequestId: 唯一请求 ID，每次请求都会返回。定位问题时需要提供该次请求的 RequestId。
        :type RequestId: str
        """
        self.TotalCount = None
        self.Rows = None
        self.RequestId = None


    def _deserialize(self, params):
        self.TotalCount = params.get("TotalCount")
        if params.get("Rows") is not None:
            self.Rows = []
            for item in params.get("Rows"):
                obj = UdfInfo()
                obj._deserialize(item)
                self.Rows.append(obj)
        self.RequestId = params.get("RequestId")


class DescribeDatabasesRequest(AbstractModel):
    """DescribeDatabases请求参数结构体

    """

    def __init__(self):
        r"""
        :param Limit: 返回数量，默认为10，最大值为100。
        :type Limit: int
        :param Offset: 数据偏移量，从0开始，默认为0。
        :type Offset: int
        :param KeyWord: 模糊匹配，库名关键字。
        :type KeyWord: str
        :param DatasourceConnectionName: 数据源唯名称，该名称可以通过DescribeDatasourceConnection接口查询到。默认为DataLakeCatalog
        :type DatasourceConnectionName: str
        :param Sort: 排序字段，CreateTime：创建时间，Name：数据库名称
        :type Sort: str
        :param Asc: 排序类型：false：降序（默认）、true：升序
        :type Asc: bool
        """
        self.Limit = None
        self.Offset = None
        self.KeyWord = None
        self.DatasourceConnectionName = None
        self.Sort = None
        self.Asc = None


    def _deserialize(self, params):
        self.Limit = params.get("Limit")
        self.Offset = params.get("Offset")
        self.KeyWord = params.get("KeyWord")
        self.DatasourceConnectionName = params.get("DatasourceConnectionName")
        self.Sort = params.get("Sort")
        self.Asc = params.get("Asc")
        memeber_set = set(params.keys())
        for name, value in vars(self).items():
            if name in memeber_set:
                memeber_set.remove(name)
        if len(memeber_set) > 0:
            warnings.warn("%s fileds are useless." % ",".join(memeber_set))
        


class DescribeDatabasesResponse(AbstractModel):
    """DescribeDatabases返回参数结构体

    """

    def __init__(self):
        r"""
        :param DatabaseList: 数据库对象列表。
        :type DatabaseList: list of DatabaseResponseInfo
        :param TotalCount: 实例总数。
        :type TotalCount: int
        :param RequestId: 唯一请求 ID，每次请求都会返回。定位问题时需要提供该次请求的 RequestId。
        :type RequestId: str
        """
        self.DatabaseList = None
        self.TotalCount = None
        self.RequestId = None


    def _deserialize(self, params):
        if params.get("DatabaseList") is not None:
            self.DatabaseList = []
            for item in params.get("DatabaseList"):
                obj = DatabaseResponseInfo()
                obj._deserialize(item)
                self.DatabaseList.append(obj)
        self.TotalCount = params.get("TotalCount")
        self.RequestId = params.get("RequestId")


class DescribeDatasourceConnectionRequest(AbstractModel):
    """DescribeDatasourceConnection请求参数结构体

    """

    def __init__(self):
        r"""
        :param DatasourceConnectionIds: 连接ID列表，指定要查询的连接ID
        :type DatasourceConnectionIds: list of str
        :param Filters: 过滤条件，当前支持的过滤键为：DatasourceConnectionName（数据源连接名）。
DatasourceConnectionType   （数据源连接连接类型）
        :type Filters: list of Filter
        :param Offset: 偏移量，默认为0
        :type Offset: int
        :param Limit: 返回数量，默认20，最大值100
        :type Limit: int
        :param SortBy: 排序字段，支持如下字段类型，create-time（默认，创建时间）、update-time（更新时间）
        :type SortBy: str
        :param Sorting: 排序方式，desc表示正序，asc表示反序， 默认为desc
        :type Sorting: str
        :param StartTime: 筛选字段：起始时间
        :type StartTime: str
        :param EndTime: 筛选字段：截止时间
        :type EndTime: str
        :param DatasourceConnectionNames: 连接名称列表，指定要查询的连接名称
        :type DatasourceConnectionNames: list of str
        :param DatasourceConnectionTypes: 连接类型，支持Mysql/HiveCos/Kafka/DataLakeCatalog
        :type DatasourceConnectionTypes: list of str
        """
        self.DatasourceConnectionIds = None
        self.Filters = None
        self.Offset = None
        self.Limit = None
        self.SortBy = None
        self.Sorting = None
        self.StartTime = None
        self.EndTime = None
        self.DatasourceConnectionNames = None
        self.DatasourceConnectionTypes = None


    def _deserialize(self, params):
        self.DatasourceConnectionIds = params.get("DatasourceConnectionIds")
        if params.get("Filters") is not None:
            self.Filters = []
            for item in params.get("Filters"):
                obj = Filter()
                obj._deserialize(item)
                self.Filters.append(obj)
        self.Offset = params.get("Offset")
        self.Limit = params.get("Limit")
        self.SortBy = params.get("SortBy")
        self.Sorting = params.get("Sorting")
        self.StartTime = params.get("StartTime")
        self.EndTime = params.get("EndTime")
        self.DatasourceConnectionNames = params.get("DatasourceConnectionNames")
        self.DatasourceConnectionTypes = params.get("DatasourceConnectionTypes")
        memeber_set = set(params.keys())
        for name, value in vars(self).items():
            if name in memeber_set:
                memeber_set.remove(name)
        if len(memeber_set) > 0:
            warnings.warn("%s fileds are useless." % ",".join(memeber_set))
        


class DescribeDatasourceConnectionResponse(AbstractModel):
    """DescribeDatasourceConnection返回参数结构体

    """

    def __init__(self):
        r"""
        :param TotalCount: 数据连接总数
        :type TotalCount: int
        :param ConnectionSet: 数据连接对象集合
        :type ConnectionSet: list of DatasourceConnectionInfo
        :param RequestId: 唯一请求 ID，每次请求都会返回。定位问题时需要提供该次请求的 RequestId。
        :type RequestId: str
        """
        self.TotalCount = None
        self.ConnectionSet = None
        self.RequestId = None


    def _deserialize(self, params):
        self.TotalCount = params.get("TotalCount")
        if params.get("ConnectionSet") is not None:
            self.ConnectionSet = []
            for item in params.get("ConnectionSet"):
                obj = DatasourceConnectionInfo()
                obj._deserialize(item)
                self.ConnectionSet.append(obj)
        self.RequestId = params.get("RequestId")


class DescribeDefaultEngineConfigRequest(AbstractModel):
    """DescribeDefaultEngineConfig请求参数结构体

    """

    def __init__(self):
        r"""
        :param PayMode: 后付费0；预付费1
        :type PayMode: int
        """
        self.PayMode = None


    def _deserialize(self, params):
        self.PayMode = params.get("PayMode")
        memeber_set = set(params.keys())
        for name, value in vars(self).items():
            if name in memeber_set:
                memeber_set.remove(name)
        if len(memeber_set) > 0:
            warnings.warn("%s fileds are useless." % ",".join(memeber_set))
        


class DescribeDefaultEngineConfigResponse(AbstractModel):
    """DescribeDefaultEngineConfig返回参数结构体

    """

    def __init__(self):
        r"""
        :param DefaultEngineConfigs: 默认配置文件数组
        :type DefaultEngineConfigs: list of DefaultEngineConfig
        :param RequestId: 唯一请求 ID，每次请求都会返回。定位问题时需要提供该次请求的 RequestId。
        :type RequestId: str
        """
        self.DefaultEngineConfigs = None
        self.RequestId = None


    def _deserialize(self, params):
        if params.get("DefaultEngineConfigs") is not None:
            self.DefaultEngineConfigs = []
            for item in params.get("DefaultEngineConfigs"):
                obj = DefaultEngineConfig()
                obj._deserialize(item)
                self.DefaultEngineConfigs.append(obj)
        self.RequestId = params.get("RequestId")


class DescribeEngineUsageInfoRequest(AbstractModel):
    """DescribeEngineUsageInfo请求参数结构体

    """

    def __init__(self):
        r"""
        :param DataEngineId: 数据引擎ID
        :type DataEngineId: str
        """
        self.DataEngineId = None


    def _deserialize(self, params):
        self.DataEngineId = params.get("DataEngineId")
        memeber_set = set(params.keys())
        for name, value in vars(self).items():
            if name in memeber_set:
                memeber_set.remove(name)
        if len(memeber_set) > 0:
            warnings.warn("%s fileds are useless." % ",".join(memeber_set))
        


class DescribeEngineUsageInfoResponse(AbstractModel):
    """DescribeEngineUsageInfo返回参数结构体

    """

    def __init__(self):
        r"""
        :param Total: 集群总规格
        :type Total: int
        :param Used: 已占用集群规格
        :type Used: int
        :param Available: 剩余集群规格
        :type Available: int
        :param RequestId: 唯一请求 ID，每次请求都会返回。定位问题时需要提供该次请求的 RequestId。
        :type RequestId: str
        """
        self.Total = None
        self.Used = None
        self.Available = None
        self.RequestId = None


    def _deserialize(self, params):
        self.Total = params.get("Total")
        self.Used = params.get("Used")
        self.Available = params.get("Available")
        self.RequestId = params.get("RequestId")


class DescribeExportResultTasksRequest(AbstractModel):
    """DescribeExportResultTasks请求参数结构体

    """

    def __init__(self):
        r"""
        :param SessionId: SQL查询窗口Id
        :type SessionId: str
        :param Limit: 返回数量，默认为10，最大值为100。
        :type Limit: int
        :param Offset: 偏移量，默认为0。
        :type Offset: int
        :param SortBy: 排序字段，暂只支持create-time
        :type SortBy: str
        :param Sorting: 排序方式，desc表示正序，asc表示反序， 默认为asc。
        :type Sorting: str
        """
        self.SessionId = None
        self.Limit = None
        self.Offset = None
        self.SortBy = None
        self.Sorting = None


    def _deserialize(self, params):
        self.SessionId = params.get("SessionId")
        self.Limit = params.get("Limit")
        self.Offset = params.get("Offset")
        self.SortBy = params.get("SortBy")
        self.Sorting = params.get("Sorting")
        memeber_set = set(params.keys())
        for name, value in vars(self).items():
            if name in memeber_set:
                memeber_set.remove(name)
        if len(memeber_set) > 0:
            warnings.warn("%s fileds are useless." % ",".join(memeber_set))
        


class DescribeExportResultTasksResponse(AbstractModel):
    """DescribeExportResultTasks返回参数结构体

    """

    def __init__(self):
        r"""
        :param TaskList: 任务对象列表
        :type TaskList: list of ResultExportResponseInfo
        :param TotalCount: 任务总数
        :type TotalCount: int
        :param RequestId: 唯一请求 ID，每次请求都会返回。定位问题时需要提供该次请求的 RequestId。
        :type RequestId: str
        """
        self.TaskList = None
        self.TotalCount = None
        self.RequestId = None


    def _deserialize(self, params):
        if params.get("TaskList") is not None:
            self.TaskList = []
            for item in params.get("TaskList"):
                obj = ResultExportResponseInfo()
                obj._deserialize(item)
                self.TaskList.append(obj)
        self.TotalCount = params.get("TotalCount")
        self.RequestId = params.get("RequestId")


class DescribeFatherAndSonTaskInstancesRequest(AbstractModel):
    """DescribeFatherAndSonTaskInstances请求参数结构体

    """

    def __init__(self):
        r"""
        :param TaskId: 调度任务ID
        :type TaskId: str
        :param ScheduleTaskRunDate: 实例运行日期
        :type ScheduleTaskRunDate: str
        :param IsFather: 是否为父实例
        :type IsFather: bool
        :param Limit: 返回数量，默认为10，最大值为100。
        :type Limit: int
        :param Offset: 偏移量，默认为0。
        :type Offset: int
        """
        self.TaskId = None
        self.ScheduleTaskRunDate = None
        self.IsFather = None
        self.Limit = None
        self.Offset = None


    def _deserialize(self, params):
        self.TaskId = params.get("TaskId")
        self.ScheduleTaskRunDate = params.get("ScheduleTaskRunDate")
        self.IsFather = params.get("IsFather")
        self.Limit = params.get("Limit")
        self.Offset = params.get("Offset")
        memeber_set = set(params.keys())
        for name, value in vars(self).items():
            if name in memeber_set:
                memeber_set.remove(name)
        if len(memeber_set) > 0:
            warnings.warn("%s fileds are useless." % ",".join(memeber_set))
        


class DescribeFatherAndSonTaskInstancesResponse(AbstractModel):
    """DescribeFatherAndSonTaskInstances返回参数结构体

    """

    def __init__(self):
        r"""
        :param ScheduleTaskInstances: 父子实例列表
        :type ScheduleTaskInstances: list of ScheduleInstanceInfo
        :param TotalElements: 父子实例总数
        :type TotalElements: int
        :param RequestId: 唯一请求 ID，每次请求都会返回。定位问题时需要提供该次请求的 RequestId。
        :type RequestId: str
        """
        self.ScheduleTaskInstances = None
        self.TotalElements = None
        self.RequestId = None


    def _deserialize(self, params):
        if params.get("ScheduleTaskInstances") is not None:
            self.ScheduleTaskInstances = []
            for item in params.get("ScheduleTaskInstances"):
                obj = ScheduleInstanceInfo()
                obj._deserialize(item)
                self.ScheduleTaskInstances.append(obj)
        self.TotalElements = params.get("TotalElements")
        self.RequestId = params.get("RequestId")


class DescribeFatherAndSonTasksRequest(AbstractModel):
    """DescribeFatherAndSonTasks请求参数结构体

    """

    def __init__(self):
        r"""
        :param TaskId: 调度任务ID
        :type TaskId: str
        :param IsFather: 是否父任务
        :type IsFather: bool
        :param ScheduleTaskStatusList: 任务状态列表
        :type ScheduleTaskStatusList: list of str
        :param Limit: 返回数量，默认为10，最大值为100。
        :type Limit: int
        :param Offset: 偏移量，默认为0。
        :type Offset: int
        """
        self.TaskId = None
        self.IsFather = None
        self.ScheduleTaskStatusList = None
        self.Limit = None
        self.Offset = None


    def _deserialize(self, params):
        self.TaskId = params.get("TaskId")
        self.IsFather = params.get("IsFather")
        self.ScheduleTaskStatusList = params.get("ScheduleTaskStatusList")
        self.Limit = params.get("Limit")
        self.Offset = params.get("Offset")
        memeber_set = set(params.keys())
        for name, value in vars(self).items():
            if name in memeber_set:
                memeber_set.remove(name)
        if len(memeber_set) > 0:
            warnings.warn("%s fileds are useless." % ",".join(memeber_set))
        


class DescribeFatherAndSonTasksResponse(AbstractModel):
    """DescribeFatherAndSonTasks返回参数结构体

    """

    def __init__(self):
        r"""
        :param ScheduleTasks: 调度任务列表
        :type ScheduleTasks: list of ScheduleTaskInfo
        :param TotalElements: 调度任务总数
        :type TotalElements: int
        :param RequestId: 唯一请求 ID，每次请求都会返回。定位问题时需要提供该次请求的 RequestId。
        :type RequestId: str
        """
        self.ScheduleTasks = None
        self.TotalElements = None
        self.RequestId = None


    def _deserialize(self, params):
        if params.get("ScheduleTasks") is not None:
            self.ScheduleTasks = []
            for item in params.get("ScheduleTasks"):
                obj = ScheduleTaskInfo()
                obj._deserialize(item)
                self.ScheduleTasks.append(obj)
        self.TotalElements = params.get("TotalElements")
        self.RequestId = params.get("RequestId")


class DescribeForbiddenTableProRequest(AbstractModel):
    """DescribeForbiddenTablePro请求参数结构体

    """


class DescribeForbiddenTableProResponse(AbstractModel):
    """DescribeForbiddenTablePro返回参数结构体

    """

    def __init__(self):
        r"""
        :param ForbiddenTableProperties: 被禁用的表属性列表，该列表的属性不可进行增删改操作
        :type ForbiddenTableProperties: list of str
        :param RequestId: 唯一请求 ID，每次请求都会返回。定位问题时需要提供该次请求的 RequestId。
        :type RequestId: str
        """
        self.ForbiddenTableProperties = None
        self.RequestId = None


    def _deserialize(self, params):
        self.ForbiddenTableProperties = params.get("ForbiddenTableProperties")
        self.RequestId = params.get("RequestId")


class DescribeForbiddenTablePropertiesRequest(AbstractModel):
    """DescribeForbiddenTableProperties请求参数结构体

    """


class DescribeForbiddenTablePropertiesResponse(AbstractModel):
    """DescribeForbiddenTableProperties返回参数结构体

    """

    def __init__(self):
        r"""
        :param ForbiddenTableProperties: 被禁用的表属性列表，该列表的属性不可进行增删改操作
        :type ForbiddenTableProperties: list of str
        :param RequestId: 唯一请求 ID，每次请求都会返回。定位问题时需要提供该次请求的 RequestId。
        :type RequestId: str
        """
        self.ForbiddenTableProperties = None
        self.RequestId = None


    def _deserialize(self, params):
        self.ForbiddenTableProperties = params.get("ForbiddenTableProperties")
        self.RequestId = params.get("RequestId")


class DescribeFunctionsRequest(AbstractModel):
    """DescribeFunctions请求参数结构体

    """

    def __init__(self):
        r"""
        :param DatabaseName: 数据库名称
        :type DatabaseName: str
        :param DatasourceConnectionName: 数据目录名称
        :type DatasourceConnectionName: str
        :param Limit: 展示条数
        :type Limit: int
        :param Offset: 偏移量
        :type Offset: int
        """
        self.DatabaseName = None
        self.DatasourceConnectionName = None
        self.Limit = None
        self.Offset = None


    def _deserialize(self, params):
        self.DatabaseName = params.get("DatabaseName")
        self.DatasourceConnectionName = params.get("DatasourceConnectionName")
        self.Limit = params.get("Limit")
        self.Offset = params.get("Offset")
        memeber_set = set(params.keys())
        for name, value in vars(self).items():
            if name in memeber_set:
                memeber_set.remove(name)
        if len(memeber_set) > 0:
            warnings.warn("%s fileds are useless." % ",".join(memeber_set))
        


class DescribeFunctionsResponse(AbstractModel):
    """DescribeFunctions返回参数结构体

    """

    def __init__(self):
        r"""
        :param TotalCount: 列表总数
注意：此字段可能返回 null，表示取不到有效值。
        :type TotalCount: int
        :param Rows: UDF数据
注意：此字段可能返回 null，表示取不到有效值。
        :type Rows: list of FunctionSimpleData
        :param RequestId: 唯一请求 ID，每次请求都会返回。定位问题时需要提供该次请求的 RequestId。
        :type RequestId: str
        """
        self.TotalCount = None
        self.Rows = None
        self.RequestId = None


    def _deserialize(self, params):
        self.TotalCount = params.get("TotalCount")
        if params.get("Rows") is not None:
            self.Rows = []
            for item in params.get("Rows"):
                obj = FunctionSimpleData()
                obj._deserialize(item)
                self.Rows.append(obj)
        self.RequestId = params.get("RequestId")


class DescribeGovernDefaultPolicyRequest(AbstractModel):
    """DescribeGovernDefaultPolicy请求参数结构体

    """


class DescribeGovernDefaultPolicyResponse(AbstractModel):
    """DescribeGovernDefaultPolicy返回参数结构体

    """

    def __init__(self):
        r"""
        :param Threshold: 数据值里规则默认值
        :type Threshold: :class:`tencentcloud.dlc.v20210125.models.DataGovernPolicy`
        :param RequestId: 唯一请求 ID，每次请求都会返回。定位问题时需要提供该次请求的 RequestId。
        :type RequestId: str
        """
        self.Threshold = None
        self.RequestId = None


    def _deserialize(self, params):
        if params.get("Threshold") is not None:
            self.Threshold = DataGovernPolicy()
            self.Threshold._deserialize(params.get("Threshold"))
        self.RequestId = params.get("RequestId")


class DescribeGovernEventRuleRequest(AbstractModel):
    """DescribeGovernEventRule请求参数结构体

    """

    def __init__(self):
        r"""
        :param Name: 数据治理事件阈值名称
        :type Name: str
        """
        self.Name = None


    def _deserialize(self, params):
        self.Name = params.get("Name")
        memeber_set = set(params.keys())
        for name, value in vars(self).items():
            if name in memeber_set:
                memeber_set.remove(name)
        if len(memeber_set) > 0:
            warnings.warn("%s fileds are useless." % ",".join(memeber_set))
        


class DescribeGovernEventRuleResponse(AbstractModel):
    """DescribeGovernEventRule返回参数结构体

    """

    def __init__(self):
        r"""
        :param RuleThreshold: 用户的数据治理事件阈值
        :type RuleThreshold: :class:`tencentcloud.dlc.v20210125.models.TenantGovernEventRules`
        :param RequestId: 唯一请求 ID，每次请求都会返回。定位问题时需要提供该次请求的 RequestId。
        :type RequestId: str
        """
        self.RuleThreshold = None
        self.RequestId = None


    def _deserialize(self, params):
        if params.get("RuleThreshold") is not None:
            self.RuleThreshold = TenantGovernEventRules()
            self.RuleThreshold._deserialize(params.get("RuleThreshold"))
        self.RequestId = params.get("RequestId")


class DescribeGovernMetaInfoRequest(AbstractModel):
    """DescribeGovernMetaInfo请求参数结构体

    """

    def __init__(self):
        r"""
        :param Catalog: 数据目录名称
        :type Catalog: str
        :param Database: 数据库名称
        :type Database: str
        :param Table: 数据表名称
        :type Table: str
        """
        self.Catalog = None
        self.Database = None
        self.Table = None


    def _deserialize(self, params):
        self.Catalog = params.get("Catalog")
        self.Database = params.get("Database")
        self.Table = params.get("Table")
        memeber_set = set(params.keys())
        for name, value in vars(self).items():
            if name in memeber_set:
                memeber_set.remove(name)
        if len(memeber_set) > 0:
            warnings.warn("%s fileds are useless." % ",".join(memeber_set))
        


class DescribeGovernMetaInfoResponse(AbstractModel):
    """DescribeGovernMetaInfo返回参数结构体

    """

    def __init__(self):
        r"""
        :param GovernMeta: 数据治理元信息
        :type GovernMeta: :class:`tencentcloud.dlc.v20210125.models.GovernMetaInfo`
        :param RequestId: 唯一请求 ID，每次请求都会返回。定位问题时需要提供该次请求的 RequestId。
        :type RequestId: str
        """
        self.GovernMeta = None
        self.RequestId = None


    def _deserialize(self, params):
        if params.get("GovernMeta") is not None:
            self.GovernMeta = GovernMetaInfo()
            self.GovernMeta._deserialize(params.get("GovernMeta"))
        self.RequestId = params.get("RequestId")


class DescribeHouseEventsRequest(AbstractModel):
    """DescribeHouseEvents请求参数结构体

    """

    def __init__(self):
        r"""
        :param HouseName: 虚拟集群名称
        :type HouseName: str
        :param Limit: 返回数量，默认为10，最大为100
        :type Limit: int
        :param Offset: 偏移量，默认为0
        :type Offset: int
        """
        self.HouseName = None
        self.Limit = None
        self.Offset = None


    def _deserialize(self, params):
        self.HouseName = params.get("HouseName")
        self.Limit = params.get("Limit")
        self.Offset = params.get("Offset")
        memeber_set = set(params.keys())
        for name, value in vars(self).items():
            if name in memeber_set:
                memeber_set.remove(name)
        if len(memeber_set) > 0:
            warnings.warn("%s fileds are useless." % ",".join(memeber_set))
        


class DescribeHouseEventsResponse(AbstractModel):
    """DescribeHouseEvents返回参数结构体

    """

    def __init__(self):
        r"""
        :param Events: 事件详细信息
注意：此字段可能返回 null，表示取不到有效值。
        :type Events: list of HouseEventsInfo
        :param Page: 分页号
注意：此字段可能返回 null，表示取不到有效值。
        :type Page: int
        :param Size: 分页大小
注意：此字段可能返回 null，表示取不到有效值。
        :type Size: int
        :param TotalPages: 总页数
注意：此字段可能返回 null，表示取不到有效值。
        :type TotalPages: int
        :param RequestId: 唯一请求 ID，每次请求都会返回。定位问题时需要提供该次请求的 RequestId。
        :type RequestId: str
        """
        self.Events = None
        self.Page = None
        self.Size = None
        self.TotalPages = None
        self.RequestId = None


    def _deserialize(self, params):
        if params.get("Events") is not None:
            self.Events = []
            for item in params.get("Events"):
                obj = HouseEventsInfo()
                obj._deserialize(item)
                self.Events.append(obj)
        self.Page = params.get("Page")
        self.Size = params.get("Size")
        self.TotalPages = params.get("TotalPages")
        self.RequestId = params.get("RequestId")


class DescribeInstanceLogListRequest(AbstractModel):
    """DescribeInstanceLogList请求参数结构体

    """

    def __init__(self):
        r"""
        :param TaskId: 调度任务ID
        :type TaskId: str
        :param RunDate: 调度任务数据日期
        :type RunDate: str
        """
        self.TaskId = None
        self.RunDate = None


    def _deserialize(self, params):
        self.TaskId = params.get("TaskId")
        self.RunDate = params.get("RunDate")
        memeber_set = set(params.keys())
        for name, value in vars(self).items():
            if name in memeber_set:
                memeber_set.remove(name)
        if len(memeber_set) > 0:
            warnings.warn("%s fileds are useless." % ",".join(memeber_set))
        


class DescribeInstanceLogListResponse(AbstractModel):
    """DescribeInstanceLogList返回参数结构体

    """

    def __init__(self):
        r"""
        :param ScheduleInstanceLogList: 调度任务实例日志列表
        :type ScheduleInstanceLogList: list of ScheduleInstanceLog
        :param RequestId: 唯一请求 ID，每次请求都会返回。定位问题时需要提供该次请求的 RequestId。
        :type RequestId: str
        """
        self.ScheduleInstanceLogList = None
        self.RequestId = None


    def _deserialize(self, params):
        if params.get("ScheduleInstanceLogList") is not None:
            self.ScheduleInstanceLogList = []
            for item in params.get("ScheduleInstanceLogList"):
                obj = ScheduleInstanceLog()
                obj._deserialize(item)
                self.ScheduleInstanceLogList.append(obj)
        self.RequestId = params.get("RequestId")


class DescribeLakeFsAccessRequest(AbstractModel):
    """DescribeLakeFsAccess请求参数结构体

    """

    def __init__(self):
        r"""
        :param FsPath: 文件路径
        :type FsPath: str
        :param AvailablePeriod: 有效期
        :type AvailablePeriod: int
        :param Identity: 访问身份信息
        :type Identity: str
        """
        self.FsPath = None
        self.AvailablePeriod = None
        self.Identity = None


    def _deserialize(self, params):
        self.FsPath = params.get("FsPath")
        self.AvailablePeriod = params.get("AvailablePeriod")
        self.Identity = params.get("Identity")
        memeber_set = set(params.keys())
        for name, value in vars(self).items():
            if name in memeber_set:
                memeber_set.remove(name)
        if len(memeber_set) > 0:
            warnings.warn("%s fileds are useless." % ",".join(memeber_set))
        


class DescribeLakeFsAccessResponse(AbstractModel):
    """DescribeLakeFsAccess返回参数结构体

    """

    def __init__(self):
        r"""
        :param AccessToken: 临时访问秘钥
        :type AccessToken: :class:`tencentcloud.dlc.v20210125.models.LakeFileSystemToken`
        :param RequestId: 唯一请求 ID，每次请求都会返回。定位问题时需要提供该次请求的 RequestId。
        :type RequestId: str
        """
        self.AccessToken = None
        self.RequestId = None


    def _deserialize(self, params):
        if params.get("AccessToken") is not None:
            self.AccessToken = LakeFileSystemToken()
            self.AccessToken._deserialize(params.get("AccessToken"))
        self.RequestId = params.get("RequestId")


class DescribeLakeFsChdfsBindingsRequest(AbstractModel):
    """DescribeLakeFsChdfsBindings请求参数结构体

    """


class DescribeLakeFsChdfsBindingsResponse(AbstractModel):
    """DescribeLakeFsChdfsBindings返回参数结构体

    """

    def __init__(self):
        r"""
        :param ChdfsBindings: 绑定关系列表
        :type ChdfsBindings: :class:`tencentcloud.dlc.v20210125.models.MountPointAssociateInfo`
        :param Total: 绑定关系个数
        :type Total: int
        :param RequestId: 唯一请求 ID，每次请求都会返回。定位问题时需要提供该次请求的 RequestId。
        :type RequestId: str
        """
        self.ChdfsBindings = None
        self.Total = None
        self.RequestId = None


    def _deserialize(self, params):
        if params.get("ChdfsBindings") is not None:
            self.ChdfsBindings = MountPointAssociateInfo()
            self.ChdfsBindings._deserialize(params.get("ChdfsBindings"))
        self.Total = params.get("Total")
        self.RequestId = params.get("RequestId")


class DescribeLakeFsChdfsNamesRequest(AbstractModel):
    """DescribeLakeFsChdfsNames请求参数结构体

    """


class DescribeLakeFsChdfsNamesResponse(AbstractModel):
    """DescribeLakeFsChdfsNames返回参数结构体

    """

    def __init__(self):
        r"""
        :param Names: 查询到的名称列表
        :type Names: list of str
        :param Total: 名称个数
        :type Total: int
        :param RequestId: 唯一请求 ID，每次请求都会返回。定位问题时需要提供该次请求的 RequestId。
        :type RequestId: str
        """
        self.Names = None
        self.Total = None
        self.RequestId = None


    def _deserialize(self, params):
        self.Names = params.get("Names")
        self.Total = params.get("Total")
        self.RequestId = params.get("RequestId")


class DescribeLakeFsDirSummaryRequest(AbstractModel):
    """DescribeLakeFsDirSummary请求参数结构体

    """

    def __init__(self):
        r"""
        :param Name: 托管存储名称
        :type Name: str
        :param Path: 目录全路径
        :type Path: str
        """
        self.Name = None
        self.Path = None


    def _deserialize(self, params):
        self.Name = params.get("Name")
        self.Path = params.get("Path")
        memeber_set = set(params.keys())
        for name, value in vars(self).items():
            if name in memeber_set:
                memeber_set.remove(name)
        if len(memeber_set) > 0:
            warnings.warn("%s fileds are useless." % ",".join(memeber_set))
        


class DescribeLakeFsDirSummaryResponse(AbstractModel):
    """DescribeLakeFsDirSummary返回参数结构体

    """

    def __init__(self):
        r"""
        :param Summary: Summary统计信息
        :type Summary: :class:`tencentcloud.dlc.v20210125.models.LakeFsSummary`
        :param RequestId: 唯一请求 ID，每次请求都会返回。定位问题时需要提供该次请求的 RequestId。
        :type RequestId: str
        """
        self.Summary = None
        self.RequestId = None


    def _deserialize(self, params):
        if params.get("Summary") is not None:
            self.Summary = LakeFsSummary()
            self.Summary._deserialize(params.get("Summary"))
        self.RequestId = params.get("RequestId")


class DescribeLakeFsInfoRequest(AbstractModel):
    """DescribeLakeFsInfo请求参数结构体

    """


class DescribeLakeFsInfoResponse(AbstractModel):
    """DescribeLakeFsInfo返回参数结构体

    """

    def __init__(self):
        r"""
        :param LakeFsInfos: 托管存储信息
注意：此字段可能返回 null，表示取不到有效值。
        :type LakeFsInfos: list of LakeFsInfo
        :param RequestId: 唯一请求 ID，每次请求都会返回。定位问题时需要提供该次请求的 RequestId。
        :type RequestId: str
        """
        self.LakeFsInfos = None
        self.RequestId = None


    def _deserialize(self, params):
        if params.get("LakeFsInfos") is not None:
            self.LakeFsInfos = []
            for item in params.get("LakeFsInfos"):
                obj = LakeFsInfo()
                obj._deserialize(item)
                self.LakeFsInfos.append(obj)
        self.RequestId = params.get("RequestId")


class DescribeLakeFsPathRequest(AbstractModel):
    """DescribeLakeFsPath请求参数结构体

    """

    def __init__(self):
        r"""
        :param FsPath: 需要fagnwen
        :type FsPath: str
        """
        self.FsPath = None


    def _deserialize(self, params):
        self.FsPath = params.get("FsPath")
        memeber_set = set(params.keys())
        for name, value in vars(self).items():
            if name in memeber_set:
                memeber_set.remove(name)
        if len(memeber_set) > 0:
            warnings.warn("%s fileds are useless." % ",".join(memeber_set))
        


class DescribeLakeFsPathResponse(AbstractModel):
    """DescribeLakeFsPath返回参数结构体

    """

    def __init__(self):
        r"""
        :param AccessToken: 路径的访问实例
        :type AccessToken: :class:`tencentcloud.dlc.v20210125.models.LakeFileSystemToken`
        :param RequestId: 唯一请求 ID，每次请求都会返回。定位问题时需要提供该次请求的 RequestId。
        :type RequestId: str
        """
        self.AccessToken = None
        self.RequestId = None


    def _deserialize(self, params):
        if params.get("AccessToken") is not None:
            self.AccessToken = LakeFileSystemToken()
            self.AccessToken._deserialize(params.get("AccessToken"))
        self.RequestId = params.get("RequestId")


class DescribeLakeFsWarehouseAccessRequest(AbstractModel):
    """DescribeLakeFsWarehouseAccess请求参数结构体

    """

    def __init__(self):
        r"""
        :param Name: 托管存储名称
        :type Name: str
        :param Mode: 访问模式
        :type Mode: int
        """
        self.Name = None
        self.Mode = None


    def _deserialize(self, params):
        self.Name = params.get("Name")
        self.Mode = params.get("Mode")
        memeber_set = set(params.keys())
        for name, value in vars(self).items():
            if name in memeber_set:
                memeber_set.remove(name)
        if len(memeber_set) > 0:
            warnings.warn("%s fileds are useless." % ",".join(memeber_set))
        


class DescribeLakeFsWarehouseAccessResponse(AbstractModel):
    """DescribeLakeFsWarehouseAccess返回参数结构体

    """

    def __init__(self):
        r"""
        :param AccessToken: 访问token
注意：此字段可能返回 null，表示取不到有效值。
        :type AccessToken: :class:`tencentcloud.dlc.v20210125.models.LakeFileSystemToken`
        :param RequestId: 唯一请求 ID，每次请求都会返回。定位问题时需要提供该次请求的 RequestId。
        :type RequestId: str
        """
        self.AccessToken = None
        self.RequestId = None


    def _deserialize(self, params):
        if params.get("AccessToken") is not None:
            self.AccessToken = LakeFileSystemToken()
            self.AccessToken._deserialize(params.get("AccessToken"))
        self.RequestId = params.get("RequestId")


class DescribeMainDataDataEngineRequest(AbstractModel):
    """DescribeMainDataDataEngine请求参数结构体

    """


class DescribeMainDataDataEngineResponse(AbstractModel):
    """DescribeMainDataDataEngine返回参数结构体

    """

    def __init__(self):
        r"""
        :param Data: 统计详情
        :type Data: list of MainDataDataEngineStat
        :param RequestId: 唯一请求 ID，每次请求都会返回。定位问题时需要提供该次请求的 RequestId。
        :type RequestId: str
        """
        self.Data = None
        self.RequestId = None


    def _deserialize(self, params):
        if params.get("Data") is not None:
            self.Data = []
            for item in params.get("Data"):
                obj = MainDataDataEngineStat()
                obj._deserialize(item)
                self.Data.append(obj)
        self.RequestId = params.get("RequestId")


class DescribeMainDataOverviewLineRequest(AbstractModel):
    """DescribeMainDataOverviewLine请求参数结构体

    """


class DescribeMainDataOverviewLineResponse(AbstractModel):
    """DescribeMainDataOverviewLine返回参数结构体

    """

    def __init__(self):
        r"""
        :param MainViewLine: 首页CU时用量折线图
注意：此字段可能返回 null，表示取不到有效值。
        :type MainViewLine: list of MainViewLine
        :param RequestId: 唯一请求 ID，每次请求都会返回。定位问题时需要提供该次请求的 RequestId。
        :type RequestId: str
        """
        self.MainViewLine = None
        self.RequestId = None


    def _deserialize(self, params):
        if params.get("MainViewLine") is not None:
            self.MainViewLine = []
            for item in params.get("MainViewLine"):
                obj = MainViewLine()
                obj._deserialize(item)
                self.MainViewLine.append(obj)
        self.RequestId = params.get("RequestId")


class DescribeMainDataOverviewRequest(AbstractModel):
    """DescribeMainDataOverview请求参数结构体

    """


class DescribeMainDataOverviewResponse(AbstractModel):
    """DescribeMainDataOverview返回参数结构体

    """

    def __init__(self):
        r"""
        :param MainViewData: 首页数据概览
注意：此字段可能返回 null，表示取不到有效值。
        :type MainViewData: :class:`tencentcloud.dlc.v20210125.models.MainViewData`
        :param RequestId: 唯一请求 ID，每次请求都会返回。定位问题时需要提供该次请求的 RequestId。
        :type RequestId: str
        """
        self.MainViewData = None
        self.RequestId = None


    def _deserialize(self, params):
        if params.get("MainViewData") is not None:
            self.MainViewData = MainViewData()
            self.MainViewData._deserialize(params.get("MainViewData"))
        self.RequestId = params.get("RequestId")


class DescribeMainDataPrivateEngineLineRequest(AbstractModel):
    """DescribeMainDataPrivateEngineLine请求参数结构体

    """


class DescribeMainDataPrivateEngineLineResponse(AbstractModel):
    """DescribeMainDataPrivateEngineLine返回参数结构体

    """

    def __init__(self):
        r"""
        :param TopData: 首页CU用量top2数据
注意：此字段可能返回 null，表示取不到有效值。
        :type TopData: :class:`tencentcloud.dlc.v20210125.models.TopPrivateEngineData`
        :param RequestId: 唯一请求 ID，每次请求都会返回。定位问题时需要提供该次请求的 RequestId。
        :type RequestId: str
        """
        self.TopData = None
        self.RequestId = None


    def _deserialize(self, params):
        if params.get("TopData") is not None:
            self.TopData = TopPrivateEngineData()
            self.TopData._deserialize(params.get("TopData"))
        self.RequestId = params.get("RequestId")


class DescribeMainDataShareEngineLineRequest(AbstractModel):
    """DescribeMainDataShareEngineLine请求参数结构体

    """


class DescribeMainDataShareEngineLineResponse(AbstractModel):
    """DescribeMainDataShareEngineLine返回参数结构体

    """

    def __init__(self):
        r"""
        :param MainShareLine: 首页共享引擎折线图
注意：此字段可能返回 null，表示取不到有效值。
        :type MainShareLine: list of MainShareLine
        :param RequestId: 唯一请求 ID，每次请求都会返回。定位问题时需要提供该次请求的 RequestId。
        :type RequestId: str
        """
        self.MainShareLine = None
        self.RequestId = None


    def _deserialize(self, params):
        if params.get("MainShareLine") is not None:
            self.MainShareLine = []
            for item in params.get("MainShareLine"):
                obj = MainShareLine()
                obj._deserialize(item)
                self.MainShareLine.append(obj)
        self.RequestId = params.get("RequestId")


class DescribeMainDataTaskLineRequest(AbstractModel):
    """DescribeMainDataTaskLine请求参数结构体

    """

    def __init__(self):
        r"""
        :param DayStart: 开始时间，秒级时间戳
        :type DayStart: int
        :param DayEnd: 结束时间，秒级时间戳
        :type DayEnd: int
        """
        self.DayStart = None
        self.DayEnd = None


    def _deserialize(self, params):
        self.DayStart = params.get("DayStart")
        self.DayEnd = params.get("DayEnd")
        memeber_set = set(params.keys())
        for name, value in vars(self).items():
            if name in memeber_set:
                memeber_set.remove(name)
        if len(memeber_set) > 0:
            warnings.warn("%s fileds are useless." % ",".join(memeber_set))
        


class DescribeMainDataTaskLineResponse(AbstractModel):
    """DescribeMainDataTaskLine返回参数结构体

    """

    def __init__(self):
        r"""
        :param TaskData: 首页任务监控-折线图
注意：此字段可能返回 null，表示取不到有效值。
        :type TaskData: :class:`tencentcloud.dlc.v20210125.models.MainTaskData`
        :param RequestId: 唯一请求 ID，每次请求都会返回。定位问题时需要提供该次请求的 RequestId。
        :type RequestId: str
        """
        self.TaskData = None
        self.RequestId = None


    def _deserialize(self, params):
        if params.get("TaskData") is not None:
            self.TaskData = MainTaskData()
            self.TaskData._deserialize(params.get("TaskData"))
        self.RequestId = params.get("RequestId")


class DescribeMetaDatabaseRequest(AbstractModel):
    """DescribeMetaDatabase请求参数结构体

    """

    def __init__(self):
        r"""
        :param DatabaseName: 数据库名称
        :type DatabaseName: str
        :param DatasourceConnectionName: 数据连接名称，不填默认为DataLakeCatalog
        :type DatasourceConnectionName: str
        """
        self.DatabaseName = None
        self.DatasourceConnectionName = None


    def _deserialize(self, params):
        self.DatabaseName = params.get("DatabaseName")
        self.DatasourceConnectionName = params.get("DatasourceConnectionName")
        memeber_set = set(params.keys())
        for name, value in vars(self).items():
            if name in memeber_set:
                memeber_set.remove(name)
        if len(memeber_set) > 0:
            warnings.warn("%s fileds are useless." % ",".join(memeber_set))
        


class DescribeMetaDatabaseResponse(AbstractModel):
    """DescribeMetaDatabase返回参数结构体

    """

    def __init__(self):
        r"""
        :param DatabaseInfo: 数据库信息
        :type DatabaseInfo: :class:`tencentcloud.dlc.v20210125.models.DatabaseResponseInfo`
        :param RequestId: 唯一请求 ID，每次请求都会返回。定位问题时需要提供该次请求的 RequestId。
        :type RequestId: str
        """
        self.DatabaseInfo = None
        self.RequestId = None


    def _deserialize(self, params):
        if params.get("DatabaseInfo") is not None:
            self.DatabaseInfo = DatabaseResponseInfo()
            self.DatabaseInfo._deserialize(params.get("DatabaseInfo"))
        self.RequestId = params.get("RequestId")


class DescribeMetaDatabasesRequest(AbstractModel):
    """DescribeMetaDatabases请求参数结构体

    """

    def __init__(self):
        r"""
        :param Limit: 返回数量，默认为10，最大值为100。
        :type Limit: int
        :param Offset: 数据偏移量，从0开始，默认为0。
        :type Offset: int
        :param KeyWord: 模糊匹配，库名关键字。
        :type KeyWord: str
        :param DatasourceConnectionName: 数据源名称，默认DataLakeCatalog
        :type DatasourceConnectionName: str
        :param Sort: 排序字段：CreateTime、Name（不传则默认按name升序）
        :type Sort: str
        :param Asc: 排序类型：false：降序（默认）、true：升序
        :type Asc: bool
        """
        self.Limit = None
        self.Offset = None
        self.KeyWord = None
        self.DatasourceConnectionName = None
        self.Sort = None
        self.Asc = None


    def _deserialize(self, params):
        self.Limit = params.get("Limit")
        self.Offset = params.get("Offset")
        self.KeyWord = params.get("KeyWord")
        self.DatasourceConnectionName = params.get("DatasourceConnectionName")
        self.Sort = params.get("Sort")
        self.Asc = params.get("Asc")
        memeber_set = set(params.keys())
        for name, value in vars(self).items():
            if name in memeber_set:
                memeber_set.remove(name)
        if len(memeber_set) > 0:
            warnings.warn("%s fileds are useless." % ",".join(memeber_set))
        


class DescribeMetaDatabasesResponse(AbstractModel):
    """DescribeMetaDatabases返回参数结构体

    """

    def __init__(self):
        r"""
        :param DatabaseList: 数据库对象列表。
        :type DatabaseList: list of DatabaseResponseInfo
        :param TotalCount: 实例总数。
        :type TotalCount: int
        :param RequestId: 唯一请求 ID，每次请求都会返回。定位问题时需要提供该次请求的 RequestId。
        :type RequestId: str
        """
        self.DatabaseList = None
        self.TotalCount = None
        self.RequestId = None


    def _deserialize(self, params):
        if params.get("DatabaseList") is not None:
            self.DatabaseList = []
            for item in params.get("DatabaseList"):
                obj = DatabaseResponseInfo()
                obj._deserialize(item)
                self.DatabaseList.append(obj)
        self.TotalCount = params.get("TotalCount")
        self.RequestId = params.get("RequestId")


class DescribeMetaKeyConstraintRequest(AbstractModel):
    """DescribeMetaKeyConstraint请求参数结构体

    """

    def __init__(self):
        r"""
        :param DatabaseName: 数据库名称
        :type DatabaseName: str
        :param TableName: 表名称
        :type TableName: str
        :param ConstraintName: 约束名称
        :type ConstraintName: str
        """
        self.DatabaseName = None
        self.TableName = None
        self.ConstraintName = None


    def _deserialize(self, params):
        self.DatabaseName = params.get("DatabaseName")
        self.TableName = params.get("TableName")
        self.ConstraintName = params.get("ConstraintName")
        memeber_set = set(params.keys())
        for name, value in vars(self).items():
            if name in memeber_set:
                memeber_set.remove(name)
        if len(memeber_set) > 0:
            warnings.warn("%s fileds are useless." % ",".join(memeber_set))
        


class DescribeMetaKeyConstraintResponse(AbstractModel):
    """DescribeMetaKeyConstraint返回参数结构体

    """

    def __init__(self):
        r"""
        :param MetaKeyConstraints: 约束列表
        :type MetaKeyConstraints: list of MetaKeyConstraint
        :param RequestId: 唯一请求 ID，每次请求都会返回。定位问题时需要提供该次请求的 RequestId。
        :type RequestId: str
        """
        self.MetaKeyConstraints = None
        self.RequestId = None


    def _deserialize(self, params):
        if params.get("MetaKeyConstraints") is not None:
            self.MetaKeyConstraints = []
            for item in params.get("MetaKeyConstraints"):
                obj = MetaKeyConstraint()
                obj._deserialize(item)
                self.MetaKeyConstraints.append(obj)
        self.RequestId = params.get("RequestId")


class DescribeMetaTableInternalRequest(AbstractModel):
    """DescribeMetaTableInternal请求参数结构体

    """

    def __init__(self):
        r"""
        :param TableName: 查询对象表名称
        :type TableName: str
        :param DatabaseName: 查询表所在的数据库名称。
        :type DatabaseName: str
        :param DatasourceConnectionName: 查询表所在的数据源名称
        :type DatasourceConnectionName: str
        :param GetLocation: 开放托管存储表location获取限制（默认传false，不开启，true：开启）
        :type GetLocation: bool
        """
        self.TableName = None
        self.DatabaseName = None
        self.DatasourceConnectionName = None
        self.GetLocation = None


    def _deserialize(self, params):
        self.TableName = params.get("TableName")
        self.DatabaseName = params.get("DatabaseName")
        self.DatasourceConnectionName = params.get("DatasourceConnectionName")
        self.GetLocation = params.get("GetLocation")
        memeber_set = set(params.keys())
        for name, value in vars(self).items():
            if name in memeber_set:
                memeber_set.remove(name)
        if len(memeber_set) > 0:
            warnings.warn("%s fileds are useless." % ",".join(memeber_set))
        


class DescribeMetaTableInternalResponse(AbstractModel):
    """DescribeMetaTableInternal返回参数结构体

    """

    def __init__(self):
        r"""
        :param Table: 数据表对象
        :type Table: :class:`tencentcloud.dlc.v20210125.models.TableResponseInfo`
        :param RequestId: 唯一请求 ID，每次请求都会返回。定位问题时需要提供该次请求的 RequestId。
        :type RequestId: str
        """
        self.Table = None
        self.RequestId = None


    def _deserialize(self, params):
        if params.get("Table") is not None:
            self.Table = TableResponseInfo()
            self.Table._deserialize(params.get("Table"))
        self.RequestId = params.get("RequestId")


class DescribeMetaTableRequest(AbstractModel):
    """DescribeMetaTable请求参数结构体

    """

    def __init__(self):
        r"""
        :param TableName: 查询对象表名称
        :type TableName: str
        :param DatabaseName: 查询表所在的数据库名称。
        :type DatabaseName: str
        :param DatasourceConnectionName: 查询表所在的数据源名称
        :type DatasourceConnectionName: str
        """
        self.TableName = None
        self.DatabaseName = None
        self.DatasourceConnectionName = None


    def _deserialize(self, params):
        self.TableName = params.get("TableName")
        self.DatabaseName = params.get("DatabaseName")
        self.DatasourceConnectionName = params.get("DatasourceConnectionName")
        memeber_set = set(params.keys())
        for name, value in vars(self).items():
            if name in memeber_set:
                memeber_set.remove(name)
        if len(memeber_set) > 0:
            warnings.warn("%s fileds are useless." % ",".join(memeber_set))
        


class DescribeMetaTableResponse(AbstractModel):
    """DescribeMetaTable返回参数结构体

    """

    def __init__(self):
        r"""
        :param Table: 数据表对象
        :type Table: :class:`tencentcloud.dlc.v20210125.models.TableResponseInfo`
        :param RequestId: 唯一请求 ID，每次请求都会返回。定位问题时需要提供该次请求的 RequestId。
        :type RequestId: str
        """
        self.Table = None
        self.RequestId = None


    def _deserialize(self, params):
        if params.get("Table") is not None:
            self.Table = TableResponseInfo()
            self.Table._deserialize(params.get("Table"))
        self.RequestId = params.get("RequestId")


class DescribeMetaTablesRequest(AbstractModel):
    """DescribeMetaTables请求参数结构体

    """

    def __init__(self):
        r"""
        :param Limit: 返回数量，默认为10，最大值为100。
        :type Limit: int
        :param Offset: 数据偏移量，从0开始，默认为0。
        :type Offset: int
        :param DatabaseName: 列出该数据库下所属数据表。
        :type DatabaseName: str
        :param Filters: 过滤条件，如下支持的过滤类型，传参Name应为其一
table-name - String - （过滤条件）数据表名称,形如：table-001。
table-id - String - （过滤条件）table id形如：12342。
        :type Filters: list of Filter
        :param DatasourceConnectionName: 指定查询的数据源名称，默认为DataLakeCatalog
        :type DatasourceConnectionName: str
        :param StartTime: 起始时间：用于对更新时间的筛选
        :type StartTime: str
        :param EndTime: 终止时间：用于对更新时间的筛选
        :type EndTime: str
        :param Sort: 排序字段，支持：ModifiedTime（默认）；CreateTime
        :type Sort: str
        :param Asc: 排序字段，false：降序（默认）；true
        :type Asc: bool
        :param TableType: table type，表类型查询,可用值:EXTERNAL_TABLE,INDEX_TABLE,MANAGED_TABLE,MATERIALIZED_VIEW,TABLE,VIEW,VIRTUAL_VIEW
        :type TableType: str
        """
        self.Limit = None
        self.Offset = None
        self.DatabaseName = None
        self.Filters = None
        self.DatasourceConnectionName = None
        self.StartTime = None
        self.EndTime = None
        self.Sort = None
        self.Asc = None
        self.TableType = None


    def _deserialize(self, params):
        self.Limit = params.get("Limit")
        self.Offset = params.get("Offset")
        self.DatabaseName = params.get("DatabaseName")
        if params.get("Filters") is not None:
            self.Filters = []
            for item in params.get("Filters"):
                obj = Filter()
                obj._deserialize(item)
                self.Filters.append(obj)
        self.DatasourceConnectionName = params.get("DatasourceConnectionName")
        self.StartTime = params.get("StartTime")
        self.EndTime = params.get("EndTime")
        self.Sort = params.get("Sort")
        self.Asc = params.get("Asc")
        self.TableType = params.get("TableType")
        memeber_set = set(params.keys())
        for name, value in vars(self).items():
            if name in memeber_set:
                memeber_set.remove(name)
        if len(memeber_set) > 0:
            warnings.warn("%s fileds are useless." % ",".join(memeber_set))
        


class DescribeMetaTablesResponse(AbstractModel):
    """DescribeMetaTables返回参数结构体

    """

    def __init__(self):
        r"""
        :param TableList: 数据表对象列表。
        :type TableList: list of TableResponseInfo
        :param TotalCount: 实例总数。
        :type TotalCount: int
        :param RequestId: 唯一请求 ID，每次请求都会返回。定位问题时需要提供该次请求的 RequestId。
        :type RequestId: str
        """
        self.TableList = None
        self.TotalCount = None
        self.RequestId = None


    def _deserialize(self, params):
        if params.get("TableList") is not None:
            self.TableList = []
            for item in params.get("TableList"):
                obj = TableResponseInfo()
                obj._deserialize(item)
                self.TableList.append(obj)
        self.TotalCount = params.get("TotalCount")
        self.RequestId = params.get("RequestId")


class DescribeMonitorObjectsRequest(AbstractModel):
    """DescribeMonitorObjects请求参数结构体

    """

    def __init__(self):
        r"""
        :param Limit: 返回数量
        :type Limit: int
        :param Offset: 数据偏移量
        :type Offset: int
        """
        self.Limit = None
        self.Offset = None


    def _deserialize(self, params):
        self.Limit = params.get("Limit")
        self.Offset = params.get("Offset")
        memeber_set = set(params.keys())
        for name, value in vars(self).items():
            if name in memeber_set:
                memeber_set.remove(name)
        if len(memeber_set) > 0:
            warnings.warn("%s fileds are useless." % ",".join(memeber_set))
        


class DescribeMonitorObjectsResponse(AbstractModel):
    """DescribeMonitorObjects返回参数结构体

    """

    def __init__(self):
        r"""
        :param MonitorObjects: 监控对象
        :type MonitorObjects: list of MonitorObject
        :param TotalCount: 总数
        :type TotalCount: int
        :param RequestId: 唯一请求 ID，每次请求都会返回。定位问题时需要提供该次请求的 RequestId。
        :type RequestId: str
        """
        self.MonitorObjects = None
        self.TotalCount = None
        self.RequestId = None


    def _deserialize(self, params):
        if params.get("MonitorObjects") is not None:
            self.MonitorObjects = []
            for item in params.get("MonitorObjects"):
                obj = MonitorObject()
                obj._deserialize(item)
                self.MonitorObjects.append(obj)
        self.TotalCount = params.get("TotalCount")
        self.RequestId = params.get("RequestId")


class DescribeNetworkConnectionsRequest(AbstractModel):
    """DescribeNetworkConnections请求参数结构体

    """

    def __init__(self):
        r"""
        :param NetworkConnectionType: 网络配置类型
        :type NetworkConnectionType: int
        :param DataEngineName: 计算引擎名称
        :type DataEngineName: str
        :param DatasourceConnectionVpcId: 数据源vpcid
        :type DatasourceConnectionVpcId: str
        :param Limit: 返回数量，默认为10，最大值为100。
        :type Limit: int
        :param Offset: 偏移量，默认为0。
        :type Offset: int
        :param NetworkConnectionName: 网络配置名称
        :type NetworkConnectionName: str
        """
        self.NetworkConnectionType = None
        self.DataEngineName = None
        self.DatasourceConnectionVpcId = None
        self.Limit = None
        self.Offset = None
        self.NetworkConnectionName = None


    def _deserialize(self, params):
        self.NetworkConnectionType = params.get("NetworkConnectionType")
        self.DataEngineName = params.get("DataEngineName")
        self.DatasourceConnectionVpcId = params.get("DatasourceConnectionVpcId")
        self.Limit = params.get("Limit")
        self.Offset = params.get("Offset")
        self.NetworkConnectionName = params.get("NetworkConnectionName")
        memeber_set = set(params.keys())
        for name, value in vars(self).items():
            if name in memeber_set:
                memeber_set.remove(name)
        if len(memeber_set) > 0:
            warnings.warn("%s fileds are useless." % ",".join(memeber_set))
        


class DescribeNetworkConnectionsResponse(AbstractModel):
    """DescribeNetworkConnections返回参数结构体

    """

    def __init__(self):
        r"""
        :param TotalCount: 总条数
        :type TotalCount: int
        :param NetworkConnectionSet: 网络配置列表
        :type NetworkConnectionSet: list of NetworkConnection
        :param RequestId: 唯一请求 ID，每次请求都会返回。定位问题时需要提供该次请求的 RequestId。
        :type RequestId: str
        """
        self.TotalCount = None
        self.NetworkConnectionSet = None
        self.RequestId = None


    def _deserialize(self, params):
        self.TotalCount = params.get("TotalCount")
        if params.get("NetworkConnectionSet") is not None:
            self.NetworkConnectionSet = []
            for item in params.get("NetworkConnectionSet"):
                obj = NetworkConnection()
                obj._deserialize(item)
                self.NetworkConnectionSet.append(obj)
        self.RequestId = params.get("RequestId")


class DescribeNotebookSessionLogRequest(AbstractModel):
    """DescribeNotebookSessionLog请求参数结构体

    """

    def __init__(self):
        r"""
        :param SessionId: Session唯一标识
        :type SessionId: str
        :param Limit: 分页参数，默认200
        :type Limit: int
        :param Offset: 分页参数，默认0
        :type Offset: int
        """
        self.SessionId = None
        self.Limit = None
        self.Offset = None


    def _deserialize(self, params):
        self.SessionId = params.get("SessionId")
        self.Limit = params.get("Limit")
        self.Offset = params.get("Offset")
        memeber_set = set(params.keys())
        for name, value in vars(self).items():
            if name in memeber_set:
                memeber_set.remove(name)
        if len(memeber_set) > 0:
            warnings.warn("%s fileds are useless." % ",".join(memeber_set))
        


class DescribeNotebookSessionLogResponse(AbstractModel):
    """DescribeNotebookSessionLog返回参数结构体

    """

    def __init__(self):
        r"""
        :param Logs: 日志信息，默认获取最新的200条
        :type Logs: list of str
        :param Limit: 分页参数，默认200
        :type Limit: int
        :param Offset: 分页参数，默认0
        :type Offset: int
        :param RequestId: 唯一请求 ID，每次请求都会返回。定位问题时需要提供该次请求的 RequestId。
        :type RequestId: str
        """
        self.Logs = None
        self.Limit = None
        self.Offset = None
        self.RequestId = None


    def _deserialize(self, params):
        self.Logs = params.get("Logs")
        self.Limit = params.get("Limit")
        self.Offset = params.get("Offset")
        self.RequestId = params.get("RequestId")


class DescribeNotebookSessionRequest(AbstractModel):
    """DescribeNotebookSession请求参数结构体

    """

    def __init__(self):
        r"""
        :param SessionId: Session唯一标识
        :type SessionId: str
        """
        self.SessionId = None


    def _deserialize(self, params):
        self.SessionId = params.get("SessionId")
        memeber_set = set(params.keys())
        for name, value in vars(self).items():
            if name in memeber_set:
                memeber_set.remove(name)
        if len(memeber_set) > 0:
            warnings.warn("%s fileds are useless." % ",".join(memeber_set))
        


class DescribeNotebookSessionResponse(AbstractModel):
    """DescribeNotebookSession返回参数结构体

    """

    def __init__(self):
        r"""
        :param Session: Session详情信息
        :type Session: :class:`tencentcloud.dlc.v20210125.models.NotebookSessionInfo`
        :param RequestId: 唯一请求 ID，每次请求都会返回。定位问题时需要提供该次请求的 RequestId。
        :type RequestId: str
        """
        self.Session = None
        self.RequestId = None


    def _deserialize(self, params):
        if params.get("Session") is not None:
            self.Session = NotebookSessionInfo()
            self.Session._deserialize(params.get("Session"))
        self.RequestId = params.get("RequestId")


class DescribeNotebookSessionStatementRequest(AbstractModel):
    """DescribeNotebookSessionStatement请求参数结构体

    """

    def __init__(self):
        r"""
        :param SessionId: Session唯一标识
        :type SessionId: str
        :param StatementId: Session Statement唯一标识
        :type StatementId: str
        :param TaskId: 任务唯一标识
        :type TaskId: str
        """
        self.SessionId = None
        self.StatementId = None
        self.TaskId = None


    def _deserialize(self, params):
        self.SessionId = params.get("SessionId")
        self.StatementId = params.get("StatementId")
        self.TaskId = params.get("TaskId")
        memeber_set = set(params.keys())
        for name, value in vars(self).items():
            if name in memeber_set:
                memeber_set.remove(name)
        if len(memeber_set) > 0:
            warnings.warn("%s fileds are useless." % ",".join(memeber_set))
        


class DescribeNotebookSessionStatementResponse(AbstractModel):
    """DescribeNotebookSessionStatement返回参数结构体

    """

    def __init__(self):
        r"""
        :param NotebookSessionStatement: Session Statement详情
        :type NotebookSessionStatement: :class:`tencentcloud.dlc.v20210125.models.NotebookSessionStatementInfo`
        :param RequestId: 唯一请求 ID，每次请求都会返回。定位问题时需要提供该次请求的 RequestId。
        :type RequestId: str
        """
        self.NotebookSessionStatement = None
        self.RequestId = None


    def _deserialize(self, params):
        if params.get("NotebookSessionStatement") is not None:
            self.NotebookSessionStatement = NotebookSessionStatementInfo()
            self.NotebookSessionStatement._deserialize(params.get("NotebookSessionStatement"))
        self.RequestId = params.get("RequestId")


class DescribeNotebookSessionStatementSqlResultRequest(AbstractModel):
    """DescribeNotebookSessionStatementSqlResult请求参数结构体

    """

    def __init__(self):
        r"""
        :param TaskId: 任务唯一ID
        :type TaskId: str
        :param MaxResults: 返回结果的最大行数，范围0~1000，默认为1000.
        :type MaxResults: int
        :param NextToken: 上一次请求响应返回的分页信息。第一次可以不带，从头开始返回数据，每次返回MaxResults字段设置的数据量。
        :type NextToken: str
        """
        self.TaskId = None
        self.MaxResults = None
        self.NextToken = None


    def _deserialize(self, params):
        self.TaskId = params.get("TaskId")
        self.MaxResults = params.get("MaxResults")
        self.NextToken = params.get("NextToken")
        memeber_set = set(params.keys())
        for name, value in vars(self).items():
            if name in memeber_set:
                memeber_set.remove(name)
        if len(memeber_set) > 0:
            warnings.warn("%s fileds are useless." % ",".join(memeber_set))
        


class DescribeNotebookSessionStatementSqlResultResponse(AbstractModel):
    """DescribeNotebookSessionStatementSqlResult返回参数结构体

    """

    def __init__(self):
        r"""
        :param TaskId: 任务Id
        :type TaskId: str
        :param ResultSet: 结果数据
        :type ResultSet: str
        :param ResultSchema: schema
        :type ResultSchema: list of Column
        :param NextToken: 分页信息
注意：此字段可能返回 null，表示取不到有效值。
        :type NextToken: str
        :param OutputPath: 存储结果地址
注意：此字段可能返回 null，表示取不到有效值。
        :type OutputPath: str
        :param RequestId: 唯一请求 ID，每次请求都会返回。定位问题时需要提供该次请求的 RequestId。
        :type RequestId: str
        """
        self.TaskId = None
        self.ResultSet = None
        self.ResultSchema = None
        self.NextToken = None
        self.OutputPath = None
        self.RequestId = None


    def _deserialize(self, params):
        self.TaskId = params.get("TaskId")
        self.ResultSet = params.get("ResultSet")
        if params.get("ResultSchema") is not None:
            self.ResultSchema = []
            for item in params.get("ResultSchema"):
                obj = Column()
                obj._deserialize(item)
                self.ResultSchema.append(obj)
        self.NextToken = params.get("NextToken")
        self.OutputPath = params.get("OutputPath")
        self.RequestId = params.get("RequestId")


class DescribeNotebookSessionStatementsRequest(AbstractModel):
    """DescribeNotebookSessionStatements请求参数结构体

    """

    def __init__(self):
        r"""
        :param SessionId: Session唯一标识
        :type SessionId: str
        :param BatchId: 批任务id
        :type BatchId: str
        """
        self.SessionId = None
        self.BatchId = None


    def _deserialize(self, params):
        self.SessionId = params.get("SessionId")
        self.BatchId = params.get("BatchId")
        memeber_set = set(params.keys())
        for name, value in vars(self).items():
            if name in memeber_set:
                memeber_set.remove(name)
        if len(memeber_set) > 0:
            warnings.warn("%s fileds are useless." % ",".join(memeber_set))
        


class DescribeNotebookSessionStatementsResponse(AbstractModel):
    """DescribeNotebookSessionStatements返回参数结构体

    """

    def __init__(self):
        r"""
        :param NotebookSessionStatements: Session Statement详情
        :type NotebookSessionStatements: :class:`tencentcloud.dlc.v20210125.models.NotebookSessionStatementBatchInformation`
        :param RequestId: 唯一请求 ID，每次请求都会返回。定位问题时需要提供该次请求的 RequestId。
        :type RequestId: str
        """
        self.NotebookSessionStatements = None
        self.RequestId = None


    def _deserialize(self, params):
        if params.get("NotebookSessionStatements") is not None:
            self.NotebookSessionStatements = NotebookSessionStatementBatchInformation()
            self.NotebookSessionStatements._deserialize(params.get("NotebookSessionStatements"))
        self.RequestId = params.get("RequestId")


class DescribeNotebookSessionsRequest(AbstractModel):
    """DescribeNotebookSessions请求参数结构体

    """

    def __init__(self):
        r"""
        :param DataEngineName: DLC Spark作业引擎名称
        :type DataEngineName: str
        :param State: Session状态，包含：not_started（未启动）、starting（已启动）、idle（等待输入）、busy(正在运行statement)、shutting_down（停止）、error（异常）、dead（已退出）、killed（被杀死）、success（正常停止）
        :type State: list of str
        :param SortFields: 排序字段（默认按创建时间）
        :type SortFields: list of str
        :param Asc: 排序字段：true：升序、false：降序（默认）
        :type Asc: bool
        :param Limit: 分页参数，默认10
        :type Limit: int
        :param Offset: 分页参数，默认0
        :type Offset: int
        """
        self.DataEngineName = None
        self.State = None
        self.SortFields = None
        self.Asc = None
        self.Limit = None
        self.Offset = None


    def _deserialize(self, params):
        self.DataEngineName = params.get("DataEngineName")
        self.State = params.get("State")
        self.SortFields = params.get("SortFields")
        self.Asc = params.get("Asc")
        self.Limit = params.get("Limit")
        self.Offset = params.get("Offset")
        memeber_set = set(params.keys())
        for name, value in vars(self).items():
            if name in memeber_set:
                memeber_set.remove(name)
        if len(memeber_set) > 0:
            warnings.warn("%s fileds are useless." % ",".join(memeber_set))
        


class DescribeNotebookSessionsResponse(AbstractModel):
    """DescribeNotebookSessions返回参数结构体

    """

    def __init__(self):
        r"""
        :param TotalElements: session总数量
        :type TotalElements: int
        :param TotalPages: 总页数
        :type TotalPages: int
        :param Page: 当前页码
        :type Page: int
        :param Size: 当前页数量
        :type Size: int
        :param Sessions: session列表信息
        :type Sessions: list of NotebookSessions
        :param RequestId: 唯一请求 ID，每次请求都会返回。定位问题时需要提供该次请求的 RequestId。
        :type RequestId: str
        """
        self.TotalElements = None
        self.TotalPages = None
        self.Page = None
        self.Size = None
        self.Sessions = None
        self.RequestId = None


    def _deserialize(self, params):
        self.TotalElements = params.get("TotalElements")
        self.TotalPages = params.get("TotalPages")
        self.Page = params.get("Page")
        self.Size = params.get("Size")
        if params.get("Sessions") is not None:
            self.Sessions = []
            for item in params.get("Sessions"):
                obj = NotebookSessions()
                obj._deserialize(item)
                self.Sessions.append(obj)
        self.RequestId = params.get("RequestId")


class DescribeOrCreateCHDFSAccessGroupsRequest(AbstractModel):
    """DescribeOrCreateCHDFSAccessGroups请求参数结构体

    """

    def __init__(self):
        r"""
        :param MountPointAssociateInfos: 挂载点绑定信息
        :type MountPointAssociateInfos: list of MountPointAssociateInfo
        """
        self.MountPointAssociateInfos = None


    def _deserialize(self, params):
        if params.get("MountPointAssociateInfos") is not None:
            self.MountPointAssociateInfos = []
            for item in params.get("MountPointAssociateInfos"):
                obj = MountPointAssociateInfo()
                obj._deserialize(item)
                self.MountPointAssociateInfos.append(obj)
        memeber_set = set(params.keys())
        for name, value in vars(self).items():
            if name in memeber_set:
                memeber_set.remove(name)
        if len(memeber_set) > 0:
            warnings.warn("%s fileds are useless." % ",".join(memeber_set))
        


class DescribeOrCreateCHDFSAccessGroupsResponse(AbstractModel):
    """DescribeOrCreateCHDFSAccessGroups返回参数结构体

    """

    def __init__(self):
        r"""
        :param AssociateInfos: 挂载点绑定信息
        :type AssociateInfos: list of MountPointAssociateInfo
        :param RequestId: 唯一请求 ID，每次请求都会返回。定位问题时需要提供该次请求的 RequestId。
        :type RequestId: str
        """
        self.AssociateInfos = None
        self.RequestId = None


    def _deserialize(self, params):
        if params.get("AssociateInfos") is not None:
            self.AssociateInfos = []
            for item in params.get("AssociateInfos"):
                obj = MountPointAssociateInfo()
                obj._deserialize(item)
                self.AssociateInfos.append(obj)
        self.RequestId = params.get("RequestId")


class DescribeOtherCHDFSBindingListRequest(AbstractModel):
    """DescribeOtherCHDFSBindingList请求参数结构体

    """

    def __init__(self):
        r"""
        :param BucketId: 桶名
        :type BucketId: str
        """
        self.BucketId = None


    def _deserialize(self, params):
        self.BucketId = params.get("BucketId")
        memeber_set = set(params.keys())
        for name, value in vars(self).items():
            if name in memeber_set:
                memeber_set.remove(name)
        if len(memeber_set) > 0:
            warnings.warn("%s fileds are useless." % ",".join(memeber_set))
        


class DescribeOtherCHDFSBindingListResponse(AbstractModel):
    """DescribeOtherCHDFSBindingList返回参数结构体

    """

    def __init__(self):
        r"""
        :param OtherCHDFSBindingList: 非DLC 产品绑定列表
        :type OtherCHDFSBindingList: list of OtherCHDFSBinding
        :param Total: 总记录数
        :type Total: int
        :param RequestId: 唯一请求 ID，每次请求都会返回。定位问题时需要提供该次请求的 RequestId。
        :type RequestId: str
        """
        self.OtherCHDFSBindingList = None
        self.Total = None
        self.RequestId = None


    def _deserialize(self, params):
        if params.get("OtherCHDFSBindingList") is not None:
            self.OtherCHDFSBindingList = []
            for item in params.get("OtherCHDFSBindingList"):
                obj = OtherCHDFSBinding()
                obj._deserialize(item)
                self.OtherCHDFSBindingList.append(obj)
        self.Total = params.get("Total")
        self.RequestId = params.get("RequestId")


class DescribeQueryDirRequest(AbstractModel):
    """DescribeQueryDir请求参数结构体

    """

    def __init__(self):
        r"""
        :param Name: 查到的目录的名称
        :type Name: str
        """
        self.Name = None


    def _deserialize(self, params):
        self.Name = params.get("Name")
        memeber_set = set(params.keys())
        for name, value in vars(self).items():
            if name in memeber_set:
                memeber_set.remove(name)
        if len(memeber_set) > 0:
            warnings.warn("%s fileds are useless." % ",".join(memeber_set))
        


class DescribeQueryDirResponse(AbstractModel):
    """DescribeQueryDir返回参数结构体

    """

    def __init__(self):
        r"""
        :param Dirs: 查到到的目录列表
注意：此字段可能返回 null，表示取不到有效值。
        :type Dirs: list of DataQueryDir
        :param RequestId: 唯一请求 ID，每次请求都会返回。定位问题时需要提供该次请求的 RequestId。
        :type RequestId: str
        """
        self.Dirs = None
        self.RequestId = None


    def _deserialize(self, params):
        if params.get("Dirs") is not None:
            self.Dirs = []
            for item in params.get("Dirs"):
                obj = DataQueryDir()
                obj._deserialize(item)
                self.Dirs.append(obj)
        self.RequestId = params.get("RequestId")


class DescribeQueryDirsRequest(AbstractModel):
    """DescribeQueryDirs请求参数结构体

    """

    def __init__(self):
        r"""
        :param Offset: 列举的偏移位置
        :type Offset: int
        :param Limit: 列举的最大条数
        :type Limit: int
        """
        self.Offset = None
        self.Limit = None


    def _deserialize(self, params):
        self.Offset = params.get("Offset")
        self.Limit = params.get("Limit")
        memeber_set = set(params.keys())
        for name, value in vars(self).items():
            if name in memeber_set:
                memeber_set.remove(name)
        if len(memeber_set) > 0:
            warnings.warn("%s fileds are useless." % ",".join(memeber_set))
        


class DescribeQueryDirsResponse(AbstractModel):
    """DescribeQueryDirs返回参数结构体

    """

    def __init__(self):
        r"""
        :param Dirs: 列举的目录清单
        :type Dirs: list of DataQueryDir
        :param RequestId: 唯一请求 ID，每次请求都会返回。定位问题时需要提供该次请求的 RequestId。
        :type RequestId: str
        """
        self.Dirs = None
        self.RequestId = None


    def _deserialize(self, params):
        if params.get("Dirs") is not None:
            self.Dirs = []
            for item in params.get("Dirs"):
                obj = DataQueryDir()
                obj._deserialize(item)
                self.Dirs.append(obj)
        self.RequestId = params.get("RequestId")


class DescribeQueueRequest(AbstractModel):
    """DescribeQueue请求参数结构体

    """


class DescribeQueueResponse(AbstractModel):
    """DescribeQueue返回参数结构体

    """

    def __init__(self):
        r"""
        :param VpcCidrBlock: 计算集群所在的VPC的网段
        :type VpcCidrBlock: str
        :param State: 计算集群状态，0：初始化中 1：正常 2：迁移中 3：过期
        :type State: int
        :param RequestId: 唯一请求 ID，每次请求都会返回。定位问题时需要提供该次请求的 RequestId。
        :type RequestId: str
        """
        self.VpcCidrBlock = None
        self.State = None
        self.RequestId = None


    def _deserialize(self, params):
        self.VpcCidrBlock = params.get("VpcCidrBlock")
        self.State = params.get("State")
        self.RequestId = params.get("RequestId")


class DescribeRegionRequest(AbstractModel):
    """DescribeRegion请求参数结构体

    """


class DescribeRegionResponse(AbstractModel):
    """DescribeRegion返回参数结构体

    """

    def __init__(self):
        r"""
        :param RegionList: 当前用户可用的地域列表
注意：此字段可能返回 null，表示取不到有效值。
        :type RegionList: list of str
        :param RequestId: 唯一请求 ID，每次请求都会返回。定位问题时需要提供该次请求的 RequestId。
        :type RequestId: str
        """
        self.RegionList = None
        self.RequestId = None


    def _deserialize(self, params):
        self.RegionList = params.get("RegionList")
        self.RequestId = params.get("RequestId")


class DescribeResultDownloadInfoRequest(AbstractModel):
    """DescribeResultDownloadInfo请求参数结构体

    """

    def __init__(self):
        r"""
        :param DataPath: SQL查询结果存放的路径，目前只支持托管的查询结果导出，即Path是lakefs协议的路径
        :type DataPath: str
        :param TaskId: SQL 任务id
        :type TaskId: str
        :param Format: 格式类型 csv/ excel
        :type Format: str
        :param Options: 格式化参数
        :type Options: list of KVPair
        """
        self.DataPath = None
        self.TaskId = None
        self.Format = None
        self.Options = None


    def _deserialize(self, params):
        self.DataPath = params.get("DataPath")
        self.TaskId = params.get("TaskId")
        self.Format = params.get("Format")
        if params.get("Options") is not None:
            self.Options = []
            for item in params.get("Options"):
                obj = KVPair()
                obj._deserialize(item)
                self.Options.append(obj)
        memeber_set = set(params.keys())
        for name, value in vars(self).items():
            if name in memeber_set:
                memeber_set.remove(name)
        if len(memeber_set) > 0:
            warnings.warn("%s fileds are useless." % ",".join(memeber_set))
        


class DescribeResultDownloadInfoResponse(AbstractModel):
    """DescribeResultDownloadInfo返回参数结构体

    """

    def __init__(self):
        r"""
        :param Fs: 托管存储对象
        :type Fs: :class:`tencentcloud.dlc.v20210125.models.LakeFileSystem`
        :param Status: 状态  init | queue | format |  compress | success | error |timeout
注意：此字段可能返回 null，表示取不到有效值。
        :type Status: str
        :param Reason: 原因
注意：此字段可能返回 null，表示取不到有效值。
        :type Reason: str
        :param RequestId: 唯一请求 ID，每次请求都会返回。定位问题时需要提供该次请求的 RequestId。
        :type RequestId: str
        """
        self.Fs = None
        self.Status = None
        self.Reason = None
        self.RequestId = None


    def _deserialize(self, params):
        if params.get("Fs") is not None:
            self.Fs = LakeFileSystem()
            self.Fs._deserialize(params.get("Fs"))
        self.Status = params.get("Status")
        self.Reason = params.get("Reason")
        self.RequestId = params.get("RequestId")


class DescribeResultDownloadRequest(AbstractModel):
    """DescribeResultDownload请求参数结构体

    """

    def __init__(self):
        r"""
        :param DownloadId: 查询任务Id
        :type DownloadId: str
        """
        self.DownloadId = None


    def _deserialize(self, params):
        self.DownloadId = params.get("DownloadId")
        memeber_set = set(params.keys())
        for name, value in vars(self).items():
            if name in memeber_set:
                memeber_set.remove(name)
        if len(memeber_set) > 0:
            warnings.warn("%s fileds are useless." % ",".join(memeber_set))
        


class DescribeResultDownloadResponse(AbstractModel):
    """DescribeResultDownload返回参数结构体

    """

    def __init__(self):
        r"""
        :param Path: 下载文件路径
注意：此字段可能返回 null，表示取不到有效值。
        :type Path: str
        :param Status: 任务状态 init | queue | format | compress | success|  timeout | error
        :type Status: str
        :param Reason: 任务异常原因
注意：此字段可能返回 null，表示取不到有效值。
        :type Reason: str
        :param SecretId: 临时SecretId
注意：此字段可能返回 null，表示取不到有效值。
        :type SecretId: str
        :param SecretKey: 临时SecretKey
注意：此字段可能返回 null，表示取不到有效值。
        :type SecretKey: str
        :param Token: 临时Token
注意：此字段可能返回 null，表示取不到有效值。
        :type Token: str
        :param RequestId: 唯一请求 ID，每次请求都会返回。定位问题时需要提供该次请求的 RequestId。
        :type RequestId: str
        """
        self.Path = None
        self.Status = None
        self.Reason = None
        self.SecretId = None
        self.SecretKey = None
        self.Token = None
        self.RequestId = None


    def _deserialize(self, params):
        self.Path = params.get("Path")
        self.Status = params.get("Status")
        self.Reason = params.get("Reason")
        self.SecretId = params.get("SecretId")
        self.SecretKey = params.get("SecretKey")
        self.Token = params.get("Token")
        self.RequestId = params.get("RequestId")


class DescribeResultSizeRequest(AbstractModel):
    """DescribeResultSize请求参数结构体

    """

    def __init__(self):
        r"""
        :param DataPath: SQL查询结果地址，由于目前只支持托管的查询结果下载，即Path是lakefs协议的地址
        :type DataPath: str
        """
        self.DataPath = None


    def _deserialize(self, params):
        self.DataPath = params.get("DataPath")
        memeber_set = set(params.keys())
        for name, value in vars(self).items():
            if name in memeber_set:
                memeber_set.remove(name)
        if len(memeber_set) > 0:
            warnings.warn("%s fileds are useless." % ",".join(memeber_set))
        


class DescribeResultSizeResponse(AbstractModel):
    """DescribeResultSize返回参数结构体

    """

    def __init__(self):
        r"""
        :param DataAmount: 结果数据大小，单位为B
        :type DataAmount: int
        :param RequestId: 唯一请求 ID，每次请求都会返回。定位问题时需要提供该次请求的 RequestId。
        :type RequestId: str
        """
        self.DataAmount = None
        self.RequestId = None


    def _deserialize(self, params):
        self.DataAmount = params.get("DataAmount")
        self.RequestId = params.get("RequestId")


class DescribeSQLSessionCatalogRequest(AbstractModel):
    """DescribeSQLSessionCatalog请求参数结构体

    """


class DescribeSQLSessionCatalogResponse(AbstractModel):
    """DescribeSQLSessionCatalog返回参数结构体

    """

    def __init__(self):
        r"""
        :param Status: SUCCESS：成功、FAIL：失败、FLUSH：会话内容已变更，请刷新（修改时触发）、DUPLICATE：重名，请调整、NOTEMPTY：该目录下不为空，无法删除、
LIMITEXCEEDED：创建的会话超过限制；
        :type Status: str
        :param Total: 列表总数
        :type Total: int
        :param SQLSessionCatalogList: 获取目录列表
        :type SQLSessionCatalogList: list of SQLSessionCatalogInfo
        :param RequestId: 唯一请求 ID，每次请求都会返回。定位问题时需要提供该次请求的 RequestId。
        :type RequestId: str
        """
        self.Status = None
        self.Total = None
        self.SQLSessionCatalogList = None
        self.RequestId = None


    def _deserialize(self, params):
        self.Status = params.get("Status")
        self.Total = params.get("Total")
        if params.get("SQLSessionCatalogList") is not None:
            self.SQLSessionCatalogList = []
            for item in params.get("SQLSessionCatalogList"):
                obj = SQLSessionCatalogInfo()
                obj._deserialize(item)
                self.SQLSessionCatalogList.append(obj)
        self.RequestId = params.get("RequestId")


class DescribeSQLSessionSnapshotRequest(AbstractModel):
    """DescribeSQLSessionSnapshot请求参数结构体

    """

    def __init__(self):
        r"""
        :param SessionId: 会话ID
        :type SessionId: str
        """
        self.SessionId = None


    def _deserialize(self, params):
        self.SessionId = params.get("SessionId")
        memeber_set = set(params.keys())
        for name, value in vars(self).items():
            if name in memeber_set:
                memeber_set.remove(name)
        if len(memeber_set) > 0:
            warnings.warn("%s fileds are useless." % ",".join(memeber_set))
        


class DescribeSQLSessionSnapshotResponse(AbstractModel):
    """DescribeSQLSessionSnapshot返回参数结构体

    """

    def __init__(self):
        r"""
        :param SQLSessionSnapshotInfo: 会话详情信息
        :type SQLSessionSnapshotInfo: :class:`tencentcloud.dlc.v20210125.models.SQLSessionSnapshotInfo`
        :param Status: SUCCESS：成功、FAIL：失败、FLUSH：会话内容已变更，请刷新（修改时触发）、DUPLICATE：重名，请调整、NOTEMPTY：该目录下不为空，无法删除、
LIMITEXCEEDED：创建的会话超过限制；
        :type Status: str
        :param RequestId: 唯一请求 ID，每次请求都会返回。定位问题时需要提供该次请求的 RequestId。
        :type RequestId: str
        """
        self.SQLSessionSnapshotInfo = None
        self.Status = None
        self.RequestId = None


    def _deserialize(self, params):
        if params.get("SQLSessionSnapshotInfo") is not None:
            self.SQLSessionSnapshotInfo = SQLSessionSnapshotInfo()
            self.SQLSessionSnapshotInfo._deserialize(params.get("SQLSessionSnapshotInfo"))
        self.Status = params.get("Status")
        self.RequestId = params.get("RequestId")


class DescribeSQLSessionSnapshotsRequest(AbstractModel):
    """DescribeSQLSessionSnapshots请求参数结构体

    """

    def __init__(self):
        r"""
        :param SessionId: 会话ID
        :type SessionId: str
        :param SessionName: 会话名称
        :type SessionName: str
        :param Operator: 操作者
        :type Operator: str
        :param StartTime: 开始时间
        :type StartTime: str
        :param EndTime: 结束时间
        :type EndTime: str
        :param Sort: 排序字段：当前支持CreateTime、UpdateTIme、LastUsed
        :type Sort: str
        :param Asc: true：升序、false：降序（默认）
        :type Asc: bool
        :param Limit: 分页字段
        :type Limit: int
        :param Offset: 分页字段
        :type Offset: int
        """
        self.SessionId = None
        self.SessionName = None
        self.Operator = None
        self.StartTime = None
        self.EndTime = None
        self.Sort = None
        self.Asc = None
        self.Limit = None
        self.Offset = None


    def _deserialize(self, params):
        self.SessionId = params.get("SessionId")
        self.SessionName = params.get("SessionName")
        self.Operator = params.get("Operator")
        self.StartTime = params.get("StartTime")
        self.EndTime = params.get("EndTime")
        self.Sort = params.get("Sort")
        self.Asc = params.get("Asc")
        self.Limit = params.get("Limit")
        self.Offset = params.get("Offset")
        memeber_set = set(params.keys())
        for name, value in vars(self).items():
            if name in memeber_set:
                memeber_set.remove(name)
        if len(memeber_set) > 0:
            warnings.warn("%s fileds are useless." % ",".join(memeber_set))
        


class DescribeSQLSessionSnapshotsResponse(AbstractModel):
    """DescribeSQLSessionSnapshots返回参数结构体

    """

    def __init__(self):
        r"""
        :param Total: 列表总数
        :type Total: int
        :param SQLSessionSnapshotList: 会话快照列表
        :type SQLSessionSnapshotList: list of SQLSessionSnapshotBaseInfo
        :param RequestId: 唯一请求 ID，每次请求都会返回。定位问题时需要提供该次请求的 RequestId。
        :type RequestId: str
        """
        self.Total = None
        self.SQLSessionSnapshotList = None
        self.RequestId = None


    def _deserialize(self, params):
        self.Total = params.get("Total")
        if params.get("SQLSessionSnapshotList") is not None:
            self.SQLSessionSnapshotList = []
            for item in params.get("SQLSessionSnapshotList"):
                obj = SQLSessionSnapshotBaseInfo()
                obj._deserialize(item)
                self.SQLSessionSnapshotList.append(obj)
        self.RequestId = params.get("RequestId")


class DescribeSQLSessionSubmitRecordsRequest(AbstractModel):
    """DescribeSQLSessionSubmitRecords请求参数结构体

    """

    def __init__(self):
        r"""
        :param SessionId: 会话ID
        :type SessionId: str
        :param StartTime: 开始时间
        :type StartTime: str
        :param EndTime: 结束时间
        :type EndTime: str
        :param Sort: 排序字段：当前支持SubmitTime
        :type Sort: str
        :param Asc: true：升序、false：降序（默认）
        :type Asc: bool
        :param Limit: 分页字段
        :type Limit: int
        :param Offset: 分页字段
        :type Offset: int
        """
        self.SessionId = None
        self.StartTime = None
        self.EndTime = None
        self.Sort = None
        self.Asc = None
        self.Limit = None
        self.Offset = None


    def _deserialize(self, params):
        self.SessionId = params.get("SessionId")
        self.StartTime = params.get("StartTime")
        self.EndTime = params.get("EndTime")
        self.Sort = params.get("Sort")
        self.Asc = params.get("Asc")
        self.Limit = params.get("Limit")
        self.Offset = params.get("Offset")
        memeber_set = set(params.keys())
        for name, value in vars(self).items():
            if name in memeber_set:
                memeber_set.remove(name)
        if len(memeber_set) > 0:
            warnings.warn("%s fileds are useless." % ",".join(memeber_set))
        


class DescribeSQLSessionSubmitRecordsResponse(AbstractModel):
    """DescribeSQLSessionSubmitRecords返回参数结构体

    """

    def __init__(self):
        r"""
        :param Total: 列表总数
        :type Total: int
        :param SQLSessionSubmitRecordsList: SQL会话详情信息列表
        :type SQLSessionSubmitRecordsList: list of SQLSessionSubmitRecord
        :param Status: SUCCESS：成功、FAIL：失败、FLUSH：会话内容已变更，请刷新（修改时触发）、DUPLICATE：重名，请调整、NOTEMPTY：该目录下不为空，无法删除、
LIMITEXCEEDED：创建的会话超过限制；
        :type Status: str
        :param RequestId: 唯一请求 ID，每次请求都会返回。定位问题时需要提供该次请求的 RequestId。
        :type RequestId: str
        """
        self.Total = None
        self.SQLSessionSubmitRecordsList = None
        self.Status = None
        self.RequestId = None


    def _deserialize(self, params):
        self.Total = params.get("Total")
        if params.get("SQLSessionSubmitRecordsList") is not None:
            self.SQLSessionSubmitRecordsList = []
            for item in params.get("SQLSessionSubmitRecordsList"):
                obj = SQLSessionSubmitRecord()
                obj._deserialize(item)
                self.SQLSessionSubmitRecordsList.append(obj)
        self.Status = params.get("Status")
        self.RequestId = params.get("RequestId")


class DescribeScheduleExecutionInfoRequest(AbstractModel):
    """DescribeScheduleExecutionInfo请求参数结构体

    """

    def __init__(self):
        r"""
        :param ScriptId: 脚本ID
        :type ScriptId: str
        :param ScriptName: 脚本名称
        :type ScriptName: str
        :param TaskType: 任务类型，SQL,SparkJar等
        :type TaskType: str
        :param Params: 调度任务自定义参数，[{"Key":"abc","Value":"edf"}]
        :type Params: list of KVPair
        :param Script: sql内容的base64编码
        :type Script: str
        """
        self.ScriptId = None
        self.ScriptName = None
        self.TaskType = None
        self.Params = None
        self.Script = None


    def _deserialize(self, params):
        self.ScriptId = params.get("ScriptId")
        self.ScriptName = params.get("ScriptName")
        self.TaskType = params.get("TaskType")
        if params.get("Params") is not None:
            self.Params = []
            for item in params.get("Params"):
                obj = KVPair()
                obj._deserialize(item)
                self.Params.append(obj)
        self.Script = params.get("Script")
        memeber_set = set(params.keys())
        for name, value in vars(self).items():
            if name in memeber_set:
                memeber_set.remove(name)
        if len(memeber_set) > 0:
            warnings.warn("%s fileds are useless." % ",".join(memeber_set))
        


class DescribeScheduleExecutionInfoResponse(AbstractModel):
    """DescribeScheduleExecutionInfo返回参数结构体

    """

    def __init__(self):
        r"""
        :param ExecutionInfo: 执行信息
注意：此字段可能返回 null，表示取不到有效值。
        :type ExecutionInfo: str
        :param RequestId: 唯一请求 ID，每次请求都会返回。定位问题时需要提供该次请求的 RequestId。
        :type RequestId: str
        """
        self.ExecutionInfo = None
        self.RequestId = None


    def _deserialize(self, params):
        self.ExecutionInfo = params.get("ExecutionInfo")
        self.RequestId = params.get("RequestId")


class DescribeScheduleTaskInstancesRequest(AbstractModel):
    """DescribeScheduleTaskInstances请求参数结构体

    """

    def __init__(self):
        r"""
        :param Limit: 返回数量，默认为10，最大值为100。
        :type Limit: int
        :param Offset: 偏移量，默认为0。
        :type Offset: int
        :param Filters: 过滤条件，如下支持的过滤类型，传参Name应为以下其中一个,其中task-id支持最大50个过滤个数，其他过滤参数支持的总数不超过5个。
"start-time" //开始时间，必须
"end-time" //结束时间，必须
"owner-list" // 责任人列表，必须
"status-list" //实例状态列表，非必须
"workflow-id-list" // 工作流列表，非必须
"cycle-type-list" // 调度类型列表，非必须
"keyword" //任务id,非必须
        :type Filters: list of Filter
        :param Sort: 排序字段，支持如下字段类型，biz-date（数据时间）、tries（重试次数）
        :type Sort: str
        :param Asc: 是否升序
        :type Asc: bool
        """
        self.Limit = None
        self.Offset = None
        self.Filters = None
        self.Sort = None
        self.Asc = None


    def _deserialize(self, params):
        self.Limit = params.get("Limit")
        self.Offset = params.get("Offset")
        if params.get("Filters") is not None:
            self.Filters = []
            for item in params.get("Filters"):
                obj = Filter()
                obj._deserialize(item)
                self.Filters.append(obj)
        self.Sort = params.get("Sort")
        self.Asc = params.get("Asc")
        memeber_set = set(params.keys())
        for name, value in vars(self).items():
            if name in memeber_set:
                memeber_set.remove(name)
        if len(memeber_set) > 0:
            warnings.warn("%s fileds are useless." % ",".join(memeber_set))
        


class DescribeScheduleTaskInstancesResponse(AbstractModel):
    """DescribeScheduleTaskInstances返回参数结构体

    """

    def __init__(self):
        r"""
        :param ScheduleTaskInstances: 调度任务实例
        :type ScheduleTaskInstances: list of ScheduleInstanceInfo
        :param TotalElements: 实例总数
        :type TotalElements: int
        :param RequestId: 唯一请求 ID，每次请求都会返回。定位问题时需要提供该次请求的 RequestId。
        :type RequestId: str
        """
        self.ScheduleTaskInstances = None
        self.TotalElements = None
        self.RequestId = None


    def _deserialize(self, params):
        if params.get("ScheduleTaskInstances") is not None:
            self.ScheduleTaskInstances = []
            for item in params.get("ScheduleTaskInstances"):
                obj = ScheduleInstanceInfo()
                obj._deserialize(item)
                self.ScheduleTaskInstances.append(obj)
        self.TotalElements = params.get("TotalElements")
        self.RequestId = params.get("RequestId")


class DescribeScheduleTasksRequest(AbstractModel):
    """DescribeScheduleTasks请求参数结构体

    """

    def __init__(self):
        r"""
        :param Sort: 排序字段
        :type Sort: str
        :param Asc: 是否升序
        :type Asc: bool
        :param Limit: 返回数量，默认为10，最大值为100。
        :type Limit: int
        :param Offset: 偏移量，默认为0。
        :type Offset: int
        :param Filters: 过滤条件，如下支持的过滤类型，传参Name应为以下其中一个,其中task-id支持最大50个过滤个数，其他过滤参数支持的总数不超过5个。
"update-start-time" //开始时间
update-end-time" //结束时间
keyword" //任务id或任务名称模糊查询
script-name" // 查询名称
        :type Filters: list of Filter
        """
        self.Sort = None
        self.Asc = None
        self.Limit = None
        self.Offset = None
        self.Filters = None


    def _deserialize(self, params):
        self.Sort = params.get("Sort")
        self.Asc = params.get("Asc")
        self.Limit = params.get("Limit")
        self.Offset = params.get("Offset")
        if params.get("Filters") is not None:
            self.Filters = []
            for item in params.get("Filters"):
                obj = Filter()
                obj._deserialize(item)
                self.Filters.append(obj)
        memeber_set = set(params.keys())
        for name, value in vars(self).items():
            if name in memeber_set:
                memeber_set.remove(name)
        if len(memeber_set) > 0:
            warnings.warn("%s fileds are useless." % ",".join(memeber_set))
        


class DescribeScheduleTasksResponse(AbstractModel):
    """DescribeScheduleTasks返回参数结构体

    """

    def __init__(self):
        r"""
        :param ScheduleTasks: 调度任务详情
        :type ScheduleTasks: list of ScheduleTaskInfo
        :param TotalElements: 任务总数
        :type TotalElements: int
        :param RequestId: 唯一请求 ID，每次请求都会返回。定位问题时需要提供该次请求的 RequestId。
        :type RequestId: str
        """
        self.ScheduleTasks = None
        self.TotalElements = None
        self.RequestId = None


    def _deserialize(self, params):
        if params.get("ScheduleTasks") is not None:
            self.ScheduleTasks = []
            for item in params.get("ScheduleTasks"):
                obj = ScheduleTaskInfo()
                obj._deserialize(item)
                self.ScheduleTasks.append(obj)
        self.TotalElements = params.get("TotalElements")
        self.RequestId = params.get("RequestId")


class DescribeScriptsRequest(AbstractModel):
    """DescribeScripts请求参数结构体

    """

    def __init__(self):
        r"""
        :param Limit: 返回数量，默认为10，最大值为100。
        :type Limit: int
        :param Offset: 偏移量，默认为0。
        :type Offset: int
        :param SortBy: 按字段排序，支持如下字段类型，update-time
        :type SortBy: str
        :param Sorting: 排序方式，desc表示正序，asc表示反序，默认asc
        :type Sorting: str
        :param Filters: 过滤条件，如下支持的过滤类型，传参Name应为其一
script-id - String - （过滤条件）script-id取值形如：157de0d1-26b4-4df2-a2d0-b64afc406c25。
script-name-keyword - String - （过滤条件）数据表名称,形如：script-test。
        :type Filters: list of Filter
        """
        self.Limit = None
        self.Offset = None
        self.SortBy = None
        self.Sorting = None
        self.Filters = None


    def _deserialize(self, params):
        self.Limit = params.get("Limit")
        self.Offset = params.get("Offset")
        self.SortBy = params.get("SortBy")
        self.Sorting = params.get("Sorting")
        if params.get("Filters") is not None:
            self.Filters = []
            for item in params.get("Filters"):
                obj = Filter()
                obj._deserialize(item)
                self.Filters.append(obj)
        memeber_set = set(params.keys())
        for name, value in vars(self).items():
            if name in memeber_set:
                memeber_set.remove(name)
        if len(memeber_set) > 0:
            warnings.warn("%s fileds are useless." % ",".join(memeber_set))
        


class DescribeScriptsResponse(AbstractModel):
    """DescribeScripts返回参数结构体

    """

    def __init__(self):
        r"""
        :param Scripts: Script列表
注意：此字段可能返回 null，表示取不到有效值。
        :type Scripts: list of Script
        :param TotalCount: 实例总数
        :type TotalCount: int
        :param RequestId: 唯一请求 ID，每次请求都会返回。定位问题时需要提供该次请求的 RequestId。
        :type RequestId: str
        """
        self.Scripts = None
        self.TotalCount = None
        self.RequestId = None


    def _deserialize(self, params):
        if params.get("Scripts") is not None:
            self.Scripts = []
            for item in params.get("Scripts"):
                obj = Script()
                obj._deserialize(item)
                self.Scripts.append(obj)
        self.TotalCount = params.get("TotalCount")
        self.RequestId = params.get("RequestId")


class DescribeSparkAppJobImagesRequest(AbstractModel):
    """DescribeSparkAppJobImages请求参数结构体

    """


class DescribeSparkAppJobImagesResponse(AbstractModel):
    """DescribeSparkAppJobImages返回参数结构体

    """

    def __init__(self):
        r"""
        :param Total: 总数
        :type Total: int
        :param SparkAppJobImages: Spark镜像信息列表
        :type SparkAppJobImages: list of SparkAppJobImage
        :param RequestId: 唯一请求 ID，每次请求都会返回。定位问题时需要提供该次请求的 RequestId。
        :type RequestId: str
        """
        self.Total = None
        self.SparkAppJobImages = None
        self.RequestId = None


    def _deserialize(self, params):
        self.Total = params.get("Total")
        if params.get("SparkAppJobImages") is not None:
            self.SparkAppJobImages = []
            for item in params.get("SparkAppJobImages"):
                obj = SparkAppJobImage()
                obj._deserialize(item)
                self.SparkAppJobImages.append(obj)
        self.RequestId = params.get("RequestId")


class DescribeSparkAppJobRequest(AbstractModel):
    """DescribeSparkAppJob请求参数结构体

    """

    def __init__(self):
        r"""
        :param JobId: spark作业Id，与JobName同时存在时，JobName无效，JobId与JobName至少存在一个
        :type JobId: str
        :param JobName: spark作业名
        :type JobName: str
        """
        self.JobId = None
        self.JobName = None


    def _deserialize(self, params):
        self.JobId = params.get("JobId")
        self.JobName = params.get("JobName")
        memeber_set = set(params.keys())
        for name, value in vars(self).items():
            if name in memeber_set:
                memeber_set.remove(name)
        if len(memeber_set) > 0:
            warnings.warn("%s fileds are useless." % ",".join(memeber_set))
        


class DescribeSparkAppJobResponse(AbstractModel):
    """DescribeSparkAppJob返回参数结构体

    """

    def __init__(self):
        r"""
        :param Job: spark作业详情
注意：此字段可能返回 null，表示取不到有效值。
        :type Job: :class:`tencentcloud.dlc.v20210125.models.SparkJobInfo`
        :param IsExists: 查询的spark作业是否存在
        :type IsExists: bool
        :param RequestId: 唯一请求 ID，每次请求都会返回。定位问题时需要提供该次请求的 RequestId。
        :type RequestId: str
        """
        self.Job = None
        self.IsExists = None
        self.RequestId = None


    def _deserialize(self, params):
        if params.get("Job") is not None:
            self.Job = SparkJobInfo()
            self.Job._deserialize(params.get("Job"))
        self.IsExists = params.get("IsExists")
        self.RequestId = params.get("RequestId")


class DescribeSparkAppJobUserInfoRequest(AbstractModel):
    """DescribeSparkAppJobUserInfo请求参数结构体

    """

    def __init__(self):
        r"""
        :param SparkAppId: Spark任务返回的唯一标识
        :type SparkAppId: str
        """
        self.SparkAppId = None


    def _deserialize(self, params):
        self.SparkAppId = params.get("SparkAppId")
        memeber_set = set(params.keys())
        for name, value in vars(self).items():
            if name in memeber_set:
                memeber_set.remove(name)
        if len(memeber_set) > 0:
            warnings.warn("%s fileds are useless." % ",".join(memeber_set))
        


class DescribeSparkAppJobUserInfoResponse(AbstractModel):
    """DescribeSparkAppJobUserInfo返回参数结构体

    """

    def __init__(self):
        r"""
        :param AppId: 提交任务的用户Appid
        :type AppId: str
        :param Uin: 提交任务的用户Uin
        :type Uin: str
        :param SubAccountUin: 提交任务的用户SubUin
        :type SubAccountUin: str
        :param RequestId: 唯一请求 ID，每次请求都会返回。定位问题时需要提供该次请求的 RequestId。
        :type RequestId: str
        """
        self.AppId = None
        self.Uin = None
        self.SubAccountUin = None
        self.RequestId = None


    def _deserialize(self, params):
        self.AppId = params.get("AppId")
        self.Uin = params.get("Uin")
        self.SubAccountUin = params.get("SubAccountUin")
        self.RequestId = params.get("RequestId")


class DescribeSparkAppJobsRequest(AbstractModel):
    """DescribeSparkAppJobs请求参数结构体

    """

    def __init__(self):
        r"""
        :param SortBy: 返回结果按照该字段排序
        :type SortBy: str
        :param Sorting: 正序或者倒序，例如：desc
        :type Sorting: str
        :param Filters: 过滤条件，如下支持的过滤类型，传参Name应为其一:spark-job-name（作业名称），spark-job-id（作业id），spark-app-type（作业类型，1：批任务，2：流任务，4：SQL作业），user-name（创建人），key-word（作业名称或ID关键词模糊搜索）
        :type Filters: list of Filter
        :param StartTime: 更新时间起始点，支持格式：yyyy-MM-dd HH:mm:ss
        :type StartTime: str
        :param EndTime: 更新时间截止点，支持格式：yyyy-MM-dd HH:mm:ss
        :type EndTime: str
        :param Offset: 查询列表偏移量, 默认值0
        :type Offset: int
        :param Limit: 查询列表限制数量, 默认值100
        :type Limit: int
        """
        self.SortBy = None
        self.Sorting = None
        self.Filters = None
        self.StartTime = None
        self.EndTime = None
        self.Offset = None
        self.Limit = None


    def _deserialize(self, params):
        self.SortBy = params.get("SortBy")
        self.Sorting = params.get("Sorting")
        if params.get("Filters") is not None:
            self.Filters = []
            for item in params.get("Filters"):
                obj = Filter()
                obj._deserialize(item)
                self.Filters.append(obj)
        self.StartTime = params.get("StartTime")
        self.EndTime = params.get("EndTime")
        self.Offset = params.get("Offset")
        self.Limit = params.get("Limit")
        memeber_set = set(params.keys())
        for name, value in vars(self).items():
            if name in memeber_set:
                memeber_set.remove(name)
        if len(memeber_set) > 0:
            warnings.warn("%s fileds are useless." % ",".join(memeber_set))
        


class DescribeSparkAppJobsResponse(AbstractModel):
    """DescribeSparkAppJobs返回参数结构体

    """

    def __init__(self):
        r"""
        :param SparkAppJobs: spark作业列表详情
        :type SparkAppJobs: list of SparkJobInfo
        :param TotalCount: spark作业总数
        :type TotalCount: int
        :param RequestId: 唯一请求 ID，每次请求都会返回。定位问题时需要提供该次请求的 RequestId。
        :type RequestId: str
        """
        self.SparkAppJobs = None
        self.TotalCount = None
        self.RequestId = None


    def _deserialize(self, params):
        if params.get("SparkAppJobs") is not None:
            self.SparkAppJobs = []
            for item in params.get("SparkAppJobs"):
                obj = SparkJobInfo()
                obj._deserialize(item)
                self.SparkAppJobs.append(obj)
        self.TotalCount = params.get("TotalCount")
        self.RequestId = params.get("RequestId")


class DescribeSparkAppTasksRequest(AbstractModel):
    """DescribeSparkAppTasks请求参数结构体

    """

    def __init__(self):
        r"""
        :param JobId: spark作业Id
        :type JobId: str
        :param Offset: 分页查询偏移量
        :type Offset: int
        :param Limit: 分页查询Limit
        :type Limit: int
        :param TaskId: 执行实例id
        :type TaskId: str
        :param StartTime: 更新时间起始点，支持格式：yyyy-MM-dd HH:mm:ss
        :type StartTime: str
        :param EndTime: 更新时间截止点，支持格式：yyyy-MM-dd HH:mm:ss
        :type EndTime: str
        :param Filters: 按照该参数过滤,支持task-state
        :type Filters: list of Filter
        """
        self.JobId = None
        self.Offset = None
        self.Limit = None
        self.TaskId = None
        self.StartTime = None
        self.EndTime = None
        self.Filters = None


    def _deserialize(self, params):
        self.JobId = params.get("JobId")
        self.Offset = params.get("Offset")
        self.Limit = params.get("Limit")
        self.TaskId = params.get("TaskId")
        self.StartTime = params.get("StartTime")
        self.EndTime = params.get("EndTime")
        if params.get("Filters") is not None:
            self.Filters = []
            for item in params.get("Filters"):
                obj = Filter()
                obj._deserialize(item)
                self.Filters.append(obj)
        memeber_set = set(params.keys())
        for name, value in vars(self).items():
            if name in memeber_set:
                memeber_set.remove(name)
        if len(memeber_set) > 0:
            warnings.warn("%s fileds are useless." % ",".join(memeber_set))
        


class DescribeSparkAppTasksResponse(AbstractModel):
    """DescribeSparkAppTasks返回参数结构体

    """

    def __init__(self):
        r"""
        :param Tasks: 任务结果（该字段已废弃）
注意：此字段可能返回 null，表示取不到有效值。
        :type Tasks: :class:`tencentcloud.dlc.v20210125.models.TaskResponseInfo`
        :param TotalCount: 任务总数
        :type TotalCount: int
        :param SparkAppTasks: 任务结果列表
注意：此字段可能返回 null，表示取不到有效值。
        :type SparkAppTasks: list of TaskResponseInfo
        :param RequestId: 唯一请求 ID，每次请求都会返回。定位问题时需要提供该次请求的 RequestId。
        :type RequestId: str
        """
        self.Tasks = None
        self.TotalCount = None
        self.SparkAppTasks = None
        self.RequestId = None


    def _deserialize(self, params):
        if params.get("Tasks") is not None:
            self.Tasks = TaskResponseInfo()
            self.Tasks._deserialize(params.get("Tasks"))
        self.TotalCount = params.get("TotalCount")
        if params.get("SparkAppTasks") is not None:
            self.SparkAppTasks = []
            for item in params.get("SparkAppTasks"):
                obj = TaskResponseInfo()
                obj._deserialize(item)
                self.SparkAppTasks.append(obj)
        self.RequestId = params.get("RequestId")


class DescribeSparkSessionBatchSqlLogRequest(AbstractModel):
    """DescribeSparkSessionBatchSqlLog请求参数结构体

    """

    def __init__(self):
        r"""
        :param BatchId: SparkSQL唯一标识
        :type BatchId: str
        """
        self.BatchId = None


    def _deserialize(self, params):
        self.BatchId = params.get("BatchId")
        memeber_set = set(params.keys())
        for name, value in vars(self).items():
            if name in memeber_set:
                memeber_set.remove(name)
        if len(memeber_set) > 0:
            warnings.warn("%s fileds are useless." % ",".join(memeber_set))
        


class DescribeSparkSessionBatchSqlLogResponse(AbstractModel):
    """DescribeSparkSessionBatchSqlLog返回参数结构体

    """

    def __init__(self):
        r"""
        :param State: 状态：0：初始化、1：成功、2：失败、3：取消、4：异常；
        :type State: int
        :param LogSet: 日志信息列表
注意：此字段可能返回 null，表示取不到有效值。
        :type LogSet: list of SparkSessionBatchLog
        :param RequestId: 唯一请求 ID，每次请求都会返回。定位问题时需要提供该次请求的 RequestId。
        :type RequestId: str
        """
        self.State = None
        self.LogSet = None
        self.RequestId = None


    def _deserialize(self, params):
        self.State = params.get("State")
        if params.get("LogSet") is not None:
            self.LogSet = []
            for item in params.get("LogSet"):
                obj = SparkSessionBatchLog()
                obj._deserialize(item)
                self.LogSet.append(obj)
        self.RequestId = params.get("RequestId")


class DescribeSparkSessionBatchSqlTasksRequest(AbstractModel):
    """DescribeSparkSessionBatchSqlTasks请求参数结构体

    """

    def __init__(self):
        r"""
        :param Filters: 过滤条件，如下支持的过滤类型，传参Name应为以下其中一个,其中task-id支持最大50个过滤个数，其他过滤参数支持的总数不超过5个。
batch-id - String - （批任务ID准确过滤）batch-id取值形如：e386471f-139a-4e59-877f-50ece8135b99;
session-id - String - (livy Session ID过滤)，如：livy-session-12321;
task-state - String - （任务状态过滤）取值范围 0(初始化)， 1(运行中)， 2(成功)， -1(失败)、-3（已终止）;
task-sql-keyword - String - （SQL语句关键字模糊过滤）取值形如：DROP TABLE;
task-operator- string （子uin过滤）;
task-kind - string （任务类型过滤）;
        :type Filters: list of Filter
        :param SortBy: 排序字段，支持如下字段类型，create-time（创建时间，默认）、update-time（更新时间）
        :type SortBy: str
        :param Sorting: 排序方式，desc表示正序，asc表示反序， 默认为asc。
        :type Sorting: str
        :param StartTime: 起始时间点，格式为yyyy-mm-dd HH:MM:SS。默认为45天前的当前时刻
        :type StartTime: str
        :param EndTime: 结束时间点，格式为yyyy-mm-dd HH:MM:SS时间跨度在(0,30天]，支持最近45天数据查询。默认为当前时刻
        :type EndTime: str
        :param DataEngineName: 支持计算资源名字筛选
        :type DataEngineName: str
        :param Limit: 返回数量，默认为10，最大值为100。
        :type Limit: int
        :param Offset: 偏移量，默认为0。
        :type Offset: int
        """
        self.Filters = None
        self.SortBy = None
        self.Sorting = None
        self.StartTime = None
        self.EndTime = None
        self.DataEngineName = None
        self.Limit = None
        self.Offset = None


    def _deserialize(self, params):
        if params.get("Filters") is not None:
            self.Filters = []
            for item in params.get("Filters"):
                obj = Filter()
                obj._deserialize(item)
                self.Filters.append(obj)
        self.SortBy = params.get("SortBy")
        self.Sorting = params.get("Sorting")
        self.StartTime = params.get("StartTime")
        self.EndTime = params.get("EndTime")
        self.DataEngineName = params.get("DataEngineName")
        self.Limit = params.get("Limit")
        self.Offset = params.get("Offset")
        memeber_set = set(params.keys())
        for name, value in vars(self).items():
            if name in memeber_set:
                memeber_set.remove(name)
        if len(memeber_set) > 0:
            warnings.warn("%s fileds are useless." % ",".join(memeber_set))
        


class DescribeSparkSessionBatchSqlTasksResponse(AbstractModel):
    """DescribeSparkSessionBatchSqlTasks返回参数结构体

    """

    def __init__(self):
        r"""
        :param SparkBatchSQLInformation: 批任务详情
注意：此字段可能返回 null，表示取不到有效值。
        :type SparkBatchSQLInformation: list of SparkSessionBatchSQL
        :param Total: 数量
        :type Total: int
        :param RequestId: 唯一请求 ID，每次请求都会返回。定位问题时需要提供该次请求的 RequestId。
        :type RequestId: str
        """
        self.SparkBatchSQLInformation = None
        self.Total = None
        self.RequestId = None


    def _deserialize(self, params):
        if params.get("SparkBatchSQLInformation") is not None:
            self.SparkBatchSQLInformation = []
            for item in params.get("SparkBatchSQLInformation"):
                obj = SparkSessionBatchSQL()
                obj._deserialize(item)
                self.SparkBatchSQLInformation.append(obj)
        self.Total = params.get("Total")
        self.RequestId = params.get("RequestId")


class DescribeSparkTaskLogDownloadInfoRequest(AbstractModel):
    """DescribeSparkTaskLogDownloadInfo请求参数结构体

    """

    def __init__(self):
        r"""
        :param Sort: 排序字段，默认按创建时间排序
        :type Sort: str
        :param Asc: 是否升序，默认为降序
        :type Asc: bool
        :param Limit: 返回数量
        :type Limit: int
        :param Offset: 偏移量，默认为0。
        :type Offset: int
        """
        self.Sort = None
        self.Asc = None
        self.Limit = None
        self.Offset = None


    def _deserialize(self, params):
        self.Sort = params.get("Sort")
        self.Asc = params.get("Asc")
        self.Limit = params.get("Limit")
        self.Offset = params.get("Offset")
        memeber_set = set(params.keys())
        for name, value in vars(self).items():
            if name in memeber_set:
                memeber_set.remove(name)
        if len(memeber_set) > 0:
            warnings.warn("%s fileds are useless." % ",".join(memeber_set))
        


class DescribeSparkTaskLogDownloadInfoResponse(AbstractModel):
    """DescribeSparkTaskLogDownloadInfo返回参数结构体

    """

    def __init__(self):
        r"""
        :param LogInfos: 日志信息详情
注意：此字段可能返回 null，表示取不到有效值。
        :type LogInfos: list of SparkLogDownloadInfo
        :param TotalCount: 记录总数
注意：此字段可能返回 null，表示取不到有效值。
        :type TotalCount: int
        :param RequestId: 唯一请求 ID，每次请求都会返回。定位问题时需要提供该次请求的 RequestId。
        :type RequestId: str
        """
        self.LogInfos = None
        self.TotalCount = None
        self.RequestId = None


    def _deserialize(self, params):
        if params.get("LogInfos") is not None:
            self.LogInfos = []
            for item in params.get("LogInfos"):
                obj = SparkLogDownloadInfo()
                obj._deserialize(item)
                self.LogInfos.append(obj)
        self.TotalCount = params.get("TotalCount")
        self.RequestId = params.get("RequestId")


class DescribeSparkUiUrlRequest(AbstractModel):
    """DescribeSparkUiUrl请求参数结构体

    """

    def __init__(self):
        r"""
        :param TaskId: spark任务Id
        :type TaskId: str
        """
        self.TaskId = None


    def _deserialize(self, params):
        self.TaskId = params.get("TaskId")
        memeber_set = set(params.keys())
        for name, value in vars(self).items():
            if name in memeber_set:
                memeber_set.remove(name)
        if len(memeber_set) > 0:
            warnings.warn("%s fileds are useless." % ",".join(memeber_set))
        


class DescribeSparkUiUrlResponse(AbstractModel):
    """DescribeSparkUiUrl返回参数结构体

    """

    def __init__(self):
        r"""
        :param SparkUiUrl: spark ui url
        :type SparkUiUrl: str
        :param TaskId: 任务Id
        :type TaskId: str
        :param RequestId: 唯一请求 ID，每次请求都会返回。定位问题时需要提供该次请求的 RequestId。
        :type RequestId: str
        """
        self.SparkUiUrl = None
        self.TaskId = None
        self.RequestId = None


    def _deserialize(self, params):
        self.SparkUiUrl = params.get("SparkUiUrl")
        self.TaskId = params.get("TaskId")
        self.RequestId = params.get("RequestId")


class DescribeStandbyDataEngineRequest(AbstractModel):
    """DescribeStandbyDataEngine请求参数结构体

    """

    def __init__(self):
        r"""
        :param DataEngineName: 主集群名称
        :type DataEngineName: str
        """
        self.DataEngineName = None


    def _deserialize(self, params):
        self.DataEngineName = params.get("DataEngineName")
        memeber_set = set(params.keys())
        for name, value in vars(self).items():
            if name in memeber_set:
                memeber_set.remove(name)
        if len(memeber_set) > 0:
            warnings.warn("%s fileds are useless." % ",".join(memeber_set))
        


class DescribeStandbyDataEngineResponse(AbstractModel):
    """DescribeStandbyDataEngine返回参数结构体

    """

    def __init__(self):
        r"""
        :param SpareDataEngineList: 备集群详细信息
        :type SpareDataEngineList: list of DataEngineInfo
        :param RequestId: 唯一请求 ID，每次请求都会返回。定位问题时需要提供该次请求的 RequestId。
        :type RequestId: str
        """
        self.SpareDataEngineList = None
        self.RequestId = None


    def _deserialize(self, params):
        if params.get("SpareDataEngineList") is not None:
            self.SpareDataEngineList = []
            for item in params.get("SpareDataEngineList"):
                obj = DataEngineInfo()
                obj._deserialize(item)
                self.SpareDataEngineList.append(obj)
        self.RequestId = params.get("RequestId")


class DescribeStoreLocationRequest(AbstractModel):
    """DescribeStoreLocation请求参数结构体

    """


class DescribeStoreLocationResponse(AbstractModel):
    """DescribeStoreLocation返回参数结构体

    """

    def __init__(self):
        r"""
        :param StoreLocation: 返回用户设置的结果存储位置路径，如果未设置则返回空字符串：""
注意：此字段可能返回 null，表示取不到有效值。
        :type StoreLocation: str
        :param RequestId: 唯一请求 ID，每次请求都会返回。定位问题时需要提供该次请求的 RequestId。
        :type RequestId: str
        """
        self.StoreLocation = None
        self.RequestId = None


    def _deserialize(self, params):
        self.StoreLocation = params.get("StoreLocation")
        self.RequestId = params.get("RequestId")


class DescribeSubUsersRequest(AbstractModel):
    """DescribeSubUsers请求参数结构体

    """


class DescribeSubUsersResponse(AbstractModel):
    """DescribeSubUsers返回参数结构体

    """

    def __init__(self):
        r"""
        :param UserinfoList: 用户信息列表
        :type UserinfoList: list of UserAliasInfo
        :param Total: 用户信息总数
        :type Total: int
        :param RequestId: 唯一请求 ID，每次请求都会返回。定位问题时需要提供该次请求的 RequestId。
        :type RequestId: str
        """
        self.UserinfoList = None
        self.Total = None
        self.RequestId = None


    def _deserialize(self, params):
        if params.get("UserinfoList") is not None:
            self.UserinfoList = []
            for item in params.get("UserinfoList"):
                obj = UserAliasInfo()
                obj._deserialize(item)
                self.UserinfoList.append(obj)
        self.Total = params.get("Total")
        self.RequestId = params.get("RequestId")


class DescribeSubuinsRequest(AbstractModel):
    """DescribeSubuins请求参数结构体

    """

    def __init__(self):
        r"""
        :param Limit: 返回个数，默认为10
        :type Limit: int
        :param Offset: 偏移量，默认为0。
        :type Offset: int
        """
        self.Limit = None
        self.Offset = None


    def _deserialize(self, params):
        self.Limit = params.get("Limit")
        self.Offset = params.get("Offset")
        memeber_set = set(params.keys())
        for name, value in vars(self).items():
            if name in memeber_set:
                memeber_set.remove(name)
        if len(memeber_set) > 0:
            warnings.warn("%s fileds are useless." % ",".join(memeber_set))
        


class DescribeSubuinsResponse(AbstractModel):
    """DescribeSubuins返回参数结构体

    """

    def __init__(self):
        r"""
        :param Subuins: 无
        :type Subuins: list of str
        :param RequestId: 唯一请求 ID，每次请求都会返回。定位问题时需要提供该次请求的 RequestId。
        :type RequestId: str
        """
        self.Subuins = None
        self.RequestId = None


    def _deserialize(self, params):
        self.Subuins = params.get("Subuins")
        self.RequestId = params.get("RequestId")


class DescribeSystemStorageRequest(AbstractModel):
    """DescribeSystemStorage请求参数结构体

    """

    def __init__(self):
        r"""
        :param Type: 目录类型，如0为数据导入临时目录，1为udf使用临时目录
        :type Type: int
        """
        self.Type = None


    def _deserialize(self, params):
        self.Type = params.get("Type")
        memeber_set = set(params.keys())
        for name, value in vars(self).items():
            if name in memeber_set:
                memeber_set.remove(name)
        if len(memeber_set) > 0:
            warnings.warn("%s fileds are useless." % ",".join(memeber_set))
        


class DescribeSystemStorageResponse(AbstractModel):
    """DescribeSystemStorage返回参数结构体

    """

    def __init__(self):
        r"""
        :param LakeFileSystem: LakeFileSystem信息
        :type LakeFileSystem: :class:`tencentcloud.dlc.v20210125.models.LakeFileSystem`
        :param RequestId: 唯一请求 ID，每次请求都会返回。定位问题时需要提供该次请求的 RequestId。
        :type RequestId: str
        """
        self.LakeFileSystem = None
        self.RequestId = None


    def _deserialize(self, params):
        if params.get("LakeFileSystem") is not None:
            self.LakeFileSystem = LakeFileSystem()
            self.LakeFileSystem._deserialize(params.get("LakeFileSystem"))
        self.RequestId = params.get("RequestId")


class DescribeTableRequest(AbstractModel):
    """DescribeTable请求参数结构体

    """

    def __init__(self):
        r"""
        :param TableName: 查询对象表名称
        :type TableName: str
        :param DatabaseName: 查询表所在的数据库名称。
        :type DatabaseName: str
        :param DatasourceConnectionName: 查询表所在的数据源名称
        :type DatasourceConnectionName: str
        """
        self.TableName = None
        self.DatabaseName = None
        self.DatasourceConnectionName = None


    def _deserialize(self, params):
        self.TableName = params.get("TableName")
        self.DatabaseName = params.get("DatabaseName")
        self.DatasourceConnectionName = params.get("DatasourceConnectionName")
        memeber_set = set(params.keys())
        for name, value in vars(self).items():
            if name in memeber_set:
                memeber_set.remove(name)
        if len(memeber_set) > 0:
            warnings.warn("%s fileds are useless." % ",".join(memeber_set))
        


class DescribeTableResponse(AbstractModel):
    """DescribeTable返回参数结构体

    """

    def __init__(self):
        r"""
        :param Table: 数据表对象
        :type Table: :class:`tencentcloud.dlc.v20210125.models.TableResponseInfo`
        :param RequestId: 唯一请求 ID，每次请求都会返回。定位问题时需要提供该次请求的 RequestId。
        :type RequestId: str
        """
        self.Table = None
        self.RequestId = None


    def _deserialize(self, params):
        if params.get("Table") is not None:
            self.Table = TableResponseInfo()
            self.Table._deserialize(params.get("Table"))
        self.RequestId = params.get("RequestId")


class DescribeTablesExtendRequest(AbstractModel):
    """DescribeTablesExtend请求参数结构体

    """

    def __init__(self):
        r"""
        :param DatabaseNames: 需要查找的数据库列表
        :type DatabaseNames: list of str
        :param Limit: 返回数量，默认为10，最大值为100。
        :type Limit: int
        :param Offset: 数据偏移量，该接口只支持0。
        :type Offset: int
        :param Filters: 过滤条件，如下支持的过滤类型，传参Name应为其一
table-name - String - （过滤条件）数据表名称,形如：table-001。
table-id - String - （过滤条件）table id形如：12342。
        :type Filters: list of Filter
        :param DatasourceConnectionName: 指定查询的数据源名称，默认为CosDataCatalog
        :type DatasourceConnectionName: str
        """
        self.DatabaseNames = None
        self.Limit = None
        self.Offset = None
        self.Filters = None
        self.DatasourceConnectionName = None


    def _deserialize(self, params):
        self.DatabaseNames = params.get("DatabaseNames")
        self.Limit = params.get("Limit")
        self.Offset = params.get("Offset")
        if params.get("Filters") is not None:
            self.Filters = []
            for item in params.get("Filters"):
                obj = Filter()
                obj._deserialize(item)
                self.Filters.append(obj)
        self.DatasourceConnectionName = params.get("DatasourceConnectionName")
        memeber_set = set(params.keys())
        for name, value in vars(self).items():
            if name in memeber_set:
                memeber_set.remove(name)
        if len(memeber_set) > 0:
            warnings.warn("%s fileds are useless." % ",".join(memeber_set))
        


class DescribeTablesExtendResponse(AbstractModel):
    """DescribeTablesExtend返回参数结构体

    """

    def __init__(self):
        r"""
        :param TableList: 数据表对象列表。
        :type TableList: list of TableResponseInfo
        :param RequestId: 唯一请求 ID，每次请求都会返回。定位问题时需要提供该次请求的 RequestId。
        :type RequestId: str
        """
        self.TableList = None
        self.RequestId = None


    def _deserialize(self, params):
        if params.get("TableList") is not None:
            self.TableList = []
            for item in params.get("TableList"):
                obj = TableResponseInfo()
                obj._deserialize(item)
                self.TableList.append(obj)
        self.RequestId = params.get("RequestId")


class DescribeTablesRequest(AbstractModel):
    """DescribeTables请求参数结构体

    """

    def __init__(self):
        r"""
        :param DatabaseName: 列出该数据库下所属数据表。
        :type DatabaseName: str
        :param Limit: 返回数量，默认为10，最大值为100。
        :type Limit: int
        :param Offset: 数据偏移量，从0开始，默认为0。
        :type Offset: int
        :param Filters: 过滤条件，如下支持的过滤类型，传参Name应为其一
table-name - String - （过滤条件）数据表名称,形如：table-001。
table-id - String - （过滤条件）table id形如：12342。
        :type Filters: list of Filter
        :param DatasourceConnectionName: 指定查询的数据源名称，默认为DataLakeCatalog
        :type DatasourceConnectionName: str
        :param StartTime: 起始时间：用于对更新时间的筛选，格式为yyyy-mm-dd HH:MM:SS
        :type StartTime: str
        :param EndTime: 终止时间：用于对更新时间的筛选，格式为yyyy-mm-dd HH:MM:SS
        :type EndTime: str
        :param Sort: 排序字段，支持：CreateTime（创建时间）、UpdateTime（更新时间）、StorageSize（存储空间）、RecordCount（行数）、Name（表名称）（不传则默认按name升序）
        :type Sort: str
        :param Asc: 排序字段，false：降序（默认）；true：升序
        :type Asc: bool
        :param TableType: table type，表类型查询,可用值:EXTERNAL_TABLE,INDEX_TABLE,MANAGED_TABLE,MATERIALIZED_VIEW,TABLE,VIEW,VIRTUAL_VIEW
        :type TableType: str
        :param TableFormat: 筛选字段-表格式：不传（默认）为查全部；LAKEFS：托管表；ICEBERG：非托管iceberg表；HIVE：非托管hive表；OTHER：非托管其它；
        :type TableFormat: str
        """
        self.DatabaseName = None
        self.Limit = None
        self.Offset = None
        self.Filters = None
        self.DatasourceConnectionName = None
        self.StartTime = None
        self.EndTime = None
        self.Sort = None
        self.Asc = None
        self.TableType = None
        self.TableFormat = None


    def _deserialize(self, params):
        self.DatabaseName = params.get("DatabaseName")
        self.Limit = params.get("Limit")
        self.Offset = params.get("Offset")
        if params.get("Filters") is not None:
            self.Filters = []
            for item in params.get("Filters"):
                obj = Filter()
                obj._deserialize(item)
                self.Filters.append(obj)
        self.DatasourceConnectionName = params.get("DatasourceConnectionName")
        self.StartTime = params.get("StartTime")
        self.EndTime = params.get("EndTime")
        self.Sort = params.get("Sort")
        self.Asc = params.get("Asc")
        self.TableType = params.get("TableType")
        self.TableFormat = params.get("TableFormat")
        memeber_set = set(params.keys())
        for name, value in vars(self).items():
            if name in memeber_set:
                memeber_set.remove(name)
        if len(memeber_set) > 0:
            warnings.warn("%s fileds are useless." % ",".join(memeber_set))
        


class DescribeTablesResponse(AbstractModel):
    """DescribeTables返回参数结构体

    """

    def __init__(self):
        r"""
        :param TableList: 数据表对象列表。
        :type TableList: list of TableResponseInfo
        :param TotalCount: 实例总数。
        :type TotalCount: int
        :param RequestId: 唯一请求 ID，每次请求都会返回。定位问题时需要提供该次请求的 RequestId。
        :type RequestId: str
        """
        self.TableList = None
        self.TotalCount = None
        self.RequestId = None


    def _deserialize(self, params):
        if params.get("TableList") is not None:
            self.TableList = []
            for item in params.get("TableList"):
                obj = TableResponseInfo()
                obj._deserialize(item)
                self.TableList.append(obj)
        self.TotalCount = params.get("TotalCount")
        self.RequestId = params.get("RequestId")


class DescribeTaskMetricsRequest(AbstractModel):
    """DescribeTaskMetrics请求参数结构体

    """

    def __init__(self):
        r"""
        :param TaskId: 任务Id
        :type TaskId: str
        """
        self.TaskId = None


    def _deserialize(self, params):
        self.TaskId = params.get("TaskId")
        memeber_set = set(params.keys())
        for name, value in vars(self).items():
            if name in memeber_set:
                memeber_set.remove(name)
        if len(memeber_set) > 0:
            warnings.warn("%s fileds are useless." % ",".join(memeber_set))
        


class DescribeTaskMetricsResponse(AbstractModel):
    """DescribeTaskMetrics返回参数结构体

    """

    def __init__(self):
        r"""
        :param Metrics: 指标
注意：此字段可能返回 null，表示取不到有效值。
        :type Metrics: :class:`tencentcloud.dlc.v20210125.models.TaskStatisticMetrics`
        :param RequestId: 唯一请求 ID，每次请求都会返回。定位问题时需要提供该次请求的 RequestId。
        :type RequestId: str
        """
        self.Metrics = None
        self.RequestId = None


    def _deserialize(self, params):
        if params.get("Metrics") is not None:
            self.Metrics = TaskStatisticMetrics()
            self.Metrics._deserialize(params.get("Metrics"))
        self.RequestId = params.get("RequestId")


class DescribeTaskResultRequest(AbstractModel):
    """DescribeTaskResult请求参数结构体

    """

    def __init__(self):
        r"""
        :param TaskId: 任务唯一ID
        :type TaskId: str
        :param NextToken: 上一次请求响应返回的分页信息。第一次可以不带，从头开始返回数据，每次返回MaxResults字段设置的数据量。
        :type NextToken: str
        :param MaxResults: 返回结果的最大行数，范围0~1000，默认为1000.
        :type MaxResults: int
        """
        self.TaskId = None
        self.NextToken = None
        self.MaxResults = None


    def _deserialize(self, params):
        self.TaskId = params.get("TaskId")
        self.NextToken = params.get("NextToken")
        self.MaxResults = params.get("MaxResults")
        memeber_set = set(params.keys())
        for name, value in vars(self).items():
            if name in memeber_set:
                memeber_set.remove(name)
        if len(memeber_set) > 0:
            warnings.warn("%s fileds are useless." % ",".join(memeber_set))
        


class DescribeTaskResultResponse(AbstractModel):
    """DescribeTaskResult返回参数结构体

    """

    def __init__(self):
        r"""
        :param TaskInfo: 查询的任务信息，返回为空表示输入任务ID对应的任务不存在。只有当任务状态为成功（2）的时候，才会返回任务的结果。
注意：此字段可能返回 null，表示取不到有效值。
        :type TaskInfo: :class:`tencentcloud.dlc.v20210125.models.TaskResultInfo`
        :param RequestId: 唯一请求 ID，每次请求都会返回。定位问题时需要提供该次请求的 RequestId。
        :type RequestId: str
        """
        self.TaskInfo = None
        self.RequestId = None


    def _deserialize(self, params):
        if params.get("TaskInfo") is not None:
            self.TaskInfo = TaskResultInfo()
            self.TaskInfo._deserialize(params.get("TaskInfo"))
        self.RequestId = params.get("RequestId")


class DescribeTasksOverviewRequest(AbstractModel):
    """DescribeTasksOverview请求参数结构体

    """

    def __init__(self):
        r"""
        :param StartTime: 开始时间
        :type StartTime: str
        :param EndTime: 结束时间
        :type EndTime: str
        :param Filters: 筛选条件
        :type Filters: list of Filter
        :param DataEngineName: 引擎名
        :type DataEngineName: str
        """
        self.StartTime = None
        self.EndTime = None
        self.Filters = None
        self.DataEngineName = None


    def _deserialize(self, params):
        self.StartTime = params.get("StartTime")
        self.EndTime = params.get("EndTime")
        if params.get("Filters") is not None:
            self.Filters = []
            for item in params.get("Filters"):
                obj = Filter()
                obj._deserialize(item)
                self.Filters.append(obj)
        self.DataEngineName = params.get("DataEngineName")
        memeber_set = set(params.keys())
        for name, value in vars(self).items():
            if name in memeber_set:
                memeber_set.remove(name)
        if len(memeber_set) > 0:
            warnings.warn("%s fileds are useless." % ",".join(memeber_set))
        


class DescribeTasksOverviewResponse(AbstractModel):
    """DescribeTasksOverview返回参数结构体

    """

    def __init__(self):
        r"""
        :param TasksOverview: 各类任务个数大于0
        :type TasksOverview: :class:`tencentcloud.dlc.v20210125.models.TasksOverview`
        :param RequestId: 唯一请求 ID，每次请求都会返回。定位问题时需要提供该次请求的 RequestId。
        :type RequestId: str
        """
        self.TasksOverview = None
        self.RequestId = None


    def _deserialize(self, params):
        if params.get("TasksOverview") is not None:
            self.TasksOverview = TasksOverview()
            self.TasksOverview._deserialize(params.get("TasksOverview"))
        self.RequestId = params.get("RequestId")


class DescribeTasksRequest(AbstractModel):
    """DescribeTasks请求参数结构体

    """

    def __init__(self):
        r"""
        :param Limit: 返回数量，默认为10，最大值为100。
        :type Limit: int
        :param Offset: 偏移量，默认为0。
        :type Offset: int
        :param Filters: 过滤条件，如下支持的过滤类型，传参Name应为以下其中一个,其中task-id支持最大50个过滤个数，其他过滤参数支持的总数不超过5个。
task-id - String - （任务ID准确过滤）task-id取值形如：e386471f-139a-4e59-877f-50ece8135b99。
task-state - String - （任务状态过滤）取值范围 0(初始化)， 1(运行中)， 2(成功)， -1(失败)。
task-sql-keyword - String - （SQL语句关键字模糊过滤）取值形如：DROP TABLE。
task-operator- string （子uin过滤）
task-kind - string （任务类型过滤）
        :type Filters: list of Filter
        :param SortBy: 排序字段，支持如下字段类型，create-time（创建时间，默认）、update-time（更新时间）
        :type SortBy: str
        :param Sorting: 排序方式，desc表示正序，asc表示反序， 默认为asc。
        :type Sorting: str
        :param StartTime: 起始时间点，格式为yyyy-mm-dd HH:MM:SS。默认为45天前的当前时刻
        :type StartTime: str
        :param EndTime: 结束时间点，格式为yyyy-mm-dd HH:MM:SS时间跨度在(0,30天]，支持最近45天数据查询。默认为当前时刻
        :type EndTime: str
        :param DataEngineName: 数据引擎名称，用于筛选
        :type DataEngineName: str
        :param Config: 配置信息，key-value数组，对外不可见。key1：AuthorityRole（鉴权角色，默认传SubUin，base64加密，仅在jdbc提交任务时使用）
        :type Config: list of KVPair
        :param NoNeedDataset: 是否不需要返回数据集，false:需要返回数据集，true:不需要返回数据集
        :type NoNeedDataset: bool
        """
        self.Limit = None
        self.Offset = None
        self.Filters = None
        self.SortBy = None
        self.Sorting = None
        self.StartTime = None
        self.EndTime = None
        self.DataEngineName = None
        self.Config = None
        self.NoNeedDataset = None


    def _deserialize(self, params):
        self.Limit = params.get("Limit")
        self.Offset = params.get("Offset")
        if params.get("Filters") is not None:
            self.Filters = []
            for item in params.get("Filters"):
                obj = Filter()
                obj._deserialize(item)
                self.Filters.append(obj)
        self.SortBy = params.get("SortBy")
        self.Sorting = params.get("Sorting")
        self.StartTime = params.get("StartTime")
        self.EndTime = params.get("EndTime")
        self.DataEngineName = params.get("DataEngineName")
        if params.get("Config") is not None:
            self.Config = []
            for item in params.get("Config"):
                obj = KVPair()
                obj._deserialize(item)
                self.Config.append(obj)
        self.NoNeedDataset = params.get("NoNeedDataset")
        memeber_set = set(params.keys())
        for name, value in vars(self).items():
            if name in memeber_set:
                memeber_set.remove(name)
        if len(memeber_set) > 0:
            warnings.warn("%s fileds are useless." % ",".join(memeber_set))
        


class DescribeTasksResponse(AbstractModel):
    """DescribeTasks返回参数结构体

    """

    def __init__(self):
        r"""
        :param TaskList: 任务对象列表。
        :type TaskList: list of TaskResponseInfo
        :param TotalCount: 实例总数。
        :type TotalCount: int
        :param TasksOverview: 任务概览信息
注意：此字段可能返回 null，表示取不到有效值。
        :type TasksOverview: :class:`tencentcloud.dlc.v20210125.models.TasksOverview`
        :param RequestId: 唯一请求 ID，每次请求都会返回。定位问题时需要提供该次请求的 RequestId。
        :type RequestId: str
        """
        self.TaskList = None
        self.TotalCount = None
        self.TasksOverview = None
        self.RequestId = None


    def _deserialize(self, params):
        if params.get("TaskList") is not None:
            self.TaskList = []
            for item in params.get("TaskList"):
                obj = TaskResponseInfo()
                obj._deserialize(item)
                self.TaskList.append(obj)
        self.TotalCount = params.get("TotalCount")
        if params.get("TasksOverview") is not None:
            self.TasksOverview = TasksOverview()
            self.TasksOverview._deserialize(params.get("TasksOverview"))
        self.RequestId = params.get("RequestId")


class DescribeUpdatableDataEnginesRequest(AbstractModel):
    """DescribeUpdatableDataEngines请求参数结构体

    """

    def __init__(self):
        r"""
        :param DataEngineConfigCommand: 引擎配置操作命令，UpdateSparkSQLLakefsPath 更新托管表路径，UpdateSparkSQLResultPath 更新结果桶路径
        :type DataEngineConfigCommand: str
        """
        self.DataEngineConfigCommand = None


    def _deserialize(self, params):
        self.DataEngineConfigCommand = params.get("DataEngineConfigCommand")
        memeber_set = set(params.keys())
        for name, value in vars(self).items():
            if name in memeber_set:
                memeber_set.remove(name)
        if len(memeber_set) > 0:
            warnings.warn("%s fileds are useless." % ",".join(memeber_set))
        


class DescribeUpdatableDataEnginesResponse(AbstractModel):
    """DescribeUpdatableDataEngines返回参数结构体

    """

    def __init__(self):
        r"""
        :param DataEngineBasicInfos: 集群基础信息
        :type DataEngineBasicInfos: list of DataEngineBasicInfo
        :param TotalCount: 集群个数
        :type TotalCount: int
        :param RequestId: 唯一请求 ID，每次请求都会返回。定位问题时需要提供该次请求的 RequestId。
        :type RequestId: str
        """
        self.DataEngineBasicInfos = None
        self.TotalCount = None
        self.RequestId = None


    def _deserialize(self, params):
        if params.get("DataEngineBasicInfos") is not None:
            self.DataEngineBasicInfos = []
            for item in params.get("DataEngineBasicInfos"):
                obj = DataEngineBasicInfo()
                obj._deserialize(item)
                self.DataEngineBasicInfos.append(obj)
        self.TotalCount = params.get("TotalCount")
        self.RequestId = params.get("RequestId")


class DescribeUserDataEngineConfigRequest(AbstractModel):
    """DescribeUserDataEngineConfig请求参数结构体

    """

    def __init__(self):
        r"""
        :param Sorting: 排序方式，desc表示正序，asc表示反序
        :type Sorting: str
        :param Limit: 返回数量，默认为10，最大值为100。
        :type Limit: int
        :param Offset: 偏移量，默认为0。
        :type Offset: int
        :param SortBy: 排序字段，支持如下字段类型，create-time
        :type SortBy: str
        :param Filters: 过滤条件，如下支持的过滤类型，传参Name应为以下其中一个,每种过滤参数支持的过滤值不超过5个。
app-id - String - （appid过滤）
engine-id - String - （引擎ID过滤）
        :type Filters: list of Filter
        """
        self.Sorting = None
        self.Limit = None
        self.Offset = None
        self.SortBy = None
        self.Filters = None


    def _deserialize(self, params):
        self.Sorting = params.get("Sorting")
        self.Limit = params.get("Limit")
        self.Offset = params.get("Offset")
        self.SortBy = params.get("SortBy")
        if params.get("Filters") is not None:
            self.Filters = []
            for item in params.get("Filters"):
                obj = Filter()
                obj._deserialize(item)
                self.Filters.append(obj)
        memeber_set = set(params.keys())
        for name, value in vars(self).items():
            if name in memeber_set:
                memeber_set.remove(name)
        if len(memeber_set) > 0:
            warnings.warn("%s fileds are useless." % ",".join(memeber_set))
        


class DescribeUserDataEngineConfigResponse(AbstractModel):
    """DescribeUserDataEngineConfig返回参数结构体

    """

    def __init__(self):
        r"""
        :param DataEngineConfigInstanceInfos: 用户引擎自定义配置项列表。
注意：此字段可能返回 null，表示取不到有效值。
        :type DataEngineConfigInstanceInfos: list of DataEngineConfigInstanceInfo
        :param TotalCount: 配置项总数。
        :type TotalCount: int
        :param RequestId: 唯一请求 ID，每次请求都会返回。定位问题时需要提供该次请求的 RequestId。
        :type RequestId: str
        """
        self.DataEngineConfigInstanceInfos = None
        self.TotalCount = None
        self.RequestId = None


    def _deserialize(self, params):
        if params.get("DataEngineConfigInstanceInfos") is not None:
            self.DataEngineConfigInstanceInfos = []
            for item in params.get("DataEngineConfigInstanceInfos"):
                obj = DataEngineConfigInstanceInfo()
                obj._deserialize(item)
                self.DataEngineConfigInstanceInfos.append(obj)
        self.TotalCount = params.get("TotalCount")
        self.RequestId = params.get("RequestId")


class DescribeUserInfoRequest(AbstractModel):
    """DescribeUserInfo请求参数结构体

    """

    def __init__(self):
        r"""
        :param UserId: 用户Id
        :type UserId: str
        :param Type: 查询的信息类型，Group：工作组 DataAuth：数据权限 EngineAuth:引擎权限 RowFilter：行级别权限
        :type Type: str
        :param Filters: 查询的过滤条件。

当Type为Group时，支持Key为workgroup-name的模糊搜索；

当Type为DataAuth时，支持key：

policy-type：权限类型。

policy-source：数据来源。

data-name：库表的模糊搜索。

当Type为EngineAuth时，支持key：

policy-type：权限类型。

policy-source：数据来源。

engine-name：库表的模糊搜索。
        :type Filters: list of Filter
        :param SortBy: 排序字段。

当Type为Group时，支持create-time、group-name

当Type为DataAuth时，支持create-time

当Type为EngineAuth时，支持create-time
        :type SortBy: str
        :param Sorting: 排序方式，desc表示正序，asc表示反序， 默认为asc
        :type Sorting: str
        :param Limit: 返回数量，默认20，最大值100
        :type Limit: int
        :param Offset: 偏移量，默认为0
        :type Offset: int
        """
        self.UserId = None
        self.Type = None
        self.Filters = None
        self.SortBy = None
        self.Sorting = None
        self.Limit = None
        self.Offset = None


    def _deserialize(self, params):
        self.UserId = params.get("UserId")
        self.Type = params.get("Type")
        if params.get("Filters") is not None:
            self.Filters = []
            for item in params.get("Filters"):
                obj = Filter()
                obj._deserialize(item)
                self.Filters.append(obj)
        self.SortBy = params.get("SortBy")
        self.Sorting = params.get("Sorting")
        self.Limit = params.get("Limit")
        self.Offset = params.get("Offset")
        memeber_set = set(params.keys())
        for name, value in vars(self).items():
            if name in memeber_set:
                memeber_set.remove(name)
        if len(memeber_set) > 0:
            warnings.warn("%s fileds are useless." % ",".join(memeber_set))
        


class DescribeUserInfoResponse(AbstractModel):
    """DescribeUserInfo返回参数结构体

    """

    def __init__(self):
        r"""
        :param UserInfo: 用户详细信息
注意：此字段可能返回 null，表示取不到有效值。
        :type UserInfo: :class:`tencentcloud.dlc.v20210125.models.UserDetailInfo`
        :param RequestId: 唯一请求 ID，每次请求都会返回。定位问题时需要提供该次请求的 RequestId。
        :type RequestId: str
        """
        self.UserInfo = None
        self.RequestId = None


    def _deserialize(self, params):
        if params.get("UserInfo") is not None:
            self.UserInfo = UserDetailInfo()
            self.UserInfo._deserialize(params.get("UserInfo"))
        self.RequestId = params.get("RequestId")


class DescribeUserRolesRequest(AbstractModel):
    """DescribeUserRoles请求参数结构体

    """

    def __init__(self):
        r"""
        :param Limit: 列举的数量限制
        :type Limit: int
        :param Offset: 列举的偏移位置
        :type Offset: int
        :param Fuzzy: 按照arn模糊列举
        :type Fuzzy: str
        """
        self.Limit = None
        self.Offset = None
        self.Fuzzy = None


    def _deserialize(self, params):
        self.Limit = params.get("Limit")
        self.Offset = params.get("Offset")
        self.Fuzzy = params.get("Fuzzy")
        memeber_set = set(params.keys())
        for name, value in vars(self).items():
            if name in memeber_set:
                memeber_set.remove(name)
        if len(memeber_set) > 0:
            warnings.warn("%s fileds are useless." % ",".join(memeber_set))
        


class DescribeUserRolesResponse(AbstractModel):
    """DescribeUserRoles返回参数结构体

    """

    def __init__(self):
        r"""
        :param Total: 符合列举条件的总数量
        :type Total: int
        :param UserRoles: 用户角色信息
        :type UserRoles: list of UserRole
        :param RequestId: 唯一请求 ID，每次请求都会返回。定位问题时需要提供该次请求的 RequestId。
        :type RequestId: str
        """
        self.Total = None
        self.UserRoles = None
        self.RequestId = None


    def _deserialize(self, params):
        self.Total = params.get("Total")
        if params.get("UserRoles") is not None:
            self.UserRoles = []
            for item in params.get("UserRoles"):
                obj = UserRole()
                obj._deserialize(item)
                self.UserRoles.append(obj)
        self.RequestId = params.get("RequestId")


class DescribeUserTypeRequest(AbstractModel):
    """DescribeUserType请求参数结构体

    """

    def __init__(self):
        r"""
        :param UserId: 用户ID（UIN），如果不填默认为调用方的子UIN
        :type UserId: str
        """
        self.UserId = None


    def _deserialize(self, params):
        self.UserId = params.get("UserId")
        memeber_set = set(params.keys())
        for name, value in vars(self).items():
            if name in memeber_set:
                memeber_set.remove(name)
        if len(memeber_set) > 0:
            warnings.warn("%s fileds are useless." % ",".join(memeber_set))
        


class DescribeUserTypeResponse(AbstractModel):
    """DescribeUserType返回参数结构体

    """

    def __init__(self):
        r"""
        :param UserType: 用户类型。ADMIN：管理员 COMMON：普通用户
注意：此字段可能返回 null，表示取不到有效值。
        :type UserType: str
        :param RequestId: 唯一请求 ID，每次请求都会返回。定位问题时需要提供该次请求的 RequestId。
        :type RequestId: str
        """
        self.UserType = None
        self.RequestId = None


    def _deserialize(self, params):
        self.UserType = params.get("UserType")
        self.RequestId = params.get("RequestId")


class DescribeUserUseSceneRequest(AbstractModel):
    """DescribeUserUseScene请求参数结构体

    """


class DescribeUserUseSceneResponse(AbstractModel):
    """DescribeUserUseScene返回参数结构体

    """

    def __init__(self):
        r"""
        :param UseScene: 使用场景，1:数据应用开发，2:企业数据平台搭建
        :type UseScene: int
        :param NeedGuide: 是否需要指导,false:不需要，true需要
        :type NeedGuide: bool
        :param RequestId: 唯一请求 ID，每次请求都会返回。定位问题时需要提供该次请求的 RequestId。
        :type RequestId: str
        """
        self.UseScene = None
        self.NeedGuide = None
        self.RequestId = None


    def _deserialize(self, params):
        self.UseScene = params.get("UseScene")
        self.NeedGuide = params.get("NeedGuide")
        self.RequestId = params.get("RequestId")


class DescribeUsersRequest(AbstractModel):
    """DescribeUsers请求参数结构体

    """

    def __init__(self):
        r"""
        :param UserId: 指定查询的子用户uin，用户需要通过CreateUser接口创建。
        :type UserId: str
        :param Offset: 偏移量，默认为0
        :type Offset: int
        :param Limit: 返回数量，默认20，最大值100
        :type Limit: int
        :param SortBy: 排序字段，支持如下字段类型，create-time
        :type SortBy: str
        :param Sorting: 排序方式，desc表示正序，asc表示反序， 默认为asc
        :type Sorting: str
        :param Filters: 过滤条件，支持如下字段类型，user-type：根据用户类型过滤。user-keyword：根据用户名称过滤
        :type Filters: list of Filter
        """
        self.UserId = None
        self.Offset = None
        self.Limit = None
        self.SortBy = None
        self.Sorting = None
        self.Filters = None


    def _deserialize(self, params):
        self.UserId = params.get("UserId")
        self.Offset = params.get("Offset")
        self.Limit = params.get("Limit")
        self.SortBy = params.get("SortBy")
        self.Sorting = params.get("Sorting")
        if params.get("Filters") is not None:
            self.Filters = []
            for item in params.get("Filters"):
                obj = Filter()
                obj._deserialize(item)
                self.Filters.append(obj)
        memeber_set = set(params.keys())
        for name, value in vars(self).items():
            if name in memeber_set:
                memeber_set.remove(name)
        if len(memeber_set) > 0:
            warnings.warn("%s fileds are useless." % ",".join(memeber_set))
        


class DescribeUsersResponse(AbstractModel):
    """DescribeUsers返回参数结构体

    """

    def __init__(self):
        r"""
        :param TotalCount: 查询到的用户总数
        :type TotalCount: int
        :param UserSet: 查询到的授权用户信息集合
        :type UserSet: list of UserInfo
        :param RequestId: 唯一请求 ID，每次请求都会返回。定位问题时需要提供该次请求的 RequestId。
        :type RequestId: str
        """
        self.TotalCount = None
        self.UserSet = None
        self.RequestId = None


    def _deserialize(self, params):
        self.TotalCount = params.get("TotalCount")
        if params.get("UserSet") is not None:
            self.UserSet = []
            for item in params.get("UserSet"):
                obj = UserInfo()
                obj._deserialize(item)
                self.UserSet.append(obj)
        self.RequestId = params.get("RequestId")


class DescribeViewRequest(AbstractModel):
    """DescribeView请求参数结构体

    """

    def __init__(self):
        r"""
        :param DatabaseName: 数据库名称
        :type DatabaseName: str
        :param ViewName: 视图名称
        :type ViewName: str
        :param DatasourceConnectionName: 数据连接名称
        :type DatasourceConnectionName: str
        """
        self.DatabaseName = None
        self.ViewName = None
        self.DatasourceConnectionName = None


    def _deserialize(self, params):
        self.DatabaseName = params.get("DatabaseName")
        self.ViewName = params.get("ViewName")
        self.DatasourceConnectionName = params.get("DatasourceConnectionName")
        memeber_set = set(params.keys())
        for name, value in vars(self).items():
            if name in memeber_set:
                memeber_set.remove(name)
        if len(memeber_set) > 0:
            warnings.warn("%s fileds are useless." % ",".join(memeber_set))
        


class DescribeViewResponse(AbstractModel):
    """DescribeView返回参数结构体

    """

    def __init__(self):
        r"""
        :param View: 视图的详细信息
        :type View: :class:`tencentcloud.dlc.v20210125.models.ViewResponseInfo`
        :param RequestId: 唯一请求 ID，每次请求都会返回。定位问题时需要提供该次请求的 RequestId。
        :type RequestId: str
        """
        self.View = None
        self.RequestId = None


    def _deserialize(self, params):
        if params.get("View") is not None:
            self.View = ViewResponseInfo()
            self.View._deserialize(params.get("View"))
        self.RequestId = params.get("RequestId")


class DescribeViewsRequest(AbstractModel):
    """DescribeViews请求参数结构体

    """

    def __init__(self):
        r"""
        :param DatabaseName: 列出该数据库下所属数据表。
        :type DatabaseName: str
        :param Limit: 返回数量，默认为10，最大值为100。
        :type Limit: int
        :param Offset: 数据偏移量，从0开始，默认为0。
        :type Offset: int
        :param Filters: 过滤条件，如下支持的过滤类型，传参Name应为其一
view-name - String - （过滤条件）数据表名称,形如：view-001。
view-id - String - （过滤条件）view id形如：12342。
        :type Filters: list of Filter
        :param DatasourceConnectionName: 数据库所属的数据源名称
        :type DatasourceConnectionName: str
        :param Sort: 排序字段
        :type Sort: str
        :param Asc: 排序规则，true:升序；false:降序
        :type Asc: bool
        :param StartTime: 按视图更新时间筛选，开始时间，如2021-11-11 00:00:00
        :type StartTime: str
        :param EndTime: 按视图更新时间筛选，结束时间，如2021-11-12 00:00:00
        :type EndTime: str
        """
        self.DatabaseName = None
        self.Limit = None
        self.Offset = None
        self.Filters = None
        self.DatasourceConnectionName = None
        self.Sort = None
        self.Asc = None
        self.StartTime = None
        self.EndTime = None


    def _deserialize(self, params):
        self.DatabaseName = params.get("DatabaseName")
        self.Limit = params.get("Limit")
        self.Offset = params.get("Offset")
        if params.get("Filters") is not None:
            self.Filters = []
            for item in params.get("Filters"):
                obj = Filter()
                obj._deserialize(item)
                self.Filters.append(obj)
        self.DatasourceConnectionName = params.get("DatasourceConnectionName")
        self.Sort = params.get("Sort")
        self.Asc = params.get("Asc")
        self.StartTime = params.get("StartTime")
        self.EndTime = params.get("EndTime")
        memeber_set = set(params.keys())
        for name, value in vars(self).items():
            if name in memeber_set:
                memeber_set.remove(name)
        if len(memeber_set) > 0:
            warnings.warn("%s fileds are useless." % ",".join(memeber_set))
        


class DescribeViewsResponse(AbstractModel):
    """DescribeViews返回参数结构体

    """

    def __init__(self):
        r"""
        :param ViewList: 视图对象列表。
        :type ViewList: list of ViewResponseInfo
        :param TotalCount: 实例总数。
        :type TotalCount: int
        :param RequestId: 唯一请求 ID，每次请求都会返回。定位问题时需要提供该次请求的 RequestId。
        :type RequestId: str
        """
        self.ViewList = None
        self.TotalCount = None
        self.RequestId = None


    def _deserialize(self, params):
        if params.get("ViewList") is not None:
            self.ViewList = []
            for item in params.get("ViewList"):
                obj = ViewResponseInfo()
                obj._deserialize(item)
                self.ViewList.append(obj)
        self.TotalCount = params.get("TotalCount")
        self.RequestId = params.get("RequestId")


class DescribeWhitelistRequest(AbstractModel):
    """DescribeWhitelist请求参数结构体

    """

    def __init__(self):
        r"""
        :param WhiteListKey: 白名单key值
        :type WhiteListKey: str
        :param WhiteListValue: 白名单value值
        :type WhiteListValue: str
        :param WhiteListKeyList: 白名单多个key值
        :type WhiteListKeyList: list of str
        """
        self.WhiteListKey = None
        self.WhiteListValue = None
        self.WhiteListKeyList = None


    def _deserialize(self, params):
        self.WhiteListKey = params.get("WhiteListKey")
        self.WhiteListValue = params.get("WhiteListValue")
        self.WhiteListKeyList = params.get("WhiteListKeyList")
        memeber_set = set(params.keys())
        for name, value in vars(self).items():
            if name in memeber_set:
                memeber_set.remove(name)
        if len(memeber_set) > 0:
            warnings.warn("%s fileds are useless." % ",".join(memeber_set))
        


class DescribeWhitelistResponse(AbstractModel):
    """DescribeWhitelist返回参数结构体

    """

    def __init__(self):
        r"""
        :param WhiteListResult: 如返回“1”表示在白名单内，否则不在
注意：此字段可能返回 null，表示取不到有效值。
        :type WhiteListResult: str
        :param WhiteListResultList: 按照key传入顺序返回对应的值，如返回“1”表示在白名单内，否则不在
注意：此字段可能返回 null，表示取不到有效值。
        :type WhiteListResultList: list of str
        :param RequestId: 唯一请求 ID，每次请求都会返回。定位问题时需要提供该次请求的 RequestId。
        :type RequestId: str
        """
        self.WhiteListResult = None
        self.WhiteListResultList = None
        self.RequestId = None


    def _deserialize(self, params):
        self.WhiteListResult = params.get("WhiteListResult")
        self.WhiteListResultList = params.get("WhiteListResultList")
        self.RequestId = params.get("RequestId")


class DescribeWorkGroupInfoRequest(AbstractModel):
    """DescribeWorkGroupInfo请求参数结构体

    """

    def __init__(self):
        r"""
        :param WorkGroupId: 工作组Id
        :type WorkGroupId: int
        :param Type: 查询信息类型：User：用户信息 DataAuth：数据权限 EngineAuth：引擎权限
        :type Type: str
        :param Filters: 查询的过滤条件。

当Type为User时，支持Key为user-name的模糊搜索；

当Type为DataAuth时，支持key：

policy-type：权限类型。

policy-source：数据来源。

data-name：库表的模糊搜索。

当Type为EngineAuth时，支持key：

policy-type：权限类型。

policy-source：数据来源。

engine-name：库表的模糊搜索。
        :type Filters: list of Filter
        :param SortBy: 排序字段。

当Type为User时，支持create-time、user-name

当Type为DataAuth时，支持create-time

当Type为EngineAuth时，支持create-time
        :type SortBy: str
        :param Sorting: 排序方式，desc表示正序，asc表示反序， 默认为asc
        :type Sorting: str
        :param Limit: 返回数量，默认20，最大值100
        :type Limit: int
        :param Offset: 偏移量，默认为0
        :type Offset: int
        """
        self.WorkGroupId = None
        self.Type = None
        self.Filters = None
        self.SortBy = None
        self.Sorting = None
        self.Limit = None
        self.Offset = None


    def _deserialize(self, params):
        self.WorkGroupId = params.get("WorkGroupId")
        self.Type = params.get("Type")
        if params.get("Filters") is not None:
            self.Filters = []
            for item in params.get("Filters"):
                obj = Filter()
                obj._deserialize(item)
                self.Filters.append(obj)
        self.SortBy = params.get("SortBy")
        self.Sorting = params.get("Sorting")
        self.Limit = params.get("Limit")
        self.Offset = params.get("Offset")
        memeber_set = set(params.keys())
        for name, value in vars(self).items():
            if name in memeber_set:
                memeber_set.remove(name)
        if len(memeber_set) > 0:
            warnings.warn("%s fileds are useless." % ",".join(memeber_set))
        


class DescribeWorkGroupInfoResponse(AbstractModel):
    """DescribeWorkGroupInfo返回参数结构体

    """

    def __init__(self):
        r"""
        :param WorkGroupInfo: 工作组详细信息
注意：此字段可能返回 null，表示取不到有效值。
        :type WorkGroupInfo: :class:`tencentcloud.dlc.v20210125.models.WorkGroupDetailInfo`
        :param RequestId: 唯一请求 ID，每次请求都会返回。定位问题时需要提供该次请求的 RequestId。
        :type RequestId: str
        """
        self.WorkGroupInfo = None
        self.RequestId = None


    def _deserialize(self, params):
        if params.get("WorkGroupInfo") is not None:
            self.WorkGroupInfo = WorkGroupDetailInfo()
            self.WorkGroupInfo._deserialize(params.get("WorkGroupInfo"))
        self.RequestId = params.get("RequestId")


class DescribeWorkGroupsRequest(AbstractModel):
    """DescribeWorkGroups请求参数结构体

    """

    def __init__(self):
        r"""
        :param WorkGroupId: 查询的工作组Id，不填或填0表示不过滤。
        :type WorkGroupId: int
        :param Filters: 过滤条件，当前仅支持按照工作组名称进行模糊搜索。Key为workgroup-name
        :type Filters: list of Filter
        :param Offset: 偏移量，默认为0
        :type Offset: int
        :param Limit: 返回数量，默认20，最大值100
        :type Limit: int
        :param SortBy: 排序字段，支持如下字段类型，create-time
        :type SortBy: str
        :param Sorting: 排序方式，desc表示正序，asc表示反序， 默认为asc
        :type Sorting: str
        """
        self.WorkGroupId = None
        self.Filters = None
        self.Offset = None
        self.Limit = None
        self.SortBy = None
        self.Sorting = None


    def _deserialize(self, params):
        self.WorkGroupId = params.get("WorkGroupId")
        if params.get("Filters") is not None:
            self.Filters = []
            for item in params.get("Filters"):
                obj = Filter()
                obj._deserialize(item)
                self.Filters.append(obj)
        self.Offset = params.get("Offset")
        self.Limit = params.get("Limit")
        self.SortBy = params.get("SortBy")
        self.Sorting = params.get("Sorting")
        memeber_set = set(params.keys())
        for name, value in vars(self).items():
            if name in memeber_set:
                memeber_set.remove(name)
        if len(memeber_set) > 0:
            warnings.warn("%s fileds are useless." % ",".join(memeber_set))
        


class DescribeWorkGroupsResponse(AbstractModel):
    """DescribeWorkGroups返回参数结构体

    """

    def __init__(self):
        r"""
        :param TotalCount: 工作组总数
        :type TotalCount: int
        :param WorkGroupSet: 工作组信息集合
        :type WorkGroupSet: list of WorkGroupInfo
        :param RequestId: 唯一请求 ID，每次请求都会返回。定位问题时需要提供该次请求的 RequestId。
        :type RequestId: str
        """
        self.TotalCount = None
        self.WorkGroupSet = None
        self.RequestId = None


    def _deserialize(self, params):
        self.TotalCount = params.get("TotalCount")
        if params.get("WorkGroupSet") is not None:
            self.WorkGroupSet = []
            for item in params.get("WorkGroupSet"):
                obj = WorkGroupInfo()
                obj._deserialize(item)
                self.WorkGroupSet.append(obj)
        self.RequestId = params.get("RequestId")


class DescribeWorkloadStatRequest(AbstractModel):
    """DescribeWorkloadStat请求参数结构体

    """

    def __init__(self):
        r"""
        :param DataEngineId: 数据引擎Id
        :type DataEngineId: str
        :param StatType: 统计类型：5min,hour,day
        :type StatType: str
        :param StartTime: 查询统计信息的开始时间，yyyy-MM-dd HH:mm:ss
        :type StartTime: str
        :param EndTime: 查询统计信息的结束时间，yyyy-MM-dd HH:mm:ss
        :type EndTime: str
        """
        self.DataEngineId = None
        self.StatType = None
        self.StartTime = None
        self.EndTime = None


    def _deserialize(self, params):
        self.DataEngineId = params.get("DataEngineId")
        self.StatType = params.get("StatType")
        self.StartTime = params.get("StartTime")
        self.EndTime = params.get("EndTime")
        memeber_set = set(params.keys())
        for name, value in vars(self).items():
            if name in memeber_set:
                memeber_set.remove(name)
        if len(memeber_set) > 0:
            warnings.warn("%s fileds are useless." % ",".join(memeber_set))
        


class DescribeWorkloadStatResponse(AbstractModel):
    """DescribeWorkloadStat返回参数结构体

    """

    def __init__(self):
        r"""
        :param WorkloadStats: 统计信息
        :type WorkloadStats: list of WorkloadStat
        :param RequestId: 唯一请求 ID，每次请求都会返回。定位问题时需要提供该次请求的 RequestId。
        :type RequestId: str
        """
        self.WorkloadStats = None
        self.RequestId = None


    def _deserialize(self, params):
        if params.get("WorkloadStats") is not None:
            self.WorkloadStats = []
            for item in params.get("WorkloadStats"):
                obj = WorkloadStat()
                obj._deserialize(item)
                self.WorkloadStats.append(obj)
        self.RequestId = params.get("RequestId")


class DescribeYuntiUserRequest(AbstractModel):
    """DescribeYuntiUser请求参数结构体

    """


class DescribeYuntiUserResponse(AbstractModel):
    """DescribeYuntiUser返回参数结构体

    """

    def __init__(self):
        r"""
        :param YuntiUser: 用户是否是云梯账号
        :type YuntiUser: bool
        :param RequestId: 唯一请求 ID，每次请求都会返回。定位问题时需要提供该次请求的 RequestId。
        :type RequestId: str
        """
        self.YuntiUser = None
        self.RequestId = None


    def _deserialize(self, params):
        self.YuntiUser = params.get("YuntiUser")
        self.RequestId = params.get("RequestId")


class DetachUserPolicyRequest(AbstractModel):
    """DetachUserPolicy请求参数结构体

    """

    def __init__(self):
        r"""
        :param UserId: 用户Id，和CAM侧Uin匹配
        :type UserId: str
        :param PolicySet: 解绑的权限集合
        :type PolicySet: list of Policy
        """
        self.UserId = None
        self.PolicySet = None


    def _deserialize(self, params):
        self.UserId = params.get("UserId")
        if params.get("PolicySet") is not None:
            self.PolicySet = []
            for item in params.get("PolicySet"):
                obj = Policy()
                obj._deserialize(item)
                self.PolicySet.append(obj)
        memeber_set = set(params.keys())
        for name, value in vars(self).items():
            if name in memeber_set:
                memeber_set.remove(name)
        if len(memeber_set) > 0:
            warnings.warn("%s fileds are useless." % ",".join(memeber_set))
        


class DetachUserPolicyResponse(AbstractModel):
    """DetachUserPolicy返回参数结构体

    """

    def __init__(self):
        r"""
        :param RequestId: 唯一请求 ID，每次请求都会返回。定位问题时需要提供该次请求的 RequestId。
        :type RequestId: str
        """
        self.RequestId = None


    def _deserialize(self, params):
        self.RequestId = params.get("RequestId")


class DetachWorkGroupPolicyRequest(AbstractModel):
    """DetachWorkGroupPolicy请求参数结构体

    """

    def __init__(self):
        r"""
        :param WorkGroupId: 工作组Id
        :type WorkGroupId: int
        :param PolicySet: 解绑的权限集合
        :type PolicySet: list of Policy
        """
        self.WorkGroupId = None
        self.PolicySet = None


    def _deserialize(self, params):
        self.WorkGroupId = params.get("WorkGroupId")
        if params.get("PolicySet") is not None:
            self.PolicySet = []
            for item in params.get("PolicySet"):
                obj = Policy()
                obj._deserialize(item)
                self.PolicySet.append(obj)
        memeber_set = set(params.keys())
        for name, value in vars(self).items():
            if name in memeber_set:
                memeber_set.remove(name)
        if len(memeber_set) > 0:
            warnings.warn("%s fileds are useless." % ",".join(memeber_set))
        


class DetachWorkGroupPolicyResponse(AbstractModel):
    """DetachWorkGroupPolicy返回参数结构体

    """

    def __init__(self):
        r"""
        :param RequestId: 唯一请求 ID，每次请求都会返回。定位问题时需要提供该次请求的 RequestId。
        :type RequestId: str
        """
        self.RequestId = None


    def _deserialize(self, params):
        self.RequestId = params.get("RequestId")


class DisassociateCHDFSAccessGroupsRequest(AbstractModel):
    """DisassociateCHDFSAccessGroups请求参数结构体

    """

    def __init__(self):
        r"""
        :param MountPointAssociateInfos: 挂载点绑定信息
        :type MountPointAssociateInfos: list of MountPointAssociateInfo
        """
        self.MountPointAssociateInfos = None


    def _deserialize(self, params):
        if params.get("MountPointAssociateInfos") is not None:
            self.MountPointAssociateInfos = []
            for item in params.get("MountPointAssociateInfos"):
                obj = MountPointAssociateInfo()
                obj._deserialize(item)
                self.MountPointAssociateInfos.append(obj)
        memeber_set = set(params.keys())
        for name, value in vars(self).items():
            if name in memeber_set:
                memeber_set.remove(name)
        if len(memeber_set) > 0:
            warnings.warn("%s fileds are useless." % ",".join(memeber_set))
        


class DisassociateCHDFSAccessGroupsResponse(AbstractModel):
    """DisassociateCHDFSAccessGroups返回参数结构体

    """

    def __init__(self):
        r"""
        :param Result: 解绑结果
        :type Result: bool
        :param RequestId: 唯一请求 ID，每次请求都会返回。定位问题时需要提供该次请求的 RequestId。
        :type RequestId: str
        """
        self.Result = None
        self.RequestId = None


    def _deserialize(self, params):
        self.Result = params.get("Result")
        self.RequestId = params.get("RequestId")


class DownloadResultRequest(AbstractModel):
    """DownloadResult请求参数结构体

    """

    def __init__(self):
        r"""
        :param DataPath: SQL查询结果存放的路径，目前只支持托管的查询结果导出，即Path是lakefs协议的路径
        :type DataPath: str
        """
        self.DataPath = None


    def _deserialize(self, params):
        self.DataPath = params.get("DataPath")
        memeber_set = set(params.keys())
        for name, value in vars(self).items():
            if name in memeber_set:
                memeber_set.remove(name)
        if len(memeber_set) > 0:
            warnings.warn("%s fileds are useless." % ",".join(memeber_set))
        


class DownloadResultResponse(AbstractModel):
    """DownloadResult返回参数结构体

    """

    def __init__(self):
        r"""
        :param Fs: 托管存储对象
        :type Fs: :class:`tencentcloud.dlc.v20210125.models.LakeFileSystem`
        :param RequestId: 唯一请求 ID，每次请求都会返回。定位问题时需要提供该次请求的 RequestId。
        :type RequestId: str
        """
        self.Fs = None
        self.RequestId = None


    def _deserialize(self, params):
        if params.get("Fs") is not None:
            self.Fs = LakeFileSystem()
            self.Fs._deserialize(params.get("Fs"))
        self.RequestId = params.get("RequestId")


class DownloadSparkTaskLogRequest(AbstractModel):
    """DownloadSparkTaskLog请求参数结构体

    """

    def __init__(self):
        r"""
        :param TaskId: 任务ID
        :type TaskId: str
        :param Filters: 下载日志的通用过滤条件
        :type Filters: list of Filter
        """
        self.TaskId = None
        self.Filters = None


    def _deserialize(self, params):
        self.TaskId = params.get("TaskId")
        if params.get("Filters") is not None:
            self.Filters = []
            for item in params.get("Filters"):
                obj = Filter()
                obj._deserialize(item)
                self.Filters.append(obj)
        memeber_set = set(params.keys())
        for name, value in vars(self).items():
            if name in memeber_set:
                memeber_set.remove(name)
        if len(memeber_set) > 0:
            warnings.warn("%s fileds are useless." % ",".join(memeber_set))
        


class DownloadSparkTaskLogResponse(AbstractModel):
    """DownloadSparkTaskLog返回参数结构体

    """

    def __init__(self):
        r"""
        :param DownloadId: 下载ID
        :type DownloadId: str
        :param RequestId: 唯一请求 ID，每次请求都会返回。定位问题时需要提供该次请求的 RequestId。
        :type RequestId: str
        """
        self.DownloadId = None
        self.RequestId = None


    def _deserialize(self, params):
        self.DownloadId = params.get("DownloadId")
        self.RequestId = params.get("RequestId")


class DropDMSDatabaseRequest(AbstractModel):
    """DropDMSDatabase请求参数结构体

    """

    def __init__(self):
        r"""
        :param Name: 数据库名称
        :type Name: str
        :param DeleteData: 是否删除数据
        :type DeleteData: bool
        :param Cascade: 是否级联删除
        :type Cascade: bool
        """
        self.Name = None
        self.DeleteData = None
        self.Cascade = None


    def _deserialize(self, params):
        self.Name = params.get("Name")
        self.DeleteData = params.get("DeleteData")
        self.Cascade = params.get("Cascade")
        memeber_set = set(params.keys())
        for name, value in vars(self).items():
            if name in memeber_set:
                memeber_set.remove(name)
        if len(memeber_set) > 0:
            warnings.warn("%s fileds are useless." % ",".join(memeber_set))
        


class DropDMSDatabaseResponse(AbstractModel):
    """DropDMSDatabase返回参数结构体

    """

    def __init__(self):
        r"""
        :param RequestId: 唯一请求 ID，每次请求都会返回。定位问题时需要提供该次请求的 RequestId。
        :type RequestId: str
        """
        self.RequestId = None


    def _deserialize(self, params):
        self.RequestId = params.get("RequestId")


class DropDMSPartitionColumnStatisticRequest(AbstractModel):
    """DropDMSPartitionColumnStatistic请求参数结构体

    """

    def __init__(self):
        r"""
        :param DatabaseName: 数据库名
        :type DatabaseName: str
        :param TableName: 表名称
        :type TableName: str
        :param PartitionName: 分区名
        :type PartitionName: str
        :param ColumnName: 字段名
        :type ColumnName: str
        """
        self.DatabaseName = None
        self.TableName = None
        self.PartitionName = None
        self.ColumnName = None


    def _deserialize(self, params):
        self.DatabaseName = params.get("DatabaseName")
        self.TableName = params.get("TableName")
        self.PartitionName = params.get("PartitionName")
        self.ColumnName = params.get("ColumnName")
        memeber_set = set(params.keys())
        for name, value in vars(self).items():
            if name in memeber_set:
                memeber_set.remove(name)
        if len(memeber_set) > 0:
            warnings.warn("%s fileds are useless." % ",".join(memeber_set))
        


class DropDMSPartitionColumnStatisticResponse(AbstractModel):
    """DropDMSPartitionColumnStatistic返回参数结构体

    """

    def __init__(self):
        r"""
        :param Status: 状态
        :type Status: bool
        :param RequestId: 唯一请求 ID，每次请求都会返回。定位问题时需要提供该次请求的 RequestId。
        :type RequestId: str
        """
        self.Status = None
        self.RequestId = None


    def _deserialize(self, params):
        self.Status = params.get("Status")
        self.RequestId = params.get("RequestId")


class DropDMSPartitionsRequest(AbstractModel):
    """DropDMSPartitions请求参数结构体

    """

    def __init__(self):
        r"""
        :param DatabaseName: 数据库名称
        :type DatabaseName: str
        :param SchemaName: 数据库Schema名称
        :type SchemaName: str
        :param TableName: 数据表名称
        :type TableName: str
        :param Name: 分区名称
        :type Name: str
        :param Values: 单个分区名称
        :type Values: list of str
        :param DeleteData: 是否删除分区数据
        :type DeleteData: bool
        """
        self.DatabaseName = None
        self.SchemaName = None
        self.TableName = None
        self.Name = None
        self.Values = None
        self.DeleteData = None


    def _deserialize(self, params):
        self.DatabaseName = params.get("DatabaseName")
        self.SchemaName = params.get("SchemaName")
        self.TableName = params.get("TableName")
        self.Name = params.get("Name")
        self.Values = params.get("Values")
        self.DeleteData = params.get("DeleteData")
        memeber_set = set(params.keys())
        for name, value in vars(self).items():
            if name in memeber_set:
                memeber_set.remove(name)
        if len(memeber_set) > 0:
            warnings.warn("%s fileds are useless." % ",".join(memeber_set))
        


class DropDMSPartitionsResponse(AbstractModel):
    """DropDMSPartitions返回参数结构体

    """

    def __init__(self):
        r"""
        :param Status: 状态
        :type Status: bool
        :param RequestId: 唯一请求 ID，每次请求都会返回。定位问题时需要提供该次请求的 RequestId。
        :type RequestId: str
        """
        self.Status = None
        self.RequestId = None


    def _deserialize(self, params):
        self.Status = params.get("Status")
        self.RequestId = params.get("RequestId")


class DropDMSTableColumnStatisticRequest(AbstractModel):
    """DropDMSTableColumnStatistic请求参数结构体

    """

    def __init__(self):
        r"""
        :param DatabaseName: 数据库名
        :type DatabaseName: str
        :param TableName: 表名称
        :type TableName: str
        :param ColumnName: 字段名
        :type ColumnName: str
        """
        self.DatabaseName = None
        self.TableName = None
        self.ColumnName = None


    def _deserialize(self, params):
        self.DatabaseName = params.get("DatabaseName")
        self.TableName = params.get("TableName")
        self.ColumnName = params.get("ColumnName")
        memeber_set = set(params.keys())
        for name, value in vars(self).items():
            if name in memeber_set:
                memeber_set.remove(name)
        if len(memeber_set) > 0:
            warnings.warn("%s fileds are useless." % ",".join(memeber_set))
        


class DropDMSTableColumnStatisticResponse(AbstractModel):
    """DropDMSTableColumnStatistic返回参数结构体

    """

    def __init__(self):
        r"""
        :param Status: 状态
        :type Status: bool
        :param RequestId: 唯一请求 ID，每次请求都会返回。定位问题时需要提供该次请求的 RequestId。
        :type RequestId: str
        """
        self.Status = None
        self.RequestId = None


    def _deserialize(self, params):
        self.Status = params.get("Status")
        self.RequestId = params.get("RequestId")


class DropDMSTableRequest(AbstractModel):
    """DropDMSTable请求参数结构体

    """

    def __init__(self):
        r"""
        :param DbName: 数据库名称
        :type DbName: str
        :param Name: 表名称
        :type Name: str
        :param DeleteData: 是否删除数据
        :type DeleteData: bool
        :param EnvProps: 环境属性
        :type EnvProps: :class:`tencentcloud.dlc.v20210125.models.KVPair`
        """
        self.DbName = None
        self.Name = None
        self.DeleteData = None
        self.EnvProps = None


    def _deserialize(self, params):
        self.DbName = params.get("DbName")
        self.Name = params.get("Name")
        self.DeleteData = params.get("DeleteData")
        if params.get("EnvProps") is not None:
            self.EnvProps = KVPair()
            self.EnvProps._deserialize(params.get("EnvProps"))
        memeber_set = set(params.keys())
        for name, value in vars(self).items():
            if name in memeber_set:
                memeber_set.remove(name)
        if len(memeber_set) > 0:
            warnings.warn("%s fileds are useless." % ",".join(memeber_set))
        


class DropDMSTableResponse(AbstractModel):
    """DropDMSTable返回参数结构体

    """

    def __init__(self):
        r"""
        :param RequestId: 唯一请求 ID，每次请求都会返回。定位问题时需要提供该次请求的 RequestId。
        :type RequestId: str
        """
        self.RequestId = None


    def _deserialize(self, params):
        self.RequestId = params.get("RequestId")


class ElasticsearchInfo(AbstractModel):
    """Elasticsearch数据源的详细信息

    """

    def __init__(self):
        r"""
        :param InstanceId: 数据源ID
注意：此字段可能返回 null，表示取不到有效值。
        :type InstanceId: str
        :param InstanceName: 数据源名称
注意：此字段可能返回 null，表示取不到有效值。
        :type InstanceName: str
        :param User: 用户名
注意：此字段可能返回 null，表示取不到有效值。
        :type User: str
        :param Password: 密码，需要base64编码
注意：此字段可能返回 null，表示取不到有效值。
        :type Password: str
        :param Location: 数据源的VPC和子网信息
注意：此字段可能返回 null，表示取不到有效值。
        :type Location: :class:`tencentcloud.dlc.v20210125.models.DatasourceConnectionLocation`
        :param DbName: 默认数据库名称
注意：此字段可能返回 null，表示取不到有效值。
        :type DbName: str
        :param ServiceInfo: 访问Elasticsearch的ip、端口信息
注意：此字段可能返回 null，表示取不到有效值。
        :type ServiceInfo: list of IpPortPair
        """
        self.InstanceId = None
        self.InstanceName = None
        self.User = None
        self.Password = None
        self.Location = None
        self.DbName = None
        self.ServiceInfo = None


    def _deserialize(self, params):
        self.InstanceId = params.get("InstanceId")
        self.InstanceName = params.get("InstanceName")
        self.User = params.get("User")
        self.Password = params.get("Password")
        if params.get("Location") is not None:
            self.Location = DatasourceConnectionLocation()
            self.Location._deserialize(params.get("Location"))
        self.DbName = params.get("DbName")
        if params.get("ServiceInfo") is not None:
            self.ServiceInfo = []
            for item in params.get("ServiceInfo"):
                obj = IpPortPair()
                obj._deserialize(item)
                self.ServiceInfo.append(obj)
        memeber_set = set(params.keys())
        for name, value in vars(self).items():
            if name in memeber_set:
                memeber_set.remove(name)
        if len(memeber_set) > 0:
            warnings.warn("%s fileds are useless." % ",".join(memeber_set))
        


class EngineParameter(AbstractModel):
    """引擎参数。

    """

    def __init__(self):
        r"""
        :param KeyName: 参数key
        :type KeyName: str
        :param KeyDescription: Key描述信息
注意：此字段可能返回 null，表示取不到有效值。
        :type KeyDescription: str
        :param ValueType: value类型
        :type ValueType: str
        :param ValueLengthLimit: value长度限制
注意：此字段可能返回 null，表示取不到有效值。
        :type ValueLengthLimit: str
        :param ValueRegexpLimit: value正则限制
注意：此字段可能返回 null，表示取不到有效值。
        :type ValueRegexpLimit: str
        :param ValueDefault: value默认值
注意：此字段可能返回 null，表示取不到有效值。
        :type ValueDefault: str
        """
        self.KeyName = None
        self.KeyDescription = None
        self.ValueType = None
        self.ValueLengthLimit = None
        self.ValueRegexpLimit = None
        self.ValueDefault = None


    def _deserialize(self, params):
        self.KeyName = params.get("KeyName")
        self.KeyDescription = params.get("KeyDescription")
        self.ValueType = params.get("ValueType")
        self.ValueLengthLimit = params.get("ValueLengthLimit")
        self.ValueRegexpLimit = params.get("ValueRegexpLimit")
        self.ValueDefault = params.get("ValueDefault")
        memeber_set = set(params.keys())
        for name, value in vars(self).items():
            if name in memeber_set:
                memeber_set.remove(name)
        if len(memeber_set) > 0:
            warnings.warn("%s fileds are useless." % ",".join(memeber_set))
        


class Execution(AbstractModel):
    """SQL语句对象

    """

    def __init__(self):
        r"""
        :param SQL: 自动生成SQL语句。
        :type SQL: str
        """
        self.SQL = None


    def _deserialize(self, params):
        self.SQL = params.get("SQL")
        memeber_set = set(params.keys())
        for name, value in vars(self).items():
            if name in memeber_set:
                memeber_set.remove(name)
        if len(memeber_set) > 0:
            warnings.warn("%s fileds are useless." % ",".join(memeber_set))
        


class ExpiredSnapshotsInfo(AbstractModel):
    """快照过期数据治理项信息

    """

    def __init__(self):
        r"""
        :param ExpiredSnapshotsEnable: 是否启用快照过期治理项：enable、none
        :type ExpiredSnapshotsEnable: str
        :param Engine: 用于运行快照过期治理项的引擎名称
        :type Engine: str
        :param RetainLast: 需要保留的最近快照个数
        :type RetainLast: int
        :param BeforeDays: 过期指定天前的快照
        :type BeforeDays: int
        :param MaxConcurrentDeletes: 清理过期快照的并行数
        :type MaxConcurrentDeletes: int
        :param IntervalMin: 快照过期治理运行周期，单位为分钟
        :type IntervalMin: int
        """
        self.ExpiredSnapshotsEnable = None
        self.Engine = None
        self.RetainLast = None
        self.BeforeDays = None
        self.MaxConcurrentDeletes = None
        self.IntervalMin = None


    def _deserialize(self, params):
        self.ExpiredSnapshotsEnable = params.get("ExpiredSnapshotsEnable")
        self.Engine = params.get("Engine")
        self.RetainLast = params.get("RetainLast")
        self.BeforeDays = params.get("BeforeDays")
        self.MaxConcurrentDeletes = params.get("MaxConcurrentDeletes")
        self.IntervalMin = params.get("IntervalMin")
        memeber_set = set(params.keys())
        for name, value in vars(self).items():
            if name in memeber_set:
                memeber_set.remove(name)
        if len(memeber_set) > 0:
            warnings.warn("%s fileds are useless." % ",".join(memeber_set))
        


class ExportResultRequest(AbstractModel):
    """ExportResult请求参数结构体

    """

    def __init__(self):
        r"""
        :param DataPath: SQL查询结果存放的路径，目前只支持托管的查询结果导出，即Path是lakefs协议的路径
        :type DataPath: str
        :param Target: 目标桶信息，包括桶名、区域、Key
        :type Target: :class:`tencentcloud.dlc.v20210125.models.CosObject`
        :param SessionId: SQL查询窗口ID
        :type SessionId: str
        """
        self.DataPath = None
        self.Target = None
        self.SessionId = None


    def _deserialize(self, params):
        self.DataPath = params.get("DataPath")
        if params.get("Target") is not None:
            self.Target = CosObject()
            self.Target._deserialize(params.get("Target"))
        self.SessionId = params.get("SessionId")
        memeber_set = set(params.keys())
        for name, value in vars(self).items():
            if name in memeber_set:
                memeber_set.remove(name)
        if len(memeber_set) > 0:
            warnings.warn("%s fileds are useless." % ",".join(memeber_set))
        


class ExportResultResponse(AbstractModel):
    """ExportResult返回参数结构体

    """

    def __init__(self):
        r"""
        :param TaskId: 任务ID
        :type TaskId: str
        :param RequestId: 唯一请求 ID，每次请求都会返回。定位问题时需要提供该次请求的 RequestId。
        :type RequestId: str
        """
        self.TaskId = None
        self.RequestId = None


    def _deserialize(self, params):
        self.TaskId = params.get("TaskId")
        self.RequestId = params.get("RequestId")


class FileType(AbstractModel):
    """文件类型

    """

    def __init__(self):
        r"""
        :param CSV: CSV文件,[CSV,JSON,AVRO,PARQUET,ORC]五选一
        :type CSV: :class:`tencentcloud.dlc.v20210125.models.CSVFile`
        :param Json: JSON文件, [CSV,JSON,AVRO,PARQUET,ORC]五选一
        :type Json: :class:`tencentcloud.dlc.v20210125.models.JsonFile`
        :param AVRO: AVRO文件, [CSV,JSON,AVRO,PARQUET,ORC]五选一
        :type AVRO: :class:`tencentcloud.dlc.v20210125.models.AVROFile`
        :param Parquet: PARQUET文件, [CSV,JSON,AVRO,PARQUET,ORC]五选一
        :type Parquet: :class:`tencentcloud.dlc.v20210125.models.ParquetFile`
        :param ORC: ORC文件, [CSV,JSON,AVRO,PARQUET,ORC]五选一
        :type ORC: :class:`tencentcloud.dlc.v20210125.models.ORCFile`
        """
        self.CSV = None
        self.Json = None
        self.AVRO = None
        self.Parquet = None
        self.ORC = None


    def _deserialize(self, params):
        if params.get("CSV") is not None:
            self.CSV = CSVFile()
            self.CSV._deserialize(params.get("CSV"))
        if params.get("Json") is not None:
            self.Json = JsonFile()
            self.Json._deserialize(params.get("Json"))
        if params.get("AVRO") is not None:
            self.AVRO = AVROFile()
            self.AVRO._deserialize(params.get("AVRO"))
        if params.get("Parquet") is not None:
            self.Parquet = ParquetFile()
            self.Parquet._deserialize(params.get("Parquet"))
        if params.get("ORC") is not None:
            self.ORC = ORCFile()
            self.ORC._deserialize(params.get("ORC"))
        memeber_set = set(params.keys())
        for name, value in vars(self).items():
            if name in memeber_set:
                memeber_set.remove(name)
        if len(memeber_set) > 0:
            warnings.warn("%s fileds are useless." % ",".join(memeber_set))
        


class Filter(AbstractModel):
    """查询列表过滤条件参数

    """

    def __init__(self):
        r"""
        :param Name: 属性名称, 若存在多个Filter时，Filter间的关系为逻辑或（OR）关系。
        :type Name: str
        :param Values: 属性值, 若同一个Filter存在多个Values，同一Filter下Values间的关系为逻辑或（OR）关系。
        :type Values: list of str
        """
        self.Name = None
        self.Values = None


    def _deserialize(self, params):
        self.Name = params.get("Name")
        self.Values = params.get("Values")
        memeber_set = set(params.keys())
        for name, value in vars(self).items():
            if name in memeber_set:
                memeber_set.remove(name)
        if len(memeber_set) > 0:
            warnings.warn("%s fileds are useless." % ",".join(memeber_set))
        


class ForceSuccessScheduleTaskInstancesRequest(AbstractModel):
    """ForceSuccessScheduleTaskInstances请求参数结构体

    """

    def __init__(self):
        r"""
        :param Instances: 调度任务实例列表
        :type Instances: list of ScheduleInstanceRunInfo
        """
        self.Instances = None


    def _deserialize(self, params):
        if params.get("Instances") is not None:
            self.Instances = []
            for item in params.get("Instances"):
                obj = ScheduleInstanceRunInfo()
                obj._deserialize(item)
                self.Instances.append(obj)
        memeber_set = set(params.keys())
        for name, value in vars(self).items():
            if name in memeber_set:
                memeber_set.remove(name)
        if len(memeber_set) > 0:
            warnings.warn("%s fileds are useless." % ",".join(memeber_set))
        


class ForceSuccessScheduleTaskInstancesResponse(AbstractModel):
    """ForceSuccessScheduleTaskInstances返回参数结构体

    """

    def __init__(self):
        r"""
        :param Result: 调度任务置为成功请求结果
        :type Result: bool
        :param RequestId: 唯一请求 ID，每次请求都会返回。定位问题时需要提供该次请求的 RequestId。
        :type RequestId: str
        """
        self.Result = None
        self.RequestId = None


    def _deserialize(self, params):
        self.Result = params.get("Result")
        self.RequestId = params.get("RequestId")


class FreezeScheduleTasksRequest(AbstractModel):
    """FreezeScheduleTasks请求参数结构体

    """

    def __init__(self):
        r"""
        :param TaskIdList: 调度任务ID列表
        :type TaskIdList: list of str
        """
        self.TaskIdList = None


    def _deserialize(self, params):
        self.TaskIdList = params.get("TaskIdList")
        memeber_set = set(params.keys())
        for name, value in vars(self).items():
            if name in memeber_set:
                memeber_set.remove(name)
        if len(memeber_set) > 0:
            warnings.warn("%s fileds are useless." % ",".join(memeber_set))
        


class FreezeScheduleTasksResponse(AbstractModel):
    """FreezeScheduleTasks返回参数结构体

    """

    def __init__(self):
        r"""
        :param Total: 总冻结任务数
        :type Total: int
        :param Success: 冻结任务成功数
        :type Success: int
        :param Running: 冻结任务运行中数
        :type Running: int
        :param Failed: 冻结任务失败数
        :type Failed: int
        :param RequestId: 唯一请求 ID，每次请求都会返回。定位问题时需要提供该次请求的 RequestId。
        :type RequestId: str
        """
        self.Total = None
        self.Success = None
        self.Running = None
        self.Failed = None
        self.RequestId = None


    def _deserialize(self, params):
        self.Total = params.get("Total")
        self.Success = params.get("Success")
        self.Running = params.get("Running")
        self.Failed = params.get("Failed")
        self.RequestId = params.get("RequestId")


class FunctionSimpleData(AbstractModel):
    """udf简单信息

    """

    def __init__(self):
        r"""
        :param Id: udf对应id
注意：此字段可能返回 null，表示取不到有效值。
        :type Id: int
        :param FuncName: 函数名称
注意：此字段可能返回 null，表示取不到有效值。
        :type FuncName: str
        :param Desc: 描述信息
注意：此字段可能返回 null，表示取不到有效值。
        :type Desc: str
        """
        self.Id = None
        self.FuncName = None
        self.Desc = None


    def _deserialize(self, params):
        self.Id = params.get("Id")
        self.FuncName = params.get("FuncName")
        self.Desc = params.get("Desc")
        memeber_set = set(params.keys())
        for name, value in vars(self).items():
            if name in memeber_set:
                memeber_set.remove(name)
        if len(memeber_set) > 0:
            warnings.warn("%s fileds are useless." % ",".join(memeber_set))
        


class GenerateCreateMangedTableSqlRequest(AbstractModel):
    """GenerateCreateMangedTableSql请求参数结构体

    """

    def __init__(self):
        r"""
        :param TableBaseInfo: 表基本信息
        :type TableBaseInfo: :class:`tencentcloud.dlc.v20210125.models.TableBaseInfo`
        :param Columns: 表字段信息
        :type Columns: list of TColumn
        :param Partitions: 表分区信息
        :type Partitions: list of TPartition
        :param Properties: 表属性信息
        :type Properties: list of Property
        :param UpsertKeys: V2 upsert表 upsert键
        :type UpsertKeys: list of str
        """
        self.TableBaseInfo = None
        self.Columns = None
        self.Partitions = None
        self.Properties = None
        self.UpsertKeys = None


    def _deserialize(self, params):
        if params.get("TableBaseInfo") is not None:
            self.TableBaseInfo = TableBaseInfo()
            self.TableBaseInfo._deserialize(params.get("TableBaseInfo"))
        if params.get("Columns") is not None:
            self.Columns = []
            for item in params.get("Columns"):
                obj = TColumn()
                obj._deserialize(item)
                self.Columns.append(obj)
        if params.get("Partitions") is not None:
            self.Partitions = []
            for item in params.get("Partitions"):
                obj = TPartition()
                obj._deserialize(item)
                self.Partitions.append(obj)
        if params.get("Properties") is not None:
            self.Properties = []
            for item in params.get("Properties"):
                obj = Property()
                obj._deserialize(item)
                self.Properties.append(obj)
        self.UpsertKeys = params.get("UpsertKeys")
        memeber_set = set(params.keys())
        for name, value in vars(self).items():
            if name in memeber_set:
                memeber_set.remove(name)
        if len(memeber_set) > 0:
            warnings.warn("%s fileds are useless." % ",".join(memeber_set))
        


class GenerateCreateMangedTableSqlResponse(AbstractModel):
    """GenerateCreateMangedTableSql返回参数结构体

    """

    def __init__(self):
        r"""
        :param Execution: 创建托管存储内表sql语句描述
        :type Execution: :class:`tencentcloud.dlc.v20210125.models.Execution`
        :param RequestId: 唯一请求 ID，每次请求都会返回。定位问题时需要提供该次请求的 RequestId。
        :type RequestId: str
        """
        self.Execution = None
        self.RequestId = None


    def _deserialize(self, params):
        if params.get("Execution") is not None:
            self.Execution = Execution()
            self.Execution._deserialize(params.get("Execution"))
        self.RequestId = params.get("RequestId")


class GetWorkflowCanvasRequest(AbstractModel):
    """GetWorkflowCanvas请求参数结构体

    """

    def __init__(self):
        r"""
        :param WorkflowId: 调度计划ID
        :type WorkflowId: str
        """
        self.WorkflowId = None


    def _deserialize(self, params):
        self.WorkflowId = params.get("WorkflowId")
        memeber_set = set(params.keys())
        for name, value in vars(self).items():
            if name in memeber_set:
                memeber_set.remove(name)
        if len(memeber_set) > 0:
            warnings.warn("%s fileds are useless." % ",".join(memeber_set))
        


class GetWorkflowCanvasResponse(AbstractModel):
    """GetWorkflowCanvas返回参数结构体

    """

    def __init__(self):
        r"""
        :param ResultData: 画布数据
        :type ResultData: :class:`tencentcloud.dlc.v20210125.models.CanvasInfo`
        :param RequestId: 唯一请求 ID，每次请求都会返回。定位问题时需要提供该次请求的 RequestId。
        :type RequestId: str
        """
        self.ResultData = None
        self.RequestId = None


    def _deserialize(self, params):
        if params.get("ResultData") is not None:
            self.ResultData = CanvasInfo()
            self.ResultData._deserialize(params.get("ResultData"))
        self.RequestId = params.get("RequestId")


class GetWorkflowInfoRequest(AbstractModel):
    """GetWorkflowInfo请求参数结构体

    """

    def __init__(self):
        r"""
        :param WorkflowId: 调度计划ID
        :type WorkflowId: str
        """
        self.WorkflowId = None


    def _deserialize(self, params):
        self.WorkflowId = params.get("WorkflowId")
        memeber_set = set(params.keys())
        for name, value in vars(self).items():
            if name in memeber_set:
                memeber_set.remove(name)
        if len(memeber_set) > 0:
            warnings.warn("%s fileds are useless." % ",".join(memeber_set))
        


class GetWorkflowInfoResponse(AbstractModel):
    """GetWorkflowInfo返回参数结构体

    """

    def __init__(self):
        r"""
        :param WorkflowInfo: 调度计划信息
        :type WorkflowInfo: :class:`tencentcloud.dlc.v20210125.models.WorkflowInfo`
        :param RequestId: 唯一请求 ID，每次请求都会返回。定位问题时需要提供该次请求的 RequestId。
        :type RequestId: str
        """
        self.WorkflowInfo = None
        self.RequestId = None


    def _deserialize(self, params):
        if params.get("WorkflowInfo") is not None:
            self.WorkflowInfo = WorkflowInfo()
            self.WorkflowInfo._deserialize(params.get("WorkflowInfo"))
        self.RequestId = params.get("RequestId")


class GovernMetaInfo(AbstractModel):
    """数据实例元信息数据结构

    """

    def __init__(self):
        r"""
        :param Version: 数据表版本信息
注意：此字段可能返回 null，表示取不到有效值。
        :type Version: int
        :param UpsertEnable: 表是否支持Upsert操过
注意：此字段可能返回 null，表示取不到有效值。
        :type UpsertEnable: bool
        :param InheritEnable: 表是否是继承库策略
注意：此字段可能返回 null，表示取不到有效值。
        :type InheritEnable: bool
        :param GovernPolicy: 表有效治理规则
注意：此字段可能返回 null，表示取不到有效值。
        :type GovernPolicy: :class:`tencentcloud.dlc.v20210125.models.DataGovernPolicy`
        """
        self.Version = None
        self.UpsertEnable = None
        self.InheritEnable = None
        self.GovernPolicy = None


    def _deserialize(self, params):
        self.Version = params.get("Version")
        self.UpsertEnable = params.get("UpsertEnable")
        self.InheritEnable = params.get("InheritEnable")
        if params.get("GovernPolicy") is not None:
            self.GovernPolicy = DataGovernPolicy()
            self.GovernPolicy._deserialize(params.get("GovernPolicy"))
        memeber_set = set(params.keys())
        for name, value in vars(self).items():
            if name in memeber_set:
                memeber_set.remove(name)
        if len(memeber_set) > 0:
            warnings.warn("%s fileds are useless." % ",".join(memeber_set))
        


class HiveInfo(AbstractModel):
    """hive类型数据源的信息

    """

    def __init__(self):
        r"""
        :param MetaStoreUrl: hive metastore的地址
        :type MetaStoreUrl: str
        :param Type: hive数据源类型，代表数据储存的位置，COS或者HDFS
        :type Type: str
        :param Location: 数据源所在的私有网络信息
        :type Location: :class:`tencentcloud.dlc.v20210125.models.DatasourceConnectionLocation`
        :param User: 如果类型为HDFS，需要传一个用户名
        :type User: str
        :param HighAvailability: 如果类型为HDFS，需要选择是否高可用
        :type HighAvailability: bool
        :param BucketUrl: 如果类型为COS，需要填写COS桶连接
        :type BucketUrl: str
        :param HdfsProperties: json字符串。如果类型为HDFS，需要填写该字段
        :type HdfsProperties: str
        :param Mysql: Hive的元数据库信息
注意：此字段可能返回 null，表示取不到有效值。
        :type Mysql: :class:`tencentcloud.dlc.v20210125.models.MysqlInfo`
        :param InstanceId: emr集群Id
注意：此字段可能返回 null，表示取不到有效值。
        :type InstanceId: str
        :param InstanceName: emr集群名称
注意：此字段可能返回 null，表示取不到有效值。
        :type InstanceName: str
        :param HiveVersion: EMR集群中hive组件的版本号
注意：此字段可能返回 null，表示取不到有效值。
        :type HiveVersion: str
        :param KerberosInfo: Kerberos详细信息
注意：此字段可能返回 null，表示取不到有效值。
        :type KerberosInfo: :class:`tencentcloud.dlc.v20210125.models.KerberosInfo`
        :param KerberosEnable: 是否开启Kerberos
注意：此字段可能返回 null，表示取不到有效值。
        :type KerberosEnable: bool
        """
        self.MetaStoreUrl = None
        self.Type = None
        self.Location = None
        self.User = None
        self.HighAvailability = None
        self.BucketUrl = None
        self.HdfsProperties = None
        self.Mysql = None
        self.InstanceId = None
        self.InstanceName = None
        self.HiveVersion = None
        self.KerberosInfo = None
        self.KerberosEnable = None


    def _deserialize(self, params):
        self.MetaStoreUrl = params.get("MetaStoreUrl")
        self.Type = params.get("Type")
        if params.get("Location") is not None:
            self.Location = DatasourceConnectionLocation()
            self.Location._deserialize(params.get("Location"))
        self.User = params.get("User")
        self.HighAvailability = params.get("HighAvailability")
        self.BucketUrl = params.get("BucketUrl")
        self.HdfsProperties = params.get("HdfsProperties")
        if params.get("Mysql") is not None:
            self.Mysql = MysqlInfo()
            self.Mysql._deserialize(params.get("Mysql"))
        self.InstanceId = params.get("InstanceId")
        self.InstanceName = params.get("InstanceName")
        self.HiveVersion = params.get("HiveVersion")
        if params.get("KerberosInfo") is not None:
            self.KerberosInfo = KerberosInfo()
            self.KerberosInfo._deserialize(params.get("KerberosInfo"))
        self.KerberosEnable = params.get("KerberosEnable")
        memeber_set = set(params.keys())
        for name, value in vars(self).items():
            if name in memeber_set:
                memeber_set.remove(name)
        if len(memeber_set) > 0:
            warnings.warn("%s fileds are useless." % ",".join(memeber_set))
        


class HouseEventsInfo(AbstractModel):
    """集群事件日志

    """

    def __init__(self):
        r"""
        :param Time: 事件时间
注意：此字段可能返回 null，表示取不到有效值。
        :type Time: list of str
        :param EventsAction: 事件类型
注意：此字段可能返回 null，表示取不到有效值。
        :type EventsAction: list of str
        :param ClusterInfo: 集群信息
注意：此字段可能返回 null，表示取不到有效值。
        :type ClusterInfo: list of str
        """
        self.Time = None
        self.EventsAction = None
        self.ClusterInfo = None


    def _deserialize(self, params):
        self.Time = params.get("Time")
        self.EventsAction = params.get("EventsAction")
        self.ClusterInfo = params.get("ClusterInfo")
        memeber_set = set(params.keys())
        for name, value in vars(self).items():
            if name in memeber_set:
                memeber_set.remove(name)
        if len(memeber_set) > 0:
            warnings.warn("%s fileds are useless." % ",".join(memeber_set))
        


class ImageOperateRecord(AbstractModel):
    """集群镜像操作日志。

    """

    def __init__(self):
        r"""
        :param RecordId: 日志记录唯一id
        :type RecordId: str
        :param DataEngineId: 引擎唯一id
        :type DataEngineId: str
        :param ImageVersionId: 集群镜像大版本id
        :type ImageVersionId: str
        :param ImageVersion: 集群镜像大版本名称
        :type ImageVersion: str
        :param ChildImageVersionId: 集群镜像小版本id
        :type ChildImageVersionId: str
        :param Operate: 操作类型：初始化：InitImage、变配ModifyResource、升级： UpgradeImage、切换：SwitchImage、回滚：RollbackImage
        :type Operate: str
        :param EngineSize: 引擎规格
        :type EngineSize: str
        :param UserAppId: 用户appid
        :type UserAppId: int
        :param UserAlias: 用户昵称
        :type UserAlias: str
        :param UserUin: 用户Uin
        :type UserUin: str
        :param InsertTime: 创建时间
        :type InsertTime: str
        """
        self.RecordId = None
        self.DataEngineId = None
        self.ImageVersionId = None
        self.ImageVersion = None
        self.ChildImageVersionId = None
        self.Operate = None
        self.EngineSize = None
        self.UserAppId = None
        self.UserAlias = None
        self.UserUin = None
        self.InsertTime = None


    def _deserialize(self, params):
        self.RecordId = params.get("RecordId")
        self.DataEngineId = params.get("DataEngineId")
        self.ImageVersionId = params.get("ImageVersionId")
        self.ImageVersion = params.get("ImageVersion")
        self.ChildImageVersionId = params.get("ChildImageVersionId")
        self.Operate = params.get("Operate")
        self.EngineSize = params.get("EngineSize")
        self.UserAppId = params.get("UserAppId")
        self.UserAlias = params.get("UserAlias")
        self.UserUin = params.get("UserUin")
        self.InsertTime = params.get("InsertTime")
        memeber_set = set(params.keys())
        for name, value in vars(self).items():
            if name in memeber_set:
                memeber_set.remove(name)
        if len(memeber_set) > 0:
            warnings.warn("%s fileds are useless." % ",".join(memeber_set))
        


class InferInternalTableSchemaRequest(AbstractModel):
    """InferInternalTableSchema请求参数结构体

    """

    def __init__(self):
        r"""
        :param FileType: 文件类型相关信息，如文件类型，压缩格式等
        :type FileType: :class:`tencentcloud.dlc.v20210125.models.FileType`
        :param Location: 文件路径，如lakefs://xxx-123456/xxx/
        :type Location: str
        """
        self.FileType = None
        self.Location = None


    def _deserialize(self, params):
        if params.get("FileType") is not None:
            self.FileType = FileType()
            self.FileType._deserialize(params.get("FileType"))
        self.Location = params.get("Location")
        memeber_set = set(params.keys())
        for name, value in vars(self).items():
            if name in memeber_set:
                memeber_set.remove(name)
        if len(memeber_set) > 0:
            warnings.warn("%s fileds are useless." % ",".join(memeber_set))
        


class InferInternalTableSchemaResponse(AbstractModel):
    """InferInternalTableSchema返回参数结构体

    """

    def __init__(self):
        r"""
        :param Data: 无
        :type Data: str
        :param RequestId: 唯一请求 ID，每次请求都会返回。定位问题时需要提供该次请求的 RequestId。
        :type RequestId: str
        """
        self.Data = None
        self.RequestId = None


    def _deserialize(self, params):
        self.Data = params.get("Data")
        self.RequestId = params.get("RequestId")


class InferSchemaRequest(AbstractModel):
    """InferSchema请求参数结构体

    """

    def __init__(self):
        r"""
        :param FileType: 文件类型相关信息，如文件类型，压缩格式等
        :type FileType: :class:`tencentcloud.dlc.v20210125.models.FileType`
        :param Location: 文件路径，如cosn://xxx-123456/xxx/
        :type Location: str
        """
        self.FileType = None
        self.Location = None


    def _deserialize(self, params):
        if params.get("FileType") is not None:
            self.FileType = FileType()
            self.FileType._deserialize(params.get("FileType"))
        self.Location = params.get("Location")
        memeber_set = set(params.keys())
        for name, value in vars(self).items():
            if name in memeber_set:
                memeber_set.remove(name)
        if len(memeber_set) > 0:
            warnings.warn("%s fileds are useless." % ",".join(memeber_set))
        


class InferSchemaResponse(AbstractModel):
    """InferSchema返回参数结构体

    """

    def __init__(self):
        r"""
        :param Data: 推断后的schema信息，通过json格式展现
注意：此字段可能返回 null，表示取不到有效值。
        :type Data: str
        :param RequestId: 唯一请求 ID，每次请求都会返回。定位问题时需要提供该次请求的 RequestId。
        :type RequestId: str
        """
        self.Data = None
        self.RequestId = None


    def _deserialize(self, params):
        self.Data = params.get("Data")
        self.RequestId = params.get("RequestId")


class InquireCreateDataEnginePriceRequest(AbstractModel):
    """InquireCreateDataEnginePrice请求参数结构体

    """

    def __init__(self):
        r"""
        :param Size: 数据引擎单个集群的规模，单位CU
        :type Size: int
        :param MinClusters: 数据引擎最小集群数，在预付费模式下，最小为1，最大为10，在后付费模式下，最小为0，最大为1
        :type MinClusters: int
        :param MaxClusters: 数据引擎最大集群数，最小为1，最大为10，并要大于等于MinClusters
        :type MaxClusters: int
        :param PayMode: 计费模式。0：按量计费；1：包年包月计费
        :type PayMode: int
        :param TimeSpan: 计费时长。按量计费下固定为1；包年包月计费下表示购买的月份
        :type TimeSpan: int
        :param TimeUnit: 计费时长单位。按量计费下固定为h；包年包月计费下固定为m
        :type TimeUnit: str
        :param ResourceType: 资源类型。Standard_CU：标准型，Memory_CU：内存型。
        :type ResourceType: str
        """
        self.Size = None
        self.MinClusters = None
        self.MaxClusters = None
        self.PayMode = None
        self.TimeSpan = None
        self.TimeUnit = None
        self.ResourceType = None


    def _deserialize(self, params):
        self.Size = params.get("Size")
        self.MinClusters = params.get("MinClusters")
        self.MaxClusters = params.get("MaxClusters")
        self.PayMode = params.get("PayMode")
        self.TimeSpan = params.get("TimeSpan")
        self.TimeUnit = params.get("TimeUnit")
        self.ResourceType = params.get("ResourceType")
        memeber_set = set(params.keys())
        for name, value in vars(self).items():
            if name in memeber_set:
                memeber_set.remove(name)
        if len(memeber_set) > 0:
            warnings.warn("%s fileds are useless." % ",".join(memeber_set))
        


class InquireCreateDataEnginePriceResponse(AbstractModel):
    """InquireCreateDataEnginePrice返回参数结构体

    """

    def __init__(self):
        r"""
        :param ResidentResourcePrice: 创建数据引擎的常驻部分资源的价格信息
注意：此字段可能返回 null，表示取不到有效值。
        :type ResidentResourcePrice: :class:`tencentcloud.dlc.v20210125.models.Price`
        :param ElasticResourcePrice: 创建数据引擎的弹性部分资源的价格信息
注意：此字段可能返回 null，表示取不到有效值。
        :type ElasticResourcePrice: :class:`tencentcloud.dlc.v20210125.models.Price`
        :param RequestId: 唯一请求 ID，每次请求都会返回。定位问题时需要提供该次请求的 RequestId。
        :type RequestId: str
        """
        self.ResidentResourcePrice = None
        self.ElasticResourcePrice = None
        self.RequestId = None


    def _deserialize(self, params):
        if params.get("ResidentResourcePrice") is not None:
            self.ResidentResourcePrice = Price()
            self.ResidentResourcePrice._deserialize(params.get("ResidentResourcePrice"))
        if params.get("ElasticResourcePrice") is not None:
            self.ElasticResourcePrice = Price()
            self.ElasticResourcePrice._deserialize(params.get("ElasticResourcePrice"))
        self.RequestId = params.get("RequestId")


class InquirePriceCreateDataEngineRequest(AbstractModel):
    """InquirePriceCreateDataEngine请求参数结构体

    """

    def __init__(self):
        r"""
        :param Size: 数据引擎单个集群的规模，单位CU
        :type Size: int
        :param MinClusters: 数据引擎最小集群数，最小为1，最大为10
        :type MinClusters: int
        :param MaxClusters: 数据引擎最大集群数，最小为1，最大为10，并要大于等于MinClusters
        :type MaxClusters: int
        :param PayMode: 计费模式。0：按量计费；1：包年包月计费
        :type PayMode: int
        :param TimeSpan: 计费时长。按量计费下固定为3600；包年包月计费下表示购买的月份
        :type TimeSpan: int
        :param TimeUnit: 计费时长单位。按量计费下固定为s；包年包月计费下固定为m
        :type TimeUnit: str
        :param ResourceType: 资源类型，Standard_CU：标准型；Memory_CU：内存型。
        :type ResourceType: str
        """
        self.Size = None
        self.MinClusters = None
        self.MaxClusters = None
        self.PayMode = None
        self.TimeSpan = None
        self.TimeUnit = None
        self.ResourceType = None


    def _deserialize(self, params):
        self.Size = params.get("Size")
        self.MinClusters = params.get("MinClusters")
        self.MaxClusters = params.get("MaxClusters")
        self.PayMode = params.get("PayMode")
        self.TimeSpan = params.get("TimeSpan")
        self.TimeUnit = params.get("TimeUnit")
        self.ResourceType = params.get("ResourceType")
        memeber_set = set(params.keys())
        for name, value in vars(self).items():
            if name in memeber_set:
                memeber_set.remove(name)
        if len(memeber_set) > 0:
            warnings.warn("%s fileds are useless." % ",".join(memeber_set))
        


class InquirePriceCreateDataEngineResponse(AbstractModel):
    """InquirePriceCreateDataEngine返回参数结构体

    """

    def __init__(self):
        r"""
        :param Price: 创建数据引擎的价格信息
        :type Price: :class:`tencentcloud.dlc.v20210125.models.Price`
        :param RequestId: 唯一请求 ID，每次请求都会返回。定位问题时需要提供该次请求的 RequestId。
        :type RequestId: str
        """
        self.Price = None
        self.RequestId = None


    def _deserialize(self, params):
        if params.get("Price") is not None:
            self.Price = Price()
            self.Price._deserialize(params.get("Price"))
        self.RequestId = params.get("RequestId")


class InquirePriceModifyDataEngineRequest(AbstractModel):
    """InquirePriceModifyDataEngine请求参数结构体

    """

    def __init__(self):
        r"""
        :param DataEngineName: 数据引擎名称
        :type DataEngineName: str
        :param Size: 变配后的数据引擎规格
        :type Size: int
        :param MinClusters: 变配后的数据引擎最小集群数
        :type MinClusters: int
        :param MaxClusters: 变配后的数据引擎最大集群数
        :type MaxClusters: int
        """
        self.DataEngineName = None
        self.Size = None
        self.MinClusters = None
        self.MaxClusters = None


    def _deserialize(self, params):
        self.DataEngineName = params.get("DataEngineName")
        self.Size = params.get("Size")
        self.MinClusters = params.get("MinClusters")
        self.MaxClusters = params.get("MaxClusters")
        memeber_set = set(params.keys())
        for name, value in vars(self).items():
            if name in memeber_set:
                memeber_set.remove(name)
        if len(memeber_set) > 0:
            warnings.warn("%s fileds are useless." % ",".join(memeber_set))
        


class InquirePriceModifyDataEngineResponse(AbstractModel):
    """InquirePriceModifyDataEngine返回参数结构体

    """

    def __init__(self):
        r"""
        :param Price: 变配价格汇总信息，在按量计费模式下，是新的最低配置的价格
        :type Price: :class:`tencentcloud.dlc.v20210125.models.Price`
        :param NewPrice: 新配置的购买信息，只有包年包月会返回该字段
注意：此字段可能返回 null，表示取不到有效值。
        :type NewPrice: :class:`tencentcloud.dlc.v20210125.models.Price`
        :param RefundPrice: 旧配置退款的信息，只有包年包月会返回该字段
注意：此字段可能返回 null，表示取不到有效值。
        :type RefundPrice: :class:`tencentcloud.dlc.v20210125.models.Price`
        :param ElasticPrice: 新配置的弹性部分的价格，只在有弹性资源的时候才会按照此收费
注意：此字段可能返回 null，表示取不到有效值。
        :type ElasticPrice: :class:`tencentcloud.dlc.v20210125.models.Price`
        :param RequestId: 唯一请求 ID，每次请求都会返回。定位问题时需要提供该次请求的 RequestId。
        :type RequestId: str
        """
        self.Price = None
        self.NewPrice = None
        self.RefundPrice = None
        self.ElasticPrice = None
        self.RequestId = None


    def _deserialize(self, params):
        if params.get("Price") is not None:
            self.Price = Price()
            self.Price._deserialize(params.get("Price"))
        if params.get("NewPrice") is not None:
            self.NewPrice = Price()
            self.NewPrice._deserialize(params.get("NewPrice"))
        if params.get("RefundPrice") is not None:
            self.RefundPrice = Price()
            self.RefundPrice._deserialize(params.get("RefundPrice"))
        if params.get("ElasticPrice") is not None:
            self.ElasticPrice = Price()
            self.ElasticPrice._deserialize(params.get("ElasticPrice"))
        self.RequestId = params.get("RequestId")


class InquirePriceTerminateDataEngineRequest(AbstractModel):
    """InquirePriceTerminateDataEngine请求参数结构体

    """

    def __init__(self):
        r"""
        :param DataEngineNames: 需要退费的引擎的名称列表
        :type DataEngineNames: list of str
        """
        self.DataEngineNames = None


    def _deserialize(self, params):
        self.DataEngineNames = params.get("DataEngineNames")
        memeber_set = set(params.keys())
        for name, value in vars(self).items():
            if name in memeber_set:
                memeber_set.remove(name)
        if len(memeber_set) > 0:
            warnings.warn("%s fileds are useless." % ",".join(memeber_set))
        


class InquirePriceTerminateDataEngineResponse(AbstractModel):
    """InquirePriceTerminateDataEngine返回参数结构体

    """

    def __init__(self):
        r"""
        :param RefundInfo: 退款详细信息
注意：此字段可能返回 null，表示取不到有效值。
        :type RefundInfo: list of DataEngineRefundMessage
        :param RequestId: 唯一请求 ID，每次请求都会返回。定位问题时需要提供该次请求的 RequestId。
        :type RequestId: str
        """
        self.RefundInfo = None
        self.RequestId = None


    def _deserialize(self, params):
        if params.get("RefundInfo") is not None:
            self.RefundInfo = []
            for item in params.get("RefundInfo"):
                obj = DataEngineRefundMessage()
                obj._deserialize(item)
                self.RefundInfo.append(obj)
        self.RequestId = params.get("RequestId")


class IpPortPair(AbstractModel):
    """ip端口对信息

    """

    def __init__(self):
        r"""
        :param Ip: ip信息
注意：此字段可能返回 null，表示取不到有效值。
        :type Ip: str
        :param Port: 端口信息
注意：此字段可能返回 null，表示取不到有效值。
        :type Port: int
        """
        self.Ip = None
        self.Port = None


    def _deserialize(self, params):
        self.Ip = params.get("Ip")
        self.Port = params.get("Port")
        memeber_set = set(params.keys())
        for name, value in vars(self).items():
            if name in memeber_set:
                memeber_set.remove(name)
        if len(memeber_set) > 0:
            warnings.warn("%s fileds are useless." % ",".join(memeber_set))
        


class JobLogResult(AbstractModel):
    """日志详情

    """

    def __init__(self):
        r"""
        :param Time: 日志时间戳，毫秒
注意：此字段可能返回 null，表示取不到有效值。
        :type Time: int
        :param TopicId: 日志topic id
注意：此字段可能返回 null，表示取不到有效值。
        :type TopicId: str
        :param TopicName: 日志topic name
注意：此字段可能返回 null，表示取不到有效值。
        :type TopicName: str
        :param LogJson: 日志内容，json字符串
注意：此字段可能返回 null，表示取不到有效值。
        :type LogJson: str
        :param PkgLogId: 日志ID
注意：此字段可能返回 null，表示取不到有效值。
        :type PkgLogId: str
        """
        self.Time = None
        self.TopicId = None
        self.TopicName = None
        self.LogJson = None
        self.PkgLogId = None


    def _deserialize(self, params):
        self.Time = params.get("Time")
        self.TopicId = params.get("TopicId")
        self.TopicName = params.get("TopicName")
        self.LogJson = params.get("LogJson")
        self.PkgLogId = params.get("PkgLogId")
        memeber_set = set(params.keys())
        for name, value in vars(self).items():
            if name in memeber_set:
                memeber_set.remove(name)
        if len(memeber_set) > 0:
            warnings.warn("%s fileds are useless." % ",".join(memeber_set))
        


class JsonFile(AbstractModel):
    """Json类型文件

    """

    def __init__(self):
        r"""
        :param Format: 文本类型，本参数取值为Json。
        :type Format: str
        :param CodeCompress: 压缩格式，["Snappy","Gzip","None"选一]
        :type CodeCompress: str
        """
        self.Format = None
        self.CodeCompress = None


    def _deserialize(self, params):
        self.Format = params.get("Format")
        self.CodeCompress = params.get("CodeCompress")
        memeber_set = set(params.keys())
        for name, value in vars(self).items():
            if name in memeber_set:
                memeber_set.remove(name)
        if len(memeber_set) > 0:
            warnings.warn("%s fileds are useless." % ",".join(memeber_set))
        


class KVPair(AbstractModel):
    """配置格式

    """

    def __init__(self):
        r"""
        :param Key: 配置的key值
注意：此字段可能返回 null，表示取不到有效值。
        :type Key: str
        :param Value: 配置的value值
注意：此字段可能返回 null，表示取不到有效值。
        :type Value: str
        """
        self.Key = None
        self.Value = None


    def _deserialize(self, params):
        self.Key = params.get("Key")
        self.Value = params.get("Value")
        memeber_set = set(params.keys())
        for name, value in vars(self).items():
            if name in memeber_set:
                memeber_set.remove(name)
        if len(memeber_set) > 0:
            warnings.warn("%s fileds are useless." % ",".join(memeber_set))
        


class KafkaInfo(AbstractModel):
    """Kafka连接信息

    """

    def __init__(self):
        r"""
        :param InstanceId: kakfa实例Id
        :type InstanceId: str
        :param Location: kakfa数据源的网络信息
        :type Location: :class:`tencentcloud.dlc.v20210125.models.DatasourceConnectionLocation`
        """
        self.InstanceId = None
        self.Location = None


    def _deserialize(self, params):
        self.InstanceId = params.get("InstanceId")
        if params.get("Location") is not None:
            self.Location = DatasourceConnectionLocation()
            self.Location._deserialize(params.get("Location"))
        memeber_set = set(params.keys())
        for name, value in vars(self).items():
            if name in memeber_set:
                memeber_set.remove(name)
        if len(memeber_set) > 0:
            warnings.warn("%s fileds are useless." % ",".join(memeber_set))
        


class KerberosInfo(AbstractModel):
    """Kerberos详细信息

    """

    def __init__(self):
        r"""
        :param Krb5Conf: Krb5Conf文件值
        :type Krb5Conf: str
        :param KeyTab: KeyTab文件值
        :type KeyTab: str
        :param ServicePrincipal: 服务主体
        :type ServicePrincipal: str
        """
        self.Krb5Conf = None
        self.KeyTab = None
        self.ServicePrincipal = None


    def _deserialize(self, params):
        self.Krb5Conf = params.get("Krb5Conf")
        self.KeyTab = params.get("KeyTab")
        self.ServicePrincipal = params.get("ServicePrincipal")
        memeber_set = set(params.keys())
        for name, value in vars(self).items():
            if name in memeber_set:
                memeber_set.remove(name)
        if len(memeber_set) > 0:
            warnings.warn("%s fileds are useless." % ",".join(memeber_set))
        


class KillScheduleTaskInstancesRequest(AbstractModel):
    """KillScheduleTaskInstances请求参数结构体

    """

    def __init__(self):
        r"""
        :param Instances: 调度任务实例信息
        :type Instances: list of ScheduleInstanceRunInfo
        """
        self.Instances = None


    def _deserialize(self, params):
        if params.get("Instances") is not None:
            self.Instances = []
            for item in params.get("Instances"):
                obj = ScheduleInstanceRunInfo()
                obj._deserialize(item)
                self.Instances.append(obj)
        memeber_set = set(params.keys())
        for name, value in vars(self).items():
            if name in memeber_set:
                memeber_set.remove(name)
        if len(memeber_set) > 0:
            warnings.warn("%s fileds are useless." % ",".join(memeber_set))
        


class KillScheduleTaskInstancesResponse(AbstractModel):
    """KillScheduleTaskInstances返回参数结构体

    """

    def __init__(self):
        r"""
        :param Result: 终止调度任务实例请求结果
        :type Result: bool
        :param RequestId: 唯一请求 ID，每次请求都会返回。定位问题时需要提供该次请求的 RequestId。
        :type RequestId: str
        """
        self.Result = None
        self.RequestId = None


    def _deserialize(self, params):
        self.Result = params.get("Result")
        self.RequestId = params.get("RequestId")


class LakeFileSystem(AbstractModel):
    """LakeFileSystem详细信息

    """

    def __init__(self):
        r"""
        :param Schema: schem
        :type Schema: str
        :param Namespace: xxx
        :type Namespace: str
        :param Resource: xxx
        :type Resource: str
        :param Region: 地域
        :type Region: str
        :param Uri: lakefs uri
        :type Uri: str
        :param AccessToken: token
        :type AccessToken: :class:`tencentcloud.dlc.v20210125.models.LakeFileSystemToken`
        """
        self.Schema = None
        self.Namespace = None
        self.Resource = None
        self.Region = None
        self.Uri = None
        self.AccessToken = None


    def _deserialize(self, params):
        self.Schema = params.get("Schema")
        self.Namespace = params.get("Namespace")
        self.Resource = params.get("Resource")
        self.Region = params.get("Region")
        self.Uri = params.get("Uri")
        if params.get("AccessToken") is not None:
            self.AccessToken = LakeFileSystemToken()
            self.AccessToken._deserialize(params.get("AccessToken"))
        memeber_set = set(params.keys())
        for name, value in vars(self).items():
            if name in memeber_set:
                memeber_set.remove(name)
        if len(memeber_set) > 0:
            warnings.warn("%s fileds are useless." % ",".join(memeber_set))
        


class LakeFileSystemToken(AbstractModel):
    """LakeFileSystem使用的临时token

    """

    def __init__(self):
        r"""
        :param SecretId: Token使用的临时秘钥的ID
        :type SecretId: str
        :param SecretKey: Token使用的临时秘钥
        :type SecretKey: str
        :param Token: Token信息
        :type Token: str
        :param ExpiredTime: 过期时间
        :type ExpiredTime: int
        :param IssueTime: 颁布时间
        :type IssueTime: int
        :param AppId: 访问的App ID
注意：此字段可能返回 null，表示取不到有效值。
        :type AppId: str
        """
        self.SecretId = None
        self.SecretKey = None
        self.Token = None
        self.ExpiredTime = None
        self.IssueTime = None
        self.AppId = None


    def _deserialize(self, params):
        self.SecretId = params.get("SecretId")
        self.SecretKey = params.get("SecretKey")
        self.Token = params.get("Token")
        self.ExpiredTime = params.get("ExpiredTime")
        self.IssueTime = params.get("IssueTime")
        self.AppId = params.get("AppId")
        memeber_set = set(params.keys())
        for name, value in vars(self).items():
            if name in memeber_set:
                memeber_set.remove(name)
        if len(memeber_set) > 0:
            warnings.warn("%s fileds are useless." % ",".join(memeber_set))
        


class LakeFsInfo(AbstractModel):
    """描述DLC托管存储基本信息

    """

    def __init__(self):
        r"""
        :param Name: 托管存储名称
        :type Name: str
        :param Type: 托管存储类型
        :type Type: str
        :param SpaceUsedSize: 容量
        :type SpaceUsedSize: float
        :param CreateTimeStamp: 创建时候的时间戳
        :type CreateTimeStamp: int
        """
        self.Name = None
        self.Type = None
        self.SpaceUsedSize = None
        self.CreateTimeStamp = None


    def _deserialize(self, params):
        self.Name = params.get("Name")
        self.Type = params.get("Type")
        self.SpaceUsedSize = params.get("SpaceUsedSize")
        self.CreateTimeStamp = params.get("CreateTimeStamp")
        memeber_set = set(params.keys())
        for name, value in vars(self).items():
            if name in memeber_set:
                memeber_set.remove(name)
        if len(memeber_set) > 0:
            warnings.warn("%s fileds are useless." % ",".join(memeber_set))
        


class LakeFsSummary(AbstractModel):
    """托管存储Summary统计信息

    """

    def __init__(self):
        r"""
        :param Truncated: 是否是截断统计
        :type Truncated: bool
        :param TotalSubDirs: 子目录个数
        :type TotalSubDirs: int
        :param TotalFiles: 文件个数
        :type TotalFiles: int
        :param TotalBytes: 总文件大小字节数
        :type TotalBytes: int
        """
        self.Truncated = None
        self.TotalSubDirs = None
        self.TotalFiles = None
        self.TotalBytes = None


    def _deserialize(self, params):
        self.Truncated = params.get("Truncated")
        self.TotalSubDirs = params.get("TotalSubDirs")
        self.TotalFiles = params.get("TotalFiles")
        self.TotalBytes = params.get("TotalBytes")
        memeber_set = set(params.keys())
        for name, value in vars(self).items():
            if name in memeber_set:
                memeber_set.remove(name)
        if len(memeber_set) > 0:
            warnings.warn("%s fileds are useless." % ",".join(memeber_set))
        


class Link(AbstractModel):
    """任务依赖关系

    """

    def __init__(self):
        r"""
        :param TaskFrom: 父任务ID
        :type TaskFrom: str
        :param TaskTo: 子任务ID
        :type TaskTo: str
        :param WorkflowId: 调度计划ID
        :type WorkflowId: str
        :param Id: 依赖关系ID
        :type Id: str
        """
        self.TaskFrom = None
        self.TaskTo = None
        self.WorkflowId = None
        self.Id = None


    def _deserialize(self, params):
        self.TaskFrom = params.get("TaskFrom")
        self.TaskTo = params.get("TaskTo")
        self.WorkflowId = params.get("WorkflowId")
        self.Id = params.get("Id")
        memeber_set = set(params.keys())
        for name, value in vars(self).items():
            if name in memeber_set:
                memeber_set.remove(name)
        if len(memeber_set) > 0:
            warnings.warn("%s fileds are useless." % ",".join(memeber_set))
        


class ListDataEnginesRequest(AbstractModel):
    """ListDataEngines请求参数结构体

    """

    def __init__(self):
        r"""
        :param Offset: 偏移量，默认为0。
        :type Offset: int
        :param Filters: 滤类型，传参Name应为以下其中一个,
data-engine-name - String 
engine-type - String
state - String 
mode - String 
create-time - String 
message - String
        :type Filters: list of Filter
        :param SortBy: 排序字段，支持如下字段类型，create-time
        :type SortBy: str
        :param Sorting: 排序方式，desc表示正序，asc表示反序， 默认为asc。
        :type Sorting: str
        :param Limit: 返回数量，默认为10，最大值为100。
        :type Limit: int
        :param DatasourceConnectionName: 已废弃，请使用DatasourceConnectionNameSet
        :type DatasourceConnectionName: str
        :param ExcludePublicEngine: 是否不返回共享引擎，true不返回共享引擎，false可以返回共享引擎
        :type ExcludePublicEngine: bool
        :param AccessTypes: 参数应该为引擎权限类型，有效类型："USE", "MODIFY", "OPERATE", "MONITOR", "DELETE"
        :type AccessTypes: list of str
        :param EngineExecType: 引擎执行任务类型，有效值：SQL/BATCH
        :type EngineExecType: str
        :param EngineType: 引擎类型，有效值：spark/presto
        :type EngineType: str
        :param DatasourceConnectionNameSet: 网络配置列表，若传入该参数，则返回网络配置关联的计算引擎
        :type DatasourceConnectionNameSet: list of str
        """
        self.Offset = None
        self.Filters = None
        self.SortBy = None
        self.Sorting = None
        self.Limit = None
        self.DatasourceConnectionName = None
        self.ExcludePublicEngine = None
        self.AccessTypes = None
        self.EngineExecType = None
        self.EngineType = None
        self.DatasourceConnectionNameSet = None


    def _deserialize(self, params):
        self.Offset = params.get("Offset")
        if params.get("Filters") is not None:
            self.Filters = []
            for item in params.get("Filters"):
                obj = Filter()
                obj._deserialize(item)
                self.Filters.append(obj)
        self.SortBy = params.get("SortBy")
        self.Sorting = params.get("Sorting")
        self.Limit = params.get("Limit")
        self.DatasourceConnectionName = params.get("DatasourceConnectionName")
        self.ExcludePublicEngine = params.get("ExcludePublicEngine")
        self.AccessTypes = params.get("AccessTypes")
        self.EngineExecType = params.get("EngineExecType")
        self.EngineType = params.get("EngineType")
        self.DatasourceConnectionNameSet = params.get("DatasourceConnectionNameSet")
        memeber_set = set(params.keys())
        for name, value in vars(self).items():
            if name in memeber_set:
                memeber_set.remove(name)
        if len(memeber_set) > 0:
            warnings.warn("%s fileds are useless." % ",".join(memeber_set))
        


class ListDataEnginesResponse(AbstractModel):
    """ListDataEngines返回参数结构体

    """

    def __init__(self):
        r"""
        :param DataEngines: 数据引擎列表
注意：此字段可能返回 null，表示取不到有效值。
        :type DataEngines: list of DataEngineInfo
        :param TotalCount: 总条数
注意：此字段可能返回 null，表示取不到有效值。
        :type TotalCount: int
        :param RequestId: 唯一请求 ID，每次请求都会返回。定位问题时需要提供该次请求的 RequestId。
        :type RequestId: str
        """
        self.DataEngines = None
        self.TotalCount = None
        self.RequestId = None


    def _deserialize(self, params):
        if params.get("DataEngines") is not None:
            self.DataEngines = []
            for item in params.get("DataEngines"):
                obj = DataEngineInfo()
                obj._deserialize(item)
                self.DataEngines.append(obj)
        self.TotalCount = params.get("TotalCount")
        self.RequestId = params.get("RequestId")


class ListHouseRequest(AbstractModel):
    """ListHouse请求参数结构体

    """

    def __init__(self):
        r"""
        :param Offset: 偏移量，默认为0。
        :type Offset: int
        :param Filters: 滤类型，传参Name应为以下其中一个,
house-name - String 
engine-type - String
state - String 
mode - String 
create-time - String 
message - String
        :type Filters: list of Filter
        :param SortBy: 排序字段，支持如下字段类型，create-time
        :type SortBy: str
        :param Sorting: 排序方式，desc表示正序，asc表示反序， 默认为asc。
        :type Sorting: str
        :param Limit: 返回数量，默认为10，最大值为100。
        :type Limit: int
        """
        self.Offset = None
        self.Filters = None
        self.SortBy = None
        self.Sorting = None
        self.Limit = None


    def _deserialize(self, params):
        self.Offset = params.get("Offset")
        if params.get("Filters") is not None:
            self.Filters = []
            for item in params.get("Filters"):
                obj = Filter()
                obj._deserialize(item)
                self.Filters.append(obj)
        self.SortBy = params.get("SortBy")
        self.Sorting = params.get("Sorting")
        self.Limit = params.get("Limit")
        memeber_set = set(params.keys())
        for name, value in vars(self).items():
            if name in memeber_set:
                memeber_set.remove(name)
        if len(memeber_set) > 0:
            warnings.warn("%s fileds are useless." % ",".join(memeber_set))
        


class ListHouseResponse(AbstractModel):
    """ListHouse返回参数结构体

    """

    def __init__(self):
        r"""
        :param Houses: House信息列表
注意：此字段可能返回 null，表示取不到有效值。
        :type Houses: list of DataEngineInfo
        :param TotalCount: 总条数
注意：此字段可能返回 null，表示取不到有效值。
        :type TotalCount: int
        :param RequestId: 唯一请求 ID，每次请求都会返回。定位问题时需要提供该次请求的 RequestId。
        :type RequestId: str
        """
        self.Houses = None
        self.TotalCount = None
        self.RequestId = None


    def _deserialize(self, params):
        if params.get("Houses") is not None:
            self.Houses = []
            for item in params.get("Houses"):
                obj = DataEngineInfo()
                obj._deserialize(item)
                self.Houses.append(obj)
        self.TotalCount = params.get("TotalCount")
        self.RequestId = params.get("RequestId")


class ListTaskJobLogDetailRequest(AbstractModel):
    """ListTaskJobLogDetail请求参数结构体

    """

    def __init__(self):
        r"""
        :param TaskId: 列表返回的Id
        :type TaskId: str
        :param StartTime: 开始运行时间，unix时间戳（毫秒）
        :type StartTime: int
        :param EndTime: 结束运行时间，unix时间戳（毫秒）
        :type EndTime: int
        :param Limit: 分页大小，最大1000，配合Context一起使用
        :type Limit: int
        :param Context: 下一次分页参数，第一次传空
        :type Context: str
        :param Asc: 最近1000条日志是否升序排列，true:升序排序，false:倒序，默认false，倒序排列
        :type Asc: bool
        :param Filters: 预览日志的通用过滤条件
        :type Filters: list of Filter
        :param BatchId: SparkSQL任务唯一ID
        :type BatchId: str
        """
        self.TaskId = None
        self.StartTime = None
        self.EndTime = None
        self.Limit = None
        self.Context = None
        self.Asc = None
        self.Filters = None
        self.BatchId = None


    def _deserialize(self, params):
        self.TaskId = params.get("TaskId")
        self.StartTime = params.get("StartTime")
        self.EndTime = params.get("EndTime")
        self.Limit = params.get("Limit")
        self.Context = params.get("Context")
        self.Asc = params.get("Asc")
        if params.get("Filters") is not None:
            self.Filters = []
            for item in params.get("Filters"):
                obj = Filter()
                obj._deserialize(item)
                self.Filters.append(obj)
        self.BatchId = params.get("BatchId")
        memeber_set = set(params.keys())
        for name, value in vars(self).items():
            if name in memeber_set:
                memeber_set.remove(name)
        if len(memeber_set) > 0:
            warnings.warn("%s fileds are useless." % ",".join(memeber_set))
        


class ListTaskJobLogDetailResponse(AbstractModel):
    """ListTaskJobLogDetail返回参数结构体

    """

    def __init__(self):
        r"""
        :param Context: 下一次分页参数
注意：此字段可能返回 null，表示取不到有效值。
        :type Context: str
        :param ListOver: 是否获取完结
注意：此字段可能返回 null，表示取不到有效值。
        :type ListOver: bool
        :param Results: 日志详情
注意：此字段可能返回 null，表示取不到有效值。
        :type Results: list of JobLogResult
        :param LogUrl: 日志url
注意：此字段可能返回 null，表示取不到有效值。
        :type LogUrl: str
        :param RequestId: 唯一请求 ID，每次请求都会返回。定位问题时需要提供该次请求的 RequestId。
        :type RequestId: str
        """
        self.Context = None
        self.ListOver = None
        self.Results = None
        self.LogUrl = None
        self.RequestId = None


    def _deserialize(self, params):
        self.Context = params.get("Context")
        self.ListOver = params.get("ListOver")
        if params.get("Results") is not None:
            self.Results = []
            for item in params.get("Results"):
                obj = JobLogResult()
                obj._deserialize(item)
                self.Results.append(obj)
        self.LogUrl = params.get("LogUrl")
        self.RequestId = params.get("RequestId")


class ListTaskJobLogNameRequest(AbstractModel):
    """ListTaskJobLogName请求参数结构体

    """

    def __init__(self):
        r"""
        :param TaskId: 查询的taskId
        :type TaskId: str
        :param BatchId: SparkSQL批任务唯一ID
        :type BatchId: str
        """
        self.TaskId = None
        self.BatchId = None


    def _deserialize(self, params):
        self.TaskId = params.get("TaskId")
        self.BatchId = params.get("BatchId")
        memeber_set = set(params.keys())
        for name, value in vars(self).items():
            if name in memeber_set:
                memeber_set.remove(name)
        if len(memeber_set) > 0:
            warnings.warn("%s fileds are useless." % ",".join(memeber_set))
        


class ListTaskJobLogNameResponse(AbstractModel):
    """ListTaskJobLogName返回参数结构体

    """

    def __init__(self):
        r"""
        :param Names: 日志名称列表
        :type Names: list of str
        :param TopicId: 日志topic
        :type TopicId: str
        :param RequestId: 唯一请求 ID，每次请求都会返回。定位问题时需要提供该次请求的 RequestId。
        :type RequestId: str
        """
        self.Names = None
        self.TopicId = None
        self.RequestId = None


    def _deserialize(self, params):
        self.Names = params.get("Names")
        self.TopicId = params.get("TopicId")
        self.RequestId = params.get("RequestId")


class ListWorkflowRequest(AbstractModel):
    """ListWorkflow请求参数结构体

    """

    def __init__(self):
        r"""
        :param Limit: 个数限制，默认无限制
        :type Limit: int
        :param Offset: 偏移量，默认为0。
        :type Offset: int
        :param Filters: 过滤条件
        :type Filters: list of Filter
        """
        self.Limit = None
        self.Offset = None
        self.Filters = None


    def _deserialize(self, params):
        self.Limit = params.get("Limit")
        self.Offset = params.get("Offset")
        if params.get("Filters") is not None:
            self.Filters = []
            for item in params.get("Filters"):
                obj = Filter()
                obj._deserialize(item)
                self.Filters.append(obj)
        memeber_set = set(params.keys())
        for name, value in vars(self).items():
            if name in memeber_set:
                memeber_set.remove(name)
        if len(memeber_set) > 0:
            warnings.warn("%s fileds are useless." % ",".join(memeber_set))
        


class ListWorkflowResponse(AbstractModel):
    """ListWorkflow返回参数结构体

    """

    def __init__(self):
        r"""
        :param WorkflowInfo: 调度计划列表
注意：此字段可能返回 null，表示取不到有效值。
        :type WorkflowInfo: list of WorkflowInfo
        :param TotalCount: workflow总数
注意：此字段可能返回 null，表示取不到有效值。
        :type TotalCount: int
        :param RequestId: 唯一请求 ID，每次请求都会返回。定位问题时需要提供该次请求的 RequestId。
        :type RequestId: str
        """
        self.WorkflowInfo = None
        self.TotalCount = None
        self.RequestId = None


    def _deserialize(self, params):
        if params.get("WorkflowInfo") is not None:
            self.WorkflowInfo = []
            for item in params.get("WorkflowInfo"):
                obj = WorkflowInfo()
                obj._deserialize(item)
                self.WorkflowInfo.append(obj)
        self.TotalCount = params.get("TotalCount")
        self.RequestId = params.get("RequestId")


class LockComponentInfo(AbstractModel):
    """元数据加锁内容

    """

    def __init__(self):
        r"""
        :param DbName: 数据库名称
        :type DbName: str
        :param TableName: 表名称
        :type TableName: str
        :param Partition: 分区
        :type Partition: str
        :param LockType: 锁类型：SHARED_READ、SHARED_WRITE、EXCLUSIVE
        :type LockType: str
        :param LockLevel: 锁级别：DB、TABLE、PARTITION
        :type LockLevel: str
        :param DataOperationType: 锁操作：SELECT,INSERT,UPDATE,DELETE,UNSET,NO_TXN
        :type DataOperationType: str
        :param IsAcid: 是否保持Acid
        :type IsAcid: bool
        :param IsDynamicPartitionWrite: 是否动态分区写
        :type IsDynamicPartitionWrite: bool
        """
        self.DbName = None
        self.TableName = None
        self.Partition = None
        self.LockType = None
        self.LockLevel = None
        self.DataOperationType = None
        self.IsAcid = None
        self.IsDynamicPartitionWrite = None


    def _deserialize(self, params):
        self.DbName = params.get("DbName")
        self.TableName = params.get("TableName")
        self.Partition = params.get("Partition")
        self.LockType = params.get("LockType")
        self.LockLevel = params.get("LockLevel")
        self.DataOperationType = params.get("DataOperationType")
        self.IsAcid = params.get("IsAcid")
        self.IsDynamicPartitionWrite = params.get("IsDynamicPartitionWrite")
        memeber_set = set(params.keys())
        for name, value in vars(self).items():
            if name in memeber_set:
                memeber_set.remove(name)
        if len(memeber_set) > 0:
            warnings.warn("%s fileds are useless." % ",".join(memeber_set))
        


class LockMetaDataRequest(AbstractModel):
    """LockMetaData请求参数结构体

    """

    def __init__(self):
        r"""
        :param LockComponentList: 加锁内容
        :type LockComponentList: list of LockComponentInfo
        :param DatasourceConnectionName: 数据源名称
        :type DatasourceConnectionName: str
        :param TxnId: 事务id
        :type TxnId: int
        :param AgentInfo: 客户端信息
        :type AgentInfo: str
        :param Hostname: 主机名
        :type Hostname: str
        """
        self.LockComponentList = None
        self.DatasourceConnectionName = None
        self.TxnId = None
        self.AgentInfo = None
        self.Hostname = None


    def _deserialize(self, params):
        if params.get("LockComponentList") is not None:
            self.LockComponentList = []
            for item in params.get("LockComponentList"):
                obj = LockComponentInfo()
                obj._deserialize(item)
                self.LockComponentList.append(obj)
        self.DatasourceConnectionName = params.get("DatasourceConnectionName")
        self.TxnId = params.get("TxnId")
        self.AgentInfo = params.get("AgentInfo")
        self.Hostname = params.get("Hostname")
        memeber_set = set(params.keys())
        for name, value in vars(self).items():
            if name in memeber_set:
                memeber_set.remove(name)
        if len(memeber_set) > 0:
            warnings.warn("%s fileds are useless." % ",".join(memeber_set))
        


class LockMetaDataResponse(AbstractModel):
    """LockMetaData返回参数结构体

    """

    def __init__(self):
        r"""
        :param LockId: 锁id
        :type LockId: int
        :param LockState: 锁状态：ACQUIRED、WAITING、ABORT、NOT_ACQUIRED
        :type LockState: str
        :param RequestId: 唯一请求 ID，每次请求都会返回。定位问题时需要提供该次请求的 RequestId。
        :type RequestId: str
        """
        self.LockId = None
        self.LockState = None
        self.RequestId = None


    def _deserialize(self, params):
        self.LockId = params.get("LockId")
        self.LockState = params.get("LockState")
        self.RequestId = params.get("RequestId")


class LookupAttribute(AbstractModel):
    """审计事件查询条件数组

    """

    def __init__(self):
        r"""
        :param AttributeKey: PrincipalId：子账号，EventType：事件名称
        :type AttributeKey: str
        :param AttributeValue: xxx
        :type AttributeValue: str
        """
        self.AttributeKey = None
        self.AttributeValue = None


    def _deserialize(self, params):
        self.AttributeKey = params.get("AttributeKey")
        self.AttributeValue = params.get("AttributeValue")
        memeber_set = set(params.keys())
        for name, value in vars(self).items():
            if name in memeber_set:
                memeber_set.remove(name)
        if len(memeber_set) > 0:
            warnings.warn("%s fileds are useless." % ",".join(memeber_set))
        


class MainDataDataEngineStat(AbstractModel):
    """概览页数据引擎相关数据

    """

    def __init__(self):
        r"""
        :param StatDate: 统计日期
        :type StatDate: str
        :param DataEngineCnt: 独享引擎数量
        :type DataEngineCnt: int
        :param ExpiringDataEngineCnt: 7日内过期的引擎数量
        :type ExpiringDataEngineCnt: int
        :param IsolateDataEngineCnt: 隔离引擎数量
        :type IsolateDataEngineCnt: int
        :param TaskCntWeek: 7日内独享引擎运行任务数
        :type TaskCntWeek: int
        :param AvgTaskUseTimeWeek: 7日内独享引擎运行任务平均运行时长，ms
        :type AvgTaskUseTimeWeek: float
        :param ElasticCusWeek: 7日内集群使用CU时
        :type ElasticCusWeek: float
        """
        self.StatDate = None
        self.DataEngineCnt = None
        self.ExpiringDataEngineCnt = None
        self.IsolateDataEngineCnt = None
        self.TaskCntWeek = None
        self.AvgTaskUseTimeWeek = None
        self.ElasticCusWeek = None


    def _deserialize(self, params):
        self.StatDate = params.get("StatDate")
        self.DataEngineCnt = params.get("DataEngineCnt")
        self.ExpiringDataEngineCnt = params.get("ExpiringDataEngineCnt")
        self.IsolateDataEngineCnt = params.get("IsolateDataEngineCnt")
        self.TaskCntWeek = params.get("TaskCntWeek")
        self.AvgTaskUseTimeWeek = params.get("AvgTaskUseTimeWeek")
        self.ElasticCusWeek = params.get("ElasticCusWeek")
        memeber_set = set(params.keys())
        for name, value in vars(self).items():
            if name in memeber_set:
                memeber_set.remove(name)
        if len(memeber_set) > 0:
            warnings.warn("%s fileds are useless." % ",".join(memeber_set))
        


class MainShareLine(AbstractModel):
    """共享引擎折线图数据

    """

    def __init__(self):
        r"""
        :param Hour: 小时数
注意：此字段可能返回 null，表示取不到有效值。
        :type Hour: int
        :param Count: 任务数量
注意：此字段可能返回 null，表示取不到有效值。
        :type Count: int
        """
        self.Hour = None
        self.Count = None


    def _deserialize(self, params):
        self.Hour = params.get("Hour")
        self.Count = params.get("Count")
        memeber_set = set(params.keys())
        for name, value in vars(self).items():
            if name in memeber_set:
                memeber_set.remove(name)
        if len(memeber_set) > 0:
            warnings.warn("%s fileds are useless." % ",".join(memeber_set))
        


class MainTaskData(AbstractModel):
    """任务监控-折线图数据

    """

    def __init__(self):
        r"""
        :param Total: 任务总数
注意：此字段可能返回 null，表示取不到有效值。
        :type Total: int
        :param DayStart: 开始日期
注意：此字段可能返回 null，表示取不到有效值。
        :type DayStart: str
        :param DayEnd: 结束日期
注意：此字段可能返回 null，表示取不到有效值。
        :type DayEnd: str
        :param Lines: 每日任务数据
注意：此字段可能返回 null，表示取不到有效值。
        :type Lines: list of MainTaskDataLine
        """
        self.Total = None
        self.DayStart = None
        self.DayEnd = None
        self.Lines = None


    def _deserialize(self, params):
        self.Total = params.get("Total")
        self.DayStart = params.get("DayStart")
        self.DayEnd = params.get("DayEnd")
        if params.get("Lines") is not None:
            self.Lines = []
            for item in params.get("Lines"):
                obj = MainTaskDataLine()
                obj._deserialize(item)
                self.Lines.append(obj)
        memeber_set = set(params.keys())
        for name, value in vars(self).items():
            if name in memeber_set:
                memeber_set.remove(name)
        if len(memeber_set) > 0:
            warnings.warn("%s fileds are useless." % ",".join(memeber_set))
        


class MainTaskDataLine(AbstractModel):
    """任务监控-折线图数据明细

    """

    def __init__(self):
        r"""
        :param Day: 日期
注意：此字段可能返回 null，表示取不到有效值。
        :type Day: str
        :param Count: 任务数
注意：此字段可能返回 null，表示取不到有效值。
        :type Count: int
        """
        self.Day = None
        self.Count = None


    def _deserialize(self, params):
        self.Day = params.get("Day")
        self.Count = params.get("Count")
        memeber_set = set(params.keys())
        for name, value in vars(self).items():
            if name in memeber_set:
                memeber_set.remove(name)
        if len(memeber_set) > 0:
            warnings.warn("%s fileds are useless." % ",".join(memeber_set))
        


class MainViewData(AbstractModel):
    """首页概览数据

    """

    def __init__(self):
        r"""
        :param StorageAmount: 数据存储量
注意：此字段可能返回 null，表示取不到有效值。
        :type StorageAmount: str
        :param PrivateEngineCount: 独享数据引擎个数
注意：此字段可能返回 null，表示取不到有效值。
        :type PrivateEngineCount: int
        :param YesterdayCuCount: 昨日CU时用量
注意：此字段可能返回 null，表示取不到有效值。
        :type YesterdayCuCount: float
        :param LakeFsStorageAmount: 托管存储用量
注意：此字段可能返回 null，表示取不到有效值。
        :type LakeFsStorageAmount: str
        """
        self.StorageAmount = None
        self.PrivateEngineCount = None
        self.YesterdayCuCount = None
        self.LakeFsStorageAmount = None


    def _deserialize(self, params):
        self.StorageAmount = params.get("StorageAmount")
        self.PrivateEngineCount = params.get("PrivateEngineCount")
        self.YesterdayCuCount = params.get("YesterdayCuCount")
        self.LakeFsStorageAmount = params.get("LakeFsStorageAmount")
        memeber_set = set(params.keys())
        for name, value in vars(self).items():
            if name in memeber_set:
                memeber_set.remove(name)
        if len(memeber_set) > 0:
            warnings.warn("%s fileds are useless." % ",".join(memeber_set))
        


class MainViewLine(AbstractModel):
    """首页CU时折线数据

    """

    def __init__(self):
        r"""
        :param Day: 日期
注意：此字段可能返回 null，表示取不到有效值。
        :type Day: str
        :param Count: CU时用量
注意：此字段可能返回 null，表示取不到有效值。
        :type Count: float
        """
        self.Day = None
        self.Count = None


    def _deserialize(self, params):
        self.Day = params.get("Day")
        self.Count = params.get("Count")
        memeber_set = set(params.keys())
        for name, value in vars(self).items():
            if name in memeber_set:
                memeber_set.remove(name)
        if len(memeber_set) > 0:
            warnings.warn("%s fileds are useless." % ",".join(memeber_set))
        


class MergeManifestsInfo(AbstractModel):
    """合并元数据Manifests文件数据治理项信息

    """

    def __init__(self):
        r"""
        :param MergeManifestsEnable: 是否启用合并元数据Manifests文件治理项：enable、none
        :type MergeManifestsEnable: str
        :param Engine: 用于运行合并元数据Manifests文件治理项的引擎名称
        :type Engine: str
        :param IntervalMin: 合并元数据Manifests文件治理运行周期，单位为分钟
        :type IntervalMin: int
        """
        self.MergeManifestsEnable = None
        self.Engine = None
        self.IntervalMin = None


    def _deserialize(self, params):
        self.MergeManifestsEnable = params.get("MergeManifestsEnable")
        self.Engine = params.get("Engine")
        self.IntervalMin = params.get("IntervalMin")
        memeber_set = set(params.keys())
        for name, value in vars(self).items():
            if name in memeber_set:
                memeber_set.remove(name)
        if len(memeber_set) > 0:
            warnings.warn("%s fileds are useless." % ",".join(memeber_set))
        


class MetaDatabaseInfo(AbstractModel):
    """元数据库基本信息

    """

    def __init__(self):
        r"""
        :param DatabaseName: 数据库名称。
        :type DatabaseName: str
        :param Comment: 数据库描述信息，长度 0~2048。
注意：此字段可能返回 null，表示取不到有效值。
        :type Comment: str
        :param Location: 数据库cos路径
注意：此字段可能返回 null，表示取不到有效值。
        :type Location: str
        """
        self.DatabaseName = None
        self.Comment = None
        self.Location = None


    def _deserialize(self, params):
        self.DatabaseName = params.get("DatabaseName")
        self.Comment = params.get("Comment")
        self.Location = params.get("Location")
        memeber_set = set(params.keys())
        for name, value in vars(self).items():
            if name in memeber_set:
                memeber_set.remove(name)
        if len(memeber_set) > 0:
            warnings.warn("%s fileds are useless." % ",".join(memeber_set))
        


class MetaKeyConstraint(AbstractModel):
    """元数据约束

    """

    def __init__(self):
        r"""
        :param DatabaseId: 数据库主键
注意：此字段可能返回 null，表示取不到有效值。
        :type DatabaseId: int
        :param DatabaseName: 数据库名册个
注意：此字段可能返回 null，表示取不到有效值。
        :type DatabaseName: str
        :param ParentTableId: tbl数据表id
注意：此字段可能返回 null，表示取不到有效值。
        :type ParentTableId: int
        :param TableName: 数据表名称
注意：此字段可能返回 null，表示取不到有效值。
        :type TableName: str
        :param ChildCdId: 字段主键
注意：此字段可能返回 null，表示取不到有效值。
        :type ChildCdId: int
        :param ChildIntegerIndex: 子索引
注意：此字段可能返回 null，表示取不到有效值。
        :type ChildIntegerIndex: int
        :param ChildTableId: 子表主键
注意：此字段可能返回 null，表示取不到有效值。
        :type ChildTableId: int
        :param ParentCdId: 字段id
注意：此字段可能返回 null，表示取不到有效值。
        :type ParentCdId: int
        :param ParentIntegerIndex: 父索引
注意：此字段可能返回 null，表示取不到有效值。
        :type ParentIntegerIndex: int
        :param Position: 位置
注意：此字段可能返回 null，表示取不到有效值。
        :type Position: int
        :param ConstraintName: 约束名称
注意：此字段可能返回 null，表示取不到有效值。
        :type ConstraintName: str
        :param ConstraintType: 约束类型
注意：此字段可能返回 null，表示取不到有效值。
        :type ConstraintType: str
        :param UpdateRule: 更新规则
注意：此字段可能返回 null，表示取不到有效值。
        :type UpdateRule: int
        :param DeleteRule: 删除规则
注意：此字段可能返回 null，表示取不到有效值。
        :type DeleteRule: int
        :param EnableValidateRely: 是否启用验证
注意：此字段可能返回 null，表示取不到有效值。
        :type EnableValidateRely: int
        :param ParentColumnName: 父列名
注意：此字段可能返回 null，表示取不到有效值。
        :type ParentColumnName: str
        """
        self.DatabaseId = None
        self.DatabaseName = None
        self.ParentTableId = None
        self.TableName = None
        self.ChildCdId = None
        self.ChildIntegerIndex = None
        self.ChildTableId = None
        self.ParentCdId = None
        self.ParentIntegerIndex = None
        self.Position = None
        self.ConstraintName = None
        self.ConstraintType = None
        self.UpdateRule = None
        self.DeleteRule = None
        self.EnableValidateRely = None
        self.ParentColumnName = None


    def _deserialize(self, params):
        self.DatabaseId = params.get("DatabaseId")
        self.DatabaseName = params.get("DatabaseName")
        self.ParentTableId = params.get("ParentTableId")
        self.TableName = params.get("TableName")
        self.ChildCdId = params.get("ChildCdId")
        self.ChildIntegerIndex = params.get("ChildIntegerIndex")
        self.ChildTableId = params.get("ChildTableId")
        self.ParentCdId = params.get("ParentCdId")
        self.ParentIntegerIndex = params.get("ParentIntegerIndex")
        self.Position = params.get("Position")
        self.ConstraintName = params.get("ConstraintName")
        self.ConstraintType = params.get("ConstraintType")
        self.UpdateRule = params.get("UpdateRule")
        self.DeleteRule = params.get("DeleteRule")
        self.EnableValidateRely = params.get("EnableValidateRely")
        self.ParentColumnName = params.get("ParentColumnName")
        memeber_set = set(params.keys())
        for name, value in vars(self).items():
            if name in memeber_set:
                memeber_set.remove(name)
        if len(memeber_set) > 0:
            warnings.warn("%s fileds are useless." % ",".join(memeber_set))
        


class MigrateDatasourceConnectionRequest(AbstractModel):
    """MigrateDatasourceConnection请求参数结构体

    """

    def __init__(self):
        r"""
        :param VpcCidrBlock: VPC的CIDR
        :type VpcCidrBlock: str
        :param DataEngineName: 迁移虚拟集群的名称
        :type DataEngineName: str
        """
        self.VpcCidrBlock = None
        self.DataEngineName = None


    def _deserialize(self, params):
        self.VpcCidrBlock = params.get("VpcCidrBlock")
        self.DataEngineName = params.get("DataEngineName")
        memeber_set = set(params.keys())
        for name, value in vars(self).items():
            if name in memeber_set:
                memeber_set.remove(name)
        if len(memeber_set) > 0:
            warnings.warn("%s fileds are useless." % ",".join(memeber_set))
        


class MigrateDatasourceConnectionResponse(AbstractModel):
    """MigrateDatasourceConnection返回参数结构体

    """

    def __init__(self):
        r"""
        :param RequestId: 唯一请求 ID，每次请求都会返回。定位问题时需要提供该次请求的 RequestId。
        :type RequestId: str
        """
        self.RequestId = None


    def _deserialize(self, params):
        self.RequestId = params.get("RequestId")


class ModifyAdvancedStoreLocationRequest(AbstractModel):
    """ModifyAdvancedStoreLocation请求参数结构体

    """

    def __init__(self):
        r"""
        :param StoreLocation: 查询结果保存cos路径
        :type StoreLocation: str
        :param Enable: 是否启用高级设置：0-否，1-是
        :type Enable: int
        """
        self.StoreLocation = None
        self.Enable = None


    def _deserialize(self, params):
        self.StoreLocation = params.get("StoreLocation")
        self.Enable = params.get("Enable")
        memeber_set = set(params.keys())
        for name, value in vars(self).items():
            if name in memeber_set:
                memeber_set.remove(name)
        if len(memeber_set) > 0:
            warnings.warn("%s fileds are useless." % ",".join(memeber_set))
        


class ModifyAdvancedStoreLocationResponse(AbstractModel):
    """ModifyAdvancedStoreLocation返回参数结构体

    """

    def __init__(self):
        r"""
        :param RequestId: 唯一请求 ID，每次请求都会返回。定位问题时需要提供该次请求的 RequestId。
        :type RequestId: str
        """
        self.RequestId = None


    def _deserialize(self, params):
        self.RequestId = params.get("RequestId")


class ModifyCHDFSMountPointAssociateInfoRequest(AbstractModel):
    """ModifyCHDFSMountPointAssociateInfo请求参数结构体

    """

    def __init__(self):
        r"""
        :param MountPointAssociateInfos: 挂载点绑定信息
        :type MountPointAssociateInfos: list of MountPointAssociateInfo
        """
        self.MountPointAssociateInfos = None


    def _deserialize(self, params):
        if params.get("MountPointAssociateInfos") is not None:
            self.MountPointAssociateInfos = []
            for item in params.get("MountPointAssociateInfos"):
                obj = MountPointAssociateInfo()
                obj._deserialize(item)
                self.MountPointAssociateInfos.append(obj)
        memeber_set = set(params.keys())
        for name, value in vars(self).items():
            if name in memeber_set:
                memeber_set.remove(name)
        if len(memeber_set) > 0:
            warnings.warn("%s fileds are useless." % ",".join(memeber_set))
        


class ModifyCHDFSMountPointAssociateInfoResponse(AbstractModel):
    """ModifyCHDFSMountPointAssociateInfo返回参数结构体

    """

    def __init__(self):
        r"""
        :param Result: 修改结果
        :type Result: bool
        :param RequestId: 唯一请求 ID，每次请求都会返回。定位问题时需要提供该次请求的 RequestId。
        :type RequestId: str
        """
        self.Result = None
        self.RequestId = None


    def _deserialize(self, params):
        self.Result = params.get("Result")
        self.RequestId = params.get("RequestId")


class ModifyCHDFSMountPointSuperuserRequest(AbstractModel):
    """ModifyCHDFSMountPointSuperuser请求参数结构体

    """

    def __init__(self):
        r"""
        :param BucketId: 桶id
        :type BucketId: str
        :param Superuser: superuser列表
        :type Superuser: list of str
        """
        self.BucketId = None
        self.Superuser = None


    def _deserialize(self, params):
        self.BucketId = params.get("BucketId")
        self.Superuser = params.get("Superuser")
        memeber_set = set(params.keys())
        for name, value in vars(self).items():
            if name in memeber_set:
                memeber_set.remove(name)
        if len(memeber_set) > 0:
            warnings.warn("%s fileds are useless." % ",".join(memeber_set))
        


class ModifyCHDFSMountPointSuperuserResponse(AbstractModel):
    """ModifyCHDFSMountPointSuperuser返回参数结构体

    """

    def __init__(self):
        r"""
        :param RequestId: 唯一请求 ID，每次请求都会返回。定位问题时需要提供该次请求的 RequestId。
        :type RequestId: str
        """
        self.RequestId = None


    def _deserialize(self, params):
        self.RequestId = params.get("RequestId")


class ModifyCHDFSProductRequest(AbstractModel):
    """ModifyCHDFSProduct请求参数结构体

    """

    def __init__(self):
        r"""
        :param ProductName: 产品名称
        :type ProductName: str
        :param SuperUser: 超级用户名称数组
        :type SuperUser: list of str
        :param VpcInfo: vpc配置信息数组
        :type VpcInfo: list of CHDFSProductVpcInfo
        """
        self.ProductName = None
        self.SuperUser = None
        self.VpcInfo = None


    def _deserialize(self, params):
        self.ProductName = params.get("ProductName")
        self.SuperUser = params.get("SuperUser")
        if params.get("VpcInfo") is not None:
            self.VpcInfo = []
            for item in params.get("VpcInfo"):
                obj = CHDFSProductVpcInfo()
                obj._deserialize(item)
                self.VpcInfo.append(obj)
        memeber_set = set(params.keys())
        for name, value in vars(self).items():
            if name in memeber_set:
                memeber_set.remove(name)
        if len(memeber_set) > 0:
            warnings.warn("%s fileds are useless." % ",".join(memeber_set))
        


class ModifyCHDFSProductResponse(AbstractModel):
    """ModifyCHDFSProduct返回参数结构体

    """

    def __init__(self):
        r"""
        :param RequestId: 唯一请求 ID，每次请求都会返回。定位问题时需要提供该次请求的 RequestId。
        :type RequestId: str
        """
        self.RequestId = None


    def _deserialize(self, params):
        self.RequestId = params.get("RequestId")


class ModifyDataEngineDescriptionRequest(AbstractModel):
    """ModifyDataEngineDescription请求参数结构体

    """

    def __init__(self):
        r"""
        :param DataEngineName: 要修改的引擎的名称
        :type DataEngineName: str
        :param Message: 引擎的描述信息，最大长度为250
        :type Message: str
        """
        self.DataEngineName = None
        self.Message = None


    def _deserialize(self, params):
        self.DataEngineName = params.get("DataEngineName")
        self.Message = params.get("Message")
        memeber_set = set(params.keys())
        for name, value in vars(self).items():
            if name in memeber_set:
                memeber_set.remove(name)
        if len(memeber_set) > 0:
            warnings.warn("%s fileds are useless." % ",".join(memeber_set))
        


class ModifyDataEngineDescriptionResponse(AbstractModel):
    """ModifyDataEngineDescription返回参数结构体

    """

    def __init__(self):
        r"""
        :param RequestId: 唯一请求 ID，每次请求都会返回。定位问题时需要提供该次请求的 RequestId。
        :type RequestId: str
        """
        self.RequestId = None


    def _deserialize(self, params):
        self.RequestId = params.get("RequestId")


class ModifyDatabaseUDFRequest(AbstractModel):
    """ModifyDatabaseUDF请求参数结构体

    """

    def __init__(self):
        r"""
        :param DatabaseName: 数据库名称
        :type DatabaseName: str
        :param Name: udf名称
        :type Name: str
        :param StoreType: 存储方式：1-上传到系统保存，2-指定cos挂载
        :type StoreType: int
        :param PackageSource: 程序包来源：1-本地上传，2-数据存储cos
        :type PackageSource: int
        :param PackagePath: cos路径
        :type PackagePath: str
        :param PackageName: jar包名称
        :type PackageName: str
        :param MainClass: 主类
        :type MainClass: str
        :param Id: 主键id
        :type Id: int
        :param Description: 描述
        :type Description: str
        :param DataEngineName: udf对应的spark计算资源
        :type DataEngineName: str
        """
        self.DatabaseName = None
        self.Name = None
        self.StoreType = None
        self.PackageSource = None
        self.PackagePath = None
        self.PackageName = None
        self.MainClass = None
        self.Id = None
        self.Description = None
        self.DataEngineName = None


    def _deserialize(self, params):
        self.DatabaseName = params.get("DatabaseName")
        self.Name = params.get("Name")
        self.StoreType = params.get("StoreType")
        self.PackageSource = params.get("PackageSource")
        self.PackagePath = params.get("PackagePath")
        self.PackageName = params.get("PackageName")
        self.MainClass = params.get("MainClass")
        self.Id = params.get("Id")
        self.Description = params.get("Description")
        self.DataEngineName = params.get("DataEngineName")
        memeber_set = set(params.keys())
        for name, value in vars(self).items():
            if name in memeber_set:
                memeber_set.remove(name)
        if len(memeber_set) > 0:
            warnings.warn("%s fileds are useless." % ",".join(memeber_set))
        


class ModifyDatabaseUDFResponse(AbstractModel):
    """ModifyDatabaseUDF返回参数结构体

    """

    def __init__(self):
        r"""
        :param BatchId: 任务提交批次id
注意：此字段可能返回 null，表示取不到有效值。
        :type BatchId: str
        :param TaskIdSet: 任务批次对应的每个taskId
注意：此字段可能返回 null，表示取不到有效值。
        :type TaskIdSet: list of str
        :param RequestId: 唯一请求 ID，每次请求都会返回。定位问题时需要提供该次请求的 RequestId。
        :type RequestId: str
        """
        self.BatchId = None
        self.TaskIdSet = None
        self.RequestId = None


    def _deserialize(self, params):
        self.BatchId = params.get("BatchId")
        self.TaskIdSet = params.get("TaskIdSet")
        self.RequestId = params.get("RequestId")


class ModifyDatasourceConnectionRequest(AbstractModel):
    """ModifyDatasourceConnection请求参数结构体

    """

    def __init__(self):
        r"""
        :param DatasourceConnectionId: 数据连接的唯一Id
        :type DatasourceConnectionId: str
        :param DatasourceConnectionDesc: 数据连接描述
        :type DatasourceConnectionDesc: str
        :param DatasourceConnectionConfig: 数据连接属性，数据源的具体配置，如mysql的信息、Hive的信息等。
        :type DatasourceConnectionConfig: :class:`tencentcloud.dlc.v20210125.models.DatasourceConnectionConfig`
        :param DataEngineNames: 数据源需要绑定的计算资源名称
        :type DataEngineNames: list of str
        """
        self.DatasourceConnectionId = None
        self.DatasourceConnectionDesc = None
        self.DatasourceConnectionConfig = None
        self.DataEngineNames = None


    def _deserialize(self, params):
        self.DatasourceConnectionId = params.get("DatasourceConnectionId")
        self.DatasourceConnectionDesc = params.get("DatasourceConnectionDesc")
        if params.get("DatasourceConnectionConfig") is not None:
            self.DatasourceConnectionConfig = DatasourceConnectionConfig()
            self.DatasourceConnectionConfig._deserialize(params.get("DatasourceConnectionConfig"))
        self.DataEngineNames = params.get("DataEngineNames")
        memeber_set = set(params.keys())
        for name, value in vars(self).items():
            if name in memeber_set:
                memeber_set.remove(name)
        if len(memeber_set) > 0:
            warnings.warn("%s fileds are useless." % ",".join(memeber_set))
        


class ModifyDatasourceConnectionResponse(AbstractModel):
    """ModifyDatasourceConnection返回参数结构体

    """

    def __init__(self):
        r"""
        :param RequestId: 唯一请求 ID，每次请求都会返回。定位问题时需要提供该次请求的 RequestId。
        :type RequestId: str
        """
        self.RequestId = None


    def _deserialize(self, params):
        self.RequestId = params.get("RequestId")


class ModifyGovernEventRuleRequest(AbstractModel):
    """ModifyGovernEventRule请求参数结构体

    """

    def __init__(self):
        r"""
        :param Name: 数据治理事件阈值名称
        :type Name: str
        :param Rule: 数据治理事件阈值
        :type Rule: :class:`tencentcloud.dlc.v20210125.models.RuleThreshold`
        """
        self.Name = None
        self.Rule = None


    def _deserialize(self, params):
        self.Name = params.get("Name")
        if params.get("Rule") is not None:
            self.Rule = RuleThreshold()
            self.Rule._deserialize(params.get("Rule"))
        memeber_set = set(params.keys())
        for name, value in vars(self).items():
            if name in memeber_set:
                memeber_set.remove(name)
        if len(memeber_set) > 0:
            warnings.warn("%s fileds are useless." % ",".join(memeber_set))
        


class ModifyGovernEventRuleResponse(AbstractModel):
    """ModifyGovernEventRule返回参数结构体

    """

    def __init__(self):
        r"""
        :param RequestId: 唯一请求 ID，每次请求都会返回。定位问题时需要提供该次请求的 RequestId。
        :type RequestId: str
        """
        self.RequestId = None


    def _deserialize(self, params):
        self.RequestId = params.get("RequestId")


class ModifyMetaDatabaseRequest(AbstractModel):
    """ModifyMetaDatabase请求参数结构体

    """

    def __init__(self):
        r"""
        :param MetaDatabaseInfo: 元数据库基本信息
        :type MetaDatabaseInfo: :class:`tencentcloud.dlc.v20210125.models.MetaDatabaseInfo`
        :param DatasourceConnectionName: 数据源名称，默认DataLakeCatalog
        :type DatasourceConnectionName: str
        :param GovernPolicy: 数据治理配置项
        :type GovernPolicy: :class:`tencentcloud.dlc.v20210125.models.DataGovernPolicy`
        """
        self.MetaDatabaseInfo = None
        self.DatasourceConnectionName = None
        self.GovernPolicy = None


    def _deserialize(self, params):
        if params.get("MetaDatabaseInfo") is not None:
            self.MetaDatabaseInfo = MetaDatabaseInfo()
            self.MetaDatabaseInfo._deserialize(params.get("MetaDatabaseInfo"))
        self.DatasourceConnectionName = params.get("DatasourceConnectionName")
        if params.get("GovernPolicy") is not None:
            self.GovernPolicy = DataGovernPolicy()
            self.GovernPolicy._deserialize(params.get("GovernPolicy"))
        memeber_set = set(params.keys())
        for name, value in vars(self).items():
            if name in memeber_set:
                memeber_set.remove(name)
        if len(memeber_set) > 0:
            warnings.warn("%s fileds are useless." % ",".join(memeber_set))
        


class ModifyMetaDatabaseResponse(AbstractModel):
    """ModifyMetaDatabase返回参数结构体

    """

    def __init__(self):
        r"""
        :param BatchId: 本批次提交的任务的批次Id
        :type BatchId: str
        :param TaskIdSet: 任务Id集合，按照执行顺序排列
        :type TaskIdSet: list of str
        :param RequestId: 唯一请求 ID，每次请求都会返回。定位问题时需要提供该次请求的 RequestId。
        :type RequestId: str
        """
        self.BatchId = None
        self.TaskIdSet = None
        self.RequestId = None


    def _deserialize(self, params):
        self.BatchId = params.get("BatchId")
        self.TaskIdSet = params.get("TaskIdSet")
        self.RequestId = params.get("RequestId")


class ModifySQLSessionCatalogRequest(AbstractModel):
    """ModifySQLSessionCatalog请求参数结构体

    """

    def __init__(self):
        r"""
        :param OldPath: 支持路径移动，存移动之前的路径
        :type OldPath: str
        :param NewPath: 支持路径移动，存移动之后的路径
        :type NewPath: str
        :param Type: 节点类型：0：目录，1：会话
        :type Type: str
        :param Operator: 操作用户
        :type Operator: str
        :param UserVisibility: 授权的子用户，空为自己和管理员可见
        :type UserVisibility: str
        :param PurviewInfoSet: 权限信息
        :type PurviewInfoSet: list of PurviewInfo
        """
        self.OldPath = None
        self.NewPath = None
        self.Type = None
        self.Operator = None
        self.UserVisibility = None
        self.PurviewInfoSet = None


    def _deserialize(self, params):
        self.OldPath = params.get("OldPath")
        self.NewPath = params.get("NewPath")
        self.Type = params.get("Type")
        self.Operator = params.get("Operator")
        self.UserVisibility = params.get("UserVisibility")
        if params.get("PurviewInfoSet") is not None:
            self.PurviewInfoSet = []
            for item in params.get("PurviewInfoSet"):
                obj = PurviewInfo()
                obj._deserialize(item)
                self.PurviewInfoSet.append(obj)
        memeber_set = set(params.keys())
        for name, value in vars(self).items():
            if name in memeber_set:
                memeber_set.remove(name)
        if len(memeber_set) > 0:
            warnings.warn("%s fileds are useless." % ",".join(memeber_set))
        


class ModifySQLSessionCatalogResponse(AbstractModel):
    """ModifySQLSessionCatalog返回参数结构体

    """

    def __init__(self):
        r"""
        :param Status: SUCCESS：成功、FAIL：失败、FLUSH：会话内容已变更，请刷新（修改时触发）、DUPLICATE：重名，请调整、NOTEMPTY：该目录下不为空，无法删除、
LIMITEXCEEDED：创建的会话超过限制；
        :type Status: str
        :param RequestId: 唯一请求 ID，每次请求都会返回。定位问题时需要提供该次请求的 RequestId。
        :type RequestId: str
        """
        self.Status = None
        self.RequestId = None


    def _deserialize(self, params):
        self.Status = params.get("Status")
        self.RequestId = params.get("RequestId")


class ModifySQLSessionSnapshotRequest(AbstractModel):
    """ModifySQLSessionSnapshot请求参数结构体

    """

    def __init__(self):
        r"""
        :param SQLSessionSnapshotInfo: 会话信息，复杂类型
        :type SQLSessionSnapshotInfo: :class:`tencentcloud.dlc.v20210125.models.SQLSessionSnapshotInfo`
        """
        self.SQLSessionSnapshotInfo = None


    def _deserialize(self, params):
        if params.get("SQLSessionSnapshotInfo") is not None:
            self.SQLSessionSnapshotInfo = SQLSessionSnapshotInfo()
            self.SQLSessionSnapshotInfo._deserialize(params.get("SQLSessionSnapshotInfo"))
        memeber_set = set(params.keys())
        for name, value in vars(self).items():
            if name in memeber_set:
                memeber_set.remove(name)
        if len(memeber_set) > 0:
            warnings.warn("%s fileds are useless." % ",".join(memeber_set))
        


class ModifySQLSessionSnapshotResponse(AbstractModel):
    """ModifySQLSessionSnapshot返回参数结构体

    """

    def __init__(self):
        r"""
        :param Status: SUCCESS：成功、FAIL：失败、FLUSH：会话内容已变更，请刷新（修改时触发）、DUPLICATE：重名，请调整、NOTEMPTY：该目录下不为空，无法删除、
LIMITEXCEEDED：创建的会话超过限制；
        :type Status: str
        :param Version: 会话版本号，用于跟踪会话更新
        :type Version: int
        :param RequestId: 唯一请求 ID，每次请求都会返回。定位问题时需要提供该次请求的 RequestId。
        :type RequestId: str
        """
        self.Status = None
        self.Version = None
        self.RequestId = None


    def _deserialize(self, params):
        self.Status = params.get("Status")
        self.Version = params.get("Version")
        self.RequestId = params.get("RequestId")


class ModifyScheduleTaskExecuteInfoRequest(AbstractModel):
    """ModifyScheduleTaskExecuteInfo请求参数结构体

    """

    def __init__(self):
        r"""
        :param ScriptId: 脚本ID
        :type ScriptId: str
        :param ScriptName: 脚本名称
        :type ScriptName: str
        :param TaskType: 任务类型，SQL,SparkJar等，默认为SQL任务
        :type TaskType: str
        :param Params: 调度任务自定义参数，[{"Key":"abc","Value":"edf"}]
        :type Params: list of KVPair
        """
        self.ScriptId = None
        self.ScriptName = None
        self.TaskType = None
        self.Params = None


    def _deserialize(self, params):
        self.ScriptId = params.get("ScriptId")
        self.ScriptName = params.get("ScriptName")
        self.TaskType = params.get("TaskType")
        if params.get("Params") is not None:
            self.Params = []
            for item in params.get("Params"):
                obj = KVPair()
                obj._deserialize(item)
                self.Params.append(obj)
        memeber_set = set(params.keys())
        for name, value in vars(self).items():
            if name in memeber_set:
                memeber_set.remove(name)
        if len(memeber_set) > 0:
            warnings.warn("%s fileds are useless." % ",".join(memeber_set))
        


class ModifyScheduleTaskExecuteInfoResponse(AbstractModel):
    """ModifyScheduleTaskExecuteInfo返回参数结构体

    """

    def __init__(self):
        r"""
        :param Result: 更新结果
        :type Result: bool
        :param RequestId: 唯一请求 ID，每次请求都会返回。定位问题时需要提供该次请求的 RequestId。
        :type RequestId: str
        """
        self.Result = None
        self.RequestId = None


    def _deserialize(self, params):
        self.Result = params.get("Result")
        self.RequestId = params.get("RequestId")


class ModifyScheduleTaskRequest(AbstractModel):
    """ModifyScheduleTask请求参数结构体

    """

    def __init__(self):
        r"""
        :param ScheduleTaskInfo: 调度任务详情
        :type ScheduleTaskInfo: :class:`tencentcloud.dlc.v20210125.models.ScheduleTaskInfo`
        """
        self.ScheduleTaskInfo = None


    def _deserialize(self, params):
        if params.get("ScheduleTaskInfo") is not None:
            self.ScheduleTaskInfo = ScheduleTaskInfo()
            self.ScheduleTaskInfo._deserialize(params.get("ScheduleTaskInfo"))
        memeber_set = set(params.keys())
        for name, value in vars(self).items():
            if name in memeber_set:
                memeber_set.remove(name)
        if len(memeber_set) > 0:
            warnings.warn("%s fileds are useless." % ",".join(memeber_set))
        


class ModifyScheduleTaskResponse(AbstractModel):
    """ModifyScheduleTask返回参数结构体

    """

    def __init__(self):
        r"""
        :param Result: 更新任务是否成功
        :type Result: bool
        :param RequestId: 唯一请求 ID，每次请求都会返回。定位问题时需要提供该次请求的 RequestId。
        :type RequestId: str
        """
        self.Result = None
        self.RequestId = None


    def _deserialize(self, params):
        self.Result = params.get("Result")
        self.RequestId = params.get("RequestId")


class ModifySparkAppBatchRequest(AbstractModel):
    """ModifySparkAppBatch请求参数结构体

    """

    def __init__(self):
        r"""
        :param SparkAppId: 需要批量修改的Spark作业任务ID列表
        :type SparkAppId: list of str
        :param DataEngine: 引擎ID
        :type DataEngine: str
        :param AppDriverSize: driver规格：small,medium,large,xlarge；内存型(引擎类型)：m.small,m.medium,m.large,m.xlarge
        :type AppDriverSize: str
        :param AppExecutorSize: executor规格：small,medium,large,xlarge；内存型(引擎类型)：m.small,m.medium,m.large,m.xlarge
        :type AppExecutorSize: str
        :param AppExecutorNums: 指定executor数量，最小值为1，最大值小于集群规格
        :type AppExecutorNums: int
        :param AppExecutorMaxNumbers: 指定executor max数量（动态配置场景下），最小值为1，最大值小于集群规格（当ExecutorMaxNumbers小于ExecutorNums时，改值设定为ExecutorNums）
        :type AppExecutorMaxNumbers: int
        :param IsInherit: 任务资源配置是否继承集群模板，0（默认）不继承，1：继承
        :type IsInherit: int
        """
        self.SparkAppId = None
        self.DataEngine = None
        self.AppDriverSize = None
        self.AppExecutorSize = None
        self.AppExecutorNums = None
        self.AppExecutorMaxNumbers = None
        self.IsInherit = None


    def _deserialize(self, params):
        self.SparkAppId = params.get("SparkAppId")
        self.DataEngine = params.get("DataEngine")
        self.AppDriverSize = params.get("AppDriverSize")
        self.AppExecutorSize = params.get("AppExecutorSize")
        self.AppExecutorNums = params.get("AppExecutorNums")
        self.AppExecutorMaxNumbers = params.get("AppExecutorMaxNumbers")
        self.IsInherit = params.get("IsInherit")
        memeber_set = set(params.keys())
        for name, value in vars(self).items():
            if name in memeber_set:
                memeber_set.remove(name)
        if len(memeber_set) > 0:
            warnings.warn("%s fileds are useless." % ",".join(memeber_set))
        


class ModifySparkAppBatchResponse(AbstractModel):
    """ModifySparkAppBatch返回参数结构体

    """

    def __init__(self):
        r"""
        :param RequestId: 唯一请求 ID，每次请求都会返回。定位问题时需要提供该次请求的 RequestId。
        :type RequestId: str
        """
        self.RequestId = None


    def _deserialize(self, params):
        self.RequestId = params.get("RequestId")


class ModifySparkAppRequest(AbstractModel):
    """ModifySparkApp请求参数结构体

    """

    def __init__(self):
        r"""
        :param AppName: spark作业名
        :type AppName: str
        :param AppType: spark作业类型，1代表spark jar作业，2代表spark streaming作业
        :type AppType: int
        :param DataEngine: 执行spark作业的数据引擎名称
        :type DataEngine: str
        :param AppFile: spark作业程序包文件路径
        :type AppFile: str
        :param RoleArn: 数据访问策略，CAM Role arn
        :type RoleArn: int
        :param AppDriverSize: 指定的Driver规格，当前支持：small（默认，1cu）、medium（2cu）、large（4cu）、xlarge（8cu）
        :type AppDriverSize: str
        :param AppExecutorSize: 指定的Executor规格，当前支持：small（默认，1cu）、medium（2cu）、large（4cu）、xlarge（8cu）
        :type AppExecutorSize: str
        :param AppExecutorNums: spark作业executor个数
        :type AppExecutorNums: int
        :param SparkAppId: spark作业Id
        :type SparkAppId: str
        :param Eni: 该字段已下线，请使用字段Datasource
        :type Eni: str
        :param IsLocal: spark作业程序包是否本地上传，cos：存放与cos，lakefs：本地上传（控制台使用，该方式不支持直接接口调用）
        :type IsLocal: str
        :param MainClass: spark作业主类
        :type MainClass: str
        :param AppConf: spark配置，以换行符分隔
        :type AppConf: str
        :param IsLocalJars: spark 作业依赖jar包是否本地上传，cos：存放与cos，lakefs：本地上传（控制台使用，该方式不支持直接接口调用）
        :type IsLocalJars: str
        :param AppJars: spark 作业依赖jar包（--jars），以逗号分隔
        :type AppJars: str
        :param IsLocalFiles: spark作业依赖文件资源是否本地上传，cos：存放与cos，lakefs：本地上传（控制台使用，该方式不支持直接接口调用）
        :type IsLocalFiles: str
        :param AppFiles: spark作业依赖文件资源（--files）（非jar、zip），以逗号分隔
        :type AppFiles: str
        :param IsLocalPythonFiles: pyspark：依赖上传方式，cos：存放与cos，lakefs：本地上传（控制台使用，该方式不支持直接接口调用）
        :type IsLocalPythonFiles: str
        :param AppPythonFiles: pyspark作业依赖python资源（--py-files），支持py/zip/egg等归档格式，多文件以逗号分隔
        :type AppPythonFiles: str
        :param CmdArgs: spark作业程序入参
        :type CmdArgs: str
        :param MaxRetries: 最大重试次数，只对spark流任务生效
        :type MaxRetries: int
        :param DataSource: 数据源名
        :type DataSource: str
        :param IsLocalArchives: spark作业依赖archives资源是否本地上传，cos：存放与cos，lakefs：本地上传（控制台使用，该方式不支持直接接口调用）
        :type IsLocalArchives: str
        :param AppArchives: spark作业依赖archives资源（--archives），支持tar.gz/tgz/tar等归档格式，以逗号分隔
        :type AppArchives: str
        :param SparkImage: Spark Image 版本号
        :type SparkImage: str
        :param SparkImageVersion: Spark Image 版本名称
        :type SparkImageVersion: str
        :param AppExecutorMaxNumbers: 指定的Executor数量（最大值），默认为1，当开启动态分配有效，若未开启，则该值等于AppExecutorNums
        :type AppExecutorMaxNumbers: int
        :param SessionId: 关联dlc查询脚本
        :type SessionId: str
        :param IsInherit: 任务资源配置是否继承集群配置模板：0（默认）不继承、1：继承
        :type IsInherit: int
        """
        self.AppName = None
        self.AppType = None
        self.DataEngine = None
        self.AppFile = None
        self.RoleArn = None
        self.AppDriverSize = None
        self.AppExecutorSize = None
        self.AppExecutorNums = None
        self.SparkAppId = None
        self.Eni = None
        self.IsLocal = None
        self.MainClass = None
        self.AppConf = None
        self.IsLocalJars = None
        self.AppJars = None
        self.IsLocalFiles = None
        self.AppFiles = None
        self.IsLocalPythonFiles = None
        self.AppPythonFiles = None
        self.CmdArgs = None
        self.MaxRetries = None
        self.DataSource = None
        self.IsLocalArchives = None
        self.AppArchives = None
        self.SparkImage = None
        self.SparkImageVersion = None
        self.AppExecutorMaxNumbers = None
        self.SessionId = None
        self.IsInherit = None


    def _deserialize(self, params):
        self.AppName = params.get("AppName")
        self.AppType = params.get("AppType")
        self.DataEngine = params.get("DataEngine")
        self.AppFile = params.get("AppFile")
        self.RoleArn = params.get("RoleArn")
        self.AppDriverSize = params.get("AppDriverSize")
        self.AppExecutorSize = params.get("AppExecutorSize")
        self.AppExecutorNums = params.get("AppExecutorNums")
        self.SparkAppId = params.get("SparkAppId")
        self.Eni = params.get("Eni")
        self.IsLocal = params.get("IsLocal")
        self.MainClass = params.get("MainClass")
        self.AppConf = params.get("AppConf")
        self.IsLocalJars = params.get("IsLocalJars")
        self.AppJars = params.get("AppJars")
        self.IsLocalFiles = params.get("IsLocalFiles")
        self.AppFiles = params.get("AppFiles")
        self.IsLocalPythonFiles = params.get("IsLocalPythonFiles")
        self.AppPythonFiles = params.get("AppPythonFiles")
        self.CmdArgs = params.get("CmdArgs")
        self.MaxRetries = params.get("MaxRetries")
        self.DataSource = params.get("DataSource")
        self.IsLocalArchives = params.get("IsLocalArchives")
        self.AppArchives = params.get("AppArchives")
        self.SparkImage = params.get("SparkImage")
        self.SparkImageVersion = params.get("SparkImageVersion")
        self.AppExecutorMaxNumbers = params.get("AppExecutorMaxNumbers")
        self.SessionId = params.get("SessionId")
        self.IsInherit = params.get("IsInherit")
        memeber_set = set(params.keys())
        for name, value in vars(self).items():
            if name in memeber_set:
                memeber_set.remove(name)
        if len(memeber_set) > 0:
            warnings.warn("%s fileds are useless." % ",".join(memeber_set))
        


class ModifySparkAppResponse(AbstractModel):
    """ModifySparkApp返回参数结构体

    """

    def __init__(self):
        r"""
        :param RequestId: 唯一请求 ID，每次请求都会返回。定位问题时需要提供该次请求的 RequestId。
        :type RequestId: str
        """
        self.RequestId = None


    def _deserialize(self, params):
        self.RequestId = params.get("RequestId")


class ModifySparkImageRequest(AbstractModel):
    """ModifySparkImage请求参数结构体

    """

    def __init__(self):
        r"""
        :param ImageId: 镜像编码
        :type ImageId: str
        :param ImageTag: 镜像tag
        :type ImageTag: str
        :param Description: 镜像描述
        :type Description: str
        :param IsPublic: 是否为公共镜像：0：非公共；1：公共
        :type IsPublic: int
        :param Operator: 操作者
        :type Operator: str
        """
        self.ImageId = None
        self.ImageTag = None
        self.Description = None
        self.IsPublic = None
        self.Operator = None


    def _deserialize(self, params):
        self.ImageId = params.get("ImageId")
        self.ImageTag = params.get("ImageTag")
        self.Description = params.get("Description")
        self.IsPublic = params.get("IsPublic")
        self.Operator = params.get("Operator")
        memeber_set = set(params.keys())
        for name, value in vars(self).items():
            if name in memeber_set:
                memeber_set.remove(name)
        if len(memeber_set) > 0:
            warnings.warn("%s fileds are useless." % ",".join(memeber_set))
        


class ModifySparkImageResponse(AbstractModel):
    """ModifySparkImage返回参数结构体

    """

    def __init__(self):
        r"""
        :param RequestId: 唯一请求 ID，每次请求都会返回。定位问题时需要提供该次请求的 RequestId。
        :type RequestId: str
        """
        self.RequestId = None


    def _deserialize(self, params):
        self.RequestId = params.get("RequestId")


class ModifyUserAliasRequest(AbstractModel):
    """ModifyUserAlias请求参数结构体

    """

    def __init__(self):
        r"""
        :param UserId: 用户Id，和CAM侧Uin匹配
        :type UserId: str
        :param UserAlias: 用户别名
        :type UserAlias: str
        """
        self.UserId = None
        self.UserAlias = None


    def _deserialize(self, params):
        self.UserId = params.get("UserId")
        self.UserAlias = params.get("UserAlias")
        memeber_set = set(params.keys())
        for name, value in vars(self).items():
            if name in memeber_set:
                memeber_set.remove(name)
        if len(memeber_set) > 0:
            warnings.warn("%s fileds are useless." % ",".join(memeber_set))
        


class ModifyUserAliasResponse(AbstractModel):
    """ModifyUserAlias返回参数结构体

    """

    def __init__(self):
        r"""
        :param RequestId: 唯一请求 ID，每次请求都会返回。定位问题时需要提供该次请求的 RequestId。
        :type RequestId: str
        """
        self.RequestId = None


    def _deserialize(self, params):
        self.RequestId = params.get("RequestId")


class ModifyUserRequest(AbstractModel):
    """ModifyUser请求参数结构体

    """

    def __init__(self):
        r"""
        :param UserId: 用户Id，和CAM侧Uin匹配
        :type UserId: str
        :param UserDescription: 用户描述
        :type UserDescription: str
        """
        self.UserId = None
        self.UserDescription = None


    def _deserialize(self, params):
        self.UserId = params.get("UserId")
        self.UserDescription = params.get("UserDescription")
        memeber_set = set(params.keys())
        for name, value in vars(self).items():
            if name in memeber_set:
                memeber_set.remove(name)
        if len(memeber_set) > 0:
            warnings.warn("%s fileds are useless." % ",".join(memeber_set))
        


class ModifyUserResponse(AbstractModel):
    """ModifyUser返回参数结构体

    """

    def __init__(self):
        r"""
        :param RequestId: 唯一请求 ID，每次请求都会返回。定位问题时需要提供该次请求的 RequestId。
        :type RequestId: str
        """
        self.RequestId = None


    def _deserialize(self, params):
        self.RequestId = params.get("RequestId")


class ModifyUserTypeRequest(AbstractModel):
    """ModifyUserType请求参数结构体

    """

    def __init__(self):
        r"""
        :param UserId: 用户ID
        :type UserId: str
        :param UserType: 用户要修改到的类型，ADMIN：管理员，COMMON：一般用户。
        :type UserType: str
        """
        self.UserId = None
        self.UserType = None


    def _deserialize(self, params):
        self.UserId = params.get("UserId")
        self.UserType = params.get("UserType")
        memeber_set = set(params.keys())
        for name, value in vars(self).items():
            if name in memeber_set:
                memeber_set.remove(name)
        if len(memeber_set) > 0:
            warnings.warn("%s fileds are useless." % ",".join(memeber_set))
        


class ModifyUserTypeResponse(AbstractModel):
    """ModifyUserType返回参数结构体

    """

    def __init__(self):
        r"""
        :param RequestId: 唯一请求 ID，每次请求都会返回。定位问题时需要提供该次请求的 RequestId。
        :type RequestId: str
        """
        self.RequestId = None


    def _deserialize(self, params):
        self.RequestId = params.get("RequestId")


class ModifyUserUseSceneRequest(AbstractModel):
    """ModifyUserUseScene请求参数结构体

    """

    def __init__(self):
        r"""
        :param Scene: 使用场景，1:数据应用开发，2:企业数据平台搭建
        :type Scene: int
        :param NeedGuide: 是否需要指导,false不需要，true需要
        :type NeedGuide: bool
        """
        self.Scene = None
        self.NeedGuide = None


    def _deserialize(self, params):
        self.Scene = params.get("Scene")
        self.NeedGuide = params.get("NeedGuide")
        memeber_set = set(params.keys())
        for name, value in vars(self).items():
            if name in memeber_set:
                memeber_set.remove(name)
        if len(memeber_set) > 0:
            warnings.warn("%s fileds are useless." % ",".join(memeber_set))
        


class ModifyUserUseSceneResponse(AbstractModel):
    """ModifyUserUseScene返回参数结构体

    """

    def __init__(self):
        r"""
        :param RequestId: 唯一请求 ID，每次请求都会返回。定位问题时需要提供该次请求的 RequestId。
        :type RequestId: str
        """
        self.RequestId = None


    def _deserialize(self, params):
        self.RequestId = params.get("RequestId")


class ModifyWorkGroupRequest(AbstractModel):
    """ModifyWorkGroup请求参数结构体

    """

    def __init__(self):
        r"""
        :param WorkGroupId: 工作组Id
        :type WorkGroupId: int
        :param WorkGroupDescription: 工作组描述
        :type WorkGroupDescription: str
        """
        self.WorkGroupId = None
        self.WorkGroupDescription = None


    def _deserialize(self, params):
        self.WorkGroupId = params.get("WorkGroupId")
        self.WorkGroupDescription = params.get("WorkGroupDescription")
        memeber_set = set(params.keys())
        for name, value in vars(self).items():
            if name in memeber_set:
                memeber_set.remove(name)
        if len(memeber_set) > 0:
            warnings.warn("%s fileds are useless." % ",".join(memeber_set))
        


class ModifyWorkGroupResponse(AbstractModel):
    """ModifyWorkGroup返回参数结构体

    """

    def __init__(self):
        r"""
        :param RequestId: 唯一请求 ID，每次请求都会返回。定位问题时需要提供该次请求的 RequestId。
        :type RequestId: str
        """
        self.RequestId = None


    def _deserialize(self, params):
        self.RequestId = params.get("RequestId")


class MonitorObject(AbstractModel):
    """监控对象

    """

    def __init__(self):
        r"""
        :param MonitorObjectId: 监控对象ID
        :type MonitorObjectId: str
        :param MonitorObjectName: 监控对象名称
        :type MonitorObjectName: str
        """
        self.MonitorObjectId = None
        self.MonitorObjectName = None


    def _deserialize(self, params):
        self.MonitorObjectId = params.get("MonitorObjectId")
        self.MonitorObjectName = params.get("MonitorObjectName")
        memeber_set = set(params.keys())
        for name, value in vars(self).items():
            if name in memeber_set:
                memeber_set.remove(name)
        if len(memeber_set) > 0:
            warnings.warn("%s fileds are useless." % ",".join(memeber_set))
        


class MountPoint(AbstractModel):
    """挂载点信息

    """

    def __init__(self):
        r"""
        :param MountPointId: 挂载点ID
        :type MountPointId: str
        :param MountPointName: 挂载点名称
注意：此字段可能返回 null，表示取不到有效值。
        :type MountPointName: str
        :param FileSystemId: 文件系统ID
注意：此字段可能返回 null，表示取不到有效值。
        :type FileSystemId: str
        :param AccessGroupIds: 绑定的权限组ID列表
注意：此字段可能返回 null，表示取不到有效值。
        :type AccessGroupIds: list of str
        :param Status: 挂载点状态（1：打开；2：关闭）
注意：此字段可能返回 null，表示取不到有效值。
        :type Status: int
        :param CreateTime: 创建时间
注意：此字段可能返回 null，表示取不到有效值。
        :type CreateTime: str
        """
        self.MountPointId = None
        self.MountPointName = None
        self.FileSystemId = None
        self.AccessGroupIds = None
        self.Status = None
        self.CreateTime = None


    def _deserialize(self, params):
        self.MountPointId = params.get("MountPointId")
        self.MountPointName = params.get("MountPointName")
        self.FileSystemId = params.get("FileSystemId")
        self.AccessGroupIds = params.get("AccessGroupIds")
        self.Status = params.get("Status")
        self.CreateTime = params.get("CreateTime")
        memeber_set = set(params.keys())
        for name, value in vars(self).items():
            if name in memeber_set:
                memeber_set.remove(name)
        if len(memeber_set) > 0:
            warnings.warn("%s fileds are useless." % ",".join(memeber_set))
        


class MountPointAssociateInfo(AbstractModel):
    """挂载点绑定详情

    """

    def __init__(self):
        r"""
        :param MountPointId: 挂载点ID
        :type MountPointId: str
        :param DataEngineName: 数据引擎名称
        :type DataEngineName: str
        :param AccessGroupId: 权限组ID
        :type AccessGroupId: str
        """
        self.MountPointId = None
        self.DataEngineName = None
        self.AccessGroupId = None


    def _deserialize(self, params):
        self.MountPointId = params.get("MountPointId")
        self.DataEngineName = params.get("DataEngineName")
        self.AccessGroupId = params.get("AccessGroupId")
        memeber_set = set(params.keys())
        for name, value in vars(self).items():
            if name in memeber_set:
                memeber_set.remove(name)
        if len(memeber_set) > 0:
            warnings.warn("%s fileds are useless." % ",".join(memeber_set))
        


class MysqlInfo(AbstractModel):
    """Mysql类型数据源信息

    """

    def __init__(self):
        r"""
        :param JdbcUrl: 连接mysql的jdbc url
        :type JdbcUrl: str
        :param User: 用户名
        :type User: str
        :param Password: mysql密码
        :type Password: str
        :param Location: mysql数据源的网络信息
        :type Location: :class:`tencentcloud.dlc.v20210125.models.DatasourceConnectionLocation`
        :param DbName: 数据库名称
        :type DbName: str
        :param InstanceId: 数据库实例ID，和数据库侧保持一致
注意：此字段可能返回 null，表示取不到有效值。
        :type InstanceId: str
        :param InstanceName: 数据库实例名称，和数据库侧保持一致
注意：此字段可能返回 null，表示取不到有效值。
        :type InstanceName: str
        """
        self.JdbcUrl = None
        self.User = None
        self.Password = None
        self.Location = None
        self.DbName = None
        self.InstanceId = None
        self.InstanceName = None


    def _deserialize(self, params):
        self.JdbcUrl = params.get("JdbcUrl")
        self.User = params.get("User")
        self.Password = params.get("Password")
        if params.get("Location") is not None:
            self.Location = DatasourceConnectionLocation()
            self.Location._deserialize(params.get("Location"))
        self.DbName = params.get("DbName")
        self.InstanceId = params.get("InstanceId")
        self.InstanceName = params.get("InstanceName")
        memeber_set = set(params.keys())
        for name, value in vars(self).items():
            if name in memeber_set:
                memeber_set.remove(name)
        if len(memeber_set) > 0:
            warnings.warn("%s fileds are useless." % ",".join(memeber_set))
        


class NetworkConnection(AbstractModel):
    """网络配置

    """

    def __init__(self):
        r"""
        :param Id: 网络配置id
注意：此字段可能返回 null，表示取不到有效值。
        :type Id: int
        :param AssociateId: 网络配置唯一标志符
注意：此字段可能返回 null，表示取不到有效值。
        :type AssociateId: str
        :param HouseId: 计算引擎id
注意：此字段可能返回 null，表示取不到有效值。
        :type HouseId: str
        :param DatasourceConnectionId: 数据源id(已废弃)
注意：此字段可能返回 null，表示取不到有效值。
        :type DatasourceConnectionId: str
        :param State: 网络配置状态（0-初始化，1-正常）
注意：此字段可能返回 null，表示取不到有效值。
        :type State: int
        :param CreateTime: 创建时间
注意：此字段可能返回 null，表示取不到有效值。
        :type CreateTime: int
        :param UpdateTime: 修改时间
注意：此字段可能返回 null，表示取不到有效值。
        :type UpdateTime: int
        :param Appid: 创建用户Appid
注意：此字段可能返回 null，表示取不到有效值。
        :type Appid: int
        :param HouseName: 计算引擎名称
注意：此字段可能返回 null，表示取不到有效值。
        :type HouseName: str
        :param DatasourceConnectionName: 网络配置名称
注意：此字段可能返回 null，表示取不到有效值。
        :type DatasourceConnectionName: str
        :param NetworkConnectionType: 网络配置类型
注意：此字段可能返回 null，表示取不到有效值。
        :type NetworkConnectionType: int
        :param Uin: 创建用户uin
注意：此字段可能返回 null，表示取不到有效值。
        :type Uin: str
        :param SubAccountUin: 创建用户SubAccountUin
注意：此字段可能返回 null，表示取不到有效值。
        :type SubAccountUin: str
        :param NetworkConnectionDesc: 网络配置描述
注意：此字段可能返回 null，表示取不到有效值。
        :type NetworkConnectionDesc: str
        :param DatasourceConnectionVpcId: 数据源vpcid
注意：此字段可能返回 null，表示取不到有效值。
        :type DatasourceConnectionVpcId: str
        :param DatasourceConnectionSubnetId: 数据源SubnetId
注意：此字段可能返回 null，表示取不到有效值。
        :type DatasourceConnectionSubnetId: str
        :param DatasourceConnectionCidrBlock: 数据源SubnetId
注意：此字段可能返回 null，表示取不到有效值。
        :type DatasourceConnectionCidrBlock: str
        :param DatasourceConnectionSubnetCidrBlock: 数据源SubnetCidrBlock
注意：此字段可能返回 null，表示取不到有效值。
        :type DatasourceConnectionSubnetCidrBlock: str
        """
        self.Id = None
        self.AssociateId = None
        self.HouseId = None
        self.DatasourceConnectionId = None
        self.State = None
        self.CreateTime = None
        self.UpdateTime = None
        self.Appid = None
        self.HouseName = None
        self.DatasourceConnectionName = None
        self.NetworkConnectionType = None
        self.Uin = None
        self.SubAccountUin = None
        self.NetworkConnectionDesc = None
        self.DatasourceConnectionVpcId = None
        self.DatasourceConnectionSubnetId = None
        self.DatasourceConnectionCidrBlock = None
        self.DatasourceConnectionSubnetCidrBlock = None


    def _deserialize(self, params):
        self.Id = params.get("Id")
        self.AssociateId = params.get("AssociateId")
        self.HouseId = params.get("HouseId")
        self.DatasourceConnectionId = params.get("DatasourceConnectionId")
        self.State = params.get("State")
        self.CreateTime = params.get("CreateTime")
        self.UpdateTime = params.get("UpdateTime")
        self.Appid = params.get("Appid")
        self.HouseName = params.get("HouseName")
        self.DatasourceConnectionName = params.get("DatasourceConnectionName")
        self.NetworkConnectionType = params.get("NetworkConnectionType")
        self.Uin = params.get("Uin")
        self.SubAccountUin = params.get("SubAccountUin")
        self.NetworkConnectionDesc = params.get("NetworkConnectionDesc")
        self.DatasourceConnectionVpcId = params.get("DatasourceConnectionVpcId")
        self.DatasourceConnectionSubnetId = params.get("DatasourceConnectionSubnetId")
        self.DatasourceConnectionCidrBlock = params.get("DatasourceConnectionCidrBlock")
        self.DatasourceConnectionSubnetCidrBlock = params.get("DatasourceConnectionSubnetCidrBlock")
        memeber_set = set(params.keys())
        for name, value in vars(self).items():
            if name in memeber_set:
                memeber_set.remove(name)
        if len(memeber_set) > 0:
            warnings.warn("%s fileds are useless." % ",".join(memeber_set))
        


class NotebookSessionInfo(AbstractModel):
    """Notebook Session详细信息。

    """

    def __init__(self):
        r"""
        :param Name: Session名称
        :type Name: str
        :param Kind: 类型，当前支持：spark、pyspark、sparkr、sql
        :type Kind: str
        :param DataEngineName: DLC Spark作业引擎名称
        :type DataEngineName: str
        :param Arguments: Session相关配置，当前支持：eni、roleArn以及用户指定的配置
注意：此字段可能返回 null，表示取不到有效值。
        :type Arguments: list of KVPair
        :param ProgramDependentFiles: 运行程序地址，当前支持：cosn://和lakefs://两种路径
注意：此字段可能返回 null，表示取不到有效值。
        :type ProgramDependentFiles: list of str
        :param ProgramDependentJars: 依赖的jar程序地址，当前支持：cosn://和lakefs://两种路径
注意：此字段可能返回 null，表示取不到有效值。
        :type ProgramDependentJars: list of str
        :param ProgramDependentPython: 依赖的python程序地址，当前支持：cosn://和lakefs://两种路径
注意：此字段可能返回 null，表示取不到有效值。
        :type ProgramDependentPython: list of str
        :param ProgramArchives: 依赖的pyspark虚拟环境地址，当前支持：cosn://和lakefs://两种路径
注意：此字段可能返回 null，表示取不到有效值。
        :type ProgramArchives: list of str
        :param DriverSize: 指定的Driver规格，当前支持：small（默认，1cu）、medium（2cu）、large（4cu）、xlarge（8cu）
注意：此字段可能返回 null，表示取不到有效值。
        :type DriverSize: str
        :param ExecutorSize: 指定的Executor规格，当前支持：small（默认，1cu）、medium（2cu）、large（4cu）、xlarge（8cu）
注意：此字段可能返回 null，表示取不到有效值。
        :type ExecutorSize: str
        :param ExecutorNumbers: 指定的Executor数量，默认为1
注意：此字段可能返回 null，表示取不到有效值。
        :type ExecutorNumbers: int
        :param ProxyUser: 代理用户，默认为root
注意：此字段可能返回 null，表示取不到有效值。
        :type ProxyUser: str
        :param TimeoutInSecond: 指定的Session超时时间，单位秒，默认3600秒
注意：此字段可能返回 null，表示取不到有效值。
        :type TimeoutInSecond: int
        :param SparkAppId: Spark任务返回的AppId
注意：此字段可能返回 null，表示取不到有效值。
        :type SparkAppId: str
        :param SessionId: Session唯一标识
        :type SessionId: str
        :param State: Session状态，包含：not_started（未启动）、starting（已启动）、idle（等待输入）、busy(正在运行statement)、shutting_down（停止）、error（异常）、dead（已退出）、killed（被杀死）、success（正常停止）
        :type State: str
        :param CreateTime: Session创建时间
        :type CreateTime: str
        :param AppInfo: 其它信息
注意：此字段可能返回 null，表示取不到有效值。
        :type AppInfo: list of KVPair
        :param SparkUiUrl: Spark ui地址
注意：此字段可能返回 null，表示取不到有效值。
        :type SparkUiUrl: str
        :param ExecutorMaxNumbers: 指定的Executor数量（最大值），默认为1，当开启动态分配有效，若未开启，则该值等于ExecutorNumbers
注意：此字段可能返回 null，表示取不到有效值。
        :type ExecutorMaxNumbers: int
        """
        self.Name = None
        self.Kind = None
        self.DataEngineName = None
        self.Arguments = None
        self.ProgramDependentFiles = None
        self.ProgramDependentJars = None
        self.ProgramDependentPython = None
        self.ProgramArchives = None
        self.DriverSize = None
        self.ExecutorSize = None
        self.ExecutorNumbers = None
        self.ProxyUser = None
        self.TimeoutInSecond = None
        self.SparkAppId = None
        self.SessionId = None
        self.State = None
        self.CreateTime = None
        self.AppInfo = None
        self.SparkUiUrl = None
        self.ExecutorMaxNumbers = None


    def _deserialize(self, params):
        self.Name = params.get("Name")
        self.Kind = params.get("Kind")
        self.DataEngineName = params.get("DataEngineName")
        if params.get("Arguments") is not None:
            self.Arguments = []
            for item in params.get("Arguments"):
                obj = KVPair()
                obj._deserialize(item)
                self.Arguments.append(obj)
        self.ProgramDependentFiles = params.get("ProgramDependentFiles")
        self.ProgramDependentJars = params.get("ProgramDependentJars")
        self.ProgramDependentPython = params.get("ProgramDependentPython")
        self.ProgramArchives = params.get("ProgramArchives")
        self.DriverSize = params.get("DriverSize")
        self.ExecutorSize = params.get("ExecutorSize")
        self.ExecutorNumbers = params.get("ExecutorNumbers")
        self.ProxyUser = params.get("ProxyUser")
        self.TimeoutInSecond = params.get("TimeoutInSecond")
        self.SparkAppId = params.get("SparkAppId")
        self.SessionId = params.get("SessionId")
        self.State = params.get("State")
        self.CreateTime = params.get("CreateTime")
        if params.get("AppInfo") is not None:
            self.AppInfo = []
            for item in params.get("AppInfo"):
                obj = KVPair()
                obj._deserialize(item)
                self.AppInfo.append(obj)
        self.SparkUiUrl = params.get("SparkUiUrl")
        self.ExecutorMaxNumbers = params.get("ExecutorMaxNumbers")
        memeber_set = set(params.keys())
        for name, value in vars(self).items():
            if name in memeber_set:
                memeber_set.remove(name)
        if len(memeber_set) > 0:
            warnings.warn("%s fileds are useless." % ",".join(memeber_set))
        


class NotebookSessionStatementBatchInformation(AbstractModel):
    """按批提交Statement运行SQL任务。

    """

    def __init__(self):
        r"""
        :param NotebookSessionStatementBatch: 任务详情列表
注意：此字段可能返回 null，表示取不到有效值。
        :type NotebookSessionStatementBatch: list of NotebookSessionStatementInfo
        :param IsAvailable: 当前批任务是否运行完成
注意：此字段可能返回 null，表示取不到有效值。
        :type IsAvailable: bool
        :param SessionId: Session唯一标识
注意：此字段可能返回 null，表示取不到有效值。
        :type SessionId: str
        :param BatchId: Batch唯一标识
注意：此字段可能返回 null，表示取不到有效值。
        :type BatchId: str
        """
        self.NotebookSessionStatementBatch = None
        self.IsAvailable = None
        self.SessionId = None
        self.BatchId = None


    def _deserialize(self, params):
        if params.get("NotebookSessionStatementBatch") is not None:
            self.NotebookSessionStatementBatch = []
            for item in params.get("NotebookSessionStatementBatch"):
                obj = NotebookSessionStatementInfo()
                obj._deserialize(item)
                self.NotebookSessionStatementBatch.append(obj)
        self.IsAvailable = params.get("IsAvailable")
        self.SessionId = params.get("SessionId")
        self.BatchId = params.get("BatchId")
        memeber_set = set(params.keys())
        for name, value in vars(self).items():
            if name in memeber_set:
                memeber_set.remove(name)
        if len(memeber_set) > 0:
            warnings.warn("%s fileds are useless." % ",".join(memeber_set))
        


class NotebookSessionStatementInfo(AbstractModel):
    """NotebookSessionStatement详情。

    """

    def __init__(self):
        r"""
        :param Completed: 完成时间戳
注意：此字段可能返回 null，表示取不到有效值。
        :type Completed: int
        :param Started: 开始时间戳
注意：此字段可能返回 null，表示取不到有效值。
        :type Started: int
        :param Progress: 完成进度，百分制
注意：此字段可能返回 null，表示取不到有效值。
        :type Progress: float
        :param StatementId: Session Statement唯一标识
        :type StatementId: str
        :param State: Session Statement状态，包含：waiting（排队中）、running（运行中）、available（正常）、error（异常）、cancelling（取消中）、cancelled（已取消）
        :type State: str
        :param OutPut: Statement输出信息
注意：此字段可能返回 null，表示取不到有效值。
        :type OutPut: :class:`tencentcloud.dlc.v20210125.models.StatementOutput`
        :param BatchId: 批任务id
注意：此字段可能返回 null，表示取不到有效值。
        :type BatchId: str
        :param Code: 运行语句
注意：此字段可能返回 null，表示取不到有效值。
        :type Code: str
        :param TaskId: 任务ID
注意：此字段可能返回 null，表示取不到有效值。
        :type TaskId: str
        """
        self.Completed = None
        self.Started = None
        self.Progress = None
        self.StatementId = None
        self.State = None
        self.OutPut = None
        self.BatchId = None
        self.Code = None
        self.TaskId = None


    def _deserialize(self, params):
        self.Completed = params.get("Completed")
        self.Started = params.get("Started")
        self.Progress = params.get("Progress")
        self.StatementId = params.get("StatementId")
        self.State = params.get("State")
        if params.get("OutPut") is not None:
            self.OutPut = StatementOutput()
            self.OutPut._deserialize(params.get("OutPut"))
        self.BatchId = params.get("BatchId")
        self.Code = params.get("Code")
        self.TaskId = params.get("TaskId")
        memeber_set = set(params.keys())
        for name, value in vars(self).items():
            if name in memeber_set:
                memeber_set.remove(name)
        if len(memeber_set) > 0:
            warnings.warn("%s fileds are useless." % ",".join(memeber_set))
        


class NotebookSessions(AbstractModel):
    """notebook session列表信息。

    """

    def __init__(self):
        r"""
        :param Kind: 类型，当前支持：spark、pyspark、sparkr、sql
        :type Kind: str
        :param SessionId: Session唯一标识
        :type SessionId: str
        :param ProxyUser: 代理用户，默认为root
注意：此字段可能返回 null，表示取不到有效值。
        :type ProxyUser: str
        :param State: Session状态，包含：not_started（未启动）、starting（已启动）、idle（等待输入）、busy(正在运行statement)、shutting_down（停止）、error（异常）、dead（已退出）、killed（被杀死）、success（正常停止）
        :type State: str
        :param SparkAppId: Spark任务返回的AppId
注意：此字段可能返回 null，表示取不到有效值。
        :type SparkAppId: str
        :param Name: Session名称
        :type Name: str
        :param CreateTime: Session创建时间
        :type CreateTime: str
        :param DataEngineName: 引擎名称
        :type DataEngineName: str
        :param LastRunningTime: 最新的运行时间
注意：此字段可能返回 null，表示取不到有效值。
        :type LastRunningTime: str
        :param Creator: 创建者
        :type Creator: str
        :param SparkUiUrl: spark ui地址
注意：此字段可能返回 null，表示取不到有效值。
        :type SparkUiUrl: str
        """
        self.Kind = None
        self.SessionId = None
        self.ProxyUser = None
        self.State = None
        self.SparkAppId = None
        self.Name = None
        self.CreateTime = None
        self.DataEngineName = None
        self.LastRunningTime = None
        self.Creator = None
        self.SparkUiUrl = None


    def _deserialize(self, params):
        self.Kind = params.get("Kind")
        self.SessionId = params.get("SessionId")
        self.ProxyUser = params.get("ProxyUser")
        self.State = params.get("State")
        self.SparkAppId = params.get("SparkAppId")
        self.Name = params.get("Name")
        self.CreateTime = params.get("CreateTime")
        self.DataEngineName = params.get("DataEngineName")
        self.LastRunningTime = params.get("LastRunningTime")
        self.Creator = params.get("Creator")
        self.SparkUiUrl = params.get("SparkUiUrl")
        memeber_set = set(params.keys())
        for name, value in vars(self).items():
            if name in memeber_set:
                memeber_set.remove(name)
        if len(memeber_set) > 0:
            warnings.warn("%s fileds are useless." % ",".join(memeber_set))
        


class ORCFile(AbstractModel):
    """ORC类型文件

    """

    def __init__(self):
        r"""
        :param Format: 文本类型，本参数取值为ORC。
        :type Format: str
        :param CodeCompress: 压缩格式，["Snappy","Gzip","None"选一]
        :type CodeCompress: str
        """
        self.Format = None
        self.CodeCompress = None


    def _deserialize(self, params):
        self.Format = params.get("Format")
        self.CodeCompress = params.get("CodeCompress")
        memeber_set = set(params.keys())
        for name, value in vars(self).items():
            if name in memeber_set:
                memeber_set.remove(name)
        if len(memeber_set) > 0:
            warnings.warn("%s fileds are useless." % ",".join(memeber_set))
        


class Other(AbstractModel):
    """数据格式其它类型。

    """

    def __init__(self):
        r"""
        :param Format: 枚举类型，默认值为Json，可选值为[Json, Parquet, ORC, AVRD]之一。
        :type Format: str
        """
        self.Format = None


    def _deserialize(self, params):
        self.Format = params.get("Format")
        memeber_set = set(params.keys())
        for name, value in vars(self).items():
            if name in memeber_set:
                memeber_set.remove(name)
        if len(memeber_set) > 0:
            warnings.warn("%s fileds are useless." % ",".join(memeber_set))
        


class OtherCHDFSBinding(AbstractModel):
    """非DLC产品CHDFS绑定

    """

    def __init__(self):
        r"""
        :param ProductName: 产品名称
注意：此字段可能返回 null，表示取不到有效值。
        :type ProductName: str
        :param SuperUser: 用户名称（该字段已废弃）
注意：此字段可能返回 null，表示取不到有效值。
        :type SuperUser: list of str
        :param VpcInfo: vpc配置信息
注意：此字段可能返回 null，表示取不到有效值。
        :type VpcInfo: list of CHDFSProductVpcInfo
        :param IsBind: 是否与该桶绑定（该字段已废弃）
注意：此字段可能返回 null，表示取不到有效值。
        :type IsBind: bool
        """
        self.ProductName = None
        self.SuperUser = None
        self.VpcInfo = None
        self.IsBind = None


    def _deserialize(self, params):
        self.ProductName = params.get("ProductName")
        self.SuperUser = params.get("SuperUser")
        if params.get("VpcInfo") is not None:
            self.VpcInfo = []
            for item in params.get("VpcInfo"):
                obj = CHDFSProductVpcInfo()
                obj._deserialize(item)
                self.VpcInfo.append(obj)
        self.IsBind = params.get("IsBind")
        memeber_set = set(params.keys())
        for name, value in vars(self).items():
            if name in memeber_set:
                memeber_set.remove(name)
        if len(memeber_set) > 0:
            warnings.warn("%s fileds are useless." % ",".join(memeber_set))
        


class OtherDatasourceConnection(AbstractModel):
    """其他数据源

    """

    def __init__(self):
        r"""
        :param Location: 网络参数
        :type Location: :class:`tencentcloud.dlc.v20210125.models.DatasourceConnectionLocation`
        """
        self.Location = None


    def _deserialize(self, params):
        if params.get("Location") is not None:
            self.Location = DatasourceConnectionLocation()
            self.Location._deserialize(params.get("Location"))
        memeber_set = set(params.keys())
        for name, value in vars(self).items():
            if name in memeber_set:
                memeber_set.remove(name)
        if len(memeber_set) > 0:
            warnings.warn("%s fileds are useless." % ",".join(memeber_set))
        


class ParquetFile(AbstractModel):
    """Parquet类型文件

    """

    def __init__(self):
        r"""
        :param Format: 文本类型，本参数取值为Parquet。
        :type Format: str
        :param CodeCompress: 压缩格式，["Snappy","Gzip","None"选一]
        :type CodeCompress: str
        """
        self.Format = None
        self.CodeCompress = None


    def _deserialize(self, params):
        self.Format = params.get("Format")
        self.CodeCompress = params.get("CodeCompress")
        memeber_set = set(params.keys())
        for name, value in vars(self).items():
            if name in memeber_set:
                memeber_set.remove(name)
        if len(memeber_set) > 0:
            warnings.warn("%s fileds are useless." % ",".join(memeber_set))
        


class Partition(AbstractModel):
    """数据表分块信息。

    """

    def __init__(self):
        r"""
        :param Name: 分区列名。
        :type Name: str
        :param Type: 分区类型。
        :type Type: str
        :param Comment: 对分区的描述。
        :type Comment: str
        :param Transform: 隐式分区转换策略
注意：此字段可能返回 null，表示取不到有效值。
        :type Transform: str
        :param TransformArgs: 转换策略参数
注意：此字段可能返回 null，表示取不到有效值。
        :type TransformArgs: list of str
        :param CreateTime: 创建时间
注意：此字段可能返回 null，表示取不到有效值。
        :type CreateTime: int
        """
        self.Name = None
        self.Type = None
        self.Comment = None
        self.Transform = None
        self.TransformArgs = None
        self.CreateTime = None


    def _deserialize(self, params):
        self.Name = params.get("Name")
        self.Type = params.get("Type")
        self.Comment = params.get("Comment")
        self.Transform = params.get("Transform")
        self.TransformArgs = params.get("TransformArgs")
        self.CreateTime = params.get("CreateTime")
        memeber_set = set(params.keys())
        for name, value in vars(self).items():
            if name in memeber_set:
                memeber_set.remove(name)
        if len(memeber_set) > 0:
            warnings.warn("%s fileds are useless." % ",".join(memeber_set))
        


class Policy(AbstractModel):
    """权限对象

    """

    def __init__(self):
        r"""
        :param Database: 需要授权的数据库名，填*代表当前Catalog下所有数据库。当授权类型为管理员级别时，只允许填“*”，当授权类型为数据连接级别时只允许填空，其他类型下可以任意指定数据库。
        :type Database: str
        :param Catalog: 需要授权的数据源名称，管理员级别下只支持填*（代表该级别全部资源）；数据源级别和数据库级别鉴权的情况下，只支持填COSDataCatalog或者*；在数据表级别鉴权下可以填写用户自定义数据源。不填情况下默认为DataLakeCatalog。注意：如果是对用户自定义数据源进行鉴权，DLC能够管理的权限是用户接入数据源的时候提供的账户的子集。
        :type Catalog: str
        :param Table: 需要授权的表名，填*代表当前Database下所有表。当授权类型为管理员级别时，只允许填“*”，当授权类型为数据连接级别、数据库级别时只允许填空，其他类型下可以任意指定数据表。
        :type Table: str
        :param Operation: 授权的权限操作，对于不同级别的鉴权提供不同操作。管理员权限：ALL，不填默认为ALL；数据连接级鉴权：CREATE；数据库级别鉴权：ALL、CREATE、ALTER、DROP；数据表权限：ALL、SELECT、INSERT、ALTER、DELETE、DROP、UPDATE。注意：在数据表权限下，指定的数据源不为COSDataCatalog的时候，只支持SELECT操作。
        :type Operation: str
        :param PolicyType: 授权类型，现在支持八种授权类型：ADMIN:管理员级别鉴权 DATASOURCE：数据连接级别鉴权 DATABASE：数据库级别鉴权 TABLE：表级别鉴权 VIEW：视图级别鉴权 FUNCTION：函数级别鉴权 COLUMN：列级别鉴权 ENGINE：数据引擎鉴权。不填默认为管理员级别鉴权。
        :type PolicyType: str
        :param Function: 需要授权的函数名，填*代表当前Catalog下所有函数。当授权类型为管理员级别时，只允许填“*”，当授权类型为数据连接级别时只允许填空，其他类型下可以任意指定函数。
注意：此字段可能返回 null，表示取不到有效值。
        :type Function: str
        :param View: 需要授权的视图，填*代表当前Database下所有视图。当授权类型为管理员级别时，只允许填“*”，当授权类型为数据连接级别、数据库级别时只允许填空，其他类型下可以任意指定视图。
注意：此字段可能返回 null，表示取不到有效值。
        :type View: str
        :param Column: 需要授权的列，填*代表当前所有列。当授权类型为管理员级别时，只允许填“*”
注意：此字段可能返回 null，表示取不到有效值。
        :type Column: str
        :param DataEngine: 需要授权的数据引擎，填*代表当前所有引擎。当授权类型为管理员级别时，只允许填“*”
注意：此字段可能返回 null，表示取不到有效值。
        :type DataEngine: str
        :param ReAuth: 用户是否可以进行二次授权。当为true的时候，被授权的用户可以将本次获取的权限再次授权给其他子用户。默认为false
注意：此字段可能返回 null，表示取不到有效值。
        :type ReAuth: bool
        :param Source: 权限来源，入参不填。USER：权限来自用户本身；WORKGROUP：权限来自绑定的工作组
注意：此字段可能返回 null，表示取不到有效值。
        :type Source: str
        :param Mode: 授权模式，入参不填。COMMON：普通模式；SENIOR：高级模式。
注意：此字段可能返回 null，表示取不到有效值。
        :type Mode: str
        :param Operator: 操作者，入参不填。
注意：此字段可能返回 null，表示取不到有效值。
        :type Operator: str
        :param CreateTime: 权限创建的时间，入参不填
注意：此字段可能返回 null，表示取不到有效值。
        :type CreateTime: str
        :param SourceId: 权限所属工作组的ID，只有当该权限的来源为工作组时才会有值。即仅当Source字段的值为WORKGROUP时该字段才有值。
注意：此字段可能返回 null，表示取不到有效值。
        :type SourceId: int
        :param SourceName: 权限所属工作组的名称，只有当该权限的来源为工作组时才会有值。即仅当Source字段的值为WORKGROUP时该字段才有值。
注意：此字段可能返回 null，表示取不到有效值。
        :type SourceName: str
        :param Id: 策略ID
注意：此字段可能返回 null，表示取不到有效值。
        :type Id: int
        """
        self.Database = None
        self.Catalog = None
        self.Table = None
        self.Operation = None
        self.PolicyType = None
        self.Function = None
        self.View = None
        self.Column = None
        self.DataEngine = None
        self.ReAuth = None
        self.Source = None
        self.Mode = None
        self.Operator = None
        self.CreateTime = None
        self.SourceId = None
        self.SourceName = None
        self.Id = None


    def _deserialize(self, params):
        self.Database = params.get("Database")
        self.Catalog = params.get("Catalog")
        self.Table = params.get("Table")
        self.Operation = params.get("Operation")
        self.PolicyType = params.get("PolicyType")
        self.Function = params.get("Function")
        self.View = params.get("View")
        self.Column = params.get("Column")
        self.DataEngine = params.get("DataEngine")
        self.ReAuth = params.get("ReAuth")
        self.Source = params.get("Source")
        self.Mode = params.get("Mode")
        self.Operator = params.get("Operator")
        self.CreateTime = params.get("CreateTime")
        self.SourceId = params.get("SourceId")
        self.SourceName = params.get("SourceName")
        self.Id = params.get("Id")
        memeber_set = set(params.keys())
        for name, value in vars(self).items():
            if name in memeber_set:
                memeber_set.remove(name)
        if len(memeber_set) > 0:
            warnings.warn("%s fileds are useless." % ",".join(memeber_set))
        


class Policys(AbstractModel):
    """策略集合

    """

    def __init__(self):
        r"""
        :param PolicySet: 策略集合
注意：此字段可能返回 null，表示取不到有效值。
        :type PolicySet: list of Policy
        :param TotalCount: 策略总数
注意：此字段可能返回 null，表示取不到有效值。
        :type TotalCount: int
        """
        self.PolicySet = None
        self.TotalCount = None


    def _deserialize(self, params):
        if params.get("PolicySet") is not None:
            self.PolicySet = []
            for item in params.get("PolicySet"):
                obj = Policy()
                obj._deserialize(item)
                self.PolicySet.append(obj)
        self.TotalCount = params.get("TotalCount")
        memeber_set = set(params.keys())
        for name, value in vars(self).items():
            if name in memeber_set:
                memeber_set.remove(name)
        if len(memeber_set) > 0:
            warnings.warn("%s fileds are useless." % ",".join(memeber_set))
        


class PrestoMonitorMetrics(AbstractModel):
    """Presto监控指标

    """

    def __init__(self):
        r"""
        :param LocalCacheHitRate: 	Alluxio本地缓存命中率
注意：此字段可能返回 null，表示取不到有效值。
        :type LocalCacheHitRate: float
        :param FragmentCacheHitRate: Fragment缓存命中率
注意：此字段可能返回 null，表示取不到有效值。
        :type FragmentCacheHitRate: float
        """
        self.LocalCacheHitRate = None
        self.FragmentCacheHitRate = None


    def _deserialize(self, params):
        self.LocalCacheHitRate = params.get("LocalCacheHitRate")
        self.FragmentCacheHitRate = params.get("FragmentCacheHitRate")
        memeber_set = set(params.keys())
        for name, value in vars(self).items():
            if name in memeber_set:
                memeber_set.remove(name)
        if len(memeber_set) > 0:
            warnings.warn("%s fileds are useless." % ",".join(memeber_set))
        


class Price(AbstractModel):
    """价格信息

    """

    def __init__(self):
        r"""
        :param PayMode: 计费模式。0：按量计费；1：包年包月计费
        :type PayMode: int
        :param TimeUnit: 计费时长单位。按量计费下固定为s；包年包月计费下固定为m
        :type TimeUnit: str
        :param TimeSpan: 计费时长。按量计费下固定为3600；包年包月计费下表示购买的月份
        :type TimeSpan: float
        :param TotalPrice: 总价
        :type TotalPrice: float
        :param TotalPriceDiscount: 总价的折扣价
        :type TotalPriceDiscount: float
        :param UnitPrice: 单价，按量计费下单位为元/CU/小时；包年包月下单位为元/CU/月
        :type UnitPrice: float
        :param OriginPrice: 原始价格
注意：此字段可能返回 null，表示取不到有效值。
        :type OriginPrice: float
        """
        self.PayMode = None
        self.TimeUnit = None
        self.TimeSpan = None
        self.TotalPrice = None
        self.TotalPriceDiscount = None
        self.UnitPrice = None
        self.OriginPrice = None


    def _deserialize(self, params):
        self.PayMode = params.get("PayMode")
        self.TimeUnit = params.get("TimeUnit")
        self.TimeSpan = params.get("TimeSpan")
        self.TotalPrice = params.get("TotalPrice")
        self.TotalPriceDiscount = params.get("TotalPriceDiscount")
        self.UnitPrice = params.get("UnitPrice")
        self.OriginPrice = params.get("OriginPrice")
        memeber_set = set(params.keys())
        for name, value in vars(self).items():
            if name in memeber_set:
                memeber_set.remove(name)
        if len(memeber_set) > 0:
            warnings.warn("%s fileds are useless." % ",".join(memeber_set))
        


class Property(AbstractModel):
    """数据库和数据表属性信息

    """

    def __init__(self):
        r"""
        :param Key: 属性key名称。
        :type Key: str
        :param Value: 属性key对应的value。
        :type Value: str
        """
        self.Key = None
        self.Value = None


    def _deserialize(self, params):
        self.Key = params.get("Key")
        self.Value = params.get("Value")
        memeber_set = set(params.keys())
        for name, value in vars(self).items():
            if name in memeber_set:
                memeber_set.remove(name)
        if len(memeber_set) > 0:
            warnings.warn("%s fileds are useless." % ",".join(memeber_set))
        


class PurviewInfo(AbstractModel):
    """查询脚本权限信息

    """

    def __init__(self):
        r"""
        :param WorkGroupSet: 用户组Id列表
注意：此字段可能返回 null，表示取不到有效值。
        :type WorkGroupSet: list of int
        :param UserSet: 用户id列表
注意：此字段可能返回 null，表示取不到有效值。
        :type UserSet: list of str
        :param PurviewSet: 权限范围：1-读取 2-修改 3-删除
注意：此字段可能返回 null，表示取不到有效值。
        :type PurviewSet: list of int
        """
        self.WorkGroupSet = None
        self.UserSet = None
        self.PurviewSet = None


    def _deserialize(self, params):
        self.WorkGroupSet = params.get("WorkGroupSet")
        self.UserSet = params.get("UserSet")
        self.PurviewSet = params.get("PurviewSet")
        memeber_set = set(params.keys())
        for name, value in vars(self).items():
            if name in memeber_set:
                memeber_set.remove(name)
        if len(memeber_set) > 0:
            warnings.warn("%s fileds are useless." % ",".join(memeber_set))
        


class PythonSparkImage(AbstractModel):
    """python-spark镜像信息。

    """

    def __init__(self):
        r"""
        :param SparkImageId: spark镜像唯一id
        :type SparkImageId: str
        :param ChildImageVersionId: 集群小版本镜像id
        :type ChildImageVersionId: str
        :param SparkImageVersion: spark镜像名称
        :type SparkImageVersion: str
        :param Description: spark镜像描述信息
注意：此字段可能返回 null，表示取不到有效值。
        :type Description: str
        :param CreateTime: 创建时间
        :type CreateTime: str
        :param UpdateTime: 更新时间
        :type UpdateTime: str
        """
        self.SparkImageId = None
        self.ChildImageVersionId = None
        self.SparkImageVersion = None
        self.Description = None
        self.CreateTime = None
        self.UpdateTime = None


    def _deserialize(self, params):
        self.SparkImageId = params.get("SparkImageId")
        self.ChildImageVersionId = params.get("ChildImageVersionId")
        self.SparkImageVersion = params.get("SparkImageVersion")
        self.Description = params.get("Description")
        self.CreateTime = params.get("CreateTime")
        self.UpdateTime = params.get("UpdateTime")
        memeber_set = set(params.keys())
        for name, value in vars(self).items():
            if name in memeber_set:
                memeber_set.remove(name)
        if len(memeber_set) > 0:
            warnings.warn("%s fileds are useless." % ",".join(memeber_set))
        


class QueryInternalTableWarehouseRequest(AbstractModel):
    """QueryInternalTableWarehouse请求参数结构体

    """

    def __init__(self):
        r"""
        :param DatabaseName: 库名
        :type DatabaseName: str
        :param TableName: 表名
        :type TableName: str
        """
        self.DatabaseName = None
        self.TableName = None


    def _deserialize(self, params):
        self.DatabaseName = params.get("DatabaseName")
        self.TableName = params.get("TableName")
        memeber_set = set(params.keys())
        for name, value in vars(self).items():
            if name in memeber_set:
                memeber_set.remove(name)
        if len(memeber_set) > 0:
            warnings.warn("%s fileds are useless." % ",".join(memeber_set))
        


class QueryInternalTableWarehouseResponse(AbstractModel):
    """QueryInternalTableWarehouse返回参数结构体

    """

    def __init__(self):
        r"""
        :param WarehousePath: warehouse路径
        :type WarehousePath: str
        :param RequestId: 唯一请求 ID，每次请求都会返回。定位问题时需要提供该次请求的 RequestId。
        :type RequestId: str
        """
        self.WarehousePath = None
        self.RequestId = None


    def _deserialize(self, params):
        self.WarehousePath = params.get("WarehousePath")
        self.RequestId = params.get("RequestId")


class QueryResultRequest(AbstractModel):
    """QueryResult请求参数结构体

    """

    def __init__(self):
        r"""
        :param TaskId: 任务ID
        :type TaskId: str
        :param NextToken: lastReadFile为上一次读取的文件，lastReadOffset为上一次读取到的位置
        :type NextToken: str
        :param Config: 配置信息，key-value数组，对外不可见。key1：AuthorityRole（鉴权角色，默认传SubUin，base64加密，仅在jdbc提交任务时使用）
        :type Config: list of KVPair
        """
        self.TaskId = None
        self.NextToken = None
        self.Config = None


    def _deserialize(self, params):
        self.TaskId = params.get("TaskId")
        self.NextToken = params.get("NextToken")
        if params.get("Config") is not None:
            self.Config = []
            for item in params.get("Config"):
                obj = KVPair()
                obj._deserialize(item)
                self.Config.append(obj)
        memeber_set = set(params.keys())
        for name, value in vars(self).items():
            if name in memeber_set:
                memeber_set.remove(name)
        if len(memeber_set) > 0:
            warnings.warn("%s fileds are useless." % ",".join(memeber_set))
        


class QueryResultResponse(AbstractModel):
    """QueryResult返回参数结构体

    """

    def __init__(self):
        r"""
        :param TaskId: 任务Id
        :type TaskId: str
        :param ResultSet: 结果数据
        :type ResultSet: str
        :param ResultSchema: schema
        :type ResultSchema: list of Column
        :param NextToken: 分页信息
注意：此字段可能返回 null，表示取不到有效值。
        :type NextToken: str
        :param RequestId: 唯一请求 ID，每次请求都会返回。定位问题时需要提供该次请求的 RequestId。
        :type RequestId: str
        """
        self.TaskId = None
        self.ResultSet = None
        self.ResultSchema = None
        self.NextToken = None
        self.RequestId = None


    def _deserialize(self, params):
        self.TaskId = params.get("TaskId")
        self.ResultSet = params.get("ResultSet")
        if params.get("ResultSchema") is not None:
            self.ResultSchema = []
            for item in params.get("ResultSchema"):
                obj = Column()
                obj._deserialize(item)
                self.ResultSchema.append(obj)
        self.NextToken = params.get("NextToken")
        self.RequestId = params.get("RequestId")


class QuerySparkImageUserRecordsRequest(AbstractModel):
    """QuerySparkImageUserRecords请求参数结构体

    """

    def __init__(self):
        r"""
        :param ImageId: 镜像编码
        :type ImageId: str
        :param UserAppId: 用户APPID
        :type UserAppId: int
        :param Limit: 分页字段
        :type Limit: int
        :param Offset: 分页字段
        :type Offset: int
        """
        self.ImageId = None
        self.UserAppId = None
        self.Limit = None
        self.Offset = None


    def _deserialize(self, params):
        self.ImageId = params.get("ImageId")
        self.UserAppId = params.get("UserAppId")
        self.Limit = params.get("Limit")
        self.Offset = params.get("Offset")
        memeber_set = set(params.keys())
        for name, value in vars(self).items():
            if name in memeber_set:
                memeber_set.remove(name)
        if len(memeber_set) > 0:
            warnings.warn("%s fileds are useless." % ",".join(memeber_set))
        


class QuerySparkImageUserRecordsResponse(AbstractModel):
    """QuerySparkImageUserRecords返回参数结构体

    """

    def __init__(self):
        r"""
        :param Total: 总数
        :type Total: int
        :param SparkImagesUserRecords: 用户私有镜像列表
        :type SparkImagesUserRecords: list of SparkImagesUserRecord
        :param RequestId: 唯一请求 ID，每次请求都会返回。定位问题时需要提供该次请求的 RequestId。
        :type RequestId: str
        """
        self.Total = None
        self.SparkImagesUserRecords = None
        self.RequestId = None


    def _deserialize(self, params):
        self.Total = params.get("Total")
        if params.get("SparkImagesUserRecords") is not None:
            self.SparkImagesUserRecords = []
            for item in params.get("SparkImagesUserRecords"):
                obj = SparkImagesUserRecord()
                obj._deserialize(item)
                self.SparkImagesUserRecords.append(obj)
        self.RequestId = params.get("RequestId")


class QuerySparkImagesRequest(AbstractModel):
    """QuerySparkImages请求参数结构体

    """

    def __init__(self):
        r"""
        :param ImageVersion: 镜像version
        :type ImageVersion: str
        :param ImageId: 镜像编号
        :type ImageId: str
        :param Limit: 分页字段
        :type Limit: int
        :param Offset: 分页字段
        :type Offset: int
        """
        self.ImageVersion = None
        self.ImageId = None
        self.Limit = None
        self.Offset = None


    def _deserialize(self, params):
        self.ImageVersion = params.get("ImageVersion")
        self.ImageId = params.get("ImageId")
        self.Limit = params.get("Limit")
        self.Offset = params.get("Offset")
        memeber_set = set(params.keys())
        for name, value in vars(self).items():
            if name in memeber_set:
                memeber_set.remove(name)
        if len(memeber_set) > 0:
            warnings.warn("%s fileds are useless." % ",".join(memeber_set))
        


class QuerySparkImagesResponse(AbstractModel):
    """QuerySparkImages返回参数结构体

    """

    def __init__(self):
        r"""
        :param Total: 总数
        :type Total: int
        :param SparkImages: 镜像信息列表
        :type SparkImages: list of SparkImage
        :param RequestId: 唯一请求 ID，每次请求都会返回。定位问题时需要提供该次请求的 RequestId。
        :type RequestId: str
        """
        self.Total = None
        self.SparkImages = None
        self.RequestId = None


    def _deserialize(self, params):
        self.Total = params.get("Total")
        if params.get("SparkImages") is not None:
            self.SparkImages = []
            for item in params.get("SparkImages"):
                obj = SparkImage()
                obj._deserialize(item)
                self.SparkImages.append(obj)
        self.RequestId = params.get("RequestId")


class QuerySystemStorageRequest(AbstractModel):
    """QuerySystemStorage请求参数结构体

    """

    def __init__(self):
        r"""
        :param Type: 目录类型，如0为数据导入临时目录，1为udf使用临时目录
        :type Type: int
        """
        self.Type = None


    def _deserialize(self, params):
        self.Type = params.get("Type")
        memeber_set = set(params.keys())
        for name, value in vars(self).items():
            if name in memeber_set:
                memeber_set.remove(name)
        if len(memeber_set) > 0:
            warnings.warn("%s fileds are useless." % ",".join(memeber_set))
        


class QuerySystemStorageResponse(AbstractModel):
    """QuerySystemStorage返回参数结构体

    """

    def __init__(self):
        r"""
        :param LakeFileSystem: LakeFileSystem信息
        :type LakeFileSystem: :class:`tencentcloud.dlc.v20210125.models.LakeFileSystem`
        :param RequestId: 唯一请求 ID，每次请求都会返回。定位问题时需要提供该次请求的 RequestId。
        :type RequestId: str
        """
        self.LakeFileSystem = None
        self.RequestId = None


    def _deserialize(self, params):
        if params.get("LakeFileSystem") is not None:
            self.LakeFileSystem = LakeFileSystem()
            self.LakeFileSystem._deserialize(params.get("LakeFileSystem"))
        self.RequestId = params.get("RequestId")


class QueryTaskResultRequest(AbstractModel):
    """QueryTaskResult请求参数结构体

    """

    def __init__(self):
        r"""
        :param TaskId: 任务唯一ID
        :type TaskId: str
        :param NextToken: 上一次请求响应返回的分页信息。第一次可以不带，从头开始返回数据，每次返回1000行数据。
        :type NextToken: str
        :param MaxResults: 返回结果的最大行数，范围0~1000，默认为1000.
        :type MaxResults: int
        """
        self.TaskId = None
        self.NextToken = None
        self.MaxResults = None


    def _deserialize(self, params):
        self.TaskId = params.get("TaskId")
        self.NextToken = params.get("NextToken")
        self.MaxResults = params.get("MaxResults")
        memeber_set = set(params.keys())
        for name, value in vars(self).items():
            if name in memeber_set:
                memeber_set.remove(name)
        if len(memeber_set) > 0:
            warnings.warn("%s fileds are useless." % ",".join(memeber_set))
        


class QueryTaskResultResponse(AbstractModel):
    """QueryTaskResult返回参数结构体

    """

    def __init__(self):
        r"""
        :param TaskInfo: 查询的任务信息，返回为空表示输入任务ID对应的任务不存在。只有当任务状态为成功（2）的时候，才会返回任务的结果。
注意：此字段可能返回 null，表示取不到有效值。
        :type TaskInfo: :class:`tencentcloud.dlc.v20210125.models.TaskResultInfo`
        :param RequestId: 唯一请求 ID，每次请求都会返回。定位问题时需要提供该次请求的 RequestId。
        :type RequestId: str
        """
        self.TaskInfo = None
        self.RequestId = None


    def _deserialize(self, params):
        if params.get("TaskInfo") is not None:
            self.TaskInfo = TaskResultInfo()
            self.TaskInfo._deserialize(params.get("TaskInfo"))
        self.RequestId = params.get("RequestId")


class RemoveOrphanFilesInfo(AbstractModel):
    """移除孤立文件数据治理项信息

    """

    def __init__(self):
        r"""
        :param RemoveOrphanFilesEnable: 是否启用移除孤立文件治理项：enable、none
        :type RemoveOrphanFilesEnable: str
        :param Engine: 用于运行移除孤立文件治理项的引擎名称
        :type Engine: str
        :param BeforeDays: 移除指定天前的孤立文件
        :type BeforeDays: int
        :param MaxConcurrentDeletes: 移除孤立文件的并行数
        :type MaxConcurrentDeletes: int
        :param IntervalMin: 移除孤立文件治理运行周期，单位为分钟
        :type IntervalMin: int
        """
        self.RemoveOrphanFilesEnable = None
        self.Engine = None
        self.BeforeDays = None
        self.MaxConcurrentDeletes = None
        self.IntervalMin = None


    def _deserialize(self, params):
        self.RemoveOrphanFilesEnable = params.get("RemoveOrphanFilesEnable")
        self.Engine = params.get("Engine")
        self.BeforeDays = params.get("BeforeDays")
        self.MaxConcurrentDeletes = params.get("MaxConcurrentDeletes")
        self.IntervalMin = params.get("IntervalMin")
        memeber_set = set(params.keys())
        for name, value in vars(self).items():
            if name in memeber_set:
                memeber_set.remove(name)
        if len(memeber_set) > 0:
            warnings.warn("%s fileds are useless." % ",".join(memeber_set))
        


class RemoveTaskRequest(AbstractModel):
    """RemoveTask请求参数结构体

    """

    def __init__(self):
        r"""
        :param Task: 任务数据
        :type Task: :class:`tencentcloud.dlc.v20210125.models.TaskDto`
        """
        self.Task = None


    def _deserialize(self, params):
        if params.get("Task") is not None:
            self.Task = TaskDto()
            self.Task._deserialize(params.get("Task"))
        memeber_set = set(params.keys())
        for name, value in vars(self).items():
            if name in memeber_set:
                memeber_set.remove(name)
        if len(memeber_set) > 0:
            warnings.warn("%s fileds are useless." % ",".join(memeber_set))
        


class RemoveTaskResponse(AbstractModel):
    """RemoveTask返回参数结构体

    """

    def __init__(self):
        r"""
        :param RequestId: 唯一请求 ID，每次请求都会返回。定位问题时需要提供该次请求的 RequestId。
        :type RequestId: str
        """
        self.RequestId = None


    def _deserialize(self, params):
        self.RequestId = params.get("RequestId")


class RenewDataEngineRequest(AbstractModel):
    """RenewDataEngine请求参数结构体

    """

    def __init__(self):
        r"""
        :param DataEngineName: CU队列名称
        :type DataEngineName: str
        :param TimeSpan: 续费时长，单位月，最少续费1一个月
        :type TimeSpan: int
        :param PayMode: 付费类型，默认为1，预付费
        :type PayMode: int
        :param TimeUnit: 单位，默认m，仅能填m
        :type TimeUnit: str
        :param RenewFlag: 自动续费标志，0，初始状态，默认不自动续费，若用户有预付费不停服特权，自动续费。1：自动续费。2：明确不自动续费。不传该参数默认为0
        :type RenewFlag: int
        """
        self.DataEngineName = None
        self.TimeSpan = None
        self.PayMode = None
        self.TimeUnit = None
        self.RenewFlag = None


    def _deserialize(self, params):
        self.DataEngineName = params.get("DataEngineName")
        self.TimeSpan = params.get("TimeSpan")
        self.PayMode = params.get("PayMode")
        self.TimeUnit = params.get("TimeUnit")
        self.RenewFlag = params.get("RenewFlag")
        memeber_set = set(params.keys())
        for name, value in vars(self).items():
            if name in memeber_set:
                memeber_set.remove(name)
        if len(memeber_set) > 0:
            warnings.warn("%s fileds are useless." % ",".join(memeber_set))
        


class RenewDataEngineResponse(AbstractModel):
    """RenewDataEngine返回参数结构体

    """

    def __init__(self):
        r"""
        :param RequestId: 唯一请求 ID，每次请求都会返回。定位问题时需要提供该次请求的 RequestId。
        :type RequestId: str
        """
        self.RequestId = None


    def _deserialize(self, params):
        self.RequestId = params.get("RequestId")


class RenewHouseRequest(AbstractModel):
    """RenewHouse请求参数结构体

    """

    def __init__(self):
        r"""
        :param HouseName: CU队列名称
        :type HouseName: str
        :param TimeSpan: 续费时长，单位月，最少续费1一个月
        :type TimeSpan: int
        :param PayMode: 付费类型，默认为1，预付费
        :type PayMode: int
        :param TimeUnit: 单位，默认m，仅能填m
        :type TimeUnit: str
        """
        self.HouseName = None
        self.TimeSpan = None
        self.PayMode = None
        self.TimeUnit = None


    def _deserialize(self, params):
        self.HouseName = params.get("HouseName")
        self.TimeSpan = params.get("TimeSpan")
        self.PayMode = params.get("PayMode")
        self.TimeUnit = params.get("TimeUnit")
        memeber_set = set(params.keys())
        for name, value in vars(self).items():
            if name in memeber_set:
                memeber_set.remove(name)
        if len(memeber_set) > 0:
            warnings.warn("%s fileds are useless." % ",".join(memeber_set))
        


class RenewHouseResponse(AbstractModel):
    """RenewHouse返回参数结构体

    """

    def __init__(self):
        r"""
        :param RequestId: 唯一请求 ID，每次请求都会返回。定位问题时需要提供该次请求的 RequestId。
        :type RequestId: str
        """
        self.RequestId = None


    def _deserialize(self, params):
        self.RequestId = params.get("RequestId")


class ReportHeartbeatMetaDataRequest(AbstractModel):
    """ReportHeartbeatMetaData请求参数结构体

    """

    def __init__(self):
        r"""
        :param DatasourceConnectionName: 数据源名称
        :type DatasourceConnectionName: str
        :param LockId: 锁ID
        :type LockId: int
        :param TxnId: 事务ID
        :type TxnId: int
        """
        self.DatasourceConnectionName = None
        self.LockId = None
        self.TxnId = None


    def _deserialize(self, params):
        self.DatasourceConnectionName = params.get("DatasourceConnectionName")
        self.LockId = params.get("LockId")
        self.TxnId = params.get("TxnId")
        memeber_set = set(params.keys())
        for name, value in vars(self).items():
            if name in memeber_set:
                memeber_set.remove(name)
        if len(memeber_set) > 0:
            warnings.warn("%s fileds are useless." % ",".join(memeber_set))
        


class ReportHeartbeatMetaDataResponse(AbstractModel):
    """ReportHeartbeatMetaData返回参数结构体

    """

    def __init__(self):
        r"""
        :param RequestId: 唯一请求 ID，每次请求都会返回。定位问题时需要提供该次请求的 RequestId。
        :type RequestId: str
        """
        self.RequestId = None


    def _deserialize(self, params):
        self.RequestId = params.get("RequestId")


class RerunScheduleTaskInstancesRequest(AbstractModel):
    """RerunScheduleTaskInstances请求参数结构体

    """

    def __init__(self):
        r"""
        :param ReRunType: 重跑类型:自身（1），孩子（3），自身及孩子（2)
        :type ReRunType: str
        :param CheckFather: 是否检查父实例
        :type CheckFather: bool
        :param Instances: 重跑实例信息
        :type Instances: list of ScheduleInstanceRunInfo
        """
        self.ReRunType = None
        self.CheckFather = None
        self.Instances = None


    def _deserialize(self, params):
        self.ReRunType = params.get("ReRunType")
        self.CheckFather = params.get("CheckFather")
        if params.get("Instances") is not None:
            self.Instances = []
            for item in params.get("Instances"):
                obj = ScheduleInstanceRunInfo()
                obj._deserialize(item)
                self.Instances.append(obj)
        memeber_set = set(params.keys())
        for name, value in vars(self).items():
            if name in memeber_set:
                memeber_set.remove(name)
        if len(memeber_set) > 0:
            warnings.warn("%s fileds are useless." % ",".join(memeber_set))
        


class RerunScheduleTaskInstancesResponse(AbstractModel):
    """RerunScheduleTaskInstances返回参数结构体

    """

    def __init__(self):
        r"""
        :param Result: 重跑实例提交结果
        :type Result: bool
        :param RequestId: 唯一请求 ID，每次请求都会返回。定位问题时需要提供该次请求的 RequestId。
        :type RequestId: str
        """
        self.Result = None
        self.RequestId = None


    def _deserialize(self, params):
        self.Result = params.get("Result")
        self.RequestId = params.get("RequestId")


class RestartDataEngineRequest(AbstractModel):
    """RestartDataEngine请求参数结构体

    """

    def __init__(self):
        r"""
        :param DataEngineId: 引擎ID
        :type DataEngineId: str
        :param ForcedOperation: 是否强制重启，忽略任务
        :type ForcedOperation: bool
        """
        self.DataEngineId = None
        self.ForcedOperation = None


    def _deserialize(self, params):
        self.DataEngineId = params.get("DataEngineId")
        self.ForcedOperation = params.get("ForcedOperation")
        memeber_set = set(params.keys())
        for name, value in vars(self).items():
            if name in memeber_set:
                memeber_set.remove(name)
        if len(memeber_set) > 0:
            warnings.warn("%s fileds are useless." % ",".join(memeber_set))
        


class RestartDataEngineResponse(AbstractModel):
    """RestartDataEngine返回参数结构体

    """

    def __init__(self):
        r"""
        :param RequestId: 唯一请求 ID，每次请求都会返回。定位问题时需要提供该次请求的 RequestId。
        :type RequestId: str
        """
        self.RequestId = None


    def _deserialize(self, params):
        self.RequestId = params.get("RequestId")


class ResultExportResponseInfo(AbstractModel):
    """结果数据导出信息

    """

    def __init__(self):
        r"""
        :param TaskId: 任务ID
        :type TaskId: str
        :param TaskInfo: 文件名路径等信息
注意：此字段可能返回 null，表示取不到有效值。
        :type TaskInfo: str
        :param State: 状态
        :type State: int
        :param Message: 错误信息
        :type Message: str
        :param CreateTime: 时间戳
        :type CreateTime: str
        :param UpdateTime: 时间戳
注意：此字段可能返回 null，表示取不到有效值。
        :type UpdateTime: str
        :param DataAmount: 数据大小
注意：此字段可能返回 null，表示取不到有效值。
        :type DataAmount: int
        """
        self.TaskId = None
        self.TaskInfo = None
        self.State = None
        self.Message = None
        self.CreateTime = None
        self.UpdateTime = None
        self.DataAmount = None


    def _deserialize(self, params):
        self.TaskId = params.get("TaskId")
        self.TaskInfo = params.get("TaskInfo")
        self.State = params.get("State")
        self.Message = params.get("Message")
        self.CreateTime = params.get("CreateTime")
        self.UpdateTime = params.get("UpdateTime")
        self.DataAmount = params.get("DataAmount")
        memeber_set = set(params.keys())
        for name, value in vars(self).items():
            if name in memeber_set:
                memeber_set.remove(name)
        if len(memeber_set) > 0:
            warnings.warn("%s fileds are useless." % ",".join(memeber_set))
        


class RewriteDataInfo(AbstractModel):
    """数据重排布数据治理信息

    """

    def __init__(self):
        r"""
        :param RewriteDataEnable: 是否启用数据重排布治理项：enable（启动）、disable（不启用，默认）
        :type RewriteDataEnable: str
        :param Engine: 用于运行数据重排布治理项的引擎名称
        :type Engine: str
        :param MinInputFiles: 重排布任务执行的文件个数
        :type MinInputFiles: int
        :param TargetFileSizeBytes: 数据重排布写后的数据文件大小，单位为字节
        :type TargetFileSizeBytes: int
        :param IntervalMin: 数据重排布治理运行周期，单位为分钟
        :type IntervalMin: int
        """
        self.RewriteDataEnable = None
        self.Engine = None
        self.MinInputFiles = None
        self.TargetFileSizeBytes = None
        self.IntervalMin = None


    def _deserialize(self, params):
        self.RewriteDataEnable = params.get("RewriteDataEnable")
        self.Engine = params.get("Engine")
        self.MinInputFiles = params.get("MinInputFiles")
        self.TargetFileSizeBytes = params.get("TargetFileSizeBytes")
        self.IntervalMin = params.get("IntervalMin")
        memeber_set = set(params.keys())
        for name, value in vars(self).items():
            if name in memeber_set:
                memeber_set.remove(name)
        if len(memeber_set) > 0:
            warnings.warn("%s fileds are useless." % ",".join(memeber_set))
        


class RollbackDataEngineImageRequest(AbstractModel):
    """RollbackDataEngineImage请求参数结构体

    """

    def __init__(self):
        r"""
        :param DataEngineId: 引擎ID
        :type DataEngineId: str
        :param FromRecordId: 检查是否能回滚的接口返回的FromRecordId参数
        :type FromRecordId: str
        :param ToRecordId: 检查是否能回滚的接口返回的ToRecordId参数
        :type ToRecordId: str
        """
        self.DataEngineId = None
        self.FromRecordId = None
        self.ToRecordId = None


    def _deserialize(self, params):
        self.DataEngineId = params.get("DataEngineId")
        self.FromRecordId = params.get("FromRecordId")
        self.ToRecordId = params.get("ToRecordId")
        memeber_set = set(params.keys())
        for name, value in vars(self).items():
            if name in memeber_set:
                memeber_set.remove(name)
        if len(memeber_set) > 0:
            warnings.warn("%s fileds are useless." % ",".join(memeber_set))
        


class RollbackDataEngineImageResponse(AbstractModel):
    """RollbackDataEngineImage返回参数结构体

    """

    def __init__(self):
        r"""
        :param RequestId: 唯一请求 ID，每次请求都会返回。定位问题时需要提供该次请求的 RequestId。
        :type RequestId: str
        """
        self.RequestId = None


    def _deserialize(self, params):
        self.RequestId = params.get("RequestId")


class RuleThreshold(AbstractModel):
    """数据治理事件规则阈值定义

    """

    def __init__(self):
        r"""
        :param AddDataFiles: 增加的文件数量阈值, 超过值将触发小文件合并
        :type AddDataFiles: int
        :param AddEqualityDeletes: 增加的Equality delete数量阈值, 超过值将触发小文件合并
        :type AddEqualityDeletes: int
        :param AddPositionDeletes: 增加的Position delete数量阈值, 超过值将触发小文件合并
        :type AddPositionDeletes: int
        :param AddDeleteFiles: 增加的delete file数量阈值，过期快照的AddDataFiles + AddDeleteFiles的总和大于阈值AddDataFiles + AddDeleteFiles将从该快照处删除快照
        :type AddDeleteFiles: int
        """
        self.AddDataFiles = None
        self.AddEqualityDeletes = None
        self.AddPositionDeletes = None
        self.AddDeleteFiles = None


    def _deserialize(self, params):
        self.AddDataFiles = params.get("AddDataFiles")
        self.AddEqualityDeletes = params.get("AddEqualityDeletes")
        self.AddPositionDeletes = params.get("AddPositionDeletes")
        self.AddDeleteFiles = params.get("AddDeleteFiles")
        memeber_set = set(params.keys())
        for name, value in vars(self).items():
            if name in memeber_set:
                memeber_set.remove(name)
        if len(memeber_set) > 0:
            warnings.warn("%s fileds are useless." % ",".join(memeber_set))
        


class RunScheduleTaskRequest(AbstractModel):
    """RunScheduleTask请求参数结构体

    """

    def __init__(self):
        r"""
        :param TaskIds: 调度任务ID列表
        :type TaskIds: list of str
        :param AutoRun: 是否自动启动，默认true
        :type AutoRun: bool
        """
        self.TaskIds = None
        self.AutoRun = None


    def _deserialize(self, params):
        self.TaskIds = params.get("TaskIds")
        self.AutoRun = params.get("AutoRun")
        memeber_set = set(params.keys())
        for name, value in vars(self).items():
            if name in memeber_set:
                memeber_set.remove(name)
        if len(memeber_set) > 0:
            warnings.warn("%s fileds are useless." % ",".join(memeber_set))
        


class RunScheduleTaskResponse(AbstractModel):
    """RunScheduleTask返回参数结构体

    """

    def __init__(self):
        r"""
        :param Result: 启动调度任务请求结果
        :type Result: bool
        :param RequestId: 唯一请求 ID，每次请求都会返回。定位问题时需要提供该次请求的 RequestId。
        :type RequestId: str
        """
        self.Result = None
        self.RequestId = None


    def _deserialize(self, params):
        self.Result = params.get("Result")
        self.RequestId = params.get("RequestId")


class SQLSessionCatalogInfo(AbstractModel):
    """SQL Session快照列表信息。

    """

    def __init__(self):
        r"""
        :param Id: 会话ID
        :type Id: str
        :param Name: 会话名称
        :type Name: str
        :param Operator: 操作人
        :type Operator: str
        :param CreateTime: 会话创建时间
        :type CreateTime: str
        :param UpdateTime: 会话更新时间
        :type UpdateTime: str
        :param LastUsed: 会话最近一次打开时间
        :type LastUsed: str
        :param IsOpened: 会话是否被打开：0（关闭，默认）；1（打开）
        :type IsOpened: int
        :param Type: 节点类型：0：目录节点、1：会话节点
        :type Type: str
        :param Version: 版本号：更新时会迭代，用于做更新校验
        :type Version: int
        :param Path: 父节点目录信息
        :type Path: str
        :param UserVisibility: 授权的子用户，空为自己和管理员可见
注意：此字段可能返回 null，表示取不到有效值。
        :type UserVisibility: str
        """
        self.Id = None
        self.Name = None
        self.Operator = None
        self.CreateTime = None
        self.UpdateTime = None
        self.LastUsed = None
        self.IsOpened = None
        self.Type = None
        self.Version = None
        self.Path = None
        self.UserVisibility = None


    def _deserialize(self, params):
        self.Id = params.get("Id")
        self.Name = params.get("Name")
        self.Operator = params.get("Operator")
        self.CreateTime = params.get("CreateTime")
        self.UpdateTime = params.get("UpdateTime")
        self.LastUsed = params.get("LastUsed")
        self.IsOpened = params.get("IsOpened")
        self.Type = params.get("Type")
        self.Version = params.get("Version")
        self.Path = params.get("Path")
        self.UserVisibility = params.get("UserVisibility")
        memeber_set = set(params.keys())
        for name, value in vars(self).items():
            if name in memeber_set:
                memeber_set.remove(name)
        if len(memeber_set) > 0:
            warnings.warn("%s fileds are useless." % ",".join(memeber_set))
        


class SQLSessionSnapshotBaseInfo(AbstractModel):
    """SQL Session快照列表信息。

    """

    def __init__(self):
        r"""
        :param SessionId: 会话ID
        :type SessionId: str
        :param SessionName: 会话名称
        :type SessionName: str
        :param Operator: 操作人
        :type Operator: str
        :param CreateTime: 会话创建时间
        :type CreateTime: str
        :param UpdateTime: 会话更新时间
        :type UpdateTime: str
        :param LastUsed: 会话最近一次打开时间
注意：此字段可能返回 null，表示取不到有效值。
        :type LastUsed: str
        :param IsOpened: 会话是否被打开：0（关闭，默认）；1（打开）
注意：此字段可能返回 null，表示取不到有效值。
        :type IsOpened: int
        """
        self.SessionId = None
        self.SessionName = None
        self.Operator = None
        self.CreateTime = None
        self.UpdateTime = None
        self.LastUsed = None
        self.IsOpened = None


    def _deserialize(self, params):
        self.SessionId = params.get("SessionId")
        self.SessionName = params.get("SessionName")
        self.Operator = params.get("Operator")
        self.CreateTime = params.get("CreateTime")
        self.UpdateTime = params.get("UpdateTime")
        self.LastUsed = params.get("LastUsed")
        self.IsOpened = params.get("IsOpened")
        memeber_set = set(params.keys())
        for name, value in vars(self).items():
            if name in memeber_set:
                memeber_set.remove(name)
        if len(memeber_set) > 0:
            warnings.warn("%s fileds are useless." % ",".join(memeber_set))
        


class SQLSessionSnapshotInfo(AbstractModel):
    """SQL会话快照信息。

    """

    def __init__(self):
        r"""
        :param SessionName: 会话名称
        :type SessionName: str
        :param SessionResourceConfig: 会话资源配置
        :type SessionResourceConfig: :class:`tencentcloud.dlc.v20210125.models.SessionResourceConfig`
        :param Operator: 操作人
        :type Operator: str
        :param SessionId: 会话ID
注意：此字段可能返回 null，表示取不到有效值。
        :type SessionId: str
        :param SessionSQL: 会话SQL
注意：此字段可能返回 null，表示取不到有效值。
        :type SessionSQL: str
        :param SessionSQLSelection: SQL选中区域
注意：此字段可能返回 null，表示取不到有效值。
        :type SessionSQLSelection: str
        :param CreateTime: 会话创建时间
注意：此字段可能返回 null，表示取不到有效值。
        :type CreateTime: str
        :param UpdateTime: 会话更新时间
注意：此字段可能返回 null，表示取不到有效值。
        :type UpdateTime: str
        :param State: 会话状态：0：初始化、1：正常、2：已删除
注意：此字段可能返回 null，表示取不到有效值。
        :type State: str
        :param LastUsed: 会话最近一次打开时间
注意：此字段可能返回 null，表示取不到有效值。
        :type LastUsed: str
        :param IsOpened: 会话是否被打开：0（关闭，默认）；1（打开）
注意：此字段可能返回 null，表示取不到有效值。
        :type IsOpened: int
        :param Params: 会话参数，json结构
注意：此字段可能返回 null，表示取不到有效值。
        :type Params: list of Config
        :param Version: 更新时校验版本号
        :type Version: int
        :param Path: 会话路径
        :type Path: str
        :param IsMove: 是否移动目录：0（默认，不移动）、1（移动）
        :type IsMove: int
        :param ViewKey: 记录历史运行用户选择的可视化关键词，包含：BatchId、SessionSQL、ComputeEngine、ComputeResource、DataAmount、DataNumber、DeployStatus、SubmitTime
        :type ViewKey: list of str
        :param UserVisibility: 授权的子用户，空为自己和管理员可见
注意：此字段可能返回 null，表示取不到有效值。
        :type UserVisibility: str
        :param PurviewInfoSet: 权限组信息
注意：此字段可能返回 null，表示取不到有效值。
        :type PurviewInfoSet: list of PurviewInfo
        """
        self.SessionName = None
        self.SessionResourceConfig = None
        self.Operator = None
        self.SessionId = None
        self.SessionSQL = None
        self.SessionSQLSelection = None
        self.CreateTime = None
        self.UpdateTime = None
        self.State = None
        self.LastUsed = None
        self.IsOpened = None
        self.Params = None
        self.Version = None
        self.Path = None
        self.IsMove = None
        self.ViewKey = None
        self.UserVisibility = None
        self.PurviewInfoSet = None


    def _deserialize(self, params):
        self.SessionName = params.get("SessionName")
        if params.get("SessionResourceConfig") is not None:
            self.SessionResourceConfig = SessionResourceConfig()
            self.SessionResourceConfig._deserialize(params.get("SessionResourceConfig"))
        self.Operator = params.get("Operator")
        self.SessionId = params.get("SessionId")
        self.SessionSQL = params.get("SessionSQL")
        self.SessionSQLSelection = params.get("SessionSQLSelection")
        self.CreateTime = params.get("CreateTime")
        self.UpdateTime = params.get("UpdateTime")
        self.State = params.get("State")
        self.LastUsed = params.get("LastUsed")
        self.IsOpened = params.get("IsOpened")
        if params.get("Params") is not None:
            self.Params = []
            for item in params.get("Params"):
                obj = Config()
                obj._deserialize(item)
                self.Params.append(obj)
        self.Version = params.get("Version")
        self.Path = params.get("Path")
        self.IsMove = params.get("IsMove")
        self.ViewKey = params.get("ViewKey")
        self.UserVisibility = params.get("UserVisibility")
        if params.get("PurviewInfoSet") is not None:
            self.PurviewInfoSet = []
            for item in params.get("PurviewInfoSet"):
                obj = PurviewInfo()
                obj._deserialize(item)
                self.PurviewInfoSet.append(obj)
        memeber_set = set(params.keys())
        for name, value in vars(self).items():
            if name in memeber_set:
                memeber_set.remove(name)
        if len(memeber_set) > 0:
            warnings.warn("%s fileds are useless." % ",".join(memeber_set))
        


class SQLSessionSubmitRecord(AbstractModel):
    """获取SQL会话提交记录详情。

    """

    def __init__(self):
        r"""
        :param SessionId: 会话ID
        :type SessionId: str
        :param BatchId: 批量提交任务ID
        :type BatchId: str
        :param TaskIdSet: 任务ID集合
        :type TaskIdSet: list of str
        :param DeployStatus: 批量执行状态，INIT（初始化，默认）、SUCCESS（成功）、PARTIAL-SUCCESS （部分成功）、FAIL（失败）
注意：此字段可能返回 null，表示取不到有效值。
        :type DeployStatus: str
        :param SuccessNumber: 任务成功数量
注意：此字段可能返回 null，表示取不到有效值。
        :type SuccessNumber: int
        :param FailNumber: 任务失败数量
注意：此字段可能返回 null，表示取不到有效值。
        :type FailNumber: int
        :param SubmitTime: 任务提交时间
        :type SubmitTime: str
        :param WaitNumber: 等待中的任务
注意：此字段可能返回 null，表示取不到有效值。
        :type WaitNumber: int
        :param SessionSQL: 会话SQL
注意：此字段可能返回 null，表示取不到有效值。
        :type SessionSQL: str
        :param ComputeEngine: 执行引擎
注意：此字段可能返回 null，表示取不到有效值。
        :type ComputeEngine: str
        :param ComputeResource: 计算资源
注意：此字段可能返回 null，表示取不到有效值。
        :type ComputeResource: str
        :param DataAmount: 扫描量
注意：此字段可能返回 null，表示取不到有效值。
        :type DataAmount: int
        :param DataNumber: 数据条数
注意：此字段可能返回 null，表示取不到有效值。
        :type DataNumber: int
        :param TotalTime: 任务总耗时：单位ms
注意：此字段可能返回 null，表示取不到有效值。
        :type TotalTime: int
        :param UsedTime: 任务计算耗时：单位ms
注意：此字段可能返回 null，表示取不到有效值。
        :type UsedTime: int
        :param TotalNumber: 总的任务数
        :type TotalNumber: int
        """
        self.SessionId = None
        self.BatchId = None
        self.TaskIdSet = None
        self.DeployStatus = None
        self.SuccessNumber = None
        self.FailNumber = None
        self.SubmitTime = None
        self.WaitNumber = None
        self.SessionSQL = None
        self.ComputeEngine = None
        self.ComputeResource = None
        self.DataAmount = None
        self.DataNumber = None
        self.TotalTime = None
        self.UsedTime = None
        self.TotalNumber = None


    def _deserialize(self, params):
        self.SessionId = params.get("SessionId")
        self.BatchId = params.get("BatchId")
        self.TaskIdSet = params.get("TaskIdSet")
        self.DeployStatus = params.get("DeployStatus")
        self.SuccessNumber = params.get("SuccessNumber")
        self.FailNumber = params.get("FailNumber")
        self.SubmitTime = params.get("SubmitTime")
        self.WaitNumber = params.get("WaitNumber")
        self.SessionSQL = params.get("SessionSQL")
        self.ComputeEngine = params.get("ComputeEngine")
        self.ComputeResource = params.get("ComputeResource")
        self.DataAmount = params.get("DataAmount")
        self.DataNumber = params.get("DataNumber")
        self.TotalTime = params.get("TotalTime")
        self.UsedTime = params.get("UsedTime")
        self.TotalNumber = params.get("TotalNumber")
        memeber_set = set(params.keys())
        for name, value in vars(self).items():
            if name in memeber_set:
                memeber_set.remove(name)
        if len(memeber_set) > 0:
            warnings.warn("%s fileds are useless." % ",".join(memeber_set))
        


class SQLTask(AbstractModel):
    """SQL查询任务

    """

    def __init__(self):
        r"""
        :param SQL: base64加密后的SQL语句
        :type SQL: str
        :param Config: 任务的配置信息
        :type Config: list of KVPair
        """
        self.SQL = None
        self.Config = None


    def _deserialize(self, params):
        self.SQL = params.get("SQL")
        if params.get("Config") is not None:
            self.Config = []
            for item in params.get("Config"):
                obj = KVPair()
                obj._deserialize(item)
                self.Config.append(obj)
        memeber_set = set(params.keys())
        for name, value in vars(self).items():
            if name in memeber_set:
                memeber_set.remove(name)
        if len(memeber_set) > 0:
            warnings.warn("%s fileds are useless." % ",".join(memeber_set))
        


class SavePositionRequest(AbstractModel):
    """SavePosition请求参数结构体

    """

    def __init__(self):
        r"""
        :param WorkflowId: 调度计划ID
        :type WorkflowId: str
        :param Task: 任务数据
        :type Task: :class:`tencentcloud.dlc.v20210125.models.TaskDto`
        """
        self.WorkflowId = None
        self.Task = None


    def _deserialize(self, params):
        self.WorkflowId = params.get("WorkflowId")
        if params.get("Task") is not None:
            self.Task = TaskDto()
            self.Task._deserialize(params.get("Task"))
        memeber_set = set(params.keys())
        for name, value in vars(self).items():
            if name in memeber_set:
                memeber_set.remove(name)
        if len(memeber_set) > 0:
            warnings.warn("%s fileds are useless." % ",".join(memeber_set))
        


class SavePositionResponse(AbstractModel):
    """SavePosition返回参数结构体

    """

    def __init__(self):
        r"""
        :param RequestId: 唯一请求 ID，每次请求都会返回。定位问题时需要提供该次请求的 RequestId。
        :type RequestId: str
        """
        self.RequestId = None


    def _deserialize(self, params):
        self.RequestId = params.get("RequestId")


class ScheduleInstanceInfo(AbstractModel):
    """调度任务实例信息

    """

    def __init__(self):
        r"""
        :param TaskId: 调度任务ID
        :type TaskId: str
        :param TaskName: 调度任务名称
        :type TaskName: str
        :param ScriptName: 调度任务关联脚本名称
        :type ScriptName: str
        :param DataEngineName: 数据引擎名称
        :type DataEngineName: str
        :param CycleType: 调度周期类型，分钟(MINUTE_CYCLE)，小时(HOUR_CYCLE)，天(DAY_CYCLE)，周(WEEK_CYCLE),月(MONTH_CYCLE)，一次性(ONEOFF_CYCLE)
不支持修改
        :type CycleType: str
        :param CycleStep: 任务调度周期间隔
        :type CycleStep: int
        :param DelayTime: 调度任务延迟时间，从调度周期开始时间计算的分钟数
        :type DelayTime: int
        :param TaskAction: 指定周期的第几个单位，周日：1；周一：2，当月第1天：1，等
        :type TaskAction: str
        :param Status: 成功（2），失败（3），终止（8），等待调度（0，6，7，9），正在运行（1，10），正在终止（4，5）
        :type Status: str
        :param RetryCount: 重试次数
        :type RetryCount: int
        :param ScheduleRunTime: 实例运行时间
        :type ScheduleRunTime: str
        :param ScheduleBizTime: 实例运行数据时间
        :type ScheduleBizTime: str
        :param ComputeUseTime: 实例运行时间，ms
        :type ComputeUseTime: int
        :param DataScanVolume: 实例运行扫描量
        :type DataScanVolume: int
        """
        self.TaskId = None
        self.TaskName = None
        self.ScriptName = None
        self.DataEngineName = None
        self.CycleType = None
        self.CycleStep = None
        self.DelayTime = None
        self.TaskAction = None
        self.Status = None
        self.RetryCount = None
        self.ScheduleRunTime = None
        self.ScheduleBizTime = None
        self.ComputeUseTime = None
        self.DataScanVolume = None


    def _deserialize(self, params):
        self.TaskId = params.get("TaskId")
        self.TaskName = params.get("TaskName")
        self.ScriptName = params.get("ScriptName")
        self.DataEngineName = params.get("DataEngineName")
        self.CycleType = params.get("CycleType")
        self.CycleStep = params.get("CycleStep")
        self.DelayTime = params.get("DelayTime")
        self.TaskAction = params.get("TaskAction")
        self.Status = params.get("Status")
        self.RetryCount = params.get("RetryCount")
        self.ScheduleRunTime = params.get("ScheduleRunTime")
        self.ScheduleBizTime = params.get("ScheduleBizTime")
        self.ComputeUseTime = params.get("ComputeUseTime")
        self.DataScanVolume = params.get("DataScanVolume")
        memeber_set = set(params.keys())
        for name, value in vars(self).items():
            if name in memeber_set:
                memeber_set.remove(name)
        if len(memeber_set) > 0:
            warnings.warn("%s fileds are useless." % ",".join(memeber_set))
        


class ScheduleInstanceLog(AbstractModel):
    """调度任务实例运行日志

    """

    def __init__(self):
        r"""
        :param TaskId: 调度任务ID
        :type TaskId: str
        :param BatchId: 调度任务实例执行批次ID
        :type BatchId: str
        :param RetryCount: 重试次数
        :type RetryCount: int
        :param ScheduleBizTime: 调度任务数据时间
        :type ScheduleBizTime: str
        :param ComputeUseTime: 计算耗时
        :type ComputeUseTime: int
        :param DataScanVolume: 扫描量
        :type DataScanVolume: int
        :param Log: 日志
        :type Log: str
        """
        self.TaskId = None
        self.BatchId = None
        self.RetryCount = None
        self.ScheduleBizTime = None
        self.ComputeUseTime = None
        self.DataScanVolume = None
        self.Log = None


    def _deserialize(self, params):
        self.TaskId = params.get("TaskId")
        self.BatchId = params.get("BatchId")
        self.RetryCount = params.get("RetryCount")
        self.ScheduleBizTime = params.get("ScheduleBizTime")
        self.ComputeUseTime = params.get("ComputeUseTime")
        self.DataScanVolume = params.get("DataScanVolume")
        self.Log = params.get("Log")
        memeber_set = set(params.keys())
        for name, value in vars(self).items():
            if name in memeber_set:
                memeber_set.remove(name)
        if len(memeber_set) > 0:
            warnings.warn("%s fileds are useless." % ",".join(memeber_set))
        


class ScheduleInstanceRunInfo(AbstractModel):
    """调度任务实例运行信息

    """

    def __init__(self):
        r"""
        :param TaskId: 调度任务ID
        :type TaskId: str
        :param RunDate: 重跑实例日期
        :type RunDate: str
        """
        self.TaskId = None
        self.RunDate = None


    def _deserialize(self, params):
        self.TaskId = params.get("TaskId")
        self.RunDate = params.get("RunDate")
        memeber_set = set(params.keys())
        for name, value in vars(self).items():
            if name in memeber_set:
                memeber_set.remove(name)
        if len(memeber_set) > 0:
            warnings.warn("%s fileds are useless." % ",".join(memeber_set))
        


class ScheduleTaskInfo(AbstractModel):
    """调度任务信息

    """

    def __init__(self):
        r"""
        :param TaskId: 调度任务ID
        :type TaskId: str
        :param TaskName: 调度任务名称
        :type TaskName: str
        :param VirtualFlag: 是否为虚拟任务
        :type VirtualFlag: bool
        :param LeftCoordinate: 调度任务在调度计划画布坐标1
        :type LeftCoordinate: float
        :param TopCoordinate: 调度任务在调度计划画布坐标2
        :type TopCoordinate: float
        :param DataEngineName: 数据引擎名称
        :type DataEngineName: str
        :param DelayTime: 调度任务延迟时间，从调度周期开始时间计算的分钟数
        :type DelayTime: int
        :param StartTime: 调度任务开始时间
        :type StartTime: str
        :param EndTime: 调度任务结束时间
        :type EndTime: str
        :param SelfDepend: 任务依赖属性,PARALLEL:并行;SERIAL:无序串行;ORDERLY:有序串行
        :type SelfDepend: str
        :param TryLimit: 重试次数
        :type TryLimit: int
        :param VirtualWorkflowId: 虚拟工作流id
        :type VirtualWorkflowId: str
        :param VirtualWorkflowName: 虚拟工作流名称
        :type VirtualWorkflowName: str
        :param ScriptId: 脚本ID
        :type ScriptId: str
        :param Status: N：新建
NS：草稿
P：审批
A：审批通过
Y：运行
F：停止
O：冻结
R:驳回
D：删除
        :type Status: str
        :param ScriptName: 调度任务对应脚本名称
        :type ScriptName: str
        :param VirtualTaskId: 虚拟任务ID
        :type VirtualTaskId: str
        :param WorkflowId: 调度任务所属调度计划Id
        :type WorkflowId: str
        :param WorkflowName: 调度任务所属调度计划名称
        :type WorkflowName: str
        :param OwnerSubUin: 责任人的subuin
        :type OwnerSubUin: str
        :param OwnerName: 责任人名称
        :type OwnerName: str
        :param OwnerGroup: 责任人所属组
        :type OwnerGroup: str
        :param Desc: 调度任务描述
        :type Desc: str
        :param Params: 调度任务自定义参数，[{"Key":"abc","Value":"edf"}]
        :type Params: str
        :param DataEngineId: 数据引擎ID
        :type DataEngineId: str
        :param DatasourceConnectionName: 数据源名称，默认为DataLakeCatalog
        :type DatasourceConnectionName: str
        :param CycleType: 调度周期类型，分钟(MINUTE_CYCLE)，小时(HOUR_CYCLE)，天(DAY_CYCLE)，周(WEEK_CYCLE),月(MONTH_CYCLE)，一次性(ONEOFF_CYCLE)
不支持修改
        :type CycleType: str
        :param CycleStep: 任务调度周期间隔
        :type CycleStep: int
        :param TaskAction: 在指定周期的第n个单位时间运行（周和月任务使用），比如周任务周日运行：TaskAction=1；周一运行：TaskAction=2，月任务当月第1天运行：TaskAction=1，等
        :type TaskAction: str
        :param Timeout: 超时时间，分钟
        :type Timeout: int
        :param ProductName: 产品名称
        :type ProductName: str
        :param ProjectId: 项目id
        :type ProjectId: int
        :param TaskTypeId: 任务类型id
        :type TaskTypeId: int
        :param UserAppId: appid
        :type UserAppId: str
        :param UserUin: uin
        :type UserUin: str
        :param TaskType: 任务类型，SQL,SparkJar等
        :type TaskType: str
        :param CreateUserUin: 创建人subuin
        :type CreateUserUin: str
        :param CreateUserName: 创建人名称
        :type CreateUserName: str
        :param ExecuteInfo: 执行信息，SQL任务为SQL脚本；Spark任务为命令行信息
        :type ExecuteInfo: str
        :param KVPairs: 调度任务自定义参数，[{"Key":"abc","Value":"edf"}]
注意：此字段可能返回 null，表示取不到有效值。
        :type KVPairs: list of KVPair
        :param WaitingTimeout: 任务等待调度超时时间
注意：此字段可能返回 null，表示取不到有效值。
        :type WaitingTimeout: int
        :param RetryWait: 重试等待
注意：此字段可能返回 null，表示取不到有效值。
        :type RetryWait: int
        :param IsDelete: 是否被删除
注意：此字段可能返回 null，表示取不到有效值。
        :type IsDelete: int
        :param CreateTime: 创建时间
注意：此字段可能返回 null，表示取不到有效值。
        :type CreateTime: str
        :param UpdateTime: 更新时间
注意：此字段可能返回 null，表示取不到有效值。
        :type UpdateTime: str
        :param NonFinishedInstancesCount: 无
注意：此字段可能返回 null，表示取不到有效值。
        :type NonFinishedInstancesCount: int
        """
        self.TaskId = None
        self.TaskName = None
        self.VirtualFlag = None
        self.LeftCoordinate = None
        self.TopCoordinate = None
        self.DataEngineName = None
        self.DelayTime = None
        self.StartTime = None
        self.EndTime = None
        self.SelfDepend = None
        self.TryLimit = None
        self.VirtualWorkflowId = None
        self.VirtualWorkflowName = None
        self.ScriptId = None
        self.Status = None
        self.ScriptName = None
        self.VirtualTaskId = None
        self.WorkflowId = None
        self.WorkflowName = None
        self.OwnerSubUin = None
        self.OwnerName = None
        self.OwnerGroup = None
        self.Desc = None
        self.Params = None
        self.DataEngineId = None
        self.DatasourceConnectionName = None
        self.CycleType = None
        self.CycleStep = None
        self.TaskAction = None
        self.Timeout = None
        self.ProductName = None
        self.ProjectId = None
        self.TaskTypeId = None
        self.UserAppId = None
        self.UserUin = None
        self.TaskType = None
        self.CreateUserUin = None
        self.CreateUserName = None
        self.ExecuteInfo = None
        self.KVPairs = None
        self.WaitingTimeout = None
        self.RetryWait = None
        self.IsDelete = None
        self.CreateTime = None
        self.UpdateTime = None
        self.NonFinishedInstancesCount = None


    def _deserialize(self, params):
        self.TaskId = params.get("TaskId")
        self.TaskName = params.get("TaskName")
        self.VirtualFlag = params.get("VirtualFlag")
        self.LeftCoordinate = params.get("LeftCoordinate")
        self.TopCoordinate = params.get("TopCoordinate")
        self.DataEngineName = params.get("DataEngineName")
        self.DelayTime = params.get("DelayTime")
        self.StartTime = params.get("StartTime")
        self.EndTime = params.get("EndTime")
        self.SelfDepend = params.get("SelfDepend")
        self.TryLimit = params.get("TryLimit")
        self.VirtualWorkflowId = params.get("VirtualWorkflowId")
        self.VirtualWorkflowName = params.get("VirtualWorkflowName")
        self.ScriptId = params.get("ScriptId")
        self.Status = params.get("Status")
        self.ScriptName = params.get("ScriptName")
        self.VirtualTaskId = params.get("VirtualTaskId")
        self.WorkflowId = params.get("WorkflowId")
        self.WorkflowName = params.get("WorkflowName")
        self.OwnerSubUin = params.get("OwnerSubUin")
        self.OwnerName = params.get("OwnerName")
        self.OwnerGroup = params.get("OwnerGroup")
        self.Desc = params.get("Desc")
        self.Params = params.get("Params")
        self.DataEngineId = params.get("DataEngineId")
        self.DatasourceConnectionName = params.get("DatasourceConnectionName")
        self.CycleType = params.get("CycleType")
        self.CycleStep = params.get("CycleStep")
        self.TaskAction = params.get("TaskAction")
        self.Timeout = params.get("Timeout")
        self.ProductName = params.get("ProductName")
        self.ProjectId = params.get("ProjectId")
        self.TaskTypeId = params.get("TaskTypeId")
        self.UserAppId = params.get("UserAppId")
        self.UserUin = params.get("UserUin")
        self.TaskType = params.get("TaskType")
        self.CreateUserUin = params.get("CreateUserUin")
        self.CreateUserName = params.get("CreateUserName")
        self.ExecuteInfo = params.get("ExecuteInfo")
        if params.get("KVPairs") is not None:
            self.KVPairs = []
            for item in params.get("KVPairs"):
                obj = KVPair()
                obj._deserialize(item)
                self.KVPairs.append(obj)
        self.WaitingTimeout = params.get("WaitingTimeout")
        self.RetryWait = params.get("RetryWait")
        self.IsDelete = params.get("IsDelete")
        self.CreateTime = params.get("CreateTime")
        self.UpdateTime = params.get("UpdateTime")
        self.NonFinishedInstancesCount = params.get("NonFinishedInstancesCount")
        memeber_set = set(params.keys())
        for name, value in vars(self).items():
            if name in memeber_set:
                memeber_set.remove(name)
        if len(memeber_set) > 0:
            warnings.warn("%s fileds are useless." % ",".join(memeber_set))
        


class Script(AbstractModel):
    """script实例。

    """

    def __init__(self):
        r"""
        :param ScriptId: 脚本Id，长度36字节。
注意：此字段可能返回 null，表示取不到有效值。
        :type ScriptId: str
        :param ScriptName: 脚本名称，长度0-25。
注意：此字段可能返回 null，表示取不到有效值。
        :type ScriptName: str
        :param ScriptDesc: 脚本描述，长度0-50。
注意：此字段可能返回 null，表示取不到有效值。
        :type ScriptDesc: str
        :param DatabaseName: 默认关联数据库。
注意：此字段可能返回 null，表示取不到有效值。
        :type DatabaseName: str
        :param SQLStatement: SQL描述，长度0-10000。
注意：此字段可能返回 null，表示取不到有效值。
        :type SQLStatement: str
        :param UpdateTime: 更新时间戳， 单位：ms。
注意：此字段可能返回 null，表示取不到有效值。
        :type UpdateTime: int
        """
        self.ScriptId = None
        self.ScriptName = None
        self.ScriptDesc = None
        self.DatabaseName = None
        self.SQLStatement = None
        self.UpdateTime = None


    def _deserialize(self, params):
        self.ScriptId = params.get("ScriptId")
        self.ScriptName = params.get("ScriptName")
        self.ScriptDesc = params.get("ScriptDesc")
        self.DatabaseName = params.get("DatabaseName")
        self.SQLStatement = params.get("SQLStatement")
        self.UpdateTime = params.get("UpdateTime")
        memeber_set = set(params.keys())
        for name, value in vars(self).items():
            if name in memeber_set:
                memeber_set.remove(name)
        if len(memeber_set) > 0:
            warnings.warn("%s fileds are useless." % ",".join(memeber_set))
        


class SessionResourceConfig(AbstractModel):
    """会话资源配置。

    """

    def __init__(self):
        r"""
        :param Datasource: 数据源Catalog
        :type Datasource: str
        :param DefaultDatabase: 默认数据库配置
        :type DefaultDatabase: str
        :param ComputerResource: 计算资源配置
        :type ComputerResource: :class:`tencentcloud.dlc.v20210125.models.ComputerResource`
        :param AdvanceSetting: 高级配置
注意：此字段可能返回 null，表示取不到有效值。
        :type AdvanceSetting: :class:`tencentcloud.dlc.v20210125.models.AdvanceSetting`
        """
        self.Datasource = None
        self.DefaultDatabase = None
        self.ComputerResource = None
        self.AdvanceSetting = None


    def _deserialize(self, params):
        self.Datasource = params.get("Datasource")
        self.DefaultDatabase = params.get("DefaultDatabase")
        if params.get("ComputerResource") is not None:
            self.ComputerResource = ComputerResource()
            self.ComputerResource._deserialize(params.get("ComputerResource"))
        if params.get("AdvanceSetting") is not None:
            self.AdvanceSetting = AdvanceSetting()
            self.AdvanceSetting._deserialize(params.get("AdvanceSetting"))
        memeber_set = set(params.keys())
        for name, value in vars(self).items():
            if name in memeber_set:
                memeber_set.remove(name)
        if len(memeber_set) > 0:
            warnings.warn("%s fileds are useless." % ",".join(memeber_set))
        


class SessionResourceTemplate(AbstractModel):
    """Spark批作业集群Session资源配置模板；

    """

    def __init__(self):
        r"""
        :param DriverSize: driver规格：small,medium,large,xlarge；内存型(引擎类型)：m.small,m.medium,m.large,m.xlarge
注意：此字段可能返回 null，表示取不到有效值。
        :type DriverSize: str
        :param ExecutorSize: executor规格：small,medium,large,xlarge；内存型(引擎类型)：m.small,m.medium,m.large,m.xlarge
注意：此字段可能返回 null，表示取不到有效值。
        :type ExecutorSize: str
        :param ExecutorNums: 指定executor数量，最小值为1，最大值小于集群规格
注意：此字段可能返回 null，表示取不到有效值。
        :type ExecutorNums: int
        :param ExecutorMaxNumbers: 指定executor max数量（动态配置场景下），最小值为1，最大值小于集群规格（当ExecutorMaxNumbers小于ExecutorNums时，改值设定为ExecutorNums）
注意：此字段可能返回 null，表示取不到有效值。
        :type ExecutorMaxNumbers: int
        """
        self.DriverSize = None
        self.ExecutorSize = None
        self.ExecutorNums = None
        self.ExecutorMaxNumbers = None


    def _deserialize(self, params):
        self.DriverSize = params.get("DriverSize")
        self.ExecutorSize = params.get("ExecutorSize")
        self.ExecutorNums = params.get("ExecutorNums")
        self.ExecutorMaxNumbers = params.get("ExecutorMaxNumbers")
        memeber_set = set(params.keys())
        for name, value in vars(self).items():
            if name in memeber_set:
                memeber_set.remove(name)
        if len(memeber_set) > 0:
            warnings.warn("%s fileds are useless." % ",".join(memeber_set))
        


class SetTablePropertiesRequest(AbstractModel):
    """SetTableProperties请求参数结构体

    """

    def __init__(self):
        r"""
        :param DatasourceConnectionName: Catalog名称
        :type DatasourceConnectionName: str
        :param DatabaseName: 库名
        :type DatabaseName: str
        :param TableName: 表名
        :type TableName: str
        :param Properties: 属性列表
        :type Properties: list of Property
        """
        self.DatasourceConnectionName = None
        self.DatabaseName = None
        self.TableName = None
        self.Properties = None


    def _deserialize(self, params):
        self.DatasourceConnectionName = params.get("DatasourceConnectionName")
        self.DatabaseName = params.get("DatabaseName")
        self.TableName = params.get("TableName")
        if params.get("Properties") is not None:
            self.Properties = []
            for item in params.get("Properties"):
                obj = Property()
                obj._deserialize(item)
                self.Properties.append(obj)
        memeber_set = set(params.keys())
        for name, value in vars(self).items():
            if name in memeber_set:
                memeber_set.remove(name)
        if len(memeber_set) > 0:
            warnings.warn("%s fileds are useless." % ",".join(memeber_set))
        


class SetTablePropertiesResponse(AbstractModel):
    """SetTableProperties返回参数结构体

    """

    def __init__(self):
        r"""
        :param BatchId: 批任务Id
        :type BatchId: str
        :param TaskIdSet: TaskId列表
        :type TaskIdSet: list of str
        :param RequestId: 唯一请求 ID，每次请求都会返回。定位问题时需要提供该次请求的 RequestId。
        :type RequestId: str
        """
        self.BatchId = None
        self.TaskIdSet = None
        self.RequestId = None


    def _deserialize(self, params):
        self.BatchId = params.get("BatchId")
        self.TaskIdSet = params.get("TaskIdSet")
        self.RequestId = params.get("RequestId")


class SparkAppJobImage(AbstractModel):
    """Spark镜像返回值信息。

    """

    def __init__(self):
        r"""
        :param Version: 镜像版本
        :type Version: str
        :param Description: 镜像描述
注意：此字段可能返回 null，表示取不到有效值。
        :type Description: str
        """
        self.Version = None
        self.Description = None


    def _deserialize(self, params):
        self.Version = params.get("Version")
        self.Description = params.get("Description")
        memeber_set = set(params.keys())
        for name, value in vars(self).items():
            if name in memeber_set:
                memeber_set.remove(name)
        if len(memeber_set) > 0:
            warnings.warn("%s fileds are useless." % ",".join(memeber_set))
        


class SparkImage(AbstractModel):
    """Spark镜像信息

    """

    def __init__(self):
        r"""
        :param Id: 镜像编号
        :type Id: str
        :param Version: 镜像版本
        :type Version: str
        :param Tag: 镜像tag
        :type Tag: str
        :param Description: 镜像描述
注意：此字段可能返回 null，表示取不到有效值。
        :type Description: str
        :param IsPublic: 是否为公共镜像：0：非公共；1：公共
        :type IsPublic: int
        :param CreateTime: 镜像创建时间
        :type CreateTime: str
        :param UpdateTime: 镜像更新时间
        :type UpdateTime: str
        """
        self.Id = None
        self.Version = None
        self.Tag = None
        self.Description = None
        self.IsPublic = None
        self.CreateTime = None
        self.UpdateTime = None


    def _deserialize(self, params):
        self.Id = params.get("Id")
        self.Version = params.get("Version")
        self.Tag = params.get("Tag")
        self.Description = params.get("Description")
        self.IsPublic = params.get("IsPublic")
        self.CreateTime = params.get("CreateTime")
        self.UpdateTime = params.get("UpdateTime")
        memeber_set = set(params.keys())
        for name, value in vars(self).items():
            if name in memeber_set:
                memeber_set.remove(name)
        if len(memeber_set) > 0:
            warnings.warn("%s fileds are useless." % ",".join(memeber_set))
        


class SparkImagesUserRecord(AbstractModel):
    """用户私有镜像信息。

    """

    def __init__(self):
        r"""
        :param ImageId: 镜像编码
        :type ImageId: str
        :param UserAppid: 用户APPID
        :type UserAppid: int
        :param UserUin: 用户UIN
        :type UserUin: str
        :param UserAlias: 用户昵称
注意：此字段可能返回 null，表示取不到有效值。
        :type UserAlias: str
        :param CreateTime: 创建时间
        :type CreateTime: str
        """
        self.ImageId = None
        self.UserAppid = None
        self.UserUin = None
        self.UserAlias = None
        self.CreateTime = None


    def _deserialize(self, params):
        self.ImageId = params.get("ImageId")
        self.UserAppid = params.get("UserAppid")
        self.UserUin = params.get("UserUin")
        self.UserAlias = params.get("UserAlias")
        self.CreateTime = params.get("CreateTime")
        memeber_set = set(params.keys())
        for name, value in vars(self).items():
            if name in memeber_set:
                memeber_set.remove(name)
        if len(memeber_set) > 0:
            warnings.warn("%s fileds are useless." % ",".join(memeber_set))
        


class SparkJobInfo(AbstractModel):
    """spark作业详情。

    """

    def __init__(self):
        r"""
        :param JobId: spark作业ID
        :type JobId: str
        :param JobName: spark作业名
        :type JobName: str
        :param JobType: spark作业类型，可去1或者2，1表示batch作业， 2表示streaming作业
        :type JobType: int
        :param DataEngine: 引擎名
        :type DataEngine: str
        :param Eni: 该字段已下线，请使用字段Datasource
        :type Eni: str
        :param IsLocal: 程序包是否本地上传，cos或者lakefs
        :type IsLocal: str
        :param JobFile: 程序包路径
        :type JobFile: str
        :param RoleArn: 角色ID
        :type RoleArn: int
        :param MainClass: spark作业运行主类
        :type MainClass: str
        :param CmdArgs: 命令行参数，spark作业命令行参数，空格分隔
        :type CmdArgs: str
        :param JobConf: spark原生配置，换行符分隔
        :type JobConf: str
        :param IsLocalJars: 依赖jars是否本地上传，cos或者lakefs
        :type IsLocalJars: str
        :param JobJars: spark作业依赖jars，逗号分隔
        :type JobJars: str
        :param IsLocalFiles: 依赖文件是否本地上传，cos或者lakefs
        :type IsLocalFiles: str
        :param JobFiles: spark作业依赖文件，逗号分隔
        :type JobFiles: str
        :param JobDriverSize: spark作业driver资源大小
        :type JobDriverSize: str
        :param JobExecutorSize: spark作业executor资源大小
        :type JobExecutorSize: str
        :param JobExecutorNums: spark作业executor个数
        :type JobExecutorNums: int
        :param JobMaxAttempts: spark流任务最大重试次数
        :type JobMaxAttempts: int
        :param JobCreator: spark作业创建者
        :type JobCreator: str
        :param JobCreateTime: spark作业创建时间
        :type JobCreateTime: int
        :param JobUpdateTime: spark作业更新时间
        :type JobUpdateTime: int
        :param CurrentTaskId: spark作业最近任务ID
        :type CurrentTaskId: str
        :param JobStatus: spark作业最近运行状态
        :type JobStatus: int
        :param StreamingStat: spark流作业统计
注意：此字段可能返回 null，表示取不到有效值。
        :type StreamingStat: :class:`tencentcloud.dlc.v20210125.models.StreamingStatistics`
        :param DataSource: 数据源名
注意：此字段可能返回 null，表示取不到有效值。
        :type DataSource: str
        :param IsLocalPythonFiles: pyspark：依赖上传方式，1、cos；2、lakefs（控制台使用，该方式不支持直接接口调用）
注意：此字段可能返回 null，表示取不到有效值。
        :type IsLocalPythonFiles: str
        :param AppPythonFiles: 注：该返回值已废弃
注意：此字段可能返回 null，表示取不到有效值。
        :type AppPythonFiles: str
        :param IsLocalArchives: archives：依赖上传方式，1、cos；2、lakefs（控制台使用，该方式不支持直接接口调用）
注意：此字段可能返回 null，表示取不到有效值。
        :type IsLocalArchives: str
        :param JobArchives: archives：依赖资源
注意：此字段可能返回 null，表示取不到有效值。
        :type JobArchives: str
        :param SparkImage: Spark Image 版本
注意：此字段可能返回 null，表示取不到有效值。
        :type SparkImage: str
        :param JobPythonFiles: pyspark：python依赖, 除py文件外，还支持zip/egg等归档格式，多文件以逗号分隔
注意：此字段可能返回 null，表示取不到有效值。
        :type JobPythonFiles: str
        :param TaskNum: 当前job正在运行或准备运行的任务个数
注意：此字段可能返回 null，表示取不到有效值。
        :type TaskNum: int
        :param DataEngineStatus: 引擎状态：-100（默认：未知状态），-2~11：引擎正常状态；
注意：此字段可能返回 null，表示取不到有效值。
        :type DataEngineStatus: int
        :param JobExecutorMaxNumbers: 指定的Executor数量（最大值），默认为1，当开启动态分配有效，若未开启，则该值等于JobExecutorNums
注意：此字段可能返回 null，表示取不到有效值。
        :type JobExecutorMaxNumbers: int
        :param SparkImageVersion: 镜像版本
注意：此字段可能返回 null，表示取不到有效值。
        :type SparkImageVersion: str
        :param SessionId: 查询脚本关联id
注意：此字段可能返回 null，表示取不到有效值。
        :type SessionId: str
        :param DataEngineClusterType: spark_emr_livy
注意：此字段可能返回 null，表示取不到有效值。
        :type DataEngineClusterType: str
        :param DataEngineImageVersion: Spark 3.2-EMR
注意：此字段可能返回 null，表示取不到有效值。
        :type DataEngineImageVersion: str
        :param IsInherit: 任务资源配置是否继承集群模板，0（默认）不继承，1：继承
注意：此字段可能返回 null，表示取不到有效值。
        :type IsInherit: int
        """
        self.JobId = None
        self.JobName = None
        self.JobType = None
        self.DataEngine = None
        self.Eni = None
        self.IsLocal = None
        self.JobFile = None
        self.RoleArn = None
        self.MainClass = None
        self.CmdArgs = None
        self.JobConf = None
        self.IsLocalJars = None
        self.JobJars = None
        self.IsLocalFiles = None
        self.JobFiles = None
        self.JobDriverSize = None
        self.JobExecutorSize = None
        self.JobExecutorNums = None
        self.JobMaxAttempts = None
        self.JobCreator = None
        self.JobCreateTime = None
        self.JobUpdateTime = None
        self.CurrentTaskId = None
        self.JobStatus = None
        self.StreamingStat = None
        self.DataSource = None
        self.IsLocalPythonFiles = None
        self.AppPythonFiles = None
        self.IsLocalArchives = None
        self.JobArchives = None
        self.SparkImage = None
        self.JobPythonFiles = None
        self.TaskNum = None
        self.DataEngineStatus = None
        self.JobExecutorMaxNumbers = None
        self.SparkImageVersion = None
        self.SessionId = None
        self.DataEngineClusterType = None
        self.DataEngineImageVersion = None
        self.IsInherit = None


    def _deserialize(self, params):
        self.JobId = params.get("JobId")
        self.JobName = params.get("JobName")
        self.JobType = params.get("JobType")
        self.DataEngine = params.get("DataEngine")
        self.Eni = params.get("Eni")
        self.IsLocal = params.get("IsLocal")
        self.JobFile = params.get("JobFile")
        self.RoleArn = params.get("RoleArn")
        self.MainClass = params.get("MainClass")
        self.CmdArgs = params.get("CmdArgs")
        self.JobConf = params.get("JobConf")
        self.IsLocalJars = params.get("IsLocalJars")
        self.JobJars = params.get("JobJars")
        self.IsLocalFiles = params.get("IsLocalFiles")
        self.JobFiles = params.get("JobFiles")
        self.JobDriverSize = params.get("JobDriverSize")
        self.JobExecutorSize = params.get("JobExecutorSize")
        self.JobExecutorNums = params.get("JobExecutorNums")
        self.JobMaxAttempts = params.get("JobMaxAttempts")
        self.JobCreator = params.get("JobCreator")
        self.JobCreateTime = params.get("JobCreateTime")
        self.JobUpdateTime = params.get("JobUpdateTime")
        self.CurrentTaskId = params.get("CurrentTaskId")
        self.JobStatus = params.get("JobStatus")
        if params.get("StreamingStat") is not None:
            self.StreamingStat = StreamingStatistics()
            self.StreamingStat._deserialize(params.get("StreamingStat"))
        self.DataSource = params.get("DataSource")
        self.IsLocalPythonFiles = params.get("IsLocalPythonFiles")
        self.AppPythonFiles = params.get("AppPythonFiles")
        self.IsLocalArchives = params.get("IsLocalArchives")
        self.JobArchives = params.get("JobArchives")
        self.SparkImage = params.get("SparkImage")
        self.JobPythonFiles = params.get("JobPythonFiles")
        self.TaskNum = params.get("TaskNum")
        self.DataEngineStatus = params.get("DataEngineStatus")
        self.JobExecutorMaxNumbers = params.get("JobExecutorMaxNumbers")
        self.SparkImageVersion = params.get("SparkImageVersion")
        self.SessionId = params.get("SessionId")
        self.DataEngineClusterType = params.get("DataEngineClusterType")
        self.DataEngineImageVersion = params.get("DataEngineImageVersion")
        self.IsInherit = params.get("IsInherit")
        memeber_set = set(params.keys())
        for name, value in vars(self).items():
            if name in memeber_set:
                memeber_set.remove(name)
        if len(memeber_set) > 0:
            warnings.warn("%s fileds are useless." % ",".join(memeber_set))
        


class SparkLogDownloadInfo(AbstractModel):
    """Spark日志下载信息

    """

    def __init__(self):
        r"""
        :param SparkJobId: 作业ID
        :type SparkJobId: str
        :param SparkJobName: 作业名称
        :type SparkJobName: str
        :param SparkTaskId: 任务ID
        :type SparkTaskId: str
        :param DownloadId: 下载ID
注意：此字段可能返回 null，表示取不到有效值。
        :type DownloadId: str
        :param Status: 日志下载状态。Processing:导出正在进行中，Completed:导出完成，Failed:导出失败，Expired:日志导出已过期（三天有效期）
注意：此字段可能返回 null，表示取不到有效值。
        :type Status: str
        :param DownloadUrl: 下载链接
注意：此字段可能返回 null，表示取不到有效值。
        :type DownloadUrl: str
        :param SubUin: 操作人ID
        :type SubUin: str
        :param CreateTime: 创建时间，毫秒时间戳
        :type CreateTime: int
        :param LogName: 作业对应的日志名称
        :type LogName: str
        """
        self.SparkJobId = None
        self.SparkJobName = None
        self.SparkTaskId = None
        self.DownloadId = None
        self.Status = None
        self.DownloadUrl = None
        self.SubUin = None
        self.CreateTime = None
        self.LogName = None


    def _deserialize(self, params):
        self.SparkJobId = params.get("SparkJobId")
        self.SparkJobName = params.get("SparkJobName")
        self.SparkTaskId = params.get("SparkTaskId")
        self.DownloadId = params.get("DownloadId")
        self.Status = params.get("Status")
        self.DownloadUrl = params.get("DownloadUrl")
        self.SubUin = params.get("SubUin")
        self.CreateTime = params.get("CreateTime")
        self.LogName = params.get("LogName")
        memeber_set = set(params.keys())
        for name, value in vars(self).items():
            if name in memeber_set:
                memeber_set.remove(name)
        if len(memeber_set) > 0:
            warnings.warn("%s fileds are useless." % ",".join(memeber_set))
        


class SparkMonitorMetrics(AbstractModel):
    """Spark监控数据

    """

    def __init__(self):
        r"""
        :param ShuffleWriteBytesCos: shuffle写溢出到COS数据量，单位：byte
注意：此字段可能返回 null，表示取不到有效值。
        :type ShuffleWriteBytesCos: int
        :param ShuffleWriteBytesTotal: shuffle写数据量，单位：byte
注意：此字段可能返回 null，表示取不到有效值。
        :type ShuffleWriteBytesTotal: int
        """
        self.ShuffleWriteBytesCos = None
        self.ShuffleWriteBytesTotal = None


    def _deserialize(self, params):
        self.ShuffleWriteBytesCos = params.get("ShuffleWriteBytesCos")
        self.ShuffleWriteBytesTotal = params.get("ShuffleWriteBytesTotal")
        memeber_set = set(params.keys())
        for name, value in vars(self).items():
            if name in memeber_set:
                memeber_set.remove(name)
        if len(memeber_set) > 0:
            warnings.warn("%s fileds are useless." % ",".join(memeber_set))
        


class SparkSessionBatchLog(AbstractModel):
    """SparkSQL批任务运行日志

    """

    def __init__(self):
        r"""
        :param Step: 日志步骤：BEG/CS/DS/DSS/DSF/FINF/RTO/CANCEL/CT/DT/DTS/DTF/FINT/EXCE
注意：此字段可能返回 null，表示取不到有效值。
        :type Step: str
        :param Time: 时间
注意：此字段可能返回 null，表示取不到有效值。
        :type Time: str
        :param Message: 日志提示
注意：此字段可能返回 null，表示取不到有效值。
        :type Message: str
        :param Operate: 日志操作
注意：此字段可能返回 null，表示取不到有效值。
        :type Operate: list of SparkSessionBatchLogOperate
        """
        self.Step = None
        self.Time = None
        self.Message = None
        self.Operate = None


    def _deserialize(self, params):
        self.Step = params.get("Step")
        self.Time = params.get("Time")
        self.Message = params.get("Message")
        if params.get("Operate") is not None:
            self.Operate = []
            for item in params.get("Operate"):
                obj = SparkSessionBatchLogOperate()
                obj._deserialize(item)
                self.Operate.append(obj)
        memeber_set = set(params.keys())
        for name, value in vars(self).items():
            if name in memeber_set:
                memeber_set.remove(name)
        if len(memeber_set) > 0:
            warnings.warn("%s fileds are useless." % ",".join(memeber_set))
        


class SparkSessionBatchLogOperate(AbstractModel):
    """SparkSQL批任务日志操作信息。

    """

    def __init__(self):
        r"""
        :param Text: 操作提示
注意：此字段可能返回 null，表示取不到有效值。
        :type Text: str
        :param Operate: 操作类型：COPY、LOG、UI、RESULT、List、TAB
注意：此字段可能返回 null，表示取不到有效值。
        :type Operate: str
        :param Supplement: 补充信息：如：taskid、sessionid、sparkui等
注意：此字段可能返回 null，表示取不到有效值。
        :type Supplement: list of KVPair
        """
        self.Text = None
        self.Operate = None
        self.Supplement = None


    def _deserialize(self, params):
        self.Text = params.get("Text")
        self.Operate = params.get("Operate")
        if params.get("Supplement") is not None:
            self.Supplement = []
            for item in params.get("Supplement"):
                obj = KVPair()
                obj._deserialize(item)
                self.Supplement.append(obj)
        memeber_set = set(params.keys())
        for name, value in vars(self).items():
            if name in memeber_set:
                memeber_set.remove(name)
        if len(memeber_set) > 0:
            warnings.warn("%s fileds are useless." % ",".join(memeber_set))
        


class SparkSessionBatchSQL(AbstractModel):
    """SparkSQL批任务详情。

    """

    def __init__(self):
        r"""
        :param BatchId: 批任务唯一标识
        :type BatchId: str
        :param SessionId: session唯一标识
注意：此字段可能返回 null，表示取不到有效值。
        :type SessionId: str
        :param Type: 任务类型：默认：SparkBatchSQL
注意：此字段可能返回 null，表示取不到有效值。
        :type Type: str
        :param ExecuteSQL: 运行sql
注意：此字段可能返回 null，表示取不到有效值。
        :type ExecuteSQL: str
        :param State: 任务运行状态：1：初始化、5：运行中、0：成功、-1：失败、-3：取消；-4：过期；
注意：此字段可能返回 null，表示取不到有效值。
        :type State: int
        :param Creator: 创建人
注意：此字段可能返回 null，表示取不到有效值。
        :type Creator: str
        :param CreateTime: 创建时间
注意：此字段可能返回 null，表示取不到有效值。
        :type CreateTime: str
        :param UpdateTime: 更新时间
注意：此字段可能返回 null，表示取不到有效值。
        :type UpdateTime: str
        :param UseTime: 任务运行时间：ms
注意：此字段可能返回 null，表示取不到有效值。
        :type UseTime: int
        :param DataEngineId: 引擎ID
注意：此字段可能返回 null，表示取不到有效值。
        :type DataEngineId: str
        :param DataEngineName: 引擎名称
注意：此字段可能返回 null，表示取不到有效值。
        :type DataEngineName: str
        :param SparkUI: spark ui地址
注意：此字段可能返回 null，表示取不到有效值。
        :type SparkUI: str
        :param BatchLog: 任务日志列表
注意：此字段可能返回 null，表示取不到有效值。
        :type BatchLog: list of SparkSessionBatchLog
        :param ResourceUsage: 任务使用资源：如：10CU
注意：此字段可能返回 null，表示取不到有效值。
        :type ResourceUsage: int
        :param ImageVersionName: 镜像版本
注意：此字段可能返回 null，表示取不到有效值。
        :type ImageVersionName: str
        """
        self.BatchId = None
        self.SessionId = None
        self.Type = None
        self.ExecuteSQL = None
        self.State = None
        self.Creator = None
        self.CreateTime = None
        self.UpdateTime = None
        self.UseTime = None
        self.DataEngineId = None
        self.DataEngineName = None
        self.SparkUI = None
        self.BatchLog = None
        self.ResourceUsage = None
        self.ImageVersionName = None


    def _deserialize(self, params):
        self.BatchId = params.get("BatchId")
        self.SessionId = params.get("SessionId")
        self.Type = params.get("Type")
        self.ExecuteSQL = params.get("ExecuteSQL")
        self.State = params.get("State")
        self.Creator = params.get("Creator")
        self.CreateTime = params.get("CreateTime")
        self.UpdateTime = params.get("UpdateTime")
        self.UseTime = params.get("UseTime")
        self.DataEngineId = params.get("DataEngineId")
        self.DataEngineName = params.get("DataEngineName")
        self.SparkUI = params.get("SparkUI")
        if params.get("BatchLog") is not None:
            self.BatchLog = []
            for item in params.get("BatchLog"):
                obj = SparkSessionBatchLog()
                obj._deserialize(item)
                self.BatchLog.append(obj)
        self.ResourceUsage = params.get("ResourceUsage")
        self.ImageVersionName = params.get("ImageVersionName")
        memeber_set = set(params.keys())
        for name, value in vars(self).items():
            if name in memeber_set:
                memeber_set.remove(name)
        if len(memeber_set) > 0:
            warnings.warn("%s fileds are useless." % ",".join(memeber_set))
        


class StatementOutput(AbstractModel):
    """notebook session statement输出信息。

    """

    def __init__(self):
        r"""
        :param ExecutionCount: 执行总数
注意：此字段可能返回 null，表示取不到有效值。
        :type ExecutionCount: int
        :param Data: Statement数据
注意：此字段可能返回 null，表示取不到有效值。
        :type Data: list of KVPair
        :param Status: Statement状态:ok,error
注意：此字段可能返回 null，表示取不到有效值。
        :type Status: str
        :param ErrorName: 错误名称
注意：此字段可能返回 null，表示取不到有效值。
        :type ErrorName: str
        :param ErrorValue: 错误类型
注意：此字段可能返回 null，表示取不到有效值。
        :type ErrorValue: str
        :param ErrorMessage: 错误堆栈信息
注意：此字段可能返回 null，表示取不到有效值。
        :type ErrorMessage: list of str
        :param SQLResult: SQL类型任务结果返回
注意：此字段可能返回 null，表示取不到有效值。
        :type SQLResult: str
        """
        self.ExecutionCount = None
        self.Data = None
        self.Status = None
        self.ErrorName = None
        self.ErrorValue = None
        self.ErrorMessage = None
        self.SQLResult = None


    def _deserialize(self, params):
        self.ExecutionCount = params.get("ExecutionCount")
        if params.get("Data") is not None:
            self.Data = []
            for item in params.get("Data"):
                obj = KVPair()
                obj._deserialize(item)
                self.Data.append(obj)
        self.Status = params.get("Status")
        self.ErrorName = params.get("ErrorName")
        self.ErrorValue = params.get("ErrorValue")
        self.ErrorMessage = params.get("ErrorMessage")
        self.SQLResult = params.get("SQLResult")
        memeber_set = set(params.keys())
        for name, value in vars(self).items():
            if name in memeber_set:
                memeber_set.remove(name)
        if len(memeber_set) > 0:
            warnings.warn("%s fileds are useless." % ",".join(memeber_set))
        


class StopScheduleTasksRequest(AbstractModel):
    """StopScheduleTasks请求参数结构体

    """

    def __init__(self):
        r"""
        :param TaskIdList: 暂停调度任务id列表
        :type TaskIdList: list of str
        :param IsSingleTask: 是否单个任务暂停
        :type IsSingleTask: bool
        """
        self.TaskIdList = None
        self.IsSingleTask = None


    def _deserialize(self, params):
        self.TaskIdList = params.get("TaskIdList")
        self.IsSingleTask = params.get("IsSingleTask")
        memeber_set = set(params.keys())
        for name, value in vars(self).items():
            if name in memeber_set:
                memeber_set.remove(name)
        if len(memeber_set) > 0:
            warnings.warn("%s fileds are useless." % ",".join(memeber_set))
        


class StopScheduleTasksResponse(AbstractModel):
    """StopScheduleTasks返回参数结构体

    """

    def __init__(self):
        r"""
        :param Msg: 暂停调度任务提示信息
        :type Msg: str
        :param Failed: 暂停失败的任务数
        :type Failed: int
        :param RequestId: 唯一请求 ID，每次请求都会返回。定位问题时需要提供该次请求的 RequestId。
        :type RequestId: str
        """
        self.Msg = None
        self.Failed = None
        self.RequestId = None


    def _deserialize(self, params):
        self.Msg = params.get("Msg")
        self.Failed = params.get("Failed")
        self.RequestId = params.get("RequestId")


class StreamingStatistics(AbstractModel):
    """spark流任务统计信息

    """

    def __init__(self):
        r"""
        :param StartTime: 任务开始时间
        :type StartTime: str
        :param Receivers: 数据接收器数
        :type Receivers: int
        :param NumActiveReceivers: 运行中的接收器数
        :type NumActiveReceivers: int
        :param NumInactiveReceivers: 不活跃的接收器数
        :type NumInactiveReceivers: int
        :param NumActiveBatches: 运行中的批数
        :type NumActiveBatches: int
        :param NumRetainedCompletedBatches: 待处理的批数
        :type NumRetainedCompletedBatches: int
        :param NumTotalCompletedBatches: 已完成的批数
        :type NumTotalCompletedBatches: int
        :param AverageInputRate: 平均输入速率
        :type AverageInputRate: float
        :param AverageSchedulingDelay: 平均等待时长
        :type AverageSchedulingDelay: float
        :param AverageProcessingTime: 平均处理时长
        :type AverageProcessingTime: float
        :param AverageTotalDelay: 平均延时
        :type AverageTotalDelay: float
        """
        self.StartTime = None
        self.Receivers = None
        self.NumActiveReceivers = None
        self.NumInactiveReceivers = None
        self.NumActiveBatches = None
        self.NumRetainedCompletedBatches = None
        self.NumTotalCompletedBatches = None
        self.AverageInputRate = None
        self.AverageSchedulingDelay = None
        self.AverageProcessingTime = None
        self.AverageTotalDelay = None


    def _deserialize(self, params):
        self.StartTime = params.get("StartTime")
        self.Receivers = params.get("Receivers")
        self.NumActiveReceivers = params.get("NumActiveReceivers")
        self.NumInactiveReceivers = params.get("NumInactiveReceivers")
        self.NumActiveBatches = params.get("NumActiveBatches")
        self.NumRetainedCompletedBatches = params.get("NumRetainedCompletedBatches")
        self.NumTotalCompletedBatches = params.get("NumTotalCompletedBatches")
        self.AverageInputRate = params.get("AverageInputRate")
        self.AverageSchedulingDelay = params.get("AverageSchedulingDelay")
        self.AverageProcessingTime = params.get("AverageProcessingTime")
        self.AverageTotalDelay = params.get("AverageTotalDelay")
        memeber_set = set(params.keys())
        for name, value in vars(self).items():
            if name in memeber_set:
                memeber_set.remove(name)
        if len(memeber_set) > 0:
            warnings.warn("%s fileds are useless." % ",".join(memeber_set))
        


class SupplementDataRequest(AbstractModel):
    """SupplementData请求参数结构体

    """

    def __init__(self):
        r"""
        :param TaskId: 补数据的任务ID
        :type TaskId: str
        :param StartTime: 补录数据开始时间
        :type StartTime: str
        :param EndTime: 补录数据结束时间
        :type EndTime: str
        """
        self.TaskId = None
        self.StartTime = None
        self.EndTime = None


    def _deserialize(self, params):
        self.TaskId = params.get("TaskId")
        self.StartTime = params.get("StartTime")
        self.EndTime = params.get("EndTime")
        memeber_set = set(params.keys())
        for name, value in vars(self).items():
            if name in memeber_set:
                memeber_set.remove(name)
        if len(memeber_set) > 0:
            warnings.warn("%s fileds are useless." % ",".join(memeber_set))
        


class SupplementDataResponse(AbstractModel):
    """SupplementData返回参数结构体

    """

    def __init__(self):
        r"""
        :param Result: 补录数据提交结果
        :type Result: bool
        :param RequestId: 唯一请求 ID，每次请求都会返回。定位问题时需要提供该次请求的 RequestId。
        :type RequestId: str
        """
        self.Result = None
        self.RequestId = None


    def _deserialize(self, params):
        self.Result = params.get("Result")
        self.RequestId = params.get("RequestId")


class SuspendResumeDataEngineRequest(AbstractModel):
    """SuspendResumeDataEngine请求参数结构体

    """

    def __init__(self):
        r"""
        :param DataEngineName: 虚拟集群名称
        :type DataEngineName: str
        :param Operate: 操作类型 suspend/resume
        :type Operate: str
        """
        self.DataEngineName = None
        self.Operate = None


    def _deserialize(self, params):
        self.DataEngineName = params.get("DataEngineName")
        self.Operate = params.get("Operate")
        memeber_set = set(params.keys())
        for name, value in vars(self).items():
            if name in memeber_set:
                memeber_set.remove(name)
        if len(memeber_set) > 0:
            warnings.warn("%s fileds are useless." % ",".join(memeber_set))
        


class SuspendResumeDataEngineResponse(AbstractModel):
    """SuspendResumeDataEngine返回参数结构体

    """

    def __init__(self):
        r"""
        :param DataEngineName: 虚拟集群详细信息
        :type DataEngineName: str
        :param RequestId: 唯一请求 ID，每次请求都会返回。定位问题时需要提供该次请求的 RequestId。
        :type RequestId: str
        """
        self.DataEngineName = None
        self.RequestId = None


    def _deserialize(self, params):
        self.DataEngineName = params.get("DataEngineName")
        self.RequestId = params.get("RequestId")


class SuspendResumeHouseRequest(AbstractModel):
    """SuspendResumeHouse请求参数结构体

    """

    def __init__(self):
        r"""
        :param HouseName: House名称
        :type HouseName: str
        :param Operate: 操作类型 suspend/resume
        :type Operate: str
        """
        self.HouseName = None
        self.Operate = None


    def _deserialize(self, params):
        self.HouseName = params.get("HouseName")
        self.Operate = params.get("Operate")
        memeber_set = set(params.keys())
        for name, value in vars(self).items():
            if name in memeber_set:
                memeber_set.remove(name)
        if len(memeber_set) > 0:
            warnings.warn("%s fileds are useless." % ",".join(memeber_set))
        


class SuspendResumeHouseResponse(AbstractModel):
    """SuspendResumeHouse返回参数结构体

    """

    def __init__(self):
        r"""
        :param House: House详细信息
        :type House: :class:`tencentcloud.dlc.v20210125.models.DataEngineInfo`
        :param RequestId: 唯一请求 ID，每次请求都会返回。定位问题时需要提供该次请求的 RequestId。
        :type RequestId: str
        """
        self.House = None
        self.RequestId = None


    def _deserialize(self, params):
        if params.get("House") is not None:
            self.House = DataEngineInfo()
            self.House._deserialize(params.get("House"))
        self.RequestId = params.get("RequestId")


class SwitchDataEngineImageRequest(AbstractModel):
    """SwitchDataEngineImage请求参数结构体

    """

    def __init__(self):
        r"""
        :param DataEngineId: 引擎ID
        :type DataEngineId: str
        :param NewImageVersionId: 新镜像版本ID
        :type NewImageVersionId: str
        """
        self.DataEngineId = None
        self.NewImageVersionId = None


    def _deserialize(self, params):
        self.DataEngineId = params.get("DataEngineId")
        self.NewImageVersionId = params.get("NewImageVersionId")
        memeber_set = set(params.keys())
        for name, value in vars(self).items():
            if name in memeber_set:
                memeber_set.remove(name)
        if len(memeber_set) > 0:
            warnings.warn("%s fileds are useless." % ",".join(memeber_set))
        


class SwitchDataEngineImageResponse(AbstractModel):
    """SwitchDataEngineImage返回参数结构体

    """

    def __init__(self):
        r"""
        :param RequestId: 唯一请求 ID，每次请求都会返回。定位问题时需要提供该次请求的 RequestId。
        :type RequestId: str
        """
        self.RequestId = None


    def _deserialize(self, params):
        self.RequestId = params.get("RequestId")


class SwitchDataEngineRequest(AbstractModel):
    """SwitchDataEngine请求参数结构体

    """

    def __init__(self):
        r"""
        :param DataEngineName: 主集群名称
        :type DataEngineName: str
        :param StartStandbyCluster: 是否开启备集群
        :type StartStandbyCluster: bool
        """
        self.DataEngineName = None
        self.StartStandbyCluster = None


    def _deserialize(self, params):
        self.DataEngineName = params.get("DataEngineName")
        self.StartStandbyCluster = params.get("StartStandbyCluster")
        memeber_set = set(params.keys())
        for name, value in vars(self).items():
            if name in memeber_set:
                memeber_set.remove(name)
        if len(memeber_set) > 0:
            warnings.warn("%s fileds are useless." % ",".join(memeber_set))
        


class SwitchDataEngineResponse(AbstractModel):
    """SwitchDataEngine返回参数结构体

    """

    def __init__(self):
        r"""
        :param RequestId: 唯一请求 ID，每次请求都会返回。定位问题时需要提供该次请求的 RequestId。
        :type RequestId: str
        """
        self.RequestId = None


    def _deserialize(self, params):
        self.RequestId = params.get("RequestId")


class TColumn(AbstractModel):
    """表字段描述信息

    """

    def __init__(self):
        r"""
        :param Name: 字段名称
        :type Name: str
        :param Type: 字段类型
        :type Type: str
        :param Comment: 字段描述
        :type Comment: str
        :param Default: 字段默认值
        :type Default: str
        :param NotNull: 字段是否是非空
        :type NotNull: bool
        :param Precision: 表示整个 numeric 的长度,取值1-38
        :type Precision: int
        :param Scale: 表示小数部分的长度
Scale小于Precision
        :type Scale: int
        """
        self.Name = None
        self.Type = None
        self.Comment = None
        self.Default = None
        self.NotNull = None
        self.Precision = None
        self.Scale = None


    def _deserialize(self, params):
        self.Name = params.get("Name")
        self.Type = params.get("Type")
        self.Comment = params.get("Comment")
        self.Default = params.get("Default")
        self.NotNull = params.get("NotNull")
        self.Precision = params.get("Precision")
        self.Scale = params.get("Scale")
        memeber_set = set(params.keys())
        for name, value in vars(self).items():
            if name in memeber_set:
                memeber_set.remove(name)
        if len(memeber_set) > 0:
            warnings.warn("%s fileds are useless." % ",".join(memeber_set))
        


class TPartition(AbstractModel):
    """表分区字段信息

    """

    def __init__(self):
        r"""
        :param Name: 字段名称
        :type Name: str
        :param Type: 字段类型
        :type Type: str
        :param Comment: 字段描述
        :type Comment: str
        :param PartitionType: 分区类型
        :type PartitionType: str
        :param PartitionFormat: 分区格式
        :type PartitionFormat: str
        :param PartitionDot: 分区分隔数
        :type PartitionDot: int
        :param Transform: 分区转换策略
        :type Transform: str
        :param TransformArgs: 策略参数
        :type TransformArgs: list of str
        """
        self.Name = None
        self.Type = None
        self.Comment = None
        self.PartitionType = None
        self.PartitionFormat = None
        self.PartitionDot = None
        self.Transform = None
        self.TransformArgs = None


    def _deserialize(self, params):
        self.Name = params.get("Name")
        self.Type = params.get("Type")
        self.Comment = params.get("Comment")
        self.PartitionType = params.get("PartitionType")
        self.PartitionFormat = params.get("PartitionFormat")
        self.PartitionDot = params.get("PartitionDot")
        self.Transform = params.get("Transform")
        self.TransformArgs = params.get("TransformArgs")
        memeber_set = set(params.keys())
        for name, value in vars(self).items():
            if name in memeber_set:
                memeber_set.remove(name)
        if len(memeber_set) > 0:
            warnings.warn("%s fileds are useless." % ",".join(memeber_set))
        


class TableBaseInfo(AbstractModel):
    """数据表配置信息

    """

    def __init__(self):
        r"""
        :param DatabaseName: 该数据表所属数据库名字
        :type DatabaseName: str
        :param TableName: 数据表名字
        :type TableName: str
        :param DatasourceConnectionName: 该数据表所属数据源名字
注意：此字段可能返回 null，表示取不到有效值。
        :type DatasourceConnectionName: str
        :param TableComment: 该数据表备注
注意：此字段可能返回 null，表示取不到有效值。
        :type TableComment: str
        :param Type: 具体类型，表or视图
注意：此字段可能返回 null，表示取不到有效值。
        :type Type: str
        :param TableFormat: 数据格式类型，hive，iceberg等
注意：此字段可能返回 null，表示取不到有效值。
        :type TableFormat: str
        :param UserAlias: 建表用户昵称
注意：此字段可能返回 null，表示取不到有效值。
        :type UserAlias: str
        :param UserSubUin: 建表用户ID
注意：此字段可能返回 null，表示取不到有效值。
        :type UserSubUin: str
        :param GovernPolicy: 数据治理配置项
注意：此字段可能返回 null，表示取不到有效值。
        :type GovernPolicy: :class:`tencentcloud.dlc.v20210125.models.DataGovernPolicy`
        :param DbGovernPolicyIsDisable: 库数据治理是否关闭，关闭：true，开启：false
注意：此字段可能返回 null，表示取不到有效值。
        :type DbGovernPolicyIsDisable: str
        """
        self.DatabaseName = None
        self.TableName = None
        self.DatasourceConnectionName = None
        self.TableComment = None
        self.Type = None
        self.TableFormat = None
        self.UserAlias = None
        self.UserSubUin = None
        self.GovernPolicy = None
        self.DbGovernPolicyIsDisable = None


    def _deserialize(self, params):
        self.DatabaseName = params.get("DatabaseName")
        self.TableName = params.get("TableName")
        self.DatasourceConnectionName = params.get("DatasourceConnectionName")
        self.TableComment = params.get("TableComment")
        self.Type = params.get("Type")
        self.TableFormat = params.get("TableFormat")
        self.UserAlias = params.get("UserAlias")
        self.UserSubUin = params.get("UserSubUin")
        if params.get("GovernPolicy") is not None:
            self.GovernPolicy = DataGovernPolicy()
            self.GovernPolicy._deserialize(params.get("GovernPolicy"))
        self.DbGovernPolicyIsDisable = params.get("DbGovernPolicyIsDisable")
        memeber_set = set(params.keys())
        for name, value in vars(self).items():
            if name in memeber_set:
                memeber_set.remove(name)
        if len(memeber_set) > 0:
            warnings.warn("%s fileds are useless." % ",".join(memeber_set))
        


class TableInfo(AbstractModel):
    """返回数据表的相关信息。

    """

    def __init__(self):
        r"""
        :param TableBaseInfo: 数据表配置信息。
        :type TableBaseInfo: :class:`tencentcloud.dlc.v20210125.models.TableBaseInfo`
        :param DataFormat: 数据表格式。每次入参可选如下其一的KV结构，[TextFile，CSV，Json, Parquet, ORC, AVRD]。
        :type DataFormat: :class:`tencentcloud.dlc.v20210125.models.DataFormat`
        :param Columns: 数据表列信息。
        :type Columns: list of Column
        :param Partitions: 数据表分块信息。
        :type Partitions: list of Partition
        :param Location: 数据存储路径。当前仅支持cos路径，格式如下：cosn://bucket-name/filepath。
        :type Location: str
        """
        self.TableBaseInfo = None
        self.DataFormat = None
        self.Columns = None
        self.Partitions = None
        self.Location = None


    def _deserialize(self, params):
        if params.get("TableBaseInfo") is not None:
            self.TableBaseInfo = TableBaseInfo()
            self.TableBaseInfo._deserialize(params.get("TableBaseInfo"))
        if params.get("DataFormat") is not None:
            self.DataFormat = DataFormat()
            self.DataFormat._deserialize(params.get("DataFormat"))
        if params.get("Columns") is not None:
            self.Columns = []
            for item in params.get("Columns"):
                obj = Column()
                obj._deserialize(item)
                self.Columns.append(obj)
        if params.get("Partitions") is not None:
            self.Partitions = []
            for item in params.get("Partitions"):
                obj = Partition()
                obj._deserialize(item)
                self.Partitions.append(obj)
        self.Location = params.get("Location")
        memeber_set = set(params.keys())
        for name, value in vars(self).items():
            if name in memeber_set:
                memeber_set.remove(name)
        if len(memeber_set) > 0:
            warnings.warn("%s fileds are useless." % ",".join(memeber_set))
        


class TableResponseInfo(AbstractModel):
    """查询表信息对象

    """

    def __init__(self):
        r"""
        :param TableBaseInfo: 数据表基本信息。
        :type TableBaseInfo: :class:`tencentcloud.dlc.v20210125.models.TableBaseInfo`
        :param Columns: 数据表列信息。
注意：此字段可能返回 null，表示取不到有效值。
        :type Columns: list of Column
        :param Partitions: 数据表分块信息。
注意：此字段可能返回 null，表示取不到有效值。
        :type Partitions: list of Partition
        :param Location: 数据存储路径。
注意：此字段可能返回 null，表示取不到有效值。
        :type Location: str
        :param Properties: 数据表属性信息。
注意：此字段可能返回 null，表示取不到有效值。
        :type Properties: list of Property
        :param ModifiedTime: 数据表更新时间, 单位: ms。
注意：此字段可能返回 null，表示取不到有效值。
        :type ModifiedTime: str
        :param CreateTime: 数据表创建时间,单位: ms。
注意：此字段可能返回 null，表示取不到有效值。
        :type CreateTime: str
        :param InputFormat: 数据格式。
注意：此字段可能返回 null，表示取不到有效值。
        :type InputFormat: str
        :param StorageSize: 数据表存储大小（单位：Byte）
注意：此字段可能返回 null，表示取不到有效值。
        :type StorageSize: int
        :param RecordCount: 数据表行数
注意：此字段可能返回 null，表示取不到有效值。
        :type RecordCount: int
        :param MapMaterializedViewName: xxxx
注意：此字段可能返回 null，表示取不到有效值。
        :type MapMaterializedViewName: str
        :param Comment: test
注意：此字段可能返回 null，表示取不到有效值。
        :type Comment: str
        :param ViewOriginalText: 创建视图原始文本
注意：此字段可能返回 null，表示取不到有效值。
        :type ViewOriginalText: str
        :param ViewExpandedText: 创建视图展开文本
注意：此字段可能返回 null，表示取不到有效值。
        :type ViewExpandedText: str
        :param Guid: 唯一标识
注意：此字段可能返回 null，表示取不到有效值。
        :type Guid: str
        """
        self.TableBaseInfo = None
        self.Columns = None
        self.Partitions = None
        self.Location = None
        self.Properties = None
        self.ModifiedTime = None
        self.CreateTime = None
        self.InputFormat = None
        self.StorageSize = None
        self.RecordCount = None
        self.MapMaterializedViewName = None
        self.Comment = None
        self.ViewOriginalText = None
        self.ViewExpandedText = None
        self.Guid = None


    def _deserialize(self, params):
        if params.get("TableBaseInfo") is not None:
            self.TableBaseInfo = TableBaseInfo()
            self.TableBaseInfo._deserialize(params.get("TableBaseInfo"))
        if params.get("Columns") is not None:
            self.Columns = []
            for item in params.get("Columns"):
                obj = Column()
                obj._deserialize(item)
                self.Columns.append(obj)
        if params.get("Partitions") is not None:
            self.Partitions = []
            for item in params.get("Partitions"):
                obj = Partition()
                obj._deserialize(item)
                self.Partitions.append(obj)
        self.Location = params.get("Location")
        if params.get("Properties") is not None:
            self.Properties = []
            for item in params.get("Properties"):
                obj = Property()
                obj._deserialize(item)
                self.Properties.append(obj)
        self.ModifiedTime = params.get("ModifiedTime")
        self.CreateTime = params.get("CreateTime")
        self.InputFormat = params.get("InputFormat")
        self.StorageSize = params.get("StorageSize")
        self.RecordCount = params.get("RecordCount")
        self.MapMaterializedViewName = params.get("MapMaterializedViewName")
        self.Comment = params.get("Comment")
        self.ViewOriginalText = params.get("ViewOriginalText")
        self.ViewExpandedText = params.get("ViewExpandedText")
        self.Guid = params.get("Guid")
        memeber_set = set(params.keys())
        for name, value in vars(self).items():
            if name in memeber_set:
                memeber_set.remove(name)
        if len(memeber_set) > 0:
            warnings.warn("%s fileds are useless." % ",".join(memeber_set))
        


class TagInfo(AbstractModel):
    """标签对信息

    """

    def __init__(self):
        r"""
        :param TagKey: 标签键
注意：此字段可能返回 null，表示取不到有效值。
        :type TagKey: str
        :param TagValue: 标签值
注意：此字段可能返回 null，表示取不到有效值。
        :type TagValue: str
        """
        self.TagKey = None
        self.TagValue = None


    def _deserialize(self, params):
        self.TagKey = params.get("TagKey")
        self.TagValue = params.get("TagValue")
        memeber_set = set(params.keys())
        for name, value in vars(self).items():
            if name in memeber_set:
                memeber_set.remove(name)
        if len(memeber_set) > 0:
            warnings.warn("%s fileds are useless." % ",".join(memeber_set))
        


class Task(AbstractModel):
    """任务类型，任务如SQL查询等。

    """

    def __init__(self):
        r"""
        :param SQLTask: SQL查询任务
        :type SQLTask: :class:`tencentcloud.dlc.v20210125.models.SQLTask`
        :param SparkSQLTask: Spark SQL查询任务
        :type SparkSQLTask: :class:`tencentcloud.dlc.v20210125.models.SQLTask`
        """
        self.SQLTask = None
        self.SparkSQLTask = None


    def _deserialize(self, params):
        if params.get("SQLTask") is not None:
            self.SQLTask = SQLTask()
            self.SQLTask._deserialize(params.get("SQLTask"))
        if params.get("SparkSQLTask") is not None:
            self.SparkSQLTask = SQLTask()
            self.SparkSQLTask._deserialize(params.get("SparkSQLTask"))
        memeber_set = set(params.keys())
        for name, value in vars(self).items():
            if name in memeber_set:
                memeber_set.remove(name)
        if len(memeber_set) > 0:
            warnings.warn("%s fileds are useless." % ",".join(memeber_set))
        


class TaskDto(AbstractModel):
    """任务基本信息

    """

    def __init__(self):
        r"""
        :param TaskId: 任务ID
        :type TaskId: str
        :param LeftCoordinate: 任务坐标
        :type LeftCoordinate: float
        :param TopCoordinate: 任务坐标
        :type TopCoordinate: float
        :param VirtualTaskId: 虚拟任务ID
        :type VirtualTaskId: str
        """
        self.TaskId = None
        self.LeftCoordinate = None
        self.TopCoordinate = None
        self.VirtualTaskId = None


    def _deserialize(self, params):
        self.TaskId = params.get("TaskId")
        self.LeftCoordinate = params.get("LeftCoordinate")
        self.TopCoordinate = params.get("TopCoordinate")
        self.VirtualTaskId = params.get("VirtualTaskId")
        memeber_set = set(params.keys())
        for name, value in vars(self).items():
            if name in memeber_set:
                memeber_set.remove(name)
        if len(memeber_set) > 0:
            warnings.warn("%s fileds are useless." % ",".join(memeber_set))
        


class TaskResponseInfo(AbstractModel):
    """任务实例。

    """

    def __init__(self):
        r"""
        :param DatabaseName: 任务所属Database的名称。
        :type DatabaseName: str
        :param DataAmount: 任务数据量。
        :type DataAmount: int
        :param Id: 任务Id。
        :type Id: str
        :param UsedTime: 计算耗时，单位： ms
        :type UsedTime: int
        :param OutputPath: 任务输出路径。
        :type OutputPath: str
        :param CreateTime: 任务创建时间。
        :type CreateTime: str
        :param State: 任务状态：0 初始化， 1 执行中， 2 执行成功，-1 执行失败，-3 已取消。
        :type State: int
        :param SQLType: 任务SQL类型，DDL|DML等
        :type SQLType: str
        :param SQL: 任务SQL语句
        :type SQL: str
        :param ResultExpired: 结果是否过期。
        :type ResultExpired: bool
        :param RowAffectInfo: 数据影响统计信息。
        :type RowAffectInfo: str
        :param DataSet: 任务结果数据表。
注意：此字段可能返回 null，表示取不到有效值。
        :type DataSet: str
        :param Error: 失败信息, 例如：errorMessage。该字段已废弃。
        :type Error: str
        :param Percentage: 任务执行进度num/100(%)
        :type Percentage: int
        :param ResultDataState: 数据写入cos的状态。该字段已废弃。
        :type ResultDataState: int
        :param SchemaAffected: 是否影响库表结构，可用来判断是否刷新等。
        :type SchemaAffected: bool
        :param ResultDataMessage: 数据搬迁任务输出，如异常信息等。该字段已废弃。
        :type ResultDataMessage: str
        :param OutputMessage: 任务执行输出信息。
        :type OutputMessage: str
        :param TaskType: 执行SQL的引擎类型
        :type TaskType: str
        :param ProgressDetail: 任务进度明细
注意：此字段可能返回 null，表示取不到有效值。
        :type ProgressDetail: str
        :param UpdateTime: 任务结束时间
注意：此字段可能返回 null，表示取不到有效值。
        :type UpdateTime: str
        :param DataEngineId: 计算资源id
注意：此字段可能返回 null，表示取不到有效值。
        :type DataEngineId: str
        :param OperateUin: 执行sql的子uin
注意：此字段可能返回 null，表示取不到有效值。
        :type OperateUin: str
        :param DataEngineName: 计算资源名字
注意：此字段可能返回 null，表示取不到有效值。
        :type DataEngineName: str
        :param InputType: 导入类型是本地导入还是cos
注意：此字段可能返回 null，表示取不到有效值。
        :type InputType: str
        :param InputConf: 导入配置
注意：此字段可能返回 null，表示取不到有效值。
        :type InputConf: str
        :param DataNumber: 数据条数
注意：此字段可能返回 null，表示取不到有效值。
        :type DataNumber: int
        :param CanDownload: 查询数据能不能下载
注意：此字段可能返回 null，表示取不到有效值。
        :type CanDownload: bool
        :param UserAlias: 用户别名
注意：此字段可能返回 null，表示取不到有效值。
        :type UserAlias: str
        :param SparkJobName: spark应用作业名
注意：此字段可能返回 null，表示取不到有效值。
        :type SparkJobName: str
        :param SparkJobId: spark应用作业Id
注意：此字段可能返回 null，表示取不到有效值。
        :type SparkJobId: str
        :param SparkJobFile: spark应用入口jar文件
注意：此字段可能返回 null，表示取不到有效值。
        :type SparkJobFile: str
        :param UiUrl: spark ui url
注意：此字段可能返回 null，表示取不到有效值。
        :type UiUrl: str
        :param TotalTime: 任务耗时，单位： ms
注意：此字段可能返回 null，表示取不到有效值。
        :type TotalTime: int
        :param CmdArgs: spark app job执行task的程序入口参数
注意：此字段可能返回 null，表示取不到有效值。
        :type CmdArgs: str
        :param ImageVersion: 集群镜像大版本名称
注意：此字段可能返回 null，表示取不到有效值。
        :type ImageVersion: str
        :param StreamingStat: streaming任务统计信息
注意：此字段可能返回 null，表示取不到有效值。
        :type StreamingStat: :class:`tencentcloud.dlc.v20210125.models.StreamingStatistics`
        :param ResourceUsage: 任务预设资源大小
注意：此字段可能返回 null，表示取不到有效值。
        :type ResourceUsage: int
        :param OutputConf: 输出配置信息
注意：此字段可能返回 null，表示取不到有效值。
        :type OutputConf: str
        :param TaskKind: 任务类别
注意：此字段可能返回 null，表示取不到有效值。
        :type TaskKind: str
        :param DriverSize: driver规格：small,medium,large,xlarge；内存型(引擎类型)：m.small,m.medium,m.large,m.xlarge
注意：此字段可能返回 null，表示取不到有效值。
        :type DriverSize: str
        :param ExecutorSize: executor规格：small,medium,large,xlarge；内存型(引擎类型)：m.small,m.medium,m.large,m.xlarge
注意：此字段可能返回 null，表示取不到有效值。
        :type ExecutorSize: str
        :param ExecutorNums: 指定executor数量，最小值为1，最大值小于集群规格
注意：此字段可能返回 null，表示取不到有效值。
        :type ExecutorNums: int
        :param ExecutorMaxNumbers: 指定executor max数量（动态配置场景下），最小值为1，最大值小于集群规格（当ExecutorMaxNumbers小于ExecutorNums时，改值设定为ExecutorNums）
注意：此字段可能返回 null，表示取不到有效值。
        :type ExecutorMaxNumbers: int
        :param CommonMetrics: 任务公共指标数据
注意：此字段可能返回 null，表示取不到有效值。
        :type CommonMetrics: :class:`tencentcloud.dlc.v20210125.models.CommonMetrics`
        :param SparkMonitorMetrics: spark任务指标数据
注意：此字段可能返回 null，表示取不到有效值。
        :type SparkMonitorMetrics: :class:`tencentcloud.dlc.v20210125.models.SparkMonitorMetrics`
        :param PrestoMonitorMetrics: presto任务指标数据
注意：此字段可能返回 null，表示取不到有效值。
        :type PrestoMonitorMetrics: :class:`tencentcloud.dlc.v20210125.models.PrestoMonitorMetrics`
        """
        self.DatabaseName = None
        self.DataAmount = None
        self.Id = None
        self.UsedTime = None
        self.OutputPath = None
        self.CreateTime = None
        self.State = None
        self.SQLType = None
        self.SQL = None
        self.ResultExpired = None
        self.RowAffectInfo = None
        self.DataSet = None
        self.Error = None
        self.Percentage = None
        self.ResultDataState = None
        self.SchemaAffected = None
        self.ResultDataMessage = None
        self.OutputMessage = None
        self.TaskType = None
        self.ProgressDetail = None
        self.UpdateTime = None
        self.DataEngineId = None
        self.OperateUin = None
        self.DataEngineName = None
        self.InputType = None
        self.InputConf = None
        self.DataNumber = None
        self.CanDownload = None
        self.UserAlias = None
        self.SparkJobName = None
        self.SparkJobId = None
        self.SparkJobFile = None
        self.UiUrl = None
        self.TotalTime = None
        self.CmdArgs = None
        self.ImageVersion = None
        self.StreamingStat = None
        self.ResourceUsage = None
        self.OutputConf = None
        self.TaskKind = None
        self.DriverSize = None
        self.ExecutorSize = None
        self.ExecutorNums = None
        self.ExecutorMaxNumbers = None
        self.CommonMetrics = None
        self.SparkMonitorMetrics = None
        self.PrestoMonitorMetrics = None


    def _deserialize(self, params):
        self.DatabaseName = params.get("DatabaseName")
        self.DataAmount = params.get("DataAmount")
        self.Id = params.get("Id")
        self.UsedTime = params.get("UsedTime")
        self.OutputPath = params.get("OutputPath")
        self.CreateTime = params.get("CreateTime")
        self.State = params.get("State")
        self.SQLType = params.get("SQLType")
        self.SQL = params.get("SQL")
        self.ResultExpired = params.get("ResultExpired")
        self.RowAffectInfo = params.get("RowAffectInfo")
        self.DataSet = params.get("DataSet")
        self.Error = params.get("Error")
        self.Percentage = params.get("Percentage")
        self.ResultDataState = params.get("ResultDataState")
        self.SchemaAffected = params.get("SchemaAffected")
        self.ResultDataMessage = params.get("ResultDataMessage")
        self.OutputMessage = params.get("OutputMessage")
        self.TaskType = params.get("TaskType")
        self.ProgressDetail = params.get("ProgressDetail")
        self.UpdateTime = params.get("UpdateTime")
        self.DataEngineId = params.get("DataEngineId")
        self.OperateUin = params.get("OperateUin")
        self.DataEngineName = params.get("DataEngineName")
        self.InputType = params.get("InputType")
        self.InputConf = params.get("InputConf")
        self.DataNumber = params.get("DataNumber")
        self.CanDownload = params.get("CanDownload")
        self.UserAlias = params.get("UserAlias")
        self.SparkJobName = params.get("SparkJobName")
        self.SparkJobId = params.get("SparkJobId")
        self.SparkJobFile = params.get("SparkJobFile")
        self.UiUrl = params.get("UiUrl")
        self.TotalTime = params.get("TotalTime")
        self.CmdArgs = params.get("CmdArgs")
        self.ImageVersion = params.get("ImageVersion")
        if params.get("StreamingStat") is not None:
            self.StreamingStat = StreamingStatistics()
            self.StreamingStat._deserialize(params.get("StreamingStat"))
        self.ResourceUsage = params.get("ResourceUsage")
        self.OutputConf = params.get("OutputConf")
        self.TaskKind = params.get("TaskKind")
        self.DriverSize = params.get("DriverSize")
        self.ExecutorSize = params.get("ExecutorSize")
        self.ExecutorNums = params.get("ExecutorNums")
        self.ExecutorMaxNumbers = params.get("ExecutorMaxNumbers")
        if params.get("CommonMetrics") is not None:
            self.CommonMetrics = CommonMetrics()
            self.CommonMetrics._deserialize(params.get("CommonMetrics"))
        if params.get("SparkMonitorMetrics") is not None:
            self.SparkMonitorMetrics = SparkMonitorMetrics()
            self.SparkMonitorMetrics._deserialize(params.get("SparkMonitorMetrics"))
        if params.get("PrestoMonitorMetrics") is not None:
            self.PrestoMonitorMetrics = PrestoMonitorMetrics()
            self.PrestoMonitorMetrics._deserialize(params.get("PrestoMonitorMetrics"))
        memeber_set = set(params.keys())
        for name, value in vars(self).items():
            if name in memeber_set:
                memeber_set.remove(name)
        if len(memeber_set) > 0:
            warnings.warn("%s fileds are useless." % ",".join(memeber_set))
        


class TaskResultInfo(AbstractModel):
    """任务结果信息。

    """

    def __init__(self):
        r"""
        :param TaskId: 任务唯一ID
        :type TaskId: str
        :param DatasourceConnectionName: 数据源名称，当前任务执行时候选中的默认数据源
注意：此字段可能返回 null，表示取不到有效值。
        :type DatasourceConnectionName: str
        :param DatabaseName: 数据库名称，当前任务执行时候选中的默认数据库
注意：此字段可能返回 null，表示取不到有效值。
        :type DatabaseName: str
        :param SQL: 当前执行的SQL，一个任务包含一个SQL
        :type SQL: str
        :param SQLType: 执行任务的类型，现在分为DDL、DML、DQL
        :type SQLType: str
        :param State: 任务当前的状态，0：初始化 1：任务运行中 2：任务执行成功  3：数据写入中 4：排队中 -1：任务执行失败 -3：用户手动终止 。只有任务执行成功的情况下，才会返回任务执行的结果
        :type State: int
        :param DataAmount: 扫描的数据量，单位byte
        :type DataAmount: int
        :param UsedTime: 计算耗时，单位： ms
        :type UsedTime: int
        :param OutputPath: 任务结果输出的COS桶地址
        :type OutputPath: str
        :param CreateTime: 任务创建时间，时间戳
        :type CreateTime: str
        :param OutputMessage: 任务执行信息，成功时返回success，失败时返回失败原因
        :type OutputMessage: str
        :param RowAffectInfo: 被影响的行数
        :type RowAffectInfo: str
        :param ResultSchema: 结果的schema信息
注意：此字段可能返回 null，表示取不到有效值。
        :type ResultSchema: list of Column
        :param ResultSet: 结果信息，反转义后，外层数组的每个元素为一行数据
注意：此字段可能返回 null，表示取不到有效值。
        :type ResultSet: str
        :param NextToken: 分页信息，如果没有更多结果数据，nextToken为空
        :type NextToken: str
        :param Percentage: 任务执行进度num/100(%)
        :type Percentage: int
        :param ProgressDetail: 任务进度明细
        :type ProgressDetail: str
        :param DisplayFormat: 控制台展示格式。table：表格展示 text：文本展示
        :type DisplayFormat: str
        :param SchemaAffected: 是否影响库表结构，可用来判断是否刷新等。
        :type SchemaAffected: bool
        :param CanDownload: 是否支持下载标识
        :type CanDownload: bool
        :param TotalTime: 任务耗时，单位： ms
        :type TotalTime: int
        """
        self.TaskId = None
        self.DatasourceConnectionName = None
        self.DatabaseName = None
        self.SQL = None
        self.SQLType = None
        self.State = None
        self.DataAmount = None
        self.UsedTime = None
        self.OutputPath = None
        self.CreateTime = None
        self.OutputMessage = None
        self.RowAffectInfo = None
        self.ResultSchema = None
        self.ResultSet = None
        self.NextToken = None
        self.Percentage = None
        self.ProgressDetail = None
        self.DisplayFormat = None
        self.SchemaAffected = None
        self.CanDownload = None
        self.TotalTime = None


    def _deserialize(self, params):
        self.TaskId = params.get("TaskId")
        self.DatasourceConnectionName = params.get("DatasourceConnectionName")
        self.DatabaseName = params.get("DatabaseName")
        self.SQL = params.get("SQL")
        self.SQLType = params.get("SQLType")
        self.State = params.get("State")
        self.DataAmount = params.get("DataAmount")
        self.UsedTime = params.get("UsedTime")
        self.OutputPath = params.get("OutputPath")
        self.CreateTime = params.get("CreateTime")
        self.OutputMessage = params.get("OutputMessage")
        self.RowAffectInfo = params.get("RowAffectInfo")
        if params.get("ResultSchema") is not None:
            self.ResultSchema = []
            for item in params.get("ResultSchema"):
                obj = Column()
                obj._deserialize(item)
                self.ResultSchema.append(obj)
        self.ResultSet = params.get("ResultSet")
        self.NextToken = params.get("NextToken")
        self.Percentage = params.get("Percentage")
        self.ProgressDetail = params.get("ProgressDetail")
        self.DisplayFormat = params.get("DisplayFormat")
        self.SchemaAffected = params.get("SchemaAffected")
        self.CanDownload = params.get("CanDownload")
        self.TotalTime = params.get("TotalTime")
        memeber_set = set(params.keys())
        for name, value in vars(self).items():
            if name in memeber_set:
                memeber_set.remove(name)
        if len(memeber_set) > 0:
            warnings.warn("%s fileds are useless." % ",".join(memeber_set))
        


class TaskStatisticMetrics(AbstractModel):
    """任务指标信息

    """

    def __init__(self):
        r"""
        :param QueryResultTime: 获取结果时间
注意：此字段可能返回 null，表示取不到有效值。
        :type QueryResultTime: float
        """
        self.QueryResultTime = None


    def _deserialize(self, params):
        self.QueryResultTime = params.get("QueryResultTime")
        memeber_set = set(params.keys())
        for name, value in vars(self).items():
            if name in memeber_set:
                memeber_set.remove(name)
        if len(memeber_set) > 0:
            warnings.warn("%s fileds are useless." % ",".join(memeber_set))
        


class TasksInfo(AbstractModel):
    """批量顺序执行任务集合

    """

    def __init__(self):
        r"""
        :param TaskType: 任务类型，SQLTask：SQL查询任务。SparkSQLTask：Spark SQL查询任务
        :type TaskType: str
        :param FailureTolerance: 容错策略。Proceed：前面任务出错/取消后继续执行后面的任务。Terminate：前面的任务出错/取消之后终止后面任务的执行，后面的任务全部标记为已取消。
        :type FailureTolerance: str
        :param SQL: base64加密后的SQL语句，用";"号分隔每个SQL语句，一次最多提交50个任务。严格按照前后顺序执行
        :type SQL: str
        :param Config: 任务的配置信息，当前仅支持SparkSQLTask任务。
        :type Config: list of KVPair
        :param Params: 任务的用户自定义参数信息
        :type Params: list of KVPair
        """
        self.TaskType = None
        self.FailureTolerance = None
        self.SQL = None
        self.Config = None
        self.Params = None


    def _deserialize(self, params):
        self.TaskType = params.get("TaskType")
        self.FailureTolerance = params.get("FailureTolerance")
        self.SQL = params.get("SQL")
        if params.get("Config") is not None:
            self.Config = []
            for item in params.get("Config"):
                obj = KVPair()
                obj._deserialize(item)
                self.Config.append(obj)
        if params.get("Params") is not None:
            self.Params = []
            for item in params.get("Params"):
                obj = KVPair()
                obj._deserialize(item)
                self.Params.append(obj)
        memeber_set = set(params.keys())
        for name, value in vars(self).items():
            if name in memeber_set:
                memeber_set.remove(name)
        if len(memeber_set) > 0:
            warnings.warn("%s fileds are useless." % ",".join(memeber_set))
        


class TasksOverview(AbstractModel):
    """任务概览

    """

    def __init__(self):
        r"""
        :param TaskQueuedCount: 正在排队的任务个数
        :type TaskQueuedCount: int
        :param TaskInitCount: 初始化的任务个数
        :type TaskInitCount: int
        :param TaskRunningCount: 正在执行的任务个数
        :type TaskRunningCount: int
        :param TotalTaskCount: 当前时间范围的总任务个数
        :type TotalTaskCount: int
        """
        self.TaskQueuedCount = None
        self.TaskInitCount = None
        self.TaskRunningCount = None
        self.TotalTaskCount = None


    def _deserialize(self, params):
        self.TaskQueuedCount = params.get("TaskQueuedCount")
        self.TaskInitCount = params.get("TaskInitCount")
        self.TaskRunningCount = params.get("TaskRunningCount")
        self.TotalTaskCount = params.get("TotalTaskCount")
        memeber_set = set(params.keys())
        for name, value in vars(self).items():
            if name in memeber_set:
                memeber_set.remove(name)
        if len(memeber_set) > 0:
            warnings.warn("%s fileds are useless." % ",".join(memeber_set))
        


class TenantGovernEventRules(AbstractModel):
    """用户数据治理事件阈值

    """

    def __init__(self):
        r"""
        :param Id: 事件阈值ID
        :type Id: int
        :param Type: 事件阈值类型
        :type Type: str
        :param AppId: 用户AppId
        :type AppId: str
        :param Name: 治理事件阈值名称
        :type Name: str
        :param Rule: 数据治理时间阈值
        :type Rule: :class:`tencentcloud.dlc.v20210125.models.RuleThreshold`
        """
        self.Id = None
        self.Type = None
        self.AppId = None
        self.Name = None
        self.Rule = None


    def _deserialize(self, params):
        self.Id = params.get("Id")
        self.Type = params.get("Type")
        self.AppId = params.get("AppId")
        self.Name = params.get("Name")
        if params.get("Rule") is not None:
            self.Rule = RuleThreshold()
            self.Rule._deserialize(params.get("Rule"))
        memeber_set = set(params.keys())
        for name, value in vars(self).items():
            if name in memeber_set:
                memeber_set.remove(name)
        if len(memeber_set) > 0:
            warnings.warn("%s fileds are useless." % ",".join(memeber_set))
        


class TextFile(AbstractModel):
    """文本格式

    """

    def __init__(self):
        r"""
        :param Format: 文本类型，本参数取值为TextFile。
        :type Format: str
        :param Regex: 处理文本用的正则表达式。
注意：此字段可能返回 null，表示取不到有效值。
        :type Regex: str
        """
        self.Format = None
        self.Regex = None


    def _deserialize(self, params):
        self.Format = params.get("Format")
        self.Regex = params.get("Regex")
        memeber_set = set(params.keys())
        for name, value in vars(self).items():
            if name in memeber_set:
                memeber_set.remove(name)
        if len(memeber_set) > 0:
            warnings.warn("%s fileds are useless." % ",".join(memeber_set))
        


class TopPrivateEngineData(AbstractModel):
    """首页CU用量top2数据

    """

    def __init__(self):
        r"""
        :param TopFirst: top1数据
注意：此字段可能返回 null，表示取不到有效值。
        :type TopFirst: :class:`tencentcloud.dlc.v20210125.models.TopPrivateEngineDataDetail`
        :param TopSecond: top2数据
注意：此字段可能返回 null，表示取不到有效值。
        :type TopSecond: :class:`tencentcloud.dlc.v20210125.models.TopPrivateEngineDataDetail`
        """
        self.TopFirst = None
        self.TopSecond = None


    def _deserialize(self, params):
        if params.get("TopFirst") is not None:
            self.TopFirst = TopPrivateEngineDataDetail()
            self.TopFirst._deserialize(params.get("TopFirst"))
        if params.get("TopSecond") is not None:
            self.TopSecond = TopPrivateEngineDataDetail()
            self.TopSecond._deserialize(params.get("TopSecond"))
        memeber_set = set(params.keys())
        for name, value in vars(self).items():
            if name in memeber_set:
                memeber_set.remove(name)
        if len(memeber_set) > 0:
            warnings.warn("%s fileds are useless." % ",".join(memeber_set))
        


class TopPrivateEngineDataDetail(AbstractModel):
    """首页CU用量top2数据明细

    """

    def __init__(self):
        r"""
        :param Name: CU名称
注意：此字段可能返回 null，表示取不到有效值。
        :type Name: str
        :param Size: CU规格
注意：此字段可能返回 null，表示取不到有效值。
        :type Size: int
        :param List: top分小时数据
注意：此字段可能返回 null，表示取不到有效值。
        :type List: list of TopPrivateEngineDataLine
        :param MinClusters: CU最小规格
注意：此字段可能返回 null，表示取不到有效值。
        :type MinClusters: int
        :param MaxClusters: CU最大规格
注意：此字段可能返回 null，表示取不到有效值。
        :type MaxClusters: int
        :param State: 状态
注意：此字段可能返回 null，表示取不到有效值。
        :type State: int
        """
        self.Name = None
        self.Size = None
        self.List = None
        self.MinClusters = None
        self.MaxClusters = None
        self.State = None


    def _deserialize(self, params):
        self.Name = params.get("Name")
        self.Size = params.get("Size")
        if params.get("List") is not None:
            self.List = []
            for item in params.get("List"):
                obj = TopPrivateEngineDataLine()
                obj._deserialize(item)
                self.List.append(obj)
        self.MinClusters = params.get("MinClusters")
        self.MaxClusters = params.get("MaxClusters")
        self.State = params.get("State")
        memeber_set = set(params.keys())
        for name, value in vars(self).items():
            if name in memeber_set:
                memeber_set.remove(name)
        if len(memeber_set) > 0:
            warnings.warn("%s fileds are useless." % ",".join(memeber_set))
        


class TopPrivateEngineDataLine(AbstractModel):
    """首页CU用量top2数据明细折线

    """

    def __init__(self):
        r"""
        :param Hour: 小时数
注意：此字段可能返回 null，表示取不到有效值。
        :type Hour: int
        :param Count: CU时用量
注意：此字段可能返回 null，表示取不到有效值。
        :type Count: float
        """
        self.Hour = None
        self.Count = None


    def _deserialize(self, params):
        self.Hour = params.get("Hour")
        self.Count = params.get("Count")
        memeber_set = set(params.keys())
        for name, value in vars(self).items():
            if name in memeber_set:
                memeber_set.remove(name)
        if len(memeber_set) > 0:
            warnings.warn("%s fileds are useless." % ",".join(memeber_set))
        


class UdfInfo(AbstractModel):
    """Udf详细信息

    """

    def __init__(self):
        r"""
        :param DatabaseName: 数据库名称
        :type DatabaseName: str
        :param Name: udf名称
        :type Name: str
        :param StoreType: 存储方式：1-上传到系统保存，2-指定cos挂载
        :type StoreType: int
        :param PackageSource: 程序包来源：1-本地上传，2-数据存储cos
        :type PackageSource: int
        :param PackagePath: jar所在路径
        :type PackagePath: str
        :param PackageName: jar包名称
        :type PackageName: str
        :param MainClass: 主类
        :type MainClass: str
        :param Id: udf主键id
注意：此字段可能返回 null，表示取不到有效值。
        :type Id: int
        :param Description: 描述
注意：此字段可能返回 null，表示取不到有效值。
        :type Description: str
        :param BuildStatus: udf构建状态：1-初始化，2-构建中，3-构建成功，4-构建失败
注意：此字段可能返回 null，表示取不到有效值。
        :type BuildStatus: int
        :param DataEngineName: 计算资源名称
注意：此字段可能返回 null，表示取不到有效值。
        :type DataEngineName: str
        """
        self.DatabaseName = None
        self.Name = None
        self.StoreType = None
        self.PackageSource = None
        self.PackagePath = None
        self.PackageName = None
        self.MainClass = None
        self.Id = None
        self.Description = None
        self.BuildStatus = None
        self.DataEngineName = None


    def _deserialize(self, params):
        self.DatabaseName = params.get("DatabaseName")
        self.Name = params.get("Name")
        self.StoreType = params.get("StoreType")
        self.PackageSource = params.get("PackageSource")
        self.PackagePath = params.get("PackagePath")
        self.PackageName = params.get("PackageName")
        self.MainClass = params.get("MainClass")
        self.Id = params.get("Id")
        self.Description = params.get("Description")
        self.BuildStatus = params.get("BuildStatus")
        self.DataEngineName = params.get("DataEngineName")
        memeber_set = set(params.keys())
        for name, value in vars(self).items():
            if name in memeber_set:
                memeber_set.remove(name)
        if len(memeber_set) > 0:
            warnings.warn("%s fileds are useless." % ",".join(memeber_set))
        


class UnbindWorkGroupsFromUserRequest(AbstractModel):
    """UnbindWorkGroupsFromUser请求参数结构体

    """

    def __init__(self):
        r"""
        :param AddInfo: 解绑的工作组Id和用户Id的关联关系
        :type AddInfo: :class:`tencentcloud.dlc.v20210125.models.WorkGroupIdSetOfUserId`
        """
        self.AddInfo = None


    def _deserialize(self, params):
        if params.get("AddInfo") is not None:
            self.AddInfo = WorkGroupIdSetOfUserId()
            self.AddInfo._deserialize(params.get("AddInfo"))
        memeber_set = set(params.keys())
        for name, value in vars(self).items():
            if name in memeber_set:
                memeber_set.remove(name)
        if len(memeber_set) > 0:
            warnings.warn("%s fileds are useless." % ",".join(memeber_set))
        


class UnbindWorkGroupsFromUserResponse(AbstractModel):
    """UnbindWorkGroupsFromUser返回参数结构体

    """

    def __init__(self):
        r"""
        :param RequestId: 唯一请求 ID，每次请求都会返回。定位问题时需要提供该次请求的 RequestId。
        :type RequestId: str
        """
        self.RequestId = None


    def _deserialize(self, params):
        self.RequestId = params.get("RequestId")


class UnboundDatasourceHouseRequest(AbstractModel):
    """UnboundDatasourceHouse请求参数结构体

    """

    def __init__(self):
        r"""
        :param NetworkConnectionName: 网络配置名称
        :type NetworkConnectionName: str
        """
        self.NetworkConnectionName = None


    def _deserialize(self, params):
        self.NetworkConnectionName = params.get("NetworkConnectionName")
        memeber_set = set(params.keys())
        for name, value in vars(self).items():
            if name in memeber_set:
                memeber_set.remove(name)
        if len(memeber_set) > 0:
            warnings.warn("%s fileds are useless." % ",".join(memeber_set))
        


class UnboundDatasourceHouseResponse(AbstractModel):
    """UnboundDatasourceHouse返回参数结构体

    """

    def __init__(self):
        r"""
        :param RequestId: 唯一请求 ID，每次请求都会返回。定位问题时需要提供该次请求的 RequestId。
        :type RequestId: str
        """
        self.RequestId = None


    def _deserialize(self, params):
        self.RequestId = params.get("RequestId")


class UnlockMetaDataRequest(AbstractModel):
    """UnlockMetaData请求参数结构体

    """

    def __init__(self):
        r"""
        :param LockId: 锁ID
        :type LockId: int
        :param DatasourceConnectionName: 数据源名称
        :type DatasourceConnectionName: str
        """
        self.LockId = None
        self.DatasourceConnectionName = None


    def _deserialize(self, params):
        self.LockId = params.get("LockId")
        self.DatasourceConnectionName = params.get("DatasourceConnectionName")
        memeber_set = set(params.keys())
        for name, value in vars(self).items():
            if name in memeber_set:
                memeber_set.remove(name)
        if len(memeber_set) > 0:
            warnings.warn("%s fileds are useless." % ",".join(memeber_set))
        


class UnlockMetaDataResponse(AbstractModel):
    """UnlockMetaData返回参数结构体

    """

    def __init__(self):
        r"""
        :param RequestId: 唯一请求 ID，每次请求都会返回。定位问题时需要提供该次请求的 RequestId。
        :type RequestId: str
        """
        self.RequestId = None


    def _deserialize(self, params):
        self.RequestId = params.get("RequestId")


class UpdateDataEngineConfigRequest(AbstractModel):
    """UpdateDataEngineConfig请求参数结构体

    """

    def __init__(self):
        r"""
        :param DataEngineIds: 引擎ID
        :type DataEngineIds: list of str
        :param DataEngineConfigCommand: 引擎配置命令，支持UpdateSparkSQLLakefsPath（更新原生表配置）、UpdateSparkSQLResultPath（更新结果路径配置）
        :type DataEngineConfigCommand: str
        """
        self.DataEngineIds = None
        self.DataEngineConfigCommand = None


    def _deserialize(self, params):
        self.DataEngineIds = params.get("DataEngineIds")
        self.DataEngineConfigCommand = params.get("DataEngineConfigCommand")
        memeber_set = set(params.keys())
        for name, value in vars(self).items():
            if name in memeber_set:
                memeber_set.remove(name)
        if len(memeber_set) > 0:
            warnings.warn("%s fileds are useless." % ",".join(memeber_set))
        


class UpdateDataEngineConfigResponse(AbstractModel):
    """UpdateDataEngineConfig返回参数结构体

    """

    def __init__(self):
        r"""
        :param RequestId: 唯一请求 ID，每次请求都会返回。定位问题时需要提供该次请求的 RequestId。
        :type RequestId: str
        """
        self.RequestId = None


    def _deserialize(self, params):
        self.RequestId = params.get("RequestId")


class UpdateDataEngineRequest(AbstractModel):
    """UpdateDataEngine请求参数结构体

    """

    def __init__(self):
        r"""
        :param Size: 资源大小
        :type Size: int
        :param MinClusters: 最小资源
        :type MinClusters: int
        :param MaxClusters: 最大资源
        :type MaxClusters: int
        :param AutoResume: 开启自动刷新：true：开启、false（默认）：关闭
        :type AutoResume: bool
        :param DataEngineName: 数据引擎名称
        :type DataEngineName: str
        :param Message: 相关信息
        :type Message: str
        :param AutoSuspend: 是否自定挂起集群：false（默认）：不自动挂起、true：自动挂起
        :type AutoSuspend: bool
        :param CrontabResumeSuspend: 定时启停集群策略：0（默认）：关闭定时策略、1：开启定时策略（注：定时启停策略与自动挂起策略互斥）
        :type CrontabResumeSuspend: int
        :param CrontabResumeSuspendStrategy: 定时启停策略，复杂类型：包含启停时间、挂起集群策略
        :type CrontabResumeSuspendStrategy: :class:`tencentcloud.dlc.v20210125.models.CrontabResumeSuspendStrategy`
        :param MaxConcurrency: 单个集群最大并发任务数，默认5
        :type MaxConcurrency: int
        :param TolerableQueueTime: 可容忍的排队时间，默认0。当任务排队的时间超过可容忍的时间时可能会触发扩容。如果该参数为0，则表示一旦有任务排队就可能立即触发扩容。
        :type TolerableQueueTime: int
        :param AutoSuspendTime: 集群自动挂起时间
        :type AutoSuspendTime: int
        :param ElasticSwitch: spark jar 包年包月集群是否开启弹性
        :type ElasticSwitch: bool
        :param ElasticLimit: spark jar 包年包月集群弹性上限
        :type ElasticLimit: int
        :param SessionResourceTemplate: Spark批作业集群Session资源配置模板
        :type SessionResourceTemplate: :class:`tencentcloud.dlc.v20210125.models.SessionResourceTemplate`
        """
        self.Size = None
        self.MinClusters = None
        self.MaxClusters = None
        self.AutoResume = None
        self.DataEngineName = None
        self.Message = None
        self.AutoSuspend = None
        self.CrontabResumeSuspend = None
        self.CrontabResumeSuspendStrategy = None
        self.MaxConcurrency = None
        self.TolerableQueueTime = None
        self.AutoSuspendTime = None
        self.ElasticSwitch = None
        self.ElasticLimit = None
        self.SessionResourceTemplate = None


    def _deserialize(self, params):
        self.Size = params.get("Size")
        self.MinClusters = params.get("MinClusters")
        self.MaxClusters = params.get("MaxClusters")
        self.AutoResume = params.get("AutoResume")
        self.DataEngineName = params.get("DataEngineName")
        self.Message = params.get("Message")
        self.AutoSuspend = params.get("AutoSuspend")
        self.CrontabResumeSuspend = params.get("CrontabResumeSuspend")
        if params.get("CrontabResumeSuspendStrategy") is not None:
            self.CrontabResumeSuspendStrategy = CrontabResumeSuspendStrategy()
            self.CrontabResumeSuspendStrategy._deserialize(params.get("CrontabResumeSuspendStrategy"))
        self.MaxConcurrency = params.get("MaxConcurrency")
        self.TolerableQueueTime = params.get("TolerableQueueTime")
        self.AutoSuspendTime = params.get("AutoSuspendTime")
        self.ElasticSwitch = params.get("ElasticSwitch")
        self.ElasticLimit = params.get("ElasticLimit")
        if params.get("SessionResourceTemplate") is not None:
            self.SessionResourceTemplate = SessionResourceTemplate()
            self.SessionResourceTemplate._deserialize(params.get("SessionResourceTemplate"))
        memeber_set = set(params.keys())
        for name, value in vars(self).items():
            if name in memeber_set:
                memeber_set.remove(name)
        if len(memeber_set) > 0:
            warnings.warn("%s fileds are useless." % ",".join(memeber_set))
        


class UpdateDataEngineResponse(AbstractModel):
    """UpdateDataEngine返回参数结构体

    """

    def __init__(self):
        r"""
        :param RequestId: 唯一请求 ID，每次请求都会返回。定位问题时需要提供该次请求的 RequestId。
        :type RequestId: str
        """
        self.RequestId = None


    def _deserialize(self, params):
        self.RequestId = params.get("RequestId")


class UpdateDataQueryRequest(AbstractModel):
    """UpdateDataQuery请求参数结构体

    """

    def __init__(self):
        r"""
        :param Name: 更新查询的名称
        :type Name: str
        :param Dir: 更新查询的目录
        :type Dir: str
        :param Statement: 更新查询的sql信息
        :type Statement: str
        :param Params: 更新查询的参数信息
        :type Params: str
        """
        self.Name = None
        self.Dir = None
        self.Statement = None
        self.Params = None


    def _deserialize(self, params):
        self.Name = params.get("Name")
        self.Dir = params.get("Dir")
        self.Statement = params.get("Statement")
        self.Params = params.get("Params")
        memeber_set = set(params.keys())
        for name, value in vars(self).items():
            if name in memeber_set:
                memeber_set.remove(name)
        if len(memeber_set) > 0:
            warnings.warn("%s fileds are useless." % ",".join(memeber_set))
        


class UpdateDataQueryResponse(AbstractModel):
    """UpdateDataQuery返回参数结构体

    """

    def __init__(self):
        r"""
        :param RequestId: 唯一请求 ID，每次请求都会返回。定位问题时需要提供该次请求的 RequestId。
        :type RequestId: str
        """
        self.RequestId = None


    def _deserialize(self, params):
        self.RequestId = params.get("RequestId")


class UpdateDatasourceConnectionRequest(AbstractModel):
    """UpdateDatasourceConnection请求参数结构体

    """

    def __init__(self):
        r"""
        :param DatasourceConnectionIds: 数据连接唯一Id
        :type DatasourceConnectionIds: list of str
        """
        self.DatasourceConnectionIds = None


    def _deserialize(self, params):
        self.DatasourceConnectionIds = params.get("DatasourceConnectionIds")
        memeber_set = set(params.keys())
        for name, value in vars(self).items():
            if name in memeber_set:
                memeber_set.remove(name)
        if len(memeber_set) > 0:
            warnings.warn("%s fileds are useless." % ",".join(memeber_set))
        


class UpdateDatasourceConnectionResponse(AbstractModel):
    """UpdateDatasourceConnection返回参数结构体

    """

    def __init__(self):
        r"""
        :param RequestId: 唯一请求 ID，每次请求都会返回。定位问题时需要提供该次请求的 RequestId。
        :type RequestId: str
        """
        self.RequestId = None


    def _deserialize(self, params):
        self.RequestId = params.get("RequestId")


class UpdateHouseRequest(AbstractModel):
    """UpdateHouse请求参数结构体

    """

    def __init__(self):
        r"""
        :param Size: 资源大小
        :type Size: int
        :param MinClusters: 最小资源
        :type MinClusters: int
        :param MaxClusters: 最大资源
        :type MaxClusters: int
        :param AutoResume: 开启自动刷新：true：开启、false（默认）：关闭
        :type AutoResume: bool
        :param HouseName: House名称
        :type HouseName: str
        :param Message: 相关信息
        :type Message: str
        """
        self.Size = None
        self.MinClusters = None
        self.MaxClusters = None
        self.AutoResume = None
        self.HouseName = None
        self.Message = None


    def _deserialize(self, params):
        self.Size = params.get("Size")
        self.MinClusters = params.get("MinClusters")
        self.MaxClusters = params.get("MaxClusters")
        self.AutoResume = params.get("AutoResume")
        self.HouseName = params.get("HouseName")
        self.Message = params.get("Message")
        memeber_set = set(params.keys())
        for name, value in vars(self).items():
            if name in memeber_set:
                memeber_set.remove(name)
        if len(memeber_set) > 0:
            warnings.warn("%s fileds are useless." % ",".join(memeber_set))
        


class UpdateHouseResponse(AbstractModel):
    """UpdateHouse返回参数结构体

    """

    def __init__(self):
        r"""
        :param RequestId: 唯一请求 ID，每次请求都会返回。定位问题时需要提供该次请求的 RequestId。
        :type RequestId: str
        """
        self.RequestId = None


    def _deserialize(self, params):
        self.RequestId = params.get("RequestId")


class UpdateNetworkConnectionRequest(AbstractModel):
    """UpdateNetworkConnection请求参数结构体

    """

    def __init__(self):
        r"""
        :param NetworkConnectionDesc: 网络配置描述
        :type NetworkConnectionDesc: str
        :param NetworkConnectionName: 网络配置名称
        :type NetworkConnectionName: str
        """
        self.NetworkConnectionDesc = None
        self.NetworkConnectionName = None


    def _deserialize(self, params):
        self.NetworkConnectionDesc = params.get("NetworkConnectionDesc")
        self.NetworkConnectionName = params.get("NetworkConnectionName")
        memeber_set = set(params.keys())
        for name, value in vars(self).items():
            if name in memeber_set:
                memeber_set.remove(name)
        if len(memeber_set) > 0:
            warnings.warn("%s fileds are useless." % ",".join(memeber_set))
        


class UpdateNetworkConnectionResponse(AbstractModel):
    """UpdateNetworkConnection返回参数结构体

    """

    def __init__(self):
        r"""
        :param RequestId: 唯一请求 ID，每次请求都会返回。定位问题时需要提供该次请求的 RequestId。
        :type RequestId: str
        """
        self.RequestId = None


    def _deserialize(self, params):
        self.RequestId = params.get("RequestId")


class UpdateRowFilterRequest(AbstractModel):
    """UpdateRowFilter请求参数结构体

    """

    def __init__(self):
        r"""
        :param PolicyId: 行过滤策略的id，此值可以通过DescribeUserInfo或者DescribeWorkGroupInfo接口获取
        :type PolicyId: int
        :param Policy: 新的过滤策略。
        :type Policy: :class:`tencentcloud.dlc.v20210125.models.Policy`
        """
        self.PolicyId = None
        self.Policy = None


    def _deserialize(self, params):
        self.PolicyId = params.get("PolicyId")
        if params.get("Policy") is not None:
            self.Policy = Policy()
            self.Policy._deserialize(params.get("Policy"))
        memeber_set = set(params.keys())
        for name, value in vars(self).items():
            if name in memeber_set:
                memeber_set.remove(name)
        if len(memeber_set) > 0:
            warnings.warn("%s fileds are useless." % ",".join(memeber_set))
        


class UpdateRowFilterResponse(AbstractModel):
    """UpdateRowFilter返回参数结构体

    """

    def __init__(self):
        r"""
        :param RequestId: 唯一请求 ID，每次请求都会返回。定位问题时需要提供该次请求的 RequestId。
        :type RequestId: str
        """
        self.RequestId = None


    def _deserialize(self, params):
        self.RequestId = params.get("RequestId")


class UpdateTaskStatusRequest(AbstractModel):
    """UpdateTaskStatus请求参数结构体

    """

    def __init__(self):
        r"""
        :param TaskId: 任务id
        :type TaskId: str
        :param TaskStatus: 任务状态 0-执行完成 1-初始化 5-执行中
        :type TaskStatus: int
        """
        self.TaskId = None
        self.TaskStatus = None


    def _deserialize(self, params):
        self.TaskId = params.get("TaskId")
        self.TaskStatus = params.get("TaskStatus")
        memeber_set = set(params.keys())
        for name, value in vars(self).items():
            if name in memeber_set:
                memeber_set.remove(name)
        if len(memeber_set) > 0:
            warnings.warn("%s fileds are useless." % ",".join(memeber_set))
        


class UpdateTaskStatusResponse(AbstractModel):
    """UpdateTaskStatus返回参数结构体

    """

    def __init__(self):
        r"""
        :param RequestId: 唯一请求 ID，每次请求都会返回。定位问题时需要提供该次请求的 RequestId。
        :type RequestId: str
        """
        self.RequestId = None


    def _deserialize(self, params):
        self.RequestId = params.get("RequestId")


class UpdateUserDataEngineConfigRequest(AbstractModel):
    """UpdateUserDataEngineConfig请求参数结构体

    """

    def __init__(self):
        r"""
        :param DataEngineId: 引擎ID
        :type DataEngineId: str
        :param DataEngineConfigPairs: 引擎配置项
        :type DataEngineConfigPairs: list of DataEngineConfigPair
        :param SessionResourceTemplate: 作业引擎资源配置模版
        :type SessionResourceTemplate: :class:`tencentcloud.dlc.v20210125.models.SessionResourceTemplate`
        """
        self.DataEngineId = None
        self.DataEngineConfigPairs = None
        self.SessionResourceTemplate = None


    def _deserialize(self, params):
        self.DataEngineId = params.get("DataEngineId")
        if params.get("DataEngineConfigPairs") is not None:
            self.DataEngineConfigPairs = []
            for item in params.get("DataEngineConfigPairs"):
                obj = DataEngineConfigPair()
                obj._deserialize(item)
                self.DataEngineConfigPairs.append(obj)
        if params.get("SessionResourceTemplate") is not None:
            self.SessionResourceTemplate = SessionResourceTemplate()
            self.SessionResourceTemplate._deserialize(params.get("SessionResourceTemplate"))
        memeber_set = set(params.keys())
        for name, value in vars(self).items():
            if name in memeber_set:
                memeber_set.remove(name)
        if len(memeber_set) > 0:
            warnings.warn("%s fileds are useless." % ",".join(memeber_set))
        


class UpdateUserDataEngineConfigResponse(AbstractModel):
    """UpdateUserDataEngineConfig返回参数结构体

    """

    def __init__(self):
        r"""
        :param RequestId: 唯一请求 ID，每次请求都会返回。定位问题时需要提供该次请求的 RequestId。
        :type RequestId: str
        """
        self.RequestId = None


    def _deserialize(self, params):
        self.RequestId = params.get("RequestId")


class UpdateUserRoleRequest(AbstractModel):
    """UpdateUserRole请求参数结构体

    """

    def __init__(self):
        r"""
        :param RoleId: 角色ID
        :type RoleId: int
        :param Desc: 描述信息
        :type Desc: str
        """
        self.RoleId = None
        self.Desc = None


    def _deserialize(self, params):
        self.RoleId = params.get("RoleId")
        self.Desc = params.get("Desc")
        memeber_set = set(params.keys())
        for name, value in vars(self).items():
            if name in memeber_set:
                memeber_set.remove(name)
        if len(memeber_set) > 0:
            warnings.warn("%s fileds are useless." % ",".join(memeber_set))
        


class UpdateUserRoleResponse(AbstractModel):
    """UpdateUserRole返回参数结构体

    """

    def __init__(self):
        r"""
        :param RequestId: 唯一请求 ID，每次请求都会返回。定位问题时需要提供该次请求的 RequestId。
        :type RequestId: str
        """
        self.RequestId = None


    def _deserialize(self, params):
        self.RequestId = params.get("RequestId")


class UpdateWorkflowRequest(AbstractModel):
    """UpdateWorkflow请求参数结构体

    """

    def __init__(self):
        r"""
        :param WorkflowId: 调度计划ID
        :type WorkflowId: str
        :param WorkflowName: 调度计划名称
        :type WorkflowName: str
        :param CycleType: 调度周期类型，分钟(MINUTE_CYCLE)，小时(HOUR_CYCLE)，天(DAY_CYCLE)，周(WEEK_CYCLE),月(MONTH_CYCLE)，一次性(ONEOFF_CYCLE)
        :type CycleType: str
        :param CycleStep: 任务调度周期间隔
        :type CycleStep: int
        :param DelayTime: 调度任务延迟时间，从调度周期开始时间计算的分钟数
        :type DelayTime: int
        :param TaskAction: 在指定周期的第n个单位时间运行（周和月任务使用），比如周任务周日运行：TaskAction=1；周一运行：TaskAction=2，月任务当月第1天运行：TaskAction=1，等
        :type TaskAction: str
        :param StartTime: 调度计划开始时间
        :type StartTime: str
        :param EndTime: 调度计划结束时间
        :type EndTime: str
        :param WorkflowDesc: 调度计划描述
        :type WorkflowDesc: str
        :param OwnersUin: 责任人uin
        :type OwnersUin: list of str
        """
        self.WorkflowId = None
        self.WorkflowName = None
        self.CycleType = None
        self.CycleStep = None
        self.DelayTime = None
        self.TaskAction = None
        self.StartTime = None
        self.EndTime = None
        self.WorkflowDesc = None
        self.OwnersUin = None


    def _deserialize(self, params):
        self.WorkflowId = params.get("WorkflowId")
        self.WorkflowName = params.get("WorkflowName")
        self.CycleType = params.get("CycleType")
        self.CycleStep = params.get("CycleStep")
        self.DelayTime = params.get("DelayTime")
        self.TaskAction = params.get("TaskAction")
        self.StartTime = params.get("StartTime")
        self.EndTime = params.get("EndTime")
        self.WorkflowDesc = params.get("WorkflowDesc")
        self.OwnersUin = params.get("OwnersUin")
        memeber_set = set(params.keys())
        for name, value in vars(self).items():
            if name in memeber_set:
                memeber_set.remove(name)
        if len(memeber_set) > 0:
            warnings.warn("%s fileds are useless." % ",".join(memeber_set))
        


class UpdateWorkflowResponse(AbstractModel):
    """UpdateWorkflow返回参数结构体

    """

    def __init__(self):
        r"""
        :param RequestId: 唯一请求 ID，每次请求都会返回。定位问题时需要提供该次请求的 RequestId。
        :type RequestId: str
        """
        self.RequestId = None


    def _deserialize(self, params):
        self.RequestId = params.get("RequestId")


class UpgradeDataEngineImageRequest(AbstractModel):
    """UpgradeDataEngineImage请求参数结构体

    """

    def __init__(self):
        r"""
        :param DataEngineId: 引擎ID
        :type DataEngineId: str
        """
        self.DataEngineId = None


    def _deserialize(self, params):
        self.DataEngineId = params.get("DataEngineId")
        memeber_set = set(params.keys())
        for name, value in vars(self).items():
            if name in memeber_set:
                memeber_set.remove(name)
        if len(memeber_set) > 0:
            warnings.warn("%s fileds are useless." % ",".join(memeber_set))
        


class UpgradeDataEngineImageResponse(AbstractModel):
    """UpgradeDataEngineImage返回参数结构体

    """

    def __init__(self):
        r"""
        :param RequestId: 唯一请求 ID，每次请求都会返回。定位问题时需要提供该次请求的 RequestId。
        :type RequestId: str
        """
        self.RequestId = None


    def _deserialize(self, params):
        self.RequestId = params.get("RequestId")


class UserAliasInfo(AbstractModel):
    """用户id和名字信息

    """

    def __init__(self):
        r"""
        :param UserId: uin
        :type UserId: str
        :param UserAlias: 用户别名
        :type UserAlias: str
        """
        self.UserId = None
        self.UserAlias = None


    def _deserialize(self, params):
        self.UserId = params.get("UserId")
        self.UserAlias = params.get("UserAlias")
        memeber_set = set(params.keys())
        for name, value in vars(self).items():
            if name in memeber_set:
                memeber_set.remove(name)
        if len(memeber_set) > 0:
            warnings.warn("%s fileds are useless." % ",".join(memeber_set))
        


class UserDetailInfo(AbstractModel):
    """用户详细信息

    """

    def __init__(self):
        r"""
        :param UserId: 用户Id
注意：此字段可能返回 null，表示取不到有效值。
        :type UserId: str
        :param Type: 返回的信息类型，Group：返回的当前用户的工作组信息；DataAuth：返回的当前用户的数据权限信息；EngineAuth：返回的当前用户的引擎权限信息
注意：此字段可能返回 null，表示取不到有效值。
        :type Type: str
        :param UserType: 用户类型：ADMIN：管理员 COMMON：一般用户
注意：此字段可能返回 null，表示取不到有效值。
        :type UserType: str
        :param UserDescription: 用户描述信息
注意：此字段可能返回 null，表示取不到有效值。
        :type UserDescription: str
        :param DataPolicyInfo: 数据权限信息集合
注意：此字段可能返回 null，表示取不到有效值。
        :type DataPolicyInfo: :class:`tencentcloud.dlc.v20210125.models.Policys`
        :param EnginePolicyInfo: 引擎权限集合
注意：此字段可能返回 null，表示取不到有效值。
        :type EnginePolicyInfo: :class:`tencentcloud.dlc.v20210125.models.Policys`
        :param WorkGroupInfo: 绑定到该用户的工作组集合信息
注意：此字段可能返回 null，表示取不到有效值。
        :type WorkGroupInfo: :class:`tencentcloud.dlc.v20210125.models.WorkGroups`
        :param UserAlias: 用户别名
注意：此字段可能返回 null，表示取不到有效值。
        :type UserAlias: str
        :param RowFilterInfo: 行过滤集合
注意：此字段可能返回 null，表示取不到有效值。
        :type RowFilterInfo: :class:`tencentcloud.dlc.v20210125.models.Policys`
        """
        self.UserId = None
        self.Type = None
        self.UserType = None
        self.UserDescription = None
        self.DataPolicyInfo = None
        self.EnginePolicyInfo = None
        self.WorkGroupInfo = None
        self.UserAlias = None
        self.RowFilterInfo = None


    def _deserialize(self, params):
        self.UserId = params.get("UserId")
        self.Type = params.get("Type")
        self.UserType = params.get("UserType")
        self.UserDescription = params.get("UserDescription")
        if params.get("DataPolicyInfo") is not None:
            self.DataPolicyInfo = Policys()
            self.DataPolicyInfo._deserialize(params.get("DataPolicyInfo"))
        if params.get("EnginePolicyInfo") is not None:
            self.EnginePolicyInfo = Policys()
            self.EnginePolicyInfo._deserialize(params.get("EnginePolicyInfo"))
        if params.get("WorkGroupInfo") is not None:
            self.WorkGroupInfo = WorkGroups()
            self.WorkGroupInfo._deserialize(params.get("WorkGroupInfo"))
        self.UserAlias = params.get("UserAlias")
        if params.get("RowFilterInfo") is not None:
            self.RowFilterInfo = Policys()
            self.RowFilterInfo._deserialize(params.get("RowFilterInfo"))
        memeber_set = set(params.keys())
        for name, value in vars(self).items():
            if name in memeber_set:
                memeber_set.remove(name)
        if len(memeber_set) > 0:
            warnings.warn("%s fileds are useless." % ",".join(memeber_set))
        


class UserIdSetOfWorkGroupId(AbstractModel):
    """绑定到同一个工作组的用户Id的集合

    """

    def __init__(self):
        r"""
        :param WorkGroupId: 工作组Id
        :type WorkGroupId: int
        :param UserIds: 用户Id集合，和CAM侧Uin匹配
        :type UserIds: list of str
        """
        self.WorkGroupId = None
        self.UserIds = None


    def _deserialize(self, params):
        self.WorkGroupId = params.get("WorkGroupId")
        self.UserIds = params.get("UserIds")
        memeber_set = set(params.keys())
        for name, value in vars(self).items():
            if name in memeber_set:
                memeber_set.remove(name)
        if len(memeber_set) > 0:
            warnings.warn("%s fileds are useless." % ",".join(memeber_set))
        


class UserInfo(AbstractModel):
    """授权用户信息

    """

    def __init__(self):
        r"""
        :param UserId: 用户Id，和子用户uin相同
        :type UserId: str
        :param UserDescription: 用户描述信息，方便区分不同用户
注意：此字段可能返回 null，表示取不到有效值。
        :type UserDescription: str
        :param PolicySet: 单独给用户绑定的权限集合
注意：此字段可能返回 null，表示取不到有效值。
        :type PolicySet: list of Policy
        :param Creator: 当前用户的创建者
        :type Creator: str
        :param CreateTime: 创建时间，格式如2021-07-28 16:19:32
        :type CreateTime: str
        :param WorkGroupSet: 关联的工作组集合
注意：此字段可能返回 null，表示取不到有效值。
        :type WorkGroupSet: list of WorkGroupMessage
        :param IsOwner: 是否是主账号
注意：此字段可能返回 null，表示取不到有效值。
        :type IsOwner: bool
        :param UserType: 用户类型。ADMIN：管理员 COMMON：普通用户。
注意：此字段可能返回 null，表示取不到有效值。
        :type UserType: str
        :param UserAlias: 用户别名
注意：此字段可能返回 null，表示取不到有效值。
        :type UserAlias: str
        """
        self.UserId = None
        self.UserDescription = None
        self.PolicySet = None
        self.Creator = None
        self.CreateTime = None
        self.WorkGroupSet = None
        self.IsOwner = None
        self.UserType = None
        self.UserAlias = None


    def _deserialize(self, params):
        self.UserId = params.get("UserId")
        self.UserDescription = params.get("UserDescription")
        if params.get("PolicySet") is not None:
            self.PolicySet = []
            for item in params.get("PolicySet"):
                obj = Policy()
                obj._deserialize(item)
                self.PolicySet.append(obj)
        self.Creator = params.get("Creator")
        self.CreateTime = params.get("CreateTime")
        if params.get("WorkGroupSet") is not None:
            self.WorkGroupSet = []
            for item in params.get("WorkGroupSet"):
                obj = WorkGroupMessage()
                obj._deserialize(item)
                self.WorkGroupSet.append(obj)
        self.IsOwner = params.get("IsOwner")
        self.UserType = params.get("UserType")
        self.UserAlias = params.get("UserAlias")
        memeber_set = set(params.keys())
        for name, value in vars(self).items():
            if name in memeber_set:
                memeber_set.remove(name)
        if len(memeber_set) > 0:
            warnings.warn("%s fileds are useless." % ",".join(memeber_set))
        


class UserMessage(AbstractModel):
    """用户部分信息

    """

    def __init__(self):
        r"""
        :param UserId: 用户Id，和CAM侧子用户Uin匹配
        :type UserId: str
        :param UserDescription: 用户描述
注意：此字段可能返回 null，表示取不到有效值。
        :type UserDescription: str
        :param Creator: 当前用户的创建者
        :type Creator: str
        :param CreateTime: 当前用户的创建时间，形如2021-07-28 16:19:32
        :type CreateTime: str
        :param UserAlias: 用户别名
        :type UserAlias: str
        """
        self.UserId = None
        self.UserDescription = None
        self.Creator = None
        self.CreateTime = None
        self.UserAlias = None


    def _deserialize(self, params):
        self.UserId = params.get("UserId")
        self.UserDescription = params.get("UserDescription")
        self.Creator = params.get("Creator")
        self.CreateTime = params.get("CreateTime")
        self.UserAlias = params.get("UserAlias")
        memeber_set = set(params.keys())
        for name, value in vars(self).items():
            if name in memeber_set:
                memeber_set.remove(name)
        if len(memeber_set) > 0:
            warnings.warn("%s fileds are useless." % ",".join(memeber_set))
        


class UserRole(AbstractModel):
    """用户角色

    """

    def __init__(self):
        r"""
        :param RoleId: 角色ID
        :type RoleId: int
        :param AppId: 用户app ID
        :type AppId: str
        :param Uin: 用户ID
        :type Uin: str
        :param Arn: 角色权限
        :type Arn: str
        :param ModifyTime: 最近修改时间戳
        :type ModifyTime: int
        :param Desc: 角色描述信息
        :type Desc: str
        """
        self.RoleId = None
        self.AppId = None
        self.Uin = None
        self.Arn = None
        self.ModifyTime = None
        self.Desc = None


    def _deserialize(self, params):
        self.RoleId = params.get("RoleId")
        self.AppId = params.get("AppId")
        self.Uin = params.get("Uin")
        self.Arn = params.get("Arn")
        self.ModifyTime = params.get("ModifyTime")
        self.Desc = params.get("Desc")
        memeber_set = set(params.keys())
        for name, value in vars(self).items():
            if name in memeber_set:
                memeber_set.remove(name)
        if len(memeber_set) > 0:
            warnings.warn("%s fileds are useless." % ",".join(memeber_set))
        


class Users(AbstractModel):
    """用户信息集合

    """

    def __init__(self):
        r"""
        :param UserSet: 用户信息集合
注意：此字段可能返回 null，表示取不到有效值。
        :type UserSet: list of UserMessage
        :param TotalCount: 用户总数
注意：此字段可能返回 null，表示取不到有效值。
        :type TotalCount: int
        """
        self.UserSet = None
        self.TotalCount = None


    def _deserialize(self, params):
        if params.get("UserSet") is not None:
            self.UserSet = []
            for item in params.get("UserSet"):
                obj = UserMessage()
                obj._deserialize(item)
                self.UserSet.append(obj)
        self.TotalCount = params.get("TotalCount")
        memeber_set = set(params.keys())
        for name, value in vars(self).items():
            if name in memeber_set:
                memeber_set.remove(name)
        if len(memeber_set) > 0:
            warnings.warn("%s fileds are useless." % ",".join(memeber_set))
        


class ValidateWorkflowNameRequest(AbstractModel):
    """ValidateWorkflowName请求参数结构体

    """

    def __init__(self):
        r"""
        :param WorkflowName: 调度计划名称
        :type WorkflowName: str
        :param WorkflowId: 调度计划ID
        :type WorkflowId: str
        """
        self.WorkflowName = None
        self.WorkflowId = None


    def _deserialize(self, params):
        self.WorkflowName = params.get("WorkflowName")
        self.WorkflowId = params.get("WorkflowId")
        memeber_set = set(params.keys())
        for name, value in vars(self).items():
            if name in memeber_set:
                memeber_set.remove(name)
        if len(memeber_set) > 0:
            warnings.warn("%s fileds are useless." % ",".join(memeber_set))
        


class ValidateWorkflowNameResponse(AbstractModel):
    """ValidateWorkflowName返回参数结构体

    """

    def __init__(self):
        r"""
        :param IsPass: 是否通过校验
        :type IsPass: bool
        :param Msg: 校验不通过时的提示信息
注意：此字段可能返回 null，表示取不到有效值。
        :type Msg: str
        :param RequestId: 唯一请求 ID，每次请求都会返回。定位问题时需要提供该次请求的 RequestId。
        :type RequestId: str
        """
        self.IsPass = None
        self.Msg = None
        self.RequestId = None


    def _deserialize(self, params):
        self.IsPass = params.get("IsPass")
        self.Msg = params.get("Msg")
        self.RequestId = params.get("RequestId")


class ViewBaseInfo(AbstractModel):
    """视图基本配置信息

    """

    def __init__(self):
        r"""
        :param DatabaseName: 该视图所属数据库名字
        :type DatabaseName: str
        :param ViewName: 视图名称
        :type ViewName: str
        :param UserAlias: 视图创建人昵称
        :type UserAlias: str
        :param UserSubUin: 视图创建人ID
        :type UserSubUin: str
        :param ViewId: 视图ID
注意：此字段可能返回 null，表示取不到有效值。
        :type ViewId: str
        :param ViewOriginalText: 创建视图原始文本
注意：此字段可能返回 null，表示取不到有效值。
        :type ViewOriginalText: str
        :param ViewExpandedText: 创建视图展开文本
注意：此字段可能返回 null，表示取不到有效值。
        :type ViewExpandedText: str
        """
        self.DatabaseName = None
        self.ViewName = None
        self.UserAlias = None
        self.UserSubUin = None
        self.ViewId = None
        self.ViewOriginalText = None
        self.ViewExpandedText = None


    def _deserialize(self, params):
        self.DatabaseName = params.get("DatabaseName")
        self.ViewName = params.get("ViewName")
        self.UserAlias = params.get("UserAlias")
        self.UserSubUin = params.get("UserSubUin")
        self.ViewId = params.get("ViewId")
        self.ViewOriginalText = params.get("ViewOriginalText")
        self.ViewExpandedText = params.get("ViewExpandedText")
        memeber_set = set(params.keys())
        for name, value in vars(self).items():
            if name in memeber_set:
                memeber_set.remove(name)
        if len(memeber_set) > 0:
            warnings.warn("%s fileds are useless." % ",".join(memeber_set))
        


class ViewResponseInfo(AbstractModel):
    """查询视图信息对象

    """

    def __init__(self):
        r"""
        :param ViewBaseInfo: 视图基本信息。
        :type ViewBaseInfo: :class:`tencentcloud.dlc.v20210125.models.ViewBaseInfo`
        :param Columns: 视图列信息。
注意：此字段可能返回 null，表示取不到有效值。
        :type Columns: list of Column
        :param Properties: 视图属性信息。
注意：此字段可能返回 null，表示取不到有效值。
        :type Properties: list of Property
        :param CreateTime: 视图创建时间。
        :type CreateTime: str
        :param ModifiedTime: 视图更新时间。
        :type ModifiedTime: str
        :param Comment: 视图的描述信息，已废弃
注意：此字段可能返回 null，表示取不到有效值。
        :type Comment: str
        """
        self.ViewBaseInfo = None
        self.Columns = None
        self.Properties = None
        self.CreateTime = None
        self.ModifiedTime = None
        self.Comment = None


    def _deserialize(self, params):
        if params.get("ViewBaseInfo") is not None:
            self.ViewBaseInfo = ViewBaseInfo()
            self.ViewBaseInfo._deserialize(params.get("ViewBaseInfo"))
        if params.get("Columns") is not None:
            self.Columns = []
            for item in params.get("Columns"):
                obj = Column()
                obj._deserialize(item)
                self.Columns.append(obj)
        if params.get("Properties") is not None:
            self.Properties = []
            for item in params.get("Properties"):
                obj = Property()
                obj._deserialize(item)
                self.Properties.append(obj)
        self.CreateTime = params.get("CreateTime")
        self.ModifiedTime = params.get("ModifiedTime")
        self.Comment = params.get("Comment")
        memeber_set = set(params.keys())
        for name, value in vars(self).items():
            if name in memeber_set:
                memeber_set.remove(name)
        if len(memeber_set) > 0:
            warnings.warn("%s fileds are useless." % ",".join(memeber_set))
        


class VpcCidrBlock(AbstractModel):
    """VPC子网信息

    """

    def __init__(self):
        r"""
        :param CidrId: 子网Id
注意：此字段可能返回 null，表示取不到有效值。
        :type CidrId: str
        :param CidrAddr: 子网网段
注意：此字段可能返回 null，表示取不到有效值。
        :type CidrAddr: str
        """
        self.CidrId = None
        self.CidrAddr = None


    def _deserialize(self, params):
        self.CidrId = params.get("CidrId")
        self.CidrAddr = params.get("CidrAddr")
        memeber_set = set(params.keys())
        for name, value in vars(self).items():
            if name in memeber_set:
                memeber_set.remove(name)
        if len(memeber_set) > 0:
            warnings.warn("%s fileds are useless." % ",".join(memeber_set))
        


class VpcConfigure(AbstractModel):
    """vpc配置

    """

    def __init__(self):
        r"""
        :param VpcId: vpc的唯一ID
注意：此字段可能返回 null，表示取不到有效值。
        :type VpcId: str
        :param VpcName: vpc的名称
注意：此字段可能返回 null，表示取不到有效值。
        :type VpcName: str
        :param VpcCidrBlock: vpc网段
注意：此字段可能返回 null，表示取不到有效值。
        :type VpcCidrBlock: str
        :param AvailableIpAddressCount: 可用的ip个数
注意：此字段可能返回 null，表示取不到有效值。
        :type AvailableIpAddressCount: int
        """
        self.VpcId = None
        self.VpcName = None
        self.VpcCidrBlock = None
        self.AvailableIpAddressCount = None


    def _deserialize(self, params):
        self.VpcId = params.get("VpcId")
        self.VpcName = params.get("VpcName")
        self.VpcCidrBlock = params.get("VpcCidrBlock")
        self.AvailableIpAddressCount = params.get("AvailableIpAddressCount")
        memeber_set = set(params.keys())
        for name, value in vars(self).items():
            if name in memeber_set:
                memeber_set.remove(name)
        if len(memeber_set) > 0:
            warnings.warn("%s fileds are useless." % ",".join(memeber_set))
        


class VpcInfo(AbstractModel):
    """vpc信息

    """

    def __init__(self):
        r"""
        :param VpcId: vpc Id
注意：此字段可能返回 null，表示取不到有效值。
        :type VpcId: str
        :param VpcCidrBlock: vpc子网
注意：此字段可能返回 null，表示取不到有效值。
        :type VpcCidrBlock: str
        """
        self.VpcId = None
        self.VpcCidrBlock = None


    def _deserialize(self, params):
        self.VpcId = params.get("VpcId")
        self.VpcCidrBlock = params.get("VpcCidrBlock")
        memeber_set = set(params.keys())
        for name, value in vars(self).items():
            if name in memeber_set:
                memeber_set.remove(name)
        if len(memeber_set) > 0:
            warnings.warn("%s fileds are useless." % ",".join(memeber_set))
        


class Whitelist(AbstractModel):
    """白名单信息

    """

    def __init__(self):
        r"""
        :param UserId: 用户ID，和uin一致
        :type UserId: str
        :param WhiteKey: 白名单关键字，现在支持“billingNotice-skip”
        :type WhiteKey: str
        :param Strategy: 白名单策略
注意：此字段可能返回 null，表示取不到有效值。
        :type Strategy: str
        """
        self.UserId = None
        self.WhiteKey = None
        self.Strategy = None


    def _deserialize(self, params):
        self.UserId = params.get("UserId")
        self.WhiteKey = params.get("WhiteKey")
        self.Strategy = params.get("Strategy")
        memeber_set = set(params.keys())
        for name, value in vars(self).items():
            if name in memeber_set:
                memeber_set.remove(name)
        if len(memeber_set) > 0:
            warnings.warn("%s fileds are useless." % ",".join(memeber_set))
        


class WorkGroupDetailInfo(AbstractModel):
    """工作组详细信息

    """

    def __init__(self):
        r"""
        :param WorkGroupId: 工作组Id
注意：此字段可能返回 null，表示取不到有效值。
        :type WorkGroupId: int
        :param WorkGroupName: 工作组名称
注意：此字段可能返回 null，表示取不到有效值。
        :type WorkGroupName: str
        :param Type: 包含的信息类型。User：用户信息；DataAuth：数据权限；EngineAuth:引擎权限
注意：此字段可能返回 null，表示取不到有效值。
        :type Type: str
        :param UserInfo: 工作组上绑定的用户集合
注意：此字段可能返回 null，表示取不到有效值。
        :type UserInfo: :class:`tencentcloud.dlc.v20210125.models.Users`
        :param DataPolicyInfo: 数据权限集合
注意：此字段可能返回 null，表示取不到有效值。
        :type DataPolicyInfo: :class:`tencentcloud.dlc.v20210125.models.Policys`
        :param EnginePolicyInfo: 引擎权限集合
注意：此字段可能返回 null，表示取不到有效值。
        :type EnginePolicyInfo: :class:`tencentcloud.dlc.v20210125.models.Policys`
        :param WorkGroupDescription: 工作组描述信息
注意：此字段可能返回 null，表示取不到有效值。
        :type WorkGroupDescription: str
        :param RowFilterInfo: 行过滤信息集合
注意：此字段可能返回 null，表示取不到有效值。
        :type RowFilterInfo: :class:`tencentcloud.dlc.v20210125.models.Policys`
        """
        self.WorkGroupId = None
        self.WorkGroupName = None
        self.Type = None
        self.UserInfo = None
        self.DataPolicyInfo = None
        self.EnginePolicyInfo = None
        self.WorkGroupDescription = None
        self.RowFilterInfo = None


    def _deserialize(self, params):
        self.WorkGroupId = params.get("WorkGroupId")
        self.WorkGroupName = params.get("WorkGroupName")
        self.Type = params.get("Type")
        if params.get("UserInfo") is not None:
            self.UserInfo = Users()
            self.UserInfo._deserialize(params.get("UserInfo"))
        if params.get("DataPolicyInfo") is not None:
            self.DataPolicyInfo = Policys()
            self.DataPolicyInfo._deserialize(params.get("DataPolicyInfo"))
        if params.get("EnginePolicyInfo") is not None:
            self.EnginePolicyInfo = Policys()
            self.EnginePolicyInfo._deserialize(params.get("EnginePolicyInfo"))
        self.WorkGroupDescription = params.get("WorkGroupDescription")
        if params.get("RowFilterInfo") is not None:
            self.RowFilterInfo = Policys()
            self.RowFilterInfo._deserialize(params.get("RowFilterInfo"))
        memeber_set = set(params.keys())
        for name, value in vars(self).items():
            if name in memeber_set:
                memeber_set.remove(name)
        if len(memeber_set) > 0:
            warnings.warn("%s fileds are useless." % ",".join(memeber_set))
        


class WorkGroupIdSetOfUserId(AbstractModel):
    """同一个用户绑定的工作组集合

    """

    def __init__(self):
        r"""
        :param UserId: 用户Id，和CAM侧Uin匹配
        :type UserId: str
        :param WorkGroupIds: 工作组Id集合
        :type WorkGroupIds: list of int
        """
        self.UserId = None
        self.WorkGroupIds = None


    def _deserialize(self, params):
        self.UserId = params.get("UserId")
        self.WorkGroupIds = params.get("WorkGroupIds")
        memeber_set = set(params.keys())
        for name, value in vars(self).items():
            if name in memeber_set:
                memeber_set.remove(name)
        if len(memeber_set) > 0:
            warnings.warn("%s fileds are useless." % ",".join(memeber_set))
        


class WorkGroupInfo(AbstractModel):
    """工作组信息

    """

    def __init__(self):
        r"""
        :param WorkGroupId: 查询到的工作组唯一Id
        :type WorkGroupId: int
        :param WorkGroupName: 工作组名称
        :type WorkGroupName: str
        :param WorkGroupDescription: 工作组描述
注意：此字段可能返回 null，表示取不到有效值。
        :type WorkGroupDescription: str
        :param UserNum: 工作组关联的用户数量
        :type UserNum: int
        :param UserSet: 工作组关联的用户集合
注意：此字段可能返回 null，表示取不到有效值。
        :type UserSet: list of UserMessage
        :param PolicySet: 工作组绑定的权限集合
注意：此字段可能返回 null，表示取不到有效值。
        :type PolicySet: list of Policy
        :param Creator: 工作组的创建人
        :type Creator: str
        :param CreateTime: 工作组的创建时间，形如2021-07-28 16:19:32
        :type CreateTime: str
        """
        self.WorkGroupId = None
        self.WorkGroupName = None
        self.WorkGroupDescription = None
        self.UserNum = None
        self.UserSet = None
        self.PolicySet = None
        self.Creator = None
        self.CreateTime = None


    def _deserialize(self, params):
        self.WorkGroupId = params.get("WorkGroupId")
        self.WorkGroupName = params.get("WorkGroupName")
        self.WorkGroupDescription = params.get("WorkGroupDescription")
        self.UserNum = params.get("UserNum")
        if params.get("UserSet") is not None:
            self.UserSet = []
            for item in params.get("UserSet"):
                obj = UserMessage()
                obj._deserialize(item)
                self.UserSet.append(obj)
        if params.get("PolicySet") is not None:
            self.PolicySet = []
            for item in params.get("PolicySet"):
                obj = Policy()
                obj._deserialize(item)
                self.PolicySet.append(obj)
        self.Creator = params.get("Creator")
        self.CreateTime = params.get("CreateTime")
        memeber_set = set(params.keys())
        for name, value in vars(self).items():
            if name in memeber_set:
                memeber_set.remove(name)
        if len(memeber_set) > 0:
            warnings.warn("%s fileds are useless." % ",".join(memeber_set))
        


class WorkGroupMessage(AbstractModel):
    """工作组部分信息

    """

    def __init__(self):
        r"""
        :param WorkGroupId: 工作组唯一Id
        :type WorkGroupId: int
        :param WorkGroupName: 工作组名称
        :type WorkGroupName: str
        :param WorkGroupDescription: 工作组描述
注意：此字段可能返回 null，表示取不到有效值。
        :type WorkGroupDescription: str
        :param Creator: 创建者
        :type Creator: str
        :param CreateTime: 工作组创建的时间，形如2021-07-28 16:19:32
        :type CreateTime: str
        """
        self.WorkGroupId = None
        self.WorkGroupName = None
        self.WorkGroupDescription = None
        self.Creator = None
        self.CreateTime = None


    def _deserialize(self, params):
        self.WorkGroupId = params.get("WorkGroupId")
        self.WorkGroupName = params.get("WorkGroupName")
        self.WorkGroupDescription = params.get("WorkGroupDescription")
        self.Creator = params.get("Creator")
        self.CreateTime = params.get("CreateTime")
        memeber_set = set(params.keys())
        for name, value in vars(self).items():
            if name in memeber_set:
                memeber_set.remove(name)
        if len(memeber_set) > 0:
            warnings.warn("%s fileds are useless." % ",".join(memeber_set))
        


class WorkGroups(AbstractModel):
    """工作组集合

    """

    def __init__(self):
        r"""
        :param WorkGroupSet: 工作组信息集合
注意：此字段可能返回 null，表示取不到有效值。
        :type WorkGroupSet: list of WorkGroupMessage
        :param TotalCount: 工作组总数
注意：此字段可能返回 null，表示取不到有效值。
        :type TotalCount: int
        """
        self.WorkGroupSet = None
        self.TotalCount = None


    def _deserialize(self, params):
        if params.get("WorkGroupSet") is not None:
            self.WorkGroupSet = []
            for item in params.get("WorkGroupSet"):
                obj = WorkGroupMessage()
                obj._deserialize(item)
                self.WorkGroupSet.append(obj)
        self.TotalCount = params.get("TotalCount")
        memeber_set = set(params.keys())
        for name, value in vars(self).items():
            if name in memeber_set:
                memeber_set.remove(name)
        if len(memeber_set) > 0:
            warnings.warn("%s fileds are useless." % ",".join(memeber_set))
        


class WorkflowInfo(AbstractModel):
    """调度计划数据

    """

    def __init__(self):
        r"""
        :param WorkflowId: 调度计划ID
        :type WorkflowId: str
        :param WorkflowName: 调度计划名称
        :type WorkflowName: str
        :param WorkflowDesc: 调度计划描述
注意：此字段可能返回 null，表示取不到有效值。
        :type WorkflowDesc: str
        :param CreateTime: 创建时间
        :type CreateTime: str
        :param CycleType: 调度周期类型，分钟(MINUTE_CYCLE)，小时(HOUR_CYCLE)，天(DAY_CYCLE)，周(WEEK_CYCLE),月(MONTH_CYCLE)，一次性(ONEOFF_CYCLE)
        :type CycleType: str
        :param CycleStep: 任务调度周期间隔
        :type CycleStep: int
        :param DelayTime: 调度任务延迟时间，从调度周期开始时间计算的分钟数
        :type DelayTime: int
        :param TaskAction: 在指定周期的第n个单位时间运行（周和月任务使用），比如周任务周日运行：TaskAction=1；周一运行：TaskAction=2，月任务当月第1天运行：TaskAction=1，等
        :type TaskAction: str
        :param StartTime: 调度计划开始时间
        :type StartTime: str
        :param EndTime: 调度计划结束时间
        :type EndTime: str
        :param OwnersUin: 责任人uin
注意：此字段可能返回 null，表示取不到有效值。
        :type OwnersUin: list of str
        """
        self.WorkflowId = None
        self.WorkflowName = None
        self.WorkflowDesc = None
        self.CreateTime = None
        self.CycleType = None
        self.CycleStep = None
        self.DelayTime = None
        self.TaskAction = None
        self.StartTime = None
        self.EndTime = None
        self.OwnersUin = None


    def _deserialize(self, params):
        self.WorkflowId = params.get("WorkflowId")
        self.WorkflowName = params.get("WorkflowName")
        self.WorkflowDesc = params.get("WorkflowDesc")
        self.CreateTime = params.get("CreateTime")
        self.CycleType = params.get("CycleType")
        self.CycleStep = params.get("CycleStep")
        self.DelayTime = params.get("DelayTime")
        self.TaskAction = params.get("TaskAction")
        self.StartTime = params.get("StartTime")
        self.EndTime = params.get("EndTime")
        self.OwnersUin = params.get("OwnersUin")
        memeber_set = set(params.keys())
        for name, value in vars(self).items():
            if name in memeber_set:
                memeber_set.remove(name)
        if len(memeber_set) > 0:
            warnings.warn("%s fileds are useless." % ",".join(memeber_set))
        


class WorkloadStat(AbstractModel):
    """工作负载统计信息

    """

    def __init__(self):
        r"""
        :param StatStartTime: 统计开始时间，yyyy-MM-dd HH:mm:ss
        :type StatStartTime: str
        :param StatEndTime: 统计结束时间，yyyy-MM-dd HH:mm:ss
        :type StatEndTime: str
        :param StatType: 统计类型，5min,hour,day
        :type StatType: str
        :param DataEngineId: 数据引擎ID
        :type DataEngineId: str
        :param ClusterType: 数据引擎集群类型
        :type ClusterType: str
        :param TasksUsedTime: 当前统计时间周期内，任务执行耗时，单位：毫秒
        :type TasksUsedTime: int
        :param CUUsedTime: 当前统计时间段，数据引擎使用的CU时，CU为计算单元，1个计算 CU 约等于1核 CPU +4G 内存
        :type CUUsedTime: float
        :param DataScanVolume: 当前统计时间段，任务数据扫描量，单位：B
        :type DataScanVolume: int
        """
        self.StatStartTime = None
        self.StatEndTime = None
        self.StatType = None
        self.DataEngineId = None
        self.ClusterType = None
        self.TasksUsedTime = None
        self.CUUsedTime = None
        self.DataScanVolume = None


    def _deserialize(self, params):
        self.StatStartTime = params.get("StatStartTime")
        self.StatEndTime = params.get("StatEndTime")
        self.StatType = params.get("StatType")
        self.DataEngineId = params.get("DataEngineId")
        self.ClusterType = params.get("ClusterType")
        self.TasksUsedTime = params.get("TasksUsedTime")
        self.CUUsedTime = params.get("CUUsedTime")
        self.DataScanVolume = params.get("DataScanVolume")
        memeber_set = set(params.keys())
        for name, value in vars(self).items():
            if name in memeber_set:
                memeber_set.remove(name)
        if len(memeber_set) > 0:
            warnings.warn("%s fileds are useless." % ",".join(memeber_set))
        