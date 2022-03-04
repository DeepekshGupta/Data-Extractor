import re
import json

def parse_regex(name):
    
    text_file_path = r'extracted' + "/" + name############################################CHANGES2##############################
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
    # m = m.group(1)############################################CHANGES1##############################
    the_dict['pdf_name'].append(m)
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



    # print(the_dict)
    the_json = json.dumps(the_dict)
    loaded_r = json.loads(the_json)

    return(loaded_r)



from pdf2image import convert_from_path
import cv2
import os
import numpy as np
import pytesseract as tess
import json
import multiprocessing
import time
import sys
# the line below can be commented out if you have tesseract added to your PATH. If not, then include the line below.
#tess.pytesseract.tesseract_cmd = r'C:\Program Files\Tesseract-OCR\tesseract.exe'
start = time.time()



# dpath stores the path of the directory where the uploaded files are stored temporarily


# gives coordinates of text boxes - called in future function
def coordinates(arr):
    max_x = int(np.amax(arr, axis=0)[0][0])
    max_y = int(np.amax(arr, axis=0)[0][1])
    min_x = int(np.amin(arr, axis=0)[0][0])
    min_y = int(np.amin(arr, axis=0)[0][1])

    return min_x, min_y, max_x, max_y


# extracts texts from image
def Image2Text(img):
    img_txt = ''
    gap = "\n"
    #resize_val = 1000
    kernel_size = 9
    #(h, w, d) = img.shape

   
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    blurred = cv2.GaussianBlur(gray, (5, 5), 0)
    edged = cv2.Canny(blurred, 50, 200, 255)
    kernel = cv2.getStructuringElement(cv2.MORPH_RECT, (kernel_size, kernel_size))
    dilate = cv2.dilate(edged, kernel, iterations=4)

    # -----------------------Contour detection-----------------------------------------------------
    contours = cv2.findContours(dilate.copy(), cv2.RETR_EXTERNAL,cv2.CHAIN_APPROX_SIMPLE)[0]
    contours = sorted(contours, key=cv2.contourArea, reverse=True)
    len1 = len(contours)

    i = 0
    new_gray = gray
    # ------------------------------extraction of contours and then text-----------------------------------
    while i < len1:
        x1, y1, x2, y2 = coordinates(contours[i])
        cropped = new_gray[y1:y2, x1:x2]  # a text concentrated section of the cropped
        bright = cv2.inRange(cropped, 189, 255)

        #pil_image = Image.fromarray(bright)
        text = tess.image_to_string(bright,lang='eng', config='--psm 6 --oem 1  -c tessedit_char_blacklist=[]|') #-c tessedit_char_whitelist=0123456789abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ#<>(){};: ') # text is ex
        img_txt = img_txt + text + gap

        new_gray[y1:y2, x1:x2] = 255
        i += 1
    # img_txt = img_txt.replace('-\n', '')
    text = "\n".join([ll.rstrip() for ll in img_txt.splitlines() if ll.strip()])
    return text


def execute(path_pdf, name):
    # ------------------------------------------------pdf to img---------------------------------
    pages = convert_from_path(path_pdf)  # converts pdf into set of images, fmt='png'
    count = 0
    content = ''
    for page in pages:
        count += 1
        pil_image = page
        w, h = pil_image.size
        resize_val = 1000
        r = resize_val / w
        dim = (resize_val, int(h * r))
        pil_image = pil_image.resize(dim)
        open_cv_image = np.array(pil_image)
        image = cv2.cvtColor(open_cv_image, cv2.COLOR_RGB2BGR)

        # -------------------------------------------getting text from image------------------------

        document_text = Image2Text(image)
        #corrected_document_text = TextBlob(document_text)  # spellchecker

        content = content + str(document_text)

    # -----------------------------------------------saving it in a text file------------------------------
    name = name.replace('.pdf', '.txt')
    # print(name)
    # text_file_path = 'media/output' + "/" + name
    text_file_path = r'extracted' + "\\" + name
    text_file = open(text_file_path, "w")
    text_file.write(content)
    # print(content)
    
    text_file.close()
    #time.sleep(8)
    print("entering regex")
    # data_json=parse_regex(name)
    # os.remove(path_pdf)
    
    # print(data_json)
    # que.put(data_json)


# dpath = r"media/uploads"
dpath = r"uploads"

def ocr_fun(id):
    if __name__ == '__main__':
        processes = []
        #print(os.cpu_count())
        # global uuid
        # uuid=id
        # temp_json={'id':"" , 'pdfs':[]}
        # dpath = f"media/uploads/{uuid}"
        # queue1 = Queue() #create a queue object
        for filename in os.listdir(dpath):
            #print(filename)
            filepath = dpath + '/' + filename
            
            # pdf_list=[]
            p = multiprocessing.Process(target=execute, args=(filepath, filename))#,queue1))
            processes.append(p)
            # temp_json['id']=uuid


        for process in processes:
            process.start()    

        for process in processes:
            process.join()        
            # p.start()
            # p.join()
            # temp=queue1.get()
            # type(temp)
            #pdf_list.append(queue1.get())
            #print(queue1.get())
            # temp=queue1.get()
            # temp_json['pdfs'].append(temp)
            #temp_json['pdfs'].append(queue1.get())
            # b=json.stringify(temp_json)
            # str1 = b.replace('/\\/g', '')
            #processes.append(p)

        # for process in processes:
        #     process.join()
        # os.rmdir(f'media/uploads/{uuid}')
        end = time.time()
        print("time elapsed: " + str(end - start))
        
        # return temp_json


# file_name = sys.argv[1]
file_name = 2
ocr_fun(file_name)