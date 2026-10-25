// Theme toggle, giscus theme sync and the projects tag filter.
(function () {
  var root = document.documentElement;

  function currentTheme() {
    return root.getAttribute('data-theme') === 'dark' ? 'dark' : 'light';
  }

  function syncGiscus() {
    var frame = document.querySelector('iframe.giscus-frame');
    if (!frame) return;
    frame.contentWindow.postMessage({ giscus: { setConfig: { theme: currentTheme() } } }, 'https://giscus.app');
  }

  document.querySelectorAll('.theme-toggle').forEach(function (button) {
    button.addEventListener('click', function () {
      var next = currentTheme() === 'dark' ? 'light' : 'dark';
      root.setAttribute('data-theme', next);
      try { localStorage.setItem('theme', next); } catch (e) {}
      syncGiscus();
    });
  });

  // giscus is loaded here rather than in the page so it picks up the current theme.
  var comments = document.getElementById('giscus');
  if (comments) {
    var script = document.createElement('script');
    script.src = 'https://giscus.app/client.js';
    Object.keys(comments.dataset).forEach(function (key) {
      script.setAttribute('data-' + key.replace(/[A-Z]/g, function (c) { return '-' + c.toLowerCase(); }), comments.dataset[key]);
    });
    script.setAttribute('data-theme', currentTheme());
    script.setAttribute('crossorigin', 'anonymous');
    script.async = true;
    comments.appendChild(script);
  }

  // Project pages: the contents list sits beside the README on wide screens and starts folded up on narrow ones.
  var toc = document.querySelector('.project-toc details');
  if (toc && !window.matchMedia('(min-width: 1000px)').matches) toc.open = false;

  // Projects: show the filter buttons only when JS runs, so the full list is the fallback.
  var filters = document.querySelector('.filters');
  if (filters) {
    var projects = document.querySelectorAll('.project');
    filters.hidden = false;
    filters.addEventListener('click', function (event) {
      var button = event.target.closest('button[data-tag]');
      if (!button) return;
      var tag = button.dataset.tag;
      filters.querySelectorAll('button').forEach(function (b) {
        b.setAttribute('aria-pressed', b === button ? 'true' : 'false');
      });
      projects.forEach(function (project) {
        var tags = project.dataset.tags.split(' ');
        project.hidden = tag !== 'all' && tags.indexOf(tag) === -1;
      });
    });
  }
})();
