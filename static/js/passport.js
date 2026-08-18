// Passport Interactive Utilities

function copyPassportLink(url) {
  const fullUrl = window.location.origin + url;
  navigator.clipboard.writeText(fullUrl).then(() => {
    showToast("Skill Passport link copied to clipboard!");
  }).catch(() => {
    showToast("Copied: " + fullUrl);
  });
}

function triggerPassportPrint() {
  window.print();
}

function showToast(msg) {
  let toastEl = document.getElementById('spToast');
  if (!toastEl) {
    toastEl = document.createElement('div');
    toastEl.id = 'spToast';
    toastEl.className = 'position-fixed bottom-0 end-0 p-3';
    toastEl.style.zIndex = 1090;
    toastEl.innerHTML = `
      <div class="toast align-items-center text-white bg-dark border-0 show" role="alert">
        <div class="d-flex">
          <div class="toast-body" id="spToastBody"></div>
          <button type="button" class="btn-close btn-close-white me-2 m-auto" data-bs-dismiss="toast"></button>
        </div>
      </div>
    `;
    document.body.appendChild(toastEl);
  }
  document.getElementById('spToastBody').innerText = msg;
  setTimeout(() => {
    toastEl.remove();
  }, 3500);
}
