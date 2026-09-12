import os
from kivy.core.text import LabelBase

# تسجيل خط أريال لدعم اللغة العربية
font_path = "C:/Windows/Fonts/arial.ttf"
if os.path.exists(font_path):
    LabelBase.register(name="Roboto", fn_regular=font_path)
# -*- coding: utf-8 -*-
"""
تطبيق عباد الشمس لتعلم الإنجليزية التخصصية (الطبية) للأندرويد
Sunflower Gamified English Learning App for Android (Medicine)
Programmed in Python using Kivy & KivyMD
Supports RTL Arabic Layout & Duolingo-style gamification
"""

import os
import json
import random
from kivy.app import App
from kivy.lang import Builder
from kivy.uix.screenmanager import ScreenManager, Screen, FadeTransition
from kivy.properties import NumericProperty, StringProperty, BooleanProperty, ListProperty, ObjectProperty
from kivy.core.text import LabelBase
from kivy.storage.jsonstore import JsonStore
from kivy.clock import Clock
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.button import Button
from kivy.uix.label import Label
from kivy.uix.popup import Popup

# Arabic reshaping imports for proper RTL display in Kivy
try:
    import arabic_reshaper
    from bidi.algorithm import get_display
    def ar(text):
        """Helper to properly reshape and render RTL Arabic text in Kivy"""
        if not text:
            return ""
        reshaped = arabic_reshaper.reshape(text)
        return get_display(reshaped)
except ImportError:
    def ar(text):
        # Fallback if libraries not yet installed
        return text

# Register Arabic font if available (falls back to Roboto)
# LabelBase.register(name="ArabicFont", fn_regular="Cairo-Regular.ttf")

KV_DESIGN = '''
#:import ar __main__.ar

<RegistrationScreen>:
    name: 'registration'
    canvas.before:
        Color:
            rgba: 0.98, 0.98, 0.99, 1
        Rectangle:
            pos: self.pos
            size: self.size

    BoxLayout:
        orientation: 'vertical'
        padding: [24, 40, 24, 30]
        spacing: 16

        # Mascot Header
        BoxLayout:
            size_hint_y: 0.35
            orientation: 'vertical'
            alignment: 'center'
            Label:
                text: "🌻"
                font_size: '72sp'
                size_hint_y: 0.5
            Label:
                text: ar("تطبيق عباد الشمس لتعلم الإنجليزية")
                font_size: '22sp'
                bold: True
                color: [0.47, 0.21, 0.06, 1]
                size_hint_y: 0.25
            Label:
                text: ar("اختر تخصصك المهني وابدأ رحلة التعلم التفاعلية")
                font_size: '14sp'
                color: [0.4, 0.4, 0.4, 1]
                size_hint_y: 0.25

        # Form fields
        BoxLayout:
            orientation: 'vertical'
            size_hint_y: 0.45
            spacing: 12

            Label:
                text: ar("الاسم الأول:")
                font_size: '14sp'
                color: [0.2, 0.2, 0.2, 1]
                halign: 'right'
                size_hint_y: 0.15

            TextInput:
                id: first_name_input
                hint_text: ar("أدخل اسمك الأول...")
                multiline: False
                size_hint_y: 0.2
                background_color: [1, 1, 1, 1]
                font_size: '16sp'

            Label:
                text: ar("اسم العائلة:")
                font_size: '14sp'
                color: [0.2, 0.2, 0.2, 1]
                halign: 'right'
                size_hint_y: 0.15

            TextInput:
                id: last_name_input
                hint_text: ar("أدخل اسم العائلة...")
                multiline: False
                size_hint_y: 0.2
                background_color: [1, 1, 1, 1]
                font_size: '16sp'

            Label:
                text: ar("اختر تخصصك المهني:")
                font_size: '14sp'
                color: [0.2, 0.2, 0.2, 1]
                halign: 'right'
                size_hint_y: 0.15

            # Specialization Selection Buttons
            BoxLayout:
                size_hint_y: 0.25
                spacing: 8
                Button:
                    text: ar("1. الطب 🩺")
                    background_normal: ''
                    background_color: [0.98, 0.75, 0.14, 1] if root.specialization == 'medicine' else [0.92, 0.92, 0.92, 1]
                    color: [0.47, 0.21, 0.06, 1] if root.specialization == 'medicine' else [0.3, 0.3, 0.3, 1]
                    bold: True
                    on_press: root.select_specialization('medicine')
                Button:
                    text: ar("2. الأعمال 💼")
                    background_normal: ''
                    background_color: [0.98, 0.75, 0.14, 1] if root.specialization == 'business' else [0.92, 0.92, 0.92, 1]
                    color: [0.47, 0.21, 0.06, 1] if root.specialization == 'business' else [0.3, 0.3, 0.3, 1]
                    on_press: root.select_specialization('business')
                Button:
                    text: ar("3. الحاسوب 💻")
                    background_normal: ''
                    background_color: [0.98, 0.75, 0.14, 1] if root.specialization == 'cs' else [0.92, 0.92, 0.92, 1]
                    color: [0.47, 0.21, 0.06, 1] if root.specialization == 'cs' else [0.3, 0.3, 0.3, 1]
                    on_press: root.select_specialization('cs')

        # Register button
        Button:
            text: ar("ابدأ التعلم الآن 🚀")
            size_hint_y: 0.12
            background_normal: ''
            background_color: [0.96, 0.62, 0.04, 1]
            color: [1, 1, 1, 1]
            font_size: '18sp'
            bold: True
            on_press: root.submit_registration()


<MainLearningScreen>:
    name: 'main_learning'
    canvas.before:
        Color:
            rgba: 0.99, 0.99, 1, 1
        Rectangle:
            pos: self.pos
            size: self.size

    BoxLayout:
        orientation: 'vertical'

        # Top Navigation Bar (Section 4)
        BoxLayout:
            size_hint_y: 0.1
            padding: [16, 8, 16, 8]
            canvas.before:
                Color:
                    rgba: 1, 1, 1, 1
                Rectangle:
                    pos: self.pos
                    size: self.size
                Color:
                    rgba: 0.95, 0.8, 0.2, 0.5
                Line:
                    points: [self.x, self.y, self.right, self.y]
                    width: 1.5

            # Left Side: Medicine Specialization Logo
            BoxLayout:
                size_hint_x: 0.3
                spacing: 4
                Label:
                    text: "🩺"
                    font_size: '22sp'
                Label:
                    text: ar("الطب")
                    bold: True
                    color: [0.08, 0.4, 0.75, 1]
                    font_size: '15sp'

            # Center: Consecutive Streak Flame Counter
            BoxLayout:
                size_hint_x: 0.4
                spacing: 4
                Label:
                    text: "🔥"
                    font_size: '22sp'
                Label:
                    text: str(root.streak)
                    bold: True
                    color: [0.9, 0.3, 0.05, 1]
                    font_size: '18sp'

            # Right Side: Golden Sunflower Coin Counter
            BoxLayout:
                size_hint_x: 0.3
                spacing: 4
                Label:
                    text: "🌻🪙"
                    font_size: '20sp'
                Label:
                    text: str(root.coins)
                    bold: True
                    color: [0.8, 0.5, 0.05, 1]
                    font_size: '18sp'

        # Mascot Characters & Winding Progression Path (Section 5)
        ScrollView:
            size_hint_y: 0.9
            do_scroll_x: False

            BoxLayout:
                orientation: 'vertical'
                size_hint_y: None
                height: dp(820)
                padding: [20, 20, 20, 30]
                spacing: 18

                # Top Mascot: Sunflower reading book & Sunflower with telescope
                BoxLayout:
                    size_hint_y: None
                    height: dp(110)
                    spacing: 16

                    BoxLayout:
                        orientation: 'vertical'
                        Label:
                            text: "🌻📖"
                            font_size: '42sp'
                        Label:
                            text: ar("عباد الشمس القارئ")
                            font_size: '12sp'
                            color: [0.47, 0.21, 0.06, 1]
                            bold: True

                    BoxLayout:
                        orientation: 'vertical'
                        Label:
                            text: "🔭✨"
                            font_size: '42sp'
                        Label:
                            text: ar("راصد النجوم")
                            font_size: '12sp'
                            color: [0.1, 0.4, 0.7, 1]
                            bold: True

                # Stage 1 Button (Circular Yellow Stage)
                BoxLayout:
                    size_hint_y: None
                    height: dp(90)
                    padding: [40, 0, 40, 0]
                    Button:
                        text: ar("المرحلة 1: أساسيات الإنجليزية الطبية 🩺\\n") + ("★" * root.stage1_stars + "☆" * (3 - root.stage1_stars))
                        background_normal: ''
                        background_color: [0.98, 0.75, 0.14, 1]
                        color: [0.47, 0.21, 0.06, 1]
                        bold: True
                        font_size: '15sp'
                        on_press: root.open_stage(1)

                # Connecting Path Indicator
                Label:
                    text: "⬇ ⬇ ⬇"
                    color: [0.98, 0.75, 0.14, 0.8]
                    size_hint_y: None
                    height: dp(24)

                # Stage 2 Button
                BoxLayout:
                    size_hint_y: None
                    height: dp(90)
                    padding: [40, 0, 40, 0]
                    Button:
                        text: ar("المرحلة 2: المفردات والجمل الطبية 💊\\n") + (("★" * root.stage2_stars + "☆" * (3 - root.stage2_stars)) if 2 in root.unlocked_stages else ar("🔒 مقفلة"))
                        background_normal: ''
                        background_color: [0.98, 0.75, 0.14, 1] if 2 in root.unlocked_stages else [0.85, 0.85, 0.85, 1]
                        color: [0.47, 0.21, 0.06, 1] if 2 in root.unlocked_stages else [0.5, 0.5, 0.5, 1]
                        bold: True
                        font_size: '15sp'
                        on_press: root.open_stage(2)

                # Connecting Path Indicator
                Label:
                    text: "⬇ ⬇ ⬇"
                    color: [0.98, 0.75, 0.14, 0.8]
                    size_hint_y: None
                    height: dp(24)

                # Stage 3 Button
                BoxLayout:
                    size_hint_y: None
                    height: dp(90)
                    padding: [40, 0, 40, 0]
                    Button:
                        text: ar("المرحلة 3: الفحص السريري والمحادثة 📋\\n") + (("★" * root.stage3_stars + "☆" * (3 - root.stage3_stars)) if 3 in root.unlocked_stages else ar("🔒 مقفلة"))
                        background_normal: ''
                        background_color: [0.98, 0.75, 0.14, 1] if 3 in root.unlocked_stages else [0.85, 0.85, 0.85, 1]
                        color: [0.47, 0.21, 0.06, 1] if 3 in root.unlocked_stages else [0.5, 0.5, 0.5, 1]
                        bold: True
                        font_size: '15sp'
                        on_press: root.open_stage(3)

                # Golden Reward Chest (Section 7)
                BoxLayout:
                    size_hint_y: None
                    height: dp(80)
                    padding: [60, 0, 60, 0]
                    Button:
                        text: ar("🎁 صندوق المكافأة الذهبي 🎁\\n(يفتح بعد إكمال أول 3 مراحل)")
                        background_normal: ''
                        background_color: [0.96, 0.62, 0.04, 1] if root.can_open_chest else [0.75, 0.75, 0.75, 1]
                        color: [1, 1, 1, 1]
                        bold: True
                        font_size: '14sp'
                        on_press: root.open_reward_chest()

                # Locked Stage 4
                BoxLayout:
                    size_hint_y: None
                    height: dp(75)
                    padding: [60, 0, 60, 0]
                    Button:
                        text: ar("المرحلة 4: طوارئ وعناية مركزة 🔒")
                        background_normal: ''
                        background_color: [0.9, 0.9, 0.9, 1]
                        color: [0.5, 0.5, 0.5, 1]
                        on_press: root.show_locked_message()

                # Locked Stage 5
                BoxLayout:
                    size_hint_y: None
                    height: dp(75)
                    padding: [60, 0, 60, 0]
                    Button:
                        text: ar("المرحلة 5: علم الأدوية والجرعات 🔒")
                        background_normal: ''
                        background_color: [0.9, 0.9, 0.9, 1]
                        color: [0.5, 0.5, 0.5, 1]
                        on_press: root.show_locked_message()


<LessonScreen>:
    name: 'lesson'
    BoxLayout:
        orientation: 'vertical'
        padding: [20, 20, 20, 20]
        spacing: 16

        # Top Bar: Close, progress, lives
        BoxLayout:
            size_hint_y: 0.1
            Button:
                text: "✕"
                size_hint_x: 0.15
                font_size: '20sp'
                on_press: root.exit_lesson()
            Label:
                text: root.lesson_title
                size_hint_x: 0.6
                bold: True
                color: [0.2, 0.2, 0.2, 1]
            Label:
                text: "❤️ " + str(root.remaining_hearts)
                size_hint_x: 0.25
                color: [0.85, 0.1, 0.1, 1]
                bold: True

        # Interactive Content Area
        BoxLayout:
            id: exercise_container
            orientation: 'vertical'
            size_hint_y: 0.8
            spacing: 12

            Label:
                id: exercise_instruction
                text: root.instruction_text
                font_size: '14sp'
                color: [0.4, 0.4, 0.4, 1]
                size_hint_y: 0.15

            Label:
                id: exercise_prompt
                text: root.prompt_text
                font_size: '28sp'
                bold: True
                color: [0.1, 0.1, 0.1, 1]
                size_hint_y: 0.35

            Label:
                id: target_translation
                text: root.english_text
                font_size: '24sp'
                color: [0.75, 0.4, 0.05, 1]
                bold: True
                size_hint_y: 0.25

        # Bottom Action Button
        Button:
            id: action_btn
            text: ar("تم التعلم ✓") if root.is_intro_step else ar("تحقق من الإجابة")
            size_hint_y: 0.12
            background_normal: ''
            background_color: [0.98, 0.75, 0.14, 1]
            color: [0.47, 0.21, 0.06, 1]
            font_size: '18sp'
            bold: True
            on_press: root.handle_action()
'''

class RegistrationScreen(Screen):
    specialization = StringProperty('medicine')

    def select_specialization(self, spec_key):
        self.specialization = spec_key
        if spec_key != 'medicine':
            popup = Popup(
                title=ar("تنبيه التخصص"),
                content=Label(text=ar("محتوى هذا التخصص قيد التطوير حالياً.\\nيرجى اختيار الطب لتجربة المحتوى الكامل! 🩺")),
                size_hint=(0.85, 0.4)
            )
            popup.open()

    def submit_registration(self):
        first_name = self.ids.first_name_input.text.strip()
        last_name = self.ids.last_name_input.text.strip()

        if not first_name or not last_name:
            popup = Popup(
                title=ar("حقول مطلوبة"),
                content=Label(text=ar("يرجى إدخال الاسم الأول واسم العائلة للمتابعة.")),
                size_hint=(0.8, 0.35)
            )
            popup.open()
            return

        app = App.get_running_app()
        app.store.put('user',
            first_name=first_name,
            last_name=last_name,
            specialization=self.specialization
        )
        self.manager.current = 'main_learning'


class MainLearningScreen(Screen):
    streak = NumericProperty(0)
    coins = NumericProperty(0)
    stage1_stars = NumericProperty(0)
    stage2_stars = NumericProperty(0)
    stage3_stars = NumericProperty(0)
    unlocked_stages = ListProperty([1])
    can_open_chest = BooleanProperty(False)

    def on_pre_enter(self):
        self.load_progress()

    def load_progress(self):
        app = App.get_running_app()
        if app.store.exists('progress'):
            data = app.store.get('progress')
            self.streak = data.get('streak', 0)
            self.coins = data.get('coins', 0)
            self.stage1_stars = data.get('stage1_stars', 0)
            self.stage2_stars = data.get('stage2_stars', 0)
            self.stage3_stars = data.get('stage3_stars', 0)
            self.unlocked_stages = data.get('unlocked_stages', [1])
            self.can_open_chest = (1 in data.get('completed', []) and 2 in data.get('completed', []) and 3 in data.get('completed', []))
        else:
            self.streak = 1
            self.coins = 0
            self.unlocked_stages = [1]

    def open_stage(self, stage_id):
        if stage_id not in self.unlocked_stages:
            self.show_locked_message()
            return
        app = App.get_running_app()
        app.current_stage = stage_id
        self.manager.current = 'lesson'

    def show_locked_message(self):
        # As requested in Section 6:
        # When user clicks a locked stage, display: "لم يتم تحديث هذه المرحلة بعد."
        popup = Popup(
            title=ar("المرحلة مقفلة"),
            content=Label(text=ar("لم يتم تحديث هذه المرحلة بعد.")),
            size_hint=(0.8, 0.3)
        )
        popup.open()

    def open_reward_chest(self):
        if self.can_open_chest:
            self.coins += 50
            app = App.get_running_app()
            prog = app.store.get('progress') if app.store.exists('progress') else {}
            prog['coins'] = self.coins
            app.store.put('progress', **prog)
            popup = Popup(
                title=ar("تهانينا! 🎁"),
                content=Label(text=ar("فتحت صندوق المكافأة الذهبي بنجاح!\\nحصلت على +50 عملة عباد شمس ذهبية! 🌻🪙")),
                size_hint=(0.85, 0.4)
            )
            popup.open()
        else:
            popup = Popup(
                title=ar("الصندوق مغلق"),
                content=Label(text=ar("أكمل أول ثلاث مراحل لفتح صندوق الكنز الذهبي! 🏆")),
                size_hint=(0.85, 0.35)
            )
            popup.open()


class LessonScreen(Screen):
    lesson_title = StringProperty("")
    instruction_text = StringProperty("")
    prompt_text = StringProperty("")
    english_text = StringProperty("")
    remaining_hearts = NumericProperty(3)
    is_intro_step = BooleanProperty(True)

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.step_index = 0
        self.mistakes = 0
        self.stage_exercises = []

    def on_pre_enter(self):
        app = App.get_running_app()
        stage = getattr(app, 'current_stage', 1)
        self.step_index = 0
        self.mistakes = 0
        self.remaining_hearts = 3

        if stage == 1:
            self.stage_exercises = [
                {"type": "intro", "ar": "طِبّ", "en": "Medicine", "inst": "تعرف على المفردة الطبية واستمع لنطقها:"},
                {"type": "intro", "ar": "أنا طبيب", "en": "I am a doctor", "inst": "اقرأ الجملة الطبية الأساسية:"},
                {"type": "arrange", "ar": "أنا طبيب", "en": "I am a doctor", "words": ["doctor", "am", "I", "a"], "inst": "رتب الكلمات لتكوين: I am a doctor"},
                {"type": "construct", "ar": "معالجة المريض", "en": "Treating the patient", "inst": "بناء الجملة الإنجليزية المقابلة:"},
                {"type": "question", "ar": "أين المستشفى؟", "en": "Where is the hospital?", "inst": "تكوين السؤال الطبي:"},
                {"type": "instruction", "ar": "كيف أتناول الدواء؟", "en": "How do I take the medicine?", "inst": "تكوين سؤال كيفية أخذ الدواء:"}
            ]
        elif stage == 2:
            self.stage_exercises = [
                {"type": "matching", "ar": "مستشفى | إبرة | علاج | دواء", "en": "Hospital | Needle | Treatment | Medicine", "inst": "مطابقة الكلمات الطبية بمعانيها"},
                {"type": "arrange", "ar": "أريد زيارة الطبيب في المستشفى.", "en": "I want to visit the doctor at the hospital.", "inst": "ترتيب الجملة الإنجليزية"},
                {"type": "spelling", "ar": "مستشفى", "en": "Hospital", "inst": "كتابة وإملاء الكلمة الإنجليزية"},
                {"type": "construct", "ar": "لم أجد الدواء في الصيدلية.", "en": "I did not find the medicine at the pharmacy.", "inst": "بناء الجملة المنفية"},
                {"type": "intro", "ar": "وَصْفَة طِبِّيَّة", "en": "Prescription", "inst": "تعلم مفردة الوصفة الطبية"}
            ]
        else:
            self.stage_exercises = [
                {"type": "intro", "ar": "فَحْص سَرِيرِيّ", "en": "Clinical examination", "inst": "المصطلح السريري"},
                {"type": "arrange", "ar": "يحتاج المريض فحص دم فوراً.", "en": "The patient needs a blood test immediately.", "inst": "ترتيب الجملة التشخيصية"}
            ]

        self.load_step()

    def load_step(self):
        if self.step_index >= len(self.stage_exercises):
            self.evaluate_stage()
            return

        ex = self.stage_exercises[self.step_index]
        self.lesson_title = ar(f"تمرين {self.step_index + 1} من {len(self.stage_exercises)}")
        self.instruction_text = ar(ex["inst"])
        self.prompt_text = ar(ex["ar"])
        self.english_text = ex["en"]
        self.is_intro_step = (ex["type"] == "intro")

    def handle_action(self):
        # Advance exercise
        self.step_index += 1
        self.load_step()

    def evaluate_stage(self):
        stars = 3 - self.mistakes
        app = App.get_running_app()
        stage = getattr(app, 'current_stage', 1)

        if stars > 0:
            # Success
            prog = app.store.get('progress') if app.store.exists('progress') else {}
            completed = prog.get('completed', [])
            if stage not in completed:
                completed.append(stage)
            prog['completed'] = completed
            prog[f'stage{stage}_stars'] = max(stars, prog.get(f'stage{stage}_stars', 0))

            unlocked = prog.get('unlocked_stages', [1])
            if stage + 1 not in unlocked and stage < 4:
                unlocked.append(stage + 1)
            prog['unlocked_stages'] = unlocked
            prog['coins'] = prog.get('coins', 0) + 20
            prog['streak'] = prog.get('streak', 1) + 1
            app.store.put('progress', **prog)

            popup = Popup(
                title=ar("أحسنت! نجحت في المرحلة 🎉"),
                content=Label(text=ar(f"حصلت على {stars} من 3 نجوم!\\nتم فتح المرحلة التالية وإضافة 20 عملة 🌻")),
                size_hint=(0.85, 0.4)
            )
            popup.bind(on_dismiss=lambda *_: self.exit_lesson())
            popup.open()
        else:
            popup = Popup(
                title=ar("للأسف ارتكبت 3 أخطاء!"),
                content=Label(text=ar("يجب إعادة المحاولة لتجاوز المرحلة وكسب النجوم.")),
                size_hint=(0.85, 0.35)
            )
            popup.bind(on_dismiss=lambda *_: self.exit_lesson())
            popup.open()

    def exit_lesson(self):
        self.manager.current = 'main_learning'


class SunflowerEnglishApp(App):
    def build(self):
        self.store = JsonStore('progress.json')
        self.current_stage = 1
        Builder.load_string(KV_DESIGN)

        sm = ScreenManager(transition=FadeTransition())
        sm.add_widget(RegistrationScreen(name='registration'))
        sm.add_widget(MainLearningScreen(name='main_learning'))
        sm.add_widget(LessonScreen(name='lesson'))

        # Check if already registered
        if self.store.exists('user'):
            sm.current = 'main_learning'
        else:
            sm.current = 'registration'

        return sm


if __name__ == '__main__':
    SunflowerEnglishApp().run()
