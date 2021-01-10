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
<body onload="">
    <div id="main">
	
<?php

		
	//DB CONNECTION
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

	$ad = "";
	if (isset($_GET['ad'])) {
		$ad = $_GET['ad'];
	}
	$sql = "SELECT * FROM link WHERE customLink = ".$ad;
	echo $sql;
	//IF THE LINK IS VALID
	$result = $mysqli->query($sql);
	if ($result == "") { 	
		echo "<h3>INVALID URL </h3>";
		$xframe = 0;
		echo '<div class="container">';
        echo '<div class="mt-3 text-center"><a href="https://www.i0nut.com/earndogetoday/earndoge.html"><img src="./images/images-logo.png"></a></div>';
        echo '<div class="card card-login mx-auto mt-3">';
        echo '    <div class="card-header">Error</div>';
        echo '    <div class="card-body">';
        echo '        <div class="text-center">';
        echo '            <p>Sorry, but the link you used is not valid.</p>';
        echo '           <p>Use the <strong>/visit</strong> command to get a new one.</p>';
        echo '        </div>';
        echo '        <div class="text-center">';
        echo '            <a class="d-block small mt-4" href="https://www.i0nut.com/earndogetoday/earndoge.html">Return home</a>';
        echo '        </div>';
        echo '    </div>';
        echo '  </div>';
		echo '</div>';
	//IF LINK NOT VALID
	} else {
		echo "resetTime()";
		echo "<h3>VALID LINK</h3>";

	//get Link data
		echo "<h3>LINK DATA </h3>";
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
				}
			}
		}	

    //get webhook
    $webhook = "";
	$sql = "select webhook from settings";
	$result = $mysqli->query($sql);
	if ($result) {
		if ($result->num_rows > 0) {
			while ($row = $result->fetch_array()) {
				echo "<br>";
				echo $row['webhook'];
				$webhook = $row['webhook'];
			}
		}
	}	
	
	//get adCampaign
	echo "<h3>AD CAMPAIGN DATA </h3>";
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
						//window.location.replace("http://www.w3schools.com");
					}else{
						$xframe = 1;
						echo "xframe allowed";
					}
				}
			}
		}
	}
?>
	
	<script type="text/javascript">
function resetTime(){
	localStorage.setItem('timeSpentOnSite',0);
}

var timeToSpend = <?php echo $seconds - 20 ?>;
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
		var flag = 1;
		timerStart = Date.now();
		timer = setInterval(function(){
    		timeSpentOnSite = getTimeSpentOnSite()+(Date.now()-timerStart);
    		localStorage.setItem('timeSpentOnSite',timeSpentOnSite);
    		timerStart = parseInt(Date.now());
    		// Convert to seconds
			var timePassed = (timeToSpend - parseInt(timeSpentOnSite/1000));
			console.log(timePassed);
			if(timePassed <= 0){
				
				//if(flag == 1){  //only send 1 webhook and update text 1 time
				//	flag = 0;
					//postDataToWebhook();
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


function postDataToWebhook(){
  //get the values needed from the passed in json object
  var userName="ciao";
  var userPlatform="dio";
  var userEmail="bbbr";
  //url to your webhook
  var webHookUrl="$webhook";
  
  //https://developer.mozilla.org/en-US/docs/Web/API/XMLHttpRequest
  var oReq = new XMLHttpRequest();
  var myJSONStr = payload={
      "text": "Acuired new user",
      "attachments":[
        {
          "author_name": userName,
          "author_icon": "http://icons.iconarchive.com/icons/noctuline/wall-e/128/Wall-E-icon.png",
          "color": "#7CD197",
          "fields":[
              {
                "title":"Platform",
                "value":userPlatform,
                "short":true
              },
              {
                "title":"email",
                "value":userEmail,
                "short":true
              }
          ]

        }
    ]

  };
  
//register method called after data has been sent method is executed
  oReq.addEventListener("load", reqListener);
  oReq.open("POST", webHookUrl,true);
  oReq.setRequestHeader('Content-Type', 'application/x-www-form-urlencoded');
  oReq.send(JSON.stringify(myJSONStr));
}
//callback method after webhook is executed
function reqListener () {
  console.log(this.responseText);
}

</script>
	
	<div id="headbar" style="display:none">
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