<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="utf-8"><meta http-equiv="X-UA-Compatible" content="IE=edge"><meta name="viewport" content="width=device-width, initial-scale=1, shrink-to-fit=no"><meta name="description" content="Earn cryptocurrency on Telegram by visiting websites and performing other simple tasks."><meta name="author" content="earndogetoday.com">
<title>EARN DOGE today</title>
<link href="https://stackpath.bootstrapcdn.com/bootstrap/4.4.1/css/bootstrap.min.css" rel="stylesheet">
<link href="https://stackpath.bootstrapcdn.com/font-awesome/4.7.0/css/font-awesome.min.css" rel="stylesheet" type="text/css">
<link rel="apple-touch-icon-precomposed" sizes="57x57" href="favicons/images-apple-icon-57x57.png"><link rel="apple-touch-icon-precomposed" sizes="60x60" href="favicons/images-apple-icon-60x60.png"><link rel="apple-touch-icon-precomposed" sizes="72x72" href="favicons/images-apple-icon-72x72.png">
<link rel="apple-touch-icon-precomposed" sizes="76x76" href="favicons/images-apple-icon-76x76.png"><link rel="apple-touch-icon-precomposed" sizes="114x114" href="favicons/images-apple-icon-114x114.png"><link rel="apple-touch-icon-precomposed" sizes="120x120" href="favicons/images-apple-icon-120x120.png">
<link rel="apple-touch-icon-precomposed" sizes="144x144" href="favicons/images-apple-icon-144x144.png"><link rel="apple-touch-icon-precomposed" sizes="152x152" href="favicons/images-apple-icon-152x152.png"><link rel="apple-touch-icon-precomposed" sizes="180x180" href="favicons/images-apple-icon-180x180.png">
<link rel="icon" type="image/png" sizes="192x192" href="favicons/images-android-icon-192x192.png"><link rel="icon" type="image/png" sizes="32x32" href="favicons/images-favicon-32x32.png"><link rel="icon" type="image/png" sizes="96x96" href="favicons/images-favicon-96x96.png">
<meta name="theme-color" content="#ffffff">
</head>
<div class="container">
    <div class="mt-3 text-center"><a href="earndoge.html"><img src="images/images-logo.png"></a></div>
    <div class="card card-login mx-auto mt-3">
      <div class="card-body">
        <div class="text-center">
<?php
	//error_reporting(E_ERROR | E_PARSE); 
	error_reporting(E_ALL ^ E_WARNING);
	define('DB_SERVER', 'localhost');
	define('DB_USERNAME', 'telegrambot');
	define('DB_PASSWORD', 'telegrambot');
	define('DB_NAME', 'telegrambot');

	//connection
	$mysqli = new mysqli(DB_SERVER, DB_USERNAME, DB_PASSWORD, DB_NAME);
	if ($mysqli->connect_errno) {
		printf("Connect failed: %s\n", $mysqli->connect_error);
		exit();
	}
	$mysqli->set_charset("utf8");
?>

          <h4>Daily clicks by country</h4>

          <table class="table"><thead><tr><th scope="col">Code</th><th scope="col">Country</th><th scope="col">Clicks</th></tr></thead>
			  <tbody>
<?php 
		
	//get country data
	$code = "";
	$country = "";
	$clicks = "";
	
	$sql = "SELECT * FROM country ORDER BY clicks DESC";
	$result = $mysqli->query($sql);
	if ($result) {
		if ($result->num_rows > 0) {
			while ($row = $result->fetch_array()) {
				$code = $row['code'];
				$country = $row['country'];
				$clicks = $row['clicks'];
	echo "<tr>";
		echo "<th scope='row'>".$code."</th>";
			echo "<td>".$country."</td>";
			echo "<td>".$clicks."</td>";
	echo "</tr>";
			}
		}
	}	

?>
			</tbody>
		  </table>
		</div>
      </div>
    </div>
    <div class="text-center mt-4">
    <ul class="list-inline"><li class="list-inline-item"><a title="Home" class="small" href="earndoge.html">home</a></li>
        <li class="list-inline-item"><a title="Daily traffic by country" class="small" href="countries.html">traffic</a></li>
        <li class="list-inline-item"><a title="Most recent withdrawals" class="small" href="payments.html">payments</a></li>
        <li class="list-inline-item"><a title="Privacy Policy" class="small" href="privacy.html">privacy</a></li>
        <li class="list-inline-item"><a title="Terms of Service" class="small" href="terms.html">terms</a></li>
        <li class="list-inline-item"><a title="Frequently asked questions" class="small" href="faq.html">faq</a></li>
        </ul><ul class="list-inline"><li class="list-inline-item"><a title="Twitter" href="https://twitter.com/EarnDogeToday/" target="_blank"><i class="fa fa-twitter"></i></a></li>
        <li class="list-inline-item"><a title="Facebook" href="https://www.facebook.com/EarnDogeToday/" target="_blank"><i class="fa fa-facebook-official"></i></a></li>
         </ul></div>  </div> 