
jQuery('document').ready(function(){


});
function setClipboard() {
    url = window.location.origin + window.location.pathname.split('/')[0] + "/" + window.location.pathname.split('/')[1];
    console.log(url);
    var tempInput = document.createElement("input");
    tempInput.style = "position: absolute; left: -1000px; top: -1000px";
    tempInput.value = url;
    document.body.appendChild(tempInput);
    tempInput.select();
    document.execCommand("copy");
    document.body.removeChild(tempInput);
}