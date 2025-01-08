import numpy as np
import skfuzzy as fuzz
from skfuzzy import control as ctrl

# Define fuzzy variables
suhu = ctrl.Antecedent(np.arange(16, 36, 1), 'suhu')  # Suhu: 16°C - 35°C
kelembapan = ctrl.Antecedent(np.arange(20, 81, 1), 'kelembapan')  # Kelembapan: 20% - 80%
kecepatan_kipas = ctrl.Consequent(np.arange(0, 101, 1), 'kecepatan_kipas')  # Kecepatan: 0% - 100%

# Membership functions for Suhu
suhu['low'] = fuzz.trapmf(suhu.universe, [16, 16, 20, 25])
suhu['medium'] = fuzz.trimf(suhu.universe, [20, 25, 30])
suhu['high'] = fuzz.trapmf(suhu.universe, [25, 30, 35, 35])

# Membership functions for Kelembapan
kelembapan['dry'] = fuzz.trapmf(kelembapan.universe, [20, 20, 35, 50])
kelembapan['normal'] = fuzz.trimf(kelembapan.universe, [35, 50, 65])
kelembapan['humid'] = fuzz.trapmf(kelembapan.universe, [50, 65, 80, 80])

# Membership functions for Kecepatan Kipas
kecepatan_kipas['slow'] = fuzz.trimf(kecepatan_kipas.universe, [0, 25, 50])
kecepatan_kipas['medium'] = fuzz.trimf(kecepatan_kipas.universe, [25, 50, 75])
kecepatan_kipas['fast'] = fuzz.trimf(kecepatan_kipas.universe, [50, 75, 100])

# Define fuzzy rules
rule1 = ctrl.Rule(suhu['low'] & kelembapan['dry'], kecepatan_kipas['slow'])
rule2 = ctrl.Rule(suhu['low'] & kelembapan['normal'], kecepatan_kipas['slow'])
rule3 = ctrl.Rule(suhu['low'] & kelembapan['humid'], kecepatan_kipas['medium'])
rule4 = ctrl.Rule(suhu['medium'] & kelembapan['dry'], kecepatan_kipas['medium'])
rule5 = ctrl.Rule(suhu['medium'] & kelembapan['normal'], kecepatan_kipas['medium'])
rule6 = ctrl.Rule(suhu['medium'] & kelembapan['humid'], kecepatan_kipas['fast'])
rule7 = ctrl.Rule(suhu['high'] & kelembapan['dry'], kecepatan_kipas['fast'])
rule8 = ctrl.Rule(suhu['high'] & kelembapan['normal'], kecepatan_kipas['fast'])
rule9 = ctrl.Rule(suhu['high'] & kelembapan['humid'], kecepatan_kipas['fast'])

# Create control system
ac_control = ctrl.ControlSystem([rule1, rule2, rule3, rule4, rule5, rule6, rule7, rule8, rule9])
ac_simulation = ctrl.ControlSystemSimulation(ac_control)

# Input values
ac_simulation.input['suhu'] = 28  # Example input for Suhu
ac_simulation.input['kelembapan'] = 45  # Example input for Kelembapan

# Compute result
ac_simulation.compute()

# Output result
print(f"Kecepatan Kipas: {ac_simulation.output['kecepatan_kipas']}%")
