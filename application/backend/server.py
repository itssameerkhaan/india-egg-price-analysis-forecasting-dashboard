import csv
import configparser
import json
import mimetypes
import os
import subprocess
import sys
import threading
import time
import uuid
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer
from pathlib import Path
from urllib.parse import unquote, urlparse


PROJECT_ROOT = Path(__file__).resolve().parents[2]
WEB_ROOT = PROJECT_ROOT / "application" / "web"
PYTHON_EXE = PROJECT_ROOT / ".venv" / "Scripts" / "python.exe"
VALIDATION_SCRIPT = PROJECT_ROOT / "analysis" / "model_training_comparison.py"
SCRAP_PIPELINE = PROJECT_ROOT / "run_pipeline.ps1"
CHART_DIR = PROJECT_ROOT / "analysis" / "analysis_chart"
COMPARE_DIR = PROJECT_ROOT / "output" / "forecast" / "compare"
MAIN_DATA_DIR = PROJECT_ROOT / "output" / "main_data"
RAW_OUTPUT_DIR = PROJECT_ROOT / "output"
SCRAP_CONFIG = PROJECT_ROOT / "data_scrap" / "config.ini"
USERNAME = "Sameer9696196395"

JOBS = {}
JOBS_LOCK = threading.Lock()


def read_json_body(handler):
    length = int(handler.headers.get("Content-Length", "0") or "0")
    if length <= 0:
        return {}
    raw = handler.rfile.read(length).decode("utf-8")
    return json.loads(raw or "{}")


def read_csv_preview(path, limit=8):
    if not path.exists():
        return {"exists": False, "path": str(path), "rows": [], "columns": [], "row_count": 0}

    rows = []
    with path.open("r", encoding="utf-8-sig", newline="") as handle:
        reader = csv.DictReader(handle)
        columns = reader.fieldnames or []
        for index, row in enumerate(reader):
            if index < limit:
                rows.append(row)
            else:
                break

    row_count = 0
    with path.open("r", encoding="utf-8-sig", newline="") as handle:
        row_count = max(sum(1 for _ in handle) - 1, 0)

    return {
        "exists": True,
        "path": str(path),
        "columns": columns,
        "rows": rows,
        "row_count": row_count,
        "size": path.stat().st_size,
        "updated": path.stat().st_mtime,
    }


def read_metrics():
    path = COMPARE_DIR / "model_metrics.csv"
    if not path.exists():
        return []
    with path.open("r", encoding="utf-8-sig", newline="") as handle:
        return list(csv.DictReader(handle))


def read_run_summary():
    path = COMPARE_DIR / "model_run_summary.json"
    if not path.exists():
        return {}
    with path.open("r", encoding="utf-8") as handle:
        return json.load(handle)


def available_cities():
    return sorted(path.stem.replace("_main_data", "") for path in MAIN_DATA_DIR.glob("*_main_data.csv"))


def available_charts():
    chart_order = [
        ("daily_1_year_compare.html", "Daily One-Year Recursive Test"),
        ("monthly_compare.html", "Monthly Recursive Test"),
        ("weekly_compare.html", "Weekly Recursive Test"),
        ("weekly_trend_compare.html", "Weekly Recursive Test Trend"),
    ]
    charts = []
    for filename, title in chart_order:
        path = CHART_DIR / filename
        charts.append(
            {
                "title": title,
                "filename": filename,
                "url": f"/charts/{filename}",
                "exists": path.exists(),
                "updated": path.stat().st_mtime if path.exists() else None,
            }
        )
    return charts


def dataset_summary():
    summary = read_run_summary()
    city = summary.get("city", "Barwala")
    datasets = [
        ("Egg price raw data", RAW_OUTPUT_DIR / "egg_price_data.csv"),
        (f"{city} feature data", MAIN_DATA_DIR / f"{city}_main_data.csv"),
        ("Recursive validation predictions", COMPARE_DIR / "test_recursive_actual_vs_predicted.csv"),
        ("Monthly validation comparison", COMPARE_DIR / "monthly_compare.csv"),
        ("Weekly validation trend", COMPARE_DIR / "weekly_trend_compare.csv"),
    ]
    return [{"name": name, **read_csv_preview(path)} for name, path in datasets]


def read_scrap_config():
    parser = configparser.ConfigParser()
    parser.read(SCRAP_CONFIG)
    return {
        "startDate": parser.get("Scraping", "start_date", fallback=""),
        "endDate": parser.get("Scraping", "end_date", fallback=""),
        "yearsBack": parser.get("Scraping", "years_back", fallback="10"),
        "headless": parser.get("Scraping", "headless", fallback="False"),
        "maxWaitTime": parser.get("Scraping", "max_wait_time", fallback="15"),
        "saveFormats": parser.get("Output", "save_formats", fallback="csv"),
        "overwrite": parser.get("Output", "overwrite", fallback="False"),
        "websiteDelay": parser.get("Website", "request_delay", fallback="1.0"),
        "weatherDelay": parser.get("Weather", "request_delay", fallback="2.0"),
    }


def job_for_json(job):
    """Return a job dict without the process object for JSON serialization."""
    return {
        "id": job["id"],
        "kind": job["kind"],
        "status": job["status"],
        "command": job["command"],
        "cwd": job["cwd"],
        "started_at": job["started_at"],
        "finished_at": job["finished_at"],
        "returncode": job["returncode"],
        "log": job["log"],
    }


def write_scrap_config(payload):
    parser = configparser.ConfigParser()
    parser.read(SCRAP_CONFIG)
    if not parser.has_section("Scraping"):
        parser.add_section("Scraping")
    if not parser.has_section("Output"):
        parser.add_section("Output")
    if not parser.has_section("Website"):
        parser.add_section("Website")
    if not parser.has_section("Weather"):
        parser.add_section("Weather")

    parser.set("Scraping", "start_date", str(payload.get("startDate", "")).strip())
    parser.set("Scraping", "end_date", str(payload.get("endDate", "")).strip())
    parser.set("Scraping", "years_back", str(payload.get("yearsBack", "10")).strip())
    parser.set("Scraping", "headless", str(payload.get("headless", "False")))
    parser.set("Scraping", "max_wait_time", str(payload.get("maxWaitTime", "15")).strip())
    parser.set("Output", "output_dir", str(RAW_OUTPUT_DIR))
    parser.set("Output", "save_formats", str(payload.get("saveFormats", "csv")).strip())
    parser.set("Output", "overwrite", str(payload.get("overwrite", "False")))
    parser.set("Website", "request_delay", str(payload.get("websiteDelay", "1.0")).strip())
    parser.set("Weather", "request_delay", str(payload.get("weatherDelay", "2.0")).strip())

    with SCRAP_CONFIG.open("w", encoding="utf-8") as handle:
        parser.write(handle)


def make_job(kind, command, cwd):
    job_id = str(uuid.uuid4())
    job = {
        "id": job_id,
        "kind": kind,
        "status": "queued",
        "command": command,
        "cwd": str(cwd),
        "started_at": time.time(),
        "finished_at": None,
        "returncode": None,
        "log": [],
        "process": None,
    }
    with JOBS_LOCK:
        JOBS[job_id] = job

    thread = threading.Thread(target=run_job, args=(job_id,), daemon=True)
    thread.start()
    return job


def run_job(job_id):
    with JOBS_LOCK:
        job = JOBS[job_id]
        job["status"] = "running"

    def set_log_line(text, line_index=None):
        with JOBS_LOCK:
            if line_index is not None and line_index < len(job["log"]):
                job["log"][line_index] = text
            else:
                job["log"].append(text)
                line_index = len(job["log"]) - 1
            if len(job["log"]) > 500:
                overflow = len(job["log"]) - 500
                job["log"] = job["log"][overflow:]
                line_index = max(line_index - overflow, 0)
            return line_index

    try:
        process = subprocess.Popen(
            job["command"],
            cwd=job["cwd"],
            stdout=subprocess.PIPE,
            stderr=subprocess.STDOUT,
            text=True,
            encoding="utf-8",
            errors="replace",
            bufsize=1,
        )
        with JOBS_LOCK:
            job["process"] = process
        assert process.stdout is not None

        pending = ""
        progress_line = None
        last_update = 0.0
        while True:
            char = process.stdout.read(1)
            if char == "" and process.poll() is not None:
                break
            if not char:
                continue

            if char == "\r":
                if pending:
                    progress_line = set_log_line(pending.rstrip(), progress_line)
                    pending = ""
                continue

            if char == "\n":
                if pending:
                    set_log_line(pending.rstrip(), progress_line)
                    pending = ""
                progress_line = None
                continue

            pending += char
            now = time.time()
            if now - last_update >= 0.25:
                progress_line = set_log_line(pending.rstrip(), progress_line)
                last_update = now

        if pending:
            set_log_line(pending.rstrip(), progress_line)
        returncode = process.wait()
        with JOBS_LOCK:
            job["returncode"] = returncode
            if job["status"] != "stopped":
                job["status"] = "completed" if returncode == 0 else "failed"
            job["finished_at"] = time.time()
    except Exception as exc:
        with JOBS_LOCK:
            if job["status"] != "stopped":
                job["status"] = "failed"
            job["finished_at"] = time.time()
            job["returncode"] = -1
            job["log"].append(f"Backend error: {exc}")


def validation_command(payload):
    city = str(payload.get("city") or "Barwala").strip()

    if city not in available_cities():
        raise ValueError(f"Unknown city '{city}'. Choose one of: {', '.join(available_cities())}")

    return [
        str(PYTHON_EXE),
        str(VALIDATION_SCRIPT),
        "--city",
        city,
    ]


def data_scrap_command():
    return [
        "powershell.exe",
        "-NoProfile",
        "-ExecutionPolicy",
        "Bypass",
        "-File",
        str(SCRAP_PIPELINE),
    ]


class AppHandler(BaseHTTPRequestHandler):
    server_version = "EggPriceApp/1.0"

    def send_json(self, payload, status=200):
        body = json.dumps(payload, indent=2).encode("utf-8")
        self.send_response(status)
        self.send_header("Content-Type", "application/json; charset=utf-8")
        self.send_header("Content-Length", str(len(body)))
        self.end_headers()
        self.wfile.write(body)

    def send_text(self, text, status=200):
        body = text.encode("utf-8")
        self.send_response(status)
        self.send_header("Content-Type", "text/plain; charset=utf-8")
        self.send_header("Content-Length", str(len(body)))
        self.end_headers()
        self.wfile.write(body)

    def do_GET(self):
        parsed = urlparse(self.path)
        path = unquote(parsed.path)

        if path == "/api/overview":
            self.send_json(
                {
                    "username": USERNAME,
                    "cities": available_cities(),
                    "metrics": read_metrics(),
                    "runSummary": read_run_summary(),
                    "scrapConfig": read_scrap_config(),
                    "charts": available_charts(),
                    "datasets": dataset_summary(),
                    "scrapFlow": [
                        "egg_scraper.py collects NECC egg prices with Selenium.",
                        "festival_generator.py creates India holiday/festival dates.",
                        "weather_scraper.py collects Open-Meteo temperature and rainfall.",
                        "feature_extraction.py merges price, weather, festival, lag, rolling, and calendar features.",
                    ],
                }
            )
            return

        if path.startswith("/api/jobs/"):
            job_id = path.rsplit("/", 1)[-1]
            with JOBS_LOCK:
                job = JOBS.get(job_id)
            if not job:
                self.send_json({"error": "Job not found"}, status=404)
                return
            self.send_json(job_for_json(job))
            return

        if path.startswith("/charts/"):
            self.serve_file(CHART_DIR, path.replace("/charts/", "", 1))
            return

        if path == "/":
            self.serve_file(WEB_ROOT, "index.html")
            return

        self.serve_file(WEB_ROOT, path.lstrip("/"))

    def do_POST(self):
        parsed = urlparse(self.path)
        path = parsed.path
        print(f"POST request to path: {path}", flush=True)
        
        # Handle stop endpoint first (before reading JSON body)
        if path.startswith("/api/jobs/") and path.endswith("/stop"):
            job_id = path.rsplit("/", 2)[1]
            print(f"Stop request for job {job_id}", flush=True)
            with JOBS_LOCK:
                job = JOBS.get(job_id)
            if not job:
                print(f"Job {job_id} not found", flush=True)
                self.send_json({"error": "Job not found"}, status=404)
                return
            process = job.get("process")
            print(f"Job status: {job['status']}, process: {process}", flush=True)
            if process and job["status"] == "running":
                try:
                    # Kill the process and its children
                    if process.poll() is None:  # Check if still running
                        print(f"Killing process {process.pid}", flush=True)
                        if os.name == 'nt':
                            # On Windows, use taskkill to kill the procs tree
                            import subprocess as sp
                            result = sp.run(["taskkill", "/PID", str(process.pid), "/T", "/F"], 
                                           capture_output=True, timeout=5, text=True)
                            print(f"Taskkill result: {result.returncode}, stdout: {result.stdout}, stderr: {result.stderr}", flush=True)
                        else:
                            # On Unix, terminate and then kill if needed
                            process.terminate()
                            try:
                                process.wait(timeout=3)
                            except subprocess.TimeoutExpired:
                                process.kill()
                    with JOBS_LOCK:
                        job["log"].append("Job terminated by user request")
                        job["status"] = "stopped"
                        job["returncode"] = process.poll()
                        job["finished_at"] = time.time()
                    print(f"Job {job_id} stopped successfully", flush=True)
                    self.send_json({"status": "stopped", "message": "Job has been stopped"})
                except Exception as exc:
                    print(f"Error stopping job {job_id}: {exc}", flush=True)
                    with JOBS_LOCK:
                        job["log"].append(f"Error stopping job: {exc}")
                    self.send_json({"error": str(exc)}, status=400)
            else:
                print(f"Job {job_id} is not running (status: {job['status'] if job else 'unknown'})", flush=True)
                self.send_json({"error": "Job is not running"}, status=400)
            return
        
        # Handle other endpoints
        try:
            payload = read_json_body(self)
            if path == "/api/validation/run":
                command = validation_command(payload)
                job = make_job("validation", command, PROJECT_ROOT)
                self.send_json(job_for_json(job), status=202)
                return

            if path == "/api/data-scrap/run":
                write_scrap_config(payload)
                command = data_scrap_command()
                job = make_job("data-scrap", command, PROJECT_ROOT)
                self.send_json(job_for_json(job), status=202)
                return

            self.send_json({"error": "Unknown endpoint"}, status=404)
        except Exception as exc:
            self.send_json({"error": str(exc)}, status=400)

    def serve_file(self, root, relative_path):
        root = root.resolve()
        target = (root / relative_path).resolve()
        if not str(target).startswith(str(root)) or not target.exists() or target.is_dir():
            self.send_text("Not found", status=404)
            return

        content_type = mimetypes.guess_type(str(target))[0] or "application/octet-stream"
        body = target.read_bytes()
        self.send_response(200)
        self.send_header("Content-Type", content_type)
        self.send_header("Content-Length", str(len(body)))
        self.end_headers()
        self.wfile.write(body)


def main():
    if not PYTHON_EXE.exists():
        raise FileNotFoundError(f"Virtualenv python not found: {PYTHON_EXE}")
    server = ThreadingHTTPServer(("127.0.0.1", 8080), AppHandler)
    print("Egg price web app running at http://127.0.0.1:8080", flush=True)
    server.serve_forever()


if __name__ == "__main__":
    main()
