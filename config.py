weather_api_key = "3946f6d6e4515b773dbc474cc9d58571"
city_default = "Ho Chi Minh"
google_maps_api_key = "AIzaSyCO0W0DPcD0StDSg8iNvE202SxydvGeIlA"

map_center = [10.76198, 106.66956]
map_zoom = 15

restaurants = [ #Danh sách quán ăn
    #korean
    {"name": "3A Korean Food", "cuisine": "korean", "latitude": 10.746147, "longitude": 106.636509, "price": "moderate", "meal_type": "full meal", "features": {"spicy": 0.8, "sour": 0.2, "sweet": 0.6, "salty": 0.5}, "place": "restaurant"},
    {"name": "The B6 Original Taste", "cuisine": "korean", "latitude": 10.806053, "longitude": 106.715401, "price": "moderate", "meal_type": "full meal", "features": {"spicy": 0.7, "sour": 0.3, "sweet": 0.5, "salty": 0.6}, "place": "restaurant"},
    {"name": "Hẻm Fast Food", "cuisine": "korean", "latitude": 10.764710, "longitude": 106.690441, "price": "moderate", "meal_type": "full meal", "features": {"spicy": 0.6, "sour": 0.2, "sweet": 0.7, "salty": 0.5}, "place": "street"},
    {"name": "Kokoria", "cuisine": "korean", "latitude": 10.785925, "longitude": 106.664114, "price": "moderate", "meal_type": "full meal", "features": {"spicy": 0.7, "sour": 0.4, "sweet": 0.4, "salty": 0.6}, "place": "restaurant"},
    {"name": "Chicken Plus", "cuisine": "korean", "latitude": 10.761490, "longitude": 106.669544, "price": "moderate", "meal_type": "full meal", "features": {"spicy": 0.5, "sour": 0.1, "sweet": 0.8, "salty": 0.6}, "place": "restaurant"},
    {"name": "Busan Korean Food", "cuisine": "korean", "latitude": 10.762449, "longitude": 106.668803, "price": "cheap", "meal_type": "full meal", "features": {"spicy": 0.6, "sour": 0.3, "sweet": 0.6, "salty": 0.5}, "place": "restaurant"},
    {"name": "Mỳ cay Sasin", "cuisine": "korean", "latitude": 10.762929, "longitude": 106.669458, "price": "cheap", "meal_type": "full meal", "features": {"spicy": 1.0, "sour": 0.5, "sweet": 0.3, "salty": 0.6}, "place": "restaurant"},
    {"name": "Hanuri", "cuisine": "korean", "latitude": 10.772341, "longitude": 106.670941, "price": "moderate", "meal_type": "full meal", "features": {"spicy": 0.6, "sour": 0.2, "sweet": 0.7, "salty": 0.5}, "place": "restaurant"},
    #italian
    {"name": "Pizza Có Tâm", "cuisine": "italian", "latitude": 10.748176, "longitude": 106.621559, "price": "moderate", "meal_type": "full meal", "features": {"spicy": 0.1, "sour": 0.2, "sweet": 0.2, "salty": 0.7}, "place": "street"},
    {"name": "Pizza 4P's Vincom Plaza 3/2", "cuisine": "italian", "latitude": 10.776365, "longitude": 106.681096, "price": "expensive", "meal_type": "full meal", "features": {"spicy": 0.1, "sour": 0.3, "sweet": 0.2, "salty": 0.6}, "place": "restaurant"},
    {"name": "Al Fresco's", "cuisine": "italian", "latitude": 10.770951, "longitude": 106.670645, "price": "expensive", "meal_type": "full meal", "features": {"spicy": 0.2, "sour": 0.2, "sweet": 0.3, "salty": 0.8}, "place": "restaurant"},
    {"name": "Domino's Pizza", "cuisine": "italian", "latitude": 10.761977, "longitude": 106.669227, "price": "moderate", "meal_type": "full meal", "features": {"spicy": 0.3, "sour": 0.1, "sweet": 0.2, "salty": 0.7}, "place": "restaurant"},
    #chinese
    {"name": "Vua Bít Tết Tawaza", "cuisine": "chinese", "latitude": 10.766496, "longitude": 106.680463, "price": "moderate", "meal_type": "full meal", "features": {"spicy": 0.5, "sour": 0.1, "sweet": 0.4, "salty": 0.7}, "place": "restaurant"},
    {"name": "Long Wang", "cuisine": "chinese", "latitude": 10.774723, "longitude": 106.668704, "price": "expensive", "meal_type": "full meal", "features": {"spicy": 0.6, "sour": 0.2, "sweet": 0.3, "salty": 0.6}, "place": "restaurant"},
    {"name": "Chang Kang Kung", "cuisine": "chinese", "latitude": 10.773206, "longitude": 106.673273, "price": "expensive", "meal_type": "full meal", "features": {"spicy": 0.5, "sour": 0.2, "sweet": 0.3, "salty": 0.5}, "place": "restaurant"},
    {"name": "Dimsum Tâm Tâm", "cuisine": "chinese", "latitude": 10.768568, "longitude": 106.667265, "price": "cheap", "meal_type": "full meal", "features": {"spicy": 0.7, "sour": 0.2, "sweet": 0.4, "salty": 0.6}, "place": "street"},
    {"name": "Hua Wu Lou", "cuisine": "chinese", "latitude": 10.769842, "longitude": 106.681262, "price": "moderate", "meal_type": "full meal", "features": {"spicy": 0.4, "sour": 0.3, "sweet": 0.3, "salty": 0.7}, "place": "restaurant"},
    {"name": "Mì Sủi Cảo Tofu", "cuisine": "chinese", "latitude": 10.757082, "longitude": 106.669944, "price": "cheap", "meal_type": "full meal", "features": {"spicy": 0.6, "sour": 0.3, "sweet": 0.3, "salty": 0.7}, "place": "street"},
    #vietnamese
    {"name": "Steak bò 39k", "cuisine": "vietnamese", "latitude": 10.788231, "longitude": 106.678988, "price": "cheap", "meal_type": "full meal", "features": {"spicy": 0.1, "sour": 0.1, "sweet": 0.5, "salty": 0.8}, "place": "street"},
    {"name": "Phở Thắng", "cuisine": "vietnamese", "latitude": 10.764470, "longitude": 106.669958, "price": "cheap", "meal_type": "healthy meal", "features": {"spicy": 0.1, "sour": 0.2, "sweet": 0.3, "salty": 0.6}, "place": "street"},
    {"name": "Bún Thái - Cơm Việt", "cuisine": "vietnamese", "latitude": 10.764319, "longitude": 106.669897, "price": "cheap", "meal_type": "healthy meal", "features": {"spicy": 0.7, "sour": 0.6, "sweet": 0.4, "salty": 0.6}, "place": "street"},
    {"name": "De Tham Restaurant", "cuisine": "vietnamese", "latitude": 10.768887, "longitude": 106.695795, "price": "expensive", "meal_type": "full meal", "features": {"spicy": 0.2, "sour": 0.1, "sweet": 0.4, "salty": 0.5}, "place": "restaurant"},
    {"name": "Bò Nướng Nam Vang", "cuisine": "vietnamese", "latitude": 10.764649, "longitude": 106.671758, "price": "cheap", "meal_type": "full meal", "features": {"spicy": 0.4, "sour": 0.1, "sweet": 0.6, "salty": 0.7}, "place": "street"},
    {"name": "Cơm gà Tam Kỳ", "cuisine": "vietnamese", "latitude": 10.760605, "longitude": 106.668110, "price": "moderate", "meal_type": "full meal", "features": {"spicy": 0.2, "sour": 0.1, "sweet": 0.3, "salty": 0.6}, "place": "street"},
    #japanese
    {"name": "SushiWay Nguyễn Tri Phương", "cuisine": "japanese", "latitude": 10.760712, "longitude": 106.669679, "price": "expensive", "meal_type": "healthy meal", "features": {"spicy": 0.1, "sour": 0.4, "sweet": 0.3, "salty": 0.4}, "place": "restaurant"},
    {"name": "Haru Sushi", "cuisine": "japanese", "latitude": 10.765141, "longitude": 106.668457, "price": "expensive", "meal_type": "healthy meal", "features": {"spicy": 0.1, "sour": 0.3, "sweet": 0.3, "salty": 0.5}, "place": "restaurant"},
    {"name": "Toshiro Ramen", "cuisine": "japanese", "latitude": 10.760598, "longitude": 106.669583, "price": "moderate", "meal_type": "full meal", "features": {"spicy": 0.2, "sour": 0.1, "sweet": 0.2, "salty": 0.8}, "place": "restaurant"},
    {"name": "Kohaku Udon & Ramen", "cuisine": "japanese", "latitude": 10.764505, "longitude": 106.670256, "price": "moderate", "meal_type": "full meal", "features": {"spicy": 0.1, "sour": 0.2, "sweet": 0.2, "salty": 0.7}, "place": "restaurant"},
    {"name": "Up Noddle Tokyo/Saigon", "cuisine": "japanese", "latitude": 10.791508, "longitude": 106.711861, "price": "moderate", "meal_type": "full meal", "features": {"spicy": 0.2, "sour": 0.1, "sweet": 0.2, "salty": 0.7}, "place": "restaurant"},
    #thai
    {"name": "Som Tum Thai", "cuisine": "thai", "latitude": 10.765194, "longitude": 106.668182, "price": "expensive", "meal_type": "full meal", "features": {"spicy": 0.9, "sour": 0.8, "sweet": 0.5, "salty": 0.6}, "place": "restaurant"},
    {"name": "Chili Thai", "cuisine": "thai", "latitude": 10.757412, "longitude": 106.662744, "price": "expensive", "meal_type": "full meal", "features": {"spicy": 0.8, "sour": 0.7, "sweet": 0.6, "salty": 0.5}, "place": "restaurant"},
    {"name": "Quán Thái Khapi", "cuisine": "thai", "latitude": 10.739578, "longitude": 106.704333, "price": "moderate", "meal_type": "full meal", "features": {"spicy": 0.7, "sour": 0.6, "sweet": 0.6, "salty": 0.6}, "place": "street"},
    {"name": "Chada Thái", "cuisine": "thai", "latitude": 10.774460, "longitude": 106.668950, "price": "expensive", "meal_type": "full meal", "features": {"spicy": 0.8, "sour": 0.7, "sweet": 0.5, "salty": 0.6}, "place": "restaurant"},
    #western
    {"name": "Popeyes", "cuisine": "western", "latitude": 10.760805, "longitude": 106.681333, "price": "moderate", "meal_type": "fast food", "features": {"spicy": 0.4, "sour": 0.1, "sweet": 0.2, "salty": 0.8}, "place": "restaurant"},
    {"name": "McDonald's", "cuisine": "western", "latitude": 10.772261, "longitude": 106.667808, "price": "moderate", "meal_type": "fast food", "features": {"spicy": 0.1, "sour": 0.1, "sweet": 0.3, "salty": 0.7}, "place": "restaurant"},
    {"name": "KFC", "cuisine": "western", "latitude": 10.767520, "longitude": 106.674711, "price": "moderate", "meal_type": "fast food", "features": {"spicy": 0.3, "sour": 0.1, "sweet": 0.2, "salty": 0.8}, "place": "restaurant"},
    {"name": "Jollibee", "cuisine": "western", "latitude": 10.760872, "longitude": 106.663846, "price": "moderate", "meal_type": "fast food", "features": {"spicy": 0.2, "sour": 0.1, "sweet": 0.4, "salty": 0.7}, "place": "restaurant"},
    {"name": "Lotteria", "cuisine": "western", "latitude": 10.753101, "longitude": 106.670077, "price": "moderate", "meal_type": "fast food", "features": {"spicy": 0.2, "sour": 0.1, "sweet": 0.4, "salty": 0.7}, "place": "restaurant"},
    {"name": "ELSOL Meat&Wine", "cuisine": "western", "latitude": 10.775424, "longitude": 106.689897, "price": "expensive", "meal_type": "fast food", "features": {"spicy": 0.1, "sour": 0.1, "sweet": 0.2, "salty": 0.6}, "place": "restaurant"},
    {"name": "CHIIK Steak & Pasta", "cuisine": "western", "latitude": 10.820630, "longitude": 106.780258, "price": "expensive", "meal_type": "fast food", "features": {"spicy": 0.1, "sour": 0.2, "sweet": 0.2, "salty": 0.7}, "place": "restaurant"},
    #drinks
    {"name": "Gong Cha", "cuisine": "drinks", "latitude": 10.761873, "longitude": 106.669514, "price": "cheap", "meal_type": "snack", "features": {"spicy": 0.0, "sour": 0.1, "sweet": 0.9, "salty": 0.1}, "place": "restaurant"},
    {"name": "Trà sữa TocoToco", "cuisine": "drinks", "latitude": 10.763024, "longitude": 106.669031, "price": "cheap", "meal_type": "snack", "features": {"spicy": 0.0, "sour": 0.1, "sweet": 0.9, "salty": 0.1}, "place": "street"},
    {"name": "Rau Má Mix", "cuisine": "drinks", "latitude": 10.762304, "longitude": 106.670856, "price": "cheap", "meal_type": "snack", "features": {"spicy": 0.0, "sour": 0.0, "sweet": 0.8, "salty": 0.1}, "place": "street"},
    {"name": "Sinh tố Hẻm", "cuisine": "drinks", "latitude": 10.760887, "longitude": 106.668364, "price": "cheap", "meal_type": "snack", "features": {"spicy": 0.0, "sour": 0.4, "sweet": 0.8, "salty": 0.0}, "place": "street"},
    {"name": "The Coffee House", "cuisine": "drinks", "latitude": 10.757883, "longitude": 106.670365, "price": "moderate", "meal_type": "snack", "features": {"spicy": 0.0, "sour": 0.0, "sweet": 0.7, "salty": 0.1}, "place": "restaurant"},
    {"name": "Phúc Long Tea & Coffee", "cuisine": "drinks", "latitude": 10.762527, "longitude": 106.671892, "price": "moderate", "meal_type": "snack", "features": {"spicy": 0.0, "sour": 0.0, "sweet": 0.6, "salty": 0.1}, "place": "restaurant"},
    #dessert
    {"name": "Ngọt Ngào Sweet & More", "cuisine": "dessert", "latitude": 10.793007, "longitude": 106.688109, "price": "moderate", "meal_type": "snack", "features": {"spicy": 0.0, "sour": 0.2, "sweet": 0.9, "salty": 0.1}, "place": "restaurant"},
    {"name": "Doughnut House", "cuisine": "dessert", "latitude": 10.791516, "longitude": 106.690964, "price": "cheap", "meal_type": "snack", "features": {"spicy": 0.0, "sour": 0.0, "sweet": 1.0, "salty": 0.1}, "place": "street"},
    {"name": "Cream - Saigon Gelato", "cuisine": "dessert", "latitude": 10.773857930991841, "longitude": 106.67640147534718, "price": "cheap", "meal_type": "snack", "features": {"spicy": 0.0, "sour": 0.0, "sweet": 1.0, "salty": 0.1}, "place": "restaurant"},        
    {"name": "Fusu House", "cuisine": "dessert", "latitude": 10.75644516621391, "longitude": 106.6504358976925, "price": "cheap", "meal_type": "snack", "features": {"spicy": 0.0, "sour": 0.1, "sweet": 0.9, "salty": 0.1}, "place": "street"},        
    #temple meal
    {"name": "Chay An Cát Tường", "cuisine": "temple meal", "latitude": 10.761431, "longitude": 106.668780, "price": "cheap", "meal_type": "healthy meal", "features": {"spicy": 0.1, "sour": 0.2, "sweet": 0.4, "salty": 0.5}, "place": "street"},
    {"name": "Bếp chay Nhân Duyên", "cuisine": "temple meal", "latitude": 10.761520, "longitude": 106.674831, "price": "expensive", "meal_type": "healthy meal", "features": {"spicy": 0.2, "sour": 0.2, "sweet": 0.3, "salty": 0.4}, "place": "restaurant"},
    {"name": "Nhà hàng chay Mộc Nhiên", "cuisine": "temple meal", "latitude": 10.761011, "longitude": 106.673028, "price": "moderate", "meal_type": "healthy meal", "features": {"spicy": 0.1, "sour": 0.2, "sweet": 0.3, "salty": 0.5}, "place": "restaurant"},
    {"name": "Quán chay Bát Nhã", "cuisine": "temple meal", "latitude": 10.760623, "longitude": 106.666091, "price": "cheap", "meal_type": "healthy meal", "features": {"spicy": 0.2, "sour": 0.1, "sweet": 0.4, "salty": 0.5}, "place": "street"}
    ]

app_tittle = "Hôm nay ăn gì?"
app_icon = "🍽️"