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
<style>
html {
  height: 100%;
}
body {
  min-height: 100%;
}

#headbar {
    display: inline-block;
    position: fixed;
    left: 0;
    top: 0;
    height: 60px;
    width: 100%;
    background-color: #eff0f2;
    box-shadow: inset 0 -15px 15px -15px #444;
	z-index:1;
}

</style>
</head>
<body onload="resetTime()">
    <div id="main">
	
	<?php
	$ad = "";
	if (isset($_GET['ad'])) {
		$ad = $_GET['ad'];
	}
	echo "<h3>IN LINK</h3>";
	echo $ad;
	
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

	
	//get Link data
	echo "<h3>LINK DATA </h3>";
	$trattamenti = array();
	$customLink = "";
	$username = "";
	$campaignId = "";
	
	$sql = "select * from link";
	$result = $mysqli->query($sql);
	if ($result) {
		if ($result->num_rows > 0) {
			while ($row = $result->fetch_array()) {
				echo "<br>";
				echo $row['customLink'];
				$customLink = $row['customLink'];
				echo "<br>";
				echo $row['username'];
				$username = $row['username'];
				echo "<br>";
				echo $row['campaignId'];
				$campaignId = $row['campaignId'];
				echo "<br>";
				array_push($trattamenti, $row['username']);
			}
		}
	}	
	print_r($trattamenti);
	
	//get adCampaign
	echo "<h3>AD CAMPAIGN URL </h3>";
	$sql = "select url,seconds,cpc from adcampaign where campaignId = ".$campaignId;
	$result = $mysqli->query($sql);
	if ($result) {
		if ($result->num_rows > 0) {
			while ($row = $result->fetch_array()) {
				echo "<br>";
				echo "<a href=".$row['url'].">".$row['url']."</a>";
				$url = $row['url'];
				echo "<br>";
				$seconds = $row['seconds'];
				echo $seconds;
				echo "<br>";
				$cpc = $row['cpc'];
				echo $cpc;
				echo "<br>";
				if($seconds == "-1"){
					echo $seconds;
					$xframe = -1;
					echo "no xframe";
				}else{
					$xframe = 1;
					echo "xframe allowed";
				}
				echo "<br>";
			}
		}
	}	
	?>
	
	<script type="application/javascript">
function resetTime(){
	localStorage.setItem('timeSpentOnSite',0);
}

var timeToSpend = <?php echo $seconds ?>;
var cpc = <?php echo $cpc ?>;
var timer;
var timerStart;
var timeSpentOnSite = getTimeSpentOnSite();

function getTimeSpentOnSite(){
    timeSpentOnSite = parseInt(localStorage.getItem('timeSpentOnSite'));
    timeSpentOnSite = isNaN(timeSpentOnSite) ? 0 : timeSpentOnSite;
    return timeSpentOnSite;
}

function startCounting(){
		timerStart = Date.now();
		timer = setInterval(function(){
    		timeSpentOnSite = getTimeSpentOnSite()+(Date.now()-timerStart);
    		localStorage.setItem('timeSpentOnSite',timeSpentOnSite);
    		timerStart = parseInt(Date.now());
    		// Convert to seconds
    		console.log(parseInt(timeSpentOnSite/1000));
			var timePassed = (timeToSpend - parseInt(timeSpentOnSite/1000));
			console.log(timePassed);
			if(timePassed <= 0){
				document.getElementById("timer").innerHTML = "You earned "+ cpc +" DOGE!";
			} else {
				document.getElementById("timer").innerHTML = "Please wait "+ timePassed +" seconds...";
			}
		},1000);
}
startCounting();

/* ---------- Stop the timer when the window/tab is inactive ---------- */

var stopCountingWhenWindowIsInactive = true; 

if( stopCountingWhenWindowIsInactive ){
    
    if( typeof document.hidden !== "undefined" ){
        var hidden = "hidden", 
        visibilityChange = "visibilitychange", 
        visibilityState = "visibilityState";
    }else if ( typeof document.msHidden !== "undefined" ){
        var hidden = "msHidden", 
        visibilityChange = "msvisibilitychange", 
        visibilityState = "msVisibilityState";
    }
    var documentIsHidden = document[hidden];

    document.addEventListener(visibilityChange, function() {
        if(documentIsHidden != document[hidden]) {
            if( document[hidden] ){
                // Window is inactive
                clearInterval(timer);
            }else{
                // Window is active
                startCounting();
            }
            documentIsHidden = document[hidden];
        }
    });
}
</script>
	
	<div id="headbar">
	<h5 style="margin-left:20px; margin-top:15px" id="timer">Loading...</h5>
	</div>
	<div>
	<?php if($xframe == 1){ ?>
	<iframe id="iFrame1" src=" <?php echo $url ?> " frameborder="0" style="overflow: hidden; height: 100%;
        width: 100%; position: absolute;"> </iframe>
	<?php } ?>
	</div>
</div>
</body>