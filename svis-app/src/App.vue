<template>
	<div id="app" class="mh-100">

		<nav class="navbar navbar-light " id="appNav">
			<div>
				<a class="navbar-brand">SVIS</a>
				<span class="navbar-text">3D visualisation for australian PV data </span>
			</div>
			<div>
				<a @click="infoPaneVisible=true" href="#">
					<i class="fa fa-info-circle fa-2x" aria-hidden="true"></i>
				</a>
			</div>
		</nav>

		<div class="overlayUi"> <div class="filterWaitCont">
			<div class="alert alert-info" role="alert" v-if="filterWait"><div class="spinner-border" role="status"></div></div>
		</div> </div>

		<div class="overlayUi"><div id="filterboxCont"><div class="card border-dark p-3">
			<!-- ----------- DATA CONTROLS--------------------------------------------- -->
			<h3>Data Controls</h3>
			<hr/>
			<div class="form-group">
				<label >Model Type:</label>
				<select class="form-control" v-model="filters.modelType" :disabled="filterWait">
					<option value="past" selected>Past data</option>
					<option value="predict" >Predictive</option>
				</select>
			</div>
			<div class="form-group">
				<label>Time of day:</label>
				<span class="float-right">{{this.filters.timeText}}</span>
				<input type="range" class="custom-range" min="0" max="96" v-model="filters.time" @input="filter()" />
			</div>
			<div class="form-group">
				<label>Date:</label>
				<input type="date" class="form-control" v-model="filters.date" @input="filter()" />
			</div>
			<div class="alert alert-danger" role="alert" v-if="errors.dateSelect && filters.modelType=='past'">No PV data available</div>

			<!-- PREDICTIVE MODEL INPUTS --------------------------------------------- -->
			<div v-if="filters.modelType=='predict'">
				<h4>Predictive inputs</h4>
				<div class="form-group">
					<label>Use BOM weather forecast (if available)?</label> &nbsp; &nbsp;
					<input type="checkbox" v-model="filters.predictUseForecast"/>
				</div>
				<div class="form-group">
					<label>Weather Type:</label>
					<select class="form-control" v-model="filters.predictWeatherType">
						<option value="fog"> fog </option>
						<option value="light_shower"> light shower </option>
						<option value="rain"> rain </option>
						<option value="hazy"> hazy </option>
						<option value="storm"> storm </option>
						<option value="clear"> clear </option>
						<option value="sunny"> sunny </option>
						<option value="shower"> shower </option>
						<option value="cloudy"> cloudy </option>
						<option value="mostly_sunny"> mostly sunny </option>
					</select>
				</div>
				<div class="form-group">
					<label>Temperature min & max (℃):</label>
					<div class="row">
						<div class="col-6"><input type="number" class="form-control" v-model="filters.predictTemperatureMin" /> </div>
						<div class="col-6"><input type="number" class="form-control" v-model="filters.predictTemperatureMax" /> </div>
					</div>
				</div>
				<div class="form-group">
					<label>Rainfall min & max (mm):</label>
					<div class="row">
						<div class="col-6"><input type="number" class="form-control" v-model="filters.predictRainfallMin" /> </div>
						<div class="col-6"><input type="number" class="form-control" v-model="filters.predictRainfallMax" /> </div>
					</div>
				</div>
				<div class="form-group">
					<label>UV Max Index:</label>
					<input type="number" class="form-control" v-model="filters.predictUVMax" />
				</div>

				<button type="button" class="btn btn-primary">Sync predictive model</button>

			</div>

		</div></div></div>

		<!-- INFO ON SELECTED POINT --------------------------------------------- -->
		<div v-if="filters.selectedDuocode!=''" class="overlayUi"><div id="infoboxCont"><div class="card border-dark p-3">
			<h3>Selected Data Point Info</h3>
			<hr/>

			<h5>Base info:</h5>
			<strong>Type: </strong> Duocode (two digit postcode)
			<strong>Name: </strong> {{filters.selectedDuocode}} 
			<strong>Location: </strong> 🌎 (Long: {{duocodes[filters.selectedDuocode]["long"]}},Lat: {{duocodes[filters.selectedDuocode]["lat"]}})
			<hr/>

			<h5>PV info:</h5>
			<strong>Maximum capacity (MW): </strong>
			{{typeof this.appData[this.filters.date] == "undefined" ? "Capacity unnavailable" : this.appData[this.filters.date]["postcodeCapacity"][filters.selectedDuocode]}}
			<strong>Utilization: </strong>
			{{ typeof this.filteredData[filters.selectedDuocode] == 'undefined' ? "∅": this.filteredData[filters.selectedDuocode] }}%
			<div class="progress">
				<div class="progress-bar bg-success" role="progressbar" :style="'width: '+ this.filteredData[filters.selectedDuocode] +'%'" aria-valuenow="25" aria-valuemin="0" aria-valuemax="100"></div>
			</div>
			<hr/>

			<h5>Weather info:</h5>
			<div class="alert alert-danger" role="alert" v-if="weatherPoint(filters.selectedDuocode).icon_descriptor==null">No Weather Data</div>
			<div v-if="weatherPoint(filters.selectedDuocode).icon_descriptor!=null">
				<strong>Short description: </strong> <br/>
				{{weatherPoint(filters.selectedDuocode).icon_descriptor}} 
				<span style="font-size:1rem;">{{ weatherIcon(weatherPoint(filters.selectedDuocode).icon_descriptor) }}</span>
				<br/>
				<strong>Temperature min-max: </strong> <br/>
				{{weatherPoint(filters.selectedDuocode).temp_min || "∅"}}℃ to {{weatherPoint(filters.selectedDuocode).temp_max || "∅"}}℃
				<br/>
				<strong>Rainfall min-max: </strong> <br/>
				{{weatherPoint(filters.selectedDuocode).rain.amount.min || "∅"}}mm to {{weatherPoint(filters.selectedDuocode).rain.amount.max || "∅"}}mm
				<br/>
				<strong>UV Index max: </strong> <br/>
				{{weatherPoint(filters.selectedDuocode).uv.max_index || "∅"}}
			</div>

		</div></div></div>

		<!-- RENDER VISUAL HERE -->
		<div class="fillHeight">
			<Visual :filteredData="filteredData" @setSelectedDuocode="setSelectedDuocode" :filters="filters" />
		</div>

		<!-- INFO/HELP PANE --------------------------------------------- -->
		<div id="InfoPane" class="overlayUi" v-if="infoPaneVisible">
			<div id="infoPaneBackground" @click="infoPaneVisible=false">
			</div>
			<div id="infoPaneCont">
				<div class="card mx-auto mt-5" style="width: 50rem;">
					<div class="card-body">
						<h5 class="card-title">About SVIS-APP</h5>
						<hr/>
						<h6 class="card-subtitle mb-2 text-muted">About</h6>
						<p class="card-text">
							SVIS-APP is a 3d visualisation tool for solar data <br/>
							SVIS is written using vue and babylon JS <br/>
							<strong>For best results use the latest chrome build</strong> <br/>
						</p>
						<hr/>
						<h6 class="card-subtitle mb-2 text-muted">How to use</h6>
						<p class="card-text">
							Hold left mouse - orbit <br/>
							Hold right mouse - pan <br/>
							Scroll wheel - zoom <br/>
						</p>
						<hr/>
						<p class="card-text">
							Published under the GNU General Public License V3, source code available at 
							<a href="https://github.com/matthewijordan/thesis">GitHub.com</a>
						</p>
						<hr/>
						<a href="#" class="card-link" @click="infoPaneVisible=false">Close</a>
					</div>
				</div>
			</div>
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
					date: '2020-05-22',
					time: '56',
					timeText: '...',
					selectedDuocode: '52',
					hoveredDuocode: '',

					modelType: 'past',

					predictUseForecast: false,
					predictWeatherType: "clear",
					predictTemperatureMin: 20,
					predictTemperatureMax: 30,
					predictUVMax: 10,
					predictRainfallMin: 0,
					predictRainfallMax: 0
				},
				errors : {
					dateSelect: false
				},
				filterWait: 0,
				filteredData : [],
				infoPaneVisible: false
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
					this.weatherData = jdata
					return jdata
				});
				return null
			},

			//TODO: sync with UI
			fetchPredictiveData : async function () {
				fetch("http://"+window.location.hostname+":8800/predict")
				.then( response => {
					return response.json()
				}).then( jdata => {
					//console.log(jdata)
					this.predict_data = jdata
					return jdata
				});
				return null
			},

			// apply filters
			filter: function () {
				if (this.filterWait == false && this.filters.modelType=='past') {
					this.filterWait = true
					this.fetchDataByDay(this.filters.date).then( () => {
						if (this.appData[this.filters.date]["postcode"].length == 0){
							this.errors.dateSelect = true
							this.filterWait = false
							return;
						}
						this.errors.dateSelect = false
						// new moment from date
						var datetime = moment(this.filters.date).utcOffset('+1000')//.tz('Australia/NSW')
						//console.log(datetime.format());
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

						this.filterWait = false
					})
				}
			},

			filterPredictive: function() {
				if (this.filterWait == false) {
					this.filterWait = true
				}
				this.filterWait = false
			},

			// call this from data points
			setSelectedDuocode: async function (duocode) {
				this.filters.selectedDuocode = duocode;
			},

			setHoverDuocode: async function (duocode) {
				this.filters.hoveredDuocode = duocode;
			},

			weatherIcon: function (weatherIconName) {
				switch (weatherIconName){
					case "fog":
						return "🌫"
					case "light_shower":
						return "🚿"
					case "rain":
						return "🌧🌧"
					case "hazy":
						return "🌫"
					case "storm":
						return "⛈"
					case "clear":
						return "🌤"
					case "sunny":
						return "☀"
					case "shower":
						return "🚿🚿"
					case "cloudy":
						return "☁"
					case "mostly_sunny":
						return "⛅"
					default:
						return "⁉";
				}
			},

			weatherPoint: function (duocode){
				var thisWeather = {
					icon_descriptor:null,
					rain: {amount:{min:null,max:null}},
					uv: {max_index: null},
					temp_max: null,
					temp_min: null
				}
				if ( typeof this.weatherData[duocode] == 'undefined') {
					return thisWeather
				}
				for (var i = 0; i < this.weatherData[duocode].length; i++){
					if (this.weatherData[duocode][i].date.includes(this.filters.date)){
						thisWeather = this.weatherData[duocode][i]
					}
				}
				return thisWeather
			}

		},
		beforeMount: async function () {
			await this.fetchWeatherData()
			this.filter()
		},
		watch: {
			selectedDuocode: function () {
				console.log("change")
			}
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

.filterWaitCont {
	position: absolute; left: calc(40px + 25em); top: 20px;
}

#infoboxCont{
	position: absolute; left: calc(100vw - 20px - 25em); top: 20px; width:25em;
}

#filterboxCont{
	position: absolute; left: 20px; top: 20px; width:25em;
}

#infoPaneBackground{
	position: absolute; left: 0px; bottom: 0px; width: 100vw; height: 100vh;
	background-color: rgba(20,20,40,.8);
}

#infoPaneCont{
	position: absolute; left: 0px; bottom: 0px; width: 100vw; height: 100vh;
}

</style> 
