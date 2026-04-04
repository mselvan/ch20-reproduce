from flask import Flask, request, Response
from lxml import etree
import uuid
from datetime import datetime

app = Flask(__name__)

# ISO 20022 pain.002.001.03 (Customer Payment Status Report)
def build_pain002_xml(msg_id, original_msg_id, status, reason=None):
    """Constructs a pain.002 XML response."""
    ns = "urn:iso:std:iso:20022:tech:xsd:pain.002.001.03"
    root = etree.Element("{%s}Document" % ns, nsmap={None: ns})
    cstmr_pmt_sts_rpt = etree.SubElement(root, "{%s}CstmrPmtStsRpt" % ns)
    
    # Group Header
    grp_hdr = etree.SubElement(cstmr_pmt_sts_rpt, "{%s}GrpHdr" % ns)
    msg_id_elem = etree.SubElement(grp_hdr, "{%s}MsgId" % ns)
    msg_id_elem.text = str(uuid.uuid4())
    cre_dt_tm = etree.SubElement(grp_hdr, "{%s}CreDtTm" % ns)
    cre_dt_tm.text = datetime.now().isoformat()
    
    # Original Group Information
    orgnl_grp_inf = etree.SubElement(cstmr_pmt_sts_rpt, "{%s}OrgnlGrpInfAndSts" % ns)
    orgnl_msg_id_elem = etree.SubElement(orgnl_grp_inf, "{%s}OrgnlMsgId" % ns)
    orgnl_msg_id_elem.text = original_msg_id
    orgnl_msg_nm_id = etree.SubElement(orgnl_grp_inf, "{%s}OrgnlMsgNmId" % ns)
    orgnl_msg_nm_id.text = "pain.001.001.03"
    
    # Original Payment Information
    orgnl_pmt_inf = etree.SubElement(cstmr_pmt_sts_rpt, "{%s}OrgnlPmtInfAndSts" % ns)
    orgnl_pmt_inf_id = etree.SubElement(orgnl_pmt_inf, "{%s}OrgnlPmtInfId" % ns)
    orgnl_pmt_inf_id.text = "PMT-UNKNOWN"  # Simplified
    
    txn_inf = etree.SubElement(orgnl_pmt_inf, "{%s}TxnInfAndSts" % ns)
    sts_id = etree.SubElement(txn_inf, "{%s}StsId" % ns)
    sts_id.text = str(uuid.uuid4())
    
    txn_sts = etree.SubElement(txn_inf, "{%s}TxnSts" % ns)
    txn_sts.text = status # ACTC (Accepted) or RJCT (Rejected)
    
    if reason:
        sts_rsn_inf = etree.SubElement(txn_inf, "{%s}StsRsnInf" % ns)
        rsn = etree.SubElement(sts_rsn_inf, "{%s}Rsn" % ns)
        cd = etree.SubElement(rsn, "{%s}Cd" % ns)
        cd.text = reason
        
    return etree.tostring(root, pretty_print=True, xml_declaration=True, encoding='UTF-8')

def validate_swift_amount(currency, amount_str):
    if currency == "JPY":
        if "." in amount_str:
            decimal_part = amount_str.split(".")[1]
            if decimal_part and int(decimal_part) > 0:
                return False, "CH20"
            return False, "CH20"
    return True, None

@app.route('/upload', methods=['POST'])
def upload_swift_message():
    xml_data = request.data
    try:
        parser = etree.XMLParser(remove_blank_text=True)
        root = etree.fromstring(xml_data, parser)
        ns_pain001 = {'n': 'urn:iso:std:iso:20022:tech:xsd:pain.001.001.03'}
        
        msg_id = root.xpath('//n:MsgId', namespaces=ns_pain001)[0].text
        instd_amt = root.xpath('//n:InstdAmt', namespaces=ns_pain001)[0]
        currency = instd_amt.get('Ccy')
        amount_str = instd_amt.text
        
        is_valid, error_code = validate_swift_amount(currency, amount_str)
        
        if not is_valid:
            print(f"Validation FAILED: {currency} {amount_str} -> {error_code}")
            xml_response = build_pain002_xml(msg_id, msg_id, "RJCT", error_code)
            return Response(xml_response, mimetype='application/xml', status=400)
        
        print(f"Validation SUCCESS: {currency} {amount_str}")
        xml_response = build_pain002_xml(msg_id, msg_id, "ACTC")
        return Response(xml_response, mimetype='application/xml', status=200)

    except Exception as e:
        print(f"Error processing XML: {e}")
        return Response(f"Error: {e}", mimetype='text/plain', status=500)

if __name__ == '__main__':
    print("Starting Professional Mock SWIFT Server (ISO 20022)...")
    app.run(port=5005)
