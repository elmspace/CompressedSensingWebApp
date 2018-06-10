/*
	This module contain some of the JS functions used in the landing page.
*/
$(document).ready(function(){
	// If the server side msg is not nonne, display the msg in an alert.
	if(landingPage_msg["msg"] != "none"){
		console.log(landingPage_msg["msg"]);
		if(landingPage_msg["msg"] == "pass"){

			var NameOfImg = landingPage_msg["file_name"];

			var originalImg = document.getElementById("originalImg");
			var compressedImg = document.getElementById("compressedImg");
			var recoveredImg = document.getElementById("recoveredImg");

			console.log("/static/images/SaveFiles/"+String(NameOfImg)+"_original.jpg");

			var originalImg_img = document.createElement("img");
			originalImg_img.setAttribute("src","/static/images/SaveFiles/"+String(NameOfImg)+"_original.jpg");
			originalImg.appendChild(originalImg_img);

			var compressedImg_img = document.createElement("img");
			compressedImg_img.setAttribute("src","/static/images/SaveFiles/"+String(NameOfImg)+"_compressed.jpg");
			compressedImg.appendChild(compressedImg_img);

			var recoveredImg_img = document.createElement("img");
			recoveredImg_img.setAttribute("src","/static/images/SaveFiles/"+String(NameOfImg)+"_recovered.jpg");
			recoveredImg.appendChild(recoveredImg_img);



		}else{
			alert(landingPage_msg["msg"])
		}
	}
})

