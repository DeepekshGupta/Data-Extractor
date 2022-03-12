import re
import json
import sys

def parse_regex(name):
    
    text_file_path = r'extracted' + "/" + name
    fhandle = open(text_file_path, "r")
    #print(text_file_path)
    inp = fhandle.read()
    #inp=content
    #print(len(inp))

    fhandle = open(text_file_path, "r")
    #print(fhandle)
    the_dict = dict()


    invoice_key_values_list = ['pdf_name', 'all_emails', 'Sender_name','Sender_address', 'Receiver_name', 'Receiver_address', 'Billing_detail_name','Billing_address', 'address_line', 'name_line', 'for_line', 'from_line', 'To_Line', 'invoice_number','receipt_number', 'order_number', 'issue_date', 'duedate','payment_date', 'total', 'subtotal','amount_paid', 'tax', 'Tax_Rate', 'discount', 'all_phone_numbers_10_digits', 'all_dates']
    
   
    for keys in invoice_key_values_list:
        the_dict.setdefault(keys, [])
    #---------------------------------------------------------
    alist = list()
   # print(name)
    m = re.search('\S+_(\S+)\.\S+', name)
    #print(m)
    # m = m.group(1)#-----------------------------------------------------------------CHANGES1
    # the_dict['pdf_name'].append(m)--------------------------------------------------CHANGES3
    # for name
    switch_invoice_reciever = 0
    string_invoice_reciever = ''

    switch_invoice_sender = 0
    string_invoice_sender = ''

    switch_invoice_bill_to = 0
    string_invoice_bill_to = ''

    # for address
    reciever_address_switch = 0
    reciever_address_string = ''

    sender_address_switch = 0
    sender_address_string = ''

    reciever_billing_address_switch = 0
    reciever_billing_address_string = ''
    #---------------------------------------------------------

    for lines in fhandle:
        line = lines.rstrip()

        #1-------------------------------parsing reciever name#2---------------------------
        if(switch_invoice_reciever == 1):
            if(line == ""):
                continue
            else:
                string_invoice_reciever = line
                the_dict['Receiver_name'].append(string_invoice_reciever)
                switch_invoice_reciever = 0
                reciever_address_switch = 1
                continue
    #2-------------------------------parsing bill to name#2---------------------------
        if(switch_invoice_bill_to == 1):
            if(line == ""):
                continue
            else:
                string_invoice_bill_to = line
                the_dict['Billing_detail_name'].append(string_invoice_bill_to)
                switch_invoice_bill_to = 0
                reciever_billing_address_switch == 1
                continue

    #3----------------------------- parsing sender's name#2 ----------------------------
        if(switch_invoice_sender == 1):
            if(line == ""):
                continue
            else:
                string_invoice_sender = line
                the_dict['Sender_name'].append(string_invoice_sender)
                switch_invoice_sender = 0
                sender_address_switch = 1
                continue
    #4------------------------- parsing reciever's address #1-----------------
        if(reciever_address_switch == 1):
            if(line == ""):
                continue
            else:
                reciever_address_string = line
                the_dict['Receiver_address'].append(reciever_address_string)
                reciever_address_switch = 0

    #5-------------------------parsing sender's address #1--------------------------
        if(sender_address_switch == 1):
            if(line == ""):
                continue
            else:
                sender_address_string = line
                the_dict['Sender_address'].append(sender_address_string)
                sender_address_switch = 0

    #6------------------------- parsing billing address #1-----------------
        if(reciever_billing_address_switch == 1):
            if(line == ""):
                continue
            else:
                reciever_billing_address_string = line
                the_dict['Billing_address'].append(reciever_billing_address_string)
                reciever_billing_address_switch = 0

    #24---------------------------------------------------------------------
        if re.match('From.?(.{2,})', line, re.I):
            m = re.search('From.?(.{2,})', line, re.I)
            m = m.group(1)
            if (m != None):
                the_dict['from_line'].append(m)
                continue

    #26---------------------------------------------------------------------
        if re.match('To:(.{2,})', line, re.I):
            m = re.search('To.?(.{2,})', line, re.I)
            m = m.group(1)
            if (m != None):
                the_dict['To_Line'].append(m)
                continue

    #1---------------------------parsing invoice reciever #1-------------------------------
        if re.match(r'(To[:,]|Ship.?To[:,]?)', line, re.I):
            switch_invoice_reciever = 1
        #works for To:/To,/Ship to:/Ship to,/Shop with case ignorance

    #2---------------------------parsing billing name #1---------------------------
        if re.match(r'(Bill.?To[:,]?)', line, re.I):
            switch_invoice_bill_to = 1

    #3----------------------------parsing invoice sender name#1-------------------------------
        if re.match(r'From[:,]?', line, re.I):
            switch_invoice_sender = 1
        #works for From/From:/From, with case ignorance

    #7----------------------------parsing invoice number-------------------------------
        if re.search(r'invoice [#n].*', line, re.I):
            m = re.search('(\w+.\d+|\d+)', line)
            if (m != None):
                the_dict['invoice_number'].append(m.group(0))
                continue
        #works for invoice #/invoice num/invoice number with case ignorance

    #8----------------------------parsing receipt number-------------------------------
        if re.search(r'receipt [#n].*', line, re.I):
            m = re.search('\d+', line)
            if (m != None):
                the_dict['receipt_number'].append(m.group(0))
                continue

    #9-------------------------------parsing order number-----------------------------
        if re.match(r'order [#n]', line, re.I):
            m = re.search('\d+', line)
            if (m != None):
                the_dict['order_number'].append(m.group(0))
                continue
        #works for order #/order num/order number with case ignorance

    #10--------------------------------parsing issue date----------------------------
        if re.match(r'(date|date of issue|invoice date)', line, re.I):
            #matches = re.findall('(\d\d?|^[jfmasond]\w+)[/ ](\d\d?|\w+)[,/].?\d{4}', line)
            m = re.search('(\d\d?|\w+)[/ ](\d\d?|\w+)[,/].?\d{4}', line)
            if (m != None):
                the_dict['issue_date'].append(m.group(0))
                
        #works for lines strarting with date|date of issue|invoice date with date format
        # XX/XX/20XX , XX Month 20XX, Month XX 20XX, X/X/20XX

    #11--------------------------------parsing invoice due date----------------------------
        if re.match(r'due date', line, re.I):
            m = re.search('(\d\d?|\w+)[/ ](\d\d?|\w+)[,/].?\d{4}', line)
            if (m != None):
                the_dict['duedate'].append(m.group(0))
                
        #works for lines strarting with 'due date' with date format
        # XX/XX/20XX , XX Month 20XX, Month XX 20XX

    #12--------------------------------parsing receipt payment date----------------------------
        if re.match(r'payment date', line, re.I):
            m = re.search('(\d\d?|\w+)[/ ](\d\d?|\w+)[,/].?\d{4}', line)
            if (m != None):
                the_dict['payment_date'].append(m.group(0))
                

    #13------------------------------parsing the total amount---------------------------
        if re.match('Total', line, re.I):
            matches = re.findall('\d*,*\d*,*\d*\.\d{0,2}', line)
            for m in matches:
                the_dict['total'].append(m)
                continue
        #works for line starting with total and extracting the numerical part that line

    #14------------------------------parsing the subtotal-------------------------------

        if re.match('^Sub.?Total', line, re.I):
            m = re.search('\d*,*\d*,*\d*\.\d{0,2}', line)
            if (m != None):
                the_dict['subtotal'].append(m.group(0))
                continue
        #works for line starting with Subtotal/ Sub Total/ Sub-Total and extracting the numerical part that line

    #25---------------------------------------------------------------------
        if re.match('Tax Rate', line, re.I):
            m = re.search('\d*,*\d*,*\d*\.\d{0,2}', line)
            if (m != None):
                the_dict['Tax_Rate'].append(m.group(0))
                continue
    #15-------------------------------parsing sales tax/tax fields--------------------
        if re.match(r'Sales.?tax|tax', line, re.I):
            m = re.search('\d*,*\d*,*\d*\.\d{0,2}', line)
            if (m != None):
                the_dict['tax'].append(m.group(0))
                continue

    #16----------------------------parsing discount fields------------------------------
        if re.match(r'discount', line, re.I):
            m = re.search('\d*,*\d*,*\d*\.\d{0,2}', line)
            if (m != None):
                the_dict['discount'].append(m.group(0))
                continue

    #17-------------------------parsing all the phone numbers(10 digits)--------------------------
        if re.search(r'(\d{3}.?\d{3}.?\d{4})', line):
            m = re.search('(\d{3}.?\d{3}.?\d{4})', line)
            if (m != None):
                the_dict['all_phone_numbers_10_digits'].append(m.group(0))
                continue
    #18--------------------------------parsing all the dates---------------------------------
        if re.search(r'(\d\d?|\w+)[-/ ](\d\d?|\w+)[-,/].?\d{4}', line, re.I):
            #matches = re.findall('(\d\d?|^[jfmasond]\w+)[/ ](\d\d?|\w+)[,/].?\d{4}', line)
            m = re.search('(\d\d?|\w+)[/ ](\d\d?|\w+)[,/].?\d{4}', line)
            if (m != None):
                the_dict['all_dates'].append(m.group(0))
                continue

    #19----------------------------capturing all email address------------------------------
        if re.search(r'\S+@\S+\.\S+', line):
            blist= re.findall('\S+@\S+.\S+', line)
            alist.append(blist[0])
            for values in alist:
                if(values not in the_dict['all_emails']):
                    the_dict['all_emails'].append(values)
                    continue

    #20------------------------------parsing the total amount---------------------------
        if re.match('(amount paid|paid)', line, re.I):
            matches = re.findall('\d*,*\d*,*\d*\.\d{0,2}', line)
            for m in matches:
                the_dict['amount_paid'].append(m)
                continue

    #21------------------------------parsing address line-------------------------------
        if re.search('Address.?(.+)', line, re.I):
            m = re.search('Address.?(.+)', line, re.I)
            m = m.group(1)
            # print(m)
            if (m != None):
                the_dict['address_line'].append(m)
                continue

    #22--------------------------------------------------------------------
        if re.search('Name.?(.+)', line, re.I):
            m = re.search('Name.?(.+)', line, re.I)
            m = m.group(1)
            # print(m)
            if (m != None):
                the_dict['name_line'].append(m)
                continue

    #23--------------------------------------------------------------------
        if re.match('For.?(.+)', line, re.I):
            m = re.search('For.?(.+)', line, re.I)
            m = m.group(1)
            if (m != None):
                the_dict['for_line'].append(m)
                continue



    print(the_dict)
    the_json = json.dumps(the_dict)
    loaded_r = json.loads(the_json)

    return(loaded_r)

# file_name = sys.argv[1]
# print(parse_regex(file_name))