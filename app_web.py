# # import streamlit as st
# # import cv2

# # st.title("AI Virtual Try-On System")

# # run = st.checkbox('Start Camera')

# # FRAME_WINDOW = st.image([])

# # cap = cv2.VideoCapture(0)

# # while run:
# #     ret, frame = cap.read()

# #     if not ret:
# #         st.write("Camera error")
# #         break

# #     frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)

# #     FRAME_WINDOW.image(frame)

# # cap.release()
# import streamlit as st
# import cv2
# import mediapipe as mp
# import numpy as np

# # BaseOptions = mp.tasks.BaseOptions
# # FaceMesh = mp.tasks.vision.FaceLandmarker
# # FaceLandmarkerOptions = mp.tasks.vision.FaceLandmarkerOptions
# # VisionRunningMode = mp.tasks.vision.RunningMode

# # options = FaceLandmarkerOptions(
# #     base_options=BaseOptions(model_asset_path="face_landmarker.task"),
# #     running_mode=VisionRunningMode.IMAGE
# # )

# # face_mesh = FaceLandmarker.create_from_options(options)
# # ---------------- UI ----------------
# st.title("AI Virtual Try-On (Web Version)")

# run = st.checkbox("Start Camera")


# # ---------------- MEDIAPIPE ----------------
# mp_face_mesh = mp.solutions.face_mesh.FaceMesh(
#     max_num_faces=1,
#     refine_landmarks=True,
#     min_detection_confidence=0.5,
#     min_tracking_confidence=0.5
# )
# # ---------------- LOAD IMAGES ----------------
# glasses = cv2.imread("assets/glasses/g1.png", cv2.IMREAD_UNCHANGED)
# hat = cv2.imread("assets/hats/h1.png", cv2.IMREAD_UNCHANGED)
# necklace = cv2.imread("assets/necklaces/n1.png", cv2.IMREAD_UNCHANGED)

# # ---------------- OVERLAY FUNCTION ----------------
# def overlay(frame, overlay_img, x, y, w, h):
#     if overlay_img is None:
#         return frame

#     overlay_img = cv2.resize(overlay_img, (w, h))

#     for i in range(h):
#         for j in range(w):

#             if y+i >= frame.shape[0] or x+j >= frame.shape[1]:
#                 continue

#             if overlay_img.shape[2] == 4:
#                 alpha = overlay_img[i, j][3] / 255.0
#                 color = overlay_img[i, j][:3]
#             else:
#                 alpha = 1
#                 color = overlay_img[i, j]

#             frame[y+i, x+j] = (
#                 alpha * color +
#                 (1 - alpha) * frame[y+i, x+j]
#             )

#     return frame
# # ---------------- PLACEHOLDER ----------------
# frame_placeholder = st.image([])

# # ---------------- CAMERA ----------------
# cap = cv2.VideoCapture(0)

# # frame_placeholder = st.image([])
# if run:
#      while cap.isOpened():

#         ret, frame = cap.read()
#         if not ret:
#             st.warning("Camera not working")
#             break

#         frame = cv2.flip(frame, 1)
#         h, w, _ = frame.shape

#         rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)

#         results = mp_face_mesh.process(rgb)

#         if results.multi_face_landmarks:

#             for face in results.multi_face_landmarks:

#                 # -------- EYES --------
#                 left = face.landmark[33]
#                 right = face.landmark[263]

#                 x1, y1 = int(left.x * w), int(left.y * h)
#                 x2, y2 = int(right.x * w), int(right.y * h)

#                 gw = int(abs(x2 - x1) * 2.2)
#                 gh = int(gw * 0.5)

#                 gx = int(x1 - gw * 0.25)
#                 gy = int(y1 - gh * 0.5)

#                 frame = overlay(frame, glasses, gx, gy, gw, gh)

#                 # -------- HAT --------
#                 forehead = face.landmark[10]

#                 fx, fy = int(forehead.x * w), int(forehead.y * h)

#                 hw = int(gw * 1.5)
#                 hh = int(hw * 0.8)

#                 frame = overlay(frame, hat, fx - hw//2, fy - hh - 30, hw, hh)

#                 # -------- NECKLACE --------
#                 shoulder = face.landmark[152]

#                 nx, ny = int(shoulder.x * w), int(shoulder.y * h)

#                 nw = int(gw * 1.2)
#                 nh = int(nw * 0.6)

#                 frame = overlay(frame, necklace, nx - nw//2, ny + 20, nw, nh)

#         frame_placeholder.image(cv2.cvtColor(frame, cv2.COLOR_BGR2RGB))

# cap.release()
# # # ---------------- MAIN LOOP ----------------
# # while run:

# #     ret, frame = cap.read()
# #     if not success:
# #         st.warning("Camera not working")
# #         break

# #     frame = cv2.flip(frame, 1)
# #     h, w, _ = frame.shape

# #     rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
# #     results =mp_face_mesh.process(rgb_frame)

# #     if results.multi_face_landmarks:

# #         for face in results.multi_face_landmarks:

# #             # -------- EYES --------
# #             left = face.landmark[33]
# #             right = face.landmark[263]

# #             x1, y1 = int(left.x * w), int(left.y * h)
# #             x2, y2 = int(right.x * w), int(right.y * h)

# #             gw = int(abs(x2 - x1) * 2.2)
# #             gh = int(gw * 0.5)

# #             gx = int(x1 - gw * 0.25)
# #             gy = int(y1 - gh * 0.5)

# #             frame = overlay(frame, glasses, gx, gy, gw, gh)

# #             # -------- HAT --------
# #             forehead = face.landmark[10]

# #             fx, fy = int(forehead.x * w), int(forehead.y * h)

# #             hw = int(gw * 1.5)
# #             hh = int(hw * 0.8)

# #             frame = overlay(frame, hat, fx - hw//2, fy - hh - 30, hw, hh)

# #             # -------- NECKLACE --------
# #             shoulder = face.landmark[152]

# #             nx, ny = int(shoulder.x * w), int(shoulder.y * h)

# #             nw = int(gw * 1.2)
# #             nh = int(nw * 0.6)

# #             frame = overlay(frame, necklace, nx - nw//2, ny + 20, nw, nh)

# #     frame_placeholder.image(cv2.cvtColor(frame, cv2.COLOR_BGR2RGB))

# # cap.release()
# 
import streamlit as st
import cv2
import mediapipe as mp
import numpy as np

# ---------------- UI ----------------
st.title("AI Virtual Try-On (Web Version)")

run = st.checkbox("Start Camera")

# ---------------- SIDEBAR (CHANGE ITEMS) ----------------
st.sidebar.title("Try-On Items")

glasses_choice = st.sidebar.selectbox("Glasses", ["g1.png", "g2.png"])
hat_choice = st.sidebar.selectbox("Hat", ["h1.png", "h2.png"])
necklace_choice = st.sidebar.selectbox("Necklace", ["n1.png", "n2.png"])

# ---------------- SCREENSHOT STATE ----------------
if "last_frame" not in st.session_state:
    st.session_state.last_frame = None

# ---------------- MEDIAPIPE ----------------
mp_face_mesh = mp.solutions.face_mesh
face_mesh = mp_face_mesh.FaceMesh(
    static_image_mode=False,
    max_num_faces=1,
    refine_landmarks=True,
    min_detection_confidence=0.5,
    min_tracking_confidence=0.5
)

# ---------------- LOAD IMAGES ----------------
glasses = cv2.imread(f"assets/glasses/{glasses_choice}", cv2.IMREAD_UNCHANGED)
hat = cv2.imread(f"assets/hats/{hat_choice}", cv2.IMREAD_UNCHANGED)
necklace = cv2.imread(f"assets/necklaces/{necklace_choice}", cv2.IMREAD_UNCHANGED)

# ---------------- OVERLAY FUNCTION ----------------
def overlay(frame, overlay_img, x, y, w, h):

    if overlay_img is None:
        return frame

    overlay_img = cv2.resize(overlay_img, (w, h))

    for i in range(h):
        for j in range(w):

            if y+i >= frame.shape[0] or x+j >= frame.shape[1] or y+i < 0 or x+j < 0:
                continue

            if overlay_img.shape[2] == 4:
                alpha = overlay_img[i, j][3] / 255.0
                color = overlay_img[i, j][:3]
            else:
                alpha = 1.0
                color = overlay_img[i, j]

            frame[y+i, x+j] = (
                alpha * color +
                (1 - alpha) * frame[y+i, x+j]
            )

    return frame

# ---------------- CAMERA ----------------
cap = cv2.VideoCapture(0)

frame_placeholder = st.image([])

# ---------------- SCREENSHOT BUTTON ----------------
if st.button("📸 Take Screenshot"):
    if st.session_state.last_frame is not None:
        _, buffer = cv2.imencode(".png", st.session_state.last_frame)
        st.download_button(
            label="Download Image",
            data=buffer.tobytes(),
            file_name="tryon.png",
            mime="image/png"
        )

# ---------------- MAIN ----------------
if run:

    success, frame = cap.read()

    if not success:
        st.warning("Camera not working")
    else:

        frame = cv2.flip(frame, 1)
        h, w, _ = frame.shape

        # ✅ FIXED RGB ISSUE
        rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        results = face_mesh.process(rgb)

        if results.multi_face_landmarks:

            for face in results.multi_face_landmarks:

                # -------- GLASSES --------
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

                frame = overlay(frame, hat, fx - hw // 2, fy - hh - 30, hw, hh)

                # -------- NECKLACE --------
                shoulder = face.landmark[152]
                nx, ny = int(shoulder.x * w), int(shoulder.y * h)

                nw = int(gw * 1.2)
                nh = int(nw * 0.6)

                frame = overlay(frame, necklace, nx - nw // 2, ny + 20, nw, nh)

        # save for screenshot
        st.session_state.last_frame = frame.copy()

        # show frame
        frame_placeholder.image(cv2.cvtColor(frame, cv2.COLOR_BGR2RGB))

cap.release()
