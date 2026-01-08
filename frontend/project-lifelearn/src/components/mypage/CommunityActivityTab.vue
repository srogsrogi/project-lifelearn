<template>
  <div class="community-activity-tab">
    <!-- 1. 커뮤니티 통계 -->
    <CommunityStats />

    <!-- 2. 섹션 네비게이션 -->
    <div class="section-nav">
      <button @click="section = 'posts'" :class="{ active: section === 'posts' }">
        내가 쓴 글
      </button>
      <button @click="section = 'comments'" :class="{ active: section === 'comments' }">
        내가 쓴 댓글
      </button>
      <button @click="section = 'scraps'" :class="{ active: section === 'scraps' }">
        스크랩
      </button>
    </div>

    <!-- 3. 동적 콘텐츠 -->
    <div class="section-content">
      <MyPostList v-if="section === 'posts'" />
      <MyCommentList v-if="section === 'comments'" />
      <MyScrapList v-if="section === 'scraps'" />
    </div>
  </div>
</template>

<script setup>
import { ref } from 'vue';
import CommunityStats from './community/CommunityStats.vue';
import MyPostList from './community/MyPostList.vue';
import MyCommentList from './community/MyCommentList.vue';
import MyScrapList from './community/MyScrapList.vue';

const section = ref('posts'); // 기본으로 '내가 쓴 글' 섹션을 보여줍니다.
</script>

<style scoped>
.community-activity-tab {
  padding-top: 10px;
}
.section-nav {
  display: flex;
  gap: 20px;
  border-bottom: 1px solid var(--border);
  margin-bottom: 30px;
}
.section-nav button {
  padding: 10px 5px;
  font-size: 16px;
  font-weight: 600;
  color: var(--text-sub);
  background: none;
  border: none;
  cursor: pointer;
  border-bottom: 2px solid transparent;
  margin-bottom: -1px;
}
.section-nav button.active {
  color: var(--primary);
  border-bottom-color: var(--primary);
}
</style>