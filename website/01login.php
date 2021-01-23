<?php
session_start();
session_destroy();
?>

<!DOCTYPE html>
<html>
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

	</style>
</head>
<body>
<div id="background">
<?php
	if (isset($_GET['errore'])) {
		$errore = $_GET['errore'];
		if($errore == "registrazione"){
			echo "<script type='text/javascript'>alert('USERNAME DOESNT EXIST');</script>";
		} else if($errore == "password"){
			echo "<script type='text/javascript'>alert('WRONG PASSWORD');</script>";
		}
	}
?>

        <div class="card card-login mx-auto mt-3">
		
            <div class="card-body">
                <div class="text-center">
<a href="earndoge.html"><img style="width:100px" src="images/images-logo.png" alt="EarnDogeToday"></a>
                    <h4>ADMIN MENUS</h4>
                    </div>
            </div>
        </div>
		
		<br>
		<br>
		 <div class="text-center">
	<form  name='login' action='02login.php' method='post' >
		<span style="color:black" >USERNAME: </span><input type='text' name='utente' />
		<br/>
		<span style="color:black">PASSWORD: </span><input type='password' name='password' />
		<br/>
		<br>
		<input class="pure-button pure-button-primary" type='submit' value="LOGIN">
	</form>
	 </div>
<!--	
<h2 style="color:#008CBA">REGISTRAZIONE</h2>
	<form name='registrazione' action='04login.php' method='post' >
		UTENTE:<input type='text' name='utente' />
		<br/>
		PASSWORD:<input type='password' name='password' />
		<br/>
		CODICE BIGLIETTO:<input type='text' name='codicebiglietto' />
		<br/>
		<input class="registrazione" type='submit' value='REGISTRAZIONE'>
	</form>
<h1 style="color:white">_______________________</h1>
-->
	</body>
	</div>
</html>



