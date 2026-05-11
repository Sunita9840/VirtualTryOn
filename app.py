# import cv2

# cap = cv2.VideoCapture(0)

# while True:
#     success, frame = cap.read()

#     cv2.imshow("Camera", frame)

#     if cv2.waitKey(1) & 0xFF == ord('q'):
#         break

# cap.release()
# cv2.destroyAllWindows()
# import cv2
# import mediapipe as mp

# cap = cv2.VideoCapture(0)

# mp_face_mesh = mp.solutions.face_mesh
# face_mesh = mp_face_mesh.FaceMesh()

# mp_draw = mp.solutions.drawing_utils

# while True:
#     success, frame = cap.read()

#     rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)

#     results = face_mesh.process(rgb)

#     if results.multi_face_landmarks:
#         for face_landmarks in results.multi_face_landmarks:

#             mp_draw.draw_landmarks(
#                 frame,
#                 face_landmarks,
#                 mp_face_mesh.FACEMESH_TESSELATION
#             )

#     cv2.imshow("Face Mesh", frame)

#     if cv2.waitKey(1) & 0xFF == ord('q'):
#         break

# cap.release()
# cv2.destroyAllWindows()

# import cv2
# import mediapipe as mp
# import numpy as np

# cap = cv2.VideoCapture(0)

# mp_face_mesh = mp.solutions.face_mesh
# face_mesh = mp_face_mesh.FaceMesh()

# glasses = cv2.imread("assets/glasses.png", cv2.IMREAD_UNCHANGED)

# while True:
#     success, frame = cap.read()
#     h, w, _ = frame.shape

#     rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
#     results = face_mesh.process(rgb)

#     if results.multi_face_landmarks:
#         for face_landmarks in results.multi_face_landmarks:

#             left_eye = face_landmarks.landmark[33]
#             right_eye = face_landmarks.landmark[263]

#             x1, y1 = int(left_eye.x * w), int(left_eye.y * h)
#             x2, y2 = int(right_eye.x * w), int(right_eye.y * h)

#             glasses_width = abs(x2 - x1) + 80
#             glasses_height = int(glasses_width * 0.5)

#             resized_glasses = cv2.resize(glasses, (glasses_width, glasses_height))

#             x = x1 - 40
#             y = y1 - 40

#         for i in range(glasses_height):
#              for j in range(glasses_width):

#               if y+i >= h or x+j >= w:
#                  continue

#         if resized_glasses.shape[2] == 4:
#             alpha = resized_glasses[i, j][3] / 255.0
#             color = resized_glasses[i, j][:3]
#         else:
#             alpha = 1
#             color = resized_glasses[i, j]

#         frame[y+i, x+j] = (
#             alpha * color +
#             (1 - alpha) * frame[y+i, x+j]
#         )

#     cv2.imshow("Virtual Try On", frame)

#     if cv2.waitKey(1) & 0xFF == ord('q'):
#         break

# cap.release()
# cv2.destroyAllWindows()
import os
os.environ['TF_CPP_MIN_LOG_LEVEL'] = '3'

import warnings
warnings.filterwarnings("ignore")

import cv2
import mediapipe as mp
import numpy as np

# ---------------- Setup ----------------
cap = cv2.VideoCapture(0)

mp_face_mesh = mp.solutions.face_mesh
face_mesh = mp_face_mesh.FaceMesh(
    max_num_faces=1,
    refine_landmarks=True,
    min_detection_confidence=0.5,
    min_tracking_confidence=0.5
)

#glasses = cv2.imread("assets/glasses.png", cv2.IMREAD_UNCHANGED)
# ---------------- LOAD GLASSES ----------------
glasses_list = [
    cv2.imread("assets/glasses/g1.png", cv2.IMREAD_UNCHANGED),
    cv2.imread("assets/glasses/g2.png", cv2.IMREAD_UNCHANGED),
    cv2.imread("assets/glasses/g3.png", cv2.IMREAD_UNCHANGED)
]

# ---------------- LOAD HATS ----------------
hat_list = [
    cv2.imread("assets/hats/h1.png", cv2.IMREAD_UNCHANGED),
    cv2.imread("assets/hats/h2.png", cv2.IMREAD_UNCHANGED),
    cv2.imread("assets/hats/h3.png", cv2.IMREAD_UNCHANGED)
]

# ---------------- LOAD NECKLACES ----------------
necklace_list = [
    cv2.imread("assets/necklaces/n1.png", cv2.IMREAD_UNCHANGED),
    cv2.imread("assets/necklaces/n2.png", cv2.IMREAD_UNCHANGED),
    cv2.imread("assets/necklaces/n3.png", cv2.IMREAD_UNCHANGED)
]
# ---------------- CHECK FILES ----------------
all_images = glasses_list + hat_list + necklace_list

# for img in all_images:
#     if img is None:
#         print("ERROR: One or more PNG files not found!")
#         exit()
image_names = [
    "g1.png", "g2.png", "g3.png",
    "h1.png", "h2.png", "h3.png",
    "n1.png", "n2.png", "n3.png"
]

for img, name in zip(all_images, image_names):
    if img is None:
        print(f"ERROR: {name} not found!")
current_glasses = 0
current_hat = 0
current_necklace = 0

show_hat = True
show_necklace = True
# snapshot
snapshot_count = 0
# if glasses is None:
#     print("ERROR: glasses.png not found!")
#     exit()

# ---------------- Helper Function ----------------
def overlay_image(frame, overlay, x, y, w, h):
    overlay = cv2.resize(overlay, (w, h))

    for i in range(h):
        for j in range(w):

            if y + i >= frame.shape[0] or x + j >= frame.shape[1]:
                continue
            if x + j < 0 or y + i < 0:
                continue
            if overlay.shape[2] == 4:
                alpha = overlay[i, j][3] / 255.0
                color = overlay[i, j][:3]
            else:
                alpha = 1.0
                color = overlay[i, j]

            frame[y + i, x + j] = (
                alpha * color +
                (1 - alpha) * frame[y + i, x + j]
            )

    return frame

# ---------------- Main Loop ----------------
while True:
    success, frame = cap.read()
    if not success:
        break

    frame = cv2.flip(frame, 1)
    h, w, _ = frame.shape

    rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
    results = face_mesh.process(rgb)

    if results.multi_face_landmarks:
        for face_landmarks in results.multi_face_landmarks:

            # Eye landmarks
            left_eye = face_landmarks.landmark[33]
            right_eye = face_landmarks.landmark[263]

            x1, y1 = int(left_eye.x * w), int(left_eye.y * h)
            x2, y2 = int(right_eye.x * w), int(right_eye.y * h)

            # Distance between eyes (auto scaling)
            glasses_width = int(abs(x2 - x1) * 2.2)
            glasses_height = int(glasses_width * 0.5)

            # Position adjustment (centered)
            gx = int(x1 - glasses_width * 0.25)
            gy = int(y1 - glasses_height * 0.5)

            # Overlay
            # frame = overlay_transparent(
            #     frame,
            #     glasses,
            #     x,
            #     y,
            #     glasses_width,
            #     glasses_height
            # )
            frame = overlay_image(
                    frame,
                    glasses_list[current_glasses],
                    gx,
                    gy,
                    glasses_width,
                    glasses_height
               )
            if show_hat:

                forehead = face_landmarks.landmark[10]

                fx = int(forehead.x * w)
                fy = int(forehead.y * h)

                hat_width = int(glasses_width * 1.5)
                hat_height = int(hat_width * 0.8)

                hx = int(fx - hat_width / 2)
                hy = int(fy - hat_height - 40)

                frame = overlay_image(
                     frame,
                      hat_list[current_hat],
                      hx,
                      hy,
                      hat_width,
                      hat_height
                   )
                # ---------------- NECKLACE ----------------
            if show_necklace:

                left_shoulder = face_landmarks.landmark[234]
                right_shoulder = face_landmarks.landmark[454]

                sx1 = int(left_shoulder.x * w)
                sx2 = int(right_shoulder.x * w)

                sy = int(face_landmarks.landmark[152].y * h)

                necklace_width = int(abs(sx2 - sx1) * 1.2)
                necklace_height = int(necklace_width * 0.6)

                nx = int(sx1 - necklace_width * 0.1)
                ny = int(sy + 20)

                frame = overlay_image(
                    frame,
                    necklace_list[current_necklace],
                    nx,
                    ny,
                    necklace_width,
                    necklace_height
                )

    # ---------------- TEXT ----------------
    cv2.putText(
        frame,
        "1-3 Glasses | 4-6 Hats | 7-9 Necklaces",
        (20, 40),
        cv2.FONT_HERSHEY_SIMPLEX,
        0.7,
        (0, 255, 0),
        2
    )

    cv2.putText(
        frame,
        "H = Toggle Hat | N = Toggle Necklace | Q = Quit",
        (20, 80),
        cv2.FONT_HERSHEY_SIMPLEX,
        0.7,
        (0, 255, 0),
        2
    )

    cv2.imshow("AI Virtual Try-On System", frame)

    # ---------------- KEYBOARD ----------------
    key = cv2.waitKey(1) & 0xFF
    # ----------------SCREENSHOT ----------------
    # ---------------- SCREENSHOT ----------------
    if key == ord('s'):
       snapshot_count += 1
       filename = f"snapshot_{snapshot_count}.png"
       cv2.imwrite(filename, frame)
       print(f"Saved: {filename}") 
    # ---------------- GLASSES ----------------
    if key == ord('1'):
        current_glasses = 0

    elif key == ord('2'):
        current_glasses = 1

    elif key == ord('3'):
        current_glasses = 2

    # ---------------- HATS ----------------
    elif key == ord('4'):
        current_hat = 0

    elif key == ord('5'):
        current_hat = 1

    elif key == ord('6'):
        current_hat = 2

    # ---------------- NECKLACES ----------------
    elif key == ord('7'):
        current_necklace = 0

    elif key == ord('8'):
        current_necklace = 1

    elif key == ord('9'):
        current_necklace = 2

    # ---------------- TOGGLE ----------------
    elif key == ord('h'):
        show_hat = not show_hat

    elif key == ord('n'):
        show_necklace = not show_necklace
    # ✅ SCREENSHOT FEATURE
    elif key == ord('s'):
        snapshot_count += 1
        filename = f"snapshot_{snapshot_count}.png"
        cv2.imwrite(filename, frame)
        print(f"Saved: {filename}")

    # ---------------- QUIT ----------------
    elif key == ord('q'):
        break

# ---------------- CLEANUP ----------------
cap.release()
cv2.destroyAllWindows()

#     cv2.imshow("AI Virtual Try-On (Upgraded)", frame)

#     if cv2.waitKey(1) & 0xFF == ord('q'):
#         break

# cap.release()
# cv2.destroyAllWindows()