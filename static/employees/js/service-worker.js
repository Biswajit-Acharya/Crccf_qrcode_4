const CACHE_NAME = "cr-verify-pwa-v3";
const APP_SHELL = [
    "/manifest.json",
    "/scanner/",
    "/static/employees/css/styles.css",
    "/static/employees/js/pwa.js",
    "/static/employees/icons/icon-192.png",
    "/static/employees/icons/icon-512.png",
    "/static/employees/icons/maskable-192.png",
    "/static/employees/icons/maskable-512.png",
];

self.addEventListener("install", (event) => {
    event.waitUntil(
        caches.open(CACHE_NAME).then((cache) => cache.addAll(APP_SHELL))
    );
    self.skipWaiting();
});

self.addEventListener("activate", (event) => {
    event.waitUntil(
        caches.keys().then((keys) =>
            Promise.all(
                keys
                    .filter((key) => key !== CACHE_NAME)
                    .map((key) => caches.delete(key))
            )
        )
    );
    self.clients.claim();
});

self.addEventListener("fetch", (event) => {
    if (event.request.method !== "GET") {
        return;
    }

    const requestUrl = new URL(event.request.url);
    if (requestUrl.origin !== self.location.origin) {
        return;
    }

    if (requestUrl.pathname.startsWith("/v/")) {
        event.respondWith(
            fetch(event.request)
                .then((response) => {
                    if (!response.ok) {
                        return response;
                    }

                    const copy = response.clone();
                    caches.open(CACHE_NAME).then((cache) => cache.put(event.request, copy));
                    return response;
                })
                .catch(() => caches.match(event.request))
        );
        return;
    }

    event.respondWith(
        caches.match(event.request).then((cached) =>
            cached || fetch(event.request).then((response) => {
                if (!response.ok) {
                    return response;
                }

                const copy = response.clone();
                caches.open(CACHE_NAME).then((cache) => cache.put(event.request, copy));
                return response;
            })
        )
    );
});
