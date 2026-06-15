import cv2
import csv
import os
from datetime import datetime


students = {
    "VIVEK001": "Vivek Lodhi",
    "RAHUL001": "Rahul Sharma",
    "AMAN001": "Aman Verma"
}



detector = cv2.QRCodeDetector()

cap = cv2.VideoCapture(0)

last_qr = ""



if not os.path.exists("attendance.csv"):
    with open("attendance.csv", "w", newline="") as f:
        writer = csv.writer(f)
        writer.writerow(
            ["StudentID", "Name", "Date", "Time"]
        )



while True:

    ret, frame = cap.read()

    if not ret:
        break

    data, bbox, _ = detector.detectAndDecode(frame)

    if bbox is not None:

        bbox = bbox.astype(int)

        for i in range(len(bbox[0])):

            pt1 = tuple(bbox[0][i])

            pt2 = tuple(
                bbox[0][(i + 1) % len(bbox[0])]
            )

            cv2.line(
                frame,
                pt1,
                pt2,
                (0, 255, 0),
                3
            )



    if data:

        name = students.get(
            data,
            "Unknown Student"
        )

        # Show Name on Screen

        cv2.putText(
            frame,
            f"Name: {name}",
            (30, 50),
            cv2.FONT_HERSHEY_SIMPLEX,
            0.8,
            (0, 255, 0),
            2
        )

        # Save Attendance Only Once

        if data != last_qr:

            today = datetime.now().strftime(
                "%Y-%m-%d"
            )

            current_time = datetime.now().strftime(
                "%H:%M:%S"
            )

            with open(
                "attendance.csv",
                "a",
                newline=""
            ) as f:

                writer = csv.writer(f)

                writer.writerow([
                    data,
                    name,
                    today,
                    current_time
                ])

            print(
                f"Attendance Marked: {name}"
            )

            last_qr = data



    cv2.imshow(
        "QR Attendance System",
        frame
    )

    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()