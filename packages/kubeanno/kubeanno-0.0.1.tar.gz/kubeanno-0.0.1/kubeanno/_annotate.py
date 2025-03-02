import subprocess
import kubeanno

def annotate(key, value, strict=False):
    if '/' not in key:
        key = f'kubeanno/{key}'

    if kubeanno.is_active():
        info = kubeanno.kubeinfo()
        cmd = [
            info["kubectl"],
            "--token", info["token"],
            "--certificate-authority", info["ca"],
            "annotate", "pod", info["hostname"],
            f"{key}={value}", "--overwrite"
        ]

        result = subprocess.run(cmd, capture_output=True, text=True)

        if result.returncode != 0:
            err = f"Error annotating pod: {result.stderr}"
            if strict:
                raise RuntimeError(err)
            else:
                print(err)
    elif strict:
        raise RuntimeError('kubernetes not available')
