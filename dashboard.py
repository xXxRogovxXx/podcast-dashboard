import streamlit as st
import pandas as pd
import numpy as np
import plotly.graph_objects as go
from plotly.subplots import make_subplots

# ============================================
# НАСТРОЙКА СТРАНИЦЫ
# ============================================
st.set_page_config(
    page_title="🎙️ Подкаст Аналитика",
    page_icon="🎙️",
    layout="wide",
    initial_sidebar_state="expanded"
)

st.markdown("""
<style>
    .stApp {
        background: linear-gradient(135deg, #0f0c29 0%, #302b63 50%, #24243e 100%);
    }
    .main-title {
        font-size: 2.8rem;
        font-weight: 800;
        background: linear-gradient(135deg, #f093fb 0%, #f5576c 50%, #4facfe 100%);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        background-clip: text;
        text-align: center;
        padding: 0.5rem 0;
    }
    .sub-title {
        text-align: center;
        color: rgba(255,255,255,0.5);
        font-size: 0.9rem;
        margin-bottom: 1.5rem;
        letter-spacing: 2px;
    }
    .css-1d391kg {
        background: rgba(10, 8, 30, 0.95) !important;
    }
    .stSelectbox label, .stDateInput label, .stMarkdown, .stCaption {
        color: rgba(255,255,255,0.8) !important;
    }
</style>
""", unsafe_allow_html=True)

st.markdown('<div class="main-title">🎙️ Подкаст Аналитика</div>', unsafe_allow_html=True)
st.markdown('<div class="sub-title">ПРЕМИУМ ДАШБОРД • АНАЛИТИКА ПРОСЛУШИВАНИЙ • ТРЕНДЫ</div>', unsafe_allow_html=True)

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
    if period == "1 день":
        return df[df['Дата прослушивания'] >= df['Дата прослушивания'].max() - pd.Timedelta(days=1)]
    elif period == "1 неделя":
        return df[df['Дата прослушивания'] >= df['Дата прослушивания'].max() - pd.Timedelta(days=7)]
    elif period == "1 месяц":
        return df[df['Дата прослушивания'] >= df['Дата прослушивания'].max() - pd.Timedelta(days=30)]
    else:
        return df

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
    st.title("📊 Общая аналитика")
    
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
    col1.metric("🎬 Старты", f"{total_starts:,}")
    col2.metric("🎧 Стримы", f"{total_streams:,}")
    col3.metric("📈 Конверсия", f"{conversion:.1f}%")
    col4.metric("📝 Выпусков", unique_episodes)
    col5.metric("⭐ Средний RSI", f"{avg_rsi:.1f}")
    
    st.markdown("---")
    
    st.subheader("📊 Динамика прослушиваний")
    daily_stats = filtered_data.groupby('Дата прослушивания').agg({
        'Старты': 'sum',
        'Стримы': 'sum'
    }).reset_index()
    daily_stats['Конверсия'] = (daily_stats['Стримы'] / daily_stats['Старты'] * 100).fillna(0)
    
    fig = make_subplots(specs=[[{"secondary_y": True}]])
    fig.add_trace(go.Scatter(
        x=daily_stats['Дата прослушивания'],
        y=daily_stats['Старты'],
        name='Старты',
        line=dict(color='#4facfe', width=3),
        fill='tozeroy',
        fillcolor='rgba(79, 172, 254, 0.15)'
    ))
    fig.add_trace(go.Scatter(
        x=daily_stats['Дата прослушивания'],
        y=daily_stats['Стримы'],
        name='Стримы',
        line=dict(color='#f5576c', width=3),
        fill='tozeroy',
        fillcolor='rgba(245, 87, 108, 0.15)'
    ))
    fig.add_trace(go.Scatter(
        x=daily_stats['Дата прослушивания'],
        y=daily_stats['Конверсия'],
        name='Конверсия (%)',
        line=dict(color='#43e97b', width=2, dash='dash')
    ), secondary_y=True)
    fig.update_layout(
        template='plotly_dark',
        plot_bgcolor='rgba(0,0,0,0)',
        paper_bgcolor='rgba(0,0,0,0)',
        height=450,
        hovermode='x unified',
        legend=dict(orientation='h', yanchor='bottom', y=1.02, xanchor='right', x=1)
    )
    st.plotly_chart(fig, use_container_width=True)
    
    st.subheader("🏆 Топ выпусков по RSI")
    top_episodes = filtered_data.groupby(['Выпуск', 'Короткое название']).agg({
        'Старты': 'sum',
        'Стримы': 'sum',
        'RSI': 'mean'
    }).reset_index().sort_values('RSI', ascending=False).head(10)
    
    fig2 = go.Figure()
    fig2.add_trace(go.Bar(
        x=top_episodes['Короткое название'],
        y=top_episodes['RSI'],
        marker=dict(color=top_episodes['RSI'], colorscale='Viridis'),
        text=top_episodes['RSI'].round(1),
        textposition='outside'
    ))
    fig2.update_layout(
        template='plotly_dark',
        plot_bgcolor='rgba(0,0,0,0)',
        paper_bgcolor='rgba(0,0,0,0)',
        height=400,
        xaxis=dict(tickangle=-20)
    )
    st.plotly_chart(fig2, use_container_width=True)

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
    
    all_data = df_merged.copy()
    filtered_by_period = filter_by_period(all_data, period)
    episode_data = filtered_by_period[filtered_by_period['Выпуск'] == selected_episode]
    
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
        
        st.markdown("---")
        
        st.subheader("📊 Сравнение со средними показателями")
        metrics = ['Старты', 'Стримы', 'RSI']
        comparison_data = []
        for metric in metrics:
            pos = get_episode_position(episode_data, filtered_by_period, metric)
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
            hovermode='x unified'
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
        filtered = filter_by_period(all_data, period)
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
                legend=dict(orientation='h', yanchor='bottom', y=1.02, xanchor='right', x=1)
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