"""
Filters required for added translation behavior.

See https://docs.openedx.org/projects/openedx-filters for docs.

NOTE that for the pipeline step to be enabled, you must add configuration to your environment's
OPEN_EDX_FILTERS_CONFIG as in translatable_xblocks/settings/devstack.py.
"""

# run_filter can have a number of different args, that is desired behavior
# pylint: disable=arguments-differ

from openedx_filters.filters import PipelineStep

from translatable_xblocks.utils import language_selection_to_django_language


class UpdateRequestLanguageCode(PipelineStep):
    """
    Stop certificate creation if user is not in third party service.
    """

    def run_filter(self, context, student_view_context):
        """Filter step to update language code for requests which have requested a translation."""
        if student_view_context.get("src_lang") and student_view_context.get(
            "dest_lang"
        ):
            translation_language = student_view_context.get("dest_lang")
            context["LANGUAGE_CODE"] = language_selection_to_django_language(
                translation_language
            )

        return context, student_view_context
