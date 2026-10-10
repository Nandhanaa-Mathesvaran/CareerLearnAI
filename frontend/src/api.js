const API_BASE_URL =
  import.meta.env.VITE_API_BASE_URL || "http://localhost:8000/api";

export async function analyzeSkills(targetCareer, currentSkills, experienceLevel) {
    const req = await fetch(`${API_BASE_URL}/analyze`, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ targetCareer, currentSkills, experienceLevel })
    });

    if (!req.ok) {
        throw new Error("Failed to analyze skills");
    }

    return await req.json();
}