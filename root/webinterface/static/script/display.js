var reg = 'reg',
    clas = 'clas';

$(document).ready(function() {

    $('#status').text('Everything\'s loaded and ready. This is a decision support system that - based on a dataset ' +
        'of patient information - should be able to predict the longevity of a total hip replacement implant.');
    clearTable();

    $('#resetmodel').click(function() {
        // figure out how
    });

    $('#regress').click(function() {
        loading();
        $('.result_element').remove();
        $.getJSON('../../regress', function(data) {
            $('#r2button').show();
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

    $('#mlp').click(function() {
        loading();
        $('.result_element').remove();
        $.getJSON('../../mlp', function(data) {
            $('#data').fadeIn();
            $('#r2button').show();
            updateTable(data, reg);
            $('#resultheader').text('Results - Training the MLP regression model');
            $('#resultcontext').text('These are the results from training and testing the Multi-Layer Perceptron ' +
                'regression model on the dataset - not very important results, but the information is useful when ' +
                'comparing different regression models..');
            $('#loadinggif').hide();
            displayImage();
        });
    });

    $('#target').click(function() {
        loading();
        $('.result_element').remove();
        $.getJSON('../../target', function(data) {
            $('#data').show();
            $('#r2button').show();
            updateTable(data, clas);
            $('#resultheader').text('Results - Target prediction');
            $('#resultcontext').text('The predicted \'years in vivo\' value represent the years that the implant is ' +
                'predicted to last in the patient.');
            $('#loadinggif').hide();
        });
    });

    $('#featurebtn').click(function() {
        clearTable();
        loading();
        $.get('../../features', function(input) {
            $('#features').append(input);
            $('#resultheader').text('Dataset features');
            $('#resultcontext').text('These are the features of the dataset - each feature is a column that contains ' +
                'some value. If you want to run the prediction using a specific set of values, deselect those you do ' +
                'not want to be included in the prediction.');
            $('#loadinggif').hide();
            $('.feature').fadeIn();
        });

        /*  The original Save File function - deprecated for now
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
        */
    });

    $('#r2button').click(function() {
        $('#r2info').fadeToggle();
    });

    $('#saveFeatures').click(function() {
        $.post('../../features', function(features) {
            console.log('what' + features);
        })
    })


});

function updateTable(json, type) {
    if ('r2' in json) {
        $('#r2info').text('This prediction model has an R2 score of ' + parseFloat(json.r2).toFixed(7));
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

function clearTable() {
    $('#results').hide();
    $('#graphs').hide();
    $('#r2info').hide();
    $('#r2button').hide();
    $('.feature').hide();
    $('#loadinggif').hide();
    $('#resultheader').text('');
    $('#resultcontext').text('');
    $('.result_element').remove();
    $('#features').empty();
    $('.graphImage').remove();
}

function loading() {
    clearTable();
    $('#loadinggif').fadeIn();
    $('#resultheader').text('Loading...');
    $('#resultcontext').text('We\'re doing some heavy lifting, this shouldn\'t take too long');
    $('#data').show();

    $('#results').slideDown();
}

function displayImage() {
    $('#graphs').show();
    for(var i = 0; i < 3; i++){
        var img = document.createElement('img');
        img.setAttribute('src', '../static/img/graph.png');
        img.setAttribute('class', 'graphImage');
        document.getElementById('graphs').appendChild(img);
    }

    /*
    var img = document.createElement('img');
    img.setAttribute('src', '../static/img/scatterplot.png');
    img.setAttribute('class', 'graphImage');
    document.getElementById('graphs').appendChild(img);
    */
}