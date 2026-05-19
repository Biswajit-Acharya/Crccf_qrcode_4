(function () {
    function isStandalone() {
        return window.matchMedia("(display-mode: standalone)").matches ||
            window.matchMedia("(display-mode: fullscreen)").matches ||
            window.navigator.standalone === true;
    }

    function setDisplayModeClass() {
        document.documentElement.classList.toggle("pwa-standalone", isStandalone());
    }

    setDisplayModeClass();

    if ("serviceWorker" in navigator) {
        window.addEventListener("load", function () {
            navigator.serviceWorker.register("/service-worker.js").catch(function () {});
        });
    }

    let deferredPrompt = null;

    window.addEventListener("beforeinstallprompt", function (event) {
        if (isStandalone()) {
            return;
        }

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
        document.documentElement.classList.add("pwa-standalone");
        document.documentElement.classList.remove("pwa-install-ready");
    });

    function watchDisplayMode(query) {
        const mediaQuery = window.matchMedia(query);
        if (mediaQuery.addEventListener) {
            mediaQuery.addEventListener("change", setDisplayModeClass);
        } else if (mediaQuery.addListener) {
            mediaQuery.addListener(setDisplayModeClass);
        }
    }

    watchDisplayMode("(display-mode: standalone)");
    watchDisplayMode("(display-mode: fullscreen)");
})();
