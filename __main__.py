#!/usr/bin/env python3

__author__ = "Rick Myers"

import os

from ledger import GiftCardLedger


if not os.path.isfile('gift_cards.db'):
    GiftCardLedger.initialize_db()
gift_card_ledger = GiftCardLedger()
gift_card_ledger.mainloop()
