from sneks.engine.config.instantiation import config
from sneks.engine.core.action import Action
from sneks.engine.core.bearing import Bearing


class Velocity:
    azimuth: Bearing

    def __init__(self):
        self.azimuth = Bearing(0, 0)

    def add(self, action: Action) -> None:
        match action:
            case Action.UP:
                self.azimuth.y = min(
                    config.game.directional_speed_limit, self.azimuth.y + 1
                )
            case Action.DOWN:
                self.azimuth.y = max(
                    -1 * config.game.directional_speed_limit, self.azimuth.y - 1
                )
            case Action.LEFT:
                self.azimuth.x = max(
                    -1 * config.game.directional_speed_limit, self.azimuth.x - 1
                )
            case Action.RIGHT:
                self.azimuth.x = min(
                    config.game.directional_speed_limit, self.azimuth.x + 1
                )
