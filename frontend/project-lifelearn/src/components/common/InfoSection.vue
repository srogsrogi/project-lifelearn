<template>
  <section class="info-section">
    <div class="section-header">
      <span v-if="icon" class="section-icon">{{ icon }}</span>
      <h2 class="section-title">{{ title }}</h2>
    </div>
    <div class="section-content">
      <slot></slot>
    </div>
  </section>
</template>

<script setup>
defineProps({
  title: {
    type: String,
    required: true
  },
  icon: {
    type: String,
    default: ''
  }
});
</script>

<style scoped>
.info-section {
  background: #f9fafb;
  border: 1px solid #e5e7eb;
  border-radius: 12px;
  padding: 28px 32px;
  margin-bottom: 32px;
  transition: box-shadow 0.2s ease;
}

.info-section:hover {
  box-shadow: 0 4px 12px rgba(0, 0, 0, 0.04);
}

.section-header {
  display: flex;
  align-items: center;
  gap: 10px;
  margin-bottom: 20px;
  padding-bottom: 16px;
  border-bottom: 2px solid #e5e7eb;
}

.section-icon {
  font-size: 1.5rem;
  line-height: 1;
}

.section-title {
  margin: 0;
  font-size: 1.35rem;
  font-weight: 700;
  color: #111827;
  letter-spacing: -0.02em;
}

.section-content {
  color: #374151;
  line-height: 1.7;
}
</style>
