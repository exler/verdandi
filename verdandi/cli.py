from shutil import get_terminal_size


def print_header(text: str, padding_symbol: str = "=") -> None:
    """
    Prints given text padded from both sides with `padding_symbol` up to terminal width
    """
    text_length = len(text)
    columns = get_terminal_size()[0]

    padding_length = ((columns - text_length) // 2) - 1  # Substract one whitespace from each side
    padding = padding_symbol * padding_length

    print(f"{padding} {text} {padding}")
