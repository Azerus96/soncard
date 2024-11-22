# app.py
from flask import Flask, render_template, jsonify
import random

app = Flask(__name__)

class Deck:
    def __init__(self):
        suits = ['hearts', 'diamonds', 'clubs', 'spades']
        ranks = ['2', '3', '4', '5', '6', '7', '8', '9', '10', 'J', 'Q', 'K', 'A']
        self.cards = [{'suit': suit, 'rank': rank} for suit in suits for rank in ranks]
        random.shuffle(self.cards)
    
    def draw(self, count):
        if len(self.cards) < count:
            return []
        return [self.cards.pop() for _ in range(count)]

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/start')
def start_game():
    deck = Deck()
    initial_cards = deck.draw(5)
    return jsonify({'cards': initial_cards})

@app.route('/draw')
def draw_cards():
    deck = Deck()
    next_cards = deck.draw(3)
    return jsonify({'cards': next_cards})

if __name__ == '__main__':
    app.run(debug=True)
