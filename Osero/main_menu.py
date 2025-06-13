import tkinter as tk
from game import ReversiGame  # 直接クラスを使う

root = tk.Tk()
root.title("リバーシ メインメニュー")
root.geometry("400x650")

selected_mode = None
selected_ai_first = None
selected_ai_level = None
click_count = 0

button_refs = []

def highlight_button(btn):
    for b in button_refs:
        b.config(highlightbackground="SystemButtonFace", highlightthickness=0)
    btn.config(highlightbackground="red", highlightthickness=3)

def select_mode(mode):
    global selected_mode, selected_ai_first, selected_ai_level, click_count
    selected_mode = mode
    selected_ai_first = None
    selected_ai_level = None
    click_count = 0
    highlight_button(btn_ai if mode == "AI" else btn_player)
    hide_all_options()

    if mode == "AI":
        first_label.pack(pady=10)
        btn_ai_first.pack(pady=3)
        btn_player_first.pack(pady=3)
    elif mode == "Player":
        start_button.pack(pady=20)

def set_ai_first(is_ai_first):
    global selected_ai_first, click_count
    selected_ai_first = is_ai_first
    click_count = 0
    highlight_button(btn_ai_first if is_ai_first else btn_player_first)
    btn_easy.config(text="初心者モード", fg="black", command=handle_easy_click)

    reset_button_highlight([btn_easy, btn_medium, btn_hard, btn_oni])
    ai_level_label.pack(pady=10)
    btn_easy.pack(pady=2)
    btn_medium.pack(pady=2)
    btn_hard.pack(pady=2)
    btn_oni.pack(pady=2)
    start_button.pack_forget()

def select_ai_level(level, btn):
    global selected_ai_level
    selected_ai_level = level
    highlight_button(btn)
    start_button.pack(pady=20)

def handle_easy_click():
    global click_count, selected_ai_level
    click_count += 1

    if btn_easy.cget("text") == "初心者モード":
        if click_count >= 3:
            btn_easy.config(text="接待モード（隠し）", fg="red")
            click_count = 0
            selected_ai_level = 0
        else:
            selected_ai_level = 1
    else:
        if click_count >= 3:
            btn_easy.config(text="初心者モード", fg="black")
            click_count = 0
            selected_ai_level = 1
        else:
            selected_ai_level = 0

    highlight_button(btn_easy)
    start_button.pack(pady=20)

def reset_button_highlight(btn_list):
    for btn in btn_list:
        btn.config(highlightbackground="SystemButtonFace", highlightthickness=0)

def hide_all_options():
    first_label.pack_forget()
    btn_ai_first.pack_forget()
    btn_player_first.pack_forget()
    ai_level_label.pack_forget()
    btn_easy.pack_forget()
    btn_medium.pack_forget()
    btn_hard.pack_forget()
    btn_oni.pack_forget()
    start_button.pack_forget()

def launch_game():
    if selected_mode == "AI":
        if selected_ai_first is not None and selected_ai_level is not None:
            root.withdraw()
            game_window = tk.Toplevel()
            game_window.title("リバーシ - 対戦画面")
            game_window.geometry("640x720")
            ReversiGame(game_window, "AI", selected_ai_first, selected_ai_level)
            game_window.protocol("WM_DELETE_WINDOW", game_window.destroy)
            root.wait_window(game_window)
            root.deiconify()
    elif selected_mode == "Player":
        root.withdraw()
        game_window = tk.Toplevel()
        game_window.title("リバーシ - 対戦画面")
        game_window.geometry("640x720")
        ReversiGame(game_window, "Player", None, None)
        game_window.protocol("WM_DELETE_WINDOW", game_window.destroy)
        root.wait_window(game_window)
        root.deiconify()

# UI構築
title_label = tk.Label(root, text="リバーシ", font=("Arial", 20, "bold"))
title_label.pack(pady=20)

btn_ai = tk.Button(root, text="AIと対戦", width=20, font=("Arial", 12), command=lambda: select_mode("AI"))
btn_player = tk.Button(root, text="人と対戦", width=20, font=("Arial", 12), command=lambda: select_mode("Player"))
btn_ai.pack(pady=5)
btn_player.pack(pady=5)

first_label = tk.Label(root, text="先攻を選んでください", font=("Arial", 11))
btn_ai_first = tk.Button(root, text="AIが先攻", width=20, font=("Arial", 11), command=lambda: set_ai_first(True))
btn_player_first = tk.Button(root, text="あなたが先攻", width=20, font=("Arial", 11), command=lambda: set_ai_first(False))

ai_level_label = tk.Label(root, text="AIの強さを選んでください", font=("Arial", 11))
btn_easy = tk.Button(root, text="初心者モード", width=20, font=("Arial", 11), command=handle_easy_click)
btn_medium = tk.Button(root, text="中級者モード", width=20, font=("Arial", 11), command=lambda: select_ai_level(2, btn_medium))
btn_hard = tk.Button(root, text="上級者モード", width=20, font=("Arial", 11), command=lambda: select_ai_level(3, btn_hard))
btn_oni = tk.Button(root, text="鬼モード", width=20, font=("Arial", 11), command=lambda: select_ai_level(4, btn_oni))

start_button = tk.Button(root, text="ゲーム開始", width=20, font=("Arial", 13, "bold"), command=launch_game)

button_refs = [btn_ai, btn_player, btn_ai_first, btn_player_first, btn_easy, btn_medium, btn_hard, btn_oni]

root.mainloop()
