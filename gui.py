import tkinter as tk
from tkinter import messagebox
from configparser import ConfigParser
import requests

aa = 'https://api.openweathermap.org/data/2.5/weather?q={}&lang=pt_br&appid={}'

config_file = 'config.ini'
config = ConfigParser()
config.read(config_file)
api_key = config['api_key']['key']

def get_weather(city):
    result = requests.get(aa.format(city, api_key))
    if result.status_code == 200:
        json_data = result.json()
        cidade = json_data['name']
        pais = json_data['sys']['country']
        temp_klv = json_data['main']['temp']
        temp_celsius = temp_klv - 273.15
        clima = json_data['weather'][0]['description']
        return cidade, pais, temp_celsius, clima
    else:
        return None

def busca(event=None):  # Agora aceita um argumento de evento (event)
    cidade = cidade_txt.get()
    clima = get_weather(cidade)
    if clima:
        local.config(text=f'Local: {clima[0]}, {clima[1]}')
        temp.config(text=f'Temperatura: {clima[2]:.2f}°C')
        desc.config(text=f'Descrição: {clima[3].capitalize()}')
    else:
        messagebox.showerror('Erro', 'Não foi possível encontrar informações para a cidade.')

window = tk.Tk()
window.title('teste')
window.geometry('600x400')

cidade_txt = tk.StringVar()
cidade_busca = tk.Entry(window, textvariable=cidade_txt)
cidade_busca.pack()

# Vincular a função de busca ao evento <Return> (Enter) na Entry
cidade_busca.bind('<Return>', busca)

botao_busca = tk.Button(window, text='Buscar', width=12, command=busca)
botao_busca.pack()

local = tk.Label(window, text='Local', font=('bold', 20))
local.pack()

temp = tk.Label(window, text='Temperatura')
temp.pack()

desc = tk.Label(window, text='Descrição')
desc.pack()

window.mainloop()