$(function() {
  var $input = $('.monthly_working_time')
  var $updated = $('#updated_list')
  updated = []
  $input.on('input', function(event) {
    console.log(this.name);
    if (!updated.includes(this.name)) {
      updated.push(this.name)
    }
    console.log(updated);
    $updated.val(updated)
  });
});
