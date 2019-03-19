var dateInput;
var timeSelect;
var specialistSelect;
var datetimeInput;

$(document).ready(function() {
    dateInput = $('#datepicker');
    timeSelect = $('#timepicker');
    timePickerBlock = $('#timepicker-block');
    specialistSelect = $('#id_specialist');
    datetimeInput = $('#id_datetime');

    var unallowedDaysJson;

    specialistSelect.change(function() {
        $.ajax({
            url: getUnavailableDaysUrl,
            data: {
                'specialist': specialistSelect.val()
            },
            success: function(response) {
                unallowedDaysJson = response.unavailableDaysJson;
                dateInput.datepicker({
                    language: "ru",
                    daysOfWeekDisabled: [0, 6],
                    beforeShowDay: function(date) {
                        var month = date.getMonth() + 1;
                        var day = date.getDate();
                        if (month in unallowedDaysJson) {
                            if (unallowedDaysJson[month].includes(day)) {
                                return false;
                            }
                        }
                        return true;
                    }
                });
                dateInput.change(function() {
                    $.ajax({
                        url: getAvailableTimeUrl,
                        data: {
                            'specialist': specialistSelect.val(),
                            'date': dateInput.val()
                        },
                        success: function(response) {
                            timeSelect.html(response.options);
                            timePickerBlock.show();
                            timeSelect.change(function() {
                                datetimeInput.val(dateInput.val() + ' ' + $(this).val());
                            })
                        },
                        error: function(response) {
                            timePickerBlock.hide();
                            console.log(response);
                        }
                    })
                })
            },
            error: function(response) {
                console.log(response);
            }
        })
        dateInput.prop('disabled', false);
    })
})
