from ..alarm_item import AlarmItem, AlarmSeverity
from ..alarm_table_view import AlarmTableType, AlarmTableViewWidget
from ..kafka_reader import KafkaReader
from ..main_window import AlarmHandlerMainWindow
from datetime import datetime, timedelta
from kafka.producer import KafkaProducer
from qtpy.QtCore import QThread
import pytest


@pytest.fixture(scope="function")
def main_window(monkeypatch, mock_kafka_producer):
    """Create an instance of the main window of this application for testing"""
    monkeypatch.setattr(KafkaProducer, "__init__", lambda *args, **kwargs: None)
    monkeypatch.setattr(KafkaReader, "__init__", lambda *args, **kwargs: None)
    monkeypatch.setattr(KafkaReader, "moveToThread", lambda *args: None)
    monkeypatch.setattr(QThread, "start", lambda *args: None)

    main_window = AlarmHandlerMainWindow(["TEST_TOPIC"], ["localhost:9092"])
    return main_window


def test_create_and_show(qtbot, main_window):
    """Ensure the main window of the application inits and shows without any errors"""
    qtbot.addWidget(main_window)
    with qtbot.waitExposed(main_window):
        main_window.show()


def test_create_and_show_plot(qtbot, main_window):
    """Ensure a plot can be created and shown correctly without errors"""
    main_window.create_plot_widget()
    with qtbot.waitExposed(main_window):
        main_window.show()


def test_update_tables(qtbot, main_window, tree_model, mock_kafka_producer):
    """Test the various updates that can happen to the alarm table view"""

    # First verify that the columns in the active and acknowledged tables resize in sync
    main_window.show()
    # Want to use main-window's tables created during init, so the resize-column signals are connected
    main_window.active_alarm_tables["TEST_TOPIC"].alarmView.horizontalHeader().resizeSection(2, 200)

    other_table_column_width = main_window.acknowledged_alarm_tables["TEST_TOPIC"].alarmView.columnWidth(2)
    assert other_table_column_width == 200

    qtbot.addWidget(main_window)
    # Create new tables for testing
    main_window.active_alarm_tables["TEST"] = AlarmTableViewWidget(
        tree_model, mock_kafka_producer, "TEST_TOPIC", AlarmTableType.ACTIVE, lambda x: x
    )

    main_window.acknowledged_alarm_tables["TEST"] = AlarmTableViewWidget(
        tree_model, mock_kafka_producer, "TEST_TOPIC", AlarmTableType.ACKNOWLEDGED, lambda x: x
    )

    # Now let's add both an active and an acknowledged alarm so we have some test data to work with
    active_alarm = AlarmItem("ACTIVE:ALARM", path="/path/to/ACTIVE:ALARM", alarm_severity=AlarmSeverity.MAJOR)
    acknowledged_alarm = AlarmItem("ACK:ALARM", path="/path/to/ACK:ALARM", alarm_severity=AlarmSeverity.MINOR_ACK)
    main_window.active_alarm_tables["TEST"].alarmModel.append(active_alarm)
    main_window.acknowledged_alarm_tables["TEST"].alarmModel.append(acknowledged_alarm)

    # Simulate that an active filter was added to the alarm,
    # and confirm that filter values remain even after alarm is disabled then re-enabled through table updates
    active_alarm.filtered = True
    active_alarm.alarm_filter = "ACTIVE:ALARM == 1"

    main_window.update_table(
        "TEST", "ACTIVE:ALARM", "", AlarmSeverity.MAJOR, "Disabled", None, "", AlarmSeverity.MAJOR, ""
    )
    main_window.update_table(
        "TEST", "ACTIVE:ALARM", "", AlarmSeverity.MAJOR, "Enabled", None, "", AlarmSeverity.MAJOR, ""
    )

    assert active_alarm.filtered is True
    assert active_alarm.alarm_filter == "ACTIVE:ALARM == 1"

    active_alarm.filtered = False
    active_alarm.alarm_filter = ""

    # Now send a "disabled" update for the active alarm. This means the user has disabled this
    # alarm and it should no longer be monitored.
    main_window.update_table(
        "TEST", "ACTIVE:ALARM", "", AlarmSeverity.MAJOR, "Disabled", None, "", AlarmSeverity.MAJOR, ""
    )

    assert len(main_window.active_alarm_tables["TEST"].alarmModel.alarm_items) == 0  # Remove as expected
    assert len(main_window.acknowledged_alarm_tables["TEST"].alarmModel.alarm_items) == 1  # Unaffected

    # Now put it back, and simulate a user acknowledging the alarm
    main_window.active_alarm_tables["TEST"].alarmModel.append(active_alarm)
    # The MAJOR_ACK indicates an acknowledgment action
    main_window.update_table("TEST", "ACTIVE:ALARM", "", AlarmSeverity.MAJOR_ACK, "", None, "", AlarmSeverity.MAJOR, "")
    # Again the active alarm was removed
    assert len(main_window.active_alarm_tables["TEST"].alarmModel.alarm_items) == 0
    # But this time added to acknowledged alarms
    assert len(main_window.acknowledged_alarm_tables["TEST"].alarmModel.alarm_items) == 2

    # Now simulate the alarm returning to an OK state, this should clear the alarm since it is both acknowledged and OK
    main_window.update_table("TEST", "ACTIVE:ALARM", "", AlarmSeverity.OK, "", None, "", AlarmSeverity.OK, "")
    # This should not have changed
    assert len(main_window.active_alarm_tables["TEST"].alarmModel.alarm_items) == 0
    # But this should have cleared one alarm now
    assert len(main_window.acknowledged_alarm_tables["TEST"].alarmModel.alarm_items) == 1

    # And finally update the severity of the acknowledged alarm. This change of state will set it back to being active
    main_window.update_table("TEST", "ACK:ALARM", "", AlarmSeverity.MAJOR, "", None, "", AlarmSeverity.MAJOR, "")
    # This alarm is now activate again
    assert len(main_window.active_alarm_tables["TEST"].alarmModel.alarm_items) == 1
    # And it was moved out of this table
    assert len(main_window.acknowledged_alarm_tables["TEST"].alarmModel.alarm_items) == 0


def test_all_topic(qtbot, main_window, tree_model, mock_kafka_producer):
    """Test that the 'All' topic menu-option appears and tables contain all other topic's data"""

    all_topic_main_window = AlarmHandlerMainWindow(["TOPIC_1", "TOPIC_2"], ["localhost:9092"])
    qtbot.addWidget(all_topic_main_window)

    # Test that topic-selection combo box has option for 'All'
    comboBox = all_topic_main_window.alarm_select_combo_box
    comboBoxOptions = [comboBox.itemText(i) for i in range(comboBox.count())]
    assert "All" in comboBoxOptions

    # Send table updates to populate the topics with some alarms.
    # We expect the 'All' topic will get updated with these as well as the specified topic.
    all_topic_main_window.update_table(
        "TOPIC_1", "ACTIVE:ALARM_1", "", AlarmSeverity.MAJOR, "Enabled", None, "", AlarmSeverity.MAJOR, ""
    )
    all_topic_main_window.update_table(
        "TOPIC_1", "ACTIVE:ALARM_2", "", AlarmSeverity.MAJOR, "Enabled", None, "", AlarmSeverity.MAJOR, ""
    )
    all_topic_main_window.update_table(
        "TOPIC_2", "ACTIVE:ALARM_3", "", AlarmSeverity.MAJOR, "Enabled", None, "", AlarmSeverity.MAJOR, ""
    )
    all_topic_main_window.update_table(
        "TOPIC_2", "ACK:ALARM", "", AlarmSeverity.MAJOR_ACK, "Enabled", None, "", AlarmSeverity.MAJOR, ""
    )

    # Expect 'All' topic to have all alarms across the 2 topics: 3 active and 1 acknowledged
    assert len(all_topic_main_window.active_alarm_tables["TOPIC_1"].alarmModel.alarm_items) == 2
    assert len(all_topic_main_window.acknowledged_alarm_tables["TOPIC_1"].alarmModel.alarm_items) == 0

    assert len(all_topic_main_window.active_alarm_tables["TOPIC_2"].alarmModel.alarm_items) == 1
    assert len(all_topic_main_window.acknowledged_alarm_tables["TOPIC_2"].alarmModel.alarm_items) == 1

    assert len(all_topic_main_window.active_alarm_tables["All"].alarmModel.alarm_items) == 3
    assert len(all_topic_main_window.acknowledged_alarm_tables["All"].alarmModel.alarm_items) == 1

    # Now confirm that an updating alarm in 'TOPIC_2' also updates it in 'All'
    all_topic_main_window.update_table(
        "TOPIC_2", "ACTIVE:ALARM_3", "", AlarmSeverity.MAJOR_ACK, "Enabled", None, "", AlarmSeverity.MAJOR, ""
    )
    assert len(all_topic_main_window.active_alarm_tables["All"].alarmModel.alarm_items) == 2
    assert len(all_topic_main_window.acknowledged_alarm_tables["All"].alarmModel.alarm_items) == 2


def test_check_server_status(qtbot, main_window):
    """Verify that the disconnected alarm server banner shows and hides as expected"""
    # When the application first starts up and has a fresh update, there should be no warning banner visible
    now = datetime.now()
    main_window.last_received_update_time["TEST_TOPIC"] = now
    main_window.check_server_status()
    assert main_window.alarm_server_disconnected_banner.isHidden()

    # Mock a last received update 30 seconds ago, verify that the warning banner is now displayed
    server_timeout = now - timedelta(seconds=30)
    main_window.last_received_update_time["TEST_TOPIC"] = server_timeout
    main_window.check_server_status()
    assert not main_window.alarm_server_disconnected_banner.isHidden()

    # Mock the server coming back online, verify that the banner is hidden again
    main_window.last_received_update_time["TEST_TOPIC"] = datetime.now()
    main_window.check_server_status()
    assert main_window.alarm_server_disconnected_banner.isHidden()
