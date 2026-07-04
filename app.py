import streamlit as st

# НАСТРОЙКА СТРАНИЦЫ
st.set_page_config(
    page_title="🎙️ Подкаст Аналитика",
    page_icon="🎙️",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Стили для темной темы
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

# ЗАГОЛОВОК
st.markdown('<div class="main-title">🎙️ Подкаст Аналитика</div>', unsafe_allow_html=True)
st.markdown('<div class="sub-title">ПРЕМИУМ ДАШБОРД • АНАЛИТИКА ПРОСЛУШИВАНИЙ • ТРЕНДЫ</div>', unsafe_allow_html=True)

# ИМПОРТ СТРАНИЦ
from pages import page_overview, page_episode, page_compare

# НАВИГАЦИЯ
page = st.sidebar.radio(
    "📊 Меню",
    ["📊 Общая аналитика", "📋 Анализ выпуска", "🔄 Сравнение выпусков"],
    index=0
)

# ОТОБРАЖЕНИЕ СТРАНИЦ
if page == "📊 Общая аналитика":
    page_overview.show()
elif page == "📋 Анализ выпуска":
    page_episode.show()
else:
    page_compare.show()