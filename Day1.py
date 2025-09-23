%%manim -qm --renderer=cairo -r 1080,1920 Manim30DayChallengeIntro
from manim import *
import numpy as np

# ----------------- MOBILE / VERTICAL (9:16) -----------------
config.pixel_width = 1080
config.pixel_height = 1920
config.frame_rate = 30
config.frame_width = 9
config.frame_height = 16

# ----------------- SCENE -----------------
class Manim30DayChallengeIntro(Scene):
    """
    A simple, punchy 30-second vertical intro for a 30‑Day Manim Shorts Challenge.
    Flow (~30s):
      1) Title ribbon (2.0s)
      2) What you'll build (bullets pop) (8.5s)
      3) 30-day grid fills (12.0s)
      4) Rules + CTA (7.0s)
      5) Final hold (0.5s)
    """
    def construct(self):
        # --------- Top ribbon (Title) ---------
        ribbon = Rectangle(width=8.6, height=1.2, fill_opacity=0.9, fill_color=BLACK, stroke_width=0)
        ribbon.to_edge(UP, buff=0.4)
        title = Text("30-Day Manim Shorts Challenge", font_size=40, weight=MEDIUM)
        title.move_to(ribbon.get_center())
        subtitle = Text("Learn high-end animations • 30 sec a day", font_size=28)
        subtitle.next_to(ribbon, DOWN, buff=0.12)
        self.play(FadeIn(ribbon, run_time=0.5), Write(title, run_time=1.0))  # 1.5s
        self.play(FadeIn(subtitle, run_time=0.5))  # 0.5s (→ 2.0s)

        # --------- What you'll build (bullets) ---------
        bullets = VGroup(
            Text("Day themes: vectors · paths · graphs", font_size=34),
            Text("Fourier & epicycles · param plots", font_size=34),
            Text("Physics touches · camera moves", font_size=34),
            Text("Logo morphs · data viz basics", font_size=34),
        )
        bullets.arrange(DOWN, aligned_edge=LEFT, buff=0.22)
        bullets.move_to(UP*2.7)

        # pop bullets one by one
        for i, line in enumerate(bullets):
            line.set_opacity(0)
            self.play(FadeIn(line, shift=UP*0.1), run_time=0.8)
        # quick sweep accent underlines
        accents = VGroup()
        for line in bullets:
            underline = Line(line.get_left()+DOWN*0.22, line.get_right()+DOWN*0.22).set_stroke(GRAY_D, 4)
            accents.add(underline)
        self.play(LaggedStart(*[Create(u) for u in accents], lag_ratio=0.2, run_time=1.2))  # (~8.5s total so far)

        # --------- Calendar grid (30 day fill) ---------
        cols, rows = 6, 5  # 6x5 = 30
        size = 0.85
        grid = VGroup()
        day_labels = VGroup()
        n = 1
        for r in range(rows):
            row = VGroup()
            for c in range(cols):
                cell = RoundedRectangle(corner_radius=0.12, width=size, height=size)
                cell.set_fill(GRAY_E, opacity=1).set_stroke(width=0)
                num = Text(str(n), font_size=28, weight=MEDIUM).set_color(GRAY_B)
                num.move_to(cell.get_center())
                grp = VGroup(cell, num)
                row.add(grp)
                day_labels.add(num)
                n += 1
            row.arrange(RIGHT, buff=0.16)
            grid.add(row)
        grid.arrange(DOWN, buff=0.16)
        grid.move_to(DOWN*0.8)

        self.play(FadeIn(grid, scale=0.98), run_time=0.6)

        # fill cells in waves to suggest daily progress
        palette = [TEAL_A, BLUE_A, PURPLE_A, YELLOW_A]
        fills = []
        idx = 0
        for r in range(rows):
            for c in range(cols):
                cell = grid[r][c][0]
                num = grid[r][c][1]
                fills.append(AnimationGroup(
                    cell.animate.set_fill(palette[(idx // 3) % len(palette)]),
                    num.animate.set_color(WHITE),
                    lag_ratio=0.0,
                ))
                idx += 1
        # 30 cells → play in chunks for timing control
        chunk = 6  # 5 chunks * 0.8s ≈ 4.0s + earlier 8.5 + 0.6 ≈ 13.1s; add more waves below
        k = 0
        while k < len(fills):
            self.play(LaggedStart(*fills[k:k+chunk], lag_ratio=0.05, run_time=0.8))
            k += chunk
        # orbit highlight around today cell (use last one as example)
        halo = Circle(radius=size*0.65).set_stroke(WHITE, 4)
        halo.move_to(grid[-1][-1].get_center())
        self.play(Create(halo), run_time=0.4)
        self.play(Rotate(halo, angle=TAU/2), run_time=0.8, rate_func=linear)
        self.play(FadeOut(halo), run_time=0.2)
        # (Grid section ~12.0s)

        # --------- Rules + CTA ---------
        rules = VGroup(
            Text("Rules:", font_size=36, weight=MEDIUM),
            Text("• 30s max per day", font_size=32),
            Text("• Post daily for 30 days", font_size=32),
            Text("• Use hashtag #Manim30Shorts", font_size=32),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.18)
        rules.next_to(grid, UP, buff=0.5)
        self.play(FadeIn(rules), run_time=0.8)

        cta = VGroup(
            Text("Day 1 drops tomorrow", font_size=36, weight=MEDIUM),
            Text("Follow + Save to join", font_size=34),
        ).arrange(DOWN, buff=0.12)
        cta.to_edge(DOWN, buff=0.7)
        self.play(GrowFromCenter(cta), run_time=0.6)

        # quick pulse to end
        self.play(cta.animate.scale(1.05), run_time=0.3, rate_func=there_and_back)
        self.wait(0.6)  # final hold

# ----------------- RENDER -----------------
# Quick preview (Cairo renderer is stable):
# manim -pqm --renderer=cairo -r 1080,1920 manim_30day_challenge_intro.py Manim30DayChallengeIntro
# High quality:
# manim -pqh --renderer=cairo -r 1080,1920 manim_30day_challenge_intro.py Manim30DayChallengeIntro
