$(document).ready(function () {
    $('#status').text('System is currently loaded and ready.');
    clearTable();

    $('#resetmodel').click(function() {
        // figure out how
    });

    $('#linear').click(function() {
        loading();
        $('.result_element').remove();
        $.getJSON('/linear', function(data) {
            $('#r2button').show();
            updateTable(data);
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
        $.getJSON('/mlp', function(data) {
            $('#data').fadeIn();
            $('#r2button').show();
            updateTable(data);
            $('#resultheader').text('Results - Training the MLP regression model');
            $('#resultcontext').text('These are the results from training and testing the Multi-Layer Perceptron ' +
                'regression model on the dataset - not very important results, but the information is useful when ' +
                'comparing different regression models..');
            $('#loadinggif').hide();
            displayImage();
        });
    });

    $('#dt').click(function() {
        loading();
        $('.result_element').remove();
        $.getJSON('/dt', function(data) {
            $('#data').show();
            $('#r2button').show();
            updateTable(data);
            $('#resultheader').text('Results - Target prediction');
            $('#resultcontext').text('The predicted \'years in vivo\' value represent the years that the implant is ' +
                'predicted to last in the patient.');
            $('#loadinggif').hide();
            displayImage(data['graphs']);
        });
    });

    $('#featurebtn').click(function() {
        clearTable();
        loading();
        $('#status').text('System may have stopped working.');
        $.get('/features', function(input) {
            $('#features').append(input);
            $('#resultheader').text('Dataset features');
            $('#resultcontext').text('These are the features (or columns) of the dataset - also known as the categories of information gathered from each patient.').append("<br /><br />").append('The checkboxes indicate whether or not a feature will be included when the system predicts how long an implant will last in the given patient, by checking a box you include that feature in the prediction.');
            $('#loadinggif').hide();
            $('.feature').fadeIn();
            $('#status').text('System is currently loaded and ready.');
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

    $('#saveFeatures').click(function() {
        $.each($('#feats'), function(feature) {
            console.log(feature);
            console.log(feature.attr('id'));
        });
        $.ajax({
            url: '/features',
            data: $('.feat').serialize(),
            type: 'POST',
            success: function(response) {
                console.log(response);
            },
            error: function(response) {
                console.log('Oh no, ' + response.valueOf());
            }
        })
    });

    $('#r2button').click(function() {
        $('#r2info').fadeToggle();
    });
});

function updateTable(json, type) {
    $('#status').text('System is currently loaded and ready.');
    if ('r2' in json) {
        $('#r2info').text('This prediction model has an R2 score of ' + parseFloat(json.r2).toFixed(7));
    }
    $.each(json.result, function (index, item) {
        appendDataToTable(item, type);
    });
}

function appendDataToTable(rowdata) {
    $('#results_table').append(function () {
        return '<tr class="result_element"><td>Actual: ' + rowdata['Actual'].toFixed(5) + '</td>' + '\n' +
            '<td>Predicted: ' + rowdata['Predicted'].toFixed(5) + '</td></tr>';
    });
}

function clearTable() {
    $('#results').hide();
    $('#graphFiller').hide();
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
    $('#status').text('System is running predictions');

    clearTable();
    $('#loadinggif').fadeIn();
    $('#resultheader').text('Loading...');
    $('#resultcontext').text('We\'re doing some heavy lifting, this shouldn\'t take too long');
    $('#data').show();

    $('#results').slideDown();
}

function displayImage(images) {

    for(var image in images) {
        var img = document.createElement('img');
        img.setAttribute('src', '../static/img/' + images[image]);
        img.setAttribute('class', 'graphImage');
        document.getElementById('graphs').appendChild(img);
    }

    $('#graphFiller').fadeIn();
}