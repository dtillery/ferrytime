import re
import itertools
import json
import os

from invoke import task

from ask import AskCli

BASE_MODELS_DIR = "skill/models"
UTTERANCE_TEMPLATE_PATTERN = re.compile(r"\??\[([-a-zA-Z. _'\|]*)\]")


@task
def simulate(c, text):
    alexa = AskCli(skill_dir="skill")
    print(f"=== Simulating: \"{text}\"")
    r = alexa.simulate(text)
    if not r.successful:
        print(f"Simulation failed: {r.error_message}")
    else:
        print("=== Simulation Results:")
        print(f"Intent: {r.intent.name}")
        print(f"Slots: {r.intent.slots}")


@task
def build_models(c):
    models = [model for model in os.listdir(BASE_MODELS_DIR) if os.path.isdir(os.path.join(BASE_MODELS_DIR, model))]
    for model in models:
        build_model(model)


def build_model(model):
    model_dir = f"{BASE_MODELS_DIR}/{model}"

    with open(f"{model_dir}/base.json", "rb") as f:
        model_config = json.load(f)

    model_config = add_types(model_config, model_dir)
    model_config = add_intents(model_config, model_dir)

    with open(f"{BASE_MODELS_DIR}/{model}.json", "w") as f:
        json.dump(model_config, f, indent=2)


def add_types(model_config, model_dir):
    with open(f"{model_dir}/types.json", "rb") as f:
        types_config = json.load(f)
    model_config["interactionModel"]["languageModel"]["types"] = types_config
    return model_config


def add_intents(model_config, model_dir):
    intents_dir = f"{model_dir}/intents"
    intents = []
    if os.path.isdir(intents_dir):
        intent_names = os.listdir(intents_dir)
        for intent_name in intent_names:
            intents.append(create_intent(intent_name, intents_dir))
    model_config["interactionModel"]["languageModel"]["intents"].extend(intents)
    return model_config


def create_intent(intent_name, intents_dir):
    intent_dir = f"{intents_dir}/{intent_name}"
    intent_config = {
        "name": intent_name
    }
    intent_config_files = os.listdir(intent_dir)

    if "slots.json" in intent_config_files:
        intent_config_files.remove("slots.json")
        with open(f"{intent_dir}/slots.json", "rb") as f:
            intent_config["slots"] = json.load(f)

    intent_config["samples"] = make_intent_samples(intent_dir, intent_config_files)

    return intent_config


def make_intent_samples(intent_dir, config_files):
    utterance_set = set()
    utterance_configs = []
    for config_file in config_files:
        with open(f"{intent_dir}/{config_file}", "rb") as f:
            utterance_configs.extend(json.load(f))
    for utterance_config in utterance_configs:
        for utterance_string in utterance_config.get("utterances", []):
            utterance_set.update(render_utterances(utterance_string))
    return sorted(list(utterance_set))


def render_utterances(template_string):
    matches = []
    def sub_for_interpolation(match):
        options = match.group(1).split("|")
        if match.group(0).startswith("?"):
            options.append("")
        matches.append(options)
        return "{}"

    # match [...] or ?[...], capture text between brackets
    base_string = UTTERANCE_TEMPLATE_PATTERN.sub(sub_for_interpolation, template_string)
    combinations = [base_string.format(*combo) for combo in itertools.product(*matches)]
    return [" ".join(string.split()) for string in combinations]
