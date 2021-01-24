<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="utf-8"><meta http-equiv="X-UA-Compatible" content="IE=edge"><meta name="viewport" content="width=device-width, initial-scale=1, shrink-to-fit=no"><meta name="description" content="Earn cryptocurrency on Telegram by visiting websites and performing other simple tasks."><meta name="author" content="earndogetoday.com">
<title>EARN DOGE today</title>
<link href="https://cdnjs.cloudflare.com/ajax/libs/materialize/0.97.7/css/materialize.min.css" rel="stylesheet">
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
<body>
    <div id="main">
	<br>
	<br>
	<br>
<?php

		
	//DB CONNECTION
	error_reporting(E_ALL ^ E_WARNING);
	define('DB_SERVER', 'localhost');
	define('DB_USERNAME', 'root');
	define('DB_PASSWORD', '');
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
	
	
	$valid = 0;
	
	$sql = "SELECT * FROM link WHERE customLink = ".$ad;
	//IF THE LINK IS NOT VALID
	$result = $mysqli->query($sql);
	if ($result == "") { 	
		$valid = 0;
	//IF LINK IS VALID
	} else {
	//get Link data
		if ($result) {
			if ($result->num_rows > 0) {
				while ($row = $result->fetch_array()) {
					$customLink = $row['customLink'];
					$username = $row['username'];
					$campaignId = $row['campaignId'];
					//echo $campaignId;
					$valid = 1;
				}
			}
		}	

    //get webhook
    $webhook = "";
	$sql = "select webhookWebsite,ownerTake,referralTake from settings";
	$result = $mysqli->query($sql);
	if ($result) {
		if ($result->num_rows > 0) {
			while ($row = $result->fetch_array()) {
				$webhook = $row['webhookWebsite'];
				$ownerTake = $row['ownerTake'];
				$referralTake = $row['referralTake'];
			}
		}
	}

	$sql = "SELECT referredBy FROM user WHERE username = '".$username."'";
	$result = $mysqli->query($sql);
	if ($result) {
		if ($result->num_rows > 0) {
				$referredBy = 1;
			} else {
				$referredBy = 0;	
			}
		}
	
	//get adCampaign
	if($valid != 0){
		$sql = "select url,seconds,cpc from adcampaign where campaignId = ".$campaignId;
		$result = $mysqli->query($sql);
		if ($result) {
			if ($result->num_rows > 0) {
				while ($row = $result->fetch_array()) {
					$url = $row['url'];
					$seconds = $row['seconds'];
					$cpc = $row['cpc'];
					
					if($referredBy == 1){
						$userCpc = $cpc -(($cpc*$ownerTake)/100);
						$referralCpc = (($userCpc*$referralTake)/100);
						$userCpc = $userCpc - $referralCpc;
					} else {
						$userCpc = $cpc-(($cpc*$ownerTake)/100);
					}
					
					
					
					if($seconds == "-1"){
						$xframe = 0; // if seconds = -1 means that the user doesn't want to force users to see the ad
					}else{
						$xframe = 1; // else is seconds higher than -1
					}
				}
			}
		}
	} else {
		$xframe = -1; //if url not valid
	}
	
	
}
?>
<a id="send" style="display:none" class="btn btn-large btn-full-width waves-effect waves-light">Send</a>

<script src="https://code.jquery.com/jquery-2.1.1.min.js" type="text/javascript"></script> 
<script src="https://cdnjs.cloudflare.com/ajax/libs/materialize/0.97.7/js/materialize.min.js"></script>
 
    <script>
    $(function() {
        $('#send').click(function(e) {
        var url = "<?php echo $webhook; ?>";
        var customLink = "<?php echo $customLink; ?>";
        var username = "<?php echo $username; ?>";
		var campaignId = "<?php echo $campaignId; ?>";
		var xframe = "<?php echo $xframe; ?>";
        //$.post(url,{"customLink": customLink,"username": username,"campaignId": campaignId,"xframe": xframe});
        
		var row_data = JSON.stringify({"customLink": customLink,"username": username,"campaignId": campaignId,"xframe": xframe});
        //console.log(row_data);
        $.post(""+url+"", row_data);
	
		});
    });
    </script>
	
	
<script type="text/javascript">
function resetTime(){	
	console.log("XFRAME = "+xframe);
	localStorage.setItem('timeSpentOnSite',0);
	startCounting();
}


/*function resetTime10(){
	var xframe = "<?php echo $xframe; ?>";
	console.log("XFRAME = "+xframe);
	localStorage.setItem('timeSpentOnSite',0);
	var timeToSpend = 10;
	startCounting();
}*/

var flag = 1;

var timeToSpend = <?php echo $seconds+1; ?>;

var ownerTake = <?php echo $ownerTake ?>;
var cpc = <?php echo $userCpc ?>;
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
			var timePassed = (timeToSpend - parseInt(timeSpentOnSite/1000));
			console.log(timePassed);
			if(timePassed <= 0){
				
				if(flag == 1){  //only send 1 webhook and update text 1 time
				flag = 0;
					document.getElementById("timer").innerHTML = "You earned "+ cpc.toFixed(4) +" DOGE!";	
					console.log("SENT");
					$('#send').click();
					//postDataToWebhook();	
					if(xframe == 0){
						
						window.location.replace("<?php echo $url ?>");
					}
				}	
				
				} else {
				document.getElementById("timer").innerHTML = "Please wait "+ timePassed +" seconds...";				
			}
		},1000);
}

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
	
	<div>
	<?php if($xframe == 1){ ?> <!-- IF AD IS VALID -->
	<div id="headbar">
	<h5 style="margin-left:20px; margin-top:15px" id="timer">Loading...</h5>
	</div>
	<script>xframe = 1;</script>
	<script>resetTime();</script>
	<iframe id="iFrame1" src=" <?php echo ""."$url".""; ?> " frameborder="0" style="overflow: hidden; height: 100%;
        width: 100%; position: absolute;"> </iframe>
		
	<?php } else if($xframe == 0) { ?> <!-- IF AD sec -1 -->
	<div style="display:none" id="headbar">
	<h5 style="margin-left:20px; margin-top:15px" id="timer">Loading...</h5>
	</div>
	<script>xframe = 0;</script>
	<script>resetTime();</script>
		
	<?php } else { ?>  <!-- IF AD NOT VALID -->
		<div class="container">
        <div class="mt-3 text-center"><a href="https://www.i0nut.com/earndogetoday/earndoge.html"><img src="./images/images-logo.png"></a></div>
        <div class="card card-login mx-auto mt-3">
            <div class="card-header">Error</div>
            <div class="card-body">
                <div class="text-center">
                    <p>Sorry, but the link you used is not valid.</p>
                   <p>Use the <strong>/visit</strong> command to get a new one.</p>
                </div>
                <div class="text-center">
                    <a class="d-block small mt-4" href="https://www.i0nut.com/earndogetoday/earndoge.html">Return home</a>
                </div>
            </div>
          </div>
		</div>
	<?php } ?>
	</div>
</div>
</body>