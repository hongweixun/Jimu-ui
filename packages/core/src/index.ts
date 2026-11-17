import type { App, Plugin } from 'vue'

import '@jimu/tokens/index.css'
import './styles/base.css'
import './styles/ripple.css'

import Button from './components/Button.vue'
import Tag from './components/Tag.vue'
import Divider from './components/Divider.vue'
import Cell from './components/Cell.vue'
import CellGroup from './components/CellGroup.vue'
import Badge from './components/Badge.vue'
import Switch from './components/Switch.vue'
import Checkbox from './components/Checkbox.vue'
import CheckboxGroup from './components/CheckboxGroup.vue'
import Radio from './components/Radio.vue'
import RadioGroup from './components/RadioGroup.vue'
import Input from './components/Input.vue'
import Form from './components/Form.vue'
import FormItem from './components/FormItem.vue'
import Search from './components/Search.vue'
import Stepper from './components/Stepper.vue'
import Progress from './components/Progress.vue'
import Rate from './components/Rate.vue'
import Tabs from './components/Tabs.vue'
import Tab from './components/Tab.vue'
import NavBar from './components/NavBar.vue'
import Tabbar from './components/Tabbar.vue'
import TabbarItem from './components/TabbarItem.vue'
import Steps from './components/Steps.vue'
import Step from './components/Step.vue'
import Timeline from './components/Timeline.vue'
import TimelineItem from './components/TimelineItem.vue'
import Statistic from './components/Statistic.vue'
import Signature from './components/Signature.vue'
import PhotoWall from './components/PhotoWall.vue'
import Card from './components/Card.vue'
import Descriptions from './components/Descriptions.vue'
import DescriptionsItem from './components/DescriptionsItem.vue'
import Tooltip from './components/Tooltip.vue'
import Tree from './components/Tree.vue'
import TreeSelect from './components/TreeSelect.vue'
import Transfer from './components/Transfer.vue'
import Table from './components/Table.vue'
import LoadingBarHost from './components/LoadingBarHost.vue'
import Scanner from './components/Scanner.vue'
import SafeBottom from './components/SafeBottom.vue'
import Collapse from './components/Collapse.vue'
import CollapseItem from './components/CollapseItem.vue'
import Popup from './components/Popup.vue'
import ActionSheet from './components/ActionSheet.vue'
import Dialog from './components/Dialog.vue'
import Loading from './components/Loading.vue'
import Empty from './components/Empty.vue'
import Skeleton from './components/Skeleton.vue'
import SkeletonAvatar from './components/SkeletonAvatar.vue'
import SkeletonTitle from './components/SkeletonTitle.vue'
import SkeletonParagraph from './components/SkeletonParagraph.vue'
import VirtualList from './components/VirtualList.vue'
import NoticeBar from './components/NoticeBar.vue'
import Sticky from './components/Sticky.vue'
import Grid from './components/Grid.vue'
import GridItem from './components/GridItem.vue'
import Image from './components/Image.vue'
import Swipe from './components/Swipe.vue'
import SwipeItem from './components/SwipeItem.vue'
import PullRefresh from './components/PullRefresh.vue'
import List from './components/List.vue'
import Picker from './components/Picker.vue'
import Uploader from './components/Uploader.vue'
import ImagePreview from './components/ImagePreview.vue'
import Calendar from './components/Calendar.vue'
import CascadePicker from './components/CascadePicker.vue'
import Icon from './components/Icon.vue'
import Space from './components/Space.vue'
import Row from './components/Row.vue'
import Col from './components/Col.vue'
import Avatar from './components/Avatar.vue'
import AvatarGroup from './components/AvatarGroup.vue'
import SwipeCell from './components/SwipeCell.vue'
import Slider from './components/Slider.vue'
import DropdownMenu from './components/DropdownMenu.vue'
import DropdownItem from './components/DropdownItem.vue'
import DatePicker from './components/DatePicker.vue'
import IndexBar from './components/IndexBar.vue'
import IndexAnchor from './components/IndexAnchor.vue'
import CountDown from './components/CountDown.vue'
import Circle from './components/Circle.vue'
import NumberKeyboard from './components/NumberKeyboard.vue'
import PasswordInput from './components/PasswordInput.vue'
import Result from './components/Result.vue'
import Watermark from './components/Watermark.vue'
import Notify from './components/Notify.vue'
import Popover from './components/Popover.vue'
import Segmented from './components/Segmented.vue'
import Fab from './components/Fab.vue'
import BackTop from './components/BackTop.vue'
import CheckTag from './components/CheckTag.vue'
import Pagination from './components/Pagination.vue'
import Ellipsis from './components/Ellipsis.vue'
import Video from './components/Video.vue'
import Drag from './components/Drag.vue'
import QRCode from './components/QRCode.vue'
import Guide from './components/Guide.vue'

import { setupAppearance } from './composables/useAppearance'
import { vRipple } from './utils/ripple'

export const version = '0.25.0'

export {
  Button,
  Tag,
  Divider,
  Cell,
  CellGroup,
  Badge,
  Switch,
  Checkbox,
  CheckboxGroup,
  Radio,
  RadioGroup,
  Input,
  Form,
  FormItem,
  Search,
  Stepper,
  Progress,
  Rate,
  Tabs,
  Tab,
  NavBar,
  Tabbar,
  TabbarItem,
  Steps,
  Step,
  Collapse,
  CollapseItem,
  Popup,
  ActionSheet,
  Dialog,
  Loading,
  Empty,
  Skeleton,
  SkeletonAvatar,
  SkeletonTitle,
  SkeletonParagraph,
  VirtualList,
  NoticeBar,
  Sticky,
  Grid,
  GridItem,
  Image,
  Swipe,
  SwipeItem,
  PullRefresh,
  List,
  Picker,
  CascadePicker,
  Uploader,
  ImagePreview,
  Calendar,
  Icon,
  Space,
  Row,
  Col,
  Avatar,
  AvatarGroup,
  SwipeCell,
  Slider,
  DropdownMenu,
  DropdownItem,
  DatePicker,
  IndexBar,
  IndexAnchor,
  CountDown,
  Circle,
  NumberKeyboard,
  PasswordInput,
  Result,
  Watermark,
  Notify,
  Popover,
  Segmented,
  Fab,
  BackTop,
  CheckTag,
  Pagination,
  Drag,
  QRCode,
  Guide,
  Ellipsis,
  Video,
  Timeline,
  TimelineItem,
  Statistic,
  Signature,
  PhotoWall,
  Card,
  Descriptions,
  DescriptionsItem,
  Tooltip,
  Tree,
  TreeSelect,
  Transfer,
  Table,
  LoadingBarHost,
  Scanner,
  SafeBottom,
}

export { showToast, closeToast, toastState } from './components/toast'
export { showSnackbar, clearSnackbar, snackbarState } from './components/snackbar'
export { showNotify, closeNotify, notifyState } from './components/notify'
export type { NotifyOptions, NotifyType, NotifyItem } from './components/notify'
export { showImagePreview, closeImagePreview, imagePreviewState } from './components/image-preview'
export type { ImagePreviewOptions } from './components/image-preview'
export type { ToastOptions, ToastType, ToastPosition } from './components/toast'
export type { SnackbarOptions, SnackbarType, SnackbarPosition, SnackbarHandle } from './components/snackbar'
export { showLoadingBar, hideLoadingBar, loadingBarState } from './components/loading-bar'
export type { LoadingBarOptions, LoadingBarController } from './components/loading-bar'

export { appearance, setupAppearance, useAppearance } from './composables/useAppearance'
export type { ThemeMode } from './composables/useAppearance'

/* ---- 组合式函数（横切能力） ---- */
export { useFocusTrap } from './composables/useFocusTrap'
export type { FocusTrapOptions } from './composables/useFocusTrap'
export { useIntersection } from './composables/useIntersection'
export type { UseIntersectionOptions, UseIntersectionReturn } from './composables/useIntersection'
export { useCountDown } from './composables/useCountDown'
export type { UseCountDownOptions, UseCountDownReturn } from './composables/useCountDown'
export { useClickOutside, useClickOutsideWhen } from './composables/useClickOutside'
export type { UseClickOutsideOptions } from './composables/useClickOutside'
export { useLockScroll } from './composables/useLockScroll'
export { useSwipe } from './composables/useSwipe'
export type { UseSwipeOptions, UseSwipeReturn, SwipeDirection } from './composables/useSwipe'
export { useDebounceFn, useThrottleFn } from './composables/useDebounceFn'
export type {
  UseDebounceFnOptions,
  UseThrottleFnOptions,
  PausableFn,
} from './composables/useDebounceFn'

/* ---- 指令（横切能力） ---- */
/* vLongpress 别名：模板里写 v-longpress 时，<script setup> 局部绑定的
   camel 化结果是 vLongpress（小写 p），用 vLongPress 会匹配不上而走全局查找 */
export { vLongPress, vLongPress as vLongpress } from './directives/longpress'
export type { LongPressOptions } from './directives/longpress'
export { vCopy } from './directives/copy'
export type { CopyOptions } from './directives/copy'
export { vLazy } from './directives/lazy'
export type { LazyOptions } from './directives/lazy'

export { vRipple } from './utils/ripple'
export type { RippleOptions } from './utils/ripple'

export { withInstall, hexToRgba, toCssSize, lockScroll, unlockScroll, isClient } from './utils'
export type { SFCWithInstall } from './utils'

export type {
  ComponentType,
  ComponentSize,
  ActionSheetAction,
  UploaderFile,
  UploaderHelpers,
  UploaderRequest,
  CountDownTimeData,
  CircleColorStop,
  SegmentedOption,
} from './types'
export type {
  DatePickerType,
  DatePickerUnit,
  DatePickerFormatter,
  DatePickerConfirmPayload,
} from './components/date-picker-context'
export { registerIcon, hasIcon, iconNames, icons } from './components/icons'
export type { IconDefinition } from './components/icons'
export type { DropdownOption } from './components/dropdown-context'
export type { CollapseName } from './components/collapse-context'
export type { StepStatus } from './components/steps-context'
export type { TabName, TabItem } from './components/tabs-context'
export type { TimelineType } from './components/timeline-context'
export type { PhotoWallItem } from './components/photo-wall-context'
export type { TreeNode, TreeCheckState, TreeCheckInfo, TreeExpandInfo } from './components/tree-context'
export type { TransferItem } from './components/transfer-context'
export type { TableColumn } from './components/table-context'
export type {
  DescriptionsDirection,
  DescriptionsAlign,
  DescriptionsSize,
} from './components/descriptions-context'
export type { TabbarName } from './components/tabbar-context'
export type { FormRule, FormValidateState, FormValidateTrigger } from './components/form-context'
export type {
  PickerOption,
  PickerFieldNames,
  PickerConfirmPayload,
  CascadeOption,
} from './components/picker-context'
export type {
  CalendarType,
  CalendarShape,
  CalendarSwitchMode,
  CalendarDay,
  CalendarDayType,
  CalendarFormatter,
  CalendarValue,
} from './components/calendar-context'

const components = [
  Button,
  Tag,
  Divider,
  Cell,
  CellGroup,
  Badge,
  Switch,
  Checkbox,
  CheckboxGroup,
  Radio,
  RadioGroup,
  Input,
  Form,
  FormItem,
  Search,
  Stepper,
  Progress,
  Rate,
  Tabs,
  Tab,
  NavBar,
  Tabbar,
  TabbarItem,
  Steps,
  Step,
  Collapse,
  CollapseItem,
  Popup,
  ActionSheet,
  Dialog,
  Loading,
  Empty,
  Skeleton,
  SkeletonAvatar,
  SkeletonTitle,
  SkeletonParagraph,
  VirtualList,
  NoticeBar,
  Sticky,
  Grid,
  GridItem,
  Image,
  Swipe,
  SwipeItem,
  PullRefresh,
  List,
  Picker,
  CascadePicker,
  Uploader,
  ImagePreview,
  Calendar,
  Icon,
  Space,
  Row,
  Col,
  Avatar,
  AvatarGroup,
  SwipeCell,
  Slider,
  DropdownMenu,
  DropdownItem,
  DatePicker,
  IndexBar,
  IndexAnchor,
  CountDown,
  Circle,
  NumberKeyboard,
  PasswordInput,
  Result,
  Watermark,
  Notify,
  Popover,
  Segmented,
  Fab,
  BackTop,
  CheckTag,
  Pagination,
  Drag,
  QRCode,
  Guide,
  Ellipsis,
  Video,
  Timeline,
  TimelineItem,
  Statistic,
  Signature,
  PhotoWall,
  Card,
  Descriptions,
  DescriptionsItem,
  Tooltip,
  Tree,
  TreeSelect,
  Transfer,
  Table,
  LoadingBarHost,
  Scanner,
  SafeBottom,
]

/** 全量安装：app.use(JimuUI) */
const JimuUI: Plugin & { version: string } = {
  version,
  install(app: App) {
    components.forEach((comp) => {
      if (comp.name) app.component(comp.name, comp)
    })
    app.directive('ripple', vRipple)
    setupAppearance()
  },
}

export default JimuUI
