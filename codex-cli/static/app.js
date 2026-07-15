const urlInput = document.querySelector('#url');
const submitButton = document.querySelector('#submit');
const status = document.querySelector('#status');
const results = document.querySelector('#results');
const codexStatus = document.querySelector('#codexStatus');

const esc = (value = '') => String(value).replace(/[&<>'"]/g, char => ({
  '&': '&amp;',
  '<': '&lt;',
  '>': '&gt;',
  "'": '&#39;',
  '"': '&quot;'
}[char]));

const duration = seconds => seconds
  ? `${Math.floor(seconds / 60)}:${String(seconds % 60).padStart(2, '0')}`
  : '';

const views = value => value
  ? `${new Intl.NumberFormat('en', { notation: 'compact' }).format(value)} views`
  : '';

async function checkCodex() {
  try {
    const data = await fetch('/api/status').then(response => response.json());
    codexStatus.className = `codex-status ${data.loggedIn ? 'ok' : 'warn'}`;
    codexStatus.textContent = data.loggedIn ? 'Codex CLI is signed in with ChatGPT.' : data.message;
  } catch {
    codexStatus.textContent = 'Unable to check Codex CLI status.';
  }
}

function render(data) {
  results.innerHTML = `
    <div class="overview"><span>Overview</span><p>${esc(data.overview)}</p></div>
    ${(data.videos || []).map((video, index) => `
      <article class="video-card">
        <div class="number">${String(index + 1).padStart(2, '0')}</div>
        <div>
          <a class="title" href="${esc(video.url)}" target="_blank" rel="noopener">${esc(video.title)}</a>
          <div class="meta">${[duration(video.duration), views(video.view_count)].filter(Boolean).join(' | ')}</div>
          <p class="summary">${esc(video.summary)}</p>
          <ul>${(video.points || []).map(point => `<li>${esc(point)}</li>`).join('')}</ul>
          <blockquote>${esc(video.takeaway)}</blockquote>
        </div>
      </article>`).join('')}
    <p class="disclaimer">${esc(data.disclaimer)}</p>`;
}

async function summarize() {
  const url = urlInput.value.trim();
  if (!url) {
    status.textContent = 'Paste a YouTube URL first.';
    urlInput.focus();
    return;
  }
  submitButton.disabled = true;
  results.innerHTML = '';
  status.innerHTML = '<span class="spinner"></span> Reading transcripts and asking Codex to summarize. Channel URLs may take a few minutes...';
  try {
    const response = await fetch('/api/summarize', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ url })
    });
    const data = await response.json();
    if (!response.ok) throw new Error(data.error || 'Unable to complete the summary.');
    status.textContent = `Done. Summarized ${data.videos?.length || 0} video(s).`;
    render(data);
  } catch (error) {
    status.textContent = error.message;
  } finally {
    submitButton.disabled = false;
  }
}

submitButton.addEventListener('click', summarize);
urlInput.addEventListener('keydown', event => {
  if (event.key === 'Enter') summarize();
});
checkCodex();
