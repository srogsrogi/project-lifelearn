<template>
  <div class="result-list-container">

    <!-- Case 1: 분석 중 (로딩 상태) -->
    <div v-if="isLoading" class="loading-container">
      <div class="loading-spinner"></div>
      <h2>AI 분석 진행 중...</h2>
      <p>강좌 정보를 수집하고 맞춤 분석을 진행하고 있습니다. 잠시만 기다려주세요.</p>
    </div>

    <!-- Case 2: 분석 완료 후 (결과 표시) -->
    <template v-else-if="isAnalyzed">
      <!-- Top Recommendation Hero (1위 추천 강좌) -->
      <div v-if="topRecommendation" class="comments-section">
        <div class="ai-comment-box highlight">
          <div class="comment-content">
            <!-- 1. 라벨 및 아이콘 (좌상단) -->
            <div class="comment-header">
              <span class="crown-icon">👑</span>
              <span class="comment-label">AI 최우수 추천</span>
            </div>

            <!-- 2. 강의 제목 (강조) -->
            <h2 class="course-name-hero">{{ topRecommendation.course_name }}</h2>

            <!-- 3. 추천 코멘트 -->
            <p class="comment-text">"{{ topRecommendation.recommendation_reason }}"</p>
          </div>
        </div>
      </div>

      <!-- Cards Grid -->
      <div class="cards-grid">
        <AnalysisResultCard
          v-for="res in results"
          :key="res.id"
          :result="res"
        />
      </div>

      <!-- 참고 문구 (하단 이동) -->
      <p class="comment-note">※ AI 분석은 참고용이며 최종 결정은 학습자의 판단이 필요합니다.</p>
    </template>

    <!-- Case 3: 분석 전 (사용 가이드) -->
    <div v-else class="guide-container">
      <div class="guide-header">
        <h2>AI 강좌 분석 사용 가이드</h2>
        <p>
          단순한 스펙 비교를 넘어, <strong>LLM(거대언어모델)</strong>이 사용자의 학습 목표를 이해하고<br>
          가중치 기반 알고리즘으로 <strong>나에게 가장 적합한 강좌</strong>를 논리적으로 분석해 드립니다.
        </p>
      </div>

      <div class="steps-grid">
        <div class="step-item">
          <div class="step-num">1</div>
          <div class="step-content">
            <h3>관심강좌 등록</h3>
            <p>분석하고 싶은 강의를 먼저 <strong>관심강좌(찜)</strong>에 등록해 주세요. 수강 중인 강좌도 포함할 수 있습니다.</p>
          </div>
        </div>

        <div class="step-item">
          <div class="step-num">2</div>
          <div class="step-content">
            <h3>학습 목표 입력</h3>
            <p>
              "비전공자인데 데이터 분석가로 취업하고 싶어"처럼 구체적인 목표를 적어주세요.<br>
              <strong>AI가 문맥을 파악</strong>하여 이 강좌가 왜 적합한지 설명해 줍니다.
            </p>
          </div>
        </div>

        <div class="step-item">
          <div class="step-num">3</div>
          <div class="step-content">
            <h3>선호도 가중치 설정</h3>
            <p>
              이론/실무/난이도/기간 중 나에게 중요한 요소에 높은 점수를 주세요.<br>
              <strong>유클리드 거리 알고리즘</strong>을 통해 개인화된 <strong>적합도 점수(%)</strong>가 산출됩니다.
            </p>
          </div>
        </div>

        <div class="step-item">
          <div class="step-num">4</div>
          <div class="step-content">
            <h3>비교 대상 선택</h3>
            <p>좌측 목록에서 분석할 강좌를 <strong>최대 3개까지 선택</strong>하세요. 너무 많은 강좌는 비교가 어려울 수 있습니다.</p>
          </div>
        </div>

        <div class="step-item highlight">
          <div class="step-num">5</div>
          <div class="step-content">
            <h3>AI 분석 시작</h3>
            <p>
              <strong>[분석 시작]</strong> 버튼을 누르면 AI 코멘트, 리뷰 요약(장단점), 적합도 점수를 한눈에 볼 수 있습니다.
            </p>
          </div>
        </div>
      </div>
    </div>

  </div>
</template>

<script setup>
import { computed } from 'vue';
import AnalysisResultCard from './AnalysisResultCard.vue';

const props = defineProps({
  results: {
    type: Array,
    required: true
  },
  personalizedComments: {
    type: Array,
    default: () => []
  },
  isAnalyzed: {
    type: Boolean,
    default: false
  },
  isLoading: {
    type: Boolean,
    default: false
  }
});

// 1위 추천 코멘트 (results[0]에 해당하는 코멘트)
const topRecommendation = computed(() => {
  return props.personalizedComments.length > 0 ? props.personalizedComments[0] : null;
});
</script>

<style scoped>
.result-list-container {
  display: flex;
  flex-direction: column;
  gap: 32px;
}

/* Loading State */
.loading-container {
  background: white;
  border: 1px solid var(--border);
  border-radius: 24px;
  padding: 60px 40px;
  text-align: center;
}

.loading-spinner {
  width: 50px;
  height: 50px;
  border: 4px solid #f3f4f6;
  border-top: 4px solid var(--primary);
  border-radius: 50%;
  animation: spin 1s linear infinite;
  margin: 0 auto 24px;
}

@keyframes spin {
  0% { transform: rotate(0deg); }
  100% { transform: rotate(360deg); }
}

.loading-container h2 {
  font-size: 20px;
  font-weight: 700;
  color: var(--text-main);
  margin-bottom: 12px;
}

.loading-container p {
  font-size: 14px;
  color: var(--text-sub);
}

/* Comments Section */
.comments-section {
  display: flex;
  flex-direction: column;
  gap: 20px;
}

/* AI Comment Box */
.ai-comment-box {
  background: linear-gradient(135deg, #ffffff 0%, #fff8f9 100%);
  border: 2px solid #ffe4e6;
  border-radius: 24px;
  padding: 36px 40px;
  position: relative;
  overflow: hidden;
  box-shadow: 0 4px 24px rgba(246, 73, 89, 0.08);
  transition: all 0.3s ease;
}

.ai-comment-box::before {
  content: '';
  position: absolute;
  top: 0;
  left: 0;
  right: 0;
  height: 4px;
  background: linear-gradient(90deg, var(--primary) 0%, #ff8fa3 100%);
}

.ai-comment-box.highlight:hover {
  transform: translateY(-2px);
  box-shadow: 0 8px 32px rgba(246, 73, 89, 0.15);
}

.comment-content {
  position: relative;
  z-index: 1;
}

.comment-header {
  display: inline-flex;
  align-items: center;
  gap: 6px;
  margin-bottom: 16px;
  background: linear-gradient(135deg, #fff 0%, #ffe4e6 100%);
  padding: 6px 14px;
  border-radius: 20px;
  box-shadow: 0 2px 8px rgba(246, 73, 89, 0.1);
  border: 1px solid #ffcdd4;
}

.crown-icon {
  font-size: 16px;
  animation: bounce 2s infinite;
}

@keyframes bounce {
  0%, 100% { transform: translateY(0); }
  50% { transform: translateY(-2px); }
}

.comment-label {
  font-size: 11px;
  font-weight: 800;
  color: var(--primary);
  text-transform: uppercase;
  letter-spacing: 0.5px;
}

.course-name-hero {
  font-size: 26px;
  font-weight: 800;
  color: #111;
  margin: 0 0 20px 0;
  line-height: 1.4;
  word-break: keep-all;
  letter-spacing: -0.5px;
}

.comment-text {
  font-size: 16px;
  font-weight: 500;
  color: #444;
  line-height: 1.8;
  margin-bottom: 0;
  word-break: keep-all;
  padding: 0 8px;
}

.comment-note {
  font-size: 12px;
  color: #999;
  text-align: center;
  margin-top: 40px; /* 상단 여백 추가 */
}

/* Cards Grid */
.cards-grid {
  display: grid;
  grid-template-columns: 1fr;
  gap: 32px;
  align-items: start; /* 각 카드를 상단 정렬하여 높이가 달라도 깔끔하게 정렬 */
}

@media (min-width: 1280px) {
  .cards-grid {
    grid-template-columns: repeat(2, 1fr);
  }
}

/* Guide Container (New) */
.guide-container {
  background: white;
  border: 1px solid var(--border);
  border-radius: 24px;
  padding: 60px 40px; /* 상하 패딩 증가 (40px -> 60px) */
  text-align: center;
  box-shadow: 0 4px 20px rgba(0,0,0,0.03);
}

.guide-header h2 {
  font-size: 26px; /* 폰트 크기 증가 */
  font-weight: 800;
  color: var(--text-main);
  margin-bottom: 16px;
}

.guide-header p {
  color: var(--text-sub);
  font-size: 16px;
  line-height: 1.6; /* 줄간격 증가 */
  margin-bottom: 50px; /* 하단 여백 증가 */
}

.steps-grid {
  display: grid;
  grid-template-columns: 1fr;
  gap: 20px; /* 그리드 간격 증가 */
  text-align: left;
}

.step-item {
  display: flex;
  align-items: flex-start;
  gap: 20px; /* 아이템 내부 간격 증가 */
  padding: 24px; /* 내부 패딩 증가 */
  background: #f9f9f9;
  border-radius: 16px; /* 라운드 증가 */
  transition: 0.2s;
}

.step-item:hover {
  background: white;
  box-shadow: 0 8px 24px rgba(0,0,0,0.06); /* 그림자 강화 */
  transform: translateY(-4px); /* 호버 효과 강화 */
}

.step-item.highlight {
  background: #fff0f2;
  border: 1px solid #ffdce0;
}

.step-num {
  width: 32px; height: 32px; /* 번호표 크기 증가 */
  background: var(--text-main);
  color: white;
  border-radius: 50%;
  display: flex; align-items: center; justify-content: center;
  font-weight: 800;
  font-size: 15px;
  flex-shrink: 0;
  margin-top: 2px;
}

.step-item.highlight .step-num {
  background: var(--primary);
}

.step-content h3 {
  font-size: 16px; /* 제목 크기 증가 */
  font-weight: 700;
  color: var(--text-main);
  margin-bottom: 8px;
}

.step-content p {
  font-size: 14px;
  color: var(--text-sub);
  line-height: 1.6; /* 가독성을 위한 줄간격 */
  margin: 0;
  word-break: keep-all; /* 한글 단어 끊김 방지 */
}

.step-content strong {
  color: var(--primary-dark);
  font-weight: 600;
}
</style>
