/**
 * Created by alasdairjohnson on 12/27/17.
 */

/**
 * EditAccount
 * sets up buttons to be able to update account without
 * page relode
 * this acomplished with buttons
 * editAccount- transforms td to input feilds and shows the savechanges buttons
 * saveChanges- saves the changes with ajax call to server from input feilds
 */
function editAccount(){
    $( "#editAccount" ).click(function(){
        $( "#editAccount" ).hide();
        createInputFeilds()
    });
    $("#saveChanges").click(function () {
        $( "#editAccount" ).show();
        $('.userEditInput').tooltip('dispose');//hide any potential errors
        var fields = $(".userEditInput");//gets input feilds
        sendData(fields, $(".userID")[0].id);
        }
    );
}


function createInputFeilds(){
     $("#saveChanges").show();//shows the save changes button
        var userInfo = $(".UserInfo");//gets all the td feilds of this class
        userInfo.each(function () {//iterates through each feild
            var $this = $(this);//online code not sure why this is nesasary

            //console.log($this);
            var $input = $('<input>', {
            value: $this.text(),
            type: 'text',
            class: "form-control userEditInput",
            id: this.id + "input"

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
    $("#phoneNumer").text(user["phoneNumber"]);
    $("#age").text(user["age"]);
    $("#carCapacity").text(user["carCapacity"]);
    $("#height").text(user["height"])
}

function sendData(feilds, clientID){
    $.ajax({
      type: "POST",
      url: "/api/updateUser",
      data: getFeilds(feilds, clientID),
      success: function(response) {
                console.log(response);
                if (response["status"]==="error"){
                    parseErrors(response["errors"]);
                }
                else{
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

//Parsley Validation

// $(function ()
//     {
//         $('#userEditInput').parsley().on('field:error', function (fieldInstance)
//          {
//             fieldInstance.$element.popover(
//             {
//                 trigger: 'manual',
//                 container: 'body',
//                 placement: 'right',
//                 content: function ()
//                 {
//                     return fieldInstance.getErrorsMessages().join(';');
//                 }
//             }).popover('show');
//         })
//         .on('field:success', function (fieldInstance)
//         {
//             fieldInstance.$element.popover('dispose');
//          });
//     });


    //currently not in use needs work to figure out how
    //to get it so that we check the date is current
    //and that the dates are sequential
