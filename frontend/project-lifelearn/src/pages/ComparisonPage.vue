<template>
  <div class="comparison-page container">

    <main class="main-grid">
      <!-- Left Sidebar -->
      <div class="col-sidebar">
        <AnalysisSidebar
          v-model:settings="settings"
          :is-analyzing="isAnalyzing"
          @analyze="runAnalysis"
        />
      </div>

      <!-- Right Content -->
      <div class="col-content">
        <AnalysisResultList
          :results="sortedResults"
          :personalized-comments="personalizedComments"
          :is-analyzed="hasRunAnalysis"
          :is-loading="isAnalyzing"
        />
      </div>
    </main>

    <!-- 하단바 (ComparisonPage 전용) -->
    <ComparisonBar @analyze="runAnalysis" />
  </div>
</template>

<script setup>
import { ref, computed, onMounted } from 'vue';
import { useComparisonStore } from '@/stores/comparison';
import { analyzeComparison } from '@/api/comparison';
import AnalysisSidebar from '@/components/comparison/AnalysisSidebar.vue';
import AnalysisResultList from '@/components/comparison/AnalysisResultList.vue';
import ComparisonBar from '@/components/comparison/ComparisonBar.vue';

const comparisonStore = useComparisonStore();
const hasRunAnalysis = ref(false);
const isAnalyzing = ref(false);

// --- 상태 (Settings) ---
const settings = ref({
  weeklyHours: 12,
  userGoal: "비전공자이지만 데이터 분석 역량을 키워 이직하고 싶습니다. 파이썬 기초는 있지만 실무 경험은 없어서 프로젝트 위주의 강좌를 선호합니다.",
  userPreferences: {
    theory: 3,       // 0-5
    practical: 4,
    difficulty: 2,
    duration: 3
  }
});

// 분석 결과 저장
const analysisResults = ref([]);

// AI 개인화 코멘트 목록
const personalizedComments = computed(() => {
  return analysisResults.value.map(result => result.personalized_comment);
});

// --- 백엔드 응답 → 프론트엔드 형식으로 변환 ---
const mapBackendResponse = (backendData) => {
  return backendData.map(item => {
    // AI 평가 점수 1-5 → 0-100 변환
    const scaleRating = (rating) => ((rating - 1) / 4) * 100;

    return {
      // 강좌 기본 정보
      id: item.course.id,
      name: item.course.name,
      orgName: item.course.org_name,
      professor: item.course.professor,
      courseImage: item.course.course_image,
      url: item.course.url,
      studyEnd: item.course.study_end,
      week: item.course.week,
      coursePlaytime: item.course.course_playtime,

      // 매칭 점수 (백엔드에서 이미 0-100)
      totalScore: item.match_score,

      // 타임라인 정보
      minHoursPerWeek: item.timeline.min_hours_per_week,
      totalWeeks: item.timeline.total_weeks,
      remainingWeeks: item.timeline.remaining_weeks,
      timelineStatus: item.timeline.status,
      timelineRatio: item.timeline.ratio,

      // 감성분석 정보
      sentiment: item.sentiment.positive_ratio,
      reviewCount: item.sentiment.review_count,
      reliability: item.sentiment.reliability,

      // AI 평가 (1-5 → 0-100 변환)
      courseSummary: item.ai_review.course_summary,
      scores: {
        theory: scaleRating(item.ai_review.theory_rating),
        practical: scaleRating(item.ai_review.practical_rating),
        difficulty: scaleRating(item.ai_review.difficulty_rating),
        duration: scaleRating(item.ai_review.duration_rating)
      },

      // 리뷰 요약
      reviewSummary: item.review_summary.review_summary.summary,
      reviewPros: item.review_summary.review_summary.pros,
      reviewCons: item.review_summary.review_summary.cons,
      reviewWarning: item.review_summary.warning_message,

      // AI 맞춤 코멘트
      personalized_comment: item.personalized_comment
    };
  });
};

// 정렬된 결과 (매칭 점수 기준)
const sortedResults = computed(() => {
  // 백엔드에서 이미 정렬되어 오지만, 안전을 위해 한번 더 정렬
  return [...analysisResults.value].sort((a, b) => b.totalScore - a.totalScore);
});

const runAnalysis = async () => {
  if (isAnalyzing.value) return;

  isAnalyzing.value = true;

  try {
    // 백엔드 API 호출을 위한 파라미터 구성
    const params = {
      course_ids: comparisonStore.items.map(item => item.id),
      weekly_hours: settings.value.weeklyHours,
      user_preferences: settings.value.userPreferences,
      user_goal: settings.value.userGoal
    };

    console.log('📤 API 요청:', params);

    // API 호출
    const response = await analyzeComparison(params);

    console.log('📥 API 응답:', response.data);

    // 응답 데이터 변환 및 저장
    analysisResults.value = mapBackendResponse(response.data.results);

    hasRunAnalysis.value = true;

    // 성공 알림
    alert("AI 분석이 완료되었습니다!");

  } catch (error) {
    console.error('❌ API 호출 실패:', error);

    // 에러 상세 정보 출력
    if (error.response) {
      console.error('응답 에러:', error.response.data);
      alert(`분석 중 오류가 발생했습니다.\n${error.response.data.detail || '서버 오류'}`);
    } else if (error.request) {
      console.error('요청 에러:', error.request);
      alert('서버와 통신할 수 없습니다. 네트워크 연결을 확인해주세요.');
    } else {
      console.error('에러:', error.message);
      alert(`오류가 발생했습니다: ${error.message}`);
    }

  } finally {
    isAnalyzing.value = false;
  }
};
</script>

<style scoped>
.comparison-page {
  padding-top: 40px;
  padding-bottom: 100px;
}

.page-header {
  height: 80px;
  display: flex;
  align-items: center;
  justify-content: space-between;
  margin-bottom: 40px;
  border-bottom: 1px solid var(--border);
}

.page-header h1 {
  font-size: 24px;
  font-weight: 800;
  color: var(--primary-dark);
  letter-spacing: -1px;
}
.page-header h1 span {
  font-weight: 300;
  color: #ccc;
}

.points-badge {
  background: var(--bg-light);
  padding: 8px 16px;
  border-radius: 50px;
  border: 1px solid #ffdce0;
  font-size: 13px;
  color: var(--primary);
}

/* Grid Layout */
.main-grid {
  display: grid;
  grid-template-columns: 1fr;
  gap: 30px;
}

@media (min-width: 992px) {
  .main-grid {
    grid-template-columns: 300px 1fr;
  }
}
@media (min-width: 1200px) {
  .main-grid {
    grid-template-columns: 320px 1fr;
  }
}

.col-sidebar {
  /* Sidebar styles handled in component */
}
</style>
