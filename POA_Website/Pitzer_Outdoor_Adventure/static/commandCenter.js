/**
 * Created by matth_000 on 10/26/2017.
 */
$(document).ready(function ()
{
  //table
    CreateTable("userTable");
    // $("#AddClient").bind('click', function(){
    //     makeClientAddPop();
    // });
});



/**
 * Parama tableID: the id of the table we which to create
 * returns: creates a table with modals yay
 */
function CreateTable(tableID)
{
    var table = $("#" + tableID).DataTable({ //targets table and creates table
        "ajax": {
            "url": "/api/getUsers"
        },
        "columns": [
            {
                "data": "username"
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
        getModal(table.row(this).data().id);
    });
}
function getModal(id)
{
    console.log(id);
    $.get('/api/adminDialogue/' + id)
    .done(function(data)
    {
        $('#message-model-content').html(data);
       // setDropDown(data["data"]);
        $('#generalizedModal').modal('show');
        console.log($(".form-check-input"));
        $("#submitBtn").on("click", function ()
        {
            var trips = $(".form-check-input");
            parseTrips(trips);
        });
        // $('#checkIn').on('click', function ()
        // {
        //     var checkbox = $(".itemCheckBox input:checkbox");
        //     sendData(checkbox, data["ClientID"]);
        //     $('#user1Message').modal('toggle');
        // })
    });
}

function parseTrips(trips)
{
    // Parses the trips.
    for (var index in trips)
    {
        if (trips[index].checked)
        {
            var trip=trips[index];
            console.log(trip.id);
            var id = trip.id.slice(0, -6);
            console.log(id);
            var carCapacity = $("#" + id + "CarCapacity")[0].value;
            console.log(carCapacity);
        }
    }
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

