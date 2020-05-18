<template>
	<!-- <box :position="[dataPoint.x,dataPoint.value,dataPoint.y]" v-model="dataPointBab"></box> -->
    <entity v-model="dataPointBab" @complete="onComplete">
        <box :position="[dataPoint.x,dataPoint.value*0.5,dataPoint.y]" :name="'boxPoint'">
            <Material v-if="isPicked" diffuse="#F00"></Material>
        </box>

        <PolygonMesh
            :options="{
                shape: [
                    [100,0,0],
                    [0,0,0],
                    [0,0,100]
                ],
                sideOrientation: 2
            }"
        />
        
    </entity>
    
</template>

<script>
    export default {
        name: 'DataPoint',
        
        props: [
            'dataPoint',
            'isPicked'
        ],

        data: function(){
            return {
                dataPointBab: null 
            }
        },

        methods: {

            // Once all sub entities/meshes are ready
            onComplete: function() {
                // go through any attached children
                let dp = this.dataPoint
                this.dataPointBab.getChildren().forEach( (m) => {
                    m.appdata = { id: dp.duocode }
                    if(m.name=='boxPoint'){
                        console.log(m)
                    }
                } )
            },

            // shapedata to vector 3
            transformShapedata: function() {
                return [

                ]
            }
        },

        watch: {
            //I guess this is useless now
           dataPointBab: function () {
               //let dp = this.dataPoint
               //this.dataPointBab.position.x = dp.x;
               //this.dataPointBab.position.y = dp.value*0.5;
               //this.dataPointBab.position.z = dp.y;

               // register the ID/duocode so we can identify the mesh
               //this.dataPointBab.
               //console.log(this.dataPointBab.getChildren())
               //for (var i in this.dataPointBab.getChildren()) {
               //    console.log(i)
               //}
               //this.dataPointBab.appdata = { id: dp.duocode }
           }
        }

    }
</script>