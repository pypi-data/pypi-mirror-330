from .base import Base


class DataRetention(Base):

    def get_team_policies_for_user(self, user_id, params=None):
        """Get the policies which are applied to a user's teams

        user_id: The ID of the user. This can also be "me" which will point to the current user.
        page: The page to select.
        per_page: The number of policies per page.

        `Read in Mattermost API docs (data_retention - GetTeamPoliciesForUser) <https://api.mattermost.com/#tag/data_retention/operation/GetTeamPoliciesForUser>`_

        """
        return self.client.get(f"/api/v4/users/{user_id}/data_retention/team_policies", params=params)

    def get_channel_policies_for_user(self, user_id, params=None):
        """Get the policies which are applied to a user's channels

        user_id: The ID of the user. This can also be "me" which will point to the current user.
        page: The page to select.
        per_page: The number of policies per page.

        `Read in Mattermost API docs (data_retention - GetChannelPoliciesForUser) <https://api.mattermost.com/#tag/data_retention/operation/GetChannelPoliciesForUser>`_

        """
        return self.client.get(f"/api/v4/users/{user_id}/data_retention/channel_policies", params=params)

    def get_data_retention_policy(self):
        """Get the global data retention policy
        `Read in Mattermost API docs (data_retention - GetDataRetentionPolicy) <https://api.mattermost.com/#tag/data_retention/operation/GetDataRetentionPolicy>`_

        """
        return self.client.get("""/api/v4/data_retention/policy""")

    def get_data_retention_policies_count(self):
        """Get the number of granular data retention policies
        `Read in Mattermost API docs (data_retention - GetDataRetentionPoliciesCount) <https://api.mattermost.com/#tag/data_retention/operation/GetDataRetentionPoliciesCount>`_

        """
        return self.client.get("""/api/v4/data_retention/policies_count""")

    def get_data_retention_policies(self, params=None):
        """Get the granular data retention policies

        page: The page to select.
        per_page: The number of policies per page.

        `Read in Mattermost API docs (data_retention - GetDataRetentionPolicies) <https://api.mattermost.com/#tag/data_retention/operation/GetDataRetentionPolicies>`_

        """
        return self.client.get("""/api/v4/data_retention/policies""", params=params)

    def create_data_retention_policy(self, options):
        """Create a new granular data retention policy
        `Read in Mattermost API docs (data_retention - CreateDataRetentionPolicy) <https://api.mattermost.com/#tag/data_retention/operation/CreateDataRetentionPolicy>`_

        """
        return self.client.post("""/api/v4/data_retention/policies""", options=options)

    def get_data_retention_policy_by_id(self, policy_id):
        """Get a granular data retention policy

        policy_id: The ID of the granular retention policy.

        `Read in Mattermost API docs (data_retention - GetDataRetentionPolicyByID) <https://api.mattermost.com/#tag/data_retention/operation/GetDataRetentionPolicyByID>`_

        """
        return self.client.get(f"/api/v4/data_retention/policies/{policy_id}")

    def patch_data_retention_policy(self, policy_id, options):
        """Patch a granular data retention policy

        policy_id: The ID of the granular retention policy.

        `Read in Mattermost API docs (data_retention - PatchDataRetentionPolicy) <https://api.mattermost.com/#tag/data_retention/operation/PatchDataRetentionPolicy>`_

        """
        return self.client.patch(f"/api/v4/data_retention/policies/{policy_id}", options=options)

    def delete_data_retention_policy(self, policy_id):
        """Delete a granular data retention policy

        policy_id: The ID of the granular retention policy.

        `Read in Mattermost API docs (data_retention - DeleteDataRetentionPolicy) <https://api.mattermost.com/#tag/data_retention/operation/DeleteDataRetentionPolicy>`_

        """
        return self.client.delete(f"/api/v4/data_retention/policies/{policy_id}")

    def get_teams_for_retention_policy(self, policy_id, params=None):
        """Get the teams for a granular data retention policy

        policy_id: The ID of the granular retention policy.
        page: The page to select.
        per_page: The number of teams per page.

        `Read in Mattermost API docs (data_retention - GetTeamsForRetentionPolicy) <https://api.mattermost.com/#tag/data_retention/operation/GetTeamsForRetentionPolicy>`_

        """
        return self.client.get(f"/api/v4/data_retention/policies/{policy_id}/teams", params=params)

    def add_teams_to_retention_policy(self, policy_id, options):
        """Add teams to a granular data retention policy

        policy_id: The ID of the granular retention policy.

        `Read in Mattermost API docs (data_retention - AddTeamsToRetentionPolicy) <https://api.mattermost.com/#tag/data_retention/operation/AddTeamsToRetentionPolicy>`_

        """
        return self.client.post(f"/api/v4/data_retention/policies/{policy_id}/teams", options=options)

    def remove_teams_from_retention_policy(self, policy_id, params):
        """Delete teams from a granular data retention policy

        policy_id: The ID of the granular retention policy.

        `Read in Mattermost API docs (data_retention - RemoveTeamsFromRetentionPolicy) <https://api.mattermost.com/#tag/data_retention/operation/RemoveTeamsFromRetentionPolicy>`_

        """
        return self.client.delete(f"/api/v4/data_retention/policies/{policy_id}/teams", params=params)

    def search_teams_for_retention_policy(self, policy_id, options):
        """Search for the teams in a granular data retention policy

        policy_id: The ID of the granular retention policy.
        term: The search term to match against the name or display name of teams

        `Read in Mattermost API docs (data_retention - SearchTeamsForRetentionPolicy) <https://api.mattermost.com/#tag/data_retention/operation/SearchTeamsForRetentionPolicy>`_

        """
        return self.client.post(f"/api/v4/data_retention/policies/{policy_id}/teams/search", options=options)

    def get_channels_for_retention_policy(self, policy_id, params=None):
        """Get the channels for a granular data retention policy

        policy_id: The ID of the granular retention policy.
        page: The page to select.
        per_page: The number of channels per page.

        `Read in Mattermost API docs (data_retention - GetChannelsForRetentionPolicy) <https://api.mattermost.com/#tag/data_retention/operation/GetChannelsForRetentionPolicy>`_

        """
        return self.client.get(f"/api/v4/data_retention/policies/{policy_id}/channels", params=params)

    def add_channels_to_retention_policy(self, policy_id, options):
        """Add channels to a granular data retention policy

        policy_id: The ID of the granular retention policy.

        `Read in Mattermost API docs (data_retention - AddChannelsToRetentionPolicy) <https://api.mattermost.com/#tag/data_retention/operation/AddChannelsToRetentionPolicy>`_

        """
        return self.client.post(f"/api/v4/data_retention/policies/{policy_id}/channels", options=options)

    def remove_channels_from_retention_policy(self, policy_id, params):
        """Delete channels from a granular data retention policy

        policy_id: The ID of the granular retention policy.

        `Read in Mattermost API docs (data_retention - RemoveChannelsFromRetentionPolicy) <https://api.mattermost.com/#tag/data_retention/operation/RemoveChannelsFromRetentionPolicy>`_

        """
        return self.client.delete(f"/api/v4/data_retention/policies/{policy_id}/channels", params=params)

    def search_channels_for_retention_policy(self, policy_id, options):
        """Search for the channels in a granular data retention policy

        policy_id: The ID of the granular retention policy.
        term: The string to search in the channel name, display name, and purpose.
        team_ids: Filters results to channels belonging to the given team ids

        public: Filters results to only return Public / Open channels, can be used in conjunction with ``private`` to return both ``public`` and ``private`` channels

        private: Filters results to only return Private channels, can be used in conjunction with ``public`` to return both ``private`` and ``public`` channels

        deleted: Filters results to only return deleted / archived channels


        `Read in Mattermost API docs (data_retention - SearchChannelsForRetentionPolicy) <https://api.mattermost.com/#tag/data_retention/operation/SearchChannelsForRetentionPolicy>`_

        """
        return self.client.post(f"/api/v4/data_retention/policies/{policy_id}/channels/search", options=options)
