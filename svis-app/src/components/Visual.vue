<template>
	<div id="vis-container">
        <Scene>
                <!-- <box v-for="dp in dataPoints()" :position="[dp.x,dp.value,dp.y]" :key="`${dp.x},${dp.value},${dp.y}`"></box> -->
                <DataPoint v-for="dp in dataPoints()" :dataPoint="dp" :key="`${dp.x},${dp.value},${dp.y}`"/>
        </Scene>
	</div>
</template>

<script>

    import duocodes from '../data/duocodes.json'
    import DataPoint from './DataPoint.vue'

    export default {
        name: 'Visual',

        props: [
            'filteredData'
        ],

        data: function(){
            return {
                duocodes: duocodes,
                // babylon objects { 'duocode' : obj }
                dataPoints3d: null
            }
        },

        components: {
			DataPoint
		},

        methods: {

            // get data ready for rendering
            dataPoints: function() {
                var dp = []
                for (var k in duocodes) {
                    var dc = duocodes[k]
                    var thisdp = {}
                    thisdp.x = dc["long"]
                    thisdp.y = dc["lat"]
                    thisdp.duocode = k
                    thisdp.value = 0
                    if (k in this.filteredData) {
                        thisdp.value = this.filteredData[k]
                    }
                    dp.push(thisdp)
                }
                return dp
            }
        }
    }

</script>

<style>

#vis-container {
    height: 100%;
    width: 100%;
}

</style>
