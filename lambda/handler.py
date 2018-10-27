import json

import alexandra


app = alexandra.Application()

@app.intent("GetServiceAlertsIntent")
def service_alert(event, context):
    print("server_alert intent event is")
    print(event)

    return alexandra.respond("Service Alerts Intent Response")

def dispatch(event, context):
    print("Dispatch event is:")
    print(event)
    return app.dispatch_request(event)
