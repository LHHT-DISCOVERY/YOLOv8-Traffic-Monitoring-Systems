import datetime

from reportlab.lib.pagesizes import letter
from reportlab.lib.units import inch
from reportlab.pdfgen import canvas


# from reportlab.pdfgen import canvas


def bienBanNopPhat(info, image_origin, image_violate, output_file_path):
    # Tạo đối tượng Canvas với kích thước trang letter
    c = canvas.Canvas(output_file_path, pagesize=letter)
    # dfmetrics.registerFont(TTFont('Arial Unicode', 'ArialUnicode.ttf'))

    # Chèn tiêu đề biên bản phạt
    c.setFont("Helvetica-Bold", 18)
    c.drawString(130, 750, "CONG HOA XA HOI CHU NGHIA VIET NAM")
    c.drawString(170, 730, "DOC LAP - TU DO - HANH PHUC")
    c.drawString(210, 700, "BIEN BAN VI PHAM")

    # Chèn thông tin người vi phạm
    c.setFont("Helvetica-Bold", 12)
    c.drawString(50, 660, "Ho va Ten : {}".format(info['name']))
    c.drawString(50, 630, "Dia Chi Thuong Tru : {}".format(info['address']))
    c.drawString(50, 600, "Bien So Xe : ........................................"
                          "................- THOI GIAN VI PHAM : {}".format(info['date']))

    # Chèn ảnh vi phạm
    c.drawString(50, 570,
                 "Hinh Anh Vi Pham Tu He Thong Giam Sat Giao Thong TP DA NANG( {}".format(info['date']) + " )")
    c.drawImage(image_origin, 50, 300, width=3.5 * inch, height=3.5 * inch)
    c.drawImage(image_violate, 350, 300, width=3 * inch, height=3.5 * inch)

    # Chèn nội dung biên bản phạt
    c.setFont("Helvetica", 12)
    c.drawString(50, 280, "NOI DUNG BIEN BAN PHAT NGUOI :")
    c.drawString(50, 260, "- LOI VI PHAM : {}".format(info['violation']))
    c.drawString(50, 240, "- LOI KHAC (NEU CO) : {}".format(info['violationOther']))
    c.drawString(50, 220, "- MUC PHAT: {} VND".format(info['fine']))
    c.drawString(50, 200, "- HAN NOP PHAT : {}".format(info['deadline']))
    c.drawString(50, 180, "- Y KIEN CUA NGUOI DIEU KHIEN PHUONG TIEN {}".format(info['opinion']))
    c.drawString(100, 130, " NGUOI VI PHAM")
    c.drawString(410, 130, " CAN BO GIAM SAT")

    c.drawString(108, 110, "    KI TEN  ")
    c.drawString(440, 110, "  KI TEN ")

    # Lưu tệp tin PDF
    c.save()


def infoObject():
    ngay_gio_hien_tai = datetime.datetime.now()
    ngay_gio_dinh_dang = ngay_gio_hien_tai.strftime("%d-%m-%Y %H:%M:%S")
    # Thông tin biên bản phạt
    penalty_info = {
        'name': '....................................................................................................................................',
        'address': '....................................................................................................................',
        'date': str(ngay_gio_dinh_dang),
        'violation': 'DI KHONG DUNG LAN XE QUI DINH TAI DOAN DUONG NGUYEN TRI PHUONG',
        'violationOther': '....................................................................................................................',

        'fine': ".....................................................................",
        'deadline': '..................................................................',
        'opinion': ': ...................................................................'
    }
    return penalty_info

# # Đường dẫn đến file ảnh vi phạm
# image_path = "F:\python_project\data_oto_vi_pham\ 35.jpg"
#
# # Đường dẫn đến file biên bản phạt mới
# output_file_path = 'BienBanNopPhatXeOTo/ticket.pdf'
#
# # Gọi hàm để tạo biên bản phạt có chứa hình ảnh
# bienBanNopPhat(infoObject(), image_path, image_path, output_file_path)
