"""
main.py — Ponto de entrada com CLI Rich
Compatível com Python 3.10+, incluindo 3.14
"""

import sys
import time
import argparse
from pathlib import Path

from rich.console import Console
from rich.panel import Panel
from rich.table import Table
from rich.markdown import Markdown
from rich.progress import Progress, SpinnerColumn, TextColumn
from rich import box

console = Console()


def banner():
    console.print()
    console.print(
        Panel.fit(
            "[bold cyan]🤖  Agente IA — Pipeline Multi-Agente[/bold cyan]\n"
            "[dim]Powered by Anthropic Claude  •  Python 3.10+[/dim]\n"
            "[dim]Pesquisador → Analista → Redator → Gerente[/dim]",
            border_style="cyan",
            padding=(1, 6),
        )
    )
    console.print()


def exibir_agentes():
    t = Table(title="👥 Agentes do Pipeline", box=box.ROUNDED, border_style="dim cyan")
    t.add_column("Agente",      style="bold yellow", width=16)
    t.add_column("Papel",       style="white",       width=30)
    t.add_column("Ferramentas", style="green",       width=34)

    t.add_row("🔍 Pesquisador", "Coleta dados na internet",    "busca_web, data_hora")
    t.add_row("📊 Analista",    "Analisa e extrai insights",   "analisar_texto, data_hora")
    t.add_row("✍️  Redator",    "Produz relatório executivo",  "salvar_arquivo, data_hora")
    t.add_row("🎯 Gerente",     "Revisão e aprovação final",   "salvar_arquivo, data_hora")

    console.print(t)
    console.print()


def exibir_resultado(tema: str):
    console.rule("[bold green]✅ Pipeline Concluído[/bold green]")
    console.print()

    for nome in ["relatorio_revisado.md", "relatorio_final.md"]:
        caminho = Path(f"output/{nome}")
        if caminho.exists():
            console.print(Panel(
                f"[green]Relatório salvo em:[/green] [bold]output/{nome}[/bold]",
                border_style="green",
            ))
            conteudo = caminho.read_text(encoding="utf-8")
            console.print(Markdown(conteudo))
            return

    console.print("[yellow]Nenhum relatório encontrado na pasta output/[/yellow]")


def main():
    parser = argparse.ArgumentParser(description="Agente IA — Pipeline Multi-Agente")
    parser.add_argument("--tema", "-t", type=str, default=None,
                        help="Tema para pesquisa e análise")
    parser.add_argument("--listar", "-l", action="store_true",
                        help="Lista os agentes e sai")
    args = parser.parse_args()

    banner()

    if args.listar:
        exibir_agentes()
        return

    exibir_agentes()

    # Obtém tema
    if args.tema:
        tema = args.tema.strip()
    else:
        console.print("[bold]📌 Informe o tema para análise:[/bold]")
        tema = console.input("[cyan]➜  [/cyan]").strip()

    if not tema:
        console.print("[red]Tema não pode estar vazio.[/red]")
        sys.exit(1)

    console.print(Panel(
        f"[bold]Tema:[/bold] [yellow]{tema}[/yellow]",
        border_style="yellow",
        title="🚀 Iniciando pipeline",
    ))
    console.print()

    from crew import executar

    inicio = time.time()
    try:
        with Progress(
            SpinnerColumn(),
            TextColumn("[cyan]{task.description}[/cyan]"),
            console=console,
            transient=True,
        ) as prog:
            prog.add_task("Executando agentes... (pode levar alguns minutos)", total=None)
            executar(tema)

        duracao = time.time() - inicio
        console.print(f"\n[dim]⏱  Tempo total: {duracao:.1f}s[/dim]\n")
        exibir_resultado(tema)

    except KeyboardInterrupt:
        console.print("\n[yellow]⚠  Interrompido pelo usuário.[/yellow]")
        sys.exit(0)
    except Exception as e:
        console.print(f"\n[red]❌ Erro:[/red] {e}")
        console.print_exception()
        sys.exit(1)


if __name__ == "__main__":
    main()
