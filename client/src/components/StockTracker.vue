<template>
    <div class="main">
        <h1>Currently tracking</h1>
        <div class="buttons-container">
            <button class="image-button" id="apple-button">
                <img src="../assets/apple-logo.png" alt="Apple Logo">
            </button>
            <button class="image-button" id="microsoft-button">
                <img src="../assets/microsoft-logo.png" alt="Microsoft Logo">
            </button>
            <button class="image-button" id="tesla-button">
                <img src="../assets/tesla-logo.png" alt="Tesla Logo">
            </button>
        </div>

        <h2>Performances from [StartDatePicker] to [EndDatePicker]</h2>
        <LineChart />

        <h3>How is the performance of these stocks calculated?</h3>
        <p></p>

        <h2>More statistics to look at...</h2>
        <StatsTable />

        <h3>How are these statistics calculated?</h3>
        <p></p>
    </div>
</template>

<script>
import LineChart from '../components/LineChart.vue'
import StatsTable from '../components/StatsTable.vue'

export default {
    components: { LineChart, StatsTable }
}
</script>

<style scoped>
.image-button {
  display: inline-flex;
  align-items: center;
  justify-content: center;
  color: #fff;
  padding: 10px 20px;
  border: none;
  border-radius: 5px;
  cursor: pointer;
}
.image-button img {
  height: 20px;
  width: 20px;
}
.buttons-container{
    display: flex;
    column-gap: 20px;
    align-items: flex-start;
    justify-content: left;
}
</style>