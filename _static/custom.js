// Draggable divider for the primary (left nav) sidebar, sitewide. Chosen width
// persists in localStorage so it holds across pages and reloads. See AUDIT.md.
//
// chap01's own JupyterLite pane watches the sidebar's size independently (a
// ResizeObserver in its own cell), so resizing here is enough to move that
// pane too -- no coupling needed in either direction.
document.addEventListener("DOMContentLoaded", function () {
  var sidebar = document.getElementById("pst-primary-sidebar");
  if (!sidebar) return;

  var STORAGE_KEY = "pst-sidebar-width-px";
  var MIN_WIDTH = 160;
  var MAX_FRACTION = 0.6;

  function applyWidth(px) {
    var max = window.innerWidth * MAX_FRACTION;
    px = Math.max(MIN_WIDTH, Math.min(px, max));
    sidebar.style.flexBasis = px + "px";
    sidebar.style.width = px + "px";
  }

  var saved = window.localStorage.getItem(STORAGE_KEY);
  if (saved) applyWidth(parseFloat(saved));

  var resizer = document.createElement("div");
  resizer.id = "pst-sidebar-resizer";
  resizer.title = "Drag to resize";
  document.body.appendChild(resizer);

  function positionResizer() {
    resizer.style.left = (sidebar.getBoundingClientRect().right - 3) + "px";
  }
  new ResizeObserver(positionResizer).observe(sidebar);
  positionResizer();

  // Any iframe on the page (e.g. chap01's JupyterLite pane) is a separate
  // document and swallows mousemove events dispatched to it during a drag;
  // disabling pointer-events for the duration lets them keep reaching window.
  var dragging = false;
  resizer.addEventListener("mousedown", function (e) {
    dragging = true;
    resizer.classList.add("dragging");
    document.body.style.userSelect = "none";
    document.querySelectorAll("iframe").forEach(function (f) {
      f.style.pointerEvents = "none";
    });
    e.preventDefault();
  });
  window.addEventListener("mousemove", function (e) {
    if (!dragging) return;
    applyWidth(e.clientX);
  });
  window.addEventListener("mouseup", function () {
    if (!dragging) return;
    dragging = false;
    resizer.classList.remove("dragging");
    document.body.style.userSelect = "";
    document.querySelectorAll("iframe").forEach(function (f) {
      f.style.pointerEvents = "";
    });
    window.localStorage.setItem(STORAGE_KEY, sidebar.getBoundingClientRect().width);
  });
});
