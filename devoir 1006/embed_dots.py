# EX6
import argparse
import sys


"""
Embed yellow dots matrix into an existing BMP image.

Takes an input BMP image (300x200) and embeds the Abracadabra Laser Jet Pro
yellow dots pattern encoding date/time, serial number, and username.

The yellow dot matrix is 22x8 pixels and is placed with its top-left corner
at coordinate (30, 160) in the image.

Format:
  - Columns 1, 7, 14, 21: separators (0xFF) done!
  - Columns 2-6: date/time (minute, hour, day, month, year)
  - Columns 8-13: printer serial number (6 ASCII chars)
  - Columns 15-20: username (6 ASCII chars)
  - Column 22: parity (XOR of each row across data columns)

Usage:
    python3 embed_dots.py "DD/MM/YYYY HH:MM" "SERIAL" "USER00" input.bmp output.bmp
"""


from PIL import Image

def yellow_laser_ember(img, minute: int, hour: int, day: int, month: int, year: int, 
         serial: str, username: str) -> None:
    """Draw yellow dots matrix with encoded data."""
    (width, height) = (30, 160) # starting point
    
    # Separators at columns 1, 7, 14, 21, if the starting index is 0 then 1 is 0 ?
    dx = [0, 6, 13, 20]
    for x in dx:
        for y in range(8):
            img.putpixel((width + x, height + y), (255, 255, 0))
    
    datetime_values = [minute, hour, day, month, year]
    for i in range(len(datetime_values)): # I could use enumerate but this is more clear for me 
        value = datetime_values[i]
        col = 1 + i  # columns 1 to 5, same question in code-line 35
        for j in range(8):
            if value & (2**j): # 2**j values in binary are: [01,10,100,...], so this if function checks for every 1 in the "value" binary 
                # & is just an and for binaries
                img.putpixel((width + col, height + j), (255, 255, 0))
    # serial
    for i in range(6):
        col = 7 + i  # columns 7 to 12 
        char_code = ord(serial[i])
        for j in range(8):
            if char_code & (2**j):
                img.putpixel((width + col, height + j), (255, 255, 0))
    
    # username 
    for i in range(6):
        col = 14 + i  # columns 14 to 19 
        char_code = ord(username[i])
        for j in range(8):
            if char_code & (2**j):
                img.putpixel((width + col, height + j), (255, 255, 0))
    
    # parity
    for row in range(8):
        parity = 1
        check = 2**row  
        for col in range(1, 20):
            if col != 6 and col != 13: # exclude the separators columns
                # Check if pixel is set
                if (col == 1 and (minute & (check))) or \
                (col == 2 and (hour & (check))) or \
                (col == 3 and (day & (check))) or \
                (col == 4 and (month & (check))) or \
                (col == 5 and (year & (check))) or \
                (col in [7, 8, 9, 10, 11, 12] and (ord(serial[col - 7]) & (check))) or \
                (col in [14, 15, 16, 17, 18, 19] and (ord(username[col - 14]) & (check))):
                    parity ^= 1 # toggles between 0 and 1 if the current column is activated
        if parity:
            img.putpixel((width + 21, height + row), (255, 255, 0)) # yellow if the number of the active columns is pair? idk if it should be pair or odd
        for i in range(22):
            for j in range(8):
                if img.getpixel([width + i, height + j]) != (255, 255, 0):
                    img.putpixel((width + i, height + j), (255, 255, 1))
                

def validate_serial(value: str) -> str:
    """Validate that serial is exactly 6 printable ASCII characters."""
    if len(value) != 6:
        raise argparse.ArgumentTypeError(
            f"serial must be exactly 6 characters (got {len(value)})"
        )
    for ch in value:
        if not (32 <= ord(ch) <= 126):
            raise argparse.ArgumentTypeError(
                f"serial contains non-printable ASCII character: {ch!r}"
            )
    return value


def validate_username(value: str) -> str:
    """Validate that username is exactly 6 printable ASCII characters."""
    if len(value) != 6:
        raise argparse.ArgumentTypeError(
            f"username must be exactly 6 characters (got {len(value)})"
        )
    for ch in value:
        if not (32 <= ord(ch) <= 126):
            raise argparse.ArgumentTypeError(
                f"username contains non-printable ASCII character: {ch!r}"
            )
    return value


def validate_datetime(value: str):
    """Parse and validate datetime string, returning (minute, hour, day, month, year)."""
    try:
        date_part, time_part = value.split(" ")
        day, month, year_full = date_part.split("/")
        hour, minute = time_part.split(":")
        day, month, year_full = int(day), int(month), int(year_full)
        hour, minute = int(hour), int(minute)
        year = year_full % 100  # Keep only last 2 digits
    except ValueError:
        raise argparse.ArgumentTypeError("date/time format must be DD/MM/YYYY HH:MM")

    # Validate ranges
    if not (0 <= minute <= 59):
        raise argparse.ArgumentTypeError(f"minute {minute} out of range (0-59)")
    if not (0 <= hour <= 23):
        raise argparse.ArgumentTypeError(f"hour {hour} out of range (0-23)")
    if not (1 <= day <= 31):
        raise argparse.ArgumentTypeError(f"day {day} out of range (1-31)")
    if not (1 <= month <= 12):
        raise argparse.ArgumentTypeError(f"month {month} out of range (1-12)")

    return minute, hour, day, month, year

def parse_args() -> argparse.Namespace:
    """Parse command-line arguments using argparse."""
    parser = argparse.ArgumentParser(
        description="Embed yellow dots matrix into an existing BMP image.",
        epilog='Example: python3 embed_dots.py "15/11/2025 14:42" "S3CUR3" "R3MI_X" belgian_flag.bmp output.bmp',
    )

    parser.add_argument(
        "datetime",
        type=validate_datetime,
        metavar="DATETIME",
        help='Date and time in format "DD/MM/YYYY HH:MM"',
    )
    parser.add_argument(
        "serial",
        type=validate_serial,
        metavar="SERIAL",
        help="Printer serial number (exactly 6 ASCII characters)",
    )
    parser.add_argument(
        "username",
        type=validate_username,
        metavar="USERNAME",
        help="Username (exactly 6 ASCII characters)",
    )
    parser.add_argument(
        "input",
        metavar="INPUT_BMP",
        help="Input BMP image file (300x200 pixels)",
    )
    parser.add_argument(
        "output",
        metavar="OUTPUT_BMP",
        help="Output BMP image file",
    )

    return parser.parse_args()


def main():
    args = parse_args()
    minute, hour, day, month, year = args.datetime
    
    img = Image.open(args.input)
    yellow_laser_ember(img, minute, hour, day, month, year, args.serial, args.username)
    img.save(args.output)

if __name__ == "__main__":
    main()
