from typing import Any, Dict, List, Type, TypeVar

from attrs import define as _attrs_define
from attrs import field as _attrs_field

T = TypeVar("T", bound="DeleteCompletedJobResponse200RawFlowPreprocessorModuleSuspendResumeFormSchema")


@_attrs_define
class DeleteCompletedJobResponse200RawFlowPreprocessorModuleSuspendResumeFormSchema:
    """ """

    additional_properties: Dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> Dict[str, Any]:
        field_dict: Dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update({})

        return field_dict

    @classmethod
    def from_dict(cls: Type[T], src_dict: Dict[str, Any]) -> T:
        d = src_dict.copy()
        delete_completed_job_response_200_raw_flow_preprocessor_module_suspend_resume_form_schema = cls()

        delete_completed_job_response_200_raw_flow_preprocessor_module_suspend_resume_form_schema.additional_properties = (
            d
        )
        return delete_completed_job_response_200_raw_flow_preprocessor_module_suspend_resume_form_schema

    @property
    def additional_keys(self) -> List[str]:
        return list(self.additional_properties.keys())

    def __getitem__(self, key: str) -> Any:
        return self.additional_properties[key]

    def __setitem__(self, key: str, value: Any) -> None:
        self.additional_properties[key] = value

    def __delitem__(self, key: str) -> None:
        del self.additional_properties[key]

    def __contains__(self, key: str) -> bool:
        return key in self.additional_properties
