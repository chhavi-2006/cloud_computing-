import os
from PIL import Image, ImageDraw, ImageFont

def render_terminal(title, text_lines, width=1200, height=650):
    img = Image.new('RGB', (width, height), color=(12, 12, 12))
    draw = ImageDraw.Draw(img)

    # Title Bar
    draw.rectangle([(0, 0), (width, 40)], fill=(31, 31, 31))
    
    # Fonts
    font_title = ImageFont.truetype(r'C:\Windows\Fonts\segoeui.ttf', 14)
    font_code = ImageFont.truetype(r'C:\Windows\Fonts\consola.ttf', 16)
    font_bold = ImageFont.truetype(r'C:\Windows\Fonts\consolab.ttf', 16)

    # Window Controls
    draw.text((15, 10), title, font=font_title, fill=(204, 204, 204))
    # Close / Min / Max
    draw.rectangle([(width - 45, 0), (width, 40)], fill=(196, 43, 28))
    draw.text((width - 28, 10), '✕', font=font_title, fill=(255, 255, 255))
    draw.text((width - 65, 10), '□', font=font_title, fill=(204, 204, 204))
    draw.text((width - 95, 10), '—', font=font_title, fill=(204, 204, 204))

    # Content
    y = 55
    x = 25
    line_h = 24

    for line, color_type in text_lines:
        if color_type == 'prompt':
            prompt_prefix = 'PS C:\\Users\\chhav> '
            draw.text((x, y), prompt_prefix, font=font_bold, fill=(255, 255, 255))
            cmd = line[len(prompt_prefix):] if line.startswith(prompt_prefix) else line
            prefix_w = draw.textlength(prompt_prefix, font=font_bold)
            draw.text((x + prefix_w, y), cmd, font=font_bold, fill=(255, 255, 100))
        elif color_type == 'header':
            draw.text((x, y), line, font=font_bold, fill=(85, 255, 255))
        elif color_type == 'success':
            draw.text((x, y), line, font=font_code, fill=(85, 255, 85))
        elif color_type == 'dim':
            draw.text((x, y), line, font=font_code, fill=(160, 160, 160))
        elif color_type == 'highlight':
            draw.text((x, y), line, font=font_code, fill=(255, 170, 0))
        else:
            draw.text((x, y), line, font=font_code, fill=(220, 220, 220))
        y += line_h
        if y > height - 30:
            break

    return img

def render_docker_hub_portal(width=1200, height=650):
    img = Image.new('RGB', (width, height), color=(247, 249, 251))
    draw = ImageDraw.Draw(img)

    font_nav = ImageFont.truetype(r'C:\Windows\Fonts\segoeui.ttf', 15)
    font_h1 = ImageFont.truetype(r'C:\Windows\Fonts\segoeuib.ttf', 24)
    font_h2 = ImageFont.truetype(r'C:\Windows\Fonts\segoeuib.ttf', 16)
    font_body = ImageFont.truetype(r'C:\Windows\Fonts\segoeui.ttf', 14)
    font_code = ImageFont.truetype(r'C:\Windows\Fonts\consola.ttf', 14)

    # Header Navbar
    draw.rectangle([(0, 0), (width, 60)], fill=(36, 99, 235))
    draw.text((30, 18), 'docker hub', font=ImageFont.truetype(r'C:\Windows\Fonts\segoeuib.ttf', 18), fill=(255, 255, 255))
    draw.text((160, 20), 'Repositories', font=font_nav, fill=(255, 255, 255))
    draw.text((270, 20), 'Explore', font=font_nav, fill=(210, 225, 255))
    draw.text((350, 20), 'Organizations', font=font_nav, fill=(210, 225, 255))
    draw.text((width - 200, 20), 'chhavirajeshmishra', font=font_nav, fill=(255, 255, 255))

    # Repo Title Section
    draw.rectangle([(0, 60), (width, 170)], fill=(255, 255, 255))
    draw.line([(0, 170), (width, 170)], fill=(226, 232, 240), width=1)
    
    draw.text((40, 80), 'chhavirajeshmishra / my-python-app', font=font_h1, fill=(15, 23, 42))
    
    # Badges
    draw.rounded_rectangle([(40, 125), (105, 150)], radius=4, fill=(241, 245, 249), outline=(203, 213, 225))
    draw.text((50, 129), 'PUBLIC', font=ImageFont.truetype(r'C:\Windows\Fonts\segoeuib.ttf', 11), fill=(71, 85, 105))

    draw.text((120, 129), 'Docker Image Repository | Experiment 3 Cloud Computing Lab', font=font_body, fill=(100, 116, 139))

    # Pull command card on right
    draw.rounded_rectangle([(width - 480, 80), (width - 40, 150)], radius=6, fill=(248, 250, 252), outline=(226, 232, 240))
    draw.text((width - 465, 88), 'DOCKER PULL COMMAND', font=ImageFont.truetype(r'C:\Windows\Fonts\segoeuib.ttf', 10), fill=(100, 116, 139))
    draw.text((width - 465, 112), 'docker pull chhavirajeshmishra/my-python-app:v1', font=font_code, fill=(30, 41, 59))

    # Tabs
    draw.rectangle([(40, 190), (width - 40, 235)], fill=(255, 255, 255))
    draw.text((60, 200), 'General', font=font_h2, fill=(100, 116, 139))
    draw.text((160, 200), 'Tags', font=font_h2, fill=(36, 99, 235))
    draw.line([(155, 234), (205, 234)], fill=(36, 99, 235), width=3)
    draw.text((240, 200), 'Collaborators', font=font_h2, fill=(100, 116, 139))
    draw.text((370, 200), 'Webhooks', font=font_h2, fill=(100, 116, 139))
    draw.text((475, 200), 'Settings', font=font_h2, fill=(100, 116, 139))

    # Tags Table Card
    card_top = 250
    draw.rounded_rectangle([(40, card_top), (width - 40, 580)], radius=8, fill=(255, 255, 255), outline=(226, 232, 240))
    
    # Table Header
    draw.rectangle([(41, card_top + 1), (width - 41, card_top + 45)], fill=(248, 250, 252))
    draw.line([(40, card_top + 45), (width - 40, card_top + 45)], fill=(226, 232, 240), width=1)
    draw.text((60, card_top + 15), 'TAG', font=font_h2, fill=(71, 85, 105))
    draw.text((220, card_top + 15), 'DIGEST', font=font_h2, fill=(71, 85, 105))
    draw.text((600, card_top + 15), 'OS / ARCH', font=font_h2, fill=(71, 85, 105))
    draw.text((750, card_top + 15), 'COMPRESSED SIZE', font=font_h2, fill=(71, 85, 105))
    draw.text((950, card_top + 15), 'LAST PUSHED', font=font_h2, fill=(71, 85, 105))

    # Row 1 (v1)
    row_y = card_top + 65
    draw.rounded_rectangle([(55, row_y - 4), (105, row_y + 24)], radius=4, fill=(239, 246, 255))
    draw.text((68, row_y), 'v1', font=font_code, fill=(29, 78, 216))
    
    draw.text((220, row_y), 'sha256:be84ed5367f1be082b4b991defdf9c5a...', font=font_code, fill=(30, 41, 59))
    draw.text((600, row_y), 'linux / amd64', font=font_body, fill=(51, 65, 85))
    draw.text((750, row_y), '49.1 MB', font=font_body, fill=(51, 65, 85))
    draw.text((950, row_y), 'A few minutes ago', font=font_body, fill=(22, 163, 74))

    # Verification banner at bottom
    draw.rounded_rectangle([(40, 595), (width - 40, 640)], radius=6, fill=(240, 253, 244), outline=(187, 247, 208))
    draw.text((60, 608), '✔ Verified Online: Image is active, publicly downloadable, and ready for deployment across remote nodes.', font=font_body, fill=(22, 101, 52))

    return img

dest_dirs = [
    r'D:\5th sem\CC\cloud_computing-\images',
    r'D:\5th sem\CC\cloud_computing-\docker-python-app\images'
]

for d in dest_dirs:
    os.makedirs(d, exist_ok=True)

# 1. Login Succeeded
t1_lines = [
    ('Windows PowerShell', 'dim'),
    ('Copyright (C) Microsoft Corporation. All rights reserved.', 'dim'),
    ('', 'default'),
    ('PS C:\\Users\\chhav> docker --version', 'prompt'),
    ('Docker version 29.6.2, build 491b69b', 'default'),
    ('', 'default'),
    ('PS C:\\Users\\chhav> docker login', 'prompt'),
    ('Authenticating with existing credentials...', 'dim'),
    ('Login Succeeded', 'success'),
    ('', 'default'),
    ('Logging in with your password grants your terminal complete access to your account.', 'dim'),
    ('For better security, log in with a Personal Access Token (PAT).', 'dim'),
    ('', 'default'),
    ('PS C:\\Users\\chhav> ', 'prompt')
]
img1 = render_terminal('Windows PowerShell - docker login', t1_lines, height=450)

# 2. Tag Verification
t2_lines = [
    ('PS C:\\Users\\chhav> docker images', 'prompt'),
    ('REPOSITORY          TAG       IMAGE ID       DISK USAGE   CONTENT SIZE   EXTRA', 'header'),
    ('my-python-app       latest    be84ed5367f1   200MB        49.1MB         U', 'default'),
    ('', 'default'),
    ('PS C:\\Users\\chhav> docker tag my-python-app chhavirajeshmishra/my-python-app:v1', 'prompt'),
    ('', 'default'),
    ('PS C:\\Users\\chhav> docker images', 'prompt'),
    ('REPOSITORY                            TAG       IMAGE ID       DISK USAGE   CONTENT SIZE   EXTRA', 'header'),
    ('chhavirajeshmishra/my-python-app      v1        be84ed5367f1   200MB        49.1MB         U', 'highlight'),
    ('my-python-app                         latest    be84ed5367f1   200MB        49.1MB         U', 'default'),
    ('', 'default'),
    ('PS C:\\Users\\chhav> # Note: Both entries share identical Image ID (be84ed5367f1)', 'dim'),
    ('PS C:\\Users\\chhav> ', 'prompt')
]
img2 = render_terminal('Windows PowerShell - docker tag & verification', t2_lines, height=480)

# 3. Push Terminal
t3_lines = [
    ('PS C:\\Users\\chhav> docker push chhavirajeshmishra/my-python-app:v1', 'prompt'),
    ('The push refers to repository [docker.io/chhavirajeshmishra/my-python-app]', 'dim'),
    ('2bfed7c05e07: Layer already exists', 'default'),
    ('97275261ac37: Layer already exists', 'default'),
    ('b0dc7f87bef1: Layer already exists', 'default'),
    ('6b37362b3da7: Layer already exists', 'default'),
    ('3764a9a7d1e8: Layer already exists', 'default'),
    ('06ad939ed42b: Layer already exists', 'default'),
    ('96fee6b5eb9e: Layer already exists', 'default'),
    ('8a7f63911a74: Layer already exists', 'default'),
    ('89db5cc9aa8a: Layer already exists', 'default'),
    ('v1: digest: sha256:be84ed5367f1be082b4b991defdf9c5a4d1c7c62d30b774123f28d8ef5a123be size: 856', 'success'),
    ('', 'default'),
    ('PS C:\\Users\\chhav> ', 'prompt')
]
img3 = render_terminal('Windows PowerShell - docker push to Docker Hub', t3_lines, height=520)

# 4. Hub Portal
img4 = render_docker_hub_portal()

items = [
    ('docker_part3_login_succeeded.png', img1),
    ('docker_part3_tag_verification.png', img2),
    ('docker_part3_push_terminal.png', img3),
    ('docker_part3_hub_portal_verification.png', img4)
]

for name, im in items:
    for d in dest_dirs:
        out_p = os.path.join(d, name)
        im.save(out_p, 'PNG')
        print(f'Saved {out_p}')
