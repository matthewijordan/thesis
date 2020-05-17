<template>
	<!-- <box :position="[dataPoint.x,dataPoint.value,dataPoint.y]" v-model="dataPointBab"></box> -->
    <entity v-model="dataPointBab">
    <box :position="[dataPoint.x,dataPoint.value,dataPoint.y]">
        <Material v-if="isPicked" diffuse="#F00"></Material>
    </box>
    <ExtrudePolygon :options="expop" :shape="[0,0,0]"></ExtrudePolygon>
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
                dataPointBab: null ,
                expop: {
                    shape: [
                        [0,0,0],[0,0,1],[1,0,0],[0,0,0]
                    ],
                    path: [
                        [0,1,0]
                    ]
                }
            }
        },

        watch: {
           dataPointBab: function () {
               let dp = this.dataPoint
               this.dataPointBab.position.x = dp.x;
               this.dataPointBab.position.y = dp.value*0.5;
               this.dataPointBab.position.z = dp.y;

               // register the ID/duocode so we can identify the mesh
               this.dataPointBab.appdata = { id: dp.duocode }
           }
        }

    }
</script>