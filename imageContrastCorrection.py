import cv2
import numpy as np
import os
from matplotlib import pyplot as plt
def imageContrastCorrect(path):
  # 이미지 읽기
  # src = cv2.imread(path)
  # # bgr 색공간 이미지를 lab 색공간 이미지로 변환
  # lab = cv2.cvtColor(src, cv2.COLOR_BGR2LAB)
  # # l, a, b 채널 분리
  # l, a, b = cv2.split(lab)
  # # CLAHE 객체 생성
  # clahe = cv2.createCLAHE(clipLimit=2.0,tileGridSize=(8, 8))
  # # CLAHE 객체에 l 채널 입력하여 CLAHE가 적용된 l 채널 생성 
  # l = clahe.apply(l)
  # # l, a, b 채널 병합
  # lab = cv2.merge((l, a, b))
  # # lab 색공간 이미지를 bgr 색공간 이미지로 변환
  # cont_dst = cv2.cvtColor(lab, cv2.COLOR_LAB2BGR)

  # gray = cv2.cvtColor(cont_dst, cv2.COLOR_BGR2GRAY)
  # binary = cv2.adaptiveThreshold(gray, 255, cv2.ADAPTIVE_THRESH_MEAN_C, cv2.THRESH_BINARY, 467, 37)
  # cv2.imwrite(f'./result/result_gray.jpeg', gray)
  # cv2.imwrite(f'./result/result_binary.jpeg', binary)
  image = cv2.imread(path, cv2.IMREAD_GRAYSCALE)
  kernel = np.array([[0, -1, 0],
                   [-1, 5, -1],
                   [0, -1, 0]])
  image_sharp = cv2.filter2D(image, -1, kernel)
  #대상 픽셀을 강조하는 커널을 정의한 후 filter2D() 메소드를 사용하여 이미지에 적용한다.
  cv2.imwrite('./result/result_'+os.path.basename(path), image_sharp)
  return './result/result_'+os.path.basename(path)
