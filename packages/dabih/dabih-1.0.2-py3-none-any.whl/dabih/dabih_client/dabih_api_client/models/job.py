from typing import Any, Dict, Type, TypeVar

from attrs import define as _attrs_define

from ..models.job_status import JobStatus

T = TypeVar("T", bound="Job")


@_attrs_define
class Job:
    """
    Attributes:
        job_id (str):
        status (JobStatus):
    """

    job_id: str
    status: JobStatus

    def to_dict(self) -> Dict[str, Any]:
        job_id = self.job_id

        status = self.status.value

        field_dict: Dict[str, Any] = {}
        field_dict.update(
            {
                "jobId": job_id,
                "status": status,
            }
        )

        return field_dict

    @classmethod
    def from_dict(cls: Type[T], src_dict: Dict[str, Any]) -> T:
        d = src_dict.copy()
        job_id = d.pop("jobId")

        status = JobStatus(d.pop("status"))

        job = cls(
            job_id=job_id,
            status=status,
        )

        return job
