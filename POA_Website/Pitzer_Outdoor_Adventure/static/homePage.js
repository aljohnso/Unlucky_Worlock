/**
 * Created by alasdairjohnson on 10/18/17.
 */
    $(document).ready(function ()
    {
        $("#addTrip").click(function ()
        {
            console.log("clicked");
            $.get('/api/addTrip').done(function (data)
            {
                console.log(data);
                $('#message-model-content').html(data);
                $("#generalizedModal").modal("show");
            });
        })
        $("#notLoggedIn").click(function ()
        {
            console.log("clicked");
            $.get('/api/popUpMessage/' + 'Not Logged In' + "/" + "You must be logged in to add a new trip.")
            .done(function (data)
            {
                console.log(data);
                $('#message-model-content').html(data);
                $("#generalizedModal").modal("show");
            });
        })
    });