import click
from rich.console import Console
from .analysis import show_statistics
from .parser import parse_logfile

console = Console()

@click.command()
@click.option('--file', '-f', required=True, help="Log fájl elérési útvonala")
@click.option("--filter", "-k", required=False, help="Kulcsszó (opcionális)") # Átírtam opcionálisra
@click.option('--stats', '-s', is_flag=True, help="Statisztikai adatok megjelenítése")
def main(file, filter, stats):
    """Linux log elemző eszköz."""
    
    # console.print("[bold yellow]DEBUG:[/] Futtatás elindult...")
    console.print(f"Logfájl elemzése: [bold]{file}[/]")
    
    entries = parse_logfile(file, filter)

    if not entries:
        console.print("[red]Nincs találat vagy a fájl üres![/]")
        return
    
    if stats:
        show_statistics(entries)
    else:
        # Kiíratjuk az első 20 találatot
        # Mivel 'LogEntry' objektumok vannak, ponttal (.) érjük el az adatokat
        for entry in entries[:20]:
            console.print(f"[green]{entry.timestamp}[/] [cyan]{entry.service_name}[/]: {entry.message}")

        console.print(f"\n[bold green]Összesen {len(entries)} bejegyzés található.[/]")




if __name__== "__main__":
    main()