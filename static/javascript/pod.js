// $('#new-collection').on('click', (evt) => {
//     evt.preventDefault();
  
//     // Get user input from a form
//     const formData = {
//       city: $('#city-field').val(),
//       address: $('#adr-field').val()
//     };
  
//     // Send formData to the server (becomes a query string)
//     $.get('/delivery-info.json', formData, (res) => {
//       // Display response from the server
//       alert(`This will cost $${res.cost}`);
//       alert(`This will arrive in ${res.days} day(s)`);
//     });
//   });

var myModal = document.getElementById('myModal')
var myInput = document.getElementById('myInput')

myModal.addEventListener('shown.bs.modal', function () {
  myInput.focus()
})


function addToCollection(results) {
  $("#weather-info").html(results.forecast);
}

function showWeather(evt) {
  evt.preventDefault();

  let url = "/weather.json";
  let formData = {"zipcode": $("#zipcode-field").val()};

  $.get(url, formData, replaceForecast);
}

$("#weather-form").on('submit', showWeather);


$('#exampleModal').on('show.bs.modal', function (event) {
  var button = $(event.relatedTarget) // Button that triggered the modal
  var recipient = button.data('whatever') // Extract info from data-* attributes
  // If necessary, you could initiate an AJAX request here (and then do the updating in a callback).
  // Update the modal's content. We'll use jQuery here, but you could use a data binding library or other methods instead.
  var modal = $(this)
  modal.find('.modal-title').text('New message to ' + recipient)
  modal.find('.modal-body input').val(recipient)
})
