/* =========================================================
   ROADSAFE
   dashboard.js
   Dashboard analytics
   ========================================================= */

document.addEventListener("DOMContentLoaded", () => {

    "use strict";


    /* -----------------------------------------------------
       Animated numbers
    ----------------------------------------------------- */

    const counters =
        document.querySelectorAll(
            "[data-dashboard-counter], [data-counter]"
        );


    function animateCounter(element) {

        const target =
            parseFloat(
                element.dataset.dashboardCounter ||
                element.dataset.counter ||
                "0"
            );


        const duration =
            parseInt(
                element.dataset.duration ||
                "1400",
                10
            );


        const suffix =
            element.dataset.suffix ||
            "";


        const prefix =
            element.dataset.prefix ||
            "";


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
                Math.round(value).toLocaleString() +
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

    }


    if (
        counters.length &&
        "IntersectionObserver" in window
    ) {

        const observer =
            new IntersectionObserver(
                (entries) => {

                    entries.forEach(
                        (entry) => {

                            if (
                                !entry.isIntersecting
                            ) {
                                return;
                            }


                            animateCounter(
                                entry.target
                            );


                            observer.unobserve(
                                entry.target
                            );

                        }
                    );

                },
                {
                    threshold: .5
                }
            );


        counters.forEach(
            (counter) => {

                observer.observe(
                    counter
                );

            }
        );

    } else {

        counters.forEach(
            animateCounter
        );

    }


    /* -----------------------------------------------------
       Chart bars
    ----------------------------------------------------- */

    const bars =
        document.querySelectorAll(
            ".chart-bar"
        );


    if (
        bars.length &&
        "IntersectionObserver" in window
    ) {

        const chartObserver =
            new IntersectionObserver(
                (entries) => {

                    entries.forEach(
                        (entry) => {

                            if (
                                !entry.isIntersecting
                            ) {
                                return;
                            }


                            bars.forEach(
                                (bar, index) => {

                                    const height =
                                        bar.dataset.height ||
                                        bar.style.getPropertyValue(
                                            "--height"
                                        );


                                    setTimeout(
                                        () => {

                                            bar.style.height =
                                                height;

                                        },
                                        index * 80
                                    );

                                }
                            );


                            chartObserver.disconnect();

                        }
                    );

                },
                {
                    threshold: .25
                }
            );


        const chart =
            document.querySelector(
                ".chart"
            );


        if (chart) {

            chartObserver.observe(
                chart
            );

        }

    }


    /* -----------------------------------------------------
       Progress bars
    ----------------------------------------------------- */

    const progressBars =
        document.querySelectorAll(
            ".progress-fill"
        );


    progressBars.forEach(
        (bar) => {

            const width =
                bar.dataset.width ||
                bar.style.getPropertyValue(
                    "--width"
                );


            bar.style.width =
                "0";


            setTimeout(
                () => {

                    bar.style.width =
                        width;

                },
                300
            );

        }
    );


    /* -----------------------------------------------------
       Report filtering
    ----------------------------------------------------- */

    const filter =
        document.querySelector(
            "[data-report-filter]"
        );


    const rows =
        document.querySelectorAll(
            "[data-report-row]"
        );


    if (filter) {

        filter.addEventListener(
            "change",
            () => {

                const value =
                    filter.value.toLowerCase();


                rows.forEach(
                    (row) => {

                        if (
                            value === "all"
                        ) {

                            row.style.display =
                                "";

                            return;

                        }


                        const category =
                            (
                                row.dataset.category ||
                                ""
                            ).toLowerCase();


                        const severity =
                            (
                                row.dataset.severity ||
                                ""
                            ).toLowerCase();


                        const status =
                            (
                                row.dataset.status ||
                                ""
                            ).toLowerCase();


                        const visible =
                            value === category ||
                            value === severity ||
                            value === status;


                        row.style.display =
                            visible
                                ? ""
                                : "none";

                    }
                );

            }
        );

    }


    /* -----------------------------------------------------
       Search dashboard reports
    ----------------------------------------------------- */

    const search =
        document.querySelector(
            "[data-dashboard-search]"
        );


    if (search) {

        search.addEventListener(
            "input",
            () => {

                const query =
                    search.value
                        .trim()
                        .toLowerCase();


                rows.forEach(
                    (row) => {

                        const text =
                            row.textContent
                                .toLowerCase();


                        row.style.display =
                            text.includes(query)
                                ? ""
                                : "none";

                    }
                );

            }
        );

    }


    /* -----------------------------------------------------
       Refresh dashboard
    ----------------------------------------------------- */

    const refresh =
        document.querySelector(
            "[data-dashboard-refresh]"
        );


    if (refresh) {

        refresh.addEventListener(
            "click",
            () => {

                refresh.disabled =
                    true;


                const oldText =
                    refresh.textContent;


                refresh.textContent =
                    "REFRESHING...";


                setTimeout(
                    () => {

                        window.location.reload();

                    },
                    700
                );

            }
        );

    }


    /* -----------------------------------------------------
       Current date
    ----------------------------------------------------- */

    const dateElements =
        document.querySelectorAll(
            "[data-dashboard-date]"
        );


    dateElements.forEach(
        (element) => {

            element.textContent =
                new Date()
                    .toLocaleDateString(
                        "en-IN",
                        {
                            day: "numeric",
                            month: "short",
                            year: "numeric"
                        }
                    );

        }
    );


    /* -----------------------------------------------------
       Delete confirmation
    ----------------------------------------------------- */

    document.querySelectorAll(
        "[data-delete-report]"
    ).forEach(
        (button) => {

            button.addEventListener(
                "click",
                (event) => {

                    const confirmed =
                        confirm(
                            "Are you sure you want to delete this report?"
                        );


                    if (!confirmed) {

                        event.preventDefault();

                    }

                }
            );

        }
    );

});