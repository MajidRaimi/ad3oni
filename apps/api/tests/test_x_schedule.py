from src.features.x.keys import GRACE_MINUTES, POST_WINDOWS
from src.features.x.schedule import is_due, make_plan


def test_make_plan_has_one_time_per_window() -> None:
    plan = make_plan()
    assert len(plan) == len(POST_WINDOWS)


def test_make_plan_times_fall_inside_their_windows() -> None:
    for _ in range(50):
        plan = make_plan()
        for (start, end), stamp in zip(POST_WINDOWS, plan, strict=True):
            minutes = int(stamp[:2]) * 60 + int(stamp[3:])
            assert start * 60 <= minutes < end * 60


def test_make_plan_times_are_ordered_and_spread() -> None:
    plan = make_plan()
    as_minutes = [int(t[:2]) * 60 + int(t[3:]) for t in plan]
    assert as_minutes == sorted(as_minutes)


def test_is_due_at_exact_target() -> None:
    assert is_due(7 * 60 + 30, "07:30") is True


def test_is_due_within_grace_window() -> None:
    assert is_due(7 * 60 + 30 + GRACE_MINUTES, "07:30") is True


def test_is_not_due_before_target() -> None:
    assert is_due(7 * 60 + 29, "07:30") is False


def test_is_not_due_after_grace() -> None:
    assert is_due(7 * 60 + 30 + GRACE_MINUTES + 1, "07:30") is False
