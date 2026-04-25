import tkinter as tk
import threading
import asyncio
import ctypes
import os
import sys
import keyboard
from PIL import Image, ImageTk, ImageSequence, ImageDraw
from screeninfo import get_monitors
from winsdk.windows.media.control import GlobalSystemMediaTransportControlsSessionManager as MediaManager

try:
    ctypes.windll.shcore.SetProcessDpiAwareness(1)
except:
    pass

def resource_path(relative_path):
    try:
        base_path = sys._MEIPASS
    except Exception:
        base_path = os.path.abspath(".")
    return os.path.join(base_path, relative_path)

GIF_FILENAME = resource_path("frank.gif")

def send_media_key(code):
    ctypes.windll.user32.keybd_event(code, 0, 0, 0)
    ctypes.windll.user32.keybd_event(code, 0, 2, 0)

def create_rounded_rectangle(width, height, radius, color):
    scale = 4
    img = Image.new("RGBA", (width * scale, height * scale), (0, 0, 0, 0))
    draw = ImageDraw.Draw(img)
    draw.rounded_rectangle([0, 0, width * scale - 1, height * scale - 1], 
                           radius=radius * scale, fill=color)
    return img.resize((width, height), Image.Resampling.LANCZOS)

class YandexMusicWidget:
    def __init__(self, root):
        self.root = root
        self.root.title("YM Widget")
        

        self.MONITOR_INDEX = 1 
        self.width, self.height = 280, 150
        self.radius = 22
        self.TEXT_START_X = 98     
        self.CONTAINER_WIDTH = 170 
        self.TEXT_SPEED = 0.61     

        try:
            monitors = get_monitors()
            m = monitors[self.MONITOR_INDEX] if len(monitors) > self.MONITOR_INDEX else monitors[0]
            self.screen_x, self.screen_y = m.x, m.y
            self.screen_w, self.screen_h = m.width, m.height
        except:
            self.screen_x, self.screen_y, self.screen_w, self.screen_h = 0, 0, 1920, 1080

        self.fixed_x = self.screen_x + self.screen_w - self.width
        self.current_y = self.screen_y + 250

        self.root.geometry(f"{self.width}x{self.height}+{self.fixed_x}+{self.current_y}")
        self.root.overrideredirect(True)
        self.root.attributes("-topmost", True, "-alpha", 0.98)
        self.root.configure(bg="#010101")
        self.root.wm_attributes("-transparentcolor", "#010101")

        self.is_visible = True
        self.is_playing = False
        
        self.anim_data = {
            'title':  {'x': self.TEXT_START_X, 'dir': -1, 'wait': 0, 'width': 0, 'y': 38},
            'artist': {'x': self.TEXT_START_X, 'dir': -1, 'wait': 0, 'width': 0, 'y': 62}
        }

        self.frank_frames = []
        self.current_frame = 0
        self._load_gif()
        self._build_ui()

        keyboard.add_hotkey('alt+shift+s', self.toggle_visibility)
        self.main_canvas.bind('<Button-1>', self.start_move)
        self.main_canvas.bind('<B1-Motion>', self.do_move)

        self.running = True
        threading.Thread(target=self.start_async_loop, daemon=True).start()
        self.main_loop()

    def _load_gif(self):
        if os.path.exists(GIF_FILENAME):
            with Image.open(GIF_FILENAME) as im:
                for frame in ImageSequence.Iterator(im):
                    resized = frame.resize((68, 68), Image.Resampling.LANCZOS)
                    self.frank_frames.append(ImageTk.PhotoImage(resized.convert('RGBA')))

    def _build_ui(self):
        self.main_canvas = tk.Canvas(self.root, width=self.width, height=self.height,
                                     bg="#010101", highlightthickness=0)
        self.main_canvas.place(x=0, y=0)

        self.bg_img = ImageTk.PhotoImage(create_rounded_rectangle(self.width, self.height, self.radius, "#141414"))
        self.main_canvas.create_image(0, 0, image=self.bg_img, anchor="nw")

        self.title_id = self.main_canvas.create_text(self.TEXT_START_X, 38, text="...", fill="white", 
                                                     font=("Segoe UI Semibold", 11), anchor="w")
        self.artist_id = self.main_canvas.create_text(self.TEXT_START_X, 62, text="...", fill="#888888", 
                                                      font=("Segoe UI", 10), anchor="w")

        mask_w = self.TEXT_START_X
        self.mask_img = ImageTk.PhotoImage(create_rounded_rectangle(mask_w, self.height - 10, 0, "#141414"))
        self.main_canvas.create_image(0, 5, image=self.mask_img, anchor="nw")

        if self.frank_frames:
            self.frank_id = self.main_canvas.create_image(15, 23, image=self.frank_frames[0], anchor="nw")

        close_btn = self.main_canvas.create_text(self.width-18, 18, text="✕", fill="#444444", font=("Arial", 10))
        self.main_canvas.tag_bind(close_btn, "<Button-1>", lambda e: self.root.destroy())

        for txt, code, x in [("⏮", 0xB1, 85), ("⏯", 0xB3, 145), ("⏭", 0xB0, 205)]:
            color = "#FF3333" if txt == "⏯" else "#AAAAAA"
            f_size = 20 if txt == "⏯" else 16
            btn = self.main_canvas.create_text(x, 115, text=txt, fill=color, font=("Segoe UI", f_size))
            self.main_canvas.tag_bind(btn, "<Button-1>", lambda e, c=code: send_media_key(c))

    def _scroll_logic(self, key, item_id):
        d = self.anim_data[key]
        if d['width'] > self.CONTAINER_WIDTH:
            if d['wait'] > 0:
                d['wait'] -= 1
                return
            
            d['x'] += (self.TEXT_SPEED * d['dir'])
            limit = self.TEXT_START_X - (d['width'] - self.CONTAINER_WIDTH + 15)

            if d['x'] <= limit:
                d['x'] = limit
                d['dir'] = 1
                d['wait'] = 55 
            elif d['x'] >= self.TEXT_START_X:
                d['x'] = self.TEXT_START_X
                d['dir'] = -1
                d['wait'] = 55
            
            self.main_canvas.coords(item_id, d['x'], d['y'])

    def main_loop(self):
        if self.is_visible:
            if self.is_playing and self.frank_frames:
                self.current_frame = (self.current_frame + 1) % len(self.frank_frames)
                self.main_canvas.itemconfig(self.frank_id, image=self.frank_frames[self.current_frame])
            
            self._scroll_logic('title', self.title_id)
            self._scroll_logic('artist', self.artist_id)
        self.root.after(30, self.main_loop)

    def update_canvas_text(self, title, artist):
        self.main_canvas.itemconfig(self.title_id, text=title)
        self.main_canvas.itemconfig(self.artist_id, text=artist)
        for key, item in [('title', self.title_id), ('artist', self.artist_id)]:
            self.anim_data[key]['x'] = self.TEXT_START_X
            self.anim_data[key]['dir'] = -1
            self.anim_data[key]['wait'] = 30
            bbox = self.main_canvas.bbox(item)
            self.anim_data[key]['width'] = bbox[2] - bbox[0] if bbox else 0
            self.main_canvas.coords(item, self.TEXT_START_X, self.anim_data[key]['y'])

    def toggle_visibility(self):
        if self.is_visible: self.root.withdraw()
        else: self.root.deiconify(); self.root.attributes("-topmost", True)
        self.is_visible = not self.is_visible

    def start_move(self, event):
        self._offsety = event.y

    def do_move(self, event):
        new_y = self.root.winfo_y() + event.y - self._offsety
        if new_y < self.screen_y: new_y = self.screen_y
        if new_y > self.screen_y + self.screen_h - self.height: new_y = self.screen_y + self.screen_h - self.height
        self.root.geometry(f"+{self.fixed_x}+{new_y}")

    async def update_data(self):
        last_t, last_a = "", ""
        while self.running:
            try:
                sm = await MediaManager.request_async()
                curr = sm.get_current_session()
                if curr:
                    self.is_playing = (curr.get_playback_info().playback_status == 4)
                    p = await curr.try_get_media_properties_async()
                    if p.title != last_t or p.artist != last_a:
                        last_t, last_a = p.title, p.artist
                        self.root.after(0, self.update_canvas_text, p.title, p.artist)
                else: self.is_playing = False
            except: pass
            await asyncio.sleep(1.0)

    def start_async_loop(self):
        loop = asyncio.new_event_loop()
        asyncio.set_event_loop(loop)
        loop.run_until_complete(self.update_data())

if __name__ == "__main__":
    root = tk.Tk()
    app = YandexMusicWidget(root)
    root.mainloop()