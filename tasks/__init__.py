from invoke import Collection

from . import skill, aws_lambda

ns = Collection()
ns.add_collection(Collection.from_module(skill))
ns.add_collection(Collection.from_module(aws_lambda, name="lambda"))
