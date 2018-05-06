import json
import os

from invoke import task

from ask import AskCli

BASE_MODELS_DIR = "skill/models"


@task
def simulate(c, text):
    alexa = AskCli(skill_dir="skill")
    print("=== Simulating: \"{}\"".format(text))
    r = alexa.simulate(text)
    if not r.successful:
        print("Simulation failed: {}".format(r.error_message))
    else:
        print("=== Simulation Results:")
        print("Intent: {}".format(r.intent.name))
        print("Slots: {}".format(r.intent.slots))


@task
def build(c):
    print("Building")


@task
def build_models(c):
    models = [model for model in os.listdir(BASE_MODELS_DIR) if os.path.isdir(os.path.join(BASE_MODELS_DIR, model))]
    for model in models:
        build_model(model)


def build_model(model):
    model_dir = "{}/{}".format(BASE_MODELS_DIR, model)

    with open("{}/base.json".format(model_dir), "rb") as f:
        model_config = json.load(f)

    model_config = add_types(model_config, model_dir)
    model_config = add_intents(model_config, model_dir)

    with open("{}/{}.json".format(BASE_MODELS_DIR, model), "w") as f:
        json.dump(model_config, f, indent=2)


def add_types(model_config, model_dir):
    with open("{}/types.json".format(model_dir), "rb") as f:
        types_config = json.load(f)
    model_config["interactionModel"]["languageModel"]["types"] = types_config
    return model_config


def add_intents(model_config, model_dir):
    intents_dir = "{}/intents".format(model_dir)
    intents = []
    if os.path.isdir(intents_dir):
        intent_names = os.listdir(intents_dir)
        for intent_name in intent_names:
            intents.append(create_intent(intent_name, intents_dir))
    model_config["interactionModel"]["languageModel"]["intents"].extend(intents)
    return model_config


def create_intent(intent_name, intents_dir):
    intent_dir = "{}/{}".format(intents_dir, intent_name)
    intent_config = {
        "name": intent_name
    }
    intent_config_files = os.listdir(intent_dir)

    if "slots.json" in intent_config_files:
        intent_config_files.remove("slots.json")
        with open("{}/slots.json".format(intent_dir), "rb") as f:
            intent_config["slots"] = json.load(f)

    intent_config["samples"] = make_intent_samples(intent_dir, intent_config_files)

    return intent_config


def make_intent_samples(intent_dir, config_files):
    utterance_set = set()
    for config_file in config_files:
        with open("{}/{}".format(intent_dir, config_file), "rb") as f:
            utterance_configs = json.load(f)
    for utterance_config in utterance_configs:
        utterance_set.update(utterance_config.get("utterances", []))
    return list(utterance_set)

