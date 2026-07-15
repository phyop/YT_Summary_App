const urlInput = document.querySelector('#url');
const apiKeyInput = document.querySelector('#apiKey');
const submitButton = document.querySelector('#submit');
const status = document.querySelector('#status');
const results = document.querySelector('#results');

const escapeHtml = (value = '') => String(value).replace(/[&<>'"]/g, ch => ({
  '&': '&amp;', '<': '&lt;', '>': '&gt;', "'": '&#39;', '"': '&quot;'
}[ch]));

function formatDuration(seconds) {
  if (!seconds) return '';
  const minutes = Math.floor(seconds / 60);
  return `${minutes}:${String(seconds % 60).padStart(2, '0')}`;
}

function formatViews(value) {
  if (!value) return '';
  return new Intl.NumberFormat('zh-TW', { notation: 'compact' }).format(value) + ' 次觀看';
}

function render(data) {
  const cards = (data.videos || []).map((video, index) => `
    <article class="video-card">
      <div class="number">${String(index + 1).padStart(2, '0')}</div>
      <div class="content">
        <a class="title" href="${escapeHtml(video.url)}" target="_blank" rel="noopener">${escapeHtml(video.title)}</a>
        <div class="meta">${[formatDuration(video.duration), formatViews(video.view_count)].filter(Boolean).join(' · ')}</div>
        <p class="summary">${escapeHtml(video.summary)}</p>
        <ul>${(video.points || []).map(point => `<li>${escapeHtml(point)}</li>`).join('')}</ul>
        <blockquote>${escapeHtml(video.takeaway)}</blockquote>
      </div>
    </article>`).join('');

  results.innerHTML = `
    <div class="overview"><span>整體觀察</span><p>${escapeHtml(data.overview)}</p></div>
    ${cards}
    <p class="disclaimer">${escapeHtml(data.disclaimer)}</p>`;
}

async function summarize() {
  const url = urlInput.value.trim();
  if (!url) { status.textContent = '請先貼上 YouTube 網址。'; urlInput.focus(); return; }
  submitButton.disabled = true;
  results.innerHTML = '';
  status.innerHTML = '<span class="spinner"></span> 正在讀取字幕與整理重點，頻道網址可能需要幾分鐘…';
  try {
    const response = await fetch('/api/summarize', {
      method: 'POST', headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ url, apiKey: apiKeyInput.value.trim() })
    });
    const data = await response.json();
    if (!response.ok) throw new Error(data.error || '無法完成摘要');
    status.textContent = `完成，共整理 ${data.videos?.length || 0} 支影片。`;
    render(data);
  } catch (error) {
    status.textContent = error.message;
  } finally { submitButton.disabled = false; }
}

submitButton.addEventListener('click', summarize);
urlInput.addEventListener('keydown', event => { if (event.key === 'Enter') summarize(); });
apiKeyInput.addEventListener('keydown', event => { if (event.key === 'Enter') summarize(); });
