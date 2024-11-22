from flask import Flask, render_template, jsonify, session, request
import random
import os

app = Flask(__name__)
app.secret_key = os.urandom(24)

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
    if 'game_state' not in session:
        session['game_state'] = {
            'hand': [],
            'table': {
                'top': [''] * 3,
                'middle': [''] * 5,
                'bottom': [''] * 5
            },
            'used_cards': [],
            'draw_count': 0,
            'initial_cards_placed': False
        }
    return render_template('index.html', game_state=session['game_state'])

@app.route('/start')
def start_game():
    deck = Deck()
    initial_cards = deck.cards[:5]
    session['game_state'] = {
        'hand': initial_cards,
        'table': {
            'top': [''] * 3,
            'middle': [''] * 5,
            'bottom': [''] * 5
        },
        'used_cards': [f"{card['rank']}{card['suit']}" for card in initial_cards],
        'draw_count': 0,
        'initial_cards_placed': False
    }
    return jsonify({'cards': initial_cards})

@app.route('/draw')
def draw_cards():
    game_state = session['game_state']
    if not game_state['initial_cards_placed']:
        return jsonify({'cards': [], 'error': 'Сначала распределите начальные карты!'})
    if game_state['draw_count'] >= 4:
        return jsonify({'cards': [], 'error': 'Больше карт взять нельзя!'})
    
    deck = Deck()
    used_cards = game_state['used_cards']
    available_cards = [card for card in deck.cards if f"{card['rank']}{card['suit']}" not in used_cards]
    
    next_cards = available_cards[:3]
    game_state['hand'].extend(next_cards)
    game_state['used_cards'].extend([f"{card['rank']}{card['suit']}" for card in next_cards])
    game_state['draw_count'] += 1
    session['game_state'] = game_state
    
    return jsonify({'cards': next_cards})

@app.route('/update_state', methods=['POST'])
def update_state():
    game_state = request.json
    session['game_state'] = game_state
    return jsonify({'status': 'success'})

if __name__ == '__main__':
    app.run(debug=True)
