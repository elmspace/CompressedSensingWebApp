/*
	This module contain some of the JS functions used in the landing page.
*/
$(document).ready(function(){
	// If the server side msg is not nonne, display the msg in an alert.
	if(landingPage_msg["msg"] != "none"){
		alert(landingPage_msg["msg"])
	}
})

/*
	This function will extract the txt data and create a report table.
	It uses DataTables to make the table a little interactive.
*/
$(document).ready(function(){
	// Set the API end-point.
	var endPoint = "/palindromes";
	// Make an AJAX call to get the data from server
	AJAX_Get(endPoint,undefined).then(function(ServResp){
		// Parse the data into JSON object.
		document.getElementById("Palindromes").innerHTML = ServResp;
	});


	// Set the API end-point.
	var endPoint = "/palindromes/count";
	// Make an AJAX call to get the data from server
	AJAX_Get(endPoint,undefined).then(function(ServResp){
		// Parse the data into JSON object.
		document.getElementById("PalindromesCount").innerHTML = ServResp;
	});
});

