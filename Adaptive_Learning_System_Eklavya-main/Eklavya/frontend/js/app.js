/* Extra UI languages. Missing keys fall back to English. */
const K = "Home|Progress|Profile|Practice|Test|Continue Learning|Class materials|Today's plan|Submit|Next|Back to Home|View Next Lesson|Learning Path|Log out|Hello|Day streak|Language|Profile & Settings|Welcome back!|Log in|Sign up|Get Started|Well done!|Keep going!".split("|");
const PACK = {
  ta: "முகப்பு|முன்னேற்றம்|சுயவிவரம்|பயிற்சி|தேர்வு|கற்றலைத் தொடரவும்|வகுப்புப் பொருட்கள்|இன்றைய திட்டம்|சமர்ப்பி|அடுத்து|முகப்புக்குத் திரும்பு|அடுத்த பாடம் பார்|கற்றல் பாதை|வெளியேறு|வணக்கம்|தொடர் நாட்கள்|மொழி|சுயவிவரமும் அமைப்புகளும்|மீண்டும் வருக!|உள்நுழை|பதிவு செய்|தொடங்குங்கள்|அருமை!|தொடர்ந்து முயலுங்கள்!",
  te: "హోమ్|ప్రగతి|ప్రొఫైల్|అభ్యాసం|పరీక్ష|నేర్చుకోవడం కొనసాగించు|తరగతి సామగ్రి|నేటి ప్రణాళిక|సమర్పించు|తదుపరి|హోమ్‌కు తిరిగి వెళ్ళు|తదుపరి పాఠం చూడండి|అభ్యాస మార్గం|లాగ్ అవుట్|నమస్తే|వరుస రోజులు|భాష|ప్రొఫైల్ & సెట్టింగ్‌లు|తిరిగి స్వాగతం!|లాగిన్|సైన్ అప్|ప్రారంభించండి|శెభాష్!|ప్రయత్నిస్తూ ఉండండి!",
  mr: "मुख्यपृष्ठ|प्रगती|प्रोफाइल|सराव|चाचणी|शिकणे सुरू ठेवा|वर्ग साहित्य|आजची योजना|सादर करा|पुढे|मुख्यपृष्ठावर परत|पुढचा धडा पहा|शिकण्याचा मार्ग|बाहेर पडा|नमस्कार|सलग दिवस|भाषा|प्रोफाइल आणि सेटिंग्ज|पुन्हा स्वागत!|लॉग इन|साइन अप|सुरू करा|शाब्बास!|प्रयत्न करत राहा!",
  gu: "હોમ|પ્રગતિ|પ્રોફાઇલ|અભ્યાસ|કસોટી|શીખવાનું ચાલુ રાખો|વર્ગ સામગ્રી|આજની યોજના|સબમિટ કરો|આગળ|હોમ પર પાછા જાઓ|આગળનો પાઠ જુઓ|શીખવાનો માર્ગ|લૉગ આઉટ|નમસ્તે|સતત દિવસો|ભાષા|પ્રોફાઇલ અને સેટિંગ્સ|ફરી સ્વાગત છે!|લૉગ ઇન|સાઇન અપ|શરૂ કરો|શાબાશ!|પ્રયત્ન ચાલુ રાખો!",
  kn: "ಮುಖಪುಟ|ಪ್ರಗತಿ|ಪ್ರೊಫೈಲ್|ಅಭ್ಯಾಸ|ಪರೀಕ್ಷೆ|ಕಲಿಕೆ ಮುಂದುವರಿಸಿ|ತರಗತಿ ಸಾಮಗ್ರಿ|ಇಂದಿನ ಯೋಜನೆ|ಸಲ್ಲಿಸಿ|ಮುಂದೆ|ಮುಖಪುಟಕ್ಕೆ ಹಿಂತಿರುಗಿ|ಮುಂದಿನ ಪಾಠ ನೋಡಿ|ಕಲಿಕೆಯ ಹಾದಿ|ಲಾಗ್ ಔಟ್|ನಮಸ್ಕಾರ|ನಿರಂತರ ದಿನಗಳು|ಭಾಷೆ|ಪ್ರೊಫೈಲ್ ಮತ್ತು ಸೆಟ್ಟಿಂಗ್‌ಗಳು|ಮತ್ತೆ ಸ್ವಾಗತ!|ಲಾಗ್ ಇನ್|ಸೈನ್ ಅಪ್|ಪ್ರಾರಂಭಿಸಿ|ಶಹಬ್ಬಾಸ್!|ಪ್ರಯತ್ನ ಮುಂದುವರಿಸಿ!",
  ml: "ഹോം|പുരോഗതി|പ്രൊഫൈൽ|പരിശീലനം|പരീക്ഷ|പഠനം തുടരുക|ക്ലാസ് സാമഗ്രികൾ|ഇന്നത്തെ പദ്ധതി|സമർപ്പിക്കുക|അടുത്തത്|ഹോമിലേക്ക് മടങ്ങുക|അടുത്ത പാഠം കാണുക|പഠന പാത|ലോഗ് ഔട്ട്|നമസ്കാരം|തുടർച്ചയായ ദിവസങ്ങൾ|ഭാഷ|പ്രൊഫൈലും ക്രമീകരണങ്ങളും|വീണ്ടും സ്വാഗതം!|ലോഗിൻ|സൈൻ അപ്പ്|തുടങ്ങാം|കൊള്ളാം!|ശ്രമം തുടരൂ!",
  pa: "ਹੋਮ|ਤਰੱਕੀ|ਪ੍ਰੋਫਾਈਲ|ਅਭਿਆਸ|ਪ੍ਰੀਖਿਆ|ਪੜ੍ਹਾਈ ਜਾਰੀ ਰੱਖੋ|ਜਮਾਤ ਸਮੱਗਰੀ|ਅੱਜ ਦੀ ਯੋਜਨਾ|ਜਮ੍ਹਾਂ ਕਰੋ|ਅਗਲਾ|ਹੋਮ ਤੇ ਵਾਪਸ|ਅਗਲਾ ਪਾਠ ਵੇਖੋ|ਸਿੱਖਣ ਦਾ ਰਾਹ|ਲੌਗ ਆਊਟ|ਸਤ ਸ੍ਰੀ ਅਕਾਲ|ਲਗਾਤਾਰ ਦਿਨ|ਭਾਸ਼ਾ|ਪ੍ਰੋਫਾਈਲ ਅਤੇ ਸੈਟਿੰਗਾਂ|ਜੀ ਆਇਆਂ ਨੂੰ!|ਲੌਗ ਇਨ|ਸਾਈਨ ਅੱਪ|ਸ਼ੁਰੂ ਕਰੋ|ਸ਼ਾਬਾਸ਼!|ਕੋਸ਼ਿਸ਼ ਜਾਰੀ ਰੱਖੋ!",
  ur: "ہوم|پیش رفت|پروفائل|مشق|امتحان|سیکھنا جاری رکھیں|کلاس کا مواد|آج کا منصوبہ|جمع کریں|اگلا|ہوم پر واپس|اگلا سبق دیکھیں|سیکھنے کا راستہ|لاگ آؤٹ|السلام علیکم|مسلسل دن|زبان|پروفائل اور سیٹنگز|خوش آمدید!|لاگ اِن|سائن اَپ|شروع کریں|شاباش!|کوشش جاری رکھیں!",
  or: "ହୋମ|ଅଗ୍ରଗତି|ପ୍ରୋଫାଇଲ|ଅଭ୍ୟାସ|ପରୀକ୍ଷା|ଶିକ୍ଷା ଜାରି ରଖ|ଶ୍ରେଣୀ ସାମଗ୍ରୀ|ଆଜିର ଯୋଜନା|ଦାଖଲ କର|ପରବର୍ତ୍ତୀ|ହୋମକୁ ଫେର|ପରବର୍ତ୍ତୀ ପାଠ ଦେଖ|ଶିଖିବା ପଥ|ଲଗ୍ ଆଉଟ୍|ନମସ୍କାର|ଲଗାତାର ଦିନ|ଭାଷା|ପ୍ରୋଫାଇଲ ଓ ସେଟିଂସ୍|ପୁନଃ ସ୍ୱାଗତ!|ଲଗ୍ ଇନ୍|ସାଇନ୍ ଅପ୍|ଆରମ୍ଭ କର|ବାହ୍!|ଚେଷ୍ଟା ଜାରି ରଖ!",
  as: "হোম|অগ্ৰগতি|প্ৰফাইল|অনুশীলন|পৰীক্ষা|শিকা অব্যাহত ৰাখক|শ্ৰেণীৰ সমল|আজিৰ পৰিকল্পনা|জমা দিয়ক|পৰৱৰ্তী|হোমলৈ উভতি যাওক|পৰৱৰ্তী পাঠ চাওক|শিকাৰ পথ|লগ আউট|নমস্কাৰ|ক্ৰমাগত দিন|ভাষা|প্ৰফাইল আৰু ছেটিংছ|পুনৰ স্বাগতম!|লগ ইন|ছাইন আপ|আৰম্ভ কৰক|বাহ!|চেষ্টা অব্যাহত ৰাখক!"
};
const EXTRA = {};
for (const c in PACK) { const v = PACK[c].split("|"); EXTRA[c] = Object.fromEntries(K.map((k, i) => [k, v[i]])); }
const K2 = ["Notifications", "Study planner", "Achievements", "Which class are you in?", "Save topic"];
const PACK2 = {
  hi: "सूचनाएँ|अध्ययन योजनाकार|उपलब्धियाँ|आप किस कक्षा में हैं?|विषय सहेजें",
  bn: "বিজ্ঞপ্তি|পড়ার পরিকল্পনা|অর্জন|তুমি কোন ক্লাসে পড়ো?|বিষয় সংরক্ষণ করো",
  ta: "அறிவிப்புகள்|படிப்புத் திட்டம்|சாதனைகள்|நீங்கள் எந்த வகுப்பில் படிக்கிறீர்கள்?|தலைப்பைச் சேமி",
  te: "నోటిఫికేషన్లు|అధ్యయన ప్రణాళిక|విజయాలు|మీరు ఏ తరగతిలో ఉన్నారు?|అంశాన్ని సేవ్ చేయి",
  mr: "सूचना|अभ्यास नियोजक|यश|तुम्ही कोणत्या वर्गात आहात?|विषय जतन करा",
  gu: "સૂચનાઓ|અભ્યાસ આયોજક|સિદ્ધિઓ|તમે કયા ધોરણમાં છો?|વિષય સાચવો",
  kn: "ಅಧಿಸೂಚನೆಗಳು|ಅಧ್ಯಯನ ಯೋಜನೆ|ಸಾಧನೆಗಳು|ನೀವು ಯಾವ ತರಗತಿಯಲ್ಲಿದ್ದೀರಿ?|ವಿಷಯ ಉಳಿಸಿ",
  ml: "അറിയിപ്പുകൾ|പഠന പ്ലാനർ|നേട്ടങ്ങൾ|നിങ്ങൾ ഏത് ക്ലാസിലാണ്?|വിഷയം സേവ് ചെയ്യുക",
  pa: "ਸੂਚਨਾਵਾਂ|ਪੜ੍ਹਾਈ ਯੋਜਨਾਕਾਰ|ਪ੍ਰਾਪਤੀਆਂ|ਤੁਸੀਂ ਕਿਹੜੀ ਜਮਾਤ ਵਿੱਚ ਹੋ?|ਵਿਸ਼ਾ ਸੁਰੱਖਿਅਤ ਕਰੋ",
  ur: "اطلاعات|مطالعہ کا منصوبہ|کامیابیاں|آپ کس جماعت میں ہیں؟|موضوع محفوظ کریں",
  or: "ବିଜ୍ଞପ୍ତି|ଅଧ୍ୟୟନ ଯୋଜନା|ସଫଳତା|ତୁମେ କେଉଁ ଶ୍ରେଣୀରେ ଅଛ?|ବିଷୟ ସଂରକ୍ଷଣ କର",
  as: "জাননী|অধ্যয়ন পৰিকল্পনা|কৃতিত্ব|আপুনি কোনটো শ্ৰেণীত আছে?|বিষয় সংৰক্ষণ কৰক"
};
for (const c in PACK2) { const v = PACK2[c].split("|"); EXTRA[c] = { ...EXTRA[c], ...Object.fromEntries(K2.map((k, i) => [k, v[i]])) }; }
const LANG_NAMES = [["en", "English"], ["hi", "हिन्दी"], ["bn", "বাংলা"], ["ta", "தமிழ்"], ["te", "తెలుగు"], ["mr", "मराठी"], ["gu", "ગુજરાતી"], ["kn", "ಕನ್ನಡ"], ["ml", "മലയാളം"], ["pa", "ਪੰਜਾਬੀ"], ["ur", "اردو"], ["or", "ଓଡ଼ିଆ"], ["as", "অসমীয়া"]];

/* LearnWe frontend - plain JS, talks to the Python backend (backend/server.py) */
const API = localStorage.getItem("api") || "http://127.0.0.1:8000";
const S = { token: localStorage.getItem("token"), user: null, role: "student", signup: false };
const $app = document.getElementById("app");
const esc = s => String(s ?? "").replace(/[&<>"]/g, c => ({ "&": "&amp;", "<": "&lt;", ">": "&gt;", '"': "&quot;" }[c]));
const img = n => `assets/${n}.jpg`;
const COLORS = { Maths: "var(--c0)", Science: "var(--c1)", English: "var(--c2)", "Social Science": "var(--c3)" };
const ICONS = { Maths: "maths", Science: "science", English: "english", "Social Science": "social" };
const col = (s, i = 0) => COLORS[s] || `var(--c${i % 5})`;

async function api(path, method = "GET", body) {
  let res;
  try {
    res = await fetch(API + path, { method, headers: { "Content-Type": "application/json", ...(S.token ? { Authorization: "Bearer " + S.token } : {}) }, body: body ? JSON.stringify(body) : undefined });
  } catch { throw new Error("Cannot reach the server. Is backend/server.py running?"); }
  const data = await res.json().catch(() => ({}));
  if (res.status === 401 && S.token) { logout(); }
  if (!res.ok) throw new Error(data.error || "Something went wrong");
  return data;
}

function show(html, back) {
  $app.innerHTML = `<div class="screen${back ? " back" : ""}">${html}</div>`;
  requestAnimationFrame(() => requestAnimationFrame(() => {   // animate bars and rings after paint
    $app.querySelectorAll(".bar i").forEach(b => b.style.width = b.dataset.w + "%");
    $app.querySelectorAll(".ring").forEach(r => { const t = +r.dataset.p, n = r.querySelector("i"); let v = 0;
      const step = () => { v = Math.min(t, v + Math.max(1, t / 30)); r.style.setProperty("--p", v); n.textContent = Math.round(v) + "%"; if (v < t) requestAnimationFrame(step); }; step(); });
  }));
  window.scrollTo(0, 0);
}
function toast(m) { const t = document.createElement("div"); t.className = "toast"; t.textContent = m; document.body.append(t); setTimeout(() => t.remove(), 2200); }
function confetti() { const d = document.createElement("div"); d.className = "stars"; d.innerHTML = Array.from({ length: 18 }, () => `<i style="left:${Math.random() * 100}%;animation-delay:${Math.random()}s">${["⭐", "✨", "🎉"][Math.floor(Math.random() * 3)]}</i>`).join(""); $app.append(d); setTimeout(() => d.remove(), 3800); }
const hd = (title, back) => `<div class="top"><button onclick="${back}" aria-label="Back">←</button>${esc(title)}</div>`;
const bar = (label, pct, c) => `<div class="row"><span>${esc(label)}</span><b>${pct}%</b></div><div class="bar"><i data-w="${pct}" style="background:${c}"></i></div>`;
const pct = x => Math.round((x || 0) * 100);
const IC = {
  home: '<svg viewBox="0 0 24 24"><path d="M3 11l9-8 9 8v9a1 1 0 0 1-1 1h-5v-6H9v6H4a1 1 0 0 1-1-1z"/></svg>',
  progress: '<svg viewBox="0 0 24 24"><path d="M2 5h7a3 3 0 0 1 3 3v12a2 2 0 0 0-2-2H2zM22 5h-7a3 3 0 0 0-3 3v12a2 2 0 0 1 2-2h8z"/></svg>',
  profile: '<svg viewBox="0 0 24 24"><circle cx="12" cy="8" r="4"/><path d="M4 21a8 8 0 0 1 16 0"/></svg>' };
function nav(on) {
  const tabs = S.user.role === "student" ? [["Home", IC.home, "home"], ["Progress", IC.progress, "progress"], ["Profile", IC.profile, "profile"]] : [["Home", IC.home, "home"], ["Profile", IC.profile, "profile"]];
  return `<div class="nav">${tabs.map(t => `<button class="${t[2] === on ? "on" : ""}" onclick="${t[2]}()"><span>${t[1]}</span>${tr(t[0])}</button>`).join("")}</div>`;
}
function withNav(html, on) { show(html); $app.insertAdjacentHTML("beforeend", nav(on)); }
function logout() { localStorage.removeItem("token"); S.token = null; S.user = null; auth(); }
const guard = fn => async (...a) => { try { await fn(...a); } catch (e) { toast(e.message); } };

/* ---------- language (English, Hindi, Bengali) ---------- */
const I18N = {
  hi: { Home: "होम", Progress: "प्रगति", Profile: "प्रोफ़ाइल", Practice: "अभ्यास", Test: "परीक्षा", "Continue Learning": "पढ़ाई जारी रखें", "Class materials": "कक्षा सामग्री", "Today's plan": "आज की योजना", Submit: "जमा करें", Next: "अगला", "Back to Home": "होम पर वापस", "View Next Lesson": "अगला पाठ देखें", "Learning Path": "सीखने का रास्ता", "Log out": "लॉग आउट", Hello: "नमस्ते", "Day streak": "दिन लगातार", Language: "भाषा", "Profile & Settings": "प्रोफ़ाइल और सेटिंग", "Delete my account and data": "मेरा खाता और डेटा हटाएँ", "questions today": "आज के प्रश्न" },
  bn: { Home: "হোম", Progress: "অগ্রগতি", Profile: "প্রোফাইল", Practice: "অনুশীলন", Test: "পরীক্ষা", "Continue Learning": "পড়া চালিয়ে যাও", "Class materials": "ক্লাসের উপকরণ", "Today's plan": "আজকের পরিকল্পনা", Submit: "জমা দাও", Next: "পরবর্তী", "Back to Home": "হোমে ফিরে যাও", "View Next Lesson": "পরের পাঠ দেখো", "Learning Path": "শেখার পথ", "Log out": "লগ আউট", Hello: "নমস্কার", "Day streak": "দিন টানা", Language: "ভাষা", "Profile & Settings": "প্রোফাইল ও সেটিংস", "Delete my account and data": "আমার অ্যাকাউন্ট ও ডেটা মুছুন", "questions today": "আজকের প্রশ্ন" }
};
for (const c in EXTRA) I18N[c] = { ...I18N[c], ...EXTRA[c] };
const lang = () => localStorage.getItem("lang") || (S.user && S.user.language) || "en";
const tr = k => (I18N[lang()] || {})[k] || k;
document.documentElement.lang = lang(); document.documentElement.dir = lang() === "ur" ? "rtl" : "ltr";
const setLang = async l => { localStorage.setItem("lang", l); document.documentElement.lang = l; document.documentElement.dir = l === "ur" ? "rtl" : "ltr"; S.user.language = l; profile();
  try { await api("/api/me/language", "PUT", { language: l }); } catch { /* backend may not list this language yet; choice is kept on this device */ } };
const deleteMe = guard(async () => {
  if (!confirm("This permanently deletes your account and all your learning data. Continue?")) return;
  await api("/api/me", "DELETE"); logout();
});

/* ---------- splash + auth ---------- */
function splash() {
  show(`<div class="splash"><div class="sbg"></div><img class="art" src="assets/splash.jpg" alt="LearnWe - Learn at Your Own Pace"><i class="sp s1">✦</i><i class="sp s2">✦</i><i class="sp s3">✦</i><i class="sp s4">✦</i>
  <button class="btn go" onclick="auth()">${tr("Get Started")}</button></div>`);
}
function auth() {
  const r = S.role, su = S.signup, f = (id, ic, ph, type = "text") => `<div class="field"><span>${ic}</span><input id="${id}" type="${type}" placeholder="${ph}">${type === "password" ? `<button type="button" class="eye" aria-label="Show password" onclick="const i=document.getElementById('${id}');i.type=i.type==='password'?'text':'password'">👁</button>` : ""}</div>`;
  show(`${hd("", "splash()")}<h1 class="wb">${su ? "Create your account" : tr("Welcome back!")}</h1><p class="sub">${su ? "Sign up to start learning" : "Sign in to continue your learning journey"}</p>
  <div class="tabs">${["student", "teacher", "parent"].map(x => `<button class="${r === x ? "on" : ""}" onclick="S.role='${x}';auth()">${x[0].toUpperCase() + x.slice(1)}</button>`).join("")}</div>
  ${su ? f("name", "👤", "Full name") : ""}${f("email", "✉️", "Email", "email")}${f("pw", "🔒", "Password (6+ characters)", "password")}
  ${su && r === "student" ? f("parent", "👪", "Parent's email (only they can see your progress)", "email") : ""}
  ${su ? "" : `<a href="#" class="forgot" onclick="toast('Ask your teacher to reset your password');return false">Forgot password?</a>`}
  <div class="err" id="err"></div><button class="btn" onclick="submitAuth()">${tr(su ? "Sign up" : "Log in")}</button>
  <div class="or"><span>or</span></div><button class="btn grey" onclick="S.signup=${!su};auth()">${su ? "Back to " + tr("Log in") : "Create New Account"}</button>
  <p class="sub center" style="margin-top:16px">${su ? "Already have an account?" : "Don't have an account?"} <a href="#" onclick="S.signup=${!su};auth();return false" style="color:var(--blue);font-weight:600">${su ? tr("Log in") : tr("Sign up")}</a></p>`, true);
}
async function submitAuth() {
  const v = id => document.getElementById(id)?.value.trim();
  try {
    const body = { email: v("email"), password: v("pw") };
    if (S.signup) Object.assign(body, { name: v("name"), role: S.role, parent_email: v("parent") });
    const d = await api(S.signup ? "/api/register" : "/api/login", "POST", body);
    if (!S.signup && d.user.role !== S.role) throw new Error(`This account is a ${d.user.role}. Pick the ${d.user.role} tab.`);
    S.token = d.token; S.user = d.user; localStorage.setItem("token", d.token); S.signup && d.user.role === "student" ? classSelect() : home();
  } catch (e) { document.getElementById("err").textContent = e.message; }
}

/* ---------- routing by role ---------- */
const home = guard(async () => { S.user.role === "teacher" ? await teacherHome() : S.user.role === "parent" ? await parentHome() : await studentHome(); });
const profile = () => withNav(`<h1>${tr("Profile & Settings")}</h1><div class="card"><img src="${img(S.user.role === "teacher" ? "boy4" : "girl1")}" alt=""><div class="grow"><b>${esc(S.user.name)}</b><small>${esc(S.user.email)} · ${S.user.role}</small></div></div>
  <h2>${tr("Language")}</h2><div class="langs">${LANG_NAMES.map(([c, n]) => `<button class="${lang() === c ? "on" : ""}" onclick="setLang('${c}')">${n}</button>`).join("")}</div>
  <div class="card" onclick="notifications()" style="cursor:pointer"><div class="grow"><b>${tr("Notifications")}</b></div>›</div><button class="btn alt" style="color:var(--bad);border-color:var(--bad)" onclick="logout()">${tr("Log out")}</button>
  ${S.user.role !== "teacher" ? `<button class="btn alt" style="color:var(--bad);border-color:var(--bad)" onclick="deleteMe()">${tr("Delete my account and data")}</button><p class="sub">Your data is visible only to you, your teacher and the parent email you gave.</p>` : ""}`, "profile");

/* ---------- student ---------- */
async function studentHome() {
  const classes = await api("/api/classes");
  if (!classes.length) {
    withNav(`<h1>Hello, ${esc(S.user.name)} 👋</h1><p class="sub">Ask your teacher for a class code to begin.</p><input id="code" placeholder="Class code, e.g. DEMO01" style="text-transform:uppercase"><button class="btn" onclick="joinClass()">Join class</button>`, "home"); return;
  }
  S.cls = classes[0];
  const { recommendations: recs } = await api("/api/recommendations");
  const pg = await api("/api/progress?limit=1");
  const plan = recs[0];
  withNav(`<div class="hdr"><div><h1>${tr("Hello")}, ${esc(S.user.name)} 👋</h1><p class="sub">${esc(S.cls.name)}</p></div><img src="${img("bell")}" width="38" alt="Notifications" onclick="notifications()" style="cursor:pointer"></div>
  <div class="banner">${pg.streak_days ? "🔥 " + pg.streak_days + " " + tr("Day streak") : "Your learning journey"}<br><small>${Math.min(pg.answers_today, pg.daily_goal)}/${pg.daily_goal} ${tr("questions today")} · no pressure, just a little each day</small><div class="bar" style="background:#fff8;margin:8px 0 0"><i data-w="${Math.min(100, pg.answers_today / pg.daily_goal * 100)}" style="background:var(--blue)"></i></div></div>
  <div class="quick"><div onclick="learnPath()"><img src="${img("lesson")}" alt="">${tr("Continue Learning")}</div><div onclick="${plan ? `practice(${plan.topic_id})` : "learnPath()"}"><img src="${img("tasks")}" alt="">${tr("Practice")}</div><div onclick="takeTest()"><img src="${img("chart")}" alt="">${tr("Test")}</div></div>
  <div class="card" onclick="materials()" style="cursor:pointer"><div class="grow"><b>${tr("Class materials")}</b><small>Videos, notes, practice and tests from your teacher</small></div>›</div><div class="card" onclick="planner()" style="cursor:pointer"><div class="grow"><b>${tr("Study planner")}</b><small>Subject, topic and time</small></div>›</div><h2>${tr("Today's plan")}</h2>${plan ? `<div class="card" onclick="lesson(${plan.topic_id})" style="cursor:pointer"><div class="grow"><b>${esc(plan.topic)}</b><small>${esc(plan.reason)}</small></div>›</div>` : `<p class="sub">Nothing yet. Open Continue Learning.</p>`}`, "home");
}
const joinClass = guard(async () => { await api("/api/classes/join", "POST", { code: document.getElementById("code").value }); home(); });
const LABEL = { learn: "Not started", revise: "Needs revision", practice: "Needs more practice", test: "Doing well" };
const learnPath = guard(async () => {
  const { recommendations: r } = await api("/api/recommendations");
  withNav(`${hd(tr("Learning Path"), "home()")}${r.length ? r.map((x, i) => `<div class="pill" onclick="lesson(${x.topic_id})" style="background:color-mix(in srgb,${col(x.subject, i)} 18%,white)"><span>${esc(x.topic)}<small>${esc(x.subject)} · ${LABEL[x.action]}</small></span>›</div>`).join("") : `<p class="sub">No topics yet. Join a class first.</p>`}
  <div class="note">Based on your performance. This is your personalised path.</div>`, "home");
});
const lesson = guard(async (tid, tab) => {
  const l = await api(`/api/topics/${tid}/lesson`);
  show(`${hd(l.title, "learnPath()")}<h2>${esc(l.topic)}</h2><div class="tabs"><button class="on">Learn</button><button onclick="practice(${tid})">Solve</button><button onclick="takeTest()">Test</button></div>
  <div class="note"><b>Key concept</b><br>${esc(l.content).replace(/\n/g, "<br>")}</div>${l.available_languages.length > 1 ? `<p class="sub">Also in: ${l.available_languages.join(", ")}</p>` : ""}
  <button class="btn" onclick="practice(${tid})">Next</button>`);
});
let P = null;
const practice = guard(async (tid) => { P = P && P.tid === tid ? P : { tid, n: 0, ok: 0 }; await nextQ(); });
async function nextQ() {
  if (P.n >= 10) { P = null; return endScreen(); }
  const d = await api(`/api/practice/next?topic_id=${P.tid}`), q = d.question; P.q = q; P.pick = null; P.done = false; P.aid = Date.now() + "-" + Math.random().toString(36).slice(2);
  show(`${hd("Practice", "home()")}<div class="bar"><i data-w="${(P.n + 1) * 10}" style="background:var(--blue)"></i></div><p class="sub">Question ${P.n + 1} of 10</p><h2 style="font-size:20px;margin:14px 0">${esc(q.text)}</h2>
  ${q.options.map((o, i) => `<button class="opt" id="o${i}" onclick="pick(${i})"><b>${"ABCD"[i]}</b>${esc(o)}</button>`).join("")}<div id="fb"></div><button class="btn" id="go" onclick="submitQ()" disabled>${tr("Submit")}</button>`);
}
function pick(i) { if (P.done) return; P.pick = i; document.querySelectorAll(".opt").forEach((o, j) => o.classList.toggle("sel", i === j)); document.getElementById("go").disabled = false; }
const submitQ = guard(async () => {
  if (P.done) { P.n++; return nextQ(); }
  const go = document.getElementById("go"); if (go.disabled) return; go.disabled = true;
  let r; try { r = await api("/api/answers", "POST", { question_id: P.q.id, chosen: P.pick, attempt_id: P.aid }); } catch (e) { go.disabled = false; throw e; }
  P.done = true; if (r.correct) P.ok++;
  document.getElementById("o" + r.correct_index).classList.add("right");
  if (!r.correct) { document.getElementById("o" + P.pick).classList.add("wrong"); document.getElementById("fb").innerHTML = `<div class="note">Not yet, and that is okay. Mistakes help you learn. 💪<br><b>Hint:</b> ${esc(r.hint)}<br>${esc(r.explanation)}</div>${r.root_gap ? `<div class="note"><b>Root gap?</b> This may be hard because <b>${esc(r.root_gap.name)}</b> needs more practice. <a href="#" onclick="lesson(${r.root_gap.topic_id});return false">Revise it first</a></div>` : ""}`; }
  else document.getElementById("fb").innerHTML = `<div class="note">Correct! Next question will be harder.</div>`;
  go.textContent = tr("Next"); go.disabled = false;
});
function endScreen() {
  show(`<div class="center"><img class="trophy" src="${img("keepgoing")}" alt=""><button class="btn" onclick="home()">${tr("Back to Home")}</button><button class="btn alt" onclick="learnPath()">${tr("View Next Lesson")}</button></div>`); confetti();
}
let T = null;
const takeTest = guard(async (id) => {
  if (!id) { const classes = await api("/api/classes"); let m = null;
    for (const c of classes) { const ms = await api(`/api/classes/${c.id}/materials?kind=test`); if (ms[0]) { m = ms[0]; break; } }
    if (!m) return toast("Your teacher has not posted a test yet"); id = m.test_id; }
  T = { ...(await api(`/api/tests/${id}/start`, "POST")), i: 0, a: {} };
  if (T.ends_at) T.end = Date.now() + (T.ends_at - T.server_time) * 1000;   // relative time: immune to wrong device clocks
  testQ();
});
function testQ() {
  const q = T.questions[T.i], last = T.i === T.questions.length - 1;
  show(`${hd(T.title, "home()")}${T.end ? `<div class="note" style="text-align:center;font-weight:700">Time left: <span id="tmr"></span></div>` : ""}<div class="bar"><i data-w="${(T.i + 1) / T.questions.length * 100}" style="background:var(--blue)"></i></div><p class="sub">Question ${T.i + 1} of ${T.questions.length}</p><h2 style="font-size:20px;margin:14px 0">${esc(q.text)}</h2>
  ${q.options.map((o, i) => `<button class="opt ${T.a[q.id] === i ? "sel" : ""}" onclick="T.a[${q.id}]=${i};testQ()"><b>${"ABCD"[i]}</b>${esc(o)}</button>`).join("")}
  <button class="btn" onclick="${last ? "finishTest()" : "T.i++;testQ()"}">${last ? "Submit test" : "Next"}</button>`);
  tick();
}
function tick() {
  const el = document.getElementById("tmr"); if (!el || !T?.end) return;
  const left = Math.max(0, Math.round((T.end - Date.now()) / 1000));
  el.textContent = `${Math.floor(left / 60)}:${String(left % 60).padStart(2, "0")}`;
  if (left <= 0) { toast("Time is up. Submitting your answers"); return finishTest(); }
  clearTimeout(T.tm); T.tm = setTimeout(tick, 1000);
}
const finishTest = guard(async () => {
  T.end = null; clearTimeout(T.tm);
  const r = await api(`/api/tests/${T.id}/submit`, "POST", { answers: T.a }); T.review = r.review;
  show(`<div class="center"><img class="trophy" src="${img("welldone")}" alt=""><h1>${tr(r.percent >= 60 ? "Well done!" : "Keep going!")}</h1><p class="sub">You scored <b>${r.score} / ${r.total}</b></p><button class="btn alt" onclick="reviewTest()">View answers</button><button class="btn alt" onclick="takeTest(${T.id})">Retake Test</button><button class="btn" onclick="home()">Back to Home</button></div>`);
  if (r.percent >= 60) confetti();
});
const progress = guard(async () => {
  const p = await api("/api/progress"), o = p.overall;
  withNav(`${hd("My Progress", "home()")}<div class="card"><div class="ring" data-p="${pct(o.accuracy)}" style="--p:0"><i>0%</i></div><div class="grow"><b>Overall accuracy</b><small>${o.correct} correct of ${o.attempts} answers</small></div></div>
  <div style="display:flex;gap:10px"><div class="stat">${p.topics.length}<small>Topics tried</small></div><div class="stat">${o.attempts}<small>Answers</small></div><div class="stat">${pct(o.accuracy)}%<small>Accuracy</small></div></div>
  <h2>${tr("Achievements")}</h2>${badges(p)}<h2>Mastery by topic</h2>${p.topics.length ? p.topics.map((t, i) => bar(t.name, pct(t.mastery), col(t.subject, i))).join("") : `<p class="sub">Answer some practice questions to see progress.</p>`}`, "progress");
});

/* ---------- teacher ---------- */
const teacherHome = async () => {
  const classes = await api("/api/classes");
  if (!classes.length) {
    withNav(`<h1>Good morning, ${esc(S.user.name)}</h1><p class="sub">Create your first class</p><input id="cn" placeholder="Class name, e.g. 8A Maths"><input id="cg" type="number" min="6" max="10" placeholder="Class (6 to 10)"><input id="cs" placeholder="Subject, e.g. Maths"><button class="btn" onclick="makeClass()">Create class</button>`, "home"); return;
  }
  const c = classes.find(x => x.id === S.cid) || classes[0]; S.cid = c.id; S.tc = c;
  const d = await api(`/api/classes/${c.id}/dashboard`);
  withNav(`<div class="hdr"><div><h1>Good morning, ${esc(S.user.name)}</h1><p class="sub">${esc(c.name)} · Class ${c.grade}</p></div><img src="${img("bell")}" width="38" alt="Notifications" onclick="notifications()" style="cursor:pointer"></div>
  <div style="display:flex;gap:10px;margin-top:14px"><div class="stat">${d.student_count}<small>My students</small></div><div class="stat">${esc(c.join_code)}<small>Class code</small></div></div>
  <button class="btn" onclick="addContent()">Add video, notes, questions or test</button><button class="btn alt" onclick="testsScreen()">Tests & answer keys</button><h2>Student overview</h2>${d.students.length ? d.students.map((s, i) => { const weak = s.weak_topics[0]; return `<div class="card"><img src="${img(["boy1", "girl2", "boy3", "boy5"][i % 4])}" alt=""><div class="grow"><b>${esc(s.name)}</b><small style="color:${weak ? "var(--bad)" : "var(--ok)"}">${weak ? "Needs help · " + esc(weak) : s.attempts ? "Progressing well" : "Not started"}</small></div><button class="btn alt" style="width:auto;margin:0;padding:8px 16px" onclick="studentDetail(${s.student_id})">View</button></div>`; }).join("") : `<p class="sub">Share code <b>${esc(c.join_code)}</b> so students can join.</p>`}
  ${d.class_weak_topics.length ? `<div class="note"><b>Class needs help with:</b> ${d.class_weak_topics.map(t => esc(t.topic)).join(", ")}</div>` : ""}`, "home");
};
const makeClass = guard(async () => { const v = id => document.getElementById(id).value; await api("/api/classes", "POST", { name: v("cn"), grade: v("cg"), subject: v("cs") }); home(); });
const studentDetail = guard(async (sid, tab = "p") => {
  const [p, r] = await Promise.all([api(`/api/progress?student_id=${sid}`), api(`/api/recommendations?student_id=${sid}`)]);
  const weak = p.weak_topics.length;
  show(`${hd("Student Details", "home()")}<div class="card"><img src="${img("girl2")}" alt=""><div class="grow"><b>${esc(p.student.name)}</b><small>${pct(p.overall.accuracy)}% overall</small></div>${weak ? `<span class="tag">Needs support</span>` : `<span class="tag ok">On track</span>`}</div>
  <div class="tabs"><button class="${tab === "p" ? "on" : ""}" onclick="studentDetail(${sid},'p')">Progress</button><button class="${tab === "l" ? "on" : ""}" onclick="studentDetail(${sid},'l')">Learning Path</button></div>
  ${tab === "p" ? `<h2>Topic mastery</h2>${p.topics.map((t, i) => bar(t.name, pct(t.mastery), col(t.subject, i))).join("") || `<p class="sub">No answers yet.</p>`}` : r.recommendations.map(x => `<div class="card"><div class="grow"><b>${esc(x.topic)}</b><small>${LABEL[x.action]} · ${esc(x.reason)}</small></div></div>`).join("")}
  ${r.recommendations[0] ? `<div class="note"><b>Suggested action</b><br>${esc(r.recommendations[0].action)}: ${esc(r.recommendations[0].topic)}</div>` : ""}`);
});

/* ---------- parent ---------- */
const parentHome = async () => {
  const kids = await api("/api/parent/children");
  withNav(`<h1>Parent Dashboard</h1>${kids.length ? kids.map(k => `<div class="card"><div class="ring" data-p="${pct(k.overall.accuracy)}" style="--p:0"><i>0%</i></div><div class="grow"><b>${esc(k.name)}</b><small>${k.overall.attempts} answers</small></div></div>
  <h2>Recent activity</h2>${k.weak_topics.map(t => `<div class="card"><img src="${img("bellnew")}" alt=""><div class="grow"><b>Needs help in ${esc(t)}</b></div></div>`).join("")}${k.next_steps.map(n => `<div class="card"><img src="${img("chart")}" alt=""><div class="grow"><b>${esc(n.action)}: ${esc(n.topic)}</b><small>${esc(n.reason)}</small></div></div>`).join("")}`).join("") : `<p class="sub">No child linked yet. Your child must enter this email as their parent's email when signing up.</p>`}`, "home");
};

/* ---------- class materials (student) ---------- */
const fileUrl = m => `${API}/files/${m.id}?token=${S.token}`;
const materials = guard(async () => {
  const c = (await api("/api/classes"))[0], ms = await api(`/api/classes/${c.id}/materials`);
  const view = m => m.kind === "lecture" && m.has_file ? `<video controls preload="none" style="width:100%;border-radius:12px;margin-top:8px" src="${fileUrl(m)}"></video>`
    : m.kind === "note" && m.has_file ? `<a class="btn alt" style="text-align:center;text-decoration:none" target="_blank" href="${fileUrl(m)}">Open PDF</a>`
    : m.kind === "practice" ? `<button class="btn" onclick="practice(${m.topic_id})">Start practice</button>`
    : m.kind === "test" ? `<small>${info(m)}</small>${m.deadline && Date.now() / 1000 > m.deadline ? '<p class="sub">Closed</p>' : `<button class="btn" onclick="takeTest(${m.test_id})">Take test</button>`}<button class="btn alt" onclick="studentKey(${m.test_id})">Answer key</button>` : esc(m.body);
  withNav(`${hd("Class materials", "home()")}${ms.length ? ms.map(m => `<div class="card" style="display:block"><b>${esc(m.title)}</b><small>${{ lecture: "Video lecture", note: "Notes", practice: "Practice", test: "Test" }[m.kind]}</small>${view(m)}</div>`).join("") : `<p class="sub">Your teacher has not posted anything yet.</p>`}`, "home");
});

/* ---------- add content (teacher) ---------- */
const addContent = guard(async (tab = "lecture") => {
  const c = S.tc, topics = await api(`/api/topics?grade=${c.grade}&subject=${encodeURIComponent(c.subject)}`);
  const sel = (id, extra = "") => `<select id="${id}">${extra}${topics.map(t => `<option value="${t.id}">${esc(t.name)}</option>`).join("")}</select>`;
  const forms = {
    lecture: `<input id="title" placeholder="Lecture title"><input id="file" type="file" accept="video/mp4,video/webm"><button class="btn" onclick="upload('lecture')">Upload video (MP4/WebM)</button>`,
    note: `<input id="title" placeholder="Notes title"><input id="file" type="file" accept="application/pdf"><button class="btn" onclick="upload('note')">Upload PDF notes</button>`,
    question: `${sel("qt", '<option value="new">+ New topic</option>')}<input id="nt" placeholder="New topic name (if chosen above)"><select id="pre"><option value="">Builds on: nothing</option>${topics.map(t => `<option value="${t.id}">Builds on: ${esc(t.name)}</option>`).join("")}</select>
      <select id="qd"><option value="1">Easy</option><option value="2">Medium</option><option value="3">Hard</option></select><input id="qx" placeholder="Question">${[0, 1, 2, 3].map(i => `<input id="o${i}" placeholder="Option ${"ABCD"[i]}">`).join("")}
      <select id="qc">${[0, 1, 2, 3].map(i => `<option value="${i}">Correct answer: ${"ABCD"[i]}</option>`).join("")}</select><input id="qh" placeholder="Hint (shown on a wrong answer)"><input id="qe" placeholder="Explanation"><button class="btn" onclick="saveQ()">Save question</button>`,
    test: `${sel("tt").replace("<select", '<select onchange="loadQs()"')}<div id="ql"></div><input id="tl" placeholder="Title, e.g. Fractions quiz"><input id="tm" type="number" min="0" max="300" placeholder="Time limit in minutes (0 = no limit)"><label class="sub" style="display:block;margin-top:10px">Deadline (optional)</label><input id="td" type="datetime-local"><input id="tn" type="number" min="1" value="5" placeholder="Random question count (used if none picked)"><button class="btn alt" onclick="assign('practice')">Assign practice</button><button class="btn" onclick="assign('test')">Create test</button>`
  };
  show(`${hd("Add to " + c.name, "home()")}<div class="tabs" style="flex-wrap:wrap">${[["lecture", "Video"], ["note", "Notes"], ["question", "Question"], ["test", "Practice & test"]].map(([k, l]) => `<button class="${tab === k ? "on" : ""}" onclick="addContent('${k}')">${l}</button>`).join("")}</div>${forms[tab]}`);
  if (tab === "test") loadQs();
});
const upload = guard(async (kind) => {
  const f = document.getElementById("file").files[0], title = document.getElementById("title").value.trim();
  if (!f || !title) return toast("Add a title and choose a file");
  toast("Uploading...");
  const res = await fetch(`${API}/api/classes/${S.tc.id}/upload?kind=${kind}&title=${encodeURIComponent(title)}&filename=${encodeURIComponent(f.name)}`, { method: "POST", headers: { Authorization: "Bearer " + S.token, "Content-Type": "application/octet-stream" }, body: f });
  const d = await res.json(); if (!res.ok) throw new Error(d.error);
  toast("Uploaded"); home();
});
const saveQ = guard(async () => {
  const v = id => document.getElementById(id).value.trim(); let tid = v("qt");
  if (!v("o0") || !v("o1") || !v("qx")) return toast("Add the question and at least options A and B");
  if (tid === "new") { if (!v("nt")) return toast("Enter a topic name"); tid = (await api("/api/topics", "POST", { grade: S.tc.grade, subject: S.tc.subject, name: v("nt"), prereq_id: v("pre") || null })).id; }
  await api("/api/questions", "POST", { topic_id: +tid, difficulty: +v("qd"), text: v("qx"), options: [0, 1, 2, 3].map(i => v("o" + i)).filter(Boolean), correct_index: +v("qc"), hint: v("qh"), explanation: v("qe") });
  toast("Question saved"); addContent("question");
});
const assign = guard(async (kind) => {
  const v = id => document.getElementById(id).value.trim(), tid = +v("tt"), c = S.tc, title = v("tl") || "Class activity";
  if (!tid) return toast("Add a topic and questions first");
  if (kind === "practice") await api(`/api/classes/${c.id}/materials`, "POST", { kind, title, topic_id: tid });
  else { const ids = [...document.querySelectorAll(".qk:checked")].map(x => +x.value), td = v("td");
    await api("/api/tests", "POST", { title, class_id: c.id, time_limit_min: +v("tm") || 0, deadline: td ? Math.floor(new Date(td).getTime() / 1000) : null, ...(ids.length ? { question_ids: ids } : { topic_id: tid, count: +v("tn") || 5 }) }); }
  toast(kind === "practice" ? "Practice assigned" : "Test created"); home();
});

/* ---------- test details, answer keys ---------- */
const when = ts => new Date(ts * 1000).toLocaleString([], { day: "numeric", month: "short", hour: "2-digit", minute: "2-digit" });
const info = t => [t.time_limit_min ? `${t.time_limit_min} min` : "No time limit", t.deadline ? "due " + when(t.deadline) : "No deadline"].join(" · ");
const keyList = items => items.map((q, n) => `<div class="card" style="display:block"><b>${n + 1}. ${esc(q.text)}</b>${q.options.map((o, i) => `<div style="margin-top:6px;padding:6px 10px;border-radius:8px;background:${i === q.correct_index ? "#c9f0d5" : i === q.chosen ? "#ffd5d5" : "#f1f4fb"}">${"ABCD"[i]}. ${esc(o)}${i === q.correct_index ? " ✓" : i === q.chosen ? " (your answer)" : ""}</div>`).join("")}${q.explanation ? `<small>${esc(q.explanation)}</small>` : ""}</div>`).join("");
const reviewTest = () => {
  if (!T.review.length || T.review[0].correct_index == null) return toast("The answer key opens after the deadline");
  show(`${hd("Your answers", "home()")}${keyList(T.questions.map(q => { const r = T.review.find(x => x.question_id === q.id); return { ...q, correct_index: r.correct_index, chosen: r.chosen, explanation: r.explanation }; }))}`);
};
const studentKey = guard(async id => { show(`${hd("Answer key", "materials()")}${keyList(await api(`/api/tests/${id}/key`))}`); });
const testsScreen = guard(async () => {
  const ts = await api("/api/tests");
  show(`${hd("Tests & answer keys", "home()")}${ts.length ? ts.map(t => `<div class="card" style="cursor:pointer" onclick="testDetail(${t.id})"><div class="grow"><b>${esc(t.title)}</b><small>${t.question_count} questions · ${info(t)} · ${t.submissions} submitted</small></div>›</div>`).join("") : `<p class="sub">No tests yet.</p>`}`);
});
const testDetail = guard(async id => {
  const [k, r] = await Promise.all([api(`/api/tests/${id}/key`), api(`/api/tests/${id}/results`)]);
  show(`${hd("Test details", "testsScreen()")}<h2>Results</h2>${r.length ? r.map(x => `<div class="card"><div class="grow"><b>${esc(x.student)}</b></div><b>${x.score}/${x.total}</b></div>`).join("") : `<p class="sub">No submissions yet.</p>`}<h2>Answer key</h2>${keyList(k)}`);
});
const loadQs = guard(async () => {
  const id = document.getElementById("tt")?.value; if (!id) return;
  const qs = await api(`/api/questions?topic_id=${id}&limit=100`);
  document.getElementById("ql").innerHTML = qs.length ? `<h2>Pick questions (or leave empty for random)</h2>` + qs.map(q => `<label class="card" style="cursor:pointer"><input type="checkbox" class="qk" value="${q.id}" style="width:auto;margin:0"><span class="grow">${esc(q.text)}<small>${["Easy", "Medium", "Hard"][q.difficulty - 1]} · key: ${esc(q.options[q.correct_index])}</small></span></label>`).join("") : `<p class="sub">No questions for this topic yet. Add some in the Question tab.</p>`;
});

/* ---------- start ---------- */
if ("serviceWorker" in navigator) navigator.serviceWorker.register("/sw.js").catch(() => { });
(async () => {
  if (S.token) { try { S.user = await api("/api/me"); return home(); } catch { } }
  splash();
})();

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

