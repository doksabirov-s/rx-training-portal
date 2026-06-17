#!/usr/bin/env python3
import os
from fpdf import FPDF


class ArticlePDF(FPDF):
    def __init__(self, header_text=""):
        super().__init__()
        self._header_text = header_text

    def header(self):
        self.set_font("DejaVu", "B", 9)
        self.set_text_color(100, 100, 100)
        self.cell(0, 8, self._header_text, align="C")
        self.ln(4)
        self.set_draw_color(0, 102, 178)
        self.set_line_width(0.5)
        self.line(10, self.get_y(), 200, self.get_y())
        self.ln(6)

    def footer(self):
        self.set_y(-15)
        self.set_font("DejaVu", "", 8)
        self.set_text_color(128, 128, 128)
        self.cell(0, 10, f"Стр. {self.page_no()}/{{nb}}", align="C")

    def section_title(self, title):
        self.set_font("DejaVu", "B", 16)
        self.set_text_color(0, 70, 140)
        self.multi_cell(0, 9, title)
        self.set_draw_color(0, 102, 178)
        self.set_line_width(0.4)
        self.line(10, self.get_y(), 200, self.get_y())
        self.ln(6)

    def sub_title(self, title):
        self.set_font("DejaVu", "B", 12)
        self.set_text_color(40, 40, 40)
        self.multi_cell(0, 7, title)
        self.ln(3)

    def body_text(self, text):
        self.set_font("DejaVu", "", 10)
        self.set_text_color(30, 30, 30)
        self.multi_cell(0, 6, text)
        self.ln(3)

    def bold_text(self, text):
        self.set_font("DejaVu", "B", 10)
        self.set_text_color(30, 30, 30)
        self.multi_cell(0, 6, text)
        self.ln(1)

    def italic_text(self, text):
        self.set_font("DejaVu", "I", 10)
        self.set_text_color(60, 60, 60)
        self.multi_cell(0, 6, text)
        self.ln(3)

    def ref_text(self, text):
        self.set_font("DejaVu", "", 9)
        self.set_text_color(80, 80, 80)
        self.multi_cell(0, 5.5, text)
        self.ln(2)

    def green_box(self, text):
        self.set_fill_color(230, 245, 230)
        self.set_draw_color(0, 130, 0)
        self.set_line_width(0.4)
        self.set_font("DejaVu", "B", 10)
        self.set_text_color(0, 80, 0)
        y = self.get_y()
        lines = text.count("\n") + 1
        h = max(16, lines * 7 + 8)
        self.rect(10, y, 190, h, style="D")
        self.set_xy(14, y + 4)
        self.multi_cell(182, 6, text, fill=False)
        self.ln(8)

    def yellow_box(self, text):
        self.set_fill_color(255, 250, 230)
        self.set_draw_color(180, 140, 0)
        self.set_line_width(0.4)
        self.set_font("DejaVu", "I", 9.5)
        self.set_text_color(100, 80, 0)
        y = self.get_y()
        lines = text.count("\n") + 1
        h = max(14, lines * 6 + 8)
        self.rect(10, y, 190, h, style="D")
        self.set_xy(14, y + 4)
        self.multi_cell(182, 6, text, fill=False)
        self.ln(8)

    def table_row(self, cols, widths, bold=False, header=False):
        if header:
            self.set_font("DejaVu", "B", 9)
            self.set_fill_color(0, 70, 140)
            self.set_text_color(255, 255, 255)
        elif bold:
            self.set_font("DejaVu", "B", 9)
            self.set_fill_color(245, 245, 245)
            self.set_text_color(30, 30, 30)
        else:
            self.set_font("DejaVu", "", 9)
            self.set_fill_color(255, 255, 255)
            self.set_text_color(30, 30, 30)
        for i, (col, w) in enumerate(zip(cols, widths)):
            self.cell(w, 7, col, border=1, fill=True, align="C" if i > 0 else "L")
        self.ln()


def make_pdf(header_text):
    pdf = ArticlePDF(header_text)
    pdf.alias_nb_pages()
    pdf.add_font("DejaVu", "", "/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf")
    pdf.add_font("DejaVu", "B", "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf")
    pdf.add_font("DejaVu", "I", "/usr/share/fonts/truetype/freefont/FreeSansOblique.ttf")
    pdf.set_auto_page_break(auto=True, margin=20)
    pdf.add_page()
    return pdf


OUT = "/home/user/rx-training-portal/articles"
os.makedirs(OUT, exist_ok=True)

# =====================================================================
# 1. Buckshee K et al., 1997
# =====================================================================
pdf = make_pdf("Buckshee K et al., 1997 — Обзор статьи")
pdf.section_title("Микронизированная флавоноидная терапия при геморрое беременных")
pdf.bold_text("Авторы:")
pdf.body_text("Buckshee K, Takkar D, Aggarwal N.")
pdf.bold_text("Оригинальное название:")
pdf.italic_text("Micronized flavonoid therapy in internal hemorrhoids of pregnancy.")
pdf.bold_text("Журнал:")
pdf.body_text("International Journal of Gynecology & Obstetrics. 1997 May; 57(2): 145-151.")
pdf.ref_text("PMID: 9184951 | DOI: 10.1016/s0020-7292(97)02889-0\nPubMed: https://pubmed.ncbi.nlm.nih.gov/9184951/")
pdf.ln(2)

pdf.sub_title("Дизайн исследования")
pdf.body_text(
    "Открытое проспективное исследование.\n"
    "Популяция: 50 беременных женщин с острым внутренним геморроем."
)

pdf.sub_title("Препарат")
pdf.body_text(
    "Микронизированный диосмин 90% + гесперидин 10% (МОФФ (диосмин + гесперидин)).\n"
    "Длительность: медиана 8 недель до родов + 4 недели после родов."
)

pdf.sub_title("Ключевые результаты")
pdf.body_text(
    "• 66% (95% ДИ: 52.9–79.1) пациенток получили облегчение\n"
    "  острых симптомов к 4-му дню лечения\n\n"
    "• 53.6% (95% ДИ: 37.1–70.0, P < 0.001) — уменьшение числа\n"
    "  рецидивов в антенатальном периоде\n\n"
    "• Лечение хорошо переносилось\n\n"
    "• Не повлияло на:\n"
    "  — течение беременности\n"
    "  — развитие плода\n"
    "  — массу тела при рождении\n"
    "  — рост и вскармливание ребёнка"
)

pdf.green_box(
    'Вывод авторов: «В краткосрочной перспективе микронизированный\n'
    'диосмин 90% + гесперидин 10% безопасен, приемлем и эффективен\n'
    'при лечении геморроя беременных.»'
)

pdf.sub_title("Значимость для клинической практики")
pdf.body_text(
    "Это ключевое исследование, непосредственно демонстрирующее\n"
    "эффективность и безопасность МОФФ (диосмин + гесперидин)\n"
    "у беременных женщин с геморроем. Подтверждает отсутствие\n"
    "негативного влияния на исход беременности и состояние\n"
    "новорождённого."
)
pdf.output(f"{OUT}/01_Buckshee_1997.pdf")
print("  01_Buckshee_1997.pdf")

# =====================================================================
# 2. Lacroix I et al., 2015
# =====================================================================
pdf = make_pdf("Lacroix I et al., 2015 — Обзор статьи")
pdf.section_title("Первые эпидемиологические данные по венотоникам при беременности (EFEMERIS)")
pdf.bold_text("Авторы:")
pdf.body_text("Lacroix I, Beau AB, Hurault-Delarue C, Bouilhac C, Petiot D, Vayssiere C, Vidal S, Montastruc JL, Damase-Michel C.")
pdf.bold_text("Оригинальное название:")
pdf.italic_text("First epidemiological data for venotonics in pregnancy from the EFEMERIS database.")
pdf.bold_text("Журнал:")
pdf.body_text("Phlebology. 2016 Jun; 31(5): 344-348. Epub 2015 Jun 9.")
pdf.ref_text("PMID: 26060062 | DOI: 10.1177/0268355515589679\nPubMed: https://pubmed.ncbi.nlm.nih.gov/26060062/")
pdf.ln(2)

pdf.sub_title("Дизайн исследования")
pdf.body_text(
    "Эпидемиологическое когортное исследование.\n"
    "Источник: база данных EFEMERIS (Франция, 2004–2007)."
)

pdf.sub_title("Популяция")
pdf.body_text(
    "• 8 998 женщин (24%) получали хотя бы один рецепт\n"
    "  на венотоники во время беременности\n"
    "• 1 200 из них — экспозиция в период органогенеза\n"
    "• Контрольная группа: 27 963 неэкспонированных женщины\n\n"
    "Наиболее часто использовались: гесперидин, диосмин, троксерутин."
)

pdf.sub_title("Ключевые результаты безопасности")

w = [90, 45, 45]
pdf.table_row(["Параметр", "Экспонированные", "Контроль"], w, header=True)
pdf.table_row(["Живорождение", "98.4%", "93.6%"], w)
pdf.table_row(["Прерывание беременности", "1.6%", "6.4%"], w)
pdf.ln(4)

pdf.body_text(
    "• Риск прерывания беременности НИЖЕ у экспонированных:\n"
    "  HR = 0.71 (95% ДИ: 0.60–0.84)\n\n"
    "• Риск преждевременных родов НИЖЕ у экспонированных:\n"
    "  HR = 0.82 (95% ДИ: 0.73–0.93)\n\n"
    "• Мальформации при экспозиции в период органогенеза:\n"
    "  3.4% vs 3.0% — ORa = 1.134 (0.873–1.472) — нет значимой разницы\n\n"
    "• Неонатальные заболевания при экспозиции в III триместре:\n"
    "  4.9% vs 6.1% — ORa = 1.07 (0.95–1.20) — нет значимой разницы"
)

pdf.green_box(
    'Вывод: «Не выявлено увеличения риска неблагоприятных исходов\n'
    'беременности у женщин, получавших венотоники, по сравнению\n'
    'с неэкспонированными беременными.»'
)

pdf.sub_title("Значимость")
pdf.body_text(
    "Крупнейшее эпидемиологическое исследование безопасности\n"
    "венотоников (включая диосмин и гесперидин) при беременности.\n"
    "Почти 37 000 женщин. Подтверждает безопасность для матери и плода."
)
pdf.output(f"{OUT}/02_Lacroix_EFEMERIS_2015.pdf")
print("  02_Lacroix_EFEMERIS_2015.pdf")

# =====================================================================
# 3. Kadioglu M et al., 2015
# =====================================================================
pdf = make_pdf("Kadioglu M et al., 2015 — Обзор статьи")
pdf.section_title("Применение диосмина с гесперидином у беременных с варикозом")
pdf.bold_text("Авторы:")
pdf.body_text("Kadioglu M, Aykan D, Erkoseoglu I, Aran T, Engin Y, Murat K, Ersin Y, Nuri K.")
pdf.bold_text("Оригинальное название:")
pdf.italic_text("Diosmin-hesperidin use in pregnant women with varicose veins.")
pdf.bold_text("Журнал:")
pdf.body_text("Reproductive Toxicology. 2015 Nov; 57: 225.")
pdf.ref_text("DOI: 10.1016/j.reprotox.2015.06.038\nResearchGate: https://www.researchgate.net/publication/283190858")
pdf.ln(2)

pdf.sub_title("Описание")
pdf.body_text(
    "Применение комбинации диосмин/гесперидин у беременных\n"
    "с варикозной болезнью."
)

pdf.yellow_box("Примечание: статья представлена как абстракт конференции\nв Reproductive Toxicology, полный текст не индексирован в PubMed.")

pdf.sub_title("Значимость")
pdf.body_text(
    "Дополнительное свидетельство применения комбинации\n"
    "диосмин + гесперидин именно у беременных с варикозом.\n"
    "Подтверждает актуальность темы безопасности биофлавоноидов\n"
    "при беременности."
)
pdf.output(f"{OUT}/03_Kadioglu_2015.pdf")
print("  03_Kadioglu_2015.pdf")

# =====================================================================
# 4. Tsouderos Y, 1989
# =====================================================================
pdf = make_pdf("Tsouderos Y, 1989 — Обзор статьи")
pdf.section_title("Флеботонические свойства диосмина с гесперидином:\nфармакоклиническое исследование")
pdf.bold_text("Автор:")
pdf.body_text("Tsouderos Y.")
pdf.bold_text("Оригинальное название:")
pdf.italic_text(
    "Are the phlebotonic properties shown in clinical pharmacology\n"
    "predictive of a therapeutic benefit in chronic venous insufficiency?\n"
    "Our experience with micronized diosmin + hesperidin."
)
pdf.bold_text("Журнал:")
pdf.body_text("International Angiology. 1989; 8(4 Suppl): 53-59.")
pdf.ref_text("PMID: 2698902\nPubMed: https://pubmed.ncbi.nlm.nih.gov/2698902/")
pdf.ln(2)

pdf.sub_title("Дизайн исследования")
pdf.body_text(
    "Раннее фармакоклиническое исследование.\n"
    "3 группы по 10 женщин с хронической венозной недостаточностью,\n"
    "включая группу беременных (Group II)."
)

pdf.sub_title("Ключевые результаты")
pdf.body_text(
    "• Показан острый эффект повышения венозного тонуса\n"
    "  через 1 и 2 часа после приёма\n\n"
    "• Микронизированный диосмин с гесперидином значительно снижал:\n"
    "  — венозную ёмкость (p < 0.001)\n"
    "  — венозную растяжимость (p < 0.001)\n"
    "  — время венозного оттока (p < 0.001)"
)

pdf.sub_title("Значимость")
pdf.body_text(
    "Одно из ранних исследований, включавших группу беременных.\n"
    "Подтверждает быстрый фармакологический эффект диосмина\n"
    "с гесперидином на венозный тонус, в том числе у беременных."
)
pdf.output(f"{OUT}/04_Tsouderos_1989.pdf")
print("  04_Tsouderos_1989.pdf")

# =====================================================================
# 5. Дженина О.В. et al., 2019
# =====================================================================
pdf = make_pdf("Дженина О.В. et al., 2019 — Обзор статьи")
pdf.section_title("Вульварный и промежностный варикоз у беременных")
pdf.bold_text("Авторы:")
pdf.body_text("Дженина О.В., Богачев В.Ю., Боданская А.Л.")
pdf.bold_text("Журнал:")
pdf.body_text("Амбулаторная хирургия. 2019; 1–2: 14–18.")
pdf.ref_text(
    "DOI: 10.21518/1995-1477-2019-1-2-14-18\n"
    "Полный текст PDF: https://pdfs.semanticscholar.org/7166/a2a3a37d09d82fe52ad3f306c0abc46a9020.pdf"
)
pdf.ln(2)

pdf.sub_title("Популяция")
pdf.body_text(
    "192 беременных женщины с вульварным и промежностным варикозом\n"
    "во II и III триместрах беременности."
)

pdf.sub_title("Препарат")
pdf.body_text("Диосмин с гесперидином 600 мг/сут.")

pdf.sub_title("Данные EFEMERIS (цитируемые в обзоре)")
pdf.body_text(
    "8 998 женщин принимали диосмин, троксерутин и гесперидин\n"
    "во время беременности. Результат: отсутствие негативного влияния\n"
    "на течение беременности, родоразрешение, послеродовый период\n"
    "и развитие плода."
)

pdf.sub_title("Ключевые результаты")

w2 = [95, 85]
pdf.table_row(["Параметр", "Результат"], w2, header=True)
pdf.table_row(["Полное купирование боли", "47.29%"], w2)
pdf.table_row(["Уменьшение боли на ≥2 балла", "27%"], w2)
pdf.table_row(["Осложнения беременности/родов", "0 из 192"], w2)
pdf.table_row(["Разрыв вариксов при родах", "Не отмечалось"], w2)
pdf.table_row(["Пороки развития у детей", "Не отмечено"], w2)
pdf.ln(4)

pdf.green_box(
    "Вывод: Современные препараты диосмина с гесперидином\n"
    "безопасны при беременности и целесообразны при болевом\n"
    "синдроме на фоне вульварного/промежностного варикоза."
)
pdf.output(f"{OUT}/05_Dzhenina_2019.pdf")
print("  05_Dzhenina_2019.pdf")

# =====================================================================
# 6. Шибельгут Н.М. et al., 2010
# =====================================================================
pdf = make_pdf("Шибельгут Н.М. et al., 2010 — Обзор статьи")
pdf.section_title("Эффективность диосмина 600 мг при профилактике варикозной болезни вен малого таза у беременных")
pdf.bold_text("Авторы:")
pdf.body_text("Шибельгут Н.М., Баскакова Т.Б., Захаров И.С., Мозес В.Г.")
pdf.bold_text("Журнал:")
pdf.body_text("Российский вестник акушера-гинеколога. 2010; 3: 61–66.")
pdf.ref_text("Полный текст: https://medi.ru/info/6662/")
pdf.ln(2)

pdf.sub_title("Дизайн исследования")
pdf.body_text("Рандомизированное плацебо-контролируемое исследование.")

pdf.sub_title("Популяция")

w2 = [95, 85]
pdf.table_row(["Параметр", "Значение"], w2, header=True)
pdf.table_row(["Общее число пациенток", "90 беременных"], w2)
pdf.table_row(["Группа лечения", "30 (диосмин с гесперидином)"], w2)
pdf.table_row(["Группа плацебо", "60"], w2)
pdf.table_row(["Триместр", "III"], w2)
pdf.table_row(["Доза", "600 мг/сут однократно"], w2)
pdf.ln(4)

pdf.sub_title("Оценка эффективности")
pdf.body_text(
    "• 3-и сутки после родов\n"
    "• 6 месяцев после родов"
)

pdf.sub_title("Значимость")
pdf.body_text(
    "Рандомизированное плацебо-контролируемое исследование\n"
    "применения диосмина с гесперидином у беременных в III триместре\n"
    "для профилактики варикозной болезни вен малого таза.\n"
    "Важно как единственное российское РКИ по данной теме."
)
pdf.output(f"{OUT}/06_Shibelgut_2010.pdf")
print("  06_Shibelgut_2010.pdf")

# =====================================================================
# 7. Сучков И.А. et al., 2024 (СТАНДАРТ)
# =====================================================================
pdf = make_pdf("Сучков И.А. et al., 2024 — Обзор статьи")
pdf.section_title("Влияние комбинации гесперидина и диосмина на ремоделирование венозной стенки (исследование «СТАНДАРТ»)")
pdf.bold_text("Авторы:")
pdf.body_text("Сучков И.А., Мжаванадзе Н.Д., Калинин Р.Е., Щулькин А.В., Камаев А.А., Никифоров А.А., Никифорова Л.В., Поваров В.О., Маркитан Г.С., Назимова Е.Ю.")
pdf.bold_text("Журнал:")
pdf.body_text("Флебология. 2024; 18(4): 293–301.")
pdf.ref_text(
    "DOI: 10.17116/flebo202418041293\n"
    "Полный текст: https://www.mediasphera.ru/issues/flebologiya/2024/4/1199769762024041293"
)
pdf.ln(2)

pdf.sub_title("Дизайн")
pdf.body_text("Проспективное контролируемое исследование «СТАНДАРТ».")

pdf.sub_title("Препарат")

w2 = [95, 85]
pdf.table_row(["Компонент", "Значение"], w2, header=True)
pdf.table_row(["Гесперидин", "100 мг"], w2)
pdf.table_row(["Диосмин", "900 мг"], w2)
pdf.table_row(["Общая доза", "1000 мг/сут (1 раз)"], w2)
pdf.table_row(["Курс", "6 месяцев"], w2)
pdf.ln(4)

pdf.sub_title("Маркеры ремоделирования венозной стенки (через 6 мес)")

wm = [85, 50, 40]
pdf.table_row(["Маркер", "Снижение", "p"], wm, header=True)
pdf.table_row(["PAI-1 (ингибитор плазминогена)", ">6-кратное", "<0.001"], wm)
pdf.table_row(["Фибронектин (FN)", ">22-кратное", "<0.001"], wm)
pdf.table_row(["Виментин (VIM)", "2-кратное", "0.042"], wm)
pdf.table_row(["vWF (фактор фон Виллебранда)", "3-кратное", "0.001"], wm)
pdf.table_row(["PECAM-1 (CD31)", "1.5-кратное", "<0.001"], wm)
pdf.ln(4)

pdf.sub_title("Симптомы и качество жизни")

w2 = [95, 85]
pdf.table_row(["Показатель", "Улучшение"], w2, header=True)
pdf.table_row(["ВАШ (боль)", "4-кратное снижение"], w2)
pdf.table_row(["VCSS (тяжесть ХЗВ)", "3-кратное снижение"], w2)
pdf.table_row(["CIVIQ-20 (качество жизни)", ">4-кратное (p<0.001)"], w2)
pdf.ln(4)

pdf.yellow_box(
    "Примечание: беременность и лактация были критериями невключения.\n"
    "Исследование демонстрирует молекулярный механизм действия\n"
    "комбинации диосмина с гесперидином на венозную стенку."
)
pdf.output(f"{OUT}/07_Suchkov_STANDART_2024.pdf")
print("  07_Suchkov_STANDART_2024.pdf")

# =====================================================================
# 8. Sheikh P et al., 2020
# =====================================================================
pdf = make_pdf("Sheikh P et al., 2020 — Обзор статьи")
pdf.section_title("МОФФ (диосмин + гесперидин) при геморрое: систематический обзор и метаанализ")
pdf.bold_text("Авторы:")
pdf.body_text("Sheikh P, Lohsiriwat V, Shelygin Y.")
pdf.bold_text("Оригинальное название:")
pdf.italic_text(
    "Micronized Purified Flavonoid Fraction in Hemorrhoid Disease:\n"
    "A Systematic Review and Meta-Analysis."
)
pdf.bold_text("Журнал:")
pdf.body_text("Advances in Therapy. 2020 Jun; 37(6): 2792-2812.")
pdf.ref_text(
    "PMID: 32399811 | PMC: PMC7467450 (полный текст доступен)\n"
    "DOI: 10.1007/s12325-020-01353-7"
)
pdf.ln(2)

pdf.sub_title("Включено")
pdf.body_text("11 исследований из 13 публикаций (351 уникальная запись).")

pdf.sub_title("Результаты метаанализа (4 исследования)")

w4 = [65, 50, 30, 35]
pdf.table_row(["Параметр", "OR (95% ДИ)", "P", "Эффект"], w4, header=True)
pdf.table_row(["Кровотечение", "0.082 (0.027–0.250)", "<0.001", "↓ 92%"], w4)
pdf.table_row(["Выделения", "0.12 (0.04–0.42)", "<0.001", "↓ 88%"], w4)
pdf.table_row(["Улучшение (пациенты)", "5.25 (2.58–10.68)", "<0.001", "↑ 5.25x"], w4)
pdf.table_row(["Улучшение (врачи)", "5.51 (2.76–11.0)", "<0.001", "↑ 5.51x"], w4)
pdf.table_row(["Боль", "0.11 (0.01–1.11)", "= 0.06", "тренд ↓"], w4)
pdf.ln(4)

pdf.green_box(
    'Вывод: «МОФФ (диосмин + гесперидин) улучшает наиболее важные признаки и симптомы\n'
    'геморроидальной болезни, включая кровотечение, боль, зуд,\n'
    'тенезмы и анальные выделения.»'
)

pdf.sub_title("Значимость")
pdf.body_text(
    "Единственный веноактивный препарат с полным систематическим обзором и метаанализом\n"
    "по геморрою. Полный текст доступен бесплатно в PMC."
)
pdf.output(f"{OUT}/08_Sheikh_MetaAnalysis_2020.pdf")
print("  08_Sheikh_MetaAnalysis_2020.pdf")

# =====================================================================
# 9. Aziz Z et al., 2018
# =====================================================================
pdf = make_pdf("Aziz Z et al., 2018 — Обзор статьи")
pdf.section_title("Эффективность и переносимость МОФФ (диосмин + гесперидин) при геморрое: систематический обзор и метаанализ")
pdf.bold_text("Авторы:")
pdf.body_text("Aziz Z, Huin WK, Badrul Hisham MD, Tang WL, Yaacob S.")
pdf.bold_text("Оригинальное название:")
pdf.italic_text(
    "Efficacy and tolerability of micronized purified flavonoid fractions\n"
    "(MPFF) for haemorrhoids: A systematic review and meta-analysis."
)
pdf.bold_text("Журнал:")
pdf.body_text("Complementary Therapies in Medicine. 2018 Aug; 39: 49-55.")
pdf.ref_text("PMID: 30012392 | DOI: 10.1016/j.ctim.2018.05.011")
pdf.ln(2)

pdf.sub_title("Включено")
pdf.body_text("10 рандомизированных контролируемых исследований (РКИ), 1 164 участника.")

pdf.sub_title("Основной результат")
pdf.body_text(
    "МОФФ (диосмин + гесперидин) значительно улучшает кровотечение:\n"
    "RR 1.46 (95% CI: 1.10–1.93; p = 0.008)."
)

pdf.green_box(
    "Вывод: МОФФ (диосмин + гесперидин) статистически значимо\n"
    "уменьшает кровотечение при геморрое по данным 10 РКИ."
)
pdf.output(f"{OUT}/09_Aziz_MetaAnalysis_2018.pdf")
print("  09_Aziz_MetaAnalysis_2018.pdf")

# =====================================================================
# 10. Santiago FR et al., 2026
# =====================================================================
pdf = make_pdf("Santiago FR et al., 2026 — Обзор статьи")
pdf.section_title("Веноактивные препараты при ХВН: критический анализ доказательств и сравнение с международными гайдлайнами")
pdf.bold_text("Авторы:")
pdf.body_text("Santiago FR, Grillo L, Amore M, Carmelino C, Trejo JMR, Ulloa JH.")
pdf.bold_text("Оригинальное название:")
pdf.italic_text(
    "Venoactive drugs in the management of chronic venous disease:\n"
    "A critical appraisal of the evidence and comparison with\n"
    "international guidelines."
)
pdf.bold_text("Журнал:")
pdf.body_text("Vascular Pharmacology. 2026; 163: 107614.")
pdf.ref_text("PMID: 42066876 | DOI: 10.1016/j.vph.2026.107614")
pdf.ln(2)

pdf.sub_title("Ключевые данные")
pdf.body_text(
    "МОФФ (диосмин + гесперидин) —\n"
    "предпочтительный вариант во всех международных гайдлайнах\n"
    "по ведению хронических заболеваний вен, подкреплённый\n"
    "доказательствами высокого качества.\n\n"
    "Это самый свежий на момент составления обзора анализ\n"
    "позиции МОФФ (диосмин + гесперидин) в международных рекомендациях."
)
pdf.output(f"{OUT}/10_Santiago_2026.pdf")
print("  10_Santiago_2026.pdf")

# =====================================================================
# 11. Gianesini S et al., 2023
# =====================================================================
pdf = make_pdf("Gianesini S et al., 2023 — Обзор статьи")
pdf.section_title("Кардиоваскулярные аспекты ведения хронических заболеваний вен")
pdf.bold_text("Авторы:")
pdf.body_text("Gianesini S, De Luca L, Feodor T, Taha W, Bozkurt K, Lurie F.")
pdf.bold_text("Оригинальное название:")
pdf.italic_text(
    "Cardiovascular Insights for the Appropriate Management\n"
    "of Chronic Venous Disease."
)
pdf.bold_text("Журнал:")
pdf.body_text("Advances in Therapy. 2023 Dec; 40(12): 5137-5154.")
pdf.ref_text(
    "PMID: 37768506 | PMC: PMC10611621\n"
    "DOI: 10.1007/s12325-023-02657-0"
)
pdf.ln(2)

pdf.sub_title("Контекст")
pdf.body_text(
    "Материалы XIX Всемирного Конгресса Международного Союза\n"
    "Флебологии (IUP), Стамбул, сентябрь 2022 г."
)

pdf.sub_title("Ключевые данные")
pdf.body_text(
    "МОФФ (диосмин + гесперидин) — веноактивный препарат\n"
    "с доказательствами высокого качества для:\n"
    "• Облегчения симптомов и признаков ХВН\n"
    "• Улучшения качества жизни пациентов"
)
pdf.output(f"{OUT}/11_Gianesini_2023.pdf")
print("  11_Gianesini_2023.pdf")

# =====================================================================
# 12. Lurie F, Branisteanu DE, 2023
# =====================================================================
pdf = make_pdf("Lurie F, Branisteanu DE, 2023 — Обзор статьи")
pdf.section_title("Улучшение ведения ХВН с помощью МОФФ (диосмин + гесперидин): от клинических исследований к реальной практике")
pdf.bold_text("Авторы:")
pdf.body_text("Lurie F, Branisteanu DE.")
pdf.bold_text("Оригинальное название:")
pdf.italic_text(
    "Improving Chronic Venous Disease Management with Micronised\n"
    "Purified Flavonoid Fraction: New Evidence from Clinical Trials\n"
    "to Real Life."
)
pdf.bold_text("Журнал:")
pdf.body_text("Clinical Drug Investigation. 2023; 43(Suppl 1): 9-13.")
pdf.ref_text(
    "PMID: 37171748 | PMC: PMC10220107\n"
    "DOI: 10.1007/s40261-023-01261-y"
)
pdf.ln(2)

pdf.sub_title("Ключевые данные")
pdf.body_text(
    "• МОФФ (диосмин + гесперидин) высоко рекомендуется в международных гайдлайнах\n"
    "  по ведению ХВН\n\n"
    "• МОФФ (диосмин + гесперидин) является ЕДИНСТВЕННЫМ веноактивным препаратом,\n"
    "  получившим одобрение гайдлайнов для улучшения\n"
    "  качества жизни пациентов\n\n"
    "• Представлены новые данные из реальной клинической практики,\n"
    "  подтверждающие результаты клинических исследований"
)
pdf.output(f"{OUT}/12_Lurie_2023.pdf")
print("  12_Lurie_2023.pdf")

# =====================================================================
# 13. Bouskela E, Lugli M, Nicolaides A, 2022
# =====================================================================
pdf = make_pdf("Bouskela E et al., 2022 — Обзор статьи")
pdf.section_title("Новые перспективы МОФФ (диосмин + гесперидин) при хронических заболеваниях вен")
pdf.bold_text("Авторы:")
pdf.body_text("Bouskela E, Lugli M, Nicolaides A.")
pdf.bold_text("Оригинальное название:")
pdf.italic_text("New Perspectives on Micronised Purified Flavonoid Fraction\nin Chronic Venous Disease.")
pdf.bold_text("Журнал:")
pdf.body_text("Advances in Therapy. 2022 Oct; 39(10): 4413-4422.")
pdf.ref_text(
    "PMID: 35951224 | PMC: PMC9464747\n"
    "DOI: 10.1007/s12325-022-02218-x"
)
pdf.ln(2)

pdf.sub_title("Ключевые данные")
pdf.body_text(
    "Международные гайдлайны по ведению ХВН строго рекомендуют\n"
    "МОФФ (диосмин + гесперидин) для:\n\n"
    "• Уменьшения симптомов хронических заболеваний вен\n"
    "• Улучшения качества жизни пациентов\n\n"
    "Обзор обобщает новые перспективы применения МОФФ (диосмин + гесперидин)\n"
    "на основе актуальных данных."
)
pdf.output(f"{OUT}/13_Bouskela_2022.pdf")
print("  13_Bouskela_2022.pdf")

# =====================================================================
# 14. Li KX et al., 2021
# =====================================================================
pdf = make_pdf("Li KX et al., 2021 — Обзор статьи")
pdf.section_title("МОФФ (диосмин + гесперидин) при хронической венозной недостаточности с фокусом на посттромботический синдром")
pdf.bold_text("Авторы:")
pdf.body_text("Li KX, Diendere G, Galanaud JP, Mahjoub N, Kahn SR.")
pdf.bold_text("Оригинальное название:")
pdf.italic_text(
    "Micronized purified flavonoid fraction for the treatment of chronic\n"
    "venous insufficiency, with a focus on postthrombotic syndrome:\n"
    "A narrative review."
)
pdf.bold_text("Журнал:")
pdf.body_text("Research and Practice in Thrombosis and Haemostasis. 2021 May; 5(4): e12527.")
pdf.ref_text(
    "PMID: 34027293 | PMC: PMC8128666\n"
    "DOI: 10.1002/rth2.12527"
)
pdf.ln(2)

pdf.sub_title("Включено")
pdf.body_text(
    "• 14 систематических обзоров\n"
    "• 33 рандомизированных контролируемых исследования\n"
    "• 19 наблюдательных исследований"
)

pdf.sub_title("Ключевые данные")
pdf.body_text(
    "МОФФ (диосмин + гесперидин) улучшает клинические\n"
    "проявления, качество жизни и объективные венозные параметры\n"
    "хронической венозной недостаточности. Отдельное внимание\n"
    "уделено посттромботическому синдрому."
)
pdf.output(f"{OUT}/14_Li_2021.pdf")
print("  14_Li_2021.pdf")

# =====================================================================
# 15. Cazaubon M et al., 2021
# =====================================================================
pdf = make_pdf("Cazaubon M et al., 2021 — Обзор статьи")
pdf.section_title("Есть ли разница в клинической эффективности диосмина и МОФФ (диосмин + гесперидин) при ХВН?")
pdf.bold_text("Авторы:")
pdf.body_text("Cazaubon M, Benigni JP, Steinbruch M, Jabbour V, Gouhier-Kodas C.")
pdf.bold_text("Оригинальное название:")
pdf.italic_text(
    "Is There a Difference in the Clinical Efficacy of Diosmin\n"
    "and Micronized Purified Flavonoid Fraction for the Treatment\n"
    "of Chronic Venous Disorders?"
)
pdf.bold_text("Журнал:")
pdf.body_text("Vascular Health and Risk Management. 2021 Sep; 17: 591-600.")
pdf.ref_text(
    "PMID: 34556990 | PMC: PMC8455100\n"
    "DOI: 10.2147/VHRM.S324112"
)
pdf.ln(2)

pdf.sub_title("Ключевые данные")
pdf.body_text(
    "• Подтверждает, что МОФФ (диосмин + гесперидин) имеет рекомендацию 1B\n"
    "  (сильная рекомендация, умеренное качество доказательств)\n"
    "  в гайдлайнах по ведению ХВН\n\n"
    "• Анализирует различия между монопрепаратом диосмина\n"
    "  и микронизированной комбинацией диосмин + гесперидин (МОФФ (диосмин + гесперидин))\n\n"
    "• Обосновывает преимущества микронизированной комбинации"
)
pdf.output(f"{OUT}/15_Cazaubon_2021.pdf")
print("  15_Cazaubon_2021.pdf")

# =====================================================================
# 16. ESVS 2022
# =====================================================================
pdf = make_pdf("ESVS 2022 — Обзор гайдлайна")
pdf.section_title("Клинические рекомендации ESVS 2022 по ведению хронических заболеваний вен нижних конечностей")
pdf.bold_text("Источник:")
pdf.body_text("European Society for Vascular Surgery (ESVS).")
pdf.bold_text("Название:")
pdf.italic_text(
    "ESVS 2022 Clinical Practice Guidelines on the Management\n"
    "of Chronic Venous Disease of the Lower Limbs."
)
pdf.bold_text("Журнал:")
pdf.body_text("European Journal of Vascular and Endovascular Surgery. 2022 Feb.")
pdf.ref_text(
    "URL: https://www.ejves.com/article/S1078-5884(21)00979-5/fulltext\n"
    "PDF: https://www.portailvasculaire.fr/sites/default/files/docs/2022_esvs_guidelines_mvc.pdf"
)
pdf.ln(2)

pdf.sub_title("Рекомендации по веноактивным препаратам")
pdf.body_text(
    "• МОФФ (диосмин + гесперидин) имеет НАИВЫСШУЮ степень\n"
    "  рекомендации среди всех веноактивных препаратов\n\n"
    "• Доказательная база: 7 двойных слепых\n"
    "  плацебо-контролируемых РКИ (1 692 пациента)\n\n"
    "• Значительное улучшение:\n"
    "  — симптомов со стороны ног\n"
    "  — функционального дискомфорта\n"
    "  — качества жизни\n"
    "  — окружности лодыжки"
)

pdf.sub_title("Раздел о беременности")
pdf.body_text(
    "Раздел 8.2.2 гайдлайна содержит специфические рекомендации\n"
    "по ведению ХВН при беременности, включая применение\n"
    "веноактивных препаратов."
)

pdf.green_box(
    "МОФФ (диосмин + гесперидин) — рекомендация 1B (самая сильная среди всех веноактивных препаратов)\n"
    "в гайдлайнах ESVS 2022."
)
pdf.output(f"{OUT}/16_ESVS_Guideline_2022.pdf")
print("  16_ESVS_Guideline_2022.pdf")

# =====================================================================
# 17. SVS/AVF/AVLS 2023
# =====================================================================
pdf = make_pdf("SVS/AVF/AVLS 2023 — Обзор гайдлайна")
pdf.section_title("Клинические рекомендации SVS 2023 по ведению варикозной болезни нижних конечностей")
pdf.bold_text("Источник:")
pdf.body_text("Society for Vascular Surgery (SVS), American Venous Forum (AVF), American Vein & Lymphatic Society (AVLS).")
pdf.bold_text("Название:")
pdf.italic_text(
    "2023 Clinical practice guidelines for the management of varicose\n"
    "veins of the lower extremities. Part II."
)
pdf.bold_text("Журнал:")
pdf.body_text("Journal of Vascular Surgery: Venous and Lymphatic Disorders. 2023.")
pdf.ref_text("URL: https://www.jvsvenous.org/article/S2213-333X(23)00322-0/fulltext")
pdf.ln(2)

pdf.sub_title("Ключевые данные")
pdf.body_text(
    "Гайдлайны отдают предпочтение МОФФ (диосмин + гесперидин)\n"
    "и экстрактам Ruscus как наиболее изученным веноактивным\n"
    "препаратам в двойных слепых плацебо-контролируемых РКИ\n"
    "и метаанализах."
)
pdf.output(f"{OUT}/17_SVS_Guideline_2023.pdf")
print("  17_SVS_Guideline_2023.pdf")

# =====================================================================
# 18. Gloviczki ML et al., 2025
# =====================================================================
pdf = make_pdf("Gloviczki ML et al., 2025 — Обзор статьи")
pdf.section_title("Применение веноактивных препаратов при посттромботическом синдроме: систематический обзор")
pdf.bold_text("Авторы:")
pdf.body_text("Gloviczki ML et al.")
pdf.bold_text("Оригинальное название:")
pdf.italic_text(
    "Utility of venoactive compounds in post-thrombotic syndrome:\n"
    "A systematic review."
)
pdf.bold_text("Журнал:")
pdf.body_text("Journal of Vascular Surgery: Venous and Lymphatic Disorders. 2025; 13(4): 102228.")
pdf.ref_text(
    "PMID: 40101859 | PMC: PMC12018987\n"
    "DOI: 10.1016/j.jvsv.2025.102228"
)
pdf.ln(2)

pdf.sub_title("Ключевые данные")
pdf.body_text(
    "Веноактивные препараты (включая МОФФ (диосмин + гесперидин))\n"
    "имеют как минимум умеренное качество доказательств для:\n\n"
    "• Улучшения венозных симптомов\n"
    "• Уменьшения отёка\n"
    "• Ускорения заживления венозных язв\n\n"
    "Систематический обзор с фокусом на посттромботический синдром."
)
pdf.output(f"{OUT}/18_Gloviczki_2025.pdf")
print("  18_Gloviczki_2025.pdf")

print(f"\nВсе 18 PDF сохранены в папку: {OUT}")
