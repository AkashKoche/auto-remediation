import subprocess
import os

def run_action(action, instance):
    base_path = "/app/remediation"

    if action == "restart_service":
        script = os.path.join(base_path, "restart_service.sh")
        return subprocess.getoutput(f"bash {script} {instance}")
    
    elif action == "clear_disk":
        script = os.path.join(base_path, "clear_disk.sh")
        return subprocess.getoutput(f"bash {script} {instance}")
    
    return "No action executed"
