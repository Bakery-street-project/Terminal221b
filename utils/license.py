"""
Terminal221b License Management Module

Provides tiered licensing for the Polymathic Autonomous Organization (PAO).
Tiers: Free, Pro, Enterprise
"""

import os
import time
from dataclasses import dataclass
from enum import Enum
from typing import Optional, Tuple
from datetime import datetime, timedelta


class LicenseTier(Enum):
    FREE = "free"
    PRO = "pro"
    ENTERPRISE = "enterprise"


@dataclass
class LicenseLimits:
    max_runs_per_day: int
    max_tokens_per_run: int
    max_agents: int
    blockchain_enabled: bool
    priority_support: bool


# Tier configurations
TIER_LIMITS = {
    LicenseTier.FREE: LicenseLimits(
        max_runs_per_day=5,
        max_tokens_per_run=1000,
        max_agents=1,
        blockchain_enabled=False,
        priority_support=False
    ),
    LicenseTier.PRO: LicenseLimits(
        max_runs_per_day=100,
        max_tokens_per_run=10000,
        max_agents=3,
        blockchain_enabled=True,
        priority_support=True
    ),
    LicenseTier.ENTERPRISE: LicenseLimits(
        max_runs_per_day=-1,  # Unlimited
        max_tokens_per_run=-1,  # Unlimited
        max_agents=-1,  # Unlimited
        blockchain_enabled=True,
        priority_support=True
    ),
}


class LicenseManager:
    """Manages license validation and usage tracking."""
    
    def __init__(self):
        self.tier = LicenseTier.FREE
        self.key: Optional[str] = None
        self.daily_runs = 0
        self.last_reset = datetime.now()
        self._initialize()
    
    def _initialize(self):
        """Initialize license from environment variable."""
        self.key = os.environ.get("LICENSE_KEY", "")
        
        if not self.key:
            self.tier = LicenseTier.FREE
            self._print_free_tier_message()
        elif self._validate_key(self.key):
            if self.key.startswith("ENT_"):
                self.tier = LicenseTier.ENTERPRISE
                print("✅ Enterprise License activated - Unlimited usage")
            else:
                self.tier = LicenseTier.PRO
                print("✅ Pro License activated - 100 runs/day, 3 agents")
        else:
            self.tier = LicenseTier.FREE
            print("⚠️  Invalid license key. Falling back to Free Tier.")
            self._print_free_tier_message()
    
    def _validate_key(self, key: str) -> bool:
        """
        Validate license key format.
        TODO: Connect to Gumroad/LemonSqueezy API for real validation.
        """
        if key.startswith("PRO_") and len(key) >= 20:
            return True
        if key.startswith("ENT_") and len(key) >= 20:
            return True
        return False
    
    def can_run(self) -> Tuple[bool, str]:
        """Check if user can perform another run."""
        # Reset daily counter if new day
        if datetime.now() - self.last_reset > timedelta(days=1):
            self.daily_runs = 0
            self.last_reset = datetime.now()
        
        limits = TIER_LIMITS[self.tier]
        
        # Enterprise has unlimited runs
        if limits.max_runs_per_day == -1:
            self.daily_runs += 1
            return True, ""
        
        # Check limits for Free/Pro
        if self.daily_runs >= limits.max_runs_per_day:
            return False, f"Daily limit reached ({self.daily_runs}/{limits.max_runs_per_day} runs). Upgrade at https://bakerstreetproject221B.store/pricing"
        
        self.daily_runs += 1
        return True, ""
    
    def get_limits(self) -> LicenseLimits:
        """Get current tier limits."""
        return TIER_LIMITS[self.tier]
    
    def get_status(self) -> str:
        """Get current license status string."""
        limits = self.get_limits()
        if self.tier == LicenseTier.ENTERPRISE:
            return f"License: {self.tier.value.title()} | Runs today: {self.daily_runs} | Unlimited"
        return f"License: {self.tier.value.title()} | Runs: {self.daily_runs}/{limits.max_runs_per_day} | Agents: {limits.max_agents}"
    
    def can_use_blockchain(self) -> bool:
        """Check if blockchain features are available."""
        return self.get_limits().blockchain_enabled
    
    def get_max_agents(self) -> int:
        """Get maximum number of concurrent agents."""
        return self.get_limits().max_agents
    
    def _print_free_tier_message(self):
        """Print free tier welcome message."""
        print("""
╔════════════════════════════════════════════════════════════════╗
║                    🔓 FREE TIER ACTIVE                         ║
╠════════════════════════════════════════════════════════════════╣
║  Limits: 5 runs/day • 1 agent • No blockchain                  ║
║                                                                ║
║  🚀 Upgrade to Pro: $9/month                                   ║
║     → 100 runs/day • 3 agents • Solana integration             ║
║                                                                ║
║  🏢 Enterprise: Contact us for custom limits                   ║
║     → Unlimited • Custom agents • SLA & support                ║
║                                                                ║
║  ➡️  https://bakerstreetproject221B.store/pricing              ║
║  📧  kiliaan@bakerstreetproject221B.store                      ║
╚════════════════════════════════════════════════════════════════╝
""")


# Singleton instance
_license_manager: Optional[LicenseManager] = None


def get_license() -> LicenseManager:
    """Get or create the license manager singleton."""
    global _license_manager
    if _license_manager is None:
        _license_manager = LicenseManager()
    return _license_manager


def check_license() -> Tuple[bool, str]:
    """Convenience function to check if a run is allowed."""
    return get_license().can_run()


if __name__ == "__main__":
    # Demo usage
    license = get_license()
    print(f"\n{license.get_status()}")
    
    # Test runs
    for i in range(7):
        can_run, msg = license.can_run()
        if can_run:
            print(f"Run {i+1}: ✅ Allowed")
        else:
            print(f"Run {i+1}: ❌ {msg}")
            break
