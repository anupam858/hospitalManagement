var patient_id;
var curr_med ;
var object_array=[];

function pat_set(pat){
    patient_id = pat.pat_id
    console.log(patient_id);
}

$( document ).ready(function() {
    $(function() {
        $('#alerttext').hide();
        $('#add_block').hide();
        $('form#searchForm').on('submit',function(event){
            $.ajax({
                url: "/pharmacy/issuemeds",
                data: JSON.stringify({med_name: $('#med_name').val(),
                        med_avail: $('#med_avail').val() }),
                type: 'POST',
                dataType : "json",
            })
            .done(function(data){
                console.log(data);
                if(data==null){
                    $('#add_block').hide();
                    document.getElementById("alerttext").innerHTML= "No Medicine Found";
                    $('#alerttext').show(500);
                    console.log("no data");
                }
                else{
                    $('#alerttext').hide();
                    var content= "<tr> \n <th scope=\"row\"><center>"+ data.med_id+"</center></th>\n <td><center>"+ data.med_name+ "</center></td> \n <td><center>"+ data.med_rate+
                    "</center></td> \n <td><center>" +data.med_qty+ "</center></td>\n</tr>";
                    document.getElementById("med_body").innerHTML = content;
                    $('#add_block').show();
                    $('#qty').attr("max",data.med_qty);
                    curr_med = {'med_id': data.med_id,'med_name': data.med_name,'med_rate': data.med_rate, 'qty_issued':0};
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
        $("form#addForm").on("submit", function(event){
            event.preventDefault();
            curr_med.qty_issued = Number($('#qty').val());
            object_array.push(curr_med);
            console.log(object_array);
            var content = "<tr> \n <th scope=\"row\"><center>"+ curr_med.med_name+"</center></th>\n <td><center>"+ curr_med.med_rate+ "</center></td> \n <td><center>"+ curr_med.qty_issued+
            "</center></td> \n <td><center>" + (curr_med.med_rate*curr_med.qty_issued) + "</center></td>\n</tr>";
            $("#med_issued_body").append(content);
            $('form#searchForm')[0].reset();
            $('#add_block').hide();
            document.getElementById("med_body").innerHTML = "";
            $('#qty').val('');
        });

        $('button#submit_button').on('click',function(event){

            for(var i=0; i<object_array.length;i++){
                delete object_array[i]['med_name'];
                delete object_array[i]['med_rate'];
            }
            console.log("update");
            $.post('/pharmacy/issuemeds', JSON.stringify({submit_button: $('#submit_button').val(),pat_id: patient_id, data: object_array}),
            function(url){
                window.location= url;
            });
           
        });
    });
});