// /**
//  * Created by matth_000 on 10/7/2018.
//  */
// console.log($("#Other_Diet_Restrictions_Box"));
// //$("input[value='Other_Diet_Restrictions_Box']").hide();
// $("#Other_Diet_Restrictions_Box").hide();
// $('[data-toggle="tooltip"]').tooltip();
// console.log("toolTips");

$(document).ready(function ()
{
    allergiesVisible = false;
    dietRestrictionsVisible = false;
    $("#otherAllergies").change(function ()
    {
        console.log("change");
        if (!allergiesVisible)
        {
            var alternateField = "<input id=\"Other_Allergies_Box\" name=\"Other_Allergies_Box\" class=\"form-control\" required=\"\" type=\"text\">";
            $("#otherAllergiesDiv").append(alternateField);
            allergiesVisible = true;
        }
        else
        {
            $("#Other_Allergies_Box").remove();
            allergiesVisible = false;
        }
    });
    $("#Diet_Restrictions_Box").change(function ()
    {
        console.log("diet restriction changes");
        console.log($(this)[0].value);
        console.log(dietRestrictionsVisible);
        if ($(this)[0].value === "Other" && !dietRestrictionsVisible)
        {
            var alternateField = "<input id=\"Other_Diet_Restrictions_Box\" name=\"Other_Diet_Restrictions_Box\" class=\"form-control\" required=\"\" type=\"text\">";
            console.log("yay im workin");
            $("#otherRestrictionsDiv").append(alternateField);
            dietRestrictionsVisible = true;
        }
        else if ($(this)[0].value != "Other" && dietRestrictionsVisible)
        {
            console.log("the bads are happening");
            $("#Other_Diet_Restrictions_Box").remove();
            dietRestrictionsVisible = false;
        }
    });
    $("#deleteRow").click(function ()
    {
        //console.log("yay im workin");
        if (counter > 0)
        {
            $("#costName" + counter).remove();
            $("#costMagnitude" + counter).remove();
            $("#para" + counter).remove();
            counter--;
        }
    });
});