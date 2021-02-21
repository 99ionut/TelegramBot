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
		
		.pure-button {
			font-size: 100%;
		}
		
		input {
			float:right;
			margin-right:10px;
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
	
	
	if (isset($_POST['txtWebhook'])) {
		$txtWebhook = $_POST['txtWebhook'];
		$sql = "UPDATE settings SET webhook = '$txtWebhook'";
		$result = $mysqli->query($sql);
		if ($result) {
			echo '<script language="javascript">';
			echo 'alert("SETTINGS CHANGED!")';
			echo '</script>';
		}
		
	} elseif (isset($_POST['txtWebhookWebsite'])) {
		$txtWebhookWebsite = $_POST['txtWebhookWebsite'];
		$sql = "UPDATE settings SET webhookWebsite = '$txtWebhookWebsite'";
		$result = $mysqli->query($sql);
		if ($result) {
			echo '<script language="javascript">';
			echo 'alert("SETTINGS CHANGED!")';
			echo '</script>';
		}
		
	} elseif (isset($_POST['txtWebhookRestart'])) {
		$txtWebhookRestart = $_POST['txtWebhookRestart'];
		$sql = "UPDATE settings SET webhookRestart = '$txtWebhookRestart'";
		$result = $mysqli->query($sql);
		if ($result) {
			echo '<script language="javascript">';
			echo 'alert("SETTINGS CHANGED!")';
			echo '</script>';
		}
		
	} elseif (isset($_POST['txtWebhookWithdraw'])) {
		$txtWebhookWithdraw = $_POST['txtWebhookWithdraw'];
		$sql = "UPDATE settings SET webhookWithdraw = '$txtWebhookWithdraw'";
		$result = $mysqli->query($sql);
		if ($result) {
			echo '<script language="javascript">';
			echo 'alert("SETTINGS CHANGED!")';
			echo '</script>';
		}
		
	} elseif (isset($_POST['txtWebhookRevoke'])) {
		$txtWebhookRevoke = $_POST['txtWebhookRevoke'];
		$sql = "UPDATE settings SET webhookRevoke = '$txtWebhookRevoke'";
		$result = $mysqli->query($sql);
		if ($result) {
			echo '<script language="javascript">';
			echo 'alert("SETTINGS CHANGED!")';
			echo '</script>';
		}
		
	} elseif (isset($_POST['txtBlockIoApi'])) {
		$txtBlockIoApi = $_POST['txtBlockIoApi'];
		$sql = "UPDATE settings SET blockIoApi = '$txtBlockIoApi'";
		$result = $mysqli->query($sql);
		if ($result) {
			echo '<script language="javascript">';
			echo 'alert("SETTINGS CHANGED!")';
			echo '</script>';
		}
		
	} elseif (isset($_POST['txtBlockIoSecretPin'])) {
		$txtBlockIoSecret = $_POST['txtBlockIoSecretPin'];
		$sql = "UPDATE settings SET blockIoSecretPin = '$txtBlockIoSecret' ";
		$result = $mysqli->query($sql);
		if ($result) {
			echo '<script language="javascript">';
			echo 'alert("SETTINGS CHANGED!")';
			echo '</script>';
		}
	} elseif (isset($_POST['txtBlockIoVersion'])) {
		$txtBlockIoVersion = $_POST['txtBlockIoVersion'];
		$sql = "UPDATE settings SET blockIoVersion = '$txtBlockIoVersion'";
		$result = $mysqli->query($sql);
		if ($result) {
			echo '<script language="javascript">';
			echo 'alert("SETTINGS CHANGED!")';
			echo '</script>';
		}
		
	} elseif (isset($_POST['txtMinDepositAmount'])) {
		$txtMinDepositAmount = $_POST['txtMinDepositAmount'];
		$sql = "UPDATE settings SET minDepositAmount = '$txtMinDepositAmount'";
		$result = $mysqli->query($sql);
		if ($result) {
			echo '<script language="javascript">';
			echo 'alert("SETTINGS CHANGED!")';
			echo '</script>';
		}
		
	} elseif (isset($_POST['txtMinWithdrawAmount'])) {
		$txtMinWithdrawAmount = $_POST['txtMinWithdrawAmount'];
		$sql = "UPDATE settings SET minWithdrawAmount = '$txtMinWithdrawAmount'";
		$result = $mysqli->query($sql);
		if ($result) {
			echo '<script language="javascript">';
			echo 'alert("SETTINGS CHANGED!")';
			echo '</script>';
		}
		
	} elseif (isset($_POST['txtMainAccount'])) {
		$txtMainAccount = $_POST['txtMainAccount'];
		$sql = "UPDATE settings SET mainAccount = '$txtMainAccount'";
		$result = $mysqli->query($sql);
		if ($result) {
			echo '<script language="javascript">';
			echo 'alert("SETTINGS CHANGED!")';
			echo '</script>';
		}
		
	} elseif (isset($_POST['txtOwnerTake'])) {
		$txtOwnerTake = $_POST['txtOwnerTake'];
		$sql = "UPDATE settings SET ownerTake = '$txtOwnerTake'";
		$result = $mysqli->query($sql);
		if ($result) {
			echo '<script language="javascript">';
			echo 'alert("SETTINGS CHANGED!")';
			echo '</script>';
		}
		
	} elseif (isset($_POST['txtReferralTake'])) {
		$txtReferralTake = $_POST['txtReferralTake'];
		$sql = "UPDATE settings SET referralTake = '$txtReferralTake'";
		$result = $mysqli->query($sql);
		if ($result) {
			echo '<script language="javascript">';
			echo 'alert("SETTINGS CHANGED!")';
			echo '</script>';
		}
		
	} else {
		;
	}
	
	?>
	
<div class="mt-3 text-center"></div>
       
          
                <div class="text-center">

                    <h4>SETTINGS</h4>
                    </div>
            
     
		
				 <div class="text-center">

<a class="pure-button button-success pure-button-active" href="users.php">USERS</a>&nbsp;&nbsp;&nbsp;
<a class="pure-button button-error pure-button-active" href="ads.php">ADS</a>&nbsp;&nbsp;&nbsp;
<a class="pure-button button-warning pure-button-active" href="transactions.php">TRANSACTIONS</a>&nbsp;&nbsp;&nbsp;
<a class="pure-button button-purple pure-button-active" href="withdraws.php">WITHDRAWS</a>&nbsp;&nbsp;&nbsp;
<a class="pure-button pure-button-primary pure-button-active" href="settings.php">SETTINGS</a>&nbsp;&nbsp;&nbsp;
<a class="pure-button pure-button-active" href="logout.php">EXIT</a>&nbsp;&nbsp;&nbsp;
</div>
	
	
		<br><br>
	<?php
	$sql = "select * from settings";

	//echo "<pre> " . $sql . "</pre>";
	$result = $mysqli->query($sql);
	if ($result) {

		//echo "OK";
	echo "<div style='margin: 0px auto; width:850px'>";
	if ($result->num_rows > 0) {
			
			while ($row = $result->fetch_array()) {
				echo "<div><b>BLOCKIO Webhook</b>:&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;  " . $row['webhook'] . " <form name='webh' style='float:right' action='settings.php' method='POST'> <input class='pure-button pure-button-primary' type='submit' id='webhook' value='CHANGE'>  <input type='text' name='txtWebhook' ></form></div><br> ";
				echo "<div><b>Website Webhook</b>:&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;" . $row['webhookWebsite'] . "<form name='webh' style='float:right' action='settings.php' method='POST'> <input class='pure-button pure-button-primary' type='submit' id='webhookWebsite' value='CHANGE'> <input type='text' name='txtWebhookWebsite' ></form></div><br>";
				echo "<div><b>Restart Webhook</b>:&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;" . $row['webhookRestart'] . "<form name='webh' style='float:right' action='settings.php' method='POST'> <input class='pure-button pure-button-primary' type='submit' id='webhookRestart' value='CHANGE'> <input type='text' name='txtWebhookRestart' ></form></div><br>";
				echo "<div><b>Withdraw Webhook</b>:&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;" . $row['webhookWithdraw'] . "<form name='webh' style='float:right' action='settings.php' method='POST'> <input class='pure-button pure-button-primary' type='submit' id='webhookWithdraw' value='CHANGE'> <input type='text' name='txtWebhookWithdraw' ></form></div><br>";
				echo "<div><b>Revoke Webhook</b>:&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;" . $row['webhookRevoke'] . "<form name='webh' style='float:right' action='settings.php' method='POST'> <input class='pure-button pure-button-primary' type='submit' id='webhookRevoke' value='CHANGE'> <input type='text' name='txtWebhookRevoke' ></form></div><br>";
				
				
				echo "<div><b>BLOCKIO Api</b>:&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;" . $row['blockIoApi'] . "<form name='webh' style='float:right' action='settings.php' method='POST'> <input class='pure-button pure-button-primary' type='submit' id='blockIoApi' value='CHANGE'> <input type='text'  name='txtBlockIoApi' ></form></div><br>";
				echo "<div><b>BLOCKIO Secret Pin</b>:&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;" . $row['blockIoSecretPin'] . "<form name='webh' style='float:right' action='settings.php' method='POST'> <input class='pure-button pure-button-primary' type='submit' id='blockIoSecretPin' value='CHANGE'> <input type='text' name='txtBlockIoSecretPin' ></form></div><br>";
				echo "<div><b>BLOCKIO Version</b>:&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;" . $row['blockIoVersion'] . "<form name='webh' style='float:right' action='settings.php' method='POST'> <input class='pure-button pure-button-primary' type='submit' id='blockIoVersion' value='CHANGE'> <input type='text' name='txtBlockIoVersion' ></form></div><br>";
				echo "<div><b>Minimum deposit amount (DOGE)</b>:&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;" . $row['minDepositAmount'] . "<form name='webh' style='float:right' action='settings.php' method='POST'> <input class='pure-button pure-button-primary' type='submit' id='minDepositAmount' value='CHANGE'> <input type='text' name='txtMinDepositAmount' ></form></div><br>";
				echo "<div><b>Minimum Withdraw Amount (DOGE)</b>:&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;" . $row['minWithdrawAmount'] . "<form name='webh' style='float:right' action='settings.php' method='POST'> <input class='pure-button pure-button-primary' type='submit' id='minWithdrawAmount' value='CHANGE'> <input type='text' name='txtMinWithdrawAmount' ></form></div><br>";
				//echo "<div><b>Telegram Bot Token</b></div> <div>" . $row['botToken'] . "</div>";
				echo "<div><b>Founds account address</b>:&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;" . $row['mainAccount'] . "<form name='webh' style='float:right' action='settings.php' method='POST'> <input class='pure-button pure-button-primary' type='submit' id='mainAccount' value='CHANGE'> <input type='text' name='txtMainAccount' ></form></div><br>";
				echo "<div><b>Owner take (%)</b>:&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;" . $row['ownerTake'] . "<form name='webh' style='float:right' action='settings.php' method='POST'> <input class='pure-button pure-button-primary' type='submit' id='ownerTake' value='CHANGE'> <input type='text' name='txtOwnerTake' ></form></div><br>";
				echo "<div><b>Referral take (%)</b>:&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;" . $row['referralTake'] . "<form name='webh' style='float:right' action='settings.php' method='POST'> <input class='pure-button pure-button-primary' type='submit' id='referralTake' value='CHANGE'> <input type='text' name='txtReferralTake' ></form></div><br>";
				echo "</tr>";
			}
		} else "nessun dato";
		$result->close();
	}
	echo "</div>";
	?>	
	
<script type="text/javascript">
	$("#webhook").click(function(){
		var data = $("#txtWebhook").val();
		
		if(data != ""){
			console.log(data);
			<?php 
			$sql = "UPDATE settings SET Webhook = ".data." column2 = value2 WHERE condition;";
			$result = $mysqli->query($sql);
			?>
		} else {
			console.log("empty");
		}
	});
	
	$("#webhookWebsite").click(function(){
		console.log("clicck");
	});
	
	$("#blockIoApi").click(function(){
		console.log("clicck");
	});
	
	$("#blockIoSecretPin").click(function(){
		console.log("clicck");
	});
	
	$("#blockIoVersion").click(function(){
		console.log("clicck");
	});
	
	$("#minDepositAmount").click(function(){
		console.log("clicck");
	});
	
	$("#minWithdrawAmount").click(function(){
		console.log("clicck");
	});
	
	$("#mainAccount").click(function(){
		console.log("clicck");
	});
	
	$("#ownerTake").click(function(){
		console.log("clicck");
	});
	
	$("#referralTake").click(function(){
		console.log("clicck");
	});
</script>

<a style="float:right; margin-right:50px; background-color:black; color:white" class="button-warning pure-button" href="./restart.php">RESTART BOT</a>
</body>

</html>