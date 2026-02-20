import re
from datetime import datetime
from .models import LogEntry  # A relatív import (a pont az elején) nagyon fontos!

def parse_logfile(path, keyword=None):
    # MINTA LOG SOR:
    # 2025-11-01T18:20:24.128827+00:00 mozestibor-ThinkPad-T14-Gen-2a systemd[1]: Mounted...
    
    pattern = re.compile(
        r'(?P<time>\d{4}-\d{2}-\d{2}T\d{2}:\d{2}:\d{2}\.\d+\+\d{2}:\d{2})\s+'  
        r'(?P<hostname>\S+)\s+'           
        r'(?P<process>[^:]+):\s+'         
        r'(?P<message>.*)'                
    )

    entries = []
    
    try:
        with open(path, 'r', encoding='utf-8', errors='ignore') as f:
            for line in f:
                line = line.strip() 
                if not line:
                    continue 

                match = pattern.match(line)
                if not match:
                    continue
                
                data = match.groupdict()

                # --- ITT A VÁLTOZÁS ---
                # 1. Dátum konvertálása stringből datetime objektummá
                try:
                    # A Python 3.7+ fromisoformat kezeli az ilyen ISO stringeket
                    dt_object = datetime.fromisoformat(data['time'])
                except ValueError:
                    dt_object = datetime.now() # Vészmegoldás, ha a dátum hibás

                # 2. LogEntry objektum létrehozása
                # Figyeld meg: a regex 'process' csoportját a 'service_name' mezőbe tesszük
                entry = LogEntry(
                    timestamp=dt_object,
                    hostname=data['hostname'],
                    service_name=data['process'],
                    message=data['message'],
                    raw_line=line
                )

                # 3. Szűrés (már az objektum mezőire hivatkozva)
                if keyword:
                    full_text = f"{entry.service_name} {entry.message}".lower()
                    if keyword.lower() not in full_text:
                        continue

                entries.append(entry)
                
    except FileNotFoundError:
        print(f"Hiba: A fájl nem található: {path}")
        return []

    return entries