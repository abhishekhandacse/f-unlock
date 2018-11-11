import boto3
import os
# import cv2
# from gtts import gTTS


def speak(audio_string):
    print(audio_string)
#    tts = gTTS(text=audio_string, lang='en', slow=False)
#    tts.save("output.mp3")
#    os.system("mpg321 output.mp3")


# def preprocess_img(img_path):
#     img = cv2.imread(img_path)
#     img = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
#     img = cv2.resize(img, (128, 128))
#     cv2.imwrite(img_path, img)


if __name__ == "__main__":

    client = boto3.client('rekognition')
    source_imgs_path = '/home/pi/Dev/cfehome/media-root/source_imgs'
    target_img_path = '/home/pi/Dev/cfehome/media-root/target.jpg'

    # preprocess_img(target_img_path)

    result = None

    for file_name in sorted(os.listdir(source_imgs_path)):

        if file_name.endswith('jpg') or file_name.endswith('png'):

            # preprocess_img(os.path.join(source_imgs_path, file_name))

            source_img = open(os.path.join(source_imgs_path, file_name), 'rb')
            target_img = open(target_img_path, 'rb')

            # print file_name

            response = client.compare_faces(SimilarityThreshold=70,
                                            SourceImage={'Bytes': source_img.read()},
                                            TargetImage={'Bytes': target_img.read()})

            if response['FaceMatches'] is not None and len(response['FaceMatches']) > 0:
                result = file_name[:len(file_name)-4]
                break

            source_img.close()
            target_img.close()

    if result is not None:
        # speak("welcome")
        speak("Welcome")
    else:
        speak("Denied")

