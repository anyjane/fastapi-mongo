<template>
	<div class="container">
		<TableCustom :columns="columns" :tableData="tableData" :hasToolbar="false" :hasPagination="false">
			<template #code="{ rows }">
				<el-input v-if="rows.editing" v-model="rows.code"></el-input>
				<span v-else>{{ rows.code }}</span>
			</template>
			<template #name="{ rows }">
				<el-input v-if="rows.editing" v-model="rows.name"></el-input>
				<span v-else>{{ rows.name }}</span>
			</template>
			<template #buy_date="{ rows }">
				<el-input v-if="rows.editing" v-model="rows.buy_date"></el-input>
				<span v-else>{{ rows.buy_date }}</span>
			</template>
			<template #cost="{ rows }">
				<el-input v-if="rows.editing" v-model="rows.cost"></el-input>
				<span v-else>{{ rows.cost }}</span>
			</template>
			<template #shares="{ rows }">
				<el-input v-if="rows.editing" v-model="rows.shares"></el-input>
				<span v-else>{{ rows.shares }}</span>
			</template>
			<template #sell_date="{ rows }">
				<el-input v-if="rows.editing" v-model="rows.sell_date"></el-input>
				<span v-else>{{ rows.sell_date }}</span>
			</template>
			<template #sell_price="{ rows }">
				<el-input v-if="rows.editing" v-model="rows.sell_price"></el-input>
				<span v-else>{{ rows.sell_price }}</span>
			</template>
			<template #operator="{ rows, index }">
				<template v-if="!rows.editing">
					<el-button type="primary" size="small" :icon="Edit" @click="handleEdit(rows)">
						编辑
					</el-button>
					<el-button type="danger" size="small" :icon="Delete" @click="">
						删除
					</el-button>
				</template>
				<template v-else>
					<el-button type="success" size="small" :icon="Select" @click="rows.editing = false">
						保存
					</el-button>
					<el-button type="default" size="small" :icon="CloseBold" @click="handleCancel(rows, index)">
						取消
					</el-button>
				</template>
			</template>
		</TableCustom>
	</div>
</template>

<script setup lang="ts" name="table-editor">
import { ref } from 'vue';
import { Delete, Edit, CloseBold, Select } from '@element-plus/icons-vue';
import TableCustom from '@/components/table-custom.vue';
import { fetchUserData } from '@/api/index';

let columns = ref([
	{ type: 'index', label: '序号', width: 55, align: 'center' },
	{ prop: 'code', label: '代码' },
	{ prop: 'name', label: '名称' },
	{ prop: 'buy_date', label: '购入' },
	{ prop: 'cost', label: '成本' },
	{ prop: 'shares', label: '数目' },
	{ prop: 'sell_date', label: '售出'},
	{ prop: 'sell_price', label: '售价'},
	{ prop: 'operator', label: '操作', width: 180 },
])
const tableData = ref([]);
const getData = async () => {
	const res = await fetchUserData();
	tableData.value = res.data.data;
};
getData();

const rowData = ref({})

const handleEdit = (row) => {
	rowData.value = { ...row };
	row.editing = true;
};

const handleCancel = (row, index) => {
	row.editing = false;
	tableData.value[index] = { ...rowData.value };
};
</script>

<style scoped></style>
