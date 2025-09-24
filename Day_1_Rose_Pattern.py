%%manim -qm -r 1080,1920 Day1RoseShort
# manim -pqh day1_rose_short.py Day1RoseShort
# For 1080x1920: manim -pqh -r 1080,1920 day1_rose_short.py Day1RoseShort

from manim import *
import numpy as np


# ------------ MOBILE / VERTICAL (9:16) ------------
config.pixel_width  = 1080
config.pixel_height = 1920
config.frame_rate   = 30
config.frame_width  = 9
config.frame_height = 16


class Day1RoseShort(Scene):
    """
    Total ~30.0s
      0.0–5.0s  : Title ribbon + Day 1 illustration
      5.0–8.0s  : Draw initial rose
      8.0–18.0s : Animate k from 0→10 (rose morphs)
      18.0–25.0s: Square → rotate/scale → morph to circle
      25.0–30.0s: Outro (See you on Day 2)
    """

    # --- helper: rose curve (based on your RosePattern idea) ---
    def rose_vmobj(self, k: float, R: float = 3.2, turns: float = 3*TAU, stroke_w: float = 6):
        def curve_fn(t):
            r = R * np.cos(k * t)
            return np.array([r*np.cos(t), r*np.sin(t), 0.0])
        rose = ParametricFunction(curve_fn, t_range=[0, turns], stroke_width=stroke_w)
        rose.set_color_by_gradient(BLUE, WHITE, BLUE)
        return rose

    def construct(self):
        # ------------------------- INTRO (0–5s) -------------------------
        ribbon = Rectangle(width=8.6, height=1.2, stroke_width=0,
                           fill_color=BLACK, fill_opacity=0.90).to_edge(UP)
        title  = Text("30-Day Manim Shorts Challenge", weight=BOLD).scale(0.6)
        title.move_to(ribbon.get_center())

        day_chip = RoundedRectangle(corner_radius=0.22, width=2.8, height=0.8,
                                    stroke_width=0, fill_opacity=1).set_color(GREY_E)
        day_txt  = Text("Day 1", weight=BOLD).scale(0.6)
        day_grp  = VGroup(day_chip, day_txt)
        day_txt.move_to(day_chip.get_center())
        day_grp.next_to(ribbon, DOWN, buff=0.35)

        # tiny rose icon as "illustration"
        tiny_k   = 4
        tiny_rose = self.rose_vmobj(k=tiny_k, R=0.7, turns=2*TAU, stroke_w=5)
        tiny_rose.next_to(day_grp, RIGHT, buff=0.35)

        self.play(  # 0.0–2.0s
            FadeIn(ribbon, shift=0.5*DOWN),
            Write(title),
            run_time=2.0
        )
        self.play(  # 2.0–3.5s
            FadeIn(day_chip, shift=0.3*UP),
            FadeIn(day_txt, shift=0.3*UP),
            run_time=1.5
        )
        self.play(Create(tiny_rose), run_time=1.3)  # 3.5–4.8s
        self.wait(0.2)  # 4.8–5.0s

        # ----------------------- ROSE (5–18s) -----------------------
        # 5.0–8.0s: draw initial rose
        k_tracker = ValueTracker(0.0)
        rose = always_redraw(lambda: self.rose_vmobj(k_tracker.get_value(), R=3.2, turns=3*TAU, stroke_w=6))
        rose.move_to(ORIGIN).shift(0.6*DOWN)  # keep nicely framed

        self.play(Create(rose), run_time=3.0)  # 5.0–8.0s

        # 8.0–18.0s: animate k from 0 → 10 (your AnimatingWithValueTracker idea)
        self.play(k_tracker.animate.set_value(10.0), run_time=10.0, rate_func=linear)

        # ------------------ DYNAMISM TO OBJECTS (18–25s) ------------------
        # Quick homage to your square→circle morph
        sq = Square(side_length=1.8).set_stroke(width=6).set_fill(TEAL, 0.5)
        sq.move_to(3.0*LEFT + 2.8*UP)

        self.play(FadeIn(sq), run_time=0.5)            # 18.0–18.5
        self.play(sq.animate.move_to(ORIGIN), run_time=1.0)     # 18.5–19.5
        self.play(Rotate(sq, angle=PI/4), run_time=0.8)         # 19.5–20.3
        self.play(sq.animate.scale(1.4), run_time=0.8)          # 20.3–21.1
        circle = Circle(radius=1.7).set_stroke(width=6).set_fill(RED, 0.5)
        self.play(Transform(sq, circle), run_time=3.9)          # 21.1–25.0

        # ---------------------------- OUTRO (25–30s) ----------------------------
        outro = VGroup(
            Text("See you on Day 2!", weight=BOLD).scale(0.9),
            Text("Like • Share • Subscribe").scale(0.55).set_color(GREY_B)
        ).arrange(DOWN, buff=0.35).to_edge(DOWN, buff=1.1)

        # Gently dim background content and show outro
        self.play(
            rose.animate.set_opacity(0.25),
            sq.animate.set_opacity(0.25),
            FadeIn(outro, shift=0.3*UP),
            run_time=1.5
        )  # 25.0–26.5

        # Subtle pulse on the outro text to finish cleanly
        self.play(
            Indicate(outro[0], scale_factor=1.05),
            run_time=1.5
        )  # 26.5–28.0
        self.wait(2.0)  # 28.0–30.0