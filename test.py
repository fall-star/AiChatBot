from prompt_toolkit.formatted_text import HTML
from prompt_toolkit import print_formatted_text

print_formatted_text(HTML("<b><red>model_output:</red></b>"))
print_formatted_text(HTML("<red>model_output:</red>"))