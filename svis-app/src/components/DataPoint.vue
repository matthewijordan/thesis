<template>
	<!-- <box :position="[dataPoint.x,dataPoint.value,dataPoint.y]" v-model="dataPointBab"></box> -->
    <box v-model="dataPointBab"></box>
</template>

<script>
    export default {
        name: 'DataPoint',
        
        props: [
            'dataPoint',
        ],

        data: function(){
            return {
                dataPointBab: null      
            }
        },

        watch: {
           dataPointBab: function () {
               let dp = this.dataPoint
               this.dataPointBab.position.x=dp.x;
               this.dataPointBab.position.y=dp.value;
               this.dataPointBab.position.z=dp.y;

               // register the ID/duocode so we can identify the mesh
               this.dataPointBab.appdata = { id: dp.duocode }
           }
        }

    }
</script>