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
        if (!$(this).hasClass('disabled')) {
            $(this).fadeOut();
            hideAllElements();
            loading();
            $('.result_element').remove();
            $.getJSON('/dt', function (data) {
                if(data == null) {
                    systemStatusBad();
                }
                updateTable(data);
                displayImage(data['graphs']);
                displayResults();
            });
        }
    });

    $('#featurebtn').click(function() {
        hideAllElements();
        loading();
        systemStatusBad();
        $.get('/features', function(input) {
            $('#features').append(input);
            $('#resultheader').text('Dataset features');
            $('#resultcontext').text('These are the features (or columns) of the dataset - also known as the ' +
                'categories of information gathered from each patient.').append("<br /><br />").append('The ' +
                'checkboxes indicate whether or not a feature will be included when the system predicts how long ' +
                'an implant will last in the given patient, by checking a box you include that feature in the ' +
                'prediction.');
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

    $('#case').change(function() {
        if ($(this).val() == '1') {
            $('.hidden').slideDown();
        } else if ($(this).val() == '0') {
            $('.hidden').slideUp();
        }
    });

    $('#saveTarget').click(function() {
        var formValid = true;

        $('#patientInfoForm form input').each(function() {
            if ($(this).val() === "") {
                formValid = false;
                console.log('Missing value!');
                $(this).addClass('emptyForm');
            } else {
                if ($(this).hasClass('emptyForm')) {
                    console.log('yes');
                    $(this).removeClass('emptyForm');
                }
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

    $('#cancel').click(function() {
        hideAllElements();
        start();
    });

    $('#r2button').click(function() {
        $('#r2info').fadeToggle();
    });
});

function updateTable(json) {
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
        return '<tr class="result_element"><td>Actual: ' + rowdata['Actual'] + '</td>' + '\n' +
            '<td>Predicted: ' + rowdata['Predicted'] + '</td></tr>';
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
    $('#loadinggif, #cancel').fadeIn();
    $('#resultheader').text('Loading...').fadeIn();
    $('#resultcontext').text('We\'re doing some heavy lifting, this shouldn\'t take too long').fadeIn();
    $('#data').show();

    $('#centercontent').slideDown();
}

function doneLoading() {
    $('#resultheader, #resultcontext').hide();
    $('#loadinggif').hide();
}

function displayInput() {
    doneLoading();
    $('#saveFeatures').removeClass('success').text('Save feature selection');
    $('#saveTarget').removeClass('success').text('Save patient information');
    clearTable();

    $('#data').show();
    $('#centercontent .input').show();

    if (direction == 'up') {
        console.log('haha');
        $('#centercontent').fadeIn();
    } else {
        $('#centercontent').slideDown();
    }

    systemStatusGood();
}

function enterPatientInfo() {
    doneLoading();
    $('#centercontent').slideDown();
    $('#title h1').text('Patient information form');
    $('#title p').text('We need you to enter all the information on your patient here. If you\'re missing some ' +
        'data, please enter -1.');
    $('#patientInfoForm').show();
    systemStatusGood();
}

function systemStatusGood() {
    var status = $('#status');

    if (!status.is(':visible')) {
        status.fadeIn();
    }
    status.css('background-color', '#142914').text('System status: All good.');
}

function systemStatusLoading() {
    var status = $('#status');

    if (!status.is(':visible')) {
        status.fadeIn();
    }
     status.css('background-color', '#30310f').text('System status:    Loading - please wait...');
}

function systemStatusBad() {
    var status = $('#status');

    if (!status.is(':visible')) {
        status.fadeIn();
    }
     status.css('background-color', 'red').text('System status: Something stopped working - please refresh!');
}

function displayImage(images) {
    for(var image in images) {
        var img = document.createElement('img');
        img.setAttribute('src', '../static/img/' + images[image]);
        img.setAttribute('class', 'graphImage');
        document.getElementById('graphs').appendChild(img);
    }

    $('#graphFiller').fadeIn();
    systemStatusGood();
}

function loadPage() {
    hideAllElements();
    $('#input, #start').fadeIn();
    $('#scienceToggle').fadeIn();
}

function start() {
    doneLoading();
    $('#start, #cancel').hide();
    direction = 'down';
    $('#menu').css('left', 0);
    $('#buttons button').fadeIn();
    $('#status').show();
    setTimeout(systemStatusGood, 800);
    $('#title h1').text('Main menu');
    $('#title p').text('This is the main menu. To get started, we\'re going to need some information about the ' +
        'patient - if you press the big orange button in the middle of the screen you\'ll be able to enter all the ' +
        'necessary patient details.');
    setTimeout(displayInput, 1000);
    $('#scienceToggle').fadeIn();
    $('#addtarget').fadeIn();
}

function nextStep() {
    doneLoading();
    hideAllElements();
    $('#title h1').text('One last thing...');
    $('#title p').text('We\'re ready to start predicting! The prediction usually takes a minute to run, but that ' +
        'depends on how beefy your computer processor is. It might take longer. If you want, you can specify which ' +
        'parts of the patient information will be taken into consideration - after all, you\'re the most qualified to ' +
        'decide what matters and what doesn\'t.');
    direction = 'up';
    displayInput();
    $('#dt, #featurebtn').fadeIn();
}

function displayResults() {
    doneLoading();
    $('#title h1').text('Prediction results');
    $('#title p').text('Presented to you in the center part of the page are the results from ' +
        'running your data into the machine learning prediction magician.');
    $('#results_table, #graphFiller, #graphs').fadeIn();
    $('#r2button').fadeIn();
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