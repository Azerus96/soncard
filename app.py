# app.py
from flask import Flask, render_template, jsonify, session
from datetime import datetime
import random

app = Flask(__name__)
app.secret_key = 'your_secret_key'  # Добавляем для работы с session

class Deck:
    def __init__(self):
        suits = ['♥', '♦', '♣', '♠']
        ranks = ['2', '3', '4', '5', '6', '7', '8', '9', '10', 'J', 'Q', 'K', 'A']
        self.cards = [{'suit': suit, 'rank': rank} for suit in suits for rank in ranks]
        self.used_cards = []
        random.shuffle(self.cards)
    
    def draw(self, count):
        if len(self.cards) < count:
            return []
        drawn_cards = [self.cards.pop() for _ in range(count)]
        self.used_cards.extend(drawn_cards)
        return drawn_cards

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/start')
def start_game():
    deck = Deck()
    session['used_cards'] = []
    initial_cards = deck.draw(5)
    session['used_cards'] = [f"{card['rank']}{card['suit']}" for card in initial_cards]
    return jsonify({'cards': initial_cards})

@app.route('/draw')
def draw_cards():
    deck = Deck()
    # Удаляем использованные карты из колоды
    used_cards = session.get('used_cards', [])
    deck.cards = [card for card in deck.cards if f"{card['rank']}{card['suit']}" not in used_cards]
    
    next_cards = deck.draw(3)
    session['used_cards'].extend([f"{card['rank']}{card['suit']}" for card in next_cards])
    return jsonify({'cards': next_cards})

if __name__ == '__main__':
    app.run(debug=True)
