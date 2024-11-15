import streamlit as st
import pandas as pd
import hashlib
import time
import random

# Set page configuration
st.set_page_config(page_title="Online Gaming System", page_icon="🎮", layout="wide")

# Mock Data for Users (Username and Password Hash)
users_db = {
    "admin": hashlib.sha256("admin123".encode()).hexdigest(),
    "user1": hashlib.sha256("password1".encode()).hexdigest(),
    "player1": hashlib.sha256("gamer123".encode()).hexdigest()
}

# Function to check if the entered password matches the stored password hash
def check_password(username, password):
    if username in users_db:
        stored_password_hash = users_db[username]
        return stored_password_hash == hashlib.sha256(password.encode()).hexdigest()
    return False

# Function to hash a new password and add it to the user database
def register_user(username, password):
    if username not in users_db:
        users_db[username] = hashlib.sha256(password.encode()).hexdigest()
        return True
    return False

# Mock Data for Demonstration (Expanded player data)
player_data = {
    "Player": ["Alice", "Bob", "Charlie", "David", "Eve", "Frank", "Grace", "Hannah", "Ivy", "Jack"],
    "Games Played": [120, 85, 140, 60, 200, 180, 90, 145, 170, 110],
    "Wins": [70, 45, 100, 30, 150, 120, 50, 90, 110, 60],
    "Losses": [50, 40, 40, 30, 50, 50, 40, 55, 60, 50],
    "Rank": ["Gold", "Silver", "Platinum", "Bronze", "Platinum", "Gold", "Silver", "Gold", "Platinum", "Silver"],
    "Balance (INR)": [5000, 3000, 10000, 2000, 8000, 15000, 3000, 7000, 1000, 4000]  # Balance in INR
}

player_df = pd.DataFrame(player_data)

# Expanded Game Data (Including new games)
game_data = {
    "Game": [
        "BattleZone", "EpicQuest", "PixelWarriors", "SpaceRaiders",
        "DragonSlayer", "ZombieHunt", "SkyFighter", "DungeonCrawler"
    ],
    "Players Online": [random.randint(10, 100) for _ in range(8)],
    "Status": [
        "Available", "Available", "Maintenance", "Available",
        "Available", "Maintenance", "Available", "Available"
    ]
}

game_df = pd.DataFrame(game_data)

# Expanded Shop Items
shop_items = {
    "Item": ["Sword", "Shield", "Health Potion", "Magic Wand", "Armor", "Mana Potion", "Boots", "Ring of Strength"],
    "Price (INR)": [1000, 1500, 500, 2000, 2500, 800, 1200, 3000]  # Prices in INR
}

shop_df = pd.DataFrame(shop_items)

# Placeholder for session state to simulate user login
if 'authenticated' not in st.session_state:
    st.session_state.authenticated = False
    st.session_state.username = None

# Sidebar for Navigation
st.sidebar.title("Navigation")
page = st.sidebar.radio("Go to", ["Home", "Game Library", "Player Dashboard", "In-Game Shop", "Leaderboards", "Support"])

# User Login / Signup
if not st.session_state.authenticated:
    auth_option = st.sidebar.radio("Choose an option", ["Login", "Signup"])
    
    # Login form
    if auth_option == "Login":
        st.sidebar.subheader("Login")
        username = st.sidebar.text_input("Username")
        password = st.sidebar.text_input("Password", type="password")
        
        if st.sidebar.button("Login"):
            with st.spinner("Authenticating..."):
                # Check credentials
                if check_password(username, password):
                    st.session_state.authenticated = True
                    st.session_state.username = username
                    st.sidebar.success(f"Welcome back, {username}!")
                else:
                    st.sidebar.error("Invalid username or password.")
    
    # Signup form
    elif auth_option == "Signup":
        st.sidebar.subheader("Signup")
        new_username = st.sidebar.text_input("New Username")
        new_password = st.sidebar.text_input("New Password", type="password")
        confirm_password = st.sidebar.text_input("Confirm Password", type="password")
        
        if st.sidebar.button("Sign Up"):
            if new_password != confirm_password:
                st.sidebar.error("Passwords do not match.")
            elif register_user(new_username, new_password):
                st.session_state.authenticated = True
                st.session_state.username = new_username
                st.sidebar.success(f"Account created successfully! Welcome, {new_username}!")
            else:
                st.sidebar.error("Username already exists. Please choose another.")

else:
    st.sidebar.success(f"You are logged in as {st.session_state.username}!")
    st.sidebar.button("Logout", on_click=lambda: st.session_state.update(authenticated=False, username=None))

    # Show logged-in username on the top left
    st.markdown(
        f"<h3 style='color: #2e2e2e; text-align: left;'>{st.session_state.username}</h3>", 
        unsafe_allow_html=True
    )

# Home Page
if page == "Home":
    st.title("🎮 Welcome to the Online Gaming System")
    st.subheader("Your portal to an exciting world of online gaming")
    st.image("https://source.unsplash.com/1600x900/?gaming", caption="Ready to Play?", use_column_width=True)

# Game Library Page
elif page == "Game Library":
    st.title("🎮 Game Library")
    st.write("Explore and play a variety of games available on our platform.")
    st.dataframe(game_df)

    selected_game = st.selectbox("Choose a game to play", game_df["Game"])
    game_status = game_df[game_df["Game"] == selected_game]["Status"].iloc[0]
    if game_status == "Available":
        if st.button("Play Now"):
            st.success(f"Launching {selected_game}...")
            st.balloons()
    else:
        st.warning(f"{selected_game} is currently under maintenance.")

# Player Dashboard
elif page == "Player Dashboard":
    st.title("📊 Player Dashboard")
    st.subheader("View your game stats and performance")
    st.dataframe(player_df)

    # Player Profile Management
    selected_player = st.selectbox("Select Player", player_df["Player"])
    player_stats = player_df[player_df["Player"] == selected_player].iloc[0]

    st.metric("Games Played", player_stats["Games Played"])
    st.metric("Wins", player_stats["Wins"])
    st.metric("Losses", player_stats["Losses"])
    st.metric("Rank", player_stats["Rank"])
    st.metric("Account Balance (INR)", f"₹{player_stats['Balance (INR)']}")

# In-Game Shop (Updated with more items)
elif page == "In-Game Shop":
    st.title("🛒 In-Game Shop")
    st.subheader("Purchase items and boost your gaming experience")

    # Display the shop items
    st.dataframe(shop_df)

    selected_item = st.selectbox("Choose an item to buy", shop_df["Item"])
    item_price = shop_df[shop_df["Item"] == selected_item]["Price (INR)"].iloc[0]

    # Confirm purchase
    if st.button(f"Buy {selected_item} for ₹{item_price}"):
        # Deduct from the selected player's balance
        player_df.loc[player_df['Player'] == st.session_state.username, 'Balance (INR)'] -= item_price
        st.success(f"{selected_item} purchased successfully! ₹{item_price} deducted from your balance.")

# Leaderboards
elif page == "Leaderboards":
    st.title("🏆 Leaderboards")
    st.subheader("Top players on the platform")
    sorted_df = player_df.sort_values(by="Wins", ascending=False)
    st.dataframe(sorted_df)

# Support Page
elif page == "Support":
    st.title("🛠️ Support")
    st.write("Need help? Reach out to us!")

    # Contact Form
    with st.form("support_form"):
        user_email = st.text_input("Email")
        query = st.text_area("Describe your issue")
        submitted = st.form_submit_button("Submit")

        if submitted:
            st.success("Thank you for reaching out! We'll get back to you soon.")

# Footer
st.sidebar.markdown("---")
st.sidebar.write("© 2024 Online Gaming System")
