import skfuzzy as fuzz
from skfuzzy import control as ctrl
import numpy as np

class FoodFuzzyLogic:
    def __init__(self):
        #input
        self.hunger = ctrl.Antecedent(np.arange(0, 11, 1), 'hunger')
        self.budget = ctrl.Antecedent(np.arange(0, 501, 1), 'budget')
        self.time = ctrl.Antecedent(np.arange(0, 121, 1), 'time')
        self.weather = ctrl.Antecedent(np.arange(0, 11, 0.05), 'weather')
        self.health = ctrl.Antecedent(np.arange(0, 11, 1), 'health')
        #output
        self.meal_type = ctrl.Consequent(np.arange(0, 11, 0.1), 'meal_type')
        self.cuisine = ctrl.Consequent(np.arange(0, 11, 0.05), 'cuisine')
        self.price_range = ctrl.Consequent(np.arange(0, 11, 1), 'price_range')
        self.calories = ctrl.Consequent(np.arange(0, 11, 1), 'calories')
        self.place = ctrl.Consequent(np.arange(0, 11, 1), 'place')

        self.setup_membership_functions()
        self.setup_rules()

    def setup_membership_functions(self):
        self.hunger['light'] = fuzz.trapmf(self.hunger.universe,[0,0,1.5,2.5])
        self.hunger['hungry'] = fuzz.trapmf(self.hunger.universe,[2,3,5.5,6])
        self.hunger['very hungry'] = fuzz.trapmf(self.hunger.universe,[5,6,7,8])
        self.hunger['starving'] = fuzz.trapmf(self.hunger.universe,[7.5,8,10,10])

        self.budget['cheap'] = fuzz.trimf(self.budget.universe,[0,0,50])
        self.budget['average'] = fuzz.trimf(self.budget.universe,[50,80,180])
        self.budget['expensive'] = fuzz.trimf(self.budget.universe,[180,300,500])

        self.time['very short'] = fuzz.trapmf(self.time.universe,[0,3,8,10])
        self.time['short'] = fuzz.trapmf(self.time.universe,[10,12,17,20])
        self.time['medium'] = fuzz.trapmf(self.time.universe,[20,22,30,35])
        self.time['long'] = fuzz.trapmf(self.time.universe,[35,40,90,120])    

        self.weather['hot'] = fuzz.trapmf(self.weather.universe, [0,0,2.45,2.5])
        self.weather['normal'] = fuzz.trapmf(self.weather.universe, [2.45,2.5,4.95,5])
        self.weather['cold'] = fuzz.trapmf(self.weather.universe, [4.95,5,7.45,7.5])
        self.weather['rainy'] = fuzz.trapmf(self.weather.universe, [7.45,7.5,10,10])

        self.health['diet'] = fuzz.trimf(self.health.universe, [0, 0, 5])
        self.health['balanced'] = fuzz.trimf(self.health.universe, [4, 5, 7])
        self.health['bulking'] = fuzz.trimf(self.health.universe, [6, 10, 10])

        self.meal_type['snack'] = fuzz.trapmf(self.meal_type.universe, [0,0,1.9,2])
        self.meal_type['fast food'] = fuzz.trapmf(self.meal_type.universe, [2,2.1,4.9,5])
        self.meal_type['full meal'] = fuzz.trapmf(self.meal_type.universe, [5,5.1,7.9,8])
        self.meal_type['healthy meal'] = fuzz.trapmf(self.meal_type.universe, [8,8.1,9.9,10])

        self.cuisine['vietnamese'] = fuzz.trapmf(self.cuisine.universe, [0,0,0.95,1])
        self.cuisine['korean'] = fuzz.trapmf(self.cuisine.universe, [1,1.05,1.95,2])
        self.cuisine['japanese'] = fuzz.trapmf(self.cuisine.universe, [2,2.05,2.95,3])
        self.cuisine['chinese'] = fuzz.trapmf(self.cuisine.universe, [3,3.05,3.95,4])
        self.cuisine['western'] = fuzz.trapmf(self.cuisine.universe, [4,4.05,4.95,5])
        self.cuisine['thai'] = fuzz.trapmf(self.cuisine.universe, [5,5.05,5.95,6])
        self.cuisine['italian'] = fuzz.trapmf(self.cuisine.universe, [6,6.05,6.95,7])
        self.cuisine['drinks'] = fuzz.trapmf(self.cuisine.universe, [7,7.05,7.95,8])
        self.cuisine['dessert'] = fuzz.trapmf(self.cuisine.universe, [8,8.05,8.95,9])
        self.cuisine['temple meal'] = fuzz.trapmf(self.cuisine.universe, [9,9.05,10,10])

        self.price_range['cheap'] = fuzz.trimf(self.price_range.universe, [0, 0, 5])
        self.price_range['moderate'] = fuzz.trimf(self.price_range.universe, [4, 5, 7])
        self.price_range['expensive'] = fuzz.trimf(self.price_range.universe, [6, 10, 10])

        self.calories['low'] = fuzz.trimf(self.calories.universe, [0, 0, 5])
        self.calories['medium'] = fuzz.trimf(self.calories.universe, [4, 5, 7])
        self.calories['high'] = fuzz.trimf(self.calories.universe, [6, 10, 10])

        self.place['street'] = fuzz.trapmf(self.place.universe, [0, 0, 4, 6])
        self.place['restaurant'] = fuzz.trapmf(self.place.universe, [4, 6, 10, 10])

    def setup_rules(self):
        #Hunger(very hungry/ starving) + Time(very short/short)
        rule1 = ctrl.Rule(self.hunger['very hungry'] & self.time['very short'], [self.meal_type['fast food'], self.cuisine['western'], self.calories['high'], self.place['street'], self.price_range['moderate']])
        rule2 = ctrl.Rule(self.hunger['starving'] & self.time['very short'], [self.meal_type['fast food'], self.cuisine['western'], self.calories['high'], self.place['street'], self.price_range['moderate']])
        rule3 = ctrl.Rule(self.hunger['very hungry'] & self.time['short'], [self.meal_type['fast food'], self.cuisine['western'], self.calories['high'], self.place['street'], self.price_range['moderate']])
        rule4 = ctrl.Rule(self.hunger['starving'] & self.time['short'], [self.meal_type['fast food'], self.cuisine['western'], self.calories['high'], self.place['street'], self.price_range['moderate']])
        rule5 = ctrl.Rule(self.hunger['very hungry'] & self.time['short'] & self.budget['cheap'], [self.meal_type['fast food'], self.cuisine['vietnamese'], self.price_range['cheap'], self.calories['high'], self.place['street']])
        rule6 = ctrl.Rule(self.hunger['starving'] & self.time['short'] & self.budget['cheap'], [self.meal_type['fast food'], self.cuisine['vietnamese'], self.price_range['cheap'], self.calories['high'], self.place['street']])
        rule7 = ctrl.Rule(self.hunger['very hungry'] & self.time['short'] & self.budget['average'], [self.meal_type['fast food'], self.cuisine['western'], self.price_range['moderate'], self.calories['high'], self.place['street']])
        rule8 = ctrl.Rule(self.hunger['starving'] & self.time['short'] & self.budget['average'], [self.meal_type['fast food'], self.cuisine['western'], self.price_range['moderate'], self.calories['high'], self.place['street']])
        rule9 = ctrl.Rule(self.hunger['very hungry'] & self.time['short'] & self.health['bulking'], [self.meal_type['fast food'], self.cuisine['vietnamese'], self.price_range['moderate'], self.calories['high'], self.place['street']])
        rule10 = ctrl.Rule(self.hunger['starving'] & self.time['short'] & self.health['bulking'], [self.meal_type['fast food'], self.cuisine['vietnamese'], self.price_range['moderate'], self.calories['high'], self.place['street']])
        #Weather(rainy/cold) | Weather(hot)
        rule11 = ctrl.Rule(self.weather['rainy'], [self.meal_type['full meal'], self.cuisine['vietnamese'], self.place['restaurant'], self.calories['high'], self.price_range['expensive']])
        rule12 = ctrl.Rule(self.weather['cold'], [self.meal_type['full meal'], self.cuisine['chinese'], self.place['restaurant'], self.calories['high'], self.price_range['expensive']])
        rule13 = ctrl.Rule(self.weather['hot'] & self.hunger['light'], [self.meal_type['snack'], self.cuisine['drinks'], self.place['street'], self.calories['medium'], self.price_range['moderate']])
        rule14 = ctrl.Rule(self.weather['rainy'] & self.hunger['starving'], [self.meal_type['full meal'], self.cuisine['vietnamese'], self.place['restaurant'], self.calories['high'], self.price_range['moderate']])
        rule15 = ctrl.Rule(self.weather['rainy'] & self.hunger['very hungry'], [self.meal_type['full meal'], self.cuisine['vietnamese'], self.place['restaurant'], self.calories['high'], self.price_range['moderate']])        
        rule16 = ctrl.Rule(self.weather['rainy'] & self.hunger['hungry'], [self.meal_type['full meal'], self.cuisine['korean'], self.place['restaurant'], self.calories['high'], self.price_range['moderate']])
        rule17 = ctrl.Rule(self.weather['cold'] & self.hunger['hungry'], [self.meal_type['full meal'], self.cuisine['chinese'], self.place['restaurant'], self.calories['high'], self.price_range['moderate']])
        rule18 = ctrl.Rule(self.weather['rainy'] & self.time['short'], [self.meal_type['fast food'], self.cuisine['western'], self.place['restaurant'], self.calories['medium'], self.price_range['moderate']])
        rule19 = ctrl.Rule(self.weather['hot'] & self.hunger['hungry'], [self.meal_type['full meal'], self.cuisine['japanese'], self.place['restaurant'], self.calories['medium'], self.price_range['moderate']])
        rule20 = ctrl.Rule(self.weather['hot'] & self.health['balanced'], [self.meal_type['full meal'], self.cuisine['temple meal'], self.place['restaurant'], self.calories['low'], self.price_range['moderate']])
        rule21 = ctrl.Rule(self.weather['normal'] & self.time['long'] & self.budget['expensive'], [self.meal_type['full meal'], self.cuisine['italian'], self.place['restaurant'],self.calories['medium'], self.price_range['expensive']])
        #Health(diet)
        rule22 = ctrl.Rule(self.health['diet'], [self.meal_type['healthy meal'], self.cuisine['temple meal'], self.calories['low'], self.price_range['cheap'], self.place['restaurant']])
        rule23 = ctrl.Rule(self.health['diet'] & self.budget['expensive'], [self.meal_type['healthy meal'], self.cuisine['japanese'], self.calories['low'], self.price_range['expensive'], self.place['restaurant']])
        rule24 = ctrl.Rule(self.health['diet'] & self.weather['hot'], [self.meal_type['healthy meal'], self.cuisine['japanese'], self.calories['low'], self.price_range['expensive'], self.place['restaurant']])
        rule25 = ctrl.Rule(self.health['diet'] & self.hunger['hungry'], [self.meal_type['full meal'], self.cuisine['temple meal'], self.calories['low'], self.price_range['cheap'], self.place['restaurant']])
        rule26 = ctrl.Rule(self.health['diet'] & self.time['short'], [self.meal_type['healthy meal'], self.cuisine['japanese'], self.calories['low'], self.price_range['moderate'], self.place['restaurant']])
        rule27 = ctrl.Rule(self.health['diet'] & self.hunger['light'], [self.meal_type['snack'], self.cuisine['drinks'], self.calories['low'], self.price_range['cheap'], self.place['street']])
        rule28 = ctrl.Rule(self.health['diet'] & self.budget['average'], [self.meal_type['healthy meal'], self.cuisine['japanese'], self.calories['low'], self.price_range['moderate'], self.place['restaurant']])
        rule29 = ctrl.Rule(self.health['diet'] & self.weather['cold'], [self.meal_type['healthy meal'], self.cuisine['vietnamese'], self.calories['low'], self.price_range['moderate'], self.place['restaurant']])
        rule30 = ctrl.Rule(self.health['diet'] & self.budget['cheap'], [self.meal_type['healthy meal'], self.cuisine['vietnamese'], self.calories['low'], self.price_range['cheap'], self.place['street']])        
        #Budget(expensive) + Time(long)
        rule31 = ctrl.Rule(self.budget['expensive'] & self.time['long'], [self.meal_type['full meal'], self.cuisine['italian'], self.place['restaurant'], self.price_range['expensive'], self.calories['medium']])
        rule32 = ctrl.Rule(self.budget['expensive'] & self.time['long'] & self.weather['cold'], [self.meal_type['full meal'], self.cuisine['chinese'], self.place['restaurant'], self.price_range['expensive'], self.calories['high']])
        rule33 = ctrl.Rule(self.budget['expensive'] & self.time['long'] & self.health['balanced'], [self.meal_type['full meal'], self.cuisine['japanese'], self.place['restaurant'], self.price_range['expensive'], self.calories['medium']])
        rule34 = ctrl.Rule(self.budget['expensive'] & self.time['long'] & self.hunger['starving'], [self.meal_type['full meal'], self.cuisine['western'], self.place['restaurant'], self.price_range['expensive'], self.calories['high']])
        rule35 = ctrl.Rule(self.budget['expensive'] & self.time['long'] & self.weather['rainy'], [self.meal_type['full meal'], self.cuisine['chinese'], self.place['restaurant'], self.price_range['expensive'], self.calories['high']])
        rule36 = ctrl.Rule(self.budget['expensive'] & self.time['medium'], [self.meal_type['full meal'], self.cuisine['western'], self.place['restaurant'], self.price_range['expensive'], self.calories['high']])
        rule37 = ctrl.Rule(self.budget['expensive'] & self.hunger['hungry'], [self.meal_type['full meal'], self.cuisine['western'], self.place['restaurant'], self.price_range['expensive'], self.calories['high']])
        rule38 = ctrl.Rule(self.budget['expensive'] & self.weather['hot'], [self.meal_type['healthy meal'], self.cuisine['japanese'], self.place['restaurant'], self.price_range['expensive'], self.calories['low']])
        rule39 = ctrl.Rule(self.budget['expensive'] & self.hunger['light'], [self.meal_type['snack'], self.cuisine['dessert'], self.place['restaurant'], self.price_range['expensive'], self.calories['medium']])
        rule40 = ctrl.Rule(self.budget['expensive'] & self.health['balanced'], [self.meal_type['full meal'], self.cuisine['japanese'], self.place['restaurant'], self.price_range['expensive'], self.calories['medium']])
        #Hunger(light) + Time(medium/long)
        rule41 = ctrl.Rule(self.hunger['light'] & self.time['medium'], [self.meal_type['snack'], self.cuisine['drinks'], self.place['street'], self.price_range['cheap'], self.calories['low']])
        rule42 = ctrl.Rule(self.hunger['light'] & self.time['long'], [self.meal_type['snack'], self.cuisine['dessert'], self.place['restaurant'], self.price_range['moderate'], self.calories['medium']])
        rule43 = ctrl.Rule(self.hunger['light'] & self.weather['rainy'], [self.meal_type['snack'], self.cuisine['dessert'], self.place['restaurant'], self.price_range['expensive'], self.calories['medium']])
        rule44 = ctrl.Rule(self.hunger['light'] & self.weather['hot'], [self.meal_type['snack'], self.cuisine['drinks'], self.place['street'], self.price_range['cheap'], self.calories['low']])
        rule45 = ctrl.Rule(self.hunger['light'] & self.budget['expensive'], [self.meal_type['snack'], self.cuisine['dessert'], self.place['restaurant'], self.price_range['expensive'], self.calories['medium']])
        rule46 = ctrl.Rule(self.hunger['light'] & self.budget['cheap'], [self.meal_type['snack'], self.cuisine['drinks'], self.place['street'], self.price_range['cheap'], self.calories['low']])
        rule47 = ctrl.Rule(self.hunger['light'] & self.health['balanced'], [self.meal_type['snack'], self.cuisine['dessert'], self.place['restaurant'], self.price_range['expensive'], self.calories['medium']])
        rule48 = ctrl.Rule(self.hunger['light'] & self.weather['cold'], [self.meal_type['snack'], self.cuisine['drinks'], self.place['restaurant'], self.price_range['moderate'], self.calories['low']])
        rule49 = ctrl.Rule(self.hunger['light'] & self.time['medium'] & self.weather['hot'], [self.meal_type['snack'], self.cuisine['drinks'], self.place['street'], self.price_range['cheap'], self.calories['low']])
        rule50 = ctrl.Rule(self.hunger['light'] & self.time['long'] & self.budget['expensive'], [self.meal_type['snack'], self.cuisine['dessert'], self.place['restaurant'], self.price_range['expensive'], self.calories['medium']])
        #Budget(cheap) + Hunger(hungry/very hungry)
        rule51 = ctrl.Rule(self.budget['cheap'] & self.hunger['hungry'], [self.meal_type['full meal'], self.cuisine['vietnamese'], self.place['street'], self.price_range['cheap'], self.calories['medium']])
        rule52 = ctrl.Rule(self.budget['cheap'] & self.hunger['very hungry'], [self.meal_type['full meal'], self.cuisine['chinese'], self.place['street'], self.price_range['cheap'], self.calories['high']])
        rule53 = ctrl.Rule(self.budget['cheap'] & self.weather['cold'], [self.meal_type['full meal'], self.cuisine['vietnamese'], self.place['street'], self.price_range['cheap'], self.calories['high']])
        rule54 = ctrl.Rule(self.budget['cheap'] & self.time['very short'], [self.meal_type['fast food'], self.cuisine['vietnamese'], self.place['street'], self.price_range['cheap'], self.calories['medium']])
        rule55 = ctrl.Rule(self.budget['cheap'] & self.health['balanced'], [self.meal_type['healthy meal'], self.cuisine['temple meal'], self.place['street'], self.price_range['cheap'], self.calories['low']])
        # Health(bulking) + Hunger
        rule56 = ctrl.Rule(self.health['bulking'] & self.hunger['starving'], [self.meal_type['full meal'], self.cuisine['western'], self.calories['high'], self.place['restaurant'], self.price_range['expensive']])
        rule57 = ctrl.Rule(self.health['bulking'] & self.weather['cold'], [self.meal_type['full meal'], self.cuisine['korean'], self.calories['high'], self.place['restaurant'], self.price_range['moderate']])
        rule58 = ctrl.Rule(self.health['bulking'] & self.budget['average'], [self.meal_type['full meal'], self.cuisine['chinese'], self.calories['high'], self.place['restaurant'], self.price_range['moderate']])
        rule59 = ctrl.Rule(self.health['bulking'] & self.time['short'], [self.meal_type['fast food'], self.cuisine['western'], self.calories['high'], self.place['street'], self.price_range['cheap']])
        rule60 = ctrl.Rule(self.health['bulking'] & self.weather['hot'], [self.meal_type['full meal'], self.cuisine['japanese'], self.calories['medium'], self.place['restaurant'], self.price_range['expensive']])
        # Time(very short) + các điều kiện khác
        rule61 = ctrl.Rule(self.time['very short'] & self.weather['rainy'], [self.meal_type['fast food'], self.cuisine['western'], self.place['street'], self.calories['high'], self.price_range['cheap']])
        rule62 = ctrl.Rule(self.time['very short'] & self.health['diet'], [self.meal_type['snack'], self.cuisine['drinks'], self.place['street'], self.calories['low'], self.price_range['cheap']])
        rule63 = ctrl.Rule(self.time['very short'] & self.budget['expensive'], [self.meal_type['fast food'], self.cuisine['western'], self.place['restaurant'],self.calories['high'], self.price_range['expensive']])
        rule64 = ctrl.Rule(self.time['very short'] & self.hunger['light'], [self.meal_type['snack'], self.cuisine['vietnamese'], self.place['street'], self.calories['low'], self.price_range['cheap']])
        # Weather(rainy) + Budget
        rule65 = ctrl.Rule(self.weather['rainy'] & self.time['medium'], [self.meal_type['full meal'], self.cuisine['korean'], self.place['restaurant'],self.calories['high'],  self.price_range['moderate']])
        rule66 = ctrl.Rule(self.weather['rainy'] & self.budget['expensive'], [self.meal_type['full meal'], self.cuisine['chinese'], self.place['restaurant'], self.price_range['expensive'], self.calories['high']])
        rule67 = ctrl.Rule(self.hunger['starving'] & self.health['diet'], [self.meal_type['healthy meal'], self.cuisine['temple meal'], self.calories['low'], self.place['restaurant'],self.price_range['moderate']])
        rule68 = ctrl.Rule(self.time['long'] & self.budget['cheap'], [self.meal_type['snack'], self.cuisine['drinks'], self.place['street'],  self.calories['low'], self.price_range['cheap']]) 

        self.sim_ctrl = ctrl.ControlSystem([
            rule1, rule2, rule3, rule4, rule5, rule6, rule7, rule8, rule9, rule10,
            rule11, rule12, rule13, rule14, rule15, rule16, rule17, rule18, rule19, rule20,
            rule21, rule22, rule23, rule24, rule25, rule26, rule27, rule28, rule29, rule30,
            rule31, rule32, rule33, rule34, rule35, rule36, rule37, rule38, rule39, rule40,
            rule41, rule42, rule43, rule44, rule45, rule46, rule47, rule48, rule49, rule50,
            rule51, rule52, rule53, rule54, rule55, rule56, rule57, rule58, rule59, rule60,
            rule61, rule62, rule63, rule64, rule65, rule66, rule67, rule68
        ])
        self.sim = ctrl.ControlSystemSimulation(self.sim_ctrl)

    def recommend(self, hunger_ran, budget_ran, time_ran, weather_ran, health_ran):
        self.sim.input['hunger'] = hunger_ran
        self.sim.input['budget'] = budget_ran
        self.sim.input['time'] = time_ran
        self.sim.input['weather'] = weather_ran
        self.sim.input['health'] = health_ran
        self.sim.compute()
        return self.sim.output
