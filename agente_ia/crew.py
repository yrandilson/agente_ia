"""
crew.py — Orquestração do pipeline multi-agente
Pesquisador → Analista → Redator → Gerente
"""

from rich.console import Console
from rich.rule import Rule
from agents import (
    criar_pesquisador,
    criar_analista,
    criar_redator,
    criar_gerente,
)

console = Console()

# ─────────────────────────────────────────────
# Tarefas (prompts passados a cada agente)
# ─────────────────────────────────────────────

def tarefa_pesquisa(tema: str) -> str:
    return (
        f"Pesquise extensivamente sobre o tema: **{tema}**\n\n"
        "1. Faça pelo menos 3 buscas diferentes sobre o tema\n"
        "2. Registre a data/hora da pesquisa\n"
        "3. Organize em: Contexto, Situação Atual, Dados/Estatísticas, Tendências, Fontes\n"
        "4. Seja factual e cite as URLs encontradas\n"
        "5. Produza um documento com no mínimo 600 palavras"
    )


def tarefa_analise(tema: str) -> str:
    return (
        f"Analise criticamente o material de pesquisa sobre: **{tema}**\n\n"
        "1. Use a ferramenta analisar_texto no documento de pesquisa recebido\n"
        "2. Liste os 5 principais insights\n"
        "3. Crie uma tabela de Oportunidades x Riscos\n"
        "4. Avalie relevância de cada subtema (1-10)\n"
        "5. Indique lacunas de informação\n\n"
        "O contexto com o material de pesquisa está acima."
    )


def tarefa_redacao(tema: str) -> str:
    return (
        f"Produza um relatório executivo completo sobre: **{tema}**\n\n"
        "Use todo o material de pesquisa e análise disponível no contexto acima.\n"
        "Siga a estrutura de 8 seções definida no seu papel.\n"
        "Ao finalizar, salve como 'relatorio_final.md'."
    )


def tarefa_revisao(tema: str) -> str:
    return (
        f"Revise e aprove o relatório executivo sobre: **{tema}**\n\n"
        "O relatório completo está no contexto acima.\n"
        "Aplique o checklist de qualidade, faça ajustes e salve como 'relatorio_revisado.md'."
    )


# ─────────────────────────────────────────────
# Pipeline principal
# ─────────────────────────────────────────────

def executar(tema: str) -> str:
    """
    Executa o pipeline completo de 4 agentes.
    Cada agente recebe o output acumulado dos anteriores.
    """
    contexto_acumulado = ""
    resultados = {}

    etapas = [
        ("pesquisa",  criar_pesquisador, tarefa_pesquisa),
        ("analise",   criar_analista,    tarefa_analise),
        ("redacao",   criar_redator,     tarefa_redacao),
        ("revisao",   criar_gerente,     tarefa_revisao),
    ]

    for chave, factory, tarefa_fn in etapas:
        console.print(Rule(style="dim"))
        agente    = factory()
        resultado = agente.executar(
            tarefa=tarefa_fn(tema),
            contexto=contexto_acumulado,
        )
        resultados[chave]     = resultado
        contexto_acumulado   += f"\n\n### OUTPUT — {agente.nome} ###\n{resultado}"

    console.print(Rule(style="dim"))
    return resultados.get("revisao", "")
