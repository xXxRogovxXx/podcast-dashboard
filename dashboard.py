import streamlit as st
import pandas as pd
import numpy as np
import plotly.graph_objects as go
from plotly.subplots import make_subplots

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
    except Exception as e:
        st.error(f"❌ Ошибка загрузки данных: {e}")
        st.stop()
    
    df_total['Дата прослушивания'] = pd.to_datetime(df_total['Дата прослушивания'])
    df_ref['Дата релиза'] = pd.to_datetime(df_ref['Дата релиза'])
    
    try:
        df_short = pd.read_excel("Короткие названия.xlsx")
        short_names_dict = dict(zip(df_short['Оригинальное название'], df_short['Короткое название']))
        df_ref['Короткое название'] = df_ref['Выпуск'].map(short_names_dict).fillna(df_ref['Выпуск'])
    except:
        df_ref['Короткое название'] = df_ref['Выпуск']
    
    df_merged = df_total.merge(df_ref, on='Выпуск', how='left')
    df_merged['Конверсия_доля'] = df_merged['Стримы'] / df_merged['Старты']
    df_merged['Конверсия_доля'] = df_merged['Конверсия_доля'].fillna(0).replace([np.inf, -np.inf], 0)
    df_merged['RSI'] = df_merged['Стримы'] * (df_merged['Конверсия_доля'] + 1) * (df_merged['Старты'] ** 0.1)
    
    return df_total, df_ref, df_merged

df_total, df_ref, df_merged = load_data()

# ============================================
# ВСПОМОГАТЕЛЬНЫЕ ФУНКЦИИ
# ============================================
def get_short_name(long_name):
    try:
        df_short = pd.read_excel("Короткие названия.xlsx")
        short_names_dict = dict(zip(df_short['Оригинальное название'], df_short['Короткое название']))
        return short_names_dict.get(long_name, long_name)
    except:
        return long_name

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

def filter_by_period(df, period):
    if df.empty:
        return df
    max_date = df['Дата прослушивания'].max()
    if period == "1 день":
        return df[df['Дата прослушивания'] >= max_date - pd.Timedelta(days=1)]
    elif period == "1 неделя":
        return df[df['Дата прослушивания'] >= max_date - pd.Timedelta(days=7)]
    elif period == "1 месяц":
        return df[df['Дата прослушивания'] >= max_date - pd.Timedelta(days=30)]
    else:
        return df

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
# СТРАНИЦА 1: ОБЩАЯ АНАЛИТИКА (ВОССТАНОВЛЕНА)
# ============================================
if page == "📊 Общая аналитика":
    st.title("📊 Общая аналитика")
    
    # ФИЛЬТРЫ В САЙДБАРЕ
    with st.sidebar:
        st.markdown("### 🎯 Фильтры")
        min_date = df_total['Дата прослушивания'].min().date()
        max_date = df_total['Дата прослушивания'].max().date()
        
        date_range = st.date_input(
            "📅 Период",
            value=(min_date, max_date),
            min_value=min_date,
            max_value=max_date
        )
        
        formats = ['Все'] + list(df_ref['Формат'].unique())
        selected_format = st.selectbox("📂 Формат", formats)
        
        genres = ['Все'] + list(df_ref['Жанр'].unique())
        selected_genre = st.selectbox("🎭 Жанр", genres)
        
        st.markdown("---")
        st.caption(f"📊 Записей: {len(df_total):,}")
        st.caption(f"📅 С {min_date} по {max_date}")
    
    # ПРИМЕНЕНИЕ ФИЛЬТРОВ
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
    
    # ========== МЕТРИКИ ==========
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
    
    # ========== ИНФОРМАЦИОННЫЙ БЛОК ==========
    st.markdown("""
    <div class="info-block">
        <div class="info-title">📖 Что означают метрики</div>
        <div style="display: grid; grid-template-columns: 1fr 1fr 1fr; gap: 1rem;">
            <div>
                <div style="color: #4facfe; font-weight: 700; font-size: 1rem;">🎬 Старты</div>
                <div style="color: rgba(255,255,255,0.6); font-size: 0.85rem;">Количество запусков выпуска — базовый показатель популярности</div>
            </div>
            <div>
                <div style="color: #f5576c; font-weight: 700; font-size: 1rem;">🎧 Стримы</div>
                <div style="color: rgba(255,255,255,0.6); font-size: 0.85rem;">Прослушивания длительностью более 2 минут — показатель вовлеченности</div>
            </div>
            <div>
                <div style="color: #43e97b; font-weight: 700; font-size: 1rem;">📈 Конверсия</div>
                <div style="color: rgba(255,255,255,0.6); font-size: 0.85rem;">Доля стартов, перешедших в стримы. <strong style="color: #43e97b;">Формула:</strong> Стримы / Старты × 100%</div>
            </div>
            <div style="grid-column: span 3; margin-top: 0.5rem; padding-top: 0.8rem; border-top: 1px solid rgba(255,255,255,0.05);">
                <div style="color: #f093fb; font-weight: 700; font-size: 1rem;">⭐ RSI (Reach Success Index) — Индекс успешности выпуска</div>
                <div style="color: rgba(255,255,255,0.6); font-size: 0.85rem;">
                    Комплексный показатель, учитывающий:<br>
                    <strong style="color: #f5576c;">Стримы (E)</strong> — вовлеченность слушателей × 
                    <strong style="color: #43e97b;">Конверсия (F+1)</strong> — качество контента × 
                    <strong style="color: #4facfe;">Старты<sup>0.1</sup> (D)</strong> — охват аудитории<br>
                    <span style="color: rgba(255,255,255,0.4); font-size: 0.8rem;">📌 Формула: RSI = E × (F + 1) × D<sup>0.1</sup>, где E — стримы, F — конверсия (0-1), D — старты</span>
                </div>
            </div>
        </div>
    </div>
    """, unsafe_allow_html=True)
    
    # ========== ДИНАМИКА ==========
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
        hovertemplate='<b>%{x}</b><br>Старты: %{y}<extra></extra>'
    ))
    
    fig1.add_trace(go.Scatter(
        x=daily_stats['Дата прослушивания'],
        y=daily_stats['Стримы'],
        name='Стримы',
        line=dict(color='#f5576c', width=3),
        fill='tozeroy',
        fillcolor='rgba(245, 87, 108, 0.15)',
        hovertemplate='<b>%{x}</b><br>Стримы: %{y}<extra></extra>'
    ))
    
    fig1.add_trace(go.Scatter(
        x=daily_stats['Дата прослушивания'],
        y=daily_stats['Конверсия'],
        name='Конверсия (%)',
        line=dict(color='#43e97b', width=2, dash='dash'),
        hovertemplate='<b>%{x}</b><br>Конверсия: %{y:.1f}%<extra></extra>'
    ), secondary_y=True)
    
    fig1.update_layout(
        template='plotly_dark',
        plot_bgcolor='rgba(0,0,0,0)',
        paper_bgcolor='rgba(0,0,0,0)',
        height=450,
        hovermode='x unified',
        legend=dict(orientation='h', yanchor='bottom', y=1.02, xanchor='right', x=1, font=dict(color='white', size=12)),
        xaxis=dict(title='Дата', titlefont=dict(color='white', size=13), tickfont=dict(color='white', size=11), gridcolor='rgba(255,255,255,0.05)'),
        yaxis=dict(title='Количество', titlefont=dict(color='white', size=13), tickfont=dict(color='white', size=11), gridcolor='rgba(255,255,255,0.05)'),
        yaxis2=dict(title='Конверсия (%)', titlefont=dict(color='#43e97b', size=13), tickfont=dict(color='#43e97b', size=11), overlaying='y', side='right', showgrid=False)
    )
    st.plotly_chart(fig1, use_container_width=True)
    
    # ========== ТОП ВЫПУСКОВ ПО RSI ==========
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
            name='RSI',
            marker=dict(
                color=top_rsi['RSI'],
                colorscale='Viridis',
                showscale=True,
                colorbar=dict(title='RSI', titlefont=dict(color='white'), tickfont=dict(color='white'))
            ),
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
            height=450,
            xaxis=dict(tickangle=-15, tickfont=dict(color='white', size=10), gridcolor='rgba(255,255,255,0.05)'),
            yaxis=dict(title='RSI', titlefont=dict(color='white', size=13), tickfont=dict(color='white', size=11), gridcolor='rgba(255,255,255,0.05)')
        )
        st.plotly_chart(fig2, use_container_width=True)
    
    with col2:
        st.markdown("""
        <div style="background: rgba(255,255,255,0.03); border-radius: 15px; padding: 1.2rem; border: 1px solid rgba(255,255,255,0.05);">
            <h4 style="color: white; margin-bottom: 0.8rem;">⭐ Топ RSI</h4>
        """, unsafe_allow_html=True)
        
        if len(top_rsi) > 0:
            for i, (idx, row) in enumerate(top_rsi.head(5).iterrows()):
                medal = ['🥇', '🥈', '🥉', '4️⃣', '5️⃣'][i]
                name = row['Короткое название'][:25] + '...' if len(row['Короткое название']) > 25 else row['Короткое название']
                st.markdown(f"""
                <div style="color: rgba(255,255,255,0.8); margin-bottom: 0.4rem; font-size: 0.9rem;">
                    {medal} <span style="color: #4facfe; font-weight: 600;">{name}</span> — RSI: {row['RSI']:.1f}
                </div>
                """, unsafe_allow_html=True)
        
        st.markdown("</div>", unsafe_allow_html=True)
    
    st.markdown("---")
    
    # ========== ДЕТАЛЬНАЯ АНАЛИТИКА ==========
    st.markdown('<div class="section-title">🎭 Детальная аналитика</div>', unsafe_allow_html=True)
    
    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.markdown('<div class="chart-subtitle-starts">📊 По форматам</div>', unsafe_allow_html=True)
        format_stats = filtered_data.groupby('Формат').agg({'Старты': 'sum'}).reset_index()
        colors = ['#4facfe', '#f5576c', '#f093fb', '#43e97b', '#fa709a']
        
        fig3 = go.Figure(data=[go.Pie(
            labels=format_stats['Формат'],
            values=format_stats['Старты'],
            hole=0.4,
            marker=dict(colors=colors[:len(format_stats)], line=dict(color='white', width=2)),
            textfont=dict(color='white', size=12),
            hoverinfo='label+percent',
            textinfo='label+percent'
        )])
        fig3.update_layout(
            template='plotly_dark',
            plot_bgcolor='rgba(0,0,0,0)',
            paper_bgcolor='rgba(0,0,0,0)',
            height=300,
            legend=dict(font=dict(color='white'), orientation='h', yanchor='bottom', y=-0.1)
        )
        st.plotly_chart(fig3, use_container_width=True)
    
    with col2:
        st.markdown('<div class="chart-subtitle-streams">🎧 По стримам</div>', unsafe_allow_html=True)
        format_stats_streams = filtered_data.groupby('Формат').agg({'Стримы': 'sum'}).reset_index()
        colors = ['#4facfe', '#f5576c', '#f093fb', '#43e97b', '#fa709a']
        
        fig4 = go.Figure(data=[go.Pie(
            labels=format_stats_streams['Формат'],
            values=format_stats_streams['Стримы'],
            hole=0.4,
            marker=dict(colors=colors[:len(format_stats_streams)], line=dict(color='white', width=2)),
            textfont=dict(color='white', size=12),
            hoverinfo='label+percent',
            textinfo='label+percent'
        )])
        fig4.update_layout(
            template='plotly_dark',
            plot_bgcolor='rgba(0,0,0,0)',
            paper_bgcolor='rgba(0,0,0,0)',
            height=300,
            legend=dict(font=dict(color='white'), orientation='h', yanchor='bottom', y=-0.1)
        )
        st.plotly_chart(fig4, use_container_width=True)
    
    with col3:
        st.markdown('<div class="chart-subtitle-conversion">📈 По конверсии</div>', unsafe_allow_html=True)
        format_stats_conv = filtered_data.groupby('Формат').agg({
            'Старты': 'sum',
            'Стримы': 'sum'
        }).reset_index()
        format_stats_conv['Конверсия'] = (format_stats_conv['Стримы'] / format_stats_conv['Старты'] * 100).fillna(0)
        colors = ['#4facfe', '#f5576c', '#f093fb', '#43e97b', '#fa709a']
        
        fig5 = go.Figure(data=[go.Pie(
            labels=format_stats_conv['Формат'],
            values=format_stats_conv['Конверсия'],
            hole=0.4,
            marker=dict(colors=colors[:len(format_stats_conv)], line=dict(color='white', width=2)),
            textfont=dict(color='white', size=12),
            hoverinfo='label+percent',
            textinfo='label+percent'
        )])
        fig5.update_layout(
            template='plotly_dark',
            plot_bgcolor='rgba(0,0,0,0)',
            paper_bgcolor='rgba(0,0,0,0)',
            height=300,
            legend=dict(font=dict(color='white'), orientation='h', yanchor='bottom', y=-0.1)
        )
        st.plotly_chart(fig5, use_container_width=True)
    
    st.markdown("---")
    
    # ========== АКТИВНОСТЬ ПО ДНЯМ НЕДЕЛИ ==========
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
            textfont=dict(color='white', size=11),
            hovertemplate='<b>%{x}</b><br>Старты: %{y:,}<extra></extra>'
        )])
        fig6.update_layout(
            template='plotly_dark',
            plot_bgcolor='rgba(0,0,0,0)',
            paper_bgcolor='rgba(0,0,0,0)',
            height=300,
            xaxis=dict(title='День недели', titlefont=dict(color='white', size=12), tickfont=dict(color='white', size=11), showgrid=False),
            yaxis=dict(title='Старты', titlefont=dict(color='#4facfe', size=12), tickfont=dict(color='white', size=11), gridcolor='rgba(255,255,255,0.05)'),
            showlegend=False
        )
        st.plotly_chart(fig6, use_container_width=True)
    
    with col2:
        st.markdown('<div class="chart-subtitle-streams">🎧 По стримам</div>', unsafe_allow_html=True)
        fig7 = go.Figure(data=[go.Bar(
            x=weekday_stats['День'],
            y=weekday_stats['Стримы'],
            marker=dict(color=['#4facfe', '#43e97b', '#f093fb', '#f5576c', '#fa709a', '#f6d365', '#a8edea'], line=dict(color='white', width=1)),
            text=weekday_stats['Стримы'],
            textposition='outside',
            textfont=dict(color='white', size=11),
            hovertemplate='<b>%{x}</b><br>Стримы: %{y:,}<extra></extra>'
        )])
        fig7.update_layout(
            template='plotly_dark',
            plot_bgcolor='rgba(0,0,0,0)',
            paper_bgcolor='rgba(0,0,0,0)',
            height=300,
            xaxis=dict(title='День недели', titlefont=dict(color='white', size=12), tickfont=dict(color='white', size=11), showgrid=False),
            yaxis=dict(title='Стримы', titlefont=dict(color='#f5576c', size=12), tickfont=dict(color='white', size=11), gridcolor='rgba(255,255,255,0.05)'),
            showlegend=False
        )
        st.plotly_chart(fig7, use_container_width=True)
    
    st.markdown("---")
    
    # ========== НАКОПЛЕННЫЙ РОСТ ==========
    st.markdown('<div class="section-title">📈 Накопленный рост</div>', unsafe_allow_html=True)
    
    cum_stats = filtered_data.groupby('Дата прослушивания').agg({
        'Старты': 'sum',
        'Стримы': 'sum'
    }).sort_index()
    cum_stats['Старты_нак'] = cum_stats['Старты'].cumsum()
    cum_stats['Стримы_нак'] = cum_stats['Стримы'].cumsum()
    
    fig8 = go.Figure()
    fig8.add_trace(go.Scatter(
        x=cum_stats.index,
        y=cum_stats['Старты_нак'],
        name='Старты (накоп.)',
        line=dict(color='#4facfe', width=3),
        fill='tozeroy',
        fillcolor='rgba(79, 172, 254, 0.15)'
    ))
    fig8.add_trace(go.Scatter(
        x=cum_stats.index,
        y=cum_stats['Стримы_нак'],
        name='Стримы (накоп.)',
        line=dict(color='#f5576c', width=3),
        fill='tozeroy',
        fillcolor='rgba(245, 87, 108, 0.15)'
    ))
    fig8.update_layout(
        template='plotly_dark',
        plot_bgcolor='rgba(0,0,0,0)',
        paper_bgcolor='rgba(0,0,0,0)',
        height=350,
        hovermode='x unified',
        legend=dict(orientation='h', yanchor='bottom', y=1.02, xanchor='right', x=1, font=dict(color='white')),
        xaxis=dict(title='Дата', titlefont=dict(color='white', size=13), tickfont=dict(color='white', size=11), gridcolor='rgba(255,255,255,0.05)'),
        yaxis=dict(title='Накопленное количество', titlefont=dict(color='white', size=13), tickfont=dict(color='white', size=11), gridcolor='rgba(255,255,255,0.05)')
    )
    st.plotly_chart(fig8, use_container_width=True)
    
    st.markdown("---")
    st.markdown("""
    <div class="footer">
        🎙️ Подкаст Аналитика Pro • Данные обновляются автоматически
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
    
    episodes = sorted(df_merged['Выпуск'].unique())
    episode_names = {get_short_name(ep): ep for ep in episodes}
    short_names = list(episode_names.keys())
    
    selected_short = st.selectbox("🎯 Выберите выпуск:", short_names)
    selected_episode = episode_names[selected_short]
    
    all_data = df_merged[df_merged['Выпуск'] == selected_episode].copy()
    
    if all_data.empty:
        st.warning(f"⚠️ Нет данных для выпуска '{selected_short}'")
    else:
        if period != "Всё время":
            episode_data = filter_by_period(all_data, period)
        else:
            episode_data = all_data
        
        if episode_data.empty:
            st.warning(f"⚠️ Нет данных для выпуска '{selected_short}' в выбранном периоде")
        else:
            col1, col2, col3, col4 = st.columns(4)
            col1.metric("🎬 Старты", f"{episode_data['Старты'].sum():,}")
            col2.metric("🎧 Стримы", f"{episode_data['Стримы'].sum():,}")
            conv = (episode_data['Стримы'].sum() / episode_data['Старты'].sum() * 100) if episode_data['Старты'].sum() > 0 else 0
            col3.metric("📈 Конверсия", f"{conv:.1f}%")
            col4.metric("⭐ RSI", f"{episode_data['RSI'].mean():.1f}")
            
            with st.expander("ℹ️ Информация о выпуске", expanded=True):
                info = df_ref[df_ref['Выпуск'] == selected_episode].iloc[0]
                col1, col2, col3 = st.columns(3)
                with col1:
                    st.write(f"**Формат:** {info['Формат']}")
                    st.write(f"**Жанр:** {info['Жанр']}")
                with col2:
                    st.write(f"**Категория:** {info['Категория']}")
                    st.write(f"**Длительность:** {info['Длительность']}")
                with col3:
                    st.write(f"**Дата релиза:** {info['Дата релиза'].date()}")
                    days_active = (episode_data['Дата прослушивания'].max() - episode_data['Дата прослушивания'].min()).days
                    st.write(f"**Дней в эфире:** {days_active}")
            
            st.markdown("---")
            
            st.subheader("📊 Сравнение со средними показателями")
            
            compare_data = df_merged.copy()
            if period != "Всё время":
                compare_data = filter_by_period(compare_data, period)
            
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
    
    episodes = sorted(df_merged['Выпуск'].unique())
    episode_names = {get_short_name(ep): ep for ep in episodes}
    short_names = list(episode_names.keys())
    
    col1, col2 = st.columns(2)
    with col1:
        ep1_short = st.selectbox("📌 Выпуск №1:", short_names, key="ep1")
        ep1 = episode_names[ep1_short]
    with col2:
        ep2_short = st.selectbox("📌 Выпуск №2:", short_names, key="ep2")
        ep2 = episode_names[ep2_short]
    
    if ep1 == ep2:
        st.warning("⚠️ Выберите два разных выпуска для сравнения!")
    else:
        all_data = df_merged.copy()
        if period != "Всё время":
            filtered = filter_by_period(all_data, period)
        else:
            filtered = all_data
        
        data1 = filtered[filtered['Выпуск'] == ep1]
        data2 = filtered[filtered['Выпуск'] == ep2]
        
        if data1.empty or data2.empty:
            st.warning("⚠️ Нет данных для выбранных выпусков в этом периоде")
        else:
            st.subheader("📊 Сравнительная таблица")
            conv1 = (data1['Стримы'].sum() / data1['Старты'].sum() * 100) if data1['Старты'].sum() > 0 else 0
            conv2 = (data2['Стримы'].sum() / data2['Старты'].sum() * 100) if data2['Старты'].sum() > 0 else 0
            
            comp_df = pd.DataFrame({
                'Метрика': ['Старты', 'Стримы', 'Конверсия (%)', 'RSI'],
                ep1_short: [
                    data1['Старты'].sum(),
                    data1['Стримы'].sum(),
                    f"{conv1:.1f}%",
                    f"{data1['RSI'].mean():.1f}"
                ],
                ep2_short: [
                    data2['Старты'].sum(),
                    data2['Стримы'].sum(),
                    f"{conv2:.1f}%",
                    f"{data2['RSI'].mean():.1f}"
                ]
            })
            st.dataframe(comp_df, use_container_width=True)
            
            st.subheader("📈 Сравнение динамики")
            daily1 = data1.groupby('Дата прослушивания').agg({'Старты': 'sum', 'Стримы': 'sum'}).reset_index()
            daily2 = data2.groupby('Дата прослушивания').agg({'Старты': 'sum', 'Стримы': 'sum'}).reset_index()
            
            fig = make_subplots(specs=[[{"secondary_y": True}]])
            fig.add_trace(go.Scatter(
                x=daily1['Дата прослушивания'],
                y=daily1['Старты'],
                name=f'{ep1_short} (Старты)',
                line=dict(color='#4facfe', width=2)
            ))
            fig.add_trace(go.Scatter(
                x=daily2['Дата прослушивания'],
                y=daily2['Старты'],
                name=f'{ep2_short} (Старты)',
                line=dict(color='#f5576c', width=2, dash='dash')
            ))
            fig.add_trace(go.Scatter(
                x=daily1['Дата прослушивания'],
                y=daily1['Стримы'],
                name=f'{ep1_short} (Стримы)',
                line=dict(color='#43e97b', width=2)
            ), secondary_y=True)
            fig.add_trace(go.Scatter(
                x=daily2['Дата прослушивания'],
                y=daily2['Стримы'],
                name=f'{ep2_short} (Стримы)',
                line=dict(color='#f093fb', width=2, dash='dash')
            ), secondary_y=True)
            fig.update_layout(
                template='plotly_dark',
                plot_bgcolor='rgba(0,0,0,0)',
                paper_bgcolor='rgba(0,0,0,0)',
                height=450,
                hovermode='x unified',
                legend=dict(orientation='h', yanchor='bottom', y=1.02, xanchor='right', x=1, font=dict(color='white'))
            )
            st.plotly_chart(fig, use_container_width=True)
            
            st.subheader("🏆 Итоговый вердикт")
            rsi1 = data1['RSI'].mean()
            rsi2 = data2['RSI'].mean()
            
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