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

