from prompt_toolkit.filters import is_done
from prompt_toolkit.formatted_text import HTML
from prompt_toolkit.shortcuts import choice
from prompt_toolkit.styles import Style

class ChoiceFrame:
    def __init__(self, options: list):
        new_options = [(0, "新对话")]
        for i in options:
            new_options.append(i)
        self.options = new_options
        self.style = Style.from_dict(
            {
                "frame.border": "#ff4444",
                "selected-option": "bold",
                # ('noreverse' because the default toolbar style uses 'reverse')
                "bottom-toolbar": "#ffffff bg:#333333 noreverse",
            }
        )
    def choice(self):
        self.result = choice(
            message=HTML("<u>选择一个会话或者创建新会话</u>:"),
            options=self.options,
            style=self.style,
            bottom_toolbar=HTML(
                " Press <b>[Up]</b>/<b>[Down]</b> to select, <b>[Enter]</b> to accept."
            ),
            show_frame=~is_done,
        )
        return self.result
