<template>
  <div class="index-page">
    <!-- 메인 히어로 섹션 -->
    <section class="hero">
        <div class="container">
            <h1>언제 어디서나,<br>당신의 <span>배움</span>을 잇습니다.</h1>
            <p>국내 유수 대학의 명품 강좌를 무료로 만나보세요.</p>
            <div class="search-bar">
                <input type="text" placeholder="배우고 싶은 분야나 강좌명을 입력하세요" @keyup.enter="handleSearch">
                <button @click="handleSearch">🔍</button>
            </div>
        </div>
    </section>

    <!-- 카테고리 섹션 -->
    <section class="categories container">
        <div class="section-title">
            분야별 탐색
        </div>
        <div class="cate-grid">
            <router-link to="/courses?category=인문" class="cate-item"><span class="cate-icon">📚</span>인문</router-link>
            <router-link to="/courses?category=사회" class="cate-item"><span class="cate-icon">👥</span>사회</router-link>
            <router-link to="/courses?category=교육" class="cate-item"><span class="cate-icon">🎓</span>교육</router-link>
            <router-link to="/courses?category=공학" class="cate-item"><span class="cate-icon">⚙️</span>공학</router-link>
            <router-link to="/courses?category=자연" class="cate-item"><span class="cate-icon">🔬</span>자연</router-link>
            <router-link to="/courses?category=의약" class="cate-item"><span class="cate-icon">🩺</span>의약</router-link>
            <router-link to="/courses?category=예체능" class="cate-item"><span class="cate-icon">🎨</span>예체능</router-link>
            <router-link to="/courses?category=융·복합" class="cate-item"><span class="cate-icon">🧩</span>융·복합</router-link>
            <router-link to="/courses?category=기타" class="cate-item"><span class="cate-icon">✨</span>기타</router-link>
        </div>
    </section>

    <!-- 강좌 카드 그리드 -->
    <section class="course-list-section container">
        <div class="section-title">
            신규 & 인기 강좌
            <router-link to="/courses">전체보기 →</router-link>
        </div>

        <div class="course-grid">
          <CourseCard
            v-for="course in courses"
            :key="course.id"
            v-bind="course"
          />
        </div>
        <div v-if="courses.length === 0" class="no-data">
            불러올 수 있는 강좌가 없습니다.
        </div>
    </section>
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue';
import { useRouter } from 'vue-router';
import CourseCard from '@/components/common/CourseCard.vue';
import { getCourseList } from '@/api/courses';

const router = useRouter();
const courses = ref([]);

const handleSearch = (e) => {
    const query = e.target.value || e.target.previousElementSibling.value;
    if (query) {
        router.push(`/courses?search=${query}`);
    }
};

const fetchCourses = async () => {
    try {
        const params = {
            page_size: 200, // 충분한 양을 가져와서 필터링 후 8개 선택
            ordering: '-study_start' // 최근 개강 강좌 우선
        };

        const response = await getCourseList(params);
        const processedCourses = response.data.results.map(processCourseData);

        // 접수 가능한 강좌만 필터링하여 8개 선택 (접수중, 개강임박, 개강예정, 상시)
        courses.value = processedCourses
            .filter(course => ['접수중', '개강임박', '개강예정', '상시'].includes(course.status))
            .slice(0, 8);
    } catch (error) {
        console.error('강좌 목록 불러오기 실패:', error);
    }
};

const processCourseData = (course) => {
    const today = new Date().toISOString().split('T')[0];
    let status = '모집마감';
    let badgeColor = '#999';

    // 1. 수강 종료일 체크 (최우선)
    if (course.study_end && course.study_end < today) {
        status = '종료';
        badgeColor = '#666';
    }
    // 2. 상시 모집 강좌
    else if (course.enrollment_end === null) {
        status = '상시';
        badgeColor = '#333';
    }
    // 3. 모집 마감 (enrollment_end는 지났지만 study_end는 안 지남)
    else if (course.enrollment_end < today) {
        status = '모집마감';
        badgeColor = '#999';
    }
    // 4. 접수중 / 개강임박
    else if (course.enrollment_start <= today && today <= course.enrollment_end) {
        // 접수 마감까지 7일 이하면 개강임박
        const enrollEnd = new Date(course.enrollment_end);
        const todayDate = new Date(today);
        const daysUntilEnd = Math.ceil((enrollEnd - todayDate) / (1000 * 60 * 60 * 24));

        if (daysUntilEnd <= 7) {
            status = '개강임박';
            badgeColor = 'var(--secondary)';
        } else {
            status = '접수중';
            badgeColor = 'var(--primary-dark)';
        }
    }
    // 5. 개강예정 (접수 전)
    else if (course.enrollment_start > today) {
        status = '개강예정';
        badgeColor = 'var(--secondary)';
    }

    return {
        ...course,
        status,
        badgeColor
    };
};

onMounted(() => {
    fetchCourses();
});
</script>

<style scoped>
/* 메인 히어로 섹션 */
.hero { padding: 80px 0; text-align: center; background: linear-gradient(180deg, #fff 0%, #fff0f2 100%); }
.hero h1 { font-size: 48px; margin-bottom: 20px; line-height: 1.3; font-weight: 700; }
.hero span { color: var(--primary); }
.hero p { color: var(--text-sub); font-size: 18px; margin-bottom: 40px; }
.search-bar { max-width: 600px; margin: 0 auto; display: flex; position: relative; }
.search-bar input { width: 100%; padding: 18px 20px; border: 2px solid var(--primary); border-radius: 50px; font-size: 16px; outline: none; }
.search-bar button { position: absolute; right: 8px; top: 8px; background: var(--primary); color: white; border: none; width: 48px; height: 48px; border-radius: 50%; cursor: pointer; font-size: 18px; }

/* 카테고리 섹션 */
.categories { padding: 60px 0; }
.section-title { font-size: 28px; font-weight: 700; margin-bottom: 30px; display: flex; justify-content: space-between; align-items: end; }
.section-title a { font-size: 14px; color: var(--text-sub); }
.cate-grid { display: grid; grid-template-columns: repeat(3, 1fr); gap: 15px; }
@media (min-width: 992px) {
    .cate-grid { grid-template-columns: repeat(5, 1fr); }
}
.cate-item { 
    background: var(--bg-light); 
    padding: 20px 10px; 
    text-align: center; 
    border-radius: 12px; 
    transition: 0.3s; 
    cursor: pointer; 
    border: 1px solid transparent;
    text-decoration: none;
    color: inherit;
    display: block;
}
.cate-item:hover { border-color: var(--primary); color: var(--primary); transform: translateY(-3px); }
.cate-icon { font-size: 24px; margin-bottom: 10px; display: block; }

/* 강좌 카드 그리드 */
.course-list-section { padding: 60px 0 100px; }

.course-grid { display: grid; grid-template-columns: repeat(auto-fill, minmax(280px, 1fr)); gap: 30px; }
.no-data { text-align: center; padding: 50px; color: #888; grid-column: 1 / -1; }
</style>