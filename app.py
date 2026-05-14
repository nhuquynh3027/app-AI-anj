import streamlit as st
from fuzzy_logic import FoodFuzzyLogic
from api_services import APIServices
import time
import streamlit.components.v1 as components
from streamlit_js_eval import get_geolocation

st.set_page_config(page_title="Hôm nay ăn gì?", page_icon="🍴", layout="wide")

@st.cache_resource
def init_system():
    return FoodFuzzyLogic(), APIServices()

engine, api = init_system()
location = get_geolocation()

st.markdown(
    """
    <style>
    .stApp {background-color: #FFE6EB;}
    [data-testid="stSidebar"] {background-color: #FFD8DF;}
    </style>
    """,
    unsafe_allow_html=True
)

if 'api_service' not in st.session_state:
    st.session_state.api_service = APIServices()
if 'results' not in st.session_state:
    st.session_state.results = None
if 'clicked_location' not in st.session_state:
    st.session_state.clicked_location = None
if 'search_history' not in st.session_state:
    st.session_state.search_history = []

if location is None:
    st.info("Bạn ơi, vui lòng bật định vị để xem được bản đồ nhé (• ᴗ •)!")
else:
    st.toast("Ting ting! Đã kết nối GPS thành công!", icon="🎉")

st.sidebar.header("✨ Hôm nay bạn muốn ăn gì?")
hunger_ran = st.sidebar.slider("Đánh giá mức độ đói của bạn:", 0.0, 10.0, 5.0, 0.1)
budget_ran = st.sidebar.slider("Ngân sách của bạn (nghìn VND):", 0, 500, 100, 10)
time_ran = st.sidebar.slider("Thời gian bạn có (phút):", 0, 120, 30, 5)
health_goal = st.sidebar.selectbox("Mục tiêu sức khỏe:", ["Normal", "Diet", "Bulking"])

with st.spinner('Đang kiểm tra thời tiết...'):
    weather_data = api.get_weather_score("Ho Chi Minh")
    weather_score = weather_data['score']
st.sidebar.markdown("---")
st.sidebar.subheader("☁️ Thời tiết hiện tại")
st.sidebar.metric("🌡️ Nhiệt độ", f"{weather_data['temp']}°C")
st.sidebar.write(f"🌍 **Trạng thái:** {weather_data['desc']}")

@st.dialog("Kết quả của bạn đến rồi đây (˶ᵔ ᵕ ᵔ˶)~")    
def show_results_dialog(inputs, weather_score):   
    with st.spinner('Đang tính toán để tìm món ngon...'):
        time.sleep(1.5)
        health_map = {"Diet": 2.0, "Normal": 5.0, "Bulking": 8.0}
        raw = engine.recommend(
            hunger_ran=hunger_ran, 
            budget_ran=budget_ran, 
            time_ran=time_ran, 
            weather_ran=weather_score, 
            health_ran=health_map[health_goal]
        )

        res = {}
        #cuisine
        c = raw.get('cuisine', 5.0)
        if c < 1: res['cuisine_label'] = "Vietnamese"
        elif c < 2: res['cuisine_label'] = "Korean"
        elif c < 3: res['cuisine_label'] = "Japanese"
        elif c < 4: res['cuisine_label'] = "Chinese"
        elif c < 5: res['cuisine_label'] = "Western"
        elif c < 6: res['cuisine_label'] = "Thai"
        elif c < 7: res['cuisine_label'] = "Italian"
        elif c < 8: res['cuisine_label'] = "Drinks"
        elif c < 9: res['cuisine_label'] = "Dessert"
        else: res['cuisine_label'] = "Temple Meal"
        #meal_type
        m = raw.get('meal_type', 5.0)
        res['meal_type_label'] = "Ăn vặt" if m < 2.0 else "Fast food" if m < 5.0 else "Bữa chính" if m < 8.0 else "Bữa ăn lành mạnh"
        #price_range
        p = raw.get('price_range', 100)
        res['price_label'] = "Rẻ" if p < 50 else "Tầm trung" if p < 180 else "Sang chảnh"
        #place
        pl = raw.get('place', 5.0)
        res['place_label'] = "Vỉa hè" if pl < 5 else "Nhà hàng"
        st.session_state.results = res

        candidates = st.session_state.api_service.get_restaurants_by_cuisine(res['cuisine_label'])
        ranked_restaurants = st.session_state.api_service.re_rank_by_taste(candidates)
        st.session_state.final_restaurants = ranked_restaurants

        current_search = {
            "cuisine": res['cuisine_label'],
            "budget": f"{res['price_label']}",
            "time": time.strftime("%H:%M")
        }
        if not st.session_state.search_history or st.session_state.search_history[-1]['cuisine'] != current_search['cuisine']:
            st.session_state.search_history.append(current_search)
            if len(st.session_state.search_history) > 5:
                st.session_state.search_history.pop(0)

        st.success("⌯⌲ Đã tìm thấy quán phù hợp!")
        col1, col2 = st.columns(2)
        with col1:
            st.metric(f"🛒 **Kiểu ẩm thực**", res['cuisine_label'])
            st.write(f"🍜 **Loại món:** {res['meal_type_label']}")
        with col2:
            st.metric(f"💰 **Tầm giá**", res['price_label'])
            st.write(f"📍 **Địa điểm:** {res['place_label']}")
        st.write("---")
        if ranked_restaurants:
            top_choice = ranked_restaurants[0]
            st.success(f"Gợi ý dựa theo gu của bạn: **{top_choice['name']}**")
        if st.button("Xem bản đồ", use_container_width=True):
            st.session_state.results = res
            st.rerun()
        
if st.sidebar.button("Ăn gì đây （๑ᵔ⤙ᵔ๑）?", use_container_width=True):
    inputs = {'hunger': hunger_ran, 'budget': budget_ran, 'time': time_ran, 'health': health_goal}
    show_results_dialog(inputs, weather_data['score'])

st.sidebar.markdown("---")
st.sidebar.subheader("🕒 Lịch sử tìm kiếm")
if st.session_state.search_history:
    for item in reversed(st.session_state.search_history):
        st.sidebar.markdown(f"""
        <div class="history-card">
            <b>{item['cuisine']}</b> | {item['budget']}<br>
            <small>Lúc: {item['time']}</small>
        </div>
        """, unsafe_allow_html=True)
else:
    st.sidebar.write("Chưa có lịch sử tìm kiếm.")

if st.session_state.results:
    res = st.session_state.results
    st.title("🗺️Khám phá địa điểm")
    with st.expander("⌕ Xem lại thông số gợi ý", expanded=True):
        col1, col2, col3, col4 = st.columns(4)
        col1.metric("🛒 Kiểu ẩm thực", res['cuisine_label'])
        col2.metric("🍜 Loại món", res['meal_type_label'])
        col3.metric("💰 Tầm giá", res['price_label'])
        col4.metric("📍 Địa điểm", res['place_label'])
    st.divider()

    if location and 'coords' in location:
        curr_lat = location['coords']['latitude']
        curr_lng = location['coords']['longitude']
        if st.session_state.results:
            res = st.session_state.results
            filtered_shops = [
                s for s in api.restaurants 
                if s['cuisine'].lower() == res['cuisine_label'].lower()
            ]
            if filtered_shops:
                st.write(f"📌Có {len(filtered_shops)} quán {res['cuisine_label']} phù hợp!")
                shop_names = [s['name'] for s in filtered_shops]
                selected_name = st.selectbox("Bạn muốn xem đường đến quán nào?", shop_names)
                target_shop = next(s for s in filtered_shops if s['name'] == selected_name)
                st.subheader(f"Lộ trình đến: {target_shop['name']}")
                embed_url = api.get_google_maps_embed_url(
                    curr_lat, curr_lng, 
                    target_shop['latitude'], target_shop['longitude']
                )
                map_html = f"""
                    <iframe
                        width="100%" height="450" frameborder="0" 
                        style="border:0; border-radius: 15px; box-shadow: 0px 4px 12px rgba(0,0,0,0.1);"
                        src="{embed_url}" allowfullscreen>
                    </iframe>
                """
                st.components.v1.html(map_html, height=460)

                delivery_time = st.session_state.api_service.get_delivery_estimation(
                    curr_lat, curr_lng, target_shop['latitude'], target_shop['longitude']
                )
                st.info(f"🚗 **Dự kiến giao hàng:** ~{delivery_time} phút (đã bao gồm chuẩn bị)")
                if st.button(f"Xác nhận sẽ ăn ở {target_shop['name']}!", use_container_width=True):
                    st.session_state.api_service.learn_user_taste(target_shop['name'])
                    st.success(f"Cảm ơn bạn! Mình sẽ nhớ gu của bạn cho lần sau đó nha (˶ᵔ ᵕ ᵔ˶)~")
            else:
                st.warning("Hic, không tìm thấy quán nào trong database khớp với gợi ý rồi (˃̣̣̥ᯅ˂̣̣̥)!")
