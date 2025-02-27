import io
from typing import List
import matplotlib.image as mpimg
import matplotlib.pyplot as plt
from common.api.get_job import get_job
from common.aws.s3 import S3Downloader

class ImageResult:
    def __init__(self, job_id: str):
        self.image_paths = []
        self.job_id = job_id

    def has_images(self) -> bool:
        job = get_job(self.job_id)

        result_image_file_names = job.get("resultImageFileNames")

        if result_image_file_names:
            self.image_paths = result_image_file_names
            return len(self.image_paths) > 0

        return False

    def _load_image_paths(self) -> List[bytes]:
        if not self.image_paths:
            raise ValueError("No image paths found")
        
        images = [] 
        for image_path in self.image_paths:
            image_bytes = S3Downloader.download_file_to_bytes(self.job_id, image_path)
            images.append(image_bytes)
        
        return images

    def show_images(self):
        images = self._load_image_paths()
        for image in images:
            img = mpimg.imread(io.BytesIO(image), format='png')
            plt.imshow(img)
            plt.axis('off')
            plt.show()
