function confirmRepayment() {
    return confirm("Are you sure you want to repay the loan?");
}

// Smooth Scroll for nav links
document.querySelectorAll("nav a[href^='#']").forEach(anchor => {
    anchor.addEventListener("click", function (e) {
        e.preventDefault();
        const target = document.querySelector(this.getAttribute("href"));
        if (target) {
            window.scrollTo({
                top: target.offsetTop - 80,
                behavior: "smooth"
            });
        }
    });
});

// Dropdown Menu Toggle
const dropBtn = document.querySelector(".dropbtn");
if (dropBtn) {
    dropBtn.addEventListener("click", function () {
        const dropdownContent = this.nextElementSibling;
        dropdownContent.classList.toggle("show");
    });
}

// Hide dropdown when clicking outside
window.addEventListener("click", function (e) {
    if (!e.target.matches('.dropbtn')) {
        const dropdowns = document.querySelectorAll(".dropdown-content");
        dropdowns.forEach(drop => {
            if (drop.classList.contains("show")) {
                drop.classList.remove("show");
            }
        });
    }
});

// Contact form validation with messages
const form = document.querySelector(".contact-form");
if (form) {
    form.addEventListener("submit", function (e) {
        const name = form.querySelector("input[name='name']");
        const email = form.querySelector("input[name='email']");
        const message = form.querySelector("textarea[name='message']");
        let isValid = true;

        [name, email, message].forEach(field => {
            if (!field.value.trim()) {
                isValid = false;
                field.style.borderColor = "red";
                if (!field.nextElementSibling || !field.nextElementSibling.classList.contains("error-msg")) {
                    const errorMsg = document.createElement("small");
                    errorMsg.className = "error-msg";
                    errorMsg.style.color = "red";
                    errorMsg.innerText = "This field is required.";
                    field.parentNode.insertBefore(errorMsg, field.nextSibling);
                }
            } else {
                field.style.borderColor = "#ccc";
                const next = field.nextElementSibling;
                if (next && next.classList.contains("error-msg")) {
                    next.remove();
                }
            }
        });

        if (!isValid) {
            e.preventDefault();
        }
    });
}

// Scroll-to-top button
const scrollTopBtn = document.createElement("button");
scrollTopBtn.innerText = "↑";
scrollTopBtn.className = "scroll-top";
document.body.appendChild(scrollTopBtn);

Object.assign(scrollTopBtn.style, {
    position: "fixed",
    bottom: "20px",
    right: "20px",
    padding: "10px 15px",
    fontSize: "20px",
    display: "none",
    background: "#ff5722",
    color: "white",
    border: "none",
    borderRadius: "5px",
    cursor: "pointer",
    zIndex: 1000
});

window.addEventListener("scroll", () => {
    scrollTopBtn.style.display = window.scrollY > 300 ? "block" : "none";
});

scrollTopBtn.addEventListener("click", () => {
    window.scrollTo({ top: 0, behavior: "smooth" });
});

// Animate cards on scroll
const cards = document.querySelectorAll(".card");
const observer = new IntersectionObserver(entries => {
    entries.forEach(entry => {
        if (entry.isIntersecting) {
            entry.target.style.opacity = 1;
            entry.target.style.transform = "translateY(0)";
            observer.unobserve(entry.target);
        }
    });
}, { threshold: 0.1 });

cards.forEach(card => {
    card.style.opacity = 0;
    card.style.transform = "translateY(40px)";
    card.style.transition = "all 0.6s ease";
    observer.observe(card);
});

// Animate home features on scroll
const features = document.querySelectorAll(".feature-box");
features.forEach(box => {
  box.style.opacity = 0;
  box.style.transform = "translateY(40px)";
  box.style.transition = "all 0.6s ease";
  observer.observe(box);
});

// Dark mode toggle (better placement, smooth transition, icon switch)
const darkToggle = document.createElement("button");
darkToggle.innerText = "🌓";
darkToggle.title = "Toggle Dark Mode";
darkToggle.className = "dark-mode-toggle";
document.body.appendChild(darkToggle);

Object.assign(darkToggle.style, {
    position: "fixed",
    bottom: "20px",
    left: "20px",
    background: "#ffffff",
    color: "#302e4d",
    border: "2px solid #302e4d",
    borderRadius: "30px",
    padding: "10px 14px",
    fontSize: "18px",
    cursor: "pointer",
    zIndex: 1000,
    boxShadow: "0 2px 8px rgba(0, 0, 0, 0.15)",
    transition: "all 0.3s ease"
});

// Apply transition to body and theme styles
const style = document.createElement("style");
style.innerHTML = `
  body {
    transition: background-color 0.4s ease, color 0.4s ease;
  }
  body.dark-mode {
    background-color: #121212;
    color: #f1f1f1;
  }
  body.dark-mode header,
  body.dark-mode footer {
    background-color: #1e1e1e;
  }
  body.dark-mode .card {
    background-color: #2a2a2a;
    color: #f1f1f1;
  }
`;
document.head.appendChild(style);

darkToggle.addEventListener("mouseenter", () => {
    darkToggle.style.backgroundColor = "#302e4d";
    darkToggle.style.color = "#ffffff";
});

darkToggle.addEventListener("mouseleave", () => {
    if (!document.body.classList.contains("dark-mode")) {
        darkToggle.style.backgroundColor = "#ffffff";
        darkToggle.style.color = "#302e4d";
    }
});

darkToggle.addEventListener("click", () => {
    document.body.classList.toggle("dark-mode");
    darkToggle.innerText = document.body.classList.contains("dark-mode") ? "☀️" : "🌙";
});

// Animate hero section items on page load
const heroItems = document.querySelectorAll(".hero-content > *");
heroItems.forEach((el, i) => {
  el.style.opacity = 0;
  el.style.transform = "translateY(40px)";
  el.style.transition = `opacity 0.6s ease ${i * 0.2}s, transform 0.6s ease ${i * 0.2}s`;
});

window.addEventListener("load", () => {
  heroItems.forEach(el => {
    el.style.opacity = 1;
    el.style.transform = "translateY(0)";
  });
});

// Animate sections on scroll using IntersectionObserver
const fadeSections = document.querySelectorAll('.fade-in-section');

const sectionObserver = new IntersectionObserver(entries => {
  entries.forEach(entry => {
    if (entry.isIntersecting) {
      entry.target.classList.add('visible');
      sectionObserver.unobserve(entry.target);
    }
  });
}, {
  threshold: 0.1
});

fadeSections.forEach(section => {
  sectionObserver.observe(section);
});

// Typed Text Animation with banking phrases and colors
const phrases = [
  "Secure Transactions",
  "Fast Loan Approvals",
  "Trusted by Thousands",
  "24/7 Customer Support",
  "Easy Digital Banking",
  "High Interest Savings",
  "Reliable Financial Solutions",
  "Personalized Service"
];

const typedText = document.getElementById("typed-text");

let phraseIndex = 0;
let charIndex = 0;
let isDeleting = false;
const typingSpeed = 120;     // ms per character
const pauseDuration = 1500;  // pause on full phrase

function type() {
  const currentPhrase = phrases[phraseIndex];

  if (isDeleting) {
    typedText.textContent = currentPhrase.substring(0, charIndex - 1);
    charIndex--;
  } else {
    typedText.textContent = currentPhrase.substring(0, charIndex + 1);
    charIndex++;
  }

  if (!isDeleting && charIndex === currentPhrase.length) {
    setTimeout(() => {
      isDeleting = true;
      type();
    }, pauseDuration);
    return;
  } else if (isDeleting && charIndex === 0) {
    isDeleting = false;
    phraseIndex = (phraseIndex + 1) % phrases.length;
  }

  setTimeout(type, isDeleting ? typingSpeed / 2 : typingSpeed);
}

document.addEventListener("DOMContentLoaded", () => {
  if (typedText) type();
});

// Carousel Logic
const track = document.querySelector('.carousel-track');
const slides = Array.from(track.children);
const dotsNav = document.querySelector('.carousel-dots');

let currentIndex = 0;
let autoSlideInterval;

// Create dots
slides.forEach((_, i) => {
  const dot = document.createElement("button");
  if (i === 0) dot.classList.add("active");
  dotsNav.appendChild(dot);
});

const dots = Array.from(dotsNav.children);

function updateCarousel(index) {
  track.style.transform = `translateX(-${index * 100}%)`;
  dots.forEach(dot => dot.classList.remove("active"));
  dots[index].classList.add("active");
  currentIndex = index;
}

dots.forEach((dot, i) => {
  dot.addEventListener("click", () => {
    updateCarousel(i);
    resetAutoSlide();
  });
});

function autoSlide() {
  const nextIndex = (currentIndex + 1) % slides.length;
  updateCarousel(nextIndex);
}

function resetAutoSlide() {
  clearInterval(autoSlideInterval);
  autoSlideInterval = setInterval(autoSlide, 4000);
}

autoSlideInterval = setInterval(autoSlide, 4000);

// Animated Counter Stats
const counters = document.querySelectorAll('.counter');
let statsStarted = false;

function animateCounters() {
  counters.forEach(counter => {
    const target = +counter.getAttribute('data-target');
    const increment = target / 200;

    const update = () => {
      const current = +counter.innerText;
      if (current < target) {
        counter.innerText = Math.ceil(current + increment);
        setTimeout(update, 15);
      } else {
        counter.innerText = target.toLocaleString();
      }
    };
    update();
  });
}

const statsSection = document.getElementById('stats');
const statsObserver = new IntersectionObserver(entries => {
  entries.forEach(entry => {
    if (entry.isIntersecting && !statsStarted) {
      animateCounters();
      statsStarted = true;
    }
  });
}, { threshold: 0.5 });

if (statsSection) statsObserver.observe(statsSection);

// Working FAQ accordion using inner wrapper
document.querySelectorAll('.faq-question').forEach(button => {
  button.addEventListener('click', () => {
    const answer = button.nextElementSibling;
    const isOpen = answer.classList.contains('open');

    // Close all
    document.querySelectorAll('.faq-answer').forEach(a => {
      a.classList.remove('open');
      a.style.maxHeight = null;
    });

    // Open selected
    if (!isOpen) {
      const inner = answer.querySelector('.faq-answer-inner');
      answer.classList.add('open');
      answer.style.maxHeight = inner.scrollHeight + 'px';
    }
  });
});