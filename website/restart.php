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
</head>
<body>

<?php 

	include 'connection.php';

 $webhook = "";
	$sql = "select webhookRestart from settings";
	$result = $mysqli->query($sql);
	if ($result) {
		if ($result->num_rows > 0) {
			while ($row = $result->fetch_array()) {
				$webhook = $row['webhookRestart'];
			}
		}
	}

?>
<script src="https://code.jquery.com/jquery-2.1.1.min.js" type="text/javascript"></script> 
<script src="https://cdnjs.cloudflare.com/ajax/libs/materialize/0.97.7/js/materialize.min.js"></script>
 
  <script>
 

  $(document).ready(function(){
		var url = "<?php echo $webhook; ?>";
		console.log(url);
		var row_data = JSON.stringify({"restart": "1"});
        $.post(""+url+"", row_data);

		for(var i = 0; i<5000; i++){
			console.log("waiting");
		}

		window.location.replace("./settings.php");
  });
  
  
    </script>
	
</body>