"""sentrix.guard — Red teaming, attack heatmap, auto-dataset, agent security, RAG security."""
from sentrix.guard.red_team import red_team, RedTeamReport
from sentrix.guard.fingerprint import fingerprint, ModelFingerprint
from sentrix.guard.auto_dataset import auto_dataset
from sentrix.guard.attacks import PLUGIN_REGISTRY
from sentrix.guard.swarm import scan_swarm, SwarmScanReport
from sentrix.guard.toolchain import scan_toolchain, ToolchainReport
from sentrix.guard.prompt_leakage import prompt_leakage_score, LeakageReport
from sentrix.guard.multilingual import scan_multilingual, MultilingualReport

__all__ = [
    "red_team",
    "RedTeamReport",
    "fingerprint",
    "ModelFingerprint",
    "auto_dataset",
    "PLUGIN_REGISTRY",
    "scan_swarm",
    "SwarmScanReport",
    "scan_toolchain",
    "ToolchainReport",
    "prompt_leakage_score",
    "LeakageReport",
    "scan_multilingual",
    "MultilingualReport",
]
