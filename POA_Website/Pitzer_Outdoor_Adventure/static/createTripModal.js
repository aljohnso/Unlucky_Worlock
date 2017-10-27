/**
 * Created by matth_000 on 10/26/2017.
 */

$(document).ready(function ()
{
    var counter = 1;
    $('[data-toggle="tooltip"]').tooltip();
    $("#addRow").click(function ()
    {
        counter++;
        var newCost = "<input id=\"costName" + counter + "\" name=\"costName" + counter + "\" class=\"form-control\" required=\"\" type=\"text\" placeholder=\"Name of Expense\"> <input id=\"costMagnitude" + counter + "\" name=\"costMagnitude" + counter + "\" class=\"form-control\" required=\"\" type=\"text\" placeholder=\"Cost\" data-parsley-type=\"number\"> <p id=para" + counter + "></p>";
        console.log("yay im workin");
        //$("#additionalCostBreakdownDiv").append($(".cost"));
        $("#additionalCostBreakdownDiv").append(newCost);
    });
    $("#deleteRow").click(function ()
    {
        console.log("yay im workin");
        if (counter > 0)
        {
            $("#costName" + counter).remove();
            $("#costMagnitude" + counter).remove();
            $("#para" + counter).remove();
            counter--;
        }
    });
});

$(function ()
{
    $('#openForm').parsley().on('field:validated', function()
    {
        var ok = $('.parsley-error').length === 0;
        //$('.bs-callout-info').toggleClass('hidden', !ok);
        //$('.bs-callout-warning').toggleClass('hidden', ok);
    })
    .on('form:submit', function()
    {
        $.post("api/addTrip", $("#openForm").serialize());
        console.log($('#openForm').serialize());
        console.log("it worked!!!! the demo was a lie");
        $(location).reload();
        return false; // Don't submit form for this demo
    });
});