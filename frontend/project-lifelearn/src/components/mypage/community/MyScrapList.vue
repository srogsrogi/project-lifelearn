<template>
  <div class="list-container">
    <ul v-if="scraps.length > 0" class="item-list">
      <li v-for="scrap in scraps" :key="scrap.id" class="list-item">
        <div class="post-info">
          <span class="post-board">{{ scrap.post.board_name }}</span>
          <h4 class="post-title">{{ scrap.post.title }}</h4>
        </div>
        <div class="post-meta">
          <span class="meta-item">좋아요 {{ scrap.post.likes_count }}</span>
          <span class="meta-item">댓글 {{ scrap.post.comments_count }}</span>
          <span class="meta-item">{{ scrap.post.created_at }}</span>
        </div>
      </li>
    </ul>
    <div v-else class="no-data">
      <p>스크랩한 게시글이 없습니다.</p>
    </div>
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue';
import { getMyScraps } from '@/api/mypage';

const scraps = ref([]);

onMounted(async () => {
  try {
    const response = await getMyScraps();
    if (response.data.results) {
        scraps.value = response.data.results;
    } else {
        scraps.value = response.data;
    }
  } catch (error) {
    console.error('스크랩 목록을 가져오는데 실패했습니다:', error);
  }
});
</script>

<style scoped>
.item-list {
  list-style: none;
  padding: 0;
  margin: 0;
  border-top: 2px solid #333;
}
.list-item {
  display: flex;
  justify-content: space-between;
  align-items: center;
  padding: 20px 10px;
  border-bottom: 1px solid var(--border);
}
.post-board {
  font-size: 13px;
  font-weight: 600;
  color: var(--primary);
  margin-bottom: 8px;
}
.post-title {
  font-size: 16px;
  font-weight: 500;
  margin: 0;
}
.post-meta {
  font-size: 13px;
  color: var(--text-sub);
  display: flex;
  gap: 15px;
  white-space: nowrap;
}
.no-data {
  text-align: center;
  padding: 50px;
  background-color: var(--bg-light);
  border-radius: 12px;
  color: var(--text-sub);
}
</style>
