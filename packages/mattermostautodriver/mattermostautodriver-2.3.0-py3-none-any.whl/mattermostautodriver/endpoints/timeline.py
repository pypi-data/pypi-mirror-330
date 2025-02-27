from .base import Base


class Timeline(Base):

    def remove_timeline_event(self, id, event_id):
        """Remove a timeline event from the playbook run

        id: ID of the playbook run whose timeline event will be modified.
        event_id: ID of the timeline event to be deleted

        `Read in Mattermost API docs (Timeline - removeTimelineEvent) <https://api.mattermost.com/#tag/Timeline/operation/removeTimelineEvent>`_

        """
        return self.client.delete(f"/plugins/playbooks/api/v0/runs/{id}/timeline/{event_id}")
