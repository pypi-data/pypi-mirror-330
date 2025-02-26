"""
Utilities used across the Translatable XBlocks Repo.
"""
import re

from django.utils.translation import to_language, to_locale

from translatable_xblocks.platform_imports import get_platform_etree_lib

# The Google and Django languages / locales differ. Specifically, while Django includes
# extra region-specific specifiers like Spanish (Spain) vs Spanish (Latin America),
# Google does not. This helps map our requested translation (for Google) to Django.
GOOGLE_TO_DJANGO_LANGUAGE_CODE_MAPPER = {
    "es": "es-419",
    "ko": "ko-kr",
}


def language_selection_to_django_locale(language):
    """Convert requested translation language to Django locale code, if provided."""
    if isinstance(language, str):
        return to_locale(language_selection_to_django_language(language))
    return None


def language_selection_to_django_language(language):
    """Convert requested tranlsation language to Django language code."""
    if isinstance(language, str):
        if language in GOOGLE_TO_DJANGO_LANGUAGE_CODE_MAPPER:
            return GOOGLE_TO_DJANGO_LANGUAGE_CODE_MAPPER[language]
        return to_language(language)
    return None


def convert_html_to_xml(html_style_xml):
    """
    Google does not natively handle translating of XML but does handle HTML.

    For blocks with XML definitions (e.g. problem blocks)

    For translations of blocks with XML definitions (e.g. Problem Block) we have to
    use the HTML translation mode of the Google Translate API. This is the closest we can
    currently get without native XML translation support.

    A "helpful" feature of this though is that the API does a fair amount of
    reformatting. For HTML, they remove invalid tag structures (like any tag inside
    of a <label>) as well as unquote single word attributes in tags. Our XML parser
    fails for unquoted attributes so this feature breaks several problem types.

    The workaround is to parse the translated XML as HTML and rewrite to string. The
    pair of parsers here re-quote the attributes we need quoted with the side effect
    of also wrapping the entire problem in HTML / Body tags, which we strip before
    returning.
    """
    # By parsing as HTML instead of XML, we can read translated data without error
    etree = get_platform_etree_lib()
    parser = etree.HTMLParser()
    wrapped_problem_xml_tree = etree.fromstring(html_style_xml, parser)

    # Unpack problem from automatically-added HTML and Body tags
    problem_xml_tree = wrapped_problem_xml_tree[0][0]
    problem_xml = etree.tostring(problem_xml_tree, encoding="unicode")

    return problem_xml


def replace_img_base64_with_placeholder(content):
    """
    Replace base64 images with placeholder.

    This is needed to prevent the code from sending huge amount of text to Google
    as base64 images are usually single long strings that exceeds Google translate limit.
    """
    base64_images = []
    placeholder_template = "BASE64_IMG_PLACEHOLDER_{index}"

    # Function to replace base64 src with placeholders
    def replace_match(match):
        base64_images.append((match.group(3), match.group(4)))
        placeholder = placeholder_template.format(index=len(base64_images) - 1)
        return f'<img {match.group(1)}src="{placeholder}"'

    # Regex to find <img> tags with base64 src
    img_tag_regex = r'<img\s+([^>]*?)src=(["\'])data:image/(png|jpeg|jpg|gif);base64,([^"\']+)\2'
    processed_content = re.sub(img_tag_regex, replace_match, content)

    return processed_content, base64_images


def reinsert_base64_images(content, base64_images):
    """Replace placeholders with the original base64 string."""
    for index, (image_type, base64_str) in enumerate(base64_images):
        placeholder = f"BASE64_IMG_PLACEHOLDER_{index}"
        content = content.replace(placeholder, f"data:image/{image_type};base64,{base64_str}")
    return content
