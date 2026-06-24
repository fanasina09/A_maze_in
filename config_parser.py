#!/usr/bin/env python3
# ########################################################################### #
#   shebang: 1                                                                #
#                                                          :::      ::::::::  #
#   config_parser.py                                     :+:      :+:    :+:  #
#                                                      +:+ +:+         +:+    #
#   By: zo-rakot <zo-rakot@student.42antananarivo.   +#+  +:+       +#+       #
#                                                  +#+#+#+#+#+   +#+          #
#   Created: 2026/06/18 05:29:06 by zo-rakot            #+#    #+#            #
#   Updated: 2026/06/24 20:19:57 by zo-rakot           ###   ########.fr      #
#                                                                             #
# ########################################################################### #

#!/usr/bin/env python3

class ConfigParser:
    """Parse and validate maze configuration"""

    REQUIRE_KEYS = [
        "WIDTH",
        "HEIGHT",
        "ENTRY",
        "EXIT",
        "OUTPUT_FILE",
        "PERFECT"
    ]

    def __init__(self, filepath: str) -> None:
        self.filepath = filepath
        self.storage: dict = {}

    def parse_coord(self, value: str) -> tuple[int, int]:
        parts = value.split(",")

        if len(parts) != 2:
            raise ValueError(f"Invalid coord format: {value}")
        try:
            if not self.REQUIRE_KEYS:
                raise Exception("Error REQUIRE_KEY missing")
        except Exception as error:
            print(error)

        x, y = parts

        try:
            return int(x), int(y)
        except ValueError:
            raise ValueError(f"Invalid integer in coord: {value}")

    def validate(self) -> None:
        # check required keys
        for key in self.REQUIRE_KEYS:
            try:
                if key not in self.storage:
                    raise ValueError(f"Missing key: {key}")

            except ValueError as error:
                print(error)
                return (None)

        # bounds validation
        width = self.storage["WIDTH"]
        height = self.storage["HEIGHT"]

        entry_x, entry_y = self.storage["ENTRY"]
        exit_x, exit_y = self.storage["EXIT"]

        if not (0 <= entry_x < width and 0 <= entry_y < height):
            raise ValueError("ENTRY out of bounds")

        if not (0 <= exit_x < width and 0 <= exit_y < height):
            raise ValueError("EXIT out of bounds")

        if (entry_x, entry_y) == (exit_x, exit_y):
            raise ValueError("ENTRY and EXIT must be different")


    def parse_file(self) -> dict:
        try:
            with open(self.filepath, "r") as f:
                for line in f:
                    line = line.strip()

                    if not line or line.startswith("#"):
                        continue

                    if "=" not in line:
                        raise ValueError(f"Invalid line: {line}")

                    key, value = line.split("=", 1)
                    key = key.strip()
                    value = value.strip()

                    if key in ["WIDTH", "HEIGHT"]:
                        try:
                            self.storage[key] = int(value)
                        except ValueError:
                            raise ValueError(f"Invalid int for {key}: {value}")

                    elif key in ["ENTRY", "EXIT"]:
                        self.storage[key] = self.parse_coord(value)

                    elif key == "PERFECT":
                        self.storage[key] = value.lower() == "true"

                    else:
                        self.storage[key] = value

            self.validate()
            return self.storage

        except FileNotFoundError:
            raise FileNotFoundError("Config file not found")

