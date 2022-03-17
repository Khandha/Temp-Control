<template>
  <div class="summary__value">
    <span>
      {{value ? value : '-'}}
    </span>
    <span v-if="typeof value === 'number'">
      &deg;C
    </span>
  </div>
</template>

<script>
export default {
  props: {
    value: {
      type: [Number, String],
      require: true,
      default: null
    }
  },
}
</script>