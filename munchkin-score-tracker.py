import streamlit as st
import random
import math

st.set_page_config(page_title="Munchkin Score Tracker", page_icon="🃏", layout="wide")

st.title("🃏 Munchkin - Score Tracker")

# Initialize session state
if "players" not in st.session_state:
    st.session_state.players = {}

# Functions to update levels and bonuses
def lvl_up(player):
    st.session_state.players[player]["level"] += 1

def lvl_down(player):
    if st.session_state.players[player]["level"] > 1:
        st.session_state.players[player]["level"] -= 1

def bonus_up(player):
    st.session_state.players[player]["bonus"] += 1

def bonus_down(player):
    if st.session_state.players[player]["bonus"] > 0:
        st.session_state.players[player]["bonus"] -= 1

def remove_player(player):
    if player in st.session_state.players:
        del st.session_state.players[player]

# Sidebar with virtual dice and reset
st.sidebar.header("🎲 Virtual Dice & Controls")

# Instructions in sidebar
st.sidebar.markdown("""
### How to Use This App:
1. **Add Players:** Enter each player's name, select gender, and click `Add`.
2. **Adjust Levels:** Use `+Lvl` or `-Lvl` to increase or decrease the player's level.
3. **Adjust Bonuses:** Use `+Bns` or `-Bns` to increase or decrease bonus points by 1.
4. **Remove Player:** Click ❌ to remove a player.
5. **Virtual Dice:** Use the dice below to roll a d6.
6. **Winning:** First player to reach level 10 wins!
""")

# Virtual dice
dice_faces = ["⚀", "⚁", "⚂", "⚃", "⚄", "⚅"]
if st.sidebar.button("Roll d6"):
    roll = random.randint(1, 6)
    st.sidebar.markdown(f"<h1 style='font-size:80px; text-align:center;'>{dice_faces[roll-1]}</h1>", unsafe_allow_html=True)
    st.sidebar.success(f"You rolled a {roll}!")

# Reset button
if st.sidebar.button("🔄 Reset Game"):
    st.session_state.players = {}

# Add a new player with gender selection
with st.form("add_player"):
    new_player = st.text_input("Player Name")
    gender = st.radio("Gender", ["♂ Male", "♀ Female"])
    if st.form_submit_button("Add") and new_player:
        if new_player not in st.session_state.players:
            st.session_state.players[new_player] = {
                "level": 1,
                "bonus": 0,
                "gender": gender
            }

# Display players as cards (max 2 per row)
if st.session_state.players:
    st.subheader("Players")

    players_list = list(st.session_state.players.items())
    rows = math.ceil(len(players_list) / 2)

    for r in range(rows):
        row_players = players_list[r*2:(r+1)*2]
        cols = st.columns(len(row_players))

        for (player, stats), col in zip(row_players, cols):
            with col:
                st.markdown(
                    f"""
                    <div style="border:2px solid #444; border-radius:15px; padding:20px; margin-bottom:15px; background-color:#f9f9f9; text-align:center; min-height:125px; display:flex; flex-direction:column; justify-content:space-between;">
                        <div>
                            <h3 style="margin:0;">{stats['gender']} {player}</h3>
                            <p><b>Level:</b> {stats['level']} | <b>Bonus:</b> {stats['bonus']} | <b>Total:</b> {stats['level'] + stats['bonus']}</p>
                        </div>
                    </div>
                    """,
                    unsafe_allow_html=True
                )

                # Buttons on the same row
                bcol1, bcol2, bcol3, bcol4, bcol5 = st.columns(5)
                with bcol1:
                    st.button("+Lvl", key=f"lvl_up_{player}", on_click=lvl_up, args=(player,))
                with bcol2:
                    st.button("-Lvl", key=f"lvl_down_{player}", on_click=lvl_down, args=(player,))
                with bcol3:
                    st.button("+Bns", key=f"bonus_up_{player}", on_click=bonus_up, args=(player,))
                with bcol4:
                    st.button("-Bns", key=f"bonus_down_{player}", on_click=bonus_down, args=(player,))
                with bcol5:
                    st.button("❌", key=f"remove_{player}", on_click=remove_player, args=(player,))

                if stats["level"] >= 10:
                    st.success(f"🎉 {player} reached level 10 and wins!")
