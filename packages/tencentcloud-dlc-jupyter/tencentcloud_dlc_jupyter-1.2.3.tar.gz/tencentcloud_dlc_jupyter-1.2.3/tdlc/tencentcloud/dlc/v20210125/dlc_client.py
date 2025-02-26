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

import json

from tdlc.tencentcloud.common.exception.tencent_cloud_sdk_exception import TencentCloudSDKException
from tdlc.tencentcloud.common.abstract_client import AbstractClient
from tdlc.tencentcloud.dlc.v20210125 import models


class DlcClient(AbstractClient):
    _apiVersion = '2021-01-25'
    _endpoint = 'dlc.tencentcloudapi.com'
    _service = 'dlc'


    def AddColumnAfter(self, request):
        """在某列后新增列

        :param request: Request instance for AddColumnAfter.
        :type request: :class:`tencentcloud.dlc.v20210125.models.AddColumnAfterRequest`
        :rtype: :class:`tencentcloud.dlc.v20210125.models.AddColumnAfterResponse`

        """
        try:
            params = request._serialize()
            headers = request.headers
            body = self.call("AddColumnAfter", params, headers=headers)
            response = json.loads(body)
            model = models.AddColumnAfterResponse()
            model._deserialize(response["Response"])
            return model
        except Exception as e:
            if isinstance(e, TencentCloudSDKException):
                raise
            else:
                raise TencentCloudSDKException(e.message, e.message)


    def AddColumns(self, request):
        """新增字段

        :param request: Request instance for AddColumns.
        :type request: :class:`tencentcloud.dlc.v20210125.models.AddColumnsRequest`
        :rtype: :class:`tencentcloud.dlc.v20210125.models.AddColumnsResponse`

        """
        try:
            params = request._serialize()
            headers = request.headers
            body = self.call("AddColumns", params, headers=headers)
            response = json.loads(body)
            model = models.AddColumnsResponse()
            model._deserialize(response["Response"])
            return model
        except Exception as e:
            if isinstance(e, TencentCloudSDKException):
                raise
            else:
                raise TencentCloudSDKException(e.message, e.message)


    def AddDMSPartitions(self, request):
        """DMS元数据新增分区

        :param request: Request instance for AddDMSPartitions.
        :type request: :class:`tencentcloud.dlc.v20210125.models.AddDMSPartitionsRequest`
        :rtype: :class:`tencentcloud.dlc.v20210125.models.AddDMSPartitionsResponse`

        """
        try:
            params = request._serialize()
            headers = request.headers
            body = self.call("AddDMSPartitions", params, headers=headers)
            response = json.loads(body)
            model = models.AddDMSPartitionsResponse()
            model._deserialize(response["Response"])
            return model
        except Exception as e:
            if isinstance(e, TencentCloudSDKException):
                raise
            else:
                raise TencentCloudSDKException(e.message, e.message)


    def AddLakeFsChdfsBinding(self, request):
        """本接口（AddLakeFsChdfsBinding）用于添加chdfs权限组

        :param request: Request instance for AddLakeFsChdfsBinding.
        :type request: :class:`tencentcloud.dlc.v20210125.models.AddLakeFsChdfsBindingRequest`
        :rtype: :class:`tencentcloud.dlc.v20210125.models.AddLakeFsChdfsBindingResponse`

        """
        try:
            params = request._serialize()
            headers = request.headers
            body = self.call("AddLakeFsChdfsBinding", params, headers=headers)
            response = json.loads(body)
            model = models.AddLakeFsChdfsBindingResponse()
            model._deserialize(response["Response"])
            return model
        except Exception as e:
            if isinstance(e, TencentCloudSDKException):
                raise
            else:
                raise TencentCloudSDKException(e.message, e.message)


    def AddPartitionField(self, request):
        """该接口(AddPartitionField)用于新增分区字段

        :param request: Request instance for AddPartitionField.
        :type request: :class:`tencentcloud.dlc.v20210125.models.AddPartitionFieldRequest`
        :rtype: :class:`tencentcloud.dlc.v20210125.models.AddPartitionFieldResponse`

        """
        try:
            params = request._serialize()
            headers = request.headers
            body = self.call("AddPartitionField", params, headers=headers)
            response = json.loads(body)
            model = models.AddPartitionFieldResponse()
            model._deserialize(response["Response"])
            return model
        except Exception as e:
            if isinstance(e, TencentCloudSDKException):
                raise
            else:
                raise TencentCloudSDKException(e.message, e.message)


    def AddSparkImage(self, request):
        """添加Spark Image信息

        :param request: Request instance for AddSparkImage.
        :type request: :class:`tencentcloud.dlc.v20210125.models.AddSparkImageRequest`
        :rtype: :class:`tencentcloud.dlc.v20210125.models.AddSparkImageResponse`

        """
        try:
            params = request._serialize()
            headers = request.headers
            body = self.call("AddSparkImage", params, headers=headers)
            response = json.loads(body)
            model = models.AddSparkImageResponse()
            model._deserialize(response["Response"])
            return model
        except Exception as e:
            if isinstance(e, TencentCloudSDKException):
                raise
            else:
                raise TencentCloudSDKException(e.message, e.message)


    def AddSparkImageUserRecords(self, request):
        """该接口（AddSparkImageUserRecords）为用户添加私有镜像

        :param request: Request instance for AddSparkImageUserRecords.
        :type request: :class:`tencentcloud.dlc.v20210125.models.AddSparkImageUserRecordsRequest`
        :rtype: :class:`tencentcloud.dlc.v20210125.models.AddSparkImageUserRecordsResponse`

        """
        try:
            params = request._serialize()
            headers = request.headers
            body = self.call("AddSparkImageUserRecords", params, headers=headers)
            response = json.loads(body)
            model = models.AddSparkImageUserRecordsResponse()
            model._deserialize(response["Response"])
            return model
        except Exception as e:
            if isinstance(e, TencentCloudSDKException):
                raise
            else:
                raise TencentCloudSDKException(e.message, e.message)


    def AddTasks(self, request):
        """添加任务到调度计划

        :param request: Request instance for AddTasks.
        :type request: :class:`tencentcloud.dlc.v20210125.models.AddTasksRequest`
        :rtype: :class:`tencentcloud.dlc.v20210125.models.AddTasksResponse`

        """
        try:
            params = request._serialize()
            headers = request.headers
            body = self.call("AddTasks", params, headers=headers)
            response = json.loads(body)
            model = models.AddTasksResponse()
            model._deserialize(response["Response"])
            return model
        except Exception as e:
            if isinstance(e, TencentCloudSDKException):
                raise
            else:
                raise TencentCloudSDKException(e.message, e.message)


    def AddUsersToWorkGroup(self, request):
        """添加用户到工作组

        :param request: Request instance for AddUsersToWorkGroup.
        :type request: :class:`tencentcloud.dlc.v20210125.models.AddUsersToWorkGroupRequest`
        :rtype: :class:`tencentcloud.dlc.v20210125.models.AddUsersToWorkGroupResponse`

        """
        try:
            params = request._serialize()
            headers = request.headers
            body = self.call("AddUsersToWorkGroup", params, headers=headers)
            response = json.loads(body)
            model = models.AddUsersToWorkGroupResponse()
            model._deserialize(response["Response"])
            return model
        except Exception as e:
            if isinstance(e, TencentCloudSDKException):
                raise
            else:
                raise TencentCloudSDKException(e.message, e.message)


    def AddWhiteStrategy(self, request):
        """添加白名单策略

        :param request: Request instance for AddWhiteStrategy.
        :type request: :class:`tencentcloud.dlc.v20210125.models.AddWhiteStrategyRequest`
        :rtype: :class:`tencentcloud.dlc.v20210125.models.AddWhiteStrategyResponse`

        """
        try:
            params = request._serialize()
            headers = request.headers
            body = self.call("AddWhiteStrategy", params, headers=headers)
            response = json.loads(body)
            model = models.AddWhiteStrategyResponse()
            model._deserialize(response["Response"])
            return model
        except Exception as e:
            if isinstance(e, TencentCloudSDKException):
                raise
            else:
                raise TencentCloudSDKException(e.message, e.message)


    def AlterDMSDatabase(self, request):
        """DMS元数据更新库

        :param request: Request instance for AlterDMSDatabase.
        :type request: :class:`tencentcloud.dlc.v20210125.models.AlterDMSDatabaseRequest`
        :rtype: :class:`tencentcloud.dlc.v20210125.models.AlterDMSDatabaseResponse`

        """
        try:
            params = request._serialize()
            headers = request.headers
            body = self.call("AlterDMSDatabase", params, headers=headers)
            response = json.loads(body)
            model = models.AlterDMSDatabaseResponse()
            model._deserialize(response["Response"])
            return model
        except Exception as e:
            if isinstance(e, TencentCloudSDKException):
                raise
            else:
                raise TencentCloudSDKException(e.message, e.message)


    def AlterDMSPartition(self, request):
        """DMS元数据更新分区

        :param request: Request instance for AlterDMSPartition.
        :type request: :class:`tencentcloud.dlc.v20210125.models.AlterDMSPartitionRequest`
        :rtype: :class:`tencentcloud.dlc.v20210125.models.AlterDMSPartitionResponse`

        """
        try:
            params = request._serialize()
            headers = request.headers
            body = self.call("AlterDMSPartition", params, headers=headers)
            response = json.loads(body)
            model = models.AlterDMSPartitionResponse()
            model._deserialize(response["Response"])
            return model
        except Exception as e:
            if isinstance(e, TencentCloudSDKException):
                raise
            else:
                raise TencentCloudSDKException(e.message, e.message)


    def AlterDMSPartitionColumnStatistic(self, request):
        """该接口（AlterDMSPartitionColumnStatistic）用于DMS修改分区字段统计信息

        :param request: Request instance for AlterDMSPartitionColumnStatistic.
        :type request: :class:`tencentcloud.dlc.v20210125.models.AlterDMSPartitionColumnStatisticRequest`
        :rtype: :class:`tencentcloud.dlc.v20210125.models.AlterDMSPartitionColumnStatisticResponse`

        """
        try:
            params = request._serialize()
            headers = request.headers
            body = self.call("AlterDMSPartitionColumnStatistic", params, headers=headers)
            response = json.loads(body)
            model = models.AlterDMSPartitionColumnStatisticResponse()
            model._deserialize(response["Response"])
            return model
        except Exception as e:
            if isinstance(e, TencentCloudSDKException):
                raise
            else:
                raise TencentCloudSDKException(e.message, e.message)


    def AlterDMSTable(self, request):
        """DMS元数据更新表

        :param request: Request instance for AlterDMSTable.
        :type request: :class:`tencentcloud.dlc.v20210125.models.AlterDMSTableRequest`
        :rtype: :class:`tencentcloud.dlc.v20210125.models.AlterDMSTableResponse`

        """
        try:
            params = request._serialize()
            headers = request.headers
            body = self.call("AlterDMSTable", params, headers=headers)
            response = json.loads(body)
            model = models.AlterDMSTableResponse()
            model._deserialize(response["Response"])
            return model
        except Exception as e:
            if isinstance(e, TencentCloudSDKException):
                raise
            else:
                raise TencentCloudSDKException(e.message, e.message)


    def AlterDMSTableColumnStatistic(self, request):
        """该接口（AlterDMSTableColumnStatistic）用于DMS修改表字段统计信息

        :param request: Request instance for AlterDMSTableColumnStatistic.
        :type request: :class:`tencentcloud.dlc.v20210125.models.AlterDMSTableColumnStatisticRequest`
        :rtype: :class:`tencentcloud.dlc.v20210125.models.AlterDMSTableColumnStatisticResponse`

        """
        try:
            params = request._serialize()
            headers = request.headers
            body = self.call("AlterDMSTableColumnStatistic", params, headers=headers)
            response = json.loads(body)
            model = models.AlterDMSTableColumnStatisticResponse()
            model._deserialize(response["Response"])
            return model
        except Exception as e:
            if isinstance(e, TencentCloudSDKException):
                raise
            else:
                raise TencentCloudSDKException(e.message, e.message)


    def AlterMetaKeyConstraint(self, request):
        """更新元数据约束

        :param request: Request instance for AlterMetaKeyConstraint.
        :type request: :class:`tencentcloud.dlc.v20210125.models.AlterMetaKeyConstraintRequest`
        :rtype: :class:`tencentcloud.dlc.v20210125.models.AlterMetaKeyConstraintResponse`

        """
        try:
            params = request._serialize()
            headers = request.headers
            body = self.call("AlterMetaKeyConstraint", params, headers=headers)
            response = json.loads(body)
            model = models.AlterMetaKeyConstraintResponse()
            model._deserialize(response["Response"])
            return model
        except Exception as e:
            if isinstance(e, TencentCloudSDKException):
                raise
            else:
                raise TencentCloudSDKException(e.message, e.message)


    def AlterTableColumns(self, request):
        """【数据管理】修改表字段

        :param request: Request instance for AlterTableColumns.
        :type request: :class:`tencentcloud.dlc.v20210125.models.AlterTableColumnsRequest`
        :rtype: :class:`tencentcloud.dlc.v20210125.models.AlterTableColumnsResponse`

        """
        try:
            params = request._serialize()
            headers = request.headers
            body = self.call("AlterTableColumns", params, headers=headers)
            response = json.loads(body)
            model = models.AlterTableColumnsResponse()
            model._deserialize(response["Response"])
            return model
        except Exception as e:
            if isinstance(e, TencentCloudSDKException):
                raise
            else:
                raise TencentCloudSDKException(e.message, e.message)


    def AlterTableComment(self, request):
        """修改表备注

        :param request: Request instance for AlterTableComment.
        :type request: :class:`tencentcloud.dlc.v20210125.models.AlterTableCommentRequest`
        :rtype: :class:`tencentcloud.dlc.v20210125.models.AlterTableCommentResponse`

        """
        try:
            params = request._serialize()
            headers = request.headers
            body = self.call("AlterTableComment", params, headers=headers)
            response = json.loads(body)
            model = models.AlterTableCommentResponse()
            model._deserialize(response["Response"])
            return model
        except Exception as e:
            if isinstance(e, TencentCloudSDKException):
                raise
            else:
                raise TencentCloudSDKException(e.message, e.message)


    def AlterTableProperties(self, request):
        """修改表属性信息

        :param request: Request instance for AlterTableProperties.
        :type request: :class:`tencentcloud.dlc.v20210125.models.AlterTablePropertiesRequest`
        :rtype: :class:`tencentcloud.dlc.v20210125.models.AlterTablePropertiesResponse`

        """
        try:
            params = request._serialize()
            headers = request.headers
            body = self.call("AlterTableProperties", params, headers=headers)
            response = json.loads(body)
            model = models.AlterTablePropertiesResponse()
            model._deserialize(response["Response"])
            return model
        except Exception as e:
            if isinstance(e, TencentCloudSDKException):
                raise
            else:
                raise TencentCloudSDKException(e.message, e.message)


    def AssociateCHDFSAccessGroups(self, request):
        """绑定CHDFS挂载点

        :param request: Request instance for AssociateCHDFSAccessGroups.
        :type request: :class:`tencentcloud.dlc.v20210125.models.AssociateCHDFSAccessGroupsRequest`
        :rtype: :class:`tencentcloud.dlc.v20210125.models.AssociateCHDFSAccessGroupsResponse`

        """
        try:
            params = request._serialize()
            headers = request.headers
            body = self.call("AssociateCHDFSAccessGroups", params, headers=headers)
            response = json.loads(body)
            model = models.AssociateCHDFSAccessGroupsResponse()
            model._deserialize(response["Response"])
            return model
        except Exception as e:
            if isinstance(e, TencentCloudSDKException):
                raise
            else:
                raise TencentCloudSDKException(e.message, e.message)


    def AssociateDatasourceHouse(self, request):
        """绑定数据源和队列

        :param request: Request instance for AssociateDatasourceHouse.
        :type request: :class:`tencentcloud.dlc.v20210125.models.AssociateDatasourceHouseRequest`
        :rtype: :class:`tencentcloud.dlc.v20210125.models.AssociateDatasourceHouseResponse`

        """
        try:
            params = request._serialize()
            headers = request.headers
            body = self.call("AssociateDatasourceHouse", params, headers=headers)
            response = json.loads(body)
            model = models.AssociateDatasourceHouseResponse()
            model._deserialize(response["Response"])
            return model
        except Exception as e:
            if isinstance(e, TencentCloudSDKException):
                raise
            else:
                raise TencentCloudSDKException(e.message, e.message)


    def AttachUserPolicy(self, request):
        """绑定鉴权策略到用户

        :param request: Request instance for AttachUserPolicy.
        :type request: :class:`tencentcloud.dlc.v20210125.models.AttachUserPolicyRequest`
        :rtype: :class:`tencentcloud.dlc.v20210125.models.AttachUserPolicyResponse`

        """
        try:
            params = request._serialize()
            headers = request.headers
            body = self.call("AttachUserPolicy", params, headers=headers)
            response = json.loads(body)
            model = models.AttachUserPolicyResponse()
            model._deserialize(response["Response"])
            return model
        except Exception as e:
            if isinstance(e, TencentCloudSDKException):
                raise
            else:
                raise TencentCloudSDKException(e.message, e.message)


    def AttachWorkGroupPolicy(self, request):
        """绑定鉴权策略到工作组

        :param request: Request instance for AttachWorkGroupPolicy.
        :type request: :class:`tencentcloud.dlc.v20210125.models.AttachWorkGroupPolicyRequest`
        :rtype: :class:`tencentcloud.dlc.v20210125.models.AttachWorkGroupPolicyResponse`

        """
        try:
            params = request._serialize()
            headers = request.headers
            body = self.call("AttachWorkGroupPolicy", params, headers=headers)
            response = json.loads(body)
            model = models.AttachWorkGroupPolicyResponse()
            model._deserialize(response["Response"])
            return model
        except Exception as e:
            if isinstance(e, TencentCloudSDKException):
                raise
            else:
                raise TencentCloudSDKException(e.message, e.message)


    def BindDefaultSharedEngine(self, request):
        """绑定默认共享集群

        :param request: Request instance for BindDefaultSharedEngine.
        :type request: :class:`tencentcloud.dlc.v20210125.models.BindDefaultSharedEngineRequest`
        :rtype: :class:`tencentcloud.dlc.v20210125.models.BindDefaultSharedEngineResponse`

        """
        try:
            params = request._serialize()
            headers = request.headers
            body = self.call("BindDefaultSharedEngine", params, headers=headers)
            response = json.loads(body)
            model = models.BindDefaultSharedEngineResponse()
            model._deserialize(response["Response"])
            return model
        except Exception as e:
            if isinstance(e, TencentCloudSDKException):
                raise
            else:
                raise TencentCloudSDKException(e.message, e.message)


    def BindTagsToDataEngines(self, request):
        """绑定标签到数据引擎（内部接口，dryRun场景使用，未对外开放使用。开放前请评估！！！）

        :param request: Request instance for BindTagsToDataEngines.
        :type request: :class:`tencentcloud.dlc.v20210125.models.BindTagsToDataEnginesRequest`
        :rtype: :class:`tencentcloud.dlc.v20210125.models.BindTagsToDataEnginesResponse`

        """
        try:
            params = request._serialize()
            headers = request.headers
            body = self.call("BindTagsToDataEngines", params, headers=headers)
            response = json.loads(body)
            model = models.BindTagsToDataEnginesResponse()
            model._deserialize(response["Response"])
            return model
        except Exception as e:
            if isinstance(e, TencentCloudSDKException):
                raise
            else:
                raise TencentCloudSDKException(e.message, e.message)


    def BindWorkGroupsToUser(self, request):
        """绑定工作组到用户

        :param request: Request instance for BindWorkGroupsToUser.
        :type request: :class:`tencentcloud.dlc.v20210125.models.BindWorkGroupsToUserRequest`
        :rtype: :class:`tencentcloud.dlc.v20210125.models.BindWorkGroupsToUserResponse`

        """
        try:
            params = request._serialize()
            headers = request.headers
            body = self.call("BindWorkGroupsToUser", params, headers=headers)
            response = json.loads(body)
            model = models.BindWorkGroupsToUserResponse()
            model._deserialize(response["Response"])
            return model
        except Exception as e:
            if isinstance(e, TencentCloudSDKException):
                raise
            else:
                raise TencentCloudSDKException(e.message, e.message)


    def CancelNotebookSessionStatement(self, request):
        """本接口（CancelNotebookSessionStatement）用于取消session中执行的任务

        :param request: Request instance for CancelNotebookSessionStatement.
        :type request: :class:`tencentcloud.dlc.v20210125.models.CancelNotebookSessionStatementRequest`
        :rtype: :class:`tencentcloud.dlc.v20210125.models.CancelNotebookSessionStatementResponse`

        """
        try:
            params = request._serialize()
            headers = request.headers
            body = self.call("CancelNotebookSessionStatement", params, headers=headers)
            response = json.loads(body)
            model = models.CancelNotebookSessionStatementResponse()
            model._deserialize(response["Response"])
            return model
        except Exception as e:
            if isinstance(e, TencentCloudSDKException):
                raise
            else:
                raise TencentCloudSDKException(e.message, e.message)


    def CancelNotebookSessionStatementBatch(self, request):
        """本接口（CancelNotebookSessionStatementBatch）用于批量取消Session 中执行的任务

        :param request: Request instance for CancelNotebookSessionStatementBatch.
        :type request: :class:`tencentcloud.dlc.v20210125.models.CancelNotebookSessionStatementBatchRequest`
        :rtype: :class:`tencentcloud.dlc.v20210125.models.CancelNotebookSessionStatementBatchResponse`

        """
        try:
            params = request._serialize()
            headers = request.headers
            body = self.call("CancelNotebookSessionStatementBatch", params, headers=headers)
            response = json.loads(body)
            model = models.CancelNotebookSessionStatementBatchResponse()
            model._deserialize(response["Response"])
            return model
        except Exception as e:
            if isinstance(e, TencentCloudSDKException):
                raise
            else:
                raise TencentCloudSDKException(e.message, e.message)


    def CancelSparkSessionBatchSQL(self, request):
        """本接口（CancelSparkSessionBatchSQL）用于取消Spark SQL批任务。

        :param request: Request instance for CancelSparkSessionBatchSQL.
        :type request: :class:`tencentcloud.dlc.v20210125.models.CancelSparkSessionBatchSQLRequest`
        :rtype: :class:`tencentcloud.dlc.v20210125.models.CancelSparkSessionBatchSQLResponse`

        """
        try:
            params = request._serialize()
            headers = request.headers
            body = self.call("CancelSparkSessionBatchSQL", params, headers=headers)
            response = json.loads(body)
            model = models.CancelSparkSessionBatchSQLResponse()
            model._deserialize(response["Response"])
            return model
        except Exception as e:
            if isinstance(e, TencentCloudSDKException):
                raise
            else:
                raise TencentCloudSDKException(e.message, e.message)


    def CancelTableProperties(self, request):
        """本接口（CancelTableProperties）用于删除表属性

        :param request: Request instance for CancelTableProperties.
        :type request: :class:`tencentcloud.dlc.v20210125.models.CancelTablePropertiesRequest`
        :rtype: :class:`tencentcloud.dlc.v20210125.models.CancelTablePropertiesResponse`

        """
        try:
            params = request._serialize()
            headers = request.headers
            body = self.call("CancelTableProperties", params, headers=headers)
            response = json.loads(body)
            model = models.CancelTablePropertiesResponse()
            model._deserialize(response["Response"])
            return model
        except Exception as e:
            if isinstance(e, TencentCloudSDKException):
                raise
            else:
                raise TencentCloudSDKException(e.message, e.message)


    def CancelTask(self, request):
        """本接口（CancelTask），用于取消任务

        :param request: Request instance for CancelTask.
        :type request: :class:`tencentcloud.dlc.v20210125.models.CancelTaskRequest`
        :rtype: :class:`tencentcloud.dlc.v20210125.models.CancelTaskResponse`

        """
        try:
            params = request._serialize()
            headers = request.headers
            body = self.call("CancelTask", params, headers=headers)
            response = json.loads(body)
            model = models.CancelTaskResponse()
            model._deserialize(response["Response"])
            return model
        except Exception as e:
            if isinstance(e, TencentCloudSDKException):
                raise
            else:
                raise TencentCloudSDKException(e.message, e.message)


    def CancelTasks(self, request):
        """批量取消任务

        :param request: Request instance for CancelTasks.
        :type request: :class:`tencentcloud.dlc.v20210125.models.CancelTasksRequest`
        :rtype: :class:`tencentcloud.dlc.v20210125.models.CancelTasksResponse`

        """
        try:
            params = request._serialize()
            headers = request.headers
            body = self.call("CancelTasks", params, headers=headers)
            response = json.loads(body)
            model = models.CancelTasksResponse()
            model._deserialize(response["Response"])
            return model
        except Exception as e:
            if isinstance(e, TencentCloudSDKException):
                raise
            else:
                raise TencentCloudSDKException(e.message, e.message)


    def ChangeColumn(self, request):
        """修改字段

        :param request: Request instance for ChangeColumn.
        :type request: :class:`tencentcloud.dlc.v20210125.models.ChangeColumnRequest`
        :rtype: :class:`tencentcloud.dlc.v20210125.models.ChangeColumnResponse`

        """
        try:
            params = request._serialize()
            headers = request.headers
            body = self.call("ChangeColumn", params, headers=headers)
            response = json.loads(body)
            model = models.ChangeColumnResponse()
            model._deserialize(response["Response"])
            return model
        except Exception as e:
            if isinstance(e, TencentCloudSDKException):
                raise
            else:
                raise TencentCloudSDKException(e.message, e.message)


    def CheckDLCResourceRole(self, request):
        """该接口（CheckDlcRole）判断用户是否为DLC服务角色授权。

        :param request: Request instance for CheckDLCResourceRole.
        :type request: :class:`tencentcloud.dlc.v20210125.models.CheckDLCResourceRoleRequest`
        :rtype: :class:`tencentcloud.dlc.v20210125.models.CheckDLCResourceRoleResponse`

        """
        try:
            params = request._serialize()
            headers = request.headers
            body = self.call("CheckDLCResourceRole", params, headers=headers)
            response = json.loads(body)
            model = models.CheckDLCResourceRoleResponse()
            model._deserialize(response["Response"])
            return model
        except Exception as e:
            if isinstance(e, TencentCloudSDKException):
                raise
            else:
                raise TencentCloudSDKException(e.message, e.message)


    def CheckDataEngineConfigPairsValidity(self, request):
        """本接口（CheckDataEngineConfigPairsValidity）用于检查引擎用户自定义参数的有效性

        :param request: Request instance for CheckDataEngineConfigPairsValidity.
        :type request: :class:`tencentcloud.dlc.v20210125.models.CheckDataEngineConfigPairsValidityRequest`
        :rtype: :class:`tencentcloud.dlc.v20210125.models.CheckDataEngineConfigPairsValidityResponse`

        """
        try:
            params = request._serialize()
            headers = request.headers
            body = self.call("CheckDataEngineConfigPairsValidity", params, headers=headers)
            response = json.loads(body)
            model = models.CheckDataEngineConfigPairsValidityResponse()
            model._deserialize(response["Response"])
            return model
        except Exception as e:
            if isinstance(e, TencentCloudSDKException):
                raise
            else:
                raise TencentCloudSDKException(e.message, e.message)


    def CheckDataEngineImageCanBeRollback(self, request):
        """本接口（CheckDataEngineImageCanBeRollback）用于查看集群是否能回滚。

        :param request: Request instance for CheckDataEngineImageCanBeRollback.
        :type request: :class:`tencentcloud.dlc.v20210125.models.CheckDataEngineImageCanBeRollbackRequest`
        :rtype: :class:`tencentcloud.dlc.v20210125.models.CheckDataEngineImageCanBeRollbackResponse`

        """
        try:
            params = request._serialize()
            headers = request.headers
            body = self.call("CheckDataEngineImageCanBeRollback", params, headers=headers)
            response = json.loads(body)
            model = models.CheckDataEngineImageCanBeRollbackResponse()
            model._deserialize(response["Response"])
            return model
        except Exception as e:
            if isinstance(e, TencentCloudSDKException):
                raise
            else:
                raise TencentCloudSDKException(e.message, e.message)


    def CheckDataEngineImageCanBeUpgrade(self, request):
        """本接口（CheckDataEngineImageCanBeUpgrade）用于查看集群镜像是否能够升级。

        :param request: Request instance for CheckDataEngineImageCanBeUpgrade.
        :type request: :class:`tencentcloud.dlc.v20210125.models.CheckDataEngineImageCanBeUpgradeRequest`
        :rtype: :class:`tencentcloud.dlc.v20210125.models.CheckDataEngineImageCanBeUpgradeResponse`

        """
        try:
            params = request._serialize()
            headers = request.headers
            body = self.call("CheckDataEngineImageCanBeUpgrade", params, headers=headers)
            response = json.loads(body)
            model = models.CheckDataEngineImageCanBeUpgradeResponse()
            model._deserialize(response["Response"])
            return model
        except Exception as e:
            if isinstance(e, TencentCloudSDKException):
                raise
            else:
                raise TencentCloudSDKException(e.message, e.message)


    def CheckDatabaseExists(self, request):
        """本接口（CheckDatabaseExists）用于查询数据库是否存在。

        :param request: Request instance for CheckDatabaseExists.
        :type request: :class:`tencentcloud.dlc.v20210125.models.CheckDatabaseExistsRequest`
        :rtype: :class:`tencentcloud.dlc.v20210125.models.CheckDatabaseExistsResponse`

        """
        try:
            params = request._serialize()
            headers = request.headers
            body = self.call("CheckDatabaseExists", params, headers=headers)
            response = json.loads(body)
            model = models.CheckDatabaseExistsResponse()
            model._deserialize(response["Response"])
            return model
        except Exception as e:
            if isinstance(e, TencentCloudSDKException):
                raise
            else:
                raise TencentCloudSDKException(e.message, e.message)


    def CheckDatabaseUDFExists(self, request):
        """本接口（CheckDatabaseUDFExists）用于查询UDF是否存在。

        :param request: Request instance for CheckDatabaseUDFExists.
        :type request: :class:`tencentcloud.dlc.v20210125.models.CheckDatabaseUDFExistsRequest`
        :rtype: :class:`tencentcloud.dlc.v20210125.models.CheckDatabaseUDFExistsResponse`

        """
        try:
            params = request._serialize()
            headers = request.headers
            body = self.call("CheckDatabaseUDFExists", params, headers=headers)
            response = json.loads(body)
            model = models.CheckDatabaseUDFExistsResponse()
            model._deserialize(response["Response"])
            return model
        except Exception as e:
            if isinstance(e, TencentCloudSDKException):
                raise
            else:
                raise TencentCloudSDKException(e.message, e.message)


    def CheckDatasourceConnectivity(self, request):
        """本接口（CheckDatasourceConnectivity），用于检查数据源连通性

        :param request: Request instance for CheckDatasourceConnectivity.
        :type request: :class:`tencentcloud.dlc.v20210125.models.CheckDatasourceConnectivityRequest`
        :rtype: :class:`tencentcloud.dlc.v20210125.models.CheckDatasourceConnectivityResponse`

        """
        try:
            params = request._serialize()
            headers = request.headers
            body = self.call("CheckDatasourceConnectivity", params, headers=headers)
            response = json.loads(body)
            model = models.CheckDatasourceConnectivityResponse()
            model._deserialize(response["Response"])
            return model
        except Exception as e:
            if isinstance(e, TencentCloudSDKException):
                raise
            else:
                raise TencentCloudSDKException(e.message, e.message)


    def CheckInstanceName(self, request):
        """检查实例名称是否符合重名。DLC的引擎实例名称不区分大小写，即instance和INSTANCE会判断为重名。

        :param request: Request instance for CheckInstanceName.
        :type request: :class:`tencentcloud.dlc.v20210125.models.CheckInstanceNameRequest`
        :rtype: :class:`tencentcloud.dlc.v20210125.models.CheckInstanceNameResponse`

        """
        try:
            params = request._serialize()
            headers = request.headers
            body = self.call("CheckInstanceName", params, headers=headers)
            response = json.loads(body)
            model = models.CheckInstanceNameResponse()
            model._deserialize(response["Response"])
            return model
        except Exception as e:
            if isinstance(e, TencentCloudSDKException):
                raise
            else:
                raise TencentCloudSDKException(e.message, e.message)


    def CheckLakeFsChdfsEnable(self, request):
        """检查用户的托管存是否支持Chdfs

        :param request: Request instance for CheckLakeFsChdfsEnable.
        :type request: :class:`tencentcloud.dlc.v20210125.models.CheckLakeFsChdfsEnableRequest`
        :rtype: :class:`tencentcloud.dlc.v20210125.models.CheckLakeFsChdfsEnableResponse`

        """
        try:
            params = request._serialize()
            headers = request.headers
            body = self.call("CheckLakeFsChdfsEnable", params, headers=headers)
            response = json.loads(body)
            model = models.CheckLakeFsChdfsEnableResponse()
            model._deserialize(response["Response"])
            return model
        except Exception as e:
            if isinstance(e, TencentCloudSDKException):
                raise
            else:
                raise TencentCloudSDKException(e.message, e.message)


    def CheckLakeFsExist(self, request):
        """检查是否已经创建LakeFs

        :param request: Request instance for CheckLakeFsExist.
        :type request: :class:`tencentcloud.dlc.v20210125.models.CheckLakeFsExistRequest`
        :rtype: :class:`tencentcloud.dlc.v20210125.models.CheckLakeFsExistResponse`

        """
        try:
            params = request._serialize()
            headers = request.headers
            body = self.call("CheckLakeFsExist", params, headers=headers)
            response = json.loads(body)
            model = models.CheckLakeFsExistResponse()
            model._deserialize(response["Response"])
            return model
        except Exception as e:
            if isinstance(e, TencentCloudSDKException):
                raise
            else:
                raise TencentCloudSDKException(e.message, e.message)


    def CheckLockMetaData(self, request):
        """元数据锁检查

        :param request: Request instance for CheckLockMetaData.
        :type request: :class:`tencentcloud.dlc.v20210125.models.CheckLockMetaDataRequest`
        :rtype: :class:`tencentcloud.dlc.v20210125.models.CheckLockMetaDataResponse`

        """
        try:
            params = request._serialize()
            headers = request.headers
            body = self.call("CheckLockMetaData", params, headers=headers)
            response = json.loads(body)
            model = models.CheckLockMetaDataResponse()
            model._deserialize(response["Response"])
            return model
        except Exception as e:
            if isinstance(e, TencentCloudSDKException):
                raise
            else:
                raise TencentCloudSDKException(e.message, e.message)


    def CheckRegionCHDFSEnable(self, request):
        """此接口（CheckRegionCHDFSEnable）用于检查当前地域是否支持元数据加速桶能力

        :param request: Request instance for CheckRegionCHDFSEnable.
        :type request: :class:`tencentcloud.dlc.v20210125.models.CheckRegionCHDFSEnableRequest`
        :rtype: :class:`tencentcloud.dlc.v20210125.models.CheckRegionCHDFSEnableResponse`

        """
        try:
            params = request._serialize()
            headers = request.headers
            body = self.call("CheckRegionCHDFSEnable", params, headers=headers)
            response = json.loads(body)
            model = models.CheckRegionCHDFSEnableResponse()
            model._deserialize(response["Response"])
            return model
        except Exception as e:
            if isinstance(e, TencentCloudSDKException):
                raise
            else:
                raise TencentCloudSDKException(e.message, e.message)


    def CheckSQLSessionCatalogNameExists(self, request):
        """本接口（CheckSQLSessionCatalogNameExists）用于SQL会话重名校验

        :param request: Request instance for CheckSQLSessionCatalogNameExists.
        :type request: :class:`tencentcloud.dlc.v20210125.models.CheckSQLSessionCatalogNameExistsRequest`
        :rtype: :class:`tencentcloud.dlc.v20210125.models.CheckSQLSessionCatalogNameExistsResponse`

        """
        try:
            params = request._serialize()
            headers = request.headers
            body = self.call("CheckSQLSessionCatalogNameExists", params, headers=headers)
            response = json.loads(body)
            model = models.CheckSQLSessionCatalogNameExistsResponse()
            model._deserialize(response["Response"])
            return model
        except Exception as e:
            if isinstance(e, TencentCloudSDKException):
                raise
            else:
                raise TencentCloudSDKException(e.message, e.message)


    def CheckScheduleScriptExist(self, request):
        """检查调度脚本是否已被引用

        :param request: Request instance for CheckScheduleScriptExist.
        :type request: :class:`tencentcloud.dlc.v20210125.models.CheckScheduleScriptExistRequest`
        :rtype: :class:`tencentcloud.dlc.v20210125.models.CheckScheduleScriptExistResponse`

        """
        try:
            params = request._serialize()
            headers = request.headers
            body = self.call("CheckScheduleScriptExist", params, headers=headers)
            response = json.loads(body)
            model = models.CheckScheduleScriptExistResponse()
            model._deserialize(response["Response"])
            return model
        except Exception as e:
            if isinstance(e, TencentCloudSDKException):
                raise
            else:
                raise TencentCloudSDKException(e.message, e.message)


    def CheckScheduleTaskNameExists(self, request):
        """检查调度任务名称是否重名

        :param request: Request instance for CheckScheduleTaskNameExists.
        :type request: :class:`tencentcloud.dlc.v20210125.models.CheckScheduleTaskNameExistsRequest`
        :rtype: :class:`tencentcloud.dlc.v20210125.models.CheckScheduleTaskNameExistsResponse`

        """
        try:
            params = request._serialize()
            headers = request.headers
            body = self.call("CheckScheduleTaskNameExists", params, headers=headers)
            response = json.loads(body)
            model = models.CheckScheduleTaskNameExistsResponse()
            model._deserialize(response["Response"])
            return model
        except Exception as e:
            if isinstance(e, TencentCloudSDKException):
                raise
            else:
                raise TencentCloudSDKException(e.message, e.message)


    def CheckSparkImageExists(self, request):
        """该接口（CheckSparkImageExists）用于查看镜像是否存在。

        :param request: Request instance for CheckSparkImageExists.
        :type request: :class:`tencentcloud.dlc.v20210125.models.CheckSparkImageExistsRequest`
        :rtype: :class:`tencentcloud.dlc.v20210125.models.CheckSparkImageExistsResponse`

        """
        try:
            params = request._serialize()
            headers = request.headers
            body = self.call("CheckSparkImageExists", params, headers=headers)
            response = json.loads(body)
            model = models.CheckSparkImageExistsResponse()
            model._deserialize(response["Response"])
            return model
        except Exception as e:
            if isinstance(e, TencentCloudSDKException):
                raise
            else:
                raise TencentCloudSDKException(e.message, e.message)


    def CheckSparkImageUserRecordExists(self, request):
        """该接口（CheckSparkImageUserRecordExists）用于用户私有镜像记录查重

        :param request: Request instance for CheckSparkImageUserRecordExists.
        :type request: :class:`tencentcloud.dlc.v20210125.models.CheckSparkImageUserRecordExistsRequest`
        :rtype: :class:`tencentcloud.dlc.v20210125.models.CheckSparkImageUserRecordExistsResponse`

        """
        try:
            params = request._serialize()
            headers = request.headers
            body = self.call("CheckSparkImageUserRecordExists", params, headers=headers)
            response = json.loads(body)
            model = models.CheckSparkImageUserRecordExistsResponse()
            model._deserialize(response["Response"])
            return model
        except Exception as e:
            if isinstance(e, TencentCloudSDKException):
                raise
            else:
                raise TencentCloudSDKException(e.message, e.message)


    def CheckTableExists(self, request):
        """本接口（CheckTableExists）用于查询数据表是否存在。

        :param request: Request instance for CheckTableExists.
        :type request: :class:`tencentcloud.dlc.v20210125.models.CheckTableExistsRequest`
        :rtype: :class:`tencentcloud.dlc.v20210125.models.CheckTableExistsResponse`

        """
        try:
            params = request._serialize()
            headers = request.headers
            body = self.call("CheckTableExists", params, headers=headers)
            response = json.loads(body)
            model = models.CheckTableExistsResponse()
            model._deserialize(response["Response"])
            return model
        except Exception as e:
            if isinstance(e, TencentCloudSDKException):
                raise
            else:
                raise TencentCloudSDKException(e.message, e.message)


    def CheckViewExists(self, request):
        """本接口（CheckViewExists）用于查询视图是否存在。

        :param request: Request instance for CheckViewExists.
        :type request: :class:`tencentcloud.dlc.v20210125.models.CheckViewExistsRequest`
        :rtype: :class:`tencentcloud.dlc.v20210125.models.CheckViewExistsResponse`

        """
        try:
            params = request._serialize()
            headers = request.headers
            body = self.call("CheckViewExists", params, headers=headers)
            response = json.loads(body)
            model = models.CheckViewExistsResponse()
            model._deserialize(response["Response"])
            return model
        except Exception as e:
            if isinstance(e, TencentCloudSDKException):
                raise
            else:
                raise TencentCloudSDKException(e.message, e.message)


    def CheckVpcCidrBlock(self, request):
        """检查vpc的cidrblock是否符合要求

        :param request: Request instance for CheckVpcCidrBlock.
        :type request: :class:`tencentcloud.dlc.v20210125.models.CheckVpcCidrBlockRequest`
        :rtype: :class:`tencentcloud.dlc.v20210125.models.CheckVpcCidrBlockResponse`

        """
        try:
            params = request._serialize()
            headers = request.headers
            body = self.call("CheckVpcCidrBlock", params, headers=headers)
            response = json.loads(body)
            model = models.CheckVpcCidrBlockResponse()
            model._deserialize(response["Response"])
            return model
        except Exception as e:
            if isinstance(e, TencentCloudSDKException):
                raise
            else:
                raise TencentCloudSDKException(e.message, e.message)


    def CleanImportStorage(self, request):
        """清理导入数据的临时数据任务

        :param request: Request instance for CleanImportStorage.
        :type request: :class:`tencentcloud.dlc.v20210125.models.CleanImportStorageRequest`
        :rtype: :class:`tencentcloud.dlc.v20210125.models.CleanImportStorageResponse`

        """
        try:
            params = request._serialize()
            headers = request.headers
            body = self.call("CleanImportStorage", params, headers=headers)
            response = json.loads(body)
            model = models.CleanImportStorageResponse()
            model._deserialize(response["Response"])
            return model
        except Exception as e:
            if isinstance(e, TencentCloudSDKException):
                raise
            else:
                raise TencentCloudSDKException(e.message, e.message)


    def CloseOrOpenSQLSessionSnapshot(self, request):
        """本接口（CloseOrOpenSQLSessionSnapshot）用于关闭或打开SQL会话快照。

        :param request: Request instance for CloseOrOpenSQLSessionSnapshot.
        :type request: :class:`tencentcloud.dlc.v20210125.models.CloseOrOpenSQLSessionSnapshotRequest`
        :rtype: :class:`tencentcloud.dlc.v20210125.models.CloseOrOpenSQLSessionSnapshotResponse`

        """
        try:
            params = request._serialize()
            headers = request.headers
            body = self.call("CloseOrOpenSQLSessionSnapshot", params, headers=headers)
            response = json.loads(body)
            model = models.CloseOrOpenSQLSessionSnapshotResponse()
            model._deserialize(response["Response"])
            return model
        except Exception as e:
            if isinstance(e, TencentCloudSDKException):
                raise
            else:
                raise TencentCloudSDKException(e.message, e.message)


    def CreateAdministrator(self, request):
        """创建管理员用户

        :param request: Request instance for CreateAdministrator.
        :type request: :class:`tencentcloud.dlc.v20210125.models.CreateAdministratorRequest`
        :rtype: :class:`tencentcloud.dlc.v20210125.models.CreateAdministratorResponse`

        """
        try:
            params = request._serialize()
            headers = request.headers
            body = self.call("CreateAdministrator", params, headers=headers)
            response = json.loads(body)
            model = models.CreateAdministratorResponse()
            model._deserialize(response["Response"])
            return model
        except Exception as e:
            if isinstance(e, TencentCloudSDKException):
                raise
            else:
                raise TencentCloudSDKException(e.message, e.message)


    def CreateCHDFSBindingProduct(self, request):
        """此接口（CreateCHDFSBindingProduct）用于创建元数据加速桶和产品绑定关系

        :param request: Request instance for CreateCHDFSBindingProduct.
        :type request: :class:`tencentcloud.dlc.v20210125.models.CreateCHDFSBindingProductRequest`
        :rtype: :class:`tencentcloud.dlc.v20210125.models.CreateCHDFSBindingProductResponse`

        """
        try:
            params = request._serialize()
            headers = request.headers
            body = self.call("CreateCHDFSBindingProduct", params, headers=headers)
            response = json.loads(body)
            model = models.CreateCHDFSBindingProductResponse()
            model._deserialize(response["Response"])
            return model
        except Exception as e:
            if isinstance(e, TencentCloudSDKException):
                raise
            else:
                raise TencentCloudSDKException(e.message, e.message)


    def CreateCHDFSProduct(self, request):
        """此接口（CreateCHDFSProduct）创建元数据加速桶绑定产品

        :param request: Request instance for CreateCHDFSProduct.
        :type request: :class:`tencentcloud.dlc.v20210125.models.CreateCHDFSProductRequest`
        :rtype: :class:`tencentcloud.dlc.v20210125.models.CreateCHDFSProductResponse`

        """
        try:
            params = request._serialize()
            headers = request.headers
            body = self.call("CreateCHDFSProduct", params, headers=headers)
            response = json.loads(body)
            model = models.CreateCHDFSProductResponse()
            model._deserialize(response["Response"])
            return model
        except Exception as e:
            if isinstance(e, TencentCloudSDKException):
                raise
            else:
                raise TencentCloudSDKException(e.message, e.message)


    def CreateDMSDatabase(self, request):
        """DMS元数据创建库

        :param request: Request instance for CreateDMSDatabase.
        :type request: :class:`tencentcloud.dlc.v20210125.models.CreateDMSDatabaseRequest`
        :rtype: :class:`tencentcloud.dlc.v20210125.models.CreateDMSDatabaseResponse`

        """
        try:
            params = request._serialize()
            headers = request.headers
            body = self.call("CreateDMSDatabase", params, headers=headers)
            response = json.loads(body)
            model = models.CreateDMSDatabaseResponse()
            model._deserialize(response["Response"])
            return model
        except Exception as e:
            if isinstance(e, TencentCloudSDKException):
                raise
            else:
                raise TencentCloudSDKException(e.message, e.message)


    def CreateDMSTable(self, request):
        """DMS元数据创建表

        :param request: Request instance for CreateDMSTable.
        :type request: :class:`tencentcloud.dlc.v20210125.models.CreateDMSTableRequest`
        :rtype: :class:`tencentcloud.dlc.v20210125.models.CreateDMSTableResponse`

        """
        try:
            params = request._serialize()
            headers = request.headers
            body = self.call("CreateDMSTable", params, headers=headers)
            response = json.loads(body)
            model = models.CreateDMSTableResponse()
            model._deserialize(response["Response"])
            return model
        except Exception as e:
            if isinstance(e, TencentCloudSDKException):
                raise
            else:
                raise TencentCloudSDKException(e.message, e.message)


    def CreateDataEngine(self, request):
        """为用户创建数据引擎

        :param request: Request instance for CreateDataEngine.
        :type request: :class:`tencentcloud.dlc.v20210125.models.CreateDataEngineRequest`
        :rtype: :class:`tencentcloud.dlc.v20210125.models.CreateDataEngineResponse`

        """
        try:
            params = request._serialize()
            headers = request.headers
            body = self.call("CreateDataEngine", params, headers=headers)
            response = json.loads(body)
            model = models.CreateDataEngineResponse()
            model._deserialize(response["Response"])
            return model
        except Exception as e:
            if isinstance(e, TencentCloudSDKException):
                raise
            else:
                raise TencentCloudSDKException(e.message, e.message)


    def CreateDataQuery(self, request):
        """创建数据查询

        :param request: Request instance for CreateDataQuery.
        :type request: :class:`tencentcloud.dlc.v20210125.models.CreateDataQueryRequest`
        :rtype: :class:`tencentcloud.dlc.v20210125.models.CreateDataQueryResponse`

        """
        try:
            params = request._serialize()
            headers = request.headers
            body = self.call("CreateDataQuery", params, headers=headers)
            response = json.loads(body)
            model = models.CreateDataQueryResponse()
            model._deserialize(response["Response"])
            return model
        except Exception as e:
            if isinstance(e, TencentCloudSDKException):
                raise
            else:
                raise TencentCloudSDKException(e.message, e.message)


    def CreateDatabase(self, request):
        """本接口（CreateDatabase）用于生成建库SQL语句。

        :param request: Request instance for CreateDatabase.
        :type request: :class:`tencentcloud.dlc.v20210125.models.CreateDatabaseRequest`
        :rtype: :class:`tencentcloud.dlc.v20210125.models.CreateDatabaseResponse`

        """
        try:
            params = request._serialize()
            headers = request.headers
            body = self.call("CreateDatabase", params, headers=headers)
            response = json.loads(body)
            model = models.CreateDatabaseResponse()
            model._deserialize(response["Response"])
            return model
        except Exception as e:
            if isinstance(e, TencentCloudSDKException):
                raise
            else:
                raise TencentCloudSDKException(e.message, e.message)


    def CreateDatasourceConnection(self, request):
        """创建数据源

        :param request: Request instance for CreateDatasourceConnection.
        :type request: :class:`tencentcloud.dlc.v20210125.models.CreateDatasourceConnectionRequest`
        :rtype: :class:`tencentcloud.dlc.v20210125.models.CreateDatasourceConnectionResponse`

        """
        try:
            params = request._serialize()
            headers = request.headers
            body = self.call("CreateDatasourceConnection", params, headers=headers)
            response = json.loads(body)
            model = models.CreateDatasourceConnectionResponse()
            model._deserialize(response["Response"])
            return model
        except Exception as e:
            if isinstance(e, TencentCloudSDKException):
                raise
            else:
                raise TencentCloudSDKException(e.message, e.message)


    def CreateDefaultDatasourceConnection(self, request):
        """为用户创建默认数据连接

        :param request: Request instance for CreateDefaultDatasourceConnection.
        :type request: :class:`tencentcloud.dlc.v20210125.models.CreateDefaultDatasourceConnectionRequest`
        :rtype: :class:`tencentcloud.dlc.v20210125.models.CreateDefaultDatasourceConnectionResponse`

        """
        try:
            params = request._serialize()
            headers = request.headers
            body = self.call("CreateDefaultDatasourceConnection", params, headers=headers)
            response = json.loads(body)
            model = models.CreateDefaultDatasourceConnectionResponse()
            model._deserialize(response["Response"])
            return model
        except Exception as e:
            if isinstance(e, TencentCloudSDKException):
                raise
            else:
                raise TencentCloudSDKException(e.message, e.message)


    def CreateExportResultTask(self, request):
        """该接口（CreateExportResultTask）用于导出SQL查询结果

        :param request: Request instance for CreateExportResultTask.
        :type request: :class:`tencentcloud.dlc.v20210125.models.CreateExportResultTaskRequest`
        :rtype: :class:`tencentcloud.dlc.v20210125.models.CreateExportResultTaskResponse`

        """
        try:
            params = request._serialize()
            headers = request.headers
            body = self.call("CreateExportResultTask", params, headers=headers)
            response = json.loads(body)
            model = models.CreateExportResultTaskResponse()
            model._deserialize(response["Response"])
            return model
        except Exception as e:
            if isinstance(e, TencentCloudSDKException):
                raise
            else:
                raise TencentCloudSDKException(e.message, e.message)


    def CreateExportTask(self, request):
        """该接口（CreateExportTask）用于创建导出任务

        :param request: Request instance for CreateExportTask.
        :type request: :class:`tencentcloud.dlc.v20210125.models.CreateExportTaskRequest`
        :rtype: :class:`tencentcloud.dlc.v20210125.models.CreateExportTaskResponse`

        """
        try:
            params = request._serialize()
            headers = request.headers
            body = self.call("CreateExportTask", params, headers=headers)
            response = json.loads(body)
            model = models.CreateExportTaskResponse()
            model._deserialize(response["Response"])
            return model
        except Exception as e:
            if isinstance(e, TencentCloudSDKException):
                raise
            else:
                raise TencentCloudSDKException(e.message, e.message)


    def CreateHouse(self, request):
        """为用户创建默认数据连接

        :param request: Request instance for CreateHouse.
        :type request: :class:`tencentcloud.dlc.v20210125.models.CreateHouseRequest`
        :rtype: :class:`tencentcloud.dlc.v20210125.models.CreateHouseResponse`

        """
        try:
            params = request._serialize()
            headers = request.headers
            body = self.call("CreateHouse", params, headers=headers)
            response = json.loads(body)
            model = models.CreateHouseResponse()
            model._deserialize(response["Response"])
            return model
        except Exception as e:
            if isinstance(e, TencentCloudSDKException):
                raise
            else:
                raise TencentCloudSDKException(e.message, e.message)


    def CreateImportTask(self, request):
        """该接口（CreateImportTask）用于创建导入任务

        :param request: Request instance for CreateImportTask.
        :type request: :class:`tencentcloud.dlc.v20210125.models.CreateImportTaskRequest`
        :rtype: :class:`tencentcloud.dlc.v20210125.models.CreateImportTaskResponse`

        """
        try:
            params = request._serialize()
            headers = request.headers
            body = self.call("CreateImportTask", params, headers=headers)
            response = json.loads(body)
            model = models.CreateImportTaskResponse()
            model._deserialize(response["Response"])
            return model
        except Exception as e:
            if isinstance(e, TencentCloudSDKException):
                raise
            else:
                raise TencentCloudSDKException(e.message, e.message)


    def CreateInternalTable(self, request):
        """创建托管存储内表（该接口已废弃）

        :param request: Request instance for CreateInternalTable.
        :type request: :class:`tencentcloud.dlc.v20210125.models.CreateInternalTableRequest`
        :rtype: :class:`tencentcloud.dlc.v20210125.models.CreateInternalTableResponse`

        """
        try:
            params = request._serialize()
            headers = request.headers
            body = self.call("CreateInternalTable", params, headers=headers)
            response = json.loads(body)
            model = models.CreateInternalTableResponse()
            model._deserialize(response["Response"])
            return model
        except Exception as e:
            if isinstance(e, TencentCloudSDKException):
                raise
            else:
                raise TencentCloudSDKException(e.message, e.message)


    def CreateKyuubiTask(self, request):
        """创建Kyuubi任务

        :param request: Request instance for CreateKyuubiTask.
        :type request: :class:`tencentcloud.dlc.v20210125.models.CreateKyuubiTaskRequest`
        :rtype: :class:`tencentcloud.dlc.v20210125.models.CreateKyuubiTaskResponse`

        """
        try:
            params = request._serialize()
            headers = request.headers
            body = self.call("CreateKyuubiTask", params, headers=headers)
            response = json.loads(body)
            model = models.CreateKyuubiTaskResponse()
            model._deserialize(response["Response"])
            return model
        except Exception as e:
            if isinstance(e, TencentCloudSDKException):
                raise
            else:
                raise TencentCloudSDKException(e.message, e.message)


    def CreateLakeFs(self, request):
        """创建托管存储

        :param request: Request instance for CreateLakeFs.
        :type request: :class:`tencentcloud.dlc.v20210125.models.CreateLakeFsRequest`
        :rtype: :class:`tencentcloud.dlc.v20210125.models.CreateLakeFsResponse`

        """
        try:
            params = request._serialize()
            headers = request.headers
            body = self.call("CreateLakeFs", params, headers=headers)
            response = json.loads(body)
            model = models.CreateLakeFsResponse()
            model._deserialize(response["Response"])
            return model
        except Exception as e:
            if isinstance(e, TencentCloudSDKException):
                raise
            else:
                raise TencentCloudSDKException(e.message, e.message)


    def CreateLakeFsChdfsBinding(self, request):
        """创建托管存储Chdfs绑定关系

        :param request: Request instance for CreateLakeFsChdfsBinding.
        :type request: :class:`tencentcloud.dlc.v20210125.models.CreateLakeFsChdfsBindingRequest`
        :rtype: :class:`tencentcloud.dlc.v20210125.models.CreateLakeFsChdfsBindingResponse`

        """
        try:
            params = request._serialize()
            headers = request.headers
            body = self.call("CreateLakeFsChdfsBinding", params, headers=headers)
            response = json.loads(body)
            model = models.CreateLakeFsChdfsBindingResponse()
            model._deserialize(response["Response"])
            return model
        except Exception as e:
            if isinstance(e, TencentCloudSDKException):
                raise
            else:
                raise TencentCloudSDKException(e.message, e.message)


    def CreateLink(self, request):
        """创建任务依赖关系

        :param request: Request instance for CreateLink.
        :type request: :class:`tencentcloud.dlc.v20210125.models.CreateLinkRequest`
        :rtype: :class:`tencentcloud.dlc.v20210125.models.CreateLinkResponse`

        """
        try:
            params = request._serialize()
            headers = request.headers
            body = self.call("CreateLink", params, headers=headers)
            response = json.loads(body)
            model = models.CreateLinkResponse()
            model._deserialize(response["Response"])
            return model
        except Exception as e:
            if isinstance(e, TencentCloudSDKException):
                raise
            else:
                raise TencentCloudSDKException(e.message, e.message)


    def CreateMetaDatabase(self, request):
        """本接口（CreateMetaDatabase）用于创建元数据库

        :param request: Request instance for CreateMetaDatabase.
        :type request: :class:`tencentcloud.dlc.v20210125.models.CreateMetaDatabaseRequest`
        :rtype: :class:`tencentcloud.dlc.v20210125.models.CreateMetaDatabaseResponse`

        """
        try:
            params = request._serialize()
            headers = request.headers
            body = self.call("CreateMetaDatabase", params, headers=headers)
            response = json.loads(body)
            model = models.CreateMetaDatabaseResponse()
            model._deserialize(response["Response"])
            return model
        except Exception as e:
            if isinstance(e, TencentCloudSDKException):
                raise
            else:
                raise TencentCloudSDKException(e.message, e.message)


    def CreateNotebookSession(self, request):
        """本接口（CreateNotebookSession）用于创建交互式session（notebook）

        :param request: Request instance for CreateNotebookSession.
        :type request: :class:`tencentcloud.dlc.v20210125.models.CreateNotebookSessionRequest`
        :rtype: :class:`tencentcloud.dlc.v20210125.models.CreateNotebookSessionResponse`

        """
        try:
            params = request._serialize()
            headers = request.headers
            body = self.call("CreateNotebookSession", params, headers=headers)
            response = json.loads(body)
            model = models.CreateNotebookSessionResponse()
            model._deserialize(response["Response"])
            return model
        except Exception as e:
            if isinstance(e, TencentCloudSDKException):
                raise
            else:
                raise TencentCloudSDKException(e.message, e.message)


    def CreateNotebookSessionStatement(self, request):
        """本接口（CreateNotebookSessionStatement）用于在session中执行代码片段

        :param request: Request instance for CreateNotebookSessionStatement.
        :type request: :class:`tencentcloud.dlc.v20210125.models.CreateNotebookSessionStatementRequest`
        :rtype: :class:`tencentcloud.dlc.v20210125.models.CreateNotebookSessionStatementResponse`

        """
        try:
            params = request._serialize()
            headers = request.headers
            body = self.call("CreateNotebookSessionStatement", params, headers=headers)
            response = json.loads(body)
            model = models.CreateNotebookSessionStatementResponse()
            model._deserialize(response["Response"])
            return model
        except Exception as e:
            if isinstance(e, TencentCloudSDKException):
                raise
            else:
                raise TencentCloudSDKException(e.message, e.message)


    def CreateNotebookSessionStatementSupportBatchSQL(self, request):
        """本接口（CreateNotebookSessionStatementSupportBatchSQL）用于创建交互式session并执行SQL任务

        :param request: Request instance for CreateNotebookSessionStatementSupportBatchSQL.
        :type request: :class:`tencentcloud.dlc.v20210125.models.CreateNotebookSessionStatementSupportBatchSQLRequest`
        :rtype: :class:`tencentcloud.dlc.v20210125.models.CreateNotebookSessionStatementSupportBatchSQLResponse`

        """
        try:
            params = request._serialize()
            headers = request.headers
            body = self.call("CreateNotebookSessionStatementSupportBatchSQL", params, headers=headers)
            response = json.loads(body)
            model = models.CreateNotebookSessionStatementSupportBatchSQLResponse()
            model._deserialize(response["Response"])
            return model
        except Exception as e:
            if isinstance(e, TencentCloudSDKException):
                raise
            else:
                raise TencentCloudSDKException(e.message, e.message)


    def CreateOrModifyCHDFSProduct(self, request):
        """此接口（CreateOrModifyCHDFSProduct）创建或修改元数据加速桶绑定产品

        :param request: Request instance for CreateOrModifyCHDFSProduct.
        :type request: :class:`tencentcloud.dlc.v20210125.models.CreateOrModifyCHDFSProductRequest`
        :rtype: :class:`tencentcloud.dlc.v20210125.models.CreateOrModifyCHDFSProductResponse`

        """
        try:
            params = request._serialize()
            headers = request.headers
            body = self.call("CreateOrModifyCHDFSProduct", params, headers=headers)
            response = json.loads(body)
            model = models.CreateOrModifyCHDFSProductResponse()
            model._deserialize(response["Response"])
            return model
        except Exception as e:
            if isinstance(e, TencentCloudSDKException):
                raise
            else:
                raise TencentCloudSDKException(e.message, e.message)


    def CreateQueryDir(self, request):
        """创建数据查询目录

        :param request: Request instance for CreateQueryDir.
        :type request: :class:`tencentcloud.dlc.v20210125.models.CreateQueryDirRequest`
        :rtype: :class:`tencentcloud.dlc.v20210125.models.CreateQueryDirResponse`

        """
        try:
            params = request._serialize()
            headers = request.headers
            body = self.call("CreateQueryDir", params, headers=headers)
            response = json.loads(body)
            model = models.CreateQueryDirResponse()
            model._deserialize(response["Response"])
            return model
        except Exception as e:
            if isinstance(e, TencentCloudSDKException):
                raise
            else:
                raise TencentCloudSDKException(e.message, e.message)


    def CreateResultDownload(self, request):
        """创建查询结果下载任务

        :param request: Request instance for CreateResultDownload.
        :type request: :class:`tencentcloud.dlc.v20210125.models.CreateResultDownloadRequest`
        :rtype: :class:`tencentcloud.dlc.v20210125.models.CreateResultDownloadResponse`

        """
        try:
            params = request._serialize()
            headers = request.headers
            body = self.call("CreateResultDownload", params, headers=headers)
            response = json.loads(body)
            model = models.CreateResultDownloadResponse()
            model._deserialize(response["Response"])
            return model
        except Exception as e:
            if isinstance(e, TencentCloudSDKException):
                raise
            else:
                raise TencentCloudSDKException(e.message, e.message)


    def CreateSQLSessionCatalog(self, request):
        """本接口（CreateSQLSessionCatalog）用于数据探索创建目录。

        :param request: Request instance for CreateSQLSessionCatalog.
        :type request: :class:`tencentcloud.dlc.v20210125.models.CreateSQLSessionCatalogRequest`
        :rtype: :class:`tencentcloud.dlc.v20210125.models.CreateSQLSessionCatalogResponse`

        """
        try:
            params = request._serialize()
            headers = request.headers
            body = self.call("CreateSQLSessionCatalog", params, headers=headers)
            response = json.loads(body)
            model = models.CreateSQLSessionCatalogResponse()
            model._deserialize(response["Response"])
            return model
        except Exception as e:
            if isinstance(e, TencentCloudSDKException):
                raise
            else:
                raise TencentCloudSDKException(e.message, e.message)


    def CreateSQLSessionSnapshot(self, request):
        """本接口（CreateSQLSessionSnapshot）用于保存用户的SQL会话

        :param request: Request instance for CreateSQLSessionSnapshot.
        :type request: :class:`tencentcloud.dlc.v20210125.models.CreateSQLSessionSnapshotRequest`
        :rtype: :class:`tencentcloud.dlc.v20210125.models.CreateSQLSessionSnapshotResponse`

        """
        try:
            params = request._serialize()
            headers = request.headers
            body = self.call("CreateSQLSessionSnapshot", params, headers=headers)
            response = json.loads(body)
            model = models.CreateSQLSessionSnapshotResponse()
            model._deserialize(response["Response"])
            return model
        except Exception as e:
            if isinstance(e, TencentCloudSDKException):
                raise
            else:
                raise TencentCloudSDKException(e.message, e.message)


    def CreateSQLSessionSubmitRecord(self, request):
        """本接口（CreateSQLSessionSubmitRecord）用于保存SQL会话提交记录

        :param request: Request instance for CreateSQLSessionSubmitRecord.
        :type request: :class:`tencentcloud.dlc.v20210125.models.CreateSQLSessionSubmitRecordRequest`
        :rtype: :class:`tencentcloud.dlc.v20210125.models.CreateSQLSessionSubmitRecordResponse`

        """
        try:
            params = request._serialize()
            headers = request.headers
            body = self.call("CreateSQLSessionSubmitRecord", params, headers=headers)
            response = json.loads(body)
            model = models.CreateSQLSessionSubmitRecordResponse()
            model._deserialize(response["Response"])
            return model
        except Exception as e:
            if isinstance(e, TencentCloudSDKException):
                raise
            else:
                raise TencentCloudSDKException(e.message, e.message)


    def CreateScheduleTask(self, request):
        """创建调度任务

        :param request: Request instance for CreateScheduleTask.
        :type request: :class:`tencentcloud.dlc.v20210125.models.CreateScheduleTaskRequest`
        :rtype: :class:`tencentcloud.dlc.v20210125.models.CreateScheduleTaskResponse`

        """
        try:
            params = request._serialize()
            headers = request.headers
            body = self.call("CreateScheduleTask", params, headers=headers)
            response = json.loads(body)
            model = models.CreateScheduleTaskResponse()
            model._deserialize(response["Response"])
            return model
        except Exception as e:
            if isinstance(e, TencentCloudSDKException):
                raise
            else:
                raise TencentCloudSDKException(e.message, e.message)


    def CreateScript(self, request):
        """该接口（CreateScript）用于创建sql脚本。

        :param request: Request instance for CreateScript.
        :type request: :class:`tencentcloud.dlc.v20210125.models.CreateScriptRequest`
        :rtype: :class:`tencentcloud.dlc.v20210125.models.CreateScriptResponse`

        """
        try:
            params = request._serialize()
            headers = request.headers
            body = self.call("CreateScript", params, headers=headers)
            response = json.loads(body)
            model = models.CreateScriptResponse()
            model._deserialize(response["Response"])
            return model
        except Exception as e:
            if isinstance(e, TencentCloudSDKException):
                raise
            else:
                raise TencentCloudSDKException(e.message, e.message)


    def CreateSparkApp(self, request):
        """创建spark作业

        :param request: Request instance for CreateSparkApp.
        :type request: :class:`tencentcloud.dlc.v20210125.models.CreateSparkAppRequest`
        :rtype: :class:`tencentcloud.dlc.v20210125.models.CreateSparkAppResponse`

        """
        try:
            params = request._serialize()
            headers = request.headers
            body = self.call("CreateSparkApp", params, headers=headers)
            response = json.loads(body)
            model = models.CreateSparkAppResponse()
            model._deserialize(response["Response"])
            return model
        except Exception as e:
            if isinstance(e, TencentCloudSDKException):
                raise
            else:
                raise TencentCloudSDKException(e.message, e.message)


    def CreateSparkAppForSQL(self, request):
        """本接口（CreateSparkAppForSQL）用于创建Spark Batch任务运行SQL。

        :param request: Request instance for CreateSparkAppForSQL.
        :type request: :class:`tencentcloud.dlc.v20210125.models.CreateSparkAppForSQLRequest`
        :rtype: :class:`tencentcloud.dlc.v20210125.models.CreateSparkAppForSQLResponse`

        """
        try:
            params = request._serialize()
            headers = request.headers
            body = self.call("CreateSparkAppForSQL", params, headers=headers)
            response = json.loads(body)
            model = models.CreateSparkAppForSQLResponse()
            model._deserialize(response["Response"])
            return model
        except Exception as e:
            if isinstance(e, TencentCloudSDKException):
                raise
            else:
                raise TencentCloudSDKException(e.message, e.message)


    def CreateSparkAppTask(self, request):
        """启动Spark作业

        :param request: Request instance for CreateSparkAppTask.
        :type request: :class:`tencentcloud.dlc.v20210125.models.CreateSparkAppTaskRequest`
        :rtype: :class:`tencentcloud.dlc.v20210125.models.CreateSparkAppTaskResponse`

        """
        try:
            params = request._serialize()
            headers = request.headers
            body = self.call("CreateSparkAppTask", params, headers=headers)
            response = json.loads(body)
            model = models.CreateSparkAppTaskResponse()
            model._deserialize(response["Response"])
            return model
        except Exception as e:
            if isinstance(e, TencentCloudSDKException):
                raise
            else:
                raise TencentCloudSDKException(e.message, e.message)


    def CreateSparkSessionBatchSQL(self, request):
        """本接口（CreateSparkSessionBatchSQL）用于向Spark作业引擎提交Spark SQL批任务。

        :param request: Request instance for CreateSparkSessionBatchSQL.
        :type request: :class:`tencentcloud.dlc.v20210125.models.CreateSparkSessionBatchSQLRequest`
        :rtype: :class:`tencentcloud.dlc.v20210125.models.CreateSparkSessionBatchSQLResponse`

        """
        try:
            params = request._serialize()
            headers = request.headers
            body = self.call("CreateSparkSessionBatchSQL", params, headers=headers)
            response = json.loads(body)
            model = models.CreateSparkSessionBatchSQLResponse()
            model._deserialize(response["Response"])
            return model
        except Exception as e:
            if isinstance(e, TencentCloudSDKException):
                raise
            else:
                raise TencentCloudSDKException(e.message, e.message)


    def CreateStoreLocation(self, request):
        """该接口（CreateStoreLocation）新增或覆盖计算结果存储位置。

        :param request: Request instance for CreateStoreLocation.
        :type request: :class:`tencentcloud.dlc.v20210125.models.CreateStoreLocationRequest`
        :rtype: :class:`tencentcloud.dlc.v20210125.models.CreateStoreLocationResponse`

        """
        try:
            params = request._serialize()
            headers = request.headers
            body = self.call("CreateStoreLocation", params, headers=headers)
            response = json.loads(body)
            model = models.CreateStoreLocationResponse()
            model._deserialize(response["Response"])
            return model
        except Exception as e:
            if isinstance(e, TencentCloudSDKException):
                raise
            else:
                raise TencentCloudSDKException(e.message, e.message)


    def CreateTable(self, request):
        """本接口（CreateTable）用于生成建表SQL。

        :param request: Request instance for CreateTable.
        :type request: :class:`tencentcloud.dlc.v20210125.models.CreateTableRequest`
        :rtype: :class:`tencentcloud.dlc.v20210125.models.CreateTableResponse`

        """
        try:
            params = request._serialize()
            headers = request.headers
            body = self.call("CreateTable", params, headers=headers)
            response = json.loads(body)
            model = models.CreateTableResponse()
            model._deserialize(response["Response"])
            return model
        except Exception as e:
            if isinstance(e, TencentCloudSDKException):
                raise
            else:
                raise TencentCloudSDKException(e.message, e.message)


    def CreateTask(self, request):
        """本接口（CreateTask）用于创建并执行SQL任务。（推荐使用CreateTasks接口）

        :param request: Request instance for CreateTask.
        :type request: :class:`tencentcloud.dlc.v20210125.models.CreateTaskRequest`
        :rtype: :class:`tencentcloud.dlc.v20210125.models.CreateTaskResponse`

        """
        try:
            params = request._serialize()
            headers = request.headers
            body = self.call("CreateTask", params, headers=headers)
            response = json.loads(body)
            model = models.CreateTaskResponse()
            model._deserialize(response["Response"])
            return model
        except Exception as e:
            if isinstance(e, TencentCloudSDKException):
                raise
            else:
                raise TencentCloudSDKException(e.message, e.message)


    def CreateTasks(self, request):
        """本接口（CreateTasks），用于批量创建并执行SQL任务

        :param request: Request instance for CreateTasks.
        :type request: :class:`tencentcloud.dlc.v20210125.models.CreateTasksRequest`
        :rtype: :class:`tencentcloud.dlc.v20210125.models.CreateTasksResponse`

        """
        try:
            params = request._serialize()
            headers = request.headers
            body = self.call("CreateTasks", params, headers=headers)
            response = json.loads(body)
            model = models.CreateTasksResponse()
            model._deserialize(response["Response"])
            return model
        except Exception as e:
            if isinstance(e, TencentCloudSDKException):
                raise
            else:
                raise TencentCloudSDKException(e.message, e.message)


    def CreateTasksInOrder(self, request):
        """按顺序创建任务（已经废弃，后期不再维护，请使用接口CreateTasks）

        :param request: Request instance for CreateTasksInOrder.
        :type request: :class:`tencentcloud.dlc.v20210125.models.CreateTasksInOrderRequest`
        :rtype: :class:`tencentcloud.dlc.v20210125.models.CreateTasksInOrderResponse`

        """
        try:
            params = request._serialize()
            headers = request.headers
            body = self.call("CreateTasksInOrder", params, headers=headers)
            response = json.loads(body)
            model = models.CreateTasksInOrderResponse()
            model._deserialize(response["Response"])
            return model
        except Exception as e:
            if isinstance(e, TencentCloudSDKException):
                raise
            else:
                raise TencentCloudSDKException(e.message, e.message)


    def CreateUser(self, request):
        """创建用户

        :param request: Request instance for CreateUser.
        :type request: :class:`tencentcloud.dlc.v20210125.models.CreateUserRequest`
        :rtype: :class:`tencentcloud.dlc.v20210125.models.CreateUserResponse`

        """
        try:
            params = request._serialize()
            headers = request.headers
            body = self.call("CreateUser", params, headers=headers)
            response = json.loads(body)
            model = models.CreateUserResponse()
            model._deserialize(response["Response"])
            return model
        except Exception as e:
            if isinstance(e, TencentCloudSDKException):
                raise
            else:
                raise TencentCloudSDKException(e.message, e.message)


    def CreateUserRole(self, request):
        """创建用户角色

        :param request: Request instance for CreateUserRole.
        :type request: :class:`tencentcloud.dlc.v20210125.models.CreateUserRoleRequest`
        :rtype: :class:`tencentcloud.dlc.v20210125.models.CreateUserRoleResponse`

        """
        try:
            params = request._serialize()
            headers = request.headers
            body = self.call("CreateUserRole", params, headers=headers)
            response = json.loads(body)
            model = models.CreateUserRoleResponse()
            model._deserialize(response["Response"])
            return model
        except Exception as e:
            if isinstance(e, TencentCloudSDKException):
                raise
            else:
                raise TencentCloudSDKException(e.message, e.message)


    def CreateWorkGroup(self, request):
        """创建工作组

        :param request: Request instance for CreateWorkGroup.
        :type request: :class:`tencentcloud.dlc.v20210125.models.CreateWorkGroupRequest`
        :rtype: :class:`tencentcloud.dlc.v20210125.models.CreateWorkGroupResponse`

        """
        try:
            params = request._serialize()
            headers = request.headers
            body = self.call("CreateWorkGroup", params, headers=headers)
            response = json.loads(body)
            model = models.CreateWorkGroupResponse()
            model._deserialize(response["Response"])
            return model
        except Exception as e:
            if isinstance(e, TencentCloudSDKException):
                raise
            else:
                raise TencentCloudSDKException(e.message, e.message)


    def CreateWorkflow(self, request):
        """创建调度计划

        :param request: Request instance for CreateWorkflow.
        :type request: :class:`tencentcloud.dlc.v20210125.models.CreateWorkflowRequest`
        :rtype: :class:`tencentcloud.dlc.v20210125.models.CreateWorkflowResponse`

        """
        try:
            params = request._serialize()
            headers = request.headers
            body = self.call("CreateWorkflow", params, headers=headers)
            response = json.loads(body)
            model = models.CreateWorkflowResponse()
            model._deserialize(response["Response"])
            return model
        except Exception as e:
            if isinstance(e, TencentCloudSDKException):
                raise
            else:
                raise TencentCloudSDKException(e.message, e.message)


    def DeleteCHDFSBindingProduct(self, request):
        """此接口（DeleteCHDFSBindingProduct）用于删除元数据加速桶和产品绑定关系

        :param request: Request instance for DeleteCHDFSBindingProduct.
        :type request: :class:`tencentcloud.dlc.v20210125.models.DeleteCHDFSBindingProductRequest`
        :rtype: :class:`tencentcloud.dlc.v20210125.models.DeleteCHDFSBindingProductResponse`

        """
        try:
            params = request._serialize()
            headers = request.headers
            body = self.call("DeleteCHDFSBindingProduct", params, headers=headers)
            response = json.loads(body)
            model = models.DeleteCHDFSBindingProductResponse()
            model._deserialize(response["Response"])
            return model
        except Exception as e:
            if isinstance(e, TencentCloudSDKException):
                raise
            else:
                raise TencentCloudSDKException(e.message, e.message)


    def DeleteCHDFSProduct(self, request):
        """此接口（DeleteCHDFSProduct）用于删除元数据加速桶绑定产品

        :param request: Request instance for DeleteCHDFSProduct.
        :type request: :class:`tencentcloud.dlc.v20210125.models.DeleteCHDFSProductRequest`
        :rtype: :class:`tencentcloud.dlc.v20210125.models.DeleteCHDFSProductResponse`

        """
        try:
            params = request._serialize()
            headers = request.headers
            body = self.call("DeleteCHDFSProduct", params, headers=headers)
            response = json.loads(body)
            model = models.DeleteCHDFSProductResponse()
            model._deserialize(response["Response"])
            return model
        except Exception as e:
            if isinstance(e, TencentCloudSDKException):
                raise
            else:
                raise TencentCloudSDKException(e.message, e.message)


    def DeleteColumns(self, request):
        """删除字段

        :param request: Request instance for DeleteColumns.
        :type request: :class:`tencentcloud.dlc.v20210125.models.DeleteColumnsRequest`
        :rtype: :class:`tencentcloud.dlc.v20210125.models.DeleteColumnsResponse`

        """
        try:
            params = request._serialize()
            headers = request.headers
            body = self.call("DeleteColumns", params, headers=headers)
            response = json.loads(body)
            model = models.DeleteColumnsResponse()
            model._deserialize(response["Response"])
            return model
        except Exception as e:
            if isinstance(e, TencentCloudSDKException):
                raise
            else:
                raise TencentCloudSDKException(e.message, e.message)


    def DeleteDataEngine(self, request):
        """删除数据引擎

        :param request: Request instance for DeleteDataEngine.
        :type request: :class:`tencentcloud.dlc.v20210125.models.DeleteDataEngineRequest`
        :rtype: :class:`tencentcloud.dlc.v20210125.models.DeleteDataEngineResponse`

        """
        try:
            params = request._serialize()
            headers = request.headers
            body = self.call("DeleteDataEngine", params, headers=headers)
            response = json.loads(body)
            model = models.DeleteDataEngineResponse()
            model._deserialize(response["Response"])
            return model
        except Exception as e:
            if isinstance(e, TencentCloudSDKException):
                raise
            else:
                raise TencentCloudSDKException(e.message, e.message)


    def DeleteDataQuery(self, request):
        """删除数据查询

        :param request: Request instance for DeleteDataQuery.
        :type request: :class:`tencentcloud.dlc.v20210125.models.DeleteDataQueryRequest`
        :rtype: :class:`tencentcloud.dlc.v20210125.models.DeleteDataQueryResponse`

        """
        try:
            params = request._serialize()
            headers = request.headers
            body = self.call("DeleteDataQuery", params, headers=headers)
            response = json.loads(body)
            model = models.DeleteDataQueryResponse()
            model._deserialize(response["Response"])
            return model
        except Exception as e:
            if isinstance(e, TencentCloudSDKException):
                raise
            else:
                raise TencentCloudSDKException(e.message, e.message)


    def DeleteDatabaseUDF(self, request):
        """删除udf

        :param request: Request instance for DeleteDatabaseUDF.
        :type request: :class:`tencentcloud.dlc.v20210125.models.DeleteDatabaseUDFRequest`
        :rtype: :class:`tencentcloud.dlc.v20210125.models.DeleteDatabaseUDFResponse`

        """
        try:
            params = request._serialize()
            headers = request.headers
            body = self.call("DeleteDatabaseUDF", params, headers=headers)
            response = json.loads(body)
            model = models.DeleteDatabaseUDFResponse()
            model._deserialize(response["Response"])
            return model
        except Exception as e:
            if isinstance(e, TencentCloudSDKException):
                raise
            else:
                raise TencentCloudSDKException(e.message, e.message)


    def DeleteDatasourceConnection(self, request):
        """删除数据连接

        :param request: Request instance for DeleteDatasourceConnection.
        :type request: :class:`tencentcloud.dlc.v20210125.models.DeleteDatasourceConnectionRequest`
        :rtype: :class:`tencentcloud.dlc.v20210125.models.DeleteDatasourceConnectionResponse`

        """
        try:
            params = request._serialize()
            headers = request.headers
            body = self.call("DeleteDatasourceConnection", params, headers=headers)
            response = json.loads(body)
            model = models.DeleteDatasourceConnectionResponse()
            model._deserialize(response["Response"])
            return model
        except Exception as e:
            if isinstance(e, TencentCloudSDKException):
                raise
            else:
                raise TencentCloudSDKException(e.message, e.message)


    def DeleteHouse(self, request):
        """删除队列

        :param request: Request instance for DeleteHouse.
        :type request: :class:`tencentcloud.dlc.v20210125.models.DeleteHouseRequest`
        :rtype: :class:`tencentcloud.dlc.v20210125.models.DeleteHouseResponse`

        """
        try:
            params = request._serialize()
            headers = request.headers
            body = self.call("DeleteHouse", params, headers=headers)
            response = json.loads(body)
            model = models.DeleteHouseResponse()
            model._deserialize(response["Response"])
            return model
        except Exception as e:
            if isinstance(e, TencentCloudSDKException):
                raise
            else:
                raise TencentCloudSDKException(e.message, e.message)


    def DeleteLakeFs(self, request):
        """删除托管存储

        :param request: Request instance for DeleteLakeFs.
        :type request: :class:`tencentcloud.dlc.v20210125.models.DeleteLakeFsRequest`
        :rtype: :class:`tencentcloud.dlc.v20210125.models.DeleteLakeFsResponse`

        """
        try:
            params = request._serialize()
            headers = request.headers
            body = self.call("DeleteLakeFs", params, headers=headers)
            response = json.loads(body)
            model = models.DeleteLakeFsResponse()
            model._deserialize(response["Response"])
            return model
        except Exception as e:
            if isinstance(e, TencentCloudSDKException):
                raise
            else:
                raise TencentCloudSDKException(e.message, e.message)


    def DeleteLakeFsChdfsBinding(self, request):
        """删除托管存储Chdfs绑定关系

        :param request: Request instance for DeleteLakeFsChdfsBinding.
        :type request: :class:`tencentcloud.dlc.v20210125.models.DeleteLakeFsChdfsBindingRequest`
        :rtype: :class:`tencentcloud.dlc.v20210125.models.DeleteLakeFsChdfsBindingResponse`

        """
        try:
            params = request._serialize()
            headers = request.headers
            body = self.call("DeleteLakeFsChdfsBinding", params, headers=headers)
            response = json.loads(body)
            model = models.DeleteLakeFsChdfsBindingResponse()
            model._deserialize(response["Response"])
            return model
        except Exception as e:
            if isinstance(e, TencentCloudSDKException):
                raise
            else:
                raise TencentCloudSDKException(e.message, e.message)


    def DeleteLink(self, request):
        """删除任务依赖关系

        :param request: Request instance for DeleteLink.
        :type request: :class:`tencentcloud.dlc.v20210125.models.DeleteLinkRequest`
        :rtype: :class:`tencentcloud.dlc.v20210125.models.DeleteLinkResponse`

        """
        try:
            params = request._serialize()
            headers = request.headers
            body = self.call("DeleteLink", params, headers=headers)
            response = json.loads(body)
            model = models.DeleteLinkResponse()
            model._deserialize(response["Response"])
            return model
        except Exception as e:
            if isinstance(e, TencentCloudSDKException):
                raise
            else:
                raise TencentCloudSDKException(e.message, e.message)


    def DeleteMetaDatabase(self, request):
        """本接口（DeleteMetaDatabase）用于一键删除元数据库

        :param request: Request instance for DeleteMetaDatabase.
        :type request: :class:`tencentcloud.dlc.v20210125.models.DeleteMetaDatabaseRequest`
        :rtype: :class:`tencentcloud.dlc.v20210125.models.DeleteMetaDatabaseResponse`

        """
        try:
            params = request._serialize()
            headers = request.headers
            body = self.call("DeleteMetaDatabase", params, headers=headers)
            response = json.loads(body)
            model = models.DeleteMetaDatabaseResponse()
            model._deserialize(response["Response"])
            return model
        except Exception as e:
            if isinstance(e, TencentCloudSDKException):
                raise
            else:
                raise TencentCloudSDKException(e.message, e.message)


    def DeleteNotebookSession(self, request):
        """本接口（DeleteNotebookSession）用于删除交互式session（notebook）

        :param request: Request instance for DeleteNotebookSession.
        :type request: :class:`tencentcloud.dlc.v20210125.models.DeleteNotebookSessionRequest`
        :rtype: :class:`tencentcloud.dlc.v20210125.models.DeleteNotebookSessionResponse`

        """
        try:
            params = request._serialize()
            headers = request.headers
            body = self.call("DeleteNotebookSession", params, headers=headers)
            response = json.loads(body)
            model = models.DeleteNotebookSessionResponse()
            model._deserialize(response["Response"])
            return model
        except Exception as e:
            if isinstance(e, TencentCloudSDKException):
                raise
            else:
                raise TencentCloudSDKException(e.message, e.message)


    def DeletePartitionField(self, request):
        """该接口(DeletePartitionField)用于删除分区字段

        :param request: Request instance for DeletePartitionField.
        :type request: :class:`tencentcloud.dlc.v20210125.models.DeletePartitionFieldRequest`
        :rtype: :class:`tencentcloud.dlc.v20210125.models.DeletePartitionFieldResponse`

        """
        try:
            params = request._serialize()
            headers = request.headers
            body = self.call("DeletePartitionField", params, headers=headers)
            response = json.loads(body)
            model = models.DeletePartitionFieldResponse()
            model._deserialize(response["Response"])
            return model
        except Exception as e:
            if isinstance(e, TencentCloudSDKException):
                raise
            else:
                raise TencentCloudSDKException(e.message, e.message)


    def DeleteQueryDir(self, request):
        """删除数据查询目录

        :param request: Request instance for DeleteQueryDir.
        :type request: :class:`tencentcloud.dlc.v20210125.models.DeleteQueryDirRequest`
        :rtype: :class:`tencentcloud.dlc.v20210125.models.DeleteQueryDirResponse`

        """
        try:
            params = request._serialize()
            headers = request.headers
            body = self.call("DeleteQueryDir", params, headers=headers)
            response = json.loads(body)
            model = models.DeleteQueryDirResponse()
            model._deserialize(response["Response"])
            return model
        except Exception as e:
            if isinstance(e, TencentCloudSDKException):
                raise
            else:
                raise TencentCloudSDKException(e.message, e.message)


    def DeleteSQLSessionCatalog(self, request):
        """本接口（DeleteSQLSessionCatalog）用于删除目录节点

        :param request: Request instance for DeleteSQLSessionCatalog.
        :type request: :class:`tencentcloud.dlc.v20210125.models.DeleteSQLSessionCatalogRequest`
        :rtype: :class:`tencentcloud.dlc.v20210125.models.DeleteSQLSessionCatalogResponse`

        """
        try:
            params = request._serialize()
            headers = request.headers
            body = self.call("DeleteSQLSessionCatalog", params, headers=headers)
            response = json.loads(body)
            model = models.DeleteSQLSessionCatalogResponse()
            model._deserialize(response["Response"])
            return model
        except Exception as e:
            if isinstance(e, TencentCloudSDKException):
                raise
            else:
                raise TencentCloudSDKException(e.message, e.message)


    def DeleteSQLSessionSnapshot(self, request):
        """本接口（DeleteSQLSessionSnapshot）用于删除SQL会话快照

        :param request: Request instance for DeleteSQLSessionSnapshot.
        :type request: :class:`tencentcloud.dlc.v20210125.models.DeleteSQLSessionSnapshotRequest`
        :rtype: :class:`tencentcloud.dlc.v20210125.models.DeleteSQLSessionSnapshotResponse`

        """
        try:
            params = request._serialize()
            headers = request.headers
            body = self.call("DeleteSQLSessionSnapshot", params, headers=headers)
            response = json.loads(body)
            model = models.DeleteSQLSessionSnapshotResponse()
            model._deserialize(response["Response"])
            return model
        except Exception as e:
            if isinstance(e, TencentCloudSDKException):
                raise
            else:
                raise TencentCloudSDKException(e.message, e.message)


    def DeleteScheduleTask(self, request):
        """删除调度任务

        :param request: Request instance for DeleteScheduleTask.
        :type request: :class:`tencentcloud.dlc.v20210125.models.DeleteScheduleTaskRequest`
        :rtype: :class:`tencentcloud.dlc.v20210125.models.DeleteScheduleTaskResponse`

        """
        try:
            params = request._serialize()
            headers = request.headers
            body = self.call("DeleteScheduleTask", params, headers=headers)
            response = json.loads(body)
            model = models.DeleteScheduleTaskResponse()
            model._deserialize(response["Response"])
            return model
        except Exception as e:
            if isinstance(e, TencentCloudSDKException):
                raise
            else:
                raise TencentCloudSDKException(e.message, e.message)


    def DeleteScript(self, request):
        """该接口（DeleteScript）用于删除sql脚本。

        :param request: Request instance for DeleteScript.
        :type request: :class:`tencentcloud.dlc.v20210125.models.DeleteScriptRequest`
        :rtype: :class:`tencentcloud.dlc.v20210125.models.DeleteScriptResponse`

        """
        try:
            params = request._serialize()
            headers = request.headers
            body = self.call("DeleteScript", params, headers=headers)
            response = json.loads(body)
            model = models.DeleteScriptResponse()
            model._deserialize(response["Response"])
            return model
        except Exception as e:
            if isinstance(e, TencentCloudSDKException):
                raise
            else:
                raise TencentCloudSDKException(e.message, e.message)


    def DeleteSparkApp(self, request):
        """删除spark作业

        :param request: Request instance for DeleteSparkApp.
        :type request: :class:`tencentcloud.dlc.v20210125.models.DeleteSparkAppRequest`
        :rtype: :class:`tencentcloud.dlc.v20210125.models.DeleteSparkAppResponse`

        """
        try:
            params = request._serialize()
            headers = request.headers
            body = self.call("DeleteSparkApp", params, headers=headers)
            response = json.loads(body)
            model = models.DeleteSparkAppResponse()
            model._deserialize(response["Response"])
            return model
        except Exception as e:
            if isinstance(e, TencentCloudSDKException):
                raise
            else:
                raise TencentCloudSDKException(e.message, e.message)


    def DeleteSparkImage(self, request):
        """删除Spark镜像信息

        :param request: Request instance for DeleteSparkImage.
        :type request: :class:`tencentcloud.dlc.v20210125.models.DeleteSparkImageRequest`
        :rtype: :class:`tencentcloud.dlc.v20210125.models.DeleteSparkImageResponse`

        """
        try:
            params = request._serialize()
            headers = request.headers
            body = self.call("DeleteSparkImage", params, headers=headers)
            response = json.loads(body)
            model = models.DeleteSparkImageResponse()
            model._deserialize(response["Response"])
            return model
        except Exception as e:
            if isinstance(e, TencentCloudSDKException):
                raise
            else:
                raise TencentCloudSDKException(e.message, e.message)


    def DeleteSparkImageUserRecords(self, request):
        """该接口（DeleteSparkImageUserRecords）用于删除指定用户的私有镜像

        :param request: Request instance for DeleteSparkImageUserRecords.
        :type request: :class:`tencentcloud.dlc.v20210125.models.DeleteSparkImageUserRecordsRequest`
        :rtype: :class:`tencentcloud.dlc.v20210125.models.DeleteSparkImageUserRecordsResponse`

        """
        try:
            params = request._serialize()
            headers = request.headers
            body = self.call("DeleteSparkImageUserRecords", params, headers=headers)
            response = json.loads(body)
            model = models.DeleteSparkImageUserRecordsResponse()
            model._deserialize(response["Response"])
            return model
        except Exception as e:
            if isinstance(e, TencentCloudSDKException):
                raise
            else:
                raise TencentCloudSDKException(e.message, e.message)


    def DeleteTable(self, request):
        """删除表

        :param request: Request instance for DeleteTable.
        :type request: :class:`tencentcloud.dlc.v20210125.models.DeleteTableRequest`
        :rtype: :class:`tencentcloud.dlc.v20210125.models.DeleteTableResponse`

        """
        try:
            params = request._serialize()
            headers = request.headers
            body = self.call("DeleteTable", params, headers=headers)
            response = json.loads(body)
            model = models.DeleteTableResponse()
            model._deserialize(response["Response"])
            return model
        except Exception as e:
            if isinstance(e, TencentCloudSDKException):
                raise
            else:
                raise TencentCloudSDKException(e.message, e.message)


    def DeleteTableBatch(self, request):
        """本接口（DeleteTableBatch）用于批量删除表

        :param request: Request instance for DeleteTableBatch.
        :type request: :class:`tencentcloud.dlc.v20210125.models.DeleteTableBatchRequest`
        :rtype: :class:`tencentcloud.dlc.v20210125.models.DeleteTableBatchResponse`

        """
        try:
            params = request._serialize()
            headers = request.headers
            body = self.call("DeleteTableBatch", params, headers=headers)
            response = json.loads(body)
            model = models.DeleteTableBatchResponse()
            model._deserialize(response["Response"])
            return model
        except Exception as e:
            if isinstance(e, TencentCloudSDKException):
                raise
            else:
                raise TencentCloudSDKException(e.message, e.message)


    def DeleteUser(self, request):
        """删除用户

        :param request: Request instance for DeleteUser.
        :type request: :class:`tencentcloud.dlc.v20210125.models.DeleteUserRequest`
        :rtype: :class:`tencentcloud.dlc.v20210125.models.DeleteUserResponse`

        """
        try:
            params = request._serialize()
            headers = request.headers
            body = self.call("DeleteUser", params, headers=headers)
            response = json.loads(body)
            model = models.DeleteUserResponse()
            model._deserialize(response["Response"])
            return model
        except Exception as e:
            if isinstance(e, TencentCloudSDKException):
                raise
            else:
                raise TencentCloudSDKException(e.message, e.message)


    def DeleteUserRole(self, request):
        """删除用户角色

        :param request: Request instance for DeleteUserRole.
        :type request: :class:`tencentcloud.dlc.v20210125.models.DeleteUserRoleRequest`
        :rtype: :class:`tencentcloud.dlc.v20210125.models.DeleteUserRoleResponse`

        """
        try:
            params = request._serialize()
            headers = request.headers
            body = self.call("DeleteUserRole", params, headers=headers)
            response = json.loads(body)
            model = models.DeleteUserRoleResponse()
            model._deserialize(response["Response"])
            return model
        except Exception as e:
            if isinstance(e, TencentCloudSDKException):
                raise
            else:
                raise TencentCloudSDKException(e.message, e.message)


    def DeleteUsersFromWorkGroup(self, request):
        """从工作组中删除用户

        :param request: Request instance for DeleteUsersFromWorkGroup.
        :type request: :class:`tencentcloud.dlc.v20210125.models.DeleteUsersFromWorkGroupRequest`
        :rtype: :class:`tencentcloud.dlc.v20210125.models.DeleteUsersFromWorkGroupResponse`

        """
        try:
            params = request._serialize()
            headers = request.headers
            body = self.call("DeleteUsersFromWorkGroup", params, headers=headers)
            response = json.loads(body)
            model = models.DeleteUsersFromWorkGroupResponse()
            model._deserialize(response["Response"])
            return model
        except Exception as e:
            if isinstance(e, TencentCloudSDKException):
                raise
            else:
                raise TencentCloudSDKException(e.message, e.message)


    def DeleteView(self, request):
        """删除视图

        :param request: Request instance for DeleteView.
        :type request: :class:`tencentcloud.dlc.v20210125.models.DeleteViewRequest`
        :rtype: :class:`tencentcloud.dlc.v20210125.models.DeleteViewResponse`

        """
        try:
            params = request._serialize()
            headers = request.headers
            body = self.call("DeleteView", params, headers=headers)
            response = json.loads(body)
            model = models.DeleteViewResponse()
            model._deserialize(response["Response"])
            return model
        except Exception as e:
            if isinstance(e, TencentCloudSDKException):
                raise
            else:
                raise TencentCloudSDKException(e.message, e.message)


    def DeleteWorkGroup(self, request):
        """删除工作组

        :param request: Request instance for DeleteWorkGroup.
        :type request: :class:`tencentcloud.dlc.v20210125.models.DeleteWorkGroupRequest`
        :rtype: :class:`tencentcloud.dlc.v20210125.models.DeleteWorkGroupResponse`

        """
        try:
            params = request._serialize()
            headers = request.headers
            body = self.call("DeleteWorkGroup", params, headers=headers)
            response = json.loads(body)
            model = models.DeleteWorkGroupResponse()
            model._deserialize(response["Response"])
            return model
        except Exception as e:
            if isinstance(e, TencentCloudSDKException):
                raise
            else:
                raise TencentCloudSDKException(e.message, e.message)


    def DeleteWorkflow(self, request):
        """删除调度计划

        :param request: Request instance for DeleteWorkflow.
        :type request: :class:`tencentcloud.dlc.v20210125.models.DeleteWorkflowRequest`
        :rtype: :class:`tencentcloud.dlc.v20210125.models.DeleteWorkflowResponse`

        """
        try:
            params = request._serialize()
            headers = request.headers
            body = self.call("DeleteWorkflow", params, headers=headers)
            response = json.loads(body)
            model = models.DeleteWorkflowResponse()
            model._deserialize(response["Response"])
            return model
        except Exception as e:
            if isinstance(e, TencentCloudSDKException):
                raise
            else:
                raise TencentCloudSDKException(e.message, e.message)


    def DescribeAdvancedStoreLocation(self, request):
        """查询sql查询界面高级设置

        :param request: Request instance for DescribeAdvancedStoreLocation.
        :type request: :class:`tencentcloud.dlc.v20210125.models.DescribeAdvancedStoreLocationRequest`
        :rtype: :class:`tencentcloud.dlc.v20210125.models.DescribeAdvancedStoreLocationResponse`

        """
        try:
            params = request._serialize()
            headers = request.headers
            body = self.call("DescribeAdvancedStoreLocation", params, headers=headers)
            response = json.loads(body)
            model = models.DescribeAdvancedStoreLocationResponse()
            model._deserialize(response["Response"])
            return model
        except Exception as e:
            if isinstance(e, TencentCloudSDKException):
                raise
            else:
                raise TencentCloudSDKException(e.message, e.message)


    def DescribeAllColumns(self, request):
        """查询所有字段信息

        :param request: Request instance for DescribeAllColumns.
        :type request: :class:`tencentcloud.dlc.v20210125.models.DescribeAllColumnsRequest`
        :rtype: :class:`tencentcloud.dlc.v20210125.models.DescribeAllColumnsResponse`

        """
        try:
            params = request._serialize()
            headers = request.headers
            body = self.call("DescribeAllColumns", params, headers=headers)
            response = json.loads(body)
            model = models.DescribeAllColumnsResponse()
            model._deserialize(response["Response"])
            return model
        except Exception as e:
            if isinstance(e, TencentCloudSDKException):
                raise
            else:
                raise TencentCloudSDKException(e.message, e.message)


    def DescribeAuditEvents(self, request):
        """查询审计事件

        :param request: Request instance for DescribeAuditEvents.
        :type request: :class:`tencentcloud.dlc.v20210125.models.DescribeAuditEventsRequest`
        :rtype: :class:`tencentcloud.dlc.v20210125.models.DescribeAuditEventsResponse`

        """
        try:
            params = request._serialize()
            headers = request.headers
            body = self.call("DescribeAuditEvents", params, headers=headers)
            response = json.loads(body)
            model = models.DescribeAuditEventsResponse()
            model._deserialize(response["Response"])
            return model
        except Exception as e:
            if isinstance(e, TencentCloudSDKException):
                raise
            else:
                raise TencentCloudSDKException(e.message, e.message)


    def DescribeAvailableVpc(self, request):
        """获取可用的vpc信息

        :param request: Request instance for DescribeAvailableVpc.
        :type request: :class:`tencentcloud.dlc.v20210125.models.DescribeAvailableVpcRequest`
        :rtype: :class:`tencentcloud.dlc.v20210125.models.DescribeAvailableVpcResponse`

        """
        try:
            params = request._serialize()
            headers = request.headers
            body = self.call("DescribeAvailableVpc", params, headers=headers)
            response = json.loads(body)
            model = models.DescribeAvailableVpcResponse()
            model._deserialize(response["Response"])
            return model
        except Exception as e:
            if isinstance(e, TencentCloudSDKException):
                raise
            else:
                raise TencentCloudSDKException(e.message, e.message)


    def DescribeBucketType(self, request):
        """此接口（DescribeBucketType）用于查询当前桶类型

        :param request: Request instance for DescribeBucketType.
        :type request: :class:`tencentcloud.dlc.v20210125.models.DescribeBucketTypeRequest`
        :rtype: :class:`tencentcloud.dlc.v20210125.models.DescribeBucketTypeResponse`

        """
        try:
            params = request._serialize()
            headers = request.headers
            body = self.call("DescribeBucketType", params, headers=headers)
            response = json.loads(body)
            model = models.DescribeBucketTypeResponse()
            model._deserialize(response["Response"])
            return model
        except Exception as e:
            if isinstance(e, TencentCloudSDKException):
                raise
            else:
                raise TencentCloudSDKException(e.message, e.message)


    def DescribeCHDFSAccessInfos(self, request):
        """此接口（DescribeCHDFSAccessInfos）用于查询元数据加速桶访问权限配置（托管桶和用户桶）

        :param request: Request instance for DescribeCHDFSAccessInfos.
        :type request: :class:`tencentcloud.dlc.v20210125.models.DescribeCHDFSAccessInfosRequest`
        :rtype: :class:`tencentcloud.dlc.v20210125.models.DescribeCHDFSAccessInfosResponse`

        """
        try:
            params = request._serialize()
            headers = request.headers
            body = self.call("DescribeCHDFSAccessInfos", params, headers=headers)
            response = json.loads(body)
            model = models.DescribeCHDFSAccessInfosResponse()
            model._deserialize(response["Response"])
            return model
        except Exception as e:
            if isinstance(e, TencentCloudSDKException):
                raise
            else:
                raise TencentCloudSDKException(e.message, e.message)


    def DescribeCHDFSMountPointAssociateInfos(self, request):
        """查询挂载点绑定信息

        :param request: Request instance for DescribeCHDFSMountPointAssociateInfos.
        :type request: :class:`tencentcloud.dlc.v20210125.models.DescribeCHDFSMountPointAssociateInfosRequest`
        :rtype: :class:`tencentcloud.dlc.v20210125.models.DescribeCHDFSMountPointAssociateInfosResponse`

        """
        try:
            params = request._serialize()
            headers = request.headers
            body = self.call("DescribeCHDFSMountPointAssociateInfos", params, headers=headers)
            response = json.loads(body)
            model = models.DescribeCHDFSMountPointAssociateInfosResponse()
            model._deserialize(response["Response"])
            return model
        except Exception as e:
            if isinstance(e, TencentCloudSDKException):
                raise
            else:
                raise TencentCloudSDKException(e.message, e.message)


    def DescribeCHDFSMountPointSuperuser(self, request):
        """此接口（DescribeCHDFSMountPointSuperuser）用于查询桶Superuser

        :param request: Request instance for DescribeCHDFSMountPointSuperuser.
        :type request: :class:`tencentcloud.dlc.v20210125.models.DescribeCHDFSMountPointSuperuserRequest`
        :rtype: :class:`tencentcloud.dlc.v20210125.models.DescribeCHDFSMountPointSuperuserResponse`

        """
        try:
            params = request._serialize()
            headers = request.headers
            body = self.call("DescribeCHDFSMountPointSuperuser", params, headers=headers)
            response = json.loads(body)
            model = models.DescribeCHDFSMountPointSuperuserResponse()
            model._deserialize(response["Response"])
            return model
        except Exception as e:
            if isinstance(e, TencentCloudSDKException):
                raise
            else:
                raise TencentCloudSDKException(e.message, e.message)


    def DescribeCHDFSMountPoints(self, request):
        """查看CHDFS挂载点

        :param request: Request instance for DescribeCHDFSMountPoints.
        :type request: :class:`tencentcloud.dlc.v20210125.models.DescribeCHDFSMountPointsRequest`
        :rtype: :class:`tencentcloud.dlc.v20210125.models.DescribeCHDFSMountPointsResponse`

        """
        try:
            params = request._serialize()
            headers = request.headers
            body = self.call("DescribeCHDFSMountPoints", params, headers=headers)
            response = json.loads(body)
            model = models.DescribeCHDFSMountPointsResponse()
            model._deserialize(response["Response"])
            return model
        except Exception as e:
            if isinstance(e, TencentCloudSDKException):
                raise
            else:
                raise TencentCloudSDKException(e.message, e.message)


    def DescribeCHDFSProducts(self, request):
        """此接口（DescribeCHDFSProducts）用于查询元数据加速桶绑定产品

        :param request: Request instance for DescribeCHDFSProducts.
        :type request: :class:`tencentcloud.dlc.v20210125.models.DescribeCHDFSProductsRequest`
        :rtype: :class:`tencentcloud.dlc.v20210125.models.DescribeCHDFSProductsResponse`

        """
        try:
            params = request._serialize()
            headers = request.headers
            body = self.call("DescribeCHDFSProducts", params, headers=headers)
            response = json.loads(body)
            model = models.DescribeCHDFSProductsResponse()
            model._deserialize(response["Response"])
            return model
        except Exception as e:
            if isinstance(e, TencentCloudSDKException):
                raise
            else:
                raise TencentCloudSDKException(e.message, e.message)


    def DescribeColumns(self, request):
        """分页查询字段信息

        :param request: Request instance for DescribeColumns.
        :type request: :class:`tencentcloud.dlc.v20210125.models.DescribeColumnsRequest`
        :rtype: :class:`tencentcloud.dlc.v20210125.models.DescribeColumnsResponse`

        """
        try:
            params = request._serialize()
            headers = request.headers
            body = self.call("DescribeColumns", params, headers=headers)
            response = json.loads(body)
            model = models.DescribeColumnsResponse()
            model._deserialize(response["Response"])
            return model
        except Exception as e:
            if isinstance(e, TencentCloudSDKException):
                raise
            else:
                raise TencentCloudSDKException(e.message, e.message)


    def DescribeDLCCHDFSBindingList(self, request):
        """此接口（DescribeDLCCHDFSBindingList）用于查询DLC元数据加速桶绑定列表

        :param request: Request instance for DescribeDLCCHDFSBindingList.
        :type request: :class:`tencentcloud.dlc.v20210125.models.DescribeDLCCHDFSBindingListRequest`
        :rtype: :class:`tencentcloud.dlc.v20210125.models.DescribeDLCCHDFSBindingListResponse`

        """
        try:
            params = request._serialize()
            headers = request.headers
            body = self.call("DescribeDLCCHDFSBindingList", params, headers=headers)
            response = json.loads(body)
            model = models.DescribeDLCCHDFSBindingListResponse()
            model._deserialize(response["Response"])
            return model
        except Exception as e:
            if isinstance(e, TencentCloudSDKException):
                raise
            else:
                raise TencentCloudSDKException(e.message, e.message)


    def DescribeDMSDatabase(self, request):
        """DMS元数据获取库

        :param request: Request instance for DescribeDMSDatabase.
        :type request: :class:`tencentcloud.dlc.v20210125.models.DescribeDMSDatabaseRequest`
        :rtype: :class:`tencentcloud.dlc.v20210125.models.DescribeDMSDatabaseResponse`

        """
        try:
            params = request._serialize()
            headers = request.headers
            body = self.call("DescribeDMSDatabase", params, headers=headers)
            response = json.loads(body)
            model = models.DescribeDMSDatabaseResponse()
            model._deserialize(response["Response"])
            return model
        except Exception as e:
            if isinstance(e, TencentCloudSDKException):
                raise
            else:
                raise TencentCloudSDKException(e.message, e.message)


    def DescribeDMSPartitionColumnStatisticList(self, request):
        """该接口（DescribeDMSPartitionColumnStatisticList）用于获取分区字段统计信息列表

        :param request: Request instance for DescribeDMSPartitionColumnStatisticList.
        :type request: :class:`tencentcloud.dlc.v20210125.models.DescribeDMSPartitionColumnStatisticListRequest`
        :rtype: :class:`tencentcloud.dlc.v20210125.models.DescribeDMSPartitionColumnStatisticListResponse`

        """
        try:
            params = request._serialize()
            headers = request.headers
            body = self.call("DescribeDMSPartitionColumnStatisticList", params, headers=headers)
            response = json.loads(body)
            model = models.DescribeDMSPartitionColumnStatisticListResponse()
            model._deserialize(response["Response"])
            return model
        except Exception as e:
            if isinstance(e, TencentCloudSDKException):
                raise
            else:
                raise TencentCloudSDKException(e.message, e.message)


    def DescribeDMSPartitions(self, request):
        """DMS元数据获取分区

        :param request: Request instance for DescribeDMSPartitions.
        :type request: :class:`tencentcloud.dlc.v20210125.models.DescribeDMSPartitionsRequest`
        :rtype: :class:`tencentcloud.dlc.v20210125.models.DescribeDMSPartitionsResponse`

        """
        try:
            params = request._serialize()
            headers = request.headers
            body = self.call("DescribeDMSPartitions", params, headers=headers)
            response = json.loads(body)
            model = models.DescribeDMSPartitionsResponse()
            model._deserialize(response["Response"])
            return model
        except Exception as e:
            if isinstance(e, TencentCloudSDKException):
                raise
            else:
                raise TencentCloudSDKException(e.message, e.message)


    def DescribeDMSTable(self, request):
        """DMS元数据获取表

        :param request: Request instance for DescribeDMSTable.
        :type request: :class:`tencentcloud.dlc.v20210125.models.DescribeDMSTableRequest`
        :rtype: :class:`tencentcloud.dlc.v20210125.models.DescribeDMSTableResponse`

        """
        try:
            params = request._serialize()
            headers = request.headers
            body = self.call("DescribeDMSTable", params, headers=headers)
            response = json.loads(body)
            model = models.DescribeDMSTableResponse()
            model._deserialize(response["Response"])
            return model
        except Exception as e:
            if isinstance(e, TencentCloudSDKException):
                raise
            else:
                raise TencentCloudSDKException(e.message, e.message)


    def DescribeDMSTableColumnStatisticList(self, request):
        """该接口（DescribeDMSTableColumnStatisticList）用于获取表字段统计信息列表

        :param request: Request instance for DescribeDMSTableColumnStatisticList.
        :type request: :class:`tencentcloud.dlc.v20210125.models.DescribeDMSTableColumnStatisticListRequest`
        :rtype: :class:`tencentcloud.dlc.v20210125.models.DescribeDMSTableColumnStatisticListResponse`

        """
        try:
            params = request._serialize()
            headers = request.headers
            body = self.call("DescribeDMSTableColumnStatisticList", params, headers=headers)
            response = json.loads(body)
            model = models.DescribeDMSTableColumnStatisticListResponse()
            model._deserialize(response["Response"])
            return model
        except Exception as e:
            if isinstance(e, TencentCloudSDKException):
                raise
            else:
                raise TencentCloudSDKException(e.message, e.message)


    def DescribeDMSTables(self, request):
        """DMS元数据获取表列表

        :param request: Request instance for DescribeDMSTables.
        :type request: :class:`tencentcloud.dlc.v20210125.models.DescribeDMSTablesRequest`
        :rtype: :class:`tencentcloud.dlc.v20210125.models.DescribeDMSTablesResponse`

        """
        try:
            params = request._serialize()
            headers = request.headers
            body = self.call("DescribeDMSTables", params, headers=headers)
            response = json.loads(body)
            model = models.DescribeDMSTablesResponse()
            model._deserialize(response["Response"])
            return model
        except Exception as e:
            if isinstance(e, TencentCloudSDKException):
                raise
            else:
                raise TencentCloudSDKException(e.message, e.message)


    def DescribeDataEngine(self, request):
        """本接口根据名称用于获取数据引擎详细信息

        :param request: Request instance for DescribeDataEngine.
        :type request: :class:`tencentcloud.dlc.v20210125.models.DescribeDataEngineRequest`
        :rtype: :class:`tencentcloud.dlc.v20210125.models.DescribeDataEngineResponse`

        """
        try:
            params = request._serialize()
            headers = request.headers
            body = self.call("DescribeDataEngine", params, headers=headers)
            response = json.loads(body)
            model = models.DescribeDataEngineResponse()
            model._deserialize(response["Response"])
            return model
        except Exception as e:
            if isinstance(e, TencentCloudSDKException):
                raise
            else:
                raise TencentCloudSDKException(e.message, e.message)


    def DescribeDataEngineEvents(self, request):
        """查询数据引擎事件

        :param request: Request instance for DescribeDataEngineEvents.
        :type request: :class:`tencentcloud.dlc.v20210125.models.DescribeDataEngineEventsRequest`
        :rtype: :class:`tencentcloud.dlc.v20210125.models.DescribeDataEngineEventsResponse`

        """
        try:
            params = request._serialize()
            headers = request.headers
            body = self.call("DescribeDataEngineEvents", params, headers=headers)
            response = json.loads(body)
            model = models.DescribeDataEngineEventsResponse()
            model._deserialize(response["Response"])
            return model
        except Exception as e:
            if isinstance(e, TencentCloudSDKException):
                raise
            else:
                raise TencentCloudSDKException(e.message, e.message)


    def DescribeDataEngineImageOperateRecords(self, request):
        """本接口（DescribeDataEngineImageOperateRecords）用于获取引擎镜像操作日志列表。

        :param request: Request instance for DescribeDataEngineImageOperateRecords.
        :type request: :class:`tencentcloud.dlc.v20210125.models.DescribeDataEngineImageOperateRecordsRequest`
        :rtype: :class:`tencentcloud.dlc.v20210125.models.DescribeDataEngineImageOperateRecordsResponse`

        """
        try:
            params = request._serialize()
            headers = request.headers
            body = self.call("DescribeDataEngineImageOperateRecords", params, headers=headers)
            response = json.loads(body)
            model = models.DescribeDataEngineImageOperateRecordsResponse()
            model._deserialize(response["Response"])
            return model
        except Exception as e:
            if isinstance(e, TencentCloudSDKException):
                raise
            else:
                raise TencentCloudSDKException(e.message, e.message)


    def DescribeDataEngineImageVersions(self, request):
        """本接口（DescribeDataEngineImageVersions）用于获取独享集群大版本镜像列表。

        :param request: Request instance for DescribeDataEngineImageVersions.
        :type request: :class:`tencentcloud.dlc.v20210125.models.DescribeDataEngineImageVersionsRequest`
        :rtype: :class:`tencentcloud.dlc.v20210125.models.DescribeDataEngineImageVersionsResponse`

        """
        try:
            params = request._serialize()
            headers = request.headers
            body = self.call("DescribeDataEngineImageVersions", params, headers=headers)
            response = json.loads(body)
            model = models.DescribeDataEngineImageVersionsResponse()
            model._deserialize(response["Response"])
            return model
        except Exception as e:
            if isinstance(e, TencentCloudSDKException):
                raise
            else:
                raise TencentCloudSDKException(e.message, e.message)


    def DescribeDataEngineParameters(self, request):
        """本接口（DescribeDataEngineParameters），用于获取参数列表。

        :param request: Request instance for DescribeDataEngineParameters.
        :type request: :class:`tencentcloud.dlc.v20210125.models.DescribeDataEngineParametersRequest`
        :rtype: :class:`tencentcloud.dlc.v20210125.models.DescribeDataEngineParametersResponse`

        """
        try:
            params = request._serialize()
            headers = request.headers
            body = self.call("DescribeDataEngineParameters", params, headers=headers)
            response = json.loads(body)
            model = models.DescribeDataEngineParametersResponse()
            model._deserialize(response["Response"])
            return model
        except Exception as e:
            if isinstance(e, TencentCloudSDKException):
                raise
            else:
                raise TencentCloudSDKException(e.message, e.message)


    def DescribeDataEnginePythonSparkImages(self, request):
        """本接口（DescribeDataEnginePythonSparkImages）用于获取PYSPARK镜像列表

        :param request: Request instance for DescribeDataEnginePythonSparkImages.
        :type request: :class:`tencentcloud.dlc.v20210125.models.DescribeDataEnginePythonSparkImagesRequest`
        :rtype: :class:`tencentcloud.dlc.v20210125.models.DescribeDataEnginePythonSparkImagesResponse`

        """
        try:
            params = request._serialize()
            headers = request.headers
            body = self.call("DescribeDataEnginePythonSparkImages", params, headers=headers)
            response = json.loads(body)
            model = models.DescribeDataEnginePythonSparkImagesResponse()
            model._deserialize(response["Response"])
            return model
        except Exception as e:
            if isinstance(e, TencentCloudSDKException):
                raise
            else:
                raise TencentCloudSDKException(e.message, e.message)


    def DescribeDataEngineSessionParameters(self, request):
        """本接口（DescribeDataEngineSessionParameters）用于获取指定小版本下的Session配置。

        :param request: Request instance for DescribeDataEngineSessionParameters.
        :type request: :class:`tencentcloud.dlc.v20210125.models.DescribeDataEngineSessionParametersRequest`
        :rtype: :class:`tencentcloud.dlc.v20210125.models.DescribeDataEngineSessionParametersResponse`

        """
        try:
            params = request._serialize()
            headers = request.headers
            body = self.call("DescribeDataEngineSessionParameters", params, headers=headers)
            response = json.loads(body)
            model = models.DescribeDataEngineSessionParametersResponse()
            model._deserialize(response["Response"])
            return model
        except Exception as e:
            if isinstance(e, TencentCloudSDKException):
                raise
            else:
                raise TencentCloudSDKException(e.message, e.message)


    def DescribeDataEngines(self, request):
        """本接口（DescribeDataEngines）用于查询DataEngines信息列表

        :param request: Request instance for DescribeDataEngines.
        :type request: :class:`tencentcloud.dlc.v20210125.models.DescribeDataEnginesRequest`
        :rtype: :class:`tencentcloud.dlc.v20210125.models.DescribeDataEnginesResponse`

        """
        try:
            params = request._serialize()
            headers = request.headers
            body = self.call("DescribeDataEngines", params, headers=headers)
            response = json.loads(body)
            model = models.DescribeDataEnginesResponse()
            model._deserialize(response["Response"])
            return model
        except Exception as e:
            if isinstance(e, TencentCloudSDKException):
                raise
            else:
                raise TencentCloudSDKException(e.message, e.message)


    def DescribeDataQueries(self, request):
        """列举数据查询

        :param request: Request instance for DescribeDataQueries.
        :type request: :class:`tencentcloud.dlc.v20210125.models.DescribeDataQueriesRequest`
        :rtype: :class:`tencentcloud.dlc.v20210125.models.DescribeDataQueriesResponse`

        """
        try:
            params = request._serialize()
            headers = request.headers
            body = self.call("DescribeDataQueries", params, headers=headers)
            response = json.loads(body)
            model = models.DescribeDataQueriesResponse()
            model._deserialize(response["Response"])
            return model
        except Exception as e:
            if isinstance(e, TencentCloudSDKException):
                raise
            else:
                raise TencentCloudSDKException(e.message, e.message)


    def DescribeDataQuery(self, request):
        """查询数据查询

        :param request: Request instance for DescribeDataQuery.
        :type request: :class:`tencentcloud.dlc.v20210125.models.DescribeDataQueryRequest`
        :rtype: :class:`tencentcloud.dlc.v20210125.models.DescribeDataQueryResponse`

        """
        try:
            params = request._serialize()
            headers = request.headers
            body = self.call("DescribeDataQuery", params, headers=headers)
            response = json.loads(body)
            model = models.DescribeDataQueryResponse()
            model._deserialize(response["Response"])
            return model
        except Exception as e:
            if isinstance(e, TencentCloudSDKException):
                raise
            else:
                raise TencentCloudSDKException(e.message, e.message)


    def DescribeDataTaskAlarmFiled(self, request):
        """该接口（DescribeDataTaskAlarmFiled）用于云监控查询数据任务告警字段

        :param request: Request instance for DescribeDataTaskAlarmFiled.
        :type request: :class:`tencentcloud.dlc.v20210125.models.DescribeDataTaskAlarmFiledRequest`
        :rtype: :class:`tencentcloud.dlc.v20210125.models.DescribeDataTaskAlarmFiledResponse`

        """
        try:
            params = request._serialize()
            headers = request.headers
            body = self.call("DescribeDataTaskAlarmFiled", params, headers=headers)
            response = json.loads(body)
            model = models.DescribeDataTaskAlarmFiledResponse()
            model._deserialize(response["Response"])
            return model
        except Exception as e:
            if isinstance(e, TencentCloudSDKException):
                raise
            else:
                raise TencentCloudSDKException(e.message, e.message)


    def DescribeDatabase(self, request):
        """本接口（DescribeDatabase）,查询数据库详细信息

        :param request: Request instance for DescribeDatabase.
        :type request: :class:`tencentcloud.dlc.v20210125.models.DescribeDatabaseRequest`
        :rtype: :class:`tencentcloud.dlc.v20210125.models.DescribeDatabaseResponse`

        """
        try:
            params = request._serialize()
            headers = request.headers
            body = self.call("DescribeDatabase", params, headers=headers)
            response = json.loads(body)
            model = models.DescribeDatabaseResponse()
            model._deserialize(response["Response"])
            return model
        except Exception as e:
            if isinstance(e, TencentCloudSDKException):
                raise
            else:
                raise TencentCloudSDKException(e.message, e.message)


    def DescribeDatabaseUDFList(self, request):
        """查询数据库对应的UDF列表

        :param request: Request instance for DescribeDatabaseUDFList.
        :type request: :class:`tencentcloud.dlc.v20210125.models.DescribeDatabaseUDFListRequest`
        :rtype: :class:`tencentcloud.dlc.v20210125.models.DescribeDatabaseUDFListResponse`

        """
        try:
            params = request._serialize()
            headers = request.headers
            body = self.call("DescribeDatabaseUDFList", params, headers=headers)
            response = json.loads(body)
            model = models.DescribeDatabaseUDFListResponse()
            model._deserialize(response["Response"])
            return model
        except Exception as e:
            if isinstance(e, TencentCloudSDKException):
                raise
            else:
                raise TencentCloudSDKException(e.message, e.message)


    def DescribeDatabases(self, request):
        """本接口（DescribeDatabases）用于查询数据库列表。

        :param request: Request instance for DescribeDatabases.
        :type request: :class:`tencentcloud.dlc.v20210125.models.DescribeDatabasesRequest`
        :rtype: :class:`tencentcloud.dlc.v20210125.models.DescribeDatabasesResponse`

        """
        try:
            params = request._serialize()
            headers = request.headers
            body = self.call("DescribeDatabases", params, headers=headers)
            response = json.loads(body)
            model = models.DescribeDatabasesResponse()
            model._deserialize(response["Response"])
            return model
        except Exception as e:
            if isinstance(e, TencentCloudSDKException):
                raise
            else:
                raise TencentCloudSDKException(e.message, e.message)


    def DescribeDatasourceConnection(self, request):
        """本接口（DescribeDatasourceConnection）用于查询数据源信息

        :param request: Request instance for DescribeDatasourceConnection.
        :type request: :class:`tencentcloud.dlc.v20210125.models.DescribeDatasourceConnectionRequest`
        :rtype: :class:`tencentcloud.dlc.v20210125.models.DescribeDatasourceConnectionResponse`

        """
        try:
            params = request._serialize()
            headers = request.headers
            body = self.call("DescribeDatasourceConnection", params, headers=headers)
            response = json.loads(body)
            model = models.DescribeDatasourceConnectionResponse()
            model._deserialize(response["Response"])
            return model
        except Exception as e:
            if isinstance(e, TencentCloudSDKException):
                raise
            else:
                raise TencentCloudSDKException(e.message, e.message)


    def DescribeDefaultEngineConfig(self, request):
        """获取默认引擎配置

        :param request: Request instance for DescribeDefaultEngineConfig.
        :type request: :class:`tencentcloud.dlc.v20210125.models.DescribeDefaultEngineConfigRequest`
        :rtype: :class:`tencentcloud.dlc.v20210125.models.DescribeDefaultEngineConfigResponse`

        """
        try:
            params = request._serialize()
            headers = request.headers
            body = self.call("DescribeDefaultEngineConfig", params, headers=headers)
            response = json.loads(body)
            model = models.DescribeDefaultEngineConfigResponse()
            model._deserialize(response["Response"])
            return model
        except Exception as e:
            if isinstance(e, TencentCloudSDKException):
                raise
            else:
                raise TencentCloudSDKException(e.message, e.message)


    def DescribeEngineUsageInfo(self, request):
        """本接口根据引擎ID查询数据引擎资源使用情况

        :param request: Request instance for DescribeEngineUsageInfo.
        :type request: :class:`tencentcloud.dlc.v20210125.models.DescribeEngineUsageInfoRequest`
        :rtype: :class:`tencentcloud.dlc.v20210125.models.DescribeEngineUsageInfoResponse`

        """
        try:
            params = request._serialize()
            headers = request.headers
            body = self.call("DescribeEngineUsageInfo", params, headers=headers)
            response = json.loads(body)
            model = models.DescribeEngineUsageInfoResponse()
            model._deserialize(response["Response"])
            return model
        except Exception as e:
            if isinstance(e, TencentCloudSDKException):
                raise
            else:
                raise TencentCloudSDKException(e.message, e.message)


    def DescribeExportResultTasks(self, request):
        """该接口（DescribeExportResultTasks）用于查询查询结果数据导出任务列表

        :param request: Request instance for DescribeExportResultTasks.
        :type request: :class:`tencentcloud.dlc.v20210125.models.DescribeExportResultTasksRequest`
        :rtype: :class:`tencentcloud.dlc.v20210125.models.DescribeExportResultTasksResponse`

        """
        try:
            params = request._serialize()
            headers = request.headers
            body = self.call("DescribeExportResultTasks", params, headers=headers)
            response = json.loads(body)
            model = models.DescribeExportResultTasksResponse()
            model._deserialize(response["Response"])
            return model
        except Exception as e:
            if isinstance(e, TencentCloudSDKException):
                raise
            else:
                raise TencentCloudSDKException(e.message, e.message)


    def DescribeFatherAndSonTaskInstances(self, request):
        """父子实例列表

        :param request: Request instance for DescribeFatherAndSonTaskInstances.
        :type request: :class:`tencentcloud.dlc.v20210125.models.DescribeFatherAndSonTaskInstancesRequest`
        :rtype: :class:`tencentcloud.dlc.v20210125.models.DescribeFatherAndSonTaskInstancesResponse`

        """
        try:
            params = request._serialize()
            headers = request.headers
            body = self.call("DescribeFatherAndSonTaskInstances", params, headers=headers)
            response = json.loads(body)
            model = models.DescribeFatherAndSonTaskInstancesResponse()
            model._deserialize(response["Response"])
            return model
        except Exception as e:
            if isinstance(e, TencentCloudSDKException):
                raise
            else:
                raise TencentCloudSDKException(e.message, e.message)


    def DescribeFatherAndSonTasks(self, request):
        """父子任务列表

        :param request: Request instance for DescribeFatherAndSonTasks.
        :type request: :class:`tencentcloud.dlc.v20210125.models.DescribeFatherAndSonTasksRequest`
        :rtype: :class:`tencentcloud.dlc.v20210125.models.DescribeFatherAndSonTasksResponse`

        """
        try:
            params = request._serialize()
            headers = request.headers
            body = self.call("DescribeFatherAndSonTasks", params, headers=headers)
            response = json.loads(body)
            model = models.DescribeFatherAndSonTasksResponse()
            model._deserialize(response["Response"])
            return model
        except Exception as e:
            if isinstance(e, TencentCloudSDKException):
                raise
            else:
                raise TencentCloudSDKException(e.message, e.message)


    def DescribeForbiddenTablePro(self, request):
        """本接口（DescribeForbiddenTablePro）用于查询被禁用的表属性列表（新）

        :param request: Request instance for DescribeForbiddenTablePro.
        :type request: :class:`tencentcloud.dlc.v20210125.models.DescribeForbiddenTableProRequest`
        :rtype: :class:`tencentcloud.dlc.v20210125.models.DescribeForbiddenTableProResponse`

        """
        try:
            params = request._serialize()
            headers = request.headers
            body = self.call("DescribeForbiddenTablePro", params, headers=headers)
            response = json.loads(body)
            model = models.DescribeForbiddenTableProResponse()
            model._deserialize(response["Response"])
            return model
        except Exception as e:
            if isinstance(e, TencentCloudSDKException):
                raise
            else:
                raise TencentCloudSDKException(e.message, e.message)


    def DescribeForbiddenTableProperties(self, request):
        """本接口（DescribeForbiddenTableProperties）用于获取被禁用的表属性列表

        :param request: Request instance for DescribeForbiddenTableProperties.
        :type request: :class:`tencentcloud.dlc.v20210125.models.DescribeForbiddenTablePropertiesRequest`
        :rtype: :class:`tencentcloud.dlc.v20210125.models.DescribeForbiddenTablePropertiesResponse`

        """
        try:
            params = request._serialize()
            headers = request.headers
            body = self.call("DescribeForbiddenTableProperties", params, headers=headers)
            response = json.loads(body)
            model = models.DescribeForbiddenTablePropertiesResponse()
            model._deserialize(response["Response"])
            return model
        except Exception as e:
            if isinstance(e, TencentCloudSDKException):
                raise
            else:
                raise TencentCloudSDKException(e.message, e.message)


    def DescribeFunctions(self, request):
        """查询分析界面-查询数据库对应的UDF列表

        :param request: Request instance for DescribeFunctions.
        :type request: :class:`tencentcloud.dlc.v20210125.models.DescribeFunctionsRequest`
        :rtype: :class:`tencentcloud.dlc.v20210125.models.DescribeFunctionsResponse`

        """
        try:
            params = request._serialize()
            headers = request.headers
            body = self.call("DescribeFunctions", params, headers=headers)
            response = json.loads(body)
            model = models.DescribeFunctionsResponse()
            model._deserialize(response["Response"])
            return model
        except Exception as e:
            if isinstance(e, TencentCloudSDKException):
                raise
            else:
                raise TencentCloudSDKException(e.message, e.message)


    def DescribeGovernDefaultPolicy(self, request):
        """查询数据治理规则默认值

        :param request: Request instance for DescribeGovernDefaultPolicy.
        :type request: :class:`tencentcloud.dlc.v20210125.models.DescribeGovernDefaultPolicyRequest`
        :rtype: :class:`tencentcloud.dlc.v20210125.models.DescribeGovernDefaultPolicyResponse`

        """
        try:
            params = request._serialize()
            headers = request.headers
            body = self.call("DescribeGovernDefaultPolicy", params, headers=headers)
            response = json.loads(body)
            model = models.DescribeGovernDefaultPolicyResponse()
            model._deserialize(response["Response"])
            return model
        except Exception as e:
            if isinstance(e, TencentCloudSDKException):
                raise
            else:
                raise TencentCloudSDKException(e.message, e.message)


    def DescribeGovernEventRule(self, request):
        """查询数据治理事件阈值

        :param request: Request instance for DescribeGovernEventRule.
        :type request: :class:`tencentcloud.dlc.v20210125.models.DescribeGovernEventRuleRequest`
        :rtype: :class:`tencentcloud.dlc.v20210125.models.DescribeGovernEventRuleResponse`

        """
        try:
            params = request._serialize()
            headers = request.headers
            body = self.call("DescribeGovernEventRule", params, headers=headers)
            response = json.loads(body)
            model = models.DescribeGovernEventRuleResponse()
            model._deserialize(response["Response"])
            return model
        except Exception as e:
            if isinstance(e, TencentCloudSDKException):
                raise
            else:
                raise TencentCloudSDKException(e.message, e.message)


    def DescribeGovernMetaInfo(self, request):
        """查询数据治理元信息

        :param request: Request instance for DescribeGovernMetaInfo.
        :type request: :class:`tencentcloud.dlc.v20210125.models.DescribeGovernMetaInfoRequest`
        :rtype: :class:`tencentcloud.dlc.v20210125.models.DescribeGovernMetaInfoResponse`

        """
        try:
            params = request._serialize()
            headers = request.headers
            body = self.call("DescribeGovernMetaInfo", params, headers=headers)
            response = json.loads(body)
            model = models.DescribeGovernMetaInfoResponse()
            model._deserialize(response["Response"])
            return model
        except Exception as e:
            if isinstance(e, TencentCloudSDKException):
                raise
            else:
                raise TencentCloudSDKException(e.message, e.message)


    def DescribeHouseEvents(self, request):
        """查询数据引擎事件

        :param request: Request instance for DescribeHouseEvents.
        :type request: :class:`tencentcloud.dlc.v20210125.models.DescribeHouseEventsRequest`
        :rtype: :class:`tencentcloud.dlc.v20210125.models.DescribeHouseEventsResponse`

        """
        try:
            params = request._serialize()
            headers = request.headers
            body = self.call("DescribeHouseEvents", params, headers=headers)
            response = json.loads(body)
            model = models.DescribeHouseEventsResponse()
            model._deserialize(response["Response"])
            return model
        except Exception as e:
            if isinstance(e, TencentCloudSDKException):
                raise
            else:
                raise TencentCloudSDKException(e.message, e.message)


    def DescribeInstanceLogList(self, request):
        """调度任务实例日志列表

        :param request: Request instance for DescribeInstanceLogList.
        :type request: :class:`tencentcloud.dlc.v20210125.models.DescribeInstanceLogListRequest`
        :rtype: :class:`tencentcloud.dlc.v20210125.models.DescribeInstanceLogListResponse`

        """
        try:
            params = request._serialize()
            headers = request.headers
            body = self.call("DescribeInstanceLogList", params, headers=headers)
            response = json.loads(body)
            model = models.DescribeInstanceLogListResponse()
            model._deserialize(response["Response"])
            return model
        except Exception as e:
            if isinstance(e, TencentCloudSDKException):
                raise
            else:
                raise TencentCloudSDKException(e.message, e.message)


    def DescribeLakeFsAccess(self, request):
        """获取LakeFs访问的临时秘钥

        :param request: Request instance for DescribeLakeFsAccess.
        :type request: :class:`tencentcloud.dlc.v20210125.models.DescribeLakeFsAccessRequest`
        :rtype: :class:`tencentcloud.dlc.v20210125.models.DescribeLakeFsAccessResponse`

        """
        try:
            params = request._serialize()
            headers = request.headers
            body = self.call("DescribeLakeFsAccess", params, headers=headers)
            response = json.loads(body)
            model = models.DescribeLakeFsAccessResponse()
            model._deserialize(response["Response"])
            return model
        except Exception as e:
            if isinstance(e, TencentCloudSDKException):
                raise
            else:
                raise TencentCloudSDKException(e.message, e.message)


    def DescribeLakeFsChdfsBindings(self, request):
        """查询当前用户Chdfs类型托管存储绑定关系

        :param request: Request instance for DescribeLakeFsChdfsBindings.
        :type request: :class:`tencentcloud.dlc.v20210125.models.DescribeLakeFsChdfsBindingsRequest`
        :rtype: :class:`tencentcloud.dlc.v20210125.models.DescribeLakeFsChdfsBindingsResponse`

        """
        try:
            params = request._serialize()
            headers = request.headers
            body = self.call("DescribeLakeFsChdfsBindings", params, headers=headers)
            response = json.loads(body)
            model = models.DescribeLakeFsChdfsBindingsResponse()
            model._deserialize(response["Response"])
            return model
        except Exception as e:
            if isinstance(e, TencentCloudSDKException):
                raise
            else:
                raise TencentCloudSDKException(e.message, e.message)


    def DescribeLakeFsChdfsNames(self, request):
        """查询当前用户Chdfs类型的托管存储名称

        :param request: Request instance for DescribeLakeFsChdfsNames.
        :type request: :class:`tencentcloud.dlc.v20210125.models.DescribeLakeFsChdfsNamesRequest`
        :rtype: :class:`tencentcloud.dlc.v20210125.models.DescribeLakeFsChdfsNamesResponse`

        """
        try:
            params = request._serialize()
            headers = request.headers
            body = self.call("DescribeLakeFsChdfsNames", params, headers=headers)
            response = json.loads(body)
            model = models.DescribeLakeFsChdfsNamesResponse()
            model._deserialize(response["Response"])
            return model
        except Exception as e:
            if isinstance(e, TencentCloudSDKException):
                raise
            else:
                raise TencentCloudSDKException(e.message, e.message)


    def DescribeLakeFsDirSummary(self, request):
        """查询托管存储指定目录的Summary

        :param request: Request instance for DescribeLakeFsDirSummary.
        :type request: :class:`tencentcloud.dlc.v20210125.models.DescribeLakeFsDirSummaryRequest`
        :rtype: :class:`tencentcloud.dlc.v20210125.models.DescribeLakeFsDirSummaryResponse`

        """
        try:
            params = request._serialize()
            headers = request.headers
            body = self.call("DescribeLakeFsDirSummary", params, headers=headers)
            response = json.loads(body)
            model = models.DescribeLakeFsDirSummaryResponse()
            model._deserialize(response["Response"])
            return model
        except Exception as e:
            if isinstance(e, TencentCloudSDKException):
                raise
            else:
                raise TencentCloudSDKException(e.message, e.message)


    def DescribeLakeFsInfo(self, request):
        """查询用户的托管存储信息

        :param request: Request instance for DescribeLakeFsInfo.
        :type request: :class:`tencentcloud.dlc.v20210125.models.DescribeLakeFsInfoRequest`
        :rtype: :class:`tencentcloud.dlc.v20210125.models.DescribeLakeFsInfoResponse`

        """
        try:
            params = request._serialize()
            headers = request.headers
            body = self.call("DescribeLakeFsInfo", params, headers=headers)
            response = json.loads(body)
            model = models.DescribeLakeFsInfoResponse()
            model._deserialize(response["Response"])
            return model
        except Exception as e:
            if isinstance(e, TencentCloudSDKException):
                raise
            else:
                raise TencentCloudSDKException(e.message, e.message)


    def DescribeLakeFsPath(self, request):
        """获取LakeFs指定路径的访问信息

        :param request: Request instance for DescribeLakeFsPath.
        :type request: :class:`tencentcloud.dlc.v20210125.models.DescribeLakeFsPathRequest`
        :rtype: :class:`tencentcloud.dlc.v20210125.models.DescribeLakeFsPathResponse`

        """
        try:
            params = request._serialize()
            headers = request.headers
            body = self.call("DescribeLakeFsPath", params, headers=headers)
            response = json.loads(body)
            model = models.DescribeLakeFsPathResponse()
            model._deserialize(response["Response"])
            return model
        except Exception as e:
            if isinstance(e, TencentCloudSDKException):
                raise
            else:
                raise TencentCloudSDKException(e.message, e.message)


    def DescribeLakeFsWarehouseAccess(self, request):
        """查询托管存储warehouse目录的访问权限

        :param request: Request instance for DescribeLakeFsWarehouseAccess.
        :type request: :class:`tencentcloud.dlc.v20210125.models.DescribeLakeFsWarehouseAccessRequest`
        :rtype: :class:`tencentcloud.dlc.v20210125.models.DescribeLakeFsWarehouseAccessResponse`

        """
        try:
            params = request._serialize()
            headers = request.headers
            body = self.call("DescribeLakeFsWarehouseAccess", params, headers=headers)
            response = json.loads(body)
            model = models.DescribeLakeFsWarehouseAccessResponse()
            model._deserialize(response["Response"])
            return model
        except Exception as e:
            if isinstance(e, TencentCloudSDKException):
                raise
            else:
                raise TencentCloudSDKException(e.message, e.message)


    def DescribeMainDataDataEngine(self, request):
        """查看概览页数据引擎相关数据

        :param request: Request instance for DescribeMainDataDataEngine.
        :type request: :class:`tencentcloud.dlc.v20210125.models.DescribeMainDataDataEngineRequest`
        :rtype: :class:`tencentcloud.dlc.v20210125.models.DescribeMainDataDataEngineResponse`

        """
        try:
            params = request._serialize()
            headers = request.headers
            body = self.call("DescribeMainDataDataEngine", params, headers=headers)
            response = json.loads(body)
            model = models.DescribeMainDataDataEngineResponse()
            model._deserialize(response["Response"])
            return model
        except Exception as e:
            if isinstance(e, TencentCloudSDKException):
                raise
            else:
                raise TencentCloudSDKException(e.message, e.message)


    def DescribeMainDataOverview(self, request):
        """首页，查看数据概览

        :param request: Request instance for DescribeMainDataOverview.
        :type request: :class:`tencentcloud.dlc.v20210125.models.DescribeMainDataOverviewRequest`
        :rtype: :class:`tencentcloud.dlc.v20210125.models.DescribeMainDataOverviewResponse`

        """
        try:
            params = request._serialize()
            headers = request.headers
            body = self.call("DescribeMainDataOverview", params, headers=headers)
            response = json.loads(body)
            model = models.DescribeMainDataOverviewResponse()
            model._deserialize(response["Response"])
            return model
        except Exception as e:
            if isinstance(e, TencentCloudSDKException):
                raise
            else:
                raise TencentCloudSDKException(e.message, e.message)


    def DescribeMainDataOverviewLine(self, request):
        """首页，查看CU时用量折线图

        :param request: Request instance for DescribeMainDataOverviewLine.
        :type request: :class:`tencentcloud.dlc.v20210125.models.DescribeMainDataOverviewLineRequest`
        :rtype: :class:`tencentcloud.dlc.v20210125.models.DescribeMainDataOverviewLineResponse`

        """
        try:
            params = request._serialize()
            headers = request.headers
            body = self.call("DescribeMainDataOverviewLine", params, headers=headers)
            response = json.loads(body)
            model = models.DescribeMainDataOverviewLineResponse()
            model._deserialize(response["Response"])
            return model
        except Exception as e:
            if isinstance(e, TencentCloudSDKException):
                raise
            else:
                raise TencentCloudSDKException(e.message, e.message)


    def DescribeMainDataPrivateEngineLine(self, request):
        """首页，查看数据引擎-top2独享引擎折线图

        :param request: Request instance for DescribeMainDataPrivateEngineLine.
        :type request: :class:`tencentcloud.dlc.v20210125.models.DescribeMainDataPrivateEngineLineRequest`
        :rtype: :class:`tencentcloud.dlc.v20210125.models.DescribeMainDataPrivateEngineLineResponse`

        """
        try:
            params = request._serialize()
            headers = request.headers
            body = self.call("DescribeMainDataPrivateEngineLine", params, headers=headers)
            response = json.loads(body)
            model = models.DescribeMainDataPrivateEngineLineResponse()
            model._deserialize(response["Response"])
            return model
        except Exception as e:
            if isinstance(e, TencentCloudSDKException):
                raise
            else:
                raise TencentCloudSDKException(e.message, e.message)


    def DescribeMainDataShareEngineLine(self, request):
        """首页，查看数据引擎-共享引擎折线图

        :param request: Request instance for DescribeMainDataShareEngineLine.
        :type request: :class:`tencentcloud.dlc.v20210125.models.DescribeMainDataShareEngineLineRequest`
        :rtype: :class:`tencentcloud.dlc.v20210125.models.DescribeMainDataShareEngineLineResponse`

        """
        try:
            params = request._serialize()
            headers = request.headers
            body = self.call("DescribeMainDataShareEngineLine", params, headers=headers)
            response = json.loads(body)
            model = models.DescribeMainDataShareEngineLineResponse()
            model._deserialize(response["Response"])
            return model
        except Exception as e:
            if isinstance(e, TencentCloudSDKException):
                raise
            else:
                raise TencentCloudSDKException(e.message, e.message)


    def DescribeMainDataTaskLine(self, request):
        """首页，查看任务监控-折线图

        :param request: Request instance for DescribeMainDataTaskLine.
        :type request: :class:`tencentcloud.dlc.v20210125.models.DescribeMainDataTaskLineRequest`
        :rtype: :class:`tencentcloud.dlc.v20210125.models.DescribeMainDataTaskLineResponse`

        """
        try:
            params = request._serialize()
            headers = request.headers
            body = self.call("DescribeMainDataTaskLine", params, headers=headers)
            response = json.loads(body)
            model = models.DescribeMainDataTaskLineResponse()
            model._deserialize(response["Response"])
            return model
        except Exception as e:
            if isinstance(e, TencentCloudSDKException):
                raise
            else:
                raise TencentCloudSDKException(e.message, e.message)


    def DescribeMetaDatabase(self, request):
        """本接口（DescribeMetaDatabase），用于查询数据库详细信息

        :param request: Request instance for DescribeMetaDatabase.
        :type request: :class:`tencentcloud.dlc.v20210125.models.DescribeMetaDatabaseRequest`
        :rtype: :class:`tencentcloud.dlc.v20210125.models.DescribeMetaDatabaseResponse`

        """
        try:
            params = request._serialize()
            headers = request.headers
            body = self.call("DescribeMetaDatabase", params, headers=headers)
            response = json.loads(body)
            model = models.DescribeMetaDatabaseResponse()
            model._deserialize(response["Response"])
            return model
        except Exception as e:
            if isinstance(e, TencentCloudSDKException):
                raise
            else:
                raise TencentCloudSDKException(e.message, e.message)


    def DescribeMetaDatabases(self, request):
        """本接口（DescribeMetaDatabases）用于查询元数据库列表。

        :param request: Request instance for DescribeMetaDatabases.
        :type request: :class:`tencentcloud.dlc.v20210125.models.DescribeMetaDatabasesRequest`
        :rtype: :class:`tencentcloud.dlc.v20210125.models.DescribeMetaDatabasesResponse`

        """
        try:
            params = request._serialize()
            headers = request.headers
            body = self.call("DescribeMetaDatabases", params, headers=headers)
            response = json.loads(body)
            model = models.DescribeMetaDatabasesResponse()
            model._deserialize(response["Response"])
            return model
        except Exception as e:
            if isinstance(e, TencentCloudSDKException):
                raise
            else:
                raise TencentCloudSDKException(e.message, e.message)


    def DescribeMetaKeyConstraint(self, request):
        """查询元数据约束列表

        :param request: Request instance for DescribeMetaKeyConstraint.
        :type request: :class:`tencentcloud.dlc.v20210125.models.DescribeMetaKeyConstraintRequest`
        :rtype: :class:`tencentcloud.dlc.v20210125.models.DescribeMetaKeyConstraintResponse`

        """
        try:
            params = request._serialize()
            headers = request.headers
            body = self.call("DescribeMetaKeyConstraint", params, headers=headers)
            response = json.loads(body)
            model = models.DescribeMetaKeyConstraintResponse()
            model._deserialize(response["Response"])
            return model
        except Exception as e:
            if isinstance(e, TencentCloudSDKException):
                raise
            else:
                raise TencentCloudSDKException(e.message, e.message)


    def DescribeMetaTable(self, request):
        """本接口（DescribeMetaTable），用于查询元数据表详情

        :param request: Request instance for DescribeMetaTable.
        :type request: :class:`tencentcloud.dlc.v20210125.models.DescribeMetaTableRequest`
        :rtype: :class:`tencentcloud.dlc.v20210125.models.DescribeMetaTableResponse`

        """
        try:
            params = request._serialize()
            headers = request.headers
            body = self.call("DescribeMetaTable", params, headers=headers)
            response = json.loads(body)
            model = models.DescribeMetaTableResponse()
            model._deserialize(response["Response"])
            return model
        except Exception as e:
            if isinstance(e, TencentCloudSDKException):
                raise
            else:
                raise TencentCloudSDKException(e.message, e.message)


    def DescribeMetaTableInternal(self, request):
        """本接口（DescribeMetaTable），用于查询元数据表详情，该接口仅对内使用，区别：新增字段GetLocation，用于控制是否获取lakefs内表Location.

        :param request: Request instance for DescribeMetaTableInternal.
        :type request: :class:`tencentcloud.dlc.v20210125.models.DescribeMetaTableInternalRequest`
        :rtype: :class:`tencentcloud.dlc.v20210125.models.DescribeMetaTableInternalResponse`

        """
        try:
            params = request._serialize()
            headers = request.headers
            body = self.call("DescribeMetaTableInternal", params, headers=headers)
            response = json.loads(body)
            model = models.DescribeMetaTableInternalResponse()
            model._deserialize(response["Response"])
            return model
        except Exception as e:
            if isinstance(e, TencentCloudSDKException):
                raise
            else:
                raise TencentCloudSDKException(e.message, e.message)


    def DescribeMetaTables(self, request):
        """本接口（DescribeMetaTables）用于查询元数据表列表。

        :param request: Request instance for DescribeMetaTables.
        :type request: :class:`tencentcloud.dlc.v20210125.models.DescribeMetaTablesRequest`
        :rtype: :class:`tencentcloud.dlc.v20210125.models.DescribeMetaTablesResponse`

        """
        try:
            params = request._serialize()
            headers = request.headers
            body = self.call("DescribeMetaTables", params, headers=headers)
            response = json.loads(body)
            model = models.DescribeMetaTablesResponse()
            model._deserialize(response["Response"])
            return model
        except Exception as e:
            if isinstance(e, TencentCloudSDKException):
                raise
            else:
                raise TencentCloudSDKException(e.message, e.message)


    def DescribeMonitorObjects(self, request):
        """获取监控对象，满足云监控的配置需要

        :param request: Request instance for DescribeMonitorObjects.
        :type request: :class:`tencentcloud.dlc.v20210125.models.DescribeMonitorObjectsRequest`
        :rtype: :class:`tencentcloud.dlc.v20210125.models.DescribeMonitorObjectsResponse`

        """
        try:
            params = request._serialize()
            headers = request.headers
            body = self.call("DescribeMonitorObjects", params, headers=headers)
            response = json.loads(body)
            model = models.DescribeMonitorObjectsResponse()
            model._deserialize(response["Response"])
            return model
        except Exception as e:
            if isinstance(e, TencentCloudSDKException):
                raise
            else:
                raise TencentCloudSDKException(e.message, e.message)


    def DescribeNetworkConnections(self, request):
        """查询网络配置列表

        :param request: Request instance for DescribeNetworkConnections.
        :type request: :class:`tencentcloud.dlc.v20210125.models.DescribeNetworkConnectionsRequest`
        :rtype: :class:`tencentcloud.dlc.v20210125.models.DescribeNetworkConnectionsResponse`

        """
        try:
            params = request._serialize()
            headers = request.headers
            body = self.call("DescribeNetworkConnections", params, headers=headers)
            response = json.loads(body)
            model = models.DescribeNetworkConnectionsResponse()
            model._deserialize(response["Response"])
            return model
        except Exception as e:
            if isinstance(e, TencentCloudSDKException):
                raise
            else:
                raise TencentCloudSDKException(e.message, e.message)


    def DescribeNotebookSession(self, request):
        """本接口（DescribeNotebookSession）用于查询交互式 session详情信息

        :param request: Request instance for DescribeNotebookSession.
        :type request: :class:`tencentcloud.dlc.v20210125.models.DescribeNotebookSessionRequest`
        :rtype: :class:`tencentcloud.dlc.v20210125.models.DescribeNotebookSessionResponse`

        """
        try:
            params = request._serialize()
            headers = request.headers
            body = self.call("DescribeNotebookSession", params, headers=headers)
            response = json.loads(body)
            model = models.DescribeNotebookSessionResponse()
            model._deserialize(response["Response"])
            return model
        except Exception as e:
            if isinstance(e, TencentCloudSDKException):
                raise
            else:
                raise TencentCloudSDKException(e.message, e.message)


    def DescribeNotebookSessionLog(self, request):
        """本接口（DescribeNotebookSessionLog）用于查询交互式 session日志

        :param request: Request instance for DescribeNotebookSessionLog.
        :type request: :class:`tencentcloud.dlc.v20210125.models.DescribeNotebookSessionLogRequest`
        :rtype: :class:`tencentcloud.dlc.v20210125.models.DescribeNotebookSessionLogResponse`

        """
        try:
            params = request._serialize()
            headers = request.headers
            body = self.call("DescribeNotebookSessionLog", params, headers=headers)
            response = json.loads(body)
            model = models.DescribeNotebookSessionLogResponse()
            model._deserialize(response["Response"])
            return model
        except Exception as e:
            if isinstance(e, TencentCloudSDKException):
                raise
            else:
                raise TencentCloudSDKException(e.message, e.message)


    def DescribeNotebookSessionStatement(self, request):
        """本接口（DescribeNotebookSessionStatement）用于查询session 中执行任务的详情

        :param request: Request instance for DescribeNotebookSessionStatement.
        :type request: :class:`tencentcloud.dlc.v20210125.models.DescribeNotebookSessionStatementRequest`
        :rtype: :class:`tencentcloud.dlc.v20210125.models.DescribeNotebookSessionStatementResponse`

        """
        try:
            params = request._serialize()
            headers = request.headers
            body = self.call("DescribeNotebookSessionStatement", params, headers=headers)
            response = json.loads(body)
            model = models.DescribeNotebookSessionStatementResponse()
            model._deserialize(response["Response"])
            return model
        except Exception as e:
            if isinstance(e, TencentCloudSDKException):
                raise
            else:
                raise TencentCloudSDKException(e.message, e.message)


    def DescribeNotebookSessionStatementSqlResult(self, request):
        """本接口（DescribeNotebookSessionStatementSqlResult）用于获取statement运行结果。

        :param request: Request instance for DescribeNotebookSessionStatementSqlResult.
        :type request: :class:`tencentcloud.dlc.v20210125.models.DescribeNotebookSessionStatementSqlResultRequest`
        :rtype: :class:`tencentcloud.dlc.v20210125.models.DescribeNotebookSessionStatementSqlResultResponse`

        """
        try:
            params = request._serialize()
            headers = request.headers
            body = self.call("DescribeNotebookSessionStatementSqlResult", params, headers=headers)
            response = json.loads(body)
            model = models.DescribeNotebookSessionStatementSqlResultResponse()
            model._deserialize(response["Response"])
            return model
        except Exception as e:
            if isinstance(e, TencentCloudSDKException):
                raise
            else:
                raise TencentCloudSDKException(e.message, e.message)


    def DescribeNotebookSessionStatements(self, request):
        """本接口（DescribeNotebookSessionStatements）用于查询Session中执行的任务列表

        :param request: Request instance for DescribeNotebookSessionStatements.
        :type request: :class:`tencentcloud.dlc.v20210125.models.DescribeNotebookSessionStatementsRequest`
        :rtype: :class:`tencentcloud.dlc.v20210125.models.DescribeNotebookSessionStatementsResponse`

        """
        try:
            params = request._serialize()
            headers = request.headers
            body = self.call("DescribeNotebookSessionStatements", params, headers=headers)
            response = json.loads(body)
            model = models.DescribeNotebookSessionStatementsResponse()
            model._deserialize(response["Response"])
            return model
        except Exception as e:
            if isinstance(e, TencentCloudSDKException):
                raise
            else:
                raise TencentCloudSDKException(e.message, e.message)


    def DescribeNotebookSessions(self, request):
        """本接口（DescribeNotebookSessions）用于查询交互式 session列表

        :param request: Request instance for DescribeNotebookSessions.
        :type request: :class:`tencentcloud.dlc.v20210125.models.DescribeNotebookSessionsRequest`
        :rtype: :class:`tencentcloud.dlc.v20210125.models.DescribeNotebookSessionsResponse`

        """
        try:
            params = request._serialize()
            headers = request.headers
            body = self.call("DescribeNotebookSessions", params, headers=headers)
            response = json.loads(body)
            model = models.DescribeNotebookSessionsResponse()
            model._deserialize(response["Response"])
            return model
        except Exception as e:
            if isinstance(e, TencentCloudSDKException):
                raise
            else:
                raise TencentCloudSDKException(e.message, e.message)


    def DescribeOrCreateCHDFSAccessGroups(self, request):
        """查询或创建CHDFS权限组

        :param request: Request instance for DescribeOrCreateCHDFSAccessGroups.
        :type request: :class:`tencentcloud.dlc.v20210125.models.DescribeOrCreateCHDFSAccessGroupsRequest`
        :rtype: :class:`tencentcloud.dlc.v20210125.models.DescribeOrCreateCHDFSAccessGroupsResponse`

        """
        try:
            params = request._serialize()
            headers = request.headers
            body = self.call("DescribeOrCreateCHDFSAccessGroups", params, headers=headers)
            response = json.loads(body)
            model = models.DescribeOrCreateCHDFSAccessGroupsResponse()
            model._deserialize(response["Response"])
            return model
        except Exception as e:
            if isinstance(e, TencentCloudSDKException):
                raise
            else:
                raise TencentCloudSDKException(e.message, e.message)


    def DescribeOtherCHDFSBindingList(self, request):
        """此接口（DescribeOtherCHDFSBindingList）用于查询其他产品元数据加速桶绑定列表

        :param request: Request instance for DescribeOtherCHDFSBindingList.
        :type request: :class:`tencentcloud.dlc.v20210125.models.DescribeOtherCHDFSBindingListRequest`
        :rtype: :class:`tencentcloud.dlc.v20210125.models.DescribeOtherCHDFSBindingListResponse`

        """
        try:
            params = request._serialize()
            headers = request.headers
            body = self.call("DescribeOtherCHDFSBindingList", params, headers=headers)
            response = json.loads(body)
            model = models.DescribeOtherCHDFSBindingListResponse()
            model._deserialize(response["Response"])
            return model
        except Exception as e:
            if isinstance(e, TencentCloudSDKException):
                raise
            else:
                raise TencentCloudSDKException(e.message, e.message)


    def DescribeQueryDir(self, request):
        """查询数据目录

        :param request: Request instance for DescribeQueryDir.
        :type request: :class:`tencentcloud.dlc.v20210125.models.DescribeQueryDirRequest`
        :rtype: :class:`tencentcloud.dlc.v20210125.models.DescribeQueryDirResponse`

        """
        try:
            params = request._serialize()
            headers = request.headers
            body = self.call("DescribeQueryDir", params, headers=headers)
            response = json.loads(body)
            model = models.DescribeQueryDirResponse()
            model._deserialize(response["Response"])
            return model
        except Exception as e:
            if isinstance(e, TencentCloudSDKException):
                raise
            else:
                raise TencentCloudSDKException(e.message, e.message)


    def DescribeQueryDirs(self, request):
        """列举数据目录

        :param request: Request instance for DescribeQueryDirs.
        :type request: :class:`tencentcloud.dlc.v20210125.models.DescribeQueryDirsRequest`
        :rtype: :class:`tencentcloud.dlc.v20210125.models.DescribeQueryDirsResponse`

        """
        try:
            params = request._serialize()
            headers = request.headers
            body = self.call("DescribeQueryDirs", params, headers=headers)
            response = json.loads(body)
            model = models.DescribeQueryDirsResponse()
            model._deserialize(response["Response"])
            return model
        except Exception as e:
            if isinstance(e, TencentCloudSDKException):
                raise
            else:
                raise TencentCloudSDKException(e.message, e.message)


    def DescribeQueue(self, request):
        """获取计算集群信息

        :param request: Request instance for DescribeQueue.
        :type request: :class:`tencentcloud.dlc.v20210125.models.DescribeQueueRequest`
        :rtype: :class:`tencentcloud.dlc.v20210125.models.DescribeQueueResponse`

        """
        try:
            params = request._serialize()
            headers = request.headers
            body = self.call("DescribeQueue", params, headers=headers)
            response = json.loads(body)
            model = models.DescribeQueueResponse()
            model._deserialize(response["Response"])
            return model
        except Exception as e:
            if isinstance(e, TencentCloudSDKException):
                raise
            else:
                raise TencentCloudSDKException(e.message, e.message)


    def DescribeRegion(self, request):
        """获取可用的地域信息

        :param request: Request instance for DescribeRegion.
        :type request: :class:`tencentcloud.dlc.v20210125.models.DescribeRegionRequest`
        :rtype: :class:`tencentcloud.dlc.v20210125.models.DescribeRegionResponse`

        """
        try:
            params = request._serialize()
            headers = request.headers
            body = self.call("DescribeRegion", params, headers=headers)
            response = json.loads(body)
            model = models.DescribeRegionResponse()
            model._deserialize(response["Response"])
            return model
        except Exception as e:
            if isinstance(e, TencentCloudSDKException):
                raise
            else:
                raise TencentCloudSDKException(e.message, e.message)


    def DescribeResultDownload(self, request):
        """查询结果下载任务

        :param request: Request instance for DescribeResultDownload.
        :type request: :class:`tencentcloud.dlc.v20210125.models.DescribeResultDownloadRequest`
        :rtype: :class:`tencentcloud.dlc.v20210125.models.DescribeResultDownloadResponse`

        """
        try:
            params = request._serialize()
            headers = request.headers
            body = self.call("DescribeResultDownload", params, headers=headers)
            response = json.loads(body)
            model = models.DescribeResultDownloadResponse()
            model._deserialize(response["Response"])
            return model
        except Exception as e:
            if isinstance(e, TencentCloudSDKException):
                raise
            else:
                raise TencentCloudSDKException(e.message, e.message)


    def DescribeResultDownloadInfo(self, request):
        """本接口（DescribeResultDownloadInfo）用于获取SQL查询结果下载信息

        :param request: Request instance for DescribeResultDownloadInfo.
        :type request: :class:`tencentcloud.dlc.v20210125.models.DescribeResultDownloadInfoRequest`
        :rtype: :class:`tencentcloud.dlc.v20210125.models.DescribeResultDownloadInfoResponse`

        """
        try:
            params = request._serialize()
            headers = request.headers
            body = self.call("DescribeResultDownloadInfo", params, headers=headers)
            response = json.loads(body)
            model = models.DescribeResultDownloadInfoResponse()
            model._deserialize(response["Response"])
            return model
        except Exception as e:
            if isinstance(e, TencentCloudSDKException):
                raise
            else:
                raise TencentCloudSDKException(e.message, e.message)


    def DescribeResultSize(self, request):
        """本接口（DescribeResultSize）用于查询SQL结果数据大小

        :param request: Request instance for DescribeResultSize.
        :type request: :class:`tencentcloud.dlc.v20210125.models.DescribeResultSizeRequest`
        :rtype: :class:`tencentcloud.dlc.v20210125.models.DescribeResultSizeResponse`

        """
        try:
            params = request._serialize()
            headers = request.headers
            body = self.call("DescribeResultSize", params, headers=headers)
            response = json.loads(body)
            model = models.DescribeResultSizeResponse()
            model._deserialize(response["Response"])
            return model
        except Exception as e:
            if isinstance(e, TencentCloudSDKException):
                raise
            else:
                raise TencentCloudSDKException(e.message, e.message)


    def DescribeSQLSessionCatalog(self, request):
        """本接口（DescribeSQLSessionCatalog）用于获取会话目录列表

        :param request: Request instance for DescribeSQLSessionCatalog.
        :type request: :class:`tencentcloud.dlc.v20210125.models.DescribeSQLSessionCatalogRequest`
        :rtype: :class:`tencentcloud.dlc.v20210125.models.DescribeSQLSessionCatalogResponse`

        """
        try:
            params = request._serialize()
            headers = request.headers
            body = self.call("DescribeSQLSessionCatalog", params, headers=headers)
            response = json.loads(body)
            model = models.DescribeSQLSessionCatalogResponse()
            model._deserialize(response["Response"])
            return model
        except Exception as e:
            if isinstance(e, TencentCloudSDKException):
                raise
            else:
                raise TencentCloudSDKException(e.message, e.message)


    def DescribeSQLSessionSnapshot(self, request):
        """本接口（DescribeSQLSessionSnapshots）用于获取SQL会话详情

        :param request: Request instance for DescribeSQLSessionSnapshot.
        :type request: :class:`tencentcloud.dlc.v20210125.models.DescribeSQLSessionSnapshotRequest`
        :rtype: :class:`tencentcloud.dlc.v20210125.models.DescribeSQLSessionSnapshotResponse`

        """
        try:
            params = request._serialize()
            headers = request.headers
            body = self.call("DescribeSQLSessionSnapshot", params, headers=headers)
            response = json.loads(body)
            model = models.DescribeSQLSessionSnapshotResponse()
            model._deserialize(response["Response"])
            return model
        except Exception as e:
            if isinstance(e, TencentCloudSDKException):
                raise
            else:
                raise TencentCloudSDKException(e.message, e.message)


    def DescribeSQLSessionSnapshots(self, request):
        """本接口（DescribeSQLSessionSnapshots）用于获取SQL会话快照列表

        :param request: Request instance for DescribeSQLSessionSnapshots.
        :type request: :class:`tencentcloud.dlc.v20210125.models.DescribeSQLSessionSnapshotsRequest`
        :rtype: :class:`tencentcloud.dlc.v20210125.models.DescribeSQLSessionSnapshotsResponse`

        """
        try:
            params = request._serialize()
            headers = request.headers
            body = self.call("DescribeSQLSessionSnapshots", params, headers=headers)
            response = json.loads(body)
            model = models.DescribeSQLSessionSnapshotsResponse()
            model._deserialize(response["Response"])
            return model
        except Exception as e:
            if isinstance(e, TencentCloudSDKException):
                raise
            else:
                raise TencentCloudSDKException(e.message, e.message)


    def DescribeSQLSessionSubmitRecords(self, request):
        """本接口（DescribeSQLSessionSubmitRecords）用于获取SQL会话提交记录列表

        :param request: Request instance for DescribeSQLSessionSubmitRecords.
        :type request: :class:`tencentcloud.dlc.v20210125.models.DescribeSQLSessionSubmitRecordsRequest`
        :rtype: :class:`tencentcloud.dlc.v20210125.models.DescribeSQLSessionSubmitRecordsResponse`

        """
        try:
            params = request._serialize()
            headers = request.headers
            body = self.call("DescribeSQLSessionSubmitRecords", params, headers=headers)
            response = json.loads(body)
            model = models.DescribeSQLSessionSubmitRecordsResponse()
            model._deserialize(response["Response"])
            return model
        except Exception as e:
            if isinstance(e, TencentCloudSDKException):
                raise
            else:
                raise TencentCloudSDKException(e.message, e.message)


    def DescribeScheduleExecutionInfo(self, request):
        """预览调度执行信息

        :param request: Request instance for DescribeScheduleExecutionInfo.
        :type request: :class:`tencentcloud.dlc.v20210125.models.DescribeScheduleExecutionInfoRequest`
        :rtype: :class:`tencentcloud.dlc.v20210125.models.DescribeScheduleExecutionInfoResponse`

        """
        try:
            params = request._serialize()
            headers = request.headers
            body = self.call("DescribeScheduleExecutionInfo", params, headers=headers)
            response = json.loads(body)
            model = models.DescribeScheduleExecutionInfoResponse()
            model._deserialize(response["Response"])
            return model
        except Exception as e:
            if isinstance(e, TencentCloudSDKException):
                raise
            else:
                raise TencentCloudSDKException(e.message, e.message)


    def DescribeScheduleTaskInstances(self, request):
        """调度任务实例列表

        :param request: Request instance for DescribeScheduleTaskInstances.
        :type request: :class:`tencentcloud.dlc.v20210125.models.DescribeScheduleTaskInstancesRequest`
        :rtype: :class:`tencentcloud.dlc.v20210125.models.DescribeScheduleTaskInstancesResponse`

        """
        try:
            params = request._serialize()
            headers = request.headers
            body = self.call("DescribeScheduleTaskInstances", params, headers=headers)
            response = json.loads(body)
            model = models.DescribeScheduleTaskInstancesResponse()
            model._deserialize(response["Response"])
            return model
        except Exception as e:
            if isinstance(e, TencentCloudSDKException):
                raise
            else:
                raise TencentCloudSDKException(e.message, e.message)


    def DescribeScheduleTasks(self, request):
        """调度任务列表

        :param request: Request instance for DescribeScheduleTasks.
        :type request: :class:`tencentcloud.dlc.v20210125.models.DescribeScheduleTasksRequest`
        :rtype: :class:`tencentcloud.dlc.v20210125.models.DescribeScheduleTasksResponse`

        """
        try:
            params = request._serialize()
            headers = request.headers
            body = self.call("DescribeScheduleTasks", params, headers=headers)
            response = json.loads(body)
            model = models.DescribeScheduleTasksResponse()
            model._deserialize(response["Response"])
            return model
        except Exception as e:
            if isinstance(e, TencentCloudSDKException):
                raise
            else:
                raise TencentCloudSDKException(e.message, e.message)


    def DescribeScripts(self, request):
        """该接口（DescribeScripts）用于查询SQL脚本列表

        :param request: Request instance for DescribeScripts.
        :type request: :class:`tencentcloud.dlc.v20210125.models.DescribeScriptsRequest`
        :rtype: :class:`tencentcloud.dlc.v20210125.models.DescribeScriptsResponse`

        """
        try:
            params = request._serialize()
            headers = request.headers
            body = self.call("DescribeScripts", params, headers=headers)
            response = json.loads(body)
            model = models.DescribeScriptsResponse()
            model._deserialize(response["Response"])
            return model
        except Exception as e:
            if isinstance(e, TencentCloudSDKException):
                raise
            else:
                raise TencentCloudSDKException(e.message, e.message)


    def DescribeSparkAppJob(self, request):
        """查询spark作业信息

        :param request: Request instance for DescribeSparkAppJob.
        :type request: :class:`tencentcloud.dlc.v20210125.models.DescribeSparkAppJobRequest`
        :rtype: :class:`tencentcloud.dlc.v20210125.models.DescribeSparkAppJobResponse`

        """
        try:
            params = request._serialize()
            headers = request.headers
            body = self.call("DescribeSparkAppJob", params, headers=headers)
            response = json.loads(body)
            model = models.DescribeSparkAppJobResponse()
            model._deserialize(response["Response"])
            return model
        except Exception as e:
            if isinstance(e, TencentCloudSDKException):
                raise
            else:
                raise TencentCloudSDKException(e.message, e.message)


    def DescribeSparkAppJobImages(self, request):
        """获取Spark App任务镜像列表

        :param request: Request instance for DescribeSparkAppJobImages.
        :type request: :class:`tencentcloud.dlc.v20210125.models.DescribeSparkAppJobImagesRequest`
        :rtype: :class:`tencentcloud.dlc.v20210125.models.DescribeSparkAppJobImagesResponse`

        """
        try:
            params = request._serialize()
            headers = request.headers
            body = self.call("DescribeSparkAppJobImages", params, headers=headers)
            response = json.loads(body)
            model = models.DescribeSparkAppJobImagesResponse()
            model._deserialize(response["Response"])
            return model
        except Exception as e:
            if isinstance(e, TencentCloudSDKException):
                raise
            else:
                raise TencentCloudSDKException(e.message, e.message)


    def DescribeSparkAppJobUserInfo(self, request):
        """本接口（DescribeSparkAppJobUserInfo），用于获取获取spark任务的用户信息

        :param request: Request instance for DescribeSparkAppJobUserInfo.
        :type request: :class:`tencentcloud.dlc.v20210125.models.DescribeSparkAppJobUserInfoRequest`
        :rtype: :class:`tencentcloud.dlc.v20210125.models.DescribeSparkAppJobUserInfoResponse`

        """
        try:
            params = request._serialize()
            headers = request.headers
            body = self.call("DescribeSparkAppJobUserInfo", params, headers=headers)
            response = json.loads(body)
            model = models.DescribeSparkAppJobUserInfoResponse()
            model._deserialize(response["Response"])
            return model
        except Exception as e:
            if isinstance(e, TencentCloudSDKException):
                raise
            else:
                raise TencentCloudSDKException(e.message, e.message)


    def DescribeSparkAppJobs(self, request):
        """查询spark作业列表

        :param request: Request instance for DescribeSparkAppJobs.
        :type request: :class:`tencentcloud.dlc.v20210125.models.DescribeSparkAppJobsRequest`
        :rtype: :class:`tencentcloud.dlc.v20210125.models.DescribeSparkAppJobsResponse`

        """
        try:
            params = request._serialize()
            headers = request.headers
            body = self.call("DescribeSparkAppJobs", params, headers=headers)
            response = json.loads(body)
            model = models.DescribeSparkAppJobsResponse()
            model._deserialize(response["Response"])
            return model
        except Exception as e:
            if isinstance(e, TencentCloudSDKException):
                raise
            else:
                raise TencentCloudSDKException(e.message, e.message)


    def DescribeSparkAppTasks(self, request):
        """查询Spark作业的运行任务列表

        :param request: Request instance for DescribeSparkAppTasks.
        :type request: :class:`tencentcloud.dlc.v20210125.models.DescribeSparkAppTasksRequest`
        :rtype: :class:`tencentcloud.dlc.v20210125.models.DescribeSparkAppTasksResponse`

        """
        try:
            params = request._serialize()
            headers = request.headers
            body = self.call("DescribeSparkAppTasks", params, headers=headers)
            response = json.loads(body)
            model = models.DescribeSparkAppTasksResponse()
            model._deserialize(response["Response"])
            return model
        except Exception as e:
            if isinstance(e, TencentCloudSDKException):
                raise
            else:
                raise TencentCloudSDKException(e.message, e.message)


    def DescribeSparkSessionBatchSqlLog(self, request):
        """本接口（DescribeSparkSessionBatchSqlLog）用于查询Spark SQL批任务日志

        :param request: Request instance for DescribeSparkSessionBatchSqlLog.
        :type request: :class:`tencentcloud.dlc.v20210125.models.DescribeSparkSessionBatchSqlLogRequest`
        :rtype: :class:`tencentcloud.dlc.v20210125.models.DescribeSparkSessionBatchSqlLogResponse`

        """
        try:
            params = request._serialize()
            headers = request.headers
            body = self.call("DescribeSparkSessionBatchSqlLog", params, headers=headers)
            response = json.loads(body)
            model = models.DescribeSparkSessionBatchSqlLogResponse()
            model._deserialize(response["Response"])
            return model
        except Exception as e:
            if isinstance(e, TencentCloudSDKException):
                raise
            else:
                raise TencentCloudSDKException(e.message, e.message)


    def DescribeSparkSessionBatchSqlTasks(self, request):
        """本接口（DescribeSparkSessionBatchSqlTasks）用于获取SparkSQL批任务运行列表。

        :param request: Request instance for DescribeSparkSessionBatchSqlTasks.
        :type request: :class:`tencentcloud.dlc.v20210125.models.DescribeSparkSessionBatchSqlTasksRequest`
        :rtype: :class:`tencentcloud.dlc.v20210125.models.DescribeSparkSessionBatchSqlTasksResponse`

        """
        try:
            params = request._serialize()
            headers = request.headers
            body = self.call("DescribeSparkSessionBatchSqlTasks", params, headers=headers)
            response = json.loads(body)
            model = models.DescribeSparkSessionBatchSqlTasksResponse()
            model._deserialize(response["Response"])
            return model
        except Exception as e:
            if isinstance(e, TencentCloudSDKException):
                raise
            else:
                raise TencentCloudSDKException(e.message, e.message)


    def DescribeSparkTaskLogDownloadInfo(self, request):
        """查询spark任务日志下载信息

        :param request: Request instance for DescribeSparkTaskLogDownloadInfo.
        :type request: :class:`tencentcloud.dlc.v20210125.models.DescribeSparkTaskLogDownloadInfoRequest`
        :rtype: :class:`tencentcloud.dlc.v20210125.models.DescribeSparkTaskLogDownloadInfoResponse`

        """
        try:
            params = request._serialize()
            headers = request.headers
            body = self.call("DescribeSparkTaskLogDownloadInfo", params, headers=headers)
            response = json.loads(body)
            model = models.DescribeSparkTaskLogDownloadInfoResponse()
            model._deserialize(response["Response"])
            return model
        except Exception as e:
            if isinstance(e, TencentCloudSDKException):
                raise
            else:
                raise TencentCloudSDKException(e.message, e.message)


    def DescribeSparkUiUrl(self, request):
        """查询具体任务的spark ui url

        :param request: Request instance for DescribeSparkUiUrl.
        :type request: :class:`tencentcloud.dlc.v20210125.models.DescribeSparkUiUrlRequest`
        :rtype: :class:`tencentcloud.dlc.v20210125.models.DescribeSparkUiUrlResponse`

        """
        try:
            params = request._serialize()
            headers = request.headers
            body = self.call("DescribeSparkUiUrl", params, headers=headers)
            response = json.loads(body)
            model = models.DescribeSparkUiUrlResponse()
            model._deserialize(response["Response"])
            return model
        except Exception as e:
            if isinstance(e, TencentCloudSDKException):
                raise
            else:
                raise TencentCloudSDKException(e.message, e.message)


    def DescribeStandbyDataEngine(self, request):
        """查询备用集群

        :param request: Request instance for DescribeStandbyDataEngine.
        :type request: :class:`tencentcloud.dlc.v20210125.models.DescribeStandbyDataEngineRequest`
        :rtype: :class:`tencentcloud.dlc.v20210125.models.DescribeStandbyDataEngineResponse`

        """
        try:
            params = request._serialize()
            headers = request.headers
            body = self.call("DescribeStandbyDataEngine", params, headers=headers)
            response = json.loads(body)
            model = models.DescribeStandbyDataEngineResponse()
            model._deserialize(response["Response"])
            return model
        except Exception as e:
            if isinstance(e, TencentCloudSDKException):
                raise
            else:
                raise TencentCloudSDKException(e.message, e.message)


    def DescribeStoreLocation(self, request):
        """查询计算结果存储位置。

        :param request: Request instance for DescribeStoreLocation.
        :type request: :class:`tencentcloud.dlc.v20210125.models.DescribeStoreLocationRequest`
        :rtype: :class:`tencentcloud.dlc.v20210125.models.DescribeStoreLocationResponse`

        """
        try:
            params = request._serialize()
            headers = request.headers
            body = self.call("DescribeStoreLocation", params, headers=headers)
            response = json.loads(body)
            model = models.DescribeStoreLocationResponse()
            model._deserialize(response["Response"])
            return model
        except Exception as e:
            if isinstance(e, TencentCloudSDKException):
                raise
            else:
                raise TencentCloudSDKException(e.message, e.message)


    def DescribeSubUsers(self, request):
        """查询主用户下所有用户信息

        :param request: Request instance for DescribeSubUsers.
        :type request: :class:`tencentcloud.dlc.v20210125.models.DescribeSubUsersRequest`
        :rtype: :class:`tencentcloud.dlc.v20210125.models.DescribeSubUsersResponse`

        """
        try:
            params = request._serialize()
            headers = request.headers
            body = self.call("DescribeSubUsers", params, headers=headers)
            response = json.loads(body)
            model = models.DescribeSubUsersResponse()
            model._deserialize(response["Response"])
            return model
        except Exception as e:
            if isinstance(e, TencentCloudSDKException):
                raise
            else:
                raise TencentCloudSDKException(e.message, e.message)


    def DescribeSubuins(self, request):
        """获得appid下所有子uin

        :param request: Request instance for DescribeSubuins.
        :type request: :class:`tencentcloud.dlc.v20210125.models.DescribeSubuinsRequest`
        :rtype: :class:`tencentcloud.dlc.v20210125.models.DescribeSubuinsResponse`

        """
        try:
            params = request._serialize()
            headers = request.headers
            body = self.call("DescribeSubuins", params, headers=headers)
            response = json.loads(body)
            model = models.DescribeSubuinsResponse()
            model._deserialize(response["Response"])
            return model
        except Exception as e:
            if isinstance(e, TencentCloudSDKException):
                raise
            else:
                raise TencentCloudSDKException(e.message, e.message)


    def DescribeSystemStorage(self, request):
        """查询指定的托管存储的系统目录

        :param request: Request instance for DescribeSystemStorage.
        :type request: :class:`tencentcloud.dlc.v20210125.models.DescribeSystemStorageRequest`
        :rtype: :class:`tencentcloud.dlc.v20210125.models.DescribeSystemStorageResponse`

        """
        try:
            params = request._serialize()
            headers = request.headers
            body = self.call("DescribeSystemStorage", params, headers=headers)
            response = json.loads(body)
            model = models.DescribeSystemStorageResponse()
            model._deserialize(response["Response"])
            return model
        except Exception as e:
            if isinstance(e, TencentCloudSDKException):
                raise
            else:
                raise TencentCloudSDKException(e.message, e.message)


    def DescribeTable(self, request):
        """本接口（DescribeTable），用于查询单个表的详细信息。

        :param request: Request instance for DescribeTable.
        :type request: :class:`tencentcloud.dlc.v20210125.models.DescribeTableRequest`
        :rtype: :class:`tencentcloud.dlc.v20210125.models.DescribeTableResponse`

        """
        try:
            params = request._serialize()
            headers = request.headers
            body = self.call("DescribeTable", params, headers=headers)
            response = json.loads(body)
            model = models.DescribeTableResponse()
            model._deserialize(response["Response"])
            return model
        except Exception as e:
            if isinstance(e, TencentCloudSDKException):
                raise
            else:
                raise TencentCloudSDKException(e.message, e.message)


    def DescribeTables(self, request):
        """本接口（DescribeTables）用于查询数据表列表。

        :param request: Request instance for DescribeTables.
        :type request: :class:`tencentcloud.dlc.v20210125.models.DescribeTablesRequest`
        :rtype: :class:`tencentcloud.dlc.v20210125.models.DescribeTablesResponse`

        """
        try:
            params = request._serialize()
            headers = request.headers
            body = self.call("DescribeTables", params, headers=headers)
            response = json.loads(body)
            model = models.DescribeTablesResponse()
            model._deserialize(response["Response"])
            return model
        except Exception as e:
            if isinstance(e, TencentCloudSDKException):
                raise
            else:
                raise TencentCloudSDKException(e.message, e.message)


    def DescribeTablesExtend(self, request):
        """本接口（DescribleTablesExtend）用于查询多个数据库下的数据表列表（内部用接口，请勿开放到外网）

        :param request: Request instance for DescribeTablesExtend.
        :type request: :class:`tencentcloud.dlc.v20210125.models.DescribeTablesExtendRequest`
        :rtype: :class:`tencentcloud.dlc.v20210125.models.DescribeTablesExtendResponse`

        """
        try:
            params = request._serialize()
            headers = request.headers
            body = self.call("DescribeTablesExtend", params, headers=headers)
            response = json.loads(body)
            model = models.DescribeTablesExtendResponse()
            model._deserialize(response["Response"])
            return model
        except Exception as e:
            if isinstance(e, TencentCloudSDKException):
                raise
            else:
                raise TencentCloudSDKException(e.message, e.message)


    def DescribeTaskMetrics(self, request):
        """此接口（DescribeTaskMetrics）用于查询任务统计指标

        :param request: Request instance for DescribeTaskMetrics.
        :type request: :class:`tencentcloud.dlc.v20210125.models.DescribeTaskMetricsRequest`
        :rtype: :class:`tencentcloud.dlc.v20210125.models.DescribeTaskMetricsResponse`

        """
        try:
            params = request._serialize()
            headers = request.headers
            body = self.call("DescribeTaskMetrics", params, headers=headers)
            response = json.loads(body)
            model = models.DescribeTaskMetricsResponse()
            model._deserialize(response["Response"])
            return model
        except Exception as e:
            if isinstance(e, TencentCloudSDKException):
                raise
            else:
                raise TencentCloudSDKException(e.message, e.message)


    def DescribeTaskResult(self, request):
        """查询任务结果

        :param request: Request instance for DescribeTaskResult.
        :type request: :class:`tencentcloud.dlc.v20210125.models.DescribeTaskResultRequest`
        :rtype: :class:`tencentcloud.dlc.v20210125.models.DescribeTaskResultResponse`

        """
        try:
            params = request._serialize()
            headers = request.headers
            body = self.call("DescribeTaskResult", params, headers=headers)
            response = json.loads(body)
            model = models.DescribeTaskResultResponse()
            model._deserialize(response["Response"])
            return model
        except Exception as e:
            if isinstance(e, TencentCloudSDKException):
                raise
            else:
                raise TencentCloudSDKException(e.message, e.message)


    def DescribeTasks(self, request):
        """该接口（DescribleTasks）用于查询任务列表

        :param request: Request instance for DescribeTasks.
        :type request: :class:`tencentcloud.dlc.v20210125.models.DescribeTasksRequest`
        :rtype: :class:`tencentcloud.dlc.v20210125.models.DescribeTasksResponse`

        """
        try:
            params = request._serialize()
            headers = request.headers
            body = self.call("DescribeTasks", params, headers=headers)
            response = json.loads(body)
            model = models.DescribeTasksResponse()
            model._deserialize(response["Response"])
            return model
        except Exception as e:
            if isinstance(e, TencentCloudSDKException):
                raise
            else:
                raise TencentCloudSDKException(e.message, e.message)


    def DescribeTasksOverview(self, request):
        """查看任务概览页

        :param request: Request instance for DescribeTasksOverview.
        :type request: :class:`tencentcloud.dlc.v20210125.models.DescribeTasksOverviewRequest`
        :rtype: :class:`tencentcloud.dlc.v20210125.models.DescribeTasksOverviewResponse`

        """
        try:
            params = request._serialize()
            headers = request.headers
            body = self.call("DescribeTasksOverview", params, headers=headers)
            response = json.loads(body)
            model = models.DescribeTasksOverviewResponse()
            model._deserialize(response["Response"])
            return model
        except Exception as e:
            if isinstance(e, TencentCloudSDKException):
                raise
            else:
                raise TencentCloudSDKException(e.message, e.message)


    def DescribeUpdatableDataEngines(self, request):
        """查询可更新配置的引擎列表

        :param request: Request instance for DescribeUpdatableDataEngines.
        :type request: :class:`tencentcloud.dlc.v20210125.models.DescribeUpdatableDataEnginesRequest`
        :rtype: :class:`tencentcloud.dlc.v20210125.models.DescribeUpdatableDataEnginesResponse`

        """
        try:
            params = request._serialize()
            headers = request.headers
            body = self.call("DescribeUpdatableDataEngines", params, headers=headers)
            response = json.loads(body)
            model = models.DescribeUpdatableDataEnginesResponse()
            model._deserialize(response["Response"])
            return model
        except Exception as e:
            if isinstance(e, TencentCloudSDKException):
                raise
            else:
                raise TencentCloudSDKException(e.message, e.message)


    def DescribeUserDataEngineConfig(self, request):
        """查询用户自定义引擎参数

        :param request: Request instance for DescribeUserDataEngineConfig.
        :type request: :class:`tencentcloud.dlc.v20210125.models.DescribeUserDataEngineConfigRequest`
        :rtype: :class:`tencentcloud.dlc.v20210125.models.DescribeUserDataEngineConfigResponse`

        """
        try:
            params = request._serialize()
            headers = request.headers
            body = self.call("DescribeUserDataEngineConfig", params, headers=headers)
            response = json.loads(body)
            model = models.DescribeUserDataEngineConfigResponse()
            model._deserialize(response["Response"])
            return model
        except Exception as e:
            if isinstance(e, TencentCloudSDKException):
                raise
            else:
                raise TencentCloudSDKException(e.message, e.message)


    def DescribeUserInfo(self, request):
        """获取用户详细信息

        :param request: Request instance for DescribeUserInfo.
        :type request: :class:`tencentcloud.dlc.v20210125.models.DescribeUserInfoRequest`
        :rtype: :class:`tencentcloud.dlc.v20210125.models.DescribeUserInfoResponse`

        """
        try:
            params = request._serialize()
            headers = request.headers
            body = self.call("DescribeUserInfo", params, headers=headers)
            response = json.loads(body)
            model = models.DescribeUserInfoResponse()
            model._deserialize(response["Response"])
            return model
        except Exception as e:
            if isinstance(e, TencentCloudSDKException):
                raise
            else:
                raise TencentCloudSDKException(e.message, e.message)


    def DescribeUserRoles(self, request):
        """列举用户角色信息

        :param request: Request instance for DescribeUserRoles.
        :type request: :class:`tencentcloud.dlc.v20210125.models.DescribeUserRolesRequest`
        :rtype: :class:`tencentcloud.dlc.v20210125.models.DescribeUserRolesResponse`

        """
        try:
            params = request._serialize()
            headers = request.headers
            body = self.call("DescribeUserRoles", params, headers=headers)
            response = json.loads(body)
            model = models.DescribeUserRolesResponse()
            model._deserialize(response["Response"])
            return model
        except Exception as e:
            if isinstance(e, TencentCloudSDKException):
                raise
            else:
                raise TencentCloudSDKException(e.message, e.message)


    def DescribeUserType(self, request):
        """获取用户类型

        :param request: Request instance for DescribeUserType.
        :type request: :class:`tencentcloud.dlc.v20210125.models.DescribeUserTypeRequest`
        :rtype: :class:`tencentcloud.dlc.v20210125.models.DescribeUserTypeResponse`

        """
        try:
            params = request._serialize()
            headers = request.headers
            body = self.call("DescribeUserType", params, headers=headers)
            response = json.loads(body)
            model = models.DescribeUserTypeResponse()
            model._deserialize(response["Response"])
            return model
        except Exception as e:
            if isinstance(e, TencentCloudSDKException):
                raise
            else:
                raise TencentCloudSDKException(e.message, e.message)


    def DescribeUserUseScene(self, request):
        """查询用户使用场景

        :param request: Request instance for DescribeUserUseScene.
        :type request: :class:`tencentcloud.dlc.v20210125.models.DescribeUserUseSceneRequest`
        :rtype: :class:`tencentcloud.dlc.v20210125.models.DescribeUserUseSceneResponse`

        """
        try:
            params = request._serialize()
            headers = request.headers
            body = self.call("DescribeUserUseScene", params, headers=headers)
            response = json.loads(body)
            model = models.DescribeUserUseSceneResponse()
            model._deserialize(response["Response"])
            return model
        except Exception as e:
            if isinstance(e, TencentCloudSDKException):
                raise
            else:
                raise TencentCloudSDKException(e.message, e.message)


    def DescribeUsers(self, request):
        """获取用户列表信息

        :param request: Request instance for DescribeUsers.
        :type request: :class:`tencentcloud.dlc.v20210125.models.DescribeUsersRequest`
        :rtype: :class:`tencentcloud.dlc.v20210125.models.DescribeUsersResponse`

        """
        try:
            params = request._serialize()
            headers = request.headers
            body = self.call("DescribeUsers", params, headers=headers)
            response = json.loads(body)
            model = models.DescribeUsersResponse()
            model._deserialize(response["Response"])
            return model
        except Exception as e:
            if isinstance(e, TencentCloudSDKException):
                raise
            else:
                raise TencentCloudSDKException(e.message, e.message)


    def DescribeView(self, request):
        """获取指定视图信息

        :param request: Request instance for DescribeView.
        :type request: :class:`tencentcloud.dlc.v20210125.models.DescribeViewRequest`
        :rtype: :class:`tencentcloud.dlc.v20210125.models.DescribeViewResponse`

        """
        try:
            params = request._serialize()
            headers = request.headers
            body = self.call("DescribeView", params, headers=headers)
            response = json.loads(body)
            model = models.DescribeViewResponse()
            model._deserialize(response["Response"])
            return model
        except Exception as e:
            if isinstance(e, TencentCloudSDKException):
                raise
            else:
                raise TencentCloudSDKException(e.message, e.message)


    def DescribeViews(self, request):
        """本接口（DescribeViews）用于查询数据视图列表。

        :param request: Request instance for DescribeViews.
        :type request: :class:`tencentcloud.dlc.v20210125.models.DescribeViewsRequest`
        :rtype: :class:`tencentcloud.dlc.v20210125.models.DescribeViewsResponse`

        """
        try:
            params = request._serialize()
            headers = request.headers
            body = self.call("DescribeViews", params, headers=headers)
            response = json.loads(body)
            model = models.DescribeViewsResponse()
            model._deserialize(response["Response"])
            return model
        except Exception as e:
            if isinstance(e, TencentCloudSDKException):
                raise
            else:
                raise TencentCloudSDKException(e.message, e.message)


    def DescribeWhitelist(self, request):
        """获取服务白名单信息

        :param request: Request instance for DescribeWhitelist.
        :type request: :class:`tencentcloud.dlc.v20210125.models.DescribeWhitelistRequest`
        :rtype: :class:`tencentcloud.dlc.v20210125.models.DescribeWhitelistResponse`

        """
        try:
            params = request._serialize()
            headers = request.headers
            body = self.call("DescribeWhitelist", params, headers=headers)
            response = json.loads(body)
            model = models.DescribeWhitelistResponse()
            model._deserialize(response["Response"])
            return model
        except Exception as e:
            if isinstance(e, TencentCloudSDKException):
                raise
            else:
                raise TencentCloudSDKException(e.message, e.message)


    def DescribeWorkGroupInfo(self, request):
        """获取工作组详细信息

        :param request: Request instance for DescribeWorkGroupInfo.
        :type request: :class:`tencentcloud.dlc.v20210125.models.DescribeWorkGroupInfoRequest`
        :rtype: :class:`tencentcloud.dlc.v20210125.models.DescribeWorkGroupInfoResponse`

        """
        try:
            params = request._serialize()
            headers = request.headers
            body = self.call("DescribeWorkGroupInfo", params, headers=headers)
            response = json.loads(body)
            model = models.DescribeWorkGroupInfoResponse()
            model._deserialize(response["Response"])
            return model
        except Exception as e:
            if isinstance(e, TencentCloudSDKException):
                raise
            else:
                raise TencentCloudSDKException(e.message, e.message)


    def DescribeWorkGroups(self, request):
        """获取工作组列表

        :param request: Request instance for DescribeWorkGroups.
        :type request: :class:`tencentcloud.dlc.v20210125.models.DescribeWorkGroupsRequest`
        :rtype: :class:`tencentcloud.dlc.v20210125.models.DescribeWorkGroupsResponse`

        """
        try:
            params = request._serialize()
            headers = request.headers
            body = self.call("DescribeWorkGroups", params, headers=headers)
            response = json.loads(body)
            model = models.DescribeWorkGroupsResponse()
            model._deserialize(response["Response"])
            return model
        except Exception as e:
            if isinstance(e, TencentCloudSDKException):
                raise
            else:
                raise TencentCloudSDKException(e.message, e.message)


    def DescribeWorkloadStat(self, request):
        """查询工作负载统计信息

        :param request: Request instance for DescribeWorkloadStat.
        :type request: :class:`tencentcloud.dlc.v20210125.models.DescribeWorkloadStatRequest`
        :rtype: :class:`tencentcloud.dlc.v20210125.models.DescribeWorkloadStatResponse`

        """
        try:
            params = request._serialize()
            headers = request.headers
            body = self.call("DescribeWorkloadStat", params, headers=headers)
            response = json.loads(body)
            model = models.DescribeWorkloadStatResponse()
            model._deserialize(response["Response"])
            return model
        except Exception as e:
            if isinstance(e, TencentCloudSDKException):
                raise
            else:
                raise TencentCloudSDKException(e.message, e.message)


    def DescribeYuntiUser(self, request):
        """判断用户是否是云梯接口

        :param request: Request instance for DescribeYuntiUser.
        :type request: :class:`tencentcloud.dlc.v20210125.models.DescribeYuntiUserRequest`
        :rtype: :class:`tencentcloud.dlc.v20210125.models.DescribeYuntiUserResponse`

        """
        try:
            params = request._serialize()
            headers = request.headers
            body = self.call("DescribeYuntiUser", params, headers=headers)
            response = json.loads(body)
            model = models.DescribeYuntiUserResponse()
            model._deserialize(response["Response"])
            return model
        except Exception as e:
            if isinstance(e, TencentCloudSDKException):
                raise
            else:
                raise TencentCloudSDKException(e.message, e.message)


    def DetachUserPolicy(self, request):
        """解绑用户鉴权策略

        :param request: Request instance for DetachUserPolicy.
        :type request: :class:`tencentcloud.dlc.v20210125.models.DetachUserPolicyRequest`
        :rtype: :class:`tencentcloud.dlc.v20210125.models.DetachUserPolicyResponse`

        """
        try:
            params = request._serialize()
            headers = request.headers
            body = self.call("DetachUserPolicy", params, headers=headers)
            response = json.loads(body)
            model = models.DetachUserPolicyResponse()
            model._deserialize(response["Response"])
            return model
        except Exception as e:
            if isinstance(e, TencentCloudSDKException):
                raise
            else:
                raise TencentCloudSDKException(e.message, e.message)


    def DetachWorkGroupPolicy(self, request):
        """解绑工作组鉴权策略

        :param request: Request instance for DetachWorkGroupPolicy.
        :type request: :class:`tencentcloud.dlc.v20210125.models.DetachWorkGroupPolicyRequest`
        :rtype: :class:`tencentcloud.dlc.v20210125.models.DetachWorkGroupPolicyResponse`

        """
        try:
            params = request._serialize()
            headers = request.headers
            body = self.call("DetachWorkGroupPolicy", params, headers=headers)
            response = json.loads(body)
            model = models.DetachWorkGroupPolicyResponse()
            model._deserialize(response["Response"])
            return model
        except Exception as e:
            if isinstance(e, TencentCloudSDKException):
                raise
            else:
                raise TencentCloudSDKException(e.message, e.message)


    def DisassociateCHDFSAccessGroups(self, request):
        """解绑权限组

        :param request: Request instance for DisassociateCHDFSAccessGroups.
        :type request: :class:`tencentcloud.dlc.v20210125.models.DisassociateCHDFSAccessGroupsRequest`
        :rtype: :class:`tencentcloud.dlc.v20210125.models.DisassociateCHDFSAccessGroupsResponse`

        """
        try:
            params = request._serialize()
            headers = request.headers
            body = self.call("DisassociateCHDFSAccessGroups", params, headers=headers)
            response = json.loads(body)
            model = models.DisassociateCHDFSAccessGroupsResponse()
            model._deserialize(response["Response"])
            return model
        except Exception as e:
            if isinstance(e, TencentCloudSDKException):
                raise
            else:
                raise TencentCloudSDKException(e.message, e.message)


    def DownloadResult(self, request):
        """本接口（DownloadResult）用于下载SQL查询结果

        :param request: Request instance for DownloadResult.
        :type request: :class:`tencentcloud.dlc.v20210125.models.DownloadResultRequest`
        :rtype: :class:`tencentcloud.dlc.v20210125.models.DownloadResultResponse`

        """
        try:
            params = request._serialize()
            headers = request.headers
            body = self.call("DownloadResult", params, headers=headers)
            response = json.loads(body)
            model = models.DownloadResultResponse()
            model._deserialize(response["Response"])
            return model
        except Exception as e:
            if isinstance(e, TencentCloudSDKException):
                raise
            else:
                raise TencentCloudSDKException(e.message, e.message)


    def DownloadSparkTaskLog(self, request):
        """下载Spark任务日志

        :param request: Request instance for DownloadSparkTaskLog.
        :type request: :class:`tencentcloud.dlc.v20210125.models.DownloadSparkTaskLogRequest`
        :rtype: :class:`tencentcloud.dlc.v20210125.models.DownloadSparkTaskLogResponse`

        """
        try:
            params = request._serialize()
            headers = request.headers
            body = self.call("DownloadSparkTaskLog", params, headers=headers)
            response = json.loads(body)
            model = models.DownloadSparkTaskLogResponse()
            model._deserialize(response["Response"])
            return model
        except Exception as e:
            if isinstance(e, TencentCloudSDKException):
                raise
            else:
                raise TencentCloudSDKException(e.message, e.message)


    def DropDMSDatabase(self, request):
        """DMS元数据删除库

        :param request: Request instance for DropDMSDatabase.
        :type request: :class:`tencentcloud.dlc.v20210125.models.DropDMSDatabaseRequest`
        :rtype: :class:`tencentcloud.dlc.v20210125.models.DropDMSDatabaseResponse`

        """
        try:
            params = request._serialize()
            headers = request.headers
            body = self.call("DropDMSDatabase", params, headers=headers)
            response = json.loads(body)
            model = models.DropDMSDatabaseResponse()
            model._deserialize(response["Response"])
            return model
        except Exception as e:
            if isinstance(e, TencentCloudSDKException):
                raise
            else:
                raise TencentCloudSDKException(e.message, e.message)


    def DropDMSPartitionColumnStatistic(self, request):
        """该接口（DropDMSPartitionColumnStatistic）用于删除分区字段统计信息

        :param request: Request instance for DropDMSPartitionColumnStatistic.
        :type request: :class:`tencentcloud.dlc.v20210125.models.DropDMSPartitionColumnStatisticRequest`
        :rtype: :class:`tencentcloud.dlc.v20210125.models.DropDMSPartitionColumnStatisticResponse`

        """
        try:
            params = request._serialize()
            headers = request.headers
            body = self.call("DropDMSPartitionColumnStatistic", params, headers=headers)
            response = json.loads(body)
            model = models.DropDMSPartitionColumnStatisticResponse()
            model._deserialize(response["Response"])
            return model
        except Exception as e:
            if isinstance(e, TencentCloudSDKException):
                raise
            else:
                raise TencentCloudSDKException(e.message, e.message)


    def DropDMSPartitions(self, request):
        """DMS元数据删除分区

        :param request: Request instance for DropDMSPartitions.
        :type request: :class:`tencentcloud.dlc.v20210125.models.DropDMSPartitionsRequest`
        :rtype: :class:`tencentcloud.dlc.v20210125.models.DropDMSPartitionsResponse`

        """
        try:
            params = request._serialize()
            headers = request.headers
            body = self.call("DropDMSPartitions", params, headers=headers)
            response = json.loads(body)
            model = models.DropDMSPartitionsResponse()
            model._deserialize(response["Response"])
            return model
        except Exception as e:
            if isinstance(e, TencentCloudSDKException):
                raise
            else:
                raise TencentCloudSDKException(e.message, e.message)


    def DropDMSTable(self, request):
        """DMS元数据删除表

        :param request: Request instance for DropDMSTable.
        :type request: :class:`tencentcloud.dlc.v20210125.models.DropDMSTableRequest`
        :rtype: :class:`tencentcloud.dlc.v20210125.models.DropDMSTableResponse`

        """
        try:
            params = request._serialize()
            headers = request.headers
            body = self.call("DropDMSTable", params, headers=headers)
            response = json.loads(body)
            model = models.DropDMSTableResponse()
            model._deserialize(response["Response"])
            return model
        except Exception as e:
            if isinstance(e, TencentCloudSDKException):
                raise
            else:
                raise TencentCloudSDKException(e.message, e.message)


    def DropDMSTableColumnStatistic(self, request):
        """该接口（DropDMSTableColumnStatistic）用于删除表字段统计信息

        :param request: Request instance for DropDMSTableColumnStatistic.
        :type request: :class:`tencentcloud.dlc.v20210125.models.DropDMSTableColumnStatisticRequest`
        :rtype: :class:`tencentcloud.dlc.v20210125.models.DropDMSTableColumnStatisticResponse`

        """
        try:
            params = request._serialize()
            headers = request.headers
            body = self.call("DropDMSTableColumnStatistic", params, headers=headers)
            response = json.loads(body)
            model = models.DropDMSTableColumnStatisticResponse()
            model._deserialize(response["Response"])
            return model
        except Exception as e:
            if isinstance(e, TencentCloudSDKException):
                raise
            else:
                raise TencentCloudSDKException(e.message, e.message)


    def ExportResult(self, request):
        """该接口（ExportResult）用于导出SQL查询结果

        :param request: Request instance for ExportResult.
        :type request: :class:`tencentcloud.dlc.v20210125.models.ExportResultRequest`
        :rtype: :class:`tencentcloud.dlc.v20210125.models.ExportResultResponse`

        """
        try:
            params = request._serialize()
            headers = request.headers
            body = self.call("ExportResult", params, headers=headers)
            response = json.loads(body)
            model = models.ExportResultResponse()
            model._deserialize(response["Response"])
            return model
        except Exception as e:
            if isinstance(e, TencentCloudSDKException):
                raise
            else:
                raise TencentCloudSDKException(e.message, e.message)


    def ForceSuccessScheduleTaskInstances(self, request):
        """调度任务实例强制置为成功

        :param request: Request instance for ForceSuccessScheduleTaskInstances.
        :type request: :class:`tencentcloud.dlc.v20210125.models.ForceSuccessScheduleTaskInstancesRequest`
        :rtype: :class:`tencentcloud.dlc.v20210125.models.ForceSuccessScheduleTaskInstancesResponse`

        """
        try:
            params = request._serialize()
            headers = request.headers
            body = self.call("ForceSuccessScheduleTaskInstances", params, headers=headers)
            response = json.loads(body)
            model = models.ForceSuccessScheduleTaskInstancesResponse()
            model._deserialize(response["Response"])
            return model
        except Exception as e:
            if isinstance(e, TencentCloudSDKException):
                raise
            else:
                raise TencentCloudSDKException(e.message, e.message)


    def FreezeScheduleTasks(self, request):
        """冻结调度任务

        :param request: Request instance for FreezeScheduleTasks.
        :type request: :class:`tencentcloud.dlc.v20210125.models.FreezeScheduleTasksRequest`
        :rtype: :class:`tencentcloud.dlc.v20210125.models.FreezeScheduleTasksResponse`

        """
        try:
            params = request._serialize()
            headers = request.headers
            body = self.call("FreezeScheduleTasks", params, headers=headers)
            response = json.loads(body)
            model = models.FreezeScheduleTasksResponse()
            model._deserialize(response["Response"])
            return model
        except Exception as e:
            if isinstance(e, TencentCloudSDKException):
                raise
            else:
                raise TencentCloudSDKException(e.message, e.message)


    def GenerateCreateMangedTableSql(self, request):
        """生成创建托管表语句

        :param request: Request instance for GenerateCreateMangedTableSql.
        :type request: :class:`tencentcloud.dlc.v20210125.models.GenerateCreateMangedTableSqlRequest`
        :rtype: :class:`tencentcloud.dlc.v20210125.models.GenerateCreateMangedTableSqlResponse`

        """
        try:
            params = request._serialize()
            headers = request.headers
            body = self.call("GenerateCreateMangedTableSql", params, headers=headers)
            response = json.loads(body)
            model = models.GenerateCreateMangedTableSqlResponse()
            model._deserialize(response["Response"])
            return model
        except Exception as e:
            if isinstance(e, TencentCloudSDKException):
                raise
            else:
                raise TencentCloudSDKException(e.message, e.message)


    def GetWorkflowCanvas(self, request):
        """获取调度计划画布数据

        :param request: Request instance for GetWorkflowCanvas.
        :type request: :class:`tencentcloud.dlc.v20210125.models.GetWorkflowCanvasRequest`
        :rtype: :class:`tencentcloud.dlc.v20210125.models.GetWorkflowCanvasResponse`

        """
        try:
            params = request._serialize()
            headers = request.headers
            body = self.call("GetWorkflowCanvas", params, headers=headers)
            response = json.loads(body)
            model = models.GetWorkflowCanvasResponse()
            model._deserialize(response["Response"])
            return model
        except Exception as e:
            if isinstance(e, TencentCloudSDKException):
                raise
            else:
                raise TencentCloudSDKException(e.message, e.message)


    def GetWorkflowInfo(self, request):
        """根据ID查询调度计划信息

        :param request: Request instance for GetWorkflowInfo.
        :type request: :class:`tencentcloud.dlc.v20210125.models.GetWorkflowInfoRequest`
        :rtype: :class:`tencentcloud.dlc.v20210125.models.GetWorkflowInfoResponse`

        """
        try:
            params = request._serialize()
            headers = request.headers
            body = self.call("GetWorkflowInfo", params, headers=headers)
            response = json.loads(body)
            model = models.GetWorkflowInfoResponse()
            model._deserialize(response["Response"])
            return model
        except Exception as e:
            if isinstance(e, TencentCloudSDKException):
                raise
            else:
                raise TencentCloudSDKException(e.message, e.message)


    def InferInternalTableSchema(self, request):
        """推断内表数据格式

        :param request: Request instance for InferInternalTableSchema.
        :type request: :class:`tencentcloud.dlc.v20210125.models.InferInternalTableSchemaRequest`
        :rtype: :class:`tencentcloud.dlc.v20210125.models.InferInternalTableSchemaResponse`

        """
        try:
            params = request._serialize()
            headers = request.headers
            body = self.call("InferInternalTableSchema", params, headers=headers)
            response = json.loads(body)
            model = models.InferInternalTableSchemaResponse()
            model._deserialize(response["Response"])
            return model
        except Exception as e:
            if isinstance(e, TencentCloudSDKException):
                raise
            else:
                raise TencentCloudSDKException(e.message, e.message)


    def InferSchema(self, request):
        """本接口（InferSchema）用于推断文件的schema信息。

        :param request: Request instance for InferSchema.
        :type request: :class:`tencentcloud.dlc.v20210125.models.InferSchemaRequest`
        :rtype: :class:`tencentcloud.dlc.v20210125.models.InferSchemaResponse`

        """
        try:
            params = request._serialize()
            headers = request.headers
            body = self.call("InferSchema", params, headers=headers)
            response = json.loads(body)
            model = models.InferSchemaResponse()
            model._deserialize(response["Response"])
            return model
        except Exception as e:
            if isinstance(e, TencentCloudSDKException):
                raise
            else:
                raise TencentCloudSDKException(e.message, e.message)


    def InquireCreateDataEnginePrice(self, request):
        """查询创建数据引擎的价格

        :param request: Request instance for InquireCreateDataEnginePrice.
        :type request: :class:`tencentcloud.dlc.v20210125.models.InquireCreateDataEnginePriceRequest`
        :rtype: :class:`tencentcloud.dlc.v20210125.models.InquireCreateDataEnginePriceResponse`

        """
        try:
            params = request._serialize()
            headers = request.headers
            body = self.call("InquireCreateDataEnginePrice", params, headers=headers)
            response = json.loads(body)
            model = models.InquireCreateDataEnginePriceResponse()
            model._deserialize(response["Response"])
            return model
        except Exception as e:
            if isinstance(e, TencentCloudSDKException):
                raise
            else:
                raise TencentCloudSDKException(e.message, e.message)


    def InquirePriceCreateDataEngine(self, request):
        """创建数据引擎询价

        :param request: Request instance for InquirePriceCreateDataEngine.
        :type request: :class:`tencentcloud.dlc.v20210125.models.InquirePriceCreateDataEngineRequest`
        :rtype: :class:`tencentcloud.dlc.v20210125.models.InquirePriceCreateDataEngineResponse`

        """
        try:
            params = request._serialize()
            headers = request.headers
            body = self.call("InquirePriceCreateDataEngine", params, headers=headers)
            response = json.loads(body)
            model = models.InquirePriceCreateDataEngineResponse()
            model._deserialize(response["Response"])
            return model
        except Exception as e:
            if isinstance(e, TencentCloudSDKException):
                raise
            else:
                raise TencentCloudSDKException(e.message, e.message)


    def InquirePriceModifyDataEngine(self, request):
        """数据引擎变配询价

        :param request: Request instance for InquirePriceModifyDataEngine.
        :type request: :class:`tencentcloud.dlc.v20210125.models.InquirePriceModifyDataEngineRequest`
        :rtype: :class:`tencentcloud.dlc.v20210125.models.InquirePriceModifyDataEngineResponse`

        """
        try:
            params = request._serialize()
            headers = request.headers
            body = self.call("InquirePriceModifyDataEngine", params, headers=headers)
            response = json.loads(body)
            model = models.InquirePriceModifyDataEngineResponse()
            model._deserialize(response["Response"])
            return model
        except Exception as e:
            if isinstance(e, TencentCloudSDKException):
                raise
            else:
                raise TencentCloudSDKException(e.message, e.message)


    def InquirePriceTerminateDataEngine(self, request):
        """查询可退款金额

        :param request: Request instance for InquirePriceTerminateDataEngine.
        :type request: :class:`tencentcloud.dlc.v20210125.models.InquirePriceTerminateDataEngineRequest`
        :rtype: :class:`tencentcloud.dlc.v20210125.models.InquirePriceTerminateDataEngineResponse`

        """
        try:
            params = request._serialize()
            headers = request.headers
            body = self.call("InquirePriceTerminateDataEngine", params, headers=headers)
            response = json.loads(body)
            model = models.InquirePriceTerminateDataEngineResponse()
            model._deserialize(response["Response"])
            return model
        except Exception as e:
            if isinstance(e, TencentCloudSDKException):
                raise
            else:
                raise TencentCloudSDKException(e.message, e.message)


    def KillScheduleTaskInstances(self, request):
        """终止调度任务实例

        :param request: Request instance for KillScheduleTaskInstances.
        :type request: :class:`tencentcloud.dlc.v20210125.models.KillScheduleTaskInstancesRequest`
        :rtype: :class:`tencentcloud.dlc.v20210125.models.KillScheduleTaskInstancesResponse`

        """
        try:
            params = request._serialize()
            headers = request.headers
            body = self.call("KillScheduleTaskInstances", params, headers=headers)
            response = json.loads(body)
            model = models.KillScheduleTaskInstancesResponse()
            model._deserialize(response["Response"])
            return model
        except Exception as e:
            if isinstance(e, TencentCloudSDKException):
                raise
            else:
                raise TencentCloudSDKException(e.message, e.message)


    def ListDataEngines(self, request):
        """本接口（ListDataEngines）用于获取DataEngines信息列表

        :param request: Request instance for ListDataEngines.
        :type request: :class:`tencentcloud.dlc.v20210125.models.ListDataEnginesRequest`
        :rtype: :class:`tencentcloud.dlc.v20210125.models.ListDataEnginesResponse`

        """
        try:
            params = request._serialize()
            headers = request.headers
            body = self.call("ListDataEngines", params, headers=headers)
            response = json.loads(body)
            model = models.ListDataEnginesResponse()
            model._deserialize(response["Response"])
            return model
        except Exception as e:
            if isinstance(e, TencentCloudSDKException):
                raise
            else:
                raise TencentCloudSDKException(e.message, e.message)


    def ListHouse(self, request):
        """本接口（ListHouse）用于获取House信息列表

        :param request: Request instance for ListHouse.
        :type request: :class:`tencentcloud.dlc.v20210125.models.ListHouseRequest`
        :rtype: :class:`tencentcloud.dlc.v20210125.models.ListHouseResponse`

        """
        try:
            params = request._serialize()
            headers = request.headers
            body = self.call("ListHouse", params, headers=headers)
            response = json.loads(body)
            model = models.ListHouseResponse()
            model._deserialize(response["Response"])
            return model
        except Exception as e:
            if isinstance(e, TencentCloudSDKException):
                raise
            else:
                raise TencentCloudSDKException(e.message, e.message)


    def ListTaskJobLogDetail(self, request):
        """本接口（ListTaskJobLogDetail）用于获取spark 作业任务日志详情

        :param request: Request instance for ListTaskJobLogDetail.
        :type request: :class:`tencentcloud.dlc.v20210125.models.ListTaskJobLogDetailRequest`
        :rtype: :class:`tencentcloud.dlc.v20210125.models.ListTaskJobLogDetailResponse`

        """
        try:
            params = request._serialize()
            headers = request.headers
            body = self.call("ListTaskJobLogDetail", params, headers=headers)
            response = json.loads(body)
            model = models.ListTaskJobLogDetailResponse()
            model._deserialize(response["Response"])
            return model
        except Exception as e:
            if isinstance(e, TencentCloudSDKException):
                raise
            else:
                raise TencentCloudSDKException(e.message, e.message)


    def ListTaskJobLogName(self, request):
        """本接口（ListTaskJobLogName）用于获取spark-jar日志名称列表

        :param request: Request instance for ListTaskJobLogName.
        :type request: :class:`tencentcloud.dlc.v20210125.models.ListTaskJobLogNameRequest`
        :rtype: :class:`tencentcloud.dlc.v20210125.models.ListTaskJobLogNameResponse`

        """
        try:
            params = request._serialize()
            headers = request.headers
            body = self.call("ListTaskJobLogName", params, headers=headers)
            response = json.loads(body)
            model = models.ListTaskJobLogNameResponse()
            model._deserialize(response["Response"])
            return model
        except Exception as e:
            if isinstance(e, TencentCloudSDKException):
                raise
            else:
                raise TencentCloudSDKException(e.message, e.message)


    def ListWorkflow(self, request):
        """获取调度计划列表

        :param request: Request instance for ListWorkflow.
        :type request: :class:`tencentcloud.dlc.v20210125.models.ListWorkflowRequest`
        :rtype: :class:`tencentcloud.dlc.v20210125.models.ListWorkflowResponse`

        """
        try:
            params = request._serialize()
            headers = request.headers
            body = self.call("ListWorkflow", params, headers=headers)
            response = json.loads(body)
            model = models.ListWorkflowResponse()
            model._deserialize(response["Response"])
            return model
        except Exception as e:
            if isinstance(e, TencentCloudSDKException):
                raise
            else:
                raise TencentCloudSDKException(e.message, e.message)


    def LockMetaData(self, request):
        """元数据锁

        :param request: Request instance for LockMetaData.
        :type request: :class:`tencentcloud.dlc.v20210125.models.LockMetaDataRequest`
        :rtype: :class:`tencentcloud.dlc.v20210125.models.LockMetaDataResponse`

        """
        try:
            params = request._serialize()
            headers = request.headers
            body = self.call("LockMetaData", params, headers=headers)
            response = json.loads(body)
            model = models.LockMetaDataResponse()
            model._deserialize(response["Response"])
            return model
        except Exception as e:
            if isinstance(e, TencentCloudSDKException):
                raise
            else:
                raise TencentCloudSDKException(e.message, e.message)


    def MigrateDatasourceConnection(self, request):
        """迁移数据源连接

        :param request: Request instance for MigrateDatasourceConnection.
        :type request: :class:`tencentcloud.dlc.v20210125.models.MigrateDatasourceConnectionRequest`
        :rtype: :class:`tencentcloud.dlc.v20210125.models.MigrateDatasourceConnectionResponse`

        """
        try:
            params = request._serialize()
            headers = request.headers
            body = self.call("MigrateDatasourceConnection", params, headers=headers)
            response = json.loads(body)
            model = models.MigrateDatasourceConnectionResponse()
            model._deserialize(response["Response"])
            return model
        except Exception as e:
            if isinstance(e, TencentCloudSDKException):
                raise
            else:
                raise TencentCloudSDKException(e.message, e.message)


    def ModifyAdvancedStoreLocation(self, request):
        """修改sql查询界面高级设置。

        :param request: Request instance for ModifyAdvancedStoreLocation.
        :type request: :class:`tencentcloud.dlc.v20210125.models.ModifyAdvancedStoreLocationRequest`
        :rtype: :class:`tencentcloud.dlc.v20210125.models.ModifyAdvancedStoreLocationResponse`

        """
        try:
            params = request._serialize()
            headers = request.headers
            body = self.call("ModifyAdvancedStoreLocation", params, headers=headers)
            response = json.loads(body)
            model = models.ModifyAdvancedStoreLocationResponse()
            model._deserialize(response["Response"])
            return model
        except Exception as e:
            if isinstance(e, TencentCloudSDKException):
                raise
            else:
                raise TencentCloudSDKException(e.message, e.message)


    def ModifyCHDFSMountPointAssociateInfo(self, request):
        """修改数据引擎绑定挂载点信息

        :param request: Request instance for ModifyCHDFSMountPointAssociateInfo.
        :type request: :class:`tencentcloud.dlc.v20210125.models.ModifyCHDFSMountPointAssociateInfoRequest`
        :rtype: :class:`tencentcloud.dlc.v20210125.models.ModifyCHDFSMountPointAssociateInfoResponse`

        """
        try:
            params = request._serialize()
            headers = request.headers
            body = self.call("ModifyCHDFSMountPointAssociateInfo", params, headers=headers)
            response = json.loads(body)
            model = models.ModifyCHDFSMountPointAssociateInfoResponse()
            model._deserialize(response["Response"])
            return model
        except Exception as e:
            if isinstance(e, TencentCloudSDKException):
                raise
            else:
                raise TencentCloudSDKException(e.message, e.message)


    def ModifyCHDFSMountPointSuperuser(self, request):
        """此接口（ModifyCHDFSMountPointSuperuser）用于修改Superuser

        :param request: Request instance for ModifyCHDFSMountPointSuperuser.
        :type request: :class:`tencentcloud.dlc.v20210125.models.ModifyCHDFSMountPointSuperuserRequest`
        :rtype: :class:`tencentcloud.dlc.v20210125.models.ModifyCHDFSMountPointSuperuserResponse`

        """
        try:
            params = request._serialize()
            headers = request.headers
            body = self.call("ModifyCHDFSMountPointSuperuser", params, headers=headers)
            response = json.loads(body)
            model = models.ModifyCHDFSMountPointSuperuserResponse()
            model._deserialize(response["Response"])
            return model
        except Exception as e:
            if isinstance(e, TencentCloudSDKException):
                raise
            else:
                raise TencentCloudSDKException(e.message, e.message)


    def ModifyCHDFSProduct(self, request):
        """此接口（ModifyCHDFSProduct）修改元数据加速桶绑定产品

        :param request: Request instance for ModifyCHDFSProduct.
        :type request: :class:`tencentcloud.dlc.v20210125.models.ModifyCHDFSProductRequest`
        :rtype: :class:`tencentcloud.dlc.v20210125.models.ModifyCHDFSProductResponse`

        """
        try:
            params = request._serialize()
            headers = request.headers
            body = self.call("ModifyCHDFSProduct", params, headers=headers)
            response = json.loads(body)
            model = models.ModifyCHDFSProductResponse()
            model._deserialize(response["Response"])
            return model
        except Exception as e:
            if isinstance(e, TencentCloudSDKException):
                raise
            else:
                raise TencentCloudSDKException(e.message, e.message)


    def ModifyDataEngineDescription(self, request):
        """修改引擎描述信息

        :param request: Request instance for ModifyDataEngineDescription.
        :type request: :class:`tencentcloud.dlc.v20210125.models.ModifyDataEngineDescriptionRequest`
        :rtype: :class:`tencentcloud.dlc.v20210125.models.ModifyDataEngineDescriptionResponse`

        """
        try:
            params = request._serialize()
            headers = request.headers
            body = self.call("ModifyDataEngineDescription", params, headers=headers)
            response = json.loads(body)
            model = models.ModifyDataEngineDescriptionResponse()
            model._deserialize(response["Response"])
            return model
        except Exception as e:
            if isinstance(e, TencentCloudSDKException):
                raise
            else:
                raise TencentCloudSDKException(e.message, e.message)


    def ModifyDatabaseUDF(self, request):
        """修改Udf信息。

        :param request: Request instance for ModifyDatabaseUDF.
        :type request: :class:`tencentcloud.dlc.v20210125.models.ModifyDatabaseUDFRequest`
        :rtype: :class:`tencentcloud.dlc.v20210125.models.ModifyDatabaseUDFResponse`

        """
        try:
            params = request._serialize()
            headers = request.headers
            body = self.call("ModifyDatabaseUDF", params, headers=headers)
            response = json.loads(body)
            model = models.ModifyDatabaseUDFResponse()
            model._deserialize(response["Response"])
            return model
        except Exception as e:
            if isinstance(e, TencentCloudSDKException):
                raise
            else:
                raise TencentCloudSDKException(e.message, e.message)


    def ModifyDatasourceConnection(self, request):
        """修改数据源连接

        :param request: Request instance for ModifyDatasourceConnection.
        :type request: :class:`tencentcloud.dlc.v20210125.models.ModifyDatasourceConnectionRequest`
        :rtype: :class:`tencentcloud.dlc.v20210125.models.ModifyDatasourceConnectionResponse`

        """
        try:
            params = request._serialize()
            headers = request.headers
            body = self.call("ModifyDatasourceConnection", params, headers=headers)
            response = json.loads(body)
            model = models.ModifyDatasourceConnectionResponse()
            model._deserialize(response["Response"])
            return model
        except Exception as e:
            if isinstance(e, TencentCloudSDKException):
                raise
            else:
                raise TencentCloudSDKException(e.message, e.message)


    def ModifyGovernEventRule(self, request):
        """修改数据治理事件阈值

        :param request: Request instance for ModifyGovernEventRule.
        :type request: :class:`tencentcloud.dlc.v20210125.models.ModifyGovernEventRuleRequest`
        :rtype: :class:`tencentcloud.dlc.v20210125.models.ModifyGovernEventRuleResponse`

        """
        try:
            params = request._serialize()
            headers = request.headers
            body = self.call("ModifyGovernEventRule", params, headers=headers)
            response = json.loads(body)
            model = models.ModifyGovernEventRuleResponse()
            model._deserialize(response["Response"])
            return model
        except Exception as e:
            if isinstance(e, TencentCloudSDKException):
                raise
            else:
                raise TencentCloudSDKException(e.message, e.message)


    def ModifyMetaDatabase(self, request):
        """本接口（ModifyMetaDatabase）用于修改元数据库

        :param request: Request instance for ModifyMetaDatabase.
        :type request: :class:`tencentcloud.dlc.v20210125.models.ModifyMetaDatabaseRequest`
        :rtype: :class:`tencentcloud.dlc.v20210125.models.ModifyMetaDatabaseResponse`

        """
        try:
            params = request._serialize()
            headers = request.headers
            body = self.call("ModifyMetaDatabase", params, headers=headers)
            response = json.loads(body)
            model = models.ModifyMetaDatabaseResponse()
            model._deserialize(response["Response"])
            return model
        except Exception as e:
            if isinstance(e, TencentCloudSDKException):
                raise
            else:
                raise TencentCloudSDKException(e.message, e.message)


    def ModifySQLSessionCatalog(self, request):
        """本接口（ModifySQLSessionCatalog）用于修改目录信息

        :param request: Request instance for ModifySQLSessionCatalog.
        :type request: :class:`tencentcloud.dlc.v20210125.models.ModifySQLSessionCatalogRequest`
        :rtype: :class:`tencentcloud.dlc.v20210125.models.ModifySQLSessionCatalogResponse`

        """
        try:
            params = request._serialize()
            headers = request.headers
            body = self.call("ModifySQLSessionCatalog", params, headers=headers)
            response = json.loads(body)
            model = models.ModifySQLSessionCatalogResponse()
            model._deserialize(response["Response"])
            return model
        except Exception as e:
            if isinstance(e, TencentCloudSDKException):
                raise
            else:
                raise TencentCloudSDKException(e.message, e.message)


    def ModifySQLSessionSnapshot(self, request):
        """本接口（ModifySQLSessionSnapshot）用于修改用户的SQL会话

        :param request: Request instance for ModifySQLSessionSnapshot.
        :type request: :class:`tencentcloud.dlc.v20210125.models.ModifySQLSessionSnapshotRequest`
        :rtype: :class:`tencentcloud.dlc.v20210125.models.ModifySQLSessionSnapshotResponse`

        """
        try:
            params = request._serialize()
            headers = request.headers
            body = self.call("ModifySQLSessionSnapshot", params, headers=headers)
            response = json.loads(body)
            model = models.ModifySQLSessionSnapshotResponse()
            model._deserialize(response["Response"])
            return model
        except Exception as e:
            if isinstance(e, TencentCloudSDKException):
                raise
            else:
                raise TencentCloudSDKException(e.message, e.message)


    def ModifyScheduleTask(self, request):
        """修改调度任务

        :param request: Request instance for ModifyScheduleTask.
        :type request: :class:`tencentcloud.dlc.v20210125.models.ModifyScheduleTaskRequest`
        :rtype: :class:`tencentcloud.dlc.v20210125.models.ModifyScheduleTaskResponse`

        """
        try:
            params = request._serialize()
            headers = request.headers
            body = self.call("ModifyScheduleTask", params, headers=headers)
            response = json.loads(body)
            model = models.ModifyScheduleTaskResponse()
            model._deserialize(response["Response"])
            return model
        except Exception as e:
            if isinstance(e, TencentCloudSDKException):
                raise
            else:
                raise TencentCloudSDKException(e.message, e.message)


    def ModifyScheduleTaskExecuteInfo(self, request):
        """修改调度任务执行信息

        :param request: Request instance for ModifyScheduleTaskExecuteInfo.
        :type request: :class:`tencentcloud.dlc.v20210125.models.ModifyScheduleTaskExecuteInfoRequest`
        :rtype: :class:`tencentcloud.dlc.v20210125.models.ModifyScheduleTaskExecuteInfoResponse`

        """
        try:
            params = request._serialize()
            headers = request.headers
            body = self.call("ModifyScheduleTaskExecuteInfo", params, headers=headers)
            response = json.loads(body)
            model = models.ModifyScheduleTaskExecuteInfoResponse()
            model._deserialize(response["Response"])
            return model
        except Exception as e:
            if isinstance(e, TencentCloudSDKException):
                raise
            else:
                raise TencentCloudSDKException(e.message, e.message)


    def ModifySparkApp(self, request):
        """更新spark作业

        :param request: Request instance for ModifySparkApp.
        :type request: :class:`tencentcloud.dlc.v20210125.models.ModifySparkAppRequest`
        :rtype: :class:`tencentcloud.dlc.v20210125.models.ModifySparkAppResponse`

        """
        try:
            params = request._serialize()
            headers = request.headers
            body = self.call("ModifySparkApp", params, headers=headers)
            response = json.loads(body)
            model = models.ModifySparkAppResponse()
            model._deserialize(response["Response"])
            return model
        except Exception as e:
            if isinstance(e, TencentCloudSDKException):
                raise
            else:
                raise TencentCloudSDKException(e.message, e.message)


    def ModifySparkAppBatch(self, request):
        """本接口（ModifySparkAppBatch）用于批量修改Spark作业参数配置

        :param request: Request instance for ModifySparkAppBatch.
        :type request: :class:`tencentcloud.dlc.v20210125.models.ModifySparkAppBatchRequest`
        :rtype: :class:`tencentcloud.dlc.v20210125.models.ModifySparkAppBatchResponse`

        """
        try:
            params = request._serialize()
            headers = request.headers
            body = self.call("ModifySparkAppBatch", params, headers=headers)
            response = json.loads(body)
            model = models.ModifySparkAppBatchResponse()
            model._deserialize(response["Response"])
            return model
        except Exception as e:
            if isinstance(e, TencentCloudSDKException):
                raise
            else:
                raise TencentCloudSDKException(e.message, e.message)


    def ModifySparkImage(self, request):
        """该接口（ModifySparkImage）用于修改Spark镜像信息

        :param request: Request instance for ModifySparkImage.
        :type request: :class:`tencentcloud.dlc.v20210125.models.ModifySparkImageRequest`
        :rtype: :class:`tencentcloud.dlc.v20210125.models.ModifySparkImageResponse`

        """
        try:
            params = request._serialize()
            headers = request.headers
            body = self.call("ModifySparkImage", params, headers=headers)
            response = json.loads(body)
            model = models.ModifySparkImageResponse()
            model._deserialize(response["Response"])
            return model
        except Exception as e:
            if isinstance(e, TencentCloudSDKException):
                raise
            else:
                raise TencentCloudSDKException(e.message, e.message)


    def ModifyUser(self, request):
        """修改用户信息

        :param request: Request instance for ModifyUser.
        :type request: :class:`tencentcloud.dlc.v20210125.models.ModifyUserRequest`
        :rtype: :class:`tencentcloud.dlc.v20210125.models.ModifyUserResponse`

        """
        try:
            params = request._serialize()
            headers = request.headers
            body = self.call("ModifyUser", params, headers=headers)
            response = json.loads(body)
            model = models.ModifyUserResponse()
            model._deserialize(response["Response"])
            return model
        except Exception as e:
            if isinstance(e, TencentCloudSDKException):
                raise
            else:
                raise TencentCloudSDKException(e.message, e.message)


    def ModifyUserAlias(self, request):
        """修改用户名

        :param request: Request instance for ModifyUserAlias.
        :type request: :class:`tencentcloud.dlc.v20210125.models.ModifyUserAliasRequest`
        :rtype: :class:`tencentcloud.dlc.v20210125.models.ModifyUserAliasResponse`

        """
        try:
            params = request._serialize()
            headers = request.headers
            body = self.call("ModifyUserAlias", params, headers=headers)
            response = json.loads(body)
            model = models.ModifyUserAliasResponse()
            model._deserialize(response["Response"])
            return model
        except Exception as e:
            if isinstance(e, TencentCloudSDKException):
                raise
            else:
                raise TencentCloudSDKException(e.message, e.message)


    def ModifyUserType(self, request):
        """修改用户类型。只有管理员用户能够调用该接口进行操作

        :param request: Request instance for ModifyUserType.
        :type request: :class:`tencentcloud.dlc.v20210125.models.ModifyUserTypeRequest`
        :rtype: :class:`tencentcloud.dlc.v20210125.models.ModifyUserTypeResponse`

        """
        try:
            params = request._serialize()
            headers = request.headers
            body = self.call("ModifyUserType", params, headers=headers)
            response = json.loads(body)
            model = models.ModifyUserTypeResponse()
            model._deserialize(response["Response"])
            return model
        except Exception as e:
            if isinstance(e, TencentCloudSDKException):
                raise
            else:
                raise TencentCloudSDKException(e.message, e.message)


    def ModifyUserUseScene(self, request):
        """更新或创建用户使用场景

        :param request: Request instance for ModifyUserUseScene.
        :type request: :class:`tencentcloud.dlc.v20210125.models.ModifyUserUseSceneRequest`
        :rtype: :class:`tencentcloud.dlc.v20210125.models.ModifyUserUseSceneResponse`

        """
        try:
            params = request._serialize()
            headers = request.headers
            body = self.call("ModifyUserUseScene", params, headers=headers)
            response = json.loads(body)
            model = models.ModifyUserUseSceneResponse()
            model._deserialize(response["Response"])
            return model
        except Exception as e:
            if isinstance(e, TencentCloudSDKException):
                raise
            else:
                raise TencentCloudSDKException(e.message, e.message)


    def ModifyWorkGroup(self, request):
        """修改工作组信息

        :param request: Request instance for ModifyWorkGroup.
        :type request: :class:`tencentcloud.dlc.v20210125.models.ModifyWorkGroupRequest`
        :rtype: :class:`tencentcloud.dlc.v20210125.models.ModifyWorkGroupResponse`

        """
        try:
            params = request._serialize()
            headers = request.headers
            body = self.call("ModifyWorkGroup", params, headers=headers)
            response = json.loads(body)
            model = models.ModifyWorkGroupResponse()
            model._deserialize(response["Response"])
            return model
        except Exception as e:
            if isinstance(e, TencentCloudSDKException):
                raise
            else:
                raise TencentCloudSDKException(e.message, e.message)


    def QueryInternalTableWarehouse(self, request):
        """本接口（QueryInternalTableWarehouse）用于获取原生表warehouse路径

        :param request: Request instance for QueryInternalTableWarehouse.
        :type request: :class:`tencentcloud.dlc.v20210125.models.QueryInternalTableWarehouseRequest`
        :rtype: :class:`tencentcloud.dlc.v20210125.models.QueryInternalTableWarehouseResponse`

        """
        try:
            params = request._serialize()
            headers = request.headers
            body = self.call("QueryInternalTableWarehouse", params, headers=headers)
            response = json.loads(body)
            model = models.QueryInternalTableWarehouseResponse()
            model._deserialize(response["Response"])
            return model
        except Exception as e:
            if isinstance(e, TencentCloudSDKException):
                raise
            else:
                raise TencentCloudSDKException(e.message, e.message)


    def QueryResult(self, request):
        """获取任务结果查询

        :param request: Request instance for QueryResult.
        :type request: :class:`tencentcloud.dlc.v20210125.models.QueryResultRequest`
        :rtype: :class:`tencentcloud.dlc.v20210125.models.QueryResultResponse`

        """
        try:
            params = request._serialize()
            headers = request.headers
            body = self.call("QueryResult", params, headers=headers)
            response = json.loads(body)
            model = models.QueryResultResponse()
            model._deserialize(response["Response"])
            return model
        except Exception as e:
            if isinstance(e, TencentCloudSDKException):
                raise
            else:
                raise TencentCloudSDKException(e.message, e.message)


    def QuerySparkImageUserRecords(self, request):
        """该接口（QuerySparkImageUserRecords）用于查询用户私有镜像列表

        :param request: Request instance for QuerySparkImageUserRecords.
        :type request: :class:`tencentcloud.dlc.v20210125.models.QuerySparkImageUserRecordsRequest`
        :rtype: :class:`tencentcloud.dlc.v20210125.models.QuerySparkImageUserRecordsResponse`

        """
        try:
            params = request._serialize()
            headers = request.headers
            body = self.call("QuerySparkImageUserRecords", params, headers=headers)
            response = json.loads(body)
            model = models.QuerySparkImageUserRecordsResponse()
            model._deserialize(response["Response"])
            return model
        except Exception as e:
            if isinstance(e, TencentCloudSDKException):
                raise
            else:
                raise TencentCloudSDKException(e.message, e.message)


    def QuerySparkImages(self, request):
        """获取spark镜像列表

        :param request: Request instance for QuerySparkImages.
        :type request: :class:`tencentcloud.dlc.v20210125.models.QuerySparkImagesRequest`
        :rtype: :class:`tencentcloud.dlc.v20210125.models.QuerySparkImagesResponse`

        """
        try:
            params = request._serialize()
            headers = request.headers
            body = self.call("QuerySparkImages", params, headers=headers)
            response = json.loads(body)
            model = models.QuerySparkImagesResponse()
            model._deserialize(response["Response"])
            return model
        except Exception as e:
            if isinstance(e, TencentCloudSDKException):
                raise
            else:
                raise TencentCloudSDKException(e.message, e.message)


    def QuerySystemStorage(self, request):
        """查询托管指定类型的系统目录

        :param request: Request instance for QuerySystemStorage.
        :type request: :class:`tencentcloud.dlc.v20210125.models.QuerySystemStorageRequest`
        :rtype: :class:`tencentcloud.dlc.v20210125.models.QuerySystemStorageResponse`

        """
        try:
            params = request._serialize()
            headers = request.headers
            body = self.call("QuerySystemStorage", params, headers=headers)
            response = json.loads(body)
            model = models.QuerySystemStorageResponse()
            model._deserialize(response["Response"])
            return model
        except Exception as e:
            if isinstance(e, TencentCloudSDKException):
                raise
            else:
                raise TencentCloudSDKException(e.message, e.message)


    def QueryTaskResult(self, request):
        """查询任务结果，每次返回1000行数据

        :param request: Request instance for QueryTaskResult.
        :type request: :class:`tencentcloud.dlc.v20210125.models.QueryTaskResultRequest`
        :rtype: :class:`tencentcloud.dlc.v20210125.models.QueryTaskResultResponse`

        """
        try:
            params = request._serialize()
            headers = request.headers
            body = self.call("QueryTaskResult", params, headers=headers)
            response = json.loads(body)
            model = models.QueryTaskResultResponse()
            model._deserialize(response["Response"])
            return model
        except Exception as e:
            if isinstance(e, TencentCloudSDKException):
                raise
            else:
                raise TencentCloudSDKException(e.message, e.message)


    def RemoveTask(self, request):
        """删除画布中的任务

        :param request: Request instance for RemoveTask.
        :type request: :class:`tencentcloud.dlc.v20210125.models.RemoveTaskRequest`
        :rtype: :class:`tencentcloud.dlc.v20210125.models.RemoveTaskResponse`

        """
        try:
            params = request._serialize()
            headers = request.headers
            body = self.call("RemoveTask", params, headers=headers)
            response = json.loads(body)
            model = models.RemoveTaskResponse()
            model._deserialize(response["Response"])
            return model
        except Exception as e:
            if isinstance(e, TencentCloudSDKException):
                raise
            else:
                raise TencentCloudSDKException(e.message, e.message)


    def RenewDataEngine(self, request):
        """续费数据引擎

        :param request: Request instance for RenewDataEngine.
        :type request: :class:`tencentcloud.dlc.v20210125.models.RenewDataEngineRequest`
        :rtype: :class:`tencentcloud.dlc.v20210125.models.RenewDataEngineResponse`

        """
        try:
            params = request._serialize()
            headers = request.headers
            body = self.call("RenewDataEngine", params, headers=headers)
            response = json.loads(body)
            model = models.RenewDataEngineResponse()
            model._deserialize(response["Response"])
            return model
        except Exception as e:
            if isinstance(e, TencentCloudSDKException):
                raise
            else:
                raise TencentCloudSDKException(e.message, e.message)


    def RenewHouse(self, request):
        """续费数据引擎

        :param request: Request instance for RenewHouse.
        :type request: :class:`tencentcloud.dlc.v20210125.models.RenewHouseRequest`
        :rtype: :class:`tencentcloud.dlc.v20210125.models.RenewHouseResponse`

        """
        try:
            params = request._serialize()
            headers = request.headers
            body = self.call("RenewHouse", params, headers=headers)
            response = json.loads(body)
            model = models.RenewHouseResponse()
            model._deserialize(response["Response"])
            return model
        except Exception as e:
            if isinstance(e, TencentCloudSDKException):
                raise
            else:
                raise TencentCloudSDKException(e.message, e.message)


    def ReportHeartbeatMetaData(self, request):
        """上报元数据心跳

        :param request: Request instance for ReportHeartbeatMetaData.
        :type request: :class:`tencentcloud.dlc.v20210125.models.ReportHeartbeatMetaDataRequest`
        :rtype: :class:`tencentcloud.dlc.v20210125.models.ReportHeartbeatMetaDataResponse`

        """
        try:
            params = request._serialize()
            headers = request.headers
            body = self.call("ReportHeartbeatMetaData", params, headers=headers)
            response = json.loads(body)
            model = models.ReportHeartbeatMetaDataResponse()
            model._deserialize(response["Response"])
            return model
        except Exception as e:
            if isinstance(e, TencentCloudSDKException):
                raise
            else:
                raise TencentCloudSDKException(e.message, e.message)


    def RerunScheduleTaskInstances(self, request):
        """重跑调度任务实例

        :param request: Request instance for RerunScheduleTaskInstances.
        :type request: :class:`tencentcloud.dlc.v20210125.models.RerunScheduleTaskInstancesRequest`
        :rtype: :class:`tencentcloud.dlc.v20210125.models.RerunScheduleTaskInstancesResponse`

        """
        try:
            params = request._serialize()
            headers = request.headers
            body = self.call("RerunScheduleTaskInstances", params, headers=headers)
            response = json.loads(body)
            model = models.RerunScheduleTaskInstancesResponse()
            model._deserialize(response["Response"])
            return model
        except Exception as e:
            if isinstance(e, TencentCloudSDKException):
                raise
            else:
                raise TencentCloudSDKException(e.message, e.message)


    def RestartDataEngine(self, request):
        """重启引擎

        :param request: Request instance for RestartDataEngine.
        :type request: :class:`tencentcloud.dlc.v20210125.models.RestartDataEngineRequest`
        :rtype: :class:`tencentcloud.dlc.v20210125.models.RestartDataEngineResponse`

        """
        try:
            params = request._serialize()
            headers = request.headers
            body = self.call("RestartDataEngine", params, headers=headers)
            response = json.loads(body)
            model = models.RestartDataEngineResponse()
            model._deserialize(response["Response"])
            return model
        except Exception as e:
            if isinstance(e, TencentCloudSDKException):
                raise
            else:
                raise TencentCloudSDKException(e.message, e.message)


    def RollbackDataEngineImage(self, request):
        """回滚引擎镜像版本

        :param request: Request instance for RollbackDataEngineImage.
        :type request: :class:`tencentcloud.dlc.v20210125.models.RollbackDataEngineImageRequest`
        :rtype: :class:`tencentcloud.dlc.v20210125.models.RollbackDataEngineImageResponse`

        """
        try:
            params = request._serialize()
            headers = request.headers
            body = self.call("RollbackDataEngineImage", params, headers=headers)
            response = json.loads(body)
            model = models.RollbackDataEngineImageResponse()
            model._deserialize(response["Response"])
            return model
        except Exception as e:
            if isinstance(e, TencentCloudSDKException):
                raise
            else:
                raise TencentCloudSDKException(e.message, e.message)


    def RunScheduleTask(self, request):
        """启动调度任务

        :param request: Request instance for RunScheduleTask.
        :type request: :class:`tencentcloud.dlc.v20210125.models.RunScheduleTaskRequest`
        :rtype: :class:`tencentcloud.dlc.v20210125.models.RunScheduleTaskResponse`

        """
        try:
            params = request._serialize()
            headers = request.headers
            body = self.call("RunScheduleTask", params, headers=headers)
            response = json.loads(body)
            model = models.RunScheduleTaskResponse()
            model._deserialize(response["Response"])
            return model
        except Exception as e:
            if isinstance(e, TencentCloudSDKException):
                raise
            else:
                raise TencentCloudSDKException(e.message, e.message)


    def SavePosition(self, request):
        """保存任务坐标

        :param request: Request instance for SavePosition.
        :type request: :class:`tencentcloud.dlc.v20210125.models.SavePositionRequest`
        :rtype: :class:`tencentcloud.dlc.v20210125.models.SavePositionResponse`

        """
        try:
            params = request._serialize()
            headers = request.headers
            body = self.call("SavePosition", params, headers=headers)
            response = json.loads(body)
            model = models.SavePositionResponse()
            model._deserialize(response["Response"])
            return model
        except Exception as e:
            if isinstance(e, TencentCloudSDKException):
                raise
            else:
                raise TencentCloudSDKException(e.message, e.message)


    def SetTableProperties(self, request):
        """本接口（SetTableProperties）用于增加或修改表属性批量删除表

        :param request: Request instance for SetTableProperties.
        :type request: :class:`tencentcloud.dlc.v20210125.models.SetTablePropertiesRequest`
        :rtype: :class:`tencentcloud.dlc.v20210125.models.SetTablePropertiesResponse`

        """
        try:
            params = request._serialize()
            headers = request.headers
            body = self.call("SetTableProperties", params, headers=headers)
            response = json.loads(body)
            model = models.SetTablePropertiesResponse()
            model._deserialize(response["Response"])
            return model
        except Exception as e:
            if isinstance(e, TencentCloudSDKException):
                raise
            else:
                raise TencentCloudSDKException(e.message, e.message)


    def StopScheduleTasks(self, request):
        """暂停调度任务

        :param request: Request instance for StopScheduleTasks.
        :type request: :class:`tencentcloud.dlc.v20210125.models.StopScheduleTasksRequest`
        :rtype: :class:`tencentcloud.dlc.v20210125.models.StopScheduleTasksResponse`

        """
        try:
            params = request._serialize()
            headers = request.headers
            body = self.call("StopScheduleTasks", params, headers=headers)
            response = json.loads(body)
            model = models.StopScheduleTasksResponse()
            model._deserialize(response["Response"])
            return model
        except Exception as e:
            if isinstance(e, TencentCloudSDKException):
                raise
            else:
                raise TencentCloudSDKException(e.message, e.message)


    def SupplementData(self, request):
        """补录数据

        :param request: Request instance for SupplementData.
        :type request: :class:`tencentcloud.dlc.v20210125.models.SupplementDataRequest`
        :rtype: :class:`tencentcloud.dlc.v20210125.models.SupplementDataResponse`

        """
        try:
            params = request._serialize()
            headers = request.headers
            body = self.call("SupplementData", params, headers=headers)
            response = json.loads(body)
            model = models.SupplementDataResponse()
            model._deserialize(response["Response"])
            return model
        except Exception as e:
            if isinstance(e, TencentCloudSDKException):
                raise
            else:
                raise TencentCloudSDKException(e.message, e.message)


    def SuspendResumeDataEngine(self, request):
        """本接口用于控制挂起或启动数据引擎

        :param request: Request instance for SuspendResumeDataEngine.
        :type request: :class:`tencentcloud.dlc.v20210125.models.SuspendResumeDataEngineRequest`
        :rtype: :class:`tencentcloud.dlc.v20210125.models.SuspendResumeDataEngineResponse`

        """
        try:
            params = request._serialize()
            headers = request.headers
            body = self.call("SuspendResumeDataEngine", params, headers=headers)
            response = json.loads(body)
            model = models.SuspendResumeDataEngineResponse()
            model._deserialize(response["Response"])
            return model
        except Exception as e:
            if isinstance(e, TencentCloudSDKException):
                raise
            else:
                raise TencentCloudSDKException(e.message, e.message)


    def SuspendResumeHouse(self, request):
        """本接口（SuspendResumeHouse）用于控制冻结或恢复House

        :param request: Request instance for SuspendResumeHouse.
        :type request: :class:`tencentcloud.dlc.v20210125.models.SuspendResumeHouseRequest`
        :rtype: :class:`tencentcloud.dlc.v20210125.models.SuspendResumeHouseResponse`

        """
        try:
            params = request._serialize()
            headers = request.headers
            body = self.call("SuspendResumeHouse", params, headers=headers)
            response = json.loads(body)
            model = models.SuspendResumeHouseResponse()
            model._deserialize(response["Response"])
            return model
        except Exception as e:
            if isinstance(e, TencentCloudSDKException):
                raise
            else:
                raise TencentCloudSDKException(e.message, e.message)


    def SwitchDataEngine(self, request):
        """切换主备集群

        :param request: Request instance for SwitchDataEngine.
        :type request: :class:`tencentcloud.dlc.v20210125.models.SwitchDataEngineRequest`
        :rtype: :class:`tencentcloud.dlc.v20210125.models.SwitchDataEngineResponse`

        """
        try:
            params = request._serialize()
            headers = request.headers
            body = self.call("SwitchDataEngine", params, headers=headers)
            response = json.loads(body)
            model = models.SwitchDataEngineResponse()
            model._deserialize(response["Response"])
            return model
        except Exception as e:
            if isinstance(e, TencentCloudSDKException):
                raise
            else:
                raise TencentCloudSDKException(e.message, e.message)


    def SwitchDataEngineImage(self, request):
        """切换引擎镜像版本

        :param request: Request instance for SwitchDataEngineImage.
        :type request: :class:`tencentcloud.dlc.v20210125.models.SwitchDataEngineImageRequest`
        :rtype: :class:`tencentcloud.dlc.v20210125.models.SwitchDataEngineImageResponse`

        """
        try:
            params = request._serialize()
            headers = request.headers
            body = self.call("SwitchDataEngineImage", params, headers=headers)
            response = json.loads(body)
            model = models.SwitchDataEngineImageResponse()
            model._deserialize(response["Response"])
            return model
        except Exception as e:
            if isinstance(e, TencentCloudSDKException):
                raise
            else:
                raise TencentCloudSDKException(e.message, e.message)


    def UnbindWorkGroupsFromUser(self, request):
        """解绑用户上的用户组

        :param request: Request instance for UnbindWorkGroupsFromUser.
        :type request: :class:`tencentcloud.dlc.v20210125.models.UnbindWorkGroupsFromUserRequest`
        :rtype: :class:`tencentcloud.dlc.v20210125.models.UnbindWorkGroupsFromUserResponse`

        """
        try:
            params = request._serialize()
            headers = request.headers
            body = self.call("UnbindWorkGroupsFromUser", params, headers=headers)
            response = json.loads(body)
            model = models.UnbindWorkGroupsFromUserResponse()
            model._deserialize(response["Response"])
            return model
        except Exception as e:
            if isinstance(e, TencentCloudSDKException):
                raise
            else:
                raise TencentCloudSDKException(e.message, e.message)


    def UnboundDatasourceHouse(self, request):
        """解绑数据源与队列

        :param request: Request instance for UnboundDatasourceHouse.
        :type request: :class:`tencentcloud.dlc.v20210125.models.UnboundDatasourceHouseRequest`
        :rtype: :class:`tencentcloud.dlc.v20210125.models.UnboundDatasourceHouseResponse`

        """
        try:
            params = request._serialize()
            headers = request.headers
            body = self.call("UnboundDatasourceHouse", params, headers=headers)
            response = json.loads(body)
            model = models.UnboundDatasourceHouseResponse()
            model._deserialize(response["Response"])
            return model
        except Exception as e:
            if isinstance(e, TencentCloudSDKException):
                raise
            else:
                raise TencentCloudSDKException(e.message, e.message)


    def UnlockMetaData(self, request):
        """元数据解锁

        :param request: Request instance for UnlockMetaData.
        :type request: :class:`tencentcloud.dlc.v20210125.models.UnlockMetaDataRequest`
        :rtype: :class:`tencentcloud.dlc.v20210125.models.UnlockMetaDataResponse`

        """
        try:
            params = request._serialize()
            headers = request.headers
            body = self.call("UnlockMetaData", params, headers=headers)
            response = json.loads(body)
            model = models.UnlockMetaDataResponse()
            model._deserialize(response["Response"])
            return model
        except Exception as e:
            if isinstance(e, TencentCloudSDKException):
                raise
            else:
                raise TencentCloudSDKException(e.message, e.message)


    def UpdateDataEngine(self, request):
        """本接口用于更新数据引擎配置

        :param request: Request instance for UpdateDataEngine.
        :type request: :class:`tencentcloud.dlc.v20210125.models.UpdateDataEngineRequest`
        :rtype: :class:`tencentcloud.dlc.v20210125.models.UpdateDataEngineResponse`

        """
        try:
            params = request._serialize()
            headers = request.headers
            body = self.call("UpdateDataEngine", params, headers=headers)
            response = json.loads(body)
            model = models.UpdateDataEngineResponse()
            model._deserialize(response["Response"])
            return model
        except Exception as e:
            if isinstance(e, TencentCloudSDKException):
                raise
            else:
                raise TencentCloudSDKException(e.message, e.message)


    def UpdateDataEngineConfig(self, request):
        """用户某种操作，触发引擎配置修改

        :param request: Request instance for UpdateDataEngineConfig.
        :type request: :class:`tencentcloud.dlc.v20210125.models.UpdateDataEngineConfigRequest`
        :rtype: :class:`tencentcloud.dlc.v20210125.models.UpdateDataEngineConfigResponse`

        """
        try:
            params = request._serialize()
            headers = request.headers
            body = self.call("UpdateDataEngineConfig", params, headers=headers)
            response = json.loads(body)
            model = models.UpdateDataEngineConfigResponse()
            model._deserialize(response["Response"])
            return model
        except Exception as e:
            if isinstance(e, TencentCloudSDKException):
                raise
            else:
                raise TencentCloudSDKException(e.message, e.message)


    def UpdateDataQuery(self, request):
        """更新数据查询信息

        :param request: Request instance for UpdateDataQuery.
        :type request: :class:`tencentcloud.dlc.v20210125.models.UpdateDataQueryRequest`
        :rtype: :class:`tencentcloud.dlc.v20210125.models.UpdateDataQueryResponse`

        """
        try:
            params = request._serialize()
            headers = request.headers
            body = self.call("UpdateDataQuery", params, headers=headers)
            response = json.loads(body)
            model = models.UpdateDataQueryResponse()
            model._deserialize(response["Response"])
            return model
        except Exception as e:
            if isinstance(e, TencentCloudSDKException):
                raise
            else:
                raise TencentCloudSDKException(e.message, e.message)


    def UpdateDatasourceConnection(self, request):
        """更新数据连接

        :param request: Request instance for UpdateDatasourceConnection.
        :type request: :class:`tencentcloud.dlc.v20210125.models.UpdateDatasourceConnectionRequest`
        :rtype: :class:`tencentcloud.dlc.v20210125.models.UpdateDatasourceConnectionResponse`

        """
        try:
            params = request._serialize()
            headers = request.headers
            body = self.call("UpdateDatasourceConnection", params, headers=headers)
            response = json.loads(body)
            model = models.UpdateDatasourceConnectionResponse()
            model._deserialize(response["Response"])
            return model
        except Exception as e:
            if isinstance(e, TencentCloudSDKException):
                raise
            else:
                raise TencentCloudSDKException(e.message, e.message)


    def UpdateHouse(self, request):
        """本接口（UpdateHouse）用于更新House配置

        :param request: Request instance for UpdateHouse.
        :type request: :class:`tencentcloud.dlc.v20210125.models.UpdateHouseRequest`
        :rtype: :class:`tencentcloud.dlc.v20210125.models.UpdateHouseResponse`

        """
        try:
            params = request._serialize()
            headers = request.headers
            body = self.call("UpdateHouse", params, headers=headers)
            response = json.loads(body)
            model = models.UpdateHouseResponse()
            model._deserialize(response["Response"])
            return model
        except Exception as e:
            if isinstance(e, TencentCloudSDKException):
                raise
            else:
                raise TencentCloudSDKException(e.message, e.message)


    def UpdateNetworkConnection(self, request):
        """更新网络配置

        :param request: Request instance for UpdateNetworkConnection.
        :type request: :class:`tencentcloud.dlc.v20210125.models.UpdateNetworkConnectionRequest`
        :rtype: :class:`tencentcloud.dlc.v20210125.models.UpdateNetworkConnectionResponse`

        """
        try:
            params = request._serialize()
            headers = request.headers
            body = self.call("UpdateNetworkConnection", params, headers=headers)
            response = json.loads(body)
            model = models.UpdateNetworkConnectionResponse()
            model._deserialize(response["Response"])
            return model
        except Exception as e:
            if isinstance(e, TencentCloudSDKException):
                raise
            else:
                raise TencentCloudSDKException(e.message, e.message)


    def UpdateRowFilter(self, request):
        """此接口用于更新行过滤规则。注意只能更新过滤规则，不能更新规格对象catalog，database和table。

        :param request: Request instance for UpdateRowFilter.
        :type request: :class:`tencentcloud.dlc.v20210125.models.UpdateRowFilterRequest`
        :rtype: :class:`tencentcloud.dlc.v20210125.models.UpdateRowFilterResponse`

        """
        try:
            params = request._serialize()
            headers = request.headers
            body = self.call("UpdateRowFilter", params, headers=headers)
            response = json.loads(body)
            model = models.UpdateRowFilterResponse()
            model._deserialize(response["Response"])
            return model
        except Exception as e:
            if isinstance(e, TencentCloudSDKException):
                raise
            else:
                raise TencentCloudSDKException(e.message, e.message)


    def UpdateTaskStatus(self, request):
        """更新任务

        :param request: Request instance for UpdateTaskStatus.
        :type request: :class:`tencentcloud.dlc.v20210125.models.UpdateTaskStatusRequest`
        :rtype: :class:`tencentcloud.dlc.v20210125.models.UpdateTaskStatusResponse`

        """
        try:
            params = request._serialize()
            headers = request.headers
            body = self.call("UpdateTaskStatus", params, headers=headers)
            response = json.loads(body)
            model = models.UpdateTaskStatusResponse()
            model._deserialize(response["Response"])
            return model
        except Exception as e:
            if isinstance(e, TencentCloudSDKException):
                raise
            else:
                raise TencentCloudSDKException(e.message, e.message)


    def UpdateUserDataEngineConfig(self, request):
        """修改用户引擎自定义配置

        :param request: Request instance for UpdateUserDataEngineConfig.
        :type request: :class:`tencentcloud.dlc.v20210125.models.UpdateUserDataEngineConfigRequest`
        :rtype: :class:`tencentcloud.dlc.v20210125.models.UpdateUserDataEngineConfigResponse`

        """
        try:
            params = request._serialize()
            headers = request.headers
            body = self.call("UpdateUserDataEngineConfig", params, headers=headers)
            response = json.loads(body)
            model = models.UpdateUserDataEngineConfigResponse()
            model._deserialize(response["Response"])
            return model
        except Exception as e:
            if isinstance(e, TencentCloudSDKException):
                raise
            else:
                raise TencentCloudSDKException(e.message, e.message)


    def UpdateUserRole(self, request):
        """更新用户角色信息

        :param request: Request instance for UpdateUserRole.
        :type request: :class:`tencentcloud.dlc.v20210125.models.UpdateUserRoleRequest`
        :rtype: :class:`tencentcloud.dlc.v20210125.models.UpdateUserRoleResponse`

        """
        try:
            params = request._serialize()
            headers = request.headers
            body = self.call("UpdateUserRole", params, headers=headers)
            response = json.loads(body)
            model = models.UpdateUserRoleResponse()
            model._deserialize(response["Response"])
            return model
        except Exception as e:
            if isinstance(e, TencentCloudSDKException):
                raise
            else:
                raise TencentCloudSDKException(e.message, e.message)


    def UpdateWorkflow(self, request):
        """编辑调度计划基本信息

        :param request: Request instance for UpdateWorkflow.
        :type request: :class:`tencentcloud.dlc.v20210125.models.UpdateWorkflowRequest`
        :rtype: :class:`tencentcloud.dlc.v20210125.models.UpdateWorkflowResponse`

        """
        try:
            params = request._serialize()
            headers = request.headers
            body = self.call("UpdateWorkflow", params, headers=headers)
            response = json.loads(body)
            model = models.UpdateWorkflowResponse()
            model._deserialize(response["Response"])
            return model
        except Exception as e:
            if isinstance(e, TencentCloudSDKException):
                raise
            else:
                raise TencentCloudSDKException(e.message, e.message)


    def UpgradeDataEngineImage(self, request):
        """升级引擎镜像

        :param request: Request instance for UpgradeDataEngineImage.
        :type request: :class:`tencentcloud.dlc.v20210125.models.UpgradeDataEngineImageRequest`
        :rtype: :class:`tencentcloud.dlc.v20210125.models.UpgradeDataEngineImageResponse`

        """
        try:
            params = request._serialize()
            headers = request.headers
            body = self.call("UpgradeDataEngineImage", params, headers=headers)
            response = json.loads(body)
            model = models.UpgradeDataEngineImageResponse()
            model._deserialize(response["Response"])
            return model
        except Exception as e:
            if isinstance(e, TencentCloudSDKException):
                raise
            else:
                raise TencentCloudSDKException(e.message, e.message)


    def ValidateWorkflowName(self, request):
        """调度计划名称合法性校验，重名校验

        :param request: Request instance for ValidateWorkflowName.
        :type request: :class:`tencentcloud.dlc.v20210125.models.ValidateWorkflowNameRequest`
        :rtype: :class:`tencentcloud.dlc.v20210125.models.ValidateWorkflowNameResponse`

        """
        try:
            params = request._serialize()
            headers = request.headers
            body = self.call("ValidateWorkflowName", params, headers=headers)
            response = json.loads(body)
            model = models.ValidateWorkflowNameResponse()
            model._deserialize(response["Response"])
            return model
        except Exception as e:
            if isinstance(e, TencentCloudSDKException):
                raise
            else:
                raise TencentCloudSDKException(e.message, e.message)