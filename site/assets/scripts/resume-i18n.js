(function () {
  var root = document.querySelector("[data-resume-i18n]");
  if (!root) return;

  var locales = root.querySelectorAll(".resume-locale");
  var buttons = document.querySelectorAll(".i18n-toggle [data-lang]");
  var storageKey = "personwebsite-resume-lang";
  var defaultLang = "zh";

  function setLang(lang) {
    locales.forEach(function (el) {
      el.classList.toggle("is-active", el.getAttribute("data-lang") === lang);
    });
    buttons.forEach(function (btn) {
      btn.classList.toggle("is-active", btn.getAttribute("data-lang") === lang);
      btn.setAttribute("aria-pressed", btn.getAttribute("data-lang") === lang ? "true" : "false");
    });
    try {
      localStorage.setItem(storageKey, lang);
    } catch (e) {}
    document.documentElement.lang = lang === "en" ? "en" : "zh-CN";
  }

  var saved = null;
  try {
    saved = localStorage.getItem(storageKey);
  } catch (e) {}
  setLang(saved === "en" || saved === "zh" ? saved : defaultLang);

  buttons.forEach(function (btn) {
    btn.addEventListener("click", function () {
      setLang(btn.getAttribute("data-lang"));
    });
  });
})();
