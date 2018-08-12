/**
 * Created by alasdairjohnson on 12/27/17.
 */

/**
 * EditAccount
 * sets up buttons to be able to update account without
 * page reloaded
 * this accomplished with buttons
 * editAccount- transforms td to input fields and shows the savechanges buttons
 * saveChanges- saves the changes with ajax call to server from input feilds
 */
function editAccount(){
    $("#editAccount" ).click(function(){
        $("#editAccount" ).hide();
        createInputFeilds()
    });
    $("#saveChanges").click(function () {

        $('.userEditInput').tooltip('dispose');//hide any potential errors
        var fields = $(".userEditInput");//gets input fields
        sendData(fields, $(".userID")[0].id);
        }
    );
}


function createInputFeilds(){
     $("#saveChanges").show();//shows the save changes button
        var userInfo = $(".UserInfo");//gets all the td fields of this class
        userInfo.each(function () {//iterates through each field
            var $this = $(this);//online code not sure why this is necessary

            //console.log($this);
            var $input = $('<input>', {
            value: $this.text(),
            type: 'text',
            class: "form-control userEditInput",
            id: this.id + "Input"

        });//constructs the replacment for the td feild
        $input.attr("data-parsley-type","integer");
        $input.appendTo( $this.empty() );//replaces the feild
        // console.log(this.innerHTML);
        });
       // console.log(userInfo);
}

function getFeilds(feilds, clientID){
    update = {"googleNum":clientID};//return object
    feilds.each(function(){
        update[this.id] = this.value;
    });//iterate through the feilds to build object to send to server
    //console.log(update);
    return JSON.stringify(update);
}

/**
 * will update client table to reflect new values sent from server
 * @param user
 */
function updateClient(user){
    $(".userEditInput").hide();//hide input feilds
    $("#studentID").text(user["studentIDNumber"]);
    $("#email").text(user["email"]);
    $("#phoneNumber").text(user["phoneNumber"]);
    $("#age").text(user["age"]);
    $("#carCapacity").text(user["carCapacity"]);
    $("#height").text(user["height"])
}

function sendData(feilds, clientID){
    $.ajax({
      type: "POST",
      url: "/api/updateUserAccount",
      data: getFeilds(feilds, clientID),
      success: function(response) {
                if (response["status"]==="error"){
                    parseErrors(response["errors"]);
                }
                else{
                $( "#editAccount" ).show();
                user = response["user"];
                updateClient(user);
                $("#saveChanges").hide();
                }

            },
      dataType: "json",
      contentType: "json/application"
    });
}

function parseErrors(errors){
    for (var errorID in errors) {
        if (errors.hasOwnProperty(errorID)) {
            var errorText = errors[errorID];
            console.log(errorID + " -> " + errors[errorID]);
            $("#" + errorID).tooltip(
            {
                trigger : "manual",
                placement: 'bottom',
                title: errorText
            }).tooltip('show');
        }
    }
}

function displayTripsModal()
{
    $.get("/api/tripDisplay")
    .done(function(data)
    {
        $('#message-model-content').html(data);
        $('#generalizedModal').modal('show');
    });
}
