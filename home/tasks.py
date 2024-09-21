import httpx
from celery import shared_task
import requests
from VisionED import settings
from .models import EducatorUpload, Video
import logging

logger = logging.getLogger(__name__)


#@shared_task
def generate_video(educator_id):
    """
    Task to generate video for the given educator and save the video to the database.
    """
    try:
        # Fetch educator details based on educator_id
        educator_upload = EducatorUpload.objects.get(pk=educator_id)
        print(educator_upload)
        # Prepare the data for the FastAPI call
        video_data = {
            "video_url": str(educator_id),
            "ppt_path": educator_upload.ppt_file.name,
            "image_path": educator_upload.image.name,
        }

        print(video_data)
        # Call the FastAPI endpoint to generate the video
        fastapi_url = settings.FASTAPI_VIDEO_GENERATION_URL
        print(fastapi_url)
        response = httpx.post(
            fastapi_url,
            params=video_data,
        )

        print(response.status_code)
        # Check if the FastAPI call was successful
        if response.status_code == 200:
            # Extract the video file URL or path from the response
            return f"Video generated and saved for course_id: {educator_id}"
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
