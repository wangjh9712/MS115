<template>
  <div class="workflow-page">
    <div class="page-header">
      <h2>工作流</h2>
      <el-button type="primary" @click="refreshWorkflows" :loading="loading">刷新</el-button>
    </div>

    <el-card>
      <div class="table-wrap">
        <el-table :data="workflows" v-loading="loading" size="small">
        <el-table-column prop="name" label="名称" min-width="160" />
        <el-table-column prop="trigger_type" label="触发方式" width="120" />
        <el-table-column prop="timer" label="定时表达式" min-width="140" />
        <el-table-column prop="state" label="状态" width="80" />
        <el-table-column prop="run_count" label="运行次数" width="100" />
        <el-table-column label="操作" width="260">
          <template #default="{ row }">
            <el-button text type="primary" @click="runWorkflow(row.id)">执行</el-button>
            <el-button text type="success" @click="startWorkflow(row.id)">启用</el-button>
            <el-button text type="warning" @click="pauseWorkflow(row.id)">停用</el-button>
            <el-button text type="danger" @click="deleteWorkflow(row.id)">删除</el-button>
          </template>
        </el-table-column>
        </el-table>
      </div>
    </el-card>
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue'
import { ElMessage, ElMessageBox } from 'element-plus'
import { workflowApi } from '@/api'

const loading = ref(false)
const workflows = ref([])

const refreshWorkflows = async () => {
  loading.value = true
  try {
    const { data } = await workflowApi.list()
    workflows.value = data || []
  } catch (error) {
    ElMessage.error('获取工作流失败')
  } finally {
    loading.value = false
  }
}

const runWorkflow = async (id) => {
  try {
    await workflowApi.run(id)
    ElMessage.success('工作流已触发')
    await refreshWorkflows()
  } catch (error) {
    ElMessage.error('执行失败')
  }
}

const startWorkflow = async (id) => {
  try {
    await workflowApi.start(id)
    ElMessage.success('工作流已启用')
    await refreshWorkflows()
  } catch (error) {
    ElMessage.error('启用失败')
  }
}

const pauseWorkflow = async (id) => {
  try {
    await workflowApi.pause(id)
    ElMessage.success('工作流已停用')
    await refreshWorkflows()
  } catch (error) {
    ElMessage.error('停用失败')
  }
}

const deleteWorkflow = async (id) => {
  try {
    await ElMessageBox.confirm('确认删除该工作流吗？', '提示', { type: 'warning' })
    await workflowApi.delete(id)
    ElMessage.success('工作流已删除')
    await refreshWorkflows()
  } catch (error) {
    if (error !== 'cancel') {
      ElMessage.error('删除失败')
    }
  }
}

onMounted(refreshWorkflows)
</script>

<style lang="scss" scoped>
.workflow-page {
  display: flex;
  flex-direction: column;
  gap: 16px;

  .page-header {
    display: flex;
    justify-content: space-between;
    align-items: center;
  }

  .table-wrap {
    overflow-x: auto;

    .el-table {
      min-width: 840px;
    }
  }
}

@media (max-width: 1024px) {
  .workflow-page {
    .page-header {
      flex-direction: column;
      align-items: flex-start;
      gap: 10px;

      :deep(.el-button) {
        width: 100%;
      }
    }
  }
}
</style>
