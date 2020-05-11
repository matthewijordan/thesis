<template>
	<box v-model="dataPointBab"></box>
</template>

<script>
    export default {
        name: 'DataPoint',
        
        props: [
            'dataPoint'
        ],

        data: function(){
            return {
                dataPointBab: null      
            }
        },

        watch: {
            dataPointBab: function () {
                console.log(this.dataPointBab)
                this.dataPointBab.position = [this.dataPoint.x,this.dataPoint.value,this.dataPoint.y]
            }
        }

    }
</script>