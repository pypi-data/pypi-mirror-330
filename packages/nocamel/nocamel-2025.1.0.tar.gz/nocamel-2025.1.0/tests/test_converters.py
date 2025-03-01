from src.nocamel import converters


def test_to_snake():
    assert converters.to_snake("Hello World") == "hello_world"
    assert converters.to_snake("Camel Case Example") == "camel_case_example"
    assert converters.to_snake("snake_case") == "snake_case"
    assert converters.to_snake("PascalCase") == "pascalcase"
    assert converters.to_snake("with-dash") == "with-dash"


def test_to_lower():
    assert converters.to_lower("HelloWorld") == "helloworld"
    assert converters.to_lower("Hello World") == "hello world"
    assert converters.to_lower("CamelCaseExample") == "camelcaseexample"
    assert converters.to_lower("snake_case") == "snake_case"
    assert converters.to_lower("PascalCase") == "pascalcase"
    assert converters.to_lower("with-dash") == "with-dash"


def test_to_sentence():
    assert converters.to_sentence("Hello World") == "Hello world"
    assert converters.to_sentence("CamelCaseExample") == "Camelcaseexample"
    assert converters.to_sentence("snake_case") == "Snake_case"
    assert converters.to_sentence("PascalCase") == "Pascalcase"
    assert converters.to_sentence("with-dash") == "With-dash"


def test_to_snake_with_numbers_and_symbols():
    assert converters.to_snake("Hello 123!@#") == "hello_123!@#"


def test_to_lower_with_numbers_and_symbols():
    assert converters.to_lower("HELLO123!@#") == "hello123!@#"
    assert converters.to_lower("HELLO 123 !@#") == "hello 123 !@#"


def test_to_sentence_with_numbers_and_symbols():
    assert converters.to_sentence("HELLO123!@#") == "Hello123!@#"
    assert converters.to_sentence("HELLO 123 !@#") == "Hello 123 !@#"


def test_to_kebab():
    assert converters.to_kebab("Hello World") == "hello-world"
    assert converters.to_kebab("Camel Case Example") == "camel-case-example"
    assert converters.to_kebab("PascalCase") == "pascalcase"
    assert converters.to_kebab("camelCase") == "camelcase"


def test_to_kebab_with_numbers_and_symbols():
    assert converters.to_kebab("Hello 123!@#") == "hello-123!@#"
    assert converters.to_kebab("HELLO 123 !@#") == "hello-123-!@#"
