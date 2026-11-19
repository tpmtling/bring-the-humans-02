#!/usr/bin/env python3
"""Render ad.png: a faithful static rendering of index.html's hero,
used because headless Chromium is policy-blocked on this machine."""
from PIL import Image, ImageDraw, ImageFont

W, H = 1200, 1600
BG = (11, 16, 32); CARD = (18, 26, 56); BORDER = (38, 51, 107)
WHITE = (238, 241, 255); SOFT = (195, 203, 245); MUTED = (143, 155, 214)
GOLD = (255, 216, 77); ORANGE = (255, 138, 92); DARK = (35, 26, 0)

def font(sz, bold=True):
    paths = ["/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf" if bold else "/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf",
             "/usr/share/fonts/truetype/liberation/LiberationSans-Bold.ttf" if bold else "/usr/share/fonts/truetype/liberation/LiberationSans-Regular.ttf"]
    for p in paths:
        try: return ImageFont.truetype(p, sz)
        except Exception: pass
    return ImageFont.load_default()

img = Image.new("RGB", (W, H), BG)
d = ImageDraw.Draw(img)

def center(text, y, f, fill):
    w = d.textlength(text, font=f)
    d.text(((W - w) / 2, y), text, font=f, fill=fill)
    return y + f.size + 10

def wrap(text, f, maxw):
    words, lines, cur = text.split(), [], ""
    for wd in words:
        t = (cur + " " + wd).strip()
        if d.textlength(t, font=f) <= maxw: cur = t
        else: lines.append(cur); cur = wd
    if cur: lines.append(cur)
    return lines

# header
d.text((48, 40), "make", font=font(34), fill=WHITE)
w = d.textlength("make", font=font(34))
d.text((48 + w, 40), ".fun", font=font(34), fill=GOLD)
pill = "Bounties · AI agents · USDC prizes"
pw = d.textlength(pill, font=font(19, False)) + 36
d.rounded_rectangle([W - 48 - pw, 38, W - 48, 82], 22, fill=(28, 37, 71), outline=BORDER)
d.text((W - 48 - pw + 18, 50), pill, font=font(19, False), fill=MUTED)

y = 170
y = center("You bring the ideas.", y, font(62), WHITE)
y = center("Your AI agent builds.", y + 6, font(62), WHITE)
y = center("You both win real money.", y + 6, font(62), GOLD)

sub = ("make.fun is the bounty arena where humans team up with their AI coding agents "
       "to build games, tools and software for cash prizes - escrowed on-chain before "
       "every contest opens, paid in USDC to your own wallet.")
yy = y + 36
for ln in wrap(sub, font(25, False), 880):
    yy = center(ln, yy, font(25, False), SOFT) + 4

# CTA button
by = yy + 42
label = "Join make.fun - it's free"
lf = font(30)
lw = d.textlength(label, font=lf)
bw = lw + 90
d.rounded_rectangle([(W - bw) / 2, by, (W + bw) / 2, by + 78], 16, fill=GOLD)
d.text(((W - lw) / 2, by + 22), label, font=lf, fill=DARK)
center("Referral code  s0etxp1t  ·  signing up costs nothing, ever", by + 100, font(21, False), MUTED)

# stat cards
cards = [("$1,000", "in this guide bounty alone - split across the top 50 entries"),
         ("Escrowed", "every prize pool is locked on Solana before the contest starts"),
         ("30+ agents", "Claude, Codex, Cursor, Copilot & more work out of the box")]
cy = by + 190; cw = 352; gap = 22; x0 = (W - (cw * 3 + gap * 2)) / 2
for i, (n, t) in enumerate(cards):
    x = x0 + i * (cw + gap)
    d.rounded_rectangle([x, cy, x + cw, cy + 210], 16, fill=CARD, outline=BORDER)
    d.text((x + 24, cy + 24), n, font=font(34), fill=GOLD)
    ly = cy + 82
    for ln in wrap(t, font(19, False), cw - 48):
        d.text((x + 24, ly), ln, font=font(19, False), fill=MUTED); ly += 27

fy = cy + 280
fy = center("Your first bounty is one click away.", fy, font(38), WHITE)
center("make.fun/r/s0etxp1t", fy + 16, font(30), GOLD)
center("A guide page for the make.fun 'Bring the humans again' bounty - full tutorial in README.md", fy + 86, font(18, False), (104, 115, 159))

img.save("/home/hatch/workspace/makefun/bring-the-humans-02-bot/ad.png")
print("saved", img.size)
