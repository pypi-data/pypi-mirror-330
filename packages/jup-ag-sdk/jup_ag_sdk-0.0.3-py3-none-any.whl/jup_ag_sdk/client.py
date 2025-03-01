from typing import Dict


class JupiterClient:
    def __init__(self, base_url: str = "https://api.jupiter.ag/v4") -> None:
        self.base_url = base_url

    def get_quote(
        self, input_mint: str, output_mint: str, amount: int
    ) -> Dict[str, str]:
        """Placeholder method for getting a quote"""
        return {
            "inputMint": input_mint,
            "outputMint": output_mint,
            "amount": str(amount),
            "quote": "mocked-quote-data",
        }
