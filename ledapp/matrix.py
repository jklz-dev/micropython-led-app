class MatrixFrame:
    def __init__(self, delay: int = 1000):
        self._pattern_changes = [None] * Matrix.total_pixels
        self.delay = delay

    def set_cell(self, row: int, column: int, cell_color: tuple[int, int, int] = None) -> None:
        address_to_set = Matrix.get_address(row, column)
        self._pattern_changes[address_to_set] = cell_color

    def set_cells(self, cells: list[tuple[int, int]], color: tuple[int, int, int] = None) -> None:
        for [row, column] in cells:
            self.set_cell(row, column, color)

    def set_row(self, row: int, color: tuple[int, int, int] = None) -> None:
        for address in Matrix.get_row_addresses(row):
            self._pattern_changes[address] = color

    def to_display_frame(self, base_pattern: list[tuple[int, int, int] | None]) -> dict:
        if len(base_pattern) != len(self._pattern_changes) != Matrix.total_pixels:
            raise ValueError("base_pattern does not match expected length {}".format(len(self._pattern_changes)))
        pattern = [None] * Matrix.total_pixels
        for index, value in enumerate(self._pattern_changes):
            pattern[index] = value or base_pattern[index]
        display_frame = {
            "type": "pattern",
            "delay": self.delay,
            "pattern": pattern,
        }
        return display_frame


class Matrix:
    row_count: int = None
    column_count: int = None

    total_pixels: int = None

    _matrix_addresses: list[list[int]] = None

    @classmethod
    def _build_matrix_addresses(cls) -> None:
        cls.total_pixels: int = cls.row_count * cls.column_count

        if cls.total_pixels == 0:
            return None

        cls._matrix_addresses = []

        for matrix_row in range(cls.row_count):
            row_start_address_range: int = (matrix_row * cls.column_count)
            row_end_address_range: int = row_start_address_range + cls.column_count

            row_direction_left_to_right: bool = matrix_row % 2 == 0

            row_addresses: list[int] = []

            for cell_address in range(row_start_address_range, row_end_address_range):
                if row_direction_left_to_right:
                    row_addresses.append(cell_address)
                else:
                    row_addresses.insert(0, cell_address)
            cls._matrix_addresses.insert(0, row_addresses)

    @classmethod
    def get_row_addresses(cls, row: int) -> list[int]:
        if cls._matrix_addresses is None:
            cls._build_matrix_addresses()
        return cls._matrix_addresses[row]

    @classmethod
    def get_address(cls, row: int, column: int):
        return cls.get_row_addresses(row)[column]

    @classmethod
    def configure(cls, rows: int, columns: int):
        cls.row_count = rows
        cls.column_count = columns

    def __init__(self):
        self.base_pattern = [None] * Matrix.total_pixels
        self._frames: list[MatrixFrame] = []

    def fill(self, fill_color: tuple[int, int, int] = None) -> None:
        self.base_pattern = [fill_color] * Matrix.total_pixels

    def _initialize_base_pattern(self, fill_color: tuple[int, int, int] = None) -> None:
        self.base_pattern = [fill_color] * Matrix.total_pixels

    @property
    def _is_base_pattern_initialized(self) -> bool:
        return (self.base_pattern is not None) and (len(self.base_pattern) == Matrix.total_pixels)

    def set_cell(self, row: int, column: int, fill_color: tuple[int, int, int] = None) -> None:
        if not self._is_base_pattern_initialized:
            self._initialize_base_pattern()
        address_to_set = Matrix.get_address(row, column)
        self.base_pattern[address_to_set] = fill_color

    def set_cells(self, cells: list[tuple[int, int]], fill_color: tuple[int, int, int] = None) -> None:
        for [row, column] in cells:
            self.set_cell(row, column, fill_color)

    def set_row(self, row: int, color: tuple[int, int, int] = None) -> None:
        for address in Matrix.get_row_addresses(row):
            self.base_pattern[address] = color

    def create_frame(self, delay: int = None) -> MatrixFrame:
        new_frame = MatrixFrame(delay)
        self._frames.append(new_frame)
        return new_frame

    def does_frame_exist(self, order: int) -> bool:
        return 0 <= order < len(self._frames)

    def get_frame(self, order: int) -> MatrixFrame:
        if not self.does_frame_exist(order):
            raise Exception("frame does not exist for position {}".format(order))
        return self._frames[order]

    def to_pixel_display(self):
        display_frames = []
        for frame in self._frames:
            display_frames.append(frame.to_display_frame(self.base_pattern))
        display = {
            "type": "playback",
            "frames": display_frames,
        }
        return display
