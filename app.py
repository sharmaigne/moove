import wx
import cv2
import numpy as np
from datetime import datetime, timedelta

from pose_detector import *
from rep_counter import RepCounter


class MainFrame(wx.Frame):
    def __init__(self):
        super().__init__(parent=None, title="Moooove")
        self.SetSize(800, 600)

        self.panel = wx.Panel(self)
        self.panel.Bind(wx.EVT_SIZE, self.on_panel_resize)

        # Video display
        self.bmp = wx.StaticBitmap(self.panel)

        # Exercise choice dropdown
        exercise_choices = ["Squats", "Jumping Jacks"]
        self.exercise_choice = wx.Choice(self.panel, choices=exercise_choices)
        self.exercise_choice.SetSelection(0)  # default to Squats
        self.rep_counter = RepCounter( "Squats")  # default

        # Webcam capture
        self.cap = None
        self.show_camera = False

        # Timers
        self.frame_timer = wx.Timer(self)
        self.Bind(wx.EVT_TIMER, self.on_next_frame, self.frame_timer)

        self.countdown = wx.Timer(self)  # 3 second countdown
        self.Bind(wx.EVT_TIMER, self.on_countdown, self.countdown)

        self.timer = wx.Timer(self)  # 60-second session timer
        self.Bind(wx.EVT_TIMER, self.on_timer, self.timer)

        # Buttons
        self.start_btn = wx.Button(self.panel, label="Start 1-minute Session")
        self.stop_btn = wx.Button(self.panel, label="Stop Session")
        self.stop_btn.Disable()  # initially disabled

        self.start_btn.Bind(wx.EVT_BUTTON, self.on_start)
        self.stop_btn.Bind(wx.EVT_BUTTON, self.on_stop)

        # Timer label
        self.timer_label = wx.StaticText(
            self.panel, label="Time Remaining: 60 sec", style=wx.ALIGN_CENTER
        )
        font = self.timer_label.GetFont()
        font.PointSize += 8
        self.timer_label.SetFont(font)

        # Countdown before timer starts
        self.countdown_label = wx.StaticText(
            self.panel, label="", style=wx.ALIGN_CENTER
        )
        countdown_font = self.countdown_label.GetFont()
        countdown_font.PointSize += 100  # BIG
        self.countdown_label.SetFont(countdown_font)
        self.countdown_label.Hide()  # hidden by default

        # Rep count label
        self.rep_label = wx.StaticText(
            self.panel, label="Reps: 0", style=wx.ALIGN_CENTER
        )
        font2 = self.rep_label.GetFont()
        font2.PointSize += 10
        self.rep_label.SetFont(font2)

        # Layout
        btn_sizer = wx.BoxSizer(wx.HORIZONTAL)
        btn_sizer.Add(self.exercise_choice, 0, wx.ALIGN_CENTER | wx.TOP, 10)
        btn_sizer.Add(self.start_btn, 0, wx.ALL, 5)
        btn_sizer.Add(self.stop_btn, 0, wx.ALL, 5)

        main_sizer = wx.BoxSizer(wx.VERTICAL)
        main_sizer.Add(self.bmp, 1, wx.EXPAND | wx.ALL, 5)
        main_sizer.Add(self.timer_label, 0, wx.ALIGN_CENTER | wx.TOP, 5)
        main_sizer.Add(self.rep_label, 0, wx.ALIGN_CENTER | wx.TOP, 5)
        main_sizer.Add(btn_sizer, 0, wx.ALIGN_CENTER | wx.TOP, 10)

        self.panel.SetSizer(main_sizer)

        # overlay panel for countdown_label
        self.overlay_panel = wx.Panel(self.panel, style=wx.BG_STYLE_TRANSPARENT)
        self.overlay_panel.SetSize(self.panel.GetSize())
        self.overlay_panel.SetPosition((0, 0))
        self.overlay_panel.Enable(False)  # disables mouse handling, clicks go through
        self.countdown_label.Reparent(self.overlay_panel)

        # sizer for overlay panel and add the countdown_label centered
        overlay_sizer = wx.BoxSizer(wx.VERTICAL)
        overlay_sizer.AddStretchSpacer(1)
        overlay_sizer.Add(
            self.countdown_label, 1, wx.ALIGN_CENTER | wx.ALIGN_CENTER_VERTICAL
        )
        overlay_sizer.AddStretchSpacer(1)
        self.overlay_panel.SetSizer(overlay_sizer)
        self.overlay_panel.Layout()

        self.countdown_label.Show()

        # State variables
        self.is_running = False
        self.session_start = None
        self.session_duration = timedelta(seconds=60)

        self.countdown_value = 3  # 3 second pre-countdown

    def on_panel_resize(self, event):
        size = self.panel.GetSize()
        self.overlay_panel.SetSize(size)
        event.Skip()

    def on_start(self, event):
        # Disable start button immediately
        self.start_btn.Disable()
        self.stop_btn.Disable()  # disable stop during pre-countdown

        self.start_countdown()

    def start_countdown(self):
        self.countdown_value = 3
        self.countdown_label.SetLabel(str(self.countdown_value))
        self.countdown_label.Show()

        self.show_camera = True  # allow webcam to show
        if self.cap is None:
            self.cap = cv2.VideoCapture(0)

        self.frame_timer.Start(33)
        self.countdown.Start(1000)  # 3, 2, 1...

    def on_countdown(self, event):
        self.countdown_value -= 1
        if self.countdown_value > 0:
            self.countdown_label.SetLabel(str(self.countdown_value))
        else:
            self.countdown.Stop()
            self.countdown_label.Hide()
            self.start_session()

    def start_session(self):
        self.is_running = True
        self.session_start = datetime.now()
        selected_exercise = self.exercise_choice.GetStringSelection()
        self.rep_counter = RepCounter(selected_exercise)
        print(selected_exercise)
        self.rep_counter.reset()
        self.rep_label.SetLabel("Reps: 0")
        self.timer_label.SetLabel("Time Remaining: 60 sec")

        self.stop_btn.Enable()  # enable stop button now
        self.exercise_choice.Disable()  # don't allow changing mid countdown
        self.timer.Start(1000)

    def on_stop(self, event):
        self.end_session()

    def end_session(self):
        self.is_running = False
        self.frame_timer.Stop()
        self.timer.Stop()
        self.countdown.Stop()

        self.start_btn.Enable()
        self.exercise_choice.Enable()
        self.stop_btn.Disable()

        self.timer_label.SetLabel("Session stopped.")

        if self.cap.isOpened():
            self.cap.release()

    def on_timer(self, event):
        if not self.is_running or not self.session_start:
            return

        elapsed = datetime.now() - self.session_start
        remaining_sec = max(
            0, int(self.session_duration.total_seconds() - elapsed.total_seconds())
        )
        self.timer_label.SetLabel(f"Time Remaining: {remaining_sec} sec")

        if remaining_sec <= 0:
            self.end_session()
            wx.MessageBox(
                "Time's up! Well done!", "Session Complete", wx.OK | wx.ICON_INFORMATION
            )

    def on_next_frame(self, event):
        if not self.show_camera:
            return

        ret, frame_bgr = self.cap.read()
        if not ret:
            return

        frame_rgb = cv2.cvtColor(frame_bgr, cv2.COLOR_BGR2RGB)
        results, processed_img = process_frame(frame_rgb)

        if results.pose_landmarks:
            self.rep_counter.update(results.pose_landmarks)
            draw_landmarks(processed_img, results.pose_landmarks)

        height, width = processed_img.shape[:2]
        wx_img = wx.Image(width, height, processed_img.tobytes())
        self.bmp.SetBitmap(wx_img.ConvertToBitmap())

        self.rep_label.SetLabel(f"Reps: {self.rep_counter.get_count()}")

        self.panel.Refresh()

    def on_close(self, event):
        self.cap.release()
        self.Destroy()


if __name__ == "__main__":
    app = wx.App()
    frame = MainFrame()
    frame.Show()
    app.MainLoop()
