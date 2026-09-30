import cv2
import numpy

class KalmanFilter:
    def __init__(self):
        # Изменяем размерности для 2D-измерений (x, y)
        self.kf = cv2.KalmanFilter(4, 2)  # 4 состояния, 2 измерения
        
        # Матрица измерений (2x4): измеряем только x и y
        self.kf.measurementMatrix = numpy.array([
            [1, 0, 0, 0],
            [0, 1, 0, 0]
        ], numpy.float32)
        
        # Матрица перехода (4x4): x, y, dx, dy
        self.kf.transitionMatrix = numpy.array([
            [1, 0, 1, 0],
            [0, 1, 0, 1],
            [0, 0, 1, 0],
            [0, 0, 0, 1]
        ], numpy.float32)
        
        # Шумы
        self.kf.processNoiseCov = numpy.eye(4, dtype=numpy.float32) * 0.01
        self.kf.measurementNoiseCov = numpy.eye(2, dtype=numpy.float32) * 0.1

    def update(self, x, y):
        if x is None or y is None:
            # Режим предсказания (без измерений)
            predicted = self.kf.predict()
            return predicted[0, 0], predicted[1, 0]
        
        # Коррекция с измерениями
        measurement = numpy.array([[x], [y]], dtype=numpy.float32)
        self.kf.correct(measurement)
        predicted = self.kf.predict()
        return predicted[0, 0], predicted[1, 0]