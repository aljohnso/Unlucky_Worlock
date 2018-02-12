/**
 * Created by matth_000 on 10/26/2017.
 */
$(document).ready(function ()
{
  //table
    CreateUserTable("userTable");
    // $("#AddClient").bind('click', function(){
    //     makeClientAddPop();
    // });
});



/**
 * Params tableID: the id of the table we which to create
 * returns: creates a table with modals yay
 */
function CreateUserTable(tableID)
{
    var table = $("#" + tableID).DataTable({ //targets table and creates table
        "ajax": {
            "url": "/api/getUsers"
        },
        "columns": [
            {
                "data": "username"
            },
            {
               "data": "studentIDNumber"
            },
            {
                "data": "phoneNumber"
            },
            {
                "data": "email"
            }
            // ,
            // {
            //     "data": "accountButtons"
            // }
        ]
    });
    $("#" + tableID + " tbody").on('click', 'tr', function()
    {
        console.log($(".accountEditForm").attributes);
        var allTrips = $(".accountEditForm").attributes;
        // console.log(table.row(this).data().id);
        getUserModal(table.row(this).data().id, allTrips);
    });

}
function getUserModal(id, allTrips)
{
    //console.log(id);
    // id is the user id (?).
    $.get('/api/adminDialogueUser/' + id)
    .done(function(data)
    {
        $('#message-model-content').html(data);
        $('#generalizedModal').modal('show');
        console.log($(".form-check-input"));
        $("#submitBtn").on("click", function ()
        {
            // var trips = $(".form-check-input");
            //var tripLength = $(".form-check-input").length;
            sendData(id, allTrips);
            $('#generalizedModal').modal('hide');
            tableOfTrips.ajax.reload();
            console.log("Made the table reload.");
        });
    });
}

function parseTrips(id, allTrips)
{
    out = {};
    out["id"] = id;
    out["adminOut"] = $("#adminOutBox")[0].checked;
    console.log("Trips are below:");
    for (var trips in allTrips)
    {
        console.log(trips);
        // Okay, here's what you need to do. First, find some way to access a list of all trip IDs
        // inside of this function, then loop through them. Use the same code as from
        // commandCenterTrips to assign your desired variables, but append the ID number to the front
        // of all the IDs you have in the html for the AdminDialogueUserModal.
        // If you can pull that off, you have all the data you need.
        //console.log(index);
        if (trips[index].checked)
        {
            $("#adminOutBox")[0] = $(".userID")[0].id;
            //console.log(userID);
            var trip = trips[index];
            //console.log(trip.id);
            var id = trip.id.slice(0, -6);
            //console.log(id);
            var carCapacity = $("#" + id + "CarCapacity")[0].value;
            //console.log(carCapacity);
            var update = {};
            update["tripID"] = parseInt(id);
            if (carCapacity == "")
            {
                update["carCapacity"] = 0;
            }
            else
            {
                update["carCapacity"] = parseInt(carCapacity);
            }
            update["userID"] = parseInt(userID);
            update["add"] = true;
            out["tripsOut"].push(update);
        }
        else
        {
            var userID = $(".userID")[0].id;
            var trip = trips[index];
            var id = trip.id.slice(0, -6);
            var update = {};
            update["tripID"] = parseInt(id);
            update["carCapacity"] = 0;
            update["userID"] = parseInt(userID);
            update["add"] = false;
            out["tripsOut"].push(update);
        }
    }
    //$("#frozen")[0].checked;
    // out["tripsOut"] = [];
    // out["adminOut"] = false;
    // console.log(out);
    // Parses the trips.
    // var myStringArray = ["Hello","World"];
    // var arrayLength = myStringArray.length;
    // for (var i = 0; i < arrayLength; i++)
    // {
    //     alert(myStringArray[i]);
    //     //Do something
    // }
    // if (trips[0].checked)
    // {
    //     out["adminOut"] = true;
    // }
    // for (var index = 1; index < trips.length; index++)
    // {
    //     //console.log(index);
    //     if (trips[index].checked)
    //     {
    //         var userID = $(".userID")[0].id;
    //         //console.log(userID);
    //         var trip = trips[index];
    //         //console.log(trip.id);
    //         var id = trip.id.slice(0, -6);
    //         //console.log(id);
    //         var carCapacity = $("#" + id + "CarCapacity")[0].value;
    //         //console.log(carCapacity);
    //         var update = {};
    //         update["tripID"] = parseInt(id);
    //         if (carCapacity == "")
    //         {
    //             update["carCapacity"] = 0;
    //         }
    //         else
    //         {
    //             update["carCapacity"] = parseInt(carCapacity);
    //         }
    //         update["userID"] = parseInt(userID);
    //         update["add"] = true;
    //         out["tripsOut"].push(update);
    //     }
    //     else
    //     {
    //         var userID = $(".userID")[0].id;
    //         var trip = trips[index];
    //         var id = trip.id.slice(0, -6);
    //         var update = {};
    //         update["tripID"] = parseInt(id);
    //         update["carCapacity"] = 0;
    //         update["userID"] = parseInt(userID);
    //         update["add"] = false;
    //         out["tripsOut"].push(update);
    //     }
    // }
    console.log(out);
    return JSON.stringify(out);
}

function sendData(id, allTrips)
{
    $.ajax
    ({
        type: "POST",
        url: "/api/updateUser",
        data: parseTrips(id, allTrips),
        success: function()
        {
          console.log("success");
        },
        dataType: "json",
        contentType: "json/application"
    });
}

// function setDropDown(data){
//     for (var key in data){
//         setNumber(data[key]["CheckoutID"],data[key]["numCheckedOut"],data[key]["numCheckedOut"])
//     }
// }

// function setNumber(classID, numberSelected, range){
//     var $select = $("select." + classID);
//     for (var i=1;i<=range;i++){
//         $select.append($('<option></option>').val(i).html(i))
//     }
//     $select.val(numberSelected)
// }

// function processForm(checkbox, clientID) {
//     var out = [];
//     for (var index in checkbox){
//         if (checkbox[index].checked){
//             var data = {};
//             data["checkedOutID"] = checkbox[index].id;
//             data["numberReturn"] = $('select.' + checkbox[index].id).val();
//             data["clientID"] = clientID;
//             out.push(data);
//         }
//     }
//     return JSON.stringify(out);
//     }

// function sendData(checkbox, clientID){
//     $.ajax({
//       type: "POST",
//       url: "/api/returnItem",
//       data: processForm(checkbox, clientID),
//       success: function() {
//                 console.log("success");
//             },
//       dataType: "json",
//       contentType: "json/application"
//     });
// }

