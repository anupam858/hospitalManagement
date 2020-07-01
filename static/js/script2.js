var patient_id;
var curr_diag ;
var object_array=[];

function pat_set(pat){
    patient_id = pat.pat_id
    console.log(patient_id);
}

$( document ).ready(function() {
    $(function() {
        $('#alerttext').hide();
        $('#select_list').on('change',function(event){
            $.ajax({
                url: "/diagnosis/addtests",
                data: JSON.stringify({test_name: $('#select_list').val()}),
                type: 'POST',
                dataType : "json",
            })
            .done(function(data){
                console.log(data);
				if(data=='Select Option'){
                    $('#add_block2').hide();
                    document.getElementById("alerttext").innerHTML= "Invalid Selection";
                    $('#alerttext').show(500);
                    console.log("no data");
                }
				else{
                    $('#alerttext').hide();
                    var content= "<tr> \n <th scope=\"row\"><center>"+ data.test_id+"</center></th>\n <td><center>"+ data.test_name+ "</center></td> \n <td><center>"+ data.test_charge+
                    "</center></td> \n </tr>";
                    document.getElementById("diagnostics_body").innerHTML = content;
                    $('#add_block2').show();
                    curr_diag = {'test_id': data.test_id,'test_name': data.test_name,'test_charge': data.test_charge};
                }
            })
            .fail(function( xhr, status, errorThrown ) {
                alert( "Sorry, there was a problem!" );
                console.log( "Error: " + errorThrown );
                console.log( "Status: " + status );
                console.dir( xhr );
            });
            event.preventDefault();
        });
        $("form#addForm2").on("submit", function(event){
            event.preventDefault();
            object_array.push(curr_diag);
            console.log(object_array);
            var content = "<tr> \n <th scope=\"row\"><center>"+ curr_diag.test_name+"</center></th>\n <td><center>"+ curr_diag.test_charge "</tr>";
            $("#added_diagnostics").append(content);
            $('form#selectForm')[0].reset();
            $('#add_block2').hide();
            document.getElementById("diagnostics_body").innerHTML = "";
        });

        $('button#submit_button').on('click',function(event){

            for(var i=0; i<object_array.length;i++){
                delete object_array[i]['test_name'];
                delete object_array[i]['test_charge'];
            }
            console.log("update");
            $.post('/diagnosis/addtests', JSON.stringify({submit_button: $('#submit_button').val(),pat_id: patient_id, data: object_array}),
            function(url){
                window.location= url;
            });
           
        });
    });
});