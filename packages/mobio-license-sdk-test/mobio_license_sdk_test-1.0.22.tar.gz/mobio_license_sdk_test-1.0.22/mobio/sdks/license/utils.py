from .crypt_utils import CryptUtil
from .date_utils import *


class Utils:
    DATE_YYYYmmdd = "%Y%m%d"
    DATE_YYYYmm = "%Y%m"
    TIME_ZONE = 420

    @staticmethod
    def check_merchant_expire(license_key, merchant_id):
        merchant_expire = True
        try:
            result = CryptUtil.get_license_info(license_key, merchant_id)
            if (
                result
                and result.get("expire_time")
                and convert_timestamp_to_date_utc(result.get("expire_time"))
            ):
                time_stamp_now = convert_date_to_timestamp(get_utc_now())
                if result.get("expire_time") > time_stamp_now:
                    merchant_expire = False
                else:
                    print(
                        "license_sdk::check_time_merchant_expire license merchant expire_time"
                    )
            else:
                print(
                    "license_sdk::check_time_merchant_expire license expire_time not found"
                )
        except Exception as e:
            print("license_sdk::check_time_merchant_expire: ERROR: %s" % e)
        return merchant_expire
