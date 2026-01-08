<template>
  <div class="list-container">
    <ul v-if="comments.length > 0" class="item-list">
      <li v-for="comment in comments" :key="comment.id" class="list-item">
        <div class="comment-info">
          <p class="comment-text">{{ comment.content }}</p>
          <span class="comment-post-title">└ 원문: {{ comment.post_title }}</span>
        </div>
        <div class="comment-meta">
          <span class="meta-item">{{ comment.created_at }}</span>
        </div>
      </li>
    </ul>
    <div v-else class="no-data">
      <p>작성한 댓글이 없습니다.</p>
    </div>
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue';
import { getMyComments } from '@/api/mypage';

const comments = ref([]);

onMounted(async () => {
  try {
    const response = await getMyComments();
    if (response.data.results) {
        comments.value = response.data.results;
    } else {
        comments.value = response.data;
    }
  } catch (error) {
    console.error('내가 쓴 댓글 목록을 가져오는데 실패했습니다:', error);
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
.comment-text {
  font-size: 16px;
  margin-bottom: 10px;
}
.comment-post-title {
  font-size: 14px;
  color: var(--text-sub);
}
.comment-meta {
  font-size: 13px;
  color: var(--text-sub);
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
