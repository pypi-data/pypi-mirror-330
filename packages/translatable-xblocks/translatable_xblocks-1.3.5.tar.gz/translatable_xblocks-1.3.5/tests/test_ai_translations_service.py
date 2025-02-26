"""Tests for the AiTranslationService."""

import json
from hashlib import sha256
from unittest import TestCase
from unittest.mock import Mock, PropertyMock, patch

from django.conf import settings
from edx_django_utils.cache.utils import CachedResponse

from translatable_xblocks.ai_translations_service import AiTranslationService


class TestAiTranslationService(TestCase):
    """Tests for AiTranslationService."""

    @patch.object(AiTranslationService, "client", PropertyMock())
    @patch("translatable_xblocks.ai_translations_service.TieredCache")
    def test_translate(self, mock_cache):
        # Given a valid translations service
        ai_service = AiTranslationService()

        # ... and a cache miss for requested data
        mock_cache.get_cached_response = Mock(
            return_value=CachedResponse(False, "foo", "****")
        )
        mock_cache.set_all_tiers = Mock()

        with patch.object(ai_service.client, "post") as mock_post:
            mock_post.return_value.status_code = 200
            mock_post.return_value.json.return_value = {
                "translated_content": "Esto es una prueba"
            }

            content = "This is a test"
            source_language = "en"
            target_language = "es"
            block_id = "block-v1:foo+bar"
            user_id = "1"

            # When I call "translate"
            ai_service.translate(
                content, source_language, target_language, block_id, user_id
            )

            expected_url = "example.com/api/translate-xblock/"
            expected_post_data = {
                "block_id": block_id,
                "source_language": source_language,
                "target_language": target_language,
                "content": content,
                "content_hash": sha256(content.encode("utf-8")).hexdigest(),
                "cache_override": "none",
            }
            expected_headers = {
                "content-type": "application/json",
            }

            # Then I call the endpoint with the correct data
            mock_post.assert_called_with(
                expected_url,
                data=json.dumps(expected_post_data),
                headers=expected_headers,
            )

    @patch.object(AiTranslationService, "client", PropertyMock())
    @patch("translatable_xblocks.ai_translations_service.TieredCache")
    def test_translate_cached(self, mock_cache):
        # Given a valid translations service
        ai_service = AiTranslationService()

        # ... and a cache hit for requested data
        cached_translated_content = "Esto es una prueba"
        mock_cache.get_cached_response = Mock(
            return_value=CachedResponse(True, "foo", cached_translated_content)
        )
        mock_cache.set_all_tiers = Mock()

        with patch.object(ai_service.client, "post") as mock_post:
            content = "This is a test"
            source_language = "en"
            target_language = "es"
            block_id = "block-v1:foo+bar"
            user_id = "1"

            # When I call "translate"
            translated_content = ai_service.translate(
                content, source_language, target_language, block_id, user_id
            )

            # Then the Translations IDA is NOT called
            mock_post.assert_not_called()
            self.assertEqual(translated_content, cached_translated_content)

    @patch.object(AiTranslationService, "client", PropertyMock())
    @patch("translatable_xblocks.ai_translations_service.TieredCache")
    def test_translate_cache_reset(self, mock_cache):
        # Given a valid translations service
        ai_service = AiTranslationService()

        mock_cache.set_all_tiers = Mock()
        mock_cache.delete_all_tiers = Mock()
        mock_cache.get_cached_response = Mock(
            return_value=CachedResponse(False, "foo", "****")
        )

        with patch.object(ai_service.client, "post") as mock_post:
            content = "This is a test"
            content_hash = (
                "c7be1ed902fb8dd4d48997c6452f5d7e509fbcdbe2808b16bcf4edce4c07d14e"
            )
            source_language = "en"
            target_language = "es"
            block_id = "block-v1:foo+bar"
            user_id = "1"

            mock_post.return_value.status_code = 200
            mock_post.return_value.json.return_value = {
                "translated_content": "Esto es una prueba"
            }

            cache_key = AiTranslationService.cache_key(
                source_language, target_language, content_hash
            )

            # When I call "translate" with a request to reset the cache
            ai_service.translate(
                content,
                source_language,
                target_language,
                block_id,
                user_id,
                cache_override="reset",
            )

            # Then we ask the cache to reset
            mock_cache.delete_all_tiers.assert_called_once_with(cache_key)

            # ... and the Translations IDA IS called
            mock_post.assert_called_once()

            # ... and the cache is set again with newly translated content
            mock_cache.set_all_tiers.assert_called_once()

    @patch.object(AiTranslationService, "client", PropertyMock())
    @patch("translatable_xblocks.ai_translations_service.TieredCache")
    def test_translate_error(self, mock_cache):
        # Given a valid translations service
        ai_service = AiTranslationService()

        mock_cache.set_all_tiers = Mock()
        mock_cache.get_cached_response = Mock(
            return_value=CachedResponse(False, "foo", "****")
        )

        with patch.object(ai_service.client, "post") as mock_post:
            content = "This is a test"
            content_hash = (
                "c7be1ed902fb8dd4d48997c6452f5d7e509fbcdbe2808b16bcf4edce4c07d14e"
            )
            source_language = "en"
            target_language = "es"
            block_id = "block-v1:foo+bar"
            user_id = "1"

            # When there is an error with getting a translation
            mock_post.return_value.status_code = 418

            # Then we raise an exception
            with self.assertRaises(Exception):
                ai_service.translate(
                    content,
                    source_language,
                    target_language,
                    block_id,
                    user_id,
                )

            # And cache an error for a short time
            cache_key = AiTranslationService.cache_key(
                source_language, target_language, content_hash
            )
            mock_cache.set_all_tiers.assert_called_once_with(
                cache_key, None, settings.REQUEST_CACHE_FAILURE_TIMEOUT
            )

    @patch.object(AiTranslationService, "client", PropertyMock())
    @patch("translatable_xblocks.ai_translations_service.TieredCache")
    def test_translate_error_cached(self, mock_cache):
        # Given a valid translations service
        ai_service = AiTranslationService()

        mock_cache.set_all_tiers = Mock()

        with patch.object(ai_service.client, "post") as mock_post:
            content = "This is a test"
            content_hash = (
                "c7be1ed902fb8dd4d48997c6452f5d7e509fbcdbe2808b16bcf4edce4c07d14e"
            )
            source_language = "en"
            target_language = "es"
            block_id = "block-v1:foo+bar"
            user_id = "1"

            # When we ask for a translation, but get a cached error response
            cache_key = AiTranslationService.cache_key(
                source_language, target_language, content_hash
            )
            mock_cache.get_cached_response = Mock(
                return_value=CachedResponse(True, cache_key, None)
            )

            # Then we raise an exception
            with self.assertRaises(Exception):
                ai_service.translate(
                    content,
                    source_language,
                    target_language,
                    block_id,
                    user_id,
                )

        # ... and do NOT call the translations IDA
        mock_post.assert_not_called()

    @patch.object(AiTranslationService, "client", PropertyMock())
    @patch("translatable_xblocks.ai_translations_service.TieredCache")
    @patch("translatable_xblocks.ai_translations_service.convert_html_to_xml")
    def test_translate_xml(self, mock_xml_convert, mock_cache):
        # Given a valid translations service
        ai_service = AiTranslationService()

        # ... and a cache miss for requested data
        mock_cache.get_cached_response = Mock(
            return_value=CachedResponse(False, "foo", "****")
        )
        mock_cache.set_all_tiers = Mock()

        with patch.object(ai_service.client, "post") as mock_post:
            # Translated content from Google follows the HTML spec instead of XML...
            # ... causing some transforms that break XML parsing
            translated_html_style_xml = (
                "<html><body><option correct=False>False</option></body></html>"
            )

            mock_post.return_value.status_code = 200
            mock_post.return_value.json.return_value = {
                "translated_content": translated_html_style_xml
            }

            content = '<option correct="false">Attributes should be quoted</option>'
            source_language = "en"
            target_language = "es"
            block_id = "block-v1:foo+bar"
            user_id = "1"

            # When I call "translate" for XML by specifying an XML mimetype
            ai_service.translate(
                content,
                source_language,
                target_language,
                block_id,
                user_id,
                mimetype="application/xml",
            )

            expected_url = "example.com/api/translate-xblock/"
            expected_post_data = {
                "block_id": block_id,
                "source_language": source_language,
                "target_language": target_language,
                "content": content,
                "content_hash": sha256(content.encode("utf-8")).hexdigest(),
                "cache_override": "none",
            }
            expected_headers = {
                "content-type": "application/json",
            }

            # Then I call the endpoint with the correct data
            mock_post.assert_called_with(
                expected_url,
                data=json.dumps(expected_post_data),
                headers=expected_headers,
            )

            # And call the funciton to convert our HTML to XML
            mock_xml_convert.assert_called_with(translated_html_style_xml)

    @patch.object(AiTranslationService, "client", PropertyMock())
    @patch("translatable_xblocks.ai_translations_service.TieredCache")
    @patch("translatable_xblocks.ai_translations_service.convert_html_to_xml")
    def test_translate_base64_image(self, mock_xml_convert, mock_cache):
        # Given a valid translations service
        ai_service = AiTranslationService()

        # ... and a cache miss for requested data
        mock_cache.get_cached_response = Mock(
            return_value=CachedResponse(False, "foo", "****")
        )
        mock_cache.set_all_tiers = Mock()

        with patch.object(ai_service.client, "post") as mock_post:
            translated_html_style_xml = (
                "<html><body>"
                "<img src='BASE64_IMG_PLACEHOLDER_0' alt='Translated Example'><body></html>"
            )

            translated_html_style_xml_to_convert = (
                "<html><body>"
                "<img src='data:image/png;base64,iVBORw0KGgoAAAANSUhEUgAAAAUA' alt='Translated Example'><body></html>"
            )

            mock_post.return_value.status_code = 200
            mock_post.return_value.json.return_value = {
                "translated_content": translated_html_style_xml
            }

            content = (
                "<html><body>"
                "<img src='data:image/png;base64,iVBORw0KGgoAAAANSUhEUgAAAAUA' alt='Example'><body></html>"
            )
            source_language = "en"
            target_language = "es"
            block_id = "block-v1:foo+bar"
            user_id = "1"

            ai_service.translate(
                content,
                source_language,
                target_language,
                block_id,
                user_id,
                mimetype="application/xml",
            )

            expected_url = "example.com/api/translate-xblock/"
            expected_post_data = {
                "block_id": block_id,
                "source_language": source_language,
                "target_language": target_language,
                "content": (
                    '<html><body>'
                    '<img src="BASE64_IMG_PLACEHOLDER_0" alt=\'Example\'><body></html>'
                ),
                "content_hash": sha256(content.encode("utf-8")).hexdigest(),
                "cache_override": "none",
            }
            expected_headers = {
                "content-type": "application/json",
            }

            # Then I call the endpoint with the correct data
            mock_post.assert_called_with(
                expected_url,
                data=json.dumps(expected_post_data),
                headers=expected_headers,
            )

            # And call the funciton to convert our HTML to XML
            mock_xml_convert.assert_called_with(translated_html_style_xml_to_convert)

    @patch.object(AiTranslationService, "client", PropertyMock())
    @patch("translatable_xblocks.ai_translations_service.TieredCache")
    @patch("translatable_xblocks.ai_translations_service.convert_html_to_xml")
    def test_translate_xml_cached(self, mock_xml_convert, mock_cache):
        # Given a valid translations service
        ai_service = AiTranslationService()
        original_content = (
            '<option correct="false">Attributes should be quoted</option>'
        )

        # ... and a cache hit for requested data
        transformed_and_cached_translation_content = original_content
        mock_cache.get_cached_response = Mock(
            return_value=CachedResponse(
                True, "foo", transformed_and_cached_translation_content
            )
        )
        mock_cache.set_all_tiers = Mock()

        with patch.object(ai_service.client, "post") as mock_post:
            content = original_content
            source_language = "en"
            target_language = "es"
            block_id = "block-v1:foo+bar"
            user_id = "1"

            # When I call "translate" for XML by specifying an XML mimetype
            translated_content = ai_service.translate(
                content,
                source_language,
                target_language,
                block_id,
                user_id,
                mimetype="application/xml",
            )

            # Then the Translations IDA is NOT called
            mock_post.assert_not_called()
            self.assertEqual(
                translated_content, transformed_and_cached_translation_content
            )

            # And we don't re-convert our translation response
            mock_xml_convert.assert_not_called()

    @patch.object(AiTranslationService, "client", PropertyMock())
    def test_get_course_translation_languages(self):
        valid_course_key = "course-v1:edX+DemoX+Demo_Course"
        # Given a valid translations service
        ai_service = AiTranslationService()
        with patch.object(ai_service.client, "get") as mock_get:
            mock_get.return_value.status_code = 200
            mock_get.return_value.json.return_value = {
                "course_id": valid_course_key,
                "available_unit_translation_languages": [{
                    "code": "es",
                    "label": "Spanish",
                    "enabled": True
                }]
            }

            expected_url = "example.com/api/available_languages/"
            expected_response_data = [{
                "code": "es",
                "label": "Spanish",
                "enabled": True
            }]
            expected_headers = {
                "content-type": "application/json",
            }

            response = ai_service.get_course_translation_languages(valid_course_key)

            mock_get.assert_called_with(
                expected_url,
                params={"course_id": valid_course_key},
                headers=expected_headers,
                timeout=15
            )

            self.assertEqual(response, expected_response_data)

    @patch.object(AiTranslationService, "client", PropertyMock())
    def test_get_course_translation_languages_fail(self):
        valid_course_key = "course-v1:edX+DemoX+Demo_Course"
        # Given a valid translations service
        ai_service = AiTranslationService()
        with patch.object(ai_service.client, "get") as mock_get:
            mock_get.return_value.status_code = 400
            mock_get.return_value.json.return_value = {
                "course_id": valid_course_key,
                "available_unit_translation_languages": [{
                    "code": "es",
                    "label": "Spanish",
                    "enabled": True
                }]
            }

            expected_url = "example.com/api/available_languages/"
            expected_headers = {
                "content-type": "application/json",
            }

            with self.assertRaises(Exception):
                ai_service.get_course_translation_languages(valid_course_key)

                mock_get.assert_called_with(
                    expected_url,
                    params={"course_id": valid_course_key},
                    headers=expected_headers,
                )

    @patch.object(AiTranslationService, "client", PropertyMock())
    def test_post_course_translation_languages(self):
        valid_course_key = "course-v1:edX+DemoX+Demo_Course"
        # Given a valid translations service
        ai_service = AiTranslationService()
        with patch.object(ai_service.client, "post") as mock_post:
            mock_post.return_value.status_code = 200
            mock_post.return_value.json.return_value = {
                "course_id": valid_course_key,
                "available_unit_translation_languages": [{
                    "code": "es",
                    "label": "Spanish",
                    "enabled": True
                }]
            }

            expected_url = "example.com/api/available_languages/"
            expected_post_data = {
                "course_id": valid_course_key,
                "available_unit_translation_languages": [{
                    "code": "es",
                    "label": "Spanish",
                    "enabled": True
                }]
            }
            expected_headers = {
                "content-type": "application/json",
            }

            ai_service.post_course_translation_languages(expected_post_data)

            mock_post.assert_called_with(
                expected_url,
                data=json.dumps(expected_post_data),
                headers=expected_headers,
            )

    @patch.object(AiTranslationService, "client", PropertyMock())
    def test_post_course_translation_languages_fail(self):
        valid_course_key = "course-v1:edX+DemoX+Demo_Course"
        # Given a valid translations service
        ai_service = AiTranslationService()
        with patch.object(ai_service.client, "post") as mock_post:
            mock_post.return_value.status_code = 400
            mock_post.return_value.json.return_value = {
                "course_id": valid_course_key,
                "available_unit_translation_languages": [{
                    "code": "es",
                    "label": "Spanish",
                    "enabled": True
                }]
            }

            expected_url = "example.com/api/available_languages/"
            expected_post_data = {
                "course_id": valid_course_key,
                "available_unit_translation_languages": [{
                    "code": "es",
                    "label": "Spanish",
                    "enabled": True
                }]
            }
            expected_headers = {
                "content-type": "application/json",
            }

            with self.assertRaises(Exception):
                ai_service.post_course_translation_languages(expected_post_data)

                mock_post.assert_called_with(
                    expected_url,
                    data=json.dumps(expected_post_data),
                    headers=expected_headers,
                )
