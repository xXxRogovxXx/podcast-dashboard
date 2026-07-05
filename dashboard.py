import streamlit as st
import pandas as pd
import plotly.graph_objects as go
import plotly.express as px
from plotly.subplots import make_subplots
import numpy as np
from datetime import datetime

# ============================================
# НАСТРОЙКА СТРАНИЦЫ
# ============================================
st.set_page_config(
    page_title="🎙️ Подкаст Аналитика Pro",
    page_icon="🎙️",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Кастомные стили CSS
st.markdown("""
<style>
    /* Общие стили */
    .stApp {
        background: linear-gradient(135deg, #0f0c29 0%, #302b63 50%, #24243e 100%);
    }
    
    /* Заголовок */
    .main-title {
        font-size: 3.2rem;
        font-weight: 800;
        background: linear-gradient(135deg, #f093fb 0%, #f5576c 50%, #4facfe 100%);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        background-clip: text;
        padding: 1rem 0;
        text-align: center;
        letter-spacing: -1px;
        text-shadow: 0 0 40px rgba(245, 87, 108, 0.3);
    }
    
    .sub-title {
        text-align: center;
        color: rgba(255,255,255,0.6);
        font-size: 1.1rem;
        margin-bottom: 2rem;
        letter-spacing: 3px;
        font-weight: 300;
    }
    
    /* Метрики */
    .metric-card {
        background: rgba(255,255,255,0.05);
        backdrop-filter: blur(10px);
        border: 1px solid rgba(255,255,255,0.1);
        border-radius: 15px;
        padding: 1.5rem;
        text-align: center;
        transition: all 0.3s ease;
        box-shadow: 0 8px 32px rgba(0,0,0,0.3);
    }
    
    .metric-card:hover {
        transform: translateY(-5px);
        box-shadow: 0 12px 48px rgba(245, 87, 108, 0.2);
        border-color: rgba(245, 87, 108, 0.3);
    }
    
    .metric-value {
        font-size: 2.5rem;
        font-weight: 700;
        background: linear-gradient(135deg, #f093fb 0%, #4facfe 100%);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        background-clip: text;
    }
    
    .metric-label {
        color: rgba(255,255,255,0.7);
        font-size: 0.9rem;
        margin-top: 0.3rem;
        letter-spacing: 1px;
    }
    
    .metric-icon {
        font-size: 2rem;
        margin-bottom: 0.5rem;
    }
    
    .section-title {
        font-size: 1.5rem;
        font-weight: 600;
        color: white;
        padding: 1rem 0;
        border-bottom: 2px solid rgba(245, 87, 108, 0.3);
        margin-bottom: 1.5rem;
        letter-spacing: 1px;
    }
    
    .footer {
        text-align: center;
        color: rgba(255,255,255,0.3);
        padding: 2rem 0;
        font-size: 0.8rem;
        letter-spacing: 2px;
        border-top: 1px solid rgba(255,255,255,0.05);
    }
    
    /* Стили для подзаголовков графиков */
    .chart-subtitle-starts {
        color: #4facfe !important;
        font-size: 1.1rem !important;
        font-weight: 700 !important;
        padding: 0.5rem 0 !important;
        margin-bottom: 0.5rem !important;
        text-shadow: 0 0 20px rgba(79, 172, 254, 0.4) !important;
        letter-spacing: 1px !important;
    }
    
    .chart-subtitle-streams {
        color: #f5576c !important;
        font-size: 1.1rem !important;
        font-weight: 700 !important;
        padding: 0.5rem 0 !important;
        margin-bottom: 0.5rem !important;
        text-shadow: 0 0 20px rgba(245, 87, 108, 0.4) !important;
        letter-spacing: 1px !important;
    }
    
    .chart-subtitle-conversion {
        color: #43e97b !important;
        font-size: 1.1rem !important;
        font-weight: 700 !important;
        padding: 0.5rem 0 !important;
        margin-bottom: 0.5rem !important;
        text-shadow: 0 0 20px rgba(67, 233, 123, 0.4) !important;
        letter-spacing: 1px !important;
    }
    
    /* Информационный блок */
    .info-block {
        background: rgba(255,255,255,0.03);
        border: 1px solid rgba(255,255,255,0.08);
        border-radius: 15px;
        padding: 1.5rem;
        margin-bottom: 1.5rem;
    }
    
    .info-title {
        color: white;
        font-size: 1.1rem;
        font-weight: 600;
        margin-bottom: 0.8rem;
        letter-spacing: 1px;
    }
    
    /* Стили для боковой панели */
    .css-1d391kg {
        background: rgba(10, 8, 30, 0.98) !important;
        backdrop-filter: blur(20px);
        border-right: 1px solid rgba(255,255,255,0.05);
    }
    
    .css-1d391kg .stSelectbox label,
    .css-1d391kg .stDateInput label,
    .css-1d391kg .stMarkdown,
    .css-1d391kg .stCaption,
    .css-1d391kg .stText {
        color: rgba(255,255,255,0.9) !important;
    }
    
    .css-1d391kg .stSelectbox > div > div {
        background: rgba(255,255,255,0.08);
        border-radius: 10px;
        color: white !important;
        border: 1px solid rgba(255,255,255,0.1);
    }
    
    .css-1d391kg .stDateInput > div > div {
        background: rgba(255,255,255,0.08);
        border-radius: 10px;
        color: white !important;
        border: 1px solid rgba(255,255,255,0.1);
    }
    
    .css-1d391kg .stDateInput input {
        color: white !important;
    }
    
    .css-1d391kg .stSelectbox select {
        color: white !important;
    }
    
    ::-webkit-scrollbar {
        width: 8px;
        height: 8px;
    }
    ::-webkit-scrollbar-track {
        background: rgba(255,255,255,0.05);
    }
    ::-webkit-scrollbar-thumb {
        background: linear-gradient(135deg, #f093fb, #4facfe);
        border-radius: 10px;
    }
    
    /* Стили для карточек информации о выпуске */
    .info-card {
        background: rgba(255,255,255,0.05);
        backdrop-filter: blur(10px);
        border: 1px solid rgba(255,255,255,0.1);
        border-radius: 15px;
        padding: 1.2rem;
        text-align: center;
        transition: all 0.3s ease;
        box-shadow: 0 4px 16px rgba(0,0,0,0.2);
        margin-bottom: 0.5rem;
    }
    
    .info-card:hover {
        transform: translateY(-3px);
        box-shadow: 0 8px 24px rgba(245, 87, 108, 0.15);
        border-color: rgba(245, 87, 108, 0.2);
    }
    
    .info-card-label {
        color: rgba(255,255,255,0.6);
        font-size: 0.8rem;
        letter-spacing: 1px;
        margin-bottom: 0.3rem;
        text-transform: uppercase;
    }
    
    .info-card-value {
        font-size: 1.1rem;
        font-weight: 600;
        color: white;
    }
</style>
""", unsafe_allow_html=True)

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
        
        return df_total, df_ref, short_names_dict
    except Exception as e:
        st.error(f"❌ Ошибка загрузки данных: {e}")
        st.stop()

with st.spinner("🔄 Загрузка данных..."):
    df_total, df_ref, short_names_dict = load_data()

df_merged = df_total.merge(df_ref, on='Выпуск', how='left')

# ============================================
# РАСЧЕТ RSI
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
# ВСПОМОГАТЕЛЬНЫЕ ФУНКЦИИ
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

# ============================================
# ФОРМИРОВАНИЕ ХРОНОЛОГИЧЕСКОГО СПИСКА ВЫПУСКОВ
# ============================================
# Берём порядок из справочника (как в Excel)
chronological_episodes = df_ref['Выпуск'].tolist()

# Создаём словарь: короткое_название -> полное_название (с учётом порядка из справочника)
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
st.markdown('<div class="sub-title">ПРЕМИУМ ДАШБОРД • АНАЛИТИКА ПРОСЛУШИВАНИЙ • ТРЕНДЫ</div>', unsafe_allow_html=True)

# ============================================
# НАВИГАЦИЯ
# ============================================
page = st.sidebar.radio(
    "📊 Меню",
    ["📊 Общая аналитика", "📋 Анализ выпуска", "🔄 Сравнение выпусков"],
    index=0
)

# ============================================
# СТРАНИЦА 1: ОБЩАЯ АНАЛИТИКА
# ============================================
if page == "📊 Общая аналитика":
    with st.sidebar:
        st.markdown("### 🎯 Управление данными")
        st.markdown("---")
        
        min_date = df_total['Дата прослушивания'].min().date()
        max_date = df_total['Дата прослушивания'].max().date()
        
        date_range = st.date_input(
            "📅 Период",
            value=(min_date, max_date),
            min_value=min_date,
            max_value=max_date
        )
        
        st.markdown("---")
        
        formats = ['Все'] + list(df_ref['Формат'].unique())
        selected_format = st.selectbox("📂 Формат", formats)
        
        genres = ['Все'] + list(df_ref['Жанр'].unique())
        selected_genre = st.selectbox("🎭 Жанр", genres)
        
        st.markdown("---")
        st.markdown("### 📊 Статистика")
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

    total_starts = filtered_data['Старты'].sum()
    total_streams = filtered_data['Стримы'].sum()
    conversion = (total_streams / total_starts * 100) if total_starts > 0 else 0
    unique_episodes = filtered_data['Выпуск'].nunique()
    avg_rsi = filtered_data['RSI'].mean()

    col1, col2, col3, col4, col5 = st.columns(5)

    with col1:
        st.markdown(f"""
        <div class="metric-card">
            <div class="metric-icon">🎬</div>
            <div class="metric-value">{total_starts:,}</div>
            <div class="metric-label">Всего стартов</div>
        </div>
        """, unsafe_allow_html=True)

    with col2:
        st.markdown(f"""
        <div class="metric-card">
            <div class="metric-icon">🎧</div>
            <div class="metric-value">{total_streams:,}</div>
            <div class="metric-label">Всего стримов</div>
        </div>
        """, unsafe_allow_html=True)

    with col3:
        st.markdown(f"""
        <div class="metric-card">
            <div class="metric-icon">📈</div>
            <div class="metric-value">{conversion:.1f}%</div>
            <div class="metric-label">Конверсия</div>
        </div>
        """, unsafe_allow_html=True)

    with col4:
        st.markdown(f"""
        <div class="metric-card">
            <div class="metric-icon">📝</div>
            <div class="metric-value">{unique_episodes}</div>
            <div class="metric-label">Выпусков</div>
        </div>
        """, unsafe_allow_html=True)

    with col5:
        st.markdown(f"""
        <div class="metric-card">
            <div class="metric-icon">⭐</div>
            <div class="metric-value">{avg_rsi:.1f}</div>
            <div class="metric-label">Средний RSI</div>
        </div>
        """, unsafe_allow_html=True)

    st.markdown("---")

    st.markdown("""
    <div class="info-block">
        <div class="info-title">📖 Что означают метрики</div>
        <div style="display: grid; grid-template-columns: 1fr 1fr 1fr; gap: 1rem;">
            <div>
                <div style="color: #4facfe; font-weight: 700; font-size: 1rem; margin-bottom: 0.3rem;">🎬 Старты</div>
                <div style="color: rgba(255,255,255,0.7); font-size: 0.85rem;">Количество запусков выпуска — базовый показатель популярности</div>
            </div>
            <div>
                <div style="color: #f5576c; font-weight: 700; font-size: 1rem; margin-bottom: 0.3rem;">🎧 Стримы</div>
                <div style="color: rgba(255,255,255,0.7); font-size: 0.85rem;">Прослушивания > 2 минут — показатель вовлеченности</div>
            </div>
            <div>
                <div style="color: #43e97b; font-weight: 700; font-size: 1rem; margin-bottom: 0.3rem;">📈 Конверсия</div>
                <div style="color: rgba(255,255,255,0.7); font-size: 0.85rem;">Стримы / Старты × 100%</div>
            </div>
            <div style="grid-column: span 3; margin-top: 0.5rem; padding-top: 0.8rem; border-top: 1px solid rgba(255,255,255,0.05);">
                <div style="color: #f093fb; font-weight: 700; font-size: 1rem; margin-bottom: 0.3rem;">⭐ RSI — Индекс успешности выпуска</div>
                <div style="color: rgba(255,255,255,0.7); font-size: 0.85rem;">
                    <strong style="color: #f5576c;">Стримы</strong> × 
                    (<strong style="color: #43e97b;">Конверсия</strong> + 1) × 
                    <strong style="color: #4facfe;">Старты<sup>0.1</sup></strong>
                </div>
            </div>
        </div>
    </div>
    """, unsafe_allow_html=True)

    st.markdown('<div class="section-title">📊 Динамика прослушиваний</div>', unsafe_allow_html=True)

    daily_stats = filtered_data.groupby('Дата прослушивания').agg({
        'Старты': 'sum',
        'Стримы': 'sum'
    }).reset_index()
    daily_stats['Конверсия'] = (daily_stats['Стримы'] / daily_stats['Старты'] * 100).fillna(0)

    fig1 = make_subplots(specs=[[{"secondary_y": True}]])

    fig1.add_trace(go.Scatter(
        x=daily_stats['Дата прослушивания'],
        y=daily_stats['Старты'],
        name='Старты',
        line=dict(color='#4facfe', width=3),
        fill='tozeroy',
        fillcolor='rgba(79, 172, 254, 0.15)',
        mode='lines+markers',
        marker=dict(size=6, color='white', line=dict(color='#4facfe', width=2))
    ))

    fig1.add_trace(go.Scatter(
        x=daily_stats['Дата прослушивания'],
        y=daily_stats['Стримы'],
        name='Стримы',
        line=dict(color='#f5576c', width=3),
        fill='tozeroy',
        fillcolor='rgba(245, 87, 108, 0.15)',
        mode='lines+markers',
        marker=dict(size=6, color='white', line=dict(color='#f5576c', width=2))
    ))

    fig1.add_trace(go.Scatter(
        x=daily_stats['Дата прослушивания'],
        y=daily_stats['Конверсия'],
        name='Конверсия (%)',
        line=dict(color='#43e97b', width=2, dash='dash'),
        mode='lines+markers',
        marker=dict(size=5, color='#43e97b')
    ), secondary_y=True)

    fig1.update_layout(
        template='plotly_dark',
        plot_bgcolor='rgba(0,0,0,0)',
        paper_bgcolor='rgba(0,0,0,0)',
        height=500,
        hovermode='x unified',
        legend=dict(orientation='h', yanchor='bottom', y=1.02, xanchor='right', x=1, font=dict(color='white', size=12)),
        xaxis=dict(title='Дата', titlefont=dict(color='white', size=13), tickfont=dict(color='white', size=11), gridcolor='rgba(255,255,255,0.05)'),
        yaxis=dict(title='Количество', titlefont=dict(color='white', size=13), tickfont=dict(color='white', size=11), gridcolor='rgba(255,255,255,0.05)'),
        yaxis2=dict(title='Конверсия (%)', titlefont=dict(color='#43e97b', size=13), tickfont=dict(color='#43e97b', size=11), overlaying='y', side='right', showgrid=False)
    )

    st.plotly_chart(fig1, use_container_width=True)

    st.markdown('<div class="section-title">🏆 Топ выпусков по RSI</div>', unsafe_allow_html=True)

    episode_rsi = filtered_data.groupby(['Выпуск', 'Короткое название']).agg({
        'Старты': 'sum',
        'Стримы': 'sum',
        'RSI': 'mean'
    }).reset_index()
    episode_rsi['Конверсия'] = (episode_rsi['Стримы'] / episode_rsi['Старты'] * 100).fillna(0)
    episode_rsi = episode_rsi.sort_values('RSI', ascending=False)
    top_rsi = episode_rsi.head(10)

    col1, col2 = st.columns([2, 1])

    with col1:
        display_names = top_rsi['Короткое название'].tolist()
        
        fig2 = go.Figure()
        fig2.add_trace(go.Bar(
            x=display_names,
            y=top_rsi['RSI'],
            marker=dict(color=top_rsi['RSI'], colorscale='Viridis', showscale=True, colorbar=dict(title='RSI', titlefont=dict(color='white'), tickfont=dict(color='white'))),
            text=top_rsi['RSI'].round(1),
            textposition='outside',
            textfont=dict(color='white', size=11),
            hovertemplate='<b>%{x}</b><br>RSI: %{y:.1f}<br>Старты: %{customdata[0]:,}<br>Стримы: %{customdata[1]:,}<br>Конверсия: %{customdata[2]:.1f}%<extra></extra>',
            customdata=top_rsi[['Старты', 'Стримы', 'Конверсия']].values
        ))
        
        fig2.update_layout(
            template='plotly_dark',
            plot_bgcolor='rgba(0,0,0,0)',
            paper_bgcolor='rgba(0,0,0,0)',
            height=500,
            xaxis=dict(tickangle=-20, tickfont=dict(color='white', size=10), gridcolor='rgba(255,255,255,0.05)'),
            yaxis=dict(title='RSI', titlefont=dict(color='white', size=13), tickfont=dict(color='white', size=11), gridcolor='rgba(255,255,255,0.05)')
        )
        
        st.plotly_chart(fig2, use_container_width=True)

    with col2:
        st.markdown("""
        <div style="background: rgba(255,255,255,0.03); border-radius: 15px; padding: 1.5rem; border: 1px solid rgba(255,255,255,0.05);">
            <h4 style="color: white; margin-bottom: 1rem;">⭐ Топ RSI</h4>
        """, unsafe_allow_html=True)
        
        if len(top_rsi) > 0:
            for i, (idx, row) in enumerate(top_rsi.head(5).iterrows()):
                medal = ['🥇', '🥈', '🥉', '4️⃣', '5️⃣'][i]
                name = row['Короткое название']
                st.markdown(f"""
                <div style="color: rgba(255,255,255,0.8); margin-bottom: 0.5rem; font-size: 0.9rem;">
                    {medal} <span style="color: #4facfe; font-weight: 600;">{name}</span> — RSI: {row['RSI']:.1f}
                </div>
                """, unsafe_allow_html=True)
        
        st.markdown("</div>", unsafe_allow_html=True)

    st.markdown("---")

    st.markdown('<div class="section-title">🎭 Топ жанров</div>', unsafe_allow_html=True)

    genre_stats = filtered_data.groupby('Жанр').agg({
        'Старты': 'sum',
        'Стримы': 'sum',
        'RSI': 'mean'
    }).reset_index()
    genre_stats['Конверсия'] = (genre_stats['Стримы'] / genre_stats['Старты'] * 100).fillna(0)
    genre_stats = genre_stats.sort_values('Старты', ascending=False)

    col1, col2, col3 = st.columns(3)

    with col1:
        st.markdown('<div class="chart-subtitle-starts">📊 По стартам</div>', unsafe_allow_html=True)
        top_genre_starts = genre_stats.head(8)
        
        fig3 = go.Figure(data=[go.Bar(
            x=top_genre_starts['Жанр'],
            y=top_genre_starts['Старты'],
            marker=dict(color=top_genre_starts['Старты'], colorscale='Blues', showscale=False),
            text=top_genre_starts['Старты'],
            textposition='outside',
            textfont=dict(color='white', size=10)
        )])
        fig3.update_layout(template='plotly_dark', plot_bgcolor='rgba(0,0,0,0)', paper_bgcolor='rgba(0,0,0,0)', height=300, xaxis=dict(tickangle=-15, tickfont=dict(color='white', size=9)), yaxis=dict(title='Старты', titlefont=dict(color='#4facfe', size=11), tickfont=dict(color='white', size=9), gridcolor='rgba(255,255,255,0.05)'), showlegend=False)
        st.plotly_chart(fig3, use_container_width=True)

    with col2:
        st.markdown('<div class="chart-subtitle-streams">🎧 По стримам</div>', unsafe_allow_html=True)
        top_genre_streams = genre_stats.sort_values('Стримы', ascending=False).head(8)
        
        fig4 = go.Figure(data=[go.Bar(
            x=top_genre_streams['Жанр'],
            y=top_genre_streams['Стримы'],
            marker=dict(color=top_genre_streams['Стримы'], colorscale='Reds', showscale=False),
            text=top_genre_streams['Стримы'],
            textposition='outside',
            textfont=dict(color='white', size=10)
        )])
        fig4.update_layout(template='plotly_dark', plot_bgcolor='rgba(0,0,0,0)', paper_bgcolor='rgba(0,0,0,0)', height=300, xaxis=dict(tickangle=-15, tickfont=dict(color='white', size=9)), yaxis=dict(title='Стримы', titlefont=dict(color='#f5576c', size=11), tickfont=dict(color='white', size=9), gridcolor='rgba(255,255,255,0.05)'), showlegend=False)
        st.plotly_chart(fig4, use_container_width=True)

    with col3:
        st.markdown('<div class="chart-subtitle-conversion">📈 По конверсии</div>', unsafe_allow_html=True)
        top_genre_conv = genre_stats[genre_stats['Старты'] > 10].sort_values('Конверсия', ascending=False).head(8)
        
        fig5 = go.Figure(data=[go.Bar(
            x=top_genre_conv['Жанр'],
            y=top_genre_conv['Конверсия'],
            marker=dict(color=top_genre_conv['Конверсия'], colorscale='Greens', showscale=False),
            text=top_genre_conv['Конверсия'].round(1),
            textposition='outside',
            textfont=dict(color='white', size=10)
        )])
        fig5.update_layout(template='plotly_dark', plot_bgcolor='rgba(0,0,0,0)', paper_bgcolor='rgba(0,0,0,0)', height=300, xaxis=dict(tickangle=-15, tickfont=dict(color='white', size=9)), yaxis=dict(title='Конверсия (%)', titlefont=dict(color='#43e97b', size=11), tickfont=dict(color='white', size=9), gridcolor='rgba(255,255,255,0.05)'), showlegend=False)
        st.plotly_chart(fig5, use_container_width=True)

    st.markdown("---")

    st.markdown('<div class="section-title">📅 Активность по дням недели</div>', unsafe_allow_html=True)

    filtered_data['День недели'] = filtered_data['Дата прослушивания'].dt.day_name()
    weekday_order = ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday', 'Sunday']
    weekday_labels = ['Пн', 'Вт', 'Ср', 'Чт', 'Пт', 'Сб', 'Вс']

    weekday_stats = filtered_data.groupby('День недели').agg({
        'Старты': 'sum',
        'Стримы': 'sum'
    }).reindex(weekday_order).reset_index()
    weekday_stats['День'] = weekday_labels

    col1, col2 = st.columns(2)

    with col1:
        st.markdown('<div class="chart-subtitle-starts">📊 По стартам</div>', unsafe_allow_html=True)
        fig6 = go.Figure(data=[go.Bar(
            x=weekday_stats['День'],
            y=weekday_stats['Старты'],
            marker=dict(color=['#4facfe', '#43e97b', '#f093fb', '#f5576c', '#fa709a', '#f6d365', '#a8edea'], line=dict(color='white', width=1)),
            text=weekday_stats['Старты'],
            textposition='outside',
            textfont=dict(color='white', size=11)
        )])
        fig6.update_layout(template='plotly_dark', plot_bgcolor='rgba(0,0,0,0)', paper_bgcolor='rgba(0,0,0,0)', height=350, xaxis=dict(title='День недели', titlefont=dict(color='white', size=12), tickfont=dict(color='white', size=11)), yaxis=dict(title='Старты', titlefont=dict(color='#4facfe', size=12), tickfont=dict(color='white', size=11), gridcolor='rgba(255,255,255,0.05)'), showlegend=False)
        st.plotly_chart(fig6, use_container_width=True)

    with col2:
        st.markdown('<div class="chart-subtitle-streams">🎧 По стримам</div>', unsafe_allow_html=True)
        fig7 = go.Figure(data=[go.Bar(
            x=weekday_stats['День'],
            y=weekday_stats['Стримы'],
            marker=dict(color=['#4facfe', '#43e97b', '#f093fb', '#f5576c', '#fa709a', '#f6d365', '#a8edea'], line=dict(color='white', width=1)),
            text=weekday_stats['Стримы'],
            textposition='outside',
            textfont=dict(color='white', size=11)
        )])
        fig7.update_layout(template='plotly_dark', plot_bgcolor='rgba(0,0,0,0)', paper_bgcolor='rgba(0,0,0,0)', height=350, xaxis=dict(title='День недели', titlefont=dict(color='white', size=12), tickfont=dict(color='white', size=11)), yaxis=dict(title='Стримы', titlefont=dict(color='#f5576c', size=12), tickfont=dict(color='white', size=11), gridcolor='rgba(255,255,255,0.05)'), showlegend=False)
        st.plotly_chart(fig7, use_container_width=True)

    st.markdown("---")

    st.markdown('<div class="section-title">📋 Полная сводка по выпускам</div>', unsafe_allow_html=True)

    episode_summary = filtered_data.groupby(['Выпуск', 'Короткое название']).agg({
        'Старты': 'sum',
        'Стримы': 'sum',
        'RSI': 'mean',
        'Формат': 'first',
        'Жанр': 'first'
    }).reset_index()
    episode_summary['Конверсия'] = (episode_summary['Стримы'] / episode_summary['Старты'] * 100).fillna(0)
    episode_summary = episode_summary.sort_values('RSI', ascending=False)

    display_df = episode_summary[['Короткое название', 'Старты', 'Стримы', 'Конверсия', 'RSI', 'Формат', 'Жанр']].copy()
    display_df.columns = ['Название', 'Старты', 'Стримы', 'Конверсия %', 'RSI', 'Формат', 'Жанр']

    try:
        st.dataframe(display_df.head(50), width=1200, height=400)
    except:
        st.dataframe(display_df.head(50), height=400)

    st.markdown("---")
    st.markdown("""
    <div class="footer">
        🎙️ Подкаст Аналитика Pro • Премиум дашборд • Данные обновляются автоматически
    </div>
    """, unsafe_allow_html=True)

    with st.expander("ℹ️ Информация о данных", expanded=False):
        col1, col2, col3 = st.columns(3)
        with col1:
            st.markdown(f"""
            <div style="color: rgba(255,255,255,0.9); font-size: 1rem;">
                <strong style="color: white; font-size: 1.05rem;">📅 Период</strong><br>
                {filtered_data['Дата прослушивания'].min().date()} — {filtered_data['Дата прослушивания'].max().date()}
            </div>
            <div style="color: rgba(255,255,255,0.9); font-size: 1rem; margin-top: 0.8rem;">
                <strong style="color: white; font-size: 1.05rem;">📊 Всего записей</strong><br>
                {len(filtered_data):,}
            </div>
            """, unsafe_allow_html=True)
        with col2:
            st.markdown(f"""
            <div style="color: rgba(255,255,255,0.9); font-size: 1rem;">
                <strong style="color: white; font-size: 1.05rem;">📝 Уникальных выпусков</strong><br>
                {filtered_data['Выпуск'].nunique()}
            </div>
            <div style="color: rgba(255,255,255,0.9); font-size: 1rem; margin-top: 0.8rem;">
                <strong style="color: white; font-size: 1.05rem;">🎭 Жанры</strong><br>
                {', '.join(filtered_data['Жанр'].unique())}
            </div>
            """, unsafe_allow_html=True)
        with col3:
            st.markdown(f"""
            <div style="color: rgba(255,255,255,0.9); font-size: 1rem;">
                <strong style="color: white; font-size: 1.05rem;">📂 Форматы</strong><br>
                {', '.join(filtered_data['Формат'].unique())}
            </div>
            <div style="color: rgba(255,255,255,0.9); font-size: 1rem; margin-top: 0.8rem;">
                <strong style="color: white; font-size: 1.05rem;">⭐ Средний RSI</strong><br>
                {episode_summary['RSI'].mean():.1f}
            </div>
            """, unsafe_allow_html=True)


# ============================================
# СТРАНИЦА 2: АНАЛИЗ ВЫПУСКА
# ============================================
elif page == "📋 Анализ выпуска":
    st.title("📋 Детальный анализ выпуска")
    
    st.markdown("### 📅 Период")
    period = st.radio(
        "",
        ["1 день", "1 неделя", "1 месяц", "Всё время"],
        horizontal=True,
        index=3
    )
    
    # Используем хронологический порядок из справочника
    selected_short = st.selectbox("🎯 Выберите выпуск:", short_names_ordered)
    selected_episode = episode_names_ordered[selected_short]
    
    all_data = df_merged[df_merged['Выпуск'] == selected_episode].copy()
    
    # Находим фактическую первую дату прослушивания в данных
    release_date = df_total[df_total['Выпуск'] == selected_episode]['Дата прослушивания'].min()
    
    if all_data.empty:
        st.warning(f"⚠️ Нет данных для выпуска '{selected_short}'")
    else:
        if period == "1 день":
            episode_data = all_data[
                (all_data['Дата прослушивания'] >= release_date) &
                (all_data['Дата прослушивания'] <= release_date + pd.Timedelta(days=0))
            ]
        elif period == "1 неделя":
            episode_data = all_data[
                (all_data['Дата прослушивания'] >= release_date) &
                (all_data['Дата прослушивания'] <= release_date + pd.Timedelta(days=6))
            ]
        elif period == "1 месяц":
            episode_data = all_data[
                (all_data['Дата прослушивания'] >= release_date) &
                (all_data['Дата прослушивания'] <= release_date + pd.Timedelta(days=29))
            ]
        else:
            episode_data = all_data
        
        if episode_data.empty:
            st.warning(f"⚠️ Нет данных для выпуска '{selected_short}' в выбранном периоде")
        else:
            # Метрики в виде карточек
            total_starts_ep = episode_data['Старты'].sum()
            total_streams_ep = episode_data['Стримы'].sum()
            conv_ep = (total_streams_ep / total_starts_ep * 100) if total_starts_ep > 0 else 0
            rsi_ep = episode_data['RSI'].mean()
            
            col1, col2, col3, col4 = st.columns(4)
            
            with col1:
                st.markdown(f"""
                <div class="metric-card">
                    <div class="metric-icon">🎬</div>
                    <div class="metric-value">{total_starts_ep:,}</div>
                    <div class="metric-label">Всего стартов</div>
                </div>
                """, unsafe_allow_html=True)
            
            with col2:
                st.markdown(f"""
                <div class="metric-card">
                    <div class="metric-icon">🎧</div>
                    <div class="metric-value">{total_streams_ep:,}</div>
                    <div class="metric-label">Всего стримов</div>
                </div>
                """, unsafe_allow_html=True)
            
            with col3:
                st.markdown(f"""
                <div class="metric-card">
                    <div class="metric-icon">📈</div>
                    <div class="metric-value">{conv_ep:.1f}%</div>
                    <div class="metric-label">Конверсия</div>
                </div>
                """, unsafe_allow_html=True)
            
            with col4:
                st.markdown(f"""
                <div class="metric-card">
                    <div class="metric-icon">⭐</div>
                    <div class="metric-value">{rsi_ep:.1f}</div>
                    <div class="metric-label">Средний RSI</div>
                </div>
                """, unsafe_allow_html=True)
            
            # Карточки с информацией о выпуске
            st.markdown("---")
            st.markdown('<div class="section-title">ℹ️ Информация о выпуске</div>', unsafe_allow_html=True)
            
            info = df_ref[df_ref['Выпуск'] == selected_episode].iloc[0]
            days_active = (episode_data['Дата прослушивания'].max() - episode_data['Дата прослушивания'].min()).days
            
            col1, col2, col3, col4, col5 = st.columns(5)
            
            with col1:
                st.markdown(f"""
                <div class="info-card">
                    <div class="info-card-label">📂 Формат</div>
                    <div class="info-card-value">{info['Формат']}</div>
                </div>
                """, unsafe_allow_html=True)
            
            with col2:
                st.markdown(f"""
                <div class="info-card">
                    <div class="info-card-label">🎭 Жанр</div>
                    <div class="info-card-value">{info['Жанр']}</div>
                </div>
                """, unsafe_allow_html=True)
            
            with col3:
                st.markdown(f"""
                <div class="info-card">
                    <div class="info-card-label">📅 Первая дата</div>
                    <div class="info-card-value">{release_date.date()}</div>
                </div>
                """, unsafe_allow_html=True)
            
            with col4:
                st.markdown(f"""
                <div class="info-card">
                    <div class="info-card-label">📆 Дней в выборке</div>
                    <div class="info-card-value">{days_active + 1}</div>
                </div>
                """, unsafe_allow_html=True)
            
            with col5:
                st.markdown(f"""
                <div class="info-card">
                    <div class="info-card-label">⏱️ Длительность</div>
                    <div class="info-card-value">{info['Длительность']}</div>
                </div>
                """, unsafe_allow_html=True)
            
            st.markdown("---")
            
            st.subheader("📊 Сравнение со средними показателями")
            
            compare_data = df_merged.copy()
            if period == "1 день":
                compare_data = compare_data[
                    (compare_data['Дата прослушивания'] >= release_date) &
                    (compare_data['Дата прослушивания'] <= release_date + pd.Timedelta(days=0))
                ]
            elif period == "1 неделя":
                compare_data = compare_data[
                    (compare_data['Дата прослушивания'] >= release_date) &
                    (compare_data['Дата прослушивания'] <= release_date + pd.Timedelta(days=6))
                ]
            elif period == "1 месяц":
                compare_data = compare_data[
                    (compare_data['Дата прослушивания'] >= release_date) &
                    (compare_data['Дата прослушивания'] <= release_date + pd.Timedelta(days=29))
                ]
            
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
            
            st.subheader("📈 Динамика прослушиваний")
            daily_data = episode_data.groupby('Дата прослушивания').agg({
                'Старты': 'sum',
                'Стримы': 'sum'
            }).reset_index()
            
            fig = go.Figure()
            fig.add_trace(go.Scatter(
                x=daily_data['Дата прослушивания'],
                y=daily_data['Старты'],
                name='Старты',
                line=dict(color='#4facfe', width=3),
                fill='tozeroy',
                fillcolor='rgba(79, 172, 254, 0.15)'
            ))
            fig.add_trace(go.Scatter(
                x=daily_data['Дата прослушивания'],
                y=daily_data['Стримы'],
                name='Стримы',
                line=dict(color='#f5576c', width=3),
                fill='tozeroy',
                fillcolor='rgba(245, 87, 108, 0.15)'
            ))
            
            # ВЕРТИКАЛЬНАЯ ЛИНИЯ РЕЛИЗА
            fig.add_shape(
                type="line",
                x0=release_date,
                y0=0,
                x1=release_date,
                y1=1,
                yref="paper",
                line=dict(color="#f093fb", width=2, dash="dash")
            )
            fig.add_annotation(
                x=release_date,
                y=0.98,
                yref="paper",
                text="📅 Релиз",
                showarrow=False,
                font=dict(color="#f093fb", size=12),
                textangle=-90
            )
            
            fig.update_layout(
                template='plotly_dark',
                plot_bgcolor='rgba(0,0,0,0)',
                paper_bgcolor='rgba(0,0,0,0)',
                height=400,
                hovermode='x unified',
                legend=dict(orientation='h', yanchor='bottom', y=1.02, xanchor='right', x=1, font=dict(color='white'))
            )
            st.plotly_chart(fig, use_container_width=True)


# ============================================
# СТРАНИЦА 3: СРАВНЕНИЕ ВЫПУСКОВ
# ============================================
else:
    st.title("🔄 Сравнение двух выпусков")
    
    st.markdown("### 📅 Период")
    period = st.radio(
        "",
        ["1 день", "1 неделя", "1 месяц", "Всё время"],
        horizontal=True,
        index=3
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
            data1 = all_data[
                (all_data['Выпуск'] == ep1) &
                (all_data['Дата прослушивания'] >= release_date1) &
                (all_data['Дата прослушивания'] <= release_date1 + pd.Timedelta(days=0))
            ]
            data2 = all_data[
                (all_data['Выпуск'] == ep2) &
                (all_data['Дата прослушивания'] >= release_date2) &
                (all_data['Дата прослушивания'] <= release_date2 + pd.Timedelta(days=0))
            ]
        elif period == "1 неделя":
            data1 = all_data[
                (all_data['Выпуск'] == ep1) &
                (all_data['Дата прослушивания'] >= release_date1) &
                (all_data['Дата прослушивания'] <= release_date1 + pd.Timedelta(days=6))
            ]
            data2 = all_data[
                (all_data['Выпуск'] == ep2) &
                (all_data['Дата прослушивания'] >= release_date2) &
                (all_data['Дата прослушивания'] <= release_date2 + pd.Timedelta(days=6))
            ]
        elif period == "1 месяц":
            data1 = all_data[
                (all_data['Выпуск'] == ep1) &
                (all_data['Дата прослушивания'] >= release_date1) &
                (all_data['Дата прослушивания'] <= release_date1 + pd.Timedelta(days=29))
            ]
            data2 = all_data[
                (all_data['Выпуск'] == ep2) &
                (all_data['Дата прослушивания'] >= release_date2) &
                (all_data['Дата прослушивания'] <= release_date2 + pd.Timedelta(days=29))
            ]
        else:
            data1 = all_data[all_data['Выпуск'] == ep1]
            data2 = all_data[all_data['Выпуск'] == ep2]
        
        if data1.empty or data2.empty:
            st.warning("⚠️ Нет данных для выбранных выпусков в этом периоде")
        else:
            # Карточки с метриками для двух выпусков
            total_starts1 = data1['Старты'].sum()
            total_streams1 = data1['Стримы'].sum()
            conv1 = (total_streams1 / total_starts1 * 100) if total_starts1 > 0 else 0
            rsi1 = data1['RSI'].mean()
            
            total_starts2 = data2['Старты'].sum()
            total_streams2 = data2['Стримы'].sum()
            conv2 = (total_streams2 / total_starts2 * 100) if total_starts2 > 0 else 0
            rsi2 = data2['RSI'].mean()
            
            st.markdown('<div class="section-title">📊 Сравнение метрик</div>', unsafe_allow_html=True)
            
            col1, col2 = st.columns(2)
            
            with col1:
                st.markdown(f"""
                <div style="background: rgba(79, 172, 254, 0.1); border: 1px solid rgba(79, 172, 254, 0.3); border-radius: 15px; padding: 1.5rem; margin-bottom: 1rem;">
                    <h3 style="color: #4facfe; text-align: center; margin-bottom: 1rem;">{ep1_short}</h3>
                </div>
                """, unsafe_allow_html=True)
                
                subcol1, subcol2, subcol3, subcol4 = st.columns(4)
                with subcol1:
                    st.markdown(f"""
                    <div class="metric-card">
                        <div class="metric-icon">🎬</div>
                        <div class="metric-value">{total_starts1:,}</div>
                        <div class="metric-label">Старты</div>
                    </div>
                    """, unsafe_allow_html=True)
                with subcol2:
                    st.markdown(f"""
                    <div class="metric-card">
                        <div class="metric-icon">🎧</div>
                        <div class="metric-value">{total_streams1:,}</div>
                        <div class="metric-label">Стримы</div>
                    </div>
                    """, unsafe_allow_html=True)
                with subcol3:
                    st.markdown(f"""
                    <div class="metric-card">
                        <div class="metric-icon">📈</div>
                        <div class="metric-value">{conv1:.1f}%</div>
                        <div class="metric-label">Конверсия</div>
                    </div>
                    """, unsafe_allow_html=True)
                with subcol4:
                    st.markdown(f"""
                    <div class="metric-card">
                        <div class="metric-icon">⭐</div>
                        <div class="metric-value">{rsi1:.1f}</div>
                        <div class="metric-label">RSI</div>
                    </div>
                    """, unsafe_allow_html=True)
            
            with col2:
                st.markdown(f"""
                <div style="background: rgba(245, 87, 108, 0.1); border: 1px solid rgba(245, 87, 108, 0.3); border-radius: 15px; padding: 1.5rem; margin-bottom: 1rem;">
                    <h3 style="color: #f5576c; text-align: center; margin-bottom: 1rem;">{ep2_short}</h3>
                </div>
                """, unsafe_allow_html=True)
                
                subcol1, subcol2, subcol3, subcol4 = st.columns(4)
                with subcol1:
                    st.markdown(f"""
                    <div class="metric-card">
                        <div class="metric-icon">🎬</div>
                        <div class="metric-value">{total_starts2:,}</div>
                        <div class="metric-label">Старты</div>
                    </div>
                    """, unsafe_allow_html=True)
                with subcol2:
                    st.markdown(f"""
                    <div class="metric-card">
                        <div class="metric-icon">🎧</div>
                        <div class="metric-value">{total_streams2:,}</div>
                        <div class="metric-label">Стримы</div>
                    </div>
                    """, unsafe_allow_html=True)
                with subcol3:
                    st.markdown(f"""
                    <div class="metric-card">
                        <div class="metric-icon">📈</div>
                        <div class="metric-value">{conv2:.1f}%</div>
                        <div class="metric-label">Конверсия</div>
                    </div>
                    """, unsafe_allow_html=True)
                with subcol4:
                    st.markdown(f"""
                    <div class="metric-card">
                        <div class="metric-icon">⭐</div>
                        <div class="metric-value">{rsi2:.1f}</div>
                        <div class="metric-label">RSI</div>
                    </div>
                    """, unsafe_allow_html=True)
            
            st.markdown("---")
            
            # Графики по дням от релиза
            st.markdown('<div class="section-title">📈 Динамика по дням от релиза</div>', unsafe_allow_html=True)
            
            # Преобразуем даты в дни от релиза
            data1_copy = data1.copy()
            data2_copy = data2.copy()
            
            data1_copy['День от релиза'] = (data1_copy['Дата прослушивания'] - release_date1).dt.days + 1
            data2_copy['День от релиза'] = (data2_copy['Дата прослушивания'] - release_date2).dt.days + 1
            
            daily1 = data1_copy.groupby('День от релиза').agg({
                'Старты': 'sum',
                'Стримы': 'sum'
            }).reset_index()
            
            daily2 = data2_copy.groupby('День от релиза').agg({
                'Старты': 'sum',
                'Стримы': 'sum'
            }).reset_index()
            
            # График стартов
            st.markdown('<div class="chart-subtitle-starts">🎬 Сравнение стартов по дням</div>', unsafe_allow_html=True)
            
            fig_starts = go.Figure()
            fig_starts.add_trace(go.Scatter(
                x=daily1['День от релиза'],
                y=daily1['Старты'],
                name=f'{ep1_short}',
                line=dict(color='#4facfe', width=3),
                mode='lines+markers',
                marker=dict(size=8, color='white', line=dict(color='#4facfe', width=2)),
                fill='tozeroy',
                fillcolor='rgba(79, 172, 254, 0.1)'
            ))
            fig_starts.add_trace(go.Scatter(
                x=daily2['День от релиза'],
                y=daily2['Старты'],
                name=f'{ep2_short}',
                line=dict(color='#f5576c', width=3),
                mode='lines+markers',
                marker=dict(size=8, color='white', line=dict(color='#f5576c', width=2)),
                fill='tozeroy',
                fillcolor='rgba(245, 87, 108, 0.1)'
            ))
            
            fig_starts.update_layout(
                template='plotly_dark',
                plot_bgcolor='rgba(0,0,0,0)',
                paper_bgcolor='rgba(0,0,0,0)',
                height=400,
                hovermode='x unified',
                legend=dict(orientation='h', yanchor='bottom', y=1.02, xanchor='right', x=1, font=dict(color='white')),
                xaxis=dict(title='День от релиза', titlefont=dict(color='white', size=13), tickfont=dict(color='white', size=11), gridcolor='rgba(255,255,255,0.05)'),
                yaxis=dict(title='Старты', titlefont=dict(color='#4facfe', size=13), tickfont=dict(color='white', size=11), gridcolor='rgba(255,255,255,0.05)')
            )
            
            st.plotly_chart(fig_starts, use_container_width=True)
            
            # График стримов
            st.markdown('<div class="chart-subtitle-streams">🎧 Сравнение стримов по дням</div>', unsafe_allow_html=True)
            
            fig_streams = go.Figure()
            fig_streams.add_trace(go.Scatter(
                x=daily1['День от релиза'],
                y=daily1['Стримы'],
                name=f'{ep1_short}',
                line=dict(color='#43e97b', width=3),
                mode='lines+markers',
                marker=dict(size=8, color='white', line=dict(color='#43e97b', width=2)),
                fill='tozeroy',
                fillcolor='rgba(67, 233, 123, 0.1)'
            ))
            fig_streams.add_trace(go.Scatter(
                x=daily2['День от релиза'],
                y=daily2['Стримы'],
                name=f'{ep2_short}',
                line=dict(color='#f093fb', width=3),
                mode='lines+markers',
                marker=dict(size=8, color='white', line=dict(color='#f093fb', width=2)),
                fill='tozeroy',
                fillcolor='rgba(240, 147, 251, 0.1)'
            ))
            
            fig_streams.update_layout(
                template='plotly_dark',
                plot_bgcolor='rgba(0,0,0,0)',
                paper_bgcolor='rgba(0,0,0,0)',
                height=400,
                hovermode='x unified',
                legend=dict(orientation='h', yanchor='bottom', y=1.02, xanchor='right', x=1, font=dict(color='white')),
                xaxis=dict(title='День от релиза', titlefont=dict(color='white', size=13), tickfont=dict(color='white', size=11), gridcolor='rgba(255,255,255,0.05)'),
                yaxis=dict(title='Стримы', titlefont=dict(color='#f5576c', size=13), tickfont=dict(color='white', size=11), gridcolor='rgba(255,255,255,0.05)')
            )
            
            st.plotly_chart(fig_streams, use_container_width=True)
            
            # Итоговый вердикт
            st.markdown("---")
            st.markdown('<div class="section-title">🏆 Итоговый вердикт</div>', unsafe_allow_html=True)
            
            col1, col2, col3 = st.columns([1, 1, 2])
            with col1:
                st.metric(f"⭐ RSI {ep1_short}", f"{rsi1:.1f}")
            with col2:
                st.metric(f"⭐ RSI {ep2_short}", f"{rsi2:.1f}")
            with col3:
                if rsi1 > rsi2 * 1.05:
                    st.success(f"🏆 **{ep1_short}** значительно лучше по RSI!")
                elif rsi1 > rsi2:
                    st.success(f"🏆 **{ep1_short}** лучше по RSI!")
                elif rsi2 > rsi1 * 1.05:
                    st.success(f"🏆 **{ep2_short}** значительно лучше по RSI!")
                elif rsi2 > rsi1:
                    st.success(f"🏆 **{ep2_short}** лучше по RSI!")
                else:
                    st.info("🤝 Выпуски примерно равны по RSI!")