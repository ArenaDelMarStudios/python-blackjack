import tkinter as tk
import random
import os
import sys
from PIL import Image, ImageTk

# --- Dynamic Path Helper for PyInstaller ---
def get_resource_path(relative_path):
    try:
        base_path = sys._MEIPASS
    except AttributeError:
        base_path = os.path.abspath(".")
    return os.path.join(base_path, relative_path)

# --- Core Game Logic ---
def create_deck():
    ranks = ['2', '3', '4', '5', '6', '7', '8', '9', '10', 'J', 'Q', 'K', 'A']
    suits = ['♥', '♦', '♣', '♠']
    return [(r, s) for r in ranks for s in suits]

def card_value(card):
    rank = card[0]
    if rank in ['J', 'Q', 'K']:
        return 10
    elif rank == 'A':
        return 11
    else:
        return int(rank)

def hand_value(hand):
    total = sum(card_value(c) for c in hand)
    aces = sum(1 for c in hand if c[0] == 'A')
    while total > 21 and aces:
        total -= 10
        aces -= 1
    return total

class BlackjackApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Casino Blackjack")
        
        # --- Screen Centering Calculations ---
        window_width = 700
        window_height = 750
        
        screen_width = self.root.winfo_screenwidth()
        screen_height = self.root.winfo_screenheight()
        
        start_x = int((screen_width / 2) - (window_width / 2))
        start_y = int((screen_height / 2) - (window_height / 2))
        
        # Set a reasonable starting window size centered on screen
        self.root.geometry(f"{window_width}x{window_height}+{start_x}+{start_y}")
        self.root.resizable(False, False)

        # --- Theme & Style Preferences ---
        self.table_bg = "#1E5631"        # Classic Green
        self.container_bg = "#1C4E2D"    # Shaded Green
        self.card_back_color = "red"     # Default card back ('red' or 'blue')

        self.root.configure(bg=self.table_bg)

        self.deck = []
        self.player_hand = []
        self.dealer_hand = []
        
        self.player_photo_images = []
        self.dealer_photo_images = []

        self.create_menu()
        self.create_widgets()
        
        self.root.bind("<Configure>", self.on_window_resize)
        self.new_game()
        
    def create_menu(self):
        # Top Menu Bar
        menubar = tk.Menu(self.root)
        self.root.config(menu=menubar)

        # Table Theme Dropdown
        theme_menu = tk.Menu(menubar, tearoff=0)
        menubar.add_cascade(label="Table Felt", menu=theme_menu)
        theme_menu.add_command(label="Classic Green", command=lambda: self.change_table_theme("#1E5631", "#1C4E2D"))
        theme_menu.add_command(label="Royal Blue", command=lambda: self.change_table_theme("#1A365D", "#122540"))
        theme_menu.add_command(label="High-Roller Red", command=lambda: self.change_table_theme("#722F37", "#5C2028"))
        theme_menu.add_command(label="Midnight Charcoal", command=lambda: self.change_table_theme("#2B2B2B", "#1F1F1F"))

        # Card Back Dropdown
        back_menu = tk.Menu(menubar, tearoff=0)
        menubar.add_cascade(label="Card Back", menu=back_menu)
        back_menu.add_command(label="Red Back", command=lambda: self.change_card_back("red"))
        back_menu.add_command(label="Blue Back", command=lambda: self.change_card_back("blue"))

    def create_widgets(self):
        # Outer master frame holding the felt table
        self.table_frame = tk.Frame(self.root, bg=self.table_bg)
        self.table_frame.pack(fill='both', expand=True, padx=20, pady=10)

        # Dealer Area
        self.dealer_container = tk.LabelFrame(
            self.table_frame, text="DEALER", font=('Arial', 12, 'bold'),
            fg="white", bg=self.container_bg, bd=2, labelanchor="n"
        )
        self.dealer_container.pack(fill='both', expand=True, pady=10)
        
        self.dealer_cards_frame = tk.Frame(self.dealer_container, bg=self.container_bg)
        self.dealer_cards_frame.pack(expand=True)
        self.dealer_value_lbl = tk.Label(self.dealer_container, text="Value: 0", font=('Arial', 12, 'bold'), fg="#D4AF37", bg=self.container_bg)
        self.dealer_value_lbl.pack(pady=5)

        # Player Area
        self.player_container = tk.LabelFrame(
            self.table_frame, text="PLAYER", font=('Arial', 12, 'bold'),
            fg="white", bg=self.container_bg, bd=2, labelanchor="n"
        )
        self.player_container.pack(fill='both', expand=True, pady=10)
        
        self.player_cards_frame = tk.Frame(self.player_container, bg=self.container_bg)
        self.player_cards_frame.pack(expand=True)
        self.player_value_lbl = tk.Label(self.player_container, text="Value: 0", font=('Arial', 12, 'bold'), fg="#D4AF37", bg=self.container_bg)
        self.player_value_lbl.pack(pady=5)

        # Control Panel & Information Bar
        self.info_lbl = tk.Label(self.root, text="", font=('Arial', 16, 'bold'), fg="#FFD700", bg=self.table_bg)
        self.info_lbl.pack(pady=5)

        self.control_frame = tk.Frame(self.root, bg=self.table_bg)
        self.control_frame.pack(pady=15)

        self.hit_btn = tk.Button(self.control_frame, text="HIT", width=10, font=('Arial', 11, 'bold'), bg="#8B0000", fg="white", activebackground="#A30000", activeforeground="white", command=self.hit)
        self.hit_btn.pack(side='left', padx=10)

        self.stand_btn = tk.Button(self.control_frame, text="STAND", width=10, font=('Arial', 11, 'bold'), bg="#124E73", fg="white", activebackground="#1A6B9E", activeforeground="white", command=self.stand)
        self.stand_btn.pack(side='left', padx=10)

        self.deal_btn = tk.Button(self.control_frame, text="DEAL", width=10, font=('Arial', 11, 'bold'), bg="#D4AF37", fg="black", activebackground="#F3C63F", activeforeground="black", command=self.new_game)
        self.deal_btn.pack(side='left', padx=10)

    # --- Customization Theme Handlers ---
    def change_table_theme(self, table_color, container_color):
        self.table_bg = table_color
        self.container_bg = container_color
        
        # Apply new colors to all existing widget elements
        self.root.configure(bg=self.table_bg)
        self.table_frame.configure(bg=self.table_bg)
        
        self.dealer_container.configure(bg=self.container_bg)
        self.dealer_cards_frame.configure(bg=self.container_bg)
        self.dealer_value_lbl.configure(bg=self.container_bg)
        
        self.player_container.configure(bg=self.container_bg)
        self.player_cards_frame.configure(bg=self.container_bg)
        self.player_value_lbl.configure(bg=self.container_bg)
        
        self.info_lbl.configure(bg=self.table_bg)
        self.control_frame.configure(bg=self.table_bg)
        
        # Redraw cards so the frame backgrounds update seamlessly
        self.update_display(reveal_dealer=(self.hit_btn['state'] == 'disabled'))

    def change_card_back(self, color_name):
        self.card_back_color = color_name
        self.update_display(reveal_dealer=(self.hit_btn['state'] == 'disabled'))

    def new_game(self):
        self.deck = create_deck()
        random.shuffle(self.deck)
        self.player_hand = [self.deck.pop(), self.deck.pop()]
        self.dealer_hand = [self.deck.pop(), self.deck.pop()]
        
        self.info_lbl.config(text="")
        self.hit_btn.config(state='normal')
        self.stand_btn.config(state='normal')
        
        self.update_display(reveal_dealer=False)

    def on_window_resize(self, event):
        if event.widget == self.root:
            self.update_display(reveal_dealer=(self.hit_btn['state'] == 'disabled'))

    def load_and_scale_card(self, rank, suit, target_height):
        aspect_ratio = 500 / 726
        target_width = int(target_height * aspect_ratio)

        # Dynamic path based on selected color back or normal rank face
        if rank == "back":
            file_path = get_resource_path(f"cards/back_{self.card_back_color}.png")
        else:
            suit_map = {'♥': 'H', '♦': 'D', '♣': 'C', '♠': 'S'}
            file_path = get_resource_path(f"cards/{rank}{suit_map[suit]}.png")

        try:
            pil_img = Image.open(file_path)
            resized_img = pil_img.resize((target_width, target_height), Image.Resampling.LANCZOS)
            return ImageTk.PhotoImage(resized_img), target_width
        except Exception as e:
            print(f"Error loading {file_path}: {e}")
            return None, target_width

    def draw_hand(self, frame, hand, max_frame_height, hidden=False):
        for widget in frame.winfo_children():
            widget.destroy()

        cards = [hand[0], ('back', 'back')] if hidden else hand
        num_cards = len(cards)
        if num_cards == 0:
            return []
        
        # Lock card size relevant to screen resolution, but allow for a range of heights to accommodate different window sizes
        target_height = max(int(max_frame_height * 0.75), 240)
        target_height = min(target_height, 320)

        photo_images = []
        loaded_cards = []

        for rank, suit in cards:
            photo_img, card_width = self.load_and_scale_card(rank, suit, target_height)
            if photo_img:
                photo_images.append(photo_img)
                loaded_cards.append((photo_img, card_width))

        if not loaded_cards:
            return []

        standard_spacing = int(card_width * 0.65)
        total_needed_width = card_width + (num_cards - 1) * standard_spacing
        max_allowed_width = frame.winfo_width() if frame.winfo_width() > 1 else 900

        if total_needed_width > max_allowed_width and num_cards > 1:
            spacing = (max_allowed_width - card_width) // (num_cards - 1)
            min_proportional_spacing = int(card_width * 0.45) # Set minimum card stacking proportionately to card width
            spacing = max(min_proportional_spacing, spacing)
        else:
            spacing = standard_spacing

        frame.configure(width=card_width + (num_cards - 1) * spacing, height=target_height)
        frame.pack_propagate(False)

        for i, (photo_img, width) in enumerate(loaded_cards):
            lbl = tk.Label(frame, image=photo_img, bg=self.container_bg, bd=0)
            lbl.place(x=i * spacing, y=0, width=width, height=target_height)

        return photo_images

    def update_display(self, reveal_dealer=False):
        dealer_container_height = self.dealer_container.winfo_height()
        player_container_height = self.player_container.winfo_height()

        self.dealer_photo_images = self.draw_hand(
            self.dealer_cards_frame, self.dealer_hand, 
            dealer_container_height, hidden=not reveal_dealer
        )
        self.player_photo_images = self.draw_hand(
            self.player_cards_frame, self.player_hand, 
            player_container_height
        )

        dealer_val = hand_value(self.dealer_hand) if reveal_dealer else card_value(self.dealer_hand[0])
        self.dealer_value_lbl.config(text=f"Value: {dealer_val}")
        self.player_value_lbl.config(text=f"Value: {hand_value(self.player_hand)}")

    def hit(self):
        self.player_hand.append(self.deck.pop())
        player_val = hand_value(self.player_hand)
        self.update_display(reveal_dealer=False)
        
        if player_val > 21:
            self.info_lbl.config(text="💥 Bust! You lose.", fg="#FF5C5C")
            self.end_hand()

    def stand(self):
        self.hit_btn.config(state='disabled')
        self.stand_btn.config(state='disabled')
        while hand_value(self.dealer_hand) < 17:
            self.dealer_hand.append(self.deck.pop())
        self.update_display(reveal_dealer=True)
        self.determine_winner()

    def determine_winner(self):
        player_val = hand_value(self.player_hand)
        dealer_val = hand_value(self.dealer_hand)
        
        if dealer_val > 21:
            self.info_lbl.config(text="🎈 Dealer busts! You win!", fg="#2ECC71")
        elif player_val > dealer_val:
            self.info_lbl.config(text="🏆 You win!", fg="#2ECC71")
        elif player_val < dealer_val:
            self.info_lbl.config(text="😢 Dealer wins.", fg="#FF5C5C")
        else:
            self.info_lbl.config(text="🤝 Push (tie).", fg="#EAECEE")
        self.end_hand()

    def end_hand(self):
        self.hit_btn.config(state='disabled')
        self.stand_btn.config(state='disabled')
        self.update_display(reveal_dealer=True)

if __name__ == "__main__":
    root = tk.Tk()
    app = BlackjackApp(root)
    root.mainloop()