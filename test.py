from prompt_toolkit import PromptSession
from prompt_toolkit.keys import Keys
from prompt_toolkit.formatted_text import FormattedText

def run_menu():
    options = ["新建文件", "编辑文件", "删除文件", "退出"]
    current = 0

    def print_menu():
        # 构建带样式的文本列表
        result = []
        for i, opt in enumerate(options):
            if i == current:
                result.append(('class:highlight', f'> {opt}'))
            else:
                result.append(('', f'  {opt}'))
            result.append(('', '\n'))
        return result

    session = PromptSession()

    while True:
        # 显示菜单并等待按键（不等待回车）
        answer = session.prompt(
            print_menu,
            key_bindings=None,   # 我们手动处理按键
            default='',
            refresh_interval=0.1
        )
        # 但更常用的方式是使用 prompt_toolkit 的 `Application` 和键绑定
        # 为了简洁，这里展示一个简单的循环捕获按键
        # 注意：上面的 answer 会等待回车，不适合菜单。我们改用更好的方法：

 # --- 更正确的 prompt_toolkit 菜单实现，使用键绑定 ---
from prompt_toolkit.application import Application
from prompt_toolkit.application.current import get_app
from prompt_toolkit.key_binding import KeyBindings
from prompt_toolkit.layout import Layout, HSplit, Window
from prompt_toolkit.layout.controls import FormattedTextControl
from prompt_toolkit.styles import Style

def main():
    options = ["新建文件", "编辑文件", "删除文件", "退出"]
    selected_index = 0

    # 定义内容控件
    def get_content():
        lines = []
        for i, opt in enumerate(options):
            if i == selected_index:
                lines.append(('class:highlight', f'> {opt}'))
            else:
                lines.append(('', f'  {opt}'))
            lines.append(('', '\n'))
        return lines

    content_control = FormattedTextControl(get_content)
    root_container = HSplit([Window(content_control, height=len(options))])
    layout = Layout(root_container)

    # 键绑定
    kb = KeyBindings()

    @kb.add('up')
    def up(event):
        nonlocal selected_index
        selected_index = (selected_index - 1) % len(options)
        # 刷新界面
        content_control.text = get_content

    @kb.add('down')
    def down(event):
        nonlocal selected_index
        selected_index = (selected_index + 1) % len(options)
        content_control.text = get_content

    @kb.add('enter')
    def enter(event):
        print(f"你选择了：{options[selected_index]}")
        get_app().exit()

    @kb.add('q')
    def quit(event):
        get_app().exit()

    style = Style.from_dict({
        'highlight': 'bold reverse',
    })

    app = Application(layout=layout, key_bindings=kb, style=style, full_screen=True)
    app.run()

if __name__ == "__main__":
    main()