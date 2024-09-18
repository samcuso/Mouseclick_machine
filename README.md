### Mouseclick连点器代码解读

#### 基于customtkinter库以及pyautogui库实现

```python
set_appearance_mode("System")
set_default_color_theme("blue")
```

##### set_appearance_mode()方法

可接受三个参数：

“System”：随系统主题颜色变化

“Dark”：夜间主题

“Light”：日间主题

##### set_default_color_theme()方法

可接受三个参数：

“blue” “green” “dark-blue”

用于替换按钮颜色

------

```python
app = CTk()
app.geometry("400*400")
app.title("MouseClick machine")
```

##### app = CTk() 

创建了一个父对象，作为整个界面的基底

之后app后面跟的方法都是对app进行基础设定

##### .geometry()方法

用于设定界面的默认大小

##### .title()方法

用于设定界面的名称

------

```python
# 添加窗口小部件
button = CTkButton(master=app, text="Click me", command=lambda: print("Button clicked"))
button.pack(pady=20)  # 使用 pack 布局管理器
```

此处为V1的代码，主要用于演示窗口小部件的构成

