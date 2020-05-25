<template>
	<!-- <box :position="[dataPoint.x,dataPoint.value,dataPoint.y]" v-model="dataPointBab"></box> -->
    <entity v-model="dataPointBab" @complete="onComplete">
        <!--<box :position="[dataPoint.x,dataPoint.value*0.5,dataPoint.y]" :name="'boxPoint'">
            <Material v-if="isPicked" diffuse="#F00"></Material>
        </box>-->

        <ExtrudePolygon 
            v-for="p in dataPointGeom"
            :key="`${p.id}`"
            
            :options="{
                shape: p.shape,
                holes: p.holes,
                sideOrientation: 2,
                depth: 1
            }"

            :scaling="[1,(-dataPoint.value*0.5) || (-0.01),1]"
        >
            <Material v-if="isPicked" diffuse="#F00" :alpha=1></Material>
            <Material v-if="!isPicked && pickMode" diffuse="#FFF" :alpha=0.2></Material>
        </ExtrudePolygon>
        
    </entity>
    
</template>

<script>
    export default {
        name: 'DataPoint',
        
        props: [
            'dataPoint',
            'isPicked',
            'pickMode'
        ],

        data: function(){
            return {
                dataPointBab: null,
                dataPointGeom: this.transformShapedata(this.dataPoint.shapedata)
            }
        },

        methods: {

            // Once all sub entities/meshes are ready
            onComplete: function() {
                // go through any attached children
                let dp = this.dataPoint
                this.dataPointBab.getChildren().forEach( (m) => {
                    m.appdata = { id: dp.duocode }
                    //console.log(m)
                    if(m.name=='boxPoint'){
                        //console.log(m)
                    }
                } )
            },

            // shapedata to vector 3
            transformShapedata: function(shapedata) {
                var geometry = []
                
                var polyID = 0
                if (shapedata.type == "single") {
                    let shape = shapedata.coordinates[0].map( (p) => {
                        return {x:p[0],y:0,z:p[1]}
                    } )
                    geometry[0] = { shape: shape, id: polyID, holes: null }
                } else {
                    shapedata.coordinates.forEach( (sd) => {
                        let shape = sd[0].map( (p) => {
                            return {x:p[0],y:0,z:p[1]}
                        } )
                        geometry.push( { shape: shape, id: polyID, holes: null } )
                        polyID+=1;
                    } )
                }

                return geometry
            }
        },

        watch: {
            //I guess this is useless now
            dataPointBab: function () {
               
            }
        }

    }
</script>