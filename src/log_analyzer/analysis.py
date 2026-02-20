from collections import Counter
from .parser import parse_logfile
from rich.console import Console

console = Console()
def show_statistics(entries):
    console.rule("Statisztikák")

    # Itt is: e.service_name a dict lookup helyett
    process_counts = Counter(e.service_name for e in entries)
    
    console.print("[bold]A 10 leggyakoribb hibaüzenet:[/bold]")
    total_count = 0
    for proc, count in process_counts.most_common(10):
        console.print(f"{proc} : {count}")
        total_count += count

    console.print(f"\n[bold]TOP 10 bejegyzés száma:[/] {total_count}")
    total = process_counts.total()
    console.print(f"\n[bold]Összes bejegyzés:[/] {total}")
    console.print(f"[bold]TOP 10 bejegyzés aránya az összeshez:[/] {total_count / total * 100 if total > 0 else 0:.2f}%")

    # egyedi folyamatok száma
    unique_processes = len(set(e.service_name for e in entries))
    console.print(f"\n[bold]Egyedi folyamatok száma:[/] {unique_processes}")

    #kritikus események
    error_keywords = ['error', 'failed', 'critical', 'warning']
    critical_events = sum(1 for e in entries if any(keyword in e.message.lower() for keyword in error_keywords))

    if total >0:
        error_percentage = (critical_events / total) * 100
        console.print(f"\n[bold]Kritikus események száma:[/] {critical_events}")
        console.print(f"[bold]Kritikus események aránya az összeshez:[/] {error_percentage:.2f}%")

    #időbeli eloszlás
    console.print("\n[bold]Események időbeli eloszlása (óra szerint):[/bold]")
    time_buckets = Counter(e.timestamp.strftime('%Y-%m-%d %H:00') for e in entries)

    for time, count in time_buckets.most_common(10):
        console.print(f"{time} : {count} bejegyzés")
    
    console.print(f"\n[bold]Események időbeli eloszlása (nap szerint):[/bold]")
    day_buckets = Counter(e.timestamp.strftime('%Y-%m-%d') for e in entries)

    for day, count in day_buckets.most_common(10):
        console.print(f"{day} : {count} bejegyzés")

    console.rule("Statisztikák vége")