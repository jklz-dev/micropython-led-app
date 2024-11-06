from .colors import WeatherColors
from .matrix import Matrix


class WeatherDisplayConfig(dict):
    type: str  # "weather"
    sky: str  # "day", "night"
    cloudy: bool
    ground: str  # Literal["grass", "snow"]
    sky_action: str  # Optional[Literal["rising", "setting"]]
    forecast: str  # Optional[Literal["rain", "snow", "wind", "fog"]]


class Weather(object):

    def __init__(self):
        self.matrix = Matrix()

    def _draw_ground(self, value: str) -> None:
        """

        :param value: "grass", "snow"
        """
        # get color from config
        color = WeatherColors.ground[value]
        # get rows to set
        for row_index in range(Matrix.row_count - 2, Matrix.row_count):
            self.matrix.set_row(row_index, color)

    def _draw_sun(self, value: str = None) -> None:
        """

        :param value: "rising", "setting"
        """
        height: int = int(Matrix.row_count / 3)
        width: int = int(Matrix.column_count / 3)
        color = WeatherColors.sky["sun"]
        draw_cells: list[tuple[int, int]] = []

        start_column_index: int = Matrix.column_count - width - 1

        # calculate cells that will be sun
        for row_index in range(height):
            draw_width = width
            offset = start_column_index
            if row_index == 0 or row_index == (height - 1):
                draw_width -= 2
                offset += 1
            for column_index in range(offset, offset + draw_width + 1):
                draw_cells.append((row_index, column_index))
        self.matrix.set_cells(draw_cells, color)

    def _draw_moon(self, value = None) -> None:
        """

        :param value: True, "rising", "setting"
        """
        height: int = int(Matrix.row_count / 4)
        width: int = int(Matrix.row_count / 4)
        color = WeatherColors.sky["moon"]
        draw_cells: list[tuple[int, int]] = []

        start_column_index: int = Matrix.column_count - width - 1

        # calculate cells to draw
        for row_index in range(height):
            draw_width = width
            offset = start_column_index
            if row_index == 0 or row_index == (height - 1):
                draw_width -= 2
                offset += 1
            for column_index in range(offset, offset + draw_width + 1):
                draw_cells.append((row_index, column_index))
        self.matrix.set_cells(draw_cells, color)

    def _draw_clouds(self) -> None:
        height: int = int(Matrix.row_count / 3 - 1)
        width: int = int((Matrix.column_count / 3 * 2) - 1)
        color = WeatherColors.sky["cloud"]
        draw_cells: list[tuple[int, int]] = []
        for row_index in range(height):
            draw_width = width
            offset = 1
            if row_index == 0 or row_index == (height - 1):
                draw_width -= 2
                offset += 1
            for column_index in range(offset, offset + draw_width + 1):
                draw_cells.append((row_index, column_index))
        self.matrix.set_cells(draw_cells, color)

    def _draw_sky(self, sky: str, action: str = None) -> None:
        """

        :param sky: "day", "night"
        :param action: None | "rising" | "setting"
        """
        background_color = WeatherColors.sky[sky]
        self.matrix.fill(background_color)
        if sky == "day":
            self._draw_sun(action)
        elif sky == "night":
            self._draw_moon(action)

    def _animate_forcast(self, forcast: str = None) -> None:
        """

        :param forcast: "rain", "snow", "wind", "fog"
        :return:
        """
        if forcast is None:
            # add a single slide with 5 sec delay
            self.matrix.create_frame(5000)
            return None
        if forcast == "rain" or forcast == "snow":
            action_row_top: int = int(self.matrix.row_count / 4)
            action_height: int = int(self.matrix.row_count / 2)
            action_width: int = int(self.matrix.column_count / 2)
            action_column_offset: int = int(self.matrix.column_count - action_width / 2)
            for row_index in range(action_row_top, action_row_top + action_height, 2):
                action_cells: list[tuple[int, int]] = []
                for column_index in range(action_column_offset, action_column_offset + action_width, 3):
                    if row_index % 2 == 0:
                        action_cells.append((row_index, column_index))
                    else:
                        action_cells.append((row_index, column_index))
                self.matrix.create_frame(750).set_cells(action_cells, WeatherColors.forcast[forcast])

    def with_weather(self, config: WeatherDisplayConfig):
        """

        :param config: WeatherDisplayConfig
        :return: Weather
        """
        self._draw_sky(config['sky'], config['sky_action'])
        is_cloudy: bool = config['cloudy']
        if is_cloudy:
            self._draw_clouds()
        self._draw_ground(config['ground'])
        self._animate_forcast(config.get("forecast") or None)
        return self

    def to_display_playback(self) -> dict:
        return self.matrix.to_pixel_display()
