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
	
	if (isset($_GET['remove'])) {
		$remove = $_GET['remove'];
		$sql = "UPDATE user SET lastAd = -1 WHERE lastAd = '$remove'";
		$result = $mysqli->query($sql);
		$sql = "DELETE FROM adcampaign WHERE campaignId = '$remove'";
		$result = $mysqli->query($sql);
	}
	?>


<div class="mt-3 text-center"></div>
      
       
                <div class="text-center">

                    <h4>WITHDRAWS</h4>
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
	 //get webhook
    $webhook = "";
	$webhookRevoke = "";
	$sql = "select webhookWithdraw, webhookRevoke from settings";
	$result = $mysqli->query($sql);
	if ($result) {
		if ($result->num_rows > 0) {
			while ($row = $result->fetch_array()) {
				$webhook = $row['webhookWithdraw'];
				$webhookRevoke = $row['webhookRevoke'];
			}
		}
	}
	
	
	//get withdraws
	$sql = "select * from withdraw";

	//echo "<pre> " . $sql . "</pre>";
	$result = $mysqli->query($sql);
	if ($result) {

		//echo "OK";
		echo "<table id='transactionTable' >";
		echo "<thead>";
        echo "<tr>";
            echo "<th>id</th>";
            echo "<th>date</th>";
			echo "<th>username</th>";
			echo "<th>userAddress</th>";
			echo "<th>amount</th>";
			echo "<th>userPersonalAddress</th>";
			echo "<th> </th>";
			echo "<th> </th>";
			
        echo "</tr>";
		echo "</thead>";
	    echo "<tbody>";
	if ($result->num_rows > 0) {
			echo "<tr>";
			while ($row = $result->fetch_array()) {
				echo "<td>" . $row['id'] . "</td> ";
				echo "<td>" . $row['date'] . "</td>";
				echo "<td>" . $row['username'] . "</td>";
				echo "<td>" . $row['userAddress'] . "</td>";
				echo "<td>" . $row['amount'] . "</td>";
				echo "<td>" . $row['userPersonalAddress'] . "</td>";
				echo "<td> <a class='button-success pure-button' onclick=\"approveWithdraw('".$row['id']."','". $row['userAddress'] ."','". $row['amount'] ."','". $row['userPersonalAddress'] ."')\"> Approve </a> </td>";
				echo "<td> <a class='button-error pure-button' onclick=\"revokeWithdraw('".$row['id']."','". $row['amount'] ."')\"> Revoke </a></td>";
				echo "</tr>";
			}
		} else "nessun dato";
		$result->close();
	}
	echo "</tbody>";
	echo "</table>";
	?>	

<script type="text/javascript">
	function revokeWithdraw(id,amount) {
		var txt;
		var r = confirm("Are you sure you want to revoke this withdraw?");
		if (r == true) {
			var url = "<?php echo $webhookRevoke; ?>";
			txt = "You pressed OK!";
			console.log(txt);
			console.log(id);
			
			var row_data = JSON.stringify({"id": id,"amount":amount});
			$.post(""+url+"", row_data);
			
			for(var i = 0; i<300; i++){
						console.log("waiting");
						}
						
			window.location.href="./withdraws.php?revoke="+id;
		} else {
			txt = "You pressed Cancel!";
			console.log(txt);
		}	
	}
	
	function approveWithdraw(id,userAddress,amount,userPersonalAddress) {
		var txt;
		var r = confirm("Are you sure you want to approve this withdraw?");
		if (r == true) {
			var url = "<?php echo $webhook; ?>";
			txt = "You pressed OK!";
			console.log(txt);
			console.log(id);
			
			var row_data = JSON.stringify({"id": id,"userAddress": userAddress,"amount":amount,"userPersonalAddress":userPersonalAddress});
			$.post(""+url+"", row_data);
			
			for(var i = 0; i<300; i++){
						console.log("waiting");
						}
		
			window.location.href="./withdraws.php?approve="+id;
		} else {
			txt = "You pressed Cancel!";
			console.log(txt);
		}	
	}


$(document).ready( function () {
    $('#transactionTable').DataTable({
        "order": [[ 1, "desc" ]]
    });
	
} );
</script>

</body>

</html>