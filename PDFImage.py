from pdf2image import convert_from_path


class PDFImage:
    def __init__(self, pdf_path):
        self.pdf_file = pdf_path


    def pdf_to_image(self):
    # Store all the pages of the PDF in a variable
        pages = convert_from_path(self.pdf_file, 500)

        # Counter to store images of each page of PDF to image
        image_counter = 1
        # Iterate through all the pages stored above
        for page in pages:

            # Declaring filename for each page of PDF as JPG
            # For each page, filename will be:
            # PDF page 1 -> page_1.jpg
            # PDF page 2 -> page_2.jpg
            # PDF page 3 -> page_3.jpg
            # ....
            # PDF page n -> page_n.jpg
            filename = "page_"+str(image_counter)+".jpg"
            
            # Save the image of the page in system
            page.save(filename, 'JPEG')

            # Increment the counter to update filename
            image_counter += 1
        # print(image_counter)
        return image_counter

