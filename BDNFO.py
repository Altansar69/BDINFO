from genericpath import exists
import sys
import os
import shutil
import subprocess
import re
import configparser
from datetime import datetime

logo = """ÛÛÛÛÛÛÛÛÛÛÛÛÛÛÛÛÛÛÛÛÛÛÛÛÛÛÛÛÛÛÛÛÛÛÛÛÛÛÛÛÛÛÛÛÛÛÛÛÛÛÛÛÛÛÛÛÛÛÛÛÛÛÛÛÛÛÛÛÛÛÛÛÛÛÛÛÛÛÛÛ
ÛÛ                                                                            ÛÛ
ÛÛ    ±ÛÛÛÛÛÛÛÛÛ° ÛÛÛ± ±ÛÛÛÛÛÛÛÛÛÛ²  ±ÛÛÛ     ÛÛÛÛ  ÛÛÛÛÛÛÛÛÛÛÛÛ °ÛÛÛÛÛÛÛÛÛÛÛ ÛÛ
ÛÛ   ÛÛÛÛÛÛÛÛÛÛÛ  ÛÛÛ  ÛÛÛÛÛÛÛÛÛÛÛÛ± ÛÛÛÛ     ÛÛÛÛ  ÛÛÛÛÛÛÛÛÛÛ²  ÛÛÛÛÛÛÛÛÛÛÛÛ ÛÛ
ÛÛ  ÛÛÛÛ         ±±±°  ÛÛÛ²    ²ÛÛÛ  ÛÛÛÛ±±±±ÛÛÛÛ  ²ÛÛÛ±     °   ÛÛÛ±    ±ÛÛÛ ÛÛ
ÛÛ  ÛÛÛ±        °ÛÛÛ° ²ÛÛÛÛÛÛÛÛÛÛÛ± ²ÛÛÛÛÛÛÛÛÛÛÛÛ  ÛÛÛÛÛÛÛÛÛÛÛ± ²ÛÛÛÛÛÛÛÛÛÛÛ° ÛÛ
ÛÛ ²ÛÛÛ°        ÛÛÛÛ  ÛÛÛÛÛÛÛÛÛÛ²   ÛÛÛÛ°±±°²ÛÛÛ° ±ÛÛÛ±      °  ÛÛÛÛÛÛÛÛÛÛÛ±° ÛÛ
ÛÛ ²ÛÛÛÛÛÛÛÛÛÛ  ÛÛÛ± ²ÛÛÛ±         ²ÛÛÛ°    ÛÛÛÛ  ÛÛÛÛÛÛÛÛÛÛÛ± ²ÛÛÛ±    ÛÛÛÛ  ÛÛ
ÛÛ  ²ÛÛÛÛÛÛÛÛÛ ²ÛÛÛ  ÛÛÛÛ          ÛÛÛÛ    ±ÛÛÛ² °ÛÛÛÛÛÛÛÛÛÛÛ  ÛÛÛÛ    °ÛÛÛ²  ÛÛ
ÛÛ                                                                            ÛÛ
ÛÛÛÛÛÛÛÛÛÛÛÛÛÛÛÛÛÛÛÛÛÛÛÛÛÛÛÛÛÛÛÛÛÛÛÛÛÛÛÛÛÛÛÛÛÛÛÛÛÛÛÛÛÛÛÛÛÛÛÛÛÛÛÛÛÛÛÛÛÛÛÛÛÛÛÛÛÛÛÛ
ÛÛ                                                                            ÛÛ
ÛÛ                                                                            ÛÛ
ÛÛ                            °°±°±±±±±°°                                     ÛÛ
ÛÛ                         °°±±±°±°±°±°±±±±°                                  ÛÛ
ÛÛ                       °±±°°°°±±±±±±±°°°°°±°                                ÛÛ
ÛÛ                      °±°°°±±±°°    °°±±°°°±±°                              ÛÛ
ÛÛ                     ±±°°°±°           °±°°°±±°                             ÛÛ
ÛÛ                    °±°°°±°              ±°°°°±           °°°°°°            ÛÛ
ÛÛ                    ±°°°±°                ±°°°±°       °±±±±°°±±±±°         ÛÛ
ÛÛ                   °±°°°±°                °°°°°°     °±±°±°    °°°±±°       ÛÛ
ÛÛ                   °±°°°±                 ±°°°°°    ±±°°°°°    °°°°°±±      ÛÛ
ÛÛ                   °±°°°±                 °±°°°°   ±°°°°°°°°°°°±°°°°°±±     ÛÛ
ÛÛ                   °±°°°±                 °°°°°°  °±°°°°°°°°±°±°°°°°°°±°    ÛÛ
ÛÛ                    °°°°°                 °°°°°°  °±°°°°°°°°°°°°°°°°°°±°    ÛÛ
ÛÛ            °°±±±°°±±±±±±°°°±°±°±±±°±±±°±°±±±±±±±°°°°°°°°°°°°°°°°°°°°°±°    ÛÛ
ÛÛ         °±±±±±±±±±±±±±±±±±±±±±±±±±±±±±±±±±±±±±±±±±°°°°°°°°°°°°°°°°°°±±     ÛÛ
ÛÛ        °±±±±±±±±±±±±±±±±±±±±±±±±±±±±±±±±±±±±±±±±±±°°°°°°°°°°°°°°°°°±±      ÛÛ
ÛÛ        ±±±±±±±±±±±±±±±±±±±±±±±±±±±±±±±±±±±±±±±±±±±±°°°°°°°°°°°°°°°±°       ÛÛ
ÛÛ       °±±±±±±±±±±±±±±±±±±±±±±±±±±±±±±±±±±±±±±±±±±±±±±±°°°°°°°°°±°°         ÛÛ
ÛÛ       °±±±±±±±±±±±±±±±±±±±±±±±±°°°°°±±±±±±±±±±±±±±±±±±±±°°°°°°±°           ÛÛ
ÛÛ       °±±±±±±±±±±±±±±±±±±±°±°° °°° °°±°±±±±±±±±±±±±±±±±±°°°°°°±°           ÛÛ
ÛÛ       °±±±±±±±±±±±±±±±±±±±°°°±²ÛÛÛÛ²° °±±±±±±±±±±±±±±±±±°°°°°°±°           ÛÛ
ÛÛ       °±±±±±±±±±±±±±±±±±±±°±ÛÛÛÛÛÛÛÛÛ² °°±±±±±±±±±±±±±±±°°°°°°±°           ÛÛ
ÛÛ       °±±±±±±±±±±±±±±±±±±°°ÛÛÛÛÛÛÛÛÛÛÛ±°±±±±±±±±±±±±±±±±±°°°°°±°           ÛÛ
ÛÛ       °±±±±±±±±±±±±±±±±±±°±ÛÛÛÛÛÛÛÛÛÛÛ²°±±±±±±±±±±±±±±±±±±°°°°±°           ÛÛ
ÛÛ       °±±±±±±±±±±±±±±±±±±°°ÛÛÛÛÛÛÛÛÛÛÛ±°±±±±±±±±±±±±±±±±±°°°°°±°           ÛÛ
ÛÛ       °±±±±±±±±±±±±±±±±±±±°±ÛÛÛÛÛÛÛÛÛ² °±±±±±±±±±±±±±±±±±±°°°°±°           ÛÛ
ÛÛ       °±±±±±±±±±±±±±±±±±±±± °ÛÛÛÛÛÛÛ± °°±±±±±±±±±±±±±±±±±±°°°°±°           ÛÛ
ÛÛ       °±±±±±±±±±±±±±±±±±±±°° ÛÛÛÛÛÛÛ°°°±±±±±±±±±±±±±±±±±°°°°°°±°           ÛÛ
ÛÛ       °±±±±±±±±±±±±±±±±±±±±°°ÛÛÛÛÛÛÛ±°±±±±±±±±±±±±±±±±±±°°°°°°±°           ÛÛ
ÛÛ       °±±±±±±±±±±±±±±±±±±±±° ÛÛÛÛÛÛÛ±°°±±±±±±±±±±±±±±±±±°°°°°°±°           ÛÛ
ÛÛ       °±±±±±±±±±±±±±±±±±±±±°°ÛÛÛÛÛÛÛ±°±±±±±±±±±±±±±±±±±±±°°°°°±°           ÛÛ
ÛÛ       °±±±±±±±±±±±±±±±±±±±±±°ÛÛÛÛÛÛÛ±°±±±±±±±±±±±±±±±±±±±°°±±±°            ÛÛ
ÛÛ       °±±±±±±±±±±±±±±±±±±±±°°°ÛÛÛÛÛ±°°±±±±±±±±±±±±±±±±±±±±±                ÛÛ
ÛÛ       °±±±±±±±±±±±±±±±±±±±±±°° °±°°°°±±±±±±±±±±±±±±±±±±±±±°                ÛÛ
ÛÛ       °±±±±±±±±±±±±±±±±±±±±±±±°°°°°°±±±±±±±±±±±±±±±±±±±±±±±                ÛÛ
ÛÛ       °±±±±±±±±±±±±±±±±±±±±±±±±±±±±±±±±±±±±±±±±±±±±±±±±±±±±                ÛÛ
ÛÛ        ±±±±±±±±±±±±±±±±±±±±±±±±±±±±±±±±±±±±±±±±±±±±±±±±±±±°                ÛÛ
ÛÛ         ±±±±±±±±±±±±±±±±±±±±±±±±±±±±±±±±±±±±±±±±±±±±±±±±±°                 ÛÛ
ÛÛ          °±±±±±±±±±±±±±±±±±±±±±±±±±±±±±±±±±±±±±±±±±±±±±°                   ÛÛ
ÛÛ                                                                            ÛÛ
ÛÛ                                                                            ÛÛ
ÛÛÛÛÛÛÛÛÛÛÛÛÛÛÛÛÛÛÛÛÛÛÛÛÛÛÛÛÛÛÛÛÛÛÛÛÛÛÛÛÛÛÛÛÛÛÛÛÛÛÛÛÛÛÛÛÛÛÛÛÛÛÛÛÛÛÛÛÛÛÛÛÛÛÛÛÛÛÛÛ"""

def bytes_to_gb(byte_str):
    """Convertir une taille en bytes vers gigaoctets (Go)."""
    try:
        byte_value = int(re.sub(r'[^\d]', '', byte_str))  # Retirer les non-chiffres pour convertir proprement
        gb_value = byte_value / (1024 ** 3)  # Conversion en Go
        return "{:.2f} GB".format(gb_value)
    except ValueError:
        return "Unknown"


def convert_length_to_hmin(length_str):
    """Convertir une durée au format h:m:s.ms en format 'X h Y min'."""
    match = re.match(r"(\d+):(\d+):(\d+)", length_str)
    if match:
        hours = int(match.group(1))
        minutes = int(match.group(2))
        return "{} h {} min".format(hours, minutes)
    else:
        return "Unknown"


def extract_section_after_quick_summary(content):
    """Extraire tout le contenu après la section QUICK SUMMARY."""
    quick_summary_index = content.find("QUICK SUMMARY:")
    if quick_summary_index == -1:
        raise ValueError("QUICK SUMMARY introuvable dans le fichier.")
    return content[quick_summary_index + len("QUICK SUMMARY:"):].strip()


def extract_lines_by_category(content, category):
    """
    Extraire uniquement les lignes correspondant à une catégorie (VIDEO, AUDIO, SUBTITLES, SIZE, LENGTH, BITRATE, TITLE).
    Cette version est adaptée pour traiter l'audio et les sous-titres séparément.
    """
    lines = content.splitlines()
    category_lines = []

    for line in lines:
        if line.strip().startswith(category):  # Trouver la catégorie
            _, rest_of_line = line.split(":", 1)
            category_lines.append(rest_of_line.strip())
    return category_lines

def extract_video_info(content):
    """
    Extraire les informations vidéo sous la forme désirée : Codec, résolution, framerate, aspect ratio, profil, bitrate.
    """
    video_info = []
    
    # Extraire les lignes contenant "Video:"
    video_lines = extract_lines_by_category(content, "Video:")
    
    for line in video_lines:
        # Séparer les différentes informations par " / "
        parts = line.split(" / ")
        
        codec = parts[0].strip()
        if codec == "MPEG-4 AVC Video":
            codec = "AVC"
        if codec == "MPEG-H HEVC Video":
            codec = "HEVC"
        if codec == "MPEG-2 Video":
            codec = "MPEG-2"
        bitrate = parts[1].strip()
        resolution = parts[2].strip()
        fps = parts[3].strip()
        aspect_ratio = parts[4].strip()
        profile = parts[5].strip() if len(parts) > 5 else ""

        hdr = parts[7].strip() if len(parts) > 7 else ""
            
        # Formater et ajouter les informations extraites
        formatted_video = f"{codec} {resolution} {fps} {aspect_ratio} @ {bitrate}"

        if hdr:
            formatted_video += f" {hdr})"

        video_info.append(formatted_video)
    
    return video_info

def extract_audio_info(content):
    """
    Extraire les informations audio sous la forme désirée : Langue, codec, configuration et bitrate.
    """
    audio_info = []
    
    # Extraire les lignes contenant "Audio:"
    audio_lines = extract_lines_by_category(content, "Audio:")
    
    for line in audio_lines:
        # Séparer les différentes informations par " / "
        parts = line.split(" / ")
        
        language = parts[0].strip()  # Langue
        codec = parts[1].strip()     # Codec
        configuration = parts[2].strip()  # Configuration (e.g., Stereo, 5.1)
        bitrate = parts[4].strip()   # Bitrate (e.g., 192 kbps)
            
        # Formater et ajouter les informations extraites
        formatted_audio = f"{language} {codec} {configuration} @ {bitrate}"
        audio_info.append(formatted_audio)
    
    return audio_info


def extract_subtitles_info(content):
    """
    Extraire uniquement les langues des sous-titres.
    """
    subtitle_info = []
    subtitle_lines = extract_lines_by_category(content, "Subtitle:")

    for line in subtitle_lines:
        # Séparer les différentes informations par " / "
        parts = line.split(" / ")
        language = parts[0].strip()  # Langue
        
        # Formater et ajouter les informations extraites
        formatted_subtitle = f"{language}"
        subtitle_info.append(formatted_subtitle)
    
    return subtitle_info

def extract_disc_info(content, extras):
    """
    Extraire les informations principales du disque (size, bitrate, protection, length).
    Utilise `extract_lines_by_category` pour récupérer les informations.
    """
    disc_info = {}

    if extras:
        disc_info['extras'] = extras

    # Extraire la taille du disque
    size_info = extract_lines_by_category(content, "Disc Size")
    if size_info:
        disc_info['size'] = bytes_to_gb(size_info[0])

    # Extraire la durée du disque
    length_info = extract_lines_by_category(content, "Length")
    if length_info:
        disc_info['length'] = convert_length_to_hmin(length_info[0])

    # Extraire le bitrate
    bitrate_info = extract_lines_by_category(content, "Total Bitrate:")
    if bitrate_info:
        disc_info['bitrate'] = bitrate_info[0]

    # Extraire la protection du disque
    protection = extract_lines_by_category(content, "Protection")
    if protection:
        disc_info['protection'] = protection[0].strip()

    return disc_info

def extract_extras(content):
    """
    Extraire la ligne contenant 'Extras:' dans le contenu.
    Retourne une chaîne vide si la ligne n'existe pas.
    """
    # Diviser le contenu en lignes
    lines = content.splitlines()
    
    # Parcourir chaque ligne à la recherche de 'Extras:'
    for line in lines:
        if line.startswith("Extras:"):
            parts = line.split(":")
            extras = parts[1]  # Langue
            return extras.strip()  # Retourner la ligne avec 'Extras:'

    return ''  # Retourner une chaîne vide si 'Extras:' n'est pas trouvé

def parse_bdinfo_output(file_path):
    """
    Analyser le fichier BDINFO pour obtenir des sections vidéo, audio et sous-titres.
    """
    with open(file_path, 'r', encoding='utf-8') as file:
        content = file.read()
    
    extras = extract_extras(content)
    
    # Extraire tout le contenu après QUICK SUMMARY
    post_quick_summary = extract_section_after_quick_summary(content)

    # Récupérer les lignes spécifiques pour chaque catégorie
    video_info = extract_video_info(post_quick_summary)  # Utiliser la nouvelle fonction pour la vidéo
    audio_tracks = extract_audio_info(post_quick_summary)  # Utiliser la fonction audio mise à jour
    subtitles = extract_subtitles_info(post_quick_summary)  # Utiliser la fonction sous-titres mise à jour

    # Extraire les informations principales du disque
    disc_info = extract_disc_info(post_quick_summary, extras)

    return disc_info, video_info, audio_tracks, subtitles


def format_output(disc_info, video_info, audio_tracks, subtitles):
    """Format the extracted information along specified formatting."""
    # Construct the VIDEO section
    video_section = "ÃÄÄÄ VIDEO ÄÄÄÂÄ " + "\nÛÛ ³             ÃÄ ".join(video_info)
    
    # Diviser le texte par lignes
    linesVid = video_section.splitlines()

    # Assurez-vous que chaque ligne a au moins 80 caractères et termine avec les deux Û
    linesVid_with_suffix = []
    for index, lineVid in enumerate(linesVid):
        # Ajoutez simplement des espaces s'il manque de la longueur avant d'ajouter les Û
        if index != 0:
            while len(lineVid) < 78:
                lineVid += ' '
        else:
            while len(lineVid) < 75:
                lineVid += ' '
        lineVid += 'ÛÛ'  # Ajoutez les caractères Û aux positions 79 et 80
        linesVid_with_suffix.append(lineVid)

    # Ajustez la première et la dernière ligne si nécessaire
    if len(linesVid_with_suffix) == 1:
    # Si une seule ligne, remplacez le `┬` par `─`
        linesVid_with_suffix[0] = linesVid_with_suffix[0].replace('Â', 'Ä', 1)
    elif len(linesVid_with_suffix) > 1:
        # Si plusieurs lignes, remplacez la dernière par `└`
        linesVid_with_suffix[-1] = linesVid_with_suffix[-1].replace('Ã', 'À', 1)

    # Rejoindre les lignes modifiées
    video_section = "\n".join(linesVid_with_suffix)

    # Construct the AUDIO section
    audio_section = "ÃÄÄÄ AUDIO ÄÄÄÂÄ " + "\nÛÛ ³             ÃÄ ".join(audio_tracks)
    
    # Diviser le texte par lignes
    linesAud = audio_section.splitlines()

    # Assurez-vous que chaque ligne a au moins 80 caractères et termine avec les deux Û
    linesAud_with_suffix = []
    for index, lineAud in enumerate(linesAud):
        # Ajoutez simplement des espaces s'il manque de la longueur avant d'ajouter les Û
        if index != 0:
            while len(lineAud) < 78:
                lineAud += ' '
        else:
            while len(lineAud) < 75:
                lineAud += ' '
        lineAud += 'ÛÛ'  # Ajoutez les caractères Û aux positions 79 et 80
        linesAud_with_suffix.append(lineAud)

    # Ajustez la première et la dernière ligne si nécessaire
    if len(linesAud_with_suffix) == 1:
    # Si une seule ligne, remplacez le `┬` par `─`
        linesAud_with_suffix[0] = linesAud_with_suffix[0].replace('Â', 'Ä', 1)
    elif len(linesAud_with_suffix) > 1:
        # Si plusieurs lignes, remplacez la dernière par `└`
        linesAud_with_suffix[-1] = linesAud_with_suffix[-1].replace('Ã', 'À', 1)

    # Rejoindre les lignes modifiées
    audio_section = "\n".join(linesAud_with_suffix)

    # Construct the SUBTITLES section
    subtitle_section = "ÀÄÄÄ SUBS ÄÄÄÄÂÄ " + "\nÛÛ               ÃÄ ".join(subtitles)

    linesSub = subtitle_section.splitlines()

    # Assurez-vous que chaque ligne a au moins 80 caractères et termine avec les deux Û
    linesSub_with_suffix = []
    for index, lineSub in enumerate(linesSub):
        # Ajoutez simplement des espaces s'il manque de la longueur avant d'ajouter les Û
        if index != 0:
            while len(lineSub) < 78:
                lineSub += ' '
        else:
            while len(lineSub) < 75:
                lineSub += ' '
        lineSub += 'ÛÛ'  # Ajoutez les caractères Û aux positions 79 et 80
        linesSub_with_suffix.append(lineSub)

    # Ajustez la première et la dernière ligne si nécessaire
    if len(linesSub_with_suffix) == 1:
        # Si une seule ligne, remplacez le `┬` par `─`
        linesSub_with_suffix[0] = linesSub_with_suffix[0].replace('Â', 'Ä', 1)
    elif len(linesSub_with_suffix) > 1:
        # Si plusieurs lignes, remplacez la dernière par `└`
        linesSub_with_suffix[-1] = linesSub_with_suffix[-1].replace('Ã', 'À', 1)
    # Rejoindre les lignes modifiées
    subtitle_section = "\n".join(linesSub_with_suffix)
    
    protectionAndExtra = disc_info.get('protection', 'Unknown')
    if disc_info.get('extras',''):
        protectionAndExtra += ' ' + disc_info.get('extras','')

    output = (
        "ÛÛÛÛÛÛÛÛÛÛÛÛÛÛÛÛÛÛÛÛÛÛÛÛÛÛÛÛÛÛÛÛÛÛÛÛ BDiNFO ÛÛÛÛÛÛÛÛÛÛÛÛÛÛÛÛÛÛÛÛÛÛÛÛÛÛÛÛÛÛÛÛÛÛÛÛ\n"
        "ÛÛÛÛÛÛÛÛÛÛÛÛÛÛÛÛÛÛÛÛÛÛÛÛÛÛÛÛÛÛÛÛÛÛÛÛÛÛÛÛÛÛÛÛÛÛÛÛÛÛÛÛÛÛÛÛÛÛÛÛÛÛÛÛÛÛÛÛÛÛÛÛÛÛÛÛÛÛÛÛ\n"
        "ÛÛ                                                                            ÛÛ\n"
        "ÛÛ                                                                            ÛÛ\n"
        "ÛÛ ÚÄÄÄ DISC ÄÄÄÄÂÄ {protection:<57} ÛÛ\n"
        "ÛÛ ³             ÃÄ {length} @ {bitrate:<43}  ÛÛ\n"
        "ÛÛ ³             ÀÄ {size:<57} ÛÛ\n"
        "ÛÛ ³                                                                          ÛÛ\n"
        "ÛÛ {video_section}\n"
        "ÛÛ ³                                                                          ÛÛ\n"
        "ÛÛ {audio_section}\n"
        "ÛÛ ³                                                                          ÛÛ\n"
        "ÛÛ {subtitle_section}\n"
        "ÛÛ                                                                            ÛÛ\n"
        "ÛÛÛÛÛÛÛÛÛÛÛÛÛÛÛÛÛÛÛÛÛÛÛÛÛÛÛÛÛÛÛÛÛÛÛÛÛÛÛÛÛÛÛÛÛÛÛÛÛÛÛÛÛÛÛÛÛÛÛÛÛÛÛÛÛÛÛÛÛÛÛÛÛÛÛÛÛÛÛÛ"
    ).format(
        protection=protectionAndExtra,
        length=disc_info.get('length', 'Unknown'),
        bitrate=disc_info.get('bitrate', 'Unknown'),
        size=disc_info.get('size', 'Unknown'),
        video_section=video_section,
        audio_section=audio_section,
        subtitle_section=subtitle_section
    )
    
    return output

def read_greetz_from_ini(file_path):
    if not os.path.exists(file_path):
        raise FileNotFoundError("The 'greetz.ini' file cannot be found.")
    """Lire les 'greetz' à partir d'un fichier .ini."""
    config = configparser.ConfigParser()
    config.read(file_path)
    return config.get('DEFAULT', 'Greetz', fallback='DefaultGreetz')

def get_user_info():
    """Demande à l'utilisateur d'entrer des informations supplémentaires sur la release."""
    release_date = input("Release Date (e.g., 25/11/2024): ")
    if not release_date:
        release_date = datetime.today().strftime("%d/%m/%Y")
    bluray_region = input("Bluray Region (e.g., Z2): ")
    french_audio = input("French Audio (e.g., VFi): ")
    imdb_id = input("IMDb ID (e.g., tt5052448): ")
    tmdb_id = input("TMDb ID (e.g., 419430): ")
    note = input("Note (e.g., First release): ")

    user_info = {
        'release_date': release_date,
        'bluray_region': bluray_region,
        'french_audio': french_audio,
        'imdb_id': imdb_id,
        'tmdb_id': tmdb_id,
        'note': note,
    }

    return user_info

def format_user_info(user_info, file_name, greetz):
    # Calculer l'espace utilisé par le texte du titre du fichier
    text_length = len(file_name)
    
    # Calculer l'espace disponible pour les caractères Û
    total_border_length = 80 - text_length - 2
    
    # Vérifier qu'il y a encore de l'espace pour une bordure
    if total_border_length < 0:
        raise ValueError("The file name is too long for the specified format.")
    
    # Diviser l'espace de Û également de chaque côté du nom
    left_border_length = total_border_length // 2
    right_border_length = total_border_length - left_border_length
    
    border_left = 'Û' * left_border_length
    border_right = 'Û' * right_border_length
    
    # Nombre maximum de caractères sur une ligne après "Note .......... "
    note_prefix = "Note ............ "
    max_line_length = 80 - len(note_prefix) - 4  # -2 for borders, -2 for spaces

    # Préparer les sections de texte si les informations sont disponibles
    release_date = user_info.get("release_date", "")
    bluray_region = user_info.get("bluray_region", "")
    french_audio = user_info.get("french_audio", "")
    imdb_id = user_info.get("imdb_id", "")
    tmdb_id = user_info.get("tmdb_id", "")
    note_text = user_info.get("note", "")
    
    # Créer une liste de lignes pour la note
    note_lines = []
    while note_text:
        line = note_text[:max_line_length-3]
        note_lines.append(line)
        note_text = note_text[max_line_length:-3]

    note_formatted = []
    for i, line in enumerate(note_lines):
        if i == 0:
            note_formatted.append(f"ÛÛ  {note_prefix}{line:<{max_line_length-3}} ÛÛ")
        else:
            note_formatted.append(f"ÛÛ  {' ' * len(note_prefix)}{line:<{max_line_length-3}} ÛÛ")
    
    note_formatted_text = "\n".join(note_formatted)

    # Composer le texte formaté
    formatted_info = (
        "ÛÛÛÛÛÛÛÛÛÛÛÛÛÛÛÛÛÛÛÛÛÛÛÛÛÛÛÛÛÛÛÛÛÛÛÛÛÛÛÛÛÛÛÛÛÛÛÛÛÛÛÛÛÛÛÛÛÛÛÛÛÛÛÛÛÛÛÛÛÛÛÛÛÛÛÛÛÛÛÛ\n"
        f"{border_left} {file_name} {border_right}\n"
        "ÛÛÛÛÛÛÛÛÛÛÛÛÛÛÛÛÛÛÛÛÛÛÛÛÛÛÛÛÛÛÛÛÛÛÛÛÛÛÛÛÛÛÛÛÛÛÛÛÛÛÛÛÛÛÛÛÛÛÛÛÛÛÛÛÛÛÛÛÛÛÛÛÛÛÛÛÛÛÛÛ\n"
        "ÛÛ                                                                            ÛÛ\n"
        f"{'ÛÛ  Release Date .... ' + release_date + ' ' * (56 - len(release_date)) + 'ÛÛ' if release_date else ''}\n"
        f"{'ÛÛ  BluRay Region ... ' + bluray_region + ' ' * (56 - len(bluray_region)) + 'ÛÛ' if bluray_region else ''}\n"
        f"{'ÛÛ  French Audio .... ' + french_audio + ' ' * (56 - len(french_audio)) + 'ÛÛ' if french_audio else ''}\n"
        "ÛÛ                                                                            ÛÛ\n"
        f"{'ÛÛ  IMDb ............ ' + imdb_id + ' ' * (56 - len(imdb_id)) + 'ÛÛ' if imdb_id else ''}\n"
        f"{'ÛÛ  TMDb ............ ' + tmdb_id + ' ' * (56 - len(tmdb_id)) + 'ÛÛ' if tmdb_id else ''}\n"
        f"ÛÛ  Greetz .......... {greetz:<54}  ÛÛ\n"
        f"{note_formatted_text if note_lines else ''}\n"
        "ÛÛ                                                                            ÛÛ\n"
        "ÛÛÛÛÛÛÛÛÛÛÛÛÛÛÛÛÛÛÛÛÛÛÛÛÛÛÛÛÛÛÛÛÛÛÛÛÛÛÛÛÛÛÛÛÛÛÛÛÛÛÛÛÛÛÛÛÛÛÛÛÛÛÛÛÛÛÛÛÛÛÛÛÛÛÛÛÛÛÛÛ"
    )

    return "\n".join(line for line in formatted_info.split("\n") if line.strip())

def find_bdinfo_file(temp_dir):
    for file_name in os.listdir(temp_dir):
        if file_name.endswith('.txt') and 'BDINFO' in file_name:
            return os.path.join(temp_dir, file_name)
    return None

def main(input_iso):
    temp_dir = "temp"
    os.makedirs(temp_dir, exist_ok=True)

    # Extraire le nom du fichier sans extension
    iso_name = os.path.splitext(os.path.basename(input_iso))[0]
    
    try:
        # Lire les greetz depuis un .ini
        greetz = read_greetz_from_ini('greetz.ini')

        # Exécuter la commande bdinfo
        print(f"Run the BDINFO command for {input_iso}...")
        result = subprocess.run(
            ["bdinfo", input_iso, temp_dir, "-w"],
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            text=True
        )

        if result.returncode != 0:
            print(f"Error running BDINFO: {result.stderr}")
            return

        # Rechercher le fichier texte BDINFO
        bdinfo_file = find_bdinfo_file(temp_dir)
        if not bdinfo_file:
            print(f"BDINFO file missing from temporary directory.")
            return

        # Analyser le fichier de sortie
        try:
            disc_info, video_info, audio_tracks, subtitles = parse_bdinfo_output(bdinfo_file)
        except ValueError as e:
            print(f"Erreur : {e}")
            return

        # Obtenir les informations de l'utilisateur
        user_info = get_user_info()
        formatted_user_info = format_user_info(user_info, iso_name, greetz)

        # Générer le texte formaté
        formatted_output = format_output(disc_info, video_info, audio_tracks, subtitles)

        # Générer le fichier de sortie avec la même base que l'ISO mais avec l'extension .nfo
        output_txt = os.path.splitext(input_iso)[0] + ".nfo"
        
        # Sauvegarder dans un fichier
        with open(output_txt, 'w', encoding='cp1252') as output_file:
            output_file.write(logo + "\n" + formatted_user_info + "\n" + formatted_output)

        print(f"Generated file : {output_txt}")

    except FileNotFoundError as e:
        print(e)

    finally:
        # Supprimer les fichiers temporaires
        print("Cleaning temporary files...")
        if os.path.exists(temp_dir):
            shutil.rmtree(temp_dir)
        print("Temporary files deleted.")
        
if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Please drag and drop an ISO file onto this script or use contextmenu.")
        # main('test.iso')
    else:
        input_iso_path = sys.argv[1]
        main(input_iso_path)