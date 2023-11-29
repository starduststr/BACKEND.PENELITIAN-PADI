import openai
import csv
import cv2
import numpy as np
import tensorflow as tf
from chatGPT import chatGPT

gpt = chatGPT()

SEED = 548
BATCH_SIZE = 64
EPOCHS = 100
LEARNING_RATE = 0.13
IMAGE_SIZE = 112

class Prediction:
    def label(self, label):
        self.get_api_response(label)
    
    def detect(self, img_file):
        model = tf.keras.models.load_model('assets/model_klasifikasi_penyakit_padi.h5', compile=False)
        
        image_path = 'assets/images/'+img_file
        img = cv2.imread(image_path)

        # Periksa apakah gambar berhasil dimuat dengan benar
        if img is not None:
            # Lakukan resizing gambar menggunakan cv2.resize()
            img = cv2.resize(img, (IMAGE_SIZE, IMAGE_SIZE))
            img = np.array(img) / 255.0
            img = np.expand_dims(img, axis=0)
        else :
            return {'status' : '500', 'message' : 'Gambar gagal dimuat!'}, 200

        # Baca data dari file CSV dan masukkan ke dalam 'inv_map'
        input_csv_file = 'assets/dataset_labels.csv'
        inv_map = {}

        # Baca data dari file CSV dan masukkan ke dalam 'inv_map'
        with open(input_csv_file, 'r') as csvfile:
            csvreader = csv.reader(csvfile)
            next(csvreader)  # Skip header row
            for index, row in enumerate(csvreader):
                image_filename, label_name = row
                inv_map[index] = label_name
                
        predict = model.predict(img, verbose=1)
        predicted_class_index = np.argmax(predict[0])
        predicted_label = inv_map[predicted_class_index]

        # print(predicted_label)
        confidence = predict[0][predicted_class_index]
        confidence = round(confidence * 100, 2)
        # print(confidence)
        
        result = {
            'message' : 'success',
            'status' : '200',
            'data' : {
                'prediction': predicted_label,
                'confidence': confidence,
                'image_path': image_path, 
                'file_name' : img_file,
                'description' : gpt.prompt(f'ini adalah label yang saya dapatkan dari prediksi model padi, jelaskan apa itu label {predicted_label} dan gejalanya?'),
                'pengendalian_hayati' : gpt.prompt(f'buatkan saya rekomendasi pengendalian hayati untuk {predicted_label}'),
                'pengendalian_kimiawi' : gpt.prompt(f'buatkan saya rekomendasi pengendalian kimiawi untuk {predicted_label}')
            },
        }

        return result