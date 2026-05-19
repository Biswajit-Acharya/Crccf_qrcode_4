(function () {
    if ("serviceWorker" in navigator) {
        window.addEventListener("load", function () {
            navigator.serviceWorker.register("/service-worker.js").catch(function () {});
        });
    }

    let deferredPrompt = null;

    window.addEventListener("beforeinstallprompt", function (event) {
        event.preventDefault();
        deferredPrompt = event;
        document.documentElement.classList.add("pwa-install-ready");
    });

    window.installCRVerifyApp = function () {
        if (!deferredPrompt) {
            return;
        }

        deferredPrompt.prompt();
        deferredPrompt.userChoice.finally(function () {
            deferredPrompt = null;
            document.documentElement.classList.remove("pwa-install-ready");
        });
    };

    window.addEventListener("appinstalled", function () {
        deferredPrompt = null;
        document.documentElement.classList.add("pwa-installed");
        document.documentElement.classList.remove("pwa-install-ready");
    });
})();
