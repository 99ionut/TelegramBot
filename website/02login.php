<?php
session_start();
?>
<!DOCTYPE html>
<html>

<head>
	<meta charset="utf-8">

	<style>
		table {
			border-collapse: collapse;
		}
		
		table,
		th,
		td {
			border: 1px solid black;
		}
		.simbolo {
			width: 100px;
		}
	</style>
</head>

<body>

	<hr />

	<?php
	$utente = "";
	if (isset($_POST['utente'])) {
		$utente = $_POST['utente'];
	}

	$password = "";
	if (isset($_POST['password'])) {
		$password = $_POST['password'];
	}

	echo "<h1> utente:" . $utente . "</h1>";
	echo "<h1> password:" . $password . "</h1>";
	$_SESSION['utente'] = $utente;
	?>
	<hr />

	<?php

	define('DB_SERVER', 'localhost');
	define('DB_USERNAME', 'root');
	define('DB_PASSWORD', '');
	define('DB_NAME', 'telegrambot');

	// connessione
	$mysqli = new mysqli(DB_SERVER, DB_USERNAME, DB_PASSWORD, DB_NAME);
	if ($mysqli->connect_errno) {
		printf("Connect failed: %s\n", $mysqli->connect_error);
		exit();
	}
	// charset utf-8
	$mysqli->set_charset("utf8");

	// SQLinjection
	$utente = $mysqli->real_escape_string($utente);
	$password = $mysqli->real_escape_string($password);
	
	// query
	
	$sql = "SELECT * FROM admin WHERE username = '" . $utente . "' ";
	
	
	echo "<pre>" . $sql . "</pre>";
	
	$result = $mysqli->query($sql);

	if ($result) {
		if ($result->num_rows == 1) {
			while ($row = $result->fetch_array()) {
				if (($password) == $row['password']) {
					//
					echo "OK";
					
					$_SESSION['login'] = 'ok';

					header('Location: 03login.php');

				} else {
					header('Location: 01login.php?errore=password');
				}
			}
		} else {
			header('Location: 01login.php?errore=registrazione');
		}
		$result->close();
	} else {
		echo "ERRORE";
	}

	$mysqli->close();

	?>

	<a href="01login.php" title="back to login"> LOGIN</a>
</body>

</html>