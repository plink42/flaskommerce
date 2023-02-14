$(document).ready(function() {
  $('#billcountry').change(function() {

    var cc = $('#billcountry').val();

    // Make Ajax Request and expect JSON-encoded data
    $.getJSON(
      '/getstates' + '/' + cc,
      function(data) {

        // Remove old options
        $('#billstate').find('option').remove();     


        // Add new items
        if(Object.keys(data).length > 0) {
            $('#billstate').replaceWith('<select class="custom-select mr-sm-2" name="billstate" id="billstate"></select>');
            $.each(data, function(key, val) {
                var option_item = '<option value="' + key + '">' + val + '</option>'
                $('#billstate').append(option_item);
              });
        } else {
            $('#billstate').replaceWith('<input type="text" name="billstate" class="form-control" id="billstate" />');
        }
      }
    );
  });
  $('#shipcountry').change(function() {

    var cc = $('#shipcountry').val();

    // Make Ajax Request and expect JSON-encoded data
    $.getJSON(
      '/getstates' + '/' + cc,
      function(data) {

        // Remove old options
        $('#shipstate').find('option').remove();     

        if(Object.keys(data).length > 0) {
            $('#shipstate').replaceWith('<select class="custom-select mr-sm-2" name="shipstate" id="shipstate"></select>');
            $.each(data, function(key, val) {
                var option_item = '<option value="' + key + '">' + val + '</option>'
                $('#shipstate').append(option_item);
              });
        } else {
            $('#shipstate').replaceWith('<input type="text" name="shipstate" class="form-control" id="shipstate" />');
        }
        // Add new items

      }
    );
  });
});