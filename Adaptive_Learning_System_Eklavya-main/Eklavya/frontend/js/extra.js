/* LearnWe extras: class select, study planner, notifications, achievements. Loads after app.js */
const PLAN = () => JSON.parse(localStorage.getItem("plan") || "[]");
const classSelect = () => show(`<h1 style="margin-top:30px">${tr("Which class are you in?")}</h1>${[6, 7, 8, 9, 10].map(n => `<button class="opt" onclick="setGrade(${n})">Class ${n}</button>`).join("")}`);
const setGrade = n => { localStorage.setItem("grade", n); home(); };
const planner = () => {
  const L = PLAN().map((p, i) => `<div class="card"><span>📚</span><div class="grow"><b>${esc(p.s)}</b><small>${esc(p.t)} ${p.m ? "· " + esc(p.m) : ""}</small></div><button onclick="delPlan(${i})" aria-label="Remove" style="border:0;background:none;font-size:18px;cursor:pointer">✕</button></div>`).join("");
  withNav(`${hd(tr("Study planner"), "home()")}
  ${[["🎯", "ps", "Targeted subjects, e.g. Chemistry"], ["📝", "pt", "Topic, e.g. Cell division"], ["⏱️", "pm", "Time, e.g. 2h 45m"]].map(([i, id, ph]) => `<div class="card"><span style="font-size:24px">${i}</span><input id="${id}" placeholder="${ph}" style="margin:0"></div>`).join("")}
  <button class="btn alt" onclick="savePlan()">+ ${tr("Save topic")}</button><button class="btn" onclick="learnPath()">${tr("Learning Path")} ›</button>${L ? `<h2>${tr("Today's plan")}</h2>${L}` : ""}`, "home");
};
const savePlan = () => { const v = id => document.getElementById(id).value.trim(); if (!v("ps")) return toast("Add a subject"); localStorage.setItem("plan", JSON.stringify([...PLAN(), { s: v("ps"), t: v("pt"), m: v("pm") }])); planner(); };
const delPlan = i => { const p = PLAN(); p.splice(i, 1); localStorage.setItem("plan", JSON.stringify(p)); planner(); };
const notifications = guard(async () => {
  let items;
  if (S.user.role === "teacher") {
    const d = await api(`/api/classes/${S.tc.id}/dashboard`);
    items = [["bell", "Class overview", `${d.student_count} students in ${S.tc.name}`], ...d.class_weak_topics.map(t => ["bellnew", "Needs attention", t.topic])];
  } else {
    const [pg, { recommendations: r }] = await Promise.all([api("/api/progress?limit=1"), api("/api/recommendations")]);
    items = [["bell", "Daily reminder", `${Math.min(pg.answers_today, pg.daily_goal)}/${pg.daily_goal} questions done today`], ["chart", "Your progress", pg.streak_days ? `${pg.streak_days} day streak. Keep it up!` : "Answer a few questions to start a streak"],
      ...(r[0] ? [["lesson", "New lesson available", r[0].topic]] : [])];
  }
  withNav(`${hd(tr("Notifications"), "home()")}${items.map(([i, t, b]) => `<div class="card"><img src="${img(i)}" alt=""><div class="grow"><b>${esc(t)}</b><small>${esc(b)}</small></div></div>`).join("")}`, "home");
});
const badges = p => {
  const a = p.overall.attempts || 0, acc = p.overall.accuracy || 0, ds = p.streak_days || 0;
  return `<div class="quick" style="grid-template-columns:repeat(4,1fr)">${[["🌱", "First steps", a >= 1], ["🔟", "10 answers", a >= 10], ["🎯", "80% accuracy", a >= 10 && acc >= .8], ["🔥", "3-day streak", ds >= 3]].map(([i, n, ok]) => `<div class="badge${ok ? " got" : ""}"><span>${i}</span><small>${n}</small></div>`).join("")}</div>`;
};
