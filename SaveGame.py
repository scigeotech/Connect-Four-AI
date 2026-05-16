import pickle
import os
from datetime import datetime

#default data directory
DATA_DIR = "game_data"

def structure_save(game_records, record_timeline, player_algorithm, ai_algorithm, player_avg_time_ms, ai_avg_time_ms):
    return {
        "game_records": game_records,
        "record_timeline": record_timeline,
        "player_algorithm": player_algorithm,
        "ai_algorithm": ai_algorithm,
        "player_avg_time_ms": player_avg_time_ms,
        "ai_avg_time_ms": ai_avg_time_ms
    }

def guarantee_data_dir(): #create data directory if none
    if not os.path.exists(DATA_DIR):
        os.makedirs(DATA_DIR)

def save_game(game_data, file_name=None):
    #game_data: structure containing game information
    #    game_records: list of column moves
    #    record_timeline: str ("player_win", "ai_win", "draw")
    #    player_algorithm: str name of player algorithm
    #    ai_algorithm: str name of AI algorithm
    #    player_avg_time_ms: float average decision time for player
    #    ai_avg_time_ms: float average decision time for AI
    #    file_name: optional custom filename (without extension)
    guarantee_data_dir()
    
    if file_name is None:
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        file_name = f"game_{timestamp}.pkl"
    else:
        if not file_name.endswith('.pkl'):
            file_name += '.pkl'
    
    file_path = os.path.join(DATA_DIR, file_name)
    with open(file_path, 'wb') as f:
        pickle.dump(game_data, f)
    
    print(f"[SAVED] Game saved to {file_path}")
    return file_path #return path to file

def load_game(file_name): #load single game
    if not file_name.endswith('.pkl'):
        file_name += '.pkl'
    
    if file_name.startswith(DATA_DIR):
        file_path = file_name
    else:
        file_path = os.path.join(DATA_DIR, file_name)
    if not os.path.exists(file_path):
        print(f"File not found: {file_path}")
        return None
    
    with open(file_path, 'rb') as f:
        game_data = pickle.load(f)
    
    print(f"[LOADED] Game loaded from {file_path}")
    return game_data #return game data struct

def save_multiple_games(games_list, file_name=None): #probably not useful
    guarantee_data_dir()
    
    if file_name is None:
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        file_name = f"games_multiple_{timestamp}.pkl"
    else:
        if not file_name.endswith('.pkl'):
            file_name += '.pkl'
    
    file_path = os.path.join(DATA_DIR, file_name)
    with open(file_path, 'wb') as f:
        pickle.dump(games_list, f)
    
    print(f"[SAVED] {len(games_list)} games saved to {file_path}")
    return file_path #returns path to saved file

def load_multiple_games(file_name):
    if not file_name.endswith('.pkl'):
        file_name += '.pkl'
    
    if file_name.startswith(DATA_DIR):
        file_path = file_name
    else:
        file_path = os.path.join(DATA_DIR, file_name)
    if not os.path.exists(file_path):
        print(f"File not found: {file_path}")
        return []
    
    with open(file_path, 'rb') as f:
        games_list = pickle.load(f)
    
    print(f"[LOADED] {len(games_list)} games loaded from {file_path}")
    return games_list #return list of game data dictionaries

def list_saved_games():
    guarantee_data_dir()
    
    files = [f for f in os.listdir(DATA_DIR) if f.endswith('.pkl')]
    if not files:
        print("No saved games found.")
        return []
    
    print(f"Found {len(files)} saved game file(s)!: ")
    for f in sorted(files):
        file_path = os.path.join(DATA_DIR, f)
        size_kb = os.path.getsize(file_path) / 1024
        print(f"  -> {f} ({size_kb:.2f} KB)")
    
    return files