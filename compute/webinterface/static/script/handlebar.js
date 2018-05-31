var reg = 'reg',
    clas = 'clas';

$(document).ready(function() {

    $('#regress').click(function() {
        $('.result_element').remove();
        $.getJSON('../../regress', function(data) {
            updateTable(data, reg);
        });
    });

    $('#classify').click(function() {
        $('.result_element').remove();
        $.getJSON('../../classify', function(data) {
            updateTable(data, clas);
        });
    });

});

function updateTable(json, type) {
    $.each(json.result, function (index, item) {
        appendDataToTable(item, type);
    });
}

function appendDataToTable(rowdata, type) {
    if(type === 'reg') {
        $('#regression_result').append(function () {
            console.log(rowdata);
            return '<tr class="result_element"><td>Actual: ' + rowdata.Actual + '</td>' + '\n' + '<td>Predicted: ' + rowdata.Predicted + '</td></tr>';
        });
    }else if(type === 'clas'){
        $('#regression_result').append(function () {
            console.log(rowdata);
        });
    }
}