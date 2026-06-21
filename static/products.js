// Per-product edit tokens, kept in localStorage: { "<productId>": "<token>" }.
// Holding a product's token is what proves you created it.
const TOKENS_KEY = 'toolshop_tokens';

function getTokens() {
  try { return JSON.parse(localStorage.getItem(TOKENS_KEY) || '{}'); }
  catch (e) { return {}; }
}
function saveToken(id, token) {
  const t = getTokens();
  t[id] = token;
  localStorage.setItem(TOKENS_KEY, JSON.stringify(t));
}
function getToken(id) {
  return getTokens()[id];
}
function removeToken(id) {
  const t = getTokens();
  delete t[id];
  localStorage.setItem(TOKENS_KEY, JSON.stringify(t));
}
function ownsProduct(id) {
  return Boolean(getTokens()[id]);
}

function escapeHtml(str) {
  return String(str).replace(/[&<>"']/g, c => ({
    '&': '&amp;', '<': '&lt;', '>': '&gt;', '"': '&quot;', "'": '&#39;'
  }[c]));
}
