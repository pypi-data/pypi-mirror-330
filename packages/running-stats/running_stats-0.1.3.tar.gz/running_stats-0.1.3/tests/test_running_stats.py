from typing import Union

import pytest

from running_stats.running_stats import RunningMeanVar, RunningStats


@pytest.fixture
def rs_empty() -> RunningMeanVar:
    return RunningMeanVar()


@pytest.fixture(name="rs_one_value")
def fixture_rs_one_value(rs_empty: RunningMeanVar) -> RunningMeanVar:
    rs_empty.push(4.0)
    return rs_empty


@pytest.fixture(name="rs_two_values")
def fixture_rs_two_values(rs_one_value: RunningMeanVar) -> RunningMeanVar:
    rs_one_value.push(6.0)
    return rs_one_value


@pytest.fixture(name="rs_three_values")
def fixture_rs_three_values(rs_two_values: RunningMeanVar) -> RunningMeanVar:
    rs_two_values.push(2.0)
    return rs_two_values


@pytest.fixture(name="value_list")
def fixture_value_list() -> list[float]:
    return [2.0, 1.0, -3.0, -1.0]


@pytest.mark.parametrize("cls", [RunningMeanVar, RunningStats])
def test_initial_values(cls: Union[type[RunningStats], type[RunningMeanVar]]) -> None:
    rs_empty = cls()
    assert rs_empty.num_values == 0
    assert rs_empty.M1 == 0.0
    assert rs_empty.M2 == 0.0


def test_running_stats_initial_values() -> None:
    rs = RunningStats()

    assert rs.M3 == 0.0
    assert rs.M4 == 0.0


@pytest.mark.parametrize("M2", [0.0, 2.0, 4.0, 5.0])
@pytest.mark.parametrize("n", [2, 5, 11])
def test_variance_n_gt_1(M2: float, n: int) -> None:  # noqa: N803
    rs = RunningMeanVar(num_values=n, M2=M2)
    assert rs.variance() == M2 / (n - 1)


@pytest.mark.parametrize("M2", [0.0, 2.0, 4.0, 5.0])
@pytest.mark.parametrize("n", [0, 1])
def test_variance_n_eq_0_or_1(M2: float, n: int) -> None:  # noqa: N803
    rs = RunningMeanVar(num_values=n, M2=M2)
    assert rs.variance() == 0.0


@pytest.mark.parametrize("cls", [RunningMeanVar, RunningStats])
def test_one_value(cls: Union[type[RunningStats], type[RunningMeanVar]]) -> None:
    rs_one_value = cls()
    rs_one_value.push(4.0)
    assert rs_one_value.num_values == 1
    assert rs_one_value.M1 == 4.0
    assert rs_one_value.M2 == 0.0


def test_running_stats_one_value() -> None:
    rs = RunningStats()
    value = 6.0
    rs.push(value)
    assert rs.M3 == 0.0
    assert rs.M4 == 0.0


@pytest.mark.parametrize("cls", [RunningMeanVar, RunningStats])
def test_two_values(cls: Union[type[RunningStats], type[RunningMeanVar]]) -> None:
    rs_two_values = cls()
    rs_two_values.push(4.0)
    rs_two_values.push(6.0)
    assert rs_two_values.num_values == 2
    assert rs_two_values.M1 == 5.0
    assert rs_two_values.M2 == 2.0


def test_running_stats_two_values() -> None:
    rs = RunningStats()
    values = [6.0, 8.0]
    for value in values:
        rs.push(value)
    expected_mean = sum(values) / len(values)
    assert expected_mean == rs.M1
    expected_M2 = sum((x - expected_mean) ** 2 for x in values)  # noqa: N806
    assert expected_M2 == rs.M2
    expected_M3 = sum((x - expected_mean) ** 3 for x in values)  # noqa: N806
    assert expected_M3 == rs.M3
    expected_M4 = sum((x - expected_mean) ** 4 for x in values)  # noqa: N806
    assert expected_M4 == rs.M4


@pytest.mark.parametrize("cls", [RunningMeanVar, RunningStats])
def test_three_values(cls: Union[type[RunningStats], type[RunningMeanVar]]) -> None:
    rs = cls()
    rs.push(4.0)
    rs.push(6.0)
    rs.push(2.0)
    assert rs.num_values == 3
    assert rs.M1 == 4.0
    assert rs.M2 == 8.0


def test_push_iter_with_list(value_list: list[float]) -> None:
    rs = RunningMeanVar()
    rs.push_iter(value_list)
    assert rs.num_values == len(value_list)
    assert rs.mean() == -0.25
    assert rs.variance() == 4.916666666666667


def test_add_two_running_mean_var() -> None:
    a = RunningMeanVar()
    a.num_values = 3
    a.M1 = 2.0
    a.M2 = 7.8

    b = RunningMeanVar()
    b.num_values = 6
    b.M1 = 6.0
    b.M2 = 3.4

    c = a + b
    assert c.num_values == a.num_values + b.num_values
    assert c.M1 == 42.0 / 9
    assert c.M2 == 43.2


def test_iadd_two_running_mean_var() -> None:
    a = RunningMeanVar()
    a.num_values = 3
    a.M1 = 2.0
    a.M2 = 0.8

    b = RunningMeanVar()
    b.num_values = 8
    b.M1 = -3.0
    b.M2 = 4.4

    a += b
    assert a.num_values == 11
    assert a.M1 == -18.0 / 11
    assert a.M2 == 5.2 + 25.0 * 24 / 11
