/**
 * Created by alasdairjohnson on 12/27/17.
 */


function editAccount(){
    $( "#editAccount" ).click(function() {
        $("#saveChanges").show();
        var userInfo = $(".UserInfo");
        userInfo.each(function () {
            var $this = $(this);
            var $input = $('<input>', {
            value: $this.text(),
            type: 'text',
            class: "form-control"
        }).appendTo( $this.empty() );
        console.log(this.innerHTML);
        });
        console.log(userInfo);


  // $( this ).replaceWith( "<div>" + $( this ).text() + "</div>" );
});
}

