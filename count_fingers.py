import cv2
import mediapipe as mp

cap = cv2.VideoCapture(0)

mp_hands = mp.solutions.hands
mp_drawing = mp.solutions.drawing_utils

hands = mp_hands.Hands(min_detection_confidence=0.8, min_tracking_confidence=0.5)

tipIds = [4, 8, 12, 16, 20]

# Defina uma função para contar os dedos
def countFingers(image, hand_landmarks, handNo=0):
    
    if hand_landmarks:
        #Obtenha todos os pontos de referência da primeira mão visível
        landmarks = hand_landmarks[handNo].landmark
    
        #print(landmarks)
        
        # conte os dedos
        fingers = []
        
        for lm_index in tipIds:
            #Obtenha os valores y da ponta e da parte inferior do dedo
            finger_tip_y = landmarks[lm_index].y
            finger_bottom_y = landmarks[lm_index - 2].y
            
            #Obtenha os valores x da ponta e da parte inferior do polegar
            thumb_tip_x = landmarks[lm_index].x
            thumb_bottom_x = landmarks[lm_index - 2].x
            
            #verifique se algum dedo está aberto ou fechado
            
            if lm_index !=4:
                if finger_tip_y < finger_bottom_y:
                    fingers.append(1)
                    print("Dedo com id ", lm_index, " está Aberto")
                    
                if finger_tip_y > finger_bottom_y:
                    fingers.append(0)
                    print("Dedo com id ", lm_index, " está Fechado")
            
            else:
                
                if thumb_tip_x > thumb_bottom_x:
                    fingers.append(1)
                    print("Polegar aberto")
                    
                if thumb_tip_x < thumb_bottom_x:
                    fingers.append(0)
                    print("Polegar Fechado")
        
        totalFingers = fingers.count(1)
        
        text = f'Dedos:{totalFingers}'
        
        cv2.putText(image, text, (50, 50), cv2.FONT_HERSHEY_SCRIPT_SIMPLEX, 1, (255, 0, 0), 2)
    

# Defina uma função para 
def drawHandLanmarks(image, hand_landmarks):

    # Desenhar as conexões entre os pontos de referência
    if hand_landmarks:

      for landmarks in hand_landmarks:
               
        mp_drawing.draw_landmarks(image, landmarks, mp_hands.HAND_CONNECTIONS)


while True:
    success, image = cap.read()

    image = cv2.flip(image, 1)
    
    # Detecte os pontos de referência das mãos 
    results = hands.process(image)

    # Obtenha a posição do ponto de referência do resultado processado
    hand_landmarks = results.multi_hand_landmarks

    # Desenhe os pontos de referência
    drawHandLanmarks(image, hand_landmarks)

    # Obtenha a posição dos dedos da mão        
    countFingers(image, hand_landmarks)

    cv2.imshow("Controlador de Midia", image)

    # Saia da tela ao pressionar a barra de espaços
    key = cv2.waitKey(1)
    if key == 32:
        break

cv2.destroyAllWindows()
