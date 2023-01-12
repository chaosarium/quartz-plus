// code from https://gitlab.nomagic.uk/popi/js_calendar_from_ics... i don't know how it works but it works
// Depends ical.js

function ical_events(ical, event_callback, recur_event_callback) {
    jcal_events(ICAL.parse(ical), event_callback, recur_event_callback)
}

function jcal_events(jcal, event_callback, recur_event_callback) {
    for (event of new ICAL.Component(jcal).getAllSubcomponents('vevent')) {
        if (event.hasProperty('rrule')) {
            recur_event_callback(event)
        } else {
            event_callback(event)
            //console.log(event);
        }
        //var myevent = new ICAL.Event(event);
        //console.log(myevent.summary, myevent.description, myevent.start, myevent.end, myevent.title);
        //console.log(event.jCal[1][2][3]);
    }
}

function event_duration(event) {
    return new Date(event.getFirstPropertyValue('dtend').toJSDate() - event.getFirstPropertyValue('dtstart').toJSDate()).getTime()
}

function event_dtend(dtstart, duration) {
    return new ICAL.Time().fromJSDate(new Date(dtstart.toJSDate().getTime() + duration))
}

function expand_recur_event(event, dtstart, dtend, event_callback) {
    exp = new ICAL.RecurExpansion({
        component:event,
        dtstart:event.getFirstPropertyValue('dtstart')
    })
    duration = event_duration(event)
    while (! exp.complete && exp.next() < dtend) {
        if (exp.last >= dtstart) {
            event = new ICAL.Component(event.toJSON())
            event.updatePropertyWithValue('dtstart', exp.last)
            event.updatePropertyWithValue('dtend', event_dtend(exp.last, duration))
            event_callback(event)
        }
    }
}

