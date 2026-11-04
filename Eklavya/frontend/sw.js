/* Offline support: keeps the app and any lesson you opened, so it still works on a weak connection. */
const C = "learnwe-v4";
self.addEventListener("install", e => e.waitUntil(caches.open(C).then(c => c.addAll(["/", "/css/style.css", "/js/app.js"])).then(() => self.skipWaiting())));
self.addEventListener("activate", e => e.waitUntil(clients.claim()));
self.addEventListener("fetch", e => {
  const r = e.request, p = new URL(r.url).pathname;
  if (r.method !== "GET" || p.startsWith("/files/") || (p.startsWith("/api") && !p.endsWith("/lesson"))) return;
  e.respondWith(fetch(r).then(res => { if (res.ok) { const cp = res.clone(); caches.open(C).then(c => c.put(r, cp)); } return res; }).catch(() => caches.match(r)));
});
