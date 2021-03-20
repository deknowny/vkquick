import typing as ty

import typing_extensions as tye

from vkquick.api_implementation.base import APIMethod, api_method


class Account(APIMethod):
    @api_method
    async def ban(self, *, owner_id: ty.Optional[int] = None, **kwargs) -> 1:
        """
        No description provided

        :param owner_id: No description provided
        """

    @api_method
    async def change_password(
        self,
        *,
        restore_sid: ty.Optional[str] = None,
        change_password_hash: ty.Optional[str] = None,
        old_password: ty.Optional[str] = None,
        new_password: str,
        **kwargs
    ) -> 1:
        """
        Changes a user password after access is successfully restored with the [vk.com/dev/auth.restore|auth.restore] method.

        :param restore_sid: Session id received after the [vk.com/dev/auth.restore|auth.restore] method is executed. (If the password is changed right after the access was restored)
        :param change_password_hash: Hash received after a successful OAuth authorization with a code got by SMS. (If the password is changed right after the access was restored)
        :param old_password: Current user password.
        :param new_password: New password that will be set as a current
        """

    @api_method
    async def get_active_offers(
        self, *, offset: int = 0, count: int = 100, **kwargs
    ) -> 1:
        """
        Returns a list of active ads (offers) which executed by the user will bring him/her respective number of votes to his balance in the application.

        :param offset: No description provided
        :param count: Number of results to return.
        """

    @api_method
    async def get_app_permissions(self, *, user_id: int, **kwargs) -> 1:
        """
        Gets settings of the user in this application.

        :param user_id: User ID whose settings information shall be got. By default: current user.
        """

    @api_method
    async def get_banned(
        self, *, offset: ty.Optional[int] = None, count: int = 20, **kwargs
    ) -> 1:
        """
        Returns a user"s blacklist.

        :param offset: Offset needed to return a specific subset of results.
        :param count: Number of results to return.
        """

    @api_method
    async def get_counters(
        self,
        *,
        filter: ty.Optional[
            ty.Sequence[
                tye.Literal[
                    "friends",
                    "messages",
                    "photos",
                    "videos",
                    "notes",
                    "gifts",
                    "events",
                    "groups",
                    "sdk",
                    "friends_suggestions",
                ]
            ]
        ] = None,
        **kwargs
    ) -> 1:
        """
        Returns non-null values of user counters.

        :param filter: Counters to be returned.
        """

    @api_method
    async def get_info(
        self,
        *,
        fields: ty.Optional[
            ty.Sequence[
                tye.Literal[
                    "country",
                    "https_required",
                    "own_posts_default",
                    "no_wall_replies",
                    "intro",
                    "lang",
                ]
            ]
        ] = None,
        **kwargs
    ) -> 1:
        """
        Returns current account info.

        :param fields: Fields to return. Possible values: *"country" — user country,, *"https_required" — is "HTTPS only" option enabled,, *"own_posts_default" — is "Show my posts only" option is enabled,, *"no_wall_replies" — are wall replies disabled or not,, *"intro" — is intro passed by user or not,, *"lang" — user language. By default: all.
        """

    @api_method
    async def get_profile_info(self, **kwargs) -> 1:
        """
        Returns the current account info.
        """

    @api_method
    async def get_push_settings(
        self, *, device_id: ty.Optional[str] = None, **kwargs
    ) -> 1:
        """
        Gets settings of push notifications.

        :param device_id: Unique device ID.
        """

    @api_method
    async def register_device(
        self,
        *,
        token: str,
        device_model: ty.Optional[str] = None,
        device_year: ty.Optional[int] = None,
        device_id: str,
        system_version: ty.Optional[str] = None,
        settings: ty.Optional[str] = None,
        sandbox: bool = 0,
        **kwargs
    ) -> 1:
        """
        Subscribes an iOS/Android/Windows Phone-based device to receive push notifications

        :param token: Device token used to send notifications. (for mpns, the token shall be URL for sending of notifications)
        :param device_model: String name of device model.
        :param device_year: Device year.
        :param device_id: Unique device ID.
        :param system_version: String version of device operating system.
        :param settings: Push settings in a [vk.com/dev/push_settings|special format].
        :param sandbox: No description provided
        """

    @api_method
    async def save_profile_info(
        self,
        *,
        first_name: ty.Optional[str] = None,
        last_name: ty.Optional[str] = None,
        maiden_name: ty.Optional[str] = None,
        screen_name: ty.Optional[str] = None,
        cancel_request_id: ty.Optional[int] = None,
        sex: ty.Optional[int] = None,
        relation: ty.Optional[int] = None,
        relation_partner_id: ty.Optional[int] = None,
        bdate: ty.Optional[str] = None,
        bdate_visibility: ty.Optional[int] = None,
        home_town: ty.Optional[str] = None,
        country_id: ty.Optional[int] = None,
        city_id: ty.Optional[int] = None,
        status: ty.Optional[str] = None,
        **kwargs
    ) -> 1:
        """
        Edits current profile info.

        :param first_name: User first name.
        :param last_name: User last name.
        :param maiden_name: User maiden name (female only)
        :param screen_name: User screen name.
        :param cancel_request_id: ID of the name change request to be canceled. If this parameter is sent, all the others are ignored.
        :param sex: User sex. Possible values: , * "1" – female,, * "2" – male.
        :param relation: User relationship status. Possible values: , * "1" – single,, * "2" – in a relationship,, * "3" – engaged,, * "4" – married,, * "5" – it"s complicated,, * "6" – actively searching,, * "7" – in love,, * "0" – not specified.
        :param relation_partner_id: ID of the relationship partner.
        :param bdate: User birth date, format: DD.MM.YYYY.
        :param bdate_visibility: Birth date visibility. Returned values: , * "1" – show birth date,, * "2" – show only month and day,, * "0" – hide birth date.
        :param home_town: User home town.
        :param country_id: User country.
        :param city_id: User city.
        :param status: Status text.
        """

    @api_method
    async def set_info(
        self,
        *,
        name: ty.Optional[str] = None,
        value: ty.Optional[str] = None,
        **kwargs
    ) -> 1:
        """
        Allows to edit the current account info.

        :param name: Setting name.
        :param value: Setting value.
        """

    @api_method
    async def set_name_in_menu(
        self, *, user_id: int, name: ty.Optional[str] = None, **kwargs
    ) -> 1:
        """
        Sets an application screen name (up to 17 characters), that is shown to the user in the left menu.

        :param user_id: User ID.
        :param name: Application screen name.
        """

    @api_method
    async def set_offline(self, **kwargs) -> 1:
        """
        Marks a current user as offline.
        """

    @api_method
    async def set_online(
        self, *, voip: ty.Optional[bool] = None, **kwargs
    ) -> 1:
        """
        Marks the current user as online for 15 minutes.

        :param voip: "1" if videocalls are available for current device.
        """

    @api_method
    async def set_push_settings(
        self,
        *,
        device_id: str,
        settings: ty.Optional[str] = None,
        key: ty.Optional[str] = None,
        value: ty.Optional[ty.List[str]] = None,
        **kwargs
    ) -> 1:
        """
        Change push settings.

        :param device_id: Unique device ID.
        :param settings: Push settings in a [vk.com/dev/push_settings|special format].
        :param key: Notification key.
        :param value: New value for the key in a [vk.com/dev/push_settings|special format].
        """

    @api_method
    async def set_silence_mode(
        self,
        *,
        device_id: ty.Optional[str] = None,
        time: ty.Optional[int] = None,
        peer_id: ty.Optional[int] = None,
        sound: ty.Optional[int] = None,
        **kwargs
    ) -> 1:
        """
        Mutes push notifications for the set period of time.

        :param device_id: Unique device ID.
        :param time: Time in seconds for what notifications should be disabled. "-1" to disable forever.
        :param peer_id: Destination ID. "For user: "User ID", e.g. "12345". For chat: "2000000000" + "Chat ID", e.g. "2000000001". For community: "- Community ID", e.g. "-12345". "
        :param sound: "1" — to enable sound in this dialog, "0" — to disable sound. Only if "peer_id" contains user or community ID.
        """

    @api_method
    async def unban(
        self, *, owner_id: ty.Optional[int] = None, **kwargs
    ) -> 1:
        """
        No description provided

        :param owner_id: No description provided
        """

    @api_method
    async def unregister_device(
        self,
        *,
        device_id: ty.Optional[str] = None,
        sandbox: bool = 0,
        **kwargs
    ) -> 1:
        """
        Unsubscribes a device from push notifications.

        :param device_id: Unique device ID.
        :param sandbox: No description provided
        """


class Ads(APIMethod):
    @api_method
    async def add_office_users(
        self, *, account_id: int, data: ty.Sequence, **kwargs
    ) -> 1:
        """
        Adds managers and/or supervisors to advertising account.

        :param account_id: Advertising account ID.
        :param data: Serialized JSON array of objects that describe added managers. Description of "user_specification" objects see below.
        """

    @api_method
    async def check_link(
        self,
        *,
        account_id: int,
        link_type: str,
        link_url: str,
        campaign_id: ty.Optional[int] = None,
        **kwargs
    ) -> 1:
        """
        Allows to check the ad link.

        :param account_id: Advertising account ID.
        :param link_type: Object type: *"community" — community,, *"post" — community post,, *"application" — VK application,, *"video" — video,, *"site" — external site.
        :param link_url: Object URL.
        :param campaign_id: Campaign ID
        """

    @api_method
    async def create_ads(self, *, account_id: int, data: str, **kwargs) -> 1:
        """
        Creates ads.

        :param account_id: Advertising account ID.
        :param data: Serialized JSON array of objects that describe created ads. Description of "ad_specification" objects see below.
        """

    @api_method
    async def create_campaigns(
        self, *, account_id: int, data: str, **kwargs
    ) -> 1:
        """
        Creates advertising campaigns.

        :param account_id: Advertising account ID.
        :param data: Serialized JSON array of objects that describe created campaigns. Description of "campaign_specification" objects see below.
        """

    @api_method
    async def create_clients(
        self, *, account_id: int, data: str, **kwargs
    ) -> 1:
        """
        Creates clients of an advertising agency.

        :param account_id: Advertising account ID.
        :param data: Serialized JSON array of objects that describe created campaigns. Description of "client_specification" objects see below.
        """

    @api_method
    async def create_target_group(
        self,
        *,
        account_id: int,
        client_id: ty.Optional[int] = None,
        name: str,
        lifetime: int,
        target_pixel_id: ty.Optional[int] = None,
        target_pixel_rules: ty.Optional[str] = None,
        **kwargs
    ) -> 1:
        """
        Creates a group to re-target ads for users who visited advertiser"s site (viewed information about the product, registered, etc.).

        :param account_id: Advertising account ID.
        :param client_id: "Only for advertising agencies.", ID of the client with the advertising account where the group will be created.
        :param name: Name of the target group — a string up to 64 characters long.
        :param lifetime: "For groups with auditory created with pixel code only.", , Number of days after that users will be automatically removed from the group.
        :param target_pixel_id: No description provided
        :param target_pixel_rules: No description provided
        """

    @api_method
    async def delete_ads(self, *, account_id: int, ids: str, **kwargs) -> 1:
        """
        Archives ads.

        :param account_id: Advertising account ID.
        :param ids: Serialized JSON array with ad IDs.
        """

    @api_method
    async def delete_campaigns(
        self, *, account_id: int, ids: str, **kwargs
    ) -> 1:
        """
        Archives advertising campaigns.

        :param account_id: Advertising account ID.
        :param ids: Serialized JSON array with IDs of deleted campaigns.
        """

    @api_method
    async def delete_clients(
        self, *, account_id: int, ids: str, **kwargs
    ) -> 1:
        """
        Archives clients of an advertising agency.

        :param account_id: Advertising account ID.
        :param ids: Serialized JSON array with IDs of deleted clients.
        """

    @api_method
    async def delete_target_group(
        self,
        *,
        account_id: int,
        client_id: ty.Optional[int] = None,
        target_group_id: int,
        **kwargs
    ) -> 1:
        """
        Deletes a retarget group.

        :param account_id: Advertising account ID.
        :param client_id: "Only for advertising agencies." , ID of the client with the advertising account where the group will be created.
        :param target_group_id: Group ID.
        """

    @api_method
    async def get_accounts(self, **kwargs) -> 1:
        """
        Returns a list of advertising accounts.
        """

    @api_method
    async def get_ads(
        self,
        *,
        account_id: int,
        ad_ids: ty.Optional[str] = None,
        campaign_ids: ty.Optional[str] = None,
        client_id: ty.Optional[int] = None,
        include_deleted: ty.Optional[bool] = None,
        only_deleted: ty.Optional[bool] = None,
        limit: ty.Optional[int] = None,
        offset: ty.Optional[int] = None,
        **kwargs
    ) -> 1:
        """
        Returns number of ads.

        :param account_id: Advertising account ID.
        :param ad_ids: Filter by ads. Serialized JSON array with ad IDs. If the parameter is null, all ads will be shown.
        :param campaign_ids: Filter by advertising campaigns. Serialized JSON array with campaign IDs. If the parameter is null, ads of all campaigns will be shown.
        :param client_id: "Available and required for advertising agencies." ID of the client ads are retrieved from.
        :param include_deleted: Flag that specifies whether archived ads shall be shown: *0 — show only active ads,, *1 — show all ads.
        :param only_deleted: Flag that specifies whether to show only archived ads: *0 — show all ads,, *1 — show only archived ads. Available when include_deleted flag is *1
        :param limit: Limit of number of returned ads. Used only if ad_ids parameter is null, and "campaign_ids" parameter contains ID of only one campaign.
        :param offset: Offset. Used in the same cases as "limit" parameter.
        """

    @api_method
    async def get_ads_layout(
        self,
        *,
        account_id: int,
        ad_ids: ty.Optional[str] = None,
        campaign_ids: ty.Optional[str] = None,
        client_id: ty.Optional[int] = None,
        include_deleted: ty.Optional[bool] = None,
        limit: ty.Optional[int] = None,
        offset: ty.Optional[int] = None,
        **kwargs
    ) -> 1:
        """
        Returns descriptions of ad layouts.

        :param account_id: Advertising account ID.
        :param ad_ids: Filter by ads. Serialized JSON array with ad IDs. If the parameter is null, all ads will be shown.
        :param campaign_ids: Filter by advertising campaigns. Serialized JSON array with campaign IDs. If the parameter is null, ads of all campaigns will be shown.
        :param client_id: "For advertising agencies." ID of the client ads are retrieved from.
        :param include_deleted: Flag that specifies whether archived ads shall be shown. *0 — show only active ads,, *1 — show all ads.
        :param limit: Limit of number of returned ads. Used only if "ad_ids" parameter is null, and "campaign_ids" parameter contains ID of only one campaign.
        :param offset: Offset. Used in the same cases as "limit" parameter.
        """

    @api_method
    async def get_ads_targeting(
        self,
        *,
        account_id: int,
        ad_ids: ty.Optional[str] = None,
        campaign_ids: ty.Optional[str] = None,
        client_id: ty.Optional[int] = None,
        include_deleted: ty.Optional[bool] = None,
        limit: ty.Optional[int] = None,
        offset: ty.Optional[int] = None,
        **kwargs
    ) -> 1:
        """
        Returns ad targeting parameters.

        :param account_id: Advertising account ID.
        :param ad_ids: Filter by ads. Serialized JSON array with ad IDs. If the parameter is null, all ads will be shown.
        :param campaign_ids: Filter by advertising campaigns. Serialized JSON array with campaign IDs. If the parameter is null, ads of all campaigns will be shown.
        :param client_id: "For advertising agencies." ID of the client ads are retrieved from.
        :param include_deleted: flag that specifies whether archived ads shall be shown: *0 — show only active ads,, *1 — show all ads.
        :param limit: Limit of number of returned ads. Used only if "ad_ids" parameter is null, and "campaign_ids" parameter contains ID of only one campaign.
        :param offset: Offset needed to return a specific subset of results.
        """

    @api_method
    async def get_budget(self, *, account_id: int, **kwargs) -> 1:
        """
        Returns current budget of the advertising account.

        :param account_id: Advertising account ID.
        """

    @api_method
    async def get_campaigns(
        self,
        *,
        account_id: int,
        client_id: ty.Optional[int] = None,
        include_deleted: ty.Optional[bool] = None,
        campaign_ids: ty.Optional[str] = None,
        fields: ty.Optional[ty.Sequence[tye.Literal["ads_count"]]] = None,
        **kwargs
    ) -> 1:
        """
        Returns a list of campaigns in an advertising account.

        :param account_id: Advertising account ID.
        :param client_id: "For advertising agencies". ID of the client advertising campaigns are retrieved from.
        :param include_deleted: Flag that specifies whether archived ads shall be shown. *0 — show only active campaigns,, *1 — show all campaigns.
        :param campaign_ids: Filter of advertising campaigns to show. Serialized JSON array with campaign IDs. Only campaigns that exist in "campaign_ids" and belong to the specified advertising account will be shown. If the parameter is null, all campaigns will be shown.
        :param fields: No description provided
        """

    @api_method
    async def get_categories(
        self, *, lang: ty.Optional[str] = None, **kwargs
    ) -> 1:
        """
        Returns a list of possible ad categories.

        :param lang: Language. The full list of supported languages is [vk.com/dev/api_requests|here].
        """

    @api_method
    async def get_clients(self, *, account_id: int, **kwargs) -> 1:
        """
        Returns a list of advertising agency"s clients.

        :param account_id: Advertising account ID.
        """

    @api_method
    async def get_demographics(
        self,
        *,
        account_id: int,
        ids_type: str,
        ids: str,
        period: str,
        date_from: str,
        date_to: str,
        **kwargs
    ) -> 1:
        """
        Returns demographics for ads or campaigns.

        :param account_id: Advertising account ID.
        :param ids_type: Type of requested objects listed in "ids" parameter: *ad — ads,, *campaign — campaigns.
        :param ids: IDs requested ads or campaigns, separated with a comma, depending on the value set in "ids_type". Maximum 2000 objects.
        :param period: Data grouping by dates: *day — statistics by days,, *month — statistics by months,, *overall — overall statistics. "date_from" and "date_to" parameters set temporary limits.
        :param date_from: Date to show statistics from. For different value of "period" different date format is used: *day: YYYY-MM-DD, example: 2011-09-27 — September 27, 2011, **0 — day it was created on,, *month: YYYY-MM, example: 2011-09 — September 2011, **0 — month it was created in,, *overall: 0.
        :param date_to: Date to show statistics to. For different value of "period" different date format is used: *day: YYYY-MM-DD, example: 2011-09-27 — September 27, 2011, **0 — current day,, *month: YYYY-MM, example: 2011-09 — September 2011, **0 — current month,, *overall: 0.
        """

    @api_method
    async def get_flood_stats(self, *, account_id: int, **kwargs) -> 1:
        """
        Returns information about current state of a counter — number of remaining runs of methods and time to the next counter nulling in seconds.

        :param account_id: Advertising account ID.
        """

    @api_method
    async def get_lookalike_requests(
        self,
        *,
        account_id: int,
        client_id: ty.Optional[int] = None,
        requests_ids: ty.Optional[str] = None,
        offset: int = 0,
        limit: int = 10,
        sort_by: str = "id",
        **kwargs
    ) -> 1:
        """
        No description provided

        :param account_id: No description provided
        :param client_id: No description provided
        :param requests_ids: No description provided
        :param offset: No description provided
        :param limit: No description provided
        :param sort_by: No description provided
        """

    @api_method
    async def get_musicians(self, *, artist_name: str, **kwargs) -> 1:
        """
        No description provided

        :param artist_name: No description provided
        """

    @api_method
    async def get_musicians_by_ids(self, *, ids: ty.Sequence, **kwargs) -> 1:
        """
        No description provided

        :param ids: No description provided
        """

    @api_method
    async def get_office_users(self, *, account_id: int, **kwargs) -> 1:
        """
        Returns a list of managers and supervisors of advertising account.

        :param account_id: Advertising account ID.
        """

    @api_method
    async def get_posts_reach(
        self, *, account_id: int, ids_type: str, ids: str, **kwargs
    ) -> 1:
        """
        Returns detailed statistics of promoted posts reach from campaigns and ads.

        :param account_id: Advertising account ID.
        :param ids_type: Type of requested objects listed in "ids" parameter: *ad — ads,, *campaign — campaigns.
        :param ids: IDs requested ads or campaigns, separated with a comma, depending on the value set in "ids_type". Maximum 100 objects.
        """

    @api_method
    async def get_rejection_reason(
        self, *, account_id: int, ad_id: int, **kwargs
    ) -> 1:
        """
        Returns a reason of ad rejection for pre-moderation.

        :param account_id: Advertising account ID.
        :param ad_id: Ad ID.
        """

    @api_method
    async def get_statistics(
        self,
        *,
        account_id: int,
        ids_type: str,
        ids: str,
        period: str,
        date_from: str,
        date_to: str,
        stats_fields: ty.Optional[
            ty.Sequence[tye.Literal["views_times"]]
        ] = None,
        **kwargs
    ) -> 1:
        """
        Returns statistics of performance indicators for ads, campaigns, clients or the whole account.

        :param account_id: Advertising account ID.
        :param ids_type: Type of requested objects listed in "ids" parameter: *ad — ads,, *campaign — campaigns,, *client — clients,, *office — account.
        :param ids: IDs requested ads, campaigns, clients or account, separated with a comma, depending on the value set in "ids_type". Maximum 2000 objects.
        :param period: Data grouping by dates: *day — statistics by days,, *month — statistics by months,, *overall — overall statistics. "date_from" and "date_to" parameters set temporary limits.
        :param date_from: Date to show statistics from. For different value of "period" different date format is used: *day: YYYY-MM-DD, example: 2011-09-27 — September 27, 2011, **0 — day it was created on,, *month: YYYY-MM, example: 2011-09 — September 2011, **0 — month it was created in,, *overall: 0.
        :param date_to: Date to show statistics to. For different value of "period" different date format is used: *day: YYYY-MM-DD, example: 2011-09-27 — September 27, 2011, **0 — current day,, *month: YYYY-MM, example: 2011-09 — September 2011, **0 — current month,, *overall: 0.
        :param stats_fields: Additional fields to add to statistics
        """

    @api_method
    async def get_suggestions(
        self,
        *,
        section: str,
        ids: ty.Optional[str] = None,
        q: ty.Optional[str] = None,
        country: ty.Optional[int] = None,
        cities: ty.Optional[str] = None,
        lang: ty.Optional[str] = None,
        **kwargs
    ) -> 1:
        """
        Returns a set of auto-suggestions for various targeting parameters.

        :param section: Section, suggestions are retrieved in. Available values: *countries — request of a list of countries. If q is not set or blank, a short list of countries is shown. Otherwise, a full list of countries is shown. *regions — requested list of regions. "country" parameter is required. *cities — requested list of cities. "country" parameter is required. *districts — requested list of districts. "cities" parameter is required. *stations — requested list of subway stations. "cities" parameter is required. *streets — requested list of streets. "cities" parameter is required. *schools — requested list of educational organizations. "cities" parameter is required. *interests — requested list of interests. *positions — requested list of positions (professions). *group_types — requested list of group types. *religions — requested list of religious commitments. *browsers — requested list of browsers and mobile devices.
        :param ids: Objects IDs separated by commas. If the parameter is passed, "q, country, cities" should not be passed.
        :param q: Filter-line of the request (for countries, regions, cities, streets, schools, interests, positions).
        :param country: ID of the country objects are searched in.
        :param cities: IDs of cities where objects are searched in, separated with a comma.
        :param lang: Language of the returned string values. Supported languages: *ru — Russian,, *ua — Ukrainian,, *en — English.
        """

    @api_method
    async def get_target_groups(
        self,
        *,
        account_id: int,
        client_id: ty.Optional[int] = None,
        extended: ty.Optional[bool] = None,
        **kwargs
    ) -> 1:
        """
        Returns a list of target groups.

        :param account_id: Advertising account ID.
        :param client_id: "Only for advertising agencies.", ID of the client with the advertising account where the group will be created.
        :param extended: "1" — to return pixel code.
        """

    @api_method
    async def get_targeting_stats(
        self,
        *,
        account_id: int,
        client_id: ty.Optional[int] = None,
        criteria: ty.Optional[str] = None,
        ad_id: ty.Optional[int] = None,
        ad_format: ty.Optional[int] = None,
        ad_platform: ty.Optional[str] = None,
        ad_platform_no_wall: ty.Optional[str] = None,
        ad_platform_no_ad_network: ty.Optional[str] = None,
        link_url: str,
        link_domain: ty.Optional[str] = None,
        need_precise: ty.Optional[bool] = None,
        impressions_limit_period: ty.Optional[int] = None,
        **kwargs
    ) -> 1:
        """
        Returns the size of targeting audience, and also recommended values for CPC and CPM.

        :param account_id: Advertising account ID.
        :param client_id: No description provided
        :param criteria: Serialized JSON object that describes targeting parameters. Description of "criteria" object see below.
        :param ad_id: ID of an ad which targeting parameters shall be analyzed.
        :param ad_format: Ad format. Possible values: *"1" — image and text,, *"2" — big image,, *"3" — exclusive format,, *"4" — community, square image,, *"7" — special app format,, *"8" — special community format,, *"9" — post in community,, *"10" — app board.
        :param ad_platform: Platforms to use for ad showing. Possible values: (for "ad_format" = "1"), *"0" — VK and partner sites,, *"1" — VK only. (for "ad_format" = "9"), *"all" — all platforms,, *"desktop" — desktop version,, *"mobile" — mobile version and apps.
        :param ad_platform_no_wall: No description provided
        :param ad_platform_no_ad_network: No description provided
        :param link_url: URL for the advertised object.
        :param link_domain: Domain of the advertised object.
        :param need_precise: Additionally return recommended cpc and cpm to reach 5,10..95 percents of audience.
        :param impressions_limit_period: Impressions limit period in seconds, must be a multiple of 86400(day)
        """

    @api_method
    async def get_upload_u_r_l(
        self, *, ad_format: int, icon: ty.Optional[int] = None, **kwargs
    ) -> 1:
        """
        Returns URL to upload an ad photo to.

        :param ad_format: Ad format: *1 — image and text,, *2 — big image,, *3 — exclusive format,, *4 — community, square image,, *7 — special app format.
        :param icon: No description provided
        """

    @api_method
    async def get_video_upload_u_r_l(self, **kwargs) -> 1:
        """
        Returns URL to upload an ad video to.
        """

    @api_method
    async def import_target_contacts(
        self,
        *,
        account_id: int,
        client_id: ty.Optional[int] = None,
        target_group_id: int,
        contacts: str,
        **kwargs
    ) -> 1:
        """
        Imports a list of advertiser"s contacts to count VK registered users against the target group.

        :param account_id: Advertising account ID.
        :param client_id: "Only for advertising agencies." , ID of the client with the advertising account where the group will be created.
        :param target_group_id: Target group ID.
        :param contacts: List of phone numbers, emails or user IDs separated with a comma.
        """

    @api_method
    async def remove_office_users(
        self, *, account_id: int, ids: str, **kwargs
    ) -> 1:
        """
        Removes managers and/or supervisors from advertising account.

        :param account_id: Advertising account ID.
        :param ids: Serialized JSON array with IDs of deleted managers.
        """

    @api_method
    async def update_ads(self, *, account_id: int, data: str, **kwargs) -> 1:
        """
        Edits ads.

        :param account_id: Advertising account ID.
        :param data: Serialized JSON array of objects that describe changes in ads. Description of "ad_edit_specification" objects see below.
        """

    @api_method
    async def update_campaigns(
        self, *, account_id: int, data: str, **kwargs
    ) -> 1:
        """
        Edits advertising campaigns.

        :param account_id: Advertising account ID.
        :param data: Serialized JSON array of objects that describe changes in campaigns. Description of "campaign_mod" objects see below.
        """

    @api_method
    async def update_clients(
        self, *, account_id: int, data: str, **kwargs
    ) -> 1:
        """
        Edits clients of an advertising agency.

        :param account_id: Advertising account ID.
        :param data: Serialized JSON array of objects that describe changes in clients. Description of "client_mod" objects see below.
        """

    @api_method
    async def update_office_users(
        self, *, account_id: int, data: ty.Sequence, **kwargs
    ) -> 1:
        """
        Adds managers and/or supervisors to advertising account.

        :param account_id: Advertising account ID.
        :param data: Serialized JSON array of objects that describe added managers. Description of "user_specification" objects see below.
        """

    @api_method
    async def update_target_group(
        self,
        *,
        account_id: int,
        client_id: ty.Optional[int] = None,
        target_group_id: int,
        name: str,
        domain: ty.Optional[str] = None,
        lifetime: int,
        target_pixel_id: ty.Optional[int] = None,
        target_pixel_rules: ty.Optional[str] = None,
        **kwargs
    ) -> 1:
        """
        Edits a retarget group.

        :param account_id: Advertising account ID.
        :param client_id: "Only for advertising agencies." , ID of the client with the advertising account where the group will be created.
        :param target_group_id: Group ID.
        :param name: New name of the target group — a string up to 64 characters long.
        :param domain: Domain of the site where user accounting code will be placed.
        :param lifetime: "Only for the groups that get audience from sites with user accounting code.", Time in days when users added to a retarget group will be automatically excluded from it. "0" - automatic exclusion is off.
        :param target_pixel_id: No description provided
        :param target_pixel_rules: No description provided
        """


class Adsweb(APIMethod):
    @api_method
    async def get_ad_categories(self, *, office_id: int, **kwargs) -> 1:
        """
        No description provided

        :param office_id: No description provided
        """

    @api_method
    async def get_ad_unit_code(self, **kwargs) -> 1:
        """
        No description provided
        """

    @api_method
    async def get_ad_units(
        self,
        *,
        office_id: int,
        sites_ids: ty.Optional[str] = None,
        ad_units_ids: ty.Optional[str] = None,
        fields: ty.Optional[str] = None,
        limit: int = None,
        offset: int = 0,
        **kwargs
    ) -> 1:
        """
        No description provided

        :param office_id: No description provided
        :param sites_ids: No description provided
        :param ad_units_ids: No description provided
        :param fields: No description provided
        :param limit: No description provided
        :param offset: No description provided
        """

    @api_method
    async def get_fraud_history(
        self,
        *,
        office_id: int,
        sites_ids: ty.Optional[str] = None,
        limit: int = None,
        offset: int = 0,
        **kwargs
    ) -> 1:
        """
        No description provided

        :param office_id: No description provided
        :param sites_ids: No description provided
        :param limit: No description provided
        :param offset: No description provided
        """

    @api_method
    async def get_sites(
        self,
        *,
        office_id: int,
        sites_ids: ty.Optional[str] = None,
        fields: ty.Optional[str] = None,
        limit: int = None,
        offset: int = 0,
        **kwargs
    ) -> 1:
        """
        No description provided

        :param office_id: No description provided
        :param sites_ids: No description provided
        :param fields: No description provided
        :param limit: No description provided
        :param offset: No description provided
        """

    @api_method
    async def get_statistics(
        self,
        *,
        office_id: int,
        ids_type: str,
        ids: str,
        period: str,
        date_from: str,
        date_to: str,
        fields: ty.Optional[str] = None,
        limit: int = None,
        page_id: ty.Optional[str] = None,
        **kwargs
    ) -> 1:
        """
        No description provided

        :param office_id: No description provided
        :param ids_type: No description provided
        :param ids: No description provided
        :param period: No description provided
        :param date_from: No description provided
        :param date_to: No description provided
        :param fields: No description provided
        :param limit: No description provided
        :param page_id: No description provided
        """


class Appwidgets(APIMethod):
    @api_method
    async def get_app_image_upload_server(
        self, *, image_type: str, **kwargs
    ) -> 1:
        """
        Returns a URL for uploading a photo to the community collection for community app widgets

        :param image_type: No description provided
        """

    @api_method
    async def get_app_images(
        self,
        *,
        offset: ty.Optional[int] = None,
        count: int = 20,
        image_type: ty.Optional[str] = None,
        **kwargs
    ) -> 1:
        """
        Returns an app collection of images for community app widgets

        :param offset: Offset needed to return a specific subset of images.
        :param count: Maximum count of results.
        :param image_type: No description provided
        """

    @api_method
    async def get_group_image_upload_server(
        self, *, image_type: str, **kwargs
    ) -> 1:
        """
        Returns a URL for uploading a photo to the community collection for community app widgets

        :param image_type: No description provided
        """

    @api_method
    async def get_group_images(
        self,
        *,
        offset: ty.Optional[int] = None,
        count: int = 20,
        image_type: ty.Optional[str] = None,
        **kwargs
    ) -> 1:
        """
        Returns a community collection of images for community app widgets

        :param offset: Offset needed to return a specific subset of images.
        :param count: Maximum count of results.
        :param image_type: No description provided
        """

    @api_method
    async def get_images_by_id(self, *, images: ty.List[str], **kwargs) -> 1:
        """
        Returns an image for community app widgets by its ID

        :param images: List of images IDs
        """

    @api_method
    async def save_app_image(self, *, hash: str, image: str, **kwargs) -> 1:
        """
        Allows to save image into app collection for community app widgets

        :param hash: Parameter returned when photo is uploaded to server
        :param image: Parameter returned when photo is uploaded to server
        """

    @api_method
    async def save_group_image(self, *, hash: str, image: str, **kwargs) -> 1:
        """
        Allows to save image into community collection for community app widgets

        :param hash: Parameter returned when photo is uploaded to server
        :param image: Parameter returned when photo is uploaded to server
        """

    @api_method
    async def update(self, *, code: str, type: str, **kwargs) -> 1:
        """
        Allows to update community app widget

        :param code: No description provided
        :param type: No description provided
        """


class Apps(APIMethod):
    @api_method
    async def delete_app_requests(self, **kwargs) -> 1:
        """
        Deletes all request notifications from the current app.
        """

    @api_method
    async def get(
        self,
        *,
        app_id: ty.Optional[int] = None,
        app_ids: ty.Optional[ty.List[ty.Union[str, int]]] = None,
        platform: str = "web",
        extended: bool = 0,
        return_friends: bool = 0,
        fields: ty.Optional[ty.Sequence] = None,
        name_case: ty.Optional[str] = None,
        **kwargs
    ) -> 1:
        """
        Returns applications data.

        :param app_id: Application ID
        :param app_ids: List of application ID
        :param platform: platform. Possible values: *"ios" — iOS,, *"android" — Android,, *"winphone" — Windows Phone,, *"web" — приложения на vk.com. By default: "web".
        :param extended: No description provided
        :param return_friends: No description provided
        :param fields: Profile fields to return. Sample values: "nickname", "screen_name", "sex", "bdate" (birthdate), "city", "country", "timezone", "photo", "photo_medium", "photo_big", "has_mobile", "contacts", "education", "online", "counters", "relation", "last_seen", "activity", "can_write_private_message", "can_see_all_posts", "can_post", "universities", (only if return_friends - 1)
        :param name_case: Case for declension of user name and surname: "nom" — nominative (default),, "gen" — genitive,, "dat" — dative,, "acc" — accusative,, "ins" — instrumental,, "abl" — prepositional. (only if "return_friends" = "1")
        """

    @api_method
    async def get_catalog(
        self,
        *,
        sort: ty.Optional[str] = None,
        offset: ty.Optional[int] = None,
        count: int = 100,
        platform: ty.Optional[str] = None,
        extended: ty.Optional[bool] = None,
        return_friends: ty.Optional[bool] = None,
        fields: ty.Optional[ty.Sequence] = None,
        name_case: ty.Optional[str] = None,
        q: ty.Optional[str] = None,
        genre_id: ty.Optional[int] = None,
        filter: ty.Optional[str] = None,
        **kwargs
    ) -> 1:
        """
        Returns a list of applications (apps) available to users in the App Catalog.

        :param sort: Sort order: "popular_today" — popular for one day (default), "visitors" — by visitors number , "create_date" — by creation date, "growth_rate" — by growth rate, "popular_week" — popular for one week
        :param offset: Offset required to return a specific subset of apps.
        :param count: Number of apps to return.
        :param platform: No description provided
        :param extended: "1" — to return additional fields "screenshots", "MAU", "catalog_position", and "international". If set, "count" must be less than or equal to "100". "0" — not to return additional fields (default).
        :param return_friends: No description provided
        :param fields: No description provided
        :param name_case: No description provided
        :param q: Search query string.
        :param genre_id: No description provided
        :param filter: "installed" — to return list of installed apps (only for mobile platform).
        """

    @api_method
    async def get_friends_list(
        self,
        *,
        extended: bool = 0,
        count: int = 20,
        offset: int = 0,
        type: str = "invite",
        fields: ty.Optional[ty.Sequence] = None,
        **kwargs
    ) -> 1:
        """
        Creates friends list for requests and invites in current app.

        :param extended: No description provided
        :param count: List size.
        :param offset: No description provided
        :param type: List type. Possible values: * "invite" — available for invites (don"t play the game),, * "request" — available for request (play the game). By default: "invite".
        :param fields: Additional profile fields, see [vk.com/dev/fields|description].
        """

    @api_method
    async def get_leaderboard(
        self, *, type: str, global_: bool = 1, extended: bool = 0, **kwargs
    ) -> 1:
        """
        Returns players rating in the game.

        :param type: Leaderboard type. Possible values: *"level" — by level,, *"points" — by mission points,, *"score" — by score ().
        :param global_: Rating type. Possible values: *"1" — global rating among all players,, *"0" — rating among user friends.
        :param extended: 1 — to return additional info about users
        """

    @api_method
    async def get_mini_app_policies(self, *, app_id: int, **kwargs) -> 1:
        """
        Returns policies and terms given to a mini app.

        :param app_id: Mini App ID
        """

    @api_method
    async def get_scopes(self, *, type: str = "user", **kwargs) -> 1:
        """
        Returns scopes for auth

        :param type: No description provided
        """

    @api_method
    async def get_score(self, *, user_id: int, **kwargs) -> 1:
        """
        Returns user score in app

        :param user_id: No description provided
        """

    @api_method
    async def promo_has_active_gift(
        self, *, promo_id: int, user_id: ty.Optional[int] = None, **kwargs
    ) -> 1:
        """
        No description provided

        :param promo_id: Id of game promo action
        :param user_id: No description provided
        """

    @api_method
    async def promo_use_gift(
        self, *, promo_id: int, user_id: ty.Optional[int] = None, **kwargs
    ) -> 1:
        """
        No description provided

        :param promo_id: Id of game promo action
        :param user_id: No description provided
        """

    @api_method
    async def send_request(
        self,
        *,
        user_id: int,
        text: ty.Optional[str] = None,
        type: str = "request",
        name: ty.Optional[str] = None,
        key: ty.Optional[str] = None,
        separate: ty.Optional[bool] = None,
        **kwargs
    ) -> 1:
        """
        Sends a request to another user in an app that uses VK authorization.

        :param user_id: id of the user to send a request
        :param text: request text
        :param type: request type. Values: "invite" – if the request is sent to a user who does not have the app installed,, "request" – if a user has already installed the app
        :param name: No description provided
        :param key: special string key to be sent with the request
        :param separate: No description provided
        """


class Auth(APIMethod):
    @api_method
    async def restore(self, *, phone: str, last_name: str, **kwargs) -> 1:
        """
        Allows to restore account access using a code received via SMS. " This method is only available for apps with [vk.com/dev/auth_direct|Direct authorization] access. "

        :param phone: User phone number.
        :param last_name: User last name.
        """


class Board(APIMethod):
    @api_method
    async def add_topic(
        self,
        *,
        group_id: int,
        title: str,
        text: ty.Optional[str] = None,
        from_group: ty.Optional[bool] = None,
        attachments: ty.Optional[ty.List[str]] = None,
        **kwargs
    ) -> 1:
        """
        Creates a new topic on a community"s discussion board.

        :param group_id: ID of the community that owns the discussion board.
        :param title: Topic title.
        :param text: Text of the topic.
        :param from_group: For a community: "1" — to post the topic as by the community, "0" — to post the topic as by the user (default)
        :param attachments: List of media objects attached to the topic, in the following format: "<owner_id>_<media_id>,<owner_id>_<media_id>", "" — Type of media object: "photo" — photo, "video" — video, "audio" — audio, "doc" — document, "<owner_id>" — ID of the media owner. "<media_id>" — Media ID. Example: "photo100172_166443618,photo66748_265827614", , "NOTE: If you try to attach more than one reference, an error will be thrown.",
        """

    @api_method
    async def close_topic(
        self, *, group_id: int, topic_id: int, **kwargs
    ) -> 1:
        """
        Closes a topic on a community"s discussion board so that comments cannot be posted.

        :param group_id: ID of the community that owns the discussion board.
        :param topic_id: Topic ID.
        """

    @api_method
    async def create_comment(
        self,
        *,
        group_id: int,
        topic_id: int,
        message: ty.Optional[str] = None,
        attachments: ty.Optional[ty.List[str]] = None,
        from_group: ty.Optional[bool] = None,
        sticker_id: ty.Optional[int] = None,
        guid: ty.Optional[str] = None,
        **kwargs
    ) -> 1:
        """
        Adds a comment on a topic on a community"s discussion board.

        :param group_id: ID of the community that owns the discussion board.
        :param topic_id: ID of the topic to be commented on.
        :param message: (Required if "attachments" is not set.) Text of the comment.
        :param attachments: (Required if "text" is not set.) List of media objects attached to the comment, in the following format: "<owner_id>_<media_id>,<owner_id>_<media_id>", "" — Type of media object: "photo" — photo, "video" — video, "audio" — audio, "doc" — document, "<owner_id>" — ID of the media owner. "<media_id>" — Media ID.
        :param from_group: "1" — to post the comment as by the community, "0" — to post the comment as by the user (default)
        :param sticker_id: Sticker ID.
        :param guid: Unique identifier to avoid repeated comments.
        """

    @api_method
    async def delete_comment(
        self, *, group_id: int, topic_id: int, comment_id: int, **kwargs
    ) -> 1:
        """
        Deletes a comment on a topic on a community"s discussion board.

        :param group_id: ID of the community that owns the discussion board.
        :param topic_id: Topic ID.
        :param comment_id: Comment ID.
        """

    @api_method
    async def delete_topic(
        self, *, group_id: int, topic_id: int, **kwargs
    ) -> 1:
        """
        Deletes a topic from a community"s discussion board.

        :param group_id: ID of the community that owns the discussion board.
        :param topic_id: Topic ID.
        """

    @api_method
    async def edit_comment(
        self,
        *,
        group_id: int,
        topic_id: int,
        comment_id: int,
        message: ty.Optional[str] = None,
        attachments: ty.Optional[ty.List[str]] = None,
        **kwargs
    ) -> 1:
        """
        Edits a comment on a topic on a community"s discussion board.

        :param group_id: ID of the community that owns the discussion board.
        :param topic_id: Topic ID.
        :param comment_id: ID of the comment on the topic.
        :param message: (Required if "attachments" is not set). New comment text.
        :param attachments: (Required if "message" is not set.) List of media objects attached to the comment, in the following format: "<owner_id>_<media_id>,<owner_id>_<media_id>", "" — Type of media object: "photo" — photo, "video" — video, "audio" — audio, "doc" — document, "<owner_id>" — ID of the media owner. "<media_id>" — Media ID. Example: "photo100172_166443618,photo66748_265827614"
        """

    @api_method
    async def edit_topic(
        self, *, group_id: int, topic_id: int, title: str, **kwargs
    ) -> 1:
        """
        Edits the title of a topic on a community"s discussion board.

        :param group_id: ID of the community that owns the discussion board.
        :param topic_id: Topic ID.
        :param title: New title of the topic.
        """

    @api_method
    async def fix_topic(self, *, group_id: int, topic_id: int, **kwargs) -> 1:
        """
        Pins a topic (fixes its place) to the top of a community"s discussion board.

        :param group_id: ID of the community that owns the discussion board.
        :param topic_id: Topic ID.
        """

    @api_method
    async def get_comments(
        self,
        *,
        group_id: int,
        topic_id: int,
        need_likes: ty.Optional[bool] = None,
        start_comment_id: ty.Optional[int] = None,
        offset: ty.Optional[int] = None,
        count: int = 20,
        extended: ty.Optional[bool] = None,
        sort: ty.Optional[str] = None,
        **kwargs
    ) -> 1:
        """
        Returns a list of comments on a topic on a community"s discussion board.

        :param group_id: ID of the community that owns the discussion board.
        :param topic_id: Topic ID.
        :param need_likes: "1" — to return the "likes" field, "0" — not to return the "likes" field (default)
        :param start_comment_id: No description provided
        :param offset: Offset needed to return a specific subset of comments.
        :param count: Number of comments to return.
        :param extended: "1" — to return information about users who posted comments, "0" — to return no additional fields (default)
        :param sort: Sort order: "asc" — by creation date in chronological order, "desc" — by creation date in reverse chronological order,
        """

    @api_method
    async def get_topics(
        self,
        *,
        group_id: int,
        topic_ids: ty.Optional[ty.Sequence] = None,
        order: ty.Optional[int] = None,
        offset: ty.Optional[int] = None,
        count: int = 40,
        extended: ty.Optional[bool] = None,
        preview: ty.Optional[int] = None,
        preview_length: int = 90,
        **kwargs
    ) -> 1:
        """
        Returns a list of topics on a community"s discussion board.

        :param group_id: ID of the community that owns the discussion board.
        :param topic_ids: IDs of topics to be returned (100 maximum). By default, all topics are returned. If this parameter is set, the "order", "offset", and "count" parameters are ignored.
        :param order: Sort order: "1" — by date updated in reverse chronological order. "2" — by date created in reverse chronological order. "-1" — by date updated in chronological order. "-2" — by date created in chronological order. If no sort order is specified, topics are returned in the order specified by the group administrator. Pinned topics are returned first, regardless of the sorting.
        :param offset: Offset needed to return a specific subset of topics.
        :param count: Number of topics to return.
        :param extended: "1" — to return information about users who created topics or who posted there last, "0" — to return no additional fields (default)
        :param preview: "1" — to return the first comment in each topic,, "2" — to return the last comment in each topic,, "0" — to return no comments. By default: "0".
        :param preview_length: Number of characters after which to truncate the previewed comment. To preview the full comment, specify "0".
        """

    @api_method
    async def open_topic(
        self, *, group_id: int, topic_id: int, **kwargs
    ) -> 1:
        """
        Re-opens a previously closed topic on a community"s discussion board.

        :param group_id: ID of the community that owns the discussion board.
        :param topic_id: Topic ID.
        """

    @api_method
    async def restore_comment(
        self, *, group_id: int, topic_id: int, comment_id: int, **kwargs
    ) -> 1:
        """
        Restores a comment deleted from a topic on a community"s discussion board.

        :param group_id: ID of the community that owns the discussion board.
        :param topic_id: Topic ID.
        :param comment_id: Comment ID.
        """

    @api_method
    async def unfix_topic(
        self, *, group_id: int, topic_id: int, **kwargs
    ) -> 1:
        """
        Unpins a pinned topic from the top of a community"s discussion board.

        :param group_id: ID of the community that owns the discussion board.
        :param topic_id: Topic ID.
        """


class Database(APIMethod):
    @api_method
    async def get_chairs(
        self,
        *,
        faculty_id: int,
        offset: ty.Optional[int] = None,
        count: int = 100,
        **kwargs
    ) -> 1:
        """
        Returns list of chairs on a specified faculty.

        :param faculty_id: id of the faculty to get chairs from
        :param offset: offset required to get a certain subset of chairs
        :param count: amount of chairs to get
        """

    @api_method
    async def get_cities(
        self,
        *,
        country_id: int,
        region_id: ty.Optional[int] = None,
        q: ty.Optional[str] = None,
        need_all: ty.Optional[bool] = None,
        offset: ty.Optional[int] = None,
        count: int = 100,
        **kwargs
    ) -> 1:
        """
        Returns a list of cities.

        :param country_id: Country ID.
        :param region_id: Region ID.
        :param q: Search query.
        :param need_all: "1" — to return all cities in the country, "0" — to return major cities in the country (default),
        :param offset: Offset needed to return a specific subset of cities.
        :param count: Number of cities to return.
        """

    @api_method
    async def get_cities_by_id(
        self, *, city_ids: ty.Optional[ty.Sequence] = None, **kwargs
    ) -> 1:
        """
        Returns information about cities by their IDs.

        :param city_ids: City IDs.
        """

    @api_method
    async def get_countries(
        self,
        *,
        need_all: ty.Optional[bool] = None,
        code: ty.Optional[str] = None,
        offset: ty.Optional[int] = None,
        count: int = 100,
        **kwargs
    ) -> 1:
        """
        Returns a list of countries.

        :param need_all: "1" — to return a full list of all countries, "0" — to return a list of countries near the current user"s country (default).
        :param code: Country codes in [vk.com/dev/country_codes|ISO 3166-1 alpha-2] standard.
        :param offset: Offset needed to return a specific subset of countries.
        :param count: Number of countries to return.
        """

    @api_method
    async def get_countries_by_id(
        self, *, country_ids: ty.Optional[ty.Sequence] = None, **kwargs
    ) -> 1:
        """
        Returns information about countries by their IDs.

        :param country_ids: Country IDs.
        """

    @api_method
    async def get_faculties(
        self,
        *,
        university_id: int,
        offset: ty.Optional[int] = None,
        count: int = 100,
        **kwargs
    ) -> 1:
        """
        Returns a list of faculties (i.e., university departments).

        :param university_id: University ID.
        :param offset: Offset needed to return a specific subset of faculties.
        :param count: Number of faculties to return.
        """

    @api_method
    async def get_metro_stations(
        self,
        *,
        city_id: int,
        offset: ty.Optional[int] = None,
        count: int = 100,
        extended: bool = False,
        **kwargs
    ) -> 1:
        """
        Get metro stations by city

        :param city_id: No description provided
        :param offset: No description provided
        :param count: No description provided
        :param extended: No description provided
        """

    @api_method
    async def get_metro_stations_by_id(
        self, *, station_ids: ty.Optional[ty.Sequence] = None, **kwargs
    ) -> 1:
        """
        Get metro station by his id

        :param station_ids: No description provided
        """

    @api_method
    async def get_regions(
        self,
        *,
        country_id: int,
        q: ty.Optional[str] = None,
        offset: ty.Optional[int] = None,
        count: int = 100,
        **kwargs
    ) -> 1:
        """
        Returns a list of regions.

        :param country_id: Country ID, received in [vk.com/dev/database.getCountries|database.getCountries] method.
        :param q: Search query.
        :param offset: Offset needed to return specific subset of regions.
        :param count: Number of regions to return.
        """

    @api_method
    async def get_school_classes(
        self, *, country_id: ty.Optional[int] = None, **kwargs
    ) -> 1:
        """
        Returns a list of school classes specified for the country.

        :param country_id: Country ID.
        """

    @api_method
    async def get_schools(
        self,
        *,
        q: ty.Optional[str] = None,
        city_id: int,
        offset: ty.Optional[int] = None,
        count: int = 100,
        **kwargs
    ) -> 1:
        """
        Returns a list of schools.

        :param q: Search query.
        :param city_id: City ID.
        :param offset: Offset needed to return a specific subset of schools.
        :param count: Number of schools to return.
        """

    @api_method
    async def get_universities(
        self,
        *,
        q: ty.Optional[str] = None,
        country_id: ty.Optional[int] = None,
        city_id: ty.Optional[int] = None,
        offset: ty.Optional[int] = None,
        count: int = 100,
        **kwargs
    ) -> 1:
        """
        Returns a list of higher education institutions.

        :param q: Search query.
        :param country_id: Country ID.
        :param city_id: City ID.
        :param offset: Offset needed to return a specific subset of universities.
        :param count: Number of universities to return.
        """


class Docs(APIMethod):
    @api_method
    async def add(
        self,
        *,
        owner_id: int,
        doc_id: int,
        access_key: ty.Optional[str] = None,
        **kwargs
    ) -> 1:
        """
        Copies a document to a user"s or community"s document list.

        :param owner_id: ID of the user or community that owns the document. Use a negative value to designate a community ID.
        :param doc_id: Document ID.
        :param access_key: Access key. This parameter is required if "access_key" was returned with the document"s data.
        """

    @api_method
    async def delete(self, *, owner_id: int, doc_id: int, **kwargs) -> 1:
        """
        Deletes a user or community document.

        :param owner_id: ID of the user or community that owns the document. Use a negative value to designate a community ID.
        :param doc_id: Document ID.
        """

    @api_method
    async def edit(
        self,
        *,
        owner_id: int,
        doc_id: int,
        title: ty.Optional[str] = None,
        tags: ty.Optional[ty.List[str]] = None,
        **kwargs
    ) -> 1:
        """
        Edits a document.

        :param owner_id: User ID or community ID. Use a negative value to designate a community ID.
        :param doc_id: Document ID.
        :param title: Document title.
        :param tags: Document tags.
        """

    @api_method
    async def get(
        self,
        *,
        count: ty.Optional[int] = None,
        offset: ty.Optional[int] = None,
        type: int = 0,
        owner_id: ty.Optional[int] = None,
        return_tags: bool = False,
        **kwargs
    ) -> 1:
        """
        Returns detailed information about user or community documents.

        :param count: Number of documents to return. By default, all documents.
        :param offset: Offset needed to return a specific subset of documents.
        :param type: No description provided
        :param owner_id: ID of the user or community that owns the documents. Use a negative value to designate a community ID.
        :param return_tags: No description provided
        """

    @api_method
    async def get_by_id(
        self, *, docs: ty.List[str], return_tags: bool = False, **kwargs
    ) -> 1:
        """
        Returns information about documents by their IDs.

        :param docs: Document IDs. Example: , "66748_91488,66748_91455",
        :param return_tags: No description provided
        """

    @api_method
    async def get_messages_upload_server(
        self, *, type: str = "doc", peer_id: ty.Optional[int] = None, **kwargs
    ) -> 1:
        """
        Returns the server address for document upload.

        :param type: Document type.
        :param peer_id: Destination ID. "For user: "User ID", e.g. "12345". For chat: "2000000000" + "Chat ID", e.g. "2000000001". For community: "- Community ID", e.g. "-12345". "
        """

    @api_method
    async def get_types(self, *, owner_id: int, **kwargs) -> 1:
        """
        Returns documents types available for current user.

        :param owner_id: ID of the user or community that owns the documents. Use a negative value to designate a community ID.
        """

    @api_method
    async def get_upload_server(
        self, *, group_id: ty.Optional[int] = None, **kwargs
    ) -> 1:
        """
        Returns the server address for document upload.

        :param group_id: Community ID (if the document will be uploaded to the community).
        """

    @api_method
    async def get_wall_upload_server(
        self, *, group_id: ty.Optional[int] = None, **kwargs
    ) -> 1:
        """
        Returns the server address for document upload onto a user"s or community"s wall.

        :param group_id: Community ID (if the document will be uploaded to the community).
        """

    @api_method
    async def save(
        self,
        *,
        file: str,
        title: ty.Optional[str] = None,
        tags: ty.Optional[str] = None,
        return_tags: bool = False,
        **kwargs
    ) -> 1:
        """
        Saves a document after [vk.com/dev/upload_files_2|uploading it to a server].

        :param file: This parameter is returned when the file is [vk.com/dev/upload_files_2|uploaded to the server].
        :param title: Document title.
        :param tags: Document tags.
        :param return_tags: No description provided
        """

    @api_method
    async def search(
        self,
        *,
        q: str,
        search_own: ty.Optional[bool] = None,
        count: int = 20,
        offset: ty.Optional[int] = None,
        return_tags: ty.Optional[bool] = None,
        **kwargs
    ) -> 1:
        """
        Returns a list of documents matching the search criteria.

        :param q: Search query string.
        :param search_own: No description provided
        :param count: Number of results to return.
        :param offset: Offset needed to return a specific subset of results.
        :param return_tags: No description provided
        """


class Donut(APIMethod):
    @api_method
    async def get_friends(
        self,
        *,
        owner_id: int,
        offset: int = 0,
        count: int = 10,
        fields: ty.Optional[ty.List[str]] = None,
        **kwargs
    ) -> 1:
        """
        No description provided

        :param owner_id: No description provided
        :param offset: No description provided
        :param count: No description provided
        :param fields: No description provided
        """

    @api_method
    async def get_subscription(self, *, owner_id: int, **kwargs) -> 1:
        """
        No description provided

        :param owner_id: No description provided
        """

    @api_method
    async def get_subscriptions(
        self,
        *,
        fields: ty.Optional[ty.Sequence] = None,
        offset: int = 0,
        count: int = 10,
        **kwargs
    ) -> 1:
        """
        Returns a list of user"s VK Donut subscriptions.

        :param fields: No description provided
        :param offset: No description provided
        :param count: No description provided
        """

    @api_method
    async def is_don(self, *, owner_id: int, **kwargs) -> 1:
        """
        No description provided

        :param owner_id: No description provided
        """


class Downloadedgames(APIMethod):
    @api_method
    async def get_paid_status(
        self, *, user_id: ty.Optional[int] = None, **kwargs
    ) -> 1:
        """
        No description provided

        :param user_id: No description provided
        """


class Fave(APIMethod):
    @api_method
    async def add_article(self, *, url: str, **kwargs) -> 1:
        """
        No description provided

        :param url: No description provided
        """

    @api_method
    async def add_classified(
        self, *, item_source: str, item_id: str, **kwargs
    ) -> 1:
        """
        Adds a link to user faves.

        :param item_source: Classifieds item source
        :param item_id: Classifieds item id
        """

    @api_method
    async def add_link(self, *, link: str, **kwargs) -> 1:
        """
        Adds a link to user faves.

        :param link: Link URL.
        """

    @api_method
    async def add_page(
        self,
        *,
        user_id: ty.Optional[int] = None,
        group_id: ty.Optional[int] = None,
        **kwargs
    ) -> 1:
        """
        No description provided

        :param user_id: No description provided
        :param group_id: No description provided
        """

    @api_method
    async def add_post(
        self,
        *,
        owner_id: int,
        id: int,
        access_key: ty.Optional[str] = None,
        **kwargs
    ) -> 1:
        """
        No description provided

        :param owner_id: No description provided
        :param id: No description provided
        :param access_key: No description provided
        """

    @api_method
    async def add_product(
        self,
        *,
        owner_id: int,
        id: int,
        access_key: ty.Optional[str] = None,
        **kwargs
    ) -> 1:
        """
        No description provided

        :param owner_id: No description provided
        :param id: No description provided
        :param access_key: No description provided
        """

    @api_method
    async def add_tag(
        self,
        *,
        name: ty.Optional[str] = None,
        position: str = "back",
        **kwargs
    ) -> 1:
        """
        No description provided

        :param name: No description provided
        :param position: No description provided
        """

    @api_method
    async def add_video(
        self,
        *,
        owner_id: int,
        id: int,
        access_key: ty.Optional[str] = None,
        **kwargs
    ) -> 1:
        """
        No description provided

        :param owner_id: No description provided
        :param id: No description provided
        :param access_key: No description provided
        """

    @api_method
    async def edit_tag(self, *, id: int, name: str, **kwargs) -> 1:
        """
        No description provided

        :param id: No description provided
        :param name: No description provided
        """

    @api_method
    async def get(
        self,
        *,
        extended: bool = False,
        item_type: ty.Optional[str] = None,
        tag_id: ty.Optional[int] = None,
        offset: ty.Optional[int] = None,
        count: int = 50,
        fields: ty.Optional[str] = None,
        is_from_snackbar: ty.Optional[bool] = None,
        **kwargs
    ) -> 1:
        """
        No description provided

        :param extended: "1" — to return additional "wall", "profiles", and "groups" fields. By default: "0".
        :param item_type: No description provided
        :param tag_id: Tag ID.
        :param offset: Offset needed to return a specific subset of users.
        :param count: Number of users to return.
        :param fields: No description provided
        :param is_from_snackbar: No description provided
        """

    @api_method
    async def get_pages(
        self,
        *,
        offset: ty.Optional[int] = None,
        count: int = 50,
        type: ty.Optional[str] = None,
        fields: ty.Optional[ty.Sequence] = None,
        tag_id: ty.Optional[int] = None,
        **kwargs
    ) -> 1:
        """
        No description provided

        :param offset: No description provided
        :param count: No description provided
        :param type: No description provided
        :param fields: No description provided
        :param tag_id: No description provided
        """

    @api_method
    async def get_tags(self, **kwargs) -> 1:
        """
        No description provided
        """

    @api_method
    async def mark_seen(self, **kwargs) -> 1:
        """
        No description provided
        """

    @api_method
    async def remove_article(
        self, *, owner_id: int, article_id: int, **kwargs
    ) -> 1:
        """
        No description provided

        :param owner_id: No description provided
        :param article_id: No description provided
        """

    @api_method
    async def remove_classified(
        self, *, item_source: str, item_id: str, **kwargs
    ) -> 1:
        """
        Removes link from the user"s faves.

        :param item_source: Classifieds item source
        :param item_id: Classifieds item id
        """

    @api_method
    async def remove_link(
        self,
        *,
        link_id: ty.Optional[str] = None,
        link: ty.Optional[str] = None,
        **kwargs
    ) -> 1:
        """
        Removes link from the user"s faves.

        :param link_id: Link ID (can be obtained by [vk.com/dev/faves.getLinks|faves.getLinks] method).
        :param link: Link URL
        """

    @api_method
    async def remove_page(
        self,
        *,
        user_id: ty.Optional[int] = None,
        group_id: ty.Optional[int] = None,
        **kwargs
    ) -> 1:
        """
        No description provided

        :param user_id: No description provided
        :param group_id: No description provided
        """

    @api_method
    async def remove_post(self, *, owner_id: int, id: int, **kwargs) -> 1:
        """
        No description provided

        :param owner_id: No description provided
        :param id: No description provided
        """

    @api_method
    async def remove_product(self, *, owner_id: int, id: int, **kwargs) -> 1:
        """
        No description provided

        :param owner_id: No description provided
        :param id: No description provided
        """

    @api_method
    async def remove_tag(self, *, id: int, **kwargs) -> 1:
        """
        No description provided

        :param id: No description provided
        """

    @api_method
    async def remove_video(self, *, owner_id: int, id: int, **kwargs) -> 1:
        """
        No description provided

        :param owner_id: No description provided
        :param id: No description provided
        """

    @api_method
    async def reorder_tags(self, *, ids: ty.Sequence, **kwargs) -> 1:
        """
        No description provided

        :param ids: No description provided
        """

    @api_method
    async def set_page_tags(
        self,
        *,
        user_id: ty.Optional[int] = None,
        group_id: ty.Optional[int] = None,
        tag_ids: ty.Optional[ty.Sequence] = None,
        **kwargs
    ) -> 1:
        """
        No description provided

        :param user_id: No description provided
        :param group_id: No description provided
        :param tag_ids: No description provided
        """

    @api_method
    async def set_tags(
        self,
        *,
        item_type: ty.Optional[str] = None,
        item_owner_id: ty.Optional[int] = None,
        item_id: ty.Optional[int] = None,
        tag_ids: ty.Optional[ty.Sequence] = None,
        link_id: ty.Optional[str] = None,
        link_url: ty.Optional[str] = None,
        **kwargs
    ) -> 1:
        """
        No description provided

        :param item_type: No description provided
        :param item_owner_id: No description provided
        :param item_id: No description provided
        :param tag_ids: No description provided
        :param link_id: No description provided
        :param link_url: No description provided
        """

    @api_method
    async def track_page_interaction(
        self,
        *,
        user_id: ty.Optional[int] = None,
        group_id: ty.Optional[int] = None,
        **kwargs
    ) -> 1:
        """
        No description provided

        :param user_id: No description provided
        :param group_id: No description provided
        """


class Friends(APIMethod):
    @api_method
    async def add(
        self,
        *,
        user_id: ty.Optional[int] = None,
        text: ty.Optional[str] = None,
        follow: ty.Optional[bool] = None,
        **kwargs
    ) -> 1:
        """
        Approves or creates a friend request.

        :param user_id: ID of the user whose friend request will be approved or to whom a friend request will be sent.
        :param text: Text of the message (up to 500 characters) for the friend request, if any.
        :param follow: "1" to pass an incoming request to followers list.
        """

    @api_method
    async def add_list(
        self,
        *,
        name: str,
        user_ids: ty.Optional[ty.Sequence] = None,
        **kwargs
    ) -> 1:
        """
        Creates a new friend list for the current user.

        :param name: Name of the friend list.
        :param user_ids: IDs of users to be added to the friend list.
        """

    @api_method
    async def are_friends(
        self,
        *,
        user_ids: ty.Sequence,
        need_sign: ty.Optional[bool] = None,
        extended: ty.Optional[bool] = None,
        **kwargs
    ) -> 1:
        """
        Checks the current user"s friendship status with other specified users.

        :param user_ids: IDs of the users whose friendship status to check.
        :param need_sign: "1" — to return "sign" field. "sign" is md5("{id}_{user_id}_{friends_status}_{application_secret}"), where id is current user ID. This field allows to check that data has not been modified by the client. By default: "0".
        :param extended: Return friend request read_state field
        """

    @api_method
    async def delete(
        self, *, user_id: ty.Optional[int] = None, **kwargs
    ) -> 1:
        """
        Declines a friend request or deletes a user from the current user"s friend list.

        :param user_id: ID of the user whose friend request is to be declined or who is to be deleted from the current user"s friend list.
        """

    @api_method
    async def delete_all_requests(self, **kwargs) -> 1:
        """
        Marks all incoming friend requests as viewed.
        """

    @api_method
    async def delete_list(self, *, list_id: int, **kwargs) -> 1:
        """
        Deletes a friend list of the current user.

        :param list_id: ID of the friend list to delete.
        """

    @api_method
    async def edit(
        self,
        *,
        user_id: int,
        list_ids: ty.Optional[ty.Sequence] = None,
        **kwargs
    ) -> 1:
        """
        Edits the friend lists of the selected user.

        :param user_id: ID of the user whose friend list is to be edited.
        :param list_ids: IDs of the friend lists to which to add the user.
        """

    @api_method
    async def edit_list(
        self,
        *,
        name: ty.Optional[str] = None,
        list_id: int,
        user_ids: ty.Optional[ty.Sequence] = None,
        add_user_ids: ty.Optional[ty.Sequence] = None,
        delete_user_ids: ty.Optional[ty.Sequence] = None,
        **kwargs
    ) -> 1:
        """
        Edits a friend list of the current user.

        :param name: Name of the friend list.
        :param list_id: Friend list ID.
        :param user_ids: IDs of users in the friend list.
        :param add_user_ids: (Applies if "user_ids" parameter is not set.), User IDs to add to the friend list.
        :param delete_user_ids: (Applies if "user_ids" parameter is not set.), User IDs to delete from the friend list.
        """

    @api_method
    async def get(
        self,
        *,
        user_id: ty.Optional[int] = None,
        order: ty.Optional[str] = None,
        list_id: ty.Optional[int] = None,
        count: int = 5000,
        offset: ty.Optional[int] = None,
        fields: ty.Optional[ty.Sequence] = None,
        name_case: ty.Optional[str] = None,
        ref: ty.Optional[str] = None,
        **kwargs
    ) -> 1:
        """
        Returns a list of user IDs or detailed information about a user"s friends.

        :param user_id: User ID. By default, the current user ID.
        :param order: Sort order: , "name" — by name (enabled only if the "fields" parameter is used), "hints" — by rating, similar to how friends are sorted in My friends section, , This parameter is available only for [vk.com/dev/standalone|desktop applications].
        :param list_id: ID of the friend list returned by the [vk.com/dev/friends.getLists|friends.getLists] method to be used as the source. This parameter is taken into account only when the uid parameter is set to the current user ID. This parameter is available only for [vk.com/dev/standalone|desktop applications].
        :param count: Number of friends to return.
        :param offset: Offset needed to return a specific subset of friends.
        :param fields: Profile fields to return. Sample values: "uid", "first_name", "last_name", "nickname", "sex", "bdate" (birthdate), "city", "country", "timezone", "photo", "photo_medium", "photo_big", "domain", "has_mobile", "rate", "contacts", "education".
        :param name_case: Case for declension of user name and surname: , "nom" — nominative (default) , "gen" — genitive , "dat" — dative , "acc" — accusative , "ins" — instrumental , "abl" — prepositional
        :param ref: No description provided
        """

    @api_method
    async def get_app_users(self, **kwargs) -> 1:
        """
        Returns a list of IDs of the current user"s friends who installed the application.
        """

    @api_method
    async def get_by_phones(
        self,
        *,
        phones: ty.Optional[ty.List[str]] = None,
        fields: ty.Optional[ty.Sequence] = None,
        **kwargs
    ) -> 1:
        """
        Returns a list of the current user"s friends whose phone numbers, validated or specified in a profile, are in a given list.

        :param phones: List of phone numbers in MSISDN format (maximum 1000). Example: "+79219876543,+79111234567"
        :param fields: Profile fields to return. Sample values: "nickname", "screen_name", "sex", "bdate" (birthdate), "city", "country", "timezone", "photo", "photo_medium", "photo_big", "has_mobile", "rate", "contacts", "education", "online, counters".
        """

    @api_method
    async def get_lists(
        self,
        *,
        user_id: ty.Optional[int] = None,
        return_system: ty.Optional[bool] = None,
        **kwargs
    ) -> 1:
        """
        Returns a list of the user"s friend lists.

        :param user_id: User ID.
        :param return_system: "1" — to return system friend lists. By default: "0".
        """

    @api_method
    async def get_mutual(
        self,
        *,
        source_uid: ty.Optional[int] = None,
        target_uid: ty.Optional[int] = None,
        target_uids: ty.Optional[ty.Sequence] = None,
        order: ty.Optional[str] = None,
        count: ty.Optional[int] = None,
        offset: ty.Optional[int] = None,
        **kwargs
    ) -> 1:
        """
        Returns a list of user IDs of the mutual friends of two users.

        :param source_uid: ID of the user whose friends will be checked against the friends of the user specified in "target_uid".
        :param target_uid: ID of the user whose friends will be checked against the friends of the user specified in "source_uid".
        :param target_uids: IDs of the users whose friends will be checked against the friends of the user specified in "source_uid".
        :param order: Sort order: "random" — random order
        :param count: Number of mutual friends to return.
        :param offset: Offset needed to return a specific subset of mutual friends.
        """

    @api_method
    async def get_online(
        self,
        *,
        user_id: ty.Optional[int] = None,
        list_id: ty.Optional[int] = None,
        online_mobile: ty.Optional[bool] = None,
        order: ty.Optional[str] = None,
        count: ty.Optional[int] = None,
        offset: ty.Optional[int] = None,
        **kwargs
    ) -> 1:
        """
        Returns a list of user IDs of a user"s friends who are online.

        :param user_id: User ID.
        :param list_id: Friend list ID. If this parameter is not set, information about all online friends is returned.
        :param online_mobile: "1" — to return an additional "online_mobile" field, "0" — (default),
        :param order: Sort order: "random" — random order
        :param count: Number of friends to return.
        :param offset: Offset needed to return a specific subset of friends.
        """

    @api_method
    async def get_recent(self, *, count: int = 100, **kwargs) -> 1:
        """
        Returns a list of user IDs of the current user"s recently added friends.

        :param count: Number of recently added friends to return.
        """

    @api_method
    async def get_requests(
        self,
        *,
        offset: ty.Optional[int] = None,
        count: int = 100,
        extended: ty.Optional[bool] = None,
        need_mutual: ty.Optional[bool] = None,
        out: ty.Optional[bool] = None,
        sort: ty.Optional[int] = None,
        need_viewed: bool = 0,
        suggested: ty.Optional[bool] = None,
        ref: ty.Optional[str] = None,
        fields: ty.Optional[ty.Sequence] = None,
        **kwargs
    ) -> 1:
        """
        Returns information about the current user"s incoming and outgoing friend requests.

        :param offset: Offset needed to return a specific subset of friend requests.
        :param count: Number of friend requests to return (default 100, maximum 1000).
        :param extended: "1" — to return response messages from users who have sent a friend request or, if "suggested" is set to "1", to return a list of suggested friends
        :param need_mutual: "1" — to return a list of mutual friends (up to 20), if any
        :param out: "1" — to return outgoing requests, "0" — to return incoming requests (default)
        :param sort: Sort order: "1" — by number of mutual friends, "0" — by date
        :param need_viewed: No description provided
        :param suggested: "1" — to return a list of suggested friends, "0" — to return friend requests (default)
        :param ref: No description provided
        :param fields: No description provided
        """

    @api_method
    async def get_suggestions(
        self,
        *,
        filter: ty.Optional[
            ty.Sequence[tye.Literal["mutual", "contacts", "mutual_contacts"]]
        ] = None,
        count: int = 500,
        offset: ty.Optional[int] = None,
        fields: ty.Optional[ty.Sequence] = None,
        name_case: ty.Optional[str] = None,
        **kwargs
    ) -> 1:
        """
        Returns a list of profiles of users whom the current user may know.

        :param filter: Types of potential friends to return: "mutual" — users with many mutual friends , "contacts" — users found with the [vk.com/dev/account.importContacts|account.importContacts] method , "mutual_contacts" — users who imported the same contacts as the current user with the [vk.com/dev/account.importContacts|account.importContacts] method
        :param count: Number of suggestions to return.
        :param offset: Offset needed to return a specific subset of suggestions.
        :param fields: Profile fields to return. Sample values: "nickname", "screen_name", "sex", "bdate" (birthdate), "city", "country", "timezone", "photo", "photo_medium", "photo_big", "has_mobile", "rate", "contacts", "education", "online", "counters".
        :param name_case: Case for declension of user name and surname: , "nom" — nominative (default) , "gen" — genitive , "dat" — dative , "acc" — accusative , "ins" — instrumental , "abl" — prepositional
        """

    @api_method
    async def search(
        self,
        *,
        user_id: int,
        q: ty.Optional[str] = None,
        fields: ty.Optional[ty.Sequence] = None,
        name_case: str = "Nom",
        offset: ty.Optional[int] = None,
        count: int = 20,
        **kwargs
    ) -> 1:
        """
        Returns a list of friends matching the search criteria.

        :param user_id: User ID.
        :param q: Search query string (e.g., "Vasya Babich").
        :param fields: Profile fields to return. Sample values: "nickname", "screen_name", "sex", "bdate" (birthdate), "city", "country", "timezone", "photo", "photo_medium", "photo_big", "has_mobile", "rate", "contacts", "education", "online",
        :param name_case: Case for declension of user name and surname: "nom" — nominative (default), "gen" — genitive , "dat" — dative, "acc" — accusative , "ins" — instrumental , "abl" — prepositional
        :param offset: Offset needed to return a specific subset of friends.
        :param count: Number of friends to return.
        """


class Gifts(APIMethod):
    @api_method
    async def get(
        self,
        *,
        user_id: ty.Optional[int] = None,
        count: ty.Optional[int] = None,
        offset: ty.Optional[int] = None,
        **kwargs
    ) -> 1:
        """
        Returns a list of user gifts.

        :param user_id: User ID.
        :param count: Number of gifts to return.
        :param offset: Offset needed to return a specific subset of results.
        """


class Groups(APIMethod):
    @api_method
    async def add_address(
        self,
        *,
        group_id: int,
        title: str,
        address: str,
        additional_address: ty.Optional[str] = None,
        country_id: int,
        city_id: int,
        metro_id: ty.Optional[int] = None,
        latitude: float,
        longitude: float,
        phone: ty.Optional[str] = None,
        work_info_status: str = "no_information",
        timetable: ty.Optional[str] = None,
        is_main_address: ty.Optional[bool] = None,
        **kwargs
    ) -> 1:
        """
        No description provided

        :param group_id: No description provided
        :param title: No description provided
        :param address: No description provided
        :param additional_address: No description provided
        :param country_id: No description provided
        :param city_id: No description provided
        :param metro_id: No description provided
        :param latitude: No description provided
        :param longitude: No description provided
        :param phone: No description provided
        :param work_info_status: No description provided
        :param timetable: No description provided
        :param is_main_address: No description provided
        """

    @api_method
    async def add_callback_server(
        self,
        *,
        group_id: int,
        url: str,
        title: str,
        secret_key: ty.Optional[str] = None,
        **kwargs
    ) -> 1:
        """
        No description provided

        :param group_id: No description provided
        :param url: No description provided
        :param title: No description provided
        :param secret_key: No description provided
        """

    @api_method
    async def add_link(
        self,
        *,
        group_id: int,
        link: str,
        text: ty.Optional[str] = None,
        **kwargs
    ) -> 1:
        """
        Allows to add a link to the community.

        :param group_id: Community ID.
        :param link: Link URL.
        :param text: Description text for the link.
        """

    @api_method
    async def approve_request(
        self, *, group_id: int, user_id: int, **kwargs
    ) -> 1:
        """
        Allows to approve join request to the community.

        :param group_id: Community ID.
        :param user_id: User ID.
        """

    @api_method
    async def ban(
        self,
        *,
        group_id: int,
        owner_id: ty.Optional[int] = None,
        end_date: ty.Optional[int] = None,
        reason: ty.Optional[int] = None,
        comment: ty.Optional[str] = None,
        comment_visible: ty.Optional[bool] = None,
        **kwargs
    ) -> 1:
        """
        No description provided

        :param group_id: No description provided
        :param owner_id: No description provided
        :param end_date: No description provided
        :param reason: No description provided
        :param comment: No description provided
        :param comment_visible: No description provided
        """

    @api_method
    async def create(
        self,
        *,
        title: str,
        description: ty.Optional[str] = None,
        type: str = "group",
        public_category: ty.Optional[int] = None,
        subtype: ty.Optional[int] = None,
        **kwargs
    ) -> 1:
        """
        Creates a new community.

        :param title: Community title.
        :param description: Community description (ignored for "type" = "public").
        :param type: Community type. Possible values: *"group" – group,, *"event" – event,, *"public" – public page
        :param public_category: Category ID (for "type" = "public" only).
        :param subtype: Public page subtype. Possible values: *"1" – place or small business,, *"2" – company, organization or website,, *"3" – famous person or group of people,, *"4" – product or work of art.
        """

    @api_method
    async def delete_address(
        self, *, group_id: int, address_id: int, **kwargs
    ) -> 1:
        """
        No description provided

        :param group_id: No description provided
        :param address_id: No description provided
        """

    @api_method
    async def delete_callback_server(
        self, *, group_id: int, server_id: int, **kwargs
    ) -> 1:
        """
        No description provided

        :param group_id: No description provided
        :param server_id: No description provided
        """

    @api_method
    async def delete_link(
        self, *, group_id: int, link_id: int, **kwargs
    ) -> 1:
        """
        Allows to delete a link from the community.

        :param group_id: Community ID.
        :param link_id: Link ID.
        """

    @api_method
    async def disable_online(self, *, group_id: int, **kwargs) -> 1:
        """
        No description provided

        :param group_id: No description provided
        """

    @api_method
    async def edit(
        self,
        *,
        group_id: int,
        title: ty.Optional[str] = None,
        description: ty.Optional[str] = None,
        screen_name: ty.Optional[str] = None,
        access: ty.Optional[int] = None,
        website: ty.Optional[str] = None,
        subject: ty.Optional[str] = None,
        email: ty.Optional[str] = None,
        phone: ty.Optional[str] = None,
        rss: ty.Optional[str] = None,
        event_start_date: ty.Optional[int] = None,
        event_finish_date: ty.Optional[int] = None,
        event_group_id: ty.Optional[int] = None,
        public_category: ty.Optional[int] = None,
        public_subcategory: ty.Optional[int] = None,
        public_date: ty.Optional[str] = None,
        wall: ty.Optional[int] = None,
        topics: ty.Optional[int] = None,
        photos: ty.Optional[int] = None,
        video: ty.Optional[int] = None,
        audio: ty.Optional[int] = None,
        links: ty.Optional[bool] = None,
        events: ty.Optional[bool] = None,
        places: ty.Optional[bool] = None,
        contacts: ty.Optional[bool] = None,
        docs: ty.Optional[int] = None,
        wiki: ty.Optional[int] = None,
        messages: ty.Optional[bool] = None,
        articles: ty.Optional[bool] = None,
        addresses: ty.Optional[bool] = None,
        age_limits: int = 1,
        market: ty.Optional[bool] = None,
        market_comments: ty.Optional[bool] = None,
        market_country: ty.Optional[ty.Sequence] = None,
        market_city: ty.Optional[ty.Sequence] = None,
        market_currency: ty.Optional[int] = None,
        market_contact: ty.Optional[int] = None,
        market_wiki: ty.Optional[int] = None,
        obscene_filter: ty.Optional[bool] = None,
        obscene_stopwords: ty.Optional[bool] = None,
        obscene_words: ty.Optional[ty.List[str]] = None,
        main_section: ty.Optional[int] = None,
        secondary_section: ty.Optional[int] = None,
        country: ty.Optional[int] = None,
        city: ty.Optional[int] = None,
        **kwargs
    ) -> 1:
        """
        Edits a community.

        :param group_id: Community ID.
        :param title: Community title.
        :param description: Community description.
        :param screen_name: Community screen name.
        :param access: Community type. Possible values: *"0" – open,, *"1" – closed,, *"2" – private.
        :param website: Website that will be displayed in the community information field.
        :param subject: Community subject. Possible values: , *"1" – auto/moto,, *"2" – activity holidays,, *"3" – business,, *"4" – pets,, *"5" – health,, *"6" – dating and communication, , *"7" – games,, *"8" – IT (computers and software),, *"9" – cinema,, *"10" – beauty and fashion,, *"11" – cooking,, *"12" – art and culture,, *"13" – literature,, *"14" – mobile services and internet,, *"15" – music,, *"16" – science and technology,, *"17" – real estate,, *"18" – news and media,, *"19" – security,, *"20" – education,, *"21" – home and renovations,, *"22" – politics,, *"23" – food,, *"24" – industry,, *"25" – travel,, *"26" – work,, *"27" – entertainment,, *"28" – religion,, *"29" – family,, *"30" – sports,, *"31" – insurance,, *"32" – television,, *"33" – goods and services,, *"34" – hobbies,, *"35" – finance,, *"36" – photo,, *"37" – esoterics,, *"38" – electronics and appliances,, *"39" – erotic,, *"40" – humor,, *"41" – society, humanities,, *"42" – design and graphics.
        :param email: Organizer email (for events).
        :param phone: Organizer phone number (for events).
        :param rss: RSS feed address for import (available only to communities with special permission. Contact vk.com/support to get it.
        :param event_start_date: Event start date in Unixtime format.
        :param event_finish_date: Event finish date in Unixtime format.
        :param event_group_id: Organizer community ID (for events only).
        :param public_category: Public page category ID.
        :param public_subcategory: Public page subcategory ID.
        :param public_date: Founding date of a company or organization owning the community in "dd.mm.YYYY" format.
        :param wall: Wall settings. Possible values: *"0" – disabled,, *"1" – open,, *"2" – limited (groups and events only),, *"3" – closed (groups and events only).
        :param topics: Board topics settings. Possbile values: , *"0" – disabled,, *"1" – open,, *"2" – limited (for groups and events only).
        :param photos: Photos settings. Possible values: *"0" – disabled,, *"1" – open,, *"2" – limited (for groups and events only).
        :param video: Video settings. Possible values: *"0" – disabled,, *"1" – open,, *"2" – limited (for groups and events only).
        :param audio: Audio settings. Possible values: *"0" – disabled,, *"1" – open,, *"2" – limited (for groups and events only).
        :param links: Links settings (for public pages only). Possible values: *"0" – disabled,, *"1" – enabled.
        :param events: Events settings (for public pages only). Possible values: *"0" – disabled,, *"1" – enabled.
        :param places: Places settings (for public pages only). Possible values: *"0" – disabled,, *"1" – enabled.
        :param contacts: Contacts settings (for public pages only). Possible values: *"0" – disabled,, *"1" – enabled.
        :param docs: Documents settings. Possible values: *"0" – disabled,, *"1" – open,, *"2" – limited (for groups and events only).
        :param wiki: Wiki pages settings. Possible values: *"0" – disabled,, *"1" – open,, *"2" – limited (for groups and events only).
        :param messages: Community messages. Possible values: *"0" — disabled,, *"1" — enabled.
        :param articles: No description provided
        :param addresses: No description provided
        :param age_limits: Community age limits. Possible values: *"1" — no limits,, *"2" — 16+,, *"3" — 18+.
        :param market: Market settings. Possible values: *"0" – disabled,, *"1" – enabled.
        :param market_comments: market comments settings. Possible values: *"0" – disabled,, *"1" – enabled.
        :param market_country: Market delivery countries.
        :param market_city: Market delivery cities (if only one country is specified).
        :param market_currency: Market currency settings. Possbile values: , *"643" – Russian rubles,, *"980" – Ukrainian hryvnia,, *"398" – Kazakh tenge,, *"978" – Euro,, *"840" – US dollars
        :param market_contact: Seller contact for market. Set "0" for community messages.
        :param market_wiki: ID of a wiki page with market description.
        :param obscene_filter: Obscene expressions filter in comments. Possible values: , *"0" – disabled,, *"1" – enabled.
        :param obscene_stopwords: Stopwords filter in comments. Possible values: , *"0" – disabled,, *"1" – enabled.
        :param obscene_words: Keywords for stopwords filter.
        :param main_section: No description provided
        :param secondary_section: No description provided
        :param country: Country of the community.
        :param city: City of the community.
        """

    @api_method
    async def edit_address(
        self,
        *,
        group_id: int,
        address_id: int,
        title: ty.Optional[str] = None,
        address: ty.Optional[str] = None,
        additional_address: ty.Optional[str] = None,
        country_id: ty.Optional[int] = None,
        city_id: ty.Optional[int] = None,
        metro_id: ty.Optional[int] = None,
        latitude: ty.Optional[float] = None,
        longitude: ty.Optional[float] = None,
        phone: ty.Optional[str] = None,
        work_info_status: ty.Optional[str] = None,
        timetable: ty.Optional[str] = None,
        is_main_address: ty.Optional[bool] = None,
        **kwargs
    ) -> 1:
        """
        No description provided

        :param group_id: No description provided
        :param address_id: No description provided
        :param title: No description provided
        :param address: No description provided
        :param additional_address: No description provided
        :param country_id: No description provided
        :param city_id: No description provided
        :param metro_id: No description provided
        :param latitude: No description provided
        :param longitude: No description provided
        :param phone: No description provided
        :param work_info_status: No description provided
        :param timetable: No description provided
        :param is_main_address: No description provided
        """

    @api_method
    async def edit_callback_server(
        self,
        *,
        group_id: int,
        server_id: int,
        url: str,
        title: str,
        secret_key: ty.Optional[str] = None,
        **kwargs
    ) -> 1:
        """
        No description provided

        :param group_id: No description provided
        :param server_id: No description provided
        :param url: No description provided
        :param title: No description provided
        :param secret_key: No description provided
        """

    @api_method
    async def edit_link(
        self,
        *,
        group_id: int,
        link_id: int,
        text: ty.Optional[str] = None,
        **kwargs
    ) -> 1:
        """
        Allows to edit a link in the community.

        :param group_id: Community ID.
        :param link_id: Link ID.
        :param text: New description text for the link.
        """

    @api_method
    async def edit_manager(
        self,
        *,
        group_id: int,
        user_id: int,
        role: ty.Optional[str] = None,
        is_contact: ty.Optional[bool] = None,
        contact_position: ty.Optional[str] = None,
        contact_phone: ty.Optional[str] = None,
        contact_email: ty.Optional[str] = None,
        **kwargs
    ) -> 1:
        """
        Allows to add, remove or edit the community manager.

        :param group_id: Community ID.
        :param user_id: User ID.
        :param role: Manager role. Possible values: *"moderator",, *"editor",, *"administrator",, *"advertiser".
        :param is_contact: "1" — to show the manager in Contacts block of the community.
        :param contact_position: Position to show in Contacts block.
        :param contact_phone: Contact phone.
        :param contact_email: Contact e-mail.
        """

    @api_method
    async def enable_online(self, *, group_id: int, **kwargs) -> 1:
        """
        No description provided

        :param group_id: No description provided
        """

    @api_method
    async def get(
        self,
        *,
        user_id: ty.Optional[int] = None,
        extended: ty.Optional[bool] = None,
        filter: ty.Optional[ty.Sequence] = None,
        fields: ty.Optional[ty.Sequence] = None,
        offset: ty.Optional[int] = None,
        count: ty.Optional[int] = None,
        **kwargs
    ) -> 1:
        """
        Returns a list of the communities to which a user belongs.

        :param user_id: User ID.
        :param extended: "1" — to return complete information about a user"s communities, "0" — to return a list of community IDs without any additional fields (default),
        :param filter: Types of communities to return: "admin" — to return communities administered by the user , "editor" — to return communities where the user is an administrator or editor, "moder" — to return communities where the user is an administrator, editor, or moderator, "groups" — to return only groups, "publics" — to return only public pages, "events" — to return only events
        :param fields: Profile fields to return.
        :param offset: Offset needed to return a specific subset of communities.
        :param count: Number of communities to return.
        """

    @api_method
    async def get_addresses(
        self,
        *,
        group_id: int,
        address_ids: ty.Optional[ty.Sequence] = None,
        latitude: ty.Optional[float] = None,
        longitude: ty.Optional[float] = None,
        offset: ty.Optional[int] = None,
        count: int = 10,
        fields: ty.Optional[ty.Sequence] = None,
        **kwargs
    ) -> 1:
        """
        Returns a list of community addresses.

        :param group_id: ID or screen name of the community.
        :param address_ids: No description provided
        :param latitude: Latitude of  the user geo position.
        :param longitude: Longitude of the user geo position.
        :param offset: Offset needed to return a specific subset of community addresses.
        :param count: Number of community addresses to return.
        :param fields: Address fields
        """

    @api_method
    async def get_banned(
        self,
        *,
        group_id: int,
        offset: ty.Optional[int] = None,
        count: int = 20,
        fields: ty.Optional[ty.Sequence] = None,
        owner_id: ty.Optional[int] = None,
        **kwargs
    ) -> 1:
        """
        Returns a list of users on a community blacklist.

        :param group_id: Community ID.
        :param offset: Offset needed to return a specific subset of users.
        :param count: Number of users to return.
        :param fields: No description provided
        :param owner_id: No description provided
        """

    @api_method
    async def get_by_id(
        self,
        *,
        group_ids: ty.Optional[ty.List[ty.Union[str, int]]] = None,
        group_id: ty.Optional[str] = None,
        fields: ty.Optional[ty.Sequence] = None,
        **kwargs
    ) -> 1:
        """
        Returns information about communities by their IDs.

        :param group_ids: IDs or screen names of communities.
        :param group_id: ID or screen name of the community.
        :param fields: Group fields to return.
        """

    @api_method
    async def get_callback_confirmation_code(
        self, *, group_id: int, **kwargs
    ) -> 1:
        """
        Returns Callback API confirmation code for the community.

        :param group_id: Community ID.
        """

    @api_method
    async def get_callback_servers(
        self,
        *,
        group_id: int,
        server_ids: ty.Optional[ty.Sequence] = None,
        **kwargs
    ) -> 1:
        """
        No description provided

        :param group_id: No description provided
        :param server_ids: No description provided
        """

    @api_method
    async def get_callback_settings(
        self, *, group_id: int, server_id: ty.Optional[int] = None, **kwargs
    ) -> 1:
        """
        Returns [vk.com/dev/callback_api|Callback API] notifications settings.

        :param group_id: Community ID.
        :param server_id: Server ID.
        """

    @api_method
    async def get_catalog(
        self,
        *,
        category_id: ty.Optional[int] = None,
        subcategory_id: ty.Optional[int] = None,
        **kwargs
    ) -> 1:
        """
        Returns communities list for a catalog category.

        :param category_id: Category id received from [vk.com/dev/groups.getCatalogInfo|groups.getCatalogInfo].
        :param subcategory_id: Subcategory id received from [vk.com/dev/groups.getCatalogInfo|groups.getCatalogInfo].
        """

    @api_method
    async def get_catalog_info(
        self, *, extended: bool = 0, subcategories: bool = 0, **kwargs
    ) -> 1:
        """
        Returns categories list for communities catalog

        :param extended: 1 – to return communities count and three communities for preview. By default: 0.
        :param subcategories: 1 – to return subcategories info. By default: 0.
        """

    @api_method
    async def get_invited_users(
        self,
        *,
        group_id: int,
        offset: ty.Optional[int] = None,
        count: int = 20,
        fields: ty.Optional[ty.Sequence] = None,
        name_case: ty.Optional[str] = None,
        **kwargs
    ) -> 1:
        """
        Returns invited users list of a community

        :param group_id: Group ID to return invited users for.
        :param offset: Offset needed to return a specific subset of results.
        :param count: Number of results to return.
        :param fields: List of additional fields to be returned. Available values: "sex, bdate, city, country, photo_50, photo_100, photo_200_orig, photo_200, photo_400_orig, photo_max, photo_max_orig, online, online_mobile, lists, domain, has_mobile, contacts, connections, site, education, universities, schools, can_post, can_see_all_posts, can_see_audio, can_write_private_message, status, last_seen, common_count, relation, relatives, counters".
        :param name_case: Case for declension of user name and surname. Possible values: *"nom" — nominative (default),, *"gen" — genitive,, *"dat" — dative,, *"acc" — accusative, , *"ins" — instrumental,, *"abl" — prepositional.
        """

    @api_method
    async def get_invites(
        self,
        *,
        offset: ty.Optional[int] = None,
        count: int = 20,
        extended: ty.Optional[bool] = None,
        **kwargs
    ) -> 1:
        """
        Returns a list of invitations to join communities and events.

        :param offset: Offset needed to return a specific subset of invitations.
        :param count: Number of invitations to return.
        :param extended: "1" — to return additional [vk.com/dev/fields_groups|fields] for communities..
        """

    @api_method
    async def get_long_poll_server(self, *, group_id: int, **kwargs) -> 1:
        """
        Returns the data needed to query a Long Poll server for events

        :param group_id: Community ID
        """

    @api_method
    async def get_long_poll_settings(self, *, group_id: int, **kwargs) -> 1:
        """
        Returns Long Poll notification settings

        :param group_id: Community ID.
        """

    @api_method
    async def get_members(
        self,
        *,
        group_id: ty.Optional[str] = None,
        sort: str = "id_asc",
        offset: ty.Optional[int] = None,
        count: int = 1000,
        fields: ty.Optional[ty.Sequence] = None,
        filter: ty.Optional[str] = None,
        **kwargs
    ) -> 1:
        """
        Returns a list of community members.

        :param group_id: ID or screen name of the community.
        :param sort: Sort order. Available values: "id_asc", "id_desc", "time_asc", "time_desc". "time_asc" and "time_desc" are availavle only if the method is called by the group"s "moderator".
        :param offset: Offset needed to return a specific subset of community members.
        :param count: Number of community members to return.
        :param fields: List of additional fields to be returned. Available values: "sex, bdate, city, country, photo_50, photo_100, photo_200_orig, photo_200, photo_400_orig, photo_max, photo_max_orig, online, online_mobile, lists, domain, has_mobile, contacts, connections, site, education, universities, schools, can_post, can_see_all_posts, can_see_audio, can_write_private_message, status, last_seen, common_count, relation, relatives, counters".
        :param filter: *"friends" – only friends in this community will be returned,, *"unsure" – only those who pressed "I may attend" will be returned (if it"s an event).
        """

    @api_method
    async def get_requests(
        self,
        *,
        group_id: int,
        offset: ty.Optional[int] = None,
        count: int = 20,
        fields: ty.Optional[ty.Sequence] = None,
        **kwargs
    ) -> 1:
        """
        Returns a list of requests to the community.

        :param group_id: Community ID.
        :param offset: Offset needed to return a specific subset of results.
        :param count: Number of results to return.
        :param fields: Profile fields to return.
        """

    @api_method
    async def get_settings(self, *, group_id: int, **kwargs) -> 1:
        """
        Returns community settings.

        :param group_id: Community ID.
        """

    @api_method
    async def get_tag_list(self, *, group_id: int, **kwargs) -> 1:
        """
        List of group"s tags

        :param group_id: No description provided
        """

    @api_method
    async def get_token_permissions(self, **kwargs) -> 1:
        """
        No description provided
        """

    @api_method
    async def invite(self, *, group_id: int, user_id: int, **kwargs) -> 1:
        """
        Allows to invite friends to the community.

        :param group_id: Community ID.
        :param user_id: User ID.
        """

    @api_method
    async def is_member(
        self,
        *,
        group_id: str,
        user_id: ty.Optional[int] = None,
        user_ids: ty.Optional[ty.Sequence] = None,
        extended: ty.Optional[bool] = None,
        **kwargs
    ) -> 1:
        """
        Returns information specifying whether a user is a member of a community.

        :param group_id: ID or screen name of the community.
        :param user_id: User ID.
        :param user_ids: User IDs.
        :param extended: "1" — to return an extended response with additional fields. By default: "0".
        """

    @api_method
    async def join(
        self,
        *,
        group_id: ty.Optional[int] = None,
        not_sure: ty.Optional[str] = None,
        **kwargs
    ) -> 1:
        """
        With this method you can join the group or public page, and also confirm your participation in an event.

        :param group_id: ID or screen name of the community.
        :param not_sure: Optional parameter which is taken into account when "gid" belongs to the event: "1" — Perhaps I will attend, "0" — I will be there for sure (default), ,
        """

    @api_method
    async def leave(self, *, group_id: int, **kwargs) -> 1:
        """
        With this method you can leave a group, public page, or event.

        :param group_id: ID or screen name of the community.
        """

    @api_method
    async def remove_user(
        self, *, group_id: int, user_id: int, **kwargs
    ) -> 1:
        """
        Removes a user from the community.

        :param group_id: Community ID.
        :param user_id: User ID.
        """

    @api_method
    async def reorder_link(
        self,
        *,
        group_id: int,
        link_id: int,
        after: ty.Optional[int] = None,
        **kwargs
    ) -> 1:
        """
        Allows to reorder links in the community.

        :param group_id: Community ID.
        :param link_id: Link ID.
        :param after: ID of the link after which to place the link with "link_id".
        """

    @api_method
    async def search(
        self,
        *,
        q: str,
        type: ty.Optional[str] = None,
        country_id: ty.Optional[int] = None,
        city_id: ty.Optional[int] = None,
        future: ty.Optional[bool] = None,
        market: ty.Optional[bool] = None,
        sort: ty.Optional[int] = None,
        offset: ty.Optional[int] = None,
        count: int = 20,
        **kwargs
    ) -> 1:
        """
        Returns a list of communities matching the search criteria.

        :param q: Search query string.
        :param type: Community type. Possible values: "group, page, event."
        :param country_id: Country ID.
        :param city_id: City ID. If this parameter is transmitted, country_id is ignored.
        :param future: "1" — to return only upcoming events. Works with the "type" = "event" only.
        :param market: "1" — to return communities with enabled market only.
        :param sort: Sort order. Possible values: *"0" — default sorting (similar the full version of the site),, *"1" — by growth speed,, *"2"— by the "day attendance/members number" ratio,, *"3" — by the "Likes number/members number" ratio,, *"4" — by the "comments number/members number" ratio,, *"5" — by the "boards entries number/members number" ratio.
        :param offset: Offset needed to return a specific subset of results.
        :param count: Number of communities to return. "Note that you can not receive more than first thousand of results, regardless of "count" and "offset" values."
        """

    @api_method
    async def set_callback_settings(
        self,
        *,
        group_id: int,
        server_id: ty.Optional[int] = None,
        api_version: ty.Optional[str] = None,
        message_new: ty.Optional[bool] = None,
        message_reply: ty.Optional[bool] = None,
        message_allow: ty.Optional[bool] = None,
        message_edit: ty.Optional[bool] = None,
        message_deny: ty.Optional[bool] = None,
        message_typing_state: ty.Optional[bool] = None,
        photo_new: ty.Optional[bool] = None,
        audio_new: ty.Optional[bool] = None,
        video_new: ty.Optional[bool] = None,
        wall_reply_new: ty.Optional[bool] = None,
        wall_reply_edit: ty.Optional[bool] = None,
        wall_reply_delete: ty.Optional[bool] = None,
        wall_reply_restore: ty.Optional[bool] = None,
        wall_post_new: ty.Optional[bool] = None,
        wall_repost: ty.Optional[bool] = None,
        board_post_new: ty.Optional[bool] = None,
        board_post_edit: ty.Optional[bool] = None,
        board_post_restore: ty.Optional[bool] = None,
        board_post_delete: ty.Optional[bool] = None,
        photo_comment_new: ty.Optional[bool] = None,
        photo_comment_edit: ty.Optional[bool] = None,
        photo_comment_delete: ty.Optional[bool] = None,
        photo_comment_restore: ty.Optional[bool] = None,
        video_comment_new: ty.Optional[bool] = None,
        video_comment_edit: ty.Optional[bool] = None,
        video_comment_delete: ty.Optional[bool] = None,
        video_comment_restore: ty.Optional[bool] = None,
        market_comment_new: ty.Optional[bool] = None,
        market_comment_edit: ty.Optional[bool] = None,
        market_comment_delete: ty.Optional[bool] = None,
        market_comment_restore: ty.Optional[bool] = None,
        market_order_new: ty.Optional[bool] = None,
        market_order_edit: ty.Optional[bool] = None,
        poll_vote_new: ty.Optional[bool] = None,
        group_join: ty.Optional[bool] = None,
        group_leave: ty.Optional[bool] = None,
        group_change_settings: ty.Optional[bool] = None,
        group_change_photo: ty.Optional[bool] = None,
        group_officers_edit: ty.Optional[bool] = None,
        user_block: ty.Optional[bool] = None,
        user_unblock: ty.Optional[bool] = None,
        lead_forms_new: ty.Optional[bool] = None,
        like_add: ty.Optional[bool] = None,
        like_remove: ty.Optional[bool] = None,
        message_event: ty.Optional[bool] = None,
        donut_subscription_create: ty.Optional[bool] = None,
        donut_subscription_prolonged: ty.Optional[bool] = None,
        donut_subscription_cancelled: ty.Optional[bool] = None,
        donut_subscription_price_changed: ty.Optional[bool] = None,
        donut_subscription_expired: ty.Optional[bool] = None,
        donut_money_withdraw: ty.Optional[bool] = None,
        donut_money_withdraw_error: ty.Optional[bool] = None,
        **kwargs
    ) -> 1:
        """
        Allow to set notifications settings for group.

        :param group_id: Community ID.
        :param server_id: Server ID.
        :param api_version: No description provided
        :param message_new: A new incoming message has been received ("0" — disabled, "1" — enabled).
        :param message_reply: A new outcoming message has been received ("0" — disabled, "1" — enabled).
        :param message_allow: Allowed messages notifications ("0" — disabled, "1" — enabled).
        :param message_edit: No description provided
        :param message_deny: Denied messages notifications ("0" — disabled, "1" — enabled).
        :param message_typing_state: No description provided
        :param photo_new: New photos notifications ("0" — disabled, "1" — enabled).
        :param audio_new: New audios notifications ("0" — disabled, "1" — enabled).
        :param video_new: New videos notifications ("0" — disabled, "1" — enabled).
        :param wall_reply_new: New wall replies notifications ("0" — disabled, "1" — enabled).
        :param wall_reply_edit: Wall replies edited notifications ("0" — disabled, "1" — enabled).
        :param wall_reply_delete: A wall comment has been deleted ("0" — disabled, "1" — enabled).
        :param wall_reply_restore: A wall comment has been restored ("0" — disabled, "1" — enabled).
        :param wall_post_new: New wall posts notifications ("0" — disabled, "1" — enabled).
        :param wall_repost: New wall posts notifications ("0" — disabled, "1" — enabled).
        :param board_post_new: New board posts notifications ("0" — disabled, "1" — enabled).
        :param board_post_edit: Board posts edited notifications ("0" — disabled, "1" — enabled).
        :param board_post_restore: Board posts restored notifications ("0" — disabled, "1" — enabled).
        :param board_post_delete: Board posts deleted notifications ("0" — disabled, "1" — enabled).
        :param photo_comment_new: New comment to photo notifications ("0" — disabled, "1" — enabled).
        :param photo_comment_edit: A photo comment has been edited ("0" — disabled, "1" — enabled).
        :param photo_comment_delete: A photo comment has been deleted ("0" — disabled, "1" — enabled).
        :param photo_comment_restore: A photo comment has been restored ("0" — disabled, "1" — enabled).
        :param video_comment_new: New comment to video notifications ("0" — disabled, "1" — enabled).
        :param video_comment_edit: A video comment has been edited ("0" — disabled, "1" — enabled).
        :param video_comment_delete: A video comment has been deleted ("0" — disabled, "1" — enabled).
        :param video_comment_restore: A video comment has been restored ("0" — disabled, "1" — enabled).
        :param market_comment_new: New comment to market item notifications ("0" — disabled, "1" — enabled).
        :param market_comment_edit: A market comment has been edited ("0" — disabled, "1" — enabled).
        :param market_comment_delete: A market comment has been deleted ("0" — disabled, "1" — enabled).
        :param market_comment_restore: A market comment has been restored ("0" — disabled, "1" — enabled).
        :param market_order_new: No description provided
        :param market_order_edit: No description provided
        :param poll_vote_new: A vote in a public poll has been added ("0" — disabled, "1" — enabled).
        :param group_join: Joined community notifications ("0" — disabled, "1" — enabled).
        :param group_leave: Left community notifications ("0" — disabled, "1" — enabled).
        :param group_change_settings: No description provided
        :param group_change_photo: No description provided
        :param group_officers_edit: No description provided
        :param user_block: User added to community blacklist
        :param user_unblock: User removed from community blacklist
        :param lead_forms_new: New form in lead forms
        :param like_add: No description provided
        :param like_remove: No description provided
        :param message_event: No description provided
        :param donut_subscription_create: No description provided
        :param donut_subscription_prolonged: No description provided
        :param donut_subscription_cancelled: No description provided
        :param donut_subscription_price_changed: No description provided
        :param donut_subscription_expired: No description provided
        :param donut_money_withdraw: No description provided
        :param donut_money_withdraw_error: No description provided
        """

    @api_method
    async def set_long_poll_settings(
        self,
        *,
        group_id: int,
        enabled: ty.Optional[bool] = None,
        api_version: ty.Optional[str] = None,
        message_new: ty.Optional[bool] = None,
        message_reply: ty.Optional[bool] = None,
        message_allow: ty.Optional[bool] = None,
        message_deny: ty.Optional[bool] = None,
        message_edit: ty.Optional[bool] = None,
        message_typing_state: ty.Optional[bool] = None,
        photo_new: ty.Optional[bool] = None,
        audio_new: ty.Optional[bool] = None,
        video_new: ty.Optional[bool] = None,
        wall_reply_new: ty.Optional[bool] = None,
        wall_reply_edit: ty.Optional[bool] = None,
        wall_reply_delete: ty.Optional[bool] = None,
        wall_reply_restore: ty.Optional[bool] = None,
        wall_post_new: ty.Optional[bool] = None,
        wall_repost: ty.Optional[bool] = None,
        board_post_new: ty.Optional[bool] = None,
        board_post_edit: ty.Optional[bool] = None,
        board_post_restore: ty.Optional[bool] = None,
        board_post_delete: ty.Optional[bool] = None,
        photo_comment_new: ty.Optional[bool] = None,
        photo_comment_edit: ty.Optional[bool] = None,
        photo_comment_delete: ty.Optional[bool] = None,
        photo_comment_restore: ty.Optional[bool] = None,
        video_comment_new: ty.Optional[bool] = None,
        video_comment_edit: ty.Optional[bool] = None,
        video_comment_delete: ty.Optional[bool] = None,
        video_comment_restore: ty.Optional[bool] = None,
        market_comment_new: ty.Optional[bool] = None,
        market_comment_edit: ty.Optional[bool] = None,
        market_comment_delete: ty.Optional[bool] = None,
        market_comment_restore: ty.Optional[bool] = None,
        poll_vote_new: ty.Optional[bool] = None,
        group_join: ty.Optional[bool] = None,
        group_leave: ty.Optional[bool] = None,
        group_change_settings: ty.Optional[bool] = None,
        group_change_photo: ty.Optional[bool] = None,
        group_officers_edit: ty.Optional[bool] = None,
        user_block: ty.Optional[bool] = None,
        user_unblock: ty.Optional[bool] = None,
        like_add: ty.Optional[bool] = None,
        like_remove: ty.Optional[bool] = None,
        message_event: ty.Optional[bool] = None,
        donut_subscription_create: ty.Optional[bool] = None,
        donut_subscription_prolonged: ty.Optional[bool] = None,
        donut_subscription_cancelled: ty.Optional[bool] = None,
        donut_subscription_price_changed: ty.Optional[bool] = None,
        donut_subscription_expired: ty.Optional[bool] = None,
        donut_money_withdraw: ty.Optional[bool] = None,
        donut_money_withdraw_error: ty.Optional[bool] = None,
        **kwargs
    ) -> 1:
        """
        Sets Long Poll notification settings

        :param group_id: Community ID.
        :param enabled: Sets whether Long Poll is enabled ("0" — disabled, "1" — enabled).
        :param api_version: No description provided
        :param message_new: A new incoming message has been received ("0" — disabled, "1" — enabled).
        :param message_reply: A new outcoming message has been received ("0" — disabled, "1" — enabled).
        :param message_allow: Allowed messages notifications ("0" — disabled, "1" — enabled).
        :param message_deny: Denied messages notifications ("0" — disabled, "1" — enabled).
        :param message_edit: A message has been edited ("0" — disabled, "1" — enabled).
        :param message_typing_state: No description provided
        :param photo_new: New photos notifications ("0" — disabled, "1" — enabled).
        :param audio_new: New audios notifications ("0" — disabled, "1" — enabled).
        :param video_new: New videos notifications ("0" — disabled, "1" — enabled).
        :param wall_reply_new: New wall replies notifications ("0" — disabled, "1" — enabled).
        :param wall_reply_edit: Wall replies edited notifications ("0" — disabled, "1" — enabled).
        :param wall_reply_delete: A wall comment has been deleted ("0" — disabled, "1" — enabled).
        :param wall_reply_restore: A wall comment has been restored ("0" — disabled, "1" — enabled).
        :param wall_post_new: New wall posts notifications ("0" — disabled, "1" — enabled).
        :param wall_repost: New wall posts notifications ("0" — disabled, "1" — enabled).
        :param board_post_new: New board posts notifications ("0" — disabled, "1" — enabled).
        :param board_post_edit: Board posts edited notifications ("0" — disabled, "1" — enabled).
        :param board_post_restore: Board posts restored notifications ("0" — disabled, "1" — enabled).
        :param board_post_delete: Board posts deleted notifications ("0" — disabled, "1" — enabled).
        :param photo_comment_new: New comment to photo notifications ("0" — disabled, "1" — enabled).
        :param photo_comment_edit: A photo comment has been edited ("0" — disabled, "1" — enabled).
        :param photo_comment_delete: A photo comment has been deleted ("0" — disabled, "1" — enabled).
        :param photo_comment_restore: A photo comment has been restored ("0" — disabled, "1" — enabled).
        :param video_comment_new: New comment to video notifications ("0" — disabled, "1" — enabled).
        :param video_comment_edit: A video comment has been edited ("0" — disabled, "1" — enabled).
        :param video_comment_delete: A video comment has been deleted ("0" — disabled, "1" — enabled).
        :param video_comment_restore: A video comment has been restored ("0" — disabled, "1" — enabled).
        :param market_comment_new: New comment to market item notifications ("0" — disabled, "1" — enabled).
        :param market_comment_edit: A market comment has been edited ("0" — disabled, "1" — enabled).
        :param market_comment_delete: A market comment has been deleted ("0" — disabled, "1" — enabled).
        :param market_comment_restore: A market comment has been restored ("0" — disabled, "1" — enabled).
        :param poll_vote_new: A vote in a public poll has been added ("0" — disabled, "1" — enabled).
        :param group_join: Joined community notifications ("0" — disabled, "1" — enabled).
        :param group_leave: Left community notifications ("0" — disabled, "1" — enabled).
        :param group_change_settings: No description provided
        :param group_change_photo: No description provided
        :param group_officers_edit: No description provided
        :param user_block: User added to community blacklist
        :param user_unblock: User removed from community blacklist
        :param like_add: No description provided
        :param like_remove: No description provided
        :param message_event: No description provided
        :param donut_subscription_create: No description provided
        :param donut_subscription_prolonged: No description provided
        :param donut_subscription_cancelled: No description provided
        :param donut_subscription_price_changed: No description provided
        :param donut_subscription_expired: No description provided
        :param donut_money_withdraw: No description provided
        :param donut_money_withdraw_error: No description provided
        """

    @api_method
    async def set_settings(
        self,
        *,
        group_id: int,
        messages: ty.Optional[bool] = None,
        bots_capabilities: ty.Optional[bool] = None,
        bots_start_button: ty.Optional[bool] = None,
        bots_add_to_chat: ty.Optional[bool] = None,
        **kwargs
    ) -> 1:
        """
        No description provided

        :param group_id: No description provided
        :param messages: No description provided
        :param bots_capabilities: No description provided
        :param bots_start_button: No description provided
        :param bots_add_to_chat: No description provided
        """

    @api_method
    async def set_user_note(
        self,
        *,
        group_id: int,
        user_id: int,
        note: ty.Optional[str] = None,
        **kwargs
    ) -> 1:
        """
        In order to save note about group participant

        :param group_id: No description provided
        :param user_id: No description provided
        :param note: Note body
        """

    @api_method
    async def tag_add(
        self,
        *,
        group_id: int,
        tag_name: str,
        tag_color: ty.Optional[str] = None,
        **kwargs
    ) -> 1:
        """
        Add new group"s tag

        :param group_id: No description provided
        :param tag_name: No description provided
        :param tag_color: No description provided
        """

    @api_method
    async def tag_bind(
        self, *, group_id: int, tag_id: int, user_id: int, act: str, **kwargs
    ) -> 1:
        """
        Bind or unbind group"s tag to user

        :param group_id: No description provided
        :param tag_id: No description provided
        :param user_id: No description provided
        :param act: Describe the action
        """

    @api_method
    async def tag_delete(self, *, group_id: int, tag_id: int, **kwargs) -> 1:
        """
        Delete group"s tag

        :param group_id: No description provided
        :param tag_id: No description provided
        """

    @api_method
    async def tag_update(
        self, *, group_id: int, tag_id: int, tag_name: str, **kwargs
    ) -> 1:
        """
        Update group"s tag

        :param group_id: No description provided
        :param tag_id: No description provided
        :param tag_name: No description provided
        """

    @api_method
    async def toggle_market(
        self, *, group_id: int, state: str, **kwargs
    ) -> 1:
        """
        No description provided

        :param group_id: No description provided
        :param state: No description provided
        """

    @api_method
    async def unban(
        self, *, group_id: int, owner_id: ty.Optional[int] = None, **kwargs
    ) -> 1:
        """
        No description provided

        :param group_id: No description provided
        :param owner_id: No description provided
        """


class Likes(APIMethod):
    @api_method
    async def add(
        self,
        *,
        type: str,
        owner_id: ty.Optional[int] = None,
        item_id: int,
        access_key: ty.Optional[str] = None,
        **kwargs
    ) -> 1:
        """
        Adds the specified object to the "Likes" list of the current user.

        :param type: Object type: "post" — post on user or community wall, "comment" — comment on a wall post, "photo" — photo, "audio" — audio, "video" — video, "note" — note, "photo_comment" — comment on the photo, "video_comment" — comment on the video, "topic_comment" — comment in the discussion, "sitepage" — page of the site where the [vk.com/dev/Like|Like widget] is installed
        :param owner_id: ID of the user or community that owns the object.
        :param item_id: Object ID.
        :param access_key: Access key required for an object owned by a private entity.
        """

    @api_method
    async def delete(
        self,
        *,
        type: str,
        owner_id: ty.Optional[int] = None,
        item_id: int,
        access_key: ty.Optional[str] = None,
        **kwargs
    ) -> 1:
        """
        Deletes the specified object from the "Likes" list of the current user.

        :param type: Object type: "post" — post on user or community wall, "comment" — comment on a wall post, "photo" — photo, "audio" — audio, "video" — video, "note" — note, "photo_comment" — comment on the photo, "video_comment" — comment on the video, "topic_comment" — comment in the discussion, "sitepage" — page of the site where the [vk.com/dev/Like|Like widget] is installed
        :param owner_id: ID of the user or community that owns the object.
        :param item_id: Object ID.
        :param access_key: Access key required for an object owned by a private entity.
        """

    @api_method
    async def get_list(
        self,
        *,
        type: str,
        owner_id: ty.Optional[int] = None,
        item_id: ty.Optional[int] = None,
        page_url: ty.Optional[str] = None,
        filter: ty.Optional[str] = None,
        friends_only: int = 0,
        extended: ty.Optional[bool] = None,
        offset: ty.Optional[int] = None,
        count: ty.Optional[int] = None,
        skip_own: ty.Optional[bool] = None,
        **kwargs
    ) -> 1:
        """
        Returns a list of IDs of users who added the specified object to their "Likes" list.

        :param type: , Object type: "post" — post on user or community wall, "comment" — comment on a wall post, "photo" — photo, "audio" — audio, "video" — video, "note" — note, "photo_comment" — comment on the photo, "video_comment" — comment on the video, "topic_comment" — comment in the discussion, "sitepage" — page of the site where the [vk.com/dev/Like|Like widget] is installed
        :param owner_id: ID of the user, community, or application that owns the object. If the "type" parameter is set as "sitepage", the application ID is passed as "owner_id". Use negative value for a community id. If the "type" parameter is not set, the "owner_id" is assumed to be either the current user or the same application ID as if the "type" parameter was set to "sitepage".
        :param item_id: Object ID. If "type" is set as "sitepage", "item_id" can include the "page_id" parameter value used during initialization of the [vk.com/dev/Like|Like widget].
        :param page_url: URL of the page where the [vk.com/dev/Like|Like widget] is installed. Used instead of the "item_id" parameter.
        :param filter: Filters to apply: "likes" — returns information about all users who liked the object (default), "copies" — returns information only about users who told their friends about the object
        :param friends_only: Specifies which users are returned: "1" — to return only the current user"s friends, "0" — to return all users (default)
        :param extended: Specifies whether extended information will be returned. "1" — to return extended information about users and communities from the "Likes" list, "0" — to return no additional information (default)
        :param offset: Offset needed to select a specific subset of users.
        :param count: Number of user IDs to return (maximum "1000"). Default is "100" if "friends_only" is set to "0", otherwise, the default is "10" if "friends_only" is set to "1".
        :param skip_own: No description provided
        """

    @api_method
    async def is_liked(
        self,
        *,
        user_id: ty.Optional[int] = None,
        type: str,
        owner_id: ty.Optional[int] = None,
        item_id: int,
        **kwargs
    ) -> 1:
        """
        Checks for the object in the "Likes" list of the specified user.

        :param user_id: User ID.
        :param type: Object type: "post" — post on user or community wall, "comment" — comment on a wall post, "photo" — photo, "audio" — audio, "video" — video, "note" — note, "photo_comment" — comment on the photo, "video_comment" — comment on the video, "topic_comment" — comment in the discussion
        :param owner_id: ID of the user or community that owns the object.
        :param item_id: Object ID.
        """


class Market(APIMethod):
    @api_method
    async def add(
        self,
        *,
        owner_id: int,
        name: str,
        description: str,
        category_id: int,
        price: ty.Optional[float] = None,
        old_price: ty.Optional[float] = None,
        deleted: ty.Optional[bool] = None,
        main_photo_id: ty.Optional[int] = None,
        photo_ids: ty.Optional[ty.Sequence] = None,
        url: ty.Optional[str] = None,
        dimension_width: ty.Optional[int] = None,
        dimension_height: ty.Optional[int] = None,
        dimension_length: ty.Optional[int] = None,
        weight: ty.Optional[int] = None,
        **kwargs
    ) -> 1:
        """
        Ads a new item to the market.

        :param owner_id: ID of an item owner community.
        :param name: Item name.
        :param description: Item description.
        :param category_id: Item category ID.
        :param price: Item price.
        :param old_price: No description provided
        :param deleted: Item status ("1" — deleted, "0" — not deleted).
        :param main_photo_id: Cover photo ID.
        :param photo_ids: IDs of additional photos.
        :param url: Url for button in market item.
        :param dimension_width: No description provided
        :param dimension_height: No description provided
        :param dimension_length: No description provided
        :param weight: No description provided
        """

    @api_method
    async def add_album(
        self,
        *,
        owner_id: int,
        title: str,
        photo_id: ty.Optional[int] = None,
        main_album: ty.Optional[bool] = None,
        **kwargs
    ) -> 1:
        """
        Creates new collection of items

        :param owner_id: ID of an item owner community.
        :param title: Collection title.
        :param photo_id: Cover photo ID.
        :param main_album: Set as main ("1" – set, "0" – no).
        """

    @api_method
    async def add_to_album(
        self, *, owner_id: int, item_id: int, album_ids: ty.Sequence, **kwargs
    ) -> 1:
        """
        Adds an item to one or multiple collections.

        :param owner_id: ID of an item owner community.
        :param item_id: Item ID.
        :param album_ids: Collections IDs to add item to.
        """

    @api_method
    async def create_comment(
        self,
        *,
        owner_id: int,
        item_id: int,
        message: ty.Optional[str] = None,
        attachments: ty.Optional[ty.List[str]] = None,
        from_group: ty.Optional[bool] = None,
        reply_to_comment: ty.Optional[int] = None,
        sticker_id: ty.Optional[int] = None,
        guid: ty.Optional[str] = None,
        **kwargs
    ) -> 1:
        """
        Creates a new comment for an item.

        :param owner_id: ID of an item owner community.
        :param item_id: Item ID.
        :param message: Comment text (required if "attachments" parameter is not specified)
        :param attachments: Comma-separated list of objects attached to a comment. The field is submitted the following way: , ""<owner_id>_<media_id>,<owner_id>_<media_id>"", , "" - media attachment type: ""photo" - photo, "video" - video, "audio" - audio, "doc" - document", , "<owner_id>" - media owner id, "<media_id>" - media attachment id, , For example: "photo100172_166443618,photo66748_265827614",
        :param from_group: "1" - comment will be published on behalf of a community, "0" - on behalf of a user (by default).
        :param reply_to_comment: ID of a comment to reply with current comment to.
        :param sticker_id: Sticker ID.
        :param guid: Random value to avoid resending one comment.
        """

    @api_method
    async def delete(self, *, owner_id: int, item_id: int, **kwargs) -> 1:
        """
        Deletes an item.

        :param owner_id: ID of an item owner community.
        :param item_id: Item ID.
        """

    @api_method
    async def delete_album(
        self, *, owner_id: int, album_id: int, **kwargs
    ) -> 1:
        """
        Deletes a collection of items.

        :param owner_id: ID of an collection owner community.
        :param album_id: Collection ID.
        """

    @api_method
    async def delete_comment(
        self, *, owner_id: int, comment_id: int, **kwargs
    ) -> 1:
        """
        Deletes an item"s comment

        :param owner_id: identifier of an item owner community, "Note that community id in the "owner_id" parameter should be negative number. For example "owner_id"=-1 matches the [vk.com/apiclub|VK API] community "
        :param comment_id: comment id
        """

    @api_method
    async def edit(
        self,
        *,
        owner_id: int,
        item_id: int,
        name: str,
        description: str,
        category_id: int,
        price: float,
        deleted: ty.Optional[bool] = None,
        main_photo_id: int,
        photo_ids: ty.Optional[ty.Sequence] = None,
        url: ty.Optional[str] = None,
        **kwargs
    ) -> 1:
        """
        Edits an item.

        :param owner_id: ID of an item owner community.
        :param item_id: Item ID.
        :param name: Item name.
        :param description: Item description.
        :param category_id: Item category ID.
        :param price: Item price.
        :param deleted: Item status ("1" — deleted, "0" — not deleted).
        :param main_photo_id: Cover photo ID.
        :param photo_ids: IDs of additional photos.
        :param url: Url for button in market item.
        """

    @api_method
    async def edit_album(
        self,
        *,
        owner_id: int,
        album_id: int,
        title: str,
        photo_id: ty.Optional[int] = None,
        main_album: ty.Optional[bool] = None,
        **kwargs
    ) -> 1:
        """
        Edits a collection of items

        :param owner_id: ID of an collection owner community.
        :param album_id: Collection ID.
        :param title: Collection title.
        :param photo_id: Cover photo id
        :param main_album: Set as main ("1" – set, "0" – no).
        """

    @api_method
    async def edit_comment(
        self,
        *,
        owner_id: int,
        comment_id: int,
        message: ty.Optional[str] = None,
        attachments: ty.Optional[ty.List[str]] = None,
        **kwargs
    ) -> 1:
        """
        Chages item comment"s text

        :param owner_id: ID of an item owner community.
        :param comment_id: Comment ID.
        :param message: New comment text (required if "attachments" are not specified), , 2048 symbols maximum.
        :param attachments: Comma-separated list of objects attached to a comment. The field is submitted the following way: , ""<owner_id>_<media_id>,<owner_id>_<media_id>"", , "" - media attachment type: ""photo" - photo, "video" - video, "audio" - audio, "doc" - document", , "<owner_id>" - media owner id, "<media_id>" - media attachment id, , For example: "photo100172_166443618,photo66748_265827614",
        """

    @api_method
    async def edit_order(
        self,
        *,
        user_id: int,
        order_id: int,
        merchant_comment: ty.Optional[str] = None,
        status: ty.Optional[int] = None,
        track_number: ty.Optional[str] = None,
        payment_status: ty.Optional[str] = None,
        delivery_price: ty.Optional[int] = None,
        width: ty.Optional[int] = None,
        length: ty.Optional[int] = None,
        height: ty.Optional[int] = None,
        weight: ty.Optional[int] = None,
        **kwargs
    ) -> 1:
        """
        Edit order

        :param user_id: No description provided
        :param order_id: No description provided
        :param merchant_comment: No description provided
        :param status: No description provided
        :param track_number: No description provided
        :param payment_status: No description provided
        :param delivery_price: No description provided
        :param width: No description provided
        :param length: No description provided
        :param height: No description provided
        :param weight: No description provided
        """

    @api_method
    async def get(
        self,
        *,
        owner_id: int,
        album_id: int = 0,
        count: int = 100,
        offset: ty.Optional[int] = None,
        extended: ty.Optional[bool] = None,
        **kwargs
    ) -> 1:
        """
        Returns items list for a community.

        :param owner_id: ID of an item owner community, "Note that community id in the "owner_id" parameter should be negative number. For example "owner_id"=-1 matches the [vk.com/apiclub|VK API] community "
        :param album_id: No description provided
        :param count: Number of items to return.
        :param offset: Offset needed to return a specific subset of results.
        :param extended: "1" – method will return additional fields: "likes, can_comment, car_repost, photos". These parameters are not returned by default.
        """

    @api_method
    async def get_album_by_id(
        self, *, owner_id: int, album_ids: ty.Sequence, **kwargs
    ) -> 1:
        """
        Returns items album"s data

        :param owner_id: identifier of an album owner community, "Note that community id in the "owner_id" parameter should be negative number. For example "owner_id"=-1 matches the [vk.com/apiclub|VK API] community "
        :param album_ids: collections identifiers to obtain data from
        """

    @api_method
    async def get_albums(
        self,
        *,
        owner_id: int,
        offset: ty.Optional[int] = None,
        count: int = 50,
        **kwargs
    ) -> 1:
        """
        Returns community"s market collections list.

        :param owner_id: ID of an items owner community.
        :param offset: Offset needed to return a specific subset of results.
        :param count: Number of items to return.
        """

    @api_method
    async def get_by_id(
        self,
        *,
        item_ids: ty.List[ty.Union[str, int]],
        extended: ty.Optional[bool] = None,
        **kwargs
    ) -> 1:
        """
        Returns information about market items by their ids.

        :param item_ids: Comma-separated ids list: {user id}_{item id}. If an item belongs to a community -{community id} is used. " "Videos" value example: , "-4363_136089719,13245770_137352259""
        :param extended: "1" – to return additional fields: "likes, can_comment, car_repost, photos". By default: "0".
        """

    @api_method
    async def get_categories(
        self, *, count: int = 10, offset: ty.Optional[int] = None, **kwargs
    ) -> 1:
        """
        Returns a list of market categories.

        :param count: Number of results to return.
        :param offset: Offset needed to return a specific subset of results.
        """

    @api_method
    async def get_comments(
        self,
        *,
        owner_id: int,
        item_id: int,
        need_likes: ty.Optional[bool] = None,
        start_comment_id: ty.Optional[int] = None,
        offset: int = 0,
        count: int = 20,
        sort: str = "asc",
        extended: ty.Optional[bool] = None,
        fields: ty.Optional[ty.Sequence] = None,
        **kwargs
    ) -> 1:
        """
        Returns comments list for an item.

        :param owner_id: ID of an item owner community
        :param item_id: Item ID.
        :param need_likes: "1" — to return likes info.
        :param start_comment_id: ID of a comment to start a list from (details below).
        :param offset: No description provided
        :param count: Number of results to return.
        :param sort: Sort order ("asc" — from old to new, "desc" — from new to old)
        :param extended: "1" — comments will be returned as numbered objects, in addition lists of "profiles" and "groups" objects will be returned.
        :param fields: List of additional profile fields to return. See the [vk.com/dev/fields|details]
        """

    @api_method
    async def get_group_orders(
        self, *, group_id: int, offset: int = 0, count: int = 10, **kwargs
    ) -> 1:
        """
        Get market orders

        :param group_id: No description provided
        :param offset: No description provided
        :param count: No description provided
        """

    @api_method
    async def get_order_by_id(
        self,
        *,
        user_id: ty.Optional[int] = None,
        order_id: int,
        extended: ty.Optional[bool] = None,
        **kwargs
    ) -> 1:
        """
        Get order

        :param user_id: No description provided
        :param order_id: No description provided
        :param extended: No description provided
        """

    @api_method
    async def get_order_items(
        self,
        *,
        order_id: int,
        offset: ty.Optional[int] = None,
        count: int = 50,
        **kwargs
    ) -> 1:
        """
        Get market items in the order

        :param order_id: No description provided
        :param offset: No description provided
        :param count: No description provided
        """

    @api_method
    async def get_orders(
        self,
        *,
        offset: int = 0,
        count: int = 10,
        extended: ty.Optional[bool] = None,
        **kwargs
    ) -> 1:
        """
        No description provided

        :param offset: No description provided
        :param count: No description provided
        :param extended: No description provided
        """

    @api_method
    async def remove_from_album(
        self, *, owner_id: int, item_id: int, album_ids: ty.Sequence, **kwargs
    ) -> 1:
        """
        Removes an item from one or multiple collections.

        :param owner_id: ID of an item owner community.
        :param item_id: Item ID.
        :param album_ids: Collections IDs to remove item from.
        """

    @api_method
    async def reorder_albums(
        self,
        *,
        owner_id: int,
        album_id: int,
        before: ty.Optional[int] = None,
        after: ty.Optional[int] = None,
        **kwargs
    ) -> 1:
        """
        Reorders the collections list.

        :param owner_id: ID of an item owner community.
        :param album_id: Collection ID.
        :param before: ID of a collection to place current collection before it.
        :param after: ID of a collection to place current collection after it.
        """

    @api_method
    async def reorder_items(
        self,
        *,
        owner_id: int,
        album_id: ty.Optional[int] = None,
        item_id: int,
        before: ty.Optional[int] = None,
        after: ty.Optional[int] = None,
        **kwargs
    ) -> 1:
        """
        Changes item place in a collection.

        :param owner_id: ID of an item owner community.
        :param album_id: ID of a collection to reorder items in. Set 0 to reorder full items list.
        :param item_id: Item ID.
        :param before: ID of an item to place current item before it.
        :param after: ID of an item to place current item after it.
        """

    @api_method
    async def report(
        self, *, owner_id: int, item_id: int, reason: int = 0, **kwargs
    ) -> 1:
        """
        Sends a complaint to the item.

        :param owner_id: ID of an item owner community.
        :param item_id: Item ID.
        :param reason: Complaint reason. Possible values: *"0" — spam,, *"1" — child porn,, *"2" — extremism,, *"3" — violence,, *"4" — drugs propaganda,, *"5" — adult materials,, *"6" — insult.
        """

    @api_method
    async def report_comment(
        self, *, owner_id: int, comment_id: int, reason: int, **kwargs
    ) -> 1:
        """
        Sends a complaint to the item"s comment.

        :param owner_id: ID of an item owner community.
        :param comment_id: Comment ID.
        :param reason: Complaint reason. Possible values: *"0" — spam,, *"1" — child porn,, *"2" — extremism,, *"3" — violence,, *"4" — drugs propaganda,, *"5" — adult materials,, *"6" — insult.
        """

    @api_method
    async def restore(self, *, owner_id: int, item_id: int, **kwargs) -> 1:
        """
        Restores recently deleted item

        :param owner_id: ID of an item owner community.
        :param item_id: Deleted item ID.
        """

    @api_method
    async def restore_comment(
        self, *, owner_id: int, comment_id: int, **kwargs
    ) -> 1:
        """
        Restores a recently deleted comment

        :param owner_id: identifier of an item owner community, "Note that community id in the "owner_id" parameter should be negative number. For example "owner_id"=-1 matches the [vk.com/apiclub|VK API] community "
        :param comment_id: deleted comment id
        """

    @api_method
    async def search(
        self,
        *,
        owner_id: int,
        album_id: ty.Optional[int] = None,
        q: ty.Optional[str] = None,
        price_from: ty.Optional[int] = None,
        price_to: ty.Optional[int] = None,
        sort: int = 0,
        rev: int = 1,
        offset: ty.Optional[int] = None,
        count: int = 20,
        extended: bool = "0",
        status: int = 0,
        **kwargs
    ) -> 1:
        """
        Searches market items in a community"s catalog

        :param owner_id: ID of an items owner community.
        :param album_id: No description provided
        :param q: Search query, for example "pink slippers".
        :param price_from: Minimum item price value.
        :param price_to: Maximum item price value.
        :param sort: No description provided
        :param rev: "0" — do not use reverse order, "1" — use reverse order
        :param offset: Offset needed to return a specific subset of results.
        :param count: Number of items to return.
        :param extended: "1" – to return additional fields: "likes, can_comment, car_repost, photos". By default: "0".
        :param status: No description provided
        """


class Messages(APIMethod):
    @api_method
    async def add_chat_user(
        self,
        *,
        chat_id: int,
        user_id: ty.Optional[int] = None,
        visible_messages_count: ty.Optional[int] = None,
        **kwargs
    ) -> 1:
        """
        Adds a new user to a chat.

        :param chat_id: Chat ID.
        :param user_id: ID of the user to be added to the chat.
        :param visible_messages_count: No description provided
        """

    @api_method
    async def allow_messages_from_group(
        self, *, group_id: int, key: ty.Optional[str] = None, **kwargs
    ) -> 1:
        """
        Allows sending messages from community to the current user.

        :param group_id: Group ID.
        :param key: No description provided
        """

    @api_method
    async def create_chat(
        self,
        *,
        user_ids: ty.Optional[ty.Sequence] = None,
        title: ty.Optional[str] = None,
        group_id: ty.Optional[int] = None,
        **kwargs
    ) -> 1:
        """
        Creates a chat with several participants.

        :param user_ids: IDs of the users to be added to the chat.
        :param title: Chat title.
        :param group_id: No description provided
        """

    @api_method
    async def delete(
        self,
        *,
        message_ids: ty.Optional[ty.Sequence] = None,
        spam: ty.Optional[bool] = None,
        group_id: ty.Optional[int] = None,
        delete_for_all: bool = False,
        **kwargs
    ) -> 1:
        """
        Deletes one or more messages.

        :param message_ids: Message IDs.
        :param spam: "1" — to mark message as spam.
        :param group_id: Group ID (for group messages with user access token)
        :param delete_for_all: "1" — delete message for for all.
        """

    @api_method
    async def delete_chat_photo(
        self, *, chat_id: int, group_id: ty.Optional[int] = None, **kwargs
    ) -> 1:
        """
        Deletes a chat"s cover picture.

        :param chat_id: Chat ID.
        :param group_id: No description provided
        """

    @api_method
    async def delete_conversation(
        self,
        *,
        user_id: ty.Optional[int] = None,
        peer_id: ty.Optional[int] = None,
        group_id: ty.Optional[int] = None,
        **kwargs
    ) -> 1:
        """
        Deletes all private messages in a conversation.

        :param user_id: User ID. To clear a chat history use "chat_id"
        :param peer_id: Destination ID. "For user: "User ID", e.g. "12345". For chat: "2000000000" + "chat_id", e.g. "2000000001". For community: "- community ID", e.g. "-12345". "
        :param group_id: Group ID (for group messages with user access token)
        """

    @api_method
    async def deny_messages_from_group(self, *, group_id: int, **kwargs) -> 1:
        """
        Denies sending message from community to the current user.

        :param group_id: Group ID.
        """

    @api_method
    async def edit(
        self,
        *,
        peer_id: int,
        message: ty.Optional[str] = None,
        lat: ty.Optional[float] = None,
        long: ty.Optional[float] = None,
        attachment: ty.Optional[str] = None,
        keep_forward_messages: ty.Optional[bool] = None,
        keep_snippets: ty.Optional[bool] = None,
        group_id: ty.Optional[int] = None,
        dont_parse_links: bool = False,
        message_id: ty.Optional[int] = None,
        conversation_message_id: ty.Optional[int] = None,
        template: ty.Optional[str] = None,
        keyboard: ty.Optional[str] = None,
        **kwargs
    ) -> 1:
        """
        Edits the message.

        :param peer_id: Destination ID. "For user: "User ID", e.g. "12345". For chat: "2000000000" + "chat_id", e.g. "2000000001". For community: "- community ID", e.g. "-12345". "
        :param message: (Required if "attachments" is not set.) Text of the message.
        :param lat: Geographical latitude of a check-in, in degrees (from -90 to 90).
        :param long: Geographical longitude of a check-in, in degrees (from -180 to 180).
        :param attachment: (Required if "message" is not set.) List of objects attached to the message, separated by commas, in the following format: "<owner_id>_<media_id>", "" — Type of media attachment: "photo" — photo, "video" — video, "audio" — audio, "doc" — document, "wall" — wall post, "<owner_id>" — ID of the media attachment owner. "<media_id>" — media attachment ID. Example: "photo100172_166443618"
        :param keep_forward_messages: "1" — to keep forwarded, messages.
        :param keep_snippets: "1" — to keep attached snippets.
        :param group_id: Group ID (for group messages with user access token)
        :param dont_parse_links: No description provided
        :param message_id: No description provided
        :param conversation_message_id: No description provided
        :param template: No description provided
        :param keyboard: No description provided
        """

    @api_method
    async def edit_chat(
        self, *, chat_id: int, title: ty.Optional[str] = None, **kwargs
    ) -> 1:
        """
        Edits the title of a chat.

        :param chat_id: Chat ID.
        :param title: New title of the chat.
        """

    @api_method
    async def get_by_conversation_message_id(
        self,
        *,
        peer_id: int,
        conversation_message_ids: ty.Sequence,
        extended: ty.Optional[bool] = None,
        fields: ty.Optional[ty.Sequence] = None,
        group_id: ty.Optional[int] = None,
        **kwargs
    ) -> 1:
        """
        Returns messages by their IDs within the conversation.

        :param peer_id: Destination ID. "For user: "User ID", e.g. "12345". For chat: "2000000000" + "chat_id", e.g. "2000000001". For community: "- community ID", e.g. "-12345". "
        :param conversation_message_ids: Conversation message IDs.
        :param extended: Information whether the response should be extended
        :param fields: Profile fields to return.
        :param group_id: Group ID (for group messages with group access token)
        """

    @api_method
    async def get_by_id(
        self,
        *,
        message_ids: ty.Sequence,
        preview_length: int = 0,
        extended: ty.Optional[bool] = None,
        fields: ty.Optional[ty.Sequence] = None,
        group_id: ty.Optional[int] = None,
        **kwargs
    ) -> 1:
        """
        Returns messages by their IDs.

        :param message_ids: Message IDs.
        :param preview_length: Number of characters after which to truncate a previewed message. To preview the full message, specify "0". "NOTE: Messages are not truncated by default. Messages are truncated by words."
        :param extended: Information whether the response should be extended
        :param fields: Profile fields to return.
        :param group_id: Group ID (for group messages with group access token)
        """

    @api_method
    async def get_chat_preview(
        self,
        *,
        peer_id: ty.Optional[int] = None,
        link: ty.Optional[str] = None,
        fields: ty.Optional[ty.Sequence] = None,
        **kwargs
    ) -> 1:
        """
        No description provided

        :param peer_id: No description provided
        :param link: Invitation link.
        :param fields: Profile fields to return.
        """

    @api_method
    async def get_conversation_members(
        self,
        *,
        peer_id: int,
        fields: ty.Optional[ty.Sequence] = None,
        group_id: ty.Optional[int] = None,
        **kwargs
    ) -> 1:
        """
        Returns a list of IDs of users participating in a chat.

        :param peer_id: Peer ID.
        :param fields: Profile fields to return.
        :param group_id: Group ID (for group messages with group access token)
        """

    @api_method
    async def get_conversations(
        self,
        *,
        offset: int = 0,
        count: int = 20,
        filter: str = "all",
        extended: ty.Optional[bool] = None,
        start_message_id: ty.Optional[int] = None,
        fields: ty.Optional[ty.Sequence] = None,
        group_id: ty.Optional[int] = None,
        **kwargs
    ) -> 1:
        """
        Returns a list of the current user"s conversations.

        :param offset: Offset needed to return a specific subset of conversations.
        :param count: Number of conversations to return.
        :param filter: Filter to apply: "all" — all conversations, "unread" — conversations with unread messages, "important" — conversations, marked as important (only for community messages), "unanswered" — conversations, marked as unanswered (only for community messages)
        :param extended: "1" — return extra information about users and communities
        :param start_message_id: ID of the message from what to return dialogs.
        :param fields: Profile and communities fields to return.
        :param group_id: Group ID (for group messages with group access token)
        """

    @api_method
    async def get_conversations_by_id(
        self,
        *,
        peer_ids: ty.Sequence,
        extended: ty.Optional[bool] = None,
        fields: ty.Optional[ty.Sequence] = None,
        group_id: ty.Optional[int] = None,
        **kwargs
    ) -> 1:
        """
        Returns conversations by their IDs

        :param peer_ids: Destination IDs. "For user: "User ID", e.g. "12345". For chat: "2000000000" + "chat_id", e.g. "2000000001". For community: "- community ID", e.g. "-12345". "
        :param extended: Return extended properties
        :param fields: Profile and communities fields to return.
        :param group_id: Group ID (for group messages with group access token)
        """

    @api_method
    async def get_history(
        self,
        *,
        offset: ty.Optional[int] = None,
        count: int = 20,
        user_id: ty.Optional[int] = None,
        peer_id: ty.Optional[int] = None,
        start_message_id: ty.Optional[int] = None,
        rev: ty.Optional[int] = None,
        extended: ty.Optional[bool] = None,
        fields: ty.Optional[ty.Sequence] = None,
        group_id: ty.Optional[int] = None,
        **kwargs
    ) -> 1:
        """
        Returns message history for the specified user or group chat.

        :param offset: Offset needed to return a specific subset of messages.
        :param count: Number of messages to return.
        :param user_id: ID of the user whose message history you want to return.
        :param peer_id: No description provided
        :param start_message_id: Starting message ID from which to return history.
        :param rev: Sort order: "1" — return messages in chronological order. "0" — return messages in reverse chronological order.
        :param extended: Information whether the response should be extended
        :param fields: Profile fields to return.
        :param group_id: Group ID (for group messages with group access token)
        """

    @api_method
    async def get_history_attachments(
        self,
        *,
        peer_id: int,
        media_type: str = "photo",
        start_from: ty.Optional[str] = None,
        count: int = 30,
        photo_sizes: ty.Optional[bool] = None,
        fields: ty.Optional[ty.Sequence] = None,
        group_id: ty.Optional[int] = None,
        preserve_order: ty.Optional[bool] = None,
        max_forwards_level: int = 45,
        **kwargs
    ) -> 1:
        """
        Returns media files from the dialog or group chat.

        :param peer_id: Peer ID. ", For group chat: "2000000000 + chat ID" , , For community: "-community ID""
        :param media_type: Type of media files to return: *"photo",, *"video",, *"audio",, *"doc",, *"link".,*"market".,*"wall".,*"share"
        :param start_from: Message ID to start return results from.
        :param count: Number of objects to return.
        :param photo_sizes: "1" — to return photo sizes in a
        :param fields: Additional profile [vk.com/dev/fields|fields] to return.
        :param group_id: Group ID (for group messages with group access token)
        :param preserve_order: No description provided
        :param max_forwards_level: No description provided
        """

    @api_method
    async def get_important_messages(
        self,
        *,
        count: int = 20,
        offset: ty.Optional[int] = None,
        start_message_id: ty.Optional[int] = None,
        preview_length: ty.Optional[int] = None,
        fields: ty.Optional[ty.Sequence] = None,
        extended: ty.Optional[bool] = None,
        group_id: ty.Optional[int] = None,
        **kwargs
    ) -> 1:
        """
        Returns a list of user"s important messages.

        :param count: Amount of needed important messages.
        :param offset: No description provided
        :param start_message_id: No description provided
        :param preview_length: Maximum length of messages body.
        :param fields: Actors fields to return.
        :param extended: Return extended properties
        :param group_id: Group ID (for group messages with group access token)
        """

    @api_method
    async def get_intent_users(
        self,
        *,
        intent: str,
        subscribe_id: ty.Optional[int] = None,
        offset: int = 0,
        count: int = 20,
        extended: ty.Optional[bool] = None,
        name_case: ty.Optional[ty.List[str]] = None,
        fields: ty.Optional[ty.List[str]] = None,
        **kwargs
    ) -> 1:
        """
        No description provided

        :param intent: No description provided
        :param subscribe_id: No description provided
        :param offset: No description provided
        :param count: No description provided
        :param extended: No description provided
        :param name_case: No description provided
        :param fields: No description provided
        """

    @api_method
    async def get_invite_link(
        self,
        *,
        peer_id: int,
        reset: bool = False,
        group_id: ty.Optional[int] = None,
        **kwargs
    ) -> 1:
        """
        No description provided

        :param peer_id: Destination ID.
        :param reset: 1 — to generate new link (revoke previous), 0 — to return previous link.
        :param group_id: Group ID
        """

    @api_method
    async def get_last_activity(self, *, user_id: int, **kwargs) -> 1:
        """
        Returns a user"s current status and date of last activity.

        :param user_id: User ID.
        """

    @api_method
    async def get_long_poll_history(
        self,
        *,
        ts: ty.Optional[int] = None,
        pts: ty.Optional[int] = None,
        preview_length: ty.Optional[int] = None,
        onlines: ty.Optional[bool] = None,
        fields: ty.Sequence = (),
        events_limit: int = 1000,
        msgs_limit: int = 200,
        max_msg_id: ty.Optional[int] = None,
        group_id: ty.Optional[int] = None,
        lp_version: ty.Optional[int] = None,
        last_n: int = 0,
        credentials: ty.Optional[bool] = None,
        **kwargs
    ) -> 1:
        """
        Returns updates in user"s private messages.

        :param ts: Last value of the "ts" parameter returned from the Long Poll server or by using [vk.com/dev/messages.getLongPollHistory|messages.getLongPollHistory] method.
        :param pts: Lsat value of "pts" parameter returned from the Long Poll server or by using [vk.com/dev/messages.getLongPollHistory|messages.getLongPollHistory] method.
        :param preview_length: Number of characters after which to truncate a previewed message. To preview the full message, specify "0". "NOTE: Messages are not truncated by default. Messages are truncated by words."
        :param onlines: "1" — to return history with online users only.
        :param fields: Additional profile [vk.com/dev/fields|fields] to return.
        :param events_limit: Maximum number of events to return.
        :param msgs_limit: Maximum number of messages to return.
        :param max_msg_id: Maximum ID of the message among existing ones in the local copy. Both messages received with API methods (for example, , ), and data received from a Long Poll server (events with code 4) are taken into account.
        :param group_id: Group ID (for group messages with user access token)
        :param lp_version: No description provided
        :param last_n: No description provided
        :param credentials: No description provided
        """

    @api_method
    async def get_long_poll_server(
        self,
        *,
        need_pts: ty.Optional[bool] = None,
        group_id: ty.Optional[int] = None,
        lp_version: int = 0,
        **kwargs
    ) -> 1:
        """
        Returns data required for connection to a Long Poll server.

        :param need_pts: "1" — to return the "pts" field, needed for the [vk.com/dev/messages.getLongPollHistory|messages.getLongPollHistory] method.
        :param group_id: Group ID (for group messages with user access token)
        :param lp_version: Long poll version
        """

    @api_method
    async def is_messages_from_group_allowed(
        self, *, group_id: int, user_id: int, **kwargs
    ) -> 1:
        """
        Returns information whether sending messages from the community to current user is allowed.

        :param group_id: Group ID.
        :param user_id: User ID.
        """

    @api_method
    async def join_chat_by_invite_link(self, *, link: str, **kwargs) -> 1:
        """
        No description provided

        :param link: Invitation link.
        """

    @api_method
    async def mark_as_answered_conversation(
        self,
        *,
        peer_id: int,
        answered: bool = 1,
        group_id: ty.Optional[int] = None,
        **kwargs
    ) -> 1:
        """
        Marks and unmarks conversations as unanswered.

        :param peer_id: ID of conversation to mark as important.
        :param answered: "1" — to mark as answered, "0" — to remove the mark
        :param group_id: Group ID (for group messages with group access token)
        """

    @api_method
    async def mark_as_important(
        self,
        *,
        message_ids: ty.Sequence = (),
        important: ty.Optional[int] = None,
        **kwargs
    ) -> 1:
        """
        Marks and unmarks messages as important (starred).

        :param message_ids: IDs of messages to mark as important.
        :param important: "1" — to add a star (mark as important), "0" — to remove the star
        """

    @api_method
    async def mark_as_important_conversation(
        self,
        *,
        peer_id: int,
        important: bool = 1,
        group_id: ty.Optional[int] = None,
        **kwargs
    ) -> 1:
        """
        Marks and unmarks conversations as important.

        :param peer_id: ID of conversation to mark as important.
        :param important: "1" — to add a star (mark as important), "0" — to remove the star
        :param group_id: Group ID (for group messages with group access token)
        """

    @api_method
    async def mark_as_read(
        self,
        *,
        message_ids: ty.Sequence = (),
        peer_id: ty.Optional[int] = None,
        start_message_id: ty.Optional[int] = None,
        group_id: ty.Optional[int] = None,
        mark_conversation_as_read: ty.Optional[bool] = None,
        **kwargs
    ) -> 1:
        """
        Marks messages as read.

        :param message_ids: IDs of messages to mark as read.
        :param peer_id: Destination ID. "For user: "User ID", e.g. "12345". For chat: "2000000000" + "chat_id", e.g. "2000000001". For community: "- community ID", e.g. "-12345". "
        :param start_message_id: Message ID to start from.
        :param group_id: Group ID (for group messages with user access token)
        :param mark_conversation_as_read: No description provided
        """

    @api_method
    async def pin(
        self,
        *,
        peer_id: int,
        message_id: ty.Optional[int] = None,
        conversation_message_id: ty.Optional[int] = None,
        **kwargs
    ) -> 1:
        """
        Pin a message.

        :param peer_id: Destination ID. "For user: "User ID", e.g. "12345". For chat: "2000000000" + "Chat ID", e.g. "2000000001". For community: "- Community ID", e.g. "-12345". "
        :param message_id: Message ID
        :param conversation_message_id: Conversation message ID
        """

    @api_method
    async def remove_chat_user(
        self,
        *,
        chat_id: int,
        user_id: ty.Optional[int] = None,
        member_id: ty.Optional[int] = None,
        **kwargs
    ) -> 1:
        """
        Allows the current user to leave a chat or, if the current user started the chat, allows the user to remove another user from the chat.

        :param chat_id: Chat ID.
        :param user_id: ID of the user to be removed from the chat.
        :param member_id: No description provided
        """

    @api_method
    async def restore(
        self, *, message_id: int, group_id: ty.Optional[int] = None, **kwargs
    ) -> 1:
        """
        Restores a deleted message.

        :param message_id: ID of a previously-deleted message to restore.
        :param group_id: Group ID (for group messages with user access token)
        """

    @api_method
    async def search(
        self,
        *,
        q: ty.Optional[str] = None,
        peer_id: ty.Optional[int] = None,
        date: ty.Optional[int] = None,
        preview_length: int = 0,
        offset: int = 0,
        count: int = 20,
        extended: ty.Optional[bool] = None,
        fields: ty.Optional[ty.List[str]] = None,
        group_id: ty.Optional[int] = None,
        **kwargs
    ) -> 1:
        """
        Returns a list of the current user"s private messages that match search criteria.

        :param q: Search query string.
        :param peer_id: Destination ID. "For user: "User ID", e.g. "12345". For chat: "2000000000" + "chat_id", e.g. "2000000001". For community: "- community ID", e.g. "-12345". "
        :param date: Date to search message before in Unixtime.
        :param preview_length: Number of characters after which to truncate a previewed message. To preview the full message, specify "0". "NOTE: Messages are not truncated by default. Messages are truncated by words."
        :param offset: Offset needed to return a specific subset of messages.
        :param count: Number of messages to return.
        :param extended: No description provided
        :param fields: No description provided
        :param group_id: Group ID (for group messages with group access token)
        """

    @api_method
    async def search_conversations(
        self,
        *,
        q: ty.Optional[str] = None,
        count: int = 20,
        extended: ty.Optional[bool] = None,
        fields: ty.Optional[ty.Sequence] = None,
        group_id: ty.Optional[int] = None,
        **kwargs
    ) -> 1:
        """
        Returns a list of the current user"s conversations that match search criteria.

        :param q: Search query string.
        :param count: Maximum number of results.
        :param extended: "1" — return extra information about users and communities
        :param fields: Profile fields to return.
        :param group_id: Group ID (for group messages with user access token)
        """

    @api_method
    async def send(
        self,
        *,
        user_id: ty.Optional[int] = None,
        random_id: ty.Optional[int] = None,
        peer_id: ty.Optional[int] = None,
        peer_ids: ty.Optional[ty.Sequence] = None,
        domain: ty.Optional[str] = None,
        chat_id: ty.Optional[int] = None,
        user_ids: ty.Optional[ty.Sequence] = None,
        message: ty.Optional[str] = None,
        lat: ty.Optional[float] = None,
        long: ty.Optional[float] = None,
        attachment: ty.Optional[str] = None,
        reply_to: ty.Optional[int] = None,
        forward_messages: ty.Optional[ty.Sequence] = None,
        forward: ty.Optional[str] = None,
        sticker_id: ty.Optional[int] = None,
        group_id: ty.Optional[int] = None,
        keyboard: ty.Optional[str] = None,
        template: ty.Optional[str] = None,
        payload: ty.Optional[str] = None,
        content_source: ty.Optional[str] = None,
        dont_parse_links: bool = False,
        disable_mentions: bool = False,
        intent: str = "default",
        subscribe_id: ty.Optional[int] = None,
        **kwargs
    ) -> 1:
        """
        Sends a message.

        :param user_id: User ID (by default — current user).
        :param random_id: Unique identifier to avoid resending the message.
        :param peer_id: Destination ID. "For user: "User ID", e.g. "12345". For chat: "2000000000" + "chat_id", e.g. "2000000001". For community: "- community ID", e.g. "-12345". "
        :param peer_ids: IDs of message recipients. (See peer_id)
        :param domain: User"s short address (for example, "illarionov").
        :param chat_id: ID of conversation the message will relate to.
        :param user_ids: IDs of message recipients (if new conversation shall be started).
        :param message: (Required if "attachments" is not set.) Text of the message.
        :param lat: Geographical latitude of a check-in, in degrees (from -90 to 90).
        :param long: Geographical longitude of a check-in, in degrees (from -180 to 180).
        :param attachment: (Required if "message" is not set.) List of objects attached to the message, separated by commas, in the following format: "<owner_id>_<media_id>", "" — Type of media attachment: "photo" — photo, "video" — video, "audio" — audio, "doc" — document, "wall" — wall post, "<owner_id>" — ID of the media attachment owner. "<media_id>" — media attachment ID. Example: "photo100172_166443618"
        :param reply_to: No description provided
        :param forward_messages: ID of forwarded messages, separated with a comma. Listed messages of the sender will be shown in the message body at the recipient"s. Example: "123,431,544"
        :param forward: JSON describing the forwarded message or reply
        :param sticker_id: Sticker id.
        :param group_id: Group ID (for group messages with group access token)
        :param keyboard: No description provided
        :param template: No description provided
        :param payload: No description provided
        :param content_source: JSON describing the content source in the message
        :param dont_parse_links: No description provided
        :param disable_mentions: No description provided
        :param intent: No description provided
        :param subscribe_id: No description provided
        """

    @api_method
    async def send_message_event_answer(
        self,
        *,
        event_id: str,
        user_id: int,
        peer_id: int,
        event_data: ty.Optional[str] = None,
        **kwargs
    ) -> 1:
        """
        No description provided

        :param event_id: No description provided
        :param user_id: No description provided
        :param peer_id: No description provided
        :param event_data: No description provided
        """

    @api_method
    async def set_activity(
        self,
        *,
        user_id: ty.Optional[int] = None,
        type: ty.Optional[str] = None,
        peer_id: ty.Optional[int] = None,
        group_id: ty.Optional[int] = None,
        **kwargs
    ) -> 1:
        """
        Changes the status of a user as typing in a conversation.

        :param user_id: User ID.
        :param type: "typing" — user has started to type.
        :param peer_id: Destination ID. "For user: "User ID", e.g. "12345". For chat: "2000000000" + "chat_id", e.g. "2000000001". For community: "- community ID", e.g. "-12345". "
        :param group_id: Group ID (for group messages with group access token)
        """

    @api_method
    async def set_chat_photo(self, *, file: str, **kwargs) -> 1:
        """
        Sets a previously-uploaded picture as the cover picture of a chat.

        :param file: Upload URL from the "response" field returned by the [vk.com/dev/photos.getChatUploadServer|photos.getChatUploadServer] method upon successfully uploading an image.
        """

    @api_method
    async def unpin(
        self, *, peer_id: int, group_id: ty.Optional[int] = None, **kwargs
    ) -> 1:
        """
        No description provided

        :param peer_id: No description provided
        :param group_id: No description provided
        """


class Newsfeed(APIMethod):
    @api_method
    async def add_ban(
        self,
        *,
        user_ids: ty.Optional[ty.Sequence] = None,
        group_ids: ty.Optional[ty.Sequence] = None,
        **kwargs
    ) -> 1:
        """
        Prevents news from specified users and communities from appearing in the current user"s newsfeed.

        :param user_ids: No description provided
        :param group_ids: No description provided
        """

    @api_method
    async def delete_ban(
        self,
        *,
        user_ids: ty.Optional[ty.Sequence] = None,
        group_ids: ty.Optional[ty.Sequence] = None,
        **kwargs
    ) -> 1:
        """
        Allows news from previously banned users and communities to be shown in the current user"s newsfeed.

        :param user_ids: No description provided
        :param group_ids: No description provided
        """

    @api_method
    async def delete_list(self, *, list_id: int, **kwargs) -> 1:
        """
        No description provided

        :param list_id: No description provided
        """

    @api_method
    async def get(
        self,
        *,
        filters: ty.Optional[ty.Sequence] = None,
        return_banned: ty.Optional[bool] = None,
        start_time: ty.Optional[int] = None,
        end_time: ty.Optional[int] = None,
        max_photos: ty.Optional[int] = None,
        source_ids: ty.Optional[str] = None,
        start_from: ty.Optional[str] = None,
        count: ty.Optional[int] = None,
        fields: ty.Optional[ty.Sequence] = None,
        section: ty.Optional[str] = None,
        **kwargs
    ) -> 1:
        """
        Returns data required to show newsfeed for the current user.

        :param filters: Filters to apply: "post" — new wall posts, "photo" — new photos, "photo_tag" — new photo tags, "wall_photo" — new wall photos, "friend" — new friends
        :param return_banned: "1" — to return news items from banned sources
        :param start_time: Earliest timestamp (in Unix time) of a news item to return. By default, 24 hours ago.
        :param end_time: Latest timestamp (in Unix time) of a news item to return. By default, the current time.
        :param max_photos: Maximum number of photos to return. By default, "5".
        :param source_ids: Sources to obtain news from, separated by commas. User IDs can be specified in formats "" or "u" , where "" is the user"s friend ID. Community IDs can be specified in formats "-" or "g" , where "" is the community ID. If the parameter is not set, all of the user"s friends and communities are returned, except for banned sources, which can be obtained with the [vk.com/dev/newsfeed.getBanned|newsfeed.getBanned] method.
        :param start_from: identifier required to get the next page of results. Value for this parameter is returned in "next_from" field in a reply.
        :param count: Number of news items to return (default 50, maximum 100). For auto feed, you can use the "new_offset" parameter returned by this method.
        :param fields: Additional fields of [vk.com/dev/fields|profiles] and [vk.com/dev/fields_groups|communities] to return.
        :param section: No description provided
        """

    @api_method
    async def get_banned(
        self,
        *,
        extended: ty.Optional[bool] = None,
        fields: ty.Optional[ty.Sequence] = None,
        name_case: ty.Optional[str] = None,
        **kwargs
    ) -> 1:
        """
        Returns a list of users and communities banned from the current user"s newsfeed.

        :param extended: "1" — return extra information about users and communities
        :param fields: Profile fields to return.
        :param name_case: Case for declension of user name and surname: "nom" — nominative (default), "gen" — genitive , "dat" — dative, "acc" — accusative , "ins" — instrumental , "abl" — prepositional
        """

    @api_method
    async def get_comments(
        self,
        *,
        count: int = 30,
        filters: ty.Optional[ty.Sequence] = None,
        reposts: ty.Optional[str] = None,
        start_time: ty.Optional[int] = None,
        end_time: ty.Optional[int] = None,
        last_comments_count: int = 0,
        start_from: ty.Optional[str] = None,
        fields: ty.Optional[ty.Sequence] = None,
        **kwargs
    ) -> 1:
        """
        Returns a list of comments in the current user"s newsfeed.

        :param count: Number of comments to return. For auto feed, you can use the "new_offset" parameter returned by this method.
        :param filters: Filters to apply: "post" — new comments on wall posts, "photo" — new comments on photos, "video" — new comments on videos, "topic" — new comments on discussions, "note" — new comments on notes,
        :param reposts: Object ID, comments on repost of which shall be returned, e.g. "wall1_45486". (If the parameter is set, the "filters" parameter is optional.),
        :param start_time: Earliest timestamp (in Unix time) of a comment to return. By default, 24 hours ago.
        :param end_time: Latest timestamp (in Unix time) of a comment to return. By default, the current time.
        :param last_comments_count: No description provided
        :param start_from: Identificator needed to return the next page with results. Value for this parameter returns in "next_from" field.
        :param fields: Additional fields of [vk.com/dev/fields|profiles] and [vk.com/dev/fields_groups|communities] to return.
        """

    @api_method
    async def get_lists(
        self,
        *,
        list_ids: ty.Optional[ty.Sequence] = None,
        extended: bool = 0,
        **kwargs
    ) -> 1:
        """
        Returns a list of newsfeeds followed by the current user.

        :param list_ids: numeric list identifiers.
        :param extended: Return additional list info
        """

    @api_method
    async def get_mentions(
        self,
        *,
        owner_id: ty.Optional[int] = None,
        start_time: ty.Optional[int] = None,
        end_time: ty.Optional[int] = None,
        offset: ty.Optional[int] = None,
        count: int = 20,
        **kwargs
    ) -> 1:
        """
        Returns a list of posts on user walls in which the current user is mentioned.

        :param owner_id: Owner ID.
        :param start_time: Earliest timestamp (in Unix time) of a post to return. By default, 24 hours ago.
        :param end_time: Latest timestamp (in Unix time) of a post to return. By default, the current time.
        :param offset: Offset needed to return a specific subset of posts.
        :param count: Number of posts to return.
        """

    @api_method
    async def get_recommended(
        self,
        *,
        start_time: ty.Optional[int] = None,
        end_time: ty.Optional[int] = None,
        max_photos: ty.Optional[int] = None,
        start_from: ty.Optional[str] = None,
        count: ty.Optional[int] = None,
        fields: ty.Optional[ty.Sequence] = None,
        **kwargs
    ) -> 1:
        """
        , Returns a list of newsfeeds recommended to the current user.

        :param start_time: Earliest timestamp (in Unix time) of a news item to return. By default, 24 hours ago.
        :param end_time: Latest timestamp (in Unix time) of a news item to return. By default, the current time.
        :param max_photos: Maximum number of photos to return. By default, "5".
        :param start_from: "new_from" value obtained in previous call.
        :param count: Number of news items to return.
        :param fields: Additional fields of [vk.com/dev/fields|profiles] and [vk.com/dev/fields_groups|communities] to return.
        """

    @api_method
    async def get_suggested_sources(
        self,
        *,
        offset: ty.Optional[int] = None,
        count: int = 20,
        shuffle: ty.Optional[bool] = None,
        fields: ty.Optional[ty.Sequence] = None,
        **kwargs
    ) -> 1:
        """
        Returns communities and users that current user is suggested to follow.

        :param offset: offset required to choose a particular subset of communities or users.
        :param count: amount of communities or users to return.
        :param shuffle: shuffle the returned list or not.
        :param fields: list of extra fields to be returned. See available fields for [vk.com/dev/fields|users] and [vk.com/dev/fields_groups|communities].
        """

    @api_method
    async def ignore_item(
        self, *, type: str, owner_id: int = 0, item_id: int = 0, **kwargs
    ) -> 1:
        """
        Hides an item from the newsfeed.

        :param type: Item type. Possible values: *"wall" – post on the wall,, *"tag" – tag on a photo,, *"profilephoto" – profile photo,, *"video" – video,, *"audio" – audio.
        :param owner_id: Item owner"s identifier (user or community), "Note that community id must be negative. "owner_id=1" – user , "owner_id=-1" – community "
        :param item_id: Item identifier
        """

    @api_method
    async def save_list(
        self,
        *,
        list_id: ty.Optional[int] = None,
        title: str,
        source_ids: ty.Optional[ty.Sequence] = None,
        no_reposts: ty.Optional[bool] = None,
        **kwargs
    ) -> 1:
        """
        Creates and edits user newsfeed lists

        :param list_id: numeric list identifier (if not sent, will be set automatically).
        :param title: list name.
        :param source_ids: users and communities identifiers to be added to the list. Community identifiers must be negative numbers.
        :param no_reposts: reposts display on and off ("1" is for off).
        """

    @api_method
    async def search(
        self,
        *,
        q: ty.Optional[str] = None,
        extended: ty.Optional[bool] = None,
        count: int = 30,
        latitude: ty.Optional[float] = None,
        longitude: ty.Optional[float] = None,
        start_time: ty.Optional[int] = None,
        end_time: ty.Optional[int] = None,
        start_from: ty.Optional[str] = None,
        fields: ty.Optional[ty.Sequence] = None,
        **kwargs
    ) -> 1:
        """
        Returns search results by statuses.

        :param q: Search query string (e.g., "New Year").
        :param extended: "1" — to return additional information about the user or community that placed the post.
        :param count: Number of posts to return.
        :param latitude: Geographical latitude point (in degrees, -90 to 90) within which to search.
        :param longitude: Geographical longitude point (in degrees, -180 to 180) within which to search.
        :param start_time: Earliest timestamp (in Unix time) of a news item to return. By default, 24 hours ago.
        :param end_time: Latest timestamp (in Unix time) of a news item to return. By default, the current time.
        :param start_from: No description provided
        :param fields: Additional fields of [vk.com/dev/fields|profiles] and [vk.com/dev/fields_groups|communities] to return.
        """

    @api_method
    async def unignore_item(
        self,
        *,
        type: str,
        owner_id: int,
        item_id: int,
        track_code: ty.Optional[str] = None,
        **kwargs
    ) -> 1:
        """
        Returns a hidden item to the newsfeed.

        :param type: Item type. Possible values: *"wall" – post on the wall,, *"tag" – tag on a photo,, *"profilephoto" – profile photo,, *"video" – video,, *"audio" – audio.
        :param owner_id: Item owner"s identifier (user or community), "Note that community id must be negative. "owner_id=1" – user , "owner_id=-1" – community "
        :param item_id: Item identifier
        :param track_code: Track code of unignored item
        """

    @api_method
    async def unsubscribe(
        self,
        *,
        type: str,
        owner_id: ty.Optional[int] = None,
        item_id: int,
        **kwargs
    ) -> 1:
        """
        Unsubscribes the current user from specified newsfeeds.

        :param type: Type of object from which to unsubscribe: "note" — note, "photo" — photo, "post" — post on user wall or community wall, "topic" — topic, "video" — video
        :param owner_id: Object owner ID.
        :param item_id: Object ID.
        """


class Notes(APIMethod):
    @api_method
    async def add(
        self,
        *,
        title: str,
        text: str,
        privacy_view: ty.List[str] = (all,),
        privacy_comment: ty.List[str] = (all,),
        **kwargs
    ) -> 1:
        """
        Creates a new note for the current user.

        :param title: Note title.
        :param text: Note text.
        :param privacy_view: No description provided
        :param privacy_comment: No description provided
        """

    @api_method
    async def create_comment(
        self,
        *,
        note_id: int,
        owner_id: ty.Optional[int] = None,
        reply_to: ty.Optional[int] = None,
        message: str,
        guid: ty.Optional[str] = None,
        **kwargs
    ) -> 1:
        """
        Adds a new comment on a note.

        :param note_id: Note ID.
        :param owner_id: Note owner ID.
        :param reply_to: ID of the user to whom the reply is addressed (if the comment is a reply to another comment).
        :param message: Comment text.
        :param guid: No description provided
        """

    @api_method
    async def delete(self, *, note_id: int, **kwargs) -> 1:
        """
        Deletes a note of the current user.

        :param note_id: Note ID.
        """

    @api_method
    async def delete_comment(
        self, *, comment_id: int, owner_id: ty.Optional[int] = None, **kwargs
    ) -> 1:
        """
        Deletes a comment on a note.

        :param comment_id: Comment ID.
        :param owner_id: Note owner ID.
        """

    @api_method
    async def edit(
        self,
        *,
        note_id: int,
        title: str,
        text: str,
        privacy_view: ty.List[str] = (all,),
        privacy_comment: ty.List[str] = (all,),
        **kwargs
    ) -> 1:
        """
        Edits a note of the current user.

        :param note_id: Note ID.
        :param title: Note title.
        :param text: Note text.
        :param privacy_view: No description provided
        :param privacy_comment: No description provided
        """

    @api_method
    async def edit_comment(
        self,
        *,
        comment_id: int,
        owner_id: ty.Optional[int] = None,
        message: str,
        **kwargs
    ) -> 1:
        """
        Edits a comment on a note.

        :param comment_id: Comment ID.
        :param owner_id: Note owner ID.
        :param message: New comment text.
        """

    @api_method
    async def get(
        self,
        *,
        note_ids: ty.Optional[ty.Sequence] = None,
        user_id: ty.Optional[int] = None,
        offset: int = 0,
        count: int = 20,
        sort: int = 0,
        **kwargs
    ) -> 1:
        """
        Returns a list of notes created by a user.

        :param note_ids: Note IDs.
        :param user_id: Note owner ID.
        :param offset: No description provided
        :param count: Number of notes to return.
        :param sort: No description provided
        """

    @api_method
    async def get_by_id(
        self,
        *,
        note_id: int,
        owner_id: ty.Optional[int] = None,
        need_wiki: bool = 0,
        **kwargs
    ) -> 1:
        """
        Returns a note by its ID.

        :param note_id: Note ID.
        :param owner_id: Note owner ID.
        :param need_wiki: No description provided
        """

    @api_method
    async def get_comments(
        self,
        *,
        note_id: int,
        owner_id: ty.Optional[int] = None,
        sort: int = 0,
        offset: int = 0,
        count: int = 20,
        **kwargs
    ) -> 1:
        """
        Returns a list of comments on a note.

        :param note_id: Note ID.
        :param owner_id: Note owner ID.
        :param sort: No description provided
        :param offset: No description provided
        :param count: Number of comments to return.
        """

    @api_method
    async def restore_comment(
        self, *, comment_id: int, owner_id: ty.Optional[int] = None, **kwargs
    ) -> 1:
        """
        Restores a deleted comment on a note.

        :param comment_id: Comment ID.
        :param owner_id: Note owner ID.
        """


class Notifications(APIMethod):
    @api_method
    async def get(
        self,
        *,
        count: int = 30,
        start_from: ty.Optional[str] = None,
        filters: ty.Optional[
            ty.Sequence[
                tye.Literal[
                    "wall",
                    "mentions",
                    "comments",
                    "likes",
                    "reposted",
                    "followers",
                    "friends",
                ]
            ]
        ] = None,
        start_time: ty.Optional[int] = None,
        end_time: ty.Optional[int] = None,
        **kwargs
    ) -> 1:
        """
        Returns a list of notifications about other users" feedback to the current user"s wall posts.

        :param count: Number of notifications to return.
        :param start_from: No description provided
        :param filters: Type of notifications to return: "wall" — wall posts, "mentions" — mentions in wall posts, comments, or topics, "comments" — comments to wall posts, photos, and videos, "likes" — likes, "reposted" — wall posts that are copied from the current user"s wall, "followers" — new followers, "friends" — accepted friend requests
        :param start_time: Earliest timestamp (in Unix time) of a notification to return. By default, 24 hours ago.
        :param end_time: Latest timestamp (in Unix time) of a notification to return. By default, the current time.
        """

    @api_method
    async def mark_as_viewed(self, **kwargs) -> 1:
        """
        Resets the counter of new notifications about other users" feedback to the current user"s wall posts.
        """

    @api_method
    async def send_message(
        self,
        *,
        user_ids: ty.Sequence,
        message: str,
        fragment: ty.Optional[str] = None,
        group_id: ty.Optional[int] = None,
        random_id: ty.Optional[int] = None,
        **kwargs
    ) -> 1:
        """
        No description provided

        :param user_ids: No description provided
        :param message: No description provided
        :param fragment: No description provided
        :param group_id: No description provided
        :param random_id: No description provided
        """


class Orders(APIMethod):
    @api_method
    async def cancel_subscription(
        self,
        *,
        user_id: int,
        subscription_id: int,
        pending_cancel: bool = 0,
        **kwargs
    ) -> 1:
        """
        No description provided

        :param user_id: No description provided
        :param subscription_id: No description provided
        :param pending_cancel: No description provided
        """

    @api_method
    async def change_state(
        self,
        *,
        order_id: int,
        action: str,
        app_order_id: ty.Optional[int] = None,
        test_mode: ty.Optional[bool] = None,
        **kwargs
    ) -> 1:
        """
        Changes order status.

        :param order_id: order ID.
        :param action: action to be done with the order. Available actions: *cancel — to cancel unconfirmed order. *charge — to confirm unconfirmed order. Applies only if processing of [vk.com/dev/payments_status|order_change_state] notification failed. *refund — to cancel confirmed order.
        :param app_order_id: internal ID of the order in the application.
        :param test_mode: if this parameter is set to 1, this method returns a list of test mode orders. By default — 0.
        """

    @api_method
    async def get(
        self,
        *,
        offset: int = 0,
        count: int = 100,
        test_mode: ty.Optional[bool] = None,
        **kwargs
    ) -> 1:
        """
        Returns a list of orders.

        :param offset: No description provided
        :param count: number of returned orders.
        :param test_mode: if this parameter is set to 1, this method returns a list of test mode orders. By default — 0.
        """

    @api_method
    async def get_amount(
        self, *, user_id: int, votes: ty.List[str], **kwargs
    ) -> 1:
        """
        No description provided

        :param user_id: No description provided
        :param votes: No description provided
        """

    @api_method
    async def get_by_id(
        self,
        *,
        order_id: ty.Optional[int] = None,
        order_ids: ty.Optional[ty.Sequence] = None,
        test_mode: ty.Optional[bool] = None,
        **kwargs
    ) -> 1:
        """
        Returns information about orders by their IDs.

        :param order_id: order ID.
        :param order_ids: order IDs (when information about several orders is requested).
        :param test_mode: if this parameter is set to 1, this method returns a list of test mode orders. By default — 0.
        """

    @api_method
    async def get_user_subscription_by_id(
        self, *, user_id: int, subscription_id: int, **kwargs
    ) -> 1:
        """
        No description provided

        :param user_id: No description provided
        :param subscription_id: No description provided
        """

    @api_method
    async def get_user_subscriptions(self, *, user_id: int, **kwargs) -> 1:
        """
        No description provided

        :param user_id: No description provided
        """

    @api_method
    async def update_subscription(
        self, *, user_id: int, subscription_id: int, price: int, **kwargs
    ) -> 1:
        """
        No description provided

        :param user_id: No description provided
        :param subscription_id: No description provided
        :param price: No description provided
        """


class Pages(APIMethod):
    @api_method
    async def clear_cache(self, *, url: str, **kwargs) -> 1:
        """
        Allows to clear the cache of particular "external" pages which may be attached to VK posts.

        :param url: Address of the page where you need to refesh the cached version
        """

    @api_method
    async def get(
        self,
        *,
        owner_id: ty.Optional[int] = None,
        page_id: ty.Optional[int] = None,
        global_: ty.Optional[bool] = None,
        site_preview: ty.Optional[bool] = None,
        title: ty.Optional[str] = None,
        need_source: ty.Optional[bool] = None,
        need_html: ty.Optional[bool] = None,
        **kwargs
    ) -> 1:
        """
        Returns information about a wiki page.

        :param owner_id: Page owner ID.
        :param page_id: Wiki page ID.
        :param global_: "1" — to return information about a global wiki page
        :param site_preview: "1" — resulting wiki page is a preview for the attached link
        :param title: Wiki page title.
        :param need_source: No description provided
        :param need_html: "1" — to return the page as HTML,
        """

    @api_method
    async def get_history(
        self,
        *,
        page_id: int,
        group_id: ty.Optional[int] = None,
        user_id: ty.Optional[int] = None,
        **kwargs
    ) -> 1:
        """
        Returns a list of all previous versions of a wiki page.

        :param page_id: Wiki page ID.
        :param group_id: ID of the community that owns the wiki page.
        :param user_id: No description provided
        """

    @api_method
    async def get_titles(
        self, *, group_id: ty.Optional[int] = None, **kwargs
    ) -> 1:
        """
        Returns a list of wiki pages in a group.

        :param group_id: ID of the community that owns the wiki page.
        """

    @api_method
    async def get_version(
        self,
        *,
        version_id: int,
        group_id: ty.Optional[int] = None,
        user_id: ty.Optional[int] = None,
        need_html: ty.Optional[bool] = None,
        **kwargs
    ) -> 1:
        """
        Returns the text of one of the previous versions of a wiki page.

        :param version_id: No description provided
        :param group_id: ID of the community that owns the wiki page.
        :param user_id: No description provided
        :param need_html: "1" — to return the page as HTML
        """

    @api_method
    async def parse_wiki(
        self, *, text: str, group_id: ty.Optional[int] = None, **kwargs
    ) -> 1:
        """
        Returns HTML representation of the wiki markup.

        :param text: Text of the wiki page.
        :param group_id: ID of the group in the context of which this markup is interpreted.
        """

    @api_method
    async def save(
        self,
        *,
        text: ty.Optional[str] = None,
        page_id: ty.Optional[int] = None,
        group_id: ty.Optional[int] = None,
        user_id: ty.Optional[int] = None,
        title: ty.Optional[str] = None,
        **kwargs
    ) -> 1:
        """
        Saves the text of a wiki page.

        :param text: Text of the wiki page in wiki-format.
        :param page_id: Wiki page ID. The "title" parameter can be passed instead of "pid".
        :param group_id: ID of the community that owns the wiki page.
        :param user_id: User ID
        :param title: Wiki page title.
        """

    @api_method
    async def save_access(
        self,
        *,
        page_id: int,
        group_id: ty.Optional[int] = None,
        user_id: ty.Optional[int] = None,
        view: ty.Optional[int] = None,
        edit: ty.Optional[int] = None,
        **kwargs
    ) -> 1:
        """
        Saves modified read and edit access settings for a wiki page.

        :param page_id: Wiki page ID.
        :param group_id: ID of the community that owns the wiki page.
        :param user_id: No description provided
        :param view: Who can view the wiki page: "1" — only community members, "2" — all users can view the page, "0" — only community managers
        :param edit: Who can edit the wiki page: "1" — only community members, "2" — all users can edit the page, "0" — only community managers
        """


class Photos(APIMethod):
    @api_method
    async def confirm_tag(
        self,
        *,
        owner_id: ty.Optional[int] = None,
        photo_id: str,
        tag_id: int,
        **kwargs
    ) -> 1:
        """
        Confirms a tag on a photo.

        :param owner_id: ID of the user or community that owns the photo.
        :param photo_id: Photo ID.
        :param tag_id: Tag ID.
        """

    @api_method
    async def copy(
        self,
        *,
        owner_id: int,
        photo_id: int,
        access_key: ty.Optional[str] = None,
        **kwargs
    ) -> 1:
        """
        Allows to copy a photo to the "Saved photos" album

        :param owner_id: photo"s owner ID
        :param photo_id: photo ID
        :param access_key: for private photos
        """

    @api_method
    async def create_album(
        self,
        *,
        title: str,
        group_id: ty.Optional[int] = None,
        description: ty.Optional[str] = None,
        privacy_view: ty.List[str] = (all,),
        privacy_comment: ty.List[str] = (all,),
        upload_by_admins_only: ty.Optional[bool] = None,
        comments_disabled: ty.Optional[bool] = None,
        **kwargs
    ) -> 1:
        """
        Creates an empty photo album.

        :param title: Album title.
        :param group_id: ID of the community in which the album will be created.
        :param description: Album description.
        :param privacy_view: No description provided
        :param privacy_comment: No description provided
        :param upload_by_admins_only: No description provided
        :param comments_disabled: No description provided
        """

    @api_method
    async def create_comment(
        self,
        *,
        owner_id: ty.Optional[int] = None,
        photo_id: int,
        message: ty.Optional[str] = None,
        attachments: ty.Optional[ty.List[str]] = None,
        from_group: ty.Optional[bool] = None,
        reply_to_comment: ty.Optional[int] = None,
        sticker_id: ty.Optional[int] = None,
        access_key: ty.Optional[str] = None,
        guid: ty.Optional[str] = None,
        **kwargs
    ) -> 1:
        """
        Adds a new comment on the photo.

        :param owner_id: ID of the user or community that owns the photo.
        :param photo_id: Photo ID.
        :param message: Comment text.
        :param attachments: (Required if "message" is not set.) List of objects attached to the post, in the following format: "<owner_id>_<media_id>,<owner_id>_<media_id>", "" — Type of media attachment: "photo" — photo, "video" — video, "audio" — audio, "doc" — document, "<owner_id>" — Media attachment owner ID. "<media_id>" — Media attachment ID. Example: "photo100172_166443618,photo66748_265827614"
        :param from_group: "1" — to post a comment from the community
        :param reply_to_comment: No description provided
        :param sticker_id: No description provided
        :param access_key: No description provided
        :param guid: No description provided
        """

    @api_method
    async def delete(
        self, *, owner_id: ty.Optional[int] = None, photo_id: int, **kwargs
    ) -> 1:
        """
        Deletes a photo.

        :param owner_id: ID of the user or community that owns the photo.
        :param photo_id: Photo ID.
        """

    @api_method
    async def delete_album(
        self, *, album_id: int, group_id: ty.Optional[int] = None, **kwargs
    ) -> 1:
        """
        Deletes a photo album belonging to the current user.

        :param album_id: Album ID.
        :param group_id: ID of the community that owns the album.
        """

    @api_method
    async def delete_comment(
        self, *, owner_id: ty.Optional[int] = None, comment_id: int, **kwargs
    ) -> 1:
        """
        Deletes a comment on the photo.

        :param owner_id: ID of the user or community that owns the photo.
        :param comment_id: Comment ID.
        """

    @api_method
    async def edit(
        self,
        *,
        owner_id: ty.Optional[int] = None,
        photo_id: int,
        caption: ty.Optional[str] = None,
        latitude: ty.Optional[float] = None,
        longitude: ty.Optional[float] = None,
        place_str: ty.Optional[str] = None,
        foursquare_id: ty.Optional[str] = None,
        delete_place: ty.Optional[bool] = None,
        **kwargs
    ) -> 1:
        """
        Edits the caption of a photo.

        :param owner_id: ID of the user or community that owns the photo.
        :param photo_id: Photo ID.
        :param caption: New caption for the photo. If this parameter is not set, it is considered to be equal to an empty string.
        :param latitude: No description provided
        :param longitude: No description provided
        :param place_str: No description provided
        :param foursquare_id: No description provided
        :param delete_place: No description provided
        """

    @api_method
    async def edit_album(
        self,
        *,
        album_id: int,
        title: ty.Optional[str] = None,
        description: ty.Optional[str] = None,
        owner_id: ty.Optional[int] = None,
        privacy_view: ty.Optional[ty.List[str]] = None,
        privacy_comment: ty.Optional[ty.List[str]] = None,
        upload_by_admins_only: ty.Optional[bool] = None,
        comments_disabled: ty.Optional[bool] = None,
        **kwargs
    ) -> 1:
        """
        Edits information about a photo album.

        :param album_id: ID of the photo album to be edited.
        :param title: New album title.
        :param description: New album description.
        :param owner_id: ID of the user or community that owns the album.
        :param privacy_view: No description provided
        :param privacy_comment: No description provided
        :param upload_by_admins_only: No description provided
        :param comments_disabled: No description provided
        """

    @api_method
    async def edit_comment(
        self,
        *,
        owner_id: ty.Optional[int] = None,
        comment_id: int,
        message: ty.Optional[str] = None,
        attachments: ty.Optional[ty.List[str]] = None,
        **kwargs
    ) -> 1:
        """
        Edits a comment on a photo.

        :param owner_id: ID of the user or community that owns the photo.
        :param comment_id: Comment ID.
        :param message: New text of the comment.
        :param attachments: (Required if "message" is not set.) List of objects attached to the post, in the following format: "<owner_id>_<media_id>,<owner_id>_<media_id>", "" — Type of media attachment: "photo" — photo, "video" — video, "audio" — audio, "doc" — document, "<owner_id>" — Media attachment owner ID. "<media_id>" — Media attachment ID. Example: "photo100172_166443618,photo66748_265827614"
        """

    @api_method
    async def get(
        self,
        *,
        owner_id: ty.Optional[int] = None,
        album_id: ty.Optional[str] = None,
        photo_ids: ty.Optional[ty.List[ty.Union[str, int]]] = None,
        rev: ty.Optional[bool] = None,
        extended: ty.Optional[bool] = None,
        feed_type: ty.Optional[str] = None,
        feed: ty.Optional[int] = None,
        photo_sizes: ty.Optional[bool] = None,
        offset: ty.Optional[int] = None,
        count: int = 50,
        **kwargs
    ) -> 1:
        """
        Returns a list of a user"s or community"s photos.

        :param owner_id: ID of the user or community that owns the photos. Use a negative value to designate a community ID.
        :param album_id: Photo album ID. To return information about photos from service albums, use the following string values: "profile, wall, saved".
        :param photo_ids: Photo IDs.
        :param rev: Sort order: "1" — reverse chronological, "0" — chronological
        :param extended: "1" — to return additional "likes", "comments", and "tags" fields, "0" — (default)
        :param feed_type: Type of feed obtained in "feed" field of the method.
        :param feed: unixtime, that can be obtained with [vk.com/dev/newsfeed.get|newsfeed.get] method in date field to get all photos uploaded by the user on a specific day, or photos the user has been tagged on. Also, "uid" parameter of the user the event happened with shall be specified.
        :param photo_sizes: "1" — to return photo sizes in a [vk.com/dev/photo_sizes|special format]
        :param offset: No description provided
        :param count: No description provided
        """

    @api_method
    async def get_albums(
        self,
        *,
        owner_id: ty.Optional[int] = None,
        album_ids: ty.Optional[ty.Sequence] = None,
        offset: ty.Optional[int] = None,
        count: ty.Optional[int] = None,
        need_system: ty.Optional[bool] = None,
        need_covers: ty.Optional[bool] = None,
        photo_sizes: ty.Optional[bool] = None,
        **kwargs
    ) -> 1:
        """
        Returns a list of a user"s or community"s photo albums.

        :param owner_id: ID of the user or community that owns the albums.
        :param album_ids: Album IDs.
        :param offset: Offset needed to return a specific subset of albums.
        :param count: Number of albums to return.
        :param need_system: "1" — to return system albums with negative IDs
        :param need_covers: "1" — to return an additional "thumb_src" field, "0" — (default)
        :param photo_sizes: "1" — to return photo sizes in a
        """

    @api_method
    async def get_albums_count(
        self,
        *,
        user_id: ty.Optional[int] = None,
        group_id: ty.Optional[int] = None,
        **kwargs
    ) -> 1:
        """
        Returns the number of photo albums belonging to a user or community.

        :param user_id: User ID.
        :param group_id: Community ID.
        """

    @api_method
    async def get_all(
        self,
        *,
        owner_id: ty.Optional[int] = None,
        extended: ty.Optional[bool] = None,
        offset: ty.Optional[int] = None,
        count: int = 20,
        photo_sizes: ty.Optional[bool] = None,
        no_service_albums: ty.Optional[bool] = None,
        need_hidden: ty.Optional[bool] = None,
        skip_hidden: ty.Optional[bool] = None,
        **kwargs
    ) -> 1:
        """
        Returns a list of photos belonging to a user or community, in reverse chronological order.

        :param owner_id: ID of a user or community that owns the photos. Use a negative value to designate a community ID.
        :param extended: "1" — to return detailed information about photos
        :param offset: Offset needed to return a specific subset of photos. By default, "0".
        :param count: Number of photos to return.
        :param photo_sizes: "1" – to return image sizes in [vk.com/dev/photo_sizes|special format].
        :param no_service_albums: "1" – to return photos only from standard albums, "0" – to return all photos including those in service albums, e.g., "My wall photos" (default)
        :param need_hidden: "1" – to show information about photos being hidden from the block above the wall.
        :param skip_hidden: "1" – not to return photos being hidden from the block above the wall. Works only with owner_id>0, no_service_albums is ignored.
        """

    @api_method
    async def get_all_comments(
        self,
        *,
        owner_id: ty.Optional[int] = None,
        album_id: ty.Optional[int] = None,
        need_likes: ty.Optional[bool] = None,
        offset: ty.Optional[int] = None,
        count: ty.Optional[int] = None,
        **kwargs
    ) -> 1:
        """
        Returns a list of comments on a specific photo album or all albums of the user sorted in reverse chronological order.

        :param owner_id: ID of the user or community that owns the album(s).
        :param album_id: Album ID. If the parameter is not set, comments on all of the user"s albums will be returned.
        :param need_likes: "1" — to return an additional "likes" field, "0" — (default)
        :param offset: Offset needed to return a specific subset of comments. By default, "0".
        :param count: Number of comments to return. By default, "20". Maximum value, "100".
        """

    @api_method
    async def get_by_id(
        self,
        *,
        photos: ty.List[str],
        extended: ty.Optional[bool] = None,
        photo_sizes: ty.Optional[bool] = None,
        **kwargs
    ) -> 1:
        """
        Returns information about photos by their IDs.

        :param photos: IDs separated with a comma, that are IDs of users who posted photos and IDs of photos themselves with an underscore character between such IDs. To get information about a photo in the group album, you shall specify group ID instead of user ID. Example: "1_129207899,6492_135055734, , -20629724_271945303"
        :param extended: "1" — to return additional fields, "0" — (default)
        :param photo_sizes: "1" — to return photo sizes in a
        """

    @api_method
    async def get_chat_upload_server(
        self,
        *,
        chat_id: int,
        crop_x: ty.Optional[int] = None,
        crop_y: ty.Optional[int] = None,
        crop_width: ty.Optional[int] = None,
        **kwargs
    ) -> 1:
        """
        Returns an upload link for chat cover pictures.

        :param chat_id: ID of the chat for which you want to upload a cover photo.
        :param crop_x: No description provided
        :param crop_y: No description provided
        :param crop_width: Width (in pixels) of the photo after cropping.
        """

    @api_method
    async def get_comments(
        self,
        *,
        owner_id: ty.Optional[int] = None,
        photo_id: int,
        need_likes: ty.Optional[bool] = None,
        start_comment_id: ty.Optional[int] = None,
        offset: ty.Optional[int] = None,
        count: int = "20",
        sort: ty.Optional[str] = None,
        access_key: ty.Optional[str] = None,
        extended: ty.Optional[bool] = None,
        fields: ty.Optional[ty.Sequence] = None,
        **kwargs
    ) -> 1:
        """
        Returns a list of comments on a photo.

        :param owner_id: ID of the user or community that owns the photo.
        :param photo_id: Photo ID.
        :param need_likes: "1" — to return an additional "likes" field, "0" — (default)
        :param start_comment_id: No description provided
        :param offset: Offset needed to return a specific subset of comments. By default, "0".
        :param count: Number of comments to return.
        :param sort: Sort order: "asc" — old first, "desc" — new first
        :param access_key: No description provided
        :param extended: No description provided
        :param fields: No description provided
        """

    @api_method
    async def get_market_album_upload_server(
        self, *, group_id: int, **kwargs
    ) -> 1:
        """
        Returns the server address for market album photo upload.

        :param group_id: Community ID.
        """

    @api_method
    async def get_market_upload_server(
        self,
        *,
        group_id: int,
        main_photo: ty.Optional[bool] = None,
        crop_x: ty.Optional[int] = None,
        crop_y: ty.Optional[int] = None,
        crop_width: ty.Optional[int] = None,
        **kwargs
    ) -> 1:
        """
        Returns the server address for market photo upload.

        :param group_id: Community ID.
        :param main_photo: "1" if you want to upload the main item photo.
        :param crop_x: X coordinate of the crop left upper corner.
        :param crop_y: Y coordinate of the crop left upper corner.
        :param crop_width: Width of the cropped photo in px.
        """

    @api_method
    async def get_messages_upload_server(
        self, *, peer_id: ty.Optional[int] = None, **kwargs
    ) -> 1:
        """
        Returns the server address for photo upload in a private message for a user.

        :param peer_id: Destination ID. "For user: "User ID", e.g. "12345". For chat: "2000000000" + "Chat ID", e.g. "2000000001". For community: "- Community ID", e.g. "-12345". "
        """

    @api_method
    async def get_new_tags(
        self, *, offset: ty.Optional[int] = None, count: int = 20, **kwargs
    ) -> 1:
        """
        Returns a list of photos with tags that have not been viewed.

        :param offset: Offset needed to return a specific subset of photos.
        :param count: Number of photos to return.
        """

    @api_method
    async def get_owner_cover_photo_upload_server(
        self,
        *,
        group_id: int,
        crop_x: int = 0,
        crop_y: int = 0,
        crop_x2: int = 795,
        crop_y2: int = 200,
        **kwargs
    ) -> 1:
        """
        Returns the server address for owner cover upload.

        :param group_id: ID of community that owns the album (if the photo will be uploaded to a community album).
        :param crop_x: X coordinate of the left-upper corner
        :param crop_y: Y coordinate of the left-upper corner
        :param crop_x2: X coordinate of the right-bottom corner
        :param crop_y2: Y coordinate of the right-bottom corner
        """

    @api_method
    async def get_owner_photo_upload_server(
        self, *, owner_id: ty.Optional[int] = None, **kwargs
    ) -> 1:
        """
        Returns an upload server address for a profile or community photo.

        :param owner_id: identifier of a community or current user. "Note that community id must be negative. "owner_id=1" – user, "owner_id=-1" – community, "
        """

    @api_method
    async def get_tags(
        self,
        *,
        owner_id: ty.Optional[int] = None,
        photo_id: int,
        access_key: ty.Optional[str] = None,
        **kwargs
    ) -> 1:
        """
        Returns a list of tags on a photo.

        :param owner_id: ID of the user or community that owns the photo.
        :param photo_id: Photo ID.
        :param access_key: No description provided
        """

    @api_method
    async def get_upload_server(
        self,
        *,
        group_id: ty.Optional[int] = None,
        album_id: ty.Optional[int] = None,
        **kwargs
    ) -> 1:
        """
        Returns the server address for photo upload.

        :param group_id: ID of community that owns the album (if the photo will be uploaded to a community album).
        :param album_id: No description provided
        """

    @api_method
    async def get_user_photos(
        self,
        *,
        user_id: ty.Optional[int] = None,
        offset: ty.Optional[int] = None,
        count: int = 20,
        extended: ty.Optional[bool] = None,
        sort: ty.Optional[str] = None,
        **kwargs
    ) -> 1:
        """
        Returns a list of photos in which a user is tagged.

        :param user_id: User ID.
        :param offset: Offset needed to return a specific subset of photos. By default, "0".
        :param count: Number of photos to return. Maximum value is 1000.
        :param extended: "1" — to return an additional "likes" field, "0" — (default)
        :param sort: Sort order: "1" — by date the tag was added in ascending order, "0" — by date the tag was added in descending order
        """

    @api_method
    async def get_wall_upload_server(
        self, *, group_id: ty.Optional[int] = None, **kwargs
    ) -> 1:
        """
        Returns the server address for photo upload onto a user"s wall.

        :param group_id: ID of community to whose wall the photo will be uploaded.
        """

    @api_method
    async def make_cover(
        self,
        *,
        owner_id: ty.Optional[int] = None,
        photo_id: int,
        album_id: ty.Optional[int] = None,
        **kwargs
    ) -> 1:
        """
        Makes a photo into an album cover.

        :param owner_id: ID of the user or community that owns the photo.
        :param photo_id: Photo ID.
        :param album_id: Album ID.
        """

    @api_method
    async def move(
        self,
        *,
        owner_id: ty.Optional[int] = None,
        target_album_id: int,
        photo_id: int,
        **kwargs
    ) -> 1:
        """
        Moves a photo from one album to another.

        :param owner_id: ID of the user or community that owns the photo.
        :param target_album_id: ID of the album to which the photo will be moved.
        :param photo_id: Photo ID.
        """

    @api_method
    async def put_tag(
        self,
        *,
        owner_id: ty.Optional[int] = None,
        photo_id: int,
        user_id: int,
        x: ty.Optional[float] = None,
        y: ty.Optional[float] = None,
        x2: ty.Optional[float] = None,
        y2: ty.Optional[float] = None,
        **kwargs
    ) -> 1:
        """
        Adds a tag on the photo.

        :param owner_id: ID of the user or community that owns the photo.
        :param photo_id: Photo ID.
        :param user_id: ID of the user to be tagged.
        :param x: Upper left-corner coordinate of the tagged area (as a percentage of the photo"s width).
        :param y: Upper left-corner coordinate of the tagged area (as a percentage of the photo"s height).
        :param x2: Lower right-corner coordinate of the tagged area (as a percentage of the photo"s width).
        :param y2: Lower right-corner coordinate of the tagged area (as a percentage of the photo"s height).
        """

    @api_method
    async def remove_tag(
        self,
        *,
        owner_id: ty.Optional[int] = None,
        photo_id: int,
        tag_id: int,
        **kwargs
    ) -> 1:
        """
        Removes a tag from a photo.

        :param owner_id: ID of the user or community that owns the photo.
        :param photo_id: Photo ID.
        :param tag_id: Tag ID.
        """

    @api_method
    async def reorder_albums(
        self,
        *,
        owner_id: ty.Optional[int] = None,
        album_id: int,
        before: ty.Optional[int] = None,
        after: ty.Optional[int] = None,
        **kwargs
    ) -> 1:
        """
        Reorders the album in the list of user albums.

        :param owner_id: ID of the user or community that owns the album.
        :param album_id: Album ID.
        :param before: ID of the album before which the album in question shall be placed.
        :param after: ID of the album after which the album in question shall be placed.
        """

    @api_method
    async def reorder_photos(
        self,
        *,
        owner_id: ty.Optional[int] = None,
        photo_id: int,
        before: ty.Optional[int] = None,
        after: ty.Optional[int] = None,
        **kwargs
    ) -> 1:
        """
        Reorders the photo in the list of photos of the user album.

        :param owner_id: ID of the user or community that owns the photo.
        :param photo_id: Photo ID.
        :param before: ID of the photo before which the photo in question shall be placed.
        :param after: ID of the photo after which the photo in question shall be placed.
        """

    @api_method
    async def report(
        self,
        *,
        owner_id: int,
        photo_id: int,
        reason: ty.Optional[int] = None,
        **kwargs
    ) -> 1:
        """
        Reports (submits a complaint about) a photo.

        :param owner_id: ID of the user or community that owns the photo.
        :param photo_id: Photo ID.
        :param reason: Reason for the complaint: "0" – spam, "1" – child pornography, "2" – extremism, "3" – violence, "4" – drug propaganda, "5" – adult material, "6" – insult, abuse
        """

    @api_method
    async def report_comment(
        self,
        *,
        owner_id: int,
        comment_id: int,
        reason: ty.Optional[int] = None,
        **kwargs
    ) -> 1:
        """
        Reports (submits a complaint about) a comment on a photo.

        :param owner_id: ID of the user or community that owns the photo.
        :param comment_id: ID of the comment being reported.
        :param reason: Reason for the complaint: "0" – spam, "1" – child pornography, "2" – extremism, "3" – violence, "4" – drug propaganda, "5" – adult material, "6" – insult, abuse
        """

    @api_method
    async def restore(
        self, *, owner_id: ty.Optional[int] = None, photo_id: int, **kwargs
    ) -> 1:
        """
        Restores a deleted photo.

        :param owner_id: ID of the user or community that owns the photo.
        :param photo_id: Photo ID.
        """

    @api_method
    async def restore_comment(
        self, *, owner_id: ty.Optional[int] = None, comment_id: int, **kwargs
    ) -> 1:
        """
        Restores a deleted comment on a photo.

        :param owner_id: ID of the user or community that owns the photo.
        :param comment_id: ID of the deleted comment.
        """

    @api_method
    async def save(
        self,
        *,
        album_id: ty.Optional[int] = None,
        group_id: ty.Optional[int] = None,
        server: ty.Optional[int] = None,
        photos_list: ty.Optional[str] = None,
        hash: ty.Optional[str] = None,
        latitude: ty.Optional[float] = None,
        longitude: ty.Optional[float] = None,
        caption: ty.Optional[str] = None,
        **kwargs
    ) -> 1:
        """
        Saves photos after successful uploading.

        :param album_id: ID of the album to save photos to.
        :param group_id: ID of the community to save photos to.
        :param server: Parameter returned when photos are [vk.com/dev/upload_files|uploaded to server].
        :param photos_list: Parameter returned when photos are [vk.com/dev/upload_files|uploaded to server].
        :param hash: Parameter returned when photos are [vk.com/dev/upload_files|uploaded to server].
        :param latitude: Geographical latitude, in degrees (from "-90" to "90").
        :param longitude: Geographical longitude, in degrees (from "-180" to "180").
        :param caption: Text describing the photo. 2048 digits max.
        """

    @api_method
    async def save_market_album_photo(
        self, *, group_id: int, photo: str, server: int, hash: str, **kwargs
    ) -> 1:
        """
        Saves market album photos after successful uploading.

        :param group_id: Community ID.
        :param photo: Parameter returned when photos are [vk.com/dev/upload_files|uploaded to server].
        :param server: Parameter returned when photos are [vk.com/dev/upload_files|uploaded to server].
        :param hash: Parameter returned when photos are [vk.com/dev/upload_files|uploaded to server].
        """

    @api_method
    async def save_market_photo(
        self,
        *,
        group_id: ty.Optional[int] = None,
        photo: str,
        server: int,
        hash: str,
        crop_data: ty.Optional[str] = None,
        crop_hash: ty.Optional[str] = None,
        **kwargs
    ) -> 1:
        """
        Saves market photos after successful uploading.

        :param group_id: Community ID.
        :param photo: Parameter returned when photos are [vk.com/dev/upload_files|uploaded to server].
        :param server: Parameter returned when photos are [vk.com/dev/upload_files|uploaded to server].
        :param hash: Parameter returned when photos are [vk.com/dev/upload_files|uploaded to server].
        :param crop_data: Parameter returned when photos are [vk.com/dev/upload_files|uploaded to server].
        :param crop_hash: Parameter returned when photos are [vk.com/dev/upload_files|uploaded to server].
        """

    @api_method
    async def save_messages_photo(
        self,
        *,
        photo: str,
        server: ty.Optional[int] = None,
        hash: ty.Optional[str] = None,
        **kwargs
    ) -> 1:
        """
        Saves a photo after being successfully uploaded. URL obtained with [vk.com/dev/photos.getMessagesUploadServer|photos.getMessagesUploadServer] method.

        :param photo: Parameter returned when the photo is [vk.com/dev/upload_files|uploaded to the server].
        :param server: No description provided
        :param hash: No description provided
        """

    @api_method
    async def save_owner_cover_photo(
        self, *, hash: str, photo: str, **kwargs
    ) -> 1:
        """
        Saves cover photo after successful uploading.

        :param hash: Parameter returned when photos are [vk.com/dev/upload_files|uploaded to server].
        :param photo: Parameter returned when photos are [vk.com/dev/upload_files|uploaded to server].
        """

    @api_method
    async def save_owner_photo(
        self,
        *,
        server: ty.Optional[str] = None,
        hash: ty.Optional[str] = None,
        photo: ty.Optional[str] = None,
        **kwargs
    ) -> 1:
        """
        Saves a profile or community photo. Upload URL can be got with the [vk.com/dev/photos.getOwnerPhotoUploadServer|photos.getOwnerPhotoUploadServer] method.

        :param server: parameter returned after [vk.com/dev/upload_files|photo upload].
        :param hash: parameter returned after [vk.com/dev/upload_files|photo upload].
        :param photo: parameter returned after [vk.com/dev/upload_files|photo upload].
        """

    @api_method
    async def save_wall_photo(
        self,
        *,
        user_id: ty.Optional[int] = None,
        group_id: ty.Optional[int] = None,
        photo: str,
        server: ty.Optional[int] = None,
        hash: ty.Optional[str] = None,
        latitude: ty.Optional[float] = None,
        longitude: ty.Optional[float] = None,
        caption: ty.Optional[str] = None,
        **kwargs
    ) -> 1:
        """
        Saves a photo to a user"s or community"s wall after being uploaded.

        :param user_id: ID of the user on whose wall the photo will be saved.
        :param group_id: ID of community on whose wall the photo will be saved.
        :param photo: Parameter returned when the the photo is [vk.com/dev/upload_files|uploaded to the server].
        :param server: No description provided
        :param hash: No description provided
        :param latitude: Geographical latitude, in degrees (from "-90" to "90").
        :param longitude: Geographical longitude, in degrees (from "-180" to "180").
        :param caption: Text describing the photo. 2048 digits max.
        """

    @api_method
    async def search(
        self,
        *,
        q: ty.Optional[str] = None,
        lat: ty.Optional[float] = None,
        long: ty.Optional[float] = None,
        start_time: ty.Optional[int] = None,
        end_time: ty.Optional[int] = None,
        sort: ty.Optional[int] = None,
        offset: ty.Optional[int] = None,
        count: int = 100,
        radius: int = 5000,
        **kwargs
    ) -> 1:
        """
        Returns a list of photos.

        :param q: Search query string.
        :param lat: Geographical latitude, in degrees (from "-90" to "90").
        :param long: Geographical longitude, in degrees (from "-180" to "180").
        :param start_time: No description provided
        :param end_time: No description provided
        :param sort: Sort order:
        :param offset: Offset needed to return a specific subset of photos.
        :param count: Number of photos to return.
        :param radius: Radius of search in meters (works very approximately). Available values: "10", "100", "800", "6000", "50000".
        """


class Podcasts(APIMethod):
    @api_method
    async def search_podcast(
        self,
        *,
        search_string: str,
        offset: int = 0,
        count: int = 20,
        **kwargs
    ) -> 1:
        """
        No description provided

        :param search_string: No description provided
        :param offset: No description provided
        :param count: No description provided
        """


class Polls(APIMethod):
    @api_method
    async def add_vote(
        self,
        *,
        owner_id: ty.Optional[int] = None,
        poll_id: int,
        answer_ids: ty.Sequence,
        is_board: ty.Optional[bool] = None,
        **kwargs
    ) -> 1:
        """
        Adds the current user"s vote to the selected answer in the poll.

        :param owner_id: ID of the user or community that owns the poll. Use a negative value to designate a community ID.
        :param poll_id: Poll ID.
        :param answer_ids: No description provided
        :param is_board: No description provided
        """

    @api_method
    async def create(
        self,
        *,
        question: ty.Optional[str] = None,
        is_anonymous: ty.Optional[bool] = None,
        is_multiple: ty.Optional[bool] = None,
        end_date: ty.Optional[int] = None,
        owner_id: ty.Optional[int] = None,
        add_answers: ty.Optional[str] = None,
        photo_id: ty.Optional[int] = None,
        background_id: ty.Optional[str] = None,
        disable_unvote: ty.Optional[bool] = None,
        **kwargs
    ) -> 1:
        """
        Creates polls that can be attached to the users" or communities" posts.

        :param question: question text
        :param is_anonymous: "1" – anonymous poll, participants list is hidden,, "0" – public poll, participants list is available,, Default value is "0".
        :param is_multiple: No description provided
        :param end_date: No description provided
        :param owner_id: If a poll will be added to a communty it is required to send a negative group identifier. Current user by default.
        :param add_answers: available answers list, for example: " ["yes","no","maybe"]", There can be from 1 to 10 answers.
        :param photo_id: No description provided
        :param background_id: No description provided
        :param disable_unvote: No description provided
        """

    @api_method
    async def delete_vote(
        self,
        *,
        owner_id: ty.Optional[int] = None,
        poll_id: int,
        answer_id: int,
        is_board: ty.Optional[bool] = None,
        **kwargs
    ) -> 1:
        """
        Deletes the current user"s vote from the selected answer in the poll.

        :param owner_id: ID of the user or community that owns the poll. Use a negative value to designate a community ID.
        :param poll_id: Poll ID.
        :param answer_id: Answer ID.
        :param is_board: No description provided
        """

    @api_method
    async def edit(
        self,
        *,
        owner_id: ty.Optional[int] = None,
        poll_id: int,
        question: ty.Optional[str] = None,
        add_answers: ty.Optional[str] = None,
        edit_answers: ty.Optional[str] = None,
        delete_answers: ty.Optional[str] = None,
        end_date: ty.Optional[int] = None,
        photo_id: ty.Optional[int] = None,
        background_id: ty.Optional[str] = None,
        **kwargs
    ) -> 1:
        """
        Edits created polls

        :param owner_id: poll owner id
        :param poll_id: edited poll"s id
        :param question: new question text
        :param add_answers: answers list, for example: , "["yes","no","maybe"]"
        :param edit_answers: object containing answers that need to be edited,, key – answer id, value – new answer text. Example: {"382967099":"option1", "382967103":"option2"}"
        :param delete_answers: list of answer ids to be deleted. For example: "[382967099, 382967103]"
        :param end_date: No description provided
        :param photo_id: No description provided
        :param background_id: No description provided
        """

    @api_method
    async def get_backgrounds(self, **kwargs) -> 1:
        """
        No description provided
        """

    @api_method
    async def get_by_id(
        self,
        *,
        owner_id: ty.Optional[int] = None,
        is_board: ty.Optional[bool] = None,
        poll_id: int,
        extended: ty.Optional[bool] = None,
        friends_count: int = 3,
        fields: ty.Optional[ty.List[str]] = None,
        name_case: str = "nom",
        **kwargs
    ) -> 1:
        """
        Returns detailed information about a poll by its ID.

        :param owner_id: ID of the user or community that owns the poll. Use a negative value to designate a community ID.
        :param is_board: "1" – poll is in a board, "0" – poll is on a wall. "0" by default.
        :param poll_id: Poll ID.
        :param extended: No description provided
        :param friends_count: No description provided
        :param fields: No description provided
        :param name_case: No description provided
        """

    @api_method
    async def get_photo_upload_server(
        self, *, owner_id: ty.Optional[int] = None, **kwargs
    ) -> 1:
        """
        No description provided

        :param owner_id: No description provided
        """

    @api_method
    async def get_voters(
        self,
        *,
        owner_id: ty.Optional[int] = None,
        poll_id: int,
        answer_ids: ty.Sequence,
        is_board: ty.Optional[bool] = None,
        friends_only: ty.Optional[bool] = None,
        offset: ty.Optional[int] = None,
        count: ty.Optional[int] = None,
        fields: ty.Optional[ty.Sequence] = None,
        name_case: ty.Optional[str] = None,
        **kwargs
    ) -> 1:
        """
        Returns a list of IDs of users who selected specific answers in the poll.

        :param owner_id: ID of the user or community that owns the poll. Use a negative value to designate a community ID.
        :param poll_id: Poll ID.
        :param answer_ids: Answer IDs.
        :param is_board: No description provided
        :param friends_only: "1" — to return only current user"s friends, "0" — to return all users (default),
        :param offset: Offset needed to return a specific subset of voters. "0" — (default)
        :param count: Number of user IDs to return (if the "friends_only" parameter is not set, maximum "1000", otherwise "10"). "100" — (default)
        :param fields: Profile fields to return. Sample values: "nickname", "screen_name", "sex", "bdate (birthdate)", "city", "country", "timezone", "photo", "photo_medium", "photo_big", "has_mobile", "rate", "contacts", "education", "online", "counters".
        :param name_case: Case for declension of user name and surname: , "nom" — nominative (default) , "gen" — genitive , "dat" — dative , "acc" — accusative , "ins" — instrumental , "abl" — prepositional
        """

    @api_method
    async def save_photo(self, *, photo: str, hash: str, **kwargs) -> 1:
        """
        No description provided

        :param photo: No description provided
        :param hash: No description provided
        """


class Prettycards(APIMethod):
    @api_method
    async def create(
        self,
        *,
        owner_id: int,
        photo: str,
        title: str,
        link: str,
        price: ty.Optional[str] = None,
        price_old: ty.Optional[str] = None,
        button: ty.Optional[str] = None,
        **kwargs
    ) -> 1:
        """
        No description provided

        :param owner_id: No description provided
        :param photo: No description provided
        :param title: No description provided
        :param link: No description provided
        :param price: No description provided
        :param price_old: No description provided
        :param button: No description provided
        """

    @api_method
    async def delete(self, *, owner_id: int, card_id: int, **kwargs) -> 1:
        """
        No description provided

        :param owner_id: No description provided
        :param card_id: No description provided
        """

    @api_method
    async def edit(
        self,
        *,
        owner_id: int,
        card_id: int,
        photo: ty.Optional[str] = None,
        title: ty.Optional[str] = None,
        link: ty.Optional[str] = None,
        price: ty.Optional[str] = None,
        price_old: ty.Optional[str] = None,
        button: ty.Optional[str] = None,
        **kwargs
    ) -> 1:
        """
        No description provided

        :param owner_id: No description provided
        :param card_id: No description provided
        :param photo: No description provided
        :param title: No description provided
        :param link: No description provided
        :param price: No description provided
        :param price_old: No description provided
        :param button: No description provided
        """

    @api_method
    async def get(
        self, *, owner_id: int, offset: int = 0, count: int = 10, **kwargs
    ) -> 1:
        """
        No description provided

        :param owner_id: No description provided
        :param offset: No description provided
        :param count: No description provided
        """

    @api_method
    async def get_by_id(
        self, *, owner_id: int, card_ids: ty.Sequence, **kwargs
    ) -> 1:
        """
        No description provided

        :param owner_id: No description provided
        :param card_ids: No description provided
        """

    @api_method
    async def get_upload_u_r_l(self, **kwargs) -> 1:
        """
        No description provided
        """


class Search(APIMethod):
    @api_method
    async def get_hints(
        self,
        *,
        q: ty.Optional[str] = None,
        offset: ty.Optional[int] = None,
        limit: int = 9,
        filters: ty.Optional[ty.List[str]] = None,
        fields: ty.Optional[ty.List[str]] = None,
        search_global: bool = 1,
        **kwargs
    ) -> 1:
        """
        Allows the programmer to do a quick search for any substring.

        :param q: Search query string.
        :param offset: Offset for querying specific result subset
        :param limit: Maximum number of results to return.
        :param filters: No description provided
        :param fields: No description provided
        :param search_global: No description provided
        """


class Secure(APIMethod):
    @api_method
    async def add_app_event(
        self,
        *,
        user_id: int,
        activity_id: int,
        value: ty.Optional[int] = None,
        **kwargs
    ) -> 1:
        """
        Adds user activity information to an application

        :param user_id: ID of a user to save the data
        :param activity_id: there are 2 default activities: , * 1 – level. Works similar to ,, * 2 – points, saves points amount, Any other value is for saving completed missions
        :param value: depends on activity_id: * 1 – number, current level number,, * 2 – number, current user"s points amount, , Any other value is ignored
        """

    @api_method
    async def check_token(
        self,
        *,
        token: ty.Optional[str] = None,
        ip: ty.Optional[str] = None,
        **kwargs
    ) -> 1:
        """
        Checks the user authentication in "IFrame" and "Flash" apps using the "access_token" parameter.

        :param token: client "access_token"
        :param ip: user "ip address". Note that user may access using the "ipv6" address, in this case it is required to transmit the "ipv6" address. If not transmitted, the address will not be checked.
        """

    @api_method
    async def get_app_balance(self, **kwargs) -> 1:
        """
        Returns payment balance of the application in hundredth of a vote.
        """

    @api_method
    async def get_s_m_s_history(
        self,
        *,
        user_id: ty.Optional[int] = None,
        date_from: ty.Optional[int] = None,
        date_to: ty.Optional[int] = None,
        limit: int = 1000,
        **kwargs
    ) -> 1:
        """
        Shows a list of SMS notifications sent by the application using [vk.com/dev/secure.sendSMSNotification|secure.sendSMSNotification] method.

        :param user_id: No description provided
        :param date_from: filter by start date. It is set as UNIX-time.
        :param date_to: filter by end date. It is set as UNIX-time.
        :param limit: number of returned posts. By default — 1000.
        """

    @api_method
    async def get_transactions_history(
        self,
        *,
        type: ty.Optional[int] = None,
        uid_from: ty.Optional[int] = None,
        uid_to: ty.Optional[int] = None,
        date_from: ty.Optional[int] = None,
        date_to: ty.Optional[int] = None,
        limit: int = 1000,
        **kwargs
    ) -> 1:
        """
        Shows history of votes transaction between users and the application.

        :param type: No description provided
        :param uid_from: No description provided
        :param uid_to: No description provided
        :param date_from: No description provided
        :param date_to: No description provided
        :param limit: No description provided
        """

    @api_method
    async def get_user_level(self, *, user_ids: ty.Sequence, **kwargs) -> 1:
        """
        Returns one of the previously set game levels of one or more users in the application.

        :param user_ids: No description provided
        """

    @api_method
    async def give_event_sticker(
        self, *, user_ids: ty.Sequence, achievement_id: int, **kwargs
    ) -> 1:
        """
        Opens the game achievement and gives the user a sticker

        :param user_ids: No description provided
        :param achievement_id: No description provided
        """

    @api_method
    async def send_notification(
        self,
        *,
        user_ids: ty.Optional[ty.Sequence] = None,
        user_id: ty.Optional[int] = None,
        message: str,
        **kwargs
    ) -> 1:
        """
        Sends notification to the user.

        :param user_ids: No description provided
        :param user_id: No description provided
        :param message: notification text which should be sent in "UTF-8" encoding ("254" characters maximum).
        """

    @api_method
    async def send_s_m_s_notification(
        self, *, user_id: int, message: str, **kwargs
    ) -> 1:
        """
        Sends "SMS" notification to a user"s mobile device.

        :param user_id: ID of the user to whom SMS notification is sent. The user shall allow the application to send him/her notifications (, +1).
        :param message: "SMS" text to be sent in "UTF-8" encoding. Only Latin letters and numbers are allowed. Maximum size is "160" characters.
        """

    @api_method
    async def set_counter(
        self,
        *,
        counters: ty.Optional[ty.List[str]] = None,
        user_id: ty.Optional[int] = None,
        counter: ty.Optional[int] = None,
        increment: ty.Optional[bool] = None,
        **kwargs
    ) -> 1:
        """
        Sets a counter which is shown to the user in bold in the left menu.

        :param counters: No description provided
        :param user_id: No description provided
        :param counter: counter value.
        :param increment: No description provided
        """


class Stats(APIMethod):
    @api_method
    async def get(
        self,
        *,
        group_id: ty.Optional[int] = None,
        app_id: ty.Optional[int] = None,
        timestamp_from: ty.Optional[int] = None,
        timestamp_to: ty.Optional[int] = None,
        interval: str = "day",
        intervals_count: ty.Optional[int] = None,
        filters: ty.Optional[ty.List[str]] = None,
        stats_groups: ty.Optional[ty.List[str]] = None,
        extended: bool = True,
        **kwargs
    ) -> 1:
        """
        Returns statistics of a community or an application.

        :param group_id: Community ID.
        :param app_id: Application ID.
        :param timestamp_from: No description provided
        :param timestamp_to: No description provided
        :param interval: No description provided
        :param intervals_count: No description provided
        :param filters: No description provided
        :param stats_groups: No description provided
        :param extended: No description provided
        """

    @api_method
    async def get_post_reach(
        self, *, owner_id: str, post_ids: ty.Sequence, **kwargs
    ) -> 1:
        """
        Returns stats for a wall post.

        :param owner_id: post owner community id. Specify with "-" sign.
        :param post_ids: wall posts id
        """

    @api_method
    async def track_visitor(self, *, id: str, **kwargs) -> 1:
        """
        No description provided

        :param id: No description provided
        """


class Status(APIMethod):
    @api_method
    async def get(
        self,
        *,
        user_id: ty.Optional[int] = None,
        group_id: ty.Optional[int] = None,
        **kwargs
    ) -> 1:
        """
        Returns data required to show the status of a user or community.

        :param user_id: User ID or community ID. Use a negative value to designate a community ID.
        :param group_id: No description provided
        """

    @api_method
    async def set(
        self,
        *,
        text: ty.Optional[str] = None,
        group_id: ty.Optional[int] = None,
        **kwargs
    ) -> 1:
        """
        Sets a new status for the current user.

        :param text: Text of the new status.
        :param group_id: Identifier of a community to set a status in. If left blank the status is set to current user.
        """


class Storage(APIMethod):
    @api_method
    async def get(
        self,
        *,
        key: ty.Optional[str] = None,
        keys: ty.Optional[ty.List[str]] = None,
        user_id: ty.Optional[int] = None,
        **kwargs
    ) -> 1:
        """
        Returns a value of variable with the name set by key parameter.

        :param key: No description provided
        :param keys: No description provided
        :param user_id: No description provided
        """

    @api_method
    async def get_keys(
        self,
        *,
        user_id: ty.Optional[int] = None,
        offset: int = 0,
        count: int = 100,
        **kwargs
    ) -> 1:
        """
        Returns the names of all variables.

        :param user_id: user id, whose variables names are returned if they were requested with a server method.
        :param offset: No description provided
        :param count: amount of variable names the info needs to be collected from.
        """

    @api_method
    async def set(
        self,
        *,
        key: str,
        value: ty.Optional[str] = None,
        user_id: ty.Optional[int] = None,
        **kwargs
    ) -> 1:
        """
        Saves a value of variable with the name set by "key" parameter.

        :param key: No description provided
        :param value: No description provided
        :param user_id: No description provided
        """


class Store(APIMethod):
    @api_method
    async def add_stickers_to_favorite(
        self, *, sticker_ids: ty.Sequence, **kwargs
    ) -> 1:
        """
        Adds given sticker IDs to the list of user"s favorite stickers

        :param sticker_ids: Sticker IDs to be added
        """

    @api_method
    async def get_favorite_stickers(self, **kwargs) -> 1:
        """
        No description provided
        """

    @api_method
    async def get_products(
        self,
        *,
        type: ty.Optional[str] = None,
        merchant: ty.Optional[str] = None,
        section: ty.Optional[str] = None,
        product_ids: ty.Optional[ty.Sequence] = None,
        filters: ty.Optional[ty.List[str]] = None,
        extended: bool = 0,
        **kwargs
    ) -> 1:
        """
        No description provided

        :param type: No description provided
        :param merchant: No description provided
        :param section: No description provided
        :param product_ids: No description provided
        :param filters: No description provided
        :param extended: No description provided
        """

    @api_method
    async def get_stickers_keywords(
        self,
        *,
        stickers_ids: ty.Optional[ty.Sequence] = None,
        products_ids: ty.Optional[ty.Sequence] = None,
        aliases: bool = True,
        all_products: ty.Optional[bool] = None,
        need_stickers: bool = True,
        **kwargs
    ) -> 1:
        """
        No description provided

        :param stickers_ids: No description provided
        :param products_ids: No description provided
        :param aliases: No description provided
        :param all_products: No description provided
        :param need_stickers: No description provided
        """

    @api_method
    async def remove_stickers_from_favorite(
        self, *, sticker_ids: ty.Sequence, **kwargs
    ) -> 1:
        """
        Removes given sticker IDs from the list of user"s favorite stickers

        :param sticker_ids: Sticker IDs to be removed
        """


class Stories(APIMethod):
    @api_method
    async def ban_owner(self, *, owners_ids: ty.Sequence, **kwargs) -> 1:
        """
        Allows to hide stories from chosen sources from current user"s feed.

        :param owners_ids: List of sources IDs
        """

    @api_method
    async def delete(
        self,
        *,
        owner_id: ty.Optional[int] = None,
        story_id: ty.Optional[int] = None,
        stories: ty.Optional[ty.List[str]] = None,
        **kwargs
    ) -> 1:
        """
        Allows to delete story.

        :param owner_id: Story owner"s ID. Current user id is used by default.
        :param story_id: Story ID.
        :param stories: No description provided
        """

    @api_method
    async def get(
        self,
        *,
        owner_id: ty.Optional[int] = None,
        extended: bool = False,
        fields: ty.Optional[ty.Sequence] = None,
        **kwargs
    ) -> 1:
        """
        Returns stories available for current user.

        :param owner_id: Owner ID.
        :param extended: "1" — to return additional fields for users and communities. Default value is 0.
        :param fields: No description provided
        """

    @api_method
    async def get_banned(
        self,
        *,
        extended: ty.Optional[bool] = None,
        fields: ty.Optional[ty.Sequence] = None,
        **kwargs
    ) -> 1:
        """
        Returns list of sources hidden from current user"s feed.

        :param extended: "1" — to return additional fields for users and communities. Default value is 0.
        :param fields: Additional fields to return
        """

    @api_method
    async def get_by_id(
        self,
        *,
        stories: ty.List[str],
        extended: bool = False,
        fields: ty.Optional[ty.Sequence] = None,
        **kwargs
    ) -> 1:
        """
        Returns story by its ID.

        :param stories: Stories IDs separated by commas. Use format {owner_id}+"_"+{story_id}, for example, 12345_54331.
        :param extended: "1" — to return additional fields for users and communities. Default value is 0.
        :param fields: Additional fields to return
        """

    @api_method
    async def get_photo_upload_server(
        self,
        *,
        add_to_news: ty.Optional[bool] = None,
        user_ids: ty.Optional[ty.Sequence] = None,
        reply_to_story: ty.Optional[str] = None,
        link_text: ty.Optional[str] = None,
        link_url: ty.Optional[str] = None,
        group_id: ty.Optional[int] = None,
        clickable_stickers: ty.Optional[str] = None,
        **kwargs
    ) -> 1:
        """
        Returns URL for uploading a story with photo.

        :param add_to_news: 1 — to add the story to friend"s feed.
        :param user_ids: List of users IDs who can see the story.
        :param reply_to_story: ID of the story to reply with the current.
        :param link_text: Link text (for community"s stories only).
        :param link_url: Link URL. Internal links on https://vk.com only.
        :param group_id: ID of the community to upload the story (should be verified or with the "fire" icon).
        :param clickable_stickers: No description provided
        """

    @api_method
    async def get_replies(
        self,
        *,
        owner_id: int,
        story_id: int,
        access_key: ty.Optional[str] = None,
        extended: bool = False,
        fields: ty.Optional[ty.Sequence] = None,
        **kwargs
    ) -> 1:
        """
        Returns replies to the story.

        :param owner_id: Story owner ID.
        :param story_id: Story ID.
        :param access_key: Access key for the private object.
        :param extended: "1" — to return additional fields for users and communities. Default value is 0.
        :param fields: Additional fields to return
        """

    @api_method
    async def get_stats(self, *, owner_id: int, story_id: int, **kwargs) -> 1:
        """
        Returns stories available for current user.

        :param owner_id: Story owner ID.
        :param story_id: Story ID.
        """

    @api_method
    async def get_video_upload_server(
        self,
        *,
        add_to_news: ty.Optional[bool] = None,
        user_ids: ty.Optional[ty.Sequence] = None,
        reply_to_story: ty.Optional[str] = None,
        link_text: ty.Optional[str] = None,
        link_url: ty.Optional[str] = None,
        group_id: ty.Optional[int] = None,
        clickable_stickers: ty.Optional[str] = None,
        **kwargs
    ) -> 1:
        """
        Allows to receive URL for uploading story with video.

        :param add_to_news: 1 — to add the story to friend"s feed.
        :param user_ids: List of users IDs who can see the story.
        :param reply_to_story: ID of the story to reply with the current.
        :param link_text: Link text (for community"s stories only).
        :param link_url: Link URL. Internal links on https://vk.com only.
        :param group_id: ID of the community to upload the story (should be verified or with the "fire" icon).
        :param clickable_stickers: No description provided
        """

    @api_method
    async def get_viewers(
        self,
        *,
        owner_id: int,
        story_id: int,
        count: int = 100,
        offset: int = 0,
        extended: bool = 0,
        **kwargs
    ) -> 1:
        """
        Returns a list of story viewers.

        :param owner_id: Story owner ID.
        :param story_id: Story ID.
        :param count: Maximum number of results.
        :param offset: Offset needed to return a specific subset of results.
        :param extended: "1" — to return detailed information about photos
        """

    @api_method
    async def hide_all_replies(
        self, *, owner_id: int, group_id: ty.Optional[int] = None, **kwargs
    ) -> 1:
        """
        Hides all replies in the last 24 hours from the user to current user"s stories.

        :param owner_id: ID of the user whose replies should be hidden.
        :param group_id: No description provided
        """

    @api_method
    async def hide_reply(
        self, *, owner_id: int, story_id: int, **kwargs
    ) -> 1:
        """
        Hides the reply to the current user"s story.

        :param owner_id: ID of the user whose replies should be hidden.
        :param story_id: Story ID.
        """

    @api_method
    async def save(self, *, upload_results: ty.List[str], **kwargs) -> 1:
        """
        No description provided

        :param upload_results: No description provided
        """

    @api_method
    async def search(
        self,
        *,
        q: ty.Optional[str] = None,
        place_id: ty.Optional[int] = None,
        latitude: ty.Optional[float] = None,
        longitude: ty.Optional[float] = None,
        radius: ty.Optional[int] = None,
        mentioned_id: ty.Optional[int] = None,
        count: int = 20,
        extended: ty.Optional[bool] = None,
        fields: ty.Optional[ty.List[str]] = None,
        **kwargs
    ) -> 1:
        """
        No description provided

        :param q: No description provided
        :param place_id: No description provided
        :param latitude: No description provided
        :param longitude: No description provided
        :param radius: No description provided
        :param mentioned_id: No description provided
        :param count: No description provided
        :param extended: No description provided
        :param fields: No description provided
        """

    @api_method
    async def send_interaction(
        self,
        *,
        access_key: str,
        message: ty.Optional[str] = None,
        is_broadcast: bool = False,
        is_anonymous: bool = False,
        unseen_marker: bool = False,
        **kwargs
    ) -> 1:
        """
        No description provided

        :param access_key: No description provided
        :param message: No description provided
        :param is_broadcast: No description provided
        :param is_anonymous: No description provided
        :param unseen_marker: No description provided
        """

    @api_method
    async def unban_owner(self, *, owners_ids: ty.Sequence, **kwargs) -> 1:
        """
        Allows to show stories from hidden sources in current user"s feed.

        :param owners_ids: List of hidden sources to show stories from.
        """


class Streaming(APIMethod):
    @api_method
    async def get_server_url(self, **kwargs) -> 1:
        """
        Allows to receive data for the connection to Streaming API.
        """

    @api_method
    async def set_settings(
        self, *, monthly_tier: ty.Optional[str] = None, **kwargs
    ) -> 1:
        """
        No description provided

        :param monthly_tier: No description provided
        """


class Users(APIMethod):
    @api_method
    async def get(
        self,
        *,
        user_ids: ty.Optional[ty.List[ty.Union[str, int]]] = None,
        fields: ty.Optional[ty.Sequence] = None,
        name_case: ty.Optional[str] = None,
        **kwargs
    ) -> 1:
        """
        Returns detailed information on users.

        :param user_ids: User IDs or screen names ("screen_name"). By default, current user ID.
        :param fields: Profile fields to return. Sample values: "nickname", "screen_name", "sex", "bdate" (birthdate), "city", "country", "timezone", "photo", "photo_medium", "photo_big", "has_mobile", "contacts", "education", "online", "counters", "relation", "last_seen", "activity", "can_write_private_message", "can_see_all_posts", "can_post", "universities", "can_invite_to_chats"
        :param name_case: Case for declension of user name and surname: "nom" — nominative (default), "gen" — genitive , "dat" — dative, "acc" — accusative , "ins" — instrumental , "abl" — prepositional
        """

    @api_method
    async def get_followers(
        self,
        *,
        user_id: ty.Optional[int] = None,
        offset: ty.Optional[int] = None,
        count: int = 100,
        fields: ty.Optional[ty.Sequence] = None,
        name_case: ty.Optional[str] = None,
        **kwargs
    ) -> 1:
        """
        Returns a list of IDs of followers of the user in question, sorted by date added, most recent first.

        :param user_id: User ID.
        :param offset: Offset needed to return a specific subset of followers.
        :param count: Number of followers to return.
        :param fields: Profile fields to return. Sample values: "nickname", "screen_name", "sex", "bdate" (birthdate), "city", "country", "timezone", "photo", "photo_medium", "photo_big", "has_mobile", "rate", "contacts", "education", "online".
        :param name_case: Case for declension of user name and surname: "nom" — nominative (default), "gen" — genitive , "dat" — dative, "acc" — accusative , "ins" — instrumental , "abl" — prepositional
        """

    @api_method
    async def get_subscriptions(
        self,
        *,
        user_id: ty.Optional[int] = None,
        extended: ty.Optional[bool] = None,
        offset: ty.Optional[int] = None,
        count: int = 20,
        fields: ty.Optional[ty.Sequence] = None,
        **kwargs
    ) -> 1:
        """
        Returns a list of IDs of users and communities followed by the user.

        :param user_id: User ID.
        :param extended: "1" — to return a combined list of users and communities, "0" — to return separate lists of users and communities (default)
        :param offset: Offset needed to return a specific subset of subscriptions.
        :param count: Number of users and communities to return.
        :param fields: No description provided
        """

    @api_method
    async def report(
        self,
        *,
        user_id: int,
        type: str,
        comment: ty.Optional[str] = None,
        **kwargs
    ) -> 1:
        """
        Reports (submits a complain about) a user.

        :param user_id: ID of the user about whom a complaint is being made.
        :param type: Type of complaint: "porn" – pornography, "spam" – spamming, "insult" – abusive behavior, "advertisement" – disruptive advertisements
        :param comment: Comment describing the complaint.
        """

    @api_method
    async def search(
        self,
        *,
        q: ty.Optional[str] = None,
        sort: ty.Optional[int] = None,
        offset: ty.Optional[int] = None,
        count: int = 20,
        fields: ty.Optional[ty.Sequence] = None,
        city: ty.Optional[int] = None,
        country: ty.Optional[int] = None,
        hometown: ty.Optional[str] = None,
        university_country: ty.Optional[int] = None,
        university: ty.Optional[int] = None,
        university_year: ty.Optional[int] = None,
        university_faculty: ty.Optional[int] = None,
        university_chair: ty.Optional[int] = None,
        sex: ty.Optional[int] = None,
        status: ty.Optional[int] = None,
        age_from: ty.Optional[int] = None,
        age_to: ty.Optional[int] = None,
        birth_day: ty.Optional[int] = None,
        birth_month: ty.Optional[int] = None,
        birth_year: ty.Optional[int] = None,
        online: ty.Optional[bool] = None,
        has_photo: ty.Optional[bool] = None,
        school_country: ty.Optional[int] = None,
        school_city: ty.Optional[int] = None,
        school_class: ty.Optional[int] = None,
        school: ty.Optional[int] = None,
        school_year: ty.Optional[int] = None,
        religion: ty.Optional[str] = None,
        company: ty.Optional[str] = None,
        position: ty.Optional[str] = None,
        group_id: ty.Optional[int] = None,
        from_list: ty.Optional[ty.List[str]] = None,
        **kwargs
    ) -> 1:
        """
        Returns a list of users matching the search criteria.

        :param q: Search query string (e.g., "Vasya Babich").
        :param sort: Sort order: "1" — by date registered, "0" — by rating
        :param offset: Offset needed to return a specific subset of users.
        :param count: Number of users to return.
        :param fields: Profile fields to return. Sample values: "nickname", "screen_name", "sex", "bdate" (birthdate), "city", "country", "timezone", "photo", "photo_medium", "photo_big", "has_mobile", "rate", "contacts", "education", "online",
        :param city: City ID.
        :param country: Country ID.
        :param hometown: City name in a string.
        :param university_country: ID of the country where the user graduated.
        :param university: ID of the institution of higher education.
        :param university_year: Year of graduation from an institution of higher education.
        :param university_faculty: Faculty ID.
        :param university_chair: Chair ID.
        :param sex: "1" — female, "2" — male, "0" — any (default)
        :param status: Relationship status: "1" — Not married, "2" — In a relationship, "3" — Engaged, "4" — Married, "5" — It"s complicated, "6" — Actively searching, "7" — In love
        :param age_from: Minimum age.
        :param age_to: Maximum age.
        :param birth_day: Day of birth.
        :param birth_month: Month of birth.
        :param birth_year: Year of birth.
        :param online: "1" — online only, "0" — all users
        :param has_photo: "1" — with photo only, "0" — all users
        :param school_country: ID of the country where users finished school.
        :param school_city: ID of the city where users finished school.
        :param school_class: No description provided
        :param school: ID of the school.
        :param school_year: School graduation year.
        :param religion: Users" religious affiliation.
        :param company: Name of the company where users work.
        :param position: Job position.
        :param group_id: ID of a community to search in communities.
        :param from_list: No description provided
        """


class Utils(APIMethod):
    @api_method
    async def check_link(self, *, url: str, **kwargs) -> 1:
        """
        Checks whether a link is blocked in VK.

        :param url: Link to check (e.g., "http://google.com").
        """

    @api_method
    async def delete_from_last_shortened(self, *, key: str, **kwargs) -> 1:
        """
        Deletes shortened link from user"s list.

        :param key: Link key (characters after vk.cc/).
        """

    @api_method
    async def get_last_shortened_links(
        self, *, count: int = 10, offset: int = 0, **kwargs
    ) -> 1:
        """
        Returns a list of user"s shortened links.

        :param count: Number of links to return.
        :param offset: Offset needed to return a specific subset of links.
        """

    @api_method
    async def get_link_stats(
        self,
        *,
        key: str,
        source: str = "vk_cc",
        access_key: ty.Optional[str] = None,
        interval: str = "day",
        intervals_count: int = 1,
        extended: bool = False,
        **kwargs
    ) -> 1:
        """
        Returns stats data for shortened link.

        :param key: Link key (characters after vk.cc/).
        :param source: Source of scope
        :param access_key: Access key for private link stats.
        :param interval: Interval.
        :param intervals_count: Number of intervals to return.
        :param extended: 1 — to return extended stats data (sex, age, geo). 0 — to return views number only.
        """

    @api_method
    async def get_server_time(self, **kwargs) -> 1:
        """
        Returns the current time of the VK server.
        """

    @api_method
    async def get_short_link(
        self, *, url: str, private: bool = False, **kwargs
    ) -> 1:
        """
        Allows to receive a link shortened via vk.cc.

        :param url: URL to be shortened.
        :param private: 1 — private stats, 0 — public stats.
        """

    @api_method
    async def resolve_screen_name(self, *, screen_name: str, **kwargs) -> 1:
        """
        Detects a type of object (e.g., user, community, application) and its ID by screen name.

        :param screen_name: Screen name of the user, community (e.g., "apiclub," "andrew", or "rules_of_war"), or application.
        """


class Video(APIMethod):
    @api_method
    async def add(
        self,
        *,
        target_id: ty.Optional[int] = None,
        video_id: int,
        owner_id: int,
        **kwargs
    ) -> 1:
        """
        Adds a video to a user or community page.

        :param target_id: identifier of a user or community to add a video to. Use a negative value to designate a community ID.
        :param video_id: Video ID.
        :param owner_id: ID of the user or community that owns the video. Use a negative value to designate a community ID.
        """

    @api_method
    async def add_album(
        self,
        *,
        group_id: ty.Optional[int] = None,
        title: ty.Optional[str] = None,
        privacy: ty.Optional[
            ty.Sequence[tye.Literal["0", "1", "2", "3"]]
        ] = None,
        **kwargs
    ) -> 1:
        """
        Creates an empty album for videos.

        :param group_id: Community ID (if the album will be created in a community).
        :param title: Album title.
        :param privacy: new access permissions for the album. Possible values: , *"0" – all users,, *"1" – friends only,, *"2" – friends and friends of friends,, *"3" – "only me".
        """

    @api_method
    async def add_to_album(
        self,
        *,
        target_id: ty.Optional[int] = None,
        album_id: ty.Optional[int] = None,
        album_ids: ty.Optional[ty.Sequence] = None,
        owner_id: int,
        video_id: int,
        **kwargs
    ) -> 1:
        """
        No description provided

        :param target_id: No description provided
        :param album_id: No description provided
        :param album_ids: No description provided
        :param owner_id: No description provided
        :param video_id: No description provided
        """

    @api_method
    async def create_comment(
        self,
        *,
        owner_id: ty.Optional[int] = None,
        video_id: int,
        message: ty.Optional[str] = None,
        attachments: ty.Optional[ty.List[str]] = None,
        from_group: ty.Optional[bool] = None,
        reply_to_comment: ty.Optional[int] = None,
        sticker_id: ty.Optional[int] = None,
        guid: ty.Optional[str] = None,
        **kwargs
    ) -> 1:
        """
        Adds a new comment on a video.

        :param owner_id: ID of the user or community that owns the video.
        :param video_id: Video ID.
        :param message: New comment text.
        :param attachments: List of objects attached to the comment, in the following format: "<owner_id>_<media_id>,<owner_id>_<media_id>", "" — Type of media attachment: "photo" — photo, "video" — video, "audio" — audio, "doc" — document, "<owner_id>" — ID of the media attachment owner. "<media_id>" — Media attachment ID. Example: "photo100172_166443618,photo66748_265827614"
        :param from_group: "1" — to post the comment from a community name (only if "owner_id"<0)
        :param reply_to_comment: No description provided
        :param sticker_id: No description provided
        :param guid: No description provided
        """

    @api_method
    async def delete(
        self,
        *,
        video_id: int,
        owner_id: ty.Optional[int] = None,
        target_id: ty.Optional[int] = None,
        **kwargs
    ) -> 1:
        """
        Deletes a video from a user or community page.

        :param video_id: Video ID.
        :param owner_id: ID of the user or community that owns the video.
        :param target_id: No description provided
        """

    @api_method
    async def delete_album(
        self, *, group_id: ty.Optional[int] = None, album_id: int, **kwargs
    ) -> 1:
        """
        Deletes a video album.

        :param group_id: Community ID (if the album is owned by a community).
        :param album_id: Album ID.
        """

    @api_method
    async def delete_comment(
        self, *, owner_id: ty.Optional[int] = None, comment_id: int, **kwargs
    ) -> 1:
        """
        Deletes a comment on a video.

        :param owner_id: ID of the user or community that owns the video.
        :param comment_id: ID of the comment to be deleted.
        """

    @api_method
    async def edit(
        self,
        *,
        owner_id: ty.Optional[int] = None,
        video_id: int,
        name: ty.Optional[str] = None,
        desc: ty.Optional[str] = None,
        privacy_view: ty.Optional[ty.List[str]] = None,
        privacy_comment: ty.Optional[ty.List[str]] = None,
        no_comments: ty.Optional[bool] = None,
        repeat: ty.Optional[bool] = None,
        **kwargs
    ) -> 1:
        """
        Edits information about a video on a user or community page.

        :param owner_id: ID of the user or community that owns the video.
        :param video_id: Video ID.
        :param name: New video title.
        :param desc: New video description.
        :param privacy_view: Privacy settings in a [vk.com/dev/privacy_setting|special format]. Privacy setting is available for videos uploaded to own profile by user.
        :param privacy_comment: Privacy settings for comments in a [vk.com/dev/privacy_setting|special format].
        :param no_comments: Disable comments for the group video.
        :param repeat: "1" — to repeat the playback of the video, "0" — to play the video once,
        """

    @api_method
    async def edit_album(
        self,
        *,
        group_id: ty.Optional[int] = None,
        album_id: int,
        title: str,
        privacy: ty.Optional[
            ty.Sequence[tye.Literal["0", "1", "2", "3"]]
        ] = None,
        **kwargs
    ) -> 1:
        """
        Edits the title of a video album.

        :param group_id: Community ID (if the album edited is owned by a community).
        :param album_id: Album ID.
        :param title: New album title.
        :param privacy: new access permissions for the album. Possible values: , *"0" – all users,, *"1" – friends only,, *"2" – friends and friends of friends,, *"3" – "only me".
        """

    @api_method
    async def edit_comment(
        self,
        *,
        owner_id: ty.Optional[int] = None,
        comment_id: int,
        message: ty.Optional[str] = None,
        attachments: ty.Optional[ty.List[str]] = None,
        **kwargs
    ) -> 1:
        """
        Edits the text of a comment on a video.

        :param owner_id: ID of the user or community that owns the video.
        :param comment_id: Comment ID.
        :param message: New comment text.
        :param attachments: List of objects attached to the comment, in the following format: "<owner_id>_<media_id>,<owner_id>_<media_id>", "" — Type of media attachment: "photo" — photo, "video" — video, "audio" — audio, "doc" — document, "<owner_id>" — ID of the media attachment owner. "<media_id>" — Media attachment ID. Example: "photo100172_166443618,photo66748_265827614"
        """

    @api_method
    async def get(
        self,
        *,
        owner_id: ty.Optional[int] = None,
        videos: ty.Optional[ty.List[str]] = None,
        album_id: ty.Optional[int] = None,
        count: int = 100,
        offset: ty.Optional[int] = None,
        extended: ty.Optional[bool] = None,
        **kwargs
    ) -> 1:
        """
        Returns detailed information about videos.

        :param owner_id: ID of the user or community that owns the video(s).
        :param videos: Video IDs, in the following format: "<owner_id>_<media_id>,<owner_id>_<media_id>", Use a negative value to designate a community ID. Example: "-4363_136089719,13245770_137352259"
        :param album_id: ID of the album containing the video(s).
        :param count: Number of videos to return.
        :param offset: Offset needed to return a specific subset of videos.
        :param extended: "1" — to return an extended response with additional fields
        """

    @api_method
    async def get_album_by_id(
        self, *, owner_id: ty.Optional[int] = None, album_id: int, **kwargs
    ) -> 1:
        """
        Returns video album info

        :param owner_id: identifier of a user or community to add a video to. Use a negative value to designate a community ID.
        :param album_id: Album ID.
        """

    @api_method
    async def get_albums(
        self,
        *,
        owner_id: ty.Optional[int] = None,
        offset: ty.Optional[int] = None,
        count: int = 50,
        extended: ty.Optional[bool] = None,
        need_system: bool = 0,
        **kwargs
    ) -> 1:
        """
        Returns a list of video albums owned by a user or community.

        :param owner_id: ID of the user or community that owns the video album(s).
        :param offset: Offset needed to return a specific subset of video albums.
        :param count: Number of video albums to return.
        :param extended: "1" — to return additional information about album privacy settings for the current user
        :param need_system: No description provided
        """

    @api_method
    async def get_albums_by_video(
        self,
        *,
        target_id: ty.Optional[int] = None,
        owner_id: int,
        video_id: int,
        extended: bool = 0,
        **kwargs
    ) -> 1:
        """
        No description provided

        :param target_id: No description provided
        :param owner_id: No description provided
        :param video_id: No description provided
        :param extended: No description provided
        """

    @api_method
    async def get_comments(
        self,
        *,
        owner_id: ty.Optional[int] = None,
        video_id: int,
        need_likes: ty.Optional[bool] = None,
        start_comment_id: ty.Optional[int] = None,
        offset: ty.Optional[int] = None,
        count: int = 20,
        sort: ty.Optional[str] = None,
        extended: ty.Optional[bool] = None,
        fields: ty.Optional[ty.List[str]] = None,
        **kwargs
    ) -> 1:
        """
        Returns a list of comments on a video.

        :param owner_id: ID of the user or community that owns the video.
        :param video_id: Video ID.
        :param need_likes: "1" — to return an additional "likes" field
        :param start_comment_id: No description provided
        :param offset: Offset needed to return a specific subset of comments.
        :param count: Number of comments to return.
        :param sort: Sort order: "asc" — oldest comment first, "desc" — newest comment first
        :param extended: No description provided
        :param fields: No description provided
        """

    @api_method
    async def remove_from_album(
        self,
        *,
        target_id: ty.Optional[int] = None,
        album_id: ty.Optional[int] = None,
        album_ids: ty.Optional[ty.Sequence] = None,
        owner_id: int,
        video_id: int,
        **kwargs
    ) -> 1:
        """
        No description provided

        :param target_id: No description provided
        :param album_id: No description provided
        :param album_ids: No description provided
        :param owner_id: No description provided
        :param video_id: No description provided
        """

    @api_method
    async def reorder_albums(
        self,
        *,
        owner_id: ty.Optional[int] = None,
        album_id: int,
        before: ty.Optional[int] = None,
        after: ty.Optional[int] = None,
        **kwargs
    ) -> 1:
        """
        Reorders the album in the list of user video albums.

        :param owner_id: ID of the user or community that owns the albums..
        :param album_id: Album ID.
        :param before: ID of the album before which the album in question shall be placed.
        :param after: ID of the album after which the album in question shall be placed.
        """

    @api_method
    async def reorder_videos(
        self,
        *,
        target_id: ty.Optional[int] = None,
        album_id: ty.Optional[int] = None,
        owner_id: int,
        video_id: int,
        before_owner_id: ty.Optional[int] = None,
        before_video_id: ty.Optional[int] = None,
        after_owner_id: ty.Optional[int] = None,
        after_video_id: ty.Optional[int] = None,
        **kwargs
    ) -> 1:
        """
        Reorders the video in the video album.

        :param target_id: ID of the user or community that owns the album with videos.
        :param album_id: ID of the video album.
        :param owner_id: ID of the user or community that owns the video.
        :param video_id: ID of the video.
        :param before_owner_id: ID of the user or community that owns the video before which the video in question shall be placed.
        :param before_video_id: ID of the video before which the video in question shall be placed.
        :param after_owner_id: ID of the user or community that owns the video after which the photo in question shall be placed.
        :param after_video_id: ID of the video after which the photo in question shall be placed.
        """

    @api_method
    async def report(
        self,
        *,
        owner_id: int,
        video_id: int,
        reason: ty.Optional[int] = None,
        comment: ty.Optional[str] = None,
        search_query: ty.Optional[str] = None,
        **kwargs
    ) -> 1:
        """
        Reports (submits a complaint about) a video.

        :param owner_id: ID of the user or community that owns the video.
        :param video_id: Video ID.
        :param reason: Reason for the complaint: "0" – spam, "1" – child pornography, "2" – extremism, "3" – violence, "4" – drug propaganda, "5" – adult material, "6" – insult, abuse
        :param comment: Comment describing the complaint.
        :param search_query: (If the video was found in search results.) Search query string.
        """

    @api_method
    async def report_comment(
        self,
        *,
        owner_id: int,
        comment_id: int,
        reason: ty.Optional[int] = None,
        **kwargs
    ) -> 1:
        """
        Reports (submits a complaint about) a comment on a video.

        :param owner_id: ID of the user or community that owns the video.
        :param comment_id: ID of the comment being reported.
        :param reason: Reason for the complaint: , 0 – spam , 1 – child pornography , 2 – extremism , 3 – violence , 4 – drug propaganda , 5 – adult material , 6 – insult, abuse
        """

    @api_method
    async def restore(
        self, *, video_id: int, owner_id: ty.Optional[int] = None, **kwargs
    ) -> 1:
        """
        Restores a previously deleted video.

        :param video_id: Video ID.
        :param owner_id: ID of the user or community that owns the video.
        """

    @api_method
    async def restore_comment(
        self, *, owner_id: ty.Optional[int] = None, comment_id: int, **kwargs
    ) -> 1:
        """
        Restores a previously deleted comment on a video.

        :param owner_id: ID of the user or community that owns the video.
        :param comment_id: ID of the deleted comment.
        """

    @api_method
    async def save(
        self,
        *,
        name: ty.Optional[str] = None,
        description: ty.Optional[str] = None,
        is_private: ty.Optional[bool] = None,
        wallpost: ty.Optional[bool] = None,
        link: ty.Optional[str] = None,
        group_id: ty.Optional[int] = None,
        album_id: ty.Optional[int] = None,
        privacy_view: ty.Optional[ty.List[str]] = None,
        privacy_comment: ty.Optional[ty.List[str]] = None,
        no_comments: ty.Optional[bool] = None,
        repeat: ty.Optional[bool] = None,
        compression: ty.Optional[bool] = None,
        **kwargs
    ) -> 1:
        """
        Returns a server address (required for upload) and video data.

        :param name: Name of the video.
        :param description: Description of the video.
        :param is_private: "1" — to designate the video as private (send it via a private message), the video will not appear on the user"s video list and will not be available by ID for other users, "0" — not to designate the video as private
        :param wallpost: "1" — to post the saved video on a user"s wall, "0" — not to post the saved video on a user"s wall
        :param link: URL for embedding the video from an external website.
        :param group_id: ID of the community in which the video will be saved. By default, the current user"s page.
        :param album_id: ID of the album to which the saved video will be added.
        :param privacy_view: No description provided
        :param privacy_comment: No description provided
        :param no_comments: No description provided
        :param repeat: "1" — to repeat the playback of the video, "0" — to play the video once,
        :param compression: No description provided
        """

    @api_method
    async def search(
        self,
        *,
        q: str,
        sort: ty.Optional[int] = None,
        hd: ty.Optional[int] = None,
        adult: ty.Optional[bool] = None,
        filters: ty.Optional[
            ty.Sequence[tye.Literal["youtube", "vimeo", "short", "long"]]
        ] = None,
        search_own: ty.Optional[bool] = None,
        offset: ty.Optional[int] = None,
        longer: ty.Optional[int] = None,
        shorter: ty.Optional[int] = None,
        count: int = 20,
        extended: bool = 0,
        **kwargs
    ) -> 1:
        """
        Returns a list of videos under the set search criterion.

        :param q: Search query string (e.g., "The Beatles").
        :param sort: Sort order: "1" — by duration, "2" — by relevance, "0" — by date added
        :param hd: If not null, only searches for high-definition videos.
        :param adult: "1" — to disable the Safe Search filter, "0" — to enable the Safe Search filter
        :param filters: Filters to apply: "youtube" — return YouTube videos only, "vimeo" — return Vimeo videos only, "short" — return short videos only, "long" — return long videos only
        :param search_own: No description provided
        :param offset: Offset needed to return a specific subset of videos.
        :param longer: No description provided
        :param shorter: No description provided
        :param count: Number of videos to return.
        :param extended: No description provided
        """


class Wall(APIMethod):
    @api_method
    async def check_copyright_link(self, *, link: str, **kwargs) -> 1:
        """
        No description provided

        :param link: No description provided
        """

    @api_method
    async def close_comments(
        self, *, owner_id: int, post_id: int, **kwargs
    ) -> 1:
        """
        No description provided

        :param owner_id: No description provided
        :param post_id: No description provided
        """

    @api_method
    async def create_comment(
        self,
        *,
        owner_id: ty.Optional[int] = None,
        post_id: int,
        from_group: ty.Optional[int] = None,
        message: ty.Optional[str] = None,
        reply_to_comment: ty.Optional[int] = None,
        attachments: ty.Optional[ty.List[str]] = None,
        sticker_id: ty.Optional[int] = None,
        guid: ty.Optional[str] = None,
        **kwargs
    ) -> 1:
        """
        Adds a comment to a post on a user wall or community wall.

        :param owner_id: User ID or community ID. Use a negative value to designate a community ID.
        :param post_id: Post ID.
        :param from_group: Group ID.
        :param message: (Required if "attachments" is not set.) Text of the comment.
        :param reply_to_comment: ID of comment to reply.
        :param attachments: (Required if "message" is not set.) List of media objects attached to the comment, in the following format: "<owner_id>_<media_id>,<owner_id>_<media_id>", "" — Type of media ojbect: "photo" — photo, "video" — video, "audio" — audio, "doc" — document, "<owner_id>" — ID of the media owner. "<media_id>" — Media ID. For example: "photo100172_166443618,photo66748_265827614"
        :param sticker_id: Sticker ID.
        :param guid: Unique identifier to avoid repeated comments.
        """

    @api_method
    async def delete(
        self,
        *,
        owner_id: ty.Optional[int] = None,
        post_id: ty.Optional[int] = None,
        **kwargs
    ) -> 1:
        """
        Deletes a post from a user wall or community wall.

        :param owner_id: User ID or community ID. Use a negative value to designate a community ID.
        :param post_id: ID of the post to be deleted.
        """

    @api_method
    async def delete_comment(
        self, *, owner_id: ty.Optional[int] = None, comment_id: int, **kwargs
    ) -> 1:
        """
        Deletes a comment on a post on a user wall or community wall.

        :param owner_id: User ID or community ID. Use a negative value to designate a community ID.
        :param comment_id: Comment ID.
        """

    @api_method
    async def edit(
        self,
        *,
        owner_id: ty.Optional[int] = None,
        post_id: int,
        friends_only: ty.Optional[bool] = None,
        message: ty.Optional[str] = None,
        attachments: ty.Optional[ty.List[str]] = None,
        services: ty.Optional[str] = None,
        signed: ty.Optional[bool] = None,
        publish_date: ty.Optional[int] = None,
        lat: ty.Optional[float] = None,
        long: ty.Optional[float] = None,
        place_id: ty.Optional[int] = None,
        mark_as_ads: ty.Optional[bool] = None,
        close_comments: ty.Optional[bool] = None,
        donut_paid_duration: ty.Optional[int] = None,
        poster_bkg_id: ty.Optional[int] = None,
        poster_bkg_owner_id: ty.Optional[int] = None,
        poster_bkg_access_hash: ty.Optional[str] = None,
        copyright: ty.Optional[str] = None,
        **kwargs
    ) -> 1:
        """
        Edits a post on a user wall or community wall.

        :param owner_id: User ID or community ID. Use a negative value to designate a community ID.
        :param post_id: No description provided
        :param friends_only: No description provided
        :param message: (Required if "attachments" is not set.) Text of the post.
        :param attachments: (Required if "message" is not set.) List of objects attached to the post, in the following format: "<owner_id>_<media_id>,<owner_id>_<media_id>", "" — Type of media attachment: "photo" — photo, "video" — video, "audio" — audio, "doc" — document, "<owner_id>" — ID of the media application owner. "<media_id>" — Media application ID. Example: "photo100172_166443618,photo66748_265827614", May contain a link to an external page to include in the post. Example: "photo66748_265827614,http://habrahabr.ru", "NOTE: If more than one link is being attached, an error is thrown."
        :param services: No description provided
        :param signed: No description provided
        :param publish_date: No description provided
        :param lat: No description provided
        :param long: No description provided
        :param place_id: No description provided
        :param mark_as_ads: No description provided
        :param close_comments: No description provided
        :param donut_paid_duration: No description provided
        :param poster_bkg_id: No description provided
        :param poster_bkg_owner_id: No description provided
        :param poster_bkg_access_hash: No description provided
        :param copyright: No description provided
        """

    @api_method
    async def edit_ads_stealth(
        self,
        *,
        owner_id: ty.Optional[int] = None,
        post_id: int,
        message: ty.Optional[str] = None,
        attachments: ty.Optional[ty.List[str]] = None,
        signed: ty.Optional[bool] = None,
        lat: ty.Optional[float] = None,
        long: ty.Optional[float] = None,
        place_id: ty.Optional[int] = None,
        link_button: ty.Optional[str] = None,
        link_title: ty.Optional[str] = None,
        link_image: ty.Optional[str] = None,
        link_video: ty.Optional[str] = None,
        **kwargs
    ) -> 1:
        """
        Allows to edit hidden post.

        :param owner_id: User ID or community ID. Use a negative value to designate a community ID.
        :param post_id: Post ID. Used for publishing of scheduled and suggested posts.
        :param message: (Required if "attachments" is not set.) Text of the post.
        :param attachments: (Required if "message" is not set.) List of objects attached to the post, in the following format: "<owner_id>_<media_id>,<owner_id>_<media_id>", "" — Type of media attachment: "photo" — photo, "video" — video, "audio" — audio, "doc" — document, "page" — wiki-page, "note" — note, "poll" — poll, "album" — photo album, "<owner_id>" — ID of the media application owner. "<media_id>" — Media application ID. Example: "photo100172_166443618,photo66748_265827614", May contain a link to an external page to include in the post. Example: "photo66748_265827614,http://habrahabr.ru", "NOTE: If more than one link is being attached, an error will be thrown."
        :param signed: Only for posts in communities with "from_group" set to "1": "1" — post will be signed with the name of the posting user, "0" — post will not be signed (default)
        :param lat: Geographical latitude of a check-in, in degrees (from -90 to 90).
        :param long: Geographical longitude of a check-in, in degrees (from -180 to 180).
        :param place_id: ID of the location where the user was tagged.
        :param link_button: Link button ID
        :param link_title: Link title
        :param link_image: Link image url
        :param link_video: Link video ID in format "<owner_id>_<media_id>"
        """

    @api_method
    async def edit_comment(
        self,
        *,
        owner_id: ty.Optional[int] = None,
        comment_id: int,
        message: ty.Optional[str] = None,
        attachments: ty.Optional[ty.List[str]] = None,
        **kwargs
    ) -> 1:
        """
        Edits a comment on a user wall or community wall.

        :param owner_id: User ID or community ID. Use a negative value to designate a community ID.
        :param comment_id: Comment ID.
        :param message: New comment text.
        :param attachments: List of objects attached to the comment, in the following format: , "<owner_id>_<media_id>,<owner_id>_<media_id>", "" — Type of media attachment: "photo" — photo, "video" — video, "audio" — audio, "doc" — document, "<owner_id>" — ID of the media attachment owner. "<media_id>" — Media attachment ID. For example: "photo100172_166443618,photo66748_265827614"
        """

    @api_method
    async def get(
        self,
        *,
        owner_id: ty.Optional[int] = None,
        domain: ty.Optional[str] = None,
        offset: ty.Optional[int] = None,
        count: ty.Optional[int] = None,
        filter: ty.Optional[str] = None,
        extended: ty.Optional[bool] = None,
        fields: ty.Optional[ty.Sequence] = None,
        **kwargs
    ) -> 1:
        """
        Returns a list of posts on a user wall or community wall.

        :param owner_id: ID of the user or community that owns the wall. By default, current user ID. Use a negative value to designate a community ID.
        :param domain: User or community short address.
        :param offset: Offset needed to return a specific subset of posts.
        :param count: Number of posts to return (maximum 100).
        :param filter: Filter to apply: "owner" — posts by the wall owner, "others" — posts by someone else, "all" — posts by the wall owner and others (default), "postponed" — timed posts (only available for calls with an "access_token"), "suggests" — suggested posts on a community wall
        :param extended: "1" — to return "wall", "profiles", and "groups" fields, "0" — to return no additional fields (default)
        :param fields: No description provided
        """

    @api_method
    async def get_by_id(
        self,
        *,
        posts: ty.List[str],
        extended: ty.Optional[bool] = None,
        copy_history_depth: int = 2,
        fields: ty.Optional[ty.Sequence] = None,
        **kwargs
    ) -> 1:
        """
        Returns a list of posts from user or community walls by their IDs.

        :param posts: User or community IDs and post IDs, separated by underscores. Use a negative value to designate a community ID. Example: "93388_21539,93388_20904,2943_4276,-1_1"
        :param extended: "1" — to return user and community objects needed to display posts, "0" — no additional fields are returned (default)
        :param copy_history_depth: Sets the number of parent elements to include in the array "copy_history" that is returned if the post is a repost from another wall.
        :param fields: No description provided
        """

    @api_method
    async def get_comment(
        self,
        *,
        owner_id: ty.Optional[int] = None,
        comment_id: int,
        extended: ty.Optional[bool] = None,
        fields: ty.Optional[ty.Sequence] = None,
        **kwargs
    ) -> 1:
        """
        Returns a comment on a post on a user wall or community wall.

        :param owner_id: User ID or community ID. Use a negative value to designate a community ID.
        :param comment_id: Comment ID.
        :param extended: No description provided
        :param fields: No description provided
        """

    @api_method
    async def get_comments(
        self,
        *,
        owner_id: ty.Optional[int] = None,
        post_id: ty.Optional[int] = None,
        need_likes: ty.Optional[bool] = None,
        start_comment_id: ty.Optional[int] = None,
        offset: ty.Optional[int] = None,
        count: ty.Optional[int] = None,
        sort: ty.Optional[str] = None,
        preview_length: ty.Optional[int] = None,
        extended: ty.Optional[bool] = None,
        fields: ty.Optional[ty.Sequence] = None,
        comment_id: ty.Optional[int] = None,
        thread_items_count: int = 0,
        **kwargs
    ) -> 1:
        """
        Returns a list of comments on a post on a user wall or community wall.

        :param owner_id: User ID or community ID. Use a negative value to designate a community ID.
        :param post_id: Post ID.
        :param need_likes: "1" — to return the "likes" field, "0" — not to return the "likes" field (default)
        :param start_comment_id: No description provided
        :param offset: Offset needed to return a specific subset of comments.
        :param count: Number of comments to return (maximum 100).
        :param sort: Sort order: "asc" — chronological, "desc" — reverse chronological
        :param preview_length: Number of characters at which to truncate comments when previewed. By default, "90". Specify "0" if you do not want to truncate comments.
        :param extended: No description provided
        :param fields: No description provided
        :param comment_id: Comment ID.
        :param thread_items_count: Count items in threads.
        """

    @api_method
    async def get_reposts(
        self,
        *,
        owner_id: ty.Optional[int] = None,
        post_id: ty.Optional[int] = None,
        offset: ty.Optional[int] = None,
        count: int = 20,
        **kwargs
    ) -> 1:
        """
        Returns information about reposts of a post on user wall or community wall.

        :param owner_id: User ID or community ID. By default, current user ID. Use a negative value to designate a community ID.
        :param post_id: Post ID.
        :param offset: Offset needed to return a specific subset of reposts.
        :param count: Number of reposts to return.
        """

    @api_method
    async def open_comments(
        self, *, owner_id: int, post_id: int, **kwargs
    ) -> 1:
        """
        No description provided

        :param owner_id: No description provided
        :param post_id: No description provided
        """

    @api_method
    async def pin(
        self, *, owner_id: ty.Optional[int] = None, post_id: int, **kwargs
    ) -> 1:
        """
        Pins the post on wall.

        :param owner_id: ID of the user or community that owns the wall. By default, current user ID. Use a negative value to designate a community ID.
        :param post_id: Post ID.
        """

    @api_method
    async def post(
        self,
        *,
        owner_id: ty.Optional[int] = None,
        friends_only: ty.Optional[bool] = None,
        from_group: ty.Optional[bool] = None,
        message: ty.Optional[str] = None,
        attachments: ty.Optional[ty.List[str]] = None,
        services: ty.Optional[str] = None,
        signed: ty.Optional[bool] = None,
        publish_date: ty.Optional[int] = None,
        lat: ty.Optional[float] = None,
        long: ty.Optional[float] = None,
        place_id: ty.Optional[int] = None,
        post_id: ty.Optional[int] = None,
        guid: ty.Optional[str] = None,
        mark_as_ads: bool = False,
        close_comments: ty.Optional[bool] = None,
        donut_paid_duration: ty.Optional[int] = None,
        mute_notifications: ty.Optional[bool] = None,
        copyright: ty.Optional[str] = None,
        **kwargs
    ) -> 1:
        """
        Adds a new post on a user wall or community wall. Can also be used to publish suggested or scheduled posts.

        :param owner_id: User ID or community ID. Use a negative value to designate a community ID.
        :param friends_only: "1" — post will be available to friends only, "0" — post will be available to all users (default)
        :param from_group: For a community: "1" — post will be published by the community, "0" — post will be published by the user (default)
        :param message: (Required if "attachments" is not set.) Text of the post.
        :param attachments: (Required if "message" is not set.) List of objects attached to the post, in the following format: "<owner_id>_<media_id>,<owner_id>_<media_id>", "" — Type of media attachment: "photo" — photo, "video" — video, "audio" — audio, "doc" — document, "page" — wiki-page, "note" — note, "poll" — poll, "album" — photo album, "<owner_id>" — ID of the media application owner. "<media_id>" — Media application ID. Example: "photo100172_166443618,photo66748_265827614", May contain a link to an external page to include in the post. Example: "photo66748_265827614,http://habrahabr.ru", "NOTE: If more than one link is being attached, an error will be thrown."
        :param services: List of services or websites the update will be exported to, if the user has so requested. Sample values: "twitter", "facebook".
        :param signed: Only for posts in communities with "from_group" set to "1": "1" — post will be signed with the name of the posting user, "0" — post will not be signed (default)
        :param publish_date: Publication date (in Unix time). If used, posting will be delayed until the set time.
        :param lat: Geographical latitude of a check-in, in degrees (from -90 to 90).
        :param long: Geographical longitude of a check-in, in degrees (from -180 to 180).
        :param place_id: ID of the location where the user was tagged.
        :param post_id: Post ID. Used for publishing of scheduled and suggested posts.
        :param guid: No description provided
        :param mark_as_ads: No description provided
        :param close_comments: No description provided
        :param donut_paid_duration: No description provided
        :param mute_notifications: No description provided
        :param copyright: No description provided
        """

    @api_method
    async def post_ads_stealth(
        self,
        *,
        owner_id: int,
        message: ty.Optional[str] = None,
        attachments: ty.Optional[ty.List[str]] = None,
        signed: ty.Optional[bool] = None,
        lat: ty.Optional[float] = None,
        long: ty.Optional[float] = None,
        place_id: ty.Optional[int] = None,
        guid: ty.Optional[str] = None,
        link_button: ty.Optional[str] = None,
        link_title: ty.Optional[str] = None,
        link_image: ty.Optional[str] = None,
        link_video: ty.Optional[str] = None,
        **kwargs
    ) -> 1:
        """
        Allows to create hidden post which will not be shown on the community"s wall and can be used for creating an ad with type "Community post".

        :param owner_id: User ID or community ID. Use a negative value to designate a community ID.
        :param message: (Required if "attachments" is not set.) Text of the post.
        :param attachments: (Required if "message" is not set.) List of objects attached to the post, in the following format: "<owner_id>_<media_id>,<owner_id>_<media_id>", "" — Type of media attachment: "photo" — photo, "video" — video, "audio" — audio, "doc" — document, "page" — wiki-page, "note" — note, "poll" — poll, "album" — photo album, "<owner_id>" — ID of the media application owner. "<media_id>" — Media application ID. Example: "photo100172_166443618,photo66748_265827614", May contain a link to an external page to include in the post. Example: "photo66748_265827614,http://habrahabr.ru", "NOTE: If more than one link is being attached, an error will be thrown."
        :param signed: Only for posts in communities with "from_group" set to "1": "1" — post will be signed with the name of the posting user, "0" — post will not be signed (default)
        :param lat: Geographical latitude of a check-in, in degrees (from -90 to 90).
        :param long: Geographical longitude of a check-in, in degrees (from -180 to 180).
        :param place_id: ID of the location where the user was tagged.
        :param guid: Unique identifier to avoid duplication the same post.
        :param link_button: Link button ID
        :param link_title: Link title
        :param link_image: Link image url
        :param link_video: Link video ID in format "<owner_id>_<media_id>"
        """

    @api_method
    async def report_comment(
        self,
        *,
        owner_id: int,
        comment_id: int,
        reason: ty.Optional[int] = None,
        **kwargs
    ) -> 1:
        """
        Reports (submits a complaint about) a comment on a post on a user wall or community wall.

        :param owner_id: ID of the user or community that owns the wall.
        :param comment_id: Comment ID.
        :param reason: Reason for the complaint: "0" – spam, "1" – child pornography, "2" – extremism, "3" – violence, "4" – drug propaganda, "5" – adult material, "6" – insult, abuse
        """

    @api_method
    async def report_post(
        self,
        *,
        owner_id: int,
        post_id: int,
        reason: ty.Optional[int] = None,
        **kwargs
    ) -> 1:
        """
        Reports (submits a complaint about) a post on a user wall or community wall.

        :param owner_id: ID of the user or community that owns the wall.
        :param post_id: Post ID.
        :param reason: Reason for the complaint: "0" – spam, "1" – child pornography, "2" – extremism, "3" – violence, "4" – drug propaganda, "5" – adult material, "6" – insult, abuse
        """

    @api_method
    async def repost(
        self,
        *,
        object: str,
        message: ty.Optional[str] = None,
        group_id: ty.Optional[int] = None,
        mark_as_ads: bool = False,
        mute_notifications: ty.Optional[bool] = None,
        **kwargs
    ) -> 1:
        """
        Reposts (copies) an object to a user wall or community wall.

        :param object: ID of the object to be reposted on the wall. Example: "wall66748_3675"
        :param message: Comment to be added along with the reposted object.
        :param group_id: Target community ID when reposting to a community.
        :param mark_as_ads: No description provided
        :param mute_notifications: No description provided
        """

    @api_method
    async def restore(
        self,
        *,
        owner_id: ty.Optional[int] = None,
        post_id: ty.Optional[int] = None,
        **kwargs
    ) -> 1:
        """
        Restores a post deleted from a user wall or community wall.

        :param owner_id: User ID or community ID from whose wall the post was deleted. Use a negative value to designate a community ID.
        :param post_id: ID of the post to be restored.
        """

    @api_method
    async def restore_comment(
        self, *, owner_id: ty.Optional[int] = None, comment_id: int, **kwargs
    ) -> 1:
        """
        Restores a comment deleted from a user wall or community wall.

        :param owner_id: User ID or community ID. Use a negative value to designate a community ID.
        :param comment_id: Comment ID.
        """

    @api_method
    async def search(
        self,
        *,
        owner_id: ty.Optional[int] = None,
        domain: ty.Optional[str] = None,
        query: ty.Optional[str] = None,
        owners_only: ty.Optional[bool] = None,
        count: int = 20,
        offset: int = 0,
        extended: ty.Optional[bool] = None,
        fields: ty.Optional[ty.Sequence] = None,
        **kwargs
    ) -> 1:
        """
        Allows to search posts on user or community walls.

        :param owner_id: user or community id. "Remember that for a community "owner_id" must be negative."
        :param domain: user or community screen name.
        :param query: search query string.
        :param owners_only: "1" – returns only page owner"s posts.
        :param count: count of posts to return.
        :param offset: Offset needed to return a specific subset of posts.
        :param extended: show extended post info.
        :param fields: No description provided
        """

    @api_method
    async def unpin(
        self, *, owner_id: ty.Optional[int] = None, post_id: int, **kwargs
    ) -> 1:
        """
        Unpins the post on wall.

        :param owner_id: ID of the user or community that owns the wall. By default, current user ID. Use a negative value to designate a community ID.
        :param post_id: Post ID.
        """


class Widgets(APIMethod):
    @api_method
    async def get_comments(
        self,
        *,
        widget_api_id: ty.Optional[int] = None,
        url: ty.Optional[str] = None,
        page_id: ty.Optional[str] = None,
        order: str = "date",
        fields: ty.Optional[ty.Sequence] = None,
        offset: int = 0,
        count: int = 10,
        **kwargs
    ) -> 1:
        """
        Gets a list of comments for the page added through the [vk.com/dev/Comments|Comments widget].

        :param widget_api_id: No description provided
        :param url: No description provided
        :param page_id: No description provided
        :param order: No description provided
        :param fields: No description provided
        :param offset: No description provided
        :param count: No description provided
        """

    @api_method
    async def get_pages(
        self,
        *,
        widget_api_id: ty.Optional[int] = None,
        order: str = "friend_likes",
        period: str = "week",
        offset: int = 0,
        count: int = 10,
        **kwargs
    ) -> 1:
        """
        Gets a list of application/site pages where the [vk.com/dev/Comments|Comments widget] or [vk.com/dev/Like|Like widget] is installed.

        :param widget_api_id: No description provided
        :param order: No description provided
        :param period: No description provided
        :param offset: No description provided
        :param count: No description provided
        """
