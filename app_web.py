# import streamlit as st
# import cv2

# st.title("AI Virtual Try-On System")

# run = st.checkbox('Start Camera')

# FRAME_WINDOW = st.image([])

# cap = cv2.VideoCapture(0)

# while run:
#     ret, frame = cap.read()

#     if not ret:
#         st.write("Camera error")
#         break

#     frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)

#     FRAME_WINDOW.image(frame)

# cap.release()
import streamlit as st
import cv2
import mediapipe as mp
import numpy as np

# ---------------- UI ----------------
st.title("AI Virtual Try-On (Web Version)")

run = st.checkbox("Start Camera")

# ---------------- MEDIAPIPE ----------------

mp_face_mesh = mp.solutions.face_mesh.FaceMesh(
    max_num_faces=1,
    refine_landmarks=True
)
# ---------------- LOAD IMAGES ----------------
glasses = cv2.imread("assets/glasses/g1.png", cv2.IMREAD_UNCHANGED)
hat = cv2.imread("assets/hats/h1.png", cv2.IMREAD_UNCHANGED)
necklace = cv2.imread("assets/necklaces/n1.png", cv2.IMREAD_UNCHANGED)

# ---------------- OVERLAY FUNCTION ----------------
def overlay(frame, overlay_img, x, y, w, h):

    overlay_img = cv2.resize(overlay_img, (w, h))

    for i in range(h):
        for j in range(w):

            if y+i >= frame.shape[0] or x+j >= frame.shape[1]:
                continue

            if overlay_img.shape[2] == 4:
                alpha = overlay_img[i, j][3] / 255.0
                color = overlay_img[i, j][:3]
            else:
                alpha = 1
                color = overlay_img[i, j]

            frame[y+i, x+j] = (
                alpha * color +
                (1 - alpha) * frame[y+i, x+j]
            )

    return frame

# ---------------- CAMERA ----------------
cap = cv2.VideoCapture(0)

frame_placeholder = st.image([])

# ---------------- MAIN LOOP ----------------
while run:

    success, frame = cap.read()
    if not success:
        st.warning("Camera not working")
        break

    frame = cv2.flip(frame, 1)
    h, w, _ = frame.shape

    rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
    results = face_mesh.process(rgb)

    if results.multi_face_landmarks:

        for face in results.multi_face_landmarks:

            # -------- EYES --------
            left = face.landmark[33]
            right = face.landmark[263]

            x1, y1 = int(left.x * w), int(left.y * h)
            x2, y2 = int(right.x * w), int(right.y * h)

            gw = int(abs(x2 - x1) * 2.2)
            gh = int(gw * 0.5)

            gx = int(x1 - gw * 0.25)
            gy = int(y1 - gh * 0.5)

            frame = overlay(frame, glasses, gx, gy, gw, gh)

            # -------- HAT --------
            forehead = face.landmark[10]

            fx, fy = int(forehead.x * w), int(forehead.y * h)

            hw = int(gw * 1.5)
            hh = int(hw * 0.8)

            frame = overlay(frame, hat, fx - hw//2, fy - hh - 30, hw, hh)

            # -------- NECKLACE --------
            shoulder = face.landmark[152]

            nx, ny = int(shoulder.x * w), int(shoulder.y * h)

            nw = int(gw * 1.2)
            nh = int(nw * 0.6)

            frame = overlay(frame, necklace, nx - nw//2, ny + 20, nw, nh)

    frame_placeholder.image(cv2.cvtColor(frame, cv2.COLOR_BGR2RGB))

cap.release()
