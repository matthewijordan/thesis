<template>
	<div id="vis-container">
        <Scene>
                
                <!-- <Box v-for="z in [0, 4, -4]" :position="[x, y, z]" :key="`${x},${y},${z}`" @click="console.log('as')"></Box> -->

                <box v-for="dp in dataPoints()" :position="[dp.x,dp.value,dp.y]" :key="`${dp.x},${dp.value},${dp.y}`"></box>
        </Scene>
	</div>
</template>

<script>

    import duocodes from '../data/duocodes.json'

    export default {
        name: 'Visual',

        props: [
            'filteredData'
        ],

        data: function(){
            return {
                duocodes: duocodes
            }
        },

        methods: {
            dataPoints: function() {
                
                var dp = []

                //console.log(this.filteredDataasas)

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
