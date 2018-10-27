import json

import alexandra


app = alexandra.Application()


@app.intent("AMAZON.FallbackIntent")
def fallback(slots, context):
    return alexandra.respond("Sorry, I didn't understand what asked for.")


@app.intent("GetServiceAlertsIntent")
def service_alert(slots, context):
    print("server_alert intent slots are:")
    print(event)

    return alexandra.respond("Service Alerts Intent Response")


def dispatch(event, context):
    print("Dispatch event is:")
    print(event)
    return app.dispatch_request(event)
