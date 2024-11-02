<template>
	<div class="container">
		<div>
			<el-space direction="horizontal" :size="30">
				<el-button type="warning" :icon="CirclePlusFilled" @click="dealingAddVisible = true">新增</el-button>
				<el-radio-group v-model="radio_filter" size="large" @change="filter_change">
					<el-radio-button label="全部" value="all" />
					<el-radio-button label="持仓" value="hold" />
					<el-radio-button label="已出" value="sold" />
				</el-radio-group>
				<el-radio-group v-model="radio_filter2" size="large" @change="filter_change">
					<el-radio-button label="同代码合并" value="merge" />
					<el-radio-button label="常规" value="no-merge" />
				</el-radio-group>
			</el-space>
		</div>
		<TableCustom :columns="columns" :tableData="tableData" :hasToolbar="false" :hasPagination="false">
			<template #_id="{ rows }">
				<span >{{ rows._id }}</span>
			</template>
			<template #code="{ rows }">
				<span >{{ rows.code }}</span>
			</template>
			<template #name="{ rows }">
				<span >{{ rows.name }}</span>
			</template>
			<template #buy_date="{ rows }">
				<span >{{ rows.buy_date }}</span>
			</template>
			<template #cost="{ rows }">
				<span >{{ rows.cost }}</span>
			</template>
			<template #buy_cost="{ rows }">
				<span >{{ rows.buy_cost }}</span>
			</template>
			<template #shares="{ rows }">
				<span >{{ rows.shares }}</span>
			</template>
			<template #sell_date="{ rows }">
				<el-input v-if="rows.editing" v-model="rows.sell_date"></el-input>
				<span v-else>{{ rows.sell_date }}</span>
			</template>
			<template #sell_price="{ rows }">
				<el-input v-if="rows.editing" v-model="rows.sell_price"></el-input>
				<span v-else>{{ rows.sell_price }}</span>
			</template>
			<template #sell_cost="{ rows }">
				<el-input v-if="rows.editing" v-model="rows.sell_cost"></el-input>
				<span v-else>{{ rows.sell_cost }}</span>
			</template>
			<template #operator="{ rows, index }">
				<template v-if="!rows.editing">
					<el-button type="primary" size="small" :icon="Edit" @click="rows.editing = true">
						编辑
					</el-button>
				</template>
				<template v-else>
					<el-button type="success" size="small" :icon="Select" @click="rows.editing = false">
						保存
					</el-button>
				</template>
			</template>
		</TableCustom>
	</div>
	<el-dialog :title="'新增'" v-model="dealingAddVisible" width="700px" destroy-on-close :close-on-click-modal="false"
		@close="closeDialog">
		<el-form :model="formNewDealing" label-width="auto" style="max-width: 600px">
			<el-form-item label="代码">
				<el-input v-model="formNewDealing.code" />
			</el-form-item>
			<el-form-item label="名称">
				<el-input v-model="formNewDealing.name" />
			</el-form-item>
			<el-form-item label="买入日期">
				<el-date-picker v-model="formNewDealing.buy_date" type="date" value-format="YYYY-MM-DD" placeholder="Pick a date"
					style="width: 100%" />
			</el-form-item>
			<el-form-item label="买入单价">
				<el-input-number v-model="formNewDealing.cost" :step="0.001" />
			</el-form-item>
			<el-form-item label="买入交易成本">
				<el-input-number v-model="formNewDealing.buy_cost" :step="0.01" />
			</el-form-item>
			<el-form-item label="数量">
				<el-input-number v-model="formNewDealing.shares" :step="100" />
			</el-form-item>
		</el-form>
		<template #footer>
			<div class="dialog-footer">
				<el-button @click="dealingAddVisible = false">Cancel</el-button>
				<el-button type="primary" @click="confirmHandler">
					Confirm
				</el-button>
			</div>
		</template>
	</el-dialog>
</template>

<script setup lang="ts" name="table-editor">
import { ref } from 'vue';
import { Delete, Edit, CloseBold, Select, CirclePlusFilled } from '@element-plus/icons-vue';
import TableCustom from '@/components/table-custom.vue';
import { fetchUserData, fetchDealingDataMerge, newDealingData } from '@/api/index';
import { FormOption, FormOptionList } from '@/types/form-option';
import { DealingItem } from '@/types/dealing';
let columns = ref([
	// { type: 'index', label: '序号', width: 55, align: 'center' },
	{ prop: '_id', label: '交易编号' , width: 50},
	{ prop: 'code', label: '代码' },
	{ prop: 'name', label: '名称' },
	{ prop: 'buy_date', label: '购入日期' },
	{ prop: 'cost', label: '买入单价' },
	{ prop: 'buy_cost', label: '买入交易成本' },
	{ prop: 'shares', label: '数目' },
	{ prop: 'sell_date', label: '售出日期' },
	{ prop: 'sell_price', label: '售价' },
	{ prop: 'sell_cost', label: '售出交易成本' },
	{ prop: 'operator', label: '操作', width: 180 },
])
const tableData = ref([]);
const radio_filter = ref('all')
const radio_filter2 = ref('no-merge')
const dealingAddVisible = ref(false);
const formNewDealing = ref({
	code: 510000,
	name: '',
	buy_date: '',
	cost: 1.0,
	buy_cost: 5.0,
	shares: 1000,
})
const getData = async () => {
	var res;
	if (radio_filter2.value == 'merge') {
		res = await fetchDealingDataMerge();
	} else {
		res = await fetchUserData();
	}
	tableData.value = [];
	for (var item of res.data.data) {
		if (radio_filter.value == 'all' || (radio_filter.value == 'hold' && !isNaN(item.sell_date)) || (radio_filter.value == 'sold' && isNaN(item.sell_date))) {
			tableData.value.push(item);
		}
	}
};
getData();

const filter_change = (val) => {
	getData();
};
const closeDialog = () => {
	dealingAddVisible.value = false;
};
const confirmHandler = () => {
	dealingAddVisible.value = false;
	newDealingData(formNewDealing.value)
};
</script>

<style scoped></style>
