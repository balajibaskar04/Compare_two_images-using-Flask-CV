from flask import Flask, render_template, request
import cv2
import os
import numpy as np
app = Flask(__name__)
import webview


app = Flask(__name__, template_folder= './templates')
window = webview.create_window('compare two images',  app)
# Create a route to the main page
@app.route('/')
def main_page():
    return render_template('divide_the_pages_v1.html')

#
# Create a route to handle the file upload
@app.route('/upload', methods=['POST'])
def handle_upload():
    old = request.form['old']
    new =  request.form['new']
    output_directory =  request.form['text_input']


    image1 = cv2.imread(old)
    image2 = cv2.imread(new)
    # Extract the image file name from the file path
    image_file_name = os.path.basename(old)

    # Convert images to grayscale for difference calculation
    gray_image1 = cv2.cvtColor(image1, cv2.COLOR_BGR2GRAY)
    gray_image2 = cv2.cvtColor(image2, cv2.COLOR_BGR2GRAY)

    # Resize the images to ensure they have the same dimensions
    height, width = gray_image1.shape[:2]
    gray_image2 = cv2.resize(gray_image2, (width, height))

    # Find the absolute difference between the two images
    difference = cv2.absdiff(gray_image1, gray_image2)
    if np.all(difference == 0):
        cv2.imwrite('output_' + image_file_name, image1)
        print("image are identical")
        # Display the result image (optional)
        cv2.imshow('Result Image', image1)
        cv2.waitKey(0)
        cv2.destroyAllWindows()
        return render_template('result_img_identical.html')

    else:
        print("image are not match")

        # Threshold the difference image to highlight the changes
        _, thresholded = cv2.threshold(difference, 30, 255, cv2.THRESH_BINARY)

        # Find contours in the thresholded image
        contours, _ = cv2.findContours(thresholded, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

        # Draw bounding boxes around the differences
        for contour in contours:
            if cv2.contourArea(contour) > 100:  # You can adjust the minimum area to consider as a difference
                x, y, w, h = cv2.boundingRect(contour)
                cv2.rectangle(image1, (x, y), (x + w, y + h), (0, 128, 0), 4)

        # Save the result image
        download_path = output_directory + "/"

        cv2.imwrite(download_path + 'output_' + image_file_name, image1)

        # Display the result image (optional)
        cv2.imshow('Result Image', image1)

        cv2.waitKey(0)
        cv2.destroyAllWindows()
        return render_template('result_img_compare.html')

if __name__ == '__main__':
    #app.run(debug=True)
    webview.start()
