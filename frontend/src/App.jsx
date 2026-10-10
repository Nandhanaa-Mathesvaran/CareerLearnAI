import React, { useState, useEffect } from 'react';
import { analyzeSkills } from './api';

// ─── Icons (inline SVG, no extra package needed) ───────────────────────────
const Icon = ({ name, className = 'w-5 h-5' }) => {
  const icons = {
    zap: <path strokeLinecap="round" strokeLinejoin="round" d="M13 10V3L4 14h7v7l9-11h-7z" />,
    brain: <path strokeLinecap="round" strokeLinejoin="round" d="M9.663 17h4.673M12 3v1m6.364 1.636l-.707.707M21 12h-1M4 12H3m3.343-5.657l-.707-.707m2.828 9.9a5 5 0 117.072 0l-.548.547A3.374 3.374 0 0014 18.469V19a2 2 0 11-4 0v-.531c0-.895-.356-1.754-.988-2.386l-.548-.547z" />,
    target: <><path strokeLinecap="round" strokeLinejoin="round" d="M9 12l2 2 4-4m6 2a9 9 0 11-18 0 9 9 0 0118 0z" /></>,
    connect: <path strokeLinecap="round" strokeLinejoin="round" d="M13.828 10.172a4 4 0 00-5.656 0l-4 4a4 4 0 105.656 5.656l1.102-1.101m-.758-4.899a4 4 0 005.656 0l4-4a4 4 0 00-5.656-5.656l-1.1 1.1" />,
    code: <path strokeLinecap="round" strokeLinejoin="round" d="M10 20l4-16m4 4l4 4-4 4M6 16l-4-4 4-4" />,
    map: <path strokeLinecap="round" strokeLinejoin="round" d="M9 20l-5.447-2.724A1 1 0 013 16.382V5.618a1 1 0 011.447-.894L9 7m0 13l6-3m-6 3V7m6 10l4.553 2.276A1 1 0 0021 18.382V7.618a1 1 0 00-.553-.894L15 4m0 13V4m0 0L9 7" />,
    arrow: <path strokeLinecap="round" strokeLinejoin="round" d="M17 8l4 4m0 0l-4 4m4-4H3" />,
    arrowLeft: <path strokeLinecap="round" strokeLinejoin="round" d="M7 16l-4-4m0 0l4-4m-4 4h18" />,
    chevron: <path strokeLinecap="round" strokeLinejoin="round" d="M19 9l-7 7-7-7" />,
    check: <path strokeLinecap="round" strokeLinejoin="round" d="M5 13l4 4L19 7" />,
    clock: <><path strokeLinecap="round" strokeLinejoin="round" d="M12 8v4l3 3m6-3a9 9 0 11-18 0 9 9 0 0118 0z" /></>,
    spark: <path strokeLinecap="round" strokeLinejoin="round" d="M5 3v4M3 5h4M6 17v4m-2-2h4m5-16l2.286 6.857L21 12l-5.714 2.143L13 21l-2.286-6.857L5 12l5.714-2.143L13 3z" />,
    x: <path strokeLinecap="round" strokeLinejoin="round" d="M6 18L18 6M6 6l12 12" />,
  };
  return (
    <svg className={className} fill="none" viewBox="0 0 24 24" stroke="currentColor" strokeWidth={2}>
      {icons[name]}
    </svg>
  );
};

// ─── Pill badge ─────────────────────────────────────────────────────────────
const Badge = ({ children, variant = 'default' }) => {
  const variants = {
    default: 'bg-indigo-100 text-indigo-700',
    violet: 'bg-violet-100 text-violet-700',
    high: 'bg-red-100 text-red-600 border border-red-200',
    medium: 'bg-amber-100 text-amber-700 border border-amber-200',
    low: 'bg-sky-100 text-sky-700 border border-sky-200',
    green: 'bg-emerald-100 text-emerald-700 border border-emerald-200',
    learning: 'bg-indigo-100 text-indigo-700 border border-indigo-200',
    done: 'bg-emerald-100 text-emerald-700 border border-emerald-200',
  };
  return (
    <span className={`inline-flex items-center px-2.5 py-0.5 rounded-full text-[11px] font-bold uppercase tracking-wider ${variants[variant] || variants.default}`}>
      {children}
    </span>
  );
};

// ─── LANDING PAGE ────────────────────────────────────────────────────────────
function Landing({ onStart }) {
  const features = [
    {
      icon: 'zap', label: 'Skill Gap Analysis', desc: "Instantly see what skills you're missing for your dream career."
    },
    { icon: 'brain', label: 'Personalized Learning', desc: 'AI-curated explanations tailored to your experience level.' },
    { icon: 'connect', label: 'Concept Connections', desc: 'Understand how each skill links to your target career.' },
    { icon: 'code', label: 'Practical Challenges', desc: 'Apply what you learn with real, hands-on coding tasks.' },
  ];

  return (
    <div className="min-h-screen">
      {/* ── Hero ── */}
      <section className="relative overflow-hidden bg-hero-gradient text-white">
        {/* ambient glows */}
        <div className="glow-blob w-96 h-96 bg-violet-600 top-[-6rem] left-[-4rem]" />
        <div className="glow-blob w-80 h-80 bg-indigo-500 bottom-[-4rem] right-[10%]" />
        <div className="glow-blob w-64 h-64 bg-cyan-500 top-[30%] right-[-2rem]" />

        <div className="relative max-w-7xl mx-auto px-6 pt-20 pb-28 flex flex-col lg:flex-row items-center gap-16 z-10">
          {/* Text */}
          <div className="flex-1 text-center lg:text-left space-y-8">
            <div className="inline-flex items-center gap-2 glass rounded-full px-4 py-2 text-sm font-semibold text-violet-200">
              <Icon name="spark" className="w-4 h-4 text-violet-300" />
              AI-Powered Career Learning
            </div>

            <h1 className="text-5xl md:text-6xl lg:text-7xl font-black leading-[1.08] tracking-tight">
              Your Future Career<br />
              <span className="gradient-text">Starts Here.</span>
            </h1>

            <p className="text-lg md:text-xl text-indigo-200 max-w-xl leading-relaxed">
              Discover your skill gaps, understand what matters, and turn your learning into real-world skills — powered by AI.
            </p>

            <div className="flex flex-col sm:flex-row gap-4 justify-center lg:justify-start">
              <button
                onClick={onStart}
                className="group relative inline-flex items-center justify-center gap-2 px-8 py-4 bg-brand-gradient text-white font-bold text-lg rounded-2xl shadow-glow-indigo hover:shadow-glow-violet transition-all duration-300 overflow-hidden"
              >
                <span className="relative z-10 flex items-center gap-2">
                  Build My Career Roadmap
                  <Icon name="arrow" className="w-5 h-5 group-hover:translate-x-1 transition-transform" />
                </span>
                <div className="absolute inset-0 bg-white opacity-0 group-hover:opacity-10 transition-opacity" />
              </button>

              <button
                onClick={onStart}
                className="inline-flex items-center justify-center gap-2 px-8 py-4 glass text-white font-semibold text-lg rounded-2xl hover:bg-white/20 transition-all duration-300"
              >
                Explore How It Works
              </button>
            </div>
          </div>

          {/* SVG visual: connected skill path */}
          <div className="flex-1 max-w-sm lg:max-w-md animate-float">
            <svg viewBox="0 0 400 360" className="w-full drop-shadow-2xl" aria-hidden="true">
              <defs>
                <linearGradient id="gr1" x1="0%" y1="0%" x2="100%" y2="100%">
                  <stop offset="0%" stopColor="#6366f1" />
                  <stop offset="100%" stopColor="#8b5cf6" />
                </linearGradient>
                <linearGradient id="gr2" x1="0%" y1="0%" x2="100%" y2="100%">
                  <stop offset="0%" stopColor="#8b5cf6" />
                  <stop offset="100%" stopColor="#06b6d4" />
                </linearGradient>
                <filter id="glow">
                  <feGaussianBlur stdDeviation="4" result="blur" />
                  <feMerge><feMergeNode in="blur" /><feMergeNode in="SourceGraphic" /></feMerge>
                </filter>
              </defs>
              {/* Lines */}
              <line x1="200" y1="50" x2="100" y2="145" stroke="#6366f1" strokeWidth="2" strokeDasharray="6 4" opacity="0.6" />
              <line x1="200" y1="50" x2="300" y2="145" stroke="#8b5cf6" strokeWidth="2" strokeDasharray="6 4" opacity="0.6" />
              <line x1="100" y1="145" x2="200" y2="235" stroke="#06b6d4" strokeWidth="2" strokeDasharray="6 4" opacity="0.6" />
              <line x1="300" y1="145" x2="200" y2="235" stroke="#a5b4fc" strokeWidth="2" strokeDasharray="6 4" opacity="0.6" />
              <line x1="200" y1="235" x2="200" y2="320" stroke="url(#gr2)" strokeWidth="2.5" opacity="0.8" />
              {/* Nodes */}
              {[
                { cx: 200, cy: 50, r: 26, fill: "url(#gr1)", label: "ML", sub: "Target" },
                { cx: 100, cy: 145, r: 22, fill: "#8b5cf6", label: "Math", sub: "Foundation" },
                { cx: 300, cy: 145, r: 22, fill: "#6366f1", label: "Stats", sub: "Core" },
                { cx: 200, cy: 235, r: 24, fill: "url(#gr2)", label: "ML", sub: "Models" },
                { cx: 200, cy: 320, r: 26, fill: "#06b6d4", label: "🎯", sub: "Career" },
              ].map((n, i) => (
                <g key={i} filter="url(#glow)">
                  <circle cx={n.cx} cy={n.cy} r={n.r + 4} fill={n.fill} opacity="0.2" />
                  <circle cx={n.cx} cy={n.cy} r={n.r} fill={n.fill} />
                  <text x={n.cx} y={n.cy + 1} textAnchor="middle" dominantBaseline="middle" fill="white" fontSize="11" fontWeight="700">{n.label}</text>
                  <text x={n.cx} y={n.cy + n.r + 13} textAnchor="middle" fill="rgba(165,180,252,0.9)" fontSize="10" fontWeight="500">{n.sub}</text>
                </g>
              ))}
            </svg>
          </div>
        </div>
      </section>

      {/* ── Steps ── */}
      <section className="py-24 px-6 bg-white">
        <div className="max-w-5xl mx-auto">
          <p className="text-center text-indigo-500 font-bold uppercase tracking-[0.2em] text-sm mb-4">How It Works</p>
          <h2 className="text-4xl font-black text-center text-slate-900 mb-16">Three steps to real expertise</h2>
          <div className="grid grid-cols-1 md:grid-cols-3 gap-8 relative">
            {/* connector line */}
            <div className="hidden md:block absolute top-12 left-1/4 right-1/4 h-0.5 bg-gradient-to-r from-indigo-300 via-violet-300 to-cyan-300" />
            {[
              { num: '01', color: 'from-indigo-500 to-violet-500', title: 'Discover', desc: 'Enter your target career and current skills. Our gap engine identifies exactly what you need to learn.' },
              { num: '02', color: 'from-violet-500 to-purple-500', title: 'Understand', desc: 'AI explains every missing concept in plain language and shows how it connects to your career goals.' },
              { num: '03', color: 'from-cyan-500 to-indigo-500', title: 'Apply', desc: "Complete guided, practical coding or analysis tasks to cement every concept you've learned." },
            ].map((s, i) => (
              <div key={i} className="card-hover flex flex-col items-center text-center bg-surfaceAlt border border-indigo-100 p-8 rounded-3xl relative">
                <div className={`w-16 h-16 rounded-2xl bg-gradient-to-br ${s.color} text-white flex items-center justify-center text-2xl font-black mb-5 shadow-glow-indigo`}>{s.num}</div>
                <h3 className="text-xl font-black text-slate-900 mb-3">{s.title}</h3>
                <p className="text-slate-500 leading-relaxed text-sm">{s.desc}</p>
              </div>
            ))}
          </div>
        </div>
      </section>

      {/* ── Features ── */}
      <section className="py-24 px-6 bg-surfaceAlt">
        <div className="max-w-6xl mx-auto">
          <p className="text-center text-violet-500 font-bold uppercase tracking-[0.2em] text-sm mb-4">Features</p>
          <h2 className="text-4xl font-black text-center text-slate-900 mb-16">Everything you need to level up</h2>
          <div className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-4 gap-6">
            {features.map((f, i) => (
              <div key={i} className="card-hover glass-light p-7 rounded-3xl border border-indigo-100">
                <div className="w-12 h-12 rounded-xl bg-brand-gradient flex items-center justify-center mb-5 shadow-glow-indigo">
                  <Icon name={f.icon} className="w-6 h-6 text-white" />
                </div>
                <h3 className="font-black text-slate-800 text-lg mb-2">{f.label}</h3>
                <p className="text-slate-500 text-sm leading-relaxed">{f.desc}</p>
              </div>
            ))}
          </div>
        </div>
      </section>

      {/* ── CTA Banner ── */}
      <section className="py-24 px-6 bg-hero-gradient text-white text-center relative overflow-hidden">
        <div className="glow-blob w-72 h-72 bg-violet-600 top-[-2rem] left-[10%]" />
        <div className="glow-blob w-64 h-64 bg-cyan-500 bottom-[-2rem] right-[15%]" />
        <div className="relative z-10 max-w-2xl mx-auto space-y-6">
          <h2 className="text-4xl md:text-5xl font-black">Ready to close your skill gaps?</h2>
          <p className="text-indigo-200 text-lg">Join thousands of students who are learning smarter, not harder.</p>
          <button
            onClick={onStart}
            className="group inline-flex items-center gap-2 px-10 py-4 bg-white text-indigo-700 font-black text-lg rounded-2xl hover:shadow-glow-indigo transition-all duration-300"
          >
            Get Started Free
            <Icon name="arrow" className="w-5 h-5 group-hover:translate-x-1 transition-transform" />
          </button>
        </div>
      </section>
    </div>
  );
}

// ─── PROFILE FORM ────────────────────────────────────────────────────────────
function ProfileForm({ onAnalyze, initialProfile }) {
  const [career, setCareer] = useState(initialProfile.targetCareer || 'ML Engineer');
  const [level, setLevel] = useState(initialProfile.experienceLevel || 'Beginner');
  const [skillInput, setSkillInput] = useState('');
  const [skills, setSkills] = useState(initialProfile.currentSkills || []);

  const CAREERS = ['ML Engineer', 'Data Scientist', 'Data Analyst', 'Software Engineer', 'AI Engineer', 'Full Stack Developer'];
  const SUGGESTED = ['Python', 'SQL', 'JavaScript', 'React', 'Machine Learning', 'Statistics', 'Excel', 'Git'];

  const addSkill = (s) => {
    if (s.trim() && !skills.includes(s.trim())) setSkills(prev => [...prev, s.trim()]);
    setSkillInput('');
  };

  const onKeyDown = e => { if (e.key === 'Enter') { e.preventDefault(); addSkill(skillInput); } };

  return (
    <div className="max-w-2xl mx-auto py-12 px-4">
      <div className="text-center mb-10">
        <div className="inline-flex items-center gap-2 bg-indigo-100 text-indigo-600 rounded-full px-4 py-2 text-sm font-bold mb-4">
          <Icon name="spark" className="w-4 h-4" /> Build Your Profile
        </div>
        <h2 className="text-4xl font-black text-slate-900">Let's map your career path</h2>
        <p className="text-slate-500 mt-3 text-lg">Tell us where you are and where you want to go.</p>
      </div>

      <div className="glass-light border border-indigo-100 rounded-3xl p-8 shadow-card space-y-8">
        {/* Career */}
        <div>
          <label className="block text-sm font-bold text-slate-700 mb-2 uppercase tracking-wider">Target Career</label>
          <div className="grid grid-cols-2 sm:grid-cols-3 gap-3">
            {CAREERS.map(c => (
              <button
                key={c} type="button"
                onClick={() => setCareer(c)}
                className={`p-3 rounded-xl text-sm font-bold border-2 transition-all text-left leading-tight ${career === c ? 'border-brandPrimary bg-indigo-50 text-indigo-700 shadow-glow-indigo' : 'border-slate-200 bg-white text-slate-600 hover:border-indigo-300 hover:bg-indigo-50'}`}
              >{c}</button>
            ))}
          </div>
        </div>

        {/* Level */}
        <div>
          <label className="block text-sm font-bold text-slate-700 mb-3 uppercase tracking-wider">Experience Level</label>
          <div className="flex flex-wrap gap-3">
            {['Beginner', 'Intermediate', 'Advanced'].map(l => (
              <button
                key={l} type="button"
                onClick={() => setLevel(l)}
                className={`flex-1 py-3 rounded-xl font-bold border-2 transition-all text-sm ${level === l ? 'border-brandViolet bg-violet-50 text-violet-700' : 'border-slate-200 bg-white text-slate-600 hover:border-violet-300'}`}
              >{l}</button>
            ))}
          </div>
        </div>

        {/* Skills */}
        <div>
          <label className="block text-sm font-bold text-slate-700 mb-2 uppercase tracking-wider">Your Current Skills</label>
          <div className="flex gap-2 mb-3">
            <input
              type="text" value={skillInput}
              onChange={e => setSkillInput(e.target.value)}
              onKeyDown={onKeyDown}
              placeholder="Type a skill and press Enter…"
              className="flex-1 rounded-xl border-2 border-slate-200 bg-white p-3.5 text-slate-800 font-medium focus:border-indigo-400 focus:outline-none focus:ring-2 focus:ring-indigo-100 transition"
            />
            <button type="button" onClick={() => addSkill(skillInput)}
              className="px-5 rounded-xl bg-indigo-600 text-white font-bold hover:bg-indigo-700 transition shadow-glow-indigo">Add</button>
          </div>

          {/* Suggested */}
          <div className="flex flex-wrap gap-2 mb-4">
            {SUGGESTED.filter(s => !skills.includes(s)).slice(0, 6).map(s => (
              <button key={s} type="button" onClick={() => addSkill(s)}
                className="px-3 py-1.5 bg-indigo-50 text-indigo-600 rounded-lg text-xs font-bold border border-indigo-100 hover:bg-indigo-100 transition">+ {s}</button>
            ))}
          </div>

          {/* Added chips */}
          <div className="flex flex-wrap gap-2 min-h-[2rem]">
            {skills.map(s => (
              <span key={s} className="flex items-center gap-1.5 bg-indigo-600 text-white px-3.5 py-1.5 rounded-full text-sm font-semibold">
                {s}
                <button type="button" onClick={() => setSkills(skills.filter(sk => sk !== s))}
                  className="w-4 h-4 rounded-full bg-white/20 hover:bg-white/30 flex items-center justify-center transition">
                  <Icon name="x" className="w-2.5 h-2.5" />
                </button>
              </span>
            ))}
          </div>
        </div>

        <button
          type="button"
          onClick={() => onAnalyze({ targetCareer: career, experienceLevel: level, currentSkills: skills })}
          className="w-full py-4 bg-brand-gradient text-white font-black text-lg rounded-2xl hover:shadow-glow-violet transition-all duration-300 flex items-center justify-center gap-2"
        >
          Analyze My Skills <Icon name="arrow" className="w-5 h-5" />
        </button>
      </div>
    </div>
  );
}

// ─── DASHBOARD ───────────────────────────────────────────────────────────────
function Dashboard({ data, onSelectSkill, progress, onBack, showRoadmap }) {
  const uniqueGaps = data.skillExplanations.filter((v, i, a) => a.findIndex(t => t.skill === v.skill) === i);
  const knownSkills = data.knownSkills.filter(s => !uniqueGaps.find(u => u.skill === s));

  const readinessColor = data.readinessEstimate === 'High' ? 'from-emerald-400 to-cyan-500'
    : data.readinessEstimate === 'Medium' ? 'from-amber-400 to-orange-500' : 'from-red-400 to-rose-500';
  const readinessPct = data.readinessEstimate === 'High' ? 80 : data.readinessEstimate === 'Medium' ? 50 : 20;

  return (
    <div className="max-w-7xl mx-auto py-8 px-4 space-y-6">
      {/* Top bar */}
      <div className="flex flex-wrap justify-between items-center gap-4">
        <button onClick={onBack} className="flex items-center gap-2 text-slate-500 hover:text-indigo-600 font-semibold transition-colors group">
          <Icon name="arrowLeft" className="w-4 h-4 group-hover:-translate-x-1 transition-transform" />
          Back to Profile
        </button>
        <button onClick={showRoadmap}
          className="flex items-center gap-2 px-5 py-2.5 bg-brand-gradient text-white font-bold rounded-xl shadow-glow-indigo hover:shadow-glow-violet transition-all text-sm">
          <Icon name="map" className="w-4 h-4" /> View Learning Roadmap
        </button>
      </div>

      {/* Hero card */}
      <div className="relative overflow-hidden bg-hero-gradient text-white rounded-3xl p-8 sm:p-10 shadow-card">
        <div className="glow-blob w-72 h-72 bg-violet-600 top-[-3rem] right-[-2rem]" />
        <div className="glow-blob w-56 h-56 bg-cyan-500 bottom-[-2rem] left-[15%]" />
        <div className="relative z-10 flex flex-col sm:flex-row sm:items-center sm:justify-between gap-8">
          <div>
            <p className="text-indigo-300 font-bold uppercase tracking-widest text-xs mb-2">Target Career</p>
            <h2 className="text-4xl sm:text-5xl font-black mb-4">{data.targetCareer}</h2>
            <div className="flex flex-wrap gap-3">
              <Badge variant={data.readinessEstimate === 'High' ? 'green' : data.readinessEstimate === 'Medium' ? 'medium' : 'high'}>
                {data.readinessEstimate} Readiness
              </Badge>
              <span className="text-indigo-200 text-sm font-medium self-center">{data.knownSkills.length} skills known · {data.missingSkills.length} gaps to fill</span>
            </div>
          </div>
          {/* Readiness Bar */}
          <div className="sm:min-w-[220px]">
            <div className="flex justify-between text-sm font-bold mb-2">
              <span className="text-indigo-200">Skill Readiness</span>
              <span className="text-white">{readinessPct}%</span>
            </div>
            <div className="h-4 bg-white/10 rounded-full overflow-hidden">
              <div className={`h-full bg-gradient-to-r ${readinessColor} rounded-full progress-fill`} style={{ width: `${readinessPct}%` }} />
            </div>
            <p className="text-indigo-300 text-xs mt-2">Based on required skills for {data.targetCareer}</p>
          </div>
        </div>
      </div>

      <div className="grid grid-cols-1 lg:grid-cols-5 gap-6">
        {/* Skill Gaps — wider column */}
        <div className="lg:col-span-3 space-y-4">
          <div className="flex items-center gap-2 mb-2">
            <span className="w-3 h-3 rounded-full bg-red-400 shadow shadow-red-200" />
            <h3 className="text-xl font-black text-slate-900">Skill Gaps ({uniqueGaps.length})</h3>
            <span className="text-slate-400 text-sm ml-2">Click a skill to explore</span>
          </div>

          {uniqueGaps.length === 0 ? (
            <div className="glass-light border border-emerald-200 p-6 rounded-2xl text-center">
              <Icon name="check" className="w-12 h-12 text-emerald-500 mx-auto mb-3" />
              <p className="font-bold text-emerald-700">No skill gaps — you're ready for this role!</p>
            </div>
          ) : (
            <div className="space-y-3">
              {uniqueGaps.map((exp, i) => {
                const st = progress[exp.skill];
                const priorityVariant = exp.priority === 'HIGH' ? 'high' : exp.priority === 'MEDIUM' ? 'medium' : 'low';
                return (
                  <div key={i} onClick={() => onSelectSkill(exp.skill)}
                    className="skill-gap-card card-hover glass-light border-2 border-indigo-100 p-5 rounded-2xl cursor-pointer group animate-fade-up"
                    style={{ animationDelay: `${i * 60}ms` }}>
                    <div className="flex flex-wrap items-center justify-between gap-3">
                      <div className="flex items-center gap-3">
                        <div className="w-10 h-10 rounded-xl bg-gradient-to-br from-indigo-500 to-violet-500 flex items-center justify-center shrink-0">
                          <Icon name="zap" className="w-5 h-5 text-white" />
                        </div>
                        <span className="font-black text-slate-800 text-lg group-hover:text-indigo-600 transition-colors">{exp.skill}</span>
                      </div>
                      <div className="flex items-center gap-2">
                        <Badge variant={priorityVariant}>{exp.priority} PRIORITY</Badge>
                        {st && st !== 'Not Started' && <Badge variant={st === 'Learning' ? 'learning' : 'done'}>{st}</Badge>}
                      </div>
                    </div>
                    <div className="mt-3 flex items-center gap-2 text-indigo-400 text-sm font-semibold">
                      <span>Open learning module</span>
                      <Icon name="arrow" className="w-4 h-4 group-hover:translate-x-1 transition-transform" />
                    </div>
                  </div>
                );
              })}
            </div>
          )}
        </div>

        {/* Known Skills sidebar */}
        <div className="lg:col-span-2 space-y-4">
          <div className="flex items-center gap-2 mb-2">
            <span className="w-3 h-3 rounded-full bg-emerald-400 shadow shadow-emerald-200" />
            <h3 className="text-xl font-black text-slate-900">Known Skills</h3>
          </div>
          <div className="glass-light border border-indigo-100 rounded-2xl p-5">
            {knownSkills.length === 0 ? (
              <p className="text-slate-400 text-sm text-center py-4">No recognized skills yet — add them in your profile.</p>
            ) : (
              <div className="flex flex-wrap gap-2">
                {knownSkills.map(s => (
                  <span key={s} className="flex items-center gap-1.5 px-3.5 py-1.5 bg-emerald-50 text-emerald-700 border border-emerald-200 rounded-xl font-bold text-sm">
                    <Icon name="check" className="w-3.5 h-3.5" /> {s}
                  </span>
                ))}
              </div>
            )}
          </div>

          {/* Quick tip card */}
          <div className="bg-gradient-to-br from-indigo-600 to-violet-600 rounded-2xl p-6 text-white">
            <Icon name="brain" className="w-8 h-8 mb-3 opacity-80" />
            <h4 className="font-black text-lg mb-2">Start Smart</h4>
            <p className="text-indigo-200 text-sm leading-relaxed">Click the highest-priority gap first. Each module has a hands-on task to make your learning stick.</p>
          </div>
        </div>
      </div>
    </div>
  );
}

// ─── SKILL DETAIL ────────────────────────────────────────────────────────────
function SkillDetail({ skillId, data, onBack, progress, onUpdateProgress }) {
  if (!data) return (
    <div className="max-w-2xl mx-auto py-20 text-center">
      <div className="glass-light border border-red-200 p-10 rounded-3xl">
        <p className="text-lg font-bold text-slate-600 mb-4">Skill explanation not available.</p>
        <button onClick={onBack} className="text-indigo-600 font-bold hover:underline">← Go Back</button>
      </div>
    </div>
  );

  const statusBtns = [
    { key: 'Not Started', icon: '⚪', color: 'bg-slate-800 text-white', inactive: 'bg-slate-100 text-slate-600 hover:bg-slate-200' },
    { key: 'Learning', icon: '⏳', color: 'bg-indigo-600 text-white shadow-glow-indigo', inactive: 'bg-indigo-50 text-indigo-700 hover:bg-indigo-100 border border-indigo-200' },
    { key: 'Completed', icon: '✅', color: 'bg-emerald-600 text-white', inactive: 'bg-emerald-50 text-emerald-700 hover:bg-emerald-100 border border-emerald-200' },
  ];

  return (
    <div className="max-w-7xl mx-auto py-8 px-4 space-y-6">
      <button onClick={onBack} className="flex items-center gap-2 text-slate-500 hover:text-indigo-600 font-semibold transition-colors group">
        <Icon name="arrowLeft" className="w-4 h-4 group-hover:-translate-x-1 transition-transform" /> Back to Dashboard
      </button>

      {/* Header card */}
      <div className="relative overflow-hidden bg-hero-gradient text-white rounded-3xl p-8 sm:p-10">
        <div className="glow-blob w-64 h-64 bg-violet-600 top-[-2rem] right-[5%]" />
        <div className="relative z-10 flex flex-col sm:flex-row sm:items-start sm:justify-between gap-6">
          <div>
            <div className="flex items-center gap-2 mb-3">
              <Badge variant="violet">Learning Module</Badge>
            </div>
            <h2 className="text-3xl sm:text-5xl font-black mb-2">{skillId}</h2>
          </div>
          {/* Progress switcher */}
          <div className="flex flex-col gap-2 sm:min-w-[200px]">
            <p className="text-indigo-300 font-bold uppercase tracking-widest text-[11px] mb-1">Your Progress</p>
            {statusBtns.map(btn => (
              <button key={btn.key}
                onClick={() => onUpdateProgress(btn.key)}
                className={`flex items-center gap-2 px-4 py-2.5 rounded-xl font-bold text-sm transition-all ${progress === btn.key ? btn.color : 'glass text-white/70 hover:text-white hover:bg-white/10'}`}>
                {btn.icon} {btn.key}
              </button>
            ))}
          </div>
        </div>
      </div>

      {/* Content grid */}
      <div className="grid grid-cols-1 lg:grid-cols-2 gap-6">
        {/* Left: Understand + Connect */}
        <div className="space-y-6">
          {/* Understand */}
          <div className="card-hover glass-light border border-indigo-100 p-7 rounded-3xl shadow-card">
            <div className="flex items-center gap-3 mb-4">
              <div className="w-10 h-10 rounded-xl bg-gradient-to-br from-indigo-500 to-violet-500 flex items-center justify-center">
                <Icon name="brain" className="w-5 h-5 text-white" />
              </div>
              <h3 className="text-lg font-black text-slate-900">Understand the Concept</h3>
            </div>
            <p className="text-slate-600 leading-relaxed text-[15px]">{data.whatIsIt}</p>
          </div>

          {/* Why */}
          <div className="card-hover glass-light border border-violet-100 p-7 rounded-3xl shadow-card">
            <div className="flex items-center gap-3 mb-4">
              <div className="w-10 h-10 rounded-xl bg-gradient-to-br from-violet-500 to-purple-600 flex items-center justify-center">
                <Icon name="target" className="w-5 h-5 text-white" />
              </div>
              <h3 className="text-lg font-black text-slate-900">Why You Need It</h3>
            </div>
            <p className="text-slate-600 leading-relaxed text-[15px]">{data.whyNeeded}</p>
          </div>

          {/* Career Connection */}
          <div className="relative overflow-hidden rounded-3xl p-7 bg-gradient-to-br from-indigo-600 to-violet-600 text-white shadow-glow-indigo">
            <div className="glow-blob w-48 h-48 bg-cyan-400 bottom-[-2rem] right-[-1rem]" />
            <div className="relative z-10">
              <div className="flex items-center gap-3 mb-4">
                <div className="w-10 h-10 rounded-xl bg-white/20 flex items-center justify-center">
                  <Icon name="connect" className="w-5 h-5 text-white" />
                </div>
                <h3 className="text-lg font-black">Connect It to Your Career</h3>
              </div>
              <p className="text-indigo-100 leading-relaxed text-[15px]">{data.careerConnection}</p>
            </div>
          </div>
        </div>

        {/* Right: Apply (task card) */}
        {data.applicationTask && (
          <div className="glass-light border border-indigo-100 p-7 rounded-3xl shadow-card space-y-5">
            <div className="flex items-center gap-3 mb-1">
              <div className="w-10 h-10 rounded-xl bg-gradient-to-br from-cyan-500 to-indigo-500 flex items-center justify-center">
                <Icon name="code" className="w-5 h-5 text-white" />
              </div>
              <h3 className="text-lg font-black text-slate-900">Apply It in Practice</h3>
            </div>

            {/* Task header */}
            <div className="bg-gradient-to-br from-indigo-50 to-violet-50 border border-indigo-100 rounded-2xl p-5">
              <h4 className="font-black text-indigo-800 text-xl mb-3 leading-snug">{data.applicationTask.title}</h4>
              <div className="flex flex-wrap gap-2">
                <span className={`flex items-center gap-1 px-3 py-1 rounded-lg text-xs font-bold ${data.applicationTask.difficulty === 'Beginner' ? 'bg-emerald-100 text-emerald-700' : data.applicationTask.difficulty === 'Advanced' ? 'bg-red-100 text-red-700' : 'bg-amber-100 text-amber-700'}`}>
                  <Icon name="spark" className="w-3 h-3" /> {data.applicationTask.difficulty}
                </span>
                <span className="flex items-center gap-1 px-3 py-1 rounded-lg text-xs font-bold bg-indigo-100 text-indigo-700">
                  <Icon name="clock" className="w-3 h-3" /> {data.applicationTask.estimatedTime}
                </span>
              </div>
            </div>

            {/* Objective */}
            <div>
              <p className="text-xs font-black uppercase tracking-widest text-slate-400 mb-2">Objective</p>
              <p className="text-slate-700 font-medium text-[15px] leading-relaxed">{data.applicationTask.objective}</p>
            </div>

            {/* Steps */}
            <div>
              <p className="text-xs font-black uppercase tracking-widest text-slate-400 mb-3">Execution Steps</p>
              <ol className="space-y-3">
                {data.applicationTask.steps.map((st, i) => (
                  <li key={i} className="flex gap-3 items-start">
                    <span className="w-6 h-6 rounded-lg bg-indigo-600 text-white text-xs font-black flex items-center justify-center shrink-0 mt-0.5">{i + 1}</span>
                    <span className="text-slate-700 text-[14.5px] leading-relaxed">{st}</span>
                  </li>
                ))}
              </ol>
            </div>

            {/* Output */}
            <div className="bg-emerald-50 border border-emerald-200 rounded-2xl p-4">
              <p className="text-xs font-black uppercase tracking-widest text-emerald-600 mb-1.5">Expected Output</p>
              <p className="text-emerald-800 font-semibold text-sm">{data.applicationTask.expectedOutput}</p>
            </div>

            {/* Hint */}
            {data.applicationTask.hint && (
              <div className="bg-amber-50 border border-amber-200 rounded-2xl p-4 flex gap-3">
                <span className="text-xl shrink-0">💡</span>
                <p className="text-amber-800 text-sm font-medium"><strong>Hint:</strong> {data.applicationTask.hint}</p>
              </div>
            )}
          </div>
        )}
      </div>
    </div>
  );
}

// ─── ROADMAP ─────────────────────────────────────────────────────────────────
function Roadmap({ data, progress, onBack }) {
  const uniqueRoadmap = (data.roadmap || []).filter((v, i, a) => a.indexOf(v) === i);

  return (
    <div className="max-w-4xl mx-auto py-8 px-4 space-y-6">
      <button onClick={onBack} className="flex items-center gap-2 text-slate-500 hover:text-indigo-600 font-semibold transition-colors group">
        <Icon name="arrowLeft" className="w-4 h-4 group-hover:-translate-x-1 transition-transform" /> Back to Dashboard
      </button>

      {/* Header */}
      <div className="relative overflow-hidden bg-hero-gradient text-white rounded-3xl p-8 sm:p-10 text-center">
        <div className="glow-blob w-64 h-64 bg-violet-600 top-[-2rem] left-[15%]" />
        <div className="glow-blob w-48 h-48 bg-cyan-500 bottom-[-1rem] right-[15%]" />
        <div className="relative z-10">
          <div className="inline-flex items-center gap-2 glass rounded-full px-4 py-2 text-sm font-bold text-violet-200 mb-4">
            <Icon name="map" className="w-4 h-4" /> Learning Path
          </div>
          <h2 className="text-4xl sm:text-5xl font-black mb-3">Structured Learning Roadmap</h2>
          <p className="text-indigo-200 max-w-xl mx-auto text-lg">
            Follow this prerequisite-based sequence to master <strong className="text-white">{data.targetCareer}</strong>.
          </p>
        </div>
      </div>

      {/* Steps */}
      <div className="relative">
        {/* Vertical line */}
        <div className="absolute left-6 top-0 bottom-0 w-0.5 bg-gradient-to-b from-indigo-500 via-violet-400 to-slate-200 lg:left-1/2" />

        <div className="space-y-6">
          {uniqueRoadmap.map((skill, index) => {
            const status = progress[skill] || 'Not Started';
            const isMissing = data.missingSkills.includes(skill);
            const isActive = status === 'Learning';
            const isDone = status === 'Completed';

            const dotCls = isDone ? 'bg-emerald-500 border-emerald-200' : isActive ? 'bg-indigo-500 border-indigo-200 ring-4 ring-indigo-100' : 'bg-slate-300 border-slate-100';
            const cardCls = isDone ? 'border-emerald-300 bg-emerald-50/50' : isActive ? 'border-indigo-400 shadow-glow-indigo bg-indigo-50/50' : 'border-slate-200 bg-white hover:border-indigo-200';

            return (
              <div key={skill} className={`relative flex gap-6 items-start transition-all duration-500 animate-fade-up`} style={{ animationDelay: `${index * 60}ms` }}>
                {/* Number dot */}
                <div className={`shrink-0 w-12 h-12 rounded-full border-4 ${dotCls} flex items-center justify-center shadow-md z-10 mt-1`}>
                  {isDone
                    ? <Icon name="check" className="w-5 h-5 text-white" />
                    : <span className="text-white font-black text-sm">{index + 1}</span>
                  }
                </div>

                {/* Card */}
                <div className={`flex-1 border-2 ${cardCls} p-6 rounded-2xl transition-all duration-300 card-hover`}>
                  <div className="flex flex-wrap items-center justify-between gap-3 mb-3">
                    <h3 className="font-black text-slate-900 text-xl">{skill}</h3>
                    <div className="flex items-center gap-2">
                      {isDone && <Badge variant="done">✓ Completed</Badge>}
                      {isActive && <Badge variant="learning">⏳ Active</Badge>}
                      {!isDone && !isActive && <Badge variant="default">Pending</Badge>}
                      {!isMissing && <Badge variant="green">Known</Badge>}
                    </div>
                  </div>
                  <p className="text-slate-500 text-sm mb-4">
                    {isMissing ? 'Priority gap — work through the learning module to build this skill.' : 'You have foundational experience. Revisiting will strengthen your understanding.'}
                  </p>
                  {/* Progress bar */}
                  <div className="h-2 bg-slate-100 rounded-full overflow-hidden">
                    <div className={`h-full rounded-full progress-fill ${isDone ? 'w-full bg-emerald-500' : isActive ? 'w-1/2 bg-gradient-to-r from-indigo-500 to-violet-500' : 'w-0'}`} />
                  </div>
                </div>
              </div>
            );
          })}
        </div>
      </div>
    </div>
  );
}

// ─── ROOT APP ────────────────────────────────────────────────────────────────
export default function App() {
  const [currentView, setCurrentView] = useState('landing');
  const [profile, setProfile] = useState({ targetCareer: 'ML Engineer', experienceLevel: 'Beginner', currentSkills: [] });
  const [analysisData, setAnalysisData] = useState(null);
  const [selectedSkill, setSelectedSkill] = useState(null);
  const [loading, setLoading] = useState(false);

  const getInitialProgress = () => {
    try { return JSON.parse(localStorage.getItem('learningProgress') || '{}'); }
    catch { return {}; }
  };
  const [progress, setProgress] = useState(getInitialProgress);

  useEffect(() => {
    localStorage.setItem('learningProgress', JSON.stringify(progress));
  }, [progress]);

  const updateProgress = (skill, status) =>
    setProgress(prev => ({ ...prev, [skill]: status }));

  const handleAnalyze = async (data) => {
    setProfile(data);
    setLoading(true);
    try {
      const result = await analyzeSkills(data.targetCareer, data.currentSkills, data.experienceLevel);
      setAnalysisData({ ...result, targetCareer: data.targetCareer });
      setCurrentView('dashboard');
    } catch (e) {
      console.error(e);
      alert('Failed to analyze skills. Is the backend running?');
    } finally {
      setLoading(false);
    }
  };

  const navItems = analysisData ? [
    { key: 'profile', label: 'Profile' },
    { key: 'dashboard', label: 'Dashboard' },
    { key: 'roadmap', label: '🗺️ Roadmap' },
  ] : [];

  return (
    <div className="min-h-screen bg-surfaceAlt font-sans">
      {/* Navbar */}
      <nav className="sticky top-0 z-40 bg-white/80 backdrop-blur-xl border-b border-indigo-100 shadow-sm">
        <div className="max-w-7xl mx-auto px-6 py-3 flex items-center justify-between">
          <button onClick={() => setCurrentView('landing')} className="flex items-center gap-2.5 group">
            <div className="w-9 h-9 rounded-xl bg-brand-gradient flex items-center justify-center shadow-glow-indigo group-hover:shadow-glow-violet transition-all">
              <span className="text-white font-black text-lg">C</span>
            </div>
            <span className="hidden sm:block font-black text-slate-900 text-lg tracking-tight">
              CareerLearn <span className="text-indigo-400 font-medium">AI</span>
            </span>
          </button>

          {navItems.length > 0 && (
            <div className="flex items-center gap-1">
              {navItems.map(n => (
                <button key={n.key} onClick={() => setCurrentView(n.key)}
                  className={`px-4 py-2 rounded-xl font-bold text-sm transition-all ${currentView === n.key ? 'nav-active' : 'text-slate-500 hover:text-indigo-600 hover:bg-indigo-50'}`}>
                  {n.label}
                </button>
              ))}
              <button onClick={() => setCurrentView('profile')}
                className="ml-2 px-5 py-2 bg-brand-gradient text-white font-bold text-sm rounded-xl shadow-glow-indigo hover:shadow-glow-violet transition-all">
                New Analysis
              </button>
            </div>
          )}
        </div>
      </nav>

      {/* Loading overlay */}
      {loading && (
        <div className="fixed inset-0 z-50 flex flex-col items-center justify-center bg-slate-900/40 backdrop-blur-sm">
          <div className="bg-white rounded-3xl p-10 shadow-2xl flex flex-col items-center gap-5">
            <div className="relative w-16 h-16">
              <div className="absolute inset-0 rounded-full border-4 border-indigo-100" />
              <div className="absolute inset-0 rounded-full border-4 border-t-indigo-600 animate-spin" />
            </div>
            <div className="text-center">
              <p className="font-black text-slate-900 text-lg">Analyzing your skills…</p>
              <p className="text-slate-400 text-sm mt-1">AI is mapping your learning path</p>
            </div>
          </div>
        </div>
      )}

      <main>
        {currentView === 'landing' && <Landing onStart={() => setCurrentView('profile')} />}
        {currentView === 'profile' && <ProfileForm initialProfile={profile} onAnalyze={handleAnalyze} />}
        {currentView === 'dashboard' && analysisData && (
          <Dashboard
            data={analysisData}
            onSelectSkill={skill => { setSelectedSkill(skill); setCurrentView('skillDetail'); }}
            progress={progress}
            onBack={() => setCurrentView('profile')}
            showRoadmap={() => setCurrentView('roadmap')}
          />
        )}
        {currentView === 'skillDetail' && selectedSkill && (
          <SkillDetail
            skillId={selectedSkill}
            data={analysisData.skillExplanations.find(s => s.skill === selectedSkill) || { whatIsIt: 'Content coming soon.', whyNeeded: 'Content coming soon.', careerConnection: 'Content coming soon.', applicationTask: null }}
            onBack={() => setCurrentView('dashboard')}
            progress={progress[selectedSkill] || 'Not Started'}
            onUpdateProgress={status => updateProgress(selectedSkill, status)}
          />
        )}
        {currentView === 'roadmap' && analysisData && (
          <Roadmap data={analysisData} progress={progress} onBack={() => setCurrentView('dashboard')} />
        )}
      </main>

      {/* Footer */}
      {currentView === 'landing' && (
        <footer className="bg-hero-gradient text-indigo-300 text-center py-8 text-sm">
          <p className="font-semibold">CareerLearn AI · Built for ForgeHacks 2026 · AI + Education Track</p>
        </footer>
      )}
    </div>
  );
}
