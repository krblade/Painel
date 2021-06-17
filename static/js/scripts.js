// $(document).ready(function(){
    
//     var btnBusca = $("#busca");
//     var frmBusca = $("#busca-lotes");

//     $(btnBusca).on('click', function(e){

//         frmBusca.submit();

//     });

// });

$(document).ready(function() {
    var table = $('#dataTable').DataTable();
     
    $('#dataTable tbody')
        .on( 'mouseenter', 'td', function () {
            var colIdx = table.cell(this).index();
            var rowIdy = table.cell(this).index().row;
 
            $( table.cells().nodes() ).removeClass( 'highlight' );
            $( table.cell( colIdx ).nodes() ).addClass( 'highlight' );
            
        } );
} );