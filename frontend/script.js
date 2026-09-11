// ==========================================
// BACKEND URL
// ==========================================

// For now your FastAPI is running locally.
const API_URL = "http://127.0.0.1:8000";


let students = [];


// ==========================================
// SHOW MESSAGE
// ==========================================

function showMessage(id, message, success = false) {

    const element = document.getElementById(id);

    element.textContent = message;

    element.style.color =
        success ? "#15803d" : "#b4233c";
}


// ==========================================
// CALCULATE STATISTICS
// ==========================================

function calculateStats(data) {

    const total = data.length;

    const marks = data
        .map(student => Number(student.marks))
        .filter(mark => !Number.isNaN(mark));


    const average = marks.length
        ? (
            marks.reduce(
                (a, b) => a + b,
                0
            ) / marks.length
        ).toFixed(2)
        : 0;


    const highest = marks.length
        ? Math.max(...marks)
        : 0;


    document.getElementById(
        "totalStudents"
    ).textContent = total;


    document.getElementById(
        "averageMarks"
    ).textContent = average;


    document.getElementById(
        "highestMarks"
    ).textContent = highest;
}


// ==========================================
// DISPLAY TABLE
// ==========================================

function renderTable(tableId, data) {

    const tbody =
        document.getElementById(tableId);


    tbody.innerHTML = "";


    if (data.length === 0) {

        tbody.innerHTML = `
            <tr>
                <td colspan="4">
                    No student records found.
                </td>
            </tr>
        `;

        return;
    }


    data.forEach(student => {

        const row =
            document.createElement("tr");


        row.innerHTML = `

            <td>
                ${student.id ?? ""}
            </td>

            <td>
                ${student.name ?? ""}
            </td>

            <td>
                ${student.course ?? ""}
            </td>

            <td>
                ${student.marks ?? ""}
            </td>

        `;


        tbody.appendChild(row);

    });
}


// ==========================================
// UPDATE ALL TABLES
// ==========================================

function renderAllTables() {

    renderTable(
        "studentTable",
        students
    );


    renderTable(
        "updateTable",
        students
    );


    renderTable(
        "deleteTable",
        students
    );


    calculateStats(students);
}


// ==========================================
// GET STUDENTS
// ==========================================

async function loadStudents() {

    try {

        const response =
            await fetch(
                `${API_URL}/students`
            );


        if (!response.ok) {

            throw new Error(
                await response.text()
            );

        }


        const result =
            await response.json();


        students =
            result.data || [];


        renderAllTables();


        showMessage(
            "dashboardMessage",
            "Records refreshed successfully.",
            true
        );


    } catch (error) {

        console.error(error);


        showMessage(
            "dashboardMessage",
            "Backend connection error. Check API URL and CORS."
        );

    }
}


// ==========================================
// ADD STUDENT
// ==========================================

async function addStudent() {

    const name =
        document
            .getElementById("addName")
            .value
            .trim();


    const course =
        document
            .getElementById("addCourse")
            .value
            .trim();


    const marksValue =
        document
            .getElementById("addMarks")
            .value;


    if (!name) {

        return showMessage(
            "addStatus",
            "⚠️ Please enter student name."
        );

    }


    if (!course) {

        return showMessage(
            "addStatus",
            "⚠️ Please enter course."
        );

    }


    if (marksValue === "") {

        return showMessage(
            "addStatus",
            "⚠️ Please enter marks."
        );

    }


    const marks =
        Number(marksValue);


    if (
        !Number.isInteger(marks) ||
        marks < 0 ||
        marks > 100
    ) {

        return showMessage(
            "addStatus",
            "⚠️ Marks must be between 0 and 100."
        );

    }


    try {

        const params =
            new URLSearchParams({

                name: name,

                course: course,

                marks: marks

            });


        const response =
            await fetch(
                `${API_URL}/students?${params}`,
                {
                    method: "POST"
                }
            );


        if (!response.ok) {

            throw new Error(
                await response.text()
            );

        }


        showMessage(
            "addStatus",
            "✅ Student added successfully!",
            true
        );


        document.getElementById(
            "addName"
        ).value = "";


        document.getElementById(
            "addCourse"
        ).value = "";


        document.getElementById(
            "addMarks"
        ).value = "";


        await loadStudents();


    } catch (error) {

        console.error(error);


        showMessage(
            "addStatus",
            "❌ Backend connection error or request failed."
        );

    }
}


// ==========================================
// UPDATE STUDENT
// ==========================================

async function updateStudent() {

    const idValue =
        document
            .getElementById("updateId")
            .value;


    const name =
        document
            .getElementById("updateName")
            .value
            .trim();


    const course =
        document
            .getElementById("updateCourse")
            .value
            .trim();


    const marksValue =
        document
            .getElementById("updateMarks")
            .value;


    if (!idValue) {

        return showMessage(
            "updateStatus",
            "⚠️ Please enter Student ID."
        );

    }


    if (!name) {

        return showMessage(
            "updateStatus",
            "⚠️ Please enter student name."
        );

    }


    if (!course) {

        return showMessage(
            "updateStatus",
            "⚠️ Please enter course."
        );

    }


    if (marksValue === "") {

        return showMessage(
            "updateStatus",
            "⚠️ Please enter marks."
        );

    }


    const id =
        Number(idValue);


    const marks =
        Number(marksValue);


    if (
        !Number.isInteger(id) ||
        id < 1
    ) {

        return showMessage(
            "updateStatus",
            "⚠️ Student ID must be a valid number."
        );

    }


    if (
        !Number.isInteger(marks) ||
        marks < 0 ||
        marks > 100
    ) {

        return showMessage(
            "updateStatus",
            "⚠️ Marks must be between 0 and 100."
        );

    }


    try {

        const params =
            new URLSearchParams({

                name: name,

                course: course,

                marks: marks

            });


        const response =
            await fetch(
                `${API_URL}/students/${id}?${params}`,
                {
                    method: "PUT"
                }
            );


        if (!response.ok) {

            throw new Error(
                await response.text()
            );

        }


        showMessage(
            "updateStatus",
            "✅ Student updated successfully!",
            true
        );


        await loadStudents();


    } catch (error) {

        console.error(error);


        showMessage(
            "updateStatus",
            "❌ Backend connection error or request failed."
        );

    }
}


// ==========================================
// DELETE STUDENT
// ==========================================

async function deleteStudent() {

    const idValue =
        document
            .getElementById("deleteId")
            .value;


    if (!idValue) {

        return showMessage(
            "deleteStatus",
            "⚠️ Please enter Student ID."
        );

    }


    const id =
        Number(idValue);


    if (
        !Number.isInteger(id) ||
        id < 1
    ) {

        return showMessage(
            "deleteStatus",
            "⚠️ Student ID must be a valid number."
        );

    }


    const confirmed =
        confirm(
            `Are you sure you want to delete student ${id}?`
        );


    if (!confirmed) {

        return;

    }


    try {

        const response =
            await fetch(
                `${API_URL}/students/${id}`,
                {
                    method: "DELETE"
                }
            );


        if (!response.ok) {

            throw new Error(
                await response.text()
            );

        }


        showMessage(
            "deleteStatus",
            "✅ Student deleted successfully!",
            true
        );


        document.getElementById(
            "deleteId"
        ).value = "";


        await loadStudents();


    } catch (error) {

        console.error(error);


        showMessage(
            "deleteStatus",
            "❌ Backend connection error or request failed."
        );

    }
}


// ==========================================
// TAB NAVIGATION
// ==========================================

document
    .querySelectorAll(".tab")
    .forEach(button => {

        button.addEventListener(
            "click",
            () => {

                document
                    .querySelectorAll(".tab")
                    .forEach(btn =>
                        btn.classList.remove("active")
                    );


                document
                    .querySelectorAll(".tab-content")
                    .forEach(section =>
                        section.classList.remove("active")
                    );


                button.classList.add("active");


                document
                    .getElementById(
                        button.dataset.tab
                    )
                    .classList.add("active");

            }
        );

    });


// ==========================================
// LOAD DATA WHEN PAGE OPENS
// ==========================================

loadStudents();