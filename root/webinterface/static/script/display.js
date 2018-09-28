var slide = true,
    cancelled,
    patientInfo,
    previousWindow = []; //TODO implement as list instead, enable multiple backs

$(document).ready(function () {
    $('#scienceToggle').hide();
    clearTable();
    loadPage();

    $('#start').show().click(function() {
        previousWindow.push(start);
        start();
        cancelled = false;
    });

    $('#title h1').dblclick(function() {
        $('#scienceToggle').fadeToggle();
    });

    $('#dt').click(function() {
        previousWindow.push(nextStep);
        if (!$(this).hasClass('disabled')) {
            $(this).fadeOut();
            hideAllElements();
            loading();
            $('.result_element').remove();
            $.getJSON('/dt', function (data) {
                if(data == null) {
                    systemStatusBad();
                }
                if (!cancelled) {
                    updateTable(data);
                    displayImage(data['graphs']);
                    displayResults();
                }
            }).fail(function() {
                console.log('JSON request was terminated');
                systemStatusBad();
            });
        }
    });

    $('#featurebtn').click(function() {
        hideAllElements();
        loading();
        systemStatusBad();
        $.get('/features', function(input) {
            featureSelection(input);
            previousWindow.push(nextStep);
            nextStep();
        }).fail(function() {
            console.log('Couldn\'t get list of features!');
        });

        // TODO DOESN'T WORK!
        $('.featureSelector').on('click', function() {
            console.log('lo0l');
            var checked = $(this).prop('checked');
            if (checked) {
                $(this).prop('checked', false);
            } else {
                $(this).prop('checked', true);
            }
        });

        $('#saveFeatures').click(function() {
            $.ajax({
                url: '/features',
                data: $('.feat').serialize(),
                type: 'POST',
                success: function() {
                    $('#features').slideUp();
                    $('#saveFeatures').addClass('success').text('Successfully saved').css('margin-top', '15%');
                    previousWindow.push(featureSelection);
                    featureSelection();
                    setTimeout(nextStep, 2000);
                },
                error: function(response) {
                    console.log('Oh no, ' + response.valueOf());
                    systemStatusBad();
                }
            });
        });
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
                    console.log('Form successfully filled');
                    $(this).removeClass('emptyForm');
                }
            }
        });
        if (formValid) {
            console.log('running post request');
            patientInfo = $('.patInfo').val();
            $.ajax({
                url: '/updatetarget',
                data: $('.patInfo').serialize(),
                type: 'POST',
                success: function (response) {
                    console.log('POST response:', response);
                },
                error: function (response) {
                    console.log('Oh no, ' + response.valueOf());
                    systemStatusBad();
                }
            });
            $(this).addClass('success').text('Successfully saved');
            previousWindow.push(featureSelection);
            enterPatientInfo();
            $('#patientInfoForm form').slideUp();
            $('#saveTarget').css('margin-top', '45%');
            setTimeout(nextStep, 2000);
        }
    });

    $('#cancel').click(function() {
        stopProcess();
        hideAllElements();
        start();
    });

    $('#back').click(function() {
        stopProcess();
        hideAllElements();
        console.log(previousWindow.length);
        console.log(previousWindow[0]);

        // Bugged
        if (previousWindow.length > 0) {
            previousWindow[previousWindow.length - 1]();
        } else {
            start();
        }
    });

    $('#r2button').click(function() {
        $('#r2info').fadeToggle();
    });
});

function loading() {
    systemStatusLoading();
    clearTable();
    $('#title h1').text('Loading...');
    $('#title p').text('We\'re doing some heavy lifting. This shouldn\'t take more than a minute or a few.').append('' +
        '<br/><br/>').append('If the loading takes more than a few minutes, please check if the status bar below is ' +
        'loading as well. If it is, your computer is slow and there\'s not an awul lot to do about that.');
    $('#loadinggif, #cancel, #back, #data').fadeIn();
    $('#centercontent').slideDown();
}

function doneLoading() {
    $('#resultheader, #resultcontext, #loadinggif').hide();
    $('.success').removeClass('success');
    $('#saveFeatures').text('Save features');
    $('#saveTarget, #saveFeatures').css('margin-top', '');
}

function loadPage() {
    hideAllElements();
    $('#input, #start').fadeIn();
}

var start = function () {
    console.log('run');
    doneLoading();
    $('#start').hide();
    slide = 'down';
    $('#menu').css('left', 0);
    $('#saveFeatures').removeClass('success').text('Save feature selection');
    $('#saveTarget').removeClass('success').text('Save patient information');
    setTimeout(function() {
        enterPatientInfo();
    }, 1000);
};

var enterPatientInfo = function () {
    doneLoading();
    clearTable();
    $('#title h1').text('Patient information form');
    $('#title p').text('We need you to enter all the information on your patient here. If you\'re missing some ' +
        'data, please enter -1.');
    $('#patientInfoForm, #patientInfoForm form, .input, #data, #status').slideDown();
    if (slide) {
        $('#centercontent').slideDown();
    } else {
        $('#centercontent').fadeIn();
    }
    systemStatusGood();
};

var nextStep = function () {
    doneLoading();
    hideAllElements();
    $('#title h1').text('One last thing...');
    $('#title p').text('We\'re ready to start predicting! The prediction usually takes a minute to run, but that ' +
        'depends on how beefy your computer processor is. It might take longer. If you want, you can specify which ' +
        'parts of the patient information will be taken into consideration.');
    $('#centercontent, .input, .input button, #data, .navigation').show();
    systemStatusGood();
};

var featureSelection = function(input) {
    doneLoading();
    hideAllElements();
    $('#features').append(input);
    $('#title h1').text('Dataset features');
    $('#title p').text('These are the features (or columns) of the dataset - also known as the ' +
        'categories of information gathered from each patient.').append("<br /><br />").append('The ' +
        'checkboxes indicate whether or not a feature will be included when the system predicts how long ' +
        'an implant will last in the given patient, by checking a box you include that feature in the ' +
        'prediction.');
    $('#centercontent, #features, .feature, .feature button, #data, .navigation').show();
    systemStatusGood();
};

function displayResults() {
    doneLoading();
    $('#title h1').text('Prediction results');
    $('#title p').text('In the center page you can see the prediction result up top, with some graphs below. The ' +
        'graphs detail the relationships between implant longevity and other features (such as blood analysis ' +
        'results, angle of implant etc etc)');
    if (!cancelled) {
        $('#results_table, #graphFiller, #graphs, #r2button').fadeIn();
    } else {
        console.log('process terminated');
    }
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

function updateTable(json) {
    $.each(json, function(index, item) {
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

function appendDataToTable(rowdata) {
    $('#results_table').append(function () {
        return '<tr class="result_element"><td>Actual: ' + rowdata['Actual'] + '</td>' + '\n' +
            '<td>Predicted: ' + rowdata['Predicted'] + '</td></tr>';
    });
}

function stopProcess() {
    cancelled = true;
    $.ajax({
        url: '/stopProcess',
        type: 'POST',
        success: function () {
            console.log('Prediction stopped.');
        },
        error: function (response) {
            console.log(response);
            systemStatusBad();
        }
    });
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

function hideAllElements() {
    $('.hideContent, #data, #patientInfoForm, #graphFiller, #graphs, #status, .feature, #loadinggif, #r2info, ' +
        '#r2button, #input, #input button, .input, .input button, .optional').hide();
}

function clearTable() {
    $('#resultheader').text('');
    $('#resultcontext').text('');
    $('.result_element, .graphImage').remove();
    $('#features').empty();
}