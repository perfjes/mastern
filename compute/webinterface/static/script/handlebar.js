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
            console.log(data);
            updateTable(data, clas);
        });
    });

    $('#splitbox').submit(function () {
        var boop = $('#splot');
        if(boop != null) {
            $.ajax({
                type: 'POST',
                url: '../../split',
                data: boop
            });
        }
    });
});

function updateTable(json, type) {
    $.each(json.result, function (index, item) {
        appendDataToTable(item, type);
    });
}

function appendDataToTable(rowdata, type) {
    if(type === 'reg') {
        $('#results_table').append(function () {
            return '<tr class="result_element"><td>Actual: ' + rowdata['Actual'] + '</td>' + '\n' + '<td>Predicted: ' +
                rowdata['Predicted'] + '</td></tr>';
        });
    }else if(type === 'clas'){
        $('#results_table').append(function () {
            console.log(rowdata);

            return '<tr class="result_element"><td>' + rowdata.value + '</td></tr>'
        });
    }
}