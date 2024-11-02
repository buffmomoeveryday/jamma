(function() {
    "use strict";



    var currentLocation = window.location;
    var document = window.document;
    var currentScript = document.currentScript;
    var apiEndpoint = currentScript.getAttribute("data-api") || (new URL(currentScript.src)).origin + "/api/track";

    console.log("currentScript.src:", currentScript.src);
    console.log("apiEndpoint:", apiEndpoint);

    function ignoreEvent(reason, options) {
        if (reason) {
            console.warn("Ignoring Event: " + reason);
        }
        if (options && options.callback) {
            options.callback();
        }
    }

    function sendEvent(type, options) {

        if (window._phantom || window.__nightmare || window.navigator.webdriver || window.Cypress) {
            return ignoreEvent(null, options);
        }

        try {
            if (window.localStorage.plausible_ignore === "true") {
                return ignoreEvent("localStorage flag", options);
            }
        } catch (e) {}

        var eventData = {
            n: type,
            u: currentLocation.href,
            d: currentScript.getAttribute("data-domain"),
            r: document.referrer || null
        };

        if (options && options.meta) {
            eventData.m = JSON.stringify(options.meta);
        }

        if (options && options.props) {
            eventData.p = options.props;
        }

        var xhr = new XMLHttpRequest();
        xhr.open("POST", apiEndpoint, true);
        xhr.setRequestHeader("Content-Type", "application/json");

        xhr.send(JSON.stringify(eventData));

        console.log(xhr)

        xhr.onreadystatechange = function() {
            if (xhr.readyState === 4 && options && options.callback) {
                options.callback();
            }
        };
    }

    var queuedEvents = window.plausible && window.plausible.q || [];
    window.plausible = sendEvent;

    for (var i = 0; i < queuedEvents.length; i++) {
        sendEvent.apply(this, queuedEvents[i]);
    }

    var previousPathname;

    function trackPageview() {
        if (previousPathname !== currentLocation.pathname) {
            previousPathname = currentLocation.pathname;
            sendEvent("pageview");
        }
    }

    var history = window.history;
    if (history.pushState) {
        var pushState = history.pushState;
        history.pushState = function() {
            pushState.apply(this, arguments);
            trackPageview();
        };
        window.addEventListener("popstate", trackPageview);
    } else {
        trackPageview();
    }

    if (document.visibilityState === "prerender") {
        document.addEventListener("visibilitychange", function() {
            if (!previousPathname || document.visibilityState === "visible") {
                trackPageview();
            }
        });
    } else {
        trackPageview();
    }
})();
