import click
from rich.console import Console
from app.log_analyzer.parser import parse_logfile
from collections import Counter

console = Console()

#defining the options
@click.command()
@click.option('--file', '-f', required=True, help="Log fájl elérési útvonala")
@click.option("--filter", "-k", required=True, help="Kulcsszó")
@click.option('--stats', '-s', is_flag=True, help="Statisztikai adatok megjeleítése")

def main(file, filter, stats):
    console.print("[bold yellow]DEBUG:[/] Futtatás elindult...")
    console.print(f"Logfájl elemzése: {file}")
    entries=parse_logfile(file,filter)

    if not entries:
        console.print("Nincs találat!")
        return
    
    if stats:
        show_statistics(entries)
    else:
    #print first 20 matches
        for i in entries[:20]:
            console.print(f"[green]{i['time']}[/] {i['process']}: {i['message']}")

        console.print(f"[bold green]Összesen {len(entries)} bejegyzés található.[/]")

def show_statistics(entries):
    console.rule("Statisztikák:")

    process_counts = Counter(e["process"] for e in entries)
    console.print("Leggyakoribb folyamatok")
    for proc, count in process_counts.most_common(10):
        console.print(f"{proc} : {count}")

if __name__== "__main__":
    main()
    