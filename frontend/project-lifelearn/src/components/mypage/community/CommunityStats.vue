<template>
  <div class="community-stats">
    <div class="stat-card">
      <div class="value">{{ stats.post_count }}</div>
      <div class="label">작성한 글</div>
    </div>
    <div class="stat-card">
      <div class="value">{{ stats.comment_count }}</div>
      <div class="label">작성한 댓글</div>
    </div>
    <div class="stat-card">
      <div class="value">{{ stats.scrap_count }}</div>
      <div class="label">스크랩</div>
    </div>
    <div class="stat-card">
      <div class="value">{{ stats.received_likes_count }}</div>
      <div class="label">받은 좋아요</div>
    </div>
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue';
import { getCommunityStats } from '@/api/mypage';

const stats = ref({
  post_count: 0,
  comment_count: 0,
  scrap_count: 0,
  received_likes_count: 0,
});

onMounted(async () => {
  try {
    const response = await getCommunityStats();
    stats.value = response.data;
  } catch (error) {
    console.error('커뮤니티 활동 통계를 가져오는데 실패했습니다:', error);
  }
});
</script>

<style scoped>
.community-stats {
  display: grid;
  grid-template-columns: repeat(4, 1fr);
  gap: 20px;
  background-color: var(--bg-light);
  padding: 30px;
  border-radius: 12px;
  margin-bottom: 40px;
}
.stat-card {
  text-align: center;
}
.stat-card .value {
  font-size: 32px;
  font-weight: 700;
  color: var(--primary);
}
.stat-card .label {
  font-size: 15px;
  color: var(--text-sub);
  margin-top: 5px;
}
</style>
