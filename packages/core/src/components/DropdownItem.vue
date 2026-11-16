<script setup lang="ts">
import { computed, inject } from 'vue'
import Icon from './Icon.vue'
import { DROPDOWN_MENU_KEY, type DropdownOption } from './dropdown-context'

defineOptions({ name: 'JmDropdownItem' })

const props = withDefaults(
  defineProps<{
    /** 选中值；multiple 时为数组 */
    modelValue?: string | number | (string | number)[] | null
    options?: DropdownOption[]
    /** 自定义标题，不传时用选中项文案 */
    title?: string
    /** 未选中时的占位文案 */
    placeholder?: string
    /** 禁用（不可展开） */
    disabled?: boolean
    /** 多选模式 */
    multiple?: boolean
    /** 选项区最大高度，超出滚动，数字按 px */
    maxHeight?: number | string
  }>(),
  { options: () => [], placeholder: '请选择', multiple: false },
)

const emit = defineEmits<{
  'update:modelValue': [value: string | number | (string | number)[]]
  change: [value: string | number | (string | number)[], option: DropdownOption | null]
  open: []
  close: []
}>()

const menu = inject(DROPDOWN_MENU_KEY, null)
const index = menu ? menu.register() : 0

const opened = computed(() => menu?.active.value === index)

const selectedValues = computed<(string | number)[]>(() => {
  if (props.multiple) {
    return Array.isArray(props.modelValue) ? [...props.modelValue] : []
  }
  return props.modelValue === null || props.modelValue === undefined ? [] : [props.modelValue as string | number]
})

const selectedTexts = computed(() =>
  props.options
    .filter((o) => selectedValues.value.includes(o.value))
    .map((o) => o.text),
)

const displayTitle = computed(() => {
  if (props.title) return props.title
  if (!selectedTexts.value.length) return props.placeholder
  return props.multiple ? `${selectedTexts.value[0]} 等 ${selectedTexts.value.length} 项` : selectedTexts.value[0]
})

const panelStyle = computed(() => {
  const s: Record<string, string> = {}
  if (props.maxHeight !== undefined) {
    s.maxHeight = typeof props.maxHeight === 'number' ? `${props.maxHeight}px` : props.maxHeight
  }
  return s
})

const activeColor = computed(() => menu?.activeColor.value)

function onTitleClick() {
  if (props.disabled) return
  menu?.toggle(index)
  if (!opened.value) emit('open')
  else emit('close')
}

function isSelected(opt: DropdownOption): boolean {
  return selectedValues.value.includes(opt.value)
}

function onSelect(opt: DropdownOption) {
  if (opt.disabled) return
  let next: string | number | (string | number)[]
  if (props.multiple) {
    const list = selectedValues.value
    next = list.includes(opt.value) ? list.filter((v) => v !== opt.value) : [...list, opt.value]
  } else {
    next = opt.value
  }
  emit('update:modelValue', next)
  emit('change', next, opt)
  if (!props.multiple && menu?.closeOnClickOption.value) {
    menu.close()
    emit('close')
  }
}
</script>

<template>
  <div class="jm-dropdown-item" :class="{ 'is-opened': opened, 'is-disabled': disabled }">
    <button
      type="button"
      class="jm-dropdown-item__title"
      :disabled="disabled"
      :aria-expanded="opened"
      @click="onTitleClick"
    >
      <span
        class="jm-dropdown-item__text"
        :class="{ 'is-active': opened || selectedValues.length > 0 }"
        :style="opened || selectedValues.length ? { color: activeColor } : undefined"
      >{{ displayTitle }}</span>
      <Icon
        class="jm-dropdown-item__arrow"
        :class="{ 'is-open': opened }"
        name="chevron-down"
        :size="16"
        :color="opened ? activeColor : undefined"
      />
    </button>

    <Transition name="jm-dropdown-panel">
      <div v-if="opened" class="jm-dropdown-item__panel" :style="panelStyle">
        <slot>
          <ul class="jm-dropdown-item__options" role="listbox">
            <li
              v-for="opt in options"
              :key="opt.value"
              class="jm-dropdown-item__option"
              :class="{
                'is-active': isSelected(opt),
                'is-disabled': opt.disabled,
              }"
              role="option"
              :aria-selected="isSelected(opt)"
              @click="onSelect(opt)"
            >
              <Icon v-if="opt.icon" class="jm-dropdown-item__opt-icon" :name="opt.icon" :size="18" />
              <span class="jm-dropdown-item__opt-text">{{ opt.text }}</span>
              <Icon
                v-if="isSelected(opt)"
                class="jm-dropdown-item__check"
                name="check"
                :size="16"
                :color="activeColor ?? 'var(--jm-color-primary)'"
              />
            </li>
          </ul>
        </slot>
      </div>
    </Transition>
  </div>
</template>

<style>
.jm-dropdown-item {
  display: flex;
  flex: 1 1 0;
  min-width: 0;
}

.jm-dropdown-item__title {
  display: flex;
  flex: 1 1 auto;
  align-items: center;
  justify-content: center;
  gap: 2px;
  min-width: 0;
  padding: 0 8px;
  border: none;
  background: transparent;
  font-family: inherit;
  font-size: var(--jm-font-size-sm);
  color: var(--jm-text-primary);
  cursor: pointer;
  -webkit-tap-highlight-color: transparent;
}

.jm-dropdown-item__title:disabled {
  color: var(--jm-text-tertiary);
  cursor: not-allowed;
}

.jm-dropdown-item__text {
  overflow: hidden;
  text-overflow: ellipsis;
  white-space: nowrap;
  max-width: calc(100% - 18px);
  transition: color var(--jm-motion-color, 0.2s ease);
}

.jm-dropdown-item__arrow {
  transition: transform 0.2s ease;
}

.jm-dropdown-item__arrow.is-open {
  transform: rotate(180deg);
}

.jm-dropdown-item__panel {
  position: absolute;
  top: 100%;
  left: 0;
  right: 0;
  z-index: 1;
  overflow-y: auto;
  background: var(--jm-bg-container);
  box-shadow: 0 8px 16px rgba(0, 0, 0, 0.08);
}

.jm-dropdown-item__options {
  margin: 0;
  padding: 4px 0;
  list-style: none;
}

.jm-dropdown-item__option {
  display: flex;
  align-items: center;
  gap: 8px;
  padding: 0 16px;
  height: 44px;
  font-size: var(--jm-font-size-sm);
  color: var(--jm-text-primary);
  cursor: pointer;
}

.jm-dropdown-item__option:active {
  background: var(--jm-bg-input);
}

.jm-dropdown-item__option.is-active {
  color: var(--jm-color-primary);
  font-weight: var(--jm-font-weight-medium, 500);
}

.jm-dropdown-item__option.is-disabled {
  color: var(--jm-text-tertiary);
  cursor: not-allowed;
}

.jm-dropdown-item__opt-text {
  flex: 1 1 auto;
  min-width: 0;
  overflow: hidden;
  text-overflow: ellipsis;
  white-space: nowrap;
}

.jm-dropdown-item__check {
  flex: none;
}

.jm-dropdown-panel-enter-active,
.jm-dropdown-panel-leave-active {
  transition: opacity 0.18s ease, transform 0.18s ease;
  transform-origin: top center;
}

.jm-dropdown-panel-enter-from,
.jm-dropdown-panel-leave-to {
  opacity: 0;
  transform: translateY(-6px);
}
</style>
