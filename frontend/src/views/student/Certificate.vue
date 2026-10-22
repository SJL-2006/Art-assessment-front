<!-- 学生证书页：纸质证书卡片 + 下载按钮 -->
<template>
  <div class="page">
    <div class="page-head">
      <h2 class="title-splash">我的证书</h2>
      <span class="total">共 {{ list.length }} 张</span>
    </div>

    <div class="certs">
      <div v-for="c in list" :key="c.id" class="cert" :class="c.type === 'music' ? 'gold' : 'violet'">
        <!-- 顶部装饰 -->
        <div class="top-band"></div>

        <!-- 证书主体 -->
        <div class="body">
          <div class="corner tl"></div><div class="corner tr"></div>
          <div class="corner bl"></div><div class="corner br"></div>

          <div class="cert-head">
            <span class="emoji">{{ c.type === 'music' ? '🎵' : '🎨' }}</span>
            <div>
              <div class="cert-title">{{ c.type === 'music' ? '音乐素养测评' : '美术素养测评' }}</div>
              <div class="cert-sub">官方认证证书</div>
            </div>
          </div>

          <div class="cert-name">
            兹证明 <b>{{ c.name }}</b> 同学
          </div>
          <div class="cert-desc">
            在 {{ c.date }} 完成的{{ c.type === 'music' ? '音乐' : '美术' }}素养测评中，
            表现优异，获得等级 <span class="level">{{ c.level }}</span>，
            特发此证，以资鼓励。
          </div>

          <div class="cert-foot">
            <div class="left">
              <span class="label">证书编号</span>
              <span class="no">{{ c.no }}</span>
            </div>
            <div class="seal">{{ c.type === 'music' ? '音乐测评中心' : '美术测评中心' }}</div>
          </div>
        </div>

        <!-- 底部装饰 -->
        <div class="bottom-band"></div>

        <div class="actions">
          <button class="btn-outline">预览</button>
          <button class="btn-gradient">下载 PDF</button>
        </div>
      </div>

      <div v-if="!list.length" class="empty card">暂无证书，加油测评吧 🎉</div>
    </div>
  </div>
</template>

<script setup>
import { onMounted, ref } from 'vue'
import { api } from '../../api'

const list = ref([])

onMounted(async () => {
  try {
    const res = await api.student.workspace()
    list.value = res.certificates || []
  } catch {
    list.value = [
      { id: 1, type: 'music', name: '李明', date: '2026-06-15', level: 'A', no: 'MU-2026-00581' },
      { id: 2, type: 'art',   name: '李明', date: '2026-09-08', level: 'B+', no: 'AR-2026-01203' },
    ]
  }
})
</script>

<style scoped>
.page { display: flex; flex-direction: column; gap: 22px; }
.page-head { display: flex; align-items: center; justify-content: space-between; }
.total { font-size: 13px; color: #8a93a5; }

.certs { display: grid; grid-template-columns: repeat(2, 1fr); gap: 24px; }

.cert {
  border-radius: 14px;
  overflow: hidden;
  box-shadow: 0 6px 24px rgba(70, 90, 130, 0.12);
  transition: transform 0.2s;
  background: #fff;
}
.cert:hover { transform: translateY(-4px); }

/* 金色证书（音乐） */
.cert.gold .body {
  background: linear-gradient(180deg, #fff8e6 0%, #fffdf7 40%, #fffdf7 60%, #fff8e6 100%);
  border: 2px solid #e8c87a;
}
.cert.gold .top-band, .cert.gold .bottom-band {
  background: linear-gradient(90deg, #e8c87a, #f4dfa5, #e8c87a);
}
.cert.gold .cert-title { color: #a8750f; }
.cert.gold .level { background: #fff3d0; color: #a8750f; }
.cert.gold .seal { color: #a8750f; border: 2px solid #e8c87a; }

/* 紫色证书（美术） */
.cert.violet .body {
  background: linear-gradient(180deg, #f4efff 0%, #fdfbff 40%, #fdfbff 60%, #f4efff 100%);
  border: 2px solid #c9b5f7;
}
.cert.violet .top-band, .cert.violet .bottom-band {
  background: linear-gradient(90deg, #c9b5f7, #e0d2ff, #c9b5f7);
}
.cert.violet .cert-title { color: #6a4bd8; }
.cert.violet .level { background: #eee8fd; color: #6a4bd8; }
.cert.violet .seal { color: #6a4bd8; border: 2px solid #c9b5f7; }

.top-band { height: 6px; }
.bottom-band { height: 6px; }

.body {
  position: relative;
  padding: 30px 28px 24px;
  margin: 12px;
  border-radius: 8px;
}
/* 四角花纹 */
.corner { position: absolute; width: 24px; height: 24px; border-radius: 4px; }
.corner.tl { top: 8px; left: 8px; border-top: 2px solid; border-left: 2px solid; }
.corner.tr { top: 8px; right: 8px; border-top: 2px solid; border-right: 2px solid; }
.corner.bl { bottom: 8px; left: 8px; border-bottom: 2px solid; border-left: 2px solid; }
.corner.br { bottom: 8px; right: 8px; border-bottom: 2px solid; border-right: 2px solid; }
.gold .corner { border-color: #e8c87a; }
.violet .corner { border-color: #c9b5f7; }

.cert-head { display: flex; align-items: center; gap: 10px; margin-bottom: 18px; }
.cert-head .emoji { font-size: 28px; }
.cert-title { font-size: 18px; font-weight: 700; }
.cert-sub { font-size: 12px; color: #8a93a5; margin-top: 2px; }

.cert-name { font-size: 14px; color: #556074; text-align: center; margin-bottom: 14px; }
.cert-name b { font-size: 22px; color: #2b3445; padding: 0 6px; border-bottom: 2px solid currentColor; }

.cert-desc { font-size: 13px; color: #556074; text-align: center; line-height: 2; margin-bottom: 20px; }
.level {
  display: inline-block;
  font-weight: 700;
  padding: 2px 12px;
  border-radius: 10px;
  margin: 0 4px;
}

.cert-foot {
  display: flex; justify-content: space-between; align-items: flex-end;
  padding-top: 14px;
  border-top: 1px dashed #dfe4ee;
}
.cert-foot .label { font-size: 12px; color: #8a93a5; }
.cert-foot .no { font-family: 'Consolas', monospace; font-size: 13px; color: #2b3445; margin-top: 2px; }
.seal {
  font-size: 13px; font-weight: 600;
  padding: 4px 14px; border-radius: 4px;
  transform: rotate(-4deg);
  opacity: 0.75;
}

.actions {
  padding: 14px 18px 18px;
  display: flex; justify-content: flex-end; gap: 10px;
  background: #fafbff;
}

.empty { text-align: center; color: #8a93a5; padding: 40px; }
</style>
