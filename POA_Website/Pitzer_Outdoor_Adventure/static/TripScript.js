/**
 * Created by matth_000 on 7/2/2017.
 */
$(document).ready(function ()
{
    var tripID =window.location.pathname.substr(7);
    //gets path for example /trips/1 and indexs to only get the trip ID
    $("#addParticipant").click(function ()
    {
        console.log("clicked");
        $.get('/api/addParticipant/' + tripID)
        .done(function(data)
        {
            $('#message-model-content').html(data);
            $("#generalizedModal").modal("show");
        })
    });
    $("#cannotLeave").click(function ()
    {
        console.log("clicked");
        $.get('/api/cannotLeave')
        .done(function(data)
        {
            console.log(data);
            $('#message-model-content').html(data);
            $("#generalizedModal").modal("show");
        });
    });
    $("#editParticipant").click(function ()
    {
        console.log("clicked");
        $.get('/api/editParticipant/' + tripID)
        .done(function(data)
        {
            console.log(data);
            $('#message-model-content').html(data);
            $("#generalizedModal").modal("show");
            /* Use this for hiding the modal via code --> $("#generalizedModal").modal("hide");*/
        });
    });
    $(".meterbar > span").each(function ()
    {
        $(this)
            .data("origWidth", $(this).width())
            .width(0)
            .animate({
                width: $(this).data("origWidth")
            }, 1200); /* <-- Duration of the animation */
    });
    $('[data-toggle="tooltip"]').tooltip();
    $("#timer").TimeCircles();
});
