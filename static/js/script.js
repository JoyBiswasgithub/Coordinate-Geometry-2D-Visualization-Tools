function addEquationField() {
    const container = document.getElementById("equation-container");
    const newField = document.createElement("div");
    newField.classList.add("input-container");
    newField.innerHTML = `
        <input type="text" name="new_equation" placeholder="Enter new equation" required>
        <button type="button" onclick="removeEquationField(this)">Delete</button>
    `;
    container.appendChild(newField);
}

function removeEquationField(button) {
    const container = document.getElementById("equation-container");
    container.removeChild(button.parentElement);
}
