def html_tag(tag):
    def decorator(func):
        def wrapper(*args, **kwargs):
            return "<{tag}>{text}</{tag}>".format(tag=tag, text=func(*args, **kwargs))

        return wrapper

    return decorator


def html_tag_function_creator(tag_list: list):
    tag_function = {
    }
    for tag in tag_list:
        tag_function[tag] = '''@html_tag("{tag_name}")
def {tag_name}(content):
    return content
        '''.format(tag_name=tag)

    tag_function_str = ""
    for text in tag_function.values():
        tag_function_str += text + "\n"

    return tag_function_str


def html_tag_text(text, *tags):
    html_tag_str = text
    for tag in reversed(tags):
        html_tag_str = "<{tag}>{text}</{tag}>".format(tag=tag, text=html_tag_str)
    return html_tag_str


