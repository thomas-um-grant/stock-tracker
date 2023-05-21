<template>
    <div class="main">
        <h1>Currently tracking</h1>
        <div class="buttons-container" :currentlyTracked="currentlyTracked">
            <button class="image-button" id="AAPL" @click="updateTracking('AAPL')">
                <img src="../assets/apple-logo.png" alt="Apple Logo">
            </button>
            <button class="image-button" id="MSFT" @click="updateTracking('MSFT')">
                <img src="../assets/microsoft-logo.png" alt="Microsoft Logo">
            </button>
            <button class="image-button" id="TSLA" @click="updateTracking('TSLA')">
                <img src="../assets/tesla-logo.png" alt="Tesla Logo" >
            </button>
        </div>

        <h2>Performances from <input type="date" id="startDate" value={{startDate}} @change="trackDate('startDate')"> to <input type="date" id="endDate" value={{endDate}} @change="trackDate('endDate')"></h2>
        <ChartV2 :currentlyTracked="currentlyTracked" :startDate="startDate" :endDate="endDate"/>

        <h3>How is the performance of these stocks calculated?</h3>
        <p></p>

        <h2>More statistics to look at...</h2>
        <StatsTable />

        <h3>How are these statistics calculated?</h3>
        <p></p>
    </div>
</template>

<script>
import { ref, onMounted } from 'vue';
import ChartV2 from '../components/ChartV2.vue'
import StatsTable from '../components/StatsTable.vue'

export default {
    name: "StockTrackerV2",
    components: { ChartV2, StatsTable },
    setup(){
        const currentlyTracked = ref({'AAPL':[true,1], 'MSFT':[true,2], 'TSLA':[true,3]});
        const startDate = ref((new Date(Date.now() - 30 * 24 * 60 * 60 * 1000)).toISOString().split("T")[0]);
        const endDate = ref((new Date()).toISOString().split("T")[0]);

        const updateTracking = (id) => {
            console.log("test tracking")
            currentlyTracked.value[id][0] = !currentlyTracked.value[id][0];
            console.log(currentlyTracked.value)
        };
        const trackDate = (id) => {
            let datepicker = document.getElementById(id);
            if(id == "startDate"){
                startDate.value = datepicker.value;
            }
            else{
                endDate.value = datepicker.value;
            }
        };

        onMounted(() => {
            document.getElementById("startDate").value = startDate.value;
            document.getElementById("endDate").value = endDate.value;
            console.log(" Parent: Start Date: "+startDate.value + ", End Date: "+endDate.value)
        });

        return {
            currentlyTracked,
            startDate,
            endDate,
            updateTracking,
            trackDate
        }
    },
}
</script>

<style>
    .image-button{
        display: inline-flex;
        align-items: center;
        justify-content: center;
        padding: 10px 20px;
        border: none;
        border-radius: 5px;
        cursor: pointer;
      }
    .image-button img{
    height: 20px;
    width: 20px;
    }
    .buttons-container{
        display: flex;
        column-gap: 20px;
        align-items: flex-start;
        justify-content: left;
    }
    .image-button:hover{
        color: beige;
    }
</style>