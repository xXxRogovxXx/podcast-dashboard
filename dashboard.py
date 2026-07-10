import streamlit as st
import pandas as pd
import plotly.graph_objects as go
import plotly.express as px
from plotly.subplots import make_subplots
import numpy as np
from datetime import datetime
import base64
from io import BytesIO

# ============================================
# КОНФИГУРАЦИЯ СТРАНИЦЫ
# ============================================
st.set_page_config(layout="wide", page_title="🎙️ Подкаст Аналитика", page_icon="🎙️")

# ============================================
# КАСТОМНЫЕ CSS СТИЛИ - ГИБРИДНЫЙ ДИЗАЙН
# ============================================
st.markdown("""
<style>
    /* ===== ОСНОВНОЙ ФОН ===== */
    .stApp {
        background: #0a0a0f;
        background-image: 
            radial-gradient(ellipse at 10% 20%, rgba(79, 172, 254, 0.05) 0%, transparent 50%),
            radial-gradient(ellipse at 90% 80%, rgba(240, 147, 251, 0.05) 0%, transparent 50%),
            radial-gradient(ellipse at 50% 50%, rgba(245, 87, 108, 0.02) 0%, transparent 70%);
    }
    
    /* ===== ГИБРИДНАЯ СТРУКТУРА: НЕОБРУТАЛИСТСКАЯ СЕТКА ===== */
    .bento-grid {
        display: grid;
        gap: 1.2rem;
        padding: 0.5rem 0;
    }
    
    .bento-grid-2 {
        display: grid;
        grid-template-columns: 1fr 1fr;
        gap: 1.2rem;
    }
    
    .bento-grid-3 {
        display: grid;
        grid-template-columns: 1fr 1fr 1fr;
        gap: 1.2rem;
    }
    
    .bento-grid-4 {
        display: grid;
        grid-template-columns: 1fr 1fr 1fr 1fr;
        gap: 1.2rem;
    }
    
    .bento-grid-6 {
        display: grid;
        grid-template-columns: 1fr 1fr 1fr 1fr 1fr 1fr;
        gap: 1.2rem;
    }
    
    /* ===== LIQUID GLASS КАРТОЧКИ ===== */
    .glass-card {
        background: rgba(255, 255, 255, 0.03);
        backdrop-filter: blur(20px);
        -webkit-backdrop-filter: blur(20px);
        border: 1px solid rgba(255, 255, 255, 0.08);
        border-radius: 20px;
        padding: 1.5rem;
        transition: all 0.4s cubic-bezier(0.25, 0.46, 0.45, 0.94);
        position: relative;
        overflow: hidden;
        box-shadow: 
            0 8px 32px rgba(0, 0, 0, 0.4),
            inset 0 1px 0 rgba(255, 255, 255, 0.05);
    }
    
    .glass-card::before {
        content: '';
        position: absolute;
        top: 0;
        left: 0;
        right: 0;
        bottom: 0;
        background: linear-gradient(
            135deg,
            rgba(255, 255, 255, 0.05) 0%,
            transparent 50%,
            rgba(255, 255, 255, 0.02) 100%
        );
        pointer-events: none;
        border-radius: 20px;
    }
    
    .glass-card:hover {
        transform: translateY(-4px) scale(1.005);
        border-color: rgba(255, 255, 255, 0.15);
        box-shadow: 
            0 16px 48px rgba(0, 0, 0, 0.5),
            inset 0 1px 0 rgba(255, 255, 255, 0.08),
            0 0 60px rgba(79, 172, 254, 0.05);
    }
    
    /* ===== НЕОБРУТАЛИСТСКИЕ АКЦЕНТЫ ===== */
    .brutal-border {
        border: 3px solid #ffffff !important;
        border-radius: 12px !important;
        padding: 1.5rem !important;
        background: rgba(0, 0, 0, 0.6) !important;
        box-shadow: 8px 8px 0 rgba(0, 0, 0, 0.3) !important;
    }
    
    .brutal-accent {
        border-left: 8px solid #f5576c !important;
        border-radius: 4px !important;
        padding: 1rem 1.2rem !important;
        background: rgba(245, 87, 108, 0.05) !important;
    }
    
    .brutal-accent-blue {
        border-left: 8px solid #4facfe !important;
        border-radius: 4px !important;
        padding: 1rem 1.2rem !important;
        background: rgba(79, 172, 254, 0.05) !important;
    }
    
    .brutal-accent-green {
        border-left: 8px solid #43e97b !important;
        border-radius: 4px !important;
        padding: 1rem 1.2rem !important;
        background: rgba(67, 233, 123, 0.05) !important;
    }
    
    /* ===== ТИПОГРАФИКА ===== */
    .main-title {
        font-size: 3.8rem;
        font-weight: 900;
        letter-spacing: -3px;
        background: linear-gradient(135deg, #ffffff 0%, #a8b8ff 50%, #f093fb 100%);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        padding: 0.5rem 0;
        text-align: left;
        text-shadow: none;
        font-family: 'Inter', -apple-system, sans-serif;
    }
    
    .main-title::after {
        content: '';
        display: block;
        width: 80px;
        height: 4px;
        background: linear-gradient(90deg, #f5576c, #f093fb);
        margin-top: 0.5rem;
        border-radius: 2px;
    }
    
    .sub-title {
        color: rgba(255, 255, 255, 0.4);
        font-size: 1rem;
        letter-spacing: 4px;
        font-weight: 400;
        text-transform: uppercase;
        margin-bottom: 2rem;
        font-family: 'Inter', -apple-system, sans-serif;
    }
    
    .section-title {
        font-size: 1.8rem;
        font-weight: 700;
        color: #ffffff;
        padding: 0.5rem 0;
        margin-bottom: 1.2rem;
        font-family: 'Inter', -apple-system, sans-serif;
        letter-spacing: -0.5px;
        border-bottom: 3px solid rgba(245, 87, 108, 0.3);
        display: inline-block;
    }
    
    .section-title::after {
        content: '';
        display: block;
        width: 40px;
        height: 3px;
        background: #f5576c;
        margin-top: 0.3rem;
        border-radius: 2px;
    }
    
    /* ===== МЕТРИКИ В СТИЛЕ LIQUID GLASS ===== */
    .metric-card {
        background: rgba(255, 255, 255, 0.04);
        backdrop-filter: blur(20px);
        -webkit-backdrop-filter: blur(20px);
        border: 1px solid rgba(255, 255, 255, 0.08);
        border-radius: 16px;
        padding: 1.2rem 1rem;
        text-align: center;
        transition: all 0.3s ease;
        position: relative;
        overflow: hidden;
    }
    
    .metric-card::before {
        content: '';
        position: absolute;
        top: -50%;
        left: -50%;
        width: 200%;
        height: 200%;
        background: radial-gradient(circle at 30% 30%, rgba(255,255,255,0.03) 0%, transparent 70%);
        pointer-events: none;
    }
    
    .metric-card:hover {
        transform: translateY(-3px);
        border-color: rgba(255, 255, 255, 0.15);
        box-shadow: 0 12px 40px rgba(0, 0, 0, 0.3);
    }
    
    .metric-icon {
        font-size: 1.6rem;
        margin-bottom: 0.3rem;
        display: block;
    }
    
    .metric-value {
        font-size: 2.2rem;
        font-weight: 700;
        background: linear-gradient(135deg, #ffffff 0%, #a8b8ff 100%);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        font-family: 'Inter', -apple-system, sans-serif;
        letter-spacing: -0.5px;
    }
    
    .metric-label {
        color: rgba(255, 255, 255, 0.5);
        font-size: 0.75rem;
        margin-top: 0.2rem;
        letter-spacing: 1px;
        text-transform: uppercase;
        font-weight: 600;
    }
    
    /* ===== НЕОБРУТАЛИСТСКИЕ КАРТОЧКИ ДЛЯ ТОПОВ ===== */
    .hall-of-fame {
        background: rgba(67, 233, 123, 0.05);
        border: 2px solid rgba(67, 233, 123, 0.2);
        border-radius: 12px;
        padding: 1rem;
        margin-bottom: 0.8rem;
        transition: all 0.3s ease;
        position: relative;
    }
    
    .hall-of-fame:hover {
        border-color: #43e97b;
        transform: translateX(6px);
        box-shadow: 6px 6px 0 rgba(67, 233, 123, 0.1);
    }
    
    .danger-zone {
        background: rgba(245, 87, 108, 0.05);
        border: 2px solid rgba(245, 87, 108, 0.2);
        border-radius: 12px;
        padding: 1rem;
        margin-bottom: 0.8rem;
        transition: all 0.3s ease;
        position: relative;
    }
    
    .danger-zone:hover {
        border-color: #f5576c;
        transform: translateX(6px);
        box-shadow: 6px 6px 0 rgba(245, 87, 108, 0.1);
    }
    
    /* ===== HINT В СТИЛЕ НЕОБРУТАЛИЗМА ===== */
    .hint-block {
        background: rgba(255, 255, 255, 0.03);
        border-left: 8px solid #f093fb;
        padding: 0.8rem 1.2rem;
        margin-bottom: 1rem;
        border-radius: 4px;
        position: relative;
    }
    
    .hint-block strong {
        color: #f093fb;
        font-weight: 700;
        font-size: 0.9rem;
    }
    
    .hint-block span {
        color: rgba(255, 255, 255, 0.5);
        font-size: 0.85rem;
        margin-left: 0.5rem;
    }
    
    /* ===== ВЕРДИКТЫ ===== */
    .verdict-card {
        background: rgba(255, 255, 255, 0.03);
        border: 2px solid rgba(255, 255, 255, 0.1);
        border-radius: 12px;
        padding: 1.2rem;
        text-align: center;
        transition: all 0.3s ease;
    }
    
    .verdict-card:hover {
        transform: scale(1.02);
        border-color: rgba(255, 255, 255, 0.2);
    }
    
    /* ===== ПОДВАЛ ===== */
    .footer {
        text-align: center;
        color: rgba(255, 255, 255, 0.15);
        padding: 2rem 0;
        font-size: 0.7rem;
        letter-spacing: 3px;
        text-transform: uppercase;
        border-top: 1px solid rgba(255, 255, 255, 0.03);
        margin-top: 2rem;
    }
    
    /* ===== ИНФО БЛОК ===== */
    .info-block {
        background: rgba(255, 255, 255, 0.02);
        border: 1px solid rgba(255, 255, 255, 0.05);
        border-radius: 16px;
        padding: 1.5rem;
        backdrop-filter: blur(10px);
    }
    
    .info-title {
        color: #ffffff;
        font-size: 1.1rem;
        font-weight: 700;
        margin-bottom: 1rem;
        letter-spacing: 0.5px;
    }
    
    /* ===== ДАТЫ ===== */
    .important-dates-legend {
        background: rgba(255, 255, 255, 0.03);
        border: 1px solid rgba(255, 255, 255, 0.06);
        border-radius: 12px;
        padding: 0.8rem 1.2rem;
        margin-bottom: 1rem;
        display: flex;
        flex-wrap: wrap;
        gap: 0.8rem;
        align-items: center;
        backdrop-filter: blur(10px);
    }
    
    .date-badge {
        display: inline-flex;
        align-items: center;
        gap: 0.4rem;
        background: rgba(0, 0, 0, 0.3);
        padding: 0.2rem 0.8rem;
        border-radius: 20px;
        font-size: 0.75rem;
        border: 1px solid rgba(255, 255, 255, 0.05);
    }
    
    /* ===== STREAMLIT ОВЕРРАЙДЫ ===== */
    div[data-testid="stExpander"] details summary p {
        color: #f093fb !important;
        font-size: 1.1rem !important;
        font-weight: 700 !important;
    }
    
    div[data-testid="stExpander"] * {
        color: #ffffff !important;
    }
    
    div[role="radiogroup"] label p {
        color: #ffffff !important;
        font-weight: 600 !important;
        font-size: 0.9rem !important;
    }
    
    .stSelectbox label {
        color: rgba(255, 255, 255, 0.7) !important;
        font-weight: 600 !important;
        font-size: 0.9rem !important;
        letter-spacing: 0.5px !important;
    }
    
    /* Адаптивность */
    @media (max-width: 1200px) {
        .bento-grid-6 { grid-template-columns: 1fr 1fr 1fr; }
        .bento-grid-4 { grid-template-columns: 1fr 1fr; }
    }
    
    @media (max-width: 768px) {
        .bento-grid-2 { grid-template-columns: 1fr; }
        .bento-grid-3 { grid-template-columns: 1fr; }
        .bento-grid-4 { grid-template-columns: 1fr; }
        .bento-grid-6 { grid-template-columns: 1fr 1fr; }
        .main-title { font-size: 2.5rem; }
    }
</style>
""", unsafe_allow_html=True)

# ============================================
# ВАЖНЫЕ ДАТЫ
# ============================================
IMPORTANT_DATES = {
    "2025-05-19": {"label": "🎤 Фичеринг 1", "color": "#f093fb", "dash": "dash"},
    "2025-09-15": {"label": "🎤 Фичеринг 2", "color": "#4facfe", "dash": "dot"},
}

def add_important_dates_to_fig(fig, date_column="Дата прослушивания"):
    for date_str, props in IMPORTANT_DATES.items():
        try:
            fig.add_vline(
                x=pd.to_datetime(date_str),
                line_dash=props.get("dash", "dash"),
                line_color=props.get("color", "#f093fb"),
                line_width=2,
                annotation_text=props.get("label", ""),
                annotation_position="top",
                annotation_font=dict(
                    color=props.get("color", "#f093fb"),
                    size=10,
                    family="Inter, sans-serif"
                ),
                annotation_bgcolor="rgba(0,0,0,0.6)",
                layer="below"
            )
        except:
            pass
    return fig

# ============================================
# ПОМОЩНИК ДЛЯ HINT
# ============================================
def show_hint(emoji, title, text):
    st.markdown(f"""
    <div class="hint-block">
        <strong>{emoji} {title}</strong>
        <span>— {text}</span>
    </div>
    """, unsafe_allow_html=True)

# ============================================
# ЭКСПОРТ
# ============================================
def get_pdf_download_link(df, filename="report.pdf"):
    try:
        from reportlab.lib.pagesizes import A4
        from reportlab.platypus import SimpleDocTemplate, Table, TableStyle, Paragraph, Spacer
        from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
        from reportlab.lib import colors
        from reportlab.lib.units import inch
        from reportlab.pdfbase import pdfmetrics
        from reportlab.pdfbase.ttfonts import TTFont
        import tempfile
        import os
        
        font_paths = [
            'DejaVuSans.ttf',
            './DejaVuSans.ttf',
            os.path.join(os.path.dirname(__file__), 'DejaVuSans.ttf'),
            '/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf',
        ]
        
        font_registered = False
        for font_path in font_paths:
            try:
                if os.path.exists(font_path):
                    pdfmetrics.registerFont(TTFont('CyrillicFont', font_path))
                    font_registered = True
                    break
            except:
                continue
        
        font_name = 'CyrillicFont' if font_registered else 'Helvetica'
        
        with tempfile.NamedTemporaryFile(delete=False, suffix='.pdf') as tmp_file:
            pdf_path = tmp_file.name
        
        doc = SimpleDocTemplate(pdf_path, pagesize=A4,
                               rightMargin=72, leftMargin=72,
                               topMargin=72, bottomMargin=72)
        
        styles = getSampleStyleSheet()
        
        title_style = ParagraphStyle(
            'CustomTitle', 
            parent=styles['Heading1'], 
            fontSize=22,
            textColor=colors.HexColor('#f5576c'), 
            spaceAfter=20, 
            alignment=1, 
            fontName=font_name
        )
        
        heading_style = ParagraphStyle(
            'CustomHeading', 
            parent=styles['Heading2'], 
            fontSize=14,
            textColor=colors.HexColor('#4facfe'), 
            spaceAfter=10, 
            spaceBefore=15, 
            fontName=font_name
        )
        
        normal_style = ParagraphStyle(
            'Normal', 
            parent=styles['Normal'], 
            fontSize=10, 
            fontName=font_name
        )
        
        story = []
        
        story.append(Paragraph("🎙️ Подкаст Аналитика — Отчет", title_style))
        story.append(Paragraph(f"📅 Дата: {datetime.now().strftime('%d.%m.%Y %H:%M')}", normal_style))
        story.append(Paragraph(
            f"📊 Период: {df['Дата прослушивания'].min().date()} — {df['Дата прослушивания'].max().date()}", 
            normal_style
        ))
        story.append(Spacer(1, 15))
        
        story.append(Paragraph("📊 Общая статистика", heading_style))
        total_starts = df['Старты'].sum()
        total_streams = df['Стримы'].sum()
        conversion = (total_streams / total_starts * 100) if total_starts > 0 else 0
        avg_listen = df['Средний_прослушивания'].mean() * 100
        avg_completion = df['Дослушиваемость'].mean() * 100
        unique_episodes = df['Выпуск'].nunique()
        
        stats_data = [
            ['Метрика', 'Значение'],
            ['Всего стартов', f'{total_starts:,}'],
            ['Всего стримов', f'{total_streams:,}'],
            ['Конверсия', f'{conversion:.1f}%'],
            ['Средний % прослушивания', f'{avg_listen:.1f}%'],
            ['Средняя дослушиваемость', f'{avg_completion:.1f}%'],
            ['Количество выпусков', f'{unique_episodes}']
        ]
        
        stats_table = Table(stats_data, colWidths=[3*inch, 2.5*inch])
        stats_table.setStyle(TableStyle([
            ('BACKGROUND', (0, 0), (1, 0), colors.HexColor('#4facfe')),
            ('TEXTCOLOR', (0, 0), (1, 0), colors.white),
            ('ALIGN', (0, 0), (1, -1), 'CENTER'),
            ('FONTNAME', (0, 0), (1, -1), font_name),
            ('FONTSIZE', (0, 0), (1, 0), 11),
            ('BOTTOMPADDING', (0, 0), (1, 0), 10),
            ('BACKGROUND', (0, 1), (1, -1), colors.HexColor('#f8f9fa')),
            ('GRID', (0, 0), (1, -1), 1, colors.grey),
            ('FONTSIZE', (0, 1), (1, -1), 9),
            ('VALIGN', (0, 0), (1, -1), 'MIDDLE'),
        ]))
        story.append(stats_table)
        story.append(Spacer(1, 15))
        
        story.append(Paragraph("🏆 Топ выпусков по популярности", heading_style))
        top_episodes = df.groupby(['Выпуск', 'Короткое название']).agg({
            'Старты': 'sum', 'Стримы': 'sum', 'Дослушиваемость': 'mean'
        }).reset_index().sort_values('Старты', ascending=False).head(10)
        
        top_data = [['#', 'Название', 'Старты', 'Стримы', 'Дослуш.']]
        for i, (_, row) in enumerate(top_episodes.iterrows()):
            name = row['Короткое название'][:40] if len(row['Короткое название']) > 40 else row['Короткое название']
            top_data.append([
                str(i+1), 
                name, 
                f"{row['Старты']:,}", 
                f"{row['Стримы']:,}", 
                f"{row['Дослушиваемость']*100:.1f}%"
            ])
        
        top_table = Table(top_data, colWidths=[0.4*inch, 2.8*inch, 1*inch, 1*inch, 1*inch])
        top_table.setStyle(TableStyle([
            ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor('#f5576c')),
            ('TEXTCOLOR', (0, 0), (-1, 0), colors.white),
            ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
            ('FONTNAME', (0, 0), (-1, -1), font_name),
            ('FONTSIZE', (0, 0), (-1, 0), 10),
            ('GRID', (0, 0), (-1, -1), 1, colors.grey),
            ('FONTSIZE', (0, 1), (-1, -1), 8),
            ('VALIGN', (0, 0), (-1, -1), 'MIDDLE'),
        ]))
        story.append(top_table)
        story.append(Spacer(1, 15))
        
        story.append(Paragraph("🏆 Зал славы (лучшая дослушиваемость)", heading_style))
        hall_of_fame = df.groupby(['Выпуск', 'Короткое название']).agg({
            'Дослушиваемость': 'mean', 'Старты': 'sum', 'Средний_прослушивания': 'mean'
        }).reset_index().sort_values('Дослушиваемость', ascending=False).head(10)
        
        hall_data = [['#', 'Название', 'Дослуш.', 'Старты', 'Средний %']]
        for i, (_, row) in enumerate(hall_of_fame.iterrows()):
            name = row['Короткое название'][:40] if len(row['Короткое название']) > 40 else row['Короткое название']
            hall_data.append([
                str(i+1), 
                name, 
                f"{row['Дослушиваемость']*100:.1f}%", 
                f"{row['Старты']:,}", 
                f"{row['Средний_прослушивания']*100:.1f}%"
            ])
        
        hall_table = Table(hall_data, colWidths=[0.4*inch, 2.8*inch, 1*inch, 1*inch, 1*inch])
        hall_table.setStyle(TableStyle([
            ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor('#43e97b')),
            ('TEXTCOLOR', (0, 0), (-1, 0), colors.white),
            ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
            ('FONTNAME', (0, 0), (-1, -1), font_name),
            ('FONTSIZE', (0, 0), (-1, 0), 10),
            ('GRID', (0, 0), (-1, -1), 1, colors.grey),
            ('FONTSIZE', (0, 1), (-1, -1), 8),
            ('VALIGN', (0, 0), (-1, -1), 'MIDDLE'),
        ]))
        story.append(hall_table)
        story.append(Spacer(1, 15))
        
        story.append(Paragraph("⚠️ Зона риска (худшая дослушиваемость)", heading_style))
        danger_zone = df.groupby(['Выпуск', 'Короткое название']).agg({
            'Дослушиваемость': 'mean', 'Старты': 'sum', 'Средний_прослушивания': 'mean'
        }).reset_index().sort_values('Дослушиваемость', ascending=True).head(10)
        
        danger_data = [['#', 'Название', 'Дослуш.', 'Старты', 'Средний %']]
        for i, (_, row) in enumerate(danger_zone.iterrows()):
            name = row['Короткое название'][:40] if len(row['Короткое название']) > 40 else row['Короткое название']
            danger_data.append([
                str(i+1), 
                name, 
                f"{row['Дослушиваемость']*100:.1f}%", 
                f"{row['Старты']:,}", 
                f"{row['Средний_прослушивания']*100:.1f}%"
            ])
        
        danger_table = Table(danger_data, colWidths=[0.4*inch, 2.8*inch, 1*inch, 1*inch, 1*inch])
        danger_table.setStyle(TableStyle([
            ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor('#f5576c')),
            ('TEXTCOLOR', (0, 0), (-1, 0), colors.white),
            ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
            ('FONTNAME', (0, 0), (-1, -1), font_name),
            ('FONTSIZE', (0, 0), (-1, 0), 10),
            ('GRID', (0, 0), (-1, -1), 1, colors.grey),
            ('FONTSIZE', (0, 1), (-1, -1), 8),
            ('VALIGN', (0, 0), (-1, -1), 'MIDDLE'),
        ]))
        story.append(danger_table)
        story.append(Spacer(1, 15))
        
        footer_style = ParagraphStyle(
            'Footer', 
            parent=styles['Normal'], 
            fontSize=8, 
            textColor=colors.grey, 
            alignment=1, 
            fontName=font_name
        )
        story.append(Paragraph("🎙️ Подкаст Аналитика Pro • Сгенерировано автоматически", footer_style))
        
        doc.build(story)
        
        with open(pdf_path, 'rb') as f:
            pdf_data = f.read()
        os.unlink(pdf_path)
        
        b64 = base64.b64encode(pdf_data).decode()
        href = f'<a href="data:application/pdf;base64,{b64}" download="{filename}" style="display: inline-block; background: linear-gradient(135deg, #4facfe, #f093fb); color: white; padding: 12px 30px; border-radius: 8px; text-decoration: none; font-weight: 600; font-size: 1rem; transition: all 0.3s ease; border: 2px solid rgba(255,255,255,0.1);">📥 Скачать отчет (PDF)</a>'
        return href
        
    except Exception as e:
        try:
            csv = df.to_csv(index=False).encode('utf-8')
            b64 = base64.b64encode(csv).decode()
            return f'<a href="data:file/csv;base64,{b64}" download="{filename}" style="display: inline-block; background: linear-gradient(135deg, #4facfe, #f093fb); color: white; padding: 12px 30px; border-radius: 8px; text-decoration: none; font-weight: 600; font-size: 1rem; border: 2px solid rgba(255,255,255,0.1);">📥 Скачать отчет (CSV)</a>'
        except:
            return f"<span style='color: #f5576c;'>⚠️ Ошибка генерации: {str(e)}</span>"

def get_csv_download_link(df, filename="report.csv"):
    try:
        csv = df.to_csv(index=False).encode('utf-8')
        b64 = base64.b64encode(csv).decode()
        return f'<a href="data:file/csv;base64,{b64}" download="{filename}" style="display: inline-block; background: linear-gradient(135deg, #4facfe, #f093fb); color: white; padding: 12px 30px; border-radius: 8px; text-decoration: none; font-weight: 600; font-size: 1rem; border: 2px solid rgba(255,255,255,0.1);">📥 Скачать отчет (CSV)</a>'
    except Exception as e:
        return f"<span style='color: #f5576c;'>⚠️ Ошибка: {str(e)}</span>"

# ============================================
# ЗАГРУЗКА ДАННЫХ
# ============================================
@st.cache_data
def load_data():
    try:
        df_total = pd.read_excel("Общая.xlsx", sheet_name="Общая")
        df_ref = pd.read_excel("Спр.xlsx", sheet_name="Спр")
        
        try:
            df_short = pd.read_excel("Короткие названия.xlsx")
            short_names_dict = dict(zip(df_short['Оригинальное название'], df_short['Короткое название']))
        except:
            short_names_dict = {}
        
        df_total['Дата прослушивания'] = pd.to_datetime(df_total['Дата прослушивания'])
        df_ref['Дата релиза'] = pd.to_datetime(df_ref['Дата релиза'])
        df_ref['Короткое название'] = df_ref['Выпуск'].map(short_names_dict).fillna(df_ref['Выпуск'])
        
        if 'Средний % прослушивания' in df_total.columns:
            df_total['Средний_прослушивания'] = df_total['Средний % прослушивания'].fillna(0)
        else:
            df_total['Средний_прослушивания'] = 0
            
        if '% дослушиваемости' in df_total.columns:
            df_total['Дослушиваемость'] = df_total['% дослушиваемости'].fillna(0)
        else:
            df_total['Дослушиваемость'] = 0
        
        return df_total, df_ref, short_names_dict
    except Exception as e:
        st.error(f"❌ Ошибка загрузки данных: {e}")
        st.stop()

with st.spinner("🔄 Загрузка данных..."):
    df_total, df_ref, short_names_dict = load_data()

df_merged = df_total.merge(df_ref, on='Выпуск', how='left')

if 'Средний_прослушивания' not in df_merged.columns:
    df_merged['Средний_прослушивания'] = 0
else:
    df_merged['Средний_прослушивания'] = df_merged['Средний_прослушивания'].fillna(0)

if 'Дослушиваемость' not in df_merged.columns:
    df_merged['Дослушиваемость'] = 0
else:
    df_merged['Дослушиваемость'] = df_merged['Дослушиваемость'].fillna(0)

# ============================================
# RSI
# ============================================
def calculate_rsi(df):
    df = df.copy()
    df['Конверсия_доля'] = df['Стримы'] / df['Старты']
    df['Конверсия_доля'] = df['Конверсия_доля'].fillna(0).replace([np.inf, -np.inf], 0)
    df['RSI'] = df['Стримы'] * (df['Конверсия_доля'] + 1) * (df['Старты'] ** 0.1)
    return df

df_merged = calculate_rsi(df_merged)

def get_short_name(long_name):
    return short_names_dict.get(long_name, long_name)

# ============================================
# ВСПОМОГАТЕЛЬНЫЕ
# ============================================
def get_episode_position(episode_data, all_data, metric):
    if metric in ['Старты', 'Стримы']:
        episode_value = episode_data[metric].sum()
    else:
        episode_value = episode_data[metric].mean()
    
    if metric in ['Старты', 'Стримы']:
        all_values = all_data.groupby('Выпуск')[metric].sum()
    else:
        all_values = all_data.groupby('Выпуск')[metric].mean()
    
    mean_value = all_values.mean()
    median_value = all_values.median()
    
    if episode_value > mean_value * 1.1:
        status = "🔼 Значительно выше среднего"
        color = "#43e97b"
    elif episode_value > mean_value:
        status = "🔼 Выше среднего"
        color = "#4facfe"
    elif episode_value > mean_value * 0.9:
        status = "➖ На уровне среднего"
        color = "#f6d365"
    else:
        status = "🔽 Ниже среднего"
        color = "#f5576c"
    
    return {
        'value': episode_value,
        'mean': mean_value,
        'median': median_value,
        'status': status,
        'color': color,
        'diff_percent': ((episode_value - mean_value) / mean_value * 100)
    }

def get_funnel_data(episode_data):
    total_starts = episode_data['Старты'].sum()
    avg_listen = episode_data['Средний_прослушивания'].mean() if 'Средний_прослушивания' in episode_data.columns else 0
    completion = episode_data['Дослушиваемость'].mean() if 'Дослушиваемость' in episode_data.columns else 0
    
    if pd.isna(avg_listen): avg_listen = 0
    if pd.isna(completion): completion = 0
    
    stage_1 = total_starts
    stage_2 = total_starts * avg_listen if total_starts > 0 else 0
    stage_3 = total_starts * completion if total_starts > 0 else 0
    
    return {
        'total_starts': total_starts,
        'avg_listen': avg_listen,
        'completion': completion,
        'stage_1': stage_1,
        'stage_2': stage_2,
        'stage_3': stage_3,
        'has_data': total_starts > 0 and (avg_listen > 0 or completion > 0)
    }

def get_life_curve(episode_data, release_date):
    episode_data = episode_data.sort_values('Дата прослушивания')
    episode_data['День от релиза'] = (episode_data['Дата прослушивания'] - release_date).dt.days + 1
    
    daily = episode_data.groupby('День от релиза').agg({
        'Стримы': 'sum',
        'Старты': 'sum'
    }).reset_index()
    
    daily['Стримы_накоп'] = daily['Стримы'].cumsum()
    daily['Старты_накоп'] = daily['Старты'].cumsum()
    
    total_streams = daily['Стримы'].sum()
    if total_streams > 0:
        daily['Стримы_норм'] = (daily['Стримы_накоп'] / total_streams * 100).round(1)
    else:
        daily['Стримы_норм'] = 0
    
    return daily

def get_life_curve_for_period(episode_name, df_merged, period_days=None):
    episode_data = df_merged[df_merged['Выпуск'] == episode_name].copy()
    if episode_data.empty:
        return None
    release_date = episode_data['Дата прослушивания'].min()
    if period_days is not None:
        episode_data = episode_data[episode_data['Дата прослушивания'] <= release_date + pd.Timedelta(days=period_days - 1)]
    return get_life_curve(episode_data, release_date)

def show_important_dates_legend():
    if IMPORTANT_DATES:
        legend_html = '<div class="important-dates-legend">'
        legend_html += '<span style="color: rgba(255,255,255,0.5); font-size: 0.8rem; letter-spacing: 1px;">📅 ВАЖНЫЕ ДАТЫ</span>'
        for date_str, props in IMPORTANT_DATES.items():
            date_obj = pd.to_datetime(date_str)
            legend_html += f'<span class="date-badge">'
            legend_html += f'<span style="color: {props["color"]}; font-size: 1.2rem;">●</span>'
            legend_html += f'<span style="color: rgba(255,255,255,0.8);">{props["label"]}</span>'
            legend_html += f'<span style="color: rgba(255,255,255,0.3); font-size: 0.7rem;">{date_obj.strftime("%d.%m.%Y")}</span>'
            legend_html += '</span>'
        legend_html += '</div>'
        st.markdown(legend_html, unsafe_allow_html=True)

# ============================================
# ФОРМИРОВАНИЕ СПИСКА ВЫПУСКОВ
# ============================================
chronological_episodes = df_ref['Выпуск'].tolist()
episode_names_ordered = {}
short_names_ordered = []

for ep in chronological_episodes:
    short = get_short_name(ep)
    if short not in episode_names_ordered:
        episode_names_ordered[short] = ep
        short_names_ordered.append(short)

# ============================================
# ЗАГОЛОВОК
# ============================================
st.markdown('<div class="main-title">🎙️ Подкаст Аналитика</div>', unsafe_allow_html=True)
st.markdown('<div class="sub-title">Премиум дашборд • Аналитика прослушиваний • Тренды</div>', unsafe_allow_html=True)

# ============================================
# НАВИГАЦИЯ
# ============================================
page = st.sidebar.radio("📊 Меню", ["📊 Общая аналитика", "📋 Анализ выпуска", "🔄 Сравнение выпусков"], index=0)

with st.sidebar:
    st.markdown("---")
    st.markdown('<span style="color: rgba(255,255,255,0.4); font-size: 0.7rem; letter-spacing: 2px; text-transform: uppercase;">📅 Важные даты</span>', unsafe_allow_html=True)
    for date_str, props in IMPORTANT_DATES.items():
        date_obj = pd.to_datetime(date_str)
        st.markdown(f'<div style="display: flex; align-items: center; gap: 0.5rem; padding: 0.2rem 0;"><span style="color: {props["color"]}; font-size: 1.2rem;">●</span><span style="color: rgba(255,255,255,0.7); font-size: 0.8rem;">{props["label"]}</span><span style="color: rgba(255,255,255,0.3); font-size: 0.7rem;">{date_obj.strftime("%d.%m.%Y")}</span></div>', unsafe_allow_html=True)
    st.markdown("---")

# ============================================
# СТРАНИЦА 1: ОБЩАЯ АНАЛИТИКА
# ============================================
if page == "📊 Общая аналитика":
    with st.sidebar:
        st.markdown('<span style="color: rgba(255,255,255,0.4); font-size: 0.7rem; letter-spacing: 2px; text-transform: uppercase;">🎯 Фильтры</span>', unsafe_allow_html=True)
        st.markdown("---")
        min_date = df_total['Дата прослушивания'].min().date()
        max_date = df_total['Дата прослушивания'].max().date()
        date_range = st.date_input("📅 Период", value=(min_date, max_date), min_value=min_date, max_value=max_date)
        st.markdown("---")
        formats = ['Все'] + list(df_ref['Формат'].unique())
        selected_format = st.selectbox("📂 Формат", formats)
        genres = ['Все'] + list(df_ref['Жанр'].unique())
        selected_genre = st.selectbox("🎭 Жанр", genres)
        st.markdown("---")
        st.markdown('<span style="color: rgba(255,255,255,0.3); font-size: 0.7rem;">📊 Статистика</span>', unsafe_allow_html=True)
        st.caption(f"**Записей:** {len(df_total):,}")
        st.caption(f"**Период:** {min_date} — {max_date}")
        st.caption(f"**Выпусков:** {len(df_ref):,}")

    filtered_data = df_merged.copy()

    if len(date_range) == 2:
        filtered_data = filtered_data[
            (filtered_data['Дата прослушивания'].dt.date >= date_range[0]) &
            (filtered_data['Дата прослушивания'].dt.date <= date_range[1])
        ]

    if selected_format != 'Все':
        filtered_data = filtered_data[filtered_data['Формат'] == selected_format]

    if selected_genre != 'Все':
        filtered_data = filtered_data[filtered_data['Жанр'] == selected_genre]

    show_important_dates_legend()

    # ===== КНОПКА ЭКСПОРТА =====
    col_export, col_export2 = st.columns([1, 5])
    with col_export:
        if st.button("🔄 Сгенерировать отчет", use_container_width=True):
            with st.spinner("Генерация отчета..."):
                download_link = get_pdf_download_link(filtered_data)
                st.markdown(download_link, unsafe_allow_html=True)
    st.markdown("---")
    
    total_starts = filtered_data['Старты'].sum()
    total_streams = filtered_data['Стримы'].sum()
    conversion = (total_streams / total_starts * 100) if total_starts > 0 else 0
    unique_episodes = filtered_data['Выпуск'].nunique()
    avg_rsi = filtered_data['RSI'].mean()
    avg_listen_all = filtered_data['Средний_прослушивания'].mean()

    # ===== МЕТРИКИ В BENTO GRID =====
    st.markdown('<div class="bento-grid-6">', unsafe_allow_html=True)
    cols = st.columns(6)
    
    metrics_data = [
        (cols[0], "🎬", f"{total_starts:,}", "Всего стартов"),
        (cols[1], "🎧", f"{total_streams:,}", "Всего стримов"),
        (cols[2], "📈", f"{conversion:.1f}%", "Конверсия"),
        (cols[3], "📝", f"{unique_episodes}", "Выпусков"),
        (cols[4], "⭐", f"{avg_rsi:.1f}", "Средний RSI"),
        (cols[5], "🎯", f"{avg_listen_all:.1f}%", "Средний %")
    ]
    
    for col, icon, value, label in metrics_data:
        with col:
            st.markdown(f"""
            <div class="metric-card">
                <span class="metric-icon">{icon}</span>
                <div class="metric-value">{value}</div>
                <div class="metric-label">{label}</div>
            </div>
            """, unsafe_allow_html=True)
    st.markdown('</div>', unsafe_allow_html=True)

    st.markdown("---")

    # ===== ИНФО БЛОК =====
    st.markdown("""
    <div class="info-block">
        <div class="info-title">📖 Что означают метрики</div>
        <div style="display: grid; grid-template-columns: 1fr 1fr 1fr; gap: 1rem;">
            <div><div style="color: #4facfe; font-weight: 700; font-size: 1rem; margin-bottom: 0.3rem;">🎬 Старты</div><div style="color: rgba(255,255,255,0.5); font-size: 0.85rem;">Количество запусков выпуска</div></div>
            <div><div style="color: #f5576c; font-weight: 700; font-size: 1rem; margin-bottom: 0.3rem;">🎧 Стримы</div><div style="color: rgba(255,255,255,0.5); font-size: 0.85rem;">Прослушивания > 2 минут</div></div>
            <div><div style="color: #43e97b; font-weight: 700; font-size: 1rem; margin-bottom: 0.3rem;">📈 Конверсия</div><div style="color: rgba(255,255,255,0.5); font-size: 0.85rem;">Стримы / Старты × 100%</div></div>
            <div style="grid-column: span 3; margin-top: 0.5rem; padding-top: 0.8rem; border-top: 1px solid rgba(255,255,255,0.05);">
                <div style="color: #f093fb; font-weight: 700; font-size: 1rem; margin-bottom: 0.3rem;">⭐ RSI — Индекс успешности выпуска</div>
                <div style="color: rgba(255,255,255,0.5); font-size: 0.85rem;"><strong style="color: #f5576c;">Стримы</strong> × (<strong style="color: #43e97b;">Конверсия</strong> + 1) × <strong style="color: #4facfe;">Старты<sup>0.1</sup></strong></div>
            </div>
            <div style="grid-column: span 3; margin-top: 0.5rem; padding-top: 0.8rem; border-top: 1px solid rgba(255,255,255,0.05);">
                <div style="color: #f6d365; font-weight: 700; font-size: 1rem; margin-bottom: 0.3rem;">🎯 Средний % прослушивания</div><div style="color: rgba(255,255,255,0.5); font-size: 0.85rem;">Доля выпуска, которую в среднем слушает аудитория</div>
            </div>
            <div style="grid-column: span 3; margin-top: 0.5rem; padding-top: 0.8rem; border-top: 1px solid rgba(255,255,255,0.05);">
                <div style="color: #43e97b; font-weight: 700; font-size: 1rem; margin-bottom: 0.3rem;">🏁 % дослушиваемости</div><div style="color: rgba(255,255,255,0.5); font-size: 0.85rem;">Доля пользователей, прослушавших 90+% выпуска</div>
            </div>
        </div>
    </div>
    """, unsafe_allow_html=True)

    # ===== ДИНАМИКА =====
    st.markdown('<div class="section-title">📊 Динамика прослушиваний</div>', unsafe_allow_html=True)
    show_hint("💡", "Как читать", "Синяя линия — запуски. Красная — прослушивания >2 минут. Зеленая (пунктир) — конверсия. Смотрите на разрыв: чем он меньше — тем лучше держите внимание.")

    daily_stats = filtered_data.groupby('Дата прослушивания').agg({'Старты': 'sum', 'Стримы': 'sum'}).reset_index()
    daily_stats['Конверсия'] = (daily_stats['Стримы'] / daily_stats['Старты'] * 100).fillna(0)

    fig1 = make_subplots(specs=[[{"secondary_y": True}]])
    fig1.add_trace(go.Scatter(x=daily_stats['Дата прослушивания'], y=daily_stats['Старты'], name='Старты', line=dict(color='#4facfe', width=3), fill='tozeroy', fillcolor='rgba(79, 172, 254, 0.1)', mode='lines+markers', marker=dict(size=6, color='white', line=dict(color='#4facfe', width=1.5))))
    fig1.add_trace(go.Scatter(x=daily_stats['Дата прослушивания'], y=daily_stats['Стримы'], name='Стримы', line=dict(color='#f5576c', width=3), fill='tozeroy', fillcolor='rgba(245, 87, 108, 0.1)', mode='lines+markers', marker=dict(size=6, color='white', line=dict(color='#f5576c', width=1.5))))
    fig1.add_trace(go.Scatter(x=daily_stats['Дата прослушивания'], y=daily_stats['Конверсия'], name='Конверсия (%)', line=dict(color='#43e97b', width=2, dash='dash'), mode='lines+markers', marker=dict(size=5, color='#43e97b')), secondary_y=True)
    
    fig1 = add_important_dates_to_fig(fig1)
    
    fig1.update_layout(
        template='plotly_dark',
        plot_bgcolor='rgba(0,0,0,0)',
        paper_bgcolor='rgba(0,0,0,0)',
        height=450,
        hovermode='x unified',
        legend=dict(orientation='h', yanchor='bottom', y=1.02, xanchor='right', x=1, font=dict(color='rgba(255,255,255,0.7)', size=11)),
        xaxis=dict(title='Дата', titlefont=dict(color='rgba(255,255,255,0.5)', size=12), tickfont=dict(color='rgba(255,255,255,0.5)'), gridcolor='rgba(255,255,255,0.05)'),
        yaxis=dict(title='Количество', titlefont=dict(color='rgba(255,255,255,0.5)'), tickfont=dict(color='rgba(255,255,255,0.5)'), gridcolor='rgba(255,255,255,0.05)'),
        yaxis2=dict(title='Конверсия (%)', titlefont=dict(color='#43e97b'), tickfont=dict(color='#43e97b'), overlaying='y', side='right', showgrid=False)
    )
    st.plotly_chart(fig1, use_container_width=True)

    # ===== МАТРИЦА =====
    st.markdown("---")
    st.markdown('<div class="section-title">🎯 Матрица качества и популярности</div>', unsafe_allow_html=True)
    show_hint("💡", "Как читать", "Каждый кружок — выпуск. Чем правее — тем популярнее. Чем выше — тем качественнее. Зеленые кружки — хиты, красные — зона риска.")

    heatmap_data = filtered_data.groupby(['Выпуск', 'Короткое название']).agg({
        'Старты': 'sum', 'Стримы': 'sum', 'Средний_прослушивания': 'mean',
        'Дослушиваемость': 'mean', 'RSI': 'mean'
    }).reset_index()
    heatmap_data = heatmap_data[heatmap_data['Старты'] >= 10]

    if not heatmap_data.empty:
        fig_heatmap = go.Figure()
        fig_heatmap.add_trace(go.Scatter(
            x=heatmap_data['Старты'], y=heatmap_data['Дослушиваемость'] * 100,
            mode='markers+text', text=heatmap_data['Короткое название'], textposition='top center',
            textfont=dict(color='rgba(255,255,255,0.7)', size=9),
            marker=dict(
                size=heatmap_data['Средний_прослушивания'] * 25 + 8,
                color=heatmap_data['RSI'], colorscale='Viridis', showscale=True,
                colorbar=dict(title='RSI', titlefont=dict(color='rgba(255,255,255,0.5)'), tickfont=dict(color='rgba(255,255,255,0.5)')),
                line=dict(color='rgba(255,255,255,0.2)', width=1), sizemode='area',
                sizeref=2.*max(heatmap_data['Средний_прослушивания'] * 25 + 8)/(40.**2), sizemin=4
            ),
            hovertemplate='<b>%{text}</b><br>Старты: %{x:,.0f}<br>Дослушиваемость: %{y:.1f}%<br>RSI: %{marker.color:.1f}<extra></extra>'
        ))
        
        median_starts = heatmap_data['Старты'].median()
        median_completion = heatmap_data['Дослушиваемость'].median() * 100
        fig_heatmap.add_hline(y=median_completion, line_dash="dash", line_color="rgba(255,255,255,0.15)", line_width=1)
        fig_heatmap.add_vline(x=median_starts, line_dash="dash", line_color="rgba(255,255,255,0.15)", line_width=1)
        
        max_x = heatmap_data['Старты'].max(); max_y = heatmap_data['Дослушиваемость'].max() * 100
        fig_heatmap.add_annotation(x=max_x * 0.85, y=max_y * 0.85, text="⭐ ХИТЫ", showarrow=False, font=dict(color='#43e97b', size=16, family='Inter, sans-serif', weight=900), opacity=0.4)
        fig_heatmap.add_annotation(x=max_x * 0.15, y=max_y * 0.85, text="💎 НИШЕВЫЕ", showarrow=False, font=dict(color='#4facfe', size=16, family='Inter, sans-serif', weight=900), opacity=0.4)
        fig_heatmap.add_annotation(x=max_x * 0.85, y=max_y * 0.15, text="📊 МАССОВЫЕ", showarrow=False, font=dict(color='#f6d365', size=16, family='Inter, sans-serif', weight=900), opacity=0.4)
        fig_heatmap.add_annotation(x=max_x * 0.15, y=max_y * 0.15, text="❌ ПРОВАЛЫ", showarrow=False, font=dict(color='#f5576c', size=16, family='Inter, sans-serif', weight=900), opacity=0.4)
        
        fig_heatmap.update_layout(
            template='plotly_dark',
            plot_bgcolor='rgba(0,0,0,0)',
            paper_bgcolor='rgba(0,0,0,0)',
            height=500,
            hovermode='closest',
            xaxis=dict(title='Старты (популярность)', titlefont=dict(color='rgba(255,255,255,0.5)'), tickfont=dict(color='rgba(255,255,255,0.5)'), gridcolor='rgba(255,255,255,0.05)', type='log'),
            yaxis=dict(title='Дослушиваемость % (качество)', titlefont=dict(color='rgba(255,255,255,0.5)'), tickfont=dict(color='rgba(255,255,255,0.5)'), gridcolor='rgba(255,255,255,0.05)', range=[0, 105]),
            legend=dict(orientation='h', yanchor='bottom', y=1.02, xanchor='right', x=1, font=dict(color='rgba(255,255,255,0.5)'))
        )
        st.plotly_chart(fig_heatmap, use_container_width=True)
    else:
        st.info("ℹ️ Недостаточно данных для построения матрицы (нужно минимум 10 стартов на выпуск)")

    # ===== ЗАЛ СЛАВЫ / ЗОНА РИСКА =====
    st.markdown("---")
    st.markdown('<div class="section-title">🏆 Зал славы и ⚠️ Зона риска</div>', unsafe_allow_html=True)
    show_hint("💡", "Что это", "Зал славы — выпуски с лучшей дослушиваемостью. Зона риска — с худшей. Берите пример с первых, разбирайте вторые.")

    hall_data = filtered_data.groupby(['Выпуск', 'Короткое название']).agg({
        'Старты': 'sum', 'Стримы': 'sum', 'Дослушиваемость': 'mean',
        'Средний_прослушивания': 'mean', 'RSI': 'mean'
    }).reset_index()
    hall_data = hall_data[hall_data['Старты'] >= 10]

    if not hall_data.empty:
        hall_of_fame = hall_data.sort_values('Дослушиваемость', ascending=False).head(5)
        danger_zone = hall_data.sort_values('Дослушиваемость', ascending=True).head(5)
        
        col1, col2 = st.columns(2)
        with col1:
            st.markdown("""<div style="text-align: left; margin-bottom: 1rem;"><span style="font-size: 1.5rem; font-weight: 700; color: #43e97b;">🏆 Зал славы</span><span style="font-size: 0.8rem; color: rgba(255,255,255,0.3); margin-left: 0.5rem; letter-spacing: 1px;">ЛУЧШАЯ ДОСЛУШИВАЕМОСТЬ</span></div>""", unsafe_allow_html=True)
            for i, (_, row) in enumerate(hall_of_fame.iterrows()):
                medal = ['🥇', '🥈', '🥉', '4️⃣', '5️⃣'][i]
                st.markdown(f"""
                <div class="hall-of-fame">
                    <div style="display: flex; justify-content: space-between; align-items: center;">
                        <div>
                            <span style="font-size: 1.2rem;">{medal}</span>
                            <span style="color: white; font-weight: 600; margin-left: 0.5rem;">{row['Короткое название']}</span>
                        </div>
                        <div style="text-align: right;">
                            <span style="color: #43e97b; font-weight: 700; font-size: 1.2rem;">{row['Дослушиваемость']*100:.1f}%</span>
                            <span style="color: rgba(255,255,255,0.3); font-size: 0.7rem; margin-left: 0.5rem;">{row['Старты']:,} стартов</span>
                        </div>
                    </div>
                    <div style="display: flex; gap: 1rem; margin-top: 0.3rem; font-size: 0.75rem; color: rgba(255,255,255,0.3);">
                        <span>🎯 Средний %: {row['Средний_прослушивания']*100:.1f}%</span>
                        <span>⭐ RSI: {row['RSI']:.1f}</span>
                    </div>
                </div>
                """, unsafe_allow_html=True)
        
        with col2:
            st.markdown("""<div style="text-align: left; margin-bottom: 1rem;"><span style="font-size: 1.5rem; font-weight: 700; color: #f5576c;">⚠️ Зона риска</span><span style="font-size: 0.8rem; color: rgba(255,255,255,0.3); margin-left: 0.5rem; letter-spacing: 1px;">ХУДШАЯ ДОСЛУШИВАЕМОСТЬ</span></div>""", unsafe_allow_html=True)
            for i, (_, row) in enumerate(danger_zone.iterrows()):
                st.markdown(f"""
                <div class="danger-zone">
                    <div style="display: flex; justify-content: space-between; align-items: center;">
                        <div>
                            <span style="font-size: 1.2rem;">{'⚠️' if i < 3 else '📌'}</span>
                            <span style="color: white; font-weight: 600; margin-left: 0.5rem;">{row['Короткое название']}</span>
                        </div>
                        <div style="text-align: right;">
                            <span style="color: #f5576c; font-weight: 700; font-size: 1.2rem;">{row['Дослушиваемость']*100:.1f}%</span>
                            <span style="color: rgba(255,255,255,0.3); font-size: 0.7rem; margin-left: 0.5rem;">{row['Старты']:,} стартов</span>
                        </div>
                    </div>
                    <div style="display: flex; gap: 1rem; margin-top: 0.3rem; font-size: 0.75rem; color: rgba(255,255,255,0.3);">
                        <span>🎯 Средний %: {row['Средний_прослушивания']*100:.1f}%</span>
                        <span>⭐ RSI: {row['RSI']:.1f}</span>
                    </div>
                </div>
                """, unsafe_allow_html=True)
    else:
        st.info("ℹ️ Недостаточно данных для Зала славы и Зоны риска (нужно минимум 10 стартов на выпуск)")

    # ===== ТОП RSI =====
    st.markdown("---")
    st.markdown('<div class="section-title">🏆 Топ выпусков по RSI</div>', unsafe_allow_html=True)
    show_hint("💡", "Что такое RSI", "Индекс успешности выпуска. Чем выше — тем лучше выпуск по всем параметрам.")

    episode_rsi = filtered_data.groupby(['Выпуск', 'Короткое название']).agg({
        'Старты': 'sum', 'Стримы': 'sum', 'RSI': 'mean'
    }).reset_index()
    episode_rsi['Конверсия'] = (episode_rsi['Стримы'] / episode_rsi['Старты'] * 100).fillna(0)
    episode_rsi = episode_rsi.sort_values('RSI', ascending=False)
    top_rsi = episode_rsi.head(10)

    col1, col2 = st.columns([2, 1])
    with col1:
        display_names = top_rsi['Короткое название'].tolist()
        fig2 = go.Figure()
        fig2.add_trace(go.Bar(
            x=display_names, y=top_rsi['RSI'],
            marker=dict(color=top_rsi['RSI'], colorscale='Viridis', showscale=True, colorbar=dict(title='RSI', titlefont=dict(color='rgba(255,255,255,0.5)'), tickfont=dict(color='rgba(255,255,255,0.5)'))),
            text=top_rsi['RSI'].round(1), textposition='outside', textfont=dict(color='rgba(255,255,255,0.7)', size=10),
            hovertemplate='<b>%{x}</b><br>RSI: %{y:.1f}<br>Старты: %{customdata[0]:,}<br>Стримы: %{customdata[1]:,}<br>Конверсия: %{customdata[2]:.1f}%<extra></extra>',
            customdata=top_rsi[['Старты', 'Стримы', 'Конверсия']].values
        ))
        fig2.update_layout(
            template='plotly_dark',
            plot_bgcolor='rgba(0,0,0,0)',
            paper_bgcolor='rgba(0,0,0,0)',
            height=450,
            xaxis=dict(tickangle=-20, tickfont=dict(color='rgba(255,255,255,0.5)', size=9), gridcolor='rgba(255,255,255,0.05)'),
            yaxis=dict(title='RSI', titlefont=dict(color='rgba(255,255,255,0.5)'), tickfont=dict(color='rgba(255,255,255,0.5)'), gridcolor='rgba(255,255,255,0.05)')
        )
        st.plotly_chart(fig2, use_container_width=True)
    with col2:
        st.markdown("""
        <div style="background: rgba(255,255,255,0.03); border: 1px solid rgba(255,255,255,0.06); border-radius: 16px; padding: 1.5rem; backdrop-filter: blur(10px);">
            <h4 style="color: rgba(255,255,255,0.5); margin-bottom: 1rem; font-size: 0.8rem; letter-spacing: 1px; text-transform: uppercase;">⭐ Топ RSI</h4>
        """, unsafe_allow_html=True)
        if len(top_rsi) > 0:
            for i, (idx, row) in enumerate(top_rsi.head(5).iterrows()):
                medal = ['🥇', '🥈', '🥉', '4️⃣', '5️⃣'][i]
                st.markdown(f"""
                <div style="display: flex; align-items: center; justify-content: space-between; padding: 0.5rem 0; border-bottom: 1px solid rgba(255,255,255,0.03);">
                    <div>
                        <span style="color: rgba(255,255,255,0.3); font-size: 0.8rem;">{medal}</span>
                        <span style="color: rgba(255,255,255,0.8); font-size: 0.85rem; margin-left: 0.5rem;">{row['Короткое название']}</span>
                    </div>
                    <span style="color: #4facfe; font-weight: 700; font-size: 0.9rem;">{row['RSI']:.1f}</span>
                </div>
                """, unsafe_allow_html=True)
        st.markdown("</div>", unsafe_allow_html=True)

    # ===== ТОП ЖАНРОВ =====
    st.markdown("---")
    st.markdown('<div class="section-title">🎭 Топ жанров</div>', unsafe_allow_html=True)
    show_hint("💡", "О чем графики", "Первый — по популярности (старты). Второй — по вовлеченности (стримы). Третий — по качеству (дослушиваемость).")

    genre_stats = filtered_data.groupby('Жанр').agg({
        'Старты': 'sum', 'Стримы': 'sum', 'RSI': 'mean',
        'Дослушиваемость': 'mean', 'Средний_прослушивания': 'mean'
    }).reset_index()
    genre_stats['Конверсия'] = (genre_stats['Стримы'] / genre_stats['Старты'] * 100).fillna(0)
    genre_stats = genre_stats.sort_values('Старты', ascending=False)

    col1, col2, col3 = st.columns(3)
    with col1:
        st.markdown('<div style="color: #4facfe; font-weight: 700; font-size: 1rem; padding: 0.5rem 0;">📊 По стартам</div>', unsafe_allow_html=True)
        top_genre_starts = genre_stats.head(8)
        fig3 = go.Figure(data=[go.Bar(
            x=top_genre_starts['Жанр'], y=top_genre_starts['Старты'],
            marker=dict(color=top_genre_starts['Старты'], colorscale='Blues', showscale=False),
            text=top_genre_starts['Старты'], textposition='outside', textfont=dict(color='rgba(255,255,255,0.5)', size=9)
        )])
        fig3.update_layout(
            template='plotly_dark',
            plot_bgcolor='rgba(0,0,0,0)',
            paper_bgcolor='rgba(0,0,0,0)',
            height=280,
            xaxis=dict(tickangle=-15, tickfont=dict(color='rgba(255,255,255,0.4)', size=8)),
            yaxis=dict(title='Старты', titlefont=dict(color='rgba(255,255,255,0.4)'), tickfont=dict(color='rgba(255,255,255,0.4)'), gridcolor='rgba(255,255,255,0.05)'),
            showlegend=False,
            margin=dict(l=10, r=10, t=10, b=30)
        )
        st.plotly_chart(fig3, use_container_width=True)
    with col2:
        st.markdown('<div style="color: #f5576c; font-weight: 700; font-size: 1rem; padding: 0.5rem 0;">🎧 По стримам</div>', unsafe_allow_html=True)
        top_genre_streams = genre_stats.sort_values('Стримы', ascending=False).head(8)
        fig4 = go.Figure(data=[go.Bar(
            x=top_genre_streams['Жанр'], y=top_genre_streams['Стримы'],
            marker=dict(color=top_genre_streams['Стримы'], colorscale='Reds', showscale=False),
            text=top_genre_streams['Стримы'], textposition='outside', textfont=dict(color='rgba(255,255,255,0.5)', size=9)
        )])
        fig4.update_layout(
            template='plotly_dark',
            plot_bgcolor='rgba(0,0,0,0)',
            paper_bgcolor='rgba(0,0,0,0)',
            height=280,
            xaxis=dict(tickangle=-15, tickfont=dict(color='rgba(255,255,255,0.4)', size=8)),
            yaxis=dict(title='Стримы', titlefont=dict(color='rgba(255,255,255,0.4)'), tickfont=dict(color='rgba(255,255,255,0.4)'), gridcolor='rgba(255,255,255,0.05)'),
            showlegend=False,
            margin=dict(l=10, r=10, t=10, b=30)
        )
        st.plotly_chart(fig4, use_container_width=True)
    with col3:
        st.markdown('<div style="color: #43e97b; font-weight: 700; font-size: 1rem; padding: 0.5rem 0;">📈 По дослушиваемости</div>', unsafe_allow_html=True)
        top_genre_completion = genre_stats[genre_stats['Старты'] > 10].sort_values('Дослушиваемость', ascending=False).head(8)
        fig5 = go.Figure(data=[go.Bar(
            x=top_genre_completion['Жанр'], y=top_genre_completion['Дослушиваемость'] * 100,
            marker=dict(color=top_genre_completion['Дослушиваемость'] * 100, colorscale='Greens', showscale=False),
            text=top_genre_completion['Дослушиваемость'] * 100, texttemplate='%{text:.1f}%', textposition='outside', textfont=dict(color='rgba(255,255,255,0.5)', size=9)
        )])
        fig5.update_layout(
            template='plotly_dark',
            plot_bgcolor='rgba(0,0,0,0)',
            paper_bgcolor='rgba(0,0,0,0)',
            height=280,
            xaxis=dict(tickangle=-15, tickfont=dict(color='rgba(255,255,255,0.4)', size=8)),
            yaxis=dict(title='Дослушиваемость %', titlefont=dict(color='rgba(255,255,255,0.4)'), tickfont=dict(color='rgba(255,255,255,0.4)'), gridcolor='rgba(255,255,255,0.05)'),
            showlegend=False,
            margin=dict(l=10, r=10, t=10, b=30)
        )
        st.plotly_chart(fig5, use_container_width=True)

    # ===== АКТИВНОСТЬ ПО ДНЯМ =====
    st.markdown("---")
    st.markdown('<div class="section-title">📅 Активность по дням недели</div>', unsafe_allow_html=True)
    show_hint("💡", "Зачем смотреть", "Показывает, в какие дни недели у вас пик прослушиваний. Планируйте релизы и посты на эти дни.")

    filtered_data['День недели'] = filtered_data['Дата прослушивания'].dt.day_name()
    weekday_order = ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday', 'Sunday']
    weekday_labels = ['Пн', 'Вт', 'Ср', 'Чт', 'Пт', 'Сб', 'Вс']
    weekday_stats = filtered_data.groupby('День недели').agg({'Старты': 'sum', 'Стримы': 'sum'}).reindex(weekday_order).reset_index()
    weekday_stats['День'] = weekday_labels

    col1, col2 = st.columns(2)
    with col1:
        st.markdown('<div style="color: #4facfe; font-weight: 700; font-size: 1rem; padding: 0.5rem 0;">📊 По стартам</div>', unsafe_allow_html=True)
        fig6 = go.Figure(data=[go.Bar(
            x=weekday_stats['День'], y=weekday_stats['Старты'],
            marker=dict(color=['#4facfe', '#43e97b', '#f093fb', '#f5576c', '#fa709a', '#f6d365', '#a8edea'], line=dict(color='rgba(255,255,255,0.1)', width=1)),
            text=weekday_stats['Старты'], textposition='outside', textfont=dict(color='rgba(255,255,255,0.5)', size=10)
        )])
        fig6.update_layout(
            template='plotly_dark',
            plot_bgcolor='rgba(0,0,0,0)',
            paper_bgcolor='rgba(0,0,0,0)',
            height=300,
            xaxis=dict(title='День недели', titlefont=dict(color='rgba(255,255,255,0.4)'), tickfont=dict(color='rgba(255,255,255,0.4)')),
            yaxis=dict(title='Старты', titlefont=dict(color='rgba(255,255,255,0.4)'), tickfont=dict(color='rgba(255,255,255,0.4)'), gridcolor='rgba(255,255,255,0.05)'),
            showlegend=False
        )
        st.plotly_chart(fig6, use_container_width=True)
    with col2:
        st.markdown('<div style="color: #f5576c; font-weight: 700; font-size: 1rem; padding: 0.5rem 0;">🎧 По стримам</div>', unsafe_allow_html=True)
        fig7 = go.Figure(data=[go.Bar(
            x=weekday_stats['День'], y=weekday_stats['Стримы'],
            marker=dict(color=['#4facfe', '#43e97b', '#f093fb', '#f5576c', '#fa709a', '#f6d365', '#a8edea'], line=dict(color='rgba(255,255,255,0.1)', width=1)),
            text=weekday_stats['Стримы'], textposition='outside', textfont=dict(color='rgba(255,255,255,0.5)', size=10)
        )])
        fig7.update_layout(
            template='plotly_dark',
            plot_bgcolor='rgba(0,0,0,0)',
            paper_bgcolor='rgba(0,0,0,0)',
            height=300,
            xaxis=dict(title='День недели', titlefont=dict(color='rgba(255,255,255,0.4)'), tickfont=dict(color='rgba(255,255,255,0.4)')),
            yaxis=dict(title='Стримы', titlefont=dict(color='rgba(255,255,255,0.4)'), tickfont=dict(color='rgba(255,255,255,0.4)'), gridcolor='rgba(255,255,255,0.05)'),
            showlegend=False
        )
        st.plotly_chart(fig7, use_container_width=True)

    # ===== СВОДНАЯ ТАБЛИЦА =====
    st.markdown("---")
    st.markdown('<div class="section-title">📋 Полная сводка по выпускам</div>', unsafe_allow_html=True)
    show_hint("💡", "Что в таблице", "Все выпуски с главными метриками. Сортировка по RSI — лучшие сверху.")

    episode_summary = filtered_data.groupby(['Выпуск', 'Короткое название']).agg({
        'Старты': 'sum', 'Стримы': 'sum', 'RSI': 'mean',
        'Дослушиваемость': 'mean', 'Средний_прослушивания': 'mean',
        'Формат': 'first', 'Жанр': 'first'
    }).reset_index()
    episode_summary['Конверсия'] = (episode_summary['Стримы'] / episode_summary['Старты'] * 100).fillna(0)
    episode_summary = episode_summary.sort_values('RSI', ascending=False)

    display_df = episode_summary[['Короткое название', 'Старты', 'Стримы', 'Конверсия', 'Дослушиваемость', 'Средний_прослушивания', 'RSI', 'Формат', 'Жанр']].copy()
    display_df.columns = ['Название', 'Старты', 'Стримы', 'Конверсия %', 'Дослушиваемость %', 'Средний %', 'RSI', 'Формат', 'Жанр']
    display_df['Дослушиваемость %'] = display_df['Дослушиваемость %'] * 100
    display_df['Средний %'] = display_df['Средний %'] * 100

    try:
        st.dataframe(display_df.head(50), width=1200, height=400)
    except:
        st.dataframe(display_df.head(50), height=400)

    st.markdown("---")
    st.markdown("""<div class="footer">🎙️ Подкаст Аналитика Pro • Премиум дашборд • Данные обновляются автоматически</div>""", unsafe_allow_html=True)

    with st.expander("ℹ️ Информация о данных", expanded=False):
        col1, col2, col3 = st.columns(3)
        with col1:
            st.markdown(f"""
            <div style="background: rgba(255,255,255,0.03); border: 1px solid rgba(255,255,255,0.06); border-radius: 12px; padding: 1.2rem;">
                <div style="color: rgba(255,255,255,0.3); font-size: 0.7rem; letter-spacing: 1px; text-transform: uppercase;">📅 Период</div>
                <div style="color: white; font-size: 1.1rem; font-weight: 600; margin-top: 0.3rem;">{filtered_data['Дата прослушивания'].min().date()} — {filtered_data['Дата прослушивания'].max().date()}</div>
            </div>
            <br>
            <div style="background: rgba(255,255,255,0.03); border: 1px solid rgba(255,255,255,0.06); border-radius: 12px; padding: 1.2rem;">
                <div style="color: rgba(255,255,255,0.3); font-size: 0.7rem; letter-spacing: 1px; text-transform: uppercase;">📊 Всего записей</div>
                <div style="color: white; font-size: 1.1rem; font-weight: 600; margin-top: 0.3rem;">{len(filtered_data):,}</div>
            </div>
            """, unsafe_allow_html=True)
        with col2:
            st.markdown(f"""
            <div style="background: rgba(255,255,255,0.03); border: 1px solid rgba(255,255,255,0.06); border-radius: 12px; padding: 1.2rem;">
                <div style="color: rgba(255,255,255,0.3); font-size: 0.7rem; letter-spacing: 1px; text-transform: uppercase;">📝 Уникальных выпусков</div>
                <div style="color: white; font-size: 1.1rem; font-weight: 600; margin-top: 0.3rem;">{filtered_data['Выпуск'].nunique()}</div>
            </div>
            <br>
            <div style="background: rgba(255,255,255,0.03); border: 1px solid rgba(255,255,255,0.06); border-radius: 12px; padding: 1.2rem;">
                <div style="color: rgba(255,255,255,0.3); font-size: 0.7rem; letter-spacing: 1px; text-transform: uppercase;">🎭 Жанры</div>
                <div style="color: white; font-size: 0.9rem; margin-top: 0.3rem;">{', '.join(filtered_data['Жанр'].unique())}</div>
            </div>
            """, unsafe_allow_html=True)
        with col3:
            st.markdown(f"""
            <div style="background: rgba(255,255,255,0.03); border: 1px solid rgba(255,255,255,0.06); border-radius: 12px; padding: 1.2rem;">
                <div style="color: rgba(255,255,255,0.3); font-size: 0.7rem; letter-spacing: 1px; text-transform: uppercase;">📂 Форматы</div>
                <div style="color: white; font-size: 0.9rem; margin-top: 0.3rem;">{', '.join(filtered_data['Формат'].unique())}</div>
            </div>
            <br>
            <div style="background: rgba(255,255,255,0.03); border: 1px solid rgba(255,255,255,0.06); border-radius: 12px; padding: 1.2rem;">
                <div style="color: rgba(255,255,255,0.3); font-size: 0.7rem; letter-spacing: 1px; text-transform: uppercase;">⭐ Средний RSI</div>
                <div style="color: white; font-size: 1.1rem; font-weight: 600; margin-top: 0.3rem;">{episode_summary['RSI'].mean():.1f}</div>
            </div>
            """, unsafe_allow_html=True)

# ============================================
# СТРАНИЦА 2: АНАЛИЗ ВЫПУСКА
# ============================================
elif page == "📋 Анализ выпуска":
    st.markdown('<div style="font-size: 2.5rem; font-weight: 700; color: white; margin-bottom: 0.5rem;">📋 Детальный анализ выпуска</div>', unsafe_allow_html=True)
    
    show_important_dates_legend()
    
    period = st.radio(
        "📅 Выберите период анализа:",
        ["1 день", "1 неделя", "1 месяц", "Всё время"],
        horizontal=True,
        index=3,
        key="analysis_period"
    )
    
    selected_short = st.selectbox("🎯 Выберите выпуск:", short_names_ordered, key="analysis_episode")
    selected_episode = episode_names_ordered[selected_short]
    
    all_data = df_merged[df_merged['Выпуск'] == selected_episode].copy()
    release_date = df_total[df_total['Выпуск'] == selected_episode]['Дата прослушивания'].min()
    
    if all_data.empty:
        st.warning(f"⚠️ Нет данных для выпуска '{selected_short}'")
    else:
        if period == "1 день":
            episode_data = all_data[(all_data['Дата прослушивания'] >= release_date) & (all_data['Дата прослушивания'] <= release_date + pd.Timedelta(days=0))]
        elif period == "1 неделя":
            episode_data = all_data[(all_data['Дата прослушивания'] >= release_date) & (all_data['Дата прослушивания'] <= release_date + pd.Timedelta(days=6))]
        elif period == "1 месяц":
            episode_data = all_data[(all_data['Дата прослушивания'] >= release_date) & (all_data['Дата прослушивания'] <= release_date + pd.Timedelta(days=29))]
        else:
            episode_data = all_data
        
        if episode_data.empty:
            st.warning(f"⚠️ Нет данных для выпуска '{selected_short}' в выбранном периоде")
        else:
            total_starts_ep = episode_data['Старты'].sum()
            total_streams_ep = episode_data['Стримы'].sum()
            conv_ep = (total_streams_ep / total_starts_ep * 100) if total_starts_ep > 0 else 0
            rsi_ep = episode_data['RSI'].mean()
            
            st.markdown('<div class="bento-grid-4">', unsafe_allow_html=True)
            cols = st.columns(4)
            metrics = [
                (cols[0], "🎬", f"{total_starts_ep:,}", "Всего стартов"),
                (cols[1], "🎧", f"{total_streams_ep:,}", "Всего стримов"),
                (cols[2], "📈", f"{conv_ep:.1f}%", "Конверсия"),
                (cols[3], "⭐", f"{rsi_ep:.1f}", "Средний RSI")
            ]
            for col, icon, value, label in metrics:
                with col:
                    st.markdown(f"""
                    <div class="metric-card">
                        <span class="metric-icon">{icon}</span>
                        <div class="metric-value">{value}</div>
                        <div class="metric-label">{label}</div>
                    </div>
                    """, unsafe_allow_html=True)
            st.markdown('</div>', unsafe_allow_html=True)
            
            st.markdown("---")
            st.markdown('<div class="section-title">ℹ️ Информация о выпуске</div>', unsafe_allow_html=True)
            
            info = df_ref[df_ref['Выпуск'] == selected_episode].iloc[0]
            days_active = (episode_data['Дата прослушивания'].max() - episode_data['Дата прослушивания'].min()).days
            
            st.markdown('<div class="bento-grid-5" style="display: grid; grid-template-columns: 1fr 1fr 1fr 1fr 1fr; gap: 1rem;">', unsafe_allow_html=True)
            info_data = [
                ("📂 Формат", info['Формат']),
                ("🎭 Жанр", info['Жанр']),
                ("📅 Первая дата", release_date.date()),
                ("📆 Дней в выборке", f"{days_active + 1}"),
                ("⏱️ Длительность", info['Длительность'])
            ]
            for label, value in info_data:
                st.markdown(f"""
                <div style="background: rgba(255,255,255,0.03); border: 1px solid rgba(255,255,255,0.06); border-radius: 12px; padding: 0.8rem; text-align: center;">
                    <div style="color: rgba(255,255,255,0.3); font-size: 0.65rem; letter-spacing: 1px; text-transform: uppercase;">{label}</div>
                    <div style="color: white; font-weight: 600; margin-top: 0.2rem;">{value}</div>
                </div>
                """, unsafe_allow_html=True)
            st.markdown('</div>', unsafe_allow_html=True)
            
            st.markdown("---")
            st.markdown('<div class="section-title">📊 Сравнение со средними показателями</div>', unsafe_allow_html=True)
            
            compare_data = df_merged.copy()
            if period == "1 день":
                compare_data = compare_data[(compare_data['Дата прослушивания'] >= release_date) & (compare_data['Дата прослушивания'] <= release_date + pd.Timedelta(days=0))]
            elif period == "1 неделя":
                compare_data = compare_data[(compare_data['Дата прослушивания'] >= release_date) & (compare_data['Дата прослушивания'] <= release_date + pd.Timedelta(days=6))]
            elif period == "1 месяц":
                compare_data = compare_data[(compare_data['Дата прослушивания'] >= release_date) & (compare_data['Дата прослушивания'] <= release_date + pd.Timedelta(days=29))]
            
            metrics = ['Старты', 'Стримы', 'RSI']
            comparison_data = []
            for metric in metrics:
                pos = get_episode_position(episode_data, compare_data, metric)
                comparison_data.append({
                    'Метрика': metric, 
                    'Значение': f"{pos['value']:.1f}", 
                    'Среднее': f"{pos['mean']:.1f}", 
                    'Медиана': f"{pos['median']:.1f}", 
                    'Статус': pos['status']
                })
            st.dataframe(pd.DataFrame(comparison_data), use_container_width=True)
            
            st.markdown('<div class="section-title">📈 Динамика прослушиваний</div>', unsafe_allow_html=True)
            daily_data = episode_data.groupby('Дата прослушивания').agg({'Старты': 'sum', 'Стримы': 'sum'}).reset_index()
            
            fig = go.Figure()
            fig.add_trace(go.Scatter(x=daily_data['Дата прослушивания'], y=daily_data['Старты'], name='Старты', line=dict(color='#4facfe', width=3), fill='tozeroy', fillcolor='rgba(79, 172, 254, 0.1)'))
            fig.add_trace(go.Scatter(x=daily_data['Дата прослушивания'], y=daily_data['Стримы'], name='Стримы', line=dict(color='#f5576c', width=3), fill='tozeroy', fillcolor='rgba(245, 87, 108, 0.1)'))
            fig.add_shape(type="line", x0=release_date, y0=0, x1=release_date, y1=1, yref="paper", line=dict(color="#f093fb", width=2, dash="dash"))
            fig.add_annotation(x=release_date, y=0.98, yref="paper", text="📅 Релиз", showarrow=False, font=dict(color="#f093fb", size=11), textangle=-90)
            
            fig = add_important_dates_to_fig(fig)
            
            fig.update_layout(
                template='plotly_dark',
                plot_bgcolor='rgba(0,0,0,0)',
                paper_bgcolor='rgba(0,0,0,0)',
                height=400,
                hovermode='x unified',
                legend=dict(orientation='h', yanchor='bottom', y=1.02, xanchor='right', x=1, font=dict(color='rgba(255,255,255,0.5)'))
            )
            st.plotly_chart(fig, use_container_width=True)

            # КРИВАЯ ЖИЗНИ
            st.markdown("---")
            st.markdown('<div class="section-title">📈 Кривая жизни выпуска</div>', unsafe_allow_html=True)
            show_hint("💡", "Как читать", "Показывает, как быстро выпуск набирает прослушивания. Чем быстрее достигает 100% — тем быстрее «выдыхается».")
            
            life_curve = get_life_curve_for_period(selected_episode, df_merged, period_days=None)
            
            if life_curve is not None and not life_curve.empty:
                fig_life = go.Figure()
                fig_life.add_trace(go.Scatter(
                    x=life_curve['День от релиза'], y=life_curve['Стримы_норм'],
                    name='Стримы (накоплено)',
                    line=dict(color='#f5576c', width=4),
                    mode='lines+markers',
                    marker=dict(size=8, color='white', line=dict(color='#f5576c', width=2)),
                    fill='tozeroy',
                    fillcolor='rgba(245, 87, 108, 0.1)',
                    hovertemplate='День %{x}: %{y:.1f}%<extra></extra>'
                ))
                fig_life.add_trace(go.Scatter(
                    x=life_curve['День от релиза'], y=life_curve['Стримы_накоп'],
                    name='Стримы (абс.)',
                    line=dict(color='#f093fb', width=2, dash='dash'),
                    mode='lines',
                    yaxis='y2',
                    hovertemplate='День %{x}: %{y:,.0f} стримов<extra></extra>'
                ))
                
                try:
                    idx_50 = (life_curve['Стримы_норм'] >= 50).idxmax() if (life_curve['Стримы_норм'] >= 50).any() else None
                    if idx_50 is not None:
                        day_50 = life_curve.loc[idx_50, 'День от релиза']
                        fig_life.add_annotation(x=day_50, y=50, text=f"⚡ 50% на день {int(day_50)}", showarrow=True, arrowhead=2, ax=20, ay=-30, font=dict(color='#f6d365', size=10), arrowcolor='#f6d365')
                    idx_90 = (life_curve['Стримы_норм'] >= 90).idxmax() if (life_curve['Стримы_норм'] >= 90).any() else None
                    if idx_90 is not None:
                        day_90 = life_curve.loc[idx_90, 'День от релиза']
                        fig_life.add_annotation(x=day_90, y=90, text=f"🎯 90% на день {int(day_90)}", showarrow=True, arrowhead=2, ax=20, ay=30, font=dict(color='#43e97b', size=10), arrowcolor='#43e97b')
                except:
                    pass
                
                fig_life.update_layout(
                    template='plotly_dark',
                    plot_bgcolor='rgba(0,0,0,0)',
                    paper_bgcolor='rgba(0,0,0,0)',
                    height=400,
                    hovermode='x unified',
                    legend=dict(orientation='h', yanchor='bottom', y=1.02, xanchor='right', x=1, font=dict(color='rgba(255,255,255,0.5)')),
                    xaxis=dict(title='День от релиза', titlefont=dict(color='rgba(255,255,255,0.4)'), tickfont=dict(color='rgba(255,255,255,0.4)'), gridcolor='rgba(255,255,255,0.05)'),
                    yaxis=dict(title='% от всех стримов', titlefont=dict(color='#f5576c'), tickfont=dict(color='rgba(255,255,255,0.4)'), gridcolor='rgba(255,255,255,0.05)', range=[0, 105]),
                    yaxis2=dict(title='Стримы (абс.)', titlefont=dict(color='#f093fb'), tickfont=dict(color='rgba(255,255,255,0.4)'), overlaying='y', side='right', showgrid=False)
                )
                
                st.plotly_chart(fig_life, use_container_width=True)
                
                col1, col2, col3 = st.columns(3)
                with col1:
                    days_to_50 = life_curve[life_curve['Стримы_норм'] >= 50]['День от релиза'].min() if (life_curve['Стримы_норм'] >= 50).any() else '∞'
                    st.metric(label="⏱️ Дней до 50% стримов", value=f"{days_to_50}" if days_to_50 != '∞' else "—")
                with col2:
                    days_to_90 = life_curve[life_curve['Стримы_норм'] >= 90]['День от релиза'].min() if (life_curve['Стримы_норм'] >= 90).any() else '∞'
                    st.metric(label="⏱️ Дней до 90% стримов", value=f"{days_to_90}" if days_to_90 != '∞' else "—")
                with col3:
                    if days_to_90 != '∞':
                        if days_to_90 <= 7: status, color = "⚡ Молниеносный", "#f5576c"
                        elif days_to_90 <= 14: status, color = "📈 Средний", "#f6d365"
                        elif days_to_90 <= 30: status, color = "🐢 Долгий", "#43e97b"
                        else: status, color = "🌿 Вечнозеленый", "#4facfe"
                    else: status, color = "📊 Данных нет", "gray"
                    st.markdown(f"""
                    <div style="background: rgba(255,255,255,0.03); border: 2px solid {color}; border-radius: 12px; padding: 0.8rem; text-align: center;">
                        <div style="color: {color}; font-weight: 700;">{status}</div>
                    </div>
                    """, unsafe_allow_html=True)

            # ВОРОНКА
            st.markdown("---")
            st.markdown('<div class="section-title">📊 Воронка внимания</div>', unsafe_allow_html=True)
            show_hint("💡", "Что показывает", "Сколько слушателей доходит до каждого этапа.")
            
            funnel_data = get_funnel_data(episode_data)
            
            if funnel_data['has_data']:
                fig_funnel = go.Figure()
                stages = [f'Старты<br>{funnel_data["stage_1"]:,.0f} чел.', f'Средний %<br>{funnel_data["avg_listen"]*100:.0f}% — {funnel_data["stage_2"]:,.0f} чел.', f'Дослушали<br>{funnel_data["completion"]*100:.0f}% — {funnel_data["stage_3"]:,.0f} чел.']
                values = [funnel_data['stage_1'], funnel_data['stage_2'], funnel_data['stage_3']]
                colors = ['#4facfe', '#f6d365', '#43e97b']
                fig_funnel.add_trace(go.Funnel(
                    name='Воронка внимания',
                    y=stages,
                    x=values,
                    textinfo="value+percent initial",
                    textposition="inside",
                    textfont=dict(color="white", size=13, family="Inter, sans-serif"),
                    marker=dict(color=colors, line=dict(width=2, color='rgba(255,255,255,0.1)')),
                    hovertemplate='<b>%{y}</b><br>Количество: %{x:,.0f}<br>Процент от стартов: %{percentInitial:.1f}%<extra></extra>'
                ))
                fig_funnel.update_layout(
                    template='plotly_dark',
                    plot_bgcolor='rgba(0,0,0,0)',
                    paper_bgcolor='rgba(0,0,0,0)',
                    height=400,
                    showlegend=False,
                    xaxis=dict(title='Количество слушателей', titlefont=dict(color='rgba(255,255,255,0.4)'), tickfont=dict(color='rgba(255,255,255,0.4)'), gridcolor='rgba(255,255,255,0.05)')
                )
                st.plotly_chart(fig_funnel, use_container_width=True)
                
                st.markdown("---")
                col1, col2, col3 = st.columns(3)
                with col1:
                    drop_1 = funnel_data['stage_1'] - funnel_data['stage_2']
                    drop_1_pct = (drop_1 / funnel_data['stage_1'] * 100) if funnel_data['stage_1'] > 0 else 0
                    if drop_1_pct > 30: status, color = "⚠️ Высокая потеря", "#f5576c"
                    elif drop_1_pct > 15: status, color = "📊 Средняя потеря", "#f6d365"
                    else: status, color = "✅ Отличное удержание", "#43e97b"
                    st.markdown(f"""
                    <div style="background: rgba(255,255,255,0.03); border: 2px solid {color}; border-radius: 12px; padding: 0.8rem; text-align: center;">
                        <div style="color: {color}; font-weight: 700;">{status}</div>
                        <div style="color: rgba(255,255,255,0.3); font-size: 0.8rem; margin-top: 0.2rem;">Потеря: {drop_1_pct:.0f}% ({drop_1:,.0f} чел.)</div>
                    </div>
                    """, unsafe_allow_html=True)
                with col2:
                    drop_2 = funnel_data['stage_2'] - funnel_data['stage_3']
                    drop_2_pct = (drop_2 / funnel_data['stage_2'] * 100) if funnel_data['stage_2'] > 0 else 0
                    if drop_2_pct > 30: status, color = "⚠️ Провал в концовке", "#f5576c"
                    elif drop_2_pct > 15: status, color = "📊 Слабая концовка", "#f6d365"
                    else: status, color = "✅ Сильная концовка", "#43e97b"
                    st.markdown(f"""
                    <div style="background: rgba(255,255,255,0.03); border: 2px solid {color}; border-radius: 12px; padding: 0.8rem; text-align: center;">
                        <div style="color: {color}; font-weight: 700;">{status}</div>
                        <div style="color: rgba(255,255,255,0.3); font-size: 0.8rem; margin-top: 0.2rem;">Потеря: {drop_2_pct:.0f}% ({drop_2:,.0f} чел.)</div>
                    </div>
                    """, unsafe_allow_html=True)
                with col3:
                    if funnel_data['completion'] > 0.4: verdict, color = "🏆 Отличный результат!", "#43e97b"
                    elif funnel_data['completion'] > 0.25: verdict, color = "📊 Средний результат", "#f6d365"
                    else: verdict, color = "🔽 Требует улучшения", "#f5576c"
                    st.markdown(f"""
                    <div style="background: rgba(255,255,255,0.03); border: 2px solid {color}; border-radius: 12px; padding: 0.8rem; text-align: center;">
                        <div style="color: {color}; font-weight: 700;">{verdict}</div>
                        <div style="color: rgba(255,255,255,0.3); font-size: 0.8rem; margin-top: 0.2rem;">Дослушивают: {funnel_data["completion"]*100:.0f}% ({funnel_data["stage_3"]:,.0f} чел.)</div>
                    </div>
                    """, unsafe_allow_html=True)
            else:
                st.warning("⚠️ Недостаточно данных для построения воронки внимания.")

# ============================================
# СТРАНИЦА 3: СРАВНЕНИЕ ВЫПУСКОВ
# ============================================
else:
    st.markdown('<div style="font-size: 2.5rem; font-weight: 700; color: white; margin-bottom: 0.5rem;">🔄 Сравнение двух выпусков</div>', unsafe_allow_html=True)
    
    show_important_dates_legend()
    
    period = st.radio(
        "📅 Выберите период анализа:",
        ["1 день", "1 неделя", "1 месяц", "Всё время"],
        horizontal=True,
        index=3,
        key="comparison_period"
    )
    
    col1, col2 = st.columns(2)
    with col1:
        ep1_short = st.selectbox("📌 Выпуск №1:", short_names_ordered, key="ep1")
        ep1 = episode_names_ordered[ep1_short]
        release_date1 = df_total[df_total['Выпуск'] == ep1]['Дата прослушивания'].min()
    with col2:
        ep2_short = st.selectbox("📌 Выпуск №2:", short_names_ordered, key="ep2")
        ep2 = episode_names_ordered[ep2_short]
        release_date2 = df_total[df_total['Выпуск'] == ep2]['Дата прослушивания'].min()
    
    if ep1 == ep2:
        st.warning("⚠️ Выберите два разных выпуска для сравнения!")
    else:
        all_data = df_merged.copy()
        
        if period == "1 день":
            data1 = all_data[(all_data['Выпуск'] == ep1) & (all_data['Дата прослушивания'] >= release_date1) & (all_data['Дата прослушивания'] <= release_date1 + pd.Timedelta(days=0))]
            data2 = all_data[(all_data['Выпуск'] == ep2) & (all_data['Дата прослушивания'] >= release_date2) & (all_data['Дата прослушивания'] <= release_date2 + pd.Timedelta(days=0))]
        elif period == "1 неделя":
            data1 = all_data[(all_data['Выпуск'] == ep1) & (all_data['Дата прослушивания'] >= release_date1) & (all_data['Дата прослушивания'] <= release_date1 + pd.Timedelta(days=6))]
            data2 = all_data[(all_data['Выпуск'] == ep2) & (all_data['Дата прослушивания'] >= release_date2) & (all_data['Дата прослушивания'] <= release_date2 + pd.Timedelta(days=6))]
        elif period == "1 месяц":
            data1 = all_data[(all_data['Выпуск'] == ep1) & (all_data['Дата прослушивания'] >= release_date1) & (all_data['Дата прослушивания'] <= release_date1 + pd.Timedelta(days=29))]
            data2 = all_data[(all_data['Выпуск'] == ep2) & (all_data['Дата прослушивания'] >= release_date2) & (all_data['Дата прослушивания'] <= release_date2 + pd.Timedelta(days=29))]
        else:
            data1 = all_data[all_data['Выпуск'] == ep1]
            data2 = all_data[all_data['Выпуск'] == ep2]
        
        if data1.empty or data2.empty:
            st.warning("⚠️ Нет данных для выбранных выпусков в этом периоде")
        else:
            total_starts1 = data1['Старты'].sum(); total_streams1 = data1['Стримы'].sum()
            conv1 = (total_streams1 / total_starts1 * 100) if total_starts1 > 0 else 0
            rsi1 = data1['RSI'].mean()
            total_starts2 = data2['Старты'].sum(); total_streams2 = data2['Стримы'].sum()
            conv2 = (total_streams2 / total_starts2 * 100) if total_starts2 > 0 else 0
            rsi2 = data2['RSI'].mean()
            
            st.markdown('<div class="section-title">📊 Сравнение метрик</div>', unsafe_allow_html=True)
            
            col1, col2 = st.columns(2)
            with col1:
                st.markdown(f"""
                <div style="background: rgba(79, 172, 254, 0.05); border: 2px solid rgba(79, 172, 254, 0.2); border-radius: 16px; padding: 0.5rem; margin-bottom: 1rem;">
                    <h3 style="color: #4facfe; text-align: center; margin: 0.5rem 0;">{ep1_short}</h3>
                </div>
                """, unsafe_allow_html=True)
                st.markdown('<div class="bento-grid-4" style="margin-top: -0.5rem;">', unsafe_allow_html=True)
                subcols = st.columns(4)
                metrics1 = [
                    (subcols[0], "🎬", f"{total_starts1:,}", "Старты"),
                    (subcols[1], "🎧", f"{total_streams1:,}", "Стримы"),
                    (subcols[2], "📈", f"{conv1:.1f}%", "Конверсия"),
                    (subcols[3], "⭐", f"{rsi1:.1f}", "RSI")
                ]
                for col, icon, value, label in metrics1:
                    with col:
                        st.markdown(f"""
                        <div class="metric-card" style="padding: 0.8rem 0.5rem;">
                            <span class="metric-icon" style="font-size: 1.2rem;">{icon}</span>
                            <div class="metric-value" style="font-size: 1.5rem;">{value}</div>
                            <div class="metric-label" style="font-size: 0.6rem;">{label}</div>
                        </div>
                        """, unsafe_allow_html=True)
                st.markdown('</div>', unsafe_allow_html=True)
            
            with col2:
                st.markdown(f"""
                <div style="background: rgba(245, 87, 108, 0.05); border: 2px solid rgba(245, 87, 108, 0.2); border-radius: 16px; padding: 0.5rem; margin-bottom: 1rem;">
                    <h3 style="color: #f5576c; text-align: center; margin: 0.5rem 0;">{ep2_short}</h3>
                </div>
                """, unsafe_allow_html=True)
                st.markdown('<div class="bento-grid-4" style="margin-top: -0.5rem;">', unsafe_allow_html=True)
                subcols = st.columns(4)
                metrics2 = [
                    (subcols[0], "🎬", f"{total_starts2:,}", "Старты"),
                    (subcols[1], "🎧", f"{total_streams2:,}", "Стримы"),
                    (subcols[2], "📈", f"{conv2:.1f}%", "Конверсия"),
                    (subcols[3], "⭐", f"{rsi2:.1f}", "RSI")
                ]
                for col, icon, value, label in metrics2:
                    with col:
                        st.markdown(f"""
                        <div class="metric-card" style="padding: 0.8rem 0.5rem;">
                            <span class="metric-icon" style="font-size: 1.2rem;">{icon}</span>
                            <div class="metric-value" style="font-size: 1.5rem;">{value}</div>
                            <div class="metric-label" style="font-size: 0.6rem;">{label}</div>
                        </div>
                        """, unsafe_allow_html=True)
                st.markdown('</div>', unsafe_allow_html=True)
            
            st.markdown("---")
            st.markdown('<div class="section-title">📈 Динамика по дням от релиза</div>', unsafe_allow_html=True)
            
            data1_copy = data1.copy(); data2_copy = data2.copy()
            data1_copy['День от релиза'] = (data1_copy['Дата прослушивания'] - release_date1).dt.days + 1
            data2_copy['День от релиза'] = (data2_copy['Дата прослушивания'] - release_date2).dt.days + 1
            daily1 = data1_copy.groupby('День от релиза').agg({'Старты': 'sum', 'Стримы': 'sum'}).reset_index()
            daily2 = data2_copy.groupby('День от релиза').agg({'Старты': 'sum', 'Стримы': 'sum'}).reset_index()
            
            st.markdown('<div style="color: #4facfe; font-weight: 700; font-size: 1rem; padding: 0.5rem 0;">🎬 Сравнение стартов</div>', unsafe_allow_html=True)
            fig_starts = go.Figure()
            fig_starts.add_trace(go.Scatter(x=daily1['День от релиза'], y=daily1['Старты'], name=f'{ep1_short}', line=dict(color='#4facfe', width=3), mode='lines+markers', marker=dict(size=8, color='white', line=dict(color='#4facfe', width=1.5)), fill='tozeroy', fillcolor='rgba(79, 172, 254, 0.1)'))
            fig_starts.add_trace(go.Scatter(x=daily2['День от релиза'], y=daily2['Старты'], name=f'{ep2_short}', line=dict(color='#f5576c', width=3), mode='lines+markers', marker=dict(size=8, color='white', line=dict(color='#f5576c', width=1.5)), fill='tozeroy', fillcolor='rgba(245, 87, 108, 0.1)'))
            fig_starts.update_layout(
                template='plotly_dark',
                plot_bgcolor='rgba(0,0,0,0)',
                paper_bgcolor='rgba(0,0,0,0)',
                height=350,
                hovermode='x unified',
                legend=dict(orientation='h', yanchor='bottom', y=1.02, xanchor='right', x=1, font=dict(color='rgba(255,255,255,0.5)')),
                xaxis=dict(title='День от релиза', titlefont=dict(color='rgba(255,255,255,0.4)'), tickfont=dict(color='rgba(255,255,255,0.4)'), gridcolor='rgba(255,255,255,0.05)'),
                yaxis=dict(title='Старты', titlefont=dict(color='#4facfe'), tickfont=dict(color='rgba(255,255,255,0.4)'), gridcolor='rgba(255,255,255,0.05)')
            )
            st.plotly_chart(fig_starts, use_container_width=True)
            
            st.markdown('<div style="color: #f5576c; font-weight: 700; font-size: 1rem; padding: 0.5rem 0;">🎧 Сравнение стримов</div>', unsafe_allow_html=True)
            fig_streams = go.Figure()
            fig_streams.add_trace(go.Scatter(x=daily1['День от релиза'], y=daily1['Стримы'], name=f'{ep1_short}', line=dict(color='#43e97b', width=3), mode='lines+markers', marker=dict(size=8, color='white', line=dict(color='#43e97b', width=1.5)), fill='tozeroy', fillcolor='rgba(67, 233, 123, 0.1)'))
            fig_streams.add_trace(go.Scatter(x=daily2['День от релиза'], y=daily2['Стримы'], name=f'{ep2_short}', line=dict(color='#f093fb', width=3), mode='lines+markers', marker=dict(size=8, color='white', line=dict(color='#f093fb', width=1.5)), fill='tozeroy', fillcolor='rgba(240, 147, 251, 0.1)'))
            fig_streams.update_layout(
                template='plotly_dark',
                plot_bgcolor='rgba(0,0,0,0)',
                paper_bgcolor='rgba(0,0,0,0)',
                height=350,
                hovermode='x unified',
                legend=dict(orientation='h', yanchor='bottom', y=1.02, xanchor='right', x=1, font=dict(color='rgba(255,255,255,0.5)')),
                xaxis=dict(title='День от релиза', titlefont=dict(color='rgba(255,255,255,0.4)'), tickfont=dict(color='rgba(255,255,255,0.4)'), gridcolor='rgba(255,255,255,0.05)'),
                yaxis=dict(title='Стримы', titlefont=dict(color='#f5576c'), tickfont=dict(color='rgba(255,255,255,0.4)'), gridcolor='rgba(255,255,255,0.05)')
            )
            st.plotly_chart(fig_streams, use_container_width=True)

            # СРАВНЕНИЕ КРИВЫХ
            st.markdown("---")
            st.markdown('<div class="section-title">📈 Сравнение кривых жизни</div>', unsafe_allow_html=True)
            show_hint("💡", "Как сравнивать", "Чей график круче — тот быстрее взлетает. Чей длиннее — тот живет дольше.")
            
            life_curve1 = get_life_curve_for_period(ep1, df_merged, period_days=None)
            life_curve2 = get_life_curve_for_period(ep2, df_merged, period_days=None)
            
            if life_curve1 is not None and life_curve2 is not None and not life_curve1.empty and not life_curve2.empty:
                fig_compare_life = go.Figure()
                fig_compare_life.add_trace(go.Scatter(
                    x=life_curve1['День от релиза'], y=life_curve1['Стримы_норм'],
                    name=f'{ep1_short}',
                    line=dict(color='#4facfe', width=4),
                    mode='lines+markers',
                    marker=dict(size=8, color='white', line=dict(color='#4facfe', width=2)),
                    fill='tozeroy',
                    fillcolor='rgba(79, 172, 254, 0.1)'
                ))
                fig_compare_life.add_trace(go.Scatter(
                    x=life_curve2['День от релиза'], y=life_curve2['Стримы_норм'],
                    name=f'{ep2_short}',
                    line=dict(color='#f5576c', width=4),
                    mode='lines+markers',
                    marker=dict(size=8, color='white', line=dict(color='#f5576c', width=2)),
                    fill='tozeroy',
                    fillcolor='rgba(245, 87, 108, 0.1)'
                ))
                
                for y_val, color, label in [(50, '#f6d365', '50%'), (90, '#43e97b', '90%')]:
                    fig_compare_life.add_hline(y=y_val, line_dash="dash", line_color=color, line_width=1.5, annotation_text=label, annotation_font=dict(color=color, size=9))
                
                fig_compare_life.update_layout(
                    template='plotly_dark',
                    plot_bgcolor='rgba(0,0,0,0)',
                    paper_bgcolor='rgba(0,0,0,0)',
                    height=400,
                    hovermode='x unified',
                    legend=dict(orientation='h', yanchor='bottom', y=1.02, xanchor='right', x=1, font=dict(color='rgba(255,255,255,0.5)')),
                    xaxis=dict(title='День от релиза', titlefont=dict(color='rgba(255,255,255,0.4)'), tickfont=dict(color='rgba(255,255,255,0.4)'), gridcolor='rgba(255,255,255,0.05)'),
                    yaxis=dict(title='% от всех стримов', titlefont=dict(color='rgba(255,255,255,0.4)'), tickfont=dict(color='rgba(255,255,255,0.4)'), gridcolor='rgba(255,255,255,0.05)', range=[0, 105])
                )
                st.plotly_chart(fig_compare_life, use_container_width=True)
                
                st.markdown("---")
                st.markdown('<div class="section-title">📊 Сравнительная статистика</div>', unsafe_allow_html=True)
                
                col1, col2, col3 = st.columns(3)
                with col1:
                    days1_50 = life_curve1[life_curve1['Стримы_норм'] >= 50]['День от релиза'].min() if (life_curve1['Стримы_норм'] >= 50).any() else None
                    days2_50 = life_curve2[life_curve2['Стримы_норм'] >= 50]['День от релиза'].min() if (life_curve2['Стримы_норм'] >= 50).any() else None
                    if days1_50 and days2_50:
                        faster = "1️⃣" if days1_50 < days2_50 else "2️⃣" if days2_50 < days1_50 else "🤝"
                        st.markdown(f"""
                        <div style="background: rgba(255,255,255,0.03); border: 2px solid rgba(79, 172, 254, 0.2); border-radius: 12px; padding: 1rem; text-align: center;">
                            <div style="color: #4facfe; font-weight: 700;">⏱️ Дней до 50% {faster}</div>
                            <div style="color: rgba(255,255,255,0.7); font-size: 0.9rem; margin-top: 0.3rem;">
                                {ep1_short}: <span style="color: #4facfe; font-weight: 600;">{days1_50} дн.</span><br>
                                {ep2_short}: <span style="color: #f5576c; font-weight: 600;">{days2_50} дн.</span>
                            </div>
                        </div>
                        """, unsafe_allow_html=True)
                with col2:
                    days1_90 = life_curve1[life_curve1['Стримы_норм'] >= 90]['День от релиза'].min() if (life_curve1['Стримы_норм'] >= 90).any() else None
                    days2_90 = life_curve2[life_curve2['Стримы_норм'] >= 90]['День от релиза'].min() if (life_curve2['Стримы_норм'] >= 90).any() else None
                    if days1_90 and days2_90:
                        longer = "1️⃣" if days1_90 > days2_90 else "2️⃣" if days2_90 > days1_90 else "🤝"
                        st.markdown(f"""
                        <div style="background: rgba(255,255,255,0.03); border: 2px solid rgba(67, 233, 123, 0.2); border-radius: 12px; padding: 1rem; text-align: center;">
                            <div style="color: #43e97b; font-weight: 700;">⏱️ Дней до 90% {longer}</div>
                            <div style="color: rgba(255,255,255,0.7); font-size: 0.9rem; margin-top: 0.3rem;">
                                {ep1_short}: <span style="color: #4facfe; font-weight: 600;">{days1_90} дн.</span><br>
                                {ep2_short}: <span style="color: #f5576c; font-weight: 600;">{days2_90} дн.</span>
                            </div>
                        </div>
                        """, unsafe_allow_html=True)
                with col3:
                    if len(life_curve1) >= 3 and len(life_curve2) >= 3:
                        slope1 = (life_curve1['Стримы_норм'].iloc[2] - life_curve1['Стримы_норм'].iloc[0]) / 2
                        slope2 = (life_curve2['Стримы_норм'].iloc[2] - life_curve2['Стримы_норм'].iloc[0]) / 2
                        faster_start = "1️⃣" if slope1 > slope2 else "2️⃣" if slope2 > slope1 else "🤝"
                        st.markdown(f"""
                        <div style="background: rgba(255,255,255,0.03); border: 2px solid rgba(246, 211, 101, 0.2); border-radius: 12px; padding: 1rem; text-align: center;">
                            <div style="color: #f6d365; font-weight: 700;">🚀 Скорость старта {faster_start}</div>
                            <div style="color: rgba(255,255,255,0.7); font-size: 0.9rem; margin-top: 0.3rem;">
                                {ep1_short}: <span style="color: #4facfe; font-weight: 600;">{slope1:.1f}%/день</span><br>
                                {ep2_short}: <span style="color: #f5576c; font-weight: 600;">{slope2:.1f}%/день</span>
                            </div>
                        </div>
                        """, unsafe_allow_html=True)
                
                st.markdown("---")
                st.markdown('<div class="section-title">💡 Вывод</div>', unsafe_allow_html=True)
                
                col1, col2, col3 = st.columns([1, 1, 2])
                with col1:
                    st.markdown(f"""
                    <div style="background: rgba(255,255,255,0.03); border: 2px solid rgba(79, 172, 254, 0.2); border-radius: 12px; padding: 0.8rem; text-align: center;">
                        <div style="color: #4facfe; font-weight: 700;">⭐ {ep1_short}</div>
                        <div style="color: rgba(255,255,255,0.5); font-size: 0.8rem;">Скорость: {slope1:.1f}%/день</div>
                    </div>
                    """, unsafe_allow_html=True)
                with col2:
                    st.markdown(f"""
                    <div style="background: rgba(255,255,255,0.03); border: 2px solid rgba(245, 87, 108, 0.2); border-radius: 12px; padding: 0.8rem; text-align: center;">
                        <div style="color: #f5576c; font-weight: 700;">⭐ {ep2_short}</div>
                        <div style="color: rgba(255,255,255,0.5); font-size: 0.8rem;">Скорость: {slope2:.1f}%/день</div>
                    </div>
                    """, unsafe_allow_html=True)
                with col3:
                    if days1_50 and days2_50 and days1_90 and days2_90:
                        if days1_50 < days2_50 and days1_90 < days2_90:
                            winner, color, detail = ep1_short, "#43e97b", "быстрее набирает, но и быстрее выдыхается"
                        elif days1_50 > days2_50 and days1_90 > days2_90:
                            winner, color, detail = ep2_short, "#43e97b", "быстрее набирает, но и быстрее выдыхается"
                        elif days1_50 < days2_50 and days1_90 > days2_90:
                            winner, color, detail = ep1_short, "#f6d365", "взлетает быстрее и живет дольше — идеал!"
                        elif days1_50 > days2_50 and days1_90 < days2_90:
                            winner, color, detail = ep2_short, "#f6d365", "взлетает быстрее и живет дольше — идеал!"
                        else:
                            winner, color, detail = "Ничья", "#4facfe", "разные паттерны, смотрите график"
                        st.markdown(f"""
                        <div style="background: rgba(255,255,255,0.03); border: 2px solid {color}; border-radius: 12px; padding: 0.8rem; text-align: center;">
                            <div style="color: {color}; font-weight: 700;">🏆 Победитель</div>
                            <div style="color: {color}; font-size: 1.2rem; font-weight: 700;">{winner}</div>
                            <div style="color: rgba(255,255,255,0.5); font-size: 0.8rem;">{detail}</div>
                        </div>
                        """, unsafe_allow_html=True)

            # СРАВНЕНИЕ ВОРОНОК
            st.markdown("---")
            st.markdown('<div class="section-title">📊 Сравнение воронок внимания</div>', unsafe_allow_html=True)
            show_hint("💡", "Что сравниваем", "Потери аудитории на каждом этапе. У какого выпуска меньше потерь — тот лучше держит внимание.")
            
            funnel1 = get_funnel_data(data1)
            funnel2 = get_funnel_data(data2)
            
            if funnel1['has_data'] and funnel2['has_data']:
                col1, col2 = st.columns(2)
                with col1:
                    st.markdown(f"""
                    <div style="background: rgba(79, 172, 254, 0.05); border: 2px solid rgba(79, 172, 254, 0.2); border-radius: 12px; padding: 0.3rem; text-align: center; margin-bottom: 0.5rem;">
                        <h4 style="color: #4facfe; margin: 0.3rem;">{ep1_short}</h4>
                    </div>
                    """, unsafe_allow_html=True)
                    fig_funnel1 = go.Figure()
                    stages1 = [f'Старты<br>{funnel1["stage_1"]:,.0f}', f'Средний %<br>{funnel1["avg_listen"]*100:.0f}%', f'Дослушали<br>{funnel1["completion"]*100:.0f}%']
                    values1 = [funnel1['stage_1'], funnel1['stage_2'], funnel1['stage_3']]
                    fig_funnel1.add_trace(go.Funnel(
                        name=ep1_short, y=stages1, x=values1,
                        textinfo="value+percent initial",
                        textposition="inside",
                        textfont=dict(color="white", size=11, family="Inter, sans-serif"),
                        marker=dict(color=['#4facfe', '#f6d365', '#43e97b'], line=dict(width=2, color='rgba(255,255,255,0.1)'))
                    ))
                    fig_funnel1.update_layout(
                        template='plotly_dark',
                        plot_bgcolor='rgba(0,0,0,0)',
                        paper_bgcolor='rgba(0,0,0,0)',
                        height=350,
                        showlegend=False,
                        margin=dict(l=20, r=20, t=10, b=20),
                        xaxis=dict(title='Количество слушателей', titlefont=dict(color='rgba(255,255,255,0.4)'), tickfont=dict(color='rgba(255,255,255,0.4)'), gridcolor='rgba(255,255,255,0.05)')
                    )
                    st.plotly_chart(fig_funnel1, use_container_width=True)
                
                with col2:
                    st.markdown(f"""
                    <div style="background: rgba(245, 87, 108, 0.05); border: 2px solid rgba(245, 87, 108, 0.2); border-radius: 12px; padding: 0.3rem; text-align: center; margin-bottom: 0.5rem;">
                        <h4 style="color: #f5576c; margin: 0.3rem;">{ep2_short}</h4>
                    </div>
                    """, unsafe_allow_html=True)
                    fig_funnel2 = go.Figure()
                    stages2 = [f'Старты<br>{funnel2["stage_1"]:,.0f}', f'Средний %<br>{funnel2["avg_listen"]*100:.0f}%', f'Дослушали<br>{funnel2["completion"]*100:.0f}%']
                    values2 = [funnel2['stage_1'], funnel2['stage_2'], funnel2['stage_3']]
                    fig_funnel2.add_trace(go.Funnel(
                        name=ep2_short, y=stages2, x=values2,
                        textinfo="value+percent initial",
                        textposition="inside",
                        textfont=dict(color="white", size=11, family="Inter, sans-serif"),
                        marker=dict(color=['#f5576c', '#f6d365', '#43e97b'], line=dict(width=2, color='rgba(255,255,255,0.1)'))
                    ))
                    fig_funnel2.update_layout(
                        template='plotly_dark',
                        plot_bgcolor='rgba(0,0,0,0)',
                        paper_bgcolor='rgba(0,0,0,0)',
                        height=350,
                        showlegend=False,
                        margin=dict(l=20, r=20, t=10, b=20),
                        xaxis=dict(title='Количество слушателей', titlefont=dict(color='rgba(255,255,255,0.4)'), tickfont=dict(color='rgba(255,255,255,0.4)'), gridcolor='rgba(255,255,255,0.05)')
                    )
                    st.plotly_chart(fig_funnel2, use_container_width=True)
                
                st.markdown("---")
                st.markdown('<div class="section-title">📉 Сравнение потерь аудитории</div>', unsafe_allow_html=True)
                
                drop1_1 = funnel1['stage_1'] - funnel1['stage_2']
                drop1_1_pct = (drop1_1 / funnel1['stage_1'] * 100) if funnel1['stage_1'] > 0 else 0
                drop1_2 = funnel1['stage_2'] - funnel1['stage_3']
                drop1_2_pct = (drop1_2 / funnel1['stage_2'] * 100) if funnel1['stage_2'] > 0 else 0
                drop2_1 = funnel2['stage_1'] - funnel2['stage_2']
                drop2_1_pct = (drop2_1 / funnel2['stage_1'] * 100) if funnel2['stage_1'] > 0 else 0
                drop2_2 = funnel2['stage_2'] - funnel2['stage_3']
                drop2_2_pct = (drop2_2 / funnel2['stage_2'] * 100) if funnel2['stage_2'] > 0 else 0
                
                comparison_data = pd.DataFrame({
                    'Показатель': ['Старты (всего)', 'Средний % прослушивания', 'Дослушиваемость', 'Потеря: Старты → Средний %', 'Потеря: Средний % → Дослушивание', 'Общая потеря'],
                    ep1_short: [f"{funnel1['stage_1']:,.0f}", f"{funnel1['avg_listen']*100:.1f}%", f"{funnel1['completion']*100:.1f}%", f"{drop1_1:,.0f} ({drop1_1_pct:.1f}%)", f"{drop1_2:,.0f} ({drop1_2_pct:.1f}%)", f"{funnel1['stage_1'] - funnel1['stage_3']:,.0f} ({100 - funnel1['completion']*100:.1f}%)"],
                    ep2_short: [f"{funnel2['stage_1']:,.0f}", f"{funnel2['avg_listen']*100:.1f}%", f"{funnel2['completion']*100:.1f}%", f"{drop2_1:,.0f} ({drop2_1_pct:.1f}%)", f"{drop2_2:,.0f} ({drop2_2_pct:.1f}%)", f"{funnel2['stage_1'] - funnel2['stage_3']:,.0f} ({100 - funnel2['completion']*100:.1f}%)"]
                })
                st.dataframe(comparison_data, use_container_width=True)
                
                st.markdown("---")
                col1, col2, col3 = st.columns(3)
                with col1:
                    if funnel1['completion'] > funnel2['completion']: winner, color, detail = ep1_short, "#4facfe", "лучше удерживает аудиторию"
                    elif funnel2['completion'] > funnel1['completion']: winner, color, detail = ep2_short, "#f5576c", "лучше удерживает аудиторию"
                    else: winner, color, detail = "Ничья", "#f6d365", "одинаково удерживают"
                    st.markdown(f"""
                    <div style="background: rgba(255,255,255,0.03); border: 2px solid {color}; border-radius: 12px; padding: 0.8rem; text-align: center;">
                        <div style="color: {color}; font-weight: 700;">🏆 Победитель по удержанию</div>
                        <div style="color: {color}; font-weight: 700; font-size: 1.1rem;">{winner}</div>
                        <div style="color: rgba(255,255,255,0.4); font-size: 0.8rem;">{detail}</div>
                    </div>
                    """, unsafe_allow_html=True)
                with col2:
                    if drop1_1_pct < drop2_1_pct: better, color, detail = ep1_short, "#4facfe", "меньше теряет в начале"
                    elif drop2_1_pct < drop1_1_pct: better, color, detail = ep2_short, "#f5576c", "меньше теряет в начале"
                    else: better, color, detail = "Ничья", "#f6d365", "одинаковые потери в начале"
                    st.markdown(f"""
                    <div style="background: rgba(255,255,255,0.03); border: 2px solid {color}; border-radius: 12px; padding: 0.8rem; text-align: center;">
                        <div style="color: {color}; font-weight: 700;">🎯 Лучший старт</div>
                        <div style="color: {color}; font-weight: 700; font-size: 1.1rem;">{better}</div>
                        <div style="color: rgba(255,255,255,0.4); font-size: 0.8rem;">{detail}</div>
                    </div>
                    """, unsafe_allow_html=True)
                with col3:
                    if drop1_2_pct < drop2_2_pct: better, color, detail = ep1_short, "#43e97b", "лучшая концовка"
                    elif drop2_2_pct < drop1_2_pct: better, color, detail = ep2_short, "#43e97b", "лучшая концовка"
                    else: better, color, detail = "Ничья", "#f6d365", "одинаковые концовки"
                    st.markdown(f"""
                    <div style="background: rgba(255,255,255,0.03); border: 2px solid {color}; border-radius: 12px; padding: 0.8rem; text-align: center;">
                        <div style="color: {color}; font-weight: 700;">🏁 Лучшая концовка</div>
                        <div style="color: {color}; font-weight: 700; font-size: 1.1rem;">{better}</div>
                        <div style="color: rgba(255,255,255,0.4); font-size: 0.8rem;">{detail}</div>
                    </div>
                    """, unsafe_allow_html=True)
            else:
                st.warning("⚠️ Недостаточно данных для сравнения воронок внимания.")
            
            # ИТОГОВЫЙ ВЕРДИКТ
            st.markdown("---")
            st.markdown('<div class="section-title">🏆 Итоговый вердикт по RSI</div>', unsafe_allow_html=True)
            show_hint("💡", "Что это", "Сравнение двух выпусков по главной метрике. Победитель — тот, у кого RSI выше.")
            
            col1, col2, col3 = st.columns([1, 1, 2])
            with col1:
                st.markdown(f"""
                <div style="background: rgba(255,255,255,0.03); border: 2px solid rgba(79, 172, 254, 0.2); border-radius: 12px; padding: 0.8rem; text-align: center;">
                    <div style="color: #4facfe; font-weight: 700;">⭐ RSI {ep1_short}</div>
                    <div style="font-size: 1.5rem; font-weight: 700; color: white;">{rsi1:.1f}</div>
                </div>
                """, unsafe_allow_html=True)
            with col2:
                st.markdown(f"""
                <div style="background: rgba(255,255,255,0.03); border: 2px solid rgba(245, 87, 108, 0.2); border-radius: 12px; padding: 0.8rem; text-align: center;">
                    <div style="color: #f5576c; font-weight: 700;">⭐ RSI {ep2_short}</div>
                    <div style="font-size: 1.5rem; font-weight: 700; color: white;">{rsi2:.1f}</div>
                </div>
                """, unsafe_allow_html=True)
            with col3:
                if rsi1 > rsi2 * 1.05:
                    st.markdown(f"""
                    <div style="background: rgba(67, 233, 123, 0.05); border: 2px solid #43e97b; border-radius: 12px; padding: 0.8rem; text-align: center;">
                        <div style="color: #43e97b; font-weight: 700;">🏆 Победитель</div>
                        <div style="color: #43e97b; font-size: 1.3rem; font-weight: 700;">{ep1_short}</div>
                        <div style="color: rgba(255,255,255,0.4); font-size: 0.8rem;">значительно лучше по RSI!</div>
                    </div>
                    """, unsafe_allow_html=True)
                elif rsi1 > rsi2:
                    st.markdown(f"""
                    <div style="background: rgba(79, 172, 254, 0.05); border: 2px solid #4facfe; border-radius: 12px; padding: 0.8rem; text-align: center;">
                        <div style="color: #4facfe; font-weight: 700;">🏆 Победитель</div>
                        <div style="color: #4facfe; font-size: 1.3rem; font-weight: 700;">{ep1_short}</div>
                        <div style="color: rgba(255,255,255,0.4); font-size: 0.8rem;">лучше по RSI!</div>
                    </div>
                    """, unsafe_allow_html=True)
                elif rsi2 > rsi1 * 1.05:
                    st.markdown(f"""
                    <div style="background: rgba(67, 233, 123, 0.05); border: 2px solid #43e97b; border-radius: 12px; padding: 0.8rem; text-align: center;">
                        <div style="color: #43e97b; font-weight: 700;">🏆 Победитель</div>
                        <div style="color: #43e97b; font-size: 1.3rem; font-weight: 700;">{ep2_short}</div>
                        <div style="color: rgba(255,255,255,0.4); font-size: 0.8rem;">значительно лучше по RSI!</div>
                    </div>
                    """, unsafe_allow_html=True)
                elif rsi2 > rsi1:
                    st.markdown(f"""
                    <div style="background: rgba(79, 172, 254, 0.05); border: 2px solid #4facfe; border-radius: 12px; padding: 0.8rem; text-align: center;">
                        <div style="color: #4facfe; font-weight: 700;">🏆 Победитель</div>
                        <div style="color: #4facfe; font-size: 1.3rem; font-weight: 700;">{ep2_short}</div>
                        <div style="color: rgba(255,255,255,0.4); font-size: 0.8rem;">лучше по RSI!</div>
                    </div>
                    """, unsafe_allow_html=True)
                else:
                    st.markdown(f"""
                    <div style="background: rgba(246, 211, 101, 0.05); border: 2px solid #f6d365; border-radius: 12px; padding: 0.8rem; text-align: center;">
                        <div style="color: #f6d365; font-weight: 700;">🤝 Ничья</div>
                        <div style="color: rgba(255,255,255,0.4); font-size: 0.8rem;">выпуски примерно равны по RSI!</div>
                    </div>
                    """, unsafe_allow_html=True)

    st.markdown("---")
    st.markdown("""<div class="footer">🎙️ Подкаст Аналитика Pro • Премиум дашборд • Данные обновляются автоматически</div>""", unsafe_allow_html=True)
