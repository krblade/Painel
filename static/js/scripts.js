// $(document).ready(function(){
    
//     var btnBusca = $("#busca");
//     var frmBusca = $("#busca-lotes");

//     $(btnBusca).on('click', function(e){

//         frmBusca.submit();

//     });

// });
$('#cont').hide();
$('#exportar').hide();
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


setTimeout(function(){
    if ($('#msg').is(':empty')) {
    }else{
        $('#msg').remove();
    }
}, 2000)

$.ajax({
    type:'GET',
    url:'/lotes-lista',
    success: function(res){
        console.log('sucesso')
        $('#loader').hide();
        $('#cont').show();
    }

})
$('#busca').click(function(){ 
    $('#loader').show();
    $('#cont').hide();
});
