import { ref, computed } from 'vue';
import { defineStore } from 'pinia';
import { logout as apiLogout } from '@/api/auth';

export const useAuthStore = defineStore('auth', () => {
  // 상태 (State)
  const token = ref(localStorage.getItem('auth_token') || null);
  const user = ref(null);

  // Getter: 로그인 여부 확인
  const isAuthenticated = computed(() => !!token.value);

  // Action: 로그인 성공 처리
  const login = (newToken) => {
    console.log('AuthStore: Login called', newToken);
    token.value = newToken;
    localStorage.setItem('auth_token', newToken);
  };

  // Action: 로그아웃 처리
  const logout = async () => {
    console.log('AuthStore: Logout called');
    try {
      // 백엔드 로그아웃 API 호출 (선택 사항)
      // await apiLogout(); 
    } catch (error) {
      console.error('Logout failed:', error);
    } finally {
      // 클라이언트 상태 초기화
      console.log('AuthStore: Clearing state');
      token.value = null;
      user.value = null;
      localStorage.removeItem('auth_token');
    }
  };

  return {
    token,
    user,
    isAuthenticated,
    login,
    logout,
  };
});
