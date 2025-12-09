#!/usr/bin/env python3
"""Terminal221b - Main entry point.

Polymathic Autonomous Organization (PAO)
A sovereign, self-funding AI civilization engine.
"""

import sys
from pathlib import Path

import click
from rich.console import Console

# Add parent directory to path for imports
sys.path.insert(0, str(Path(__file__).parent.parent))

from utils.license import LicenseManager, LicenseTier

console = Console()


def print_banner():
    """Print the Terminal221b banner."""
    banner = """
╔══════════════════════════════════════════════════════════════╗
║                                                              ║
║   ████████╗███████╗██████╗ ███╗   ███╗██╗███╗   ██╗ █████╗  ║
║   ╚══██╔══╝██╔════╝██╔══██╗████╗ ████║██║████╗  ██║██╔══██╗ ║
║      ██║   █████╗  ██████╔╝██╔████╔██║██║██╔██╗ ██║███████║ ║
║      ██║   ██╔══╝  ██╔══██╗██║╚██╔╝██║██║██║╚██╗██║██╔══██║ ║
║      ██║   ███████╗██║  ██║██║ ╚═╝ ██║██║██║ ╚████║██║  ██║ ║
║      ╚═╝   ╚══════╝╚═╝  ╚═╝╚═╝     ╚═╝╚═╝╚═╝  ╚═══╝╚═╝  ╚═╝ ║
║                                                              ║
║              ██████╗ ██████╗  ██╗██████╗                     ║
║              ╚════██╗╚════██╗███║██╔══██╗                    ║
║               █████╔╝ █████╔╝╚██║██████╔╝                    ║
║              ██╔═══╝ ██╔═══╝  ██║██╔══██╗                    ║
║              ███████╗███████╗ ██║██████╔╝                    ║
║              ╚══════╝╚══════╝ ╚═╝╚═════╝                     ║
║                                                              ║
║         Polymathic Autonomous Organization (PAO)             ║
║         A sovereign, self-funding AI civilization            ║
║                                                              ║
╚══════════════════════════════════════════════════════════════╝
"""
    console.print(banner, style="bold cyan")


def print_license_info(manager: LicenseManager):
    """Print license tier information."""
    tier = manager.tier
    limits = manager.get_limits()
    
    tier_colors = {
        LicenseTier.FREE: "yellow",
        LicenseTier.PRO: "green",
        LicenseTier.ENTERPRISE: "magenta",
    }
    
    color = tier_colors.get(tier, "white")
    console.print(f"\n[{color}]License Tier: {tier.value.upper()}[/{color}]")
    
    if tier == LicenseTier.FREE:
        console.print("[dim]Upgrade to Pro for more features: https://bakerstreetproject221B.store/terminal221b[/dim]")
    
    console.print(f"  • Runs/day: {limits.max_runs_per_day if limits.max_runs_per_day > 0 else 'Unlimited'}")
    console.print(f"  • Max agents: {limits.max_agents if limits.max_agents > 0 else 'Unlimited'}")
    console.print(f"  • Blockchain: {'✓' if limits.blockchain_enabled else '✗'}")


@click.group(invoke_without_command=True)
@click.option("--version", "-v", is_flag=True, help="Show version information")
@click.option("--license-info", "-l", is_flag=True, help="Show license information")
@click.pass_context
def cli(ctx, version, license_info):
    """Terminal221b - Polymathic Autonomous Organization (PAO)
    
    A sovereign, self-funding AI civilization engine with multi-agent
    collaboration, terminal UI, and Solana blockchain integration.
    """
    ctx.ensure_object(dict)
    
    # Initialize license manager
    manager = LicenseManager()
    ctx.obj["license_manager"] = manager
    
    if version:
        from src import __version__
        console.print(f"Terminal221b v{__version__}")
        return
    
    if license_info:
        print_license_info(manager)
        return
    
    if ctx.invoked_subcommand is None:
        print_banner()
        print_license_info(manager)
        console.print("\n[bold]Available commands:[/bold]")
        console.print("  [cyan]run[/cyan]       Start an agent session")
        console.print("  [cyan]tui[/cyan]       Launch terminal UI")
        console.print("  [cyan]agents[/cyan]    List available agents")
        console.print("  [cyan]wallet[/cyan]    Manage Solana wallet (Pro+)")
        console.print("\nRun [bold]terminal221b --help[/bold] for more options.")


@cli.command()
@click.option("--agent", "-a", type=click.Choice(["analyst", "artist", "engineer", "writer"]), 
              default="analyst", help="Agent to run")
@click.option("--prompt", "-p", type=str, help="Initial prompt for the agent")
@click.pass_context
def run(ctx, agent, prompt):
    """Start an agent session."""
    manager = ctx.obj["license_manager"]
    
    # Check if we can run
    can_run, message = manager.can_run()
    if not can_run:
        console.print(f"[red]Error:[/red] {message}")
        if manager.tier == LicenseTier.FREE:
            console.print("[yellow]Upgrade to Pro for more runs: https://bakerstreetproject221B.store/terminal221b[/yellow]")
        sys.exit(1)
    
    limits = manager.get_limits()
    
    # Check agent count limit
    if limits.max_agents == 1 and agent != "analyst":
        console.print(f"[red]Error:[/red] Free tier only supports the analyst agent.")
        console.print("[yellow]Upgrade to Pro for all agents: https://bakerstreetproject221B.store/terminal221b[/yellow]")
        sys.exit(1)
    
    console.print(f"\n[bold green]Starting {agent} agent...[/bold green]")
    console.print("[dim]Agent system not yet implemented. See TODO_MVP.md[/dim]")
    
    # TODO: Implement agent system
    # from src.agents import run_agent
    # run_agent(agent, prompt, limits)


@cli.command()
@click.pass_context
def tui(ctx):
    """Launch the terminal UI."""
    manager = ctx.obj["license_manager"]
    
    can_run, message = manager.can_run()
    if not can_run:
        console.print(f"[red]Error:[/red] {message}")
        sys.exit(1)
    
    console.print("\n[bold green]Launching Terminal221b TUI...[/bold green]")
    console.print("[dim]TUI not yet implemented. See TODO_MVP.md[/dim]")
    
    # TODO: Implement TUI
    # from src.tui import Terminal221bApp
    # app = Terminal221bApp()
    # app.run()


@cli.command()
def agents():
    """List available agents."""
    console.print("\n[bold]Available Agents:[/bold]\n")
    
    agents_info = [
        ("analyst", "Data analysis, research, and insights", "Free+"),
        ("artist", "Creative content generation", "Pro+"),
        ("engineer", "Code generation and architecture", "Pro+"),
        ("writer", "Documentation and technical writing", "Pro+"),
    ]
    
    for name, desc, tier in agents_info:
        console.print(f"  [cyan]{name:12}[/cyan] {desc} [dim]({tier})[/dim]")


@cli.command()
@click.option("--create", is_flag=True, help="Create a new Solana wallet")
@click.option("--balance", is_flag=True, help="Check wallet balance")
@click.pass_context
def wallet(ctx, create, balance):
    """Manage Solana wallet (Pro+ tier)."""
    manager = ctx.obj["license_manager"]
    limits = manager.get_limits()
    
    if not limits.blockchain_enabled:
        console.print("[red]Error:[/red] Blockchain features require Pro or Enterprise tier.")
        console.print("[yellow]Upgrade at: https://bakerstreetproject221B.store/terminal221b[/yellow]")
        sys.exit(1)
    
    console.print("\n[bold green]Solana Wallet Manager[/bold green]")
    console.print("[dim]Blockchain integration not yet implemented. See TODO_MVP.md[/dim]")
    
    # TODO: Implement Solana wallet
    # from src.blockchain import WalletManager
    # wallet_mgr = WalletManager()
    # if create:
    #     wallet_mgr.create()
    # if balance:
    #     wallet_mgr.show_balance()


def main():
    """Main entry point."""
    cli(obj={})


if __name__ == "__main__":
    main()
