"""Utility functions for working with artefacts."""
import typing as tp

from varats.paper.case_study import CaseStudy
from varats.paper_mgmt.paper_config import get_loaded_paper_config
from varats.report.report import BaseReport
from varats.ts_utils.cli_util import CLIOptionConverter


class CaseStudyConverter(CLIOptionConverter[CaseStudy]):
    """CLI option converter for case studies."""

    @staticmethod
    def value_to_string(
        value: tp.Union[CaseStudy, tp.List[CaseStudy]]
    ) -> tp.Union[str, tp.List[str]]:
        if isinstance(value, tp.List):
            pc = get_loaded_paper_config()
            if value == pc.get_all_case_studies():
                return "all"
            return [f"{cs.project_name}_{cs.version}" for cs in value]
        return f"{value.project_name}_{value.version}"

    @staticmethod
    def string_to_value(
        str_value: tp.Union[str, tp.List[str]]
    ) -> tp.Union[CaseStudy, tp.List[CaseStudy]]:
        pc = get_loaded_paper_config()
        if isinstance(str_value, tp.List):
            return [
                cs for cs_name in str_value
                for cs in pc.get_case_studies(cs_name)
            ]
        if str_value == "all":
            return pc.get_all_case_studies()
        return pc.get_case_studies(str_value)[0]


class ReportTypeConverter(CLIOptionConverter[tp.Type[BaseReport]]):
    """CLI option converter for case studies."""

    @staticmethod
    def value_to_string(
        value: tp.Union[tp.Type[BaseReport], tp.List[tp.Type[BaseReport]]]
    ) -> tp.Union[str, tp.List[str]]:
        if isinstance(value, tp.List):
            raise ValueError("Conversion for lists not implemented.")
        return value.__name__

    @staticmethod
    def string_to_value(
        str_value: tp.Union[str, tp.List[str]]
    ) -> tp.Union[tp.Type[BaseReport], tp.List[tp.Type[BaseReport]]]:
        if isinstance(str_value, tp.List):
            raise ValueError("Conversion for lists not implemented.")
        return BaseReport.REPORT_TYPES[str_value]