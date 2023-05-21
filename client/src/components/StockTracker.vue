<template>
    <div class="main">
        <h1 class="title">Stock Tracker</h1>
        <h3>Currently tracking the past 2 years</h3>
        <Chart />

        <h3>How is the performance of these stocks calculated?</h3>
        <p>The performance is currently simply calculated based on the closing price each day.</p>
        <p>I thought of using a combination of price fluctuation with the closing price but it didn't look as cool as this graph.</p>
        <p>These stocks are prorated based on the first one, so they all start at 100, handy for comparisons.</p>

        <StatsTable />
        <h3>How are these statistics calculated?</h3>
        <p>Cumulative Return = ([Closing price] - [Opening price]) / [Opening price]</p>
        <p>Annualized Return = ([Closing price] / [Opening price])^(1 / [Period in years]) - 1</p>
        <p>Annualized Volatility = Standard Deviation of ([([Sum of [daily % change - average % change]]^2) / Number of days - 1])</p>
    </div>
</template>

<script>
import Chart from './Chart.vue';
import StatsTable from './StatsTable.vue'

export default {
    name: "StockTracker",
    components: { StatsTable, Chart },
}
</script>