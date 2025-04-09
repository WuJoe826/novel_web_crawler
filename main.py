import pyglet, os, random, parsel, re, requests, numpy as np, customtkinter as ctk
from tkinter import *
from PIL import Image, ImageTk
from fake_useragent import UserAgent

pyglet.font.add_file("zpix.ttf")
font_family = "zpix"
current_page = "spider_page"

file_path = os.path.dirname(os.path.realpath(__file__))
image_code = ctk.CTkImage(Image.open(file_path + "/image/terminal.png"), size=(35, 35))
image_file_pen = ctk.CTkImage(
    Image.open(file_path + "/image/file-pen.png"), size=(35, 35)
)
image_gear = ctk.CTkImage(Image.open(file_path + "/image/gear.png"), size=(35, 35))
image_cube = ctk.CTkImage(Image.open(file_path + "/image/cube.png"), size=(35, 35))
txt_export_path = r"C:\Users\wujoe\OneDrive\文件\AI_Sound_Novel\素材\文本"
# image_background = ctk.CTkImage(Image.open(file_path + "/image/background.png"), size=(1450,800))
ctk.deactivate_automatic_dpi_awareness()


def center_window_to_display(Screen: ctk, width: int, height: int):
    screen_width = Screen.winfo_screenwidth()
    screen_height = Screen.winfo_screenheight()
    x = int((screen_width / 2) - (width / 2))
    y = int((screen_height / 2) - (height / 1.8))
    return f"{width}x{height}+{x}+{y}"


class App(ctk.CTk):
    def __init__(root):
        super().__init__()

        root.title("多功能文本處理器 - Made By WuJoe")
        root.iconbitmap(file_path + "/image/icon.ico")
        window_height = 800
        window_width = 1450
        root.geometry(center_window_to_display(root, window_width, window_height))
        root.resizable(False, False)
        # container grid for all page containers
        root.grid_columnconfigure(1, weight=1)
        root.grid_rowconfigure(0, weight=1)
        # side bar
        root.sidebar_frame = ctk.CTkFrame(root, width=100, corner_radius=0)
        # side bar grid
        root.sidebar_frame.grid_rowconfigure(5, weight=1)
        # show side bar
        root.sidebar_frame.grid(row=0, column=0, rowspan=5, sticky="nsew")
        # side bar buttons
        root.spider_page_button = ctk.CTkButton(
            root.sidebar_frame,
            image=image_code,
            text="",
            width=60,
            height=60,
            fg_color="transparent",
            hover_color="#343638",
        )
        root.txt_edit_page_button = ctk.CTkButton(
            root.sidebar_frame,
            image=image_file_pen,
            text="",
            width=60,
            height=60,
            fg_color="transparent",
            hover_color="#343638",
        )
        root.cube_button = ctk.CTkButton(
            root.sidebar_frame,
            image=image_cube,
            text="",
            width=60,
            height=60,
            fg_color="transparent",
            hover_color="#343638",
        )
        root.setting_button = ctk.CTkButton(
            root.sidebar_frame,
            image=image_gear,
            text="",
            width=60,
            height=60,
            fg_color="transparent",
            hover_color="#343638",
        )
        # show side bar buttons
        root.spider_page_button.grid(
            row=0, column=0, padx=15, pady=(25, 0), sticky="nsew"
        )
        root.txt_edit_page_button.grid(
            row=1, column=0, padx=15, pady=(10, 0), sticky="nsew"
        )
        root.cube_button.grid(row=2, column=0, padx=15, pady=(10, 0), sticky="nsew")
        root.setting_button.grid(row=5, column=0, padx=15, pady=(0, 20), sticky="s")
        # spider page main_container
        root.spider_main_container = ctk.CTkFrame(
            root, fg_color="transparent", height=800, width=1350
        )
        root.txt_edit_page_main_container = ctk.CTkFrame(
            root, fg_color="transparent", height=800, width=1350
        )
        root.cube_page_main_container = ctk.CTkFrame(
            root, fg_color="transparent", height=800, width=1350
        )
        root.setting_page_main_container = ctk.CTkFrame(
            root, fg_color="transparent", height=800, width=1350
        )
        # spider_page widgets grid
        root.spider_main_container.grid_columnconfigure(1, weight=1)
        root.spider_main_container.grid_columnconfigure((2, 3), weight=1)
        root.spider_main_container.grid_rowconfigure((0, 1, 2, 3), weight=1)
        root.txt_edit_page_main_container.grid_columnconfigure(1, weight=1)
        root.txt_edit_page_main_container.grid_columnconfigure((2, 3), weight=1)
        root.txt_edit_page_main_container.grid_rowconfigure((0, 1, 2, 3), weight=1)
        root.cube_page_main_container.grid_columnconfigure(1, weight=1)
        root.cube_page_main_container.grid_columnconfigure((2, 3), weight=1)
        root.cube_page_main_container.grid_rowconfigure((0, 1, 2, 3), weight=1)
        root.setting_page_main_container.grid_columnconfigure(1, weight=1)
        root.setting_page_main_container.grid_rowconfigure((0, 1, 2, 3), weight=1)

        def switch_page(switch_to_page):
            global current_page
            if current_page == switch_to_page:
                return

            if current_page == "spider_page" and hasattr(root, "spider_main_container"):
                root.spider_main_container.grid_forget()
            elif current_page == "txt_edit_page" and hasattr(root, "txt_edit_page_main_container"):
                root.txt_edit_page_main_container.grid_forget()
            elif current_page == "cube_page" and hasattr(root, "cube_page_main_container"):
                root.cube_page_main_container.grid_forget()
            elif current_page == "setting_page" and hasattr(root, "setting_page_main_container"):
                root.setting_page_main_container.grid_forget()

            if switch_to_page == "spider_page":
                if not hasattr(root, "spider_main_container"):
                    root.spider_main_container = ctk.CTkFrame(
                        root, fg_color="transparent", height=800, width=1350
                    )
                spider_page(root)
                root.spider_main_container.grid(row=0, column=1, sticky="nsew")
            elif switch_to_page == "txt_edit_page":
                if not hasattr(root, "txt_edit_page_main_container"):
                    root.txt_edit_page_main_container = ctk.CTkFrame(
                        root, fg_color="transparent", height=800, width=1350
                    )
                txt_edit_page(root)
                root.txt_edit_page_main_container.grid(row=0, column=1, sticky="nsew")
            elif switch_to_page == "cube_page":
                if not hasattr(root, "cube_page_main_container"):
                    root.cube_page_main_container = ctk.CTkFrame(
                        root, fg_color="transparent", height=800, width=1350
                    )
                cube_page(root)
                root.cube_page_main_container.grid(row=0, column=1, sticky="nsew")
            elif switch_to_page == "setting_page":
                if not hasattr(root, "setting_page_main_container"):
                    root.setting_page_main_container = ctk.CTkFrame(
                        root, fg_color="transparent", height=800, width=1350
                    )
                setting_page(root)
                root.setting_page_main_container.grid(row=0, column=1, sticky="nsew")

            current_page = switch_to_page

        def spider_page(root):
            root.spider_main_container.grid(row=0, column=1, sticky="nsew")
            if not hasattr(root, "spider_main_container"):
                root.spider_main_container = ctk.CTkFrame(
                    root, fg_color="transparent", height=800, width=1350
                )
            if not hasattr(root, "spider_title_lable"):
                root.spider_title_lable = ctk.CTkLabel(
                    root.spider_main_container,
                    text=" 網絡小説爬取器：",
                    font=(font_family, 50, "bold"),
                )
            if not hasattr(root, "spider_textbox"):
                root.spider_textbox = ctk.CTkTextbox(
                    root.spider_main_container,
                    width=350,
                    fg_color="#2B2B2B",
                    corner_radius=15,
                    font=(font_family, 20),
                    border_spacing=35,
                )
                root.spider_textbox.configure(state="normal")
                root.spider_textbox.insert(
                    ctk.END, "> 下方輸入網址並按提取文本後開始運作。\n\n"
                )
                root.spider_textbox.configure(state="disabled")
            if not hasattr(root, "spider_entry"):
                root.spider_entry = ctk.CTkEntry(
                    root.spider_main_container,
                    placeholder_text="請輸入小説網址 (輸入/mode設定模式)",
                    font=(font_family, 20),
                    width=900,
                    height=50,
                    corner_radius=15,
                    border_width=3,
                )
            if not hasattr(root, "spider_extract_button"):
                root.spider_extract_button = ctk.CTkButton(
                    root.spider_main_container,
                    text="提取文本",
                    corner_radius=15,
                    fg_color="transparent",
                    border_width=3,
                    text_color=("gray10", "#DCE4EE"),
                    hover_color="#505050",
                    font=(font_family, 20),
                )

            def extract_button_event():
                url_input = root.spider_entry.get()
                if url_input == "/mode":
                    root.spider_textbox.configure(state="normal")
                    root.spider_textbox.delete("0.1", "end")
                    root.spider_textbox.configure(state="disabled")
                    print_text("> 目前模式：mode 0")
                    print_text("> /mode 0 : 將每個章節都打包成txt。")
                    print_text("> /mode 1 : 將所有章節打包成一個獨立txt。")
                    print_text("> /mode 2 + int : 將所有章節打包成多個固定字數的txt。")
                elif "fanqienovel.com" in url_input:
                    root.spider_extract_button.configure(
                        text="提取中", state="disabled"
                    )
                    fanqienovel(url_input)
                elif "tw.linovelib.com" in url_input:
                    root.spider_extract_button.configure(
                        text="提取中", state="disabled"
                    )
                    print("嗶哩輕小説")
                elif "novels.com.tw" in url_input:
                    root.spider_extract_button.configure(
                        text="提取中", state="disabled"
                    )
                    print("繁體小説")
                elif "novel543.com" in url_input:
                    root.spider_extract_button.configure(
                        text="提取中", state="disabled"
                    )
                    novel543(url_input)
                elif "ttkan.co" in url_input:
                    root.spider_extract_button.configure(
                        text="提取中", state="disabled"
                    )
                    print("天天看小說")
                else:
                    print_text("> 錯誤的網址，沒有此網站的記錄！")

            root.spider_extract_button.configure(command=extract_button_event)

            root.spider_title_lable.grid(
                row=0, column=1, columnspan=2, padx=(30), pady=(10, 0), sticky="w"
            )
            root.spider_textbox.grid(
                row=1,
                column=1,
                columnspan=4,
                rowspan=3,
                padx=(30),
                pady=(0, 5),
                sticky="nsew",
            )
            root.spider_entry.grid(
                row=4,
                column=1,
                columnspan=2,
                padx=(40, 0),
                pady=(15, 30),
                sticky="nsew",
            )
            root.spider_extract_button.grid(
                row=4, column=3, padx=(15, 40), pady=(15, 30), sticky="nsew"
            )

            text_queue = []

            def process_queue():
                if not text_queue:
                    return
                current_string = text_queue[0]
                if current_string == "> 正在導入必要的庫...":
                    root.spider_textbox.configure(state="normal")
                    root.spider_textbox.delete("0.1", "end")
                    root.spider_textbox.configure(state="disabled")
                update_char(current_string, 0)

            def print_text(string):
                text_queue.append(string)
                if len(text_queue) == 1:
                    process_queue()

            def update_char(string, i):
                if i < len(string):
                    root.spider_textbox.configure(state="normal")
                    root.spider_textbox.insert("end", string[i])
                    root.spider_textbox.see("end")
                    root.spider_textbox.configure(state="disabled")
                    root.after(20, update_char, string, i + 1)
                else:
                    root.spider_textbox.configure(state="normal")
                    root.spider_textbox.insert("end", "\n\n")
                    root.spider_textbox.configure(state="disabled")
                    text_queue.pop(0)
                    process_queue()

            def fanqienovel(url):
                user_agent = UserAgent(
                    browsers=["Edge", "Chrome", "Firefox"],
                    platforms="desktop",
                    os=["Windows", "Mac OS X"],
                )
                print_text("> 正在導入必要的庫...")
                print_text("> 必要庫導入成功！")
                print_text("> 正在設置目標URL...")
                print_text("> 目標URL成功設置！")
                headers = {
                    "Cookie": "Hm_lvt_2667d29c8e792e6fa9182c20a3013175=1738239566,1740120411,1740142603; "
                    "ttwid=1%7CwVQQcHc9ju2WHzl8T_R0dPCmUdARd3HOpOb2W_wY4vw%7C1740144916%7Ccb4fb65b5a7c41b60f4"
                    "51a73f9fbcc23404d1df3d45837e9faecadb3a24c68c5; novel_web_id=7391094444005492251; s_v"
                    "_web_id=verify_m51uneka_z7mieZdq_VLU4_4Qp3_BkTE_vO59AC92dt0o; _ga_S37NWVC3ZR=GS1.1.1735"
                    "008613.1.0.1735008618.0.0.0; _ga=GA1.1.640286878.1735008613; Hm_lpvt_2667d29c8e792e6fa918"
                    "2c20a3013175=1740146495; HMACCOUNT=C20A15E04EA08B70; csrf_session_id=f4c7cf8498150cd1253ed5"
                    "7c71354c8a",
                    "user-agent": user_agent.random,
                }
                print_text("> 正在發送HTTP請求...")
                response = requests.get(url=url, headers=headers)
                if response.status_code == 200:
                    print_text("> HTTP請求成功發送！")
                else:
                    print_text(
                        "> HTTP請求發送失敗，網頁狀態碼：%d" % (response.status_code)
                    )
                html = response.text
                print_text("> 正在設定parsel選擇器...")
                selector = parsel.Selector(html)
                print_text("> 選擇器成功設定為HTML！")
                print_text("> 正在解析HTML...")
                print_text("> HTML解析成功！")
                print_text("> 正在提取小説資訊...")
                print_text("> 成功獲取小説資訊！結果如下")
                print_text("{")
                novel_name = "N/A"
                novel_name = selector.css(".info-name h1::text").get()
                print_text("  小説名稱：" + novel_name)
                author_name = "N/A"
                author_name = selector.css(".author-name-text::text").get()
                print_text("  作者：" + author_name)
                novel_tag = "N/A"
                novel_tag_list = selector.css(".info-label span::text").getall()
                novel_tag = ",".join(novel_tag_list)
                print_text("  小説標簽：" + novel_tag)
                word_count = selector.css("div.info-count-word>span.detail::text").get()
                word_count_after = selector.css(
                    "div.info-count-word>span.text::text"
                ).get()
                print_text("  字數：" + str(word_count) + word_count_after)
                chapter_count = "N/A"
                chapter_info = selector.css(".volume.volume_first::text").getall()
                chapter_count = chapter_info[2]
                print_text("  目前總章數：" + chapter_count)
                print_text("}")

                chapter_title_list = selector.css(".chapter-item-title::text").getall()
                chapter_href = selector.css(".chapter-item-title::attr(href)").getall()

                def start_get_chapter_content():
                    print_text("> 開始讀取章節内容...")
                    get_chapter_content(0)
                    
                global txt_export_path
                export_path = txt_export_path + r"\\" + novel_name
                if not os.path.exists(export_path):
                    os.makedirs(export_path)

                random_number = random.randint(5000, 6000)
                root.after(random_number, start_get_chapter_content)

                def get_chapter_content(i):
                    if i < len(chapter_title_list):
                        chapter_url = "https://fanqienovel.com" + chapter_href[i + 1]
                        chapter_data = requests.get(
                            url=chapter_url, headers=headers
                        ).text
                        chapter_selector = parsel.Selector(chapter_data)
                        chapter_content_list = chapter_selector.css(
                            ".muye-reader-content.noselect p::text"
                        ).getall()
                        chapter_content = "\n".join(chapter_content_list)
                        print(chapter_title_list[i] + "\n")  # txt 名稱
                        result = []
                        for index in chapter_content:
                            try:
                                char = fanqienovel_decrypt[str(ord(index))]
                                result.append(char)
                            except KeyError:
                                char = index
                                result.append(char)
                                
                        with open(export_path + "\\" + chapter_title_list[i] + ".txt", mode='a', encoding='utf8') as f:
                            for sentence in result:
                                f.write(sentence)
                                
                        random_time = random.randint(100, 2000)

                        if i + 1 == len(chapter_title_list):
                            print_text("> 已讀取全部章節内容！")
                            root.spider_extract_button.configure(
                                text="提取文本", state="normal"
                            )
                            return None
                        else:
                            root.spider_main_container.after(
                                random_time, get_chapter_content, i + 1
                            )
                            
            def novel543(url):
                if "/dir" in url:
                    pass
                else:
                    url = url + "dir"
                user_agent = UserAgent(
                    browsers=["Edge", "Chrome", "Firefox"],
                    platforms="desktop",
                    os=["Windows", "Mac OS X"],
                )
                print_text("> 正在導入必要的庫...")
                print_text("> 必要庫導入成功！")
                print_text("> 正在設置目標URL...")
                print_text("> 目標URL成功設置！")
                headers = {
                    "Cookie": "madpfpid=ec1ef6024248732c0d572a9f8cc7829e; _ss_pp_id=11b49baccb8a95160e71740006051050; _fbp=fb.2.174"
                    "0034851275.506612941; tpdelayshowupb9z1713409295727f5=MA==; tppriorityb9z1713409295727f5=dW5kZWZpbmVk; web_ssid"
                    "=202502201500477989; _ttd_sync=1; _tg_IM=1; _td=5d6ce4d4-2b93-4ef7-898c-776563e3dfc4",
                    "user-agent": user_agent.random,
                }
                print_text("> 正在發送HTTP請求...")
                response = requests.get(url=url, headers=headers)
                if response.status_code == 200:
                    print_text("> HTTP請求成功發送！")
                else:
                    print_text(
                        "> HTTP請求發送失敗，網頁狀態碼：%d" % (response.status_code)
                    )
                html = response.text
                print_text("> 正在設定parsel選擇器...")
                selector = parsel.Selector(html)
                print_text("> 選擇器成功設定為HTML！")
                print_text("> 正在解析HTML...")
                print_text("> HTML解析成功！")
                print_text("> 正在提取小説資訊...")
                print_text("> 成功獲取小説資訊！結果如下")
                print_text("{")
                novel_name = "N/A"
                novel_name = selector.css("h1.title.is-2::text").get()
                print_text("  小説名稱：" + novel_name[:-5])
                author_name = "N/A"
                author_name = selector.css("h2.title.is-4::text").get()
                print_text("  作者：" + author_name.strip("作者 /"))
                novel_tag = "N/A"
                novel_tag = selector.css(
                    "div.meta-dir.is-justify-content-center>span:nth-child(1)>a::text"
                ).get()
                print_text("  小説標簽：" + novel_tag)
                chapter_count = "N/A"
                chapter_count = selector.css(
                    "div.meta-dir.is-justify-content-center>span:nth-child(2)::text"
                ).get()
                print_text("  目前總章數：" + chapter_count.strip("章節： "))
                print_text("}")

                chapter_title_list = selector.css(
                    ".flex.one.two-700.three-900.all>li>a::text"
                ).getall()
                chapter_href = selector.css(
                    ".flex.one.two-700.three-900.all>li>a::attr(href)"
                ).getall()

                def start_get_chapter_content():
                    print_text("> 開始讀取章節内容...")
                    get_chapter_content(0)

                random_number = random.randint(5000, 6000)
                root.after(random_number, start_get_chapter_content)

                global txt_export_path
                export_path = txt_export_path + r"\\" + novel_name[:-5]
                if not os.path.exists(export_path):
                    os.makedirs(export_path)
                
                def get_chapter_content(i):
                    if i < len(chapter_title_list):
                        chapter_url_match = re.match(
                            r"^/(\d+)/\d+_(\d+\.html)$", chapter_href[i]
                        )
                        if chapter_url_match:
                            prefix = chapter_url_match.group(1)
                            suffix = chapter_url_match.group(2)
                            chapter_url = (
                                "https://www.novel543.com/c" + f"/{prefix}_{suffix}"
                            )
                        chapter_data = requests.get(url=chapter_url, headers=headers).text
                        chapter_selector = parsel.Selector(chapter_data)
                        next_page_url = "https://www.novel543.com" + chapter_selector.css("div.warp.my-5.foot-nav a:nth-of-type(3)::attr(href)").get()
                        current_url_match = re.search(r"/c/(\d+_\d+)", chapter_url)
                        chapter_content_list = chapter_selector.css(
                            ".content.py-5>p::text"
                        ).getall()
                        result = []
                        
                        chapter_content = "\n".join(chapter_content_list)
                        for index in chapter_content:
                            try:
                                char = novel543_decrypt[str(ord(index))]
                                result.append(char)
                            except KeyError:
                                char = index
                                result.append(char)
                                    
                        with open(export_path + "\\" + chapter_title_list[i] + ".txt", mode='a', encoding='utf8') as f:
                            for sentence in result:
                                f.write(sentence)
                                
                        if current_url_match.group(1) in next_page_url:
                            next_page_data = requests.get(url=next_page_url, headers=headers).text
                            next_page_selector = parsel.Selector(next_page_data)
                            next_page_content_list = next_page_selector.css(
                            ".content.py-5>p::text"
                            ).getall()
                            next_page_content_content = "\n".join(next_page_content_list)
                            for index in next_page_content_content:
                                try:
                                    char = novel543_decrypt[str(ord(index))]
                                    result.append(char)
                                except KeyError:
                                    char = index
                                    result.append(char)
                                    
                            with open(export_path + "\\" + chapter_title_list[i] + ".txt", mode='a', encoding='utf8') as f:
                                for sentence in result:
                                    f.write(sentence)
                            
                        if i + 1 == len(chapter_title_list):
                            print_text("> 已讀取全部章節内容！")
                            root.spider_extract_button.configure(
                                text="提取文本", state="normal"
                            )
                            return None
                        else:
                            random_time = random.randint(100, 2000)
                            root.spider_main_container.after(
                                random_time, get_chapter_content, i + 1
                            )

        def txt_edit_page(root):
            root.txt_edit_page_main_container.grid(row=0, column=1, sticky="nsew")

        def cube_page(root):
            root.cube_page_main_container.grid(row=0, column=1, sticky="nsew")

        def setting_page(root):
            root.setting_page_main_container.grid(row=0, column=1, sticky="nsew")
            if not hasattr(root, "setting_page_main_container"):
                root.setting_page_main_container = ctk.CTkFrame(
                    root, fg_color="transparent", height=800, width=1350
                )
            if not hasattr(root, "setting_page_title_lable"):
                root.setting_page_title_lable = ctk.CTkLabel(
                    root.setting_page_main_container,
                    text=" 設定：",
                    font=(font_family, 50, "bold"),
                    height=70
                )
            if not hasattr(root, "setting_page_ask_spider_dir_lable"):
                root.setting_page_ask_spider_dir_lable = ctk.CTkLabel(
                    root.setting_page_main_container,
                    text="【網絡小説爬取器】文件儲存路徑：",
                    font=(font_family, 23, "normal"),
                )
            if not hasattr(root, "setting_page_ask_spider_dir_entry"):
                root.setting_page_ask_spider_dir_entry = ctk.CTkEntry(
                    root.setting_page_main_container,
                    placeholder_text="目前路徑：" + txt_export_path,
                    font=(font_family, 20),
                    width=900,
                    height=50,
                    corner_radius=15,
                    border_width=3,
                )
            if not hasattr(root, "setting_page_ask_spider_dir_button"):
                root.setting_page_ask_spider_dir_button = ctk.CTkButton(
                    root.setting_page_main_container,
                    text="修改路徑",
                    corner_radius=15,
                    fg_color="transparent",
                    border_width=3,
                    text_color=("gray10", "#DCE4EE"),
                    hover_color="#505050",
                    font=(font_family, 20),
                    height = 50
                )
            if not hasattr(root, "setting_page_ask_spider_dir_radio_button1"):
                root.setting_page_ask_spider_dir_radio_button1 = ctk.CTkRadioButton(
                    root.setting_page_main_container,
                    text=" 依據章節打包",
                    radiobutton_width = 40,
                    radiobutton_height = 40,
                    font=(font_family, 23, "normal"),
                    border_width_unchecked = 5,
                    border_width_checked = 7,
                    hover = False,
                    fg_color="#ebe8e8"
                )
            if not hasattr(root, "setting_page_ask_spider_dir_radio_button2"):
                root.setting_page_ask_spider_dir_radio_button2 = ctk.CTkRadioButton(
                    root.setting_page_main_container,
                    text=" 打包成單個TXT",
                    radiobutton_width = 40,
                    radiobutton_height = 40,
                    font=(font_family, 23, "normal"),
                    border_width_unchecked = 5,
                    border_width_checked = 7,
                    hover = False,
                    fg_color="#ebe8e8"
                )
            if not hasattr(root, "setting_page_ask_spider_dir_radio_button3"):
                root.setting_page_ask_spider_dir_radio_button3 = ctk.CTkRadioButton(
                    root.setting_page_main_container,
                    text=" 打包成多個TXT",
                    radiobutton_width = 40,
                    radiobutton_height = 40,
                    font=(font_family, 23, "normal"),
                    border_width_unchecked = 5,
                    border_width_checked = 7,
                    hover = False,
                    fg_color="#ebe8e8"
                )
            if not hasattr(root, "setting_page_ask_txt_dir_lable"):
                root.setting_page_ask_txt_dir_lable = ctk.CTkLabel(
                    root.setting_page_main_container,
                    text="【TXT整理&編輯器】文件儲存路徑：",
                    font=(font_family, 23, "normal"),
                )
            if not hasattr(root, "setting_page_ask_txt_dir_entry"):
                root.setting_page_ask_txt_dir_entry = ctk.CTkEntry(
                    root.setting_page_main_container,
                    placeholder_text="目前路徑：" + txt_export_path,
                    font=(font_family, 20),
                    width=900,
                    height=50,
                    corner_radius=15,
                    border_width=3,
                )
            if not hasattr(root, "setting_page_ask_txt_dir_button"):
                root.setting_page_ask_txt_dir_button = ctk.CTkButton(
                    root.setting_page_main_container,
                    text="修改路徑",
                    corner_radius=15,
                    fg_color="transparent",
                    border_width=3,
                    text_color=("gray10", "#DCE4EE"),
                    hover_color="#505050",
                    font=(font_family, 20),
                    height = 50
                )
                
            #root.setting_page_ask_spider_dir_button.configure(command="")
            
            root.setting_page_title_lable.grid(
                row=0, column=1, columnspan=2, padx=(40), pady=(55, 0), sticky="wn"
            )
            
            root.setting_page_ask_spider_dir_lable.grid(
                row=0, column=1, columnspan=2, padx=(50), pady=(160,0), sticky="wn"
            )
            root.setting_page_ask_spider_dir_entry.grid(
                row=0,
                column=1,
                columnspan=2,
                padx=(60,0),
                pady=(210,0),
                sticky="nw",
            )
            root.setting_page_ask_spider_dir_button.grid(
                row=0, column=1, padx=(970,30), pady=(210,0), sticky="nw"
            )
            root.setting_page_ask_spider_dir_radio_button1.grid(
                row=0, column=1, padx=(80,0), pady=(290,0), sticky="nw"
            )
            root.setting_page_ask_spider_dir_radio_button2.grid(
                row=0, column=1, padx=(310,0), pady=(290,0), sticky="nw"
            )
            root.setting_page_ask_spider_dir_radio_button3.grid(
                row=0, column=1, padx=(550,0), pady=(290,0), sticky="nw"
            )
            
            root.setting_page_ask_txt_dir_lable.grid(
                row=0, column=1, columnspan=2, padx=(50), pady=(360,0), sticky="wn"
            )
            root.setting_page_ask_txt_dir_entry.grid(
                row=0,
                column=1,
                columnspan=2,
                padx=(60,0),
                pady=(410,0),
                sticky="nw",
            )
            root.setting_page_ask_txt_dir_button.grid(
                row=0, column=1, padx=(970,30), pady=(410,0), sticky="nw"
            )

        root.spider_page_button.configure(
            command=lambda: switch_page("spider_page")
        )
        root.txt_edit_page_button.configure(
            command=lambda: switch_page("txt_edit_page")
        )
        root.cube_button.configure(
            command=lambda: switch_page("cube_page")
        )
        root.setting_button.configure(
            command=lambda: switch_page("setting_page")
        )
        spider_page(root) #default page


if __name__ == "__main__":
    app = App()
    app.mainloop()
