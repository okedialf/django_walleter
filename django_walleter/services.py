from django_walleter import exceptions
from django_walleter.models import Transaction


def check_amount(amount):
    if amount < 0:
        raise exceptions.AmountInvalid()


def verify_withdraw(holder, amount):
    if not holder.can_withdraw(amount):
        raise exceptions.InsufficientFunds()


def get_wallet(wallet):
    from django_walleter.mixins import HasWallet
    if isinstance(wallet, HasWallet):
        wallet = wallet.wallet
    return wallet


def deposit(wallet, amount, meta=None):
    check_amount(amount)

    wallet = get_wallet(wallet)
    wallet.balance += amount
    wallet.save()

    transaction = Transaction(
        type=Transaction.TYPE_DEPOSIT,
        amount=amount,
        to_wallet=wallet,
        meta=meta
    ).save()
    return transaction


def force_withdraw(wallet, amount, meta=None):
    check_amount(amount)
    wallet = get_wallet(wallet)

    wallet.balance -= amount
    wallet.save()

    transaction = Transaction(
        type=Transaction.TYPE_WITHDRAW,
        amount=amount,
        from_wallet=wallet,
        meta=meta
    ).save()
    return transaction


def force_transfer(from_wallet, to_wallet, amount, meta=None):
    check_amount(amount)

    from_wallet = get_wallet(from_wallet)
    to_wallet = get_wallet(to_wallet)

    from_wallet.balance -= amount
    from_wallet.save()
    withdraw = Transaction(
        type=Transaction.TYPE_WITHDRAW,
        amount=amount,
        from_wallet=from_wallet,
        to_wallet=to_wallet,
        meta=meta
    ).save()

    to_wallet.balance += amount
    to_wallet.save()
    deposit = Transaction(
        type=Transaction.TYPE_DEPOSIT,
        amount=amount,
        from_wallet=to_wallet,
        to_wallet=from_wallet,
        meta=meta
    ).save()

    return [withdraw, deposit]
