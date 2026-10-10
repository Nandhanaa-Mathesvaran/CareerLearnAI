export const API_BASE = "http://localhost:8000/api";

export async function analyzeSkills(targetCareer, currentSkills, experienceLevel) {
    const req = await fetch(`${API_BASE}/analyze`, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ targetCareer, currentSkills, experienceLevel })
    });
    if (!req.ok) throw new Error("Failed to analyze skills");
    return await req.json();
}
