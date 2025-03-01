class URLProvider:
    # _url = "http://localhost:8092"  # 私有静态属性，存储URL
    _url = "http://119.23.104.65:8092"  # 私有静态属性，存储URL
    @staticmethod
    def get_url():
        """静态方法，用于获取URL"""
        return URLProvider._url