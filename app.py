import streamlit as st
from fuzzy_logic import FoodFuzzyLogic
from api_services import APIServices
import time
import streamlit.components.v1 as components
from streamlit_js_eval import get_geolocation
import skfuzzy.control as ctrl

# --- 1. KHỞI TẠO HỆ THỐNG ---
st.set_page_config(page_title="Hôm nay ăn gì?", page_icon="🍴", layout="wide")

@st.cache_resource
def init_system():
    return FoodFuzzyLogic(), APIServices()


engine, api = init_system()
location = get_geolocation()

if not hasattr(engine.sim_ctrl, 'input'):
    engine.sim_ctrl = ctrl.ControlSystemSimulation(engine.sim_ctrl)
# --- 2. QUẢN LÝ TRẠNG THÁI ---
if 'started' not in st.session_state:
    st.session_state.started = False
if 'results' not in st.session_state:
    st.session_state.results = None
if 'search_history' not in st.session_state:
    st.session_state.search_history = []
if 'final_restaurants' not in st.session_state:
    st.session_state.final_restaurants = []

# --- 3. DIALOG KẾT QUẢ ---
# --- 3. DIALOG KẾT QUẢ ---
@st.dialog("Đây là gợi ý cho bạn ")    
def show_results_dialog(h_val, b_val, t_val, h_goal, w_score):   
    with st.spinner('Đang tính toán để tìm món ngon...'):
        time.sleep(1.5)
        health_map = {"Diet": 2.0, "Normal": 5.0, "Bulking": 8.0}
        
        # 1. Truyền input vào hệ thống mờ
        engine.sim_ctrl.input['hunger'] = h_val
        engine.sim_ctrl.input['budget'] = b_val / 1000
        engine.sim_ctrl.input['time'] = t_val
        engine.sim_ctrl.input['weather'] = w_score
        engine.sim_ctrl.input['health'] = health_map[h_goal]
        
        engine.sim_ctrl.compute()
        raw = engine.sim_ctrl.output

        # 2. Giải mã kết quả
        res = {}
        c = raw.get('cuisine', 5.0)
        cuisines = ["Vietnamese", "Korean", "Japanese", "Chinese", "Western", "Thai", "Italian", "Drinks", "Dessert", "Temple Meal"]
        res['cuisine_label'] = cuisines[int(min(max(c, 0), 9))]
        
        m = raw.get('meal_type', 5.0)
        res['meal_type_label'] = "Ăn vặt" if m < 2.0 else "Fast food" if m < 5.0 else "Bữa chính" if m < 8.0 else "Bữa ăn lành mạnh"
        
        p = raw.get('price_range', 100)
        res['price_label'] = "Rẻ" if p < 3.3 else "Tầm trung" if p < 6.6 else "Sang chảnh"
        
        pl = raw.get('place', 5.0)
        res['place_label'] = "Vỉa hè" if pl < 5 else "Nhà hàng"
        
        st.session_state.results = res

        # 3. XỬ LÝ GU CỦA BẠN (Tính năng mới thêm)
        # Lấy danh sách quán theo ẩm thực và sắp xếp lại theo lịch sử sở thích
        candidates = [s for s in api.restaurants if s['cuisine'].lower() == res['cuisine_label'].lower()]
        ranked_restaurants = api.re_rank_by_taste(candidates)
        st.session_state.final_restaurants = ranked_restaurants


        # 5. Hiển thị kết quả ra Dialog
        st.success("➡ Đã tìm thấy món phù hợp!")
        col1, col2 = st.columns(2)
        with col1:
            st.metric("🛒 Kiểu ẩm thực", res['cuisine_label'])
            st.write(f"🍜 **Loại món:** {res['meal_type_label']}")
        with col2:
            st.metric("💰 Tầm giá", res['price_label'])
            st.write(f"📍 **Địa điểm:** {res['place_label']}")
        
        st.write("---")
       
        if ranked_restaurants:
            top_choice = ranked_restaurants[0]
            st.info(f" Gợi ý chuẩn gu cho bạn: **{top_choice['name']}**")
        
        if st.button("Xem bản đồ ngay", use_container_width=True):
            st.rerun()

# --- 4. GIAO DIỆN & LOGIC ---

if not st.session_state.started:
    # -----------------------------------------
    # MÀN HÌNH 1: NỀN ĐỎ ĐÔ, CHỮ TRẮNG
    # -----------------------------------------
    st.markdown("""
        <style>
        .stApp { background-color: #800000 !important; }
        [data-testid="stSidebar"] { display: none; }
        .stButton>button { 
            background-color: #ffffff; color: #800000; 
            border: none; border-radius: 12px; 
            font-weight: 800; padding: 0.75rem 2rem; font-size: 1.2rem;
        }
        .stButton>button:hover { background-color: #FFD700; color: #800000; }
        </style>
    """, unsafe_allow_html=True)
    st.markdown("<h1 style='text-align: center; font-size: 4rem; color: #FFD700;'> HÔM NAY ĂN GÌ?</h1>", unsafe_allow_html=True)
    st.markdown("<p style='text-align: center; color: #f0f0f0; font-size: 1.3rem; margin-bottom: 40px;'>Hệ chuyên gia AI - Gợi ý món ăn chuẩn gu</p>", unsafe_allow_html=True)
    
   
    img_urls = [
        "https://images.unsplash.com/photo-1504674900247-0877df9cc836?w=400",
        "https://images.unsplash.com/photo-1540189549336-e6e99c3679fe?w=400",
        "https://images.unsplash.com/photo-1565299624946-b28f40a0ae38?w=400",
        "https://images.unsplash.com/photo-1512621776951-a57141f2eefd?w=400",
        "https://images.unsplash.com/photo-1493770348161-369560ae357d?w=400",
        "https://images.unsplash.com/photo-1555939594-58d7cb561ad1?w=400",
        "https://images.unsplash.com/photo-1467003909585-2f8a72700288?w=400"
    ]
    
    cols = st.columns(3)
    for i in range(len(img_urls)):
        with cols[i % 3]:
            st.image(img_urls[i], use_container_width=True)
            
    st.markdown("<br>", unsafe_allow_html=True)
    _, mid_col, _ = st.columns([1, 1, 1])
    with mid_col:
        if st.button("BẮT ĐẦU TRẢI NGHIỆM", use_container_width=True):
            st.session_state.started = True
            st.rerun()

else:
    # MÀN HÌNH 2: NỀN TRẮNG, SIDEBAR ĐỎ ĐÔ
    st.markdown("""
        <style>
        .stApp { background-color: #ffffff !important; }
        [data-testid="stSidebar"] { background-color: #800000 !important; }
        
        /* Chữ chung của sidebar là trắng */
        [data-testid="stSidebar"] * { color: #ffffff; }
        
        /* THẺ THỜI TIẾT: Nền trắng, CHỮ ĐỎ ĐÔ */
        .weather-card {
            background-color: #ffffff !important;
            border-radius: 15px;
            padding: 20px;
            margin-bottom: 20px;
            box-shadow: 0 4px 15px rgba(0,0,0,0.3);
            border-left: 5px solid #FFD700;
        }
        /* Ép chữ trong thẻ này thành màu đỏ đô */
        .weather-card h3, .weather-card b, .weather-card span, .weather-card p {
            color: #800000 !important;
            margin: 8px 0 !important;
        }
        
        .history-card { 
            background: rgba(255,255,255,0.1); padding: 10px; 
            border-radius: 10px; margin-bottom: 8px; border: 1px solid rgba(255,255,255,0.3);
        }
        .stButton>button { background-color: #000000; color: #FFD700; border-radius: 12px; }
        
        /* CSS cho thẻ thông tin quán ăn */
        .restaurant-card {
            background-color: #f8f9fa;
            border-radius: 15px;
            padding: 20px;
            margin-bottom: 20px;
            box-shadow: 0 4px 15px rgba(0,0,0,0.15);
            border-left: 5px solid #800000;
        }
        .restaurant-card h3 {
            color: #800000;
            margin-top: 0;
            font-size: 1.5rem;
        }
        .restaurant-card p {
            color: #333;
            margin: 8px 0;
            font-size: 1rem;
        }
        .restaurant-card b {
            color: #800000;
        }
        .restaurant-image {
            border-radius: 12px;
            object-fit: cover;
            width: 100%;
            height: 300px;
        }
        </style>
    """, unsafe_allow_html=True)

    weather_data = api.get_weather_score("Ho Chi Minh")
    w_score = weather_data['score']

    with st.sidebar:
        # Thẻ thời tiết đã được sửa lỗi hiển thị chữ
        st.markdown(f"""
        <div class="weather-card">
            <h3 style="text-align:center;">🌦️ Thời tiết hiện tại</h3>
            <p>🌡️ <b>Nhiệt độ:</b> <span>{weather_data['temp']}°C</span></p>
            <p>🌍 <b>Trạng thái:</b> <span>{weather_data['desc']}</span></p>
            <hr style="border-color: #800000; opacity: 0.2;">
            <p style="text-align:center; font-weight: bold; font-size: 1.1rem;">
        </div>
        """, unsafe_allow_html=True)
        st.markdown("---")
        st.markdown("<h3>🕒 Lịch sử tìm kiếm</h3>", unsafe_allow_html=True)
        if st.session_state.search_history:
            for item in reversed(st.session_state.search_history):
                st.markdown(f"""
                <div class="history-card">
                    <b>{item['cuisine']}</b> | {item['budget']}<br>
                    <small>Lúc: {item['time']}</small>
                </div>
                """, unsafe_allow_html=True)
        else:
            st.write("Chưa có lịch sử.")
            
        st.markdown("<br>", unsafe_allow_html=True)
        if st.button(" ⬅ Quay lại trang chủ", use_container_width=True):
            st.session_state.started = False
            st.session_state.results = None
            st.rerun()

    # GIỮA GIAO DIỆN
    st.markdown("<h2 style='text-align: center; color: #800000; margin-bottom: 30px;'>Hôm nay bạn muốn ăn gì?</h2>", unsafe_allow_html=True)
    
    with st.container():
        col_a, col_b = st.columns(2)
        with col_a:
            hunger_ran = st.slider("Mức độ đói của bạn:", 0.0, 10.0, 5.0)
            health_goal = st.selectbox("Mục tiêu sức khỏe:", ["Normal", "Diet", "Bulking"])
        with col_b:
            budget_ran = st.slider("Ngân sách (nghìn VND):", 0, 500, 100)
            time_ran = st.slider("Thời gian bạn có (phút):", 0, 120, 30)

    st.markdown("<br>", unsafe_allow_html=True)
    if st.button(" ĂN GÌ ĐÂY ?", use_container_width=True):
        show_results_dialog(hunger_ran, budget_ran, time_ran, health_goal, w_score)

    # PHẦN BẢN ĐỒ & CHI TIẾT
    if st.session_state.results:
        res = st.session_state.results
        st.divider()
        st.markdown("<h2 style='color: #800000;'>🗺️ Khám phá địa điểm</h2>", unsafe_allow_html=True)
        
        with st.expander("⌕ Xem lại thông số gợi ý", expanded=True):
            c1, c2, c3, c4 = st.columns(4)
            c1.metric("🛒 Ẩm thực", res['cuisine_label'])
            c2.metric("🍜 Loại món", res['meal_type_label'])
            c3.metric("💰 Tầm giá", res['price_label'])
            c4.metric("📍 Không gian", res['place_label'])

        if location and 'coords' in location:
            curr_lat, curr_lng = location['coords']['latitude'], location['coords']['longitude']
            filtered_shops = [s for s in api.restaurants if s['cuisine'].lower() == res['cuisine_label'].lower()]
            
            if filtered_shops:
                st.success(f"📌 Có {len(filtered_shops)} quán {res['cuisine_label']} phù hợp quanh đây!")
                selected_name = st.selectbox("Bạn muốn xem đường đến quán nào?", [s['name'] for s in filtered_shops])
                target_shop = next(s for s in filtered_shops if s['name'] == selected_name)
                
               # ✨ HIỂN THỊ HÌNH ẢNH QUÁN ĂN
                st.markdown(f"<h3 style='color: #800000;'>🍽️ {target_shop['name']}</h3>", unsafe_allow_html=True)
                col_img, col_info = st.columns([2, 1])
                
                with col_img:
                    if "image_url" in target_shop:
                        st.image(target_shop['image_url'], use_container_width=True, caption=target_shop['name'])
                    else:
                        st.image("https://via.placeholder.com/400x300?text=" + target_shop['name'].replace(" ", "+"), use_container_width=True)
                
                with col_info:
                    st.markdown(f"""
                    <div style='background: #f0f0f0; padding: 15px; border-radius: 10px; border-left: 4px solid #800000;'>
                        <p>🛒 <b>Loại:</b> {target_shop['cuisine'].upper()}</p>
                        <p>💰 <b>Giá:</b> {target_shop['price']}</p>
                        <p>🍜 <b>Bữa:</b> {target_shop['meal_type']}</p>
                        <p>📍 <b>Địa điểm:</b> {target_shop['place']}</p>
                    </div>
                    """, unsafe_allow_html=True)
                
                st.divider()
                
                # ✨ HIỂN THỊ BẢN ĐỒ
                st.markdown("<h3 style='color: #800000;'>📍 Lộ trình đến quán</h3>", unsafe_allow_html=True)
                embed_url = api.get_google_maps_embed_url(curr_lat, curr_lng, target_shop['latitude'], target_shop['longitude'])
                components.html(f'<iframe width="100%" height="450" src="{embed_url}" frameborder="0" style="border-radius:15px; box-shadow: 0px 4px 12px rgba(0,0,0,0.1);"></iframe>', height=460)

                delivery_time = api.get_delivery_estimation(curr_lat, curr_lng, target_shop['latitude'], target_shop['longitude'])
                st.info(f"🚗 **Dự kiến giao hàng:** ~{delivery_time} phút")
                
                if st.button(f" Xác nhận sẽ ăn ở {target_shop['name']}!", use_container_width=True):
                    api.learn_user_taste(target_shop['name'])
                    current_search = {
                        "cuisine": res['cuisine_label'],
                        "budget": res['price_label'],
                        "time": time.strftime("%H:%M")}
                    st.session_state.search_history.append(current_search)
                    if len(st.session_state.search_history) > 5:
                        st.session_state.search_history.pop(0)           
                    st.session_state.confirm_msg = f"Tuyệt vời! Mình đã ghi nhớ bạn thích quán {target_shop['name']}. Chúc bạn ngon miệng"    
                    st.rerun()
                if 'confirm_msg' in st.session_state:
                    st.success(st.session_state.confirm_msg)
                    
            else:
                st.warning("Hic, không tìm thấy quán nào trong database khớp với gợi ý rồi!")
        else:
            st.info("Vui lòng cho phép trình duyệt truy cập vị trí để hiện bản đồ quán ăn !")
