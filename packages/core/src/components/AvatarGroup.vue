<script lang="ts">
import { Comment, Fragment, cloneVNode, computed, defineComponent, h, type PropType, type VNode } from 'vue'
import { toCssSize } from '../utils'
import Avatar from './Avatar.vue'

export default defineComponent({
  name: 'JmAvatarGroup',
  props: {
    /** 最多展示几个；超出部分折叠成 +N（默认全部展示） */
    max: { type: Number, default: 0 },
    /** 实际总数，用于折叠数字；不传按插槽数量 */
    total: { type: Number, default: 0 },
    /** 统一尺寸，会注入到未显式设置的子头像 */
    size: {
      type: [String, Number] as PropType<'small' | 'medium' | 'large' | number | string>,
      default: undefined,
    },
    shape: {
      type: String as PropType<'circle' | 'square'>,
      default: undefined,
    },
    /** 叠放时每个头像露出的宽度，数字按 px */
    gap: { type: [Number, String], default: 24 },
  },
  setup(props, { slots }) {
    const styles = computed(() => ({
      '--jm-avatar-group-gap': toCssSize(props.gap) ?? '24px',
    }))

    /** v-for 在插槽里是一层 Fragment，必须先摊平才能按 max 切片 */
    function flatten(nodes: VNode[]): VNode[] {
      const out: VNode[] = []
      for (const node of nodes) {
        if (!node || node.type === Comment) continue
        if (node.type === Fragment && Array.isArray(node.children)) {
          out.push(...flatten(node.children as VNode[]))
        } else {
          out.push(node)
        }
      }
      return out
    }

    return () => {
      const list = flatten(slots.default?.() ?? [])
      const max = Number(props.max) || 0
      const total = Number(props.total) || list.length

      const overflow = max > 0 && total > max
      const visibleCount = overflow ? Math.max(0, max - 1) : list.length
      const visible = list.slice(0, visibleCount).map((vnode) => {
        if (!vnode || typeof vnode !== 'object') return vnode
        const injected: Record<string, unknown> = {}
        const own = (vnode.props ?? {}) as Record<string, unknown>
        if (props.size !== undefined && own.size === undefined) injected.size = props.size
        if (props.shape !== undefined && own.shape === undefined) injected.shape = props.shape
        return Object.keys(injected).length ? cloneVNode(vnode, injected) : vnode
      })

      if (overflow) {
        const rest = total - visibleCount
        visible.push(
          h(
            Avatar,
            {
              size: props.size,
              shape: props.shape,
              class: 'jm-avatar-group__rest',
              background: 'var(--jm-bg-input)',
              color: 'var(--jm-text-secondary)',
            },
            { default: () => `+${rest}` },
          ),
        )
      }

      return h('div', { class: 'jm-avatar-group', style: styles.value }, visible)
    }
  },
})
</script>

<style>
.jm-avatar-group {
  display: inline-flex;
  align-items: center;
  font-family: var(--jm-font-family);
}

/* 叠放：除第一个外都往左压，露出 gap 指定的宽度 */
.jm-avatar-group > .jm-avatar + .jm-avatar {
  margin-left: calc(var(--jm-avatar-group-gap, 24px) - var(--jm-avatar-size, 40px));
}

/* 后面的压在前面的上面，视觉上更像「一叠卡片」 */
.jm-avatar-group > .jm-avatar {
  position: relative;
}

.jm-avatar-group > .jm-avatar:nth-child(2) {
  z-index: 2;
}

.jm-avatar-group > .jm-avatar:nth-child(3) {
  z-index: 3;
}

.jm-avatar-group > .jm-avatar:nth-child(4) {
  z-index: 4;
}

.jm-avatar-group > .jm-avatar:nth-child(n + 5) {
  z-index: 5;
}

.jm-avatar-group__rest {
  font-size: calc(var(--jm-avatar-size, 40px) * 0.3);
  text-align: center;
}
</style>
