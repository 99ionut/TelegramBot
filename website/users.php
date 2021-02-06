<!DOCTYPE html>
<html>
<?php
session_start();
if (isset($_SESSION['login']) && $_SESSION['login'] == 'ok') {
	//echo "sessione ok";
} else {
	//echo "pagina protetta";
	header('Location: 01login.php');
	//echo '<a href="01login.php" title="back to login"> LOGIN</a>';
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

	</style>
</head>

<body>
<?php
	include 'connection.php';
	?>
	
<div class="mt-3 text-center"></div>
        <div class="card card-login mx-auto mt-3">
            <div class="card-body">
                <div class="text-center">
<a href="earndoge.html"><img style="width:70px" src="images/images-logo.png" alt="EarnDogeToday"></a>
                    <h4>USERS</h4>
                    </div>
            </div>
        </div>
		
	<?php
	$sql = "select * from user";

	//echo "<pre> " . $sql . "</pre>";
	$result = $mysqli->query($sql);
	if ($result) {

		//echo "OK";
		echo "<table id='transactionTable' >";
		echo "<thead>";
        echo "<tr>";
            echo "<th>id</th>";
            echo "<th>referral code</th>";
			echo "<th>nsfw</th>";
			echo "<th>address</th>";
			echo "<th>referred By</th>";
			echo "<th>country</th>";
			echo "<th>username</th>";
			echo "<th>date joined</th>";
			echo "<th>virtual balance</th>";
        echo "</tr>";
		echo "</thead>";
	    echo "<tbody>";
	if ($result->num_rows > 0) {
			echo "<tr>";
			while ($row = $result->fetch_array()) {
				echo "<td>" . $row['userId'] . "</td> ";
				echo "<td>" . $row['referral'] . "</td>";
				echo "<td>" . $row['seeNsfw'] . "</td>";
				echo "<td>" . $row['address'] . "</td>";
				echo "<td>" . $row['referredBy'] . "</td>";
				echo "<td>" . $row['country'] . "</td>";
				echo "<td>" . $row['username'] . "</td>";
				echo "<td>" . $row['dateJoined'] . "</td>";
				echo "<td>" . $row['virtualBalance'] . "</td>";
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