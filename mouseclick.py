import sys
import pyautogui as pa
import customtkinter as ctk
import time
import threading
import random


# 主要逻辑函数
def random_float():
    random_float_num = random.uniform(0, 0.3)
    rounded_float = round(random_float_num, 1)
    return rounded_float


def insert_and_maybe_clear(textbox, text):
    global line_counter
    textbox.insert("end", text)
    textbox.see("end")
    line_counter += text.count("\n")
    if line_counter >= 500:
        textbox.delete('1.0', "end")
        line_counter = 0


def option_menu_call_back(option):
    global current_option
    current_option = option
    insert_and_maybe_clear(output_textbox, f"选择了选项：{option}")  # 确保滚动条指向最新内容


def start_command(stop_event, current_option):
    time.sleep(4)
    global click_count, times_get
    if current_option == "持续点击":
        insert_and_maybe_clear(output_textbox, "开始持续点击.\n")
        output_textbox.see("end")
        while not stop_event.is_set():
            pa.click()
            time.sleep(random_float())
            insert_and_maybe_clear(output_textbox, f"点击了鼠标.\n")
        # 在这里执行与选项 a 相关的操作

    elif current_option == "限次连点":
        insert_and_maybe_clear(output_textbox, "开始限次连点.\n")
        output_textbox.see("end")
        # 在这里执行与选项 b 相关的操作
        while click_count < times_get and not stop_event.is_set():
            insert_and_maybe_clear(output_textbox, f"第{click_count + 1}次点击\n")
            output_textbox.see("end")
            # 记录已点击次数
            click_count += 1
            # 调用点击函数
            pa.click()

        click_count = 0
        insert_and_maybe_clear(output_textbox, "点击完成。\n")
        output_textbox.see("end")
    else:
        insert_and_maybe_clear(output_textbox, "无效操作，请重试.\n")
        output_textbox.see("end")


def validate_input(new_value):
    if new_value.isdigit():
        return True
    else:
        return False


def time_getting():
    global times_get
    input_get = entry_get_input.get()
    times_get = int(input_get)


def start_command_in_thread(current_option):
    global stop_event
    stop_event.clear()
    thread = threading.Thread(target=start_command, args=(stop_event, current_option))
    thread.start()


def toggle_click(stop_event):
    if stop_event.is_set():
        stop_event.clear()
        pause_button.configure(text="停止点击")
        output_textbox.insert("end", "点击恢复。\n")
        output_textbox.see("end")
    else:
        stop_event.set()
        pause_button.configure(text="恢复点击")
        output_textbox.insert("end", "点击停止。\n")
        output_textbox.see("end")


def handle_control(event):
    toggle_click(stop_event)


def quick_exit(event=None):
    toggle_click(stop_event)
    app.destroy()
    sys.exit()


# 全局变量区
current_option = "未选择"
times_get = 0
stop_event = threading.Event()  # 创建事件对象
click_count = 0
line_counter = 0
# 界面设置
ctk.set_appearance_mode("System")
ctk.set_default_color_theme("blue")
app = ctk.CTk()
app.geometry("400x500+400+300")
app.title("MouseClick machine")
app.resizable(True, True)

# 组件基础化
output_textbox = ctk.CTkTextbox(app, width=200, height=180)
label_start = ctk.CTkLabel(master=app, text="这是一个连点器")
tip_label = ctk.CTkLabel(master=app, text="请输入点击次数")
var = ctk.StringVar()
entry_get_input = ctk.CTkEntry(master=app,
                               validate="key",
                               textvariable=var,
                               validatecommand=(app.register(validate_input), '%P'))
check_button = ctk.CTkButton(master=app, text="确认输入", command=time_getting)
pause_button = ctk.CTkButton(master=app, text="停止点击", command=lambda: toggle_click(stop_event))
selected_option = ctk.StringVar(value="请选择模式")
option_menu = ctk.CTkOptionMenu(
    app,
    values=["持续点击", "限次连点"],
    command=lambda option: option_menu_call_back(option),
    variable=selected_option
)
button_test = ctk.CTkButton(master=app, text="让我们开始吧！",
                            command=lambda: start_command_in_thread(current_option))

# widget摆放
label_start.pack()
output_textbox.pack()
tip_label.pack()
entry_get_input.pack()
check_button.pack()
option_menu.pack(pady=20, padx=20)
button_test.pack(pady=20)
pause_button.pack(pady=20)

app.bind('<Control-q>', handle_control)
app.bind('<Control-p>', quick_exit)

if __name__ == '__main__':
    app.mainloop()
