# parser.py
import re

def parse_logfile(path, keyword=None):
    # MINTA LOG SOR:
    # 2025-11-01T18:20:24.128827+00:00 mozestibor-ThinkPad-T14-Gen-2a systemd[1]: Mounted snap-bare-5.mount - Mount unit for bare, revision 5.
    
    #splitting message into time, hostname, process, message part
    pattern = re.compile(
        r'(?P<time>\d{4}-\d{2}-\d{2}T\d{2}:\d{2}:\d{2}\.\d+\+\d{2}:\d{2})\s+'  # time + space
        r'(?P<hostname>\S+)\s+'           # Hostname (non-whitespace) + space
        r'(?P<process>[^:]+):\s+'         # Process + : + space
        r'(?P<message>.*)'                # message part until rest of the line
    )

    entries = []
    
    try:
        #open the log file
        with open(path, 'r', encoding='utf-8', errors='ignore') as f:
            #processing the file and put the matched lines to entries dict
            for line in f:
                # cut unnecessary white space 
                line = line.strip() 
                if not line:
                    # jump empty lines
                    continue 

                match = pattern.match(line)
                if not match:
                    # print(f"NO MATCH: {line}") 
                    continue
                
                entry = match.groupdict()

                # filter
                if keyword:
                    full_text = f"{entry['process']} {entry['message']}".lower()
                    if keyword.lower() not in full_text:
                        continue

                entries.append(entry)
                
    except FileNotFoundError:
        print(f"Hiba: A fájl nem található: {path}")
        return []

    return entries
