!function() {
    "use strict";
    // fuck

    var currentLocation = window.location,
        documentObj = window.document,
        currentScript = documentObj.currentScript,
        apiUrl = currentScript.getAttribute("data-api") || new URL(currentScript.src).origin + "/api/event";

    function ignoreEvent(reason, context) {
        if (reason) {
            console.warn("Ignoring Event: " + reason);
        }
        if (context && context.callback) {
            context.callback();
        }
    }

    function sendEvent(eventName, context) {
        if ((window._phantom || window.__nightmare || window.navigator.webdriver || window.Cypress) && !window.__plausible) {
            return ignoreEvent(null, context);
        }
        try {
            if ("true" === window.localStorage.plausible_ignore) {
                return ignoreEvent("localStorage flag", context);
            }
        } catch (error) {}

        var eventPayload = {
            n: eventName,
            u: currentLocation.href,
            d: currentScript.getAttribute("data-domain"),
            r: documentObj.referrer || null
        };

        if (context && context.meta) {
            eventPayload.m = JSON.stringify(context.meta);
        }
        if (context && context.props) {
            eventPayload.p = context.props;
        }

        var xhr = new XMLHttpRequest();
        xhr.open("POST", apiUrl, true);
        xhr.setRequestHeader("Content-Type", "application/json");
        xhr.send(JSON.stringify(eventPayload));
        xhr.onreadystatechange = function() {
            if (xhr.readyState === 4 && context && context.callback) {
                context.callback({ status: xhr.status });
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
        var originalPushState = history.pushState;
        history.pushState = function() {
            originalPushState.apply(this, arguments);
            trackPageview();
        };
        window.addEventListener("popstate", trackPageview);
    }

    if ("prerender" === documentObj.visibilityState) {
        documentObj.addEventListener("visibilitychange", function() {
            if (!previousPathname && "visible" === documentObj.visibilityState) {
                trackPageview();
            }
        });
    } else {
        trackPageview();
    }

    var primaryMouseButton = 1;

    function handleEventTrigger(event) {
        if ("auxclick" === event.type && event.button !== primaryMouseButton) {
            return;
        }
        var targetElement = findEventTarget(event.target);
        if (targetElement && targetElement.href) {
            var plausibleEvent = getPlausibleEvent(targetElement);
            if (plausibleEvent.name) {
                handlePlausibleEvent(event, targetElement, plausibleEvent);
            }
        }
    }

    function findEventTarget(element) {
        console.log(element.tagName)
        while (element && (!element.tagName || element.tagName.toLowerCase() !== "a" || !element.href)) {
            element = element.parentNode;
        }
        console.log(element)
        return element;
    }

    function handlePlausibleEvent(event, targetElement, plausibleEvent) {
        var context = { props: plausibleEvent.props };
        if (!shouldOpenInNewTab(event, targetElement)) {
            var redirect = function() {
                if (!context.callbackCalled) {
                    context.callbackCalled = true;
                    window.location = targetElement.href;
                }
            };
            context.callback = redirect;
            sendEvent(plausibleEvent.name, context);
            setTimeout(redirect, 5000);
            event.preventDefault();
        } else {
            sendEvent(plausibleEvent.name, context);
        }
    }

    function shouldOpenInNewTab(event, targetElement) {
        return !event.defaultPrevented && (!targetElement.target || targetElement.target.match(/^_(self|parent|top)$/i)) && !(event.ctrlKey || event.metaKey || event.shiftKey) && event.type === "click";
    }

    function getPlausibleEvent(element) {
        var plausibleEvent = { name: null, props: {} };
        var classList = element.classList;

        if (classList) {
            for (var i = 0; i < classList.length; i++) {
                var match = classList.item(i).match(/plausible-event-(.+)(=|--)(.+)/);
                if (match) {
                    var key = match[1],
                        value = match[3].replace(/\+/g, " ");
                    if (key.toLowerCase() === "name") {
                        plausibleEvent.name = value;
                    } else {
                        plausibleEvent.props[key] = value;
                    }
                }
            }
        }

        return plausibleEvent;
    }

    documentObj.addEventListener("click", handleEventTrigger);
    documentObj.addEventListener("auxclick", handleEventTrigger);

    function findPlausibleEventFormTarget(element) {
        while (element && (!element.classList || !element.classList.contains("plausible-event-name"))) {
            element = element.parentNode;
        }
        return element;
    }

    documentObj.addEventListener("submit", function(event) {
        var targetForm = event.target;
        var plausibleEvent = getPlausibleEvent(targetForm);

        if (plausibleEvent.name) {
            event.preventDefault();
            var context = { props: plausibleEvent.props, callback: function() { targetForm.submit(); } };
            sendEvent(plausibleEvent.name, context);
            setTimeout(context.callback, 5000);
        }
    });

    documentObj.addEventListener("click", handleEventTrigger);
    documentObj.addEventListener("auxclick", handleEventTrigger);

}();
