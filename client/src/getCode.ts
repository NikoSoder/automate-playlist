export function getCode() {
  const urlParams = new URLSearchParams(window.location.search);
  const code = urlParams.get("code");

  if (localStorage.getItem("code")) return true;

  if (!code) return false;

  localStorage.setItem("code", code);

  return true;
}
