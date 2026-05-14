import requests
import googlemaps
import numpy as np
import random
import pandas as pd
from config import restaurants

class APIServices:
    def __init__(self, weather_api_key="3946f6d6e4515b773dbc474cc9d58571", gmaps_api_key="AIzaSyCO0W0DPcD0StDSg8iNvE202SxydvGeIlA"):
        self.weather_api_key = weather_api_key
        self.gmaps_api_key = gmaps_api_key
        self.restaurants = restaurants
        self.user_profile = {"spicy": 0.5, "sour": 0.5, "sweet": 0.5, "salty":0.5}
        self.learning_rate = 0.1

    def get_weather_score(self, city="Ho Chi Minh"):
        url = f"http://api.openweathermap.org/data/2.5/weather?q={city}&appid={self.weather_api_key}&units=metric"
        try:
            response = requests.get(url).json()
            main_status = response['weather'][0]['main'] #trạng thái chính 
            desc = response['weather'][0]['description'] #mô tả chi tiết
            temp = response['main']['temp'] #nhiệt độ
            weather_lower = main_status.lower()
            if "rain" in weather_lower or "thunderstorm" in weather_lower:
                score = 9.0 
            elif temp < 24:
                score = 6.5
            elif 24 <= temp <= 30:
                score = 3.5  
            else:
                score = 1.2 
            return {
                "score": score,
                "temp": temp,
                "desc": desc.capitalize(),
                "status": main_status
            }
        except Exception as e:
            print(f"Lỗi hệ thống khi gọi API: {e}")
            return {
                "score": 5.0, 
                "temp": "N/A", 
                "desc": "Không lấy được dữ liệu", 
                "status": "Error"
            }
        
    def learn_user_taste(self, restaurant_name):
        restaurant = next((r for r in self.restaurants if r["name"] == restaurant_name), None)
        if restaurant and "features" in restaurant:
            feat = restaurant["features"]
            for taste in self.user_profile:
                self.user_profile[taste] += self.learning_rate * (feat[taste] - self.user_profile[taste])
            print(f"Đã lọc được gu của bạn: {self.user_profile}")
    
    def re_rank_by_taste(self, fuzzy_candidates):
        if not fuzzy_candidates:
            return []
        ranked_list = []
        for res in fuzzy_candidates:
            if "features" in res:
                res_feat = res["features"]
                diff = sum(abs(res_feat[t] - self.user_profile[t]) for t in self.user_profile)
                score = 1 / (1 + diff)
            else:
                score = 0
            ranked_list.append((res, score))
        ranked_list.sort(key=lambda x: x[1], reverse=True)
        return [item[0] for item in ranked_list]
    
    def get_restaurants_by_cuisine(self, cuisine_label):
        return [r for r in self.restaurants if r["cuisine"].lower() == cuisine_label.lower()]
        
    def get_keywords(self, cuisine_val, place_val):
        cuisines = [
            "vietnamese", "korean", "japanese", "chinese", "western", 
            "thai", "italian", "drinks", "dessert", "temple meal"
        ]
        idx = int(cuisine_val)
        idx = max(0, min(idx, len(cuisines) - 1))
        cuisine_label = cuisines[idx]
        place_label = "street" if place_val < 5.0 else "restaurant"
        return cuisine_label, place_label

    def get_google_maps_embed_url(self, origin_lat, origin_lng, dest_lat, dest_lng):
        base_url = "https://www.google.com/maps/embed/v1/directions"
        origin = f"{origin_lat},{origin_lng}"
        destination = f"{dest_lat},{dest_lng}"
        return f"{base_url}?key={self.gmaps_api_key}&origin={origin}&destination={destination}&mode=driving"
    
    def search_nearby_real_restaurants(self, lat, lng, keyword):
        places_result = self.gmaps.places_nearby(
            location=(lat, lng),
            radius=2000,
            keyword=keyword,
            type='restaurant'
        )
        return places_result.get('results', [])
    
    def get_delivery_estimation(self, lat1, lng1, lat2, lng2):
        distance = ((lat1 - lat2)**2 + (lng1 - lng2)**2)**0.5 * 111
        travel_time = distance * 2 
        prep_time = random.randint(10, 20) 
        total_time = int(travel_time + prep_time)
        return total_time 
        
