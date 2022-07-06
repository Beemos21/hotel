
//if (!$) {
//    // Need this line because Django also provided jQuery and namespaced as django.jQuery
//    $ = django.jQuery;
//}
//
//$(document).ready(function() {
//    console.log('wwwww');
//    $("select[name='checking_date_0']").change(function() {
//        _datein = document.getElementById("id_checking_date_0");
//        alert(_datein.value);
//
//    });
//});
if (!$) {
    // Need this line because Django also provided jQuery and namespaced as django.jQuery
    $ = django.jQuery;
}

$(document).ready(function() {
const input = document.getElementById('id_checking_date_0');
//const log = document.getElementById('id_phone_number');


//$("select[name='checking_date_0']").change(function() {
//var x = document.getElementById("id_phone_number");
//  x.value = 'x.value.toUpperCase()';
//
//});

//$("#id_checking_date_0").on("click",function() {
//    alert('this.click');
//});

$("#id_checking_date_0").on("focus",function() {
    checkdates();
});
$("#id_checking_date_0").on("change",function() {
    checkdates();
});

$("#id_checkout_date_0").on("focus",function() {
    checkdates();
});
$("#id_checkout_date_0").on("change",function() {
    checkdates();
});

function checkdates(){
    today = new Date();
    now_date = today.getFullYear()+'-'+(today.getMonth()+1)+'-'+today.getDate();

    checking = document.getElementById('id_checking_date_0');
//    clocklink1 = document.getElementById('calendarlink0');
//alert(clocklink1);
//
// calendarbox0 = document.getElementById('calendarbox0');
//alert(calendarbox0);


    nb = document.getElementById('id_total_days');

    checkout = document.getElementById('id_checkout_date_0');

    checking_date = new Date(checking.value);
    checkout_date = new Date(checkout.value);

    if(checking_date.getTime() < today.getTime())
    {
        checking.value = now_date;
        checking_date = new Date(checking.value);
//        return
    }

    if(checking_date.getTime() > checkout_date.getTime())
    {
        checking.value = now_date;
        checkout.value = now_date;
         nb.value = 0;
        return
    }

    Difference_In_Time = checkout_date.getTime() - checking_date.getTime();


    Difference_In_Days = parseInt(Difference_In_Time / (1000 * 3600 * 24));

//    alert(Difference_In_Days);
    nb.value = Difference_In_Days;
//    var today = new Date();
//    var date = today.getFullYear()+'-'+(today.getMonth()+1)+'-'+today.getDate();
//    var time = today.getHours() + ":" + today.getMinutes() + ":" + today.getSeconds();
//        nb.value=date;

//    log.value = 33;
}

$(function(){
    var dtToday = new Date();

    var month = dtToday.getMonth() + 1;
    var day = dtToday.getDate();
    var year = dtToday.getFullYear();
    if(month < 10)
        month = '0' + month.toString();
    if(day < 10)
        day = '0' + day.toString();

    var minDate= year + '-' + month + '-' + day;

    $('#id_checking_date_0').attr('min', minDate);
});
});