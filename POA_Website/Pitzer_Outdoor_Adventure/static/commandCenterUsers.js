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
        // var allTrips = $(".accountEditForm").attributes;
        // console.log(table.row(this).data().id);
        getUserModal(table.row(this).data().id);
    });

}
function getUserModal(id)
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
            parseTrips(id);
            $('#generalizedModal').modal('hide');
            tableOfTrips.ajax.reload();
            console.log("Made the table reload.");
        });
    });
}

function parseTrips(id)
{
    parseTripsGetHelper(function (data) {
        parseTripsParseHelper(data, id);
    });
}
function parseTripsGetHelper(callback) {
    $.get("/api/getTripIDs", callback);
}

function parseTripsParseHelper(data, id) {
    out = {};
    console.log(data.data);
    out["adminOut"] = $("#adminOutBox")[0].checked;
    out["tripsOut"] = [];
    console.log("Trips are below:");
    for (var i = 0; i < data.data.length; i++)
    {
        var idNum = data.data[i];
        console.log(idNum);
        var update = {};
        if ($("#" + idNum + "OnTrip").checked)
        {
            update["add"] = true;
        }
        else
        {
            update["add"] = false;
        }
        console.log("#" + idNum + "CarCapacity");
        console.log($("#" + idNum + "CarCapacity"));
        var carCapacity = $("#" + idNum + "CarCapacity")[0].value;
        if (carCapacity == "")
        {
            update["carCapacity"] = 0;
        }
        else
        {
            update["carCapacity"] = parseInt(carCapacity);
        }
        if ($("#" + idNum + "IsCoordinator").checked)
        {
            update["isCoordinator"] = true;
        }
        else
        {
            update["isCoordinator"] = false;
        }
        update["userID"] = parseInt(id);
        out["tripsOut"].push(update);
    }
    console.log("Hey there, mateys.");
    console.log(out);
    var jsonOut = JSON.stringify(out);
    sendData(jsonOut);
}
function sendData(data)
{
    $.ajax
    ({
        type: "POST",
        url: "/api/updateUser",
        data: data,
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

