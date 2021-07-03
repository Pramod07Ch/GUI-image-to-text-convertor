import cv2
import numpy as np
import pytesseract
from scipy import signal
from PIL import Image

# tesseract path link
pytesseract.pytesseract.tesseract_cmd = 'C:\\Program Files\\Tesseract-OCR\\tesseract.exe'


class OCRReader:
    def __init__(self, image_path: str, display_bg: bool=True, display_image: bool=True, display_text: bool=False):
        self.image = cv2.imread(image_path)  # load image
        # Preprocessing
        self.gray_scale = self.to_gray()
        self.gray_array = self.gray_to_array()
        self.background = self.get_background_color()
        if display_bg:
            self.display_image("Background")
        self.mask = self.compute_mask()
        self.processed_image = self.process_image()
        if display_image:
            self.display_image("Processed")
        self.final_image = self.array_to_image()
        self.text = self.get_image_text()

        self.write_output()
        if display_text:
            print(self.text)

    def to_gray(self):
        """
        Convert the image to gray scale
        return: 
            gray scale image
        """
        return cv2.cvtColor(self.image, cv2.COLOR_BGR2GRAY)

    def gray_to_array(self):
        """
        Convert gray image to array
        return:
            gray image in array format
        """
        return np.asarray(self.gray_scale).astype('float32') / 255.0

    def get_background_color(self):
        """
        Estimate 'background' color by a median filter
        return:
            filtered gray image
        """
        return signal.medfilt2d(self.gray_array, 15)

    def display_image(self, image: str = "Background"):
        """
        Display image i.e. background noise or processed image
        Param:
            image : Name of type of image (act as a flag)
        return: 
            None
        """
        if image == "Background":
            cv2.imshow(image, self.background)
        else:  
            # Processed
            cv2.imshow(image, self.processed_image)

        cv2.waitKey(0)  # waits until a key is pressed
        cv2.destroyAllWindows()  # destroys the window showing image

    def compute_mask(self):
        """
        Compute 'foreground' mask as anything that is significantly darker than the background
        return:
            masked image
        """
        return self.gray_array < (self.background - 0.1)

    def process_image(self):
        """
        Return the input value for all pixels in the mask or pure white otherwise
        return:
            selection based on mask image
        """
        return np.where(self.mask, self.gray_array, 1.0)

    def array_to_image(self):
        """
        convert image array back to image format
        return:
            Final image
        """
        processed_image = self.processed_image.astype(np.uint8) * 255
        return Image.fromarray(processed_image)

    def get_image_text(self):
        """
        Apply OCR reading on the filtered image
        return: 
            Text from the image
        """
        return pytesseract.image_to_string(self.final_image)

    def write_output(self, file_name="recognized.txt"):
        """
        output the content to .txt file
        param 
            file_name (str)
        return:
            None. .txt file is saved to local
        """
        text_file = open(file_name, "w")
        text_file.write(self.text)
        text_file.close()


if __name__ == "__main__":
    ocr_object = OCRReader("example_image.png")
