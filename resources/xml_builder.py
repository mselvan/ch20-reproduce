import uuid
from lxml import etree

def build_swift_xml(record_id, currency, amount):
    """
    Constructs a simplified SWIFT XML message (pain.001).
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

def parse_pain002_response(xml_string):
    """
    Parses a pain.002 XML response and returns status and reason code.
    """
    parser = etree.XMLParser(remove_blank_text=True)
    root = etree.fromstring(xml_string.encode('utf-8'), parser)
    ns = {'n': 'urn:iso:std:iso:20022:tech:xsd:pain.002.001.03'}
    
    txn_sts = root.xpath('//n:TxnSts', namespaces=ns)[0].text
    
    reason_code = ""
    rsn_elem = root.xpath('//n:Cd', namespaces=ns)
    if rsn_elem:
        reason_code = rsn_elem[0].text
        
    return {"status": txn_sts, "reason": reason_code}
