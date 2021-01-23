<?php
session_start();
?>
<!DOCTYPE html>
<html>

	<head>
		<meta charset="utf-8">
			<title>Controllo utente</title>
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

			<?php
	$utente = "";
	if (isset($_POST['utente'])) {
		$utente = $_POST['utente'];
	}

	$password = "";
	if (isset($_POST['password'])) {
		$password = $_POST['password'];
	}
	
	$codicebiglietto = "";
	if (isset($_POST['codicebiglietto'])) {
		$codicebiglietto = $_POST['codicebiglietto'];
	}
	echo "<h1> codicebiglietto:" . $codicebiglietto . "</h1>";
	echo "<h1> utente:" . $utente . "</h1>";
	echo "<h1> password:" . $password . "</h1>";
	?>

			<hr />

			<?php

	define('DB_SERVER', 'localhost');
	define('DB_USERNAME', 'root');
	define('DB_PASSWORD', '');
	define('DB_NAME', 'museo');

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
	$sql = "SELECT * FROM codicerandom WHERE codicerandom = '".$codicebiglietto."'";
	$result = $mysqli->query($sql);
	if ($result) {
        if ($mysqli->affected_rows > 0) {
	
		$sql = "INSERT INTO utente ";
		$sql .= "(utente, password, admin) ";
		$sql .= "VALUES ";
		$sql .= "('" . $utente . "', '" . $password . "', '0') ";
	
	
		echo "<pre>" . $sql . "</pre>";
	
		$result = $mysqli->query($sql);

		if ($result) {
			if ($mysqli->affected_rows > 0) {
				header('Location: 01login.php?errore=registrazionecorretta');
				} else {
				header('Location: 01login.php?errore=utentegiaregistrato');
			}
        // $result->close();
		} else {
			header('Location: 01login.php?errore=registrazionesbagliata');
		}
		} else {
		header('Location: 01login.php?errore=codicesbagliato');
		}
	}
	
	$mysqli->close();
	?>
</body>
</html>