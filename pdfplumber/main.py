import pdfplumber


def crop_pdf_image_source(page, resolution):
    images = page.images

    if images is not None:
        for i, image in enumerate(images):
            boxpoint = (
                image["x0"],
                page.height - image["y1"],
                image["x1"],
                page.height - image["y0"],
            )
            copy_crop = page.crop(boxpoint)
            image_object = copy_crop.to_image(resolution=resolution)
            image_object.save(
                f"./images/image_{page.page_number}_{i}.png", format="png"
            )

    return len(images)


def get_pdf_info(path: str, resolution: int):
    with pdfplumber.open(path) as pdf:
        # Extract the text
        for page in pdf.pages:
            text = page.extract_text()
            print(text)

            # Extract the table data
            tables = page.extract_table()
            if tables is not None:
                for table in tables:
                    print(table)

            # Extract the images
            print(crop_pdf_image_source(page, resolution))
