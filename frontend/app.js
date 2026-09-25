const form = document.querySelector('#question-form');
const questionInput = document.querySelector('#question');
const askButton = document.querySelector('#ask-button');
const result = document.querySelector('#result');
const researchList = document.querySelector('#research-list');
const researchCount = document.querySelector('#research-count');

function escapeHtml(value = '') {
  return String(value).replace(/[&<>'"]/g, char => ({ '&':'&amp;', '<':'&lt;', '>':'&gt;', "'":'&#39;', '"':'&quot;' }[char]));
}

function renderResearch(items) {
  researchCount.textContent = `${items.length} fictional excerpts`;
  researchList.innerHTML = items.map(item => `
    <article class="research-card">
      <div class="research-meta"><strong>${escapeHtml(item.source)}</strong><span>${escapeHtml(item.location)}</span></div>
      <p>${escapeHtml(item.text)}</p>
    </article>`).join('');
}

async function loadResearch() {
  try {
    const response = await fetch('/demo-research');
    if (!response.ok) throw new Error('No research endpoint');

    const data = await response.json();
    renderResearch(Array.isArray(data) ? data : data.research);
  } catch (error) {
    console.error(error);
    researchCount.textContent = 'Research unavailable';
    researchList.innerHTML = '<p>Demo research could not be loaded.</p>';
  }
}

function evidenceHtml(sources = []) {
  if (!sources.length) return '';
  return `
    <h4 class="evidence-title">Relevant research</h4>
    <div>${sources.map(source => `
      <article class="evidence-card">
        <div class="evidence-meta">
          <span><strong>${escapeHtml(source.source)}</strong> · ${escapeHtml(source.location)}</span>
          ${source.similarity_score !== undefined ? `<span>retrieval score ${escapeHtml(source.similarity_score)}</span>` : ''}
        </div>
        <blockquote>“${escapeHtml(source.text)}”</blockquote>
      </article>`).join('')}</div>`;
}

function showLoading() {
  result.className = 'result';
  result.innerHTML = '<div class="loading"><span class="spinner" aria-hidden="true"></span><span>Finding relevant research and generating a grounded response…</span></div>';
}

function renderResult(data) {
  if (data.status === 'answered') {
    result.className = 'result';
    result.innerHTML = `
      <p class="state-kicker">ANSWERED FROM AVAILABLE RESEARCH</p>
      <h3>What the research suggests</h3>
      <div class="answer-box"><div class="answer-label">AI INTERPRETATION</div><p>${escapeHtml(data.answer)}</p></div>
      ${evidenceHtml(data.sources)}`;
    return;
  }

  if (data.status === 'insufficient_evidence') {
    result.className = 'result insufficient';
    result.innerHTML = `
      <p class="state-kicker">INSUFFICIENT EVIDENCE</p>
      <h3>Not enough evidence found</h3>
      <p>The available research does not contain enough relevant information to answer this question reliably. Try rephrasing it or ask about onboarding, setup, support, or next steps.</p>`;
    return;
  }

  if (data.status === 'answer_validation_failed') {
    result.className = 'result validation';
    result.innerHTML = `
      <p class="state-kicker">ANSWER WITHHELD</p>
      <h3>I couldn't generate a reliable answer</h3>
      <p>Potentially relevant research was found, but the generated answer did not pass validation. The rejected AI answer is intentionally hidden; you can still inspect the underlying research.</p>
      ${evidenceHtml(data.sources)}`;
    return;
  }

  showError();
}

function showError() {
  result.className = 'result error';
  result.innerHTML = `
    <p class="state-kicker">TECHNICAL ERROR</p>
    <h3>Something went wrong</h3>
    <p>The system couldn't process this question right now. Please try again.</p>`;
}

form.addEventListener('submit', async event => {
  event.preventDefault();
  const question = questionInput.value.trim();
  if (!question) return;
  askButton.disabled = true;
  askButton.textContent = 'Asking…';
  showLoading();
  result.scrollIntoView({ behavior: 'smooth', block: 'nearest' });
  try {
    const response = await fetch('/questions', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ project_id: 'demo-project', question })
    });
    if (!response.ok) throw new Error(`HTTP ${response.status}`);
    renderResult(await response.json());
  } catch (error) {
    console.error(error);
    showError();
  } finally {
    askButton.disabled = false;
    askButton.textContent = 'Ask AI';
  }
});

document.querySelectorAll('[data-question]').forEach(button => {
  button.addEventListener('click', () => {
    questionInput.value = button.dataset.question;
    questionInput.focus();
  });
});

loadResearch();
