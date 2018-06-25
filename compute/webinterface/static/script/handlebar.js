var reg = 'reg',
    clas = 'clas';

$(document).ready(function() {

    clearTable();

    $('#resetmodel').click(function() {
        // figure out how
    });

    $('#regress').click(function() {
        loading();
        $('.result_element').remove();
        $.getJSON('../../regress', function(data) {
            $('#data').fadeIn();
            updateTable(data, reg);
            $('#resultheader').text('Results - Training the model');
            $('#resultcontext').text('The training function randomly selects a subset of test cases and training' +
                'cases, fitting the training data to the model. The model is then used to predict each test case ' +
                ', the results being displayed above. \"Actual\" represents the actual years in vivo value ' +
                'from the test set, while \"Predicted\" represents the value predicted by the model.');
            $('#loadinggif').hide();
        });
    });

    $('#classify').click(function() {
        loading();
        $('.result_element').remove();
        $.getJSON('../../classify', function(data) {
            $('#data').fadeIn();
            updateTable(data, clas);
            $('#resultheader').text('Results - Target prediction');
            $('#resultcontext').text('The predicted \'years in vivo\' value represent the years that the implant is ' +
                'predicted to last in the patient.');
            $('#loadinggif').hide();
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
    $('#loadinggif').hide();
}

function loading() {
    $('#loadinggif').show();
    $('#resultheader').text('Loading...');
    $('#resultcontext').text('We\'re doing some heavy lifting, this shouldn\'t take too long');
}