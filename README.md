# ferrytime

## Development

1. Install Amazon [ask-cli](https://developer.amazon.com/docs/smapi/quick-start-alexa-skills-kit-command-line-interface.html).
1. `ask init` and follow directions.
1. Install [Serverless](https://serverless.com/framework/docs/providers/aws/guide/installation/)
1. Install python 3.6+ (managed using [pyenv](https://github.com/pyenv/pyenv), for example)
1. Install [Pipenv](https://pipenv.readthedocs.io/en/latest/) and run `pipenv install`

## Testing
Start a pipenv shell session via `pipenv shell`

### Unit Tests
```
py.test -v tests/
```

### Simulating Alexa Responses
You can run a simulation of a command against the deployed skill/lambda. This is run
via the Alexa Skills Kit simulate. The start word "Alexa" is automatically prepended.

```
inv skill.simulate "ask ferry time for east river ferry service alerts"

=== Simulating: "ask ferry time for east river ferry service alerts"
=== Simulation Results:
Intent: GetServiceAlertsIntent
Slots: {'Route': {'value': 'east river ferry', 'matched_id': 'ER', 'matched_name': 'east river'}}
Response: Service Alerts Intent Response
```


## Deployment
Start a pipenv shell session via `pipenv shell`

### Lambda
1. `cd lambda`
1. `sls deploy -v`

### Skill
`inv skill.build-and-deploy`
