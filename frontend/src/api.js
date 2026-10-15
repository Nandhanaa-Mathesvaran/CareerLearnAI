const API_BASE_URL =
import.meta.env.VITE_API_BASE_URL || "http://127.0.0.1:8000/api";

async function _handleResponse(res) {
    if (!res.ok) {
        let errBody = null;
        try { errBody = await res.json(); } catch { /* ignore */ }
        const detail = errBody?.detail;
        const msg = typeof detail === 'string' ? detail : detail?.error || `Request failed: ${res.status}`;
        const err = new Error(msg);
        err.detail = detail || null;
        err.status = res.status;
        throw err;
    }
    return res.json();
}

export async function analyzeSkills(targetCareer, currentSkills, experienceLevel) {
    const res = await fetch(`${API_BASE_URL}/analyze`, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ targetCareer, currentSkills, experienceLevel })
    });
    return _handleResponse(res);
}

export async function parseResume(file) {
    const formData = new FormData();
    formData.append('file', file);
    const res = await fetch(`${API_BASE_URL}/parse-resume`, {
        method: 'POST',
        body: formData,
        // Do NOT set Content-Type — browser sets it automatically with the boundary
    });
    return _handleResponse(res);
}

export async function recommendCareers(currentSkills) {
    const res = await fetch(`${API_BASE_URL}/recommend`, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ currentSkills })
    });
    return _handleResponse(res);
}