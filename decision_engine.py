def decide_action(alert_name):
    if alert_name == "HighCPUUsage":
        return "restart_service"
    elif alert_name == "DiskFull":
        return "clear_disk"
    else:
        return "no_action"
