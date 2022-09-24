function payBill(){
  amountPaid=$("#amountPaid").val();
  billName=$("#billToPay").val().toString();
  $.ajax({
    type: 'GET',
    url: '/html/getBillData',
    success: validBillName
  })
}


function validBillName(response){
  valid=false;
  for(let i = 0; i < response.length; i++){
    nameKey="billname"+i.toString();
    if(billName===response[nameKey]){
      valid=true;
    }
  }
  if(valid){
    $.ajax({
      type: 'POST',
      url: '/html/payBill',
      data: {"amountPaid":amountPaid, "billName":billName},
      success: payBillSuccess,
      error: payBillFail
    })
  }
  else{
    $('#flashMessage').html("The bill entered does not exist");
    const myTimeout = setTimeout(endFlashMessage, 3000);
    return false;
  }
}

function payBillSuccess(response){
  const currentBillDisplay = $("#unique").html();
  if(currentBillDisplay===response["billName"]){
    id="#"+response["billName"].toString()+response["username"];
    var display=response["username"]+" Due:£"+response["amountDue"]
    display=display+" Paid:£"+response["amountPaid"]
    $(id).html(display);

    billNameID='#'+response["billName"];
    $(billNameID).html(billName+" "+response["status"]);


    //name.innerHTML="<li onclick='showBill(billName)'>"+billName+"  PENDING</li>";

  }
}

function payBillFail(response){
  alert("Error Bill payment failed");
}


function showBill(billName){
  $.ajax({
    type: 'POST',
    url: '/html/displayBill',
    data: {"billName":billName},
    success: showBillSuccess,
    error: showBillFail
  })
}

function showBillSuccess(response){
    //intialising variables
    var key=""
    var value=""

    //$('#unique').html("<h2 id='unique' class='subheadingText'>"+response.username1+"</h2>");
    document.getElementById('unique').innerHTML = response["billName"];

    $('#billDetails').empty();
    for(let i = 0; i < response.length; i++){
      console.log(i);
      //Accessing username
      key="username"+i.toString();
      var username=response[key];
      //Accessing amountPaid
      key="amountPaid"+i.toString();
      var amountPaid=response[key];
      //Accessing amountDue
      key="amountDue"+i.toString();
      var amountDue=response[key];
      //Formatting html display
      var paid = document.createElement('li');
      paid.id = response["billName"]+username;
      display=username+" Due:£"+amountDue;
      paid.innerHTML=display+" Paid:£"+amountPaid;
      $('#billDetails').append(paid);

    }
  }

function showBillFail(response){
  alert("Error the bill could not be displayed");
}


function addBill(allUserNames){
  data={};
  billName=$("#billName").val();
  value="1";
  totalValue=0;
  count=0;
  valueCheck=true;
  //Looping through input boxes for all users
  for(let i = 0; i < allUserNames; i++){
    id="#"+i.toString();
    input=$(id).val()
    //Checking if input box is not empty
    if(input!=""){
      data[i.toString()]=input;
      totalValue=totalValue+parseInt(input);
      data["c"+count.toString()]=i;
      count=count+1;
      if(isValueValid(input)===false){
        valueCheck=false;
      }
    }
  }
  data['length']=count;
  data['billName']=billName;
  data['totalValue']=totalValue;




  if(isNameValid(billName)&&valueCheck){
    $.ajax({
      type: 'POST',
      url: '/html/addBill',
      data: data,
      success: billNameSuccess,
      error: billNameFail
    })

      var name = document.createElement('li');
      name.id = billName;
      name.innerHTML="<li onclick='showBill(billName)'>"+billName+"  PENDING</li>";

      $("#allBillNames").append(name);


  }
}


function endFlashMessage(){
  $('#flashMessage').empty();
}


function billNameSuccess(response){
  //Formatting flash flashMessage
  var message="New Bill called "+response['billName'];
  for(let i = 0; i < count; i++){
    message=message+", "+response[i.toString()];
  }
  $('#flashMessage').html(message);
  const myTimeout = setTimeout(endFlashMessage, 3000);
}

function billNameFail(response){
  alert("ERROR the bill name could not be added");
}







//Function to check input parameter only contains lettters
function isNameValid(name){
  //Checking if name was empty
  if(name==""){
    $('#flashMessage').html("The billname cannot be left blank");
    const myTimeout = setTimeout(endFlashMessage, 3000);
    return false;
  }
  //regular expression which only allows letters or spaces
  var letters=/^[A-Za-z\s]*$/;
  //Matching the regular expression against the input
  if(name.match(letters)){
     return true;
    }
  else{
    $('#flashMessage').html("The billname can only contain letters");
    const myTimeout = setTimeout(endFlashMessage, 3000);
    return false;
    }
}

//Function to check input parameter only contains numbers
function isValueValid(value){
  //regular expression which only allows number
  var numbers = /^[0-9]+$/;
  //Matching the regular expression against the input
  if(value.match(numbers))
    {
     return true;
    }
  else
    {
    $('#flashMessage').html("The amount to pay can only contain numbers");
    const myTimeout = setTimeout(endFlashMessage, 3000);
    return false;
    }
}
