TOTAL="Total"
FARE="Fare" # Uber Receipts
SUBTOTAL="Subtotal"
SUB="Sub"
SUB_TOTAL="Sub-Total"
SALES_TAX="Sales Tax"
TAX="Tax"
GST="GST"
PST="PST"
HST_TAX = "HST"
BALANCE_DUE  = 'Balance Due'
AMOUNT_DUE = 'Amount Due'

LOGO_DETECTION = 3
TEXT_DETECTION = 11

CASH = 'Cash'
EFECTIVO = 'efectivo'

GRAND_TOTAL_FIELDS = [
    TOTAL.upper(),
    BALANCE_DUE.upper(),
    FARE.upper(),
    AMOUNT_DUE.upper()
]

SUBTOTAL_FIELDS = [
    SUBTOTAL.upper(),
    SUB.upper(),
    SUB_TOTAL.upper()
]

TAX_FIELDS = [
    SALES_TAX.upper(),
    HST_TAX.upper(),
    TAX.upper(),
    GST.upper(),
    PST.upper()
]

CASH_FIELDS = [
    CASH.upper(),
    EFECTIVO.upper()
]
