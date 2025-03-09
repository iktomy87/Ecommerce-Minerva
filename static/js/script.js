let slideIndex = 0;
let slideInterval; // Para manejar el temporizador del carrusel

function startSlides() {
  let slides = document.getElementsByClassName("mySlides");

  // Asegurar que todas las diapositivas estén ocultas inicialmente
  for (let i = 0; i < slides.length; i++) {
    slides[i].style.display = "none";
    slides[i].style.opacity = "0"; // Inicialmente transparentes
  }

  slideIndex = 0; // Empezar en la primera diapositiva
  showSlides(); // Mostrar la primera imagen correctamente
  slideInterval = setInterval(nextSlide, 5000); // Ejecutar cada 5s
}

function plusSlides(n) {
  clearInterval(slideInterval); // Detener temporizador
  slideIndex += n - 1; // Ajustar índice manualmente
  showSlides();
  slideInterval = setInterval(nextSlide, 5000); // Reiniciar temporizador
}

function currentSlide(n) {
  clearInterval(slideInterval);
  slideIndex = n - 1;
  showSlides();
  slideInterval = setInterval(nextSlide, 5000);
}

function nextSlide() {
  slideIndex++;
  showSlides();
}

function showSlides() {
  let slides = document.getElementsByClassName("mySlides");
  let dots = document.getElementsByClassName("dot");

  // Ajustar índice si se sale del rango
  if (slideIndex >= slides.length) { slideIndex = 0; }
  if (slideIndex < 0) { slideIndex = slides.length - 1; }

  // Ocultar todas las diapositivas
  for (let i = 0; i < slides.length; i++) {
    slides[i].style.display = "none";
    slides[i].style.opacity = "0";
  }

  // Mostrar la diapositiva actual con efecto fade
  slides[slideIndex].style.display = "block";
  setTimeout(() => {
    slides[slideIndex].style.opacity = "1";
  }, 100); // Pequeño retraso para que el fade se aplique correctamente

  // Actualizar los puntos
  for (let i = 0; i < dots.length; i++) {
    dots[i].classList.remove("active");
  }
  dots[slideIndex].classList.add("active");
}

// Iniciar el carrusel cuando la página cargue
document.addEventListener("DOMContentLoaded", startSlides);
