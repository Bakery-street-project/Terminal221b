"""Tests for license management module."""

import os
import pytest
from unittest.mock import patch
from utils.license import (
    LicenseManager, 
    LicenseTier, 
    TIER_LIMITS,
    get_license,
    check_license
)


class TestLicenseValidation:
    """Test license key validation."""
    
    def test_valid_pro_key(self):
        """Pro keys should be valid."""
        manager = LicenseManager.__new__(LicenseManager)
        manager.key = ""
        assert manager._validate_key("PRO_1234567890123456") is True
    
    def test_valid_enterprise_key(self):
        """Enterprise keys should be valid."""
        manager = LicenseManager.__new__(LicenseManager)
        assert manager._validate_key("ENT_1234567890123456") is True
    
    def test_invalid_prefix(self):
        """Keys with invalid prefix should fail."""
        manager = LicenseManager.__new__(LicenseManager)
        assert manager._validate_key("FREE_1234567890123456") is False
    
    def test_too_short_key(self):
        """Short keys should fail."""
        manager = LicenseManager.__new__(LicenseManager)
        assert manager._validate_key("PRO_123") is False
    
    def test_empty_key(self):
        """Empty keys should fail."""
        manager = LicenseManager.__new__(LicenseManager)
        assert manager._validate_key("") is False


class TestFreeTierLimits:
    """Test free tier limitations."""
    
    @patch.dict(os.environ, {}, clear=True)
    def test_free_tier_default(self):
        """No license key should default to free tier."""
        if "LICENSE_KEY" in os.environ:
            del os.environ["LICENSE_KEY"]
        manager = LicenseManager()
        assert manager.tier == LicenseTier.FREE
    
    @patch.dict(os.environ, {}, clear=True)
    def test_free_tier_run_limits(self):
        """Free tier should limit to 5 runs per day."""
        if "LICENSE_KEY" in os.environ:
            del os.environ["LICENSE_KEY"]
        manager = LicenseManager()
        
        # First 5 runs should succeed
        for i in range(5):
            can_run, msg = manager.can_run()
            assert can_run is True, f"Run {i+1} should be allowed"
        
        # 6th run should fail
        can_run, msg = manager.can_run()
        assert can_run is False
        assert "Daily limit reached" in msg


class TestProTierLimits:
    """Test pro tier features."""
    
    @patch.dict(os.environ, {"LICENSE_KEY": "PRO_12345678901234567890"})
    def test_pro_tier_activation(self):
        """Valid Pro key should activate Pro tier."""
        manager = LicenseManager()
        assert manager.tier == LicenseTier.PRO
    
    @patch.dict(os.environ, {"LICENSE_KEY": "PRO_12345678901234567890"})
    def test_pro_tier_limits(self):
        """Pro tier should have higher limits."""
        manager = LicenseManager()
        limits = manager.get_limits()
        assert limits.max_runs_per_day == 100
        assert limits.max_agents == 3
        assert limits.blockchain_enabled is True


class TestEnterpriseTier:
    """Test enterprise tier features."""
    
    @patch.dict(os.environ, {"LICENSE_KEY": "ENT_12345678901234567890"})
    def test_enterprise_activation(self):
        """Valid Enterprise key should activate Enterprise tier."""
        manager = LicenseManager()
        assert manager.tier == LicenseTier.ENTERPRISE
    
    @patch.dict(os.environ, {"LICENSE_KEY": "ENT_12345678901234567890"})
    def test_enterprise_unlimited_runs(self):
        """Enterprise tier should have unlimited runs."""
        manager = LicenseManager()
        
        # Should allow many runs
        for i in range(1000):
            can_run, _ = manager.can_run()
            assert can_run is True


class TestTierLimits:
    """Test tier limit configurations."""
    
    def test_free_tier_limits(self):
        """Free tier should have expected limits."""
        limits = TIER_LIMITS[LicenseTier.FREE]
        assert limits.max_runs_per_day == 5
        assert limits.max_tokens_per_run == 1000
        assert limits.max_agents == 1
        assert limits.blockchain_enabled is False
    
    def test_pro_tier_limits(self):
        """Pro tier should have expected limits."""
        limits = TIER_LIMITS[LicenseTier.PRO]
        assert limits.max_runs_per_day == 100
        assert limits.max_tokens_per_run == 10000
        assert limits.max_agents == 3
        assert limits.blockchain_enabled is True
    
    def test_enterprise_tier_limits(self):
        """Enterprise tier should have unlimited (-1) values."""
        limits = TIER_LIMITS[LicenseTier.ENTERPRISE]
        assert limits.max_runs_per_day == -1
        assert limits.max_tokens_per_run == -1
        assert limits.max_agents == -1


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
