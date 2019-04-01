import json

import alexandra


app = alexandra.Application()


@app.intent("AMAZON.FallbackIntent")
def fallback(slots, context):
    return alexandra.respond("Sorry, I didn't understand what asked for.")


@app.intent("GetServiceAlertsIntent")
def service_alert(slots, context):
    route = slots.get("Route")
    if not route:
        response = "Did not get any Route information from request."
    elif route.is_empty:
        response = "Did not match to Route slot."
    elif not route.is_match:
        response = f"Do not recognize route {route.original_value}."
    else:
        response = f"Getting alerts for route {route.matched_value}."

    return alexandra.respond(response)


def dispatch(event, context):
    return app.dispatch_request(event)
