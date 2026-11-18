class Urls:
    BASE_URL = "https://qa-desk.education-services.ru/"
    SIGNUP_URL = BASE_URL + "api/signup"
    SIGNIN_URL = BASE_URL + "api/signin"
    CREATE_LISTING_URL = BASE_URL + "api/create-listing"
    UPDATE_OFFER_URL = BASE_URL + "api/update-offer/{offer_id}"
    DELETE_OFFER_URL = BASE_URL + "api/listings/{offer_id}"

    @staticmethod
    def get_update_offer_url(offer_id):
        return Urls.UPDATE_OFFER_URL.format(offer_id = offer_id)

    @staticmethod
    def get_delete_offer_url(offer_id):
        return Urls.DELETE_OFFER_URL.format(offer_id = offer_id)
    