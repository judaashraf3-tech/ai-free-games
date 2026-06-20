import tkinter as tk
from tkinter import messagebox
import customtkinter as ctk
import webbrowser
import threading
import time
import urllib.parse
import re
import random

ctk.set_appearance_mode("Dark")
ctk.set_default_color_theme("blue")

class MiraUltimateAgent(ctk.CTk):
    def __init__(self):
        super().__init__()

        self.title("Mira AI - Advanced Autonomous Companion")
        self.geometry("1250x850")
        self.minsize(1000, 700)

        # الروابط الأساسية
        self.g3_search_url = "https://game3rb.com/?s="
        self.repack_search_url = "https://repack-games.com/?s="
        
        # الألوان التفاعلية
        self.accent_color = "#9370DB"  # بنفسجي ملكي
        self.bot_text_color = "#FFD700" # ذهبي
        self.user_text_color = "#E6E6FA" 

        # 1. قاعدة المعرفة السوبر-ذكية للألعاب (تصلح العامية والاختصارات)
        self.games_knowledge_base = {
            r"بلاك\s*اوبس": "Call of Duty Black Ops",
            r"بلاك\s*أوبس": "Call of Duty Black Ops",
            r"كول\s*اوف\s*ديوتي": "Call of Duty",
            r"كود\s*\d*": "Call of Duty",
            r"مودرن\s*وارفير": "Call of Duty Modern Warfare",
            r"ر[دز]+نت\s*ايفل": "Resident Evil",
            r"رزنت": "Resident Evil",
            r"سبايدر\s*مان": "Marvels Spider-Man",
            r"قراند|جتا|gta": "Grand Theft Auto",
            r"ريد\s*ديد": "Red Dead Redemption",
            r"ايلدن": "Elden Ring",
            r"سايبر\s*بانك": "Cyberpunk 2077",
            r"هيت\s*مان": "Hitman",
            r"ذا\s*لاست\s*اوف\s*اس": "The Last of Us",
            r"قود\s*اوف\s*وار": "God of War",
            r"فيفا": "EA Sports FC FIFA",
            r"اساسنز|اساسن": "Assassins Creed",
        }

        # 2. قاعدة الردود الطبيعية للدردشة
        self.chat_responses = {
            "greetings": ["أهلاً بكِ يا Mira! أشرف يرسل لكِ تحياته عبر سطوري البرمجية. ماذا سنلعب اليوم؟", "مرحباً ميرّا! أنا بكامل جاهزيتي لتحليل السيرفرات، اطلبي وتمنّي.", "أهلاً يا ميرّا. عقلي الاصطناعي مستقر 100%، أخبريني باسم اللعبة فوراً."],
            "thanks": ["على الرحب والسعة يا Mira! هذا واجبي الذي برمجني أشرف لأجله.", "في خدمتكِ دائماً! لا تترددي في سؤالي لو واجهتكِ أي مشكلة في فك الضغط.", "يسعدني جداً أنني أفدتكِ!"],
            "who_are_you": ["أنا المساعد الذكي الخاص بكِ (Mira AI). تم تصميمي وهندستي برمجياً بواسطة أشرف خصيصاً لكي أسهل عليكِ إيجاد الألعاب النظيفة وتحميلها بأمان تام."]
        }

        self.setup_ui()
        self.after(500, self.introduce_agent)

    def setup_ui(self):
        # اللوحة الجانبية
        self.sidebar = ctk.CTkFrame(self, width=280, fg_color="#09090c", corner_radius=0)
        self.sidebar.pack(side="left", fill="y")

        self.logo = ctk.CTkLabel(self.sidebar, text="MIRA AI", font=ctk.CTkFont(size=32, weight="bold"), text_color=self.accent_color)
        self.logo.pack(pady=(40, 10))
        
        self.sub_logo = ctk.CTkLabel(self.sidebar, text="Autonomous Game Engine", font=ctk.CTkFont(size=11), text_color="#666")
        self.sub_logo.pack(pady=(0, 30))

        btn_g3 = ctk.CTkButton(self.sidebar, text="🌐 فتح Game3rb الرسمي", fg_color="#b8860b", hover_color="#996515", font=ctk.CTkFont(weight="bold"), height=42, command=lambda: webbrowser.open("https://game3rb.com/"))
        btn_g3.pack(padx=20, pady=8, fill="x")

        btn_rp = ctk.CTkButton(self.sidebar, text="🌐 فتح Repack الرسمي", fg_color="#5c00a3", hover_color="#420075", font=ctk.CTkFont(weight="bold"), height=42, command=lambda: webbrowser.open("https://repack-games.com/"))
        btn_rp.pack(padx=20, pady=8, fill="x")

        # فاصل
        ctk.CTkFrame(self.sidebar, height=1, fg_color="#1f1f28").pack(padx=20, pady=25, fill="x")

        # قسم المساعدة السريعة
        lbl_help = ctk.CTkLabel(self.sidebar, text="💡 استفسارات شائعة (اضغطي):", font=ctk.CTkFont(size=13, weight="bold"), text_color="#aaa")
        lbl_help.pack(anchor="w", padx=20, pady=5)

        quick_questions = ["كيف احمل من الموقع؟", "وش البرامج اللي احتاجها؟", "اللعبة تطلع لي No Results"]
        for q in quick_questions:
            q_btn = ctk.CTkButton(self.sidebar, text=f"❓ {q}", fg_color="#13131a", hover_color="#1f1f2e", text_color="#ddd", anchor="w", height=32, command=lambda text=q: self.inject_quick_question(text))
            q_btn.pack(padx=20, pady=4, fill="x")

        # المطور بالأسفل
        self.dev_lbl = ctk.CTkLabel(self.sidebar, text="Engineered with ♥ by Ashraf\nStable Build v5.0", font=ctk.CTkFont(size=11, slant="italic"), text_color="#555")
        self.dev_lbl.pack(side="bottom", pady=30)

        # الحاوية الرئيسية
        self.main_frame = ctk.CTkFrame(self, fg_color="#040406", corner_radius=0)
        self.main_frame.pack(side="right", fill="both", expand=True)

        # الهيدر
        self.header = ctk.CTkFrame(self.main_frame, height=60, fg_color="#0a0a0f", corner_radius=0)
        self.header.pack(fill="x", side="top")
        self.status_label = ctk.CTkLabel(self.header, text="● النظام متصل ومستعد للتحليل اللغوي", font=ctk.CTkFont(size=14, weight="bold"), text_color="#00FF66")
        self.status_label.pack(pady=18)

        # شاشة المحادثة
        self.chat_box = ctk.CTkTextbox(self.main_frame, font=ctk.CTkFont(size=15), wrap="word", fg_color="#070709", border_color="#15151f", border_width=1)
        self.chat_box.pack(padx=25, pady=15, fill="both", expand=True)
        self.chat_box.configure(state="disabled")

        self.chat_box.tag_config("mira", justify="right", foreground=self.user_text_color)
        self.chat_box.tag_config("ai", justify="left", foreground=self.bot_text_color)
        self.chat_box.tag_config("system", justify="center", foreground="#8888aa")

        # حاوية الروابط الديناميكية (تظهر فيها الأزرار بعد البحث)
        self.actions_panel = ctk.CTkFrame(self.main_frame, height=70, fg_color="#0a0a0f", border_color="#15151f", border_width=1)
        self.actions_panel.pack(padx=25, pady=(0, 15), fill="x")
        self.actions_label = ctk.CTkLabel(self.actions_panel, text="[ منطقة توليد الروابط والأدوات الذكية ستظهر هنا ]", text_color="#555", font=ctk.CTkFont(size=13))
        self.actions_label.pack(pady=20)

        # شريط الإدخال
        self.input_panel = ctk.CTkFrame(self.main_frame, fg_color="transparent")
        self.input_panel.pack(padx=25, pady=(0, 20), fill="x", side="bottom")

        self.entry = ctk.CTkEntry(self.input_panel, placeholder_text="تحدثي مع AI، اطلبي لعبة (مثال: ابي كول اوف ديوتي)، أو اسألي كيف احمل...", font=ctk.CTkFont(size=14), height=52, fg_color="#0d0d12", border_color="#222")
        self.entry.pack(side="left", fill="x", expand=True, padx=(0, 15))
        self.entry.bind("<Return>", lambda e: self.trigger_user_send())

        self.btn_send = ctk.CTkButton(self.input_panel, text="إرسال لـ أشرف AI", width=140, height=52, fg_color=self.accent_color, hover_color="#7b68ee", font=ctk.CTkFont(size=14, weight="bold"), command=self.trigger_user_send)
        self.btn_send.pack(side="right")

    def introduce_agent(self):
        msg = "مرحباً بكِ يا Mira.\nأنا المساعد الذكي أشرف (AI Agent). لقد تم تزويدي بخوارزمية فهم عميقة جداً؛\n- إذا أردتِ لعبة: فقط اكتبي اسمها حتى لو بالعامية (مثال: 'ابي بلاك اوبس 6').\n- إذا لم تعرفي طريقة التحميل: فقط اسألي (كيف احمل؟) وسأعطيكِ الروابط والشرح."
        self.append_text(f"Ashraf AI\n{msg}", "ai")

    def inject_quick_question(self, text):
        self.entry.delete(0, tk.END)
        self.entry.insert(0, text)
        self.trigger_user_send()

    def append_text(self, text, tag):
        self.chat_box.configure(state="normal")
        self.chat_box.insert(tk.END, f"{text}\n\n", tag)
        self.chat_box.configure(state="disabled")
        self.chat_box.see(tk.END)

    def trigger_user_send(self):
        user_input = self.entry.get().strip()
        if not user_input: return

        self.append_text(f"Mira\n{user_input}", "mira")
        self.entry.delete(0, tk.END)
        self.status_label.configure(text="● الذكاء الاصطناعي يفكر ويحلل طلبك...", text_color="#FFD700")

        # إرسال التحليل لـ Thread آمن تماماً يمنع الـ TclError
        threading.Thread(target=self.nlp_core_processor, args=(user_input,), daemon=True).start()

    # ==========================================
    # محرك الذكاء الاصطناعي (NLP & Intent Engine)
    # ==========================================
    def nlp_core_processor(self, raw_text):
        time.sleep(0.6) # محاكاة التفكير البشري
        text = raw_text.lower()

        # 1. فحص نية "طلب المساعدة والشروحات" (Tech Support Intent)
        if any(w in text for w in ["كيف احمل", "كيف انزل", "شرح تحميل", "طريقة التحميل", "وشلون احمل", "كيف اسوي", "علمني"]):
            self.execute_safe_gui_update("support_download", raw_text)
            return

        if any(w in text for w in ["برامج", "ناقصني", "وش احط", "ملفات dll", "تطبيق تورنت", "فك الضغط"]):
            self.execute_safe_gui_update("support_tools", raw_text)
            return

        # 2. فحص نية "الدردشة الطبيعية" (Small Talk Intent)
        if any(w == text.strip() for w in ["هلا", "مرحبا", "سلام", "هاي", "اهلين", "صباح الخير", "مراحب"]):
            self.execute_safe_gui_update("chat_greet", random.choice(self.chat_responses["greetings"]))
            return

        if any(w in text for w in ["شكرا", "يعطيك العافيه", "يسلمو", "ماقصرت", "ثانكس", "حبيبي"]):
            self.execute_safe_gui_update("chat_thanks", random.choice(self.chat_responses["thanks"]))
            return

        if any(w in text for w in ["من انت", "مين برمجك", "وش اسمك", "مين اشرف"]):
            self.execute_safe_gui_update("chat_who", self.chat_responses["who_are_you"][0])
            return

        # 3. إذا لم تكن دردشة ولا مساعدة، فهي نية "البحث عن لعبة" (Game Extraction Intent)
        extracted_game = self.extract_clean_game_name(text)
        self.execute_safe_gui_update("game_found", extracted_game)

    def extract_clean_game_name(self, text):
        # البحث في القاموس الذكي أولاً
        for pattern, real_name in self.games_knowledge_base.items():
            if re.search(pattern, text):
                # سحب الأرقام لو كانت موجودة (مثال: بلاك اوبس 6 -> يسحب رقم 6)
                num = re.findall(r'\d+', text)
                addon = f" {num[0]}" if num else ""
                return f"{real_name}{addon}"

        # تنظيف الكلمات الزائدة لو كتبت اسم غير موجود بالقاموس
        stop_words = ["اريد", "لعبة", "لعبه", "ابي", "ابحث", "عن", "حمل", "تنزيل", "موقع", "اسمها", "اللي", "تطلع", "جيب"]
        cleaned = text
        for w in stop_words:
            cleaned = re.sub(r'\b' + w + r'\b', '', cleaned)
        
        # إذا تبقى كلام إنجليزي ناخذه، وإلا نأخذ الصافي
        eng = re.findall(r'[a-zA-Z0-9\-\:]+', cleaned)
        return " ".join(eng).strip() if eng else cleaned.strip()

    # ==========================================
    # الجسر الآمن لتحديث الواجهة (Thread-to-GUI Lock)
    # ==========================================
    def execute_safe_gui_update(self, action_type, payload):
        self.after(0, self._render_ai_response_safe, action_type, payload)

    def _render_ai_response_safe(self, action, payload):
        self.status_label.configure(text="● متصل ومستعد", text_color="#00FF66")

        # تنظيف لوحة الأزرار السفلية
        for widget in self.actions_panel.winfo_children():
            widget.destroy()

        if action.startswith("chat_"):
            self.append_text(f"Ashraf AI\n{payload}", "ai")
            lbl = ctk.CTkLabel(self.actions_panel, text="💬 [ يمكنكِ كتابة اسم أي لعبة للبحث عنها فوراً ]", text_color="#777")
            lbl.pack(pady=20)

        elif action == "support_download":
            reply = (
                "أبشري يا ميرّا، الشرح بالتفصيل:\n\n"
                "1. في موقع Game3rb: انزلي بالصفحة للأسفل حتى تجدي جدول (Download Links)، اضغطي على الرابط المباشر (Direct) أو (MediaFire)، سيفتح لكِ عداد 5 ثواني ثم اضغطي Click here.\n"
                "2. في موقع Repack-Games: اضغطي على زر التحميل، سيحولك لموقع اسمه (UploadHaven)، انتظري العداد واضغطي Free Download.\n\n"
                "🎥 وإذا واجهتكِ إعلانات مزعجة، جهزت لكِ هذا الزر يفتح لكِ فيديو يوتيوب مباشر يشرح التحميل عملياً في دقيقة:"
            )
            self.append_text(f"Ashraf AI (Technical Support)\n{reply}", "ai")

            yt_query = urllib.parse.quote_plus("شرح كيفية التحميل من موقع game3rb و repack")
            yt_link = f"https://www.youtube.com/results?search_query={yt_query}"
            
            btn_yt = ctk.CTkButton(self.actions_panel, text="▶️ مشاهدة شرح فيديو على YouTube", fg_color="#FF0000", hover_color="#cc0000", font=ctk.CTkFont(weight="bold"), height=38, command=lambda: webbrowser.open(yt_link))
            btn_yt.pack(pady=15, padx=20)

        elif action == "support_tools":
            reply = (
                "لتشغيل أي لعبة في العالم بدون مشاكل أو رسائل (0xc00007b)، تحتاجين فقط 3 أشياء أساسية في جهازك:\n"
                "1. برنامج فك الضغط الرسمي (WinRAR).\n"
                "2. حزمة مشغلات الألعاب (All in One Runtimes / DirectX).\n"
                "3. برنامج تحميل سريع (مثل FDM أو IDM).\n\n"
                "وضعت لكِ روابط جوجل المباشرة لتحميلها بضغطة واحدة بالأسفل:"
            )
            self.append_text(f"Ashraf AI (System Tools)\n{reply}", "ai")

            tools_frame = ctk.CTkFrame(self.actions_panel, fg_color="transparent")
            tools_frame.pack(pady=15)

            ctk.CTkButton(tools_frame, text="📦 تحميل WinRAR", fg_color="#1f538d", command=lambda: webbrowser.open("https://www.win-rar.com/download.html")).pack(side="right", padx=5)
            ctk.CTkButton(tools_frame, text="⚙️ تحميل DirectX", fg_color="#b8860b", command=lambda: webbrowser.open("https://www.google.com/search?q=DirectX+End-User+Runtime+download+microsoft")).pack(side="right", padx=5)

        elif action == "game_found":
            game_name = payload
            if len(game_name) < 2:
                self.append_text("Ashraf AI\nعذراً يا ميرّا، لم أستطع تمييز اسم اللعبة من الجملة، هل يمكنكِ كتابة اسمها بوضوح؟", "ai")
                return

            reply = f"تحليل ناجح! اكتشفت أنكِ تبحثين عن: 【 {game_name} 】\n\nقمت بتوليد 3 مسارات بحث آمنة لكِ في الأسفل:\n- الزر الأول والثاني: يبحثان داخل المواقع مباشرة.\n- الزر الثالث (سلاح الذكاء): يجعل جوجل نفسه يفتش داخل سيرفرات Game3rb ويجلب الرابط الصافي (استخدميه لو قال لكِ الموقع No Results)."
            self.append_text(f"Ashraf AI (Game Radar)\n{reply}", "ai")

            # توليد الروابط الثلاثة
            safe_query_site = urllib.parse.quote(game_name)
            safe_query_google = urllib.parse.quote_plus(f"site:game3rb.com {game_name}")

            url_g3 = f"{self.g3_search_url}{safe_query_site}"
            url_rp = f"{self.repack_search_url}{safe_query_site}"
            url_google_dork = f"https://www.google.com/search?q={safe_query_google}"

            btn_frame = ctk.CTkFrame(self.actions_panel, fg_color="transparent")
            btn_frame.pack(pady=15, fill="x", padx=10)

            btn1 = ctk.CTkButton(btn_frame, text="🎯 بحث في Game3rb", fg_color="#b8860b", hover_color="#996515", font=ctk.CTkFont(weight="bold"), height=36, command=lambda: webbrowser.open(url_g3))
            btn1.pack(side="right", padx=5, expand=True, fill="x")

            btn2 = ctk.CTkButton(btn_frame, text="🔥 بحث في Repack", fg_color="#5c00a3", hover_color="#420075", font=ctk.CTkFont(weight="bold"), height=36, command=lambda: webbrowser.open(url_rp))
            btn2.pack(side="right", padx=5, expand=True, fill="x")

            btn3 = ctk.CTkButton(btn_frame, text="🔍 كشاف Google للموقع (مضمون)", fg_color="#185c37", hover_color="#12472a", font=ctk.CTkFont(weight="bold"), height=36, command=lambda: webbrowser.open(url_google_dork))
            btn3.pack(side="right", padx=5, expand=True, fill="x")

if __name__ == "__main__":
    app = MiraUltimateAgent()
    app.mainloop()