"""
Services for AI Translations.
"""

import json
import logging
from datetime import datetime
from hashlib import sha256

from django.conf import settings
from django.core.exceptions import ObjectDoesNotExist
from edx_django_utils.cache.utils import TieredCache
from edx_rest_api_client.client import OAuthAPIClient
from oauth2_provider.models import Application
from rest_framework import status

from translatable_xblocks.utils import (
    convert_html_to_xml,
    reinsert_base64_images,
    replace_img_base64_with_placeholder,
)

logger = logging.getLogger(__name__)


class AiTranslationService:
    """
    A service which communicates with ai-translations for translation-related tasks.
    """

    def __init__(self):
        """Initialize translations service."""
        self._client = None

    @property
    def client(self):
        """Create client for communicating with ai-translations, singleton."""
        if not self._client:
            self._client = self._init_translations_client()
        return self._client

    def _init_translations_client(self):
        """Initialize OAuth connection to ai-translations."""
        application_name = settings.AI_TRANSLATIONS_OAUTH_APP_NAME

        try:
            oauth_client = Application.objects.get(name=application_name)
            return OAuthAPIClient(
                settings.LMS_ROOT_URL,
                oauth_client.client_id,
                oauth_client.client_secret,
            )
        except ObjectDoesNotExist:
            logger.error(f"OAuth Application {application_name} not found.")
            return None

    @staticmethod
    def get_content_hash(content):
        """Generate hash of provided content, using sha256."""
        return sha256(content.encode("utf-8")).hexdigest()

    @staticmethod
    def cache_key(source_language, target_language, content_hash):
        """Generate cache key, using get_content_hash result for content hash."""
        return f"ai_translation.{source_language}.{target_language}.{content_hash}"

    def translate(
        self,
        content,
        source_language,
        target_language,
        block_id,
        user_id,
        mimetype="text/html",
        cache_override=None,
    ):
        """
        Request translated version of text / HTML from Translations IDA, checking for cached version first.

        Args:
            content: HTML / text / XML content to transform
            source_language: ISO language code of original content
            target_language: ISO language code to translate content into
            block_id: block ID of originating content (if applicable), used only for logging
            user_id: user ID requesting translation, used only for logging

        Kwargs:
            mimetype (default="text/html"): provided in cases that require different handling (e.g. "application/xml")
            cache_override (default=None): arguments for overriding default cache behavior. Options:
            - "reset" instructs Translations IDA to reset the cache entry for this content.
        """
        content_hash = AiTranslationService.get_content_hash(content)
        block_id_str = str(block_id)

        logger.info(
            f"---- XBlock Translation Attempt ---- "
            f"Timestamp: {datetime.now()} "
            f"Block ID: {block_id_str} "
            f"Hash: {content_hash} "
            f"Source Language: {source_language} "
            f"Target Language: {target_language} "
            f"User ID: {user_id} "
            f"Mimetype: {mimetype} "
            f"Cache Override: {cache_override} "
        )

        # Check for cached response first, clearing if requested
        cache_key = AiTranslationService.cache_key(
            source_language, target_language, content_hash
        )
        if cache_override == "reset":
            logger.info(f"Clearing cache for key: {cache_key}")
            TieredCache.delete_all_tiers(cache_key)
        cache_result = TieredCache.get_cached_response(cache_key)

        # Cached response found, return response
        if cache_result.is_found:
            # A cache value of None (specifically where we expect there to be content)
            # is our signal that there was a cached error. Raise to avoid constantly
            # hitting Translations IDA while it may be encountiering issues.
            if cache_result.value is None and content is not None:
                exception_string = (
                    f"Cached failure response: {block_id_str}"
                    "for languages {source_language} to {target_language}"
                )
                logger.error(exception_string)
                raise Exception(exception_string)

            # Else, return value
            logger.info(f"Cached Translated Content: Found for key {cache_key}")
            return cache_result.value

        logger.info(
            f"Cached Translated Content: Not Found, requesting translation for key {cache_key}"
        )

        # Cached copy not found, query Translations IDA
        url = f"{settings.AI_TRANSLATIONS_API_URL}/translate-xblock/"
        headers = {
            "content-type": "application/json",
        }

        # sometimes, we have long base64 images in a content
        # this causes the post request not to get to the ai-translations for some unknown reasons
        # this code is added to prevent base64 images from being tranlsated is they aren't required
        processed_content, base64_images = replace_img_base64_with_placeholder(content)

        payload = {
            "block_id": block_id_str,
            "source_language": source_language,
            "target_language": target_language,
            "content": processed_content,
            "content_hash": content_hash,
            "cache_override": cache_override or "none",
        }
        response = self.client.post(url, data=json.dumps(payload), headers=headers)

        if response.status_code != status.HTTP_200_OK:
            TieredCache.set_all_tiers(
                cache_key, None, settings.REQUEST_CACHE_FAILURE_TIMEOUT
            )
            exception_string = (
                f"Failed to get translation for block: {block_id_str}"
                "for languages {source_language} to {target_language}"
            )
            logger.error(exception_string)
            raise Exception(exception_string)

        translated_content = response.json().get("translated_content")
        if len(base64_images) > 0:
            translated_content = reinsert_base64_images(translated_content, base64_images)

        # XML needs a translation before it can be used in our code.
        if mimetype == "application/xml":
            translated_content = convert_html_to_xml(translated_content)

        # Set cached content
        TieredCache.set_all_tiers(
            cache_key, translated_content, settings.REQUEST_CACHE_SUCCESS_TIMEOUT
        )

        # Return data
        return translated_content

    def get_course_translation_languages(self, course_id):
        """
        Request translation languages available for a course.

        Args:
            course_id: the course_id for the course
        """
        headers = {
            "content-type": "application/json",
        }
        url = f"{settings.AI_TRANSLATIONS_API_URL}/available_languages/"
        response = self.client.get(
            url,
            params={"course_id": course_id},
            headers=headers,
            timeout=settings.AI_TRANSLATIONS_API_TIMEOUT,
        )
        if response.status_code != status.HTTP_200_OK:
            exception_string = f"Failed to get translation languages for course: {course_id}"
            logger.error(exception_string)
            raise Exception(exception_string)

        data = response.json()
        return data['available_unit_translation_languages']

    def post_course_translation_languages(self, data):
        """
        creates/updates translation languages available for a course.

        Args:
            data (dict): Data to send in the post request
        """
        headers = {
            "content-type": "application/json",
        }
        url = f"{settings.AI_TRANSLATIONS_API_URL}/available_languages/"
        response = self.client.post(url, data=json.dumps(data), headers=headers)
        if response.status_code != status.HTTP_200_OK:
            exception_string = (
                f"Failed to create translation languages for course: {data['course_id']}"
            )
            logger.error(exception_string)
            raise Exception(exception_string)

        response_data = response.json()
        return response_data['available_unit_translation_languages']
