<template>
  <div class="my-account-tab">
    <div v-if="profile">
      <ProfileView
        v-if="!isEditing"
        :profile="profile"
        @edit="isEditing = true"
      />
      <ProfileEditForm
        v-else
        :profile-data="profile"
        @cancel="isEditing = false"
        @save="handleProfileUpdate"
      />
    </div>
    <div v-else class="loading">
      <p>프로필 정보를 불러오는 중입니다...</p>
    </div>
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue';
import ProfileView from './profile/ProfileView.vue';
import ProfileEditForm from './profile/ProfileEditForm.vue';
import { getProfile, updateProfile } from '@/api/mypage';

const profile = ref(null);
const isEditing = ref(false);

onMounted(async () => {
  try {
    const response = await getProfile();
    profile.value = response.data;
  } catch (error) {
    console.error('프로필 정보를 가져오는데 실패했습니다:', error);
  }
});

const handleProfileUpdate = async (updatedProfile) => {
  try {
    const response = await updateProfile(updatedProfile);
    profile.value = response.data;
    isEditing.value = false;
    // TODO: 성공/실패 토스트 메시지 표시
  } catch (error) {
    console.error('프로필 업데이트에 실패했습니다:', error);
    // TODO: 에러 메시지 표시 (예: 이메일 중복)
  }
};
</script>

<style scoped>
.my-account-tab {
  padding-top: 10px;
}
.loading {
  text-align: center;
  padding: 50px;
  color: var(--text-sub);
}
</style>