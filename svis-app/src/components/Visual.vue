<template>
	<div id="vis-container">
        <Scene @scene="onScene" :environment="{createSkybox:false, createGround:false}">
                <Camera v-model="camera"
                    :type="'arcRotate'"
                    :target="$vector(camTarget.x,camTarget.y,camTarget.z)"
                    :radius="100"
                ></Camera>

                <!--<SpotLight :direction="[0,-1,0]" :position="[0,200,0]" specular="#000000"></SpotLight>

                <SpotLight :direction="[0,-1,0]" :position="[100,200,100]" specular="#000000"></SpotLight>
                <SpotLight :direction="[0,-1,0]" :position="[-100,200,-100]" specular="#000000"></SpotLight>
                <SpotLight :direction="[0,-1,0]" :position="[100,200,-100]" specular="#000000"></SpotLight>
                <SpotLight :direction="[0,-1,0]" :position="[-100,200,100]" specular="#000000"></SpotLight>

                <SpotLight :direction="[0,-1,0]" :position="[100,200,100]" specular="#000000"></SpotLight>
                <SpotLight :direction="[0,-1,0]" :position="[-100,200,-100]" specular="#000000"></SpotLight>
                <SpotLight :direction="[0,-1,0]" :position="[100,200,-100]" specular="#000000"></SpotLight>
                <SpotLight :direction="[0,-1,0]" :position="[-100,200,100]" specular="#000000"></SpotLight>-->
                <HemisphericLight diffuse="#888" :direction="[0,1,1]" :position="[origin.x,300,origin.y]"></HemisphericLight>
                <DirectionalLight specular="#FFF" diffuse="#FFF" :direction="[0,-1,0]"></DirectionalLight>
                <DirectionalLight  diffuse="#ffcc99" :direction="[0,-1,1]"></DirectionalLight>

                <PointLight specular="#ff0000"
                    :position="[origin.x,100,origin.y]"
                />

                <Disc :scaling="[100,100,1]" :rotation="[3.14159/2,0,0]" :position="[origin.x,-0.1,origin.z]">
                    <Material diffuse="#00F" :alpha="0.1" :roughness="1"></Material>
                </Disc>
                
                <entity>
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

    //import babhelp from 'vue-babylonjs' 

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
                camera: null,
                pointerTrack: null,
                camTarget: { x:132, y:0, z:-16 },
                origin: {x:132, y:0, z:-24}
            }
        },

        components: {
			DataPoint
		},

        methods: {

            // get data ready for rendering
            dataPoints: function() {
                var dp = []
                var count = 0
                var cols = ["#FFD0C5","#FEBAC5","#FEBAE7","#F3BAFE","#C5C9FF","#BAFEC8","#FEFEBA","#D1BAFE","#BAFEBA","#FEBABA","#FEBABF","#BAFEDC","#D1BAFE","#FEDCBA","#F3BAFE","#C5FFED","#F4FFC5","#C5E6FF","#C5FFD0","#BAFEDC","#C5FFFB","#FFD0C5","#BAFEC8","#FFEDC5","#F4FFC5","#FBC5FF","#FEBAE7","#BAFED7","#C5E6FF","#C5C9FF","#C5FFD0","#FEBABF","#FEBAC5","#C5FFFB","#D7FFC5","#DEC5FF","#FEBABA","#FEFEBA","#D7FFC5","#FEDCBA","#DEC5FF","#DCFEBA","#FFEDC5","#C5FFDE","#BAFEBA","#FBC5FF","#DCFEBA","#C5FFDE","#BAFED7","#C5FFED"]
                for (var k in duocodes) {
                    var dc = duocodes[k]
                    var thisdp = {}
                    thisdp.x = dc["long"]
                    thisdp.y = dc["lat"]
                    thisdp.duocode = k
                    thisdp.value = 0
                    thisdp.shapedata = dc["shapedata"]
                    thisdp.colour=cols[count++]
                    if (k in this.filteredData) {
                        thisdp.value = this.filteredData[k]
                    }
                    dp.push(thisdp)
                }
                return dp
            },

            onScene: function(scene) {
                this.scene = scene
                var self = this

                scene.onPointerObservable.add((pointerInfo) => {
                    var pm = pointerInfo.pickInfo.pickedMesh;
                    switch (pointerInfo.type) {
                        case 1: // pointer down
                            if (pm != null && 'appdata' in pm){
                                self.pointerTrack = pm.appdata.id
                            } else {
                                self.pointerTrack = ''
                            }
                            break;
                        case 2: //pointer up
                            if (pm != null && 'appdata' in pm && self.pointerTrack == pm.appdata.id){
                                self.$emit('setSelectedDuocode', pm.appdata.id)
                                //self.camera.setTarget( babhelp.$vector(100,100,100) )
                                self.camTarget.x = duocodes[pm.appdata.id].long
                                self.camTarget.y = 0
                                self.camTarget.z = duocodes[pm.appdata.id].lat
                            } else if (self.pointerTrack == '') {
                                self.$emit('setSelectedDuocode', "")
                            }
                            break;
                        case 4: //pointer move
                            self.pointerTrack = null
                            break;
                    }

                });

            },

            getEnvironment: function() {
                return 0
            }

        },

        watch: {
            camera: function() {
                this.camera.alpha = -1.561667910668399
                this.camera.beta = 0.7990808589426004
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
