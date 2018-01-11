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
        console.log(table.row(this).data().id);
        getUserModal(table.row(this).data().id);
    });
}
function getUserModal(id)
{
    //console.log(id);
    $.get('/api/adminDialogue/' + id)
    .done(function(data)
    {
        $('#message-model-content').html(data);
        $('#generalizedModal').modal('show');
        console.log($(".form-check-input"));
        $("#submitBtn").on("click", function ()
        {
            var trips = $(".form-check-input");
            sendData(trips);
            $('#generalizedModal').modal('hide');
        });
    });
}

function parseTrips(trips)
{
    out = {};
    out["tripsOut"] = [];
    out["adminOut"] = false;
    console.log(out);
    // Parses the trips.
    // var myStringArray = ["Hello","World"];
    // var arrayLength = myStringArray.length;
    // for (var i = 0; i < arrayLength; i++)
    // {
    //     alert(myStringArray[i]);
    //     //Do something
    // }
    if (trips[0].checked)
    {
        out["adminOut"] = true;
    }
    for (var index = 1; index < trips.length; index++)
    {
        //console.log(index);
        if (trips[index].checked)
        {
            var userID = $(".userID")[0].id;
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
    console.log(out);
    return JSON.stringify(out);
}

function sendData(trips)
{
    $.ajax
    ({
        type: "POST",
        url: "/api/updateUser",
        data: parseTrips(trips),
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

