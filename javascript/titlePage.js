$( function() {
  alert("Javascript linked");
  return true;
})

function displayInfo(){
  alert($('#titleContainer').html());
  $('#titleContainer').html("<p>Page info</p>");
}

function displayTitle(){
  alert("displaying title");
  $('#titleContainer').html("<h1>Splitinator</h1>");
}
