var dataframeJSON;
var text;

$(document).ready(function() {

    // so this should enable JavaScript to call on python code, but it doesn't really work (yet).
    $('#regress').click(function() {
        /**
        $.ajax({
            type: 'POST',
            url: '../../regress',
            data: { param: text }
        }).done( function(json) {
            console.log(json);
            updateTable($.parseJSON(json));
        });
         **/

        $.getJSON('../../regress', function(data) {
            $('.result_element').remove();
            $.each(data.result, function(index, item) {
                appendDataToTable(item);
            });
        });
    });
});

function updateTable(json) {
    $.each(json.result, function(index, item) {
        console.log(item);
        appendDataToTable(item);
    });
}

function appendDataToTable(rowdata) {
    //var rowitem = $.parseJSON(rowdata);
    $('#regression_result').append(function() {
        console.log(rowdata);
        return '<tr class="result_element"><td>Actual: ' + rowdata.Actual + '</td>' + '\n' + '<td>Predicted: ' + rowdata.Predicted + '</td></tr>';

    });
}