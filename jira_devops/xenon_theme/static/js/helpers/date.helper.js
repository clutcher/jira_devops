// add (or subtract) business days to provided date
addBusinessDays = function (startingDate, daysToAdjust) {
    var newDate = new Date(startingDate.valueOf()),
        businessDaysLeft,
        isWeekend,
        direction;

    // Timezones are scary, let's work with whole-days only
    if (daysToAdjust !== parseInt(daysToAdjust, 10)) {
        throw new TypeError('addBusinessDays can only adjust by whole days');
    }

    // short-circuit no work; make direction assignment simpler
    if (daysToAdjust === 0) {
        return startingDate;
    }
    direction = daysToAdjust > 0 ? 1 : -1;

    // Move the date in the correct direction
    // but only count business days toward movement
    businessDaysLeft = Math.abs(daysToAdjust);
    while (businessDaysLeft) {
        newDate.setDate(newDate.getDate() + direction);
        isWeekend = newDate.getDay() in {0: 'Sunday', 6: 'Saturday'};
        if (!isWeekend) {
            businessDaysLeft--;
        }
    }
    return newDate;
};