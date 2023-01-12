// code from https://gitlab.nomagic.uk/popi/js_calendar_from_ics... i don't know how it works but it works
// Depends on ./ical_events.js

recur_events = []

function an_filter(string) {
    // remove non alphanumeric chars
    return string.replace(/[^\w\s]/gi, '')
}

function moment_icaltime(moment, timezone) {
    // TODO timezone
    return new ICAL.Time().fromJSDate(moment.toDate())
}

function expand_recur_events(start, end, timezone, events_callback) {
    events = []
    for (event of recur_events) {
	event_properties = event.event_properties
        expand_recur_event(event, moment_icaltime(start, timezone), moment_icaltime(end, timezone), function(event){
            fc_event(event, function(event){
                events.push(merge_events(event_properties, merge_events({className:['recur-event']}, event)))
            })
        })
    }
    events_callback(events)
}

function fc_events(ics, event_properties) {
    events = []
    ical_events(
        ics,
        function(event){
            fc_event(event, function(event){
                events.push(merge_events(event_properties, event))
            })
        },
        function(event){
            event.event_properties = event_properties
            recur_events.push(event)
        }
    )
    return events
}

function merge_events(e, f) {
    // f has priority
    for (k in e) {
        if (k == 'className') {
            f[k] = [].concat(f[k]).concat(e[k])
        } else if (! f[k]) {
            f[k] = e[k]
        }
    }
    return f
}

function fc_event(event, event_callback) {
    e = {
        title:event.getFirstPropertyValue('summary'),
        description:event.getFirstPropertyValue('description'),
        loc:event.getFirstPropertyValue('location'),
        // url:event.getFirstPropertyValue('attach') || event.getFirstPropertyValue('url'),
        id:event.getFirstPropertyValue('uid'),
        className:['event-'+an_filter(event.getFirstPropertyValue('uid'))],
        allDay:false
    }
    try {
        e['start'] = event.getFirstPropertyValue('dtstart').toJSDate()
    } catch (TypeError) {
        console.debug('Undefined "dtstart", vevent skipped.')
        return
    }
    try {
        e['end'] = event.getFirstPropertyValue('dtend').toJSDate()
    } catch (TypeError) {
        e['allDay'] = true
    }
    event_callback(e)
}