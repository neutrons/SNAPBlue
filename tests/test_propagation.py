from __future__ import annotations

import json
from pathlib import Path
from unittest.mock import MagicMock

from snapwrap import snapStateMgr as ssm
from snapwrap import utils


def _read_log_lines(tmp_path: Path):
    log_path = tmp_path / ".logs" / "propagation_log.jsonl"
    assert log_path.exists()
    return [json.loads(line) for line in log_path.read_text().splitlines() if line.strip()]


def test_is_propagated_entry_true_and_false():
    propagated = {
        "comments": "(copied from run:68979 version:2) original comments: measured",
    }
    measured = {
        "comments": "measured directly on Si standard",
    }

    assert utils._is_propagated_entry(propagated) is True
    assert utils._is_propagated_entry(measured) is False
    assert utils._is_propagated_entry({"comments": ""}) is False
    assert utils._is_propagated_entry({}) is False


def test_write_propagation_log_creates_jsonl(tmp_path, monkeypatch):
    monkeypatch.setattr(utils, "Config", {"instrument.calibration.home": str(tmp_path)})

    utils._write_propagation_log({
        "outcome": "dry_run",
        "donorRunNumber": "12345",
    })

    lines = _read_log_lines(tmp_path)
    assert len(lines) == 1
    assert lines[0]["outcome"] == "dry_run"
    assert lines[0]["donorRunNumber"] == "12345"
    assert "timestamp" in lines[0]
    assert "linux_user" in lines[0]


def test_propagate_guard_blocks_propagated_donor_and_logs(tmp_path, monkeypatch):
    monkeypatch.setattr(utils, "Config", {"instrument.calibration.home": str(tmp_path)})

    mock_ssm = MagicMock()
    mock_ssm.stateDef.return_value = ("donor-state", {"det_arc1": 10.0, "det_arc2": 20.0})
    mock_ssm.detectorConfig.return_value = "det-config"
    mock_ssm.checkCalibrationStatus.return_value = {
        "runIsCalibrated": True,
        "numberCalibrations": 1,
        "latestValidCalibrationDate": "2026-04-20T10:00:00",
        "latestValidCalibrationDict": {
            "version": 2,
            "runNumber": "68979",
            "cycleID": "2026-A",
            "comments": "(copied from run:12345 version:1) original comments: measured",
        },
    }

    logger_instance = MagicMock()
    monkeypatch.setattr(utils, "Logger", lambda _: logger_instance, raising=False)
    monkeypatch.setattr(utils, "ssm", mock_ssm)

    utils.propagateDifcal("68979", isLite=True, propagate=True)

    mock_ssm.copyDifcal.assert_not_called()
    logger_instance.error.assert_called_once()

    lines = _read_log_lines(tmp_path)
    assert lines[-1]["outcome"] == "skipped_donor_is_propagated"
    assert lines[-1]["donorRunNumber"] == "68979"


def test_propagate_dry_run_and_success_log_outcomes(tmp_path, monkeypatch):
    monkeypatch.setattr(utils, "Config", {"instrument.calibration.home": str(tmp_path)})

    donor_status = {
        "runIsCalibrated": True,
        "numberCalibrations": 3,
        "latestValidCalibrationDate": "2026-04-20T10:00:00",
        "latestValidCalibrationDict": {
            "version": 2,
            "runNumber": "70001",
            "cycleID": "2026-A",
            "comments": "measured directly",
        },
    }

    recipient_status = {
        "stateID": "recipient-state",
        "numberCalibrations": 1,
        "calibIndexList": [
            {"version": 0},
            {"version": 1},
        ],
        "latestCalibrationDict": {"version": 1},
    }

    def _check_cal_status(runNumber, stateID, isLite, calType):
        if runNumber is not None:
            return donor_status
        return recipient_status

    mock_ssm = MagicMock()
    mock_ssm.stateDef.return_value = ("donor-state", {"det_arc1": 10.0, "det_arc2": 20.0})
    mock_ssm.availableStates.return_value = ["donor-state", "recipient-state"]
    mock_ssm.pullStateDict.return_value = {"det_arc1": 10.0, "det_arc2": 20.0}
    mock_ssm.detectorConfig.return_value = "det-config"
    mock_ssm.checkCalibrationStatus.side_effect = _check_cal_status

    monkeypatch.setattr(utils, "ssm", mock_ssm)

    utils.propagateDifcal("70001", isLite=True, propagate=False)
    lines = _read_log_lines(tmp_path)
    assert lines[-1]["outcome"] == "dry_run"
    assert lines[-1]["recipientStateID"] == "recipient-state"
    assert lines[-1]["newVersion"] == 2
    mock_ssm.copyDifcal.assert_not_called()

    utils.propagateDifcal("70001", isLite=True, propagate=True)
    lines = _read_log_lines(tmp_path)
    assert lines[-1]["outcome"] == "success"
    assert lines[-1]["recipientStateID"] == "recipient-state"
    assert lines[-1]["newVersion"] == 2
    mock_ssm.copyDifcal.assert_called_once()


# ── guide-status constraint on detector-config matching ───────────────────
#
# propagateDifcal treats two states as compatible when their detectorConfig
# hashes match. With includeGuideStatus False that hash covers only the
# detector arm angles, so states differing solely in optics/guide position
# were considered interchangeable and calibrations were copied between them.
# These exercise the real ssm.detectorConfig -- no mocks -- because the
# mocked propagation tests above stub it out and cannot see this behaviour.


def _stateDict(opticsPos=2, exitSlit=0):
    return {
        "det_arc1": -50.442,
        "det_arc2": 89.989,
        "BL3:Mot:OpticsPos:Pos": opticsPos,
        "BL3:Mot:OpticsPos:ExitSlit": exitSlit,
    }


def test_detector_config_ignores_optics_pos_without_guide_status():
    """Without guide status the two SNAP optics positions collide."""

    posOne = ssm.detectorConfig(_stateDict(opticsPos=1), False)
    posTwo = ssm.detectorConfig(_stateDict(opticsPos=2), False)

    assert posOne == posTwo


def test_detector_config_separates_optics_pos_with_guide_status():
    """With guide status they are distinct, so propagation is refused."""

    posOne = ssm.detectorConfig(_stateDict(opticsPos=1), True)
    posTwo = ssm.detectorConfig(_stateDict(opticsPos=2), True)

    assert posOne != posTwo


def test_detector_config_separates_exit_slit_with_guide_status():
    slitOpen = ssm.detectorConfig(_stateDict(exitSlit=0), True)
    slitShut = ssm.detectorConfig(_stateDict(exitSlit=1), True)

    assert slitOpen != slitShut


def test_detector_config_still_matches_identical_guide_config():
    """Guide status must not break propagation between genuinely equal states."""

    left = ssm.detectorConfig(_stateDict(), True)
    right = ssm.detectorConfig(_stateDict(), True)

    assert left == right


def test_detector_config_arm_angle_tolerance_survives_guide_status():
    """The 0.5 deg arm rounding still applies when guide status is included."""

    near = dict(_stateDict())
    near["det_arc1"] = -50.442
    far = dict(_stateDict())
    far["det_arc1"] = -50.501  # rounds to the same half degree

    assert ssm.detectorConfig(near, True) == ssm.detectorConfig(far, True)


def test_propagate_difcal_includes_guide_status_by_default():
    """Regression guard: the default must stay True."""

    import inspect

    default = inspect.signature(utils.propagateDifcal).parameters["includeGuideStatus"].default
    assert default is True


def test_calibration_manager_propagation_defaults_match_wrap():
    """The GUI path must not quietly re-enable cross-guide propagation.

    previewPropagation and executePropagation carry their own defaults and
    pass the value through explicitly, so a False here would override the
    propagateDifcal default no matter what utils says.
    """

    import inspect

    from snapwrap.calibrationManager.model import CalibrationManagerModel

    for name in ("previewPropagation", "executePropagation"):
        sig = inspect.signature(getattr(CalibrationManagerModel, name))
        assert sig.parameters["includeGuideStatus"].default is True, name
