import json
import os
import subprocess
import threading
import webbrowser

from tabdeal.quickstart import (
    QuickstartError,
    app_home,
    example_script_path,
    generate_example_script,
    install_or_update_sdk,
    load_config,
    save_config,
    test_authenticated_connection,
    test_public_connection,
)


def load_tk():
    import tkinter as tk
    from tkinter import messagebox, ttk

    return tk, ttk, messagebox


class TabdealPanel(object):
    def __init__(self, root):
        self.tk, self.ttk, self.messagebox = load_tk()
        self.root = root
        self.root.title("Tabdeal Python Quickstart")
        self.root.geometry("860x640")
        self.root.minsize(760, 560)

        config = load_config()
        self.api_key_var = self.tk.StringVar(value=config.get("api_key", ""))
        self.api_secret_var = self.tk.StringVar(value=config.get("api_secret", ""))
        self.base_url_var = self.tk.StringVar(value=config.get("base_url", "https://api1.tabdeal.org"))
        self.market_var = self.tk.StringVar(value=config.get("market", "spot"))
        self.symbol_var = self.tk.StringVar(value=config.get("example_symbol", "BTC_IRT"))
        self.status_var = self.tk.StringVar(value="Ready")

        self._build_ui()
        self.log(
            "Panel ready.\n"
            "Credentials stay on this computer only.\n"
            "This helper does not perform real trading.\n"
            "Supported actions: install/update, public ping, account test, config save, example generation.\n"
            "Config folder: {config_dir}\n"
            "Example path: {example_path}".format(
                config_dir=app_home(),
                example_path=example_script_path(),
            )
        )

    def _build_ui(self):
        ttk = self.ttk

        self.root.columnconfigure(0, weight=1)
        self.root.rowconfigure(1, weight=1)

        header = ttk.Frame(self.root, padding=16)
        header.grid(row=0, column=0, sticky="ew")
        header.columnconfigure(0, weight=1)

        ttk.Label(
            header,
            text="Tabdeal Python Quickstart",
            font=("Segoe UI", 18, "bold"),
        ).grid(row=0, column=0, sticky="w")
        ttk.Label(
            header,
            text="Beginner-friendly installer and connection check for the SDK.",
        ).grid(row=1, column=0, sticky="w", pady=(6, 0))

        body = ttk.Panedwindow(self.root, orient="horizontal")
        body.grid(row=1, column=0, sticky="nsew", padx=16, pady=(0, 16))

        left = ttk.Frame(body, padding=12)
        right = ttk.Frame(body, padding=12)
        body.add(left, weight=2)
        body.add(right, weight=3)

        left.columnconfigure(1, weight=1)
        right.columnconfigure(0, weight=1)
        right.rowconfigure(1, weight=1)

        ttk.Label(left, text="Safety Notice", font=("Segoe UI", 11, "bold")).grid(
            row=0, column=0, columnspan=2, sticky="w", pady=(0, 8)
        )
        ttk.Label(
            left,
            text="Stores credentials locally only. No real trading is performed here.",
            foreground="#9c5a00",
            wraplength=320,
        ).grid(row=1, column=0, columnspan=2, sticky="w", pady=(0, 14))

        ttk.Label(left, text="Market").grid(row=2, column=0, sticky="w", pady=6)
        market_box = ttk.Combobox(
            left,
            textvariable=self.market_var,
            values=("spot", "future"),
            state="readonly",
        )
        market_box.grid(row=2, column=1, sticky="ew", pady=6)

        ttk.Label(left, text="Base URL").grid(row=3, column=0, sticky="w", pady=6)
        ttk.Entry(left, textvariable=self.base_url_var).grid(row=3, column=1, sticky="ew", pady=6)

        ttk.Label(left, text="API Key").grid(row=4, column=0, sticky="w", pady=6)
        ttk.Entry(left, textvariable=self.api_key_var).grid(row=4, column=1, sticky="ew", pady=6)

        ttk.Label(left, text="API Secret").grid(row=5, column=0, sticky="w", pady=6)
        ttk.Entry(left, textvariable=self.api_secret_var, show="*").grid(
            row=5, column=1, sticky="ew", pady=6
        )

        ttk.Label(left, text="Example Symbol").grid(row=6, column=0, sticky="w", pady=6)
        ttk.Entry(left, textvariable=self.symbol_var).grid(row=6, column=1, sticky="ew", pady=6)

        actions = ttk.LabelFrame(left, text="Actions", padding=12)
        actions.grid(row=7, column=0, columnspan=2, sticky="ew", pady=(16, 10))
        actions.columnconfigure(0, weight=1)
        actions.columnconfigure(1, weight=1)

        ttk.Button(actions, text="Install / Update SDK", command=self.install_sdk).grid(
            row=0, column=0, sticky="ew", padx=(0, 8), pady=6
        )
        ttk.Button(actions, text="Save Settings", command=self.save_settings).grid(
            row=0, column=1, sticky="ew", pady=6
        )
        ttk.Button(actions, text="Test Public Ping", command=self.test_ping).grid(
            row=1, column=0, sticky="ew", padx=(0, 8), pady=6
        )
        ttk.Button(actions, text="Test Account", command=self.test_account).grid(
            row=1, column=1, sticky="ew", pady=6
        )
        ttk.Button(actions, text="Generate Example", command=self.create_example).grid(
            row=2, column=0, sticky="ew", padx=(0, 8), pady=6
        )
        ttk.Button(actions, text="Open Config Folder", command=self.open_config_folder).grid(
            row=2, column=1, sticky="ew", pady=6
        )

        ttk.Button(
            left,
            text="Open Tabdeal Docs",
            command=lambda: webbrowser.open("https://docs.tabdeal.org"),
        ).grid(row=8, column=0, columnspan=2, sticky="ew", pady=(4, 12))

        ttk.Label(left, text="Status").grid(row=9, column=0, sticky="w")
        ttk.Label(left, textvariable=self.status_var).grid(row=9, column=1, sticky="w")

        ttk.Label(right, text="Activity Log", font=("Segoe UI", 12, "bold")).grid(
            row=0, column=0, sticky="w", pady=(0, 8)
        )
        self.log_widget = self.tk.Text(right, wrap="word", height=26)
        self.log_widget.grid(row=1, column=0, sticky="nsew")
        scrollbar = ttk.Scrollbar(right, orient="vertical", command=self.log_widget.yview)
        scrollbar.grid(row=1, column=1, sticky="ns")
        self.log_widget.configure(yscrollcommand=scrollbar.set)

    def current_config(self):
        return {
            "api_key": self.api_key_var.get().strip(),
            "api_secret": self.api_secret_var.get().strip(),
            "base_url": self.base_url_var.get().strip(),
            "market": self.market_var.get().strip(),
            "example_symbol": self.symbol_var.get().strip(),
        }

    def log(self, message):
        self.log_widget.insert(self.tk.END, message + "\n")
        self.log_widget.see(self.tk.END)

    def set_status(self, value):
        self.status_var.set(value)
        self.root.update_idletasks()

    def _queue_status(self, value):
        self.root.after(0, lambda: self.set_status(value))

    def _queue_log(self, message):
        self.root.after(0, lambda: self.log(message))

    def _queue_error(self, message):
        self.root.after(0, lambda: self.messagebox.showerror("Tabdeal Quickstart", message))

    def run_async(self, label, target):
        def runner():
            self._queue_status(label)
            try:
                target()
                self._queue_status("Ready")
            except Exception as exc:  # pragma: no cover
                self._queue_log("[ERROR] {0}".format(exc))
                self._queue_status("Error")
                self._queue_error(str(exc))

        thread = threading.Thread(target=runner, daemon=True)
        thread.start()

    def save_settings(self):
        path = save_config(self.current_config(), overwrite=True)
        self.log("Saved settings to {0}".format(path))
        self.set_status("Saved")

    def install_sdk(self):
        def work():
            result = install_or_update_sdk()
            self._queue_log("$ " + " ".join(result.command))
            self._queue_log(result.output or "(no output)")
            if result.returncode != 0:
                raise QuickstartError("SDK installation failed. See the activity log for details.")
            self._queue_log("SDK install/update completed successfully.")

        self.run_async("Installing", work)

    def test_ping(self):
        def work():
            self.save_settings()
            result = test_public_connection(self.current_config())
            self._queue_log("Public ping response:")
            self._queue_log(json.dumps(result, indent=2, ensure_ascii=False))

        self.run_async("Testing public ping", work)

    def test_account(self):
        def work():
            self.save_settings()
            result = test_authenticated_connection(self.current_config())
            self._queue_log("Authenticated account response:")
            self._queue_log(json.dumps(result, indent=2, ensure_ascii=False))

        self.run_async("Testing account", work)

    def create_example(self):
        path = generate_example_script(self.current_config(), overwrite=False)
        self.log("Generated example at {0}".format(path))
        self.set_status("Example generated")

    def open_config_folder(self):
        folder = app_home()
        folder.mkdir(parents=True, exist_ok=True)
        if os.name == "nt":
            os.startfile(str(folder))  # type: ignore[attr-defined]
        else:
            subprocess.run(["xdg-open", str(folder)], check=False)
        self.log("Opened config folder: {0}".format(folder))


def main():
    tk, ttk, _ = load_tk()
    root = tk.Tk()
    try:
        style = ttk.Style(root)
        if "clam" in style.theme_names():
            style.theme_use("clam")
    except Exception:
        pass
    TabdealPanel(root)
    root.mainloop()
