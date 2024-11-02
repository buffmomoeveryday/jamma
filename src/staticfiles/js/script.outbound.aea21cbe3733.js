(function() {
  "use strict";

  var currentLocation = window.location;
  var document = window.document;
  var currentScript = document.currentScript;
  var apiUrl = currentScript.getAttribute("data-api") || new URL(currentScript.src).origin + "/track/outbound";

  function ignoreEvent(reason, options) {
    if (reason) {
      console.warn("Ignoring Event: " + reason);
    }
    if (options && options.callback) {
      options.callback();
    }
  }

  function sendEvent(name, options) {
    
      // if (/^localhost$|^127(\.[0-9]+){0,2}\.[0-9]+$|^\[::1?\]$/.test(currentLocation.hostname) || currentLocation.protocol === "file:") {
      //   return ignoreEvent("localhost", options);
      // }
      
    if (window._phantom || window.__nightmare || window.navigator.webdriver || window.Cypress) {
      return ignoreEvent(null, options);
    }
    try {
      if (window.localStorage.plausible_ignore === "true") {
        return ignoreEvent("localStorage flag", options);
      }
    } catch (e) {}

    var data = {
      n: name,
      u: currentLocation.href,
      d: currentScript.getAttribute("data-domain"),
      r: document.referrer || null
    };

    if (options && options.meta) {
      data.m = JSON.stringify(options.meta);
    }
    if (options && options.props) {
      data.p = options.props;
    }

    var xhr = new XMLHttpRequest();
    xhr.open("POST", apiUrl, true);
    xhr.setRequestHeader("Content-Type", "text/plain");
    xhr.send(JSON.stringify(data));
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

  function trackPageview() {
    if (previousPathname !== currentLocation.pathname) {
      previousPathname = currentLocation.pathname;
      sendEvent("pageview");
    }
  }

  var previousPathname;
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

  var middleButton = 1;

  function handleClick(event) {
    var target = event.target;
    var eventType = event.type;

    if (
      (eventType === "auxclick" && event.button !== middleButton) ||
      (!target || !target.tagName || target.tagName.toLowerCase() !== "a" || !target.href)
    ) {
      return;
    }

    var link = target;
    var linkHref = link.href.split("?")[0];

    if (link && link.href && link.host && link.host !== currentLocation.host) {
      var eventData = {
        name: "Outbound Link: Click",
        props: { url: link.href }
      };
      var handled = !(
        event.defaultPrevented ||
        (!event.target || event.target.match(/^_(self|parent|top)$/i)) ||
        !(event.ctrlKey || event.metaKey || event.shiftKey) &&
        eventType === "click"
      );

      if (handled) {
        var meta = { props: eventData.props };
        sendEvent(eventData.name, meta);
      } else {
        var callback = function() {
          link.click();
        };
        var eventOptions = {
          props: eventData.props,
          callback: callback
        };
        sendEvent(eventData.name, eventOptions);
        setTimeout(callback, 5000);
        event.preventDefault();
      }
    }
  }

  document.addEventListener("click", handleClick);
  document.addEventListener("auxclick", handleClick);
})();
