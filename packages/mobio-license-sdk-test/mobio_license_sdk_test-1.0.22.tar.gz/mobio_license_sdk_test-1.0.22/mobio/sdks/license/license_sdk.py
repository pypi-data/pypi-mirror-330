from mobio.libs.Singleton import Singleton

from .config import Mobio
from .crypt_utils import CryptUtil
from .package_utils import PackageUtils


# from mobio.libs.ciphers import MobioCrypt2


def sdk_pre_check(func):
    def decorated_function(*args, **kwargs):
        # if not MobioLicenseSDK().admin_host:
        #     raise ValueError("admin_host None")
        # if not MobioLicenseSDK().lru_cache:
        #     raise ValueError("redis_uri None")
        # if not MobioLicenseSDK().module_encrypt:
        #     raise ValueError("module_encrypt None")
        # if not MobioLicenseSDK().module_use:
        #     raise ValueError("module_use None")
        # if MobioLicenseSDK().admin_version not in MobioLicenseSDK.LIST_VERSION_VALID:
        #     raise ValueError("admin_version invalid")
        # # if not MobioLicenseSDK().module_valid:
        # #     raise ValueError("module invalid")
        # if not MobioLicenseSDK().license_key:
        #     raise ValueError("license_key none")
        return func(*args, **kwargs)

    return decorated_function


@Singleton
class MobioLicenseSDK(object):
    # lru_cache = None
    DEFAULT_REQUEST_TIMEOUT_SECONDS = 20
    LIST_VERSION_VALID = ["v1.0", "api/v2.0", "api/v2.1"]

    def __init__(self):
        self.admin_version = MobioLicenseSDK.LIST_VERSION_VALID[-1]
        self.module_encrypt = ""
        self.module_use = ""
        self.request_header = None
        self.module_valid = False
        # self.redis_uri = None
        self.license_key = ""
        self.admin_host = ""
        self.config()

    @property
    def p_module_valid(self):
        return self.module_valid

    def config(
            self,
            admin_host=None,
            redis_uri=None,
            module_use=None,
            module_encrypt=None,
            license_key=None,
    ):
        self.admin_host = Mobio.ADMIN_HOST
        self.license_key = Mobio.LICENSE_KEY_SALT

    @sdk_pre_check
    def get_json_license(
            self,
            merchant_id, use_cache=True
    ):
        return CryptUtil.get_license_info(self.license_key, merchant_id, use_cache)

    @staticmethod
    def encrypt2(data: str):
        return CryptUtil.encrypt_mobio_crypt2(data)

    @staticmethod
    def decrypt2(data: str):
        return CryptUtil.decrypt_mobio_crypt2(data)

    @staticmethod
    def decrypt1(key_salt: str, data: str):
        return CryptUtil.decrypt_mobio_crypt1(key_salt, data)

    # @sdk_pre_check
    # def merchant_has_expired(self, merchant_id):
    #     return Utils.check_merchant_expire(self.license_key, merchant_id)

    @sdk_pre_check
    def check_allowed_quantity_for_attribute(
            self, merchant_id: str, module: str, attribute: str, number_check: int
    ):
        json_license = CryptUtil.get_license_info(self.license_key, merchant_id)
        result = PackageUtils(json_license=json_license).pre_check_allow_attribute_quantity(
            module=module, attribute=attribute, number_check=number_check
        )
        return result

    @sdk_pre_check
    def get_quantity_for_attribute(
            self, merchant_id: str, module: str, attribute: str
    ):
        json_license = CryptUtil.get_license_info(self.license_key, merchant_id)
        result = PackageUtils(json_license=json_license).pre_get_attribute_quantity(
            module=module, attribute=attribute
        )
        return result

    @sdk_pre_check
    def check_allowed_feature_attribute(
            self, merchant_id: str, module: str, attribute: str
    ):
        json_license = CryptUtil.get_license_info(self.license_key, merchant_id)
        result = PackageUtils(json_license=json_license).pre_check_allow_attribute_feature(
            module=module, attribute=attribute
        )
        return result

    @sdk_pre_check
    def get_package_module_current(
            self, merchant_id: str, module: str, use_cache=True
    ):
        json_license = CryptUtil.get_license_info(self.license_key, merchant_id, use_cache)
        package_detect = PackageUtils(json_license=json_license)
        result = package_detect.get_license_package_by_module(module)
        # su dung cho cac may on premise
        if package_detect.uncheck_license:
            return {
                "is_allowed": True,
                "uncheck_license": True,
                # package_detect.LicenseMerchant.package_code: package_detect.PackageCode.enterprise_plus
            }
        return result

    @sdk_pre_check
    def get_info_limit_activation_cdp(
            self, merchant_id: str, attribute: str
    ):
        json_license = CryptUtil.get_license_info(self.license_key, merchant_id)
        result = PackageUtils(json_license=json_license).get_limit_activation_cdp(attribute)
        return result

    @sdk_pre_check
    def get_list_package_current(
            self, merchant_id: str, use_cache=True
    ):
        json_license = CryptUtil.get_license_info(self.license_key, merchant_id, use_cache)
        result = PackageUtils(json_license=json_license).get_list_package_current()
        return result

    @sdk_pre_check
    def get_info_config_constant(
            self, merchant_id: str
    ):
        json_license = CryptUtil.get_license_info(self.license_key, merchant_id)
        result = PackageUtils(json_license=json_license).get_config_constant()
        return result

    @sdk_pre_check
    def get_number_day_retention_data(
            self, merchant_id: str, module="cdp"
    ):
        json_license = CryptUtil.get_license_info(self.license_key, merchant_id)
        attribute = "day_retention_data"
        result = PackageUtils(json_license=json_license).get_attribute_quantity_last_package(
            module=module, attribute=attribute
        )
        if "max" in result:
            return result.get("max")
        else:
            # voi goi enterprise plus hoac may onprem thi tra ve -1 = khong gioi han
            return -1
