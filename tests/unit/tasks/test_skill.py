from tasks import skill

def assert_equalish_lists(results, expecteds):
    # assert lists are same lenght and contain same values, order irrelevent
    assert len(results) == len(expecteds) and sorted(results) == sorted(expecteds)

def test_render_utterances_simple():
    test_string = "this is a test"
    rendered_strings = skill.render_utterances(test_string)
    assert rendered_strings == [test_string]


def test_render_utterances_template_single():
    template = "this is [a] test"
    rendered_strings = skill.render_utterances(template)
    assert_equalish_lists(rendered_strings, ["this is a test"])

    template = "this [is] a [test] string"
    rendered_strings = skill.render_utterances(template)
    assert_equalish_lists(rendered_strings, ["this is a test string"])


def test_render_utterances_template_multiple():
    template = "this is [a|the] test"
    rendered_strings = skill.render_utterances(template)
    assert_equalish_lists(rendered_strings, ["this is a test", "this is the test"])

    template = "this [is|was] a [test|exam]"
    rendered_strings = skill.render_utterances(template)
    assert_equalish_lists(rendered_strings, [
        "this is a test",
        "this was a test",
        "this is a exam",
        "this was a exam"
    ])

    template = "[this|it] [is|was] a [test|exam|mistake]"
    rendered_strings = skill.render_utterances(template)
    assert_equalish_lists(rendered_strings, [
        "this is a test",
        "it is a test",
        "this was a test",
        "it was a test",
        "this is a exam",
        "it is a exam",
        "this was a exam",
        "it was a exam",
        "this is a mistake",
        "it is a mistake",
        "this was a mistake",
        "it was a mistake"
    ])


def test_render_utterances_template_optional():
    template = "this is ?[a] test"
    rendered_strings = skill.render_utterances(template)
    assert_equalish_lists(rendered_strings, [
        "this is a test",
        "this is test"
    ])

    template = "this ?[is|was|will be] ?[a|the] test"
    rendered_strings = skill.render_utterances(template)
    assert_equalish_lists(rendered_strings, [
        "this is a test",
        "this is the test",
        "this is test",
        "this was a test",
        "this was the test",
        "this was test",
        "this will be a test",
        "this will be the test",
        "this will be test",
        "this a test",
        "this the test",
        "this test"
    ])
