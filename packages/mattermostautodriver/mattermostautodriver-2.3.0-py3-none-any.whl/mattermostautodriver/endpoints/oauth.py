from .base import Base


class Oauth(Base):

    def list_outgoing_o_auth_connections(self, params=None):
        """List all connections

        team_id: Current Team ID in integrations backstage

        `Read in Mattermost API docs (oauth - ListOutgoingOAuthConnections) <https://api.mattermost.com/#tag/oauth/operation/ListOutgoingOAuthConnections>`_

        """
        return self.client.get("""/api/v4/oauth/outgoing_connections""", params=params)

    def create_outgoing_o_auth_connection(self, options=None):
        """Create a connection
        `Read in Mattermost API docs (oauth - CreateOutgoingOAuthConnection) <https://api.mattermost.com/#tag/oauth/operation/CreateOutgoingOAuthConnection>`_

        """
        return self.client.post("""/api/v4/oauth/outgoing_connections""", options=options)

    def get_outgoing_o_auth_connection(self, params=None):
        """Get a connection

        team_id: Current Team ID in integrations backstage

        `Read in Mattermost API docs (oauth - GetOutgoingOAuthConnection) <https://api.mattermost.com/#tag/oauth/operation/GetOutgoingOAuthConnection>`_

        """
        return self.client.get(f"/api/v4/oauth/outgoing_connections/{connection_id}", params=params)

    def update_outgoing_o_auth_connection(self, options=None):
        """Update a connection
        `Read in Mattermost API docs (oauth - UpdateOutgoingOAuthConnection) <https://api.mattermost.com/#tag/oauth/operation/UpdateOutgoingOAuthConnection>`_

        """
        return self.client.put(f"/api/v4/oauth/outgoing_connections/{connection_id}", options=options)

    def delete_outgoing_o_auth_connection(self):
        """Delete a connection
        `Read in Mattermost API docs (oauth - DeleteOutgoingOAuthConnection) <https://api.mattermost.com/#tag/oauth/operation/DeleteOutgoingOAuthConnection>`_

        """
        return self.client.delete(f"/api/v4/oauth/outgoing_connections/{connection_id}")

    def validate_outgoing_o_auth_connection(self, options=None):
        """Validate a connection configuration
        `Read in Mattermost API docs (oauth - ValidateOutgoingOAuthConnection) <https://api.mattermost.com/#tag/oauth/operation/ValidateOutgoingOAuthConnection>`_

        """
        return self.client.post("""/api/v4/oauth/outgoing_connections/validate""", options=options)
