from typing import Callable, Literal, TypeVar

import networkx as nx
from strenum import StrEnum

SUNDRY = "諸口"
Account = TypeVar("Account", bound=str)
AccountSundry = Literal["諸口"]


class AccountType(StrEnum):
    Asset = "資産"
    """資産(借方/賃借対照表)"""
    Liability = "負債"
    """負債(貸方/賃借対照表)"""
    Equity = "純資産"
    """純資産(貸方/賃借対照表)"""
    Revenue = "収益"
    """収益(貸方/損益計算書)"""
    Expense = "費用"
    """費用(借方/損益計算書)"""
    Sundry = "諸口"
    """諸口"""

    @property
    def debit(self) -> bool | None:
        """借方(左)ならTrue, 貸方(右)ならFalse, 諸口ならNone"""
        if self == AccountType.Sundry:
            return None
        return self in (AccountType.Asset, AccountType.Expense)

    @property
    def static(self) -> bool | None:
        """賃借対照表ならTrue, 損益計算書ならFalse, 諸口ならNone"""
        if self == AccountType.Sundry:
            return None
        return self in (AccountType.Equity, AccountType.Liability, AccountType.Asset)


def get_account_type_factory(G: nx.DiGraph) -> Callable[[str], AccountType | None]:
    nonabstract_nodes = {
        d["label"]: d.get("account_type")
        for _, d in G.nodes(data=True)
        if not d["abstract"]
    }

    def _(account: str) -> AccountType | None:
        if account == SUNDRY:
            return AccountType.Sundry
        return nonabstract_nodes.get(account)

    return _
