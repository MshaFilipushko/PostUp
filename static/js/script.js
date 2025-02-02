// Анимация кнопок лайков/дизлайков
function animateButton(button, animationClass) {
  button.classList.add(animationClass);
  setTimeout(() => button.classList.remove(animationClass), 300);
}

document.querySelectorAll('.like-button, .dislike-button').forEach(btn => {
  btn.addEventListener('click', function() {
    animateButton(this, 'animate__bounceIn');
  });
});

// Плавное появление элементов
const observer = new IntersectionObserver((entries) => {
  entries.forEach(entry => {
    if (entry.isIntersecting) {
      entry.target.style.opacity = 1;
      entry.target.style.transform = 'translateY(0)';
    }
  });
});

document.querySelectorAll('.card').forEach(card => {
  card.style.opacity = 0;
  card.style.transform = 'translateY(20px)';
  card.style.transition = 'opacity 0.6s ease, transform 0.6s ease';
  observer.observe(card);
});