var reg = 'reg',
    clas = 'clas';

$(document).ready(function() {

    clearTable();

    $('#resetmodel').click(function() {
        // figure out how
    });

    $('#regress').click(function() {
        $('.result_element').remove();
        loading();
        $.getJSON('../../regress', function(data) {
            updateTable(data, reg);
            $('#resultheader').text('Results - Training the model');
            $('#resultcontext').text('The training function randomly selects a subset of test cases and training' +
                'cases, fitting the training data to the model. The model is then used to predict each test case ' +
                ', the results being displayed above. \"Actual\" represents the actual years in vivo value ' +
                'from the test set, while \"Predicted\" represents the value predicted by the model.');
            $('#data').fadeIn();
        });
    });

    $('#classify').click(function() {
        $('.result_element').remove();
        $.getJSON('../../classify', function(data) {
            updateTable(data, clas);
            $('#data').fadeIn();
            $('#resultheader').text('Results - Target prediction');
            $('#resultcontext').text('The predicted \'years in vivo\' value represent the years that the implant is ' +
                'predicted to last in the patient.');
        });
    });

    $('#save').click(function() {

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
            return '<tr class="result_element"><td>Actual: ' + rowdata['Actual'] + '</td>' + '\n' + '<td>Predicted: ' +
                rowdata['Predicted'] + '</td></tr>';
        });
    }
}

function clearTable() {
    $('#data').hide();
    $('#resultheader').text('');
    $('#resultcontext').text('');
}

function loading() {
    $('#resultheader').text('Loading...');
    $('#resultcontext').text('We\'re doing some heavy lifting, this shouldn\'t take too long');
}