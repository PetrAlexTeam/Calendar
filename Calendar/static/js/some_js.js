jQuery('document').ready(function(){
    url = $(location).attr('href');
//    alert("js join");

    //$('.today_task a').attr("href", $(location).attr('href'))

    $('textarea').text(url);


    $('button').on('click', function() {
        document.querySelector("#share-links").select();
        document.execCommand('copy');
    });
});
//alert("Hi, world!");