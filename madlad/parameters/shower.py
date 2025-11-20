import os
import warnings

from typing import Dict, Set
from omegaconf import DictConfig


def edit_shower(cfg: DictConfig) -> None:
    """Edit `run_card.dat` under the MadGraph process path :obj:`process_dir`.
    
    Args:
        process_dir (optional: str): aMC process directory.
        settings (optional: madlad.utils.config): settings.
    """
    save_dir = cfg['gen']['block_model']['save_dir']
    order = cfg['gen']['block_model']['order'].lower()

    def card_paths(order: str, base: str):
        if order == "nlo":
            return (
                os.path.join(base, "Cards", "shower_card_default.dat"),
                os.path.join(base, "Cards", "shower_card.dat"),
            )
        return (
            os.path.join(base, "Cards", "pythia8_card_default.dat"),
            os.path.join(base, "Cards", "pythia8_card.dat"),
        )

    default_path, new_path = card_paths(order, save_dir)

    comment_symbol = "#" if order == "nlo" else "!"

    try:
        raw_settings = cfg["gen"]["block_shower"]["settings"]
        settings: Dict[str, object] = {
            k.lower(): v for k, v in raw_settings.items()
        }
    except Exception:
        settings = {}

    used: Set[str] = set()

    with open(default_path) as default_card, open(new_path, "w") as new_card:
        for line in default_card:
            # Preserve comments and blank lines
            if not line.strip() or line.lstrip().startswith(comment_symbol):
                new_card.write(line)
                continue

            if "=" not in line:
                new_card.write(line)
                continue

            setting, rest = line.split("=", 1)
            key = setting.strip().lower()
            value = rest.rstrip("\n")

            if key in settings:
                val = settings[key]
                used.add(key)
                if val is None:          # remove the line
                    print(f"Removing {key}.")
                    continue
                new_card.write(f"{setting} = {val}\n")
                print(f"Setting {key} = {val}.")
            else:
                new_card.write(line)

        for key, val in settings.items():
                if key in used or val is None:
                    continue
                warnings.warn(
                    f"Option {key} was not in the default shower_card. "
                    f"Adding by hand a setting to {val}"
                )
                new_card.write(f"{key} = {val}\n")

        for block_name in ("misc",):
            block = cfg["gen"]["block_shower"].get(block_name, [])
            for entry in block:
                print(f"Writing {block_name}: {entry}")
                new_card.write(f"{entry}\n")

    print("Finished modification of shower card.")