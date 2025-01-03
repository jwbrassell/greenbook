<?php
$host = 'localhost';
$dbname = 'employees';
$username = 'user';
$password = 'password';
?>

<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>DataTables PHP Example</title>
    
    <!-- CSS -->
    <link rel="stylesheet" type="text/css" href="https://cdn.datatables.net/1.13.7/css/jquery.dataTables.css">
    <link rel="stylesheet" type="text/css" href="https://cdn.datatables.net/buttons/2.4.2/css/buttons.dataTables.min.css">
    
    <!-- JavaScript -->
    <script type="text/javascript" src="https://code.jquery.com/jquery-3.7.0.min.js"></script>
    <script type="text/javascript" src="https://cdn.datatables.net/1.13.7/js/jquery.dataTables.min.js"></script>
    <script type="text/javascript" src="https://cdn.datatables.net/buttons/2.4.2/js/dataTables.buttons.min.js"></script>
</head>
<body>
    <div class="container">
        <h1>Employees DataTable</h1>
        
        <!-- Filter Controls -->
        <div class="filters">
            <label>Age Range:</label>
            <input type="number" id="min" placeholder="Min age">
            <input type="number" id="max" placeholder="Max age">
        </div>

        <!-- DataTable -->
        <table id="employeesTable" class="display">
            <thead>
                <tr>
                    <th>Name</th>
                    <th>Position</th>
                    <th>Office</th>
                    <th>Age</th>
                    <th>Start date</th>
                    <th>Salary</th>
                    <th>Actions</th>
                </tr>
            </thead>
            <tfoot>
                <tr>
                    <th>Name</th>
                    <th>Position</th>
                    <th>Office</th>
                    <th>Age</th>
                    <th>Start date</th>
                    <th>Salary</th>
                    <th>Actions</th>
                </tr>
            </tfoot>
        </table>
    </div>

    <script>
    $(document).ready(function() {
        // Initialize DataTable
        var table = $('#employeesTable').DataTable({
            processing: true,
            serverSide: true,
            ajax: {
                url: 'server_processing.php',
                type: 'POST'
            },
            columns: [
                { data: 'name' },
                { data: 'position' },
                { data: 'office' },
                { data: 'age' },
                { data: 'start_date' },
                { 
                    data: 'salary',
                    render: function(data, type, row) {
                        return '$' + parseFloat(data).toLocaleString();
                    }
                },
                {
                    data: null,
                    render: function(data, type, row) {
                        return '<button onclick="editEmployee(' + row.id + ')" class="btn-edit">Edit</button>' +
                               '<button onclick="deleteEmployee(' + row.id + ')" class="btn-delete">Delete</button>';
                    }
                }
            ],
            dom: 'Bfrtip',
            buttons: [
                'copy', 'csv', 'excel', 'pdf', 'print'
            ],
            initComplete: function () {
                // Add column-specific filtering
                this.api().columns().every(function () {
                    var column = this;
                    var select = $('<select><option value=""></option></select>')
                        .appendTo($(column.footer()).empty())
                        .on('change', function () {
                            var val = $.fn.dataTable.util.escapeRegex(
                                $(this).val()
                            );
                            column
                                .search(val ? '^' + val + '$' : '', true, false)
                                .draw();
                        });
 
                    column.data().unique().sort().each(function (d, j) {
                        select.append('<option value="' + d + '">' + d + '</option>')
                    });
                });
            }
        });

        // Custom age range filtering
        $.fn.dataTable.ext.search.push(
            function(settings, data, dataIndex) {
                var min = parseInt($('#min').val(), 10);
                var max = parseInt($('#max').val(), 10);
                var age = parseFloat(data[3]) || 0;

                if ((isNaN(min) && isNaN(max)) ||
                    (isNaN(min) && age <= max) ||
                    (min <= age && isNaN(max)) ||
                    (min <= age && age <= max)) {
                    return true;
                }
                return false;
            }
        );

        // Update table when age range inputs change
        $('#min, #max').keyup(function() {
            table.draw();
        });
    });

    // Employee management functions
    function editEmployee(id) {
        // Implement edit functionality
        console.log('Editing employee:', id);
    }

    function deleteEmployee(id) {
        if (confirm('Are you sure you want to delete this employee?')) {
            $.ajax({
                url: 'delete_employee.php',
                type: 'POST',
                data: { id: id },
                success: function(response) {
                    if (response.success) {
                        $('#employeesTable').DataTable().ajax.reload();
                    } else {
                        alert('Error deleting employee');
                    }
                }
            });
        }
    }
    </script>

    <style>
    .container {
        margin: 20px;
        padding: 20px;
    }

    .filters {
        margin-bottom: 20px;
    }

    .filters input {
        margin: 0 10px;
        padding: 5px;
    }

    .btn-edit, .btn-delete {
        margin: 0 5px;
        padding: 5px 10px;
        border: none;
        border-radius: 3px;
        cursor: pointer;
    }

    .btn-edit {
        background-color: #4CAF50;
        color: white;
    }

    .btn-delete {
        background-color: #f44336;
        color: white;
    }
    </style>
</body>
</html>
