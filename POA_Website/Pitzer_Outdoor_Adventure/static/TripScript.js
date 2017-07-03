/**
 * Created by matth_000 on 7/2/2017.
 */
$(document).ready(function ()
{
    $("#addParticipant").click(function()
    {
        $.get('/addParticipant' + id)
        .done(function(data)
        {
            $('#message-model-content').html(data);
            $("#addParticipantModal").modal("show");
        });
    })
})