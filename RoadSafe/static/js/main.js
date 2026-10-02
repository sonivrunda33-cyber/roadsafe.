document.addEventListener("DOMContentLoaded", () => {

    // Always reveal the page even when the optional animation loader is unavailable.
    document.body.classList.add("page-loaded");
    "use strict";

    const navbar = document.getElementById("navbar") || document.querySelector(".navbar");
    const menuToggle = document.getElementById("menuToggle");
    const mobileNav = document.getElementById("mobileNav");

    const updateNavbar = () => {
        if (navbar) navbar.classList.toggle("scrolled", window.scrollY > 30);
    };
    updateNavbar();
    window.addEventListener("scroll", updateNavbar, { passive: true });

    if (menuToggle && mobileNav) {
        menuToggle.addEventListener("click", () => {
            const open = mobileNav.classList.toggle("open");
            menuToggle.setAttribute("aria-expanded", String(open));
        });
        mobileNav.querySelectorAll("a").forEach(a => {
            a.addEventListener("click", () => {
                mobileNav.classList.remove("open");
                menuToggle.setAttribute("aria-expanded", "false");
            });
        });
    }

    const reveal = document.querySelectorAll(".rs-reveal, .dashboard-card, .report-form, .auth-card, .profile-card, .side-card");
    if ("IntersectionObserver" in window) {
        const observer = new IntersectionObserver((entries, obs) => {
            entries.forEach(entry => {
                if (entry.isIntersecting) {
                    entry.target.classList.add("visible");
                    obs.unobserve(entry.target);
                }
            });
        }, { threshold: 0.12 });
        reveal.forEach((el, i) => {
            el.style.transitionDelay = `${Math.min(i * 70, 350)}ms`;
            el.classList.add("reveal");
            observer.observe(el);
        });
    } else {
        reveal.forEach(el => el.classList.add("visible"));
    }

    document.querySelectorAll('a[href^="#"]').forEach(link => {
        link.addEventListener("click", event => {
            const id = link.getAttribute("href");
            if (!id || id === "#") return;
            const target = document.querySelector(id);
            if (target) {
                event.preventDefault();
                target.scrollIntoView({ behavior: "smooth", block: "start" });
            }
        });
    });

    const fileInput = document.querySelector("input[type='file']");
    if (fileInput) {
        fileInput.addEventListener("change", () => {
            const file = fileInput.files && fileInput.files[0];
            if (!file) return;
            if (!file.type.startsWith("image/")) {
                alert("Please select a valid image.");
                fileInput.value = "";
                return;
            }
            if (file.size > 10 * 1024 * 1024) {
                alert("Image size must be less than 10MB.");
                fileInput.value = "";
            }
        });
    }

    const locationButton =
        document.querySelector("#getLocation") ||
        document.querySelector("[data-get-location]") ||
        document.querySelector(".location-button");

    if (locationButton) {
        locationButton.addEventListener("click", () => {
            if (!navigator.geolocation) {
                alert("Geolocation is not available in this browser.");
                return;
            }

            const lat = document.querySelector("[name='latitude']");
            const lng = document.querySelector("[name='longitude']");
            const original = locationButton.textContent;

            locationButton.disabled = true;
            locationButton.textContent = "Locating...";

            navigator.geolocation.getCurrentPosition(
                position => {
                    if (lat) lat.value = position.coords.latitude.toFixed(7);
                    if (lng) lng.value = position.coords.longitude.toFixed(7);
                    locationButton.disabled = false;
                    locationButton.textContent = "✓ Location Added";
                },
                () => {
                    locationButton.disabled = false;
                    locationButton.textContent = original;
                    alert("Unable to get your location. Please enter latitude and longitude manually.");
                },
                { enableHighAccuracy: true, timeout: 10000, maximumAge: 60000 }
            );
        });
    }

    document.querySelectorAll(".flash").forEach(message => {
        setTimeout(() => {
            message.style.opacity = "0";
            message.style.transform = "translateY(-8px)";
            setTimeout(() => message.remove(), 350);
        }, 4500);
    });

    // Premium pointer glow on desktop.
    if (window.matchMedia("(pointer:fine)").matches) {
        const glow = document.createElement("div");
        glow.className = "cursor-glow";
        document.body.appendChild(glow);

        let x = -100, y = -100;
        window.addEventListener("pointermove", e => {
            x = e.clientX; y = e.clientY;
            glow.style.transform = `translate3d(${x}px, ${y}px, 0)`;
        }, { passive: true });
    }
});
