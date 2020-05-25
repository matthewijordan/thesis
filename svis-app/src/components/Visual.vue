<template>
	<div id="vis-container">
        <Scene @scene="onScene" :environment="{createSkybox:false, createGround:false}">
                <Camera v-model="camera"
                    :type="'arcRotate'"
                    :target="[10,0,]"
                    :position="[10,100,-50]"
                ></Camera>
                <SpotLight :direction="[0,-1,0]" :position="[0,200,0]" specular="#FF0000"></SpotLight>
                <SpotLight :direction="[0,-1,0]" :position="[100,200,100]" specular="#FF0000"></SpotLight>
                <SpotLight :direction="[0,-1,0]" :position="[-100,200,-100]" specular="#FF0000"></SpotLight>
                <SpotLight :direction="[0,-1,0]" :position="[100,200,-100]" specular="#FF0000"></SpotLight>
                <SpotLight :direction="[0,-1,0]" :position="[-100,200,100]" specular="#FF0000"></SpotLight>

                <entity :position="[-120,0,20]">
                    <DataPoint v-for="dp in dataPoints()" :dataPoint="dp" :key="`${dp.duocode}`" 
                        :isPicked="dp.duocode==filters.selectedDuocode"
                        :pickMode="filters.selectedDuocode!=''"
                    />
                </entity>
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
            'filters'
        ],

        data: function(){
            return {
                duocodes: duocodes,
                // babylon objects { 'duocode' : obj }
                scene: null,
                camera: null
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
                    thisdp.shapedata = dc["shapedata"]
                    if (k in this.filteredData) {
                        thisdp.value = this.filteredData[k]
                    }
                    dp.push(thisdp)
                }
                return dp
            },

            onScene: function(scene) {
                // store for later...
                this.scene = scene
                var self = this
                scene.onPointerDown = function (evt, res) {
                    if(res.pickedMesh != null && 'appdata' in res.pickedMesh) {
                        //console.log(self)
                        self.$emit('setSelectedDuocode', res.pickedMesh.appdata.id)
                    } else {
                        self.$emit('setSelectedDuocode', '')
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
