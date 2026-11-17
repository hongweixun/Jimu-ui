<script setup lang="ts">
import { computed, ref } from 'vue'
import {
  Button,
  Cell,
  Checkbox,
  CheckboxGroup,
  Form,
  FormItem,
  Input,
  Picker,
  Popup,
  Radio,
  RadioGroup,
  Rate,
  Stepper,
  Switch,
  Uploader,
} from 'jimu-ui'
import type { FormRule } from 'jimu-ui'

const formRef = ref<InstanceType<typeof Form>>()

const model = ref({
  gender: '女',
  features: ['预售'] as (string | number)[],
  city: '',
  cityValues: [] as (string | number)[],
  rating: 0,
  count: 2,
  notify: true,
  remark: '',
  photos: [] as (string | { url: string })[],
})

/* ---------- 单选 / 多选 ---------- */
const genders = ['女', '男', '保密']
const features = ['包邮', '预售', '免税', '赠品']

/* ---------- 下拉（Cell + Popup + Picker） ---------- */
const cities = ['北京', '上海', '广州', '深圳', '杭州', '成都']
const showCity = ref(false)
const cityLabel = computed(() => model.value.city || '请选择所在城市')
function onCityConfirm(p: { selectedOptions: Array<{ text: string | number }> }) {
  model.value.city = String(p.selectedOptions[0]?.text ?? '')
  showCity.value = false
}

/* ---------- 校验规则 ---------- */
const cityRules: FormRule[] = [{ required: true, message: '请选择所在城市' }]
const ratingRules: FormRule[] = [
  { validator: (v: number) => (v > 0 ? true : '请给出评分') },
]
const countRules: FormRule[] = [
  { validator: (v: number) => (v >= 1 && v <= 6 ? true : '每单限购 1~6 件') },
]

const result = ref('填写后点「提交」看校验结果')

async function onSubmit() {
  const passed = await formRef.value?.validate()
  if (passed) {
    result.value = `✅ ${JSON.stringify(
      { ...model.value, photos: `${model.value.photos.length} 张图` },
      null,
      0,
    )}`
  } else {
    result.value = '❌ 校验未通过，已滚动到第一个错误字段'
  }
}
</script>

<template>
  <div class="demo-page">
    <Form
      ref="formRef"
      :model="model"
      scroll-to-error
      label-width="72"
      @submit="onSubmit"
    >
      <FormItem name="gender" label="性别">
        <RadioGroup v-model="model.gender" direction="horizontal">
          <Radio v-for="g in genders" :key="g" :value="g">{{ g }}</Radio>
        </RadioGroup>
      </FormItem>

      <FormItem name="features" label="服务标签">
        <CheckboxGroup v-model="model.features" direction="horizontal">
          <Checkbox v-for="f in features" :key="f" :value="f">{{ f }}</Checkbox>
        </CheckboxGroup>
      </FormItem>

      <FormItem name="city" label="城市" :rules="cityRules">
        <Cell
          :value="cityLabel"
          is-link
          clickable
          :border="false"
          @click="showCity = true"
        />
      </FormItem>

      <FormItem name="rating" label="评分" :rules="ratingRules">
        <Rate v-model="model.rating" allow-half />
      </FormItem>

      <FormItem name="count" label="购买数量" :rules="countRules">
        <Stepper v-model="model.count" :min="1" :max="6" />
      </FormItem>

      <FormItem name="notify" label="物流通知">
        <Switch v-model="model.notify" />
      </FormItem>

      <FormItem name="photos" label="凭证照片">
        <Uploader v-model="model.photos" :max-count="3" />
      </FormItem>

      <FormItem name="remark" label="备注">
        <Input
          v-model="model.remark"
          type="textarea"
          rows="2"
          placeholder="选填，最多 60 字"
          maxlength="60"
          show-word-limit
        />
      </FormItem>

      <div class="submit-row">
        <Button type="primary" block native-type="submit">提交</Button>
      </div>
    </Form>

    <p class="demo-tip">{{ result }}</p>

    <Popup v-model:show="showCity" position="bottom" round :teleport="false">
      <Picker
        v-model="model.cityValues"
        title="选择城市"
        :columns="cities"
        @confirm="onCityConfirm"
        @cancel="showCity = false"
      />
    </Popup>
  </div>
</template>

<style scoped>
.submit-row {
  padding: 12px;
}

.demo-tip {
  padding: 0 12px;
  font-size: var(--jm-font-size-sm);
  color: var(--jm-text-color-2);
  word-break: break-all;
}
</style>
