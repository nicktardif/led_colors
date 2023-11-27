from model.color_algorithm import ColorAlgorithm


class BodyGroup:
    def __init__(
        self,
        head_algorithm: ColorAlgorithm,
        torso_algorithm: ColorAlgorithm,
        left_arm_algorithm: ColorAlgorithm,
        right_arm_algorithm: ColorAlgorithm,
        left_leg_algorithm: ColorAlgorithm,
        right_leg_algorithm: ColorAlgorithm,
    ):
        self._head_algorithm = head_algorithm
        self._torso_algorithm = torso_algorithm
        self._left_arm_algorithm = left_arm_algorithm
        self._right_arm_algorithm = right_arm_algorithm
        self._left_leg_algorithm = left_leg_algorithm
        self._right_leg_algorithm = right_leg_algorithm

    @property
    def head(self) -> ColorAlgorithm:
        return self._head_algorithm

    @property
    def torso(self) -> ColorAlgorithm:
        return self._torso_algorithm

    @property
    def left_arm(self) -> ColorAlgorithm:
        return self._left_arm_algorithm

    @property
    def right_arm(self) -> ColorAlgorithm:
        return self._right_arm_algorithm

    @property
    def left_leg(self) -> ColorAlgorithm:
        return self._left_leg_algorithm

    @property
    def right_leg(self) -> ColorAlgorithm:
        return self._right_leg_algorithm
