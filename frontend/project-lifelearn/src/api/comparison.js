// src/api/comparison.js

import apiClient from './index';

/**
 * 강좌 비교 분석 API
 *
 * POST /api/v1/comparisons/analyze/
 *
 * @param {Object} params - 분석 요청 파라미터
 * @param {Array<number>} params.course_ids - 비교할 강좌 ID 리스트 (1-3개)
 * @param {number} params.weekly_hours - 주당 학습 가능 시간 (1-168)
 * @param {Object} params.user_preferences - 사용자 선호도 (각 항목 0-5)
 * @param {number} params.user_preferences.theory - 이론적 깊이 선호도
 * @param {number} params.user_preferences.practical - 실무 활용도 선호도
 * @param {number} params.user_preferences.difficulty - 학습 난이도 선호도
 * @param {number} params.user_preferences.duration - 학습 기간 선호도
 * @param {string} params.user_goal - 사용자 학습 목표 (10-1000자)
 *
 * @returns {Promise} 분석 결과
 */
export const analyzeComparison = (params) => {
  return apiClient.post('/comparisons/analyze/', params);
};

/**
 * 강좌 AI 평가 조회
 *
 * GET /api/v1/comparisons/courses/{course_id}/ai-review/
 *
 * @param {number} courseId - 강좌 ID
 * @returns {Promise} AI 평가 정보
 */
export const getCourseAIReview = (courseId) => {
  return apiClient.get(`/comparisons/courses/${courseId}/ai-review/`);
};

/**
 * 강좌 리뷰 요약 조회
 *
 * GET /api/v1/comparisons/courses/{course_id}/review-summary/
 *
 * @param {number} courseId - 강좌 ID
 * @returns {Promise} 리뷰 요약 정보
 */
export const getCourseReviewSummary = (courseId) => {
  return apiClient.get(`/comparisons/courses/${courseId}/review-summary/`);
};

/**
 * 강좌 감성분석 조회
 *
 * GET /api/v1/comparisons/courses/{course_id}/sentiment/
 *
 * @param {number} courseId - 강좌 ID
 * @returns {Promise} 감성분석 결과
 */
export const getCourseSentiment = (courseId) => {
  return apiClient.get(`/comparisons/courses/${courseId}/sentiment/`);
};
