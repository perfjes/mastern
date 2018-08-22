var direction = 'down';

$(document).ready(function () {
    clearTable();
    loadPage();

    $('#start').show().click(function() {
        start();
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
        if (validateForm()) {
            if (!$(this).hasClass('disabled')) {
                $(this).fadeOut();
                loading();
                $('.result_element').remove();
                $.getJSON('/dt', function (data) {
                    if(data == null){
                        systemStatusBad();
                    }
                    updateTable(data);
                    displayResults();
                });
            }
        }
    });

    $('#featurebtn').click(function() {
        hideAllElements();
        loading();
        systemStatusBad();
        $.get('/features', function(input) {
            $('#features').append(input);
            $('#resultheader').text('Dataset features');
            $('#resultcontext').text('These are the features (or columns) of the dataset - also known as the categories of information gathered from each patient.').append("<br /><br />").append('The checkboxes indicate whether or not a feature will be included when the system predicts how long an implant will last in the given patient, by checking a box you include that feature in the prediction.');
            $('#loadinggif').hide();
            $('.feature').fadeIn();
            systemStatusGood();
        });
    });

    $('#saveFeatures').click(function() {
        $.ajax({
            url: '/features',
            data: $('.feat').serialize(),
            type: 'POST',
            success: function(response) {
                console.log(response);
            },
            error: function(response) {
                console.log('Oh no, ' + response.valueOf());
                systemStatusBad();
            }
        });
        $(this).addClass('success').text('Successfully saved');
        setTimeout(nextStep, 2000);
    });

    $('#addtarget').click(function() {
        hideAllElements();
        loading();
        enterPatientInfo();
    });

    $('#saveTarget').click(function() {
        var formValid = true;

        $('#patientInfoForm form input').each(function() {
            if ($(this).val() === ""){
                formValid = false;
                console.log('Missing value!');
                $('#patientInfoForm input').addClass('emptyForm');
            }
        });
        if (formValid) {
            console.log('running post request');
            $.ajax({
                url: '/updatetarget',
                data: $('.patInfo').serialize(),
                type: 'POST',
                success: function (response) {
                    console.log(response);
                },
                error: function (response) {
                    console.log('Oh no, ' + response.valueOf());
                    systemStatusBad();
                }
            });
            $(this).addClass('success').text('Successfully saved');
            setTimeout(nextStep, 2000);
        }
    });

    $('#r2button').click(function() {
        $('#r2info').fadeToggle();
    });
});

function updateTable(json) {
    console.log(json);
    $.each(json, function(index, item) {
        console.log(json[item]);
        console.log(item);
    });
    systemStatusGood();
    if ('r2' in json) {
        $('#r2info').text('This prediction model has an R2 score of ' + parseFloat(json.r2).toFixed(7));
    }
    $.each(json.result, function (index, item) {
        appendDataToTable(item);
    });
}

// TODO THIS FUNCTION BREAKS - NEED TO REMAKE THE ENTIRE DISPLAY FUNCTIONLAITY
function appendDataToTable(rowdata) {
    $('#results_table').append(function () {
        return '<tr class="result_element"><td>Actual: ' + rowdata['Actual'].toFixed(5) + '</td>' + '\n' +
            '<td>Predicted: ' + rowdata['Predicted'].toFixed(5) + '</td></tr>';
    });
}

function clearTable() {
    $('#resultheader').text('');
    $('#resultcontext').text('');
    $('.result_element').remove();
    $('#features').empty();
    $('.graphImage').remove();
}

function loading() {
    systemStatusLoading();

    clearTable();
    $('#loadinggif').fadeIn();
    $('#resultheader').text('Loading...');
    $('#resultcontext').text('We\'re doing some heavy lifting, this shouldn\'t take too long');
    $('#data').show();

    $('#centercontent').slideDown();
}

function displayInput() {
    $('#saveFeatures').removeClass('success').text('Save feature selection');
    $('#saveTarget').removeClass('success').text('Save patient information');
    clearTable();

    $('#data').show();
    $('#centercontent .input').show();

    if (direction == 'up'){
        console.log('haha');
        $('#centercontent').fadeIn();
    } else {
        $('#centercontent').slideDown();
    }

    systemStatusGood();
}

function enterPatientInfo() {
    $('#loadinggif').hide();
    $('#centercontent').slideDown();
    $('#resultheader').text('Patient information form');
    $('#resultcontext').text('Enter the relevant medical information on your patient here. The more information ' +
        'provided, the better.');
    $('#patientInfoForm').show();
    systemStatusGood();
}

function systemStatusGood() {
    var status = $('#status');

    if (!status.is(':visible')) {
        status.show();
    }
    status.css('background-color', '#142914').text('System status: All good.');
}

function systemStatusLoading() {
    var status = $('#status');

    if (!status.is(':visible')) {
        status.show();
    }
     status.css('background-color', '#30310f').text('System status:    Loading - please wait...');
}

function systemStatusBad() {
    var status = $('#status');

    if (!status.is(':visible')) {
        status.show();
    }
     status.css('background-color', 'red').text('System status: Something stopped working - please refresh!');
}

function displayImage() {
    var img = document.createElement('img');
    img.setAttribute('src', '../static/img/graph.png');
    img.setAttribute('class', 'graphImage');
    document.getElementById('graphs').appendChild(img);

    $('#graphs').slideDown();
    systemStatusGood();
}

function validateForm() {

    return true;
}

function loadPage() {
    hideAllElements();
    $('#input, #start').fadeIn();
    $('#scienceToggle').fadeIn();
}

function start() {
    direction = 'down';
    $('#menu').css('left', 0);
    $('#buttons button').fadeIn();
    $('#start').fadeOut();
    systemStatusGood();
    $('#status').show();
    setTimeout(displayInput, 1000);
    $('#scienceToggle').fadeIn();
    $('#addtarget').fadeIn();
    $('#title h1').text('Main menu');
    $('#title p').text('This is the main menu. To get started, we\'re going to need some information about the ' +
        'patient - if you press the big orange button in the middle of the screen you\'ll be able to enter all the ' +
        'necessary patient details.');
}

function nextStep() {
    hideAllElements();
    direction = 'up';
    displayInput();
    $('#dt, #featurebtn').fadeIn();
}

function displayResults(){

}

function hideAllElements() {
    $('#centercontent').hide();
    $('#data').hide();
    $('#input, #input button, .input, .input button, .optional').hide();
    $('#patientInfoForm').hide();
    $('#graphFiller').hide();
    $('#graphs').hide();
    $('#status').hide();
    $('.feature').hide();
    $('#loadinggif').hide();
    $('#r2info').hide();
    $('#r2button').hide();
}