import subprocess

from invoke import task

LAMBDA_DIR = "lambda"

@task
def deploy(c):
    with c.cd("lambda"):
        c.run("sls deploy -v", pty=True)
