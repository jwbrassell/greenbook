<?php
header('Content-Type: application/json');

// Database configuration
$host = 'localhost';
$dbname = 'employees';
$username = 'user';
$password = 'password';

try {
    $pdo = new PDO("mysql:host=$host;dbname=$dbname", $username, $password);
    $pdo->setAttribute(PDO::ATTR_ERRMODE, PDO::ERRMODE_EXCEPTION);
} catch(PDOException $e) {
    die(json_encode([
        "draw" => 0,
        "recordsTotal" => 0,
        "recordsFiltered" => 0,
        "data" => [],
        "error" => "Connection failed: " . $e->getMessage()
    ]));
}

// DataTables parameters
$draw = isset($_POST['draw']) ? intval($_POST['draw']) : 1;
$start = isset($_POST['start']) ? intval($_POST['start']) : 0;
$length = isset($_POST['length']) ? intval($_POST['length']) : 10;
$search = isset($_POST['search']['value']) ? $_POST['search']['value'] : '';
$orderColumn = isset($_POST['order'][0]['column']) ? intval($_POST['order'][0]['column']) : 0;
$orderDir = isset($_POST['order'][0]['dir']) ? $_POST['order'][0]['dir'] : 'ASC';

// Columns for ordering
$columns = [
    0 => 'name',
    1 => 'position',
    2 => 'office',
    3 => 'age',
    4 => 'start_date',
    5 => 'salary'
];

// Base query
$query = "SELECT SQL_CALC_FOUND_ROWS 
            id, name, position, office, age, start_date, salary 
          FROM employees";

// Search condition
$searchCondition = "";
$params = [];
if (!empty($search)) {
    $searchCondition = " WHERE name LIKE :search 
                        OR position LIKE :search 
                        OR office LIKE :search";
    $params[':search'] = "%$search%";
}

// Column filters
$columnFilters = [];
for ($i = 0; $i < count($columns); $i++) {
    if (isset($_POST['columns'][$i]['search']['value']) && $_POST['columns'][$i]['search']['value'] !== '') {
        $columnFilters[] = $columns[$i] . " LIKE :filter$i";
        $params[":filter$i"] = "%" . $_POST['columns'][$i]['search']['value'] . "%";
    }
}

if (!empty($columnFilters)) {
    $searchCondition .= empty($searchCondition) ? " WHERE " : " AND ";
    $searchCondition .= implode(" AND ", $columnFilters);
}

$query .= $searchCondition;

// Ordering
$query .= " ORDER BY " . $columns[$orderColumn] . " " . $orderDir;

// Pagination
$query .= " LIMIT :start, :length";
$params[':start'] = $start;
$params[':length'] = $length;

try {
    // Execute main query
    $stmt = $pdo->prepare($query);
    foreach ($params as $key => &$value) {
        $stmt->bindParam($key, $value);
    }
    $stmt->execute();
    $data = $stmt->fetchAll(PDO::FETCH_ASSOC);

    // Get total records count
    $stmt = $pdo->query("SELECT FOUND_ROWS()");
    $recordsFiltered = $stmt->fetchColumn();

    // Get total records without filtering
    $stmt = $pdo->query("SELECT COUNT(*) FROM employees");
    $recordsTotal = $stmt->fetchColumn();

    // Format data for DataTables
    $formattedData = array_map(function($row) {
        // Format date
        $row['start_date'] = date('Y-m-d', strtotime($row['start_date']));
        // Format salary
        $row['salary'] = number_format($row['salary'], 2);
        return $row;
    }, $data);

    echo json_encode([
        "draw" => $draw,
        "recordsTotal" => $recordsTotal,
        "recordsFiltered" => $recordsFiltered,
        "data" => $formattedData
    ]);

} catch(PDOException $e) {
    echo json_encode([
        "draw" => $draw,
        "recordsTotal" => 0,
        "recordsFiltered" => 0,
        "data" => [],
        "error" => "Query failed: " . $e->getMessage()
    ]);
}
