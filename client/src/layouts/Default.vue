<template>
  <div>
    <nav class="navbar navbar-expand-lg navbar-dark bg-dark">
      <router-link
        class="navbar-brand"
        :to="{ name: 'home.index' }">
        <h2>Карта личностей</h2>
      </router-link>

    </nav>

    <div class="container pt-4">
      <div class="row">
        <div class="col col-12 parent-container">
          <!-- Content will be placed here -->
          <slot></slot>
        </div>
      </div>
    </div>

  </div>
</template>

<script>
  export default {
    name: 'default-layout',
  };
</script>

<style scoped>
  .parent-container {
    display: flex;
    align-items: center;
    justify-content: center;
  }

  
</style>
