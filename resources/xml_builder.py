import uuid

def build_swift_xml(record_id, currency, amount):
    """
    Constructs a simplified SWIFT XML message.
    """
    return f"""<?xml version="1.0" encoding="UTF-8"?>
<Document xmlns="urn:iso:std:iso:20022:tech:xsd:pain.001.001.03">
    <CstmrCdtTrfInitn>
        <GrpHdr>
            <MsgId>{uuid.uuid4()}</MsgId>
            <CreDtTm>2023-10-27T10:00:00</CreDtTm>
            <NbOfTxs>1</NbOfTxs>
        </GrpHdr>
        <PmtInf>
            <PmtInfId>PMT-{record_id}</PmtInfId>
            <PmtMtd>TRF</PmtMtd>
            <CdtTrfTxInf>
                <PmtId>
                    <EndToEndId>E2E-{record_id}</EndToEndId>
                </PmtId>
                <Amt>
                    <InstdAmt Ccy="{currency}">{amount}</InstdAmt>
                </Amt>
            </CdtTrfTxInf>
        </PmtInf>
    </CstmrCdtTrfInitn>
</Document>
"""
