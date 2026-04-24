"""
agents/base_agent.py — Motor central dos agentes
Implementa o loop tool-use do Anthropic SDK.
"""

import anthropic
from rich.console import Console
from rich.panel import Panel
from config import ANTHROPIC_API_KEY, CLAUDE_MODEL, VERBOSE
from tools import TOOLS_SCHEMA, executar_ferramenta

console = Console()
client  = anthropic.Anthropic(api_key=ANTHROPIC_API_KEY)


class Agente:
    """
    Agente baseado na API Anthropic com suporte a ferramentas.
    Executa o loop agentico até o modelo parar de chamar tools.
    """

    def __init__(
        self,
        nome: str,
        emoji: str,
        system_prompt: str,
        tools_permitidas: list[str],
        max_iteracoes: int = 8,
    ):
        self.nome             = nome
        self.emoji            = emoji
        self.system_prompt    = system_prompt
        self.tools_permitidas = tools_permitidas
        self.max_iteracoes    = max_iteracoes

        # Filtra apenas as ferramentas permitidas para este agente
        self.tools = [
            t for t in TOOLS_SCHEMA
            if t["name"] in tools_permitidas
        ]

    def _log(self, msg: str):
        if VERBOSE:
            console.print(f"  [dim]{self.emoji} [{self.nome}][/dim] {msg}")

    def executar(self, tarefa: str, contexto: str = "") -> str:
        """
        Executa a tarefa com loop agentico completo.
        Retorna o texto final produzido pelo agente.
        """
        if VERBOSE:
            console.print(
                Panel(
                    f"[bold]{tarefa[:120]}{'...' if len(tarefa) > 120 else ''}[/bold]",
                    title=f"{self.emoji}  [bold cyan]{self.nome}[/bold cyan]",
                    border_style="cyan",
                    padding=(0, 2),
                )
            )

        # Monta mensagem inicial
        conteudo_user = tarefa
        if contexto:
            conteudo_user = f"=== CONTEXTO DAS ETAPAS ANTERIORES ===\n{contexto}\n\n=== SUA TAREFA ===\n{tarefa}"

        messages = [{"role": "user", "content": conteudo_user}]

        for iteracao in range(self.max_iteracoes):
            response = client.messages.create(
                model=CLAUDE_MODEL,
                max_tokens=4096,
                system=self.system_prompt,
                tools=self.tools,
                messages=messages,
            )

            # Adiciona resposta do assistente ao histórico
            messages.append({"role": "assistant", "content": response.content})

            # Verifica se parou (end_turn = resposta final)
            if response.stop_reason == "end_turn":
                # Extrai texto da resposta
                texto = " ".join(
                    b.text for b in response.content
                    if hasattr(b, "text")
                )
                self._log(f"✅ Concluído em {iteracao + 1} iteração(ões)")
                return texto

            # Processa chamadas de ferramentas
            if response.stop_reason == "tool_use":
                tool_results = []
                for bloco in response.content:
                    if bloco.type == "tool_use":
                        self._log(f"🔧 Chamando ferramenta: [yellow]{bloco.name}[/yellow]")
                        resultado = executar_ferramenta(bloco.name, bloco.input)
                        self._log(f"   ↳ {str(resultado)[:120]}...")
                        tool_results.append({
                            "type":        "tool_result",
                            "tool_use_id": bloco.id,
                            "content":     resultado,
                        })

                # Devolve resultados ao modelo
                messages.append({"role": "user", "content": tool_results})

        # Fallback: extrai o que houver na última resposta
        return " ".join(
            b.text for b in response.content
            if hasattr(b, "text")
        )
