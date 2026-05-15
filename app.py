import streamlit as st
from fuzzy_logic import FoodFuzzyLogic
from api_services import APIServices
import time
import streamlit.components.v1 as components
from streamlit_js_eval import get_geolocation
import skfuzzy.control as ctrl

# --- 1. Khởi tạo hệ thống ---
st.set_page_config(page_title="Ăn gì hôm nay?", page_icon="🍜", layout="wide")

@st.cache_resource
def init_system():
    return FoodFuzzyLogic(), APIServices()

engine, api = init_system()
location = get_geolocation()

if not hasattr(engine.sim_ctrl, 'input'):
    engine.sim_ctrl = ctrl.ControlSystemSimulation(engine.sim_ctrl)

# --- 2. Quản lý trạng thái ---
if 'started' not in st.session_state:
    st.session_state.started = False
if 'results' not in st.session_state:
    st.session_state.results = None
if 'search_history' not in st.session_state:
    st.session_state.search_history = []
if 'final_restaurants' not in st.session_state:
    st.session_state.final_restaurants = []

# --- 3. Dialog kết quả ---
@st.dialog("Gợi ý dành cho bạn")
def show_results_dialog(h_val, b_val, t_val, h_goal, w_score):
    with st.spinner("Đang phân tích..."):
        time.sleep(1.2)
        health_map = {"Diet": 2.0, "Normal": 5.0, "Bulking": 8.0}

        engine.sim_ctrl.input['hunger'] = h_val
        engine.sim_ctrl.input['budget'] = b_val / 1000
        engine.sim_ctrl.input['time'] = t_val
        engine.sim_ctrl.input['weather'] = w_score
        engine.sim_ctrl.input['health'] = health_map[h_goal]

        engine.sim_ctrl.compute()
        raw = engine.sim_ctrl.output

        res = {}
        c = raw.get('cuisine', 5.0)
        cuisines = ["Vietnamese", "Korean", "Japanese", "Chinese", "Western", "Thai", "Italian", "Drinks", "Dessert", "Temple Meal"]
        idx = int(min(max(c, 0), 9))
        res['cuisine_label'] = cuisines[idx]

        m = raw.get('meal_type', 5.0)
        res['meal_type_label'] = "Ăn vặt" if m < 2.0 else "Fast food" if m < 5.0 else "Bữa chính" if m < 8.0 else "Bữa ăn lành mạnh"

        p = raw.get('price_range', 100)
        res['price_label'] = "Rẻ" if p < 3.3 else "Tầm trung" if p < 6.6 else "Sang chảnh"

        pl = raw.get('place', 5.0)
        res['place_label'] = "Vỉa hè" if pl < 5 else "Nhà hàng"

        st.session_state.results = res

        candidates = [s for s in api.restaurants if s['cuisine'].lower() == res['cuisine_label'].lower()]
        ranked_restaurants = api.re_rank_by_taste(candidates)
        st.session_state.final_restaurants = ranked_restaurants

        st.success("Tìm xong rồi!")

        st.markdown("""
        <style>
        [data-testid="stMetricLabel"] { font-size: 0.78rem !important; color: #888 !important; text-transform: uppercase; letter-spacing: 0.05em; }
        [data-testid="stMetricValue"] { font-size: 1.6rem !important; font-weight: 700 !important; color: #7a0000 !important; }
        </style>
        """, unsafe_allow_html=True)

        col1, col2 = st.columns(2)
        with col1:
            st.metric("🍽️ Ẩm thực", res['cuisine_label'])
            st.markdown(f"<p style='font-size:1rem; margin-top:4px;'>Loại bữa: <strong style='font-size:1.05rem; color:#7a0000;'>{res['meal_type_label']}</strong></p>", unsafe_allow_html=True)
        with col2:
            st.metric("💰 Tầm giá", res['price_label'])
            st.markdown(f"<p style='font-size:1rem; margin-top:4px;'>Không gian: <strong style='font-size:1.05rem; color:#7a0000;'>{res['place_label']}</strong></p>", unsafe_allow_html=True)

        st.write("---")

        if ranked_restaurants:
            top_choice = ranked_restaurants[0]
            st.markdown(f"""
            <div style='background:#fff8ec; border-left:4px solid #f5d97e; border-radius:8px; padding:14px 18px;'>
                <p style='margin:0; font-size:0.82rem; color:#888; text-transform:uppercase; letter-spacing:0.05em;'>Quán phù hợp nhất với bạn</p>
                <p style='margin:4px 0 0; font-size:1.35rem; font-weight:700; color:#7a0000;'>{top_choice['name']}</p>
            </div>
            """, unsafe_allow_html=True)

        if st.button("Xem trên bản đồ", use_container_width=True):
            st.rerun()


# --- 4. Giao diện & Logic ---

if not st.session_state.started:
    #Màn hình chào
    st.markdown("""
        <style>
        @import url('https://fonts.googleapis.com/css2?family=Playfair+Display:wght@700&family=Be+Vietnam+Pro:wght@400;500&display=swap');

        .stApp { background-color: #7a0000 !important; }
        [data-testid="stSidebar"] { display: none; }

        .hero-title {
            font-family: 'Playfair Display', serif;
            font-size: 3.8rem;
            color: #f5d97e;
            text-align: center;
            letter-spacing: -0.5px;
            margin-bottom: 0.2rem;
        }
        .hero-sub {
            font-family: 'Be Vietnam Pro', sans-serif;
            font-size: 1.1rem;
            color: #f0dfc0;
            text-align: center;
            opacity: 0.85;
            margin-bottom: 2.5rem;
        }
        .stButton > button {
            background-color: #f5d97e;
            color: #7a0000;
            border: none;
            border-radius: 10px;
            font-family: 'Be Vietnam Pro', sans-serif;
            font-weight: 600;
            font-size: 1rem;
            padding: 0.7rem 2rem;
            letter-spacing: 0.3px;
        }
        .stButton > button:hover {
            background-color: #ffffff;
            color: #7a0000;
        }
        </style>
    """, unsafe_allow_html=True)

    st.markdown("<div class='hero-title'>Hôm nay ăn gì?</div>", unsafe_allow_html=True)
    st.markdown("<div class='hero-sub'>Hãy để chúng tôi gợi ý món ăn phù hợp với bạn ngay lúc này.</div>", unsafe_allow_html=True)

    img_urls = [
        "https://images.unsplash.com/photo-1504674900247-0877df9cc836?w=400",
        "https://images.unsplash.com/photo-1540189549336-e6e99c3679fe?w=400",
        "https://images.unsplash.com/photo-1565299624946-b28f40a0ae38?w=400",
        "https://images.unsplash.com/photo-1512621776951-a57141f2eefd?w=400",
        "https://images.unsplash.com/photo-1493770348161-369560ae357d?w=400",
        "https://images.unsplash.com/photo-1555939594-58d7cb561ad1?w=400",
        "https://images.unsplash.com/photo-1467003909585-2f8a72700288?w=400",
    ]

    cols = st.columns(3)
    for i, url in enumerate(img_urls):
        with cols[i % 3]:
            st.image(url, use_container_width=True)

    st.markdown("<br>", unsafe_allow_html=True)
    _, mid_col, _ = st.columns([1.2, 1, 1.2])
    with mid_col:
        if st.button("Bắt đầu", use_container_width=True):
            st.session_state.started = True
            st.rerun()

else:
    #Màn hình chính
    st.markdown("""
        <style>
        @import url('https://fonts.googleapis.com/css2?family=Playfair+Display:wght@700&family=Be+Vietnam+Pro:wght@400;500;600&display=swap');

        .stApp {
            background-color: #faf8f5 !important;
            font-family: 'Be Vietnam Pro', sans-serif;
        }
       /* Ẩn nút collapse sidebar bị lỗi hiển thị icon text */
        [data-testid="collapsedControl"] { display: none !important; }
        button[kind="header"] { display: none !important; }
        [data-testid="stSidebarCollapseButton"] { display: none !important; }
        [data-testid="stSidebar"] {
            background-color: #7a0000 !important;
        }
        [data-testid="stSidebar"] * {
            color: #f0dfc0 !important;
            font-family: 'Be Vietnam Pro', sans-serif;
        }
        .weather-card {
            background-color: #fff;
            border-radius: 12px;
            padding: 18px 20px;
            margin-bottom: 18px;
            border-left: 4px solid #f5d97e;
            box-shadow: 0 2px 10px rgba(0,0,0,0.15);
        }
        .weather-card h3 {
            font-family: 'Playfair Display', serif;
            color: #7a0000 !important;
            font-size: 1.1rem;
            margin-bottom: 10px;
        }
        .weather-card p, .weather-card span, .weather-card b {
            color: #3a1a1a !important;
            font-size: 0.92rem;
        }
        .history-card {
            background: rgba(255,255,255,0.12);
            padding: 10px 12px;
            border-radius: 8px;
            margin-bottom: 8px;
            border: 1px solid rgba(255,255,255,0.2);
            font-size: 0.88rem;
        }
        .stButton > button {
            background-color: #7a0000;
            color: #f5d97e;
            border-radius: 10px;
            font-family: 'Be Vietnam Pro', sans-serif;
            font-weight: 600;
            font-size: 0.95rem;
            letter-spacing: 0.2px;
        }
        .stButton > button:hover {
            background-color: #5c0000;
        }
        h2 {
            font-family: 'Playfair Display', serif !important;
        }
        /* Slider labels */
        [data-testid="stSlider"] label p {
            font-size: 0.95rem !important;
            font-weight: 600 !important;
            color: #3a1a1a !important;
        }
        /* Selectbox label */
        [data-testid="stSelectbox"] label p {
            font-size: 0.95rem !important;
            font-weight: 600 !important;
            color: #3a1a1a !important;
        }
        /* Slider current value */
        [data-testid="stSlider"] [data-testid="stMarkdownContainer"] p {
            font-size: 1.05rem !important;
            font-weight: 700 !important;
            color: #7a0000 !important;
        }
        </style>
    """, unsafe_allow_html=True)

    weather_data = api.get_weather_score("Ho Chi Minh")
    w_score = weather_data['score']

    with st.sidebar:
        st.markdown(f"""
        <div class="weather-card">
            <h3>Thời tiết hiện tại</h3>
            <p>Nhiệt độ: <b>{weather_data['temp']}°C</b></p>
            <p>Tình trạng: <b>{weather_data['desc']}</b></p>
        </div>
        """, unsafe_allow_html=True)

        st.markdown("---")
        st.markdown("<h3 style='font-size:1rem;'>Lịch sử tìm kiếm của bạn</h3>", unsafe_allow_html=True)

        if st.session_state.search_history:
            for item in reversed(st.session_state.search_history):
                st.markdown(f"""
                <div class="history-card">
                    <b>{item['cuisine']}</b> · {item['budget']}<br>
                    <small style="opacity:0.7;">{item['time']}</small>
                </div>
                """, unsafe_allow_html=True)
        else:
            st.write("Chưa có lịch sử.")

        st.markdown("<br>", unsafe_allow_html=True)
        if st.button("← Quay lại trang chủ", use_container_width=True):
            st.session_state.started = False
            st.session_state.results = None
            st.rerun()

    #Input
    st.markdown("<h2 style='color:#7a0000; margin-bottom:1.5rem;'>Cho chúng tôi biết thêm về yêu cầu của bạn nhé</h2>", unsafe_allow_html=True)

    with st.container():
        col_a, col_b = st.columns(2)
        with col_a:
            hunger_ran = st.slider("Bạn đang đói ở mức nào?", 0.0, 10.0, 5.0)
            health_goal = st.selectbox("Mục tiêu sức khỏe:", ["Normal", "Diet", "Bulking"])
        with col_b:
            budget_ran = st.slider("Ngân sách (nghìn đồng):", 0, 500, 100)
            time_ran = st.slider("Thời gian rảnh (phút):", 0, 120, 30)

    st.markdown("<br>", unsafe_allow_html=True)

    if st.button("Gợi ý cho tôi", use_container_width=True):
        show_results_dialog(hunger_ran, budget_ran, time_ran, health_goal, w_score)

    #Map
    if st.session_state.results:
        res = st.session_state.results
        st.divider()
        st.markdown("<h2 style='color:#7a0000;'>Quán gần bạn</h2>", unsafe_allow_html=True)

        with st.expander("Xem lại gợi ý", expanded=True):
            st.markdown("""
            <style>
            [data-testid="stMetricLabel"] { font-size: 0.75rem !important; color: #999 !important; text-transform: uppercase; letter-spacing: 0.05em; }
            [data-testid="stMetricValue"] { font-size: 1.45rem !important; font-weight: 700 !important; color: #7a0000 !important; }
            </style>
            """, unsafe_allow_html=True)
            c1, c2, c3, c4 = st.columns(4)
            c1.metric("🍽️ Ẩm thực", res['cuisine_label'])
            c2.metric("🍜 Loại món", res['meal_type_label'])
            c3.metric("💰 Tầm giá", res['price_label'])
            c4.metric("📍 Không gian", res['place_label'])

        if location and 'coords' in location:
            curr_lat = location['coords']['latitude']
            curr_lng = location['coords']['longitude']
            filtered_shops = [s for s in api.restaurants if s['cuisine'].lower() == res['cuisine_label'].lower()]

            if filtered_shops:
                st.success(f"Đã tìm thấy {len(filtered_shops)} quán {res['cuisine_label']} gần đây.")
                selected_name = st.selectbox("Chọn quán mà bạn muốn đến:", [s['name'] for s in filtered_shops])
                target_shop = next(s for s in filtered_shops if s['name'] == selected_name)

                embed_url = api.get_google_maps_embed_url(curr_lat, curr_lng, target_shop['latitude'], target_shop['longitude'])
                components.html(
                    f'<iframe width="100%" height="450" src="{embed_url}" frameborder="0" style="border-radius:12px; box-shadow: 0 4px 14px rgba(0,0,0,0.1);"></iframe>',
                    height=460
                )

                delivery_time = api.get_delivery_estimation(curr_lat, curr_lng, target_shop['latitude'], target_shop['longitude'])
                st.info(f"Thời gian di chuyển ước tính: **{delivery_time} phút**")

                if st.button(f"Xác nhận dùng bữa tại {target_shop['name']}", use_container_width=True):
                    api.learn_user_taste(target_shop['name'])
                    current_search = {
                        "cuisine": res['cuisine_label'],
                        "budget": res['price_label'],
                        "time": time.strftime("%H:%M"),
                    }
                    st.session_state.search_history.append(current_search)
                    if len(st.session_state.search_history) > 5:
                        st.session_state.search_history.pop(0)
                    st.session_state.confirm_msg = f"Đã lưu lại rồi! Chúc bạn ngon miệng tại {target_shop['name']} nha."
                    st.rerun()

                if 'confirm_msg' in st.session_state:
                    st.success(st.session_state.confirm_msg)
            else:
                st.warning("Không tìm thấy quán nào phù hợp trong danh sách. Thử lại với tiêu chí khác nhé!")
        else:
            st.info("Hãy cho phép trình duyệt truy cập vị trí để xem quán nào gần bạn nha.")