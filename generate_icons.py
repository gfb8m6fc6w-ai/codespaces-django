#!/usr/bin/env python3
"""
توليد أيقونات PNG لتطبيق 5A Diamond System Pro
يتم تشغيلها بـ: python3 generate_icons.py
"""

try:
    from PIL import Image, ImageDraw, ImageFont
except ImportError:
    print("⚠️ تثبيت المكتبة المطلوبة...")
    import subprocess
    subprocess.check_call(['pip', 'install', 'pillow'])
    from PIL import Image, ImageDraw, ImageFont

import os

# الألوان
PRIMARY_COLOR = (0, 102, 204)      # أزرق
ACCENT_COLOR = (0, 204, 102)       # أخضر
BACKGROUND = (10, 10, 10)          # أسود
TEXT_COLOR = (255, 255, 255)       # أبيض

# الأحجام المطلوبة
SIZES = [72, 96, 128, 144, 152, 167, 180, 192, 384, 512]

def create_icon(size):
    """إنشاء أيقونة بحجم محدد"""
    # إنشاء صورة
    img = Image.new('RGBA', (size, size), BACKGROUND)
    draw = ImageDraw.Draw(img)
    
    # رسم دائرة أزرق
    margin = int(size * 0.1)
    draw.ellipse(
        [margin, margin, size-margin, size-margin], 
        fill=PRIMARY_COLOR, 
        outline=ACCENT_COLOR, 
        width=max(1, int(size * 0.05))
    )
    
    # رسم "5A" في المنتصف
    text = "5A"
    font_size = int(size * 0.35)
    
    # محاولة استخدام خط جميل
    try:
        font = ImageFont.truetype("/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf", font_size)
    except:
        font = ImageFont.load_default()
    
    # حساب موضع النص
    bbox = draw.textbbox((0, 0), text, font=font)
    text_width = bbox[2] - bbox[0]
    text_height = bbox[3] - bbox[1]
    
    x = (size - text_width) // 2
    y = (size - text_height) // 2 - int(size * 0.05)
    
    # رسم النص
    draw.text((x, y), text, fill=TEXT_COLOR, font=font)
    
    return img

def generate_all_icons():
    """توليد جميع الأيقونات"""
    os.makedirs('icons', exist_ok=True)
    
    print("🔄 جاري توليد الأيقونات...")
    print("=" * 50)
    
    for size in SIZES:
        try:
            img = create_icon(size)
            filename = f'icons/icon-{size}x{size}.png'
            img.save(filename)
            print(f"✅ تم إنشاء: {filename}")
        except Exception as e:
            print(f"❌ خطأ في إنشاء icon-{size}x{size}.png: {e}")
    
    print("=" * 50)
    print("✨ تم إنشاء جميع الأيقونات بنجاح!")
    print(f"📁 تم حفظها في مجلد: ./icons/")

if __name__ == '__main__':
    generate_all_icons()
