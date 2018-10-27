# ferrytime

## Development

1. Install Amazon [ask-cli](https://developer.amazon.com/docs/smapi/quick-start-alexa-skills-kit-command-line-interface.html).
1. `ask init` and follow directions.
1. Install [Serverless](https://serverless.com/framework/docs/providers/aws/guide/installation/)
1. Install python 3.6+ (managed using [pyenv](https://github.com/pyenv/pyenv), for example)
1. Install [Pipenv](https://pipenv.readthedocs.io/en/latest/) and run `pipenv install`

## Test
Start a pipenv shell session via `pipenv shell`

```
py.test -v tests/
```

## Deployment
Start a pipenv shell session via `pipenv shell`

### Lambda
1. `cd lambda`
1. `sls deploy -v`

### Skill
`inv skill.build-and-deploy`
