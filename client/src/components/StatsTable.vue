<template>
    <div class="statsTable">
        <h1 style="padding-bottom: 2%;">Statistics</h1>
        <table>
            <tr>
                <th></th>
                <th class="tableHeader">Apple (AAPL)</th>
                <th class="tableHeader">Microsoft (MSFT)</th>
                <th class="tableHeader">Tesla (TSLA)</th>
            </tr>
            <tr>
                <td class="tableHeader">Cumulative Return</td>
                <td v-if="statistics">{{statistics['AAPL'][0]}}</td>
                <td v-if="statistics">{{statistics['MSFT'][0]}}</td>
                <td v-if="statistics">{{statistics['TSLA'][0]}}</td>
            </tr>
            <tr>
                <td class="tableHeader">Annualized Return</td>
                <td v-if="statistics">{{statistics['AAPL'][1]}}</td>
                <td v-if="statistics">{{statistics['MSFT'][1]}}</td>
                <td v-if="statistics">{{statistics['TSLA'][1]}}</td>
            </tr>
            <tr>
                <td class="tableHeader">Annualized Volatility</td>
                <td v-if="statistics">{{statistics['AAPL'][2]}}</td>
                <td v-if="statistics">{{statistics['MSFT'][2]}}</td>
                <td v-if="statistics">{{statistics['TSLA'][2]}}</td>
            </tr>
        </table>
    </div>
</template>

<script>
import { ref, onMounted} from 'vue';
import axios from 'axios';

export default {
    setup() {
        const statistics = ref(null);

        const getLatestStatistics = async () => {
            const path = '/stats';
            try {
                const response = await axios.get(path);
                statistics.value = response.data;
            } catch (error) {
                console.error(error);
            };
        };

        onMounted(() => {
            getLatestStatistics();
        });

        return {
            statistics,
            getLatestStatistics
        }
    }
}
</script>