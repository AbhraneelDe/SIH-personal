// SkillPassport Core UI & Theme Engine

document.addEventListener('DOMContentLoaded', () => {
  // 1. Theme Toggle Management
  const themeToggleBtn = document.getElementById('themeToggleBtn');
  const storedTheme = localStorage.getItem('sp-theme') || (window.matchMedia('(prefers-color-scheme: dark)').matches ? 'dark' : 'light');

  document.documentElement.setAttribute('data-theme', storedTheme);
  updateThemeIcon(storedTheme);

  if (themeToggleBtn) {
    themeToggleBtn.addEventListener('click', () => {
      const currentTheme = document.documentElement.getAttribute('data-theme');
      const nextTheme = currentTheme === 'dark' ? 'light' : 'dark';
      document.documentElement.setAttribute('data-theme', nextTheme);
      localStorage.setItem('sp-theme', nextTheme);
      updateThemeIcon(nextTheme);
    });
  }

  function updateThemeIcon(theme) {
    if (!themeToggleBtn) return;
    const icon = themeToggleBtn.querySelector('i');
    if (icon) {
      if (theme === 'dark') {
        icon.className = 'fa-solid fa-sun text-warning';
      } else {
        icon.className = 'fa-solid fa-moon text-secondary';
      }
    }
  }

  // 2. Mark Notifications Read via AJAX
  const notifDropdown = document.getElementById('notificationDropdownBtn');
  if (notifDropdown) {
    notifDropdown.addEventListener('click', () => {
      fetch('/notifications/mark-read/', {
        method: 'POST',
        headers: {
          'X-CSRFToken': getCookie('csrftoken'),
          'Content-Type': 'application/json'
        }
      }).then(response => response.json())
        .then(data => {
          if (data.status === 'ok') {
            const badge = document.getElementById('notifBadge');
            if (badge) badge.style.display = 'none';
          }
        }).catch(err => console.log('Notif read update:', err));
    });
  }
});

// CSRF Token Helper
function getCookie(name) {
  let cookieValue = null;
  if (document.cookie && document.cookie !== '') {
    const cookies = document.cookie.split(';');
    for (let i = 0; i < cookies.length; i++) {
      const cookie = cookies[i].trim();
      if (cookie.substring(0, name.length + 1) === (name + '=')) {
        cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
        break;
      }
    }
  }
  return cookieValue;
}
