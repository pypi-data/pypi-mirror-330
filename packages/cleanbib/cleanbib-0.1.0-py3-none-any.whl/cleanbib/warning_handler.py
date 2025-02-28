class WarningHandler:
    """
    A centralized warning handler for cleanbib.
    - Critical warnings: Missing required fields (e.g., title, author, year).
    - Soft warnings: Issues with non-core fields (e.g., DOI not resolving).
    """

    def __init__(self):
        self.critical_warnings = []
        self.soft_warnings = []

    def add_critical(self, message: str):
        """Log a critical warning (e.g., missing essential fields)."""
        self.critical_warnings.append(message)

    def add_soft(self, message: str):
        """Log a soft warning (e.g., a broken DOI)."""
        self.soft_warnings.append(message)

    def has_critical_warnings(self) -> bool:
        """Check if there are critical warnings."""
        return bool(self.critical_warnings)

    def get_warnings(self) -> dict:
        """Return warnings in a structured JSON-friendly format."""
        return {
            "critical": self.critical_warnings,
            "soft": self.soft_warnings
        }

    def get_warnings_text(self) -> str:
        """Return warnings as a plain-text summary (for CLI users)."""
        messages = []
        if self.critical_warnings:
            messages.append("\n🚨 Critical Issues Found:")
            for warning in self.critical_warnings:
                messages.append(f"  ❌ {warning}")

        if self.soft_warnings:
            messages.append("\n⚠️ Soft Warnings (Non-Essential Issues):")
            for warning in self.soft_warnings:
                messages.append(f"  ⚠️ {warning}")

        return "\n".join(messages) if messages else "✅ No issues found. Your bibliography is clean!"
