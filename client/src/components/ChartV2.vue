<template>
  <div class="lineChart">
    <div id="chartContainer" style="position: relative; height:40vh; width:80vw">
      <canvas ref="stockChartCanvas"></canvas>
      <button @click="showStats">Show Stats</button>
    </div>
  </div>
</template>

<script>
import { ref, onMounted } from 'vue';
import Chart from 'chart.js/auto';
import axios from 'axios';

export default {
  name: 'Chart',
  props: ['currentlyTracked', 'startDate', 'endDate'],
  setup(props) {
    const stockChartCanvas = ref(null);
    const stockChart = ref(null);
    const stockData = ref(null);
    console.log(" Kid: Start Date: "+props.startDate + ", End Date: "+props.endDate)
    
    // Use toRef to create reactive references to props
    const showAAPL = props.currentlyTracked['AAPL'][0];
    const showMSFT = props.currentlyTracked['MSFT'][0];
    const showTSLA = props.currentlyTracked['TSLA'][0];
    const dateRangeStart = props.startDate;
    const dateRangeEnd = props.endDate;

    const displayOptions = {
      showAAPL,
      showMSFT,
      showTSLA,
      dateRangeStart,
      dateRangeEnd,
  };

    const buildChart = () => {
      stockChart.value = new Chart(stockChartCanvas.value, {
        type: 'line',
        data: stockData.value,
        options: {
          responsive: true,
          plugins: {
            legend: {
              display: false
            }
          },
        },
      });
    };

    const getLatestStockInfos = async () => {
      const path = '/stonksV2';
      try {
        const response = await axios.get(path);
        stockData.value = response.data;
      } catch (error) {
        console.error(error);
      }
    };

    const showStats = () => {
      console.log(displayOptions.showTSLA)
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
      displayOptions,
      buildChart,
      showStats
    };
  },

  watch: {
    displayOptions: {
      handler() {
        console.log("DisplayOptions watched")
        if (this.displayOptions.showAAPL) {
          this.stockChart.show(this.currentlyTracked['AAPL'][1]);
        } else {
          this.stockChart.hide(this.currentlyTracked['AAPL'][1]);
        }
        if (this.displayOptions.showMSFT) {
          this.stockChart.show(this.currentlyTracked['MSFT'][1]);
        } else {
          this.stockChart.hide(this.currentlyTracked['MSFT'][1]);
        }
        if (this.displayOptions.showTSLA) {
          this.stockChart.show(this.currentlyTracked['TSLA'][1]);
        } else {
          this.stockChart.hide(this.currentlyTracked['TSLA'][1]);
        }
      },
      deep: true,
    },
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
};
</script>