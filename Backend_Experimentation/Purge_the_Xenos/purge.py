import sqlite3, hashlib, os#, PyQt4
CODE = "1f3ee6bb8c39241cad74b6060f54d63a3cadf654cd179988bc84b0d397e8a9f90561d16b102ef30a39563e4a298f0d3b636c6c4d8e2f540f898fdfad98f6c79e"
DB_NAME = "Frontend/public/static/db/cloud_save.db" #Serverside database directory
PREVIEW_DIR = "Frontend/public/static/song_previews/"#Preview folder (in static)
PREVIEW_KEEP = ("dummy.wav", "song_previews")       #Files in preview folder to keep
OUTFILE_WAVS = "Frontend/wav_outfiles/"              #Audio Outfile directory
WAV_KEEP = ("wav_outfiles",)                         #Files in audio out folder to keep
OUTFILE_DBS = "Frontend/database_outfiles/"          #Database Outfile directory
DBS_KEEP = ("database_outfiles",)                    #Files in db out folder to keep
#pw = input("Enter purge password: ").encode('utf-8')

def check_password(password):
    """ Checks the password from the user """
    user_pw = password.encode('utf-8')
    hashed_pw = hashlib.sha512(user_pw).hexdigest()
    if hashed_pw == CODE:
        return True
    else:
        return False
    
def clear_serverside():
    """ Deletes all data in the serverside database """
    db = sqlite3.connect("{}".format(DB_NAME))
    cursor = db.cursor()
    cursor.execute('''DELETE FROM users;''')
    db.commit()
    cursor.execute('''DELETE FROM songs;''')
    db.commit()
    cursor.close()
    db.close()

def clear_previews():
    """ Deletes all preview files """
    files = os.listdir(PREVIEW_DIR)
    for keep in PREVIEW_KEEP:
        files.remove(keep)
    for file in files:
        os.remove("{}{}".fromat(PREVIEW_DIR, file))
        
def clear_audio_out():
    """ Deletes all preview files """
    files = os.listdir(OUTFILE_WAVS)
    for keep in WAV_KEEP:
        files.remove(keep)
    for file in files:
        os.remove("{}{}".fromat(OUTFILE_WAVS, file))
        
def clear_database_out():
    """ Deletes all cowbell database files """
    files = os.listdir(OUTFILE_DBS)
    for keep in DBS_KEEP:
        files.remove(keep)
    for file in files:
        os.remove("{}{}".fromat(OUTFILE_DBS, file))