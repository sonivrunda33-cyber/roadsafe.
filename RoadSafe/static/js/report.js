/* =========================================================
   ROADSAFE
   report.js
   Hazard reporting form
   ========================================================= */

document.addEventListener("DOMContentLoaded", () => {

    "use strict";


    const form =
        document.querySelector(
            ".report-form, #reportForm"
        );


    if (!form) return;


    /* -----------------------------------------------------
       File upload
    ----------------------------------------------------- */

    const fileInput =
        form.querySelector(
            "input[type='file']"
        );


    const uploadBox =
        form.querySelector(
            ".upload-box"
        );


    const preview =
        form.querySelector(
            ".upload-preview"
        );


    const previewImage =
        preview?.querySelector("img");


    if (fileInput) {

        fileInput.addEventListener(
            "change",
            () => {

                const file =
                    fileInput.files?.[0];


                if (!file) return;


                handleFile(file);

            }
        );

    }


    function handleFile(file) {

        if (!file.type.startsWith("image/")) {

            alert(
                "Please select a valid image."
            );

            fileInput.value = "";

            return;

        }


        const maxSize =
            5 * 1024 * 1024;


        if (file.size > maxSize) {

            alert(
                "Image size must be less than 5MB."
            );

            fileInput.value = "";

            return;

        }


        const reader =
            new FileReader();


        reader.onload =
            (event) => {

                if (
                    !preview ||
                    !previewImage
                ) return;


                previewImage.src =
                    event.target.result;


                preview.style.display =
                    "block";

            };


        reader.readAsDataURL(file);

    }


    /* -----------------------------------------------------
       Drag & Drop
    ----------------------------------------------------- */

    if (uploadBox) {

        uploadBox.addEventListener(
            "dragover",
            (event) => {

                event.preventDefault();

                uploadBox.classList.add(
                    "dragging"
                );

            }
        );


        uploadBox.addEventListener(
            "dragleave",
            () => {

                uploadBox.classList.remove(
                    "dragging"
                );

            }
        );


        uploadBox.addEventListener(
            "drop",
            (event) => {

                event.preventDefault();

                uploadBox.classList.remove(
                    "dragging"
                );


                const file =
                    event.dataTransfer.files?.[0];


                if (!file) return;


                const dataTransfer =
                    new DataTransfer();


                dataTransfer.items.add(
                    file
                );


                fileInput.files =
                    dataTransfer.files;


                handleFile(file);

            }
        );

    }


    /* -----------------------------------------------------
       Current location
    ----------------------------------------------------- */

    const locationButton =
        document.querySelector(
            "[data-get-location]"
        );


    const latitude =
        document.querySelector(
            "[name='latitude']"
        );


    const longitude =
        document.querySelector(
            "[name='longitude']"
        );


    const location =
        document.querySelector(
            "[name='location']"
        );


    if (locationButton) {

        locationButton.addEventListener(
            "click",
            getLocation
        );

    }


    function getLocation() {

        if (!navigator.geolocation) {

            alert(
                "Geolocation is not available."
            );

            return;

        }


        locationButton.disabled = true;

        locationButton.textContent =
            "LOCATING...";


        navigator.geolocation.getCurrentPosition(

            async (position) => {

                const lat =
                    position.coords.latitude;


                const lng =
                    position.coords.longitude;


                if (latitude) {

                    latitude.value =
                        lat;

                }


                if (longitude) {

                    longitude.value =
                        lng;

                }


                if (location) {

                    location.value =
                        `${lat.toFixed(6)}, ${lng.toFixed(6)}`;

                }


                locationButton.disabled =
                    false;


                locationButton.textContent =
                    "LOCATION FOUND";


                /*
                 * Reverse geocoding.
                 * This is optional.
                 */

                try {

                    const response =
                        await fetch(
                            "https://nominatim.openstreetmap.org/reverse" +
                            `?format=json&lat=${lat}&lon=${lng}`,
                            {
                                headers: {
                                    "Accept":
                                        "application/json"
                                }
                            }
                        );


                    if (!response.ok) {
                        return;
                    }


                    const data =
                        await response.json();


                    if (
                        location &&
                        data.display_name
                    ) {

                        location.value =
                            data.display_name;

                    }

                } catch (error) {

                    console.log(
                        "Could not get address."
                    );

                }

            },

            () => {

                locationButton.disabled =
                    false;


                locationButton.textContent =
                    "USE MY LOCATION";


                alert(
                    "Unable to access your location."
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
       Character counter
    ----------------------------------------------------- */

    document.querySelectorAll(
        "textarea[maxlength]"
    ).forEach((textarea) => {

        const counter =
            document.querySelector(
                `[data-counter-for="${textarea.id}"]`
            );


        const update =
            () => {

                if (!counter) return;


                counter.textContent =
                    `${textarea.value.length}/${textarea.maxLength}`;

            };


        textarea.addEventListener(
            "input",
            update
        );


        update();

    });


    /* -----------------------------------------------------
       Form progress
    ----------------------------------------------------- */

    const progress =
        document.querySelector(
            ".progress-bar"
        );


    function updateProgress() {

        if (!progress) return;


        const fields =
            form.querySelectorAll(
                "input[required], textarea[required], select[required]"
            );


        if (!fields.length) return;


        let completed = 0;


        fields.forEach((field) => {

            if (
                field.type === "radio"
            ) {

                return;

            }


            if (
                field.value.trim()
            ) {

                completed++;

            }

        });


        const radioNames =
            new Set();


        form.querySelectorAll(
            "input[type='radio'][required]"
        ).forEach((radio) => {

            radioNames.add(
                radio.name
            );

        });


        radioNames.forEach(
            (name) => {

                if (
                    form.querySelector(
                        `input[name="${CSS.escape(name)}"]:checked`
                    )
                ) {

                    completed++;

                }

            }
        );


        const percentage =
            Math.round(
                (completed /
                    fields.length) *
                100
            );


        progress.style.width =
            `${Math.min(
                percentage,
                100
            )}%`;

    }


    form.addEventListener(
        "input",
        updateProgress
    );


    form.addEventListener(
        "change",
        updateProgress
    );


    updateProgress();


    /* -----------------------------------------------------
       Submit validation
    ----------------------------------------------------- */

    form.addEventListener(
        "submit",
        (event) => {

            if (!form.checkValidity()) {

                event.preventDefault();

                form.reportValidity();

                return;

            }


            const button =
                form.querySelector(
                    "button[type='submit']"
                );


            if (button) {

                button.disabled = true;

                button.classList.add(
                    "loading"
                );

                button.innerHTML =
                    "SUBMITTING...";

            }

        }
    );

});