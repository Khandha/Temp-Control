<template>
  <section class="temperature-control">
    <div class="temperature-control__plate">
      <input
        type="number"
        v-model="temperature"
        class="temperature-control__input"
        disabled
      />
      <span class="temperature-control__suffix">&deg;C</span>
    </div>
    <div class="temperature-control__controls">
      <button @click="changeTemperature(+1)"></button>
      <button @click="changeTemperature(-1)"></button>
    </div>
  </section>
</template>

<script>
let dispatchDebounce;

export default {
  name: "TemperatureControl",
  props: {
    initialTemperature: {
      type: Number,
      require: true,
    },
  },
  data() {
    return {
      temperature: this.initialTemperature,
    };
  },
  methods: {
    changeTemperature(offset) {
      const newValue = this.temperature + offset;
      const stringLength = newValue.toString().length;
      if (stringLength <= 2 || (stringLength <= 3 && newValue < 0)) {
        this.temperature = newValue;
        this.dispatchEmit();
      }
    },
    dispatchEmit() {
      clearTimeout(dispatchDebounce);
      dispatchDebounce = setTimeout(() => {
        this.$emit("temp-change", this.temperature);
      }, 1500);
    },
  },
  emits: ["temp-change"],
};
</script>

<style lang="scss" scoped>
@import "../../assets/_variables.scss";

.temperature-control {
  position: relative;
  height: 35%;

  margin: 0 auto;
  top: 20px;

  @media screen and (min-width: 1200px) {
    height: 45%;
  }

  &__plate,
  &__background {
    border-radius: 50%;
    aspect-ratio: 1/1;
  }

  &__plate {
    display: flex;
    justify-content: center;
    align-items: center;

    height: 100%;
    position: relative;
    z-index: 0;
    margin: 0 auto;

    background: $blue;
    border: 8px solid $gray500;
    box-shadow: inset 0 10px 15px 0 $blackA, 0 5px 5px hsla(0, 0%, 0%, 0.05);

    &::after {
      content: "";
      position: absolute;
      height: 75%;
      width: 75%;
      top: 20%;
      border-radius: 50%;
      background-color: $gray500;
      z-index: 1;
      box-shadow: 0 0 5px 0 $blackA;
    }

    &::before {
      content: "";
      background: radial-gradient(
        circle at bottom left,
        $gray500 70%,
        transparent 70%
      );
      position: absolute;
      bottom: -12%;
      left: 25%;
      width: 50%;
      height: 50%;
      transform: rotate(135deg);
    }
  }

  &__controls {
    position: absolute;
    display: flex;
    align-items: center;
    justify-content: space-between;
    padding: 1%;
    border-radius: 16px;
    height: 25%;
    aspect-ratio: 2/1;
    background: #fafafa;
    box-shadow: 0 -4px 7px -6px $blackA, 0 5px 5px hsla(0, 0%, 0%, 0.05);
    left: 50%;
    transform: translate(-50%, 5px);
    bottom: 0;

    button {
      width: 48%;
      height: 100%;
      background: url("../../assets/chevron-down.svg") center/50% no-repeat;
      border-radius: 12px;
      box-shadow: inset 2px 2px 6px hsla(0, 0%, 0%, 0.05),
        inset -2px -2px 6px hsl(0, 0%, 94%);

      &:nth-of-type(1) {
        transform: rotate(180deg);
      }
    }
  }

  &__suffix,
  &__input {
    z-index: 2;
    font-weight: bold;
  }

  &__input {
    width: 30%;
    text-align: center;
    font-size: 26px;

    &::-webkit-inner-spin-button,
    &::-webkit-outer-spin-button {
      -webkit-appearance: none;
      margin: 0;
    }
  }

  &__suffix {
    font-size: 18px;
    opacity: 0.65;
  }
}
</style>
