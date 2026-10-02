/* =========================================================
   ROADSAFE
   animations.js
   Premium UI animations
   ========================================================= */

document.addEventListener("DOMContentLoaded", () => {

    "use strict";


    /* -----------------------------------------------------
       Scroll reveal
    ----------------------------------------------------- */

    const elements =
        document.querySelectorAll(
            ".rs-reveal, .reveal, [data-reveal]"
        );


    if ("IntersectionObserver" in window) {

        const observer =
            new IntersectionObserver(
                (entries) => {

                    entries.forEach((entry) => {

                        if (!entry.isIntersecting) return;

                        entry.target.classList.add(
                            "visible",
                            "active",
                            "revealed"
                        );

                        observer.unobserve(
                            entry.target
                        );

                    });

                },
                {
                    threshold: 0.12,
                    rootMargin:
                        "0px 0px -60px 0px"
                }
            );


        elements.forEach((element) => {

            observer.observe(element);

        });

    } else {

        elements.forEach((element) => {

            element.classList.add(
                "visible"
            );

        });

    }


    /* -----------------------------------------------------
       Stagger animation
    ----------------------------------------------------- */

    document.querySelectorAll(
        "[data-stagger]"
    ).forEach((container) => {

        const children =
            container.children;

        const delay =
            parseInt(
                container.dataset.stagger || "80",
                10
            );


        Array.from(children).forEach(
            (child, index) => {

                child.style.transitionDelay =
                    `${index * delay}ms`;

            }
        );

    });


    /* -----------------------------------------------------
       Floating elements
    ----------------------------------------------------- */

    const floating =
        document.querySelectorAll(
            "[data-floating], .floating"
        );


    floating.forEach((element, index) => {

        const speed =
            parseFloat(
                element.dataset.speed ||
                "1"
            );


        const amplitude =
            parseFloat(
                element.dataset.amplitude ||
                "10"
            );


        let start =
            performance.now();


        function animate(time) {

            const elapsed =
                (time - start) / 1000;


            const y =
                Math.sin(
                    elapsed * speed
                ) * amplitude;


            element.style.setProperty(
                "--float-y",
                `${y}px`
            );


            element.style.transform =
                `translate3d(0, ${y}px, 0)`;


            requestAnimationFrame(
                animate
            );

        }


        setTimeout(() => {

            requestAnimationFrame(
                animate
            );

        }, index * 100);

    });


    /* -----------------------------------------------------
       Mouse parallax
    ----------------------------------------------------- */

    if (
        window.matchMedia(
            "(pointer:fine)"
        ).matches
    ) {

        const parallaxElements =
            document.querySelectorAll(
                "[data-parallax]"
            );


        let mouseX = 0;
        let mouseY = 0;

        let currentX = 0;
        let currentY = 0;


        window.addEventListener(
            "mousemove",
            (event) => {

                mouseX =
                    event.clientX /
                    window.innerWidth -
                    0.5;


                mouseY =
                    event.clientY /
                    window.innerHeight -
                    0.5;

            },
            {
                passive: true
            }
        );


        function updateParallax() {

            currentX +=
                (mouseX - currentX) *
                0.06;


            currentY +=
                (mouseY - currentY) *
                0.06;


            parallaxElements.forEach(
                (element) => {

                    const strength =
                        parseFloat(
                            element.dataset.parallax ||
                            "15"
                        );


                    const x =
                        currentX * strength;


                    const y =
                        currentY * strength;


                    element.style.transform =
                        `translate3d(
                            ${x}px,
                            ${y}px,
                            0
                        )`;

                }
            );


            requestAnimationFrame(
                updateParallax
            );

        }


        updateParallax();

    }


    /* -----------------------------------------------------
       3D card tilt
    ----------------------------------------------------- */

    if (
        window.matchMedia(
            "(pointer:fine)"
        ).matches
    ) {

        const cards =
            document.querySelectorAll(
                "[data-tilt], .rs-feature"
            );


        cards.forEach((card) => {

            card.addEventListener(
                "mousemove",
                (event) => {

                    const rect =
                        card.getBoundingClientRect();


                    const x =
                        event.clientX -
                        rect.left;


                    const y =
                        event.clientY -
                        rect.top;


                    const rotateY =
                        ((x / rect.width) -
                        0.5) * 6;


                    const rotateX =
                        ((y / rect.height) -
                        0.5) * -6;


                    card.style.transform =
                        `perspective(900px)
                         rotateX(${rotateX}deg)
                         rotateY(${rotateY}deg)
                         translateY(-6px)`;

                }
            );


            card.addEventListener(
                "mouseleave",
                () => {

                    card.style.transform =
                        "";

                }
            );

        });

    }


    /* -----------------------------------------------------
       Number counters
    ----------------------------------------------------- */

    const counters =
        document.querySelectorAll(
            "[data-counter]"
        );


    const runCounter =
        (element) => {

            const target =
                parseFloat(
                    element.dataset.counter
                );


            const duration =
                parseInt(
                    element.dataset.duration ||
                    "1500",
                    10
                );


            const suffix =
                element.dataset.suffix ||
                "";


            const prefix =
                element.dataset.prefix ||
                "";


            const decimals =
                parseInt(
                    element.dataset.decimals ||
                    "0",
                    10
                );


            const start =
                performance.now();


            function update(now) {

                const progress =
                    Math.min(
                        (now - start) /
                        duration,
                        1
                    );


                const eased =
                    1 -
                    Math.pow(
                        1 - progress,
                        3
                    );


                const value =
                    target * eased;


                element.textContent =
                    prefix +
                    value.toFixed(
                        decimals
                    ) +
                    suffix;


                if (progress < 1) {

                    requestAnimationFrame(
                        update
                    );

                }

            }


            requestAnimationFrame(
                update
            );

        };


    if (
        counters.length &&
        "IntersectionObserver" in window
    ) {

        const counterObserver =
            new IntersectionObserver(
                (entries) => {

                    entries.forEach((entry) => {

                        if (
                            !entry.isIntersecting
                        ) {
                            return;
                        }


                        runCounter(
                            entry.target
                        );


                        counterObserver.unobserve(
                            entry.target
                        );

                    });

                },
                {
                    threshold: .5
                }
            );


        counters.forEach((counter) => {

            counterObserver.observe(
                counter
            );

        });

    }


    /* -----------------------------------------------------
       Magnetic buttons
    ----------------------------------------------------- */

    if (
        window.matchMedia(
            "(pointer:fine)"
        ).matches
    ) {

        document.querySelectorAll(
            "[data-magnetic]"
        ).forEach((button) => {

            button.addEventListener(
                "mousemove",
                (event) => {

                    const rect =
                        button.getBoundingClientRect();


                    const x =
                        event.clientX -
                        rect.left -
                        rect.width / 2;


                    const y =
                        event.clientY -
                        rect.top -
                        rect.height / 2;


                    button.style.transform =
                        `translate(
                            ${x * .12}px,
                            ${y * .12}px
                        )`;

                }
            );


            button.addEventListener(
                "mouseleave",
                () => {

                    button.style.transform =
                        "";

                }
            );

        });

    }


    /* -----------------------------------------------------
       Page loader
    ----------------------------------------------------- */

    const loader =
        document.querySelector(
            ".page-loader, #page-loader"
        );


    if (loader) {

        window.addEventListener(
            "load",
            () => {

                setTimeout(() => {

                    loader.classList.add(
                        "loaded"
                    );

                    document.body.classList.add(
                        "page-loaded"
                    );

                }, 300);

            }
        );

    }


    /* -----------------------------------------------------
       Reduced motion
    ----------------------------------------------------- */

    const reducedMotion =
        window.matchMedia(
            "(prefers-reduced-motion: reduce)"
        );


    if (reducedMotion.matches) {

        document.querySelectorAll(
            "[data-floating]"
        ).forEach((element) => {

            element.style.transform =
                "none";

        });

    }

});