/**
 * Created by matth_000 on 12/30/2017.
 */
$(document).ready(function ()
{
  //table
    CreateTripTable("tripsTable");
});



/**
 * Params tableID: the id of the table we which to create
 * returns: creates a table with modals yay
 */
function CreateTripTable(tableID)
{
    var table = $("#" + tableID).DataTable({ //targets table and creates table
        "ajax": {
            "url": "/api/getTrips"
        },
        "columns": [
            {
                "data": "trip"
            },
            {
               "data": "Participant_Cap"
            },
            {
                "data": "Participant_Num"
            },
            {
               "data": "Car_Cap"
            },
            {
                "data": "Car_Num"
            },
            {
                "data": "Departure_Date"
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
        getTripModal(table.row(this).data().id, table);
    });
}
function getTripModal(id, table)
{
    //console.log(id);
    $.get('/api/adminDialogueTrip/' + id)
    .done(function(data)
    {
        $('#message-model-content').html(data);
       // setDropDown(data["data"]);
        $('#generalizedModal').modal('show');
        // console.log($(".form-check-input"));


        $("#submitBtnTrip").on("click", function ()
        {
            // console.log("Hi there!");
            // var form1 = $(".form-check-input");
            // var form2 = $(".form-control");
            // var form = $("#tripform");
            // var form = $(".tripform");
            // sendTripData2(form1, form2);
            // console.log(form);
            sendTripData(id);
            $('#generalizedModal').modal('hide');
        });
        $("#deleteBtn").on("click", function ()
        {
            $.ajax
            ({
                type: "GET",
                url: "/api/deleteTrip/" + id,
                data: {},
                success: function()
                {
                  console.log("success");
                },
                dataType: "json",
                contentType: "json/application"
            });
            $('#generalizedModal').modal('hide');
            table.ajax.reload();
        });

        // $('#checkIn').on('click', function ()
        // {
        //     var checkbox = $(".itemCheckBox input:checkbox");
        //     sendData(checkbox, data["ClientID"]);
        //     $('#user1Message').modal('toggle');
        // })
    });
}

function parseTripForm(id)
{
    console.log("parse trips Form");
    out = {};
    // console.log($("#frozen")[0].checked);
    // console.log($("#thawtime")[0].value);
    // console.log($("#substancefree")[0].checked);
    // console.log($("#maxcars")[0].value);
    // console.log($("#maxparticipants")[0].value);
    out["id"] = id;
    out["frozen"] = $("#frozen")[0].checked;
    out["thawtime"] = $("#thawtime")[0].value;
    out["substancefree"] = $("#substancefree")[0].checked;
    out["maxcars"] = $("#maxcars")[0].value;
    out["maxparticipants"] = $("#maxparticipants")[0].value;
    // Need to return something else, this is a short-stop.
    return JSON.stringify(out);
}

function sendTripData(id)
{
    $.ajax
    ({
        type: "POST",
        url: "/api/updateTrip",
        data: parseTripForm(id),
        success: function()
        {
          console.log("success");
        },
        dataType: "json",
        contentType: "json/application"
    });
}

// function parseTripForm2(form1, form2)
// {
//     console.log(form1);
//     console.log(form2);
//     out = {};
//     out["frozen"] = form1["frozen"];
//     out["thawtime"] = form2["thawtime"];
//     out["substancefree"] = form1["substancefree"];
//     out["maxcars"] = form2["maxcars"];
//     out["maxparticipants"] = form2["maxparticipants"];
//     out["thing"] = form1;
//     // Need to return something else, this is a short-stop.
//     return JSON.stringify(out);
// }

function sendTripData2(form1, form2)
{
    $.ajax
    ({
        type: "POST",
        url: "/api/updateTrip",
        data: parseTripForm2(form1, form2),
        success: function()
        {
          console.log("success");
        },
        dataType: "json",
        contentType: "json/application"
    });
}

/*function parseTrips(trips)
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

function sendTripData(trips)
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
}*/

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

