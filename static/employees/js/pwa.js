(function () {
    const isIOS = /iphone|ipad|ipod/i.test(window.navigator.userAgent);
    const isAndroid = /android/i.test(window.navigator.userAgent);

    function isStandalone() {
        return window.matchMedia("(display-mode: standalone)").matches ||
            window.matchMedia("(display-mode: fullscreen)").matches ||
            window.navigator.standalone === true;
    }

    function installHelpText() {
        if (isStandalone()) {
            return "";
        }

        if (isIOS) {
            return "On iPhone, tap Share, then Add to Home Screen to open this verification in fullscreen app mode.";
        }

        if (deferredPrompt) {
            return "Tap Install app to add this verification to your home screen.";
        }

        if (isAndroid) {
            return "If the prompt does not open, use Chrome menu, then Add to Home screen or Install app.";
        }

        return "Use your browser menu or address bar install icon to add this verification app.";
    }

    function refreshInstallUI() {
        const standalone = isStandalone();
        document.documentElement.classList.toggle("pwa-standalone", standalone);
        document.documentElement.classList.toggle("pwa-ios", isIOS);
        document.documentElement.classList.toggle("pwa-install-supported", Boolean(deferredPrompt));

        const help = document.getElementById("pwaInstallHelp");
        if (help) {
            help.textContent = installHelpText();
        }
    }

    function setDisplayModeClass() {
        refreshInstallUI();
    }

    let deferredPrompt = null;

    refreshInstallUI();

    if ("serviceWorker" in navigator) {
        window.addEventListener("load", function () {
            navigator.serviceWorker.register("/service-worker.js").then(function (registration) {
                registration.update().catch(function () {});
            }).catch(function () {});
        });
    }

    window.addEventListener("beforeinstallprompt", function (event) {
        if (isStandalone()) {
            return;
        }

        event.preventDefault();
        deferredPrompt = event;
        document.documentElement.classList.add("pwa-install-ready");
        refreshInstallUI();
    });

    window.installCRVerifyApp = function () {
        if (document.documentElement.requestFullscreen && !document.fullscreenElement) {
            document.documentElement.requestFullscreen().catch(function () {});
        }

        if (!deferredPrompt) {
            document.documentElement.classList.add("pwa-install-fallback");
            refreshInstallUI();
            return;
        }

        deferredPrompt.prompt();
        deferredPrompt.userChoice.finally(function () {
            deferredPrompt = null;
            document.documentElement.classList.remove("pwa-install-ready");
            refreshInstallUI();
        });
    };

    window.addEventListener("appinstalled", function () {
        deferredPrompt = null;
        document.documentElement.classList.add("pwa-installed");
        document.documentElement.classList.add("pwa-standalone");
        document.documentElement.classList.remove("pwa-install-ready");
        refreshInstallUI();
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
