import random

# Константы для слот-машины
SYMBOLS = ['значение1', 'значение2', 'значение3', 'значение4', 'значение5',
           'значение6', 'значение7', 'значение8']
WILD = 'WL'  # Символ Wild
FREE_SPIN = 'FS'  # Символ Free Spins
REEL_LENGTH = 200  # Длина ленты барабана
SPINS_COUNT = 1000000  # Количество спинов для симуляции
PAYLINES = [
    [0, 3, 6],  # Top horizontal line
    [1, 4, 7],  # Middle horizontal line
    [2, 5, 8],  # Bottom horizontal line
    [0, 4, 8],  # Top-left to bottom-right diagonal
    [2, 4, 6]  # Top-right to bottom-left diagonal
]
BET_PER_LINE = 1  # Ставка на линию
FREE_SPINS_COUNT = 10  # Количество фриспинов за сочетание символов Free Spin

# Генерация барабанов
reels = [
    [symbol for symbol in SYMBOLS for _ in range(REEL_LENGTH // (len(SYMBOLS) + 2))] +
    [WILD] * (REEL_LENGTH // (len(SYMBOLS) + 2)) +
    [FREE_SPIN] * (REEL_LENGTH // (len(SYMBOLS) + 2))
    for _ in range(3)
]


# Функция для создания и расширения таблицы выплат с учетом Wild символов
def create_payouts(base_payouts):
    payouts = {}
    for symbol in SYMBOLS + [WILD]:
        payouts[symbol * 3] = base_payouts.get(symbol, 0)
    for symbol in SYMBOLS:
        payouts[symbol * 2 + WILD] = base_payouts.get(symbol, 0)
        payouts[WILD + symbol * 2] = base_payouts.get(symbol, 0)
        payouts[symbol + WILD * 2] = base_payouts.get(symbol, 0)
    payouts[WILD * 3] = max(base_payouts.values())  # Максимальная выплата за три Wild
    return payouts


# Таблица выплат
payouts = create_payouts({
    'значение1': 6,
    'значение2': 11,
    'значение3': 17,
    'значение4': 23,
    'значение5': 29,
    'значение6': 35,
    'значение7': 41,
    'значение8': 47,
    WILD: 55
})


# Функция для симуляции одного спина
def simulate_spin(reels, paylines, payouts, wild_symbol, free_spin_symbol, is_free_spin=False):
    reel_positions = [random.randint(0, REEL_LENGTH - 1) for _ in reels]
    spins = []
    for payline in paylines:
        spin_symbols = [reels[i][(position + reel_positions[i]) % REEL_LENGTH] for i, position in enumerate(payline)]
        spins.append(''.join(spin_symbols))

    total_payout = sum(payouts.get(spin, 0) for spin in spins)
    free_spins = 0
    if not is_free_spin:
        free_spins = spins.count(free_spin_symbol * 3) * FREE_SPINS_COUNT

    return total_payout, free_spins


# Проведение симуляции слот-машины
total_payout = 0
total_free_spins_awarded = 0
for _ in range(SPINS_COUNT):
    payout, free_spins = simulate_spin(reels, PAYLINES, payouts, WILD, FREE_SPIN)
    total_payout += payout
    total_free_spins_awarded += free_spins

    while free_spins > 0:
        payout, _ = simulate_spin(reels, PAYLINES, payouts, WILD, FREE_SPIN, is_free_spin=True)
        total_payout += payout
        free_spins -= 1

# Результаты симуляции
average_payout_percentage = (total_payout / (SPINS_COUNT * BET_PER_LINE * len(PAYLINES))) * 100
average_free_spin_frequency = total_free_spins_awarded / SPINS_COUNT

# Вывод результатов
print("Средний процент выплат:", average_payout_percentage)
print("Частота фриспинов:", average_free_spin_frequency)
