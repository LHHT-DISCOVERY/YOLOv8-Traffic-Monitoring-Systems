import datetime
import webbrowser

from flask import Flask, jsonify, url_for
from flask import render_template, Response
from flask_cors import CORS
from flask_mysqldb import MySQL
from testHelmet import video_detect_helmet
from testLane import *

app = Flask(__name__, static_folder='static')
CORS(app)

app.config['MYSQL_HOST'] = 'localhost'
app.config['MYSQL_USER'] = 'root'
app.config['MYSQL_PASSWORD'] = '12345'
app.config['MYSQL_DB'] = 'datn'
mysql = MySQL(app)


# Apply Flask CORSx`
# CORS(app)
# app.config['CORS_HEADERS'] = 'Content-Type'
#
@app.route('/test', methods=['GET'])
def get_violate():
    cur = mysql.connection.cursor()
    cur.execute(
        "SELECT nametransportation.vh_name  ,  transportationviolation.date_violate , COUNT(*) AS total_violate FROM transportationviolation INNER JOIN nametransportation ON transportationviolation.id_name = nametransportation.id_name  GROUP BY nametransportation.id_name ;")
    users = cur.fetchall()
    cur.close()
    return jsonify(users)


@app.route('/test1', methods=['GET'])
def get_violate_current():
    cur = mysql.connection.cursor()
    cur.execute(
        "SELECT nametransportation.vh_name  ,   transportationviolation.date_violate , COUNT(*) AS total_violate FROM transportationviolation INNER JOIN nametransportation ON transportationviolation.id_name = nametransportation.id_name  where transportationviolation.date_violate = curdate() GROUP BY nametransportation.id_name ;")
    users = cur.fetchall()
    cur.close()
    return jsonify(users)


# @app.route('/create', methods=['GET'])
def create(cls):
    with app.app_context():
        cur = mysql.connection.cursor()
        ngay_hien_tai = datetime.date.today()
        cur.execute("insert into transportationviolation(id_name , date_violate) values (%s, %s)",
                    (cls + 1, ngay_hien_tai))
        mysql.connection.commit()
        cur.close()
        return jsonify({'message': 'User created successfully'})


def call_route(cls):
    url_for('create', cls=cls)
    # return redirect(url_for('create', cls=cls))


def video_detection(path_x=""):
    cap = cv2.VideoCapture(path_x)
    model = YOLO('best_new/vehicle.pt')
    stt_m = 0
    stt_ctb = 0
    examBB = createBB.infoObject()
    dataBienBan_M = 'F:/python_project/BienBanNopPhatXeMay/ '
    dataBienBan_CTB = 'F:/python_project/BienBanNopPhatXeOTo/ '

    # results = model.track(source="Videos/test4.mp4", show=True, stream=True)
    while cap.isOpened():
        success, frame = cap.read()
        if success:
            #  Dự đoán
            results = model(frame)

            # lấy ra frame sau khi đc gắn nhãn
            annotated_frame = results[0].plot()

            # lấy kích thước (height , width , _ )
            # print("kích thước frame : ", annotated_frame.shape)

            # Hiển thị lên
            # cv2.imshow("Display ", annotated_frame)
            # results = model.track(source="Videos/test4.mp4", show=True, tracker="bytetrack.yaml", stream=True)
            for result in results:
                boxes = result.boxes.numpy()

                # Lấy tên class
                name = result.names

                # lấy tất cả các thông số trong một list tọa độ các đối tượng (x0 ,y0, x1, y1, )
                # print("list 1 ", boxes.xyxy)
                list_2 = []

                # Lấy tất các các thông số của nhiều đối tượng (x0, y0 , x1 , y1 , id ,độ chính xác , loại class)
                # print("Boxes ", boxes)

                for box in boxes:
                    # lấy tên class tương ứng bounding box trong model đã custom
                    # print("Class : ", box.cls)

                    # lấy tọa độ của bounding box đối tượng (x0y0 , x1y1)
                    print("xyxy : ", box.xyxy[0])

                    # Lấy độ chính xác của bounding box đối tượng
                    # print("Độ chính xác : ", box.conf)

                    print("ID------------------- ", box.id)
                    font = cv2.FONT_HERSHEY_SIMPLEX

                    # box.xyxy trả về ma trận 2 chiều dạng [[x0, y0 , x1 ,y1]]
                    # đó là tọa độ bounding box
                    print("box.xyxy", box.xyxy)
                    # org (Tọa độ cần vẽ lên bounding box (x,y) )
                    # thêm int để lấy số nguyên (nghĩa là lấy x0 , y0 để vẽ lên bounding box)
                    org = (int(box.xyxy[0][0]), int(box.xyxy[0][1]))

                    # fontScale (Độ lớn của chữ)
                    fontScale = 0.5

                    # Blue color in RGB (Màu sắc của chữ)
                    color = ()

                    # Line thickness of 2px (Độ dày của chữ )
                    thickness = 2

                    # Lấy tọa độ bounding box
                    x = int(box.xyxy[0][0])
                    y = int(box.xyxy[0][1])
                    w = int(box.xyxy[0][2])
                    h = int(box.xyxy[0][3])

                    text = str(name[box.cls[0]] + " ") + str(round(box.conf[0], 2))

                    #####################################################################
                    # Xe OTO vi pham lane XE MAY
                    start_line_motor = (0 * int(frame.shape[1] / 10), int((2 * frame.shape[0] / 10)))
                    # 11/20 = 5.5 / 10
                    end_line_motor = (11 * int(frame.shape[1] / 20), int(8 * frame.shape[0] / 10))
                    canh_bao_vi_pham_lane_xe_may = start_line_motor[0] < box.xyxy[0][0] < end_line_motor[0] and \
                                                   start_line_motor[1] < box.xyxy[0][
                                                       1] < end_line_motor[1]
                    #####################################################################

                    # ##################################################################
                    # Xe máy vi pham lane OTO
                    # lane xe ô tô (trục y phải khớp với vùng roi)
                    # trục x lấy 6/10 , trục y lấy 3/10
                    start_line_car = (22 * int(frame.shape[1] / 40), int((2 * frame.shape[0] / 10)))

                    # lấy từ 6/10 đến hết trục X , trục y lấy 8/10
                    end_line_car = (int(frame.shape[1]), int(8 * frame.shape[0] / 10))

                    canh_bao_vi_pham_lane_oto = start_line_car[0] < box.xyxy[0][0] < end_line_car[0] and \
                                                start_line_car[1] < box.xyxy[0][
                                                    1] < end_line_car[1]
                    # filterDataViolate(frame, (0, int(5 * frame.shape[0] / 10)),
                    #                   (int(frame.shape[1]), int(55 * frame.shape[0] / 10)))
                    center_x = (x + w) // 2
                    center_y = (y + h) // 2
                    filterData = 0 <= center_x <= (int(frame.shape[1])) and int(
                        5 * frame.shape[0] / 10) <= center_y <= int(
                        52 * frame.shape[0] / 100)
                    #####################################################################

                    # vẽ ra vùng lane xe máy và oto
                    # image = cv2.rectangle(frame, start_line_car, end_line_car
                    #                       , (0, 0, 255), thickness)
                    image = cv2.rectangle(frame, start_line_motor, end_line_motor
                                          , (255, 0, 255), thickness)

                    # xét vùng roi theo trục Y
                    if int((2 * frame.shape[0]) / 10) < int(box.xyxy[0][1]) < int((8 * frame.shape[0]) / 10):
                        cv2.rectangle(frame, (x, y), (w, h), (36, 255, 12), 2)
                        cv2.circle(frame, (center_x, center_y), 5, (0, 0, 255), -1)
                        if box.cls[0] == 1:
                            if canh_bao_vi_pham_lane_oto:
                                draw_text(frame, name[box.cls[0]] + " warning", font_scale=0.5,
                                          pos=(int(box.xyxy[0][0]), int(box.xyxy[0][1])),
                                          text_color_bg=(0, 0, 0))
                                print("tọa độ xe máy vi phạm : ", box.xyxy[0])
                                # cắt hình ảnh xe máy
                                # cropped_frame = frame[round(y, 1) - 100:round(y + h, 2) + 100,
                                #                 round(x, 1) - 100: round(x + w, 1) + 100]

                                # Cắt hình làn ô tô
                                # cropped_frame = frame[int((3 * frame.shape[0]) / 10):int((8 * frame.shape[0]) / 10),
                                #                 6 * int(frame.shape[1] / 10):int(frame.shape[1])]
                                if filterData:
                                    stt_m += 1
                                    imageMotorViolate(frame, int((2 * frame.shape[0]) / 10),
                                                      int((8 * frame.shape[0]) / 10), 2 * int(frame.shape[1] / 10),
                                                      int(frame.shape[1]), stt_m)
                                    stt_BB_m = dataBienBan_M + str(stt_m) + '.pdf'
                                    frame_pil = Image.fromarray(cv2.cvtColor(frame, cv2.COLOR_BGR2RGB))
                                    # Tạo tệp tạm thời và lưu ảnh PIL vào đó
                                    temp_image = tempfile.NamedTemporaryFile(suffix='.jpg', delete=False)
                                    frame_pil.save(temp_image.name)
                                    create(box.cls[0])
                                    createBB.bienBanNopPhat(examBB,
                                                            temp_image.name,
                                                            "F:/python_project/data_xe_may_vi_pham/ " + str(
                                                                stt_m) + '.jpg',
                                                            stt_BB_m)
                                    temp_image.close()

                                    # cv2.imwrite("F:\python_project\data_xe_may_vi_pham\ " + str(count) + ".xe_may_lan_lan.jpg",
                                    #             cropped_frame)
                                    # frame = cv2.putText(frame, name[box.cls[0]] + " warning", org, font, fontScale, (0, 0, 255),
                                    #                     thickness, cv2.LINE_AA)
                            else:
                                draw_text(frame, text, font_scale=0.5,
                                          pos=(int(box.xyxy[0][0]), int(box.xyxy[0][1])),
                                          text_color=(255, 255, 255), text_color_bg=(78, 235, 133))
                                # frame = cv2.putText(frame, text, org, font, fontScale,
                                #                     generate_random_color(int(box.cls[0])), thickness,
                                #                     cv2.LINE_AA)
                        if box.cls[0] == 0 or box.cls[0] == 3 or box.cls[0] == 4:
                            if canh_bao_vi_pham_lane_xe_may:
                                draw_text(frame, name[box.cls[0]] + " warning", font_scale=0.5,
                                          pos=(int(box.xyxy[0][0]), int(box.xyxy[0][1])),
                                          text_color_bg=(0, 0, 0))
                                # Cắt hình làn ô tô
                                if filterData:
                                    stt_ctb += 1
                                    cropped_frame = frame[
                                                    int((3 * frame.shape[0]) / 10):int((8 * frame.shape[0]) / 10),
                                                    6 * int(frame.shape[1] / 10):int(frame.shape[1])]
                                    imageCTBViolate(frame, int((2 * frame.shape[0]) / 10),
                                                    int((8 * frame.shape[0]) / 10), 0 * int(frame.shape[1] / 10),
                                                    6 *
                                                    int(frame.shape[1] / 10), stt_ctb)

                                    stt_BB_CTB = dataBienBan_CTB + str(stt_ctb) + '.pdf'
                                    frame_pil = Image.fromarray(cv2.cvtColor(frame, cv2.COLOR_BGR2RGB))
                                    # Tạo tệp tạm thời và lưu ảnh PIL vào đó
                                    temp_image = tempfile.NamedTemporaryFile(suffix='.jpg', delete=False)
                                    frame_pil.save(temp_image.name)
                                    create(box.cls[0])
                                    createBB.bienBanNopPhat(examBB,
                                                            temp_image.name,
                                                            "F:/python_project/data_oto_vi_pham/ " + str(
                                                                stt_ctb) + '.jpg',
                                                            stt_BB_CTB)
                                    temp_image.close()
                            else:
                                draw_text(frame, text, font_scale=0.5,
                                          pos=(int(box.xyxy[0][0]), int(box.xyxy[0][1])),
                                          text_color=(255, 255, 255), text_color_bg=(77, 229, 26))

                    # muốn lấy 5/10 phần của height tính từ trên xuống
                    start_point = (0, int((2 * frame.shape[0]) / 10))
                    # vẽ hết chiều rộng và chiểu cao lấy 9/10
                    end_point = (int(frame.shape[1]), int((8 * frame.shape[0]) / 10))
                    color = (255, 0, 0)
                    thickness = 2

                    # vẽ ra cái ROI
                    image = cv2.rectangle(frame, start_point, end_point, color, thickness)

                    # scale_percent = 30
                    # width = int(image.shape[1] * scale_percent / 100)
                    # height = int(image.shape[0] * scale_percent / 100)
                    # dim = (width, height)

                    # resize Image
                    # resize = cv2.resize(image, dim, interpolation=cv2.INTER_AREA)
                    # cv2.imshow("Roi ", image)
                    yield image
        else:
            break
    cv2.destroyAllWindows()


def generate_frames(path_x):
    yolo_output = video_detection(path_x)
    for detection_ in yolo_output:
        ref, buffer = cv2.imencode('.jpg', detection_)

        frame = buffer.tobytes()
        yield (b'--frame\r\n'
               b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n')


def generate_frames_helmet(path_x):
    yolo_output = video_detect_helmet(path_x)
    for detection_ in yolo_output:
        ref, buffer = cv2.imencode('.jpg', detection_)

        frame = buffer.tobytes()
        yield (b'--frame\r\n'
               b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n')


@app.route("/")
def index():
    return render_template("index.html")


@app.route("/Hethongcamera2")
def camera_2():
    return render_template("HelmetViolate.html")


@app.route("/bb")
def bb():
    return render_template("bb.html")


@app.route("/thongke")
def tk():
    return render_template("thongke.html")


@app.route("/Hethongcamera1")
def camera_1():
    return render_template("LaneViolate.html")


@app.route("/camera1")
def video():
    return Response(generate_frames(path_x="F:/python_project/Videos/main.mp4"),
                    mimetype='multipart/x-mixed-replace; boundary=frame')


@app.route("/camera2")
def video_2():
    return Response(generate_frames_helmet(path_x="Videos/test11.mp4"),
                    mimetype='multipart/x-mixed-replace; boundary=frame')


if __name__ == "__main__":
    webbrowser.open('http://127.0.0.1:8000/')
    app.run(host="0.0.0.0", port=8000, debug=True, use_reloader=True)
