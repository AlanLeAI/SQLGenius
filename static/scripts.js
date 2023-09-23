function addColumnField() {
    const columnFields = document.getElementById('columnFields');
    const columnField = document.createElement('div');
    columnField.className = 'form-group';
    const columnCount = columnFields.childElementCount + 1;

    columnField.innerHTML = `
        <label for="column_name_${columnCount}">Column Name:</label>
        <input type="text" class="form-control" id="column_name_${columnCount}" name="column_name_${columnCount}" required>

        <label for="column_datatype_${columnCount}">Data Type:</label>
        <select class="form-control" id="column_datatype_${columnCount}" name="column_datatype_${columnCount}" required>
            <option value="int">Integer</option>
            <option value="txt">Text</option>
            <option value="float">Float</option>
            <option value="date">Date</option>
        </select>

        <label for="column_condition_${columnCount}">Column Condition:</label>
        <select class="form-control" id="column_condition_${columnCount}" name="column_condition_${columnCount}">
            <option value="none">None</option>
            <option value="not_null">Not Null</option>
            <option value="primary_key">Primary Key</option>
        </select>
    `;

    columnFields.appendChild(columnField);
}

document.getElementById('addColumnBtn').addEventListener('click', addColumnField);


document.addEventListener('DOMContentLoaded', function () {
    const addTableButton = document.querySelector('#addTableBtn');
    const tableCreateDiv = document.querySelector('.table-create');

    addTableButton.addEventListener('click', function () {
        tableCreateDiv.style.display = 'flex';
    });
});
