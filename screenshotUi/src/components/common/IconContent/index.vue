<template>
  <div :class="contentClass">
    <svg class="icon" aria-hidden="true">
      <use :xlink:href="iconfontName"></use>
    </svg>
    <span class="content">{{ content }}</span>
  </div>
</template>

<script>
export default {
  name: 'IconContent',
  data() {
    return {}
  },
  props: {
    iconName: {
      type: String,
      required: true,
    },
    content: {
      type: String,
      required: false,
    },
    position: {
      type: String,
      required: false,
      default: 'bottom',
    },
  },
  computed: {
    iconfontName() {
      return '#icon-' + this.iconName
    },
    contentClass() {
      switch (this.position) {
        case 'bottom':
          return 'icon-content content-bottom'
        case 'right':
          return 'icon-content content-right'
      }
    },
  },
}
</script>
<style scoped>
@import './style.css';
</style>
