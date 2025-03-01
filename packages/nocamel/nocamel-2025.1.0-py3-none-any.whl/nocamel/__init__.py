import click
import pyperclip

from nocamel import converters

__version__ = "2025.1.0"


@click.command()
@click.option("--snake", is_flag=True, help="Convert to snake_case")
@click.option("--lower", is_flag=True, help="Convert to lowercase")
@click.option("--sentence", is_flag=True, help="Convert to sentence case")
@click.option("--kebab", is_flag=True, help="Convert to kebab case")
@click.argument("input", type=click.STRING)
def main(snake: bool | None, lower: bool | None, sentence: bool | None, kebab: bool | None, input: str) -> None:
    if [snake, lower, sentence, kebab].count(True) > 1:
        raise ValueError("Exactly one of --snake, --lower, or --sentence must be specified.")

    if not any([snake, lower, sentence, kebab]):
        sentence = True

    if snake:
        result = converters.to_snake(input)
    elif lower:
        result = converters.to_lower(input)
    elif sentence:
        result = converters.to_sentence(input)
    elif kebab:
        result = converters.to_kebab
    print(result)
    try:
        pyperclip.copy(result)  # Copy to clipboard
        click.echo("Result copied to clipboard!")
    except Exception as e:
        raise click.ClickException(f"Failed to copy to clipboard: {str(e)}")
