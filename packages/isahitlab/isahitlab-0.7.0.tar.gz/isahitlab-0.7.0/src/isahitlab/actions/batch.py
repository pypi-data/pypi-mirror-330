from typing import Dict, Optional

from isahitlab.actions.base import BaseAction
from isahitlab.domain.batch import BatchPayload
from isahitlab.operations.batch.create_batch import CreateBatchOperation
from typeguard import typechecked


class BatchActions(BaseAction):
    """Batches actions"""

    @typechecked
    def create_batch(
        self,
        project_id: str,
        name: str,
        disable_progress_bar: Optional[bool] = False
    ) -> Dict:
        """ Create a batch in a project

        Args:
            project_id: ID of the project
            name: Name of the batch
            disable_progress_bar: Disable the progress bar display

        """

        batch = BatchPayload(name=name)

        return CreateBatchOperation(self.http_client).run(project_id=project_id, batch=batch, disable_progress_bar=disable_progress_bar)
