import flet as ft
try:
    from . import core
    from .version import version
except ImportError:
    import core
    from version import version

__version__ = version
aboutmsg="""这是一个可以从松散文件和client.jar提取Minecraft的原版资源包和数据包的工具  
这个工具除了jar文件的内容以外，还提取了:
- 音乐和音效文件
- 完整的语言文件
- Unifont的位图字体
- 完整的全景图
- Programmer Art和高对比度资源包

觉得这个项目还不错，去Github给个Star没问题吧awa  
或者在爱发电给一点小小的资金鼓励！

如果你觉得这个UI不习惯的话，可以使用`aortk`回到以前的旧Tkinter UI

请勿分发使用这个程序提取出来的资源，这些资源仅用作资源包的开发，我不会对此承担任何责任"""

def page(page: ft.Page):
    # 关于窗口
    def about(e=None):
        dialog = ft.AlertDialog(
           modal=True,
           title=ft.Text("关于"),
           content=ft.Container(  # 添加尺寸限制容器
               content=ft.Column([
                   ft.Row([
                       ft.Image("icon.png",width=40, height=40),
                       ft.Text(f"All Of Resources {__version__}", size=20, weight=ft.FontWeight.BOLD)
                   ]),
                   ft.Markdown(aboutmsg)
               ], scroll=ft.ScrollMode.ALWAYS),  # 启用滚动条
               width=600,  # 固定宽度
               height=400  # 固定高度
           ),
           on_dismiss=lambda e: page.close(dialog),
           actions=[ft.TextButton("Github",on_click=lambda e: page.launch_url("https://github.com/SystemFileB/all-of-resources")),
                    ft.TextButton("爱发电",on_click=lambda e: page.launch_url("https://afdian.com/a/systemfileb")),
                    ft.TextButton("关闭", on_click=lambda e: page.close(dialog))]
        )
        page.open(dialog)
    
    page.title=f"All Of Resources {__version__}"
    page.vertical_alignment=ft.MainAxisAlignment.START
    bar = ft.AppBar(
        title=ft.Row([
            ft.Text(f"All Of Resources {__version__}"),
            ft.Container(expand=True),  # 新增中间弹性容器
            ft.IconButton(
                icon=ft.Icons.INFO_OUTLINE,
                on_click=about,
                tooltip="关于",
            )
        ], 
        expand=True,
        alignment=ft.MainAxisAlignment.START),  # 设置对齐方式
    )

    # 检查是否信息收集完毕
    def check(e=None):
        nonlocal minecraftdir_old
        result=core.check(minecraftdir_text.value,version_box.value,outputdir_text.value)
        if minecraftdir_old!=minecraftdir_text.value:
            if result[0]:
                version_box.options=[ft.dropdown.Option(i) for i in result[0]]
                version_box.value=result[0][0]
        if result[1]:
            logtext.value=result[2]
            start_button.disabled=False
        minecraftdir_old=minecraftdir_text.value
        page.update()
    
    def task(e=None):
        def callback(progress,msg):
            logtext.value=msg
            progressbar.value=progress/2000
            page.update()
        def runtask():
            def close(e=None):
                page.close(dialog)
                progressbar.value=0
                page.update()

            result=core.task(minecraftdir_text.value,version_box.value,outputdir_text.value,callback)
            if result[0]=="E":
                icon=ft.Icons.ERROR_OUTLINE
                logtext.value=result[1]
            elif result[0]=="I":
                icon=ft.Icons.INFO_OUTLINE
                logtext.value="All Of Resources FLUTTER EDITION!\n给个Star awa"
            dialog=ft.AlertDialog(modal=True,
                                  title=ft.Text("All Of Resources"),
                                  content=ft.Row([ft.Icon(icon),ft.Text(result[1])]),
                                  actions=[ft.TextButton("关闭", on_click=close)],
                                  on_dismiss=close
            )
            page.open(dialog)
            start_button.disabled=False
        
        start_button.disabled=True
        page.update()
        page.run_thread(runtask)
    
    # 文件选择器
    TO_MINECRAFTDIR=0
    TO_OUTPUTDIR=1
    pickTo=TO_MINECRAFTDIR
    def pick_dir_event(e: ft.FilePickerResultEvent):
        if pickTo==TO_MINECRAFTDIR:
            minecraftdir_text.value=e.path
        elif pickTo==TO_OUTPUTDIR:
            outputdir_text.value=e.path
        check()

    def filedialog(type,title):
        nonlocal pickTo
        pickTo=type
        file_picker.get_directory_path(title)
    file_picker=ft.FilePicker(on_result=pick_dir_event)
    page.overlay.append(file_picker)

    # 构建界面
    minecraftdir_text=ft.TextField(label=".minecraft目录位置", expand=1, on_change=check)  # 添加expand让输入框填充剩余空间
    minecraftdir_select_button=ft.ElevatedButton(text="...",on_click=lambda e: filedialog(TO_MINECRAFTDIR,"选择.minecraft目录"))
    minecraftdir = ft.Row([minecraftdir_text, minecraftdir_select_button])
    minecraftdir_old=minecraftdir_text.value

    version_box=ft.Dropdown(label="版本",width=int(float(page.width)) if page.width else 400)

    outputdir_text=ft.TextField(label="输出目录位置", expand=1, on_change=check)  # 添加expand让输入框填充剩余空间
    outputdir_select_button=ft.ElevatedButton(text="...",on_click=lambda e: filedialog(TO_OUTPUTDIR,"选择解压路径"))
    outputdir = ft.Row([outputdir_text, outputdir_select_button])

    progressbar=ft.ProgressBar(value=0)

    logtext=ft.Text(value="All Of Resources FLUTTER EDITION!\n给个Star awa\n\n注意：解压路径需要使用空文件夹")

    start_button=ft.FloatingActionButton(
        icon=ft.Icons.DOWNLOAD,
        tooltip="开始",
        disabled=True,
        on_click=task
    )

    page.add(bar,minecraftdir,version_box,outputdir,progressbar,logtext,start_button)



def main():
    ft.app(
        target=page,
        assets_dir=".",
        use_color_emoji=True,
    )

if __name__=="__main__":
    main()