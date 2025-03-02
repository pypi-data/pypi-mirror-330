/* Copyright 2024 Louis Paternault
 *
 * This file is part of pdfimpose-web.
 *
 * Pdfimpose-web is free software: you can redistribute it and/or modify it
 * under the terms of the GNU Affero General Public License as published by the
 * Free Software Foundation, either version 3 of the License, or (at your
 * option) any later version.
 *
 * Pdfimpose-web is distributed in the hope that it will be useful, but WITHOUT
 * ANY WARRANTY; without even the implied warranty of MERCHANTABILITY or FITNESS
 * FOR A PARTICULAR PURPOSE. See the GNU Affero General Public License for more
 * details.
 *
 * You should have received a copy of the GNU Affero General Public License
 * along with pdfimpose-web. If not, see <https://www.gnu.org/licenses/>.
 */

////////////////////////////////////////////////////////////////////////////////
// Select layout

var forms = [];

function layout_init_forms() {
    // Remove layout forms, and store them in `forms`
    // They will be added back when user selects the corresponding layout
    for (const layout of layouts) {
        forms[layout] = document.getElementById("form").removeChild(document.getElementById("form-" + layout));
    };
}

layout_init_forms();

function layout_select(layout) {
    document.getElementById("no-layout-description").hidden = true;
    document.getElementById("no-layout-form").hidden = true;
    document.getElementById("layout").value = layout;
    document.getElementById("submit").disabled = false;
    document.getElementById("form").appendChild(forms[layout]);
    document.getElementById("layout-button-unselect-" + layout).hidden = false;
    document.getElementById("layout-button-select-" + layout).hidden = true;
    document.getElementById("layout-description-" + layout).hidden = false;
    for (const other of layouts) {
        if (layout != other) {
            document.getElementById("layout-card-" + other).hidden = true;
        }
    };
}

function layout_unselect(layout) {
    document.getElementById("no-layout-form").hidden = false;
    document.getElementById("no-layout-description").hidden = false;
    document.getElementById("layout").value = "";
    document.getElementById("submit").disabled = true;
    forms[layout] = document.getElementById("form").removeChild(document.getElementById("form-" + layout));
    document.getElementById("layout-button-unselect-" + layout).hidden = true;
    document.getElementById("layout-button-select-" + layout).hidden = false;
    document.getElementById("layout-description-" + layout).hidden = true;
    for (const other of layouts) {
        if (layout != other) {
            document.getElementById("layout-card-" + other).hidden = false;
        }
    };
}

////////////////////////////////////////////////////////////////////////////////
// Error messages
function adderror(category, keyword, filename, message) {
    var li = document.createElement("li");
    li.innerHTML = `${gettext[keyword]} (${gettext["FILE"]} <code>${filename}</code>): ${message}`;

    const messages = document.getElementById(`messages-${category}`);
    messages.hidden = false;
    messages.querySelector("div > ul").appendChild(li);
}

function cleanmessages(categories) {
    for (const category of categories ){
        const messages = document.getElementById(`messages-${category}`);
        if (messages !== null) {
            messages.querySelector("div > ul").replaceChildren();
            messages.hidden = true;
        }
    }
}

////////////////////////////////////////////////////////////////////////////////
// Drag and drop
// Thanks to Nikita Hlopov for his tutorial
// https://nikitahl.com/custom-styled-input-type-file

const uploadlabel = document.getElementById("upload-label")
const uploadinput = document.getElementById("upload-input")

uploadlabel.addEventListener("drop", (event) => {
    event.preventDefault()
    uploadlabel.classList.remove("drag-active")
    uploadinput.files = event.dataTransfer.files
})

uploadlabel.addEventListener("change", (event) => {
    // Check file name
    file = uploadinput.files[0];
    if (! file.name.endsWith(".pdf")) {
        adderror("files", "ERROR", file.name, gettext["FILE_DOES_NOT_END_WITH_PDF"]);
        uploadinput.value = "";
        return;
    }
    // Check file size
    if (file.size > max_size) {
        adderror("files", "ERROR", file.name, gettext["FILE_TOO_BIG"])
        uploadinput.value = "";
        return;
    }

    // Load PDF with pdf-lib for further tests
    const reader = new FileReader();
    reader.readAsArrayBuffer(file);
    reader.onload = () => {
        PDFLib.PDFDocument.load(reader.result).then((pdf) => {
            var widths = new Set();
            var heights = new Set();
            for (const page of pdf.getPages()) {
                widths.add(page.getWidth());
                heights.add(page.getHeight());
            }
            if (
                (100 * (Math.max(...widths)-Math.min(...widths)) > Math.min(...widths))
                ||
                (100 * (Math.max(...heights)-Math.min(...heights)) > Math.min(...heights))
            ) {
                adderror("files", "WARNING", file.name, gettext["PAGES_HAVE_DIFFERENT_SIZES"]);
            }
        })
        .catch((error) => {
            // File is not a valid PDF
            adderror("files", "ERROR", file.name, error);
            uploadinput.value = "";
            return;
        });
    };


})

////////////////////////////////////////////////////////////////////////////////
// When an input tag get focus, check the parent radio button.
function checkparentradio(me) {
        me.closest(".form-check").querySelector("label > input[type=radio]").checked = true;
}
