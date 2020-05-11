<template>
	<div id="app" class="mh-100">

		<nav class="navbar navbar-dark bg-dark" id="appNav">
			<div>
				<a class="navbar-brand">SVIS</a>
				<span class="navbar-text">3D visualisation for australian PV data </span>
			</div>
		</nav>

		<div class="overlayUi"><div id="filterboxCont"><div class="card text-white bg-dark p-3">
			<h3>Data Controls</h3>
			<hr/>
			<div class="form-group">
				<label >Model Type:</label>
				<select class="form-control">
					<option selected>Past data</option>
					<option>Predictive</option>
				</select>
			</div>
			<div class="form-group">
				<label>Time of day:</label>
				<span class="float-right">{{this.filters.timeText}}</span>
				<input type="range" class="custom-range" min="0" max="96" v-model="filters.time" @input="filter()">
			</div>
			<div class="form-group">
				<label>Date:</label>
				<input type="date" class="form-control" v-model="filters.date" @change="filter()"/>
			</div>
			<div class="form-group">
				<label>Weather:</label>
				<select class="form-control">
				</select>
			</div>
		</div></div></div>

		<div v-if="filters.selectedDuocode!=''" id="overlayUi"><div id="infoboxCont"><div class="card text-white bg-dark p-3">
			<h3>Data Point Info</h3>
		</div></div></div>

		<div class="fillHeight">
			<Visual :filteredData="filteredData" />
		</div>

	</div>
</template>

<script>

	import duocodes from './data/duocodes.json'
	import Visual from './components/Visual.vue'
	var moment = require('moment');
	

	export default {
		name: 'App',
		components: {
			Visual
		},
		data: function () {
			return {
				appData : {},
				weatherData: {},
				duocodes: duocodes,
				filters : {
					date: '2020-03-07',
					time: '56',
					timeText: '...',
					selectedDuocode: '',
					hoveredDuocode: ''
				},
				filteredData : []
			}
		},
		methods: {

			fetchDataByDay: async function (day) {
				//console.log(this.appData)
				if(!(day in this.appData)) {
					return fetch("http://"+window.location.hostname+":8800/data/" + day)
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

			fetchWeatherData: async function () {
				fetch("http://"+window.location.hostname+":8800/weather_data")
				.then( response => {
					return response.json()
				}).then( jdata => {
					//console.log(jdata)
					this.weather_data = jdata
					return jdata
				});
				return null
			},

			// apply filters
			filter: function () {
				this.fetchDataByDay(this.filters.date).then( () => {
					// new moment from date
					var datetime = moment(this.filters.date).utcOffset('+1000')//.tz('Australia/NSW')
					console.log(datetime.format());
					// add minutes to datetime
					datetime = datetime.add(this.filters.time * 15, 'minutes');
					// minutes to display
					this.filters.timeText = datetime.format('h:mm a');

					var pcd = this.appData[this.filters.date]["postcode"]
					for (var i in pcd) {
						// find the actual timestamped collection
						if ( (datetime.utc().format()) == pcd[i]["ts"]) {
							this.filteredData = pcd[i];
							break;
						}
					}
				})
			},

			// call this from data points
			setSelectedDuocode: async function (duocode) {
				this.filters.selectedDuocode = duocode;
			},

			setHoverDuocode: async function (duocode) {
				this.filters.hoveredDuocode = duocode;
			}

		},
		beforeMount: async function () {
			await this.fetchWeatherData()
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

.overlayUi{
	position: relative; width: 0; height: 0;
}

#infoboxCont{
	position: absolute; left: 20px; bottom: 20px; width:25em;
}

#filterboxCont{
	position: absolute; left: 20px; top: 20px; width:25em;
}

</style> 
