import streamlit as st
import pandas as pd
import numpy as np

@st.cache_data
def load_data():
    """Загрузка и подготовка данных"""
    try:
        df_total = pd.read_excel("Общая.xlsx", sheet_name="Общая")
        df_ref = pd.read_excel("Спр.xlsx", sheet_name="Спр")
    except Exception as e:
        st.error(f"❌ Ошибка загрузки данных: {e}")
        st.stop()
    
    df_total['Дата прослушивания'] = pd.to_datetime(df_total['Дата прослушивания'])
    df_ref['Дата релиза'] = pd.to_datetime(df_ref['Дата релиза'])
    
    # Загрузка коротких названий
    try:
        df_short = pd.read_excel("Короткие названия.xlsx")
        short_names_dict = dict(zip(df_short['Оригинальное название'], df_short['Короткое название']))
        df_ref['Короткое название'] = df_ref['Выпуск'].map(short_names_dict).fillna(df_ref['Выпуск'])
    except:
        df_ref['Короткое название'] = df_ref['Выпуск']
    
    df_merged = df_total.merge(df_ref, on='Выпуск', how='left')
    
    # Расчет RSI
    df_merged['Конверсия_доля'] = df_merged['Стримы'] / df_merged['Старты']
    df_merged['Конверсия_доля'] = df_merged['Конверсия_доля'].fillna(0).replace([np.inf, -np.inf], 0)
    df_merged['RSI'] = df_merged['Стримы'] * (df_merged['Конверсия_доля'] + 1) * (df_merged['Старты'] ** 0.1)
    
    return df_total, df_ref, df_merged

def get_short_name(long_name):
    """Получение короткого названия"""
    try:
        df_short = pd.read_excel("Короткие названия.xlsx")
        short_names_dict = dict(zip(df_short['Оригинальное название'], df_short['Короткое название']))
        return short_names_dict.get(long_name, long_name)
    except:
        return long_name

def get_episode_position(episode_data, all_data, metric):
    """Определяет позицию выпуска относительно среднего и медианы"""
    
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
    percentile = (all_values < episode_value).sum() / len(all_values) * 100
    
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
        'percentile': percentile,
        'status': status,
        'color': color,
        'diff_percent': ((episode_value - mean_value) / mean_value * 100)
    }

def filter_by_period(df, period):
    """Фильтрует данные по периоду"""
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