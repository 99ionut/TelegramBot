<!DOCTYPE html>
<html>
<?php
session_start();
if (isset($_SESSION['login']) && $_SESSION['login'] == 'ok') {
	//echo "sessione ok";
} else {
	//echo "pagina protetta";
	
	header('Location: 01login.php');
	exit;
}
?>
<head>
<script src="https://ajax.googleapis.com/ajax/libs/jquery/3.5.1/jquery.min.js"></script>
<link rel="stylesheet" type="text/css" href="https://cdn.datatables.net/1.10.23/css/jquery.dataTables.css">
<script type="text/javascript" charset="utf8" src="https://cdn.datatables.net/1.10.23/js/jquery.dataTables.js"></script>
<link href="https://stackpath.bootstrapcdn.com/bootstrap/4.4.1/css/bootstrap.min.css" rel="stylesheet">
<link href="https://stackpath.bootstrapcdn.com/font-awesome/4.7.0/css/font-awesome.min.css" rel="stylesheet" type="text/css">
<link rel="stylesheet" href="https://unpkg.com/purecss@2.0.5/build/pure-min.css" integrity="sha384-LTIDeidl25h2dPxrB2Ekgc9c7sEC3CWGM6HeFmuDNUjX76Ert4Z4IY714dhZHPLd" crossorigin="anonymous">


	<meta charset="utf-8">
	<title>EarnDogeToday </title>
	<style>
		table {
			border-collapse: collapse;
		}
		.card-body{
			padding:0px;
		}
		body {
			background-color:#f8f9fa!important;
		}

		tr:hover {
			background-color:lightgray!important;
		}

		.simbolo {
			width: 100px;
		}
		
		#transactionTable_wrapper{
			margin:50px;
		}
		
		.odd {
			background-color: #e6e6e6!important;
		}
		
		thead{
			background-color: #ffff008f!important;
			
		}
		
		#transactionTable_wrapper {
			background-color:#ffcd66!important;
		}
		
		input[type="search"] {
			background-color:white;
		}
		
		.dataTables_wrapper .dataTables_length select {
			background-color:white!important;
		}
		
		.dataTables_wrapper .dataTables_filter input {
			background-color:white!important;
		}
		
		.button-error {
            background: rgb(202, 60, 60);
			color:white;
            /* this is a maroon */
        }

	</style>
</head>

<body>
<?php
	//error_reporting(E_ERROR | E_PARSE); 
	error_reporting(E_ALL ^ E_WARNING);
	//echo "oggi è: " . date("d-m-Y");
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
	
	if (isset($_GET['remove'])) {
		$remove = $_GET['remove'];
		$sql = "UPDATE user SET lastAd = -1 WHERE lastAd = '$remove'";
		$result = $mysqli->query($sql);
		$sql = "DELETE FROM adcampaign WHERE campaignId = '$remove'";
		$result = $mysqli->query($sql);
	}
	?>

<script type="text/javascript">
	function removeAd(id) {
		var txt;
		var r = confirm("Are you sure you want to remove this ad?");
		if (r == true) {
			txt = "You pressed OK!";
			console.log(txt);
			console.log(id);
			window.location.href="./ads.php?remove="+id;
		} else {
			txt = "You pressed Cancel!";
			console.log(txt);
		}	
	}
</script>

<div class="mt-3 text-center"></div>
        <div class="card card-login mx-auto mt-3">
            <div class="card-body">
                <div class="text-center">
<a href="earndoge.html"><img style="width:70px" src="images/images-logo.png" alt="EarnDogeToday"></a>
                    <h4>AD CAMPAIGNS</h4>
                    </div>
            </div>
        </div>
		
	<?php
	$sql = "select * from adcampaign";

	//echo "<pre> " . $sql . "</pre>";
	$result = $mysqli->query($sql);
	if ($result) {

		//echo "OK";
		echo "<table id='transactionTable' >";
		echo "<thead>";
        echo "<tr>";
            echo "<th>id</th>";
            echo "<th>title</th>";
			echo "<th>description</th>";
			echo "<th>nsfw</th>";
			echo "<th>clicks</th>";
			echo "<th>cpc</th>";
			echo "<th>daily budget</th>";
			echo "<th>status</th>";
			echo "<th>url</th>";
			echo "<th>user</th>";
			echo "<th>country</th>";
			echo "<th>seconds</th>";
			echo "<th>date</th>";
			echo "<th>speed</th>";
			echo "<th>reports</th>";
			echo "<th>remove</th>";
			
        echo "</tr>";
		echo "</thead>";
	    echo "<tbody>";
	if ($result->num_rows > 0) {
			echo "<tr>";
			while ($row = $result->fetch_array()) {
				echo "<td>" . $row['campaignId'] . "</td> ";
				echo "<td>" . $row['title'] . "</td>";
				echo "<td>" . $row['description'] . "</td>";
				echo "<td>" . $row['nsfw'] . "</td>";
				echo "<td>" . $row['clicks'] . "</td>";
				echo "<td>" . $row['cpc'] . "</td>";
				echo "<td>" . $row['dailyBudget'] . "</td>";
				echo "<td>" . $row['status'] . "</td>";
				echo "<td>" . $row['url'] . "</td>";
				echo "<td>" . $row['username'] . "</td>";
				echo "<td>" . $row['country'] . "</td>";
				echo "<td>" . $row['seconds'] . "</td>";
				echo "<td>" . $row['dateAdded'] . "</td>";
				echo "<td>" . $row['speed'] . "</td>";
				echo "<td>" . $row['reports'] . "</td>";
				echo "<td> <a class='button-error pure-button' onclick='removeAd(".$row['campaignId'].")'>Remove</a></td>";
				echo "</tr>";
			}
		} else "nessun dato";
		$result->close();
	}
	echo "</tbody>";
	echo "</table>";
	?>	
	
<script type="text/javascript">
$(document).ready( function () {
    $('#transactionTable').DataTable({
        "order": [[ 5, "desc" ]]
    });
	
} );
</script>

<a style="margin-left:50px" class="button-warning pure-button" href=" ./03login.php">BACK</a>
	

</body>

</html>