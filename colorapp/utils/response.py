class FormResponse:
    __need_rembg: bool = False
    __need_resize: bool = True
    __n_clusters: int = 5
    __base_pallet: str = ''
    __process: str

    def __init__(self, response):
        self.__need_rembg = 'remove_background' in response
        self.__need_resize = 'want_not_to_resize' in response
        if 'n_clusters' in response:
            self.__n_clusters = int(response['n_clusters'])
        if 'base_pallet' in response:
            self.__base_pallet = response['base_pallet']
        self.__process = response['process']

    def need_rembg(self) -> bool:
        return self.__need_rembg

    def need_resize(self) -> bool:
        return self.__need_resize

    def get_n_clusters(self) -> int:
        return self.__n_clusters

    def get_base_pallet(self) -> str:
        return self.__base_pallet

    def request_base_color(self) -> bool:
        return self.__process == 'base-color'

    def request_nearest_base_color(self) -> bool:
        return self.__process == 'nearest-base-color'
