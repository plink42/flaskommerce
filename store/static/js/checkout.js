$(document).ready(function() {
    if($('#shipsame').prop('checked')){
        $('#billfname').change(function() {
            $('#shipfname').val($('#billfname').val());
        });
        $('#billlname').change(function() {
            $('#shiplname').val($('#billlname').val());
        });
        $('#billaddress1').change(function() {
            $('#shipaddress1').val($('#billaddress1').val());
        });
        $('#billaddress2').change(function() {
            $('#shipaddress2').val($('#billaddress2').val());
        });
        $('#billcountry').change(function() {
            $('#shipcountry').val($('#billcountry').val());
        });
        $('#billcity').change(function() {
            $('#shipcity').val($('#billcity').val());
        });
        $('#billstate').change(function() {
            $('#shipstate').val($('#billstate').val());
        });
        $('#billzip').change(function() {
            $('#shipzip').val($('#billzip').val());
        });
    }

    $('#shipsame:checkbox').change(function() {
        if($('#shipsame').prop('checked')){
            $('#shipfname').val($('#billfname').val());
            $('#shiplname').val($('#billlname').val());
            $('#shipaddress1').val($('#billaddress1').val());
            $('#shipaddress2').val($('#billaddress2').val());
            $('#shipcountry').val($('#billcountry').val());
            $('#shipcity').val($('#billcity').val());
            $('#shipstate').val($('#billstate').val());
            $('#shipzip').val($('#billzip').val());
        } else {
            $('#shipfname').val('');
            $('#shiplname').val('');
            $('#shipaddress1').val('');
            $('#shipaddress2').val('');
            $('#shipcountry').val('');
            $('#shipcity').val('');
            $('#shipstate').val('');
            $('#shipzip').val('');
        }
    });
});