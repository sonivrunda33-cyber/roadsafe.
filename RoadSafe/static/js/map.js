/* =========================================================
   ROADSAFE
   map.js
   Interactive Leaflet safety map
   ========================================================= */

document.addEventListener("DOMContentLoaded", () => {

    "use strict";


    const mapElement =
        document.getElementById("map");


    if (!mapElement) return;


    /* -----------------------------------------------------
       Map configuration
    ----------------------------------------------------- */

    const DEFAULT_LAT = 22.30;
    const DEFAULT_LNG = 72.58;
    const DEFAULT_ZOOM = 13;


    const map =
        L.map("map", {
            zoomControl: false,
            attributionControl: true
        }).setView(
            [
                DEFAULT_LAT,
                DEFAULT_LNG
            ],
            DEFAULT_ZOOM
        );


    /* -----------------------------------------------------
       OpenStreetMap
    ----------------------------------------------------- */

    L.tileLayer(
        "https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png",
        {
            maxZoom: 19,

            attribution:
                "&copy; OpenStreetMap contributors"
        }
    ).addTo(map);


    /* -----------------------------------------------------
       Zoom
    ----------------------------------------------------- */

    L.control.zoom({
        position: "bottomleft"
    }).addTo(map);


    /* -----------------------------------------------------
       Reports supplied by Flask
    ----------------------------------------------------- */

    const sourceReports = Array.isArray(window.ROADSAFE_REPORTS)
        ? window.ROADSAFE_REPORTS
        : [];

    const reports = sourceReports
        .map((report) => ({
            id: report.id,
            lat: Number(report.latitude ?? report.lat),
            lng: Number(report.longitude ?? report.lng),
            title: report.title || "Road issue",
            category: report.category || "Other",
            description: report.description || "",
            severity: String(report.severity || "medium").toLowerCase(),
            status: report.status || "Open",
            address: report.address || "",
            image: report.image || null
        }))
        .filter((report) =>
            Number.isFinite(report.lat) &&
            Number.isFinite(report.lng)
        );


    /* -----------------------------------------------------
       Layers
    ----------------------------------------------------- */

    const layers = {

        critical:
            L.layerGroup().addTo(map),

        high:
            L.layerGroup().addTo(map),

        low:
            L.layerGroup().addTo(map)

    };


    /* -----------------------------------------------------
       Marker
    ----------------------------------------------------- */

    function createMarker(report) {

        const icon =
            L.divIcon({

                className: "",

                html: `
                    <div class="
                        rs-marker
                        ${report.severity}
                    ">
                        <span>!</span>
                    </div>
                `,

                iconSize: [
                    34,
                    34
                ],

                iconAnchor: [
                    17,
                    34
                ],

                popupAnchor: [
                    0,
                    -30
                ]

            });


        const marker =
            L.marker(
                [
                    report.lat,
                    report.lng
                ],
                {
                    icon
                }
            );


        marker.bindPopup(`

            <div class="map-popup">

                <div class="category">
                    ${escapeHTML(
                        report.category
                    )}
                </div>

                <h3>
                    ${escapeHTML(
                        report.title
                    )}
                </h3>

                <div class="map-popup-row">

                    <span>
                        Severity
                    </span>

                    <strong>
                        ${escapeHTML(
                            report.severity
                        )}
                    </strong>

                </div>

                <div class="map-popup-row">

                    <span>
                        Status
                    </span>

                    <strong>
                        ${escapeHTML(
                            report.status
                        )}
                    </strong>

                </div>

                <a
                    href="/report"
                    class="map-popup-link"
                >
                    REPORT / VIEW →
                </a>

            </div>

        `);


        return marker;

    }


    /* -----------------------------------------------------
       Add markers
    ----------------------------------------------------- */

    function renderMarkers() {

        Object.values(layers)
            .forEach((layer) => {

                layer.clearLayers();

            });


        reports.forEach((report) => {

            const marker =
                createMarker(report);


            const layer =
                layers[report.severity];


            if (layer) {

                marker.addTo(layer);

            }

        });


        updateStats();

    }


    renderMarkers();


    /* -----------------------------------------------------
       Filters
    ----------------------------------------------------- */

    document.querySelectorAll(
        ".map-filter input"
    ).forEach((checkbox) => {

        checkbox.addEventListener(
            "change",
            () => {

                const type =
                    checkbox.dataset.type ||
                    checkbox.value;


                if (!layers[type]) return;


                if (checkbox.checked) {

                    map.addLayer(
                        layers[type]
                    );

                } else {

                    map.removeLayer(
                        layers[type]
                    );

                }


                updateStats();

            }
        );

    });


    /* -----------------------------------------------------
       Search
    ----------------------------------------------------- */

    const search =
        document.querySelector(
            ".map-search input"
        );


    if (search) {

        search.addEventListener(
            "input",
            () => {

                const query =
                    search.value
                        .trim()
                        .toLowerCase();


                if (!query) {

                    return;

                }


                const result =
                    reports.find(
                        (report) => {

                            return (

                                report.title
                                    .toLowerCase()
                                    .includes(query)

                                ||

                                report.category
                                    .toLowerCase()
                                    .includes(query)

                                ||

                                report.severity
                                    .toLowerCase()
                                    .includes(query)

                            );

                        }
                    );


                if (result) {

                    map.flyTo(
                        [
                            result.lat,
                            result.lng
                        ],
                        16,
                        {
                            duration: 1
                        }
                    );

                }

            }
        );

    }


    /* -----------------------------------------------------
       Current location
    ----------------------------------------------------- */

    const locationButton =
        document.querySelector(
            "[data-current-location]"
        );


    if (locationButton) {

        locationButton.addEventListener(
            "click",
            getUserLocation
        );

    }


    function getUserLocation() {

        if (!navigator.geolocation) {

            alert(
                "Location is not supported."
            );

            return;

        }


        locationButton &&
            (locationButton.disabled = true);


        navigator.geolocation.getCurrentPosition(

            (position) => {

                const lat =
                    position.coords.latitude;

                const lng =
                    position.coords.longitude;


                map.flyTo(
                    [
                        lat,
                        lng
                    ],
                    16,
                    {
                        duration: 1.2
                    }
                );


                L.circleMarker(
                    [
                        lat,
                        lng
                    ],
                    {
                        radius: 8,
                        color: "#d9ff3f",
                        fillColor: "#d9ff3f",
                        fillOpacity: .9,
                        weight: 3
                    }
                )
                .addTo(map)
                .bindPopup(
                    "You are here"
                )
                .openPopup();


                if (locationButton) {

                    locationButton.disabled =
                        false;

                }

            },

            () => {

                if (locationButton) {

                    locationButton.disabled =
                        false;

                }


                alert(
                    "Unable to get your location."
                );

            },

            {
                enableHighAccuracy: true,
                timeout: 10000,
                maximumAge: 60000
            }

        );

    }


    /* -----------------------------------------------------
       Stats
    ----------------------------------------------------- */

    function updateStats() {

        setText(
            "[data-map-total]",
            reports.length
        );


        setText(
            "[data-map-critical]",
            reports.filter(
                r => r.severity === "critical"
            ).length
        );


        setText(
            "[data-map-high]",
            reports.filter(
                r => r.severity === "high"
            ).length
        );


        setText(
            "[data-map-low]",
            reports.filter(
                r => r.severity === "low"
            ).length
        );

    }


    function setText(
        selector,
        value
    ) {

        const element =
            document.querySelector(
                selector
            );


        if (element) {

            element.textContent =
                value;

        }

    }


    /* -----------------------------------------------------
       Escape HTML
    ----------------------------------------------------- */

    function escapeHTML(value) {

        return String(value)
            .replaceAll(
                "&",
                "&amp;"
            )
            .replaceAll(
                "<",
                "&lt;"
            )
            .replaceAll(
                ">",
                "&gt;"
            )
            .replaceAll(
                '"',
                "&quot;"
            )
            .replaceAll(
                "'",
                "&#039;"
            );

    }


    /* -----------------------------------------------------
       Map resize
    ----------------------------------------------------- */

    setTimeout(() => {

        map.invalidateSize();

    }, 500);

});