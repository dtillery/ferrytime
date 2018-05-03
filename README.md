# ferrytime

## Development

1. Install Amazon [ask-cli](https://developer.amazon.com/docs/smapi/quick-start-alexa-skills-kit-command-line-interface.html).
1. `ask init` and follow directions.
1. Install [Serverless](https://serverless.com/framework/docs/providers/aws/guide/installation/)

## Deployment

### Lambda
1. Install [serverless-python-requirements](https://github.com/UnitedIncome/serverless-python-requirements) (requires docker to run as well?)
1. `cd lambda`
1. `sls deploy -v`

### Skill
1. `cd skill`
1. `ask deploy`