from celery import shared_task
import requests

from VisionED import settings
#from django.conf import settings
from .models import EducatorUpload
import logging

# Set up logging
logger = logging.getLogger(__name__)


@shared_task
def generate_video(educator_id):
    """
    Task to generate video for the given educator.
    This task calls a FastAPI endpoint to handle the video generation process.
    """
    try:
        # Fetch educator details based on educator_id
        educator_upload = EducatorUpload.objects.get(pk=educator_id)

        # Prepare the data for the FastAPI call
        video_data = {
            "video_path": educator_id,
            "ppt_path": educator_upload.ppt_file.url,
            "image_path": educator_upload.image.url ,
        }

        # Call the FastAPI endpoint to generate the video
        fastapi_url = settings.FASTAPI_VIDEO_GENERATION_URL  # Define in Django settings
        response = requests.post(fastapi_url, json=video_data)

        # Check if the FastAPI call was successful
        if response.status_code == 200:
            logger.info(f"Video successfully generated for educator_id: {educator_id}")
            return f"Video generated successfully for educator_id: {educator_id}"
        else:
            logger.error(f"Failed to generate video for educator_id: {educator_id}, Response: {response.text}")
            return f"Error generating video for educator_id: {educator_id}"

    except EducatorUpload.DoesNotExist:
        error_msg = f"EducatorUpload with id {educator_id} does not exist."
        logger.error(error_msg)
        return error_msg

    except requests.exceptions.RequestException as e:
        error_msg = f"Failed to reach FastAPI service: {str(e)}"
        logger.error(error_msg)
        return error_msg

    except Exception as e:
        error_msg = f"An unexpected error occurred while generating video for educator_id: {educator_id}, Error: {str(e)}"
        logger.error(error_msg)
        return error_msg
