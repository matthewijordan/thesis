<template>
	<div id="app" class="mh-100">

		<nav class="navbar navbar-dark bg-dark" id="appNav">
			<div>
				<a class="navbar-brand">SVIS</a>
				<span class="navbar-text">3D visualisation for australian PV data </span>
			</div>
		</nav>

		<div id="filterboxPos"><div id="filterboxCont">
			<div class="card text-white bg-dark p-3">
				<h3>Data Controls</h3>
				<hr/>
				<div class="form-group">
					<label for="customRange1">Time of day:</label>
					<span class="float-right">{{filters.timeText}}</span>
					<input type="range" class="custom-range" min="0" max="96" v-model="filters.time" @change="filter()">
				</div>
				<div class="form-group">
					<label >Date:</label>
					<input type="date" class="form-control" v-model="filters.date" @change="filter()"/>
				</div>
			</div>
		</div></div>

		<div class="fillHeight">
			<Visual :filteredData="filteredData" />
		</div>

	</div>
</template>

<script>

	import duocodes from './data/duocodes.json'
	import Visual from './components/Visual.vue'

	export default {
		name: 'App',
		components: {
			Visual
		},
		data: function () {
			return {
				appData : {},
				duocodes: duocodes,
				filters : {
					date: '2020-03-07',
					time: '56',
					timeText: 'aaa'
				},
				filteredData : []
			}
		},
		methods: {

			fetchDataByDay: async function (day) {
				//console.log(this.appData)
				if(!(day in this.appData)) {
					return fetch("http://127.0.0.1:8800/data/" + day)
					.then( response => {
						return response.json()
					}).then( jdata => {
						//console.log(jdata)
						this.appData[day] = jdata[day]
						return jdata
					});
				}
				return null
			},

			// apply filters
			filter: function () {
				this.fetchDataByDay(this.filters.date).then( () => {

					var hours = Math.floor(this.filters.time / 4)
					var minutes = (this.filters.time % 4) * 15
					if (minutes==0) minutes='00'
					if (hours<10) hours="0"+hours.toString()

					var procTime = hours + ":" + minutes + ":00"
					this.filters.timeText=procTime

					console.log(procTime)

					var pcd = this.appData[this.filters.date]["postcode"]
					for (var i in pcd) {
						if ( (this.filters.date + 'T' + procTime + 'Z') == pcd[i]["ts"]) {
							this.filteredData = pcd[i]
							break;
						}
					}
				})
			}
		},
		beforeMount: function () {
			this.filter()
		}
	}

</script>

<style>

#app{
	height: 100%;
}

#appNav{
	height: 4em;
}

.fillHeight{
	height: calc(100vh - 4em);
}

#filterboxPos{
	position: relative; width: 0; height: 0;
}

#filterboxCont{
	position: absolute; left: 20px; top: 20px; width:25em;
}

</style> 
