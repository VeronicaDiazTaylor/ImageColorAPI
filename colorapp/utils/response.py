class FormResponse:
    __need_rembg: bool = False # 背景を削除するかどうかのフラグ
    __need_resize: bool = True # 画像のリサイズが必要かどうかのフラグ
    __n_clusters: int = 5 # クラスタの数
    __base_pallet: str = '' # 基本のパレット
    __process: str # 処理内容

    def __init__(self, response):
        self.__need_rembg = 'remove_background' in response
        self.__need_resize = 'want_not_to_resize' in response
        if 'n_clusters' in response:
            self.__n_clusters = int(response['n_clusters'])
        if 'base_pallet' in response:
            self.__base_pallet = response['base_pallet']
        self.__process = response['process']

    def need_rembg(self) -> bool:
        """背景削除が必要かどうかを返す

        Returns:
            bool: 背景削除が必要な場合はTrue、そうでない場合はFalse
        """
        return self.__need_rembg

    def need_resize(self) -> bool:
        """リサイズが必要かどうかを返す

        Returns:
            bool: リサイズが必要な場合はTrue、そうでない場合はFalse
        """
        return self.__need_resize

    def get_n_clusters(self) -> int:
        """クラスタの数を返す

        Returns:
            int: クラスタの数
        """
        return self.__n_clusters

    def get_base_pallet(self) -> str:
        """基本のパレットを返す

        Returns:
            str: 基本のパレット
        """
        return self.__base_pallet

    def request_base_color(self) -> bool:
        """処理内容が'base-color'かどうかを確認する

        Returns:
            bool: 処理内容が'base-color'の場合はTrue、そうでない場合はFalse
        """
        return self.__process == 'base-color'

    def request_nearest_base_color(self) -> bool:
        """処理内容が'nearest-base-color'かどうかを確認する

        Returns:
            bool: 処理内容が'nearest-base-color'の場合はTrue、そうでない場合はFalse
        """
        return self.__process == 'nearest-base-color'
