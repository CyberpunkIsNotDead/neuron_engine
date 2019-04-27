import * from "jquery-3.4.0.min";

counter = 2;
jQuery(function($) {
  $('form').on('change', 'input[type=file]', function() {
    var form = $(this).closest('form');
    form.append('<tr><td><input type="file" name="upload" id="id_upload'+counter+'"><label for="id_upload'+counter+'" class="finput">Выбрать файл</label></td></tr>');
    counter++;
  });
});
