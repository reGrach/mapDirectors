<template>
<div>
<v-layout>
  <label>Диапазон годов рождения</label>
  <div class="input">
    <input type="number" class="primary" v-model="yearFrom" min="1900" max="1999"/>
  </div>
  <div class="input">
    <input type="number" v-model="yearTo" min="1900" max="1999"/>
  </div>
  <div class="input"><button class="btn btn-outline-primary"
          @click="onFindClick"
          target="_blank">Найти</button></div>
  </v-layout>

  <!-- <div>
    <label>
      <gmap-autocomplete
        @place_changed="setPlace">
      </gmap-autocomplete>
      <button @click="addMarker">Add</button>
    </label>
    <br/>

  </div> -->
  <br> 
  <gmap-map
    id="googleMap"
    :center="center"
    :zoom="2"
    style="width:100%;  height: 400px;">
    <gmap-marker
      :key="index"
      v-for="(m, index) in markers"
      :position="m.position"
      @click="showDetail(m)">
        <gmap-info-window v-if="m.isVisible">
          <b>Person name: </b>{{m.title}}
          <br>
          <b>Birth place: </b>{{m.place}} 
        </gmap-info-window>
      </gmap-marker>
  </gmap-map>
</div>
</template>

<script>

  import VLayout from '@/layouts/Default';
  import * as VueGoogleMaps from "vue2-google-maps";
  import axios from 'axios';

  export default {
    name: 'home-index',
    components: {
      VLayout
    },
    data() {
      return {
        yearFrom:1900,
        yearTo: 1999,
        center: { lat: 45.508, lng: -73.587 },
        markers: [],
        places: []
      }
    },
    methods: {
      onFindClick() {
        axios.get('/peopleInfo', {
            params: {
              yearFrom: this.yearFrom,
              yearTo: this.yearTo
            }
          })
          .then((response) => {
            Object.keys(response.data).forEach(name => {
              this.addMarker(response.data[name][0],{
                lat: parseFloat(response.data[name][2]),
                lng: parseFloat(response.data[name][3]),
              }, name)
            })
          })
          .catch((error) => {
            console.log(error);
          });
    
      },
      addMarker(place, marker, personName) {
        this.markers.push({ position: marker, title: personName, place, isVisible: false });
        this.places.push(place);
      },
      showDetail(selected) {
        debugger
        this.markers = this.markers.map(marker => {
          if(marker.title === selected.title) {
            return {
              ...selected,
              isVisible: true
            }
          }
          return marker;
        })
      }
    }
  };
</script>
<style scoped>
  .input {
    margin-left: 12px;
  }

  
</style>
