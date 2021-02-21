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
		
		
		  .button-success {
            background: rgb(28, 184, 65);
			color:white;
            /* this is a green */
        }

        .button-error {
            background: rgb(202, 60, 60);
			color:white;
            /* this is a maroon */
        }

        .button-warning {
            background: rgb(223, 117, 20);
			color:white;
            /* this is an orange */
        }

        .button-secondary {
            background: rgb(66, 184, 221);
			color:white;
            /* this is a light blue */
        }
		
		.button-purple {
            background: purple;
			color:white;
            /* this is a light blue */
        }
		
		#transactionTable_wrapper{
			margin-top:20px;
		}


	</style>
</head>

<body>
<?php
	include 'connection.php';
	?>
	
<div class="mt-3 text-center"></div>
        
          
                <div class="text-center">

                    <h4>TRANSACTIONS</h4>
                    </div>
         
      
		
		
		 <div class="text-center">

<a class="pure-button button-success pure-button-active" href="users.php">USERS</a>&nbsp;&nbsp;&nbsp;
<a class="pure-button button-error pure-button-active" href="ads.php">ADS</a>&nbsp;&nbsp;&nbsp;
<a class="pure-button button-warning pure-button-active" href="transactions.php">TRANSACTIONS</a>&nbsp;&nbsp;&nbsp;
<a class="pure-button button-purple pure-button-active" href="withdraws.php">WITHDRAWS</a>&nbsp;&nbsp;&nbsp;
<a class="pure-button pure-button-primary pure-button-active" href="settings.php">SETTINGS</a>&nbsp;&nbsp;&nbsp;
<a class="pure-button pure-button-active" href="logout.php">EXIT</a>&nbsp;&nbsp;&nbsp;
</div>
	
	
	<?php
	$sql = "select * from transaction";

	//echo "<pre> " . $sql . "</pre>";
	$result = $mysqli->query($sql);
	if ($result) {

		//echo "OK";
		echo "<table id='transactionTable' >";
		echo "<thead>";
        echo "<tr>";
            echo "<th>id</th>";
            echo "<th>txid</th>";
			echo "<th>amount</th>";
			echo "<th>userAddress</th>";
			echo "<th>userUsername</th>";
			echo "<th>date</th>";
        echo "</tr>";
		echo "</thead>";
	    echo "<tbody>";
	if ($result->num_rows > 0) {
			echo "<tr>";
			while ($row = $result->fetch_array()) {
				echo "<td>" . $row['id'] . "</td> ";
				echo "<td>" . $row['transaction'] . "</td>";
				echo "<td>" . $row['amount'] . "</td>";
				echo "<td>" . $row['userAddress'] . "</td>";
				echo "<td>" . $row['userUsername'] . "</td>";
				echo "<td>" . $row['date'] . "</td>";
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


</body>

</html>