
async function getTables() {
    try {
        const response = await fetch('/get_tables', {
            method: 'GET',
            headers: {
                'Content-Type': 'application/json',
            },
        });

        if (!response.ok) {
            throw new Error('Error fetching tables');
        }

        const data = await response.json();
        return data.tables;
    } catch (error) {
        console.error('Error:', error);
        return [];
    }
}



async function addColumnField() {
    const columnFields = document.getElementById('columnFields');
    
    const columnField = document.createElement('div');
    columnField.className = 'form-group';
    const columnCount = columnFields.childElementCount + 1;

    const tables = await getTables();


    columnField.innerHTML = `
        <h2> Colume ${columnCount}</h2>
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
            <option value="none">Null</option>
            <option value="not_null">Not Null</option>
            <option value="primary_key">Primary Key</option>
            <option value="foreign_key">Foreign Key</option>
        </select>

        <div id="foreign_key_${columnCount}" style="display: none;">
            <label for="column_reference_table_${columnCount}">Reference Table:</label>
            <select class="form-control" id="column_reference_table_${columnCount}" name="column_reference_table_${columnCount}">
                ${tables.map(table => `<option value="${table.name}">${table.name}</option>`).join('')}
            </select>
        </div>
    `;
    // Show/hide reference table select based on the column condition
    const conditionSelect = columnField.querySelector(`#column_condition_${columnCount}`);
    const foreignKeyDiv = columnField.querySelector(`#foreign_key_${columnCount}`);
    conditionSelect.addEventListener('change', function () {
        if (conditionSelect.value === 'foreign_key') {
            foreignKeyDiv.style.display = 'block';
        } else {
            foreignKeyDiv.style.display = 'none';
        }
    });

    columnFields.appendChild(columnField);
}

document.getElementById('addColumnBtn').addEventListener('click', addColumnField);


document.addEventListener('DOMContentLoaded', function () {
    const addTableButton = document.querySelector('#addTableBtn');
    const tableCreateDiv = document.querySelector('.table-create');
    const editTableButton = document.querySelector('#editTableBtn');
    const tableEditDiv = document.querySelector('.table-edit');

    const info = document.getElementById('info');
    

    addTableButton.addEventListener('click', function () {
        tableCreateDiv.style.display = 'flex';
        tableEditDiv.style.display = 'none';
        info.style.display = "none"
    });


    editTableButton.addEventListener('click', function(){
        tableEditDiv.style.display = 'flex';
        info.style.display = "none";
        tableCreateDiv.style.display = 'none';

    })
});



$(document).ready(function() {
    $('#table_name_edit').change(function() {
        var tableName = $('#table_name_edit').val();
        if (tableName != "") {
            $.ajax({
                url: '/get_columns/' + tableName,
                method: 'GET',
                success: function(data) {
                    var columns = data.columns;
                    var selectElement = $('#column_name_edit');
                    selectElement.empty();
                    selectElement.append('<option value="null">None</option>');

                    for (var i = 0; i < columns.length; i++) {
                        var columnName = columns[i];
                        selectElement.append('<option value="' + columnName + '">' + columnName + '</option>');
                    }
                }
            });
        }
    });
});


