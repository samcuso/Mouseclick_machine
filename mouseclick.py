import pyautogui as pa
import customtkinter as ctk
import time
import threading


def option_menu_call_back(option):
    global current_option
    current_option = option
    output_textbox.insert("end", f"选择了选项: {option}\n")
    output_textbox.see("end")  # 确保滚动条指向最新内容


def start_command(current_option):
    time.sleep(5)
    global click_count, times_get
    if current_option == "持续点击":
        output_textbox.insert("end", "开始持续点击.\n")
        output_textbox.see("end")
        # 在这里执行与选项 a 相关的操作

    elif current_option == "限次连点":
        output_textbox.insert("end", "开始限次连点.\n")
        output_textbox.see("end")
        # 在这里执行与选项 b 相关的操作
        while click_count < times_get:
            output_textbox.insert("end", f"第 {click_count + 1} 次点击。\n")
            output_textbox.see("end")
            # 记录已点击次数
            click_count += 1
            # 调用点击函数
            pa.click()

        click_count = 0
        output_textbox.insert("end", "点击完成。\n")
        output_textbox.see("end")
    else:
        output_textbox.insert("end", "无效操作，请重试.\n")
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


current_option = "未选择"
times_get = 0
ctk.set_appearance_mode("System")
ctk.set_default_color_theme("blue")
app = ctk.CTk()
app.geometry("400x500+400+300")
app.title("MouseClick machine")
app.resizable(True, True)

click_count = 0
output_textbox = ctk.CTkTextbox(app, width=200, height=180)
label_start = ctk.CTkLabel(master=app, text="这是一个连点器")
tip_label = ctk.CTkLabel(master=app, text="请输入点击次数")

var = ctk.StringVar()
entry_get_input = ctk.CTkEntry(master=app,
                               validate="key",
                               textvariable=var,
                               validatecommand=(app.register(validate_input), '%P'))
check_button = ctk.CTkButton(master=app, text="确认输入", command=time_getting)
# 连点器逻辑还没写

selected_option = ctk.StringVar(value="请选择模式")
option_menu = ctk.CTkOptionMenu(
    app,
    values=["持续点击", "限次连点"],
    command=lambda option: option_menu_call_back(option),
    variable=selected_option
)
def start_command_in_thread(current_option):
    thread = threading.Thread(target=start_command,args=(current_option,))
    thread.start()


button_test = ctk.CTkButton(master=app, text="让我们开始吧！",
                            command=lambda: start_command_in_thread(current_option))

label_start.pack()
output_textbox.pack()
tip_label.pack()
entry_get_input.pack()
check_button.pack()
option_menu.pack(pady=20, padx=20)
button_test.pack(pady=20)

if __name__ == '__main__':
    app.mainloop()
