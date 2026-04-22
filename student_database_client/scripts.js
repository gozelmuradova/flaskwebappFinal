const API_BASE = 'https://gozelMuradova.pythonanywhere.com';

function buildTable(students) {
    if (students.length === 0) {
        return '<p>No students found.</p>';
    }

    let rows = students.map(s => `
        <tr>
            <td>${s.id}</td>
            <td>${s.first_name}</td>
            <td>${s.last_name}</td>
            <td>${s.email}</td>
            <td>${s.major}</td>
            <td>${s.classification}</td>
        </tr>
    `).join('');

    return `
        <table>
            <thead>
                <tr>
                    <th>ID</th>
                    <th>First Name</th>
                    <th>Last Name</th>
                    <th>Email</th>
                    <th>Major</th>
                    <th>Classification</th>
                </tr>
            </thead>
            <tbody>${rows}</tbody>
        </table>
    `;
}



function showMessage(elementId, text, isError = false) {
    const el = document.getElementById(elementId);
    el.textContent = text;
    el.className = isError ? 'message error' : 'message success';
}


async function getAllStudents() {
    const output = document.getElementById('all-students-output');
    output.innerHTML = '<p>Loading...</p>';

    try {
        const response = await fetch(`${API_BASE}/api/students`);
        const students = await response.json();
        output.innerHTML = buildTable(students);
    } catch (error) {
        output.innerHTML = '<p class="error">Failed to load students. Is the server running?</p>';
    }
}

async function getStudentById() {
    const id     = document.getElementById('view-id').value.trim();
    const output = document.getElementById('one-student-output');

    if (!id) {
        output.innerHTML = '<p class="error">Please enter a student ID.</p>';
        return;
    }

    output.innerHTML = '<p>Loading...</p>';

    try {
        const response = await fetch(`${API_BASE}/api/students/${id}`);
        const data     = await response.json();

        if (!response.ok) {
            output.innerHTML = `<p class="error">${data.error}</p>`;
            return;
        }

        output.innerHTML = buildTable([data]);
    } catch (error) {
        output.innerHTML = '<p class="error">Request failed. Is the server running?</p>';
    }
}


async function createStudent() {
    const body = {
        first_name:     document.getElementById('create-first').value.trim(),
        last_name:      document.getElementById('create-last').value.trim(),
        email:          document.getElementById('create-email').value.trim(),
        major:          document.getElementById('create-major').value.trim(),
        classification: document.getElementById('create-classification').value,
    };

    // Basic client-side validation
    if (Object.values(body).some(v => !v)) {
        showMessage('create-message', 'Please fill in all fields.', true);
        return;
    }

    try {
        const response = await fetch(`${API_BASE}/api/students`, {
            method:  'POST',
            headers: { 'Content-Type': 'application/json' },
            body:    JSON.stringify(body),
        });

        const data = await response.json();

        if (!response.ok) {
            showMessage('create-message', data.error, true);
            return;
        }

        showMessage('create-message', 'Student created successfully!');

        // Clear form inputs
        ['create-first', 'create-last', 'create-email', 'create-major'].forEach(id => {
            document.getElementById(id).value = '';
        });
        document.getElementById('create-classification').value = '';

    } catch (error) {
        showMessage('create-message', 'Request failed. Is the server running?', true);
    }
}

async function updateStudent() {
    const id   = document.getElementById('update-id').value.trim();
    const body = {
        first_name:     document.getElementById('update-first').value.trim(),
        last_name:      document.getElementById('update-last').value.trim(),
        email:          document.getElementById('update-email').value.trim(),
        major:          document.getElementById('update-major').value.trim(),
        classification: document.getElementById('update-classification').value,
    };

    if (!id) {
        showMessage('update-message', 'Please enter a student ID.', true);
        return;
    }

    if (Object.values(body).some(v => !v)) {
        showMessage('update-message', 'Please fill in all fields.', true);
        return;
    }

    try {
        const response = await fetch(`${API_BASE}/api/students/${id}`, {
            method:  'PUT',
            headers: { 'Content-Type': 'application/json' },
            body:    JSON.stringify(body),
        });

        const data = await response.json();

        if (!response.ok) {
            showMessage('update-message', data.error, true);
            return;
        }

        showMessage('update-message', 'Student updated successfully!');

    } catch (error) {
        showMessage('update-message', 'Request failed. Is the server running?', true);
    }
}

async function deleteStudent() {
    const id = document.getElementById('delete-id').value.trim();

    if (!id) {
        showMessage('delete-message', 'Please enter a student ID.', true);
        return;
    }

    try {
        const response = await fetch(`${API_BASE}/api/students/${id}`, {
            method: 'DELETE',
        });

        const data = await response.json();

        if (!response.ok) {
            showMessage('delete-message', data.error, true);
            return;
        }

        showMessage('delete-message', 'Student deleted successfully!');
        document.getElementById('delete-id').value = '';

    } catch (error) {
        showMessage('delete-message', 'Request failed. Is the server running?', true);
    }
}
