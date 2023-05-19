<template>
    <div class="chart-container" style="position: relative; height:40vh; width:80vw">
        <Line v-if="data.datasets" :data="data" :options="options" />
    </div>
</template>
  
<script>
    import {
        Chart as ChartJS,
        Title,
        Tooltip,
        Legend,
        LineController,
        LineElement,
        PointElement,
        CategoryScale,
        LinearScale
    } from 'chart.js';
    import { Line } from 'vue-chartjs';
    import axios from 'axios';

    ChartJS.register(CategoryScale, LinearScale, LineController, LineElement, PointElement, Title, Tooltip, Legend);

    export default {
        name: 'App',
        components : {
            Line
        },
        data() {
            return {
                data: {
                    labels: null,
                    datasets: null
                }, 
                //{
                        // labels: [1, 2, 3, 4, 5, 6, 7],
                        // datasets: [{
                        //     label: 'My First Dataset',
                        //     data: [65, 59, 80, 81, 56, 55, 40],
                        //     fill: false,
                        //     borderColor: 'rgb(75, 192, 192)',
                        //     tension: 0.1
                        // }]
                    //},
                options: {
                    responsive: true
                }
            }
        },
        
        methods: {
            updateStocksInfo(data){
                const path = 'http://127.0.0.1:5001/stocks';
                axios.get(path).then((response) => {

                    data.labels = response.data['labels'];

                    let newDatasets = [];
                    for (let datatset in response.data['datasets']){
                        let newSet = {
                            label: datatset['label'],
                            data: datatset['data'],
                            fill: false,
                            borderColor: datatset['borderColor'],
                            tension: 0.1
                        }
                        newDatasets.push(newSet);
                    }
                    data.datasets = newDatasets
                })
                .catch((error) => {
                    console.error(error);
                });
            },
        },

        // Lifecycle hook
        /*
        Creation hooks are the first hooks that run in your component. 
        They allow you to perform actions before your component has even been added to the DOM. 
        Unlike any of the other hooks, creation hooks are also run during server-side rendering.
        */
        beforeCreate() {
            console.log('At this point, events and lifecycle have been initialized.')
        },
        created(){
            console.log('At this point, this.property is now reactive and propertyComputed will update.')
            this.updateStocksInfo(this.data)
        },
        /*
        Mounting hooks are often the most used hooks. 
        They allow you to access your component immediately before and after the first render. 
        They do not, however, run during server-side rendering.
        */
        beforeMount() {
            console.log(`At this point, vm.$el has not been created yet.`)
        },
        mounted() {
            console.log(`At this point, vm.$el has been created and el has been replaced.`);
        },
        /*
        Updating hooks are called whenever a reactive property used by your component changes or something else causes it to re-render. 
        They allow you to hook into the watch-compute-render cycle for your component.
        /!\ Do not use updating hooks if you need to know when a reactive property on your component changes. Use computed properties or watchers for that instead.
        */
        beforeUpdate() {
            console.log(`At this point, Virtual DOM has not re-rendered or patched yet.`)
        },
        updated() {
            console.log(`At this point, Virtual DOM has re-rendered and patched.`)
        },
        /*
        Destruction hooks allow you to perform actions when your component is destroyed, such as cleanup or analytics sending. 
        They fire when your component is being torn down and removed from the DOM.
        */
        beforeUnmount() {
            console.log(`At this point, watchers, child components, and event listeners have not been unmounted yet.`)
        },
        unmounted() {
            console.log(`At this point, watchers, child components, and event listeners have been unmounted.`)
            console.log(this)
        },
    }
</script>