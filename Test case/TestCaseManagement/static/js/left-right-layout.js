/*! liu_hui */
function byId(id) {return document.getElementById(id)} 
window.onload = function() { 
left = byId("left"), right = byId("right"), middle = byId("middle"); 
var middleWidth=9; 
middle.onmousedown = function(e) { 
var disX = (e || event).clientX; 
middle.left = middle.offsetLeft; 
document.onmousemove = function(e) { 
var iT = middle.left + ((e || event).clientX - disX); 
var e=e||window.event,tarnameb=e.target||e.srcElement; 
maxT=document.body.clientWidth; 
iT < 0 && (iT = 0); 
iT > maxT && (iT = maxT); 
middle.style.left = left.style.width = iT + "px"; 
right.style.width = document.body.clientWidth - iT -middleWidth + "px"; 
right.style.left = iT+middleWidth+"px"; 
return false 
}; 
document.onmouseup = function() { 
document.onmousemove = null; 
document.onmouseup = null; 
middle.releaseCapture && middle.releaseCapture() 
}; 
middle.setCapture && middle.setCapture(); 
return false 
}; 

}; 


