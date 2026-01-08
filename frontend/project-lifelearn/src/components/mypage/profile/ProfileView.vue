<template>
  <div class="profile-view">
    <div v-if="profile" class="profile-details">
      <div class="detail-item">
        <label>사용자명</label>
        <p>{{ profile.username }}</p>
      </div>
      <div class="detail-item">
        <label>이름</label>
        <p>{{ profile.name }}</p>
      </div>
      <div class="detail-item">
        <label>이메일</label>
        <p>{{ profile.email }}</p>
      </div>
      <div class="detail-item">
        <label>가입일</label>
        <p>{{ formatDate(profile.date_joined) }}</p>
      </div>
      <div class="detail-item">
        <label>마케팅 정보 수신</label>
        <p class="text-sub">
          {{ profile.marketing_opt_in ? '동의' : '미동의' }}
        </p>
      </div>
    </div>
    <div class="actions">
      <button class="btn btn-primary" @click="$emit('edit')">정보 수정</button>
    </div>
  </div>
</template>

<script setup>
defineProps({
  profile: {
    type: Object,
    required: true,
  },
});
defineEmits(['edit']);

const formatDate = (dateString) => {
  if (!dateString) return '';
  const date = new Date(dateString);
  return date.toLocaleDateString('ko-KR', { 
    year: 'numeric', 
    month: 'long', 
    day: 'numeric' 
  });
};
</script>

<style scoped>
.profile-details {
  border-top: 2px solid #333;
}
.detail-item {
  display: flex;
  padding: 20px 10px;
  border-bottom: 1px solid var(--border);
  align-items: center;
}
.detail-item label {
  width: 140px;
  font-weight: 600;
  color: var(--text-main);
}
.detail-item p {
  margin: 0;
  color: var(--text-sub);
}
.text-sub {
  color: var(--text-sub) !important;
  font-weight: 400 !important;
}
.actions {
  margin-top: 30px;
  text-align: right;
}
</style>
