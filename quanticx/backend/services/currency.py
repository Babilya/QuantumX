from fastapi import HTTPException

class CurrencyManager:
    def add_bonus(self, user_id: str, amount: float) -> None:
        return None

    def convert(self, from_curr: str, to_curr: str, amount: float) -> None:
        raise HTTPException(status_code=403, detail=(
            "Конвертація між Shadow Talks та Casino Coins заборонена для уникнення зловживань!"
        ))

    def withdraw_casino(self, user_id: str, amount: float) -> None:
        return None

currency_manager = CurrencyManager()
