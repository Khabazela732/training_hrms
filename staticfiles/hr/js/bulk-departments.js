// Senzo department bulk creation JavaScript
let rowCounter = 1;

function addRow() {
    rowCounter++;
    const tbody = document.getElementById('departmentRows');
    const newRow = document.createElement('tr');
    newRow.className = 'table-row';
    newRow.dataset.row = rowCounter;
    newRow.innerHTML = `
        <td class="row-number">${rowCounter}</td>
        <td><input type="text" name="dept_name_${rowCounter}" class="form-control" placeholder="e.g. IT Department" required></td>
        <td><input type="text" name="dept_desc_${rowCounter}" class="form-control" placeholder="e.g. Handles IT support..."></td>
        <td><button type="button" class="remove-row-btn" onclick="removeRow(${rowCounter})">×</button></td>
    `;
    tbody.appendChild(newRow);
    updateRowNumbers();
}

function removeRow(rowNum) {
    const row = document.querySelector(`[data-row="${rowNum}"]`);
    if (row) {
        row.remove();
        updateRowNumbers();
    }
}

function updateRowNumbers() {
    const rows = document.querySelectorAll('#departmentRows tr');
    rows.forEach((row, index) => {
        const rowNum = index + 1;
        row.dataset.row = rowNum;
        row.querySelector('.row-number').textContent = rowNum;
        
        const nameInput = row.querySelector('input[name^="dept_name_"]');
        const descInput = row.querySelector('input[name^="dept_desc_"]');
        
        if (nameInput) nameInput.name = `dept_name_${rowNum}`;
        if (descInput) descInput.name = `dept_desc_${rowNum}`;
    });
    
    rowCounter = rows.length;
    document.getElementById('rowCount').textContent = `${rows.length} row${rows.length !== 1 ? 's' : ''}`;
    updateRemoveButtons();
}

function updateRemoveButtons() {
    const rows = document.querySelectorAll('#departmentRows tr');
    rows.forEach(row => {
        const removeBtn = row.querySelector('.remove-row-btn');
        removeBtn.style.display = rows.length > 1 ? 'block' : 'none';
    });
}

document.addEventListener('DOMContentLoaded', function() {
    updateRemoveButtons();
    updateRowNumbers();
});