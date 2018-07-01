var reg = 'reg',
    clas = 'clas';

$(document).ready(function() {

    $('#status').text('System is loaded and ready. It\'s very much in development so please cut it some slack.');
    clearTable();

    $('#resetmodel').click(function() {
        // figure out how
    });

    $('#regress').click(function() {
        loading();
        $('.result_element').remove();
        $.getJSON('../../regress', function(data) {
            $('#data').fadeIn();
            $('#r2info').show();
            updateTable(data, reg);
            $('#resultheader').text('Results - Training the model');
            $('#resultcontext').text('The training function randomly selects a subset of test cases and training' +
                'cases, fitting the training data to the model. The model is then used to predict each test case ' +
                ', the results being displayed above. \"Actual\" represents the actual years in vivo value ' +
                'from the test set, while \"Predicted\" represents the value predicted by the model.');
            $('#loadinggif').hide();
            displayImage();
        });
    });

    $('#target').click(function() {
        loading();
        $('.result_element').remove();
        $.getJSON('../../target', function(data) {
            $('#data').fadeIn();
            $('#r2info').show();
            updateTable(data, clas);
            $('#resultheader').text('Results - Target prediction');
            $('#resultcontext').text('The predicted \'years in vivo\' value represent the years that the implant is ' +
                'predicted to last in the patient.');
            $('#loadinggif').hide();
        });
    });

    $('#savebtn').click(function() {
        loading();
        $('.result_element').remove();
        $("#savestatus").load("../../save", function() {
            $('#data').fadeIn();
            if($('#success').text() == 'success'){
                $('#resultheader').text('File saved as ' + $('#fname').text());
                $('#resultcontext').text('The dataset was saved as a new file with the aforementioned name for ' +
                    'future use.');
                $('#loadinggif').hide();
            } else {
                $('#resultheader').text('An error occurred!');
                $('#resultcontext').text('The dataset has not been saved.');
                $('#loadinggif').hide();
            }
        });
    });

    $('#r2info').click(function() {

    })
});

function updateTable(json, type) {
    if ('r2' in json) {
        // Display the R2 score somewhere
        console.log(json['r2'])
    }
    $.each(json.result, function (index, item) {
        appendDataToTable(item, type);
    });
}

function appendDataToTable(rowdata, type) {
    if(type === 'reg') {
        $('#results_table').append(function () {
            return '<tr class="result_element"><td>Actual: ' + rowdata['Actual'].toFixed(5) + '</td>' + '\n' +
                '<td>Predicted: ' + rowdata['Predicted'].toFixed(5) + '</td></tr>';
        });
    }else if(type === 'clas'){
        $('#results_table').append(function () {
            return '<tr class="result_element"><td>Actual: ' + rowdata['Actual'].toFixed(5) + '</td>' + '\n' +
                '<td>Predicted: ' + rowdata['Predicted'].toFixed(5) + '</td></tr>';
        });
    }
}

function displayR2Score(r2score) {
    // Display on hover? Display in extra div? Does div overlay button? Anchored to just below button on click?
}

function clearTable() {
    $('#data').hide();
    $('#resultheader').text('');
    $('#resultcontext').text('');
}

function loading() {
    $('.graphImage').remove();
    $('#loadinggif').show();
    $('#resultheader').text('Loading...');
    $('#resultcontext').text('We\'re doing some heavy lifting, this shouldn\'t take too long');
    $('#r2info').hide();
}

function displayImage() {
    var img = document.createElement('img');
    img.setAttribute('src', '../static/img/scatterplot.png');
    img.setAttribute('class', 'graphImage');
    document.getElementById('data').appendChild(img);
}