/* Cosmic Starfield & Meteor Animation Engine */

(function () {
  'use strict';

  function initCosmicBackground() {
    let canvas = document.getElementById('cosmic-canvas');
    if (!canvas) {
      canvas = document.createElement('canvas');
      canvas.id = 'cosmic-canvas';
      document.body.appendChild(canvas);
    }

    const ctx = canvas.getContext('2d');
    let width = 0;
    let height = 0;
    let stars = [];
    let meteors = [];
    let animationFrameId = null;

    function resize() {
      width = window.innerWidth;
      height = window.innerHeight;
      canvas.width = width * window.devicePixelRatio;
      canvas.height = height * window.devicePixelRatio;
      canvas.style.width = width + 'px';
      canvas.style.height = height + 'px';
      ctx.scale(window.devicePixelRatio, window.devicePixelRatio);
      createStars();
    }

    function createStars() {
      stars = [];
      const count = Math.floor((width * height) / 3500); // Dynamic count based on screen size
      const colors = ['#ffffff', '#a7f3d0', '#93c5fd', '#c084fc', '#67e8f9'];

      for (let i = 0; i < count; i++) {
        stars.push({
          x: Math.random() * width,
          y: Math.random() * height,
          radius: Math.random() * 1.5 + 0.3,
          color: colors[Math.floor(Math.random() * colors.length)],
          alpha: Math.random() * 0.8 + 0.2,
          speed: Math.random() * 0.015 + 0.005,
          twinkleFactor: Math.random() * Math.PI * 2
        });
      }
    }

    function spawnMeteor() {
      if (meteors.length < 3 && Math.random() < 0.03) {
        const startX = Math.random() * width * 1.2 - width * 0.1;
        const startY = Math.random() * (height * 0.4);
        const length = Math.random() * 80 + 120;
        const speed = Math.random() * 8 + 10;
        const angle = Math.PI / 4 + (Math.random() * 0.2 - 0.1); // ~45 deg inclination

        meteors.push({
          x: startX,
          y: startY,
          length: length,
          speed: speed,
          dx: Math.cos(angle) * speed,
          dy: Math.sin(angle) * speed,
          opacity: 1,
          decay: Math.random() * 0.015 + 0.01
        });
      }
    }

    function draw() {
      ctx.clearRect(0, 0, width, height);

      // 1. Draw Twinkling Stars
      for (let i = 0; i < stars.length; i++) {
        const star = stars[i];
        star.twinkleFactor += star.speed;
        const currentAlpha = Math.max(0.1, star.alpha + Math.sin(star.twinkleFactor) * 0.3);

        ctx.save();
        ctx.globalAlpha = currentAlpha;
        ctx.fillStyle = star.color;
        ctx.shadowBlur = star.radius > 1.2 ? 6 : 0;
        ctx.shadowColor = star.color;

        ctx.beginPath();
        ctx.arc(star.x, star.y, star.radius, 0, Math.PI * 2);
        ctx.fill();
        ctx.restore();
      }

      // 2. Draw & Move Meteors / Shooting Stars
      spawnMeteor();
      for (let i = meteors.length - 1; i >= 0; i--) {
        const m = meteors[i];
        m.x += m.dx;
        m.y += m.dy;
        m.opacity -= m.decay;

        if (m.opacity <= 0 || m.x > width + 100 || m.y > height + 100) {
          meteors.splice(i, 1);
          continue;
        }

        ctx.save();
        ctx.globalAlpha = m.opacity;
        const grad = ctx.createLinearGradient(
          m.x,
          m.y,
          m.x - m.dx * (m.length / m.speed),
          m.y - m.dy * (m.length / m.speed)
        );
        grad.addColorStop(0, 'rgba(255, 255, 255, 1)');
        grad.addColorStop(0.3, 'rgba(56, 189, 248, 0.8)');
        grad.addColorStop(0.7, 'rgba(168, 85, 247, 0.4)');
        grad.addColorStop(1, 'rgba(168, 85, 247, 0)');

        ctx.strokeStyle = grad;
        ctx.lineWidth = 2;
        ctx.lineCap = 'round';

        ctx.beginPath();
        ctx.moveTo(m.x, m.y);
        ctx.lineTo(
          m.x - m.dx * (m.length / m.speed),
          m.y - m.dy * (m.length / m.speed)
        );
        ctx.stroke();
        ctx.restore();
      }

      animationFrameId = requestAnimationFrame(draw);
    }

    window.addEventListener('resize', resize);
    resize();
    draw();
  }

  if (document.readyState === 'loading') {
    document.addEventListener('DOMContentLoaded', initCosmicBackground);
  } else {
    initCosmicBackground();
  }
})();
