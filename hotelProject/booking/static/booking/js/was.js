//from xmlrpc.client import ServerProxy

if (!$) {
    // Need this line because Django also provided jQuery and namespaced as django.jQuery
    $ = django.jQuery;
}

$(document).ready(function() {
//    const thedata ='';
    async function get(url){
        const resp = await fetch(url);
        const thedata = await resp.json();
//        thedata = data ;
//        console.log(data);
        return thedata ;
    }
    $("select[name='customer']").change(function() {



        d = document.getElementById("id_phone_number").value;
            alert(d);
        x=document.getElementById("id_phone_number");
//        x.value="7011223344";
//        x=document.getElementById("id_booking_status");
//        console.log(x);
//        console.log(x.value);

        x=document.getElementById("id_checking_date_1");

//        console.log(x.value);
        var today = new Date();
        var date = today.getFullYear()+'-'+(today.getMonth()+1)+'-'+today.getDate();
        var time = today.getHours() + ":" + today.getMinutes() + ":" + today.getSeconds();
        x.value=time;

        let country_field = document.getElementById("id_customer");
         let city_field = document.getElementById("id_booking_status");
         country_id = 1;
         const data = { user_id: country_id};
//            let url = " {% url 'customers' %} ";
//let url = "http://127.0.0.1:8000/booking/customers/";
//            console.log(url);
//             fetch(url, {
//  method: 'GET', // or 'PUT'
//  headers: {
//    'Content-Type': 'application/json',
////    'X-CSRFToken': csrftoken
//  },
//  body: JSON.stringify(data),
//})
//.then(response => response.json())
//.then(data => {
//  console.log('Success:', data[0]['name']);
//console.log(response);
//
//  city_field.innerHTML = `<option value = "" selescted>---------------</option>`
//  for(let i = 0; i<data.length; i++){
//      city_field.innerHTML += `<option value = "${data[i]["id"]}" selescted>${data[i]["name"]}</option>`
//
//  }
//})
//.catch((error) => {
////  console.error('Error:', error);
//});
    let   currentUrl = window.location.href;
//    console.log(currentUrl);

    _hostname = window.location.hostname
//    console.log(_hostname);

    _port = window.location.port
//    console.log(_port);

    _protocol = window.location.protocol
//    console.log(_protocol);


    let urlconcat = _protocol + "//" + _hostname
    if (_port!='')
        urlconcat = urlconcat + ":" + _port;

//     console.log(urlconcat);
//    let url = "http://127.0.0.1:8000/booking/customers/";
        let url = urlconcat + "/booking/customers/";
//
//    fetch(url)
//    .then((response) => {
//      return response.json();
//    })
//    .then((data) => {
//      return data;
//    });

//      console.log('data');
    wassim = await get(url);
    thedata = wassim;
      console.log(thedata);
    });
});

//let country_field = document.getElementById("id_customer")
//        let city_field = document.getElementById("id_booking_status")
//        country_field.addEventListener("change", pickState)
//        function pickState(e){
//            country_id = e.target.value
//            const data = { user_id: country_id}
//            let url = " {% url 'customers' %} "
//
//fetch(url, {
//  method: 'POST', // or 'PUT'
//  headers: {
//    'Content-Type': 'application/json',
//    'X-CSRFToken': csrftoken
//  },
//  body: JSON.stringify(data),
//})
//.then(response => response.json())
//.then(data => {
//  console.log('Success:', data[0]['name']);
//
//  city_field.innerHTML = `<option value = "" selescted>---------------</option>`
//  for(let i = 0; i<data.length; i++){
//      city_field.innerHTML += `<option value = "${data[i]["id"]}" selescted>${data[i]["name"]}</option>`
//
//  }
//})
//.catch((error) => {
//  console.error('Error:', error);
//});
//
//        }




