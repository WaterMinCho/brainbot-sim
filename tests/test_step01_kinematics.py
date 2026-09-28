"""Step 01 수용 테스트: 자세(Pose2D)와 차동 구동 기구학.

멘토가 쓴 스펙이다. 통과시키려고 이 파일을 고치지 않는다.
테스트가 틀렸다고 생각되면 근거를 들어 이의를 제기한다.

실행:
    pytest tests/test_step01_kinematics.py -m "not bonus"   # 필수
    pytest tests/test_step01_kinematics.py -m bonus         # 선택
"""

import math

import pytest

from brainbot.core.diffdrive import body_to_wheels, step_unicycle, wheels_to_body
from brainbot.core.pose import Pose2D, normalize_angle

TWO_PI = 2.0 * math.pi
RANGE_SLACK = 1e-12


def same_direction(a: float, b: float, tol: float = 1e-9) -> bool:
    """두 각도가 같은 방향인지 본다. 2π의 배수만큼 다른 각도는 같은 방향이다."""
    return math.isclose(math.cos(a), math.cos(b), abs_tol=tol) and math.isclose(
        math.sin(a), math.sin(b), abs_tol=tol
    )


def in_range(theta: float) -> bool:
    """-π 이상 π 이하인지 본다. 경계에서는 π와 -π를 모두 허용한다."""
    return -math.pi - RANGE_SLACK <= theta <= math.pi + RANGE_SLACK


def assert_pose(actual: Pose2D, x: float, y: float, theta: float, tol: float = 1e-9) -> None:
    assert actual.x == pytest.approx(x, abs=tol)
    assert actual.y == pytest.approx(y, abs=tol)
    assert same_direction(actual.theta, theta, tol), f"theta={actual.theta}, 기대={theta}"
    assert in_range(actual.theta), f"theta={actual.theta}가 범위를 벗어났다"


class TestNormalizeAngle:
    def test_result_is_in_range_and_points_the_same_way(self) -> None:
        for k in range(-1000, 1001):
            theta = k * 0.1
            result = normalize_angle(theta)
            assert in_range(result), f"입력 {theta} → {result}"
            assert same_direction(result, theta), f"입력 {theta} → {result}"

    def test_values_inside_the_range_are_unchanged(self) -> None:
        for theta in (-3.0, -1.5, -0.1, 0.0, 0.1, 1.5, 3.0):
            assert normalize_angle(theta) == pytest.approx(theta, abs=1e-12)

    @pytest.mark.parametrize(
        ("theta", "expected"),
        [
            (TWO_PI, 0.0),
            (-TWO_PI, 0.0),
            (1.5 * math.pi, -0.5 * math.pi),
            (-1.5 * math.pi, 0.5 * math.pi),
            (50 * TWO_PI + 0.25, 0.25),
            (-50 * TWO_PI - 0.25, -0.25),
        ],
    )
    def test_wraps_around(self, theta: float, expected: float) -> None:
        assert normalize_angle(theta) == pytest.approx(expected, abs=1e-9)


class TestPose2D:
    def test_fields_in_order_x_y_theta(self) -> None:
        pose = Pose2D(1.0, 2.0, 0.5)
        assert (pose.x, pose.y, pose.theta) == (1.0, 2.0, 0.5)

    def test_keyword_arguments(self) -> None:
        pose = Pose2D(x=1.0, y=2.0, theta=0.5)
        assert pose == Pose2D(1.0, 2.0, 0.5)

    def test_is_immutable(self) -> None:
        pose = Pose2D(0.0, 0.0, 0.0)
        with pytest.raises(AttributeError):
            pose.x = 1.0  # type: ignore[misc]

    def test_compares_by_value(self) -> None:
        assert Pose2D(1.0, 2.0, 0.5) == Pose2D(1.0, 2.0, 0.5)
        assert Pose2D(1.0, 2.0, 0.5) != Pose2D(1.0, 2.0, 0.6)


class TestWheelConversion:
    WHEEL_BASE = 0.16

    def test_equal_wheels_go_straight(self) -> None:
        v, w = wheels_to_body(0.2, 0.2, self.WHEEL_BASE)
        assert v == pytest.approx(0.2)
        assert w == pytest.approx(0.0)

    def test_opposite_wheels_spin_in_place(self) -> None:
        v, w = wheels_to_body(-0.08, 0.08, self.WHEEL_BASE)
        assert v == pytest.approx(0.0)
        assert w == pytest.approx(1.0)

    def test_faster_right_wheel_turns_left(self) -> None:
        _, w = wheels_to_body(0.1, 0.3, self.WHEEL_BASE)
        assert w > 0.0

    def test_known_values(self) -> None:
        v, w = wheels_to_body(0.0, 1.0, 0.5)
        assert v == pytest.approx(0.5)
        assert w == pytest.approx(2.0)

    def test_body_to_wheels_known_values(self) -> None:
        v_left, v_right = body_to_wheels(0.5, 2.0, 0.5)
        assert v_left == pytest.approx(0.0)
        assert v_right == pytest.approx(1.0)

    @pytest.mark.parametrize(
        ("v_left", "v_right"),
        [(0.0, 0.0), (0.2, 0.2), (0.1, 0.3), (-0.2, 0.1), (0.22, -0.22)],
    )
    def test_round_trip(self, v_left: float, v_right: float) -> None:
        v, w = wheels_to_body(v_left, v_right, self.WHEEL_BASE)
        back_left, back_right = body_to_wheels(v, w, self.WHEEL_BASE)
        assert back_left == pytest.approx(v_left)
        assert back_right == pytest.approx(v_right)

    @pytest.mark.parametrize("wheel_base", [0.0, -0.16])
    def test_rejects_non_positive_wheel_base(self, wheel_base: float) -> None:
        with pytest.raises(ValueError):
            wheels_to_body(0.1, 0.1, wheel_base)
        with pytest.raises(ValueError):
            body_to_wheels(0.1, 0.0, wheel_base)


class TestStepUnicycle:
    def test_straight_along_x(self) -> None:
        assert_pose(step_unicycle(Pose2D(0.0, 0.0, 0.0), 1.0, 0.0, 1.0), 1.0, 0.0, 0.0)

    def test_straight_along_heading(self) -> None:
        start = Pose2D(1.0, 1.0, math.pi / 2)
        assert_pose(step_unicycle(start, 2.0, 0.0, 0.5), 1.0, 2.0, math.pi / 2)

    def test_reverse(self) -> None:
        assert_pose(step_unicycle(Pose2D(0.0, 0.0, 0.0), -1.0, 0.0, 1.0), -1.0, 0.0, 0.0)

    def test_rotate_in_place_counterclockwise(self) -> None:
        result = step_unicycle(Pose2D(0.0, 0.0, 0.0), 0.0, math.pi / 2, 1.0)
        assert_pose(result, 0.0, 0.0, math.pi / 2)

    def test_rotate_in_place_clockwise(self) -> None:
        result = step_unicycle(Pose2D(0.0, 0.0, 0.0), 0.0, -math.pi / 2, 1.0)
        assert_pose(result, 0.0, 0.0, -math.pi / 2)

    def test_zero_dt_keeps_pose(self) -> None:
        start = Pose2D(1.0, 2.0, 0.5)
        assert_pose(step_unicycle(start, 1.0, 1.0, 0.0), 1.0, 2.0, 0.5)

    def test_negative_dt_raises(self) -> None:
        with pytest.raises(ValueError):
            step_unicycle(Pose2D(0.0, 0.0, 0.0), 1.0, 0.0, -0.1)

    def test_does_not_change_the_input(self) -> None:
        start = Pose2D(1.0, 2.0, 0.5)
        step_unicycle(start, 1.0, 1.0, 0.1)
        assert start == Pose2D(1.0, 2.0, 0.5)

    def test_quarter_circle_in_small_steps(self) -> None:
        """반지름 1인 원의 4분의 1. 1000번으로 나눠 호출한다."""
        pose = Pose2D(0.0, 0.0, 0.0)
        for _ in range(1000):
            pose = step_unicycle(pose, math.pi / 2, math.pi / 2, 0.001)
        assert_pose(pose, 1.0, 1.0, math.pi / 2, tol=5e-3)

    def test_full_circle_comes_back(self) -> None:
        """반지름 1인 원을 한 바퀴 돈다."""
        steps = 6283
        dt = TWO_PI / steps
        pose = Pose2D(0.0, 0.0, 0.0)
        for _ in range(steps):
            pose = step_unicycle(pose, 1.0, 1.0, dt)
        assert_pose(pose, 0.0, 0.0, 0.0, tol=2e-2)

    def test_theta_stays_in_range(self) -> None:
        pose = Pose2D(0.0, 0.0, 0.0)
        for _ in range(1000):
            pose = step_unicycle(pose, 0.0, 1.0, 0.1)
            assert in_range(pose.theta), f"theta={pose.theta}"
        assert same_direction(pose.theta, 100.0, tol=1e-6)


@pytest.mark.bonus
class TestExactIntegration:
    """선택 과제. Δt가 커도 정확해야 한다. 원호 적분이 필요하다."""

    def test_quarter_circle_in_one_step(self) -> None:
        result = step_unicycle(Pose2D(0.0, 0.0, 0.0), math.pi / 2, math.pi / 2, 1.0)
        assert_pose(result, 1.0, 1.0, math.pi / 2)

    def test_half_circle_in_one_step(self) -> None:
        result = step_unicycle(Pose2D(0.0, 0.0, 0.0), math.pi, math.pi, 1.0)
        assert_pose(result, 0.0, 2.0, math.pi)

    def test_clockwise_arc(self) -> None:
        result = step_unicycle(Pose2D(0.0, 0.0, 0.0), math.pi / 2, -math.pi / 2, 1.0)
        assert_pose(result, 1.0, -1.0, -math.pi / 2)

    def test_tiny_angular_velocity_is_stable(self) -> None:
        result = step_unicycle(Pose2D(0.0, 0.0, 0.0), 1.0, 1e-12, 1.0)
        assert_pose(result, 1.0, 0.0, 0.0, tol=1e-6)
