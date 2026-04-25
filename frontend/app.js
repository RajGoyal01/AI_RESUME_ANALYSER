// ═══════════════════════════════════════
// AI RESUME ANALYSER - Frontend Logic
// ═══════════════════════════════════════

// Always point to the Flask backend server
// Works with: Live Server (Go Live), file://, or Flask itself
const API = 'http://localhost:5000';

const $ = (s) => document.querySelector(s);
const $$ = (s) => document.querySelectorAll(s);

// ─── DOM Elements ───
const form = $('#analyseForm');
const dropzone = $('#dropzone');
const fileInput = $('#resumeFile');
const fileInfo = $('#fileInfo');
const fileName = $('#fileName');
const fileRemove = $('#fileRemove');
const analyseBtn = $('#analyseBtn');
const loadingSection = $('#loadingSection');
const resultsSection = $('#results');
const errorCard = $('#errorCard');
const uploadSection = $('#upload');
const heroSection = $('#hero');

// ─── Init ───
document.addEventListener('DOMContentLoaded', init);

async function init() {
    try {
        const res = await fetch(`${API}/api/config`);
        if (res.ok) {
            const config = await res.json();
            populateSelect($('#course'), config.courses);
            populateSelect($('#branch'), config.branches);
        } else {
            throw new Error('Config fetch failed');
        }
    } catch (e) {
        // Fallback options - works even without server
        const courses = ["B.Tech","M.Tech","B.E.","M.E.","BCA","MCA","B.Sc","M.Sc","MBA","BBA","Ph.D","Diploma"];
        const branches = ["Computer Science","Data Science","Electrical Engineering","Electronics & Communication","Mechanical Engineering","Civil Engineering","MBA / Business"];
        populateSelect($('#course'), courses);
        populateSelect($('#branch'), branches);
    }
    setupDropzone();
    setupForm();
    $('#newAnalysis').addEventListener('click', resetUI);
    $('#retryBtn').addEventListener('click', resetUI);
}

function populateSelect(el, options) {
    options.forEach(opt => {
        const o = document.createElement('option');
        o.value = opt; o.textContent = opt;
        el.appendChild(o);
    });
}

// ─── Dropzone ───
function setupDropzone() {
    dropzone.addEventListener('click', () => fileInput.click());
    dropzone.addEventListener('dragover', (e) => { e.preventDefault(); dropzone.classList.add('dragover'); });
    dropzone.addEventListener('dragleave', () => dropzone.classList.remove('dragover'));
    dropzone.addEventListener('drop', (e) => {
        e.preventDefault(); dropzone.classList.remove('dragover');
        if (e.dataTransfer.files.length) { fileInput.files = e.dataTransfer.files; showFile(e.dataTransfer.files[0]); }
    });
    fileInput.addEventListener('change', () => { if (fileInput.files.length) showFile(fileInput.files[0]); });
    fileRemove.addEventListener('click', (e) => { e.stopPropagation(); clearFile(); });
}

function showFile(file) {
    fileName.textContent = `${file.name} (${(file.size/1024).toFixed(1)} KB)`;
    fileInfo.style.display = 'flex';
    dropzone.style.borderColor = 'var(--success)';
    dropzone.style.borderStyle = 'solid';
    dropzone.style.background = 'rgba(34, 197, 94, 0.03)';
}

function clearFile() {
    fileInput.value = ''; fileInfo.style.display = 'none';
    dropzone.style.borderColor = '';
    dropzone.style.borderStyle = '';
    dropzone.style.background = '';
}

// ─── Form Submit ───
function setupForm() {
    form.addEventListener('submit', async (e) => {
        e.preventDefault();
        if (!fileInput.files.length) { alert('Please upload your resume file.'); return; }
        if (!$('#course').value) { alert('Please select your course.'); return; }
        if (!$('#branch').value) { alert('Please select your branch/domain.'); return; }
        await analyseResume();
    });
}

function showError(message) {
    loadingSection.style.display = 'none';
    errorCard.style.display = 'block';
    $('#errorMsg').textContent = message;
    analyseBtn.disabled = false;
}

async function analyseResume() {
    // Show loading
    uploadSection.style.display = 'none';
    heroSection.style.display = 'none';
    errorCard.style.display = 'none';
    loadingSection.style.display = 'block';
    analyseBtn.disabled = true;

    // Validate file size on client side before uploading
    const file = fileInput.files[0];
    if (file.size > 50 * 1024 * 1024) {
        showError('File is too large. Maximum file size is 50MB.');
        return;
    }

    if (file.size === 0) {
        showError('The selected file is empty. Please choose a valid resume file.');
        return;
    }

    // Animate loading steps
    animateLoadingSteps();

    const formData = new FormData();
    formData.append('resume', file);
    formData.append('course', $('#course').value);
    formData.append('branch', $('#branch').value);
    formData.append('domain', $('#branch').value);

    try {
        // Upload directly - no blocking health check
        const controller = new AbortController();
        const timeoutId = setTimeout(() => controller.abort(), 120000);

        let res;
        try {
            res = await fetch(`${API}/api/analyze`, {
                method: 'POST',
                body: formData,
                signal: controller.signal,
            });
        } catch (fetchErr) {
            clearTimeout(timeoutId);
            if (fetchErr.name === 'AbortError') {
                showError('Request timed out. The file might be too large or the server is busy. Please try again.');
            } else {
                // This catches: server not running, CORS blocked, network errors
                showError('Cannot connect to the server. Make sure you have started the server first:\n\n1. Open Command Prompt or Terminal\n2. cd to the backend folder\n3. Run: python app.py\n4. Then open http://localhost:5000 in your browser');
            }
            return;
        }
        clearTimeout(timeoutId);

        // Read response body
        let text = '';
        try {
            text = await res.text();
        } catch (readErr) {
            showError('Connection lost while reading response. Please try again.');
            return;
        }

        // Handle empty response
        if (!text || text.trim() === '') {
            if (res.status === 413) {
                showError('File too large. Please upload a file smaller than 50MB.');
            } else if (res.status >= 500) {
                showError('Server error occurred. Check the terminal running app.py for details.');
            } else {
                showError('Server returned empty response (HTTP ' + res.status + '). Try restarting the server.');
            }
            return;
        }

        // Parse JSON
        let data;
        try {
            data = JSON.parse(text);
        } catch (parseErr) {
            if (text.includes('<html') || text.includes('<!DOCTYPE')) {
                showError(res.status === 413
                    ? 'File too large. Please upload a file smaller than 50MB.'
                    : 'Server error (HTTP ' + res.status + '). Try restarting the server.');
            } else {
                showError('Unexpected server response: ' + text.substring(0, 200));
            }
            return;
        }

        // Check for error in response
        if (!res.ok || data.error) {
            showError(data.error || 'Analysis failed (HTTP ' + res.status + ')');
            return;
        }

        // Validate results
        if (data.overall_score === undefined && data.overall_score === null) {
            showError('Server returned incomplete results. Please try again.');
            return;
        }

        // Finish loading animation
        await new Promise(r => setTimeout(r, 1500));
        loadingSection.style.display = 'none';
        renderResults(data);
    } catch (err) {
        console.error('Analysis error:', err);
        showError(err.message || 'An unexpected error occurred. Please try again.');
    }
    analyseBtn.disabled = false;
}

function animateLoadingSteps() {
    const steps = $$('#loadingSteps .step');
    steps.forEach((s, i) => {
        setTimeout(() => {
            steps.forEach(st => st.classList.remove('active'));
            if (i > 0) steps[i-1].classList.add('done');
            s.classList.add('active');
        }, i * 800);
    });
    setTimeout(() => steps[steps.length-1].classList.add('done'), steps.length * 800);
}

// ─── Render Results ───
function renderResults(data) {
    resultsSection.style.display = 'block';
    $('#nav-results').classList.add('active');
    $('#nav-upload').classList.remove('active');

    // Overall Score Ring
    const score = data.overall_score || 0;
    const circle = $('#scoreCircle');
    const circumference = 2 * Math.PI * 85;
    const offset = circumference - (score / 100) * circumference;
    setTimeout(() => { circle.style.strokeDashoffset = offset; circle.style.transition = 'stroke-dashoffset 1.5s ease'; }, 100);

    // Animate score number
    animateNumber($('#overallScore'), score);
    $('#gradeBadge').textContent = data.grade || '-';
    $('#scoreTitle').textContent = `Resume Score: ${score}/100`;
    const scoreTexts = {
        90: "Outstanding! Your resume is MNC-ready.",
        80: "Excellent! Minor improvements needed.",
        70: "Very good. Address weak areas for top companies.",
        60: "Good foundation. Focus on improvements.",
        50: "Average. Significant enhancements needed.",
        40: "Below average. Major improvements required.",
        0: "Needs complete overhaul."
    };
    for (const [threshold, text] of Object.entries(scoreTexts).sort((a,b) => b[0]-a[0])) {
        if (score >= parseInt(threshold)) { $('#scoreDesc').textContent = text; break; }
    }

    // Parsed Info
    const pi = data.parsed_info || {};
    let infoHtml = '';
    if (pi.name) infoHtml += `<span class="info-item">👤 ${pi.name}</span>`;
    if (pi.email) infoHtml += `<span class="info-item">📧 ${pi.email}</span>`;
    if (pi.phone) infoHtml += `<span class="info-item">📱 ${pi.phone}</span>`;
    if (pi.word_count) infoHtml += `<span class="info-item">📝 ${pi.word_count} words</span>`;
    if (pi.project_count) infoHtml += `<span class="info-item">🔧 ${pi.project_count} projects</span>`;
    if (data.input) infoHtml += `<span class="info-item">🎓 ${data.input.course} - ${data.input.branch}</span>`;
    $('#parsedInfo').innerHTML = infoHtml;

    // Category Breakdown
    const catNames = {
        skills_match: "🛠️ Skills Match", experience_quality: "💼 Experience",
        education: "🎓 Education", projects: "🔧 Projects",
        formatting: "📋 Formatting", keywords_ats: "🔑 ATS Keywords",
        certifications: "📜 Certifications", achievements: "🏆 Achievements",
        soft_skills: "🤝 Soft Skills"
    };
    let catHtml = '';
    for (const [key, name] of Object.entries(catNames)) {
        const s = data.scores?.[key] || 0;
        const cls = s >= 80 ? 'top' : s >= 60 ? 'high' : s >= 40 ? 'mid' : 'low';
        catHtml += `<div class="cat-item"><div class="cat-header"><span class="cat-name">${name}</span><span class="cat-score" style="color:var(--${cls === 'top' ? 'success' : cls === 'high' ? 'primary2' : cls === 'mid' ? 'warning' : 'danger'})">${s}</span></div><div class="cat-bar"><div class="cat-bar-fill ${cls}" style="width:0%"></div></div></div>`;
    }
    $('#categoriesGrid').innerHTML = catHtml;
    setTimeout(() => {
        $$('.cat-bar-fill').forEach((bar, i) => {
            const s = Object.values(data.scores || {})[i] || 0;
            setTimeout(() => bar.style.width = s + '%', i * 100);
        });
    }, 200);

    // MNC Comparison
    let mncHtml = '';
    const mncEntries = Object.entries(data.mnc_scores || {}).sort((a,b) => b[1]-a[1]);
    for (const [name, s] of mncEntries) {
        const color = s >= 70 ? 'var(--success)' : s >= 50 ? 'var(--warning)' : 'var(--danger)';
        mncHtml += `<div class="mnc-item"><div class="mnc-name">${name}</div><div class="mnc-score" style="color:${color}">${s}%</div><div class="mnc-label">readiness</div></div>`;
    }
    $('#mncGrid').innerHTML = mncHtml;

    // Weak Areas
    let weakHtml = '';
    for (const w of data.weak_areas || []) {
        let missingHtml = '';
        if (w.missing?.length) {
            missingHtml = '<div class="weak-missing">' + w.missing.map(m => `<span class="missing-tag">${m}</span>`).join('') + '</div>';
        }
        weakHtml += `<div class="weak-item ${w.severity}"><div class="weak-header"><span class="weak-title">${w.area}</span><span class="severity-badge ${w.severity}">${w.severity}</span></div><div class="weak-suggestion">💡 ${w.suggestion}</div>${missingHtml}</div>`;
    }
    $('#weakList').innerHTML = weakHtml || '<p style="color:var(--text3)">No major weak areas detected. Great job!</p>';

    // Strong Areas
    let strongHtml = '';
    for (const s of data.strong_areas || []) {
        strongHtml += `<div class="strong-item">✅ ${s}</div>`;
    }
    $('#strongList').innerHTML = strongHtml || '<p style="color:var(--text3)">Upload resume to see strengths.</p>';

    // Skills Analysis
    const details = data.details?.skills || {};
    let skillsHtml = '';
    const skillSections = [
        { title: 'Core Skills Found', items: details.found_core, cls: 'found' },
        { title: 'Programming Found', items: details.found_programming, cls: 'found' },
        { title: 'Frameworks Found', items: details.found_frameworks, cls: 'found' },
        { title: 'Technologies Found', items: details.found_technologies, cls: 'found' },
        { title: 'Missing Core Skills', items: details.missing_core, cls: 'missing' },
        { title: 'Missing Programming', items: details.missing_programming, cls: 'missing' },
    ];
    for (const sec of skillSections) {
        if (sec.items?.length) {
            skillsHtml += `<div class="skills-section"><div class="skills-section-title">${sec.title}</div><div class="skill-tags">${sec.items.map(s => `<span class="skill-tag ${sec.cls}">${s}</span>`).join('')}</div></div>`;
        }
    }
    $('#skillsSections').innerHTML = skillsHtml;

    // Suggestions
    let sugHtml = '';
    for (const s of data.suggestions || []) {
        sugHtml += `<div class="suggestion-item">${s}</div>`;
    }
    $('#suggestionsList').innerHTML = sugHtml;

    // Company Selection Chances
    const recs = data.company_recommendations || [];
    let compHtml = '';
    for (const r of recs) {
        const tierCls = `t${r.tier}`;
        const tierLabel = r.tier === 1 ? 'Tier 1' : r.tier === 2 ? 'Tier 2' : 'Tier 3';
        const domainBadge = r.domain_match ? '<span class="domain-match-badge">✓ Domain Match</span>' : '';
        compHtml += `<div class="company-card" data-tier="${r.tier}">
            <div class="company-emoji">${r.emoji}</div>
            <div class="company-info">
                <div class="company-name-row">
                    <span class="company-name">${r.company}</span>
                    <span class="company-tier ${tierCls}">${tierLabel}</span>
                    ${domainBadge}
                </div>
                <div class="company-bar-row">
                    <div class="company-bar"><div class="company-bar-fill ${r.level_color}" style="width:0%" data-width="${r.chance_score}"></div></div>
                    <span class="company-pct">${r.chance_score}%</span>
                </div>
                <div class="company-tip">💡 ${r.tip}</div>
            </div>
            <div class="company-right">
                <span class="chance-level ${r.level_color}">${r.level}</span>
                <div class="hiring-bar-text">Bar: ${r.hiring_bar}</div>
            </div>
        </div>`;
    }
    $('#companyList').innerHTML = compHtml;

    // Animate company bars
    setTimeout(() => {
        $$('.company-bar-fill').forEach((bar, i) => {
            setTimeout(() => bar.style.width = bar.dataset.width + '%', i * 60);
        });
    }, 300);

    // Tier filter buttons
    $$('.tier-btn').forEach(btn => {
        btn.addEventListener('click', () => {
            $$('.tier-btn').forEach(b => b.classList.remove('active'));
            btn.classList.add('active');
            const tier = btn.dataset.tier;
            $$('.company-card').forEach(card => {
                if (tier === 'all' || card.dataset.tier === tier) {
                    card.classList.remove('hidden');
                } else {
                    card.classList.add('hidden');
                }
            });
        });
    });

    // Scroll to results
    resultsSection.scrollIntoView({ behavior: 'smooth' });
}

function animateNumber(el, target) {
    let current = 0;
    const duration = 1500;
    const step = target / (duration / 16);
    const timer = setInterval(() => {
        current += step;
        if (current >= target) { current = target; clearInterval(timer); }
        el.textContent = Math.round(current);
    }, 16);
}

function resetUI() {
    resultsSection.style.display = 'none';
    errorCard.style.display = 'none';
    loadingSection.style.display = 'none';
    uploadSection.style.display = 'block';
    heroSection.style.display = 'block';
    clearFile();
    form.reset();
    $('#nav-upload').classList.add('active');
    $('#nav-results').classList.remove('active');
    // Reset score circle
    const circle = $('#scoreCircle');
    circle.style.transition = 'none';
    circle.style.strokeDashoffset = 534;
    window.scrollTo({ top: 0, behavior: 'smooth' });
}
