<template>
	<div id="vis-container">
        <Scene @scene="onScene" :environment="{createSkybox:false}">
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
            'filteredData',
        ],

        data: function(){
            return {
                duocodes: duocodes,
                // babylon objects { 'duocode' : obj }
                scene: null
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
            },

            selectDataPoint: function() {
                //var result = this.scene.pick(this.scene.pointerX, this.scene.pointerY)
                //console.log(result)
                console.log('test')
            },

            onScene: function(scene) {
                // store for later...
                this.scene = scene
                var self = this
                scene.onPointerDown = function (evt, res) {
                    console.log(res)
                    if(res.pickedMesh != null && 'appdata' in res.pickedMesh) {
                        console.log(self)
                        self.$emit('setSelectedDuocode', res.pickedMesh.appdata.id)
                    }
                }

            },

            getEnvironment: function() {
                return 0
            }

        },
    }

</script>

<style>

#vis-container {
    height: 100%;
    width: 100%;
}

</style>
