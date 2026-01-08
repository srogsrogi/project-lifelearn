<template>
  <div class="profile-edit-form">
    <!-- 1. 기본 정보 수정 폼 -->
    <form @submit.prevent="saveProfile" class="basic-info-form">
      <h3>기본 정보 수정</h3>
      <div class="form-item">
        <label for="username">사용자명</label>
        <input type="text" id="username" :value="profileData.username" disabled>
      </div>
      <div class="form-item">
        <label for="name">이름</label>
        <input type="text" id="name" v-model="editableProfile.name">
      </div>
      <div class="form-item">
        <label for="email">이메일</label>
        <input type="email" id="email" v-model="editableProfile.email">
      </div>
      
      <!-- 마케팅 수신 동의 체크박스 추가 -->
      <div class="form-item checkbox-item">
        <label>마케팅 정보 수신</label>
        <div class="checkbox-wrapper">
          <input type="checkbox" id="marketing" v-model="editableProfile.marketing_opt_in">
          <label for="marketing" class="checkbox-label">이벤트 및 혜택 알림 수신에 동의합니다.</label>
        </div>
      </div>

      <div class="actions">
        <button type="button" class="btn btn-outline" @click="$emit('cancel')">취소</button>
        <button type="submit" class="btn btn-primary">저장</button>
      </div>
    </form>

    <hr class="divider" />

    <!-- 2. 비밀번호 변경 폼 -->
    <div class="password-change-section">
      <h3>비밀번호 변경</h3>
      
      <form @submit.prevent="handlePasswordChange" class="password-form">
        <div class="form-item">
          <label for="current-password">현재 비밀번호</label>
          <input 
            type="password" 
            id="current-password" 
            v-model="passwordForm.old_password" 
            required
            placeholder="현재 비밀번호를 입력하세요"
          >
        </div>
        <div class="form-item">
          <label for="new-password">새 비밀번호</label>
          <input 
            type="password" 
            id="new-password" 
            v-model="passwordForm.new_password" 
            required
            placeholder="새 비밀번호를 입력하세요"
          >
        </div>
        <div class="form-item">
          <label for="confirm-password">새 비밀번호 확인</label>
          <input 
            type="password" 
            id="confirm-password" 
            v-model="passwordConfirm" 
            required
            placeholder="새 비밀번호를 다시 입력하세요"
          >
        </div>
        
        <p v-if="passwordError" class="error-msg">{{ passwordError }}</p>
        <p v-if="passwordSuccess" class="success-msg">{{ passwordSuccess }}</p>

        <div class="actions">
          <button type="submit" class="btn btn-outline btn-sm">비밀번호 변경하기</button>
        </div>
      </form>
    </div>
  </div>
</template>

<script setup>
import { ref, watchEffect } from 'vue';
import { changePassword } from '@/api/auth';

const props = defineProps({
  profileData: {
    type: Object,
    required: true,
  },
});

const emit = defineEmits(['save', 'cancel']);

// --- 기본 정보 수정 로직 ---
const editableProfile = ref({});

watchEffect(() => {
  editableProfile.value = { ...props.profileData };
});

const saveProfile = () => {
  emit('save', editableProfile.value);
};

// --- 비밀번호 변경 로직 ---
const passwordForm = ref({
  old_password: '',
  new_password: '',
});
const passwordConfirm = ref('');
const passwordError = ref('');
const passwordSuccess = ref('');

const handlePasswordChange = async () => {
  passwordError.value = '';
  passwordSuccess.value = '';

  if (passwordForm.value.new_password !== passwordConfirm.value) {
    passwordError.value = '새 비밀번호가 일치하지 않습니다.';
    return;
  }
  if (passwordForm.value.new_password.length < 8) {
     passwordError.value = '비밀번호는 8자 이상이어야 합니다.';
     return;
  }

  try {
    await changePassword(passwordForm.value);
    passwordSuccess.value = '비밀번호가 성공적으로 변경되었습니다.';
    
    passwordForm.value.old_password = '';
    passwordForm.value.new_password = '';
    passwordConfirm.value = '';

  } catch (error) {
    console.error('비밀번호 변경 실패:', error);
    if (error.response && error.response.data) {
        const data = error.response.data;
        if (data.detail) {
            passwordError.value = data.detail;
        } else if (data.old_password) {
            passwordError.value = `현재 비밀번호: ${data.old_password[0]}`;
        } else if (data.new_password) {
             passwordError.value = `새 비밀번호: ${data.new_password[0]}`;
        } else {
            passwordError.value = '비밀번호 변경 중 오류가 발생했습니다.';
        }
    } else {
        passwordError.value = '서버 통신 오류가 발생했습니다.';
    }
  }
};
</script>

<style scoped>
h3 {
    font-size: 18px;
    margin-bottom: 20px;
    font-weight: 700;
    color: var(--text-main);
}

.divider {
    margin: 40px 0;
    border: 0;
    border-top: 1px solid var(--border);
}

.form-item {
  display: flex;
  padding: 15px 10px;
  align-items: center;
  border-bottom: 1px solid #f5f5f5;
}
.form-item label {
  width: 140px;
  font-weight: 600;
  color: var(--text-sub);
}
.form-item input[type="text"],
.form-item input[type="email"],
.form-item input[type="password"] {
  flex-grow: 1;
  padding: 10px 12px;
  border: 1px solid var(--border);
  border-radius: 6px;
  transition: 0.2s;
}
.form-item input:focus {
    border-color: var(--primary);
    outline: none;
}
.form-item input:disabled {
  background-color: var(--bg-light);
  color: #999;
}

/* 체크박스 아이템 스타일 */
.checkbox-item {
  align-items: flex-start;
}
.checkbox-wrapper {
  display: flex;
  align-items: center;
  gap: 8px;
  padding-top: 2px;
}
.checkbox-wrapper input[type="checkbox"] {
  width: 18px;
  height: 18px;
  cursor: pointer;
}
.checkbox-label {
  width: auto !important;
  font-weight: 400 !important;
  color: var(--text-sub) !important;
  cursor: pointer;
  margin: 0;
}

.actions {
  margin-top: 25px;
  text-align: right;
  display: flex;
  gap: 10px;
  justify-content: flex-end;
}

.password-change-section {
    margin-top: 10px;
}

.password-form {
    background-color: #fafafa;
    padding: 20px;
    border-radius: 8px;
    border: 1px solid var(--border);
}
.error-msg {
    color: #e11d48;
    font-size: 14px;
    margin-top: 15px;
    text-align: center;
}
.success-msg {
    color: #10b981;
    font-size: 14px;
    margin-top: 15px;
    text-align: center;
    font-weight: 600;
}
.btn-sm {
    padding: 8px 16px;
    font-size: 14px;
}
</style>