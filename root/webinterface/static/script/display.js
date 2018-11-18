var slide = true,
    systemLoading = false,
    cancelled,
    patientInfo = {},
    currentWindow = []; //TODO implement as list instead, enable multiple backs

$(document).ready(function () {
    $('#scienceToggle, #patInfoSheet, #patInfoDisplay').hide();
    clearTable();
    loadPage();

    $('#start').show().click(function() {
        start();
        cancelled = false;
    });

    $('#title h1').dblclick(function() {
        $('#scienceToggle').fadeToggle();
    });

    $('#dt').click(function() {
        if (!$(this).hasClass('disabled')) {
            cancelled = false;
            $(this).fadeOut();
            hideMostElements();
            loading();
            $('.result_element').remove();
            $.getJSON('/dt', function (data) {
                if(data == null) {
                    systemStatusBad();
                }
                if (!cancelled) {
                    updateTable(data);
                    displayResults();
                    displayImage(data['graphs']);
                }
            }).fail(function() {
                console.log('JSON request was terminated');
                if (!cancelled) {
                    systemStatusBad();
                }
            });
        }
    });

    $('#featurebtn').click(function() {
        hideMostElements();
        $('#features').empty();
        systemStatusBad();
        $.get('/features', function(input) {
            featureSelection(input);
        }).fail(function() {
            console.log('Couldn\'t get list of features!');
        });

        // TODO DOESN'T WORK!
        $('.featureSelector').on('click', function() {
            let checked = $(this).prop('checked');
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
                    setTimeout(nextStep, 2000);
                },
                error: function(response) {
                    console.log('Oh no, ' + response.valueOf());
                    systemStatusBad();
                }
            });
        });
    });

    $('#case').change(function() {
        if ($(this).val() == 1) {
            $('#patientInfoForm form .hidden').slideDown();
        } else {
            // TODO this doesn't change the input value of subsequent fields.
            $('#patientInfoForm form .hidden').val(0).slideUp();
        }
    });

    $('#saveTarget').click(function() {
        let formValid = true;
        $('#patientInfoForm form input, #patientInfoForm form select').each(function() {
            if ($(this).val() === "") {
                formValid = false;
                console.log('Missing value!');
                $(this).addClass('emptyForm');
            } else {
                if ($(this).hasClass('emptyForm')) {
                    console.log('Form successfully filled');
                    $(this).removeClass('emptyForm');
                }
                // $('#patInfoSheet').append('<tr><td>' + $('label[for="' + $(this).attr('id') + '"]').text() +
                //     '</td><td>' + $(this).val() + '</td></tr>');

                patientInfo[$('label[for="' + $(this).attr('id') + '"]').text()] = $(this).val();
            }
        });

        if (formValid) {
            console.log('running post request');
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

            if ($('#patInfoSheet').children().length > 2) {
                $('#patInfoSheet tr').remove();
            }

            for(let item in patientInfo) {
                if (item.toLowerCase().search('removed') >= 0) {
                    let whetherOrNot = 'Yes';
                    if (patientInfo[item] == 0) {
                        whetherOrNot = 'No';
                    }
                    $('#patInfoSheet').append('<tr><td class="patinfodesc">' + item + '</td><td class="patinfoval">' +
                        whetherOrNot + '</td></tr>');
                } else if (item.toLowerCase().search('gender') >= 0) {
                    let gender = 'Undefined';
                    if (patientInfo[item] == 1) {
                        gender = 'Male';
                    } else if (patientInfo[item] == 2) {
                        gender = 'Female';
                    }
                    $('#patInfoSheet').append('<tr><td class="patinfodesc">' + item + '</td><td class="patinfoval">' +
                    gender + '</td></tr>');
                } else {
                    $('#patInfoSheet').append('<tr><td class="patinfodesc">' + item + '</td><td class="patinfoval">' +
                    patientInfo[item] + '</td></tr>');
                }
            }
            $('#saveTarget').addClass('success').text('Successfully saved').css('margin-top', '45%');
            $('#patientInfoForm form').slideUp();
            setTimeout(nextStep, 2000);
        }
    });

    $('#cancel').click(function() {
        stopProcess();
        hideAllElements();
        clearTable();
        $('#moreInfoButton').removeClass('buttonClicked').text('More information');
        start();
    });

    $('#patInfoDisplayButton').click(function() {
        if ($(this).hasClass('buttonClicked')) {
            $(this).removeClass('buttonClicked');
            $('#patInfoSheet').slideUp();
        } else {
            $(this).addClass('buttonClicked');
            $('#patInfoSheet').slideDown();
        }
    });

    $('#moreInfoButton').click(function() {
        if ($(this).hasClass('buttonClicked')) {
            $(this).removeClass('buttonClicked').text('More information');
        } else {
            $(this).addClass('buttonClicked').text('Less information');
        }
        $('.graphImage, #statsFiller').slideToggle();
    });

    // TODO: This function works almost as intended - when using system straight it takes user back to input (from
    // TODO: loading prediction - funky). Does weird things with select feature thing.
    $('#back').click(function() {
        stopProcess();
        clearTable();
        hideMostElements();
        $('#moreInfoButton').removeClass('buttonClicked');

        if (currentWindow.length > 1) {
            let previousWindow = currentWindow[currentWindow.length - 2];
            if (systemLoading) {
                previousWindow = currentWindow[currentWindow.length - 1];
                currentWindow.pop();
            } else {
                currentWindow.pop();
                currentWindow.pop();
            }
            previousWindow();
        } else {
            start();
        }
    });
});

function loading() {
    systemStatusLoading();
    clearTable();
    $('#title h1').text('Loading...');
    $('#title p').text('We\'re doing some heavy lifting. This shouldn\'t take more than a minute or a few.').append('' +
        '<br><br>').append('If the loading takes more than a few minutes, please check if the status bar below is ' +
        'loading as well. If it is, your computer or the network might be slow and there\'s not an awful lot to do ' +
        'about that.');
    $('#loadinggif, #cancel, #back, #data').fadeIn();
    $('#centercontent').slideDown();
}

function doneLoading() {
    systemLoading = false;
    $('#resultheader, #resultcontext, #loadinggif').hide();
    $('.success').removeClass('success');
    $('#saveFeatures').text('Save features');
    $('#saveTarget').text('Save');
    $('#saveTarget, #saveFeatures').css('margin-top', '');
}

function loadPage() {
    hideAllElements();
    $('#input, #start').fadeIn();
}

var start = function () {
    currentWindow.push(start);
    doneLoading();
    $('#start').hide();
    slide = 'down';
    $('#menu').css('left', 0);
    $('#saveFeatures').removeClass('success').text('Save feature selection');
    $('#saveTarget').removeClass('success').text('Save patient information');
    systemStatusGood();
    setTimeout(function() {
        enterPatientInfo();
    }, 1000);
};

var enterPatientInfo = function () {
    currentWindow.push(enterPatientInfo);
    doneLoading();
    clearTable();
    $('#title h1').text('Patient information form');
    $('#title p').text('This is the patient information form. The left column shows the categories of information ' +
        'we need to do an estimation of how long an implant will last in a patient.').append('<br><br>' + 'We need ' +
        'you to enter all the information on your patient here. All fields need to be filled in before you continue. ' +
        'If you don\'t have the information on a specific category, just enter 0.');
    $('#patientInfoForm, #patientInfoForm form, .input, #data').slideDown();
    systemStatusGood();
    if (slide) {
        $('#centercontent').slideDown();
    } else {
        $('#centercontent').fadeIn();
    }
};

var nextStep = function () {
    currentWindow.push(nextStep);
    doneLoading();
    hideMostElements();
    systemStatusGood();
    $('#title h1').text('One last thing...');
    $('#title p').text('We\'re ready to start the process of predicting. If you want to start this process, click the ' +
        'big orange button with \"Run prediction\" written all over it.').append('<br><br>There is an option to ' +
        'change which features (categories in the information sheet) should be included in the prediction process - ' +
        'please note however that the default setting has been recommended by an expert in medicinal statistics.');
    $('.input, .input button, #data, .navigation, #patInfoDisplay').slideDown();
};

var featureSelection = function(input) {
    currentWindow.push(featureSelection);
    doneLoading();
    hideMostElements();
    $('#features').append(input);
    $('#title h1').text('Dataset features');
    $('#title p').text('These are the features (or columns) of the dataset - also known as the ' +
        'categories of information gathered from each patient.').append('<br><br> The checkboxes indicate whether ' +
        'or not a feature (information sheet category) will be included when the system predicts how long an implant ' +
        'will last in the given patient.').append('<br><br>By clicking the checkbox for any given feature, you will' +
        'include that feature in the prediction process.<br><br>Default set of features is CR, CO, LINWEAR, ' +
        'LINWEARRATE, INC, ANT, MALE, FEMALE.');
    $('#features, .feature, .feature button, #data, .navigation').show();
    systemStatusGood();
};

var displayResults = function() {
    if (!cancelled) {
        currentWindow.push(displayResults);
        doneLoading();
        $('#title h1').text('Results');
        $('#title p').text('The center page displays the estimated longevity of the implant (in years). This ' +
            'estimation is based on the values in the patient informaton form.').append('<br><br>More statistical ' +
            'information about the predictions and the model estimating these predictions is available by clicking ' +
            'the "More information" button below the result.');
        $('#results_table, #graphFiller, #graphs').fadeIn();
    } else {
        console.log('process terminated');
    }
}

function displayImage(images) {
    for(let image in images) {
        let img = document.createElement('img');
        img.setAttribute('src', '../static/img/graphs/' + images[image]);
        img.setAttribute('class', 'graphImage');
        document.getElementById('graphs').appendChild(img);
    }
    $('.graphImage').hide();
    $('#graphFiller').slideDown();
    systemStatusGood();
}

function updateTable(json) {
    systemStatusGood();
    if ('r2' in json) {
        $('#statsFiller').append('<tr class="statistics"><td>Adjusted R<sup>2</sup> score of estimator used for this prediction</td><td class="statnum">' + parseFloat(json.r2).toFixed(4).replace('.', ',') + '</td></tr>');
    }

    if ('rmse' in json) {
        $('#statsFiller').append('<tr class="statistics"><p class="statistics"><td>Root Mean Squared Error of estimator for this prediction</td><td class="statnum">' + parseFloat(json.rmse).toFixed(4).replace('.', ',')+ '</td></tr>');
    }

    if ('stats' in json) {
        $('#statsFiller').append('<tr class="statistics"><td>Standard deviation of total predictions</td><td class="statnum">' + json.stats[0].replace('.', ',') + '</td></tr>');
        $('#statsFiller').append('<tr class="statistics"><td>Longest years of longevity predicted</td><td class="statnum">' + json.stats[1].replace('.', ',') + '</td></tr>');
        $('#statsFiller').append('<tr class="statistics"><td>Shortest years of longevity predicted</td><td class="statnum">' + json.stats[2].replace('.', ',') + '</td></tr>');
    }

    $.each(json.result, function (index, item) {
        $('#results_table').append('<tr><td id="p">Predicted implant longevity:</td></tr><tr class="result_element">' +
            '<td id="prediction">' + parseFloat(item['Predicted']).toFixed(2).replace('.', ',') + ' years.</td></tr>');
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
    systemLoading = true;
    let status = $('#status');
    if (!status.is(':visible')) {
        status.fadeIn();
    }
    status.css('background-color', '#30310f').text('System status:    Loading - please wait...');
}

function systemStatusBad() {
    let status = $('#status');
    if (!status.is(':visible')) {
        status.fadeIn();
    }
    status.css('background-color', 'red').text('System status: Something stopped working - please refresh!');
}

function hideAllElements() {
    // todo , #patInfoDisplayButton, add this
    $('.help, .hideContent, #centercontent, #data, #patientInfoForm, #graphFiller, #graphs, #status, .feature, #loadinggif, #r2info, ' +
        '#input, #input button, .input, .input button, .optional').hide();
}

// For when system is initiated
function hideMostElements() {
    $('.help, .hideContent, #data, #patientInfoForm, #graphFiller, #statsFiller, #graphs, #status, .feature, #loadinggif, #r2info, ' +
        '#input, #input button, .input, .input button, .optional').hide();
}

function clearTable() {
    $('#resultheader').text('');
    $('#resultcontext').text('');
    $('.result_element, .graphImage, .statistics, #results_table tr').remove();
    $('#features').empty();
}