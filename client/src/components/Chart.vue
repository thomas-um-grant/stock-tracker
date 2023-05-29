<template>
  <div class="lineChart">
    <div id="chartContainer" style="position: relative;">
      <canvas ref="stockChartCanvas"></canvas>
    </div>
  </div>
</template>

<script>
    import { ref, onMounted } from 'vue';
    import Chart from 'chart.js/auto';
    import axios from 'axios';

    export default {
        name: 'Chart',
        setup(){
            Chart.defaults.backgroundColor = '#5C87AD';
            Chart.defaults.borderColor = '#5C87AD';

            const stockChartCanvas = ref(null);
            const stockChart = ref(null);
            const stockData = ref(null);

            const buildChart = () => {
                stockChart.value = new Chart(stockChartCanvas.value, {
                    type: 'line',
                    data: stockData.value,
                    options: {
                        responsive: true,
                        elements: {
                            point: {
                                pointStyle: false
                            },
                        },
                    }
                });
            };

            const getLatestStockInfos = async () => {
                const path = '/stocks';
                try {
                    const response = await axios.get(path);
                    stockData.value = response.data;
                } catch (error) {
                    console.error(error);
                }
            };

            onMounted(() => {
                stockChartCanvas.value = stockChartCanvas.value.getContext('2d');
                getLatestStockInfos();
                buildChart();
            });

            return {
                stockChartCanvas,
                stockChart,
                stockData,
                buildChart,
            }
        },

        watch: {
            stockData: {
                handler () {
                    // TODO -> Fix bug
                    // I can't get stockChart.update() to work here, getting some errors, so I destoy and rebuild for the time being
                    if (this.stockChart){
                    this.stockChart.destroy();
                    }
                    this.buildChart()
                }
            }
        },
    }
</script>